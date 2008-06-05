#!/usr/bin/env python
# extract journal titles and first-two-letters of titles from J_Medline
# as CSV
# (from ftp://ftp.ncbi.nih.gov/pubmed/J_Medline.gz )

import sys

f = open(sys.argv[1], 'r')

title_list = []

for l in f:
    s = l.split(":")
    key = s[0]
    value = ":".join(s[1:])[:-1].strip().replace("'","").replace('"',"")

    if key == "JournalTitle" and value != "":# and len(value) < 40:
        #print '"%s", "%s"' % (value, value[0:2].lower())
        title_list.append('"%s",' % (value))

    if (key == "MedAbbr" or key == "IsoAbbr") \
        and value != "":
        #print '"%s", "%s"' % (value, value[0:2].lower())
        title_list.append('"%s",' % (value))

# in effect, removes duplicates
title_list = list(set(title_list))
title_list.sort()

outstr = ""
count = 1
for t in title_list:
    outstr += t + "\n"
    # write titles into a series of list files not exceeding ~1 Mb each
    # 
    if len(outstr) > (1000000 * count):
        of = open("jtitles%i.py" % (count), 'w')
        of.write("title_list = [%s]\n" % (outstr))
        of.close()
        outstr = ""
        count += 1

# last jtitles files
of = open("jtitles%s.py" % (count), 'w')
of.write("title_list = [%s]" % (outstr))
of.close()

# write the master list file, that imports them all
of = open("journal_titles.py", 'w')
of.write("title_list = []\n")
for c in range(1,count+1):
    of.write("import jtitles%i\n" % (c))
    of.write("title_list += jtitles%i.title_list\n" % (c))
