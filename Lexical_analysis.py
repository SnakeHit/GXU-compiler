import sys

KEYWORD_LIST = [
    "if",
    "else",
    "while",
    "break",
    "continue",
    "for",
    "double",
    "int",
    "float",
    "long",
    "short",
    "switch",
    "case",
    "return",
    "void",
    "printf"
    "scanf",
    "do",
    "int26",
    "struct",
    "char*"
]

SEPARATOR_LIST = ["{", "}", "[", "]", "(", ")", "~", ",", ";", ".", "?", ":"]

OPERATOR_LIST = [
    "+",
    "++",
    "-",
    "--",
    "+=",
    "-=",
    "*",
    "*=",
    "%",
    "%=",
    "->",
    "|",
    "||",
    "|=",
    "/",
    "/=",
    ">",
    "<",
    ">=",
    "<=",
    "=",
    "==",
    "!=",
    "!",
]

CATEGORY_DICT = {
    "double": 10,
    "int": 11,
    "break": 12,
    "else": 13,
    "switch": 14,
    "case": 15,
    "char": 16,
    "return": 17,
    "float": 18,
    "continue": 19,
    "for":  20,
    "void": 21,
    "do": 22,
    "if": 23,
    "while": 24,
    "static": 25,
    "{": 29,
    "}": 30,
    "[": 31,
    "]": 32,
    "(": 33,
    ")": 34,
    "~": 35,
    ",": 36,
    ";": 37,
    "?": 38,
    ":": 39,
    "<": 40,
    "<=": 41,
    ">": 42,
    ">=": 43,
    "=": 44,
    "==": 45,
    "|": 46,
    "||": 47,
    "|=": 48,
    "^": 49,
    "^=": 50,
    "&": 51,
    "&&": 52,
    "&=": 53,
    "%": 54,
    "%=": 55,
    "+": 56,
    "++": 57,
    "+=": 58,
    "-": 59,
    "--": 60,
    "-=": 61,
    "->": 62,
    "/": 63,
    "/=": 64,
    "*": 65,
    "*=": 66,
    "!": 67,
    "!=": 68,
    "ID": 70,
    "INT": 71,
    "FLOAT": 72,
    "STRING": 73,
    "OP":74,
    "printf":75,
    "scanf":76,
    "int26":77,
    "struct":88,
    ".":89,
    "structID":90,
    "char*":91
}

current_row = -1
current_line = 0
input_str = []


def is_keyword(s):
    return s in KEYWORD_LIST


def is_separator(s):
    return s in SEPARATOR_LIST


def is_operator(s):
    return s in OPERATOR_LIST


def get_cate_id(s):
    return CATEGORY_DICT[s]


def getchar():
    global current_row
    global current_line
    current_row += 1

    if current_row == len(input_str[current_line]):
        current_line += 1
        current_row = 0

    if current_line == len(input_str):
        return "SCANEOF"

    return input_str[current_line][current_row]


def ungetc():
    global current_row
    global current_line
    current_row = current_row - 1
    if current_row < 0:
        current_line = current_line - 1
        current_row = len(input_str[current_row]) - 1
    return input_str[current_line][current_row]


def read_source_file(file):
    global input_str
    f = open(file, "r")
    input_str = f.readlines()
    input_str = input_str[1:]
    f.close()


def lexical_error(msg, line=None, row=None):
    if line is None:
        line = current_line + 1
    if row is None:
        row = current_row + 1
    print(str(line) + ":" + str(row) + " Lexical error: " + msg)


def scanner():
    current_char = getchar()
    if current_char == "SCANEOF":
        return ("SCANEOF", "", "")
    if current_char.strip() == "":
        return
    if current_char.isdigit():
        int_value = 0
        while current_char.isdigit():
            int_value = int_value * 10 + int(current_char)
            current_char = getchar()

        if current_char != ".":
            ungetc()
            return ("INT", int_value, get_cate_id("INT"))

        float_value = str(int_value) + "."
        current_char = getchar()
        while current_char.isdigit():
            float_value += current_char
            current_char = getchar()
        ungetc()
        return ("FLOAT", int(eval(float_value)), get_cate_id("FLOAT"))
    if current_char.isalpha() or current_char == "_" or current_char == "." or current_char == "*":
        string = ""
        while current_char.isalpha() or current_char.isdigit() or current_char == "_"or current_char == "." or current_char == "*":
            string += current_char
            current_char = getchar()
            if current_char == "SCANEOF":
                break

        ungetc()
        if is_keyword(string):
            return (string, "", get_cate_id(string))
        elif result[-1][0] == "struct": # a.b
            return ("structID", string, get_cate_id("structID"))
        else:
            for i in result:
                if i[0] == "structID":
                    if i[1] == string:
                        return ("structID", string, get_cate_id("structID"))
            return ("ID", string.replace('.',''), get_cate_id("ID"))

    if current_char == '"':
        str_literal = ""
        global current_line
        global current_row
        line = current_line + 1
        row = current_row + 1

        current_char = getchar()
        while current_char != '"':
            str_literal += current_char
            current_char = getchar()
            if current_char == "SCANEOF":
                lexical_error('missing terminating "', line, row)

                current_line = line
                current_row = row
                return ("SCANEOF", "", "")
        return ("STRING", str_literal, get_cate_id("STRING"))

    if current_char == "/":
        next_char = getchar()
        line = int(current_line) + 1
        row = int(current_row) + 1
        if next_char == "*":
            comment = ""
            next_char = getchar()
            while True:
                if next_char == "SCANEOF":
                    lexical_error("unteminated /* comment", line, row)
                    return ("SCANEOF", "", "")
                if next_char == "*":
                    end_char = getchar()
                    if end_char == "/":
                        # Comment, return None to ignore it.
                        return None
                    if end_char == "SCANEOF":
                        lexical_error("unteminated /* comment", line, row)
                        return ("SCANEOF", "", "")
                comment += next_char
                next_char = getchar()
        elif next_char == "/":
            current_row = len(input_str[current_line]) - 1
            return None
        else:
            ungetc()
            op = current_char
            current_char = getchar()
            if is_operator(current_char):
                op += current_char
            else:
                ungetc()
            return ("OP", op, get_cate_id(op))

    if is_separator(current_char):
        return ("SEP", current_char, get_cate_id(current_char))

    if is_operator(current_char):
        op = current_char
        current_char = getchar()
        if is_operator(current_char):
            op += current_char
        else:
            ungetc()
        return ("OP", op, get_cate_id(op))
    else:
        lexical_error("unknown character: " + current_char)


def main():
    file_name = "Code.txt"
    read_source_file(file_name)
    global result
    result = []
    while True:
        r = scanner()
        if r is not None:
            if r[0] == "SCANEOF":
                break
            result += [r]
    result += ["#"]
    print(result)

    return result

if __name__ == "__main__":
    main()