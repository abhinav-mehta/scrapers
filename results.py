import urllib,urllib2
import re
from BeautifulSoup import BeautifulSoup
import string
import easygui as eg
import mechanize
import random
import time
import csv
import urllib

#file_name = eg.filesavebox(msg='Save file')

#f = open(file_name, "w")
                
job_url = "http://jee.iitd.ac.in/resultstatus.php"
print job_url

#rand = random.randint(1, 100) 
#time.sleep( float(rand)*0.01 )
br = mechanize.Browser()
br.set_handle_robots(False)   
br.set_handle_refresh(False)  
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_proxies({"http": "netmon.iitb.ac.in:80"})
br.add_proxy_password("sai.kiran", "bsk=535")
data = {"regno":'7028255'}
searchpage = br.open(job_url, data)
html = searchpage.read()
#br.select_form(nr=0)
#br.form["contact_form"] = '7028255'
#coreurlfile = br.submit()
#corepage = coreurlfile.read()
#coresoup = BeautifulSoup(corepage)

print html
