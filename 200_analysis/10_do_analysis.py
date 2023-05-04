#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re

# ###########################################################################
# METHODS
# ###########################################################################
def sanitize(entry, DEBUG):
    if DEBUG:
        print(entry)
    entry = entry.upper()

    entry = ''.join(i for i in entry if not i.isdigit())

    entry = entry.replace("\n", " ")

    entry = entry.replace("‘", "")
    entry = entry.replace("'", "")
    entry = entry.replace('"', '')
    entry = entry.replace('`', '')
    entry = entry.replace(",", "")
    entry = entry.replace(".", "")
    entry = entry.replace(":", "")
    entry = entry.replace(";", "")
    entry = entry.replace("(", "")
    entry = entry.replace(")", "")
    entry = entry.replace("[", "")
    entry = entry.replace("]", "")
    entry = entry.replace("%", "")
    entry = entry.replace("-", "")
    entry = entry.replace("$", "")
    entry = entry.replace("*", "")    
    entry = entry.replace("_", "")

    # entry = ' '.join(entry.split())
    entry = entry.replace("    ", " ")
    entry = entry.replace("   ", " ")
    entry = entry.replace("  ", " ")

    if DEBUG:
        print(entry)

    return entry

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_file_name, output_file_name):
    count = {}
    count['RegulatoryOperators'] = 0
    count['Operators'] = 0
    count['Operands'] = 0

    unique = {}
    unique['RegulatoryOperators'] = 0
    unique['Operators'] = 0
    unique['Operands'] = 0

    total_words = 0

    RegulatoryOperators = []
    input_file = open("../020_word_lists/RegulatoryOperators_sorted.csv", encoding='utf-8')
    for line in input_file.readlines():
        RegulatoryOperators.append(sanitize(line.strip(), False))

    Operators = []
    input_file = open("../020_word_lists/Operators_sorted.csv", encoding='utf-8')
    for line in input_file.readlines():
        Operators.append(sanitize(line.strip(), False))

    Operands = []
    input_file = open("../020_word_lists/Operands_sorted.csv", encoding='utf-8')
    for line in input_file.readlines():
        Operands.append(sanitize(line.strip(), False))

    # Other = []
    # input_file = open("../020_word_lists/Other.txt", encoding='utf-8')
    # for line in input_file.readlines():
    #     Operands.append(sanitize(line.strip(), False))

    if False:
        print(RegulatoryOperators)
        print(Operators)
        print(Operands)


    #
    # START WORK ON ACTUAL FILE
    #
    print("<<<<<< WORKING ON: " + input_file_name)

    if True:
        print("  READING WORDS")
        print("    # RegulatoryOperators: " + str(len(RegulatoryOperators)))
        print("    # Operators: " + str(len(Operators)))
        print("    # Operands: " + str(len(Operands)))


    # read .txt file
    in_text = ""
    input_file = open(input_file_name, 'r', encoding="utf-8")
    for line in input_file.readlines():       
        in_text += sanitize(line, False)
    input_file.close()

    total_words = len(in_text.split())
    total_chars = len(in_text)

    print("  TOTAL WORDS: " + str(total_words))
    print("  TOTAL CHARS: " + str(total_chars))

    #
    # LOOP OVER REGULATORY OPERATORS, OPERATORS AND OPERANDS...
    # - start with regulatory operators, as these are a subset of all operators and we want to identify them separately
    # - do frequency count and then change the text to avoid short terms being found often within strings
    #
    # ...AND MATCH N-GRAMS TO COMPUTE COVERAGE
    # - for this, first check all n-grams of length larger than one
    # - then sort all 1-grams in a single list and find those, longest first
    #
    freq_text = ""

    regop_matches = []
    op_matches = []
    od_matches = []

    for entry in RegulatoryOperators:
        if len(entry.split()) > 1:  # check all n-grams first across operators, operands, etc.
            entry_count = in_text.count(entry)
            if entry_count > 0 and entry != "":
                count['RegulatoryOperators'] += entry_count
                unique['RegulatoryOperators'] += 1
                freq_text += "RegulatoryOperators;" + entry + ";" + str(entry_count) + "\n"
                in_text = in_text.replace(entry, "")
        else:
            regop_matches.append(entry)

    for entry in Operators:
        if len(entry.split()) > 1:
            entry_count = in_text.count(entry)
            if entry_count > 0 and entry != "":
                count['Operators'] += entry_count
                unique['Operators'] += 1            
                freq_text += "Operators;" + entry + ";" + str(entry_count) + "\n"
                in_text = in_text.replace(entry, "")
        else:
            op_matches.append(entry)     

    for entry in Operands:
        if len(entry.split()) > 1:
            entry_count = in_text.count(entry)
            if entry_count > 0 and entry != "":
                count['Operands'] += entry_count
                unique['Operands'] += 1            
                freq_text += "Operands;" + entry + ";" + str(entry_count) + "\n"
                in_text = in_text.replace(entry, "")
        else:
            od_matches.append(entry)

    in_text = ' '.join(in_text.split())  # remove duplicate whitespaces
    
    # then loop again over all 1-grams
    for entry in sorted(regop_matches, key=len, reverse=True):
        entry_count = in_text.count(entry)
        if entry_count > 0 and entry != "":
            count['RegulatoryOperators'] += entry_count
            unique['RegulatoryOperators'] += 1
            freq_text += "RegulatoryOperators;" + entry + ";" + str(entry_count) + "\n"
            in_text = in_text.replace(entry, "")

    for entry in sorted(op_matches, key=len, reverse=True):
        entry_count = in_text.count(entry)
        if entry_count > 0 and entry != "":
            # print(entry_count, count['Operators'], ">" + entry + "<")
            count['Operators'] += entry_count
            unique['Operators'] += 1
            freq_text += "Operators;" + entry + ";" + str(entry_count) + "\n"
            in_text = in_text.replace(entry, "")

    for entry in sorted(od_matches, key=len, reverse=True):
        entry_count = in_text.count(entry)
        if entry_count > 0 and entry != "":
            count['Operands'] += entry_count
            unique['Operands'] += 1
            freq_text += "Operands;" + entry + ";" + str(entry_count) + "\n"
            in_text = in_text.replace(entry, "")

    #
    # OUTPUT
    #
    frac = 1.0 - float(len(sanitize(in_text,False)))/float(total_chars)
    print("  FRACTION FOUND: " + str(round(frac,2)))

    # create output text
    out_text = "file_name;RegulatoryOperators;UniqueRegulatoryOperators;Operands;UniqueOperands;Operators;UniqueOperators;WordCount\n"
    out_text += input_file_name + ";"
    out_text += str(count["RegulatoryOperators"]) + ";" + str(unique["RegulatoryOperators"]) + ";"
    out_text += str(count["Operands"]) + ";" + str(unique["Operands"]) + ";"
    out_text += str(count["Operators"]) + ";" + str(unique["Operators"]) + ";"
    out_text += str(total_words) + "\n"

    # create latex text
    latex_text = ""
    # latex_text = "\\begin{table}[h]\\begin{tabular}{lllllllll}\n"
    # latex_text += "\\toprule\n"
    # latex_text += "file_name & {\\bf Total Words} & {\\bf Fraction Found} & {\\bf Regulatory Operators} & {\\bf Unique Regulatory Operators} & {\\bf Operands} & {\\bf Unique Operands} & {\\bf Operators} & {\\bf Unique Operators} & {\\bf Total Volume} & {\\bf Potential Volume} & {\\bf Level}\n"
    # latex_text += "\\midrule\n"
    latex_text += input_file_name + " & " + str(total_words) + " & " + str(round(frac,2))
    latex_text += " & " + str(count["RegulatoryOperators"]) + " & " + str(unique["RegulatoryOperators"])
    latex_text += " & " + str(count["Operands"]) + " & " + str(unique["Operands"])
    latex_text += " & " + str(count["Operators"]) + " & " + str(unique["Operators"])
    TotalVolume = count["Operators"] + count["Operands"] + count["RegulatoryOperators"]
    PotentialVolume = 2 + unique["Operands"]
    Level = 100.0 * round(PotentialVolume / TotalVolume,3)
    latex_text += " & " + str(TotalVolume) + " & " + str(PotentialVolume) + " & " + str(Level) + "\%" + "\\\\\n"
    # latex_text += "\\bottomrule\n"
    # latex_text += "\end{tabular}\caption{Caption}\label{Tab::TableX}\end{table}\n"

    #
    # WRITE OUTPUT
    # 

    # write results file
    out_file = open("./results/results-" + output_file_name, 'w', encoding="utf-8")
    out_file.write(out_text)
    out_file.close()
    print("  >>> RESULTS WRITTEN TO: " + "./results/results-" + output_file_name)

    # write latex
    latex_out_file = open("./results/" + output_file_name.rstrip(".csv") + ".tex", 'w', encoding="utf-8")
    latex_out_file.write(latex_text)
    latex_out_file.close()
    print("  >>> LATEX WRITTEN TO: " + "./results/" + output_file_name.rstrip(".csv") + ".tex")

    # write frequency
    freq_file = open("./frequency/frequency-" + output_file_name, 'w', encoding="utf-8")
    freq_file.write(freq_text)
    freq_file.close()
    print("  >>> FREQUENCIES WRITTEN TO: " + "./frequency/frequency-" + output_file_name)

    # write out unclassified tokens
    out_text = ""
    out_file = open("./unclassified/unclassified-" + output_file_name, "w", encoding="utf-8")
    for token in set(sanitize(in_text, False).split(" ")):
        out_text += token + ";" + str(in_text.count(token)) + "\n"
    out_file.write(out_text)
    out_file.close()
    print("  >>> UNCLASSIFIED TOKENS WRITTEN TO: " + "./unclassified/unclassified-" + output_file_name)



    #
    # END
    #
    print(">>>>>> FINISHED")
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#
#  MAIN
#
# -------------------------------------------------------------------------
if __name__ == '__main__':
#
# VARIABLES
#
    args = sys.argv
    input_file_name = args[1]
    output_file_name = args[2]

#
# CODE
#
    do_run(input_file_name, output_file_name)