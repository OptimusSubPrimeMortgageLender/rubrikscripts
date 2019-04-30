#!/usr/bin/python
"""
Author: Dominic Rivera
Name: makestats.py
Description: makestats.py will take a .csv file from a specific report and summarize the data on a per-object_type basis. You can find the report in the amer2 gaia cluster under Dominic POC stats
Usage: ./makestats.py <filename.csv>
Sample Output (per object type):
Object type : Managed Volume
Data Transferred (GB): 271.29
Data Stored (GB): 11.75
Data Efficiency Ratio : 23.09
Backup jobs : 17
Total Duration for object type (minutes): 26.5
Average duration for object type (minutes): 1.56
Average duration (seconds) 93.47
Average Logical Throughput MB/s : 2972.04
Max throughput MB/s : 1092.11
"""

import csv
import sys

 # Create an empty dict for the stats.
stats = { }

# Open the file passed on the command line, read it in as a .csv
with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    records = 0
    for row in csv_reader:
        if records == 0:
            records += 1
        else:
            # Skip all the archival jobs
            if row[1] == "Archival":
                continue
            # Skip the Failed jobs
            if row[0] == "Failed":
                continue
            # Skip the cancelled jobs
            if row[0] == "Canceled":
                continue
            # Skip any of the EC2 object types
            if row[3] == 'Ec2 Instance':
                continue

            # Turn our CSV into some human-readable variables
            object_type = row[3]
            data_stored = float(row[10])
            data_transferred = float(row[9])
            duration = float(row[8])
            throughput = data_transferred / duration

            # Create a new dictionay key for stats if we need one
            if not stats.has_key(object_type):
                stats[row[3]] = { 'data_transferred': 0, 'data_stored': 0, 'duration': 0,'jobs': 0, 'max_throughput': 0}
            
            # Check to see if this record is the max for throughput, and store it if so
            if float(stats[object_type]['max_throughput']) < throughput:
                stats[object_type]['max_throughput'] = throughput
            
            # load the dict with our data
            stats[object_type]['data_transferred'] += data_transferred
            stats[object_type]['data_stored'] += data_stored
            stats[object_type]['duration'] += duration
            stats[object_type]['jobs'] += 1
            records += 1
    print ""
    print "Processed %d records" % records
    print ""

for key in stats:
    data_transferred = stats[key]['data_transferred'] / 1024 / 1024 / 1024
    data_stored = stats[key]['data_stored'] / 1024 / 1024 / 1024
    duration = stats[key]['duration']
    jobs = stats[key]['jobs']
    max_throughput = stats[key]['max_throughput']

    print "Object type : %s" % key
    print "Data Transferred (GB): %.2f" % data_transferred
    print "Data Stored (GB): %.2f" % data_stored
    print "Data Efficiency Ratio : %.2f" % ( data_transferred / data_stored )
    print "Backup jobs : %d" % jobs
    print "Total Duration for object type (minutes): %.1f"  % (duration / 60)
    print "Average duration for object type (minutes): %.2f" % ( duration / jobs / 60)
    print "Average duration (seconds) %.2f" % (duration/jobs)
    print "Average Logical Throughput MB/s : %.2f" % ((data_transferred * 1024) / ( duration / jobs))
    print "Max throughput MB/s : %.2f" % (max_throughput / 1024 / 1024 )
    print ""
