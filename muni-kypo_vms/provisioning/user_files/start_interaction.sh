#!/bin/bash

declare -i sec=0 # seconds
declare -i min=0 # minutes 

echo "Waiting for other virtual machines." > /home/kali/waiting_log.txt

#Cycle to check if the vagrant server is build.
while ! ping -c 1 -w 2 10.11.30.3 &> /dev/null ;
do 
	echo "down" $min:$sec >> /home/kali/waiting_log.txt
	sleep 10
	sec=sec+10
	if test $sec -ge 60;
	then 
		sec=0
		min=min+1
	fi
done

sleep 240

python3 /home/kali/interaction1.py
python3 /home/kali/interaction2.py
python3 /home/kali/interaction3.py
