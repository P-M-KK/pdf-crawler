""" ... """



# Imports

import sys
import urllib.parse
import os.path
import PyPDF2



# Globals

global_set_refs_pdf = set()
global_indent = 0



# Functions

def gogo(path):
    """ ... """

    file_handle = open(path, 'rb')

    pdf = PyPDF2.PdfFileReader(file_handle)
    pages = pdf.getNumPages()

    for page_number in range(pages):
        go(pdf.getPage(page_number))

def go(obj):
    """ ... """
    global global_set_refs_pdf, global_indent

    global_indent += 1

    orig = None
    if str(obj).startswith('IndirectObject'):
        orig = str(obj)
        obj = obj.getObject()
    
    if isinstance(obj, dict):
        if orig:
            if orig in global_set_refs_pdf:
                pass
            else:
                global_set_refs_pdf.add(orig)
                for key in obj:
                    global_indent += 1
                    print((global_indent * ' ') + 'Key: ' + str(key))
                    go(obj[key])
                    global_indent -= 1
        else:
            for key in obj:
                global_indent += 1
                print((global_indent * ' ') + 'Key: ' + str(key))
                go(obj[key])
                global_indent -= 1
    elif not isinstance(obj, str) and (isinstance(obj, list) or isinstance(obj, set) or isinstance(obj, tuple)):
        if orig:
            if orig in global_set_refs_pdf:
                pass
            else:
                global_set_refs_pdf.add(orig)
                for o in obj:
                    go(o)
        else:
            for o in obj:
                go(o)
    else:
        print((global_indent * ' ') + 'Val: ' + str(obj))

    global_indent -= 1



# Main

def main():
    """ Main """
    if len(sys.argv) > 1:
        gogo(os.path.normpath(urllib.parse.unquote(sys.argv[1].strip().upper())))
    else:
        print('Include a path to the root/first PDF.')

if __name__ == "__main__":
    main()
