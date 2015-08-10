import urllib,urllib2
import re
from BeautifulSoup import BeautifulSoup
import string
import easygui as eg
import sys
import Tkinter
import ttk
import mechanize
import random
import time
import os
import csv
import xlwt
import xlrd

stop4=0
stop3=0
stop2=0
stop=0
email_repo = []

msg         = "Naukri Scraper"
title       = "Enter the information"
fieldNames  = ["Enter the job to be searched","Enter the number of pages","Enter the page number"]
fieldValues = [] 
fieldValues = eg.multenterbox(msg, title, fieldNames)

if fieldValues == None: 
    exit()
if fieldValues[0] == None: 
    exit()
if fieldValues[1] == None: 
    exit()
if fieldValues[2] == None: 
    exit()
    
job = fieldValues[0] 
entries = fieldValues[1]
done = fieldValues[2]

if int(done)==1 :
    stop3=0
else :
    stop3=1

if entries == "all" :
    print_entry = entries    
else:
    print_entry = int(entries)*50

msg ="Do you want to"
title = "File options"
choices = ["Create new file overwriting the existing the file", "Edit the existing one"]
answer = eg.choicebox(msg, title, choices)

if answer == None: 
    exit()

if entries == "all" :
    entries = "100000"

if answer == "Create new file overwriting the existing the file" :
    method = "w"
else:
    method = "r+"
    
job2 = job.split()
final_job = '-'.join(job2) + "-jobs"

file_name0 = final_job + ".csv"
file_name = eg.filesavebox(msg='Save file.', default=file_name0 , filetypes=['*.csv'])

try :
    f = open(file_name, method)
except IOError :
    title = "File does not exist"
    eg.msgbox("Create new file", title)
    stop2 = 1
    
if stop2 == 1 :
    f = open(file_name, "w")
    f.close()
    f = open(file_name, "r+")
    
if method == "r+" :
    for r in f.readlines() :
        if r is not None :
            index = r.find(',')
            content = str(len(r)-index)
            e_mail = r.rstrip(content)
            if e_mail.find('previous:') >=0 :
                done = e_mail.replace("previous:","")
                print "Loading previous work"
                stop3=1                
            email_repo.append(e_mail)
                    
if method == "w" :
    f.write("Email,Recruiter name,Contact company,Contact Details,Job link\n")


job_url = "http://jobsearch.naukri.com/" + final_job
print job_url
    
for page in range(int(entries)+ int(done)-1):
    if page == 0 :
        rand = random.randint(1, 100) 
        time.sleep( float(rand)*0.01 )
        br = mechanize.Browser()
        br.set_handle_robots(False)   
        br.set_handle_refresh(False)  
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        searchpage = br.open('http://jobsearch.naukri.com/mynaukri/mn_newsmartsearch.php?xz=1_3_69&xid=136912864936884500')
        html = searchpage.read()

        br.select_form(nr=0)
        br.form["qp"] = 'writing'
        br.select_form(nr=0)
        br.form["qk"] = ['comp']
        br.select_form(nr=0)
        br.form["qo"] = ['15']
        coreurlfile=br.submit()
        corepage = coreurlfile.read()
        coresoup = BeautifulSoup(corepage)
    else :
        if not url_next :
            print "no more results"
            f.write('previous:'+ str(page+1) +',\n')
            f.close()
            exit()
        if url_next.find('naukri') < 0:
            print "Security check"
            title = "Security Check"
            eg.msgbox("Please ", title)            
            f.write('previous:'+ str(page+1) +',\n')
            f.close()
            exit()
        else:
            coreurl = url_next
            rand = random.randint(1, 100) 
            time.sleep( float(rand)*0.01 )
            corerequest = urllib2.Request(coreurl, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
            coreurlfile = urllib2.urlopen(corerequest)
            corepage = coreurlfile.read()
            coresoup = BeautifulSoup(corepage)
            
    if stop3 == 1 :
        if page+1 >= int(done):
            stop4=0
        if page+1 < int(done) :
            stop4=1
            
    if stop4 == 0 :
        coreregex = '<div class="disp fl searchHd">(.+?)</strong>'
        corepattern = re.compile(coreregex)
        corevalue = re.findall(corepattern,corepage)
        corevalue[0] = corevalue[0].replace("<strong>","")
                
        coredivs = coresoup.findAll('div', attrs={'class' : 'jRes'})

        for div in coredivs:
            corelink = div.find('a')
            corelink2 = corelink['href']
            rand = random.randint(1, 100) 
            time.sleep( float(rand)*0.01 )
            
            address = corelink2
            request = urllib2.Request(address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
            urlfile = urllib2.urlopen(request)
            page = urlfile.read()
            soup = BeautifulSoup(page)
                        
            print "#################### " +corevalue[0]+" (getting "+str(print_entry)+" from " +str((int(done)-1)*50+1) + ")" + " ####################"
            
            regex = 'var EMAIL="(.+?)"'
            pattern = re.compile(regex)
            value = re.findall(pattern,page)
            stop = 0
                    
            if len(email_repo) == 0 :
                if not value :
                    stop = 1
                    print "not given email"
                    
            for exist in email_repo :
                if not value :
                    stop = 1
                    print "not given email"
                    break
                else :
                    if stop3==1 :
                        if exist == value[0] :
                            print "same email"
                            stop = 1
                            break
                        
            if stop == 0 :
                if not value :
                    print "not given email"
                    f.write('not given,')
                else :
                    print value[0]
                    email_repo.append(value[0].split(','))
                    f.write(';'.join(value[0].split(',')))
                    f.write(',')
                
                   
                for div in soup.findAll('div', id="viewBtn"):
                    slink = div.find('a')
                    slink2 = slink['onclick']
                    slink3 = slink2.lstrip("makeRequest('")
                    slink4 = slink3.rstrip("',4);$n('#contactDet').show();$n('#viewBtn').hide();")
                    url = str(slink4)
                    rand = random.randint(1, 100) 
                    time.sleep( float(rand)*0.01 )
                                  
                    request2 = urllib2.Request(url, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
                    urlfile2 = urllib2.urlopen(request2)
                    page2 = urlfile2.read().decode('utf-8')
                    soup2 = BeautifulSoup(page2)
                    regex2 = '<div class="cls">(.+?)</p>'
                    pattern2 = re.compile(regex2)
                    value2 = re.findall(pattern2,page2)

                    for j in range(len(value2)):
                        s = str(value2[j]).decode(encoding='UTF-8',errors='strict')
                        s = " ".join(s.split())
                        s = s.replace("<span>","")
                        s = s.replace("</span>","")
                        s = s.replace("<p>","")
                        s = s.replace("</p>","")            
                        value2[j] = s
        
                    recruiter_name = "not given recruiter name"
                    contact_company = "not given contact company"
                           
                    for j in range(len(value2)):
                        if value2[j].find('Recruiter Name') >= 0 :
                            value2[j] = value2[j].replace("Recruiter Name:","")
                            recruiter_name = value2[j]
                        if value2[j].find('Contact Company') >= 0 :
                            value2[j] = value2[j].replace("Contact Company:","")
                            contact_company = value2[j]

                    print recruiter_name
                    print contact_company
                              
                    f.write(recruiter_name)
                    f.write(',')
                    f.write(contact_company)
                    f.write(',')

                    if not url:
                        print "not given url not" 
                        f.write('not given url,')
                    else :
                        print url
                        f.write(url)
                        f.write(',')
                                                
                    if not address:
                        print "not given address"
                        f.write('not given address,\n')
                    else :
                        print address
                        f.write(address)
                        f.write(',\n')                                                
                           
    for hyper in coresoup.findAll('a', id="pageNext"):
        slink_next = hyper['href']
        url_next = str(slink_next)
                           
f.close()

print email_repo
print type(email_repo)

wb = xlwt.Workbook()
ws = wb.add_sheet('data')
with open(file_name, 'rb') as f:
    reader = csv.reader(f)
    for r, row in enumerate(reader):
        for c, col in enumerate(row):
            ws.write(r, c, col)
wb.save(file_name + '.xls')

workbook = xlrd.open_workbook(file_name + '.xls', formatting_info=True, on_demand=True)
wb = xlwt.Workbook()
ws = wb.add_sheet('data')
worksheet = workbook.sheet_by_name('data')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1
while curr_row < num_rows :
    curr_row += 1
    row = worksheet.row(curr_row)
    curr_cell = -1
    while curr_cell < num_cells :
        dont=0
        curr_cell += 1
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        cell_value2 = worksheet.cell_value(curr_row, 0)
        print cell_value2
        
        if cell_value.find('not given') >= 0:
            ws.write_merge(curr_row, curr_row, curr_cell, curr_cell, cell_value, style = xlwt.easyxf('pattern: pattern solid, fore_colour red;'))
            dont=1
        else :
            i=0
            for mail in email_repo :
                if cell_value2 == mail[0] :
                    i+=1
            if i >= 2 :
                ws.write_merge(curr_row, curr_row, curr_cell, curr_cell, cell_value, style = xlwt.easyxf('pattern: pattern solid, fore_colour green;'))
                dont=1
                           
        if dont == 0 :
            ws.write_merge(curr_row, curr_row, curr_cell, curr_cell, cell_value)
        dont=0
        
wb.save(file_name+ "corrected" + '.xls')



            


       











    
       
