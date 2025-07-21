""" copy_text_file_using_tcl.py """

import re
import os


def copy_text_file_using_tcl(file_name:str):
    terminal_width = 20
    path = os.path.normpath(file_name)

    tcl_cmd = list()
    tcl_cmd.append('tclsh')
    tcl_cmd.append('set file [open "bootflash:%s" w]' % path.split(os.sep)[-1])

    line_remainder = str()

    with open(file_name, 'r') as file_pointer:
        for line in file_pointer:
            line = line_remainder + line
            line_remainder = ''

            if len(line) > terminal_width:
                for i in range(0, len(line), terminal_width):
                    split_line = line[i:i + terminal_width]
                    if len(split_line) == terminal_width:
                        tcl_cmd.append(format_using_tcl(split_line))
                    else:
                        line_remainder = line_remainder + split_line
            else:
                line_remainder = line_remainder + line

        tcl_cmd.append(format_using_tcl(line_remainder))
        tcl_cmd.append('exit')

        return tcl_cmd


def quote_special_characters(string):
    string = repr(string)  # Displays special characters as a string literals
    string = re.sub("(^'|'$)|(^\"|\"$)", "", string)  # Remove quotes surrounding the string
    string = re.sub("\"", "\\\"", string)  # Quote double brackets
    string = re.sub("{", "\\{", string)  # Quote curly braces
    string = re.sub("}", "\\}", string)  # Quote curly braces
    string = re.sub("\[", "\\\[", string)  # Quote square brackets
    string = re.sub("\]", "\\\]", string)  # Quote square brackets
    string = re.sub("\$", "\\$", string)  # Quote dollar signs
    string = re.sub("\?", r'\\077', string)  # Convert question mark to ASCII Key Code
    return string


def format_using_tcl(string):
    string = quote_special_characters(string)
    return 'puts -nonewline $file "%s"' % string


if __name__ == '__main__':
    
    for command in copy_text_file_using_tcl(input("Insert the path of the file to copy:")):
        print(command)




