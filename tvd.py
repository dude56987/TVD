#! /usr/bin/python
########################################################################
# Backend to dynamicly create and destroy virtual machines
# Copyright (C) 2015  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
import shutil
import os
import sys
########################################################################
def makeDir(remoteDir):
	import os
	''' Creates the defined directory, if a list of directorys are listed
	that do not exist then they will be created aswell, so beware of 
	spelling mistakes as this will create the specified directory you 
	type mindlessly.'''
	temp = remoteDir.split('/')
	remoteDir= ''
	for i in temp:
		remoteDir += (i + '/')
		if os.path.exists(remoteDir):
			print remoteDir , ': Already exists!, Moving on...'
		else:
			os.mkdir(remoteDir)
########################################################################
def loadFile(fileName):
	try:
		sys.stdout.write(("Loading :"+fileName))
		fileObject=open(fileName,'r');
	except:
		print "Failed to load :",fileName
		return False
	fileText=''
	lineCount = 0
	for line in fileObject:
		if line[:1] != '#':
			fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	sys.stdout.write(("Finished Loading :"+fileName+'\r'))
	sys.stdout.write(('                                                   \r'))
	fileObject.close()
	if fileText == None:
		return False
	else:
		return fileText
	#if somehow everything fails return false
	return False
########################################################################
def writeFile(fileName,contentToWrite):
	# figure out the file path
	filepath = fileName.split(os.sep)
	filepath.pop()
	filepath = os.sep.join(filepath)
	# check if path exists
	if os.path.exists(filepath):
		try:
			fileObject = open(fileName,'w')
			fileObject.write(contentToWrite)
			fileObject.close()
			print 'Wrote file:',fileName
		except:
			print 'Failed to write file:',fileName
			return False
	else:
		print 'Failed to write file, path:',filepath,'does not exist!'
		return False
########################################################################
def currentDirectory():
	currentDirectory = os.path.abspath(__file__)
	temp = currentDirectory.split(os.path.sep)
	currentDirectory = ''
	for item in range((len(temp)-1)):
		if len(temp[item]) != 0:
			currentDirectory += os.path.sep+temp[item]
	return (currentDirectory+os.path.sep)
########################################################################
runType = 'default'; # used for when system arguments are not used
# split the arguments by - signs to pull arguments more correctly
# this allows you to split that result by spaces for arguments with multuple entries
inputs = ' '.join(sys.argv).replace('--','-').split('-')
for arg in inputs:
	# split the arguments by spaces
	arguments = arg.split(' ')
	# grab main argument into its own variable
	mainArgument = arguments[0]
	# cut off the first argument for reading subsequent arguments
	arguments = arguments[1:]
	if (mainArgument in ['h','help']):
		# print the help file
		print(openFile('help.txt'))
		exit()
	elif (mainArgument in ['c','connect']):
		# set the address  to the first given address in arguments
		# address needs to be username@location like ssh
		destAddress= arguments[0]
		# set the runtype to connect
		runType = 'connect'
####################################################################
# deliver the payload after reading all arguments to the program
####################################################################
if runType=='connect':
	# create the mac address based string for name of virtual machine
	machineName=os.popen('ifconfig eth0 | sed "s/eth0.*Link.*.HWaddr //g" | sed "s/ $^inet.*//g" | sed "/^$/d" | sed "s/:/_/g"').read().split(' ')[0]
	# delete previous instance of virtual machine, if one does
	#  not exist then this does nothing
	print('ssh -t '+destAddress+' "virsh undefine '+machineName+' --remove-all-storage --wipe-storage"')
	os.system('ssh -t '+destAddress+' "virsh undefine '+machineName+' --remove-all-storage --wipe-storage"')
	# connect to a remote virt-manager instance and create
	#  a new instance of the virtual machine
	print('ssh -t '+destAddress+' "virt-clone --replace -o baseImage --name '+machineName+' --file /usr/share/diskimages/'+machineName+'.qcow2;"')
	os.system('ssh -t '+destAddress+' "virt-clone -o baseImage --name '+machineName+' --file /usr/share/diskimages/'+machineName+'.qcow2;"')
	# launch virt-viewer to remotely connect to newly created machine
	#print('virt-viewer -frk --connect qemu+ssh://'+destAddress+'/ '+machineName)
	#os.system('virt-viewer -frk --connect qemu+ssh://'+destAddress+'/ '+machineName)
	# start the virtual machine
	os.system('ssh -t '+destAddress+' "virsh start '+machineName)
	# run virt-viewer though x11 forwarding
	print('ssh '+destAddress+' -t -X virt-viewer -frk '+machineName)
	os.system('ssh '+destAddress+' -t -X virt-viewer -frk '+machineName)
	# -r = reconnect, -k = kiosk mode, -f = fullscreen
exit()
