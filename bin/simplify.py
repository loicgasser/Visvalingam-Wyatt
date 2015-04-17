#!/usr/bin/python

import json
from visvalingam.classes import checkArguments as check
from visvalingam import VisvalingamSimplification

input, output, threshold = check.getIOFilesThreshold()

# Open a file, containing a pure GeoJSON-geometry
json_data = open(input, 'r')
data = json.load(json_data)  # parse JSON-content
json_data.close()

nPointsPrev = len(data['coordinates'])

simplify = VisvalingamSimplification(data['coordinates'])
data['coordinates'] = simplify.simplifyLineString(float(threshold))
data['threshold'] = threshold

print 'Pointreduction:', nPointsPrev, '/', len(data['coordinates'])

# Write the resulting GeoJSON-file
json_file = open(output, 'w')
json.dump(data, json_file)
json_file.close()
