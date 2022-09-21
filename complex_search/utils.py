"""Utils function to return Model objects from string search"""
import re
from datetime import date

from django.db.models import Q

from complex_search.models import Student


def apply_boolean_operator(first_q: Q, second_q: Q, operator: str) -> Q | Exception:
    """Will return Q Expression by combining two Q objects with given Operator"""

    if operator == "AND":
        return first_q & second_q

    elif operator == "OR":
        return first_q | second_q

    else:
        raise Exception(f"{operator} is not supported currently.")


def convert_value(column: str, value: str) -> str | date | int:
    """Will return value according to Student model Field"""

    column_type = Student._meta.get_field(column).__class__.__name__

    if column_type == "DateField":
        return date(*map(int, value.split("-")))

    elif column_type == "CharField":
        return value

    elif column_type == "IntegerField":
        return int(value)


def string_to_q(field: str, operator: str, value: str) -> Q | Exception:
    """Converts serach string of form field op value into Q object"""
    if operator == "eq":
        return Q(**{field: convert_value(field, value)})

    elif operator == "ne":
        return Q(**{field: convert_value(field, value)})

    elif operator == "gt":
        check = field + "__gt"
        return Q(**{check: convert_value(field, value)})

    elif operator == "lt":
        check = field + "__lt"
        return Q(**{check: convert_value(field, value)})

    else:
        raise Exception("Not supported Operator in the string query.")


def parse_search_phrase(
    allowed_list: list[str], string_query: str
) -> Exception | None | Q:

    # replace multiple space with single space
    string_query = re.sub(" +", " ", string_query)

    # Operators that is supported in search
    operators = [" eq", " ne", " gt", " lt"]

    # regular expresiion to get field values from query
    pattern = rf'(\w+)\s*(?:\b(?:{"|".join(operators)})\b)'

    # Gives all fields that is used in the query
    fields = set(re.findall(pattern, string_query))

    # Model Fields Name
    model_fields = set(f.name for f in Student._meta.get_fields())

    # Check for only allowed Fields and Model Fields
    if not set(fields).issubset(set(allowed_list)):
        raise Exception("Contian Unallowed Fields")

    elif not set(fields).issubset(model_fields):
        raise Exception("Contain fields that are not in Model")

    # Create a list of field, values and opertaors
    split_query = string_query.split()

    # will be used to store Q objects
    query_list = []

    # will be used to store opertaors ( AND, OR )
    ops = []

    while split_query:

        if split_query[0] in fields:
            field = split_query.pop(0)
            operator = split_query.pop(0)
            value = split_query.pop(0)
            query_list.append(string_to_q(field, operator, value))

        elif split_query[0] == ")":
            while len(ops) != 0 and ops[-1] != "(":
                second_q = query_list.pop()
                first_q = query_list.pop()
                op = ops.pop()
                query_list.append(apply_boolean_operator(first_q, second_q, op))

            # pop opening brace from ops and closing brace from split_query.
            ops.pop()
            split_query.pop(0)

        else:
            """append OR, AND or braces into ops stack"""
            ops.append(split_query.pop(0))

    while len(ops) != 0:
        second_q = query_list.pop()
        first_q = query_list.pop()
        op = ops.pop()

        query_list.append(apply_boolean_operator(first_q, second_q, op))

    return query_list[-1]
