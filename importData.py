#import data
import datetime
def parseRow(data_dict, fields, row_index, row,):
	row_dict = dict(row)
	row_dict['latitude'] = float(row_dict['latitude'])
	row_dict['longitude'] = float(row_dict['longitude'])
	row_dict['date'] = datetime.datetime.strptime(row_dict['date'], '%Y-%m-%d').date()
	data_dict[row_index] = row_dict
	for field in fields:
		data_dict[field].append(row_dict[field])
	

def importFile(PathFile):
	#input filepath, string
	#output data, dict

	#parse file into data structure
	import csv
	from collections import OrderedDict

	#latitude	longitude	title	date	topic
	reader = csv.DictReader(open(PathFile), delimiter='\t')
	fields = reader.fieldnames

	data_dict = {}
	for field in fields:
		data_dict[field] = []

	row_index = 0
	for row in reader:
		parseRow(data_dict, fields, row_index,row)
		row_index += 1
	data_dict['size'] = row_index

	print("imported File")

	return data_dict
