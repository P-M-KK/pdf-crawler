""" Gets PDF links """



# Imports

import sys
import urllib.parse
import os.path
import PyPDF2



# Constants

KEY = '/Annots'
URI = '/URI'
ANK = '/A'



# Globals

global_set_links_pdf = set()
global_indent = -1



# Functions

def get_links(path):
    """ Print all links from a PDF and recurse into linked PDFs. """
    global global_set_links_pdf, global_indent

    if path.endswith('.PDF'):
        global_set_links_pdf.add(path)
        local_set_links = set()


        # Read all links from a PDF

        file_handle = open(path, 'rb')

        pdf = PyPDF2.PdfFileReader(file_handle)
        pages = pdf.getNumPages()

        for page_number in range(pages):
            page = pdf.getPage(page_number)
            page_object = page.getObject()

            if KEY in page_object:
                annotations = page_object[KEY]

                for annotation in annotations:
                    uri = annotation.getObject()

                    if URI in uri[ANK]:
                        local_set_links.add(
                            os.path.normpath(urllib.parse.unquote(uri[ANK][URI].strip().upper()))
                        )

        file_handle.close() # Close file before recursion to avoid expending OS file handles


        # Print all links from a PDF

        global_indent += 1

        for link in local_set_links:
            print((global_indent * ' ') + path + ' -> ' + link)

            if link not in global_set_links_pdf:
                get_links(link) # Recurse into linked PDFs

        global_indent -= 1

        #print(local_set_links)



# Main

def main():
    """ Main """
    if len(sys.argv) > 1:
        get_links(os.path.normpath(urllib.parse.unquote(sys.argv[1].strip().upper())))
        #print(global_set_links)
    else:
        print('Include a path to the root/first PDF.')

if __name__ == "__main__":
    main()
