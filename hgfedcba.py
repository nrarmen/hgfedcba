#!/usr/bin/python

import sys
import os
import yaml
import string

if len(sys.argv) != 2:
	print("Can only take 1 argument, a URL")
	sys.exit()
	
path = sys.argv[1]

if os.path.isdir(path):
	print("Can only accept a file path for now...")
	sys.exit()
else:
	if not os.path.isfile(path):
		print("Cannot find file.")
		sys.exit()
	
	with open(path, 'r') as yf:
		# use safe_load instead load
		deviceMap = yaml.safe_load(yf)
		headerPath = os.path.splitext(path)[0] + "_p.h"
		with open(headerPath, 'w') as hf:
			headerGuardName = os.path.splitext(os.path.basename(headerPath))[0].upper() + "_H"
			hf.write("#ifndef " + headerGuardName + "\n")
			hf.write("#define " + headerGuardName + "\n")
			hf.write("\n")
			deviceName = deviceMap['name']
			define = "#define "
			registers = deviceMap['registers']
			for regName in registers:
				register = registers[regName]
				registerPrefix = (deviceName + "_R_" + regName).upper()
				registerDefine = (define + registerPrefix + " " + "0x" + format(register['address'], '02x').upper())
				hf.write(registerDefine + "\n")
				fields = register['fields']
				for fieldName in fields:
					field = fields[fieldName]
					fieldPrefix = registerPrefix + "_F_" + fieldName.upper()
					fieldDefine = (define + fieldPrefix + "_MASK " + "0x" + format((2**(int(field[1]))-1) << int(field[0]), '02x').upper())
					hf.write(fieldDefine + "\n")
				hf.write("\n")
			hf.write("#endif")

