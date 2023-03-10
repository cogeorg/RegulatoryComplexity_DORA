#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re

# ###########################################################################
# METHODS
# ###########################################################################
def sanitize(entry):
    entry = entry.upper()

    # remove all links to other sections
    numbers = re.findall(r'([0-9]+)\.', entry)  # needs to be done before replacing "."
    for number in numbers:
        entry = entry.replace(number, "")

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

    return entry

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_file_name, output_file_name):
    out_text = "file_name;Operands;UniqueOperands;Operators;UniqueOperators;Other;UniqueOther;Unclassified;UniqueUnclassified;WordCount\n"

    count = {}
    count['Operators'] = 0
    count['Operands'] = 0
    count['Other'] = 0
    count['Unclassified'] = 0

    unique = {}
    unique['Operators'] = []
    unique['Operands'] = []
    unique['Other'] = []
    unique['Unclassified'] = []
    unique['unclassified'] = []

    total_words = 0
    total_classified = 0

    Operators = []
    input_file = open("../020_word_lists/Operators.txt", encoding='utf-8')
    for line in input_file.readlines():
        Operators.append(sanitize(line.strip()))

    Operands = []
    input_file = open("../020_word_lists/Operands.txt", encoding='utf-8')
    for line in input_file.readlines():
        Operands.append(sanitize(line.strip()))

    Other = []
    input_file = open("../020_word_lists/Other.txt", encoding='utf-8')
    for line in input_file.readlines():
        Other.append(sanitize(line.strip()))

    Unclassified = []
    input_file = open("../020_word_lists/Unclassified.txt", encoding='utf-8')
    for line in input_file.readlines():
        Unclassified.append(sanitize(line.strip()))

    if False:
        print(Operators)
        print(Operands)
        print(Other)
        print(Unclassified)


    #
    # START WORK ON ACTUAL FILE
    #
    print("<<<<<< WORKING ON: " + input_file_name)

    if True:
        print("  READING WORDS")
        print("    # Operators: " + str(len(Operators)))
        print("    # Operands: " + str(len(Operands)))
        print("    # Other: " + str(len(Other)))
        print("    # Unclassified: " + str(len(Unclassified)))

    input_file = open(input_file_name, 'r')

    # read .txt file
    for line in input_file.readlines():
        tokens = line.strip().split(" ")
        for entry in tokens:
            token = sanitize(entry)
            is_classified = False

            if token in Operators:
                is_classified = True
                count['Operators'] += 1
                try:
                    unique['Operators'].append(token)
                except:
                    pass
            if token in Operands:
                is_classified = True
                count['Operands'] += 1
                try:
                    unique['Operands'].append(token)
                except:
                    pass
            if token in Other:
                is_classified = True
                count['Other'] += 1
                try:
                    unique['Other'].append(token)
                except:
                    pass
            if token in Unclassified:
                is_classified = True
                count['Unclassified'] += 1
                try:
                    unique['Unclassified'].append(token)
                except:
                    pass

            total_words += 1
            if is_classified:
                total_classified += 1
            else: # add to list of unclassified words
                unique['unclassified'].append(token)

    #
    # CLEAN UP OPERANDS
    #
    _number = 0
    while _number <= 800:
        _count = unique['Operands'].count(str(_number))
        if _count > 0:
            unique['Operands'].remove(str(_number))
        if False:
            print(_number, _count, unique['Operands'].count(str(_number)))
        _number += 1

    #
    # OUTPUT
    #
    print("  TOTAL WORDS: " + str(total_words))
    print("  TOTAL CLASSIFIED: " + str(total_classified))
    print("  TOTAL UNCLASSIFIED: " + str(len(unique['Unclassified'])))
    print("  TOTAL OTHER: " + str(len(unique['Other'])))
    print("  TOTAL NOT FOUND: " + str(len(unique['unclassified'])))

    frac = float(total_classified)/float(total_words)
    print("  FRACTION FOUND: " + str(round(frac,2)))

    # add output
    out_text += input_file_name
    for count_key in sorted(count.keys()):
        out_text += ";" + str(count[count_key]) + ";" + str(len(set(unique[count_key])))
    out_text += ";" + str(total_words) + "\n"

    # #
    # # compute num operators, operands
    # #
    # num_unique_operators = len(set(unique['Operators']))
    # num_unique_operands = len(set(unique['Operands']))
    # num_operators = count['Operators']
    # num_operands = count['Operands']
    #
    # total_volume = num_operators + num_operands
    # potential_volume = 2.0 + num_unique_operands
    # level = float(potential_volume) / float(total_volume)
    #
    # if True:
    #     print("    << TOTAL VOLUME:" + str(total_volume))
    #     print("    << POTENTIAL VOLUME:" + str(potential_volume))
    #     print("    << LEVEL:" + str(level))
    #
    # out_text += str(num_operators) + ";" + str(num_operands) + ";" + str(num_unique_operators) + ";" + str(num_unique_operands) + ";"
    # out_text += str(total_volume) + ";" + str(potential_volume) + ";" + str(level) + "\n"

    #
    # write results file
    #
    out_file = open("./results/results-" + output_file_name, 'w')
    out_file.write(out_text)
    out_file.close()
    print("   RESULTS WRITTEN TO: " + "./results/results-" + output_file_name)

    #
    # write out unclassified tokens
    #
    out_text = ""
    out_file = open("./unclassified/unclassified-" + output_file_name, "w")
    for token in set(unique['unclassified']):
        out_text += token + ";" + str(unique['unclassified'].count(token)) + "\n"
    out_file.write(out_text)
    out_file.close()
    print("   UNCLASSIFIED TOKENS WRITTEN TO: " + "./unclassified/unclassified-" + output_file_name)

    #
    # write frequency file
    #
    out_text = ""
    out_file = open("./frequency/frequency-" + output_file_name, 'w')
    for token in set(unique['Operators']):
        out_text += "Operators;" + token + ";" + str(unique['Operators'].count(token)) + "\n"
    for token in set(unique['Operands']):
        out_text += "Operands;" + token + ";" + str(unique['Operands'].count(token)) + "\n"
    for token in set(unique['Other']):
        out_text += "Other;" + token + ";" + str(unique['Other'].count(token)) + "\n"
    for token in set(unique['Unclassified']):
        out_text += "Unclassified;" + token + ";" + str(unique['Unclassified'].count(token)) + "\n"
    out_file.write(out_text)
    out_file.close()
    print("   FREQUENCIES WRITTEN TO: " + "./frequency/frequency-" + output_file_name)

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