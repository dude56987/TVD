#! /bin/bash
########################################################################
# Monitor to pause start and destory machines created by tvd
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
# Program to monitor active tvd connections, pause and resume the virtual machine on the server
paused=false
# grab the mac address of the current machine
machineName=$(ifconfig eth0 | sed "s/eth0.*Link.*.HWaddr //g" | sed "s/ $^inet.*//g" | sed "/^$/d" | sed "s/:/_/g" | tr -s "\n" " ")
for item in $machineName;do
	# grab the first item into a variable, this is the mac address
	machineName=$item
	break
done
# start main loop of daemon
while true;do
	# sleep for 1 second
	sleep 1
	idleTime=$(xprintidle)
	echo "Idle time is $idleTime Miliseconds"
	# if idletime is greater than 10 minutes
	if [ $idleTime -gt 600000 ];then 
		if [ $idleTime -gt 7200000 ];then 
			# destroy the machine if the idle time is greater than 2 hours
			ssh -t $destAddress virsh undefine $machineName --remove-all-storage --wipe-storage
		else
			#pause the virtual machine if idle time is greater than 10 minutes
			# and less than 2 hours
			states=$(virsh list | sed "s/-//g" | sed "s/\t/\ /g" | tr -s " ")
			for line in $states;do
				echo "Item 0 is ${line[0]}"
				echo "Item 1 is ${line[1]}"
				echo "Item 2 is ${line[2]}"
			done
		fi
		# set the paused flag
		paused=true
	else
		if $paused;then
			#resume virtualmachine
			ssh -t $destAddress virsh start $machineName
			#set the unpaused variable
			paused=false
		fi
	fi
done
