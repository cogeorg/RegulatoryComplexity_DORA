#!/bin/bash

# PRELIMINARIES
# Prepare glossary - needs to be run only once
# ./05_prepare_glossary.py ../020_word_lists/RegulatoryOperators_Tax-raw.txt ../020_word_lists/RegulatoryOperators_Tax-clean.txt

# ANALYZE TEXT
for entry in  DORA_Initial-2020 DORA_Initial-2020_IA DORA_FinReg-2022 DORA_EP_PA-2022 ;
  do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
done

for entry in `seq 0 9` ;
  do time ./10_do_analysis.py ../010_raw_documents/DORA_FinReg-2022--$entry.txt DORA_FinReg-2022--$entry.csv;
done

for entry in  MICA MICA_IA AI AI_IA;
  do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
done

rm results/results.csv 2>/dev/null
echo "file_name;LogicalConnectors;UniqueLogicalConnectors;Operands;UniqueOperands;Operators;UniqueOperators;Other;UniqueOther;Unclassified;UniqueUnclassified;WordCount" > results/results.csv
cat results/results*.csv |grep -v "file_name;Operands" >> results/results.csv

rm results/latex_results.tex 2>/dev/null
cat results/*.tex >> results/latex_results.tex

# CREATE HISTOGRAMS
# for entry in DORA_EP_PA-2022 DORA_FinReg-2022 DORA_Initial-2020 DORA_Initial-2020_IA MICA MICA_IA AI AI_IA;
#   do ./11_create_histograms.py ./frequency/frequency-$entry.csv ./histograms/histo-$entry.csv ;
# done