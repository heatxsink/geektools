#!/bin/bash
# You will find this script all over the place. This is not mine,
# but it is definitely nice to have it checked in somewhere.
#
# :-) Happy Hacking
#
echo `date "+%d %B %Y"` | awk \
'{ print substr("          ",1,(21-length($0))/2) $0; }'; \
cal | awk '{ getline; print " Mo Tu We Th Fr Sa Su"; getline; \
if (substr($0,1,2) == " 1")  print "                    1 "; \
do { prevline=$0; if (getline == 0) exit; print " "\
substr(prevline,4,17) " " substr($0,1,2) " "; } while (1) }' | \
awk -v cday=`date "+%d"` '{ fill=(int(cday)>9?"":" ");    \
a=$0; sub(" "fill int(cday)" ","*"fill int(cday)"*",a); print  a }'\