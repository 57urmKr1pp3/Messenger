LENGTH_HEADER_SIZE = 8
TYPE_HEADER_SIZE = 3
USER_HEADER_SIZE = 16
ADDRESSING_HEADER_SIZE = 21
def format_message(type, username, message, adressierung):
    if not message:
        return None
    #user_header = str(username)
    Type_header = f'{type}:<{TYPE_HEADER_SIZE}'
    length_header = f'{len(message):<{LENGTH_HEADER_SIZE}}'
    user_header = f'{username:<{USER_HEADER_SIZE}}'
    adressing = f'{adressierung:<{ADDRESSING_HEADER_SIZE}}'
    return f'{Type_header}{adressing}{length_header}{user_header}{message}'