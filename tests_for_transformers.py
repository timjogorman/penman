import penman
import sys
import json
import logging
amrfilename = "tests/test-path.json"

with open(amrfilename) as amr_file:
    test_units = json.load(amr_file)
    for test_unit in test_units:
        each_amr = test_unit['amr']
        raw_amr = "\n".join([line for line in each_amr.strip().split("\n") if not line.startswith("#")])
        if raw_amr.strip() != '':
            its_amr = penman.decode(raw_amr, reify_attributes=True)
            its_dict = its_amr.amr_transformer_path(max_distance=5, shortening_method="end", plusminus=True, ordered_variable_list=["o", "c", "d", "x102", "x103"])
            its_valid = its_dict['path'] == test_unit['relation']
            if its_valid:
                print("Pass test for type:  "+test_unit["testname"])