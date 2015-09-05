import xbmcaddon
import xbmcgui
import xbmc
import xbmcvfs
import xbmcplugin
import os
import urllib,urllib2,re,cookielib
import string
import urlparse
from BeautifulSoup import BeautifulSoup
import json
from urlparse import urljoin
import jalali
#import collections


addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 
line1 = "Now we are in hijri shamsi month number:"
line2 = "That should be change to string."
line3 = "By Mohamadreza"

day = str(xbmc.getInfoLabel('System.Date(dd)'))
month = str(xbmc.getInfoLabel('System.Date(mm)'))
year = str(xbmc.getInfoLabel('System.Date(yyyy)'))
	
st = str(year+'-'+month+'-'+day)

jl = str(jalali.Gregorian(st).persian_string())
jl_month_l = jl.find('-')+1
jl_month_r = jl.rfind('-')
jl_month = str(jl[jl_month_l:jl_month_r])


xbmcgui.Dialog().ok(addonname,line1,jl_month,line2) 




path = xbmc.translatePath(addon.getAddonInfo('path'))
icon = xbmc.translatePath(os.path.join(path, 'icon.png'))
xbmcgui.Dialog().ok(addon.getAddonInfo('id'),os.path.join(path, 'icon.png'),icon)

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


req = urllib2.Request('http://192.168.1.2/test.html')
resp = opener.open(req)
html_data = resp.read()
#xbmcgui.Dialog().ok(addonname,resp2) 

soup = BeautifulSoup(html_data)
stream = soup.find('source', type='video/mp4')
rec = str(stream) 
rec2 = stream['src']
xbmcgui.Dialog().notification(rec,rec2, xbmcgui.NOTIFICATION_INFO, 15000)


title = "فیلم"
li = xbmcgui.ListItem(title)
li.setInfo( type="Video", infoLabels={"Title" : title})
li.setThumbnailImage(icon)
xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),   url='http://192.168.1.2/123.mp4',    listitem=li,  isFolder=False)	
 
xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))

'''
strr = "salam  paham dastam khoobi "
sp = str(strr.split('m'))
sp2 = str(resp.read() )
sp3 = str(sp2.split ('\n'))
tx = str(strr.rfind('oo'))
len = strr[0:10+1]
 #xbmcgui.Dialog().ok(addonname,strr,"ghg")
xbmcgui.Dialog().notification('Hi',sp3, xbmcgui.NOTIFICATION_INFO, 15000)

for i in range(1,4):
	xbmcgui.Dialog().ok(addonname,'The number is : ' + str(i) ,"yoohoo") 



     try:
        	opener.open(req)
        except urllib2.URLError, ue:
        	print("URL error trying to open playlist")
        	return None
        except urllib2.HTTPError, he:
        	print("HTTP error trying to open playlist")
        	return None

			
'''
			
#dt = xbmc.getInfoLabel('Weather.plugin ')
#xbmcgui.Dialog().ok(addonname, dt, line2, line3) 


"""
xbmc.executebuiltin('Notification("123","hi",5000)')
pth = addon.getAddonInfo('path')
xbmcgui.Dialog().ok("hi", pth, line2, line3) 





myplayer = xbmc.Player()
myplayer.play('http://192.168.1.2/123')
xbmc.sleep(2000)
myplayer.stop()


# xbmc.executebuiltin('xbmc.ejecttray()')

tx = xbmc.getIPAddress()

xbmcgui.Dialog().ok(tx,tx)


d = xbmcgui.Dialog().input('Enter secret code', type=xbmcgui.INPUT_ALPHANUM)

xbmcgui.Dialog().ok(d,d)

progress = xbmcgui.DialogProgress()
progress.create('Progress', 'This is a progress bar.')

i = 0
while i < 11:
    percent = int( ( i / 10.0 ) * 100)
    message = "Message " + str(i) + " out of 10"
    progress.update( percent, "1", message, "2" )
    xbmc.sleep( 5000 )
    if progress.iscanceled():
        break
    i = i + 1

progress.close()

"""


