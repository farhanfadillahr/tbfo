rules = [
    (r'function\s', 'FUNCTION'),
    (r'\/\/.*', 'COMMENT'),
    ('\".*\"', 'STRING'),
    ('\'.*\'', 'STRING'),
    (r'{', 'OPENCURLY'),
    (r'\n\{', 'OPENCURLY'),
    (r'\n\{\n', 'OPENCURLY'),
    (r'\}', 'CLOSECURLY'),
    (r';', 'SEMICOLON'),
    (r'\n', 'NEWLINE'),
    (r'\s', 'WHITESPACE'),
    (r'\d+','NUMBER'),
    (r'\d+.+\d','FLOAT'),
    (r'[a-zA-Z_]+[\da-zA-Z_0-9]*','IDENTIFIER'),
    (r'\(','LP'),
    (r'\)','RP'),
    (r'\)\n','RP NEWLINE'),

    # random case
    (r'\w', 'NULL'),
]