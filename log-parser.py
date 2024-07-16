import os.path
import re

flname = ''
timestamp = ' ' * 23
nas = ''
nonip = ''
noniplen = 11
direction = {
    'Tx': 'received',
    'Rx': 'transfered',
}
month = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
    'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
}

#check if file is exist
if not os.path.isfile(flname):
    flname = str(input('Filename?: '))
    if not os.path.isfile(flname):
        print('Filename "{}" doesn\'t exist or not a file'.format(flname))
        exit(1)

#pattern
regex = re.compile(
    '.+BOUND.+\s+(?P<timestamp>\d{2}:\d{2}:\d{2}:\d{3})\s+Eventid:'
    '|^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun).*day\s+'
    '(?P<month>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)).*\s+'
    '(?P<day>\d{2})\s(?P<year>\d{4})$'
    '|^(?P<srcip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.?\d{0,5})\s+'
    '>\s+(?P<dstip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.?\d{0,5}):\s+'
    '.+?len\s+(?P<len>\d+)\)'
    '|(?P<gprs>)===>GPRS Mobility'
#    'to\s+(?P<nasdst>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,5})\s+\((?P<naslen>\d+)\)$'
    '|(?P<message>)^Message :\s'
)
n=0
fout=open('c:/temp/out.txt', 'w+')
#open file and serch pattern
try:
 with open(flname, 'r') as file:
   for line in file:
        n +=1
        match = re.search(regex, line)
        if match:
            if match.lastgroup == 'timestamp':
                timestamp = '{} {} --'.format(date, match.group('timestamp'))
                nas = 'False'
            elif match.lastgroup == 'year':
                date = '{}-{}-{}'.format(match.group('year'), month[match.group('month')], match.group('day'))
            elif match.lastgroup == 'len':
                print('{} {} ==> {}, len({})'.format(timestamp, match.group('srcip'),
                                                     match.group('dstip'), match.group('len')))
                fout.write('{} {} ==> {}, len({})'.format(timestamp, match.group('srcip'),match.group('dstip'), match.group('len')))
            elif match.lastgroup == 'gprs':
                nas = 'True'
#                print(line)
            elif match.lastgroup == 'message':
                if nas == 'True':
                        print ('{} {}'.format(timestamp,line))
                        fout.write('{} {}'.format(timestamp,line))
                        nas = 'False'
except: print('error in line'+n)
fout.close()
