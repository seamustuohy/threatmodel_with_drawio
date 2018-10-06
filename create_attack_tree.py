#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018 seamus tuohy, <code@seamustuohy.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the included LICENSE file for details.
#
# Styles Derived From
# Draw.io libraries for threat modeling
# https://github.com/michenriksen/drawio-threatmodeling
# The MIT License (MIT)
# Copyright (c) 2018 Michael Henriksen
#

import argparse
from csv import DictReader
import logging
logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)


def main():
    args = parse_arguments()
    set_logging(args.verbose, args.debug)
    formatting = get_formatting()
    print(formatting)
    input_csv = get_csv(args.input_file)
    output_csv = make_drawio_csv(input_csv, args.style)
    print(output_csv)

def make_drawio_csv(input_csv, style_name):
    style_templates = {
        "attack_tree": {
            "LEAF": "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;",
            "OR": "shape=xor;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;direction=north;",
            "AND": "shape=or;whiteSpace=wrap;html=1;direction=north;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        },
        "data_flow_diagram":{}}
    style = style_templates[style_name] # Fail on not exist

    # "name","id","parent","type","url","description"
    output_csv = []
    csv_keys = list(input_csv[0].keys())
    # We don't actually need difficulty since we push it into 'type' for leaves
    csv_keys.remove('difficulty')
    csv_keys.append('style')
    csv_header_string =  '"{name}","{id}","{parent}","{type}","{url}","{description}","{style}"'
    output_csv.append(",".join(csv_keys))
    for item in input_csv:
        item['style'] = style.get(
            item['type'],
            "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
        )
        if item['type'] == "LEAF":
            item['type'] = item['difficulty']
        else:
            item['type'] = "({0})".format(item['type'])
        _string = csv_header_string.format(**item)
        output_csv.append(_string)
    return "\n".join(output_csv)


def get_csv(filename):
    data = []
    with open(filename, 'r') as fp:
        reader = DictReader(fp)
        for row in reader:
            data.append(row)
    return data

def get_test_csv_data():
    return """name,from,style,url
open safe, NONE, "shape=xor;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;direction=north;",""
Pick Lock, open safe,"rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;",""
Cut Open Safe, open safe,"rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;",""
Learn Combo, open safe, "shape=xor;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;direction=north;",""
Find Written Combo, Learn Combo, "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;",""
Get Combo from Target, Learn Combo, "shape=xor;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;direction=north;",""
Threaten, Get Combo from Target, "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;",""
Blackmail, Get Combo from Target, "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;",""
Bribe, Get Combo from Target, "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;","www.seamustuohy.com"
"""

def get_formatting():
    """

    https://about.draw.io/wp-content/uploads/2018/03/drawio-example-csv-import.txt
    https://github.com/jgraph/drawio/blob/e2e661b9937adc189e89cee711c06ce0fc59e711/src/main/webapp/js/diagramly/EditorUi.js#L9853-L9865

https://github.com/jgraph/drawio/blob/e2e661b9937adc189e89cee711c06ce0fc59e711/src/main/webapp/js/diagramly/EditorUi.js#L9891-L9910

    """
    body = {
        "info":{"comments":["Use ## for comments and # for configuration.",
                            "The following names are reserved and should not be used (or ignored):",
                            "id, tooltip, placeholder(s), link and label (see below)"],
                "values":[]},
        "label":{"comments":["Node label with placeholders and HTML.",
                             "Default is '%name_of_first_column%'."],
                 "values":['label: %name%<br><i style="color:gray;">%type%</i><br>']},
        "style":{"comments":["Node style (placeholders are replaced once).",
                             "Default is the current style for nodes."],
                 "values":["style: %style%"]},
        "identity":{"comments":["Uses the given column name as the identity for cells (updates existing cells).",
                                "Default is no identity (empty value or -)."],
                    "values":["identity: -"]},
        "connect":{"comments":['Connections between rows ("from": source colum, "to": target column).',
                               "Label, style and invert are optional. Defaults are '', current style and false.",
                               "In addition to label, an optional fromlabel and tolabel can be used to name the column",
                               "that contains the text for the label in the edges source or target (invert ignored).",
                               "The label is concatenated in the form fromlabel + label + tolabel if all are defined.",
                               "The target column may contain a comma-separated list of values.",
                               "Multiple connect entries are allowed."],
                   "values":['connect: {"from": "parent", "to": "id", "invert": true, "label": "", "style": "curved=0;rounded=0;endArrow=blockThin;endFill=1;fontSize=11;exitX=0.25;exitY=0.5;exitPerimeter=0;edgeStyle=elbowEdgeStyle;elbow=vertical;"}']},
        "left":{"comments":["Node x-coordinate. Possible value is a column name. Default is empty. Layouts will",
                            "override this value."],
                "values":["left:"]},
        "top":{"comments":["Node y-coordinate. Possible value is a column name. Default is empty. Layouts will",
                           "override this value."],
               "values":["top:"]},
        "width":{"comments":["Node width. Possible value is a number (in px), auto or an @ sign followed by a column",
                             "name that contains the value for the width. Default is auto."],
                 "values":["width: 120"]},
        "height":{"comments":["Node height. Possible value is a number (in px), auto or an @ sign followed by a column",
                              "name that contains the value for the height. Default is auto."],
                  "values":["height: 80"]},
        "padding":{"comments":["Padding for autosize. Default is 0."],
                   "values":["padding: 0"]},
        "ignore":{"comments":["Comma-separated list of ignored columns for metadata. (These can be",
                              "used for connections and styles but will not be added as metadata.)"],
                  "values":["ignore: id,image,fill,stroke,style,type"]},
        "link":{"comments":["Column to be renamed to link attribute (used as link)."],
                "values":["link: url"]},
        "nodespacing":{"comments":["Spacing between nodes. Default is 40."],
                       "values":["nodespacing: 40"]},
        "edgespacing":{"comments":["Spacing between parallel edges. Default is 40."],
                       "values":["edgespacing: 40"]},
        "layout":{"comments":["Name of layout. Possible values are auto, none, verticaltree, horizontaltree,",
                              "verticalflow, horizontalflow, organic, circle. Default is auto."],
                  "values":["layout: auto"]},
        "start csv":{"comments":[" ---- CSV below this line. First line are column names. ----"],
                     "values":[]}
    }
    text = []
    for item_name, contents in body.items():
        text.append(make_comment(""))
        text.append(make_comment("==== {0} ====".format(item_name)))
        for comment in contents.get("comments", []):
            text.append(make_comment(comment))
        text.append(make_value(""))
        for value in contents.get("values", []):
            text.append(make_value(value))
        text.append(make_value(""))
    return "\n".join(text)


def make_comment(txt):
    return "## {0}".format(txt)

def make_value(txt):
    return "# {0}".format(txt)

# Command Line Functions below this point

def set_logging(verbose=False, debug=False):
    if debug == True:
        log.setLevel("DEBUG")
    elif verbose == True:
        log.setLevel("INFO")

def parse_arguments():
    parser = argparse.ArgumentParser("Creates draw.io CSV imports for threat modeling.")
    parser.add_argument("--verbose", "-v",
                        help="Turn verbosity on",
                        action='store_true')
    parser.add_argument("--debug", "-d",
                        help="Turn debugging on",
                        action='store_true')
    parser.add_argument("--input_file", "-i",
                        help="CSV to build.",
                        required=True)
    parser.add_argument("--style", "-s",
                        help="Styles to use [attack_tree or data_flow_diagram]\nNOTE:data_flow_diagram currently not supported",
                        default="attack_tree")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
