#!/usr/bin/env python3

"""
Run some tests to illustrate getting path representations from the AMR

"""
import penman
import sys
import os
import json
import logging

amrfilename = "tests/test-path.json"

with open(amrfilename) as amr_file:
    test_units = json.load(amr_file)
    for test_unit in test_units:
        each_amr = test_unit['amr']
        raw_amr = "\n".join([line for line in each_amr.strip().split("\n") if not line.startswith("#")])
        # Just gets a normal AMR from a JSON of AMRs 
        if raw_amr.strip() != '':
            
            # Decoding with "reify attributes" makes the attributes represented as nodes
            its_amr = penman.decode(raw_amr, reify_attributes=True)

            # amr_transformer_path gets the weird format that they seem to use in https://github.com/Amazing-J/structural-transformer/
            its_dict = its_amr.amr_transformer_path(max_distance=5, shortening_method="end", plusminus=True)
            
            # You can add an ordered variable list as well.  
            # This should allow you to repeat nodes, which might be needed for whatever they are doing with BPE paths
            
            #its_dict = its_amr.amr_transformer_path(max_distance=5, shortening_method="end", plusminus=True, ordered_variable_list=test_unit['variable-order'])
            
            #
            # Test whether path output is exactly the same as we see in the paper
            # One AMR passes!
            # The second AMR is failing because of BPE splits
            # I have no idea why the third is failing. 
            its_valid = its_dict['path'] == test_unit['relation']
            if its_valid:
                print("Pass test for type:  "+test_unit["testname"])
            else:
                print("Fail test for type:  "+test_unit["testname"])
                print(its_dict['path'])
                print(test_unit['relation'])                

if len(sys.argv) > 1:
    amr_test_folder = sys.argv[1]
    amrs_validated = 0
    for each_folder, each_root, each_list_of_files in os.walk(amr_test_folder):
        for each_amr_file_name in each_list_of_files:
            its_filename = each_folder+"/"+each_amr_file_name
            with open(its_filename) as amr_file:
                for each_amr in amr_file.read().split("\n\n"):
                    raw_amr = "\n".join([x for x in each_amr.split("\n") if not x.startswith("#")])
                    if len(raw_amr.strip()) > 0:
                        its_amr = penman.decode(raw_amr, reify_attributes=True)
                        its_dict = its_amr.amr_transformer_path(max_distance=5, shortening_method="end", plusminus=True)
                        amrs_validated +=1
                        if amrs_validated % 100== 0:
                            logging.info(f"validated {amrs_validated} amrs")
                    