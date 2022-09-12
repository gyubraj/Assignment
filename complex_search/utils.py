
import re
from datetime import date

from django.db.models import Q

from complex_search.models import Student

def applyOp(a, b, op):
    """
    Will return Q EXpression by combining multiple Q and Operator
    """
    if op == 'AND': return a & b
    if op == 'OR': return a | b


def convert_value(column, value):
    """ Will return value according to Student model Field """

    column_type = Student._meta.get_field(column).__class__.__name__

    if column_type == "DateField":
        return date(*map(int, value.split('-')))

    elif column_type == "CharField":
        return value
    
    elif column_type == "IntegerField":
        return int(value)


def parse_search_phrase(allowed_list : list[str],string_query: str):

    # replace multiple space with single space
    string_query = re.sub(' +',' ',string_query)

    # Operators that is supported in search
    operators = [' eq', ' ne', ' gt', ' lt']

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
            opertaor = split_query.pop(0)
            value = split_query.pop(0)
            if opertaor == 'eq':
                condition = {
                    field : convert_value(field, value)
                }
                query_list.append(Q(**condition))
            
            elif opertaor == 'ne':
                condition = {
                    field : convert_value(field, value)
                }
                query_list.append(~Q(**condition))
            
            elif opertaor == 'gt':
                check = field + "__gt"
                condition = {
                    check: convert_value(field, value)
                }
                query_list.append(Q( **condition))
            
            elif opertaor == 'lt':
                check = field + "__lt"
                condition = {
                    check: convert_value(field, value)
                }
                query_list.append(Q(**condition))

        elif split_query[0] == ")":
            while len(ops) != 0 and ops[-1] != '(':
                val2 = query_list.pop()
                val1 = query_list.pop()
                op = ops.pop()
                
                query_list.append(applyOp(val1, val2, op))
            # pop opening brace.
            ops.pop()
            split_query.pop(0)
        
        else: 
            ops.append(split_query.pop(0))

    while len(ops) != 0:
        
        val2 = query_list.pop()
        val1 = query_list.pop()
        op = ops.pop()
                
        query_list.append(applyOp(val1, val2, op))

    return query_list[-1]

