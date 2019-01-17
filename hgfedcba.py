#!/usr/bin/python

import sys
import os
import yaml
import string

if len(sys.argv) != 3:
	print("Can only take 1 argument, a URL")
	sys.exit()
	
ypath = sys.argv[1]

if os.path.isdir(ypath):
	print("Can only accept a file path for now...")
	sys.exit()
else:
	if not os.path.isfile(ypath):
		print("Cannot find file.")
		sys.exit()
	
	with open(ypath, 'r') as yf:
		# use safe_load instead load
		deviceMap = yaml.safe_load(yf)
		deviceName = deviceMap['name']
		hpath = sys.argv[2]
		headerPath = ""
		if os.path.isdir(hpath):
			headerPath = os.path.splitext(hpath)[0] + deviceName + "_p.h"
		else:
			headerPath = hpath 
		
		with open(headerPath, 'w') as hf:
			headerGuardName = os.path.splitext(os.path.basename(headerPath))[0].upper() + "_H"
			hf.write("#ifndef " + headerGuardName + "\n")
			hf.write("#define " + headerGuardName + "\n")
			hf.write("\n")
			define = "#define "
			registers = deviceMap['registers']
			for regName in registers:
				register = registers[regName]
				registerPrefix = (deviceName + "_R_" + regName).upper()
				registerDefine = (define + registerPrefix + " " + "0x" + format(register['address'], '02x').upper())
				hf.write(registerDefine + "\n")
				try:
					fields = register['fields']
					for fieldName in fields:
						field = fields[fieldName]
						fieldPrefix = registerPrefix + "_F_" + fieldName.upper()
						fieldDefine = (define + fieldPrefix + "_MASK " + "0x" + format((2**(int(field[1]))-1) << int(field[0]), '02x').upper())
						hf.write(fieldDefine + "\n")
				except:
					pass
				hf.write("\n")
			hf.write("#endif")

