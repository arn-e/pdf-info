import os
import codecs, sys
import re
import pyodbc
from glob import glob as __g
from re import search as __s
from pyPdf import PdfFileReader

#import numpy
print "PDF Page Counter"
#Establish SQL Connection
cnxn = pyodbc.connect("DSN=odbc-af_sqlserver")
cursor = cnxn.cursor()
cursor.tables()
print "Establishing SQL Connection : odbc-af_sqlserver"

#Gather user input
sql_table_input = raw_input('SQL Table[s] : ')
print_destination = raw_input ('Output Directory : ')
#Set printfile
printfile = open(print_destination+'/'+'RESULTS.txt', 'w')

#<Modules>
#line check routine
def check_sql_input (check_line):
    if check_line.find(';'):
        delim_count = len(re.findall(';',check_line))
        check_line = check_line.replace(';', ' ')
        check_line = check_line.split()
        num_tables = delim_count + 1
        i_tables = 0
        table_list = list()
        while i_tables < num_tables:
            table_list.append(check_line[i_tables])
            i_tables = i_tables + 1
    return table_list

#query execution routine
def sql_execute (list_of_tables, number_of_tables) :
    i_tbl = 0
    full_list = list()
    batch_list = list()
    fext_list = list()
    docno_list = list()
    relpath_list = list()
    uuid_list = list()
    revstatus_list = list()
    pgcount_list = list()
    textpath_list = list()
    i_append = 0
    while i_tbl < number_of_tables :
        cursor.execute \
            (\
                "select FIELD1, FIELD2, FIELD3, FIELD4, FIELD5, FIELD6, FIELD7 from " \
                + str(list_of_tables[i_tbl]) + \
                " where #CRITERIA#"
            )
        for row in cursor :
            batch_list.append(str(row.BATCH))
            docno_list.append(str(row.DOCNO))
            fext_list.append(str(row.FEXT))
            uuid_list.append(str(row.UUID))
            relpath_list.append(str(row.RELPATH))
            revstatus_list.append(str(row.REVREVIEWSTATUS))
            pgcount_list.append(str(row.PGCOUNT))
        i_tbl = i_tbl + 1
    full_list = [FIELD1, FIELD2, FIELD3, FIELD4, FIELD5, FIELD6, FIELD7]
    return full_list

#read PDF routine
def read_pdf (file_to_read):
    to_return = []
    vPDFfile = file_to_read
    vPages = 0
    test_p = 0
    stripped = []
    vFileOpen = open(vPDFfile, 'rb', 1)
    read_array = vFileOpen.readlines()
    header_sample = read_array[0][0:10]
    print "Header Sample " + str(header_sample)
    print >> printfile, "Header Sample " + str(header_sample)
    if "1.4" in header_sample :
        vFileOpen.close()
        file_lib_open = PdfFileReader(file(file_to_read, 'rb'))
        vPages = file_lib_open.getNumPages()
        #file_lib_open.close()
    else :
        for vLine in read_array:
            if "/Count" in vLine :
                vPages = int( __s("/Count \d*", vLine).group()[7:] )
                print vPages
        vFileOpen.close()
    to_return = [file_to_read, vPages]
    return to_return

#Sequence of Operations :

#1 - verify user input [SQL tables]
#Same as text reader
print "Parsing User Table Input"
check_line = sql_table_input
table_list = check_sql_input(check_line)
table_count = len(table_list)

#2 - gather columns from SQL
#divergent
print "Running Query"
list_of_tables = table_list
number_of_tables = table_count
run_array = sql_execute(list_of_tables, number_of_tables)
cnxn.close()
print "Closing SQL Connection"

#3 read text
array_to_read = run_array
text_row = 4
arr_len = len(array_to_read[1])

print_array = []
while i < arr_len :
    file_to_read = array_to_read[4][i]
    file_to_read = "/Users/arne/myOutputDirectory" + str(file_to_read)
    print "Reading File : " + str(file_to_read)
    read_results = read_pdf(file_to_read)
    print_array.append(read_results)
    #print print_array[i]
    print_array[i].append(array_to_read[0][i])
    print_array[i].append(array_to_read[1][i])
    print_array[i].append(array_to_read[5][i])
    print_array[i].append(array_to_read[6][i])
    print print_array[i]
    print >> printfile, print_array[i]
    i = i + 1

printfile.close()






