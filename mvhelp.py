#!/usr/bin/python
"""
Author: Dominic Rivera
Name: mvhelp
Description: Generate all the commands you will need in a linux system to utilize a managed volume
Usage: ./mvhelp.py <filename.csv>
"""

import csv
import sys
#db_name = raw_input("Database Name: ")
db_name = "db2"
mvid = "fc119120-6f9a-43a6-9be3-a1341f16992d"
#mvid = raw_input("Managed Volume ID: ")
#username = raw_input("Username: ")
username = "admin"
#password = raw_input("Password: ")
password = "RubrikGoForward"
channels = {}

# Open the file passed on the command line, read it in as a .csv
with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    records = 0
    for row in csv_reader:
        if records == 0:
            records += 1
            continue
        else:
        # Make a new dict entry for the channel if one doesn't exist
            if not channels.has_key(row[0]):
                channels[row[0]] = { 'channel_number': "", 'floating_ip': "" , 'mount_point': "" }
        
            channels[row[0]]['channel_number'] = row[0]
            channels[row[0]]['floating_ip'] = row[1]
            channels[row[0]]['mount_point'] = row[2]
            records += 1



print "mkdir -p /mnt/rubrik/%s_ch{0..%d}" % (db_name, (records - 2 ))

for key in channels:
    channel_number = int(channels[key]['channel_number']) - 1
    mount_point = channels[key]['mount_point']
    floating_ip = channels[key]['floating_ip']
    print "%s:%s    /mnt/rubrik/%s_ch%s   nfs rw,bg,hard,nointr,rsize=131072,wsize=131072,tcp,vers=3,timeo=600,actimeo=0,noatime 0 0" % (floating_ip, mount_point, db_name, channel_number)



print "curl -k -X POST -u '%s:%s' 'https://%s/api/internal/managed_volume/ManagedVolume:::%s/begin_snapshot'" % ( username, password, floating_ip, mvid)
print "curl -k -X POST -u '%s:%s' 'https://%s/api/internal/managed_volume/ManagedVolume:::%s/end_snapshot'" % ( username, password, floating_ip, mvid)