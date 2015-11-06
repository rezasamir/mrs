import xbmcaddon
import xbmcgui
import xbmc
import xbmcvfs
import xbmcplugin
import os
import sys
import urllib,urllib2,re,cookielib
import string
import urlparse
#from BeautifulSoup import BeautifulSoup
import json
from urlparse import urljoin
#import jalali
import collections
import codecs
import CommonFunctions 
import urllib2
import shutil
import time
import subprocess


######################### Global Variables:
PluginID            ='plugin.image.mrspic'
addon               = xbmcaddon.Addon(PluginID)
addonpath           = addon.getAddonInfo('path')
common              = CommonFunctions
mode                = str(sys.argv[1])
DiskBase            = 'D:/temp/disk/pictures'
LocalBase           = addon.getSetting('LOCAL_PROTOCOL') + '://' + addon.getSetting('LOCAL_USER') + ':' + addon.getSetting('LOCAL_PASS') + '@' + addon.getSetting('LOCAL_SERVER') + '/' + addon.getSetting('LOCAL_FOLDER')
GlobalBase          = 'ftps://test:test@192.168.1.3/pictures'
DownloadBase        = 'D:/temp/downloads/pictures'




def ExecuteBat(script_file):

	try:
		file = script_file
		scriptpath = addonpath + '/resources/scripts/' + file
		xbmc.executebuiltin("System.Exec(%s)" %scriptpath)
		return True
	except:
		xbmcgui.Dialog().ok('ERROR','Unable to execute some scripts!')
		return False
	
	

def Lang():

	try : 
		current_lang = str(xbmc.getInfoLabel('System.Language')) 
		en = 'English (US)'
		fa = 'Persian (Iran)'
		ar = 'Arabic'

		if current_lang == en :
			langselected = 'en'
		elif current_lang == fa :
			langselected = 'fa'
		elif current_lang == ar :
			langselected = 'ar'
		else :
			langselected = 'en'

		return langselected
		
	except :
		
		return  'en'

		
		
def SetFolderThumb(listitem, path_link, folder_name ):

	try:
		thumbpath = str(path_link + '/' + folder_name + '/' + 'folder-thumb.jpg')
		dir_list = xbmcvfs.listdir(path_link + '/' + folder_name)
		
		if 'folder-thumb.jpg' in dir_list[1] :
				listitem.setArt({ 'thumb': thumbpath})
				
	except :
		xbmcgui.Dialog().ok('ERROR','Fail to set Folder Thumbnail!')
		
	return		

	

def SetFolderFanart(listitem, path_link, folder_name ):

	try:
		fanartpath = str(path_link + '/' + folder_name + '/' + 'folder-fanart.jpg')
		dir_list = xbmcvfs.listdir(path_link + '/' + folder_name)
		
		if 'folder-fanart.jpg' in dir_list[1] :
				listitem.setArt({ 'fanart': fanartpath})
				
	except :
		xbmcgui.Dialog().ok('ERROR','Fail to set Folder Fanart!')
	return		


	
def SetFileThumb(listitem, path_link, file_name ):

	try:
		thumbpath = str(path_link + '/' + file_name + '-thumb.jpg')
		dir_list = xbmcvfs.listdir(path_link)
		
		if file_name+'-thumb.jpg' in dir_list[1] :
				listitem.setArt({ 'thumb': thumbpath})
				
	except :
		xbmcgui.Dialog().ok('ERROR','Fail to set File Thumbnail!')
	return		


	
def SetFileFanart(listitem, path_link, file_name ):

	try:
		fanartpath = str(path_link + '/' + file_name + '-fanart.jpg')
		dir_list = xbmcvfs.listdir(path_link)
		
		if file_name+'-fanart.jpg' in dir_list[1] :
				listitem.setArt({ 'fanart': fanartpath})
		#else :     #### for default fanart set!
		#listitem.setArt( {'fanart' : 'special://home/addons/plugin.image.mrspic/resources/art/default-fanart.jpg'})
				
	except :
		xbmcgui.Dialog().ok('ERROR','Fail to set File Thumbnail!')
	return	
	
	
	
def SetFoldersName(path_link, folder_name ):

	try:
		foldersname_path = str(path_link + '/' + 'folders-name.xml')
		x = xbmcvfs.File(foldersname_path).read() 
		x = common.parseDOM(x,Lang())
		x = common.parseDOM(x,folder_name)
		if x[0] == '' :
			listitem = xbmcgui.ListItem(folder_name)
		else:
			listitem = xbmcgui.ListItem(x[0])
	except :
			listitem = xbmcgui.ListItem(folder_name)	
			
	return	listitem	


	
def AddDir(link, li, is_folder):

	try:
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),  url=link, listitem=li,  isFolder=is_folder)
	except:
		xbmcgui.Dialog().ok('ERROR','Fail to retrieve directories!')
	
	return

	
	
def BadExtension(file_name):

	try:
		extension_pos = file_name.rfind('.')
		extension = file_name[extension_pos+1:]
			
		if  str(extension) == 'txt' or str(extension) == 'xml' or str(extension) == 'srt' or str(extension) == 'db' :  ###### txt for folder comments ! db for thumbs.db which generates automatically y windows!
			return True  
				
		elif '-trailer' in file_name :
			return True
		
		elif '-fanart' in file_name :
			return True
		
		elif '-thumb' in file_name :
			return True
			
		else:
			return False
		
	except :
		return False


		
def SetInfos(path_link,file_name):

	infos = {}	
	title = [file_name]
	nfopath = str(path_link + '/' + file_name + '.xml')
	
	try:
		x = xbmcvfs.File(nfopath).read() 
		x = common.parseDOM(x, Lang())
		title = common.parseDOM(x, "title")
		
		if title == [] or title == [''] :
			title = [file_name]
		comment = common.parseDOM(x, "comment")
		if comment == [] :
			comment = ['']
		
			
		#infos = {'Title' : title[0] , 'exif:resolution': '720,480' }
		infos = {'Title' : title[0] }
		
		listitem = xbmcgui.ListItem(title[0])
		listitem.setInfo('pictures', infos )
		listitem.setProperty('title',title[0])
		#xbmcgui.Dialog().ok('ERROR',listitem.getLabel2())

		
	except :
		listitem = xbmcgui.ListItem(title[0])
		listitem.setInfo('pictures', infos )
		listitem.setProperty('title',title[0])

		
	return listitem
	
	
	
def FileExtension(file_name):

	try:
		extension_pos = file_name.rfind('.')
		extension = file_name[extension_pos+1:]
		return extension
		
	except:
		return 'jpg'
	
	

def SetFileContextMenu(listitem,path_link,file_name):

	try:
		path_url = path_link + '/' + file_name
		contextMenuItems = []
		L = xbmcvfs.listdir(path_link)
		
		if file_name == listitem.getProperty('title'):
			download_args = path_url + "," + DownloadBase + '/' + file_name
		else :
			download_args = path_url + "," + DownloadBase + '/' + listitem.getProperty('title') + '.' + FileExtension(file_name)
		
		contextMenuItems.append(('Show', 'Action(Play)'))
		#contextMenuItems.append(('Play from here','XBMC.RunScript(special://home/addons/plugin.image.mrspic/addon.py,DoFilesQueue,' + path_link +"," + file_name + ")'"))
		
		if FileExtension(file_name)!= 'strm':  ### skip lives!
			contextMenuItems.append(('Download','XBMC.RunScript(special://home/addons/plugin.image.mrspic/addon.py,ToDownload,' + download_args + ")'"))
		
		if file_name +'-trailer.mp4' in L[1]:  
			trailerpath = path_url + '-trailer.mp4'
			contextMenuItems.append(('Watch trailer', 'PlayMedia(' + trailerpath + ")'"))
			
			if file_name == listitem.getProperty('title'):
				trailer_download_args = trailerpath + "," + DownloadBase + '/' + file_name +'-trailer.mp4'
			else:
				trailer_download_args = trailerpath + "," + DownloadBase + '/' + listitem.getProperty('title') + '-trailer.mp4' 
			contextMenuItems.append(('Download trailer', 'XBMC.RunScript(special://home/addons/plugin.image.mrspic/addon.py,ToDownload,' + trailer_download_args + ")'"))
			
		
		contextMenuItems.append(('File information', 'Action(Info)'))
		contextMenuItems.append(('Picture section settings', 'Addon.OpenSettings(%s)' % PluginID))
		
		
		listitem.addContextMenuItems(contextMenuItems, replaceItems=True)		
	except:
		pass
		
	return



def SetFolderContextMenu(listitem,path_link,folder_name):

	try:
		contextMenuItems = []
		path_url = path_link + '/' + folder_name
		
		#contextMenuItems.append(('Play all','XBMC.RunScript(special://home/addons/plugin.image.mrspic/addon.py,DoFolderQueue,' + path_url + ")'"))
		contextMenuItems.append(('Picture section settings', 'Addon.OpenSettings(%s)' % PluginID))
		
		
		listitem.addContextMenuItems(contextMenuItems, replaceItems=True)		
	except:
		pass
		
	return


	
def FileExists(file):

	try:
		if xbmcvfs.exists(dest) :
			xbmcgui.Dialog().ok('Unable to download','The destination file exists!','Please rename or delete the existing file and try again.')
			return True
		
		else:
			return False
		
	except:
		xbmcgui.Dialog().ok('Unable to download','The destination file not exists or access is denied!')
		return True


		
def DoDownload(source_file,destination_file):
	
	try:
		if FileExists(destination_file):
			return
			
		dp = xbmcgui.DialogProgress()
		dp.create("Downloading File","Destination path:",dest)
		sf = xbmcvfs.File(source_file)
		df = xbmcvfs.File(destination_file,'wb')
		source_size = int(sf.size())
		chunk = (source_size / 100) + 100
		count = 1
		while count <= 100 :
			buffer = sf.readBytes(chunk)
			df.write(buffer)
			dp.update(count)
			count += 1
			if dp.iscanceled():
				ret = xbmcgui.Dialog().yesno('Warning!', 'Are you sure to cancel the download?')
				if ret :
					break	
				else:
					dp.close()
					dp.create("Downloading File","Destination path:",dest)	
					
		dp.close()
					
		if df.size() > 0 and sf.size() == df.size():
			xbmcgui.Dialog().ok('Successful Download','Download finished successfully.','Destination path: ' + dest )
			df.close()
		else :
			xbmcgui.Dialog().ok('Fail to download','Download failed!')
			df.close()
			try:
				xbmcvfs.delete(destination_file)
			except:
				xbmcgui.Dialog().ok('Error!','Fail to delete the temporary file! Please delete this file manually.','File path: '+ dest)
		sf.close()
		
		return
		
	except:
		xbmcgui.Dialog().ok('Fail to download','Download failed!','Please try again.')
		return

		

def FilesQueue(path_link,file_name):
	
	try:
		L = xbmcvfs.listdir(path_link)
		pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		pl.clear()
		result_pos = -1
		position = 0
		for file in L[1]:
			if BadExtension(file):
				continue
			if file == 	file_name :
				result_pos = position
				
			path_url = path_link + '/' + file
			li = SetInfos(path_link,file)
			pl.add(path_url,li)
			position += 1
			
		xbmc.Player().play(pl,startpos = result_pos)
		
	except:
		pass
	
	return	



def FolderQueue(path_link):
	
	try:
		L = xbmcvfs.listdir(path_link)
		pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		pl.clear()
		result_pos = -1
		for file in L[1]:
			if BadExtension(file):
				continue
				
			path_url = path_link + '/' + file
			li = SetInfos(path_link,file)
			pl.add(path_url,li)
			
		xbmc.Player().play(pl,startpos = result_pos)
		
	except:
		pass
	
	return	



def CreateRoot():
	
	try:
		li = xbmcgui.ListItem('Disk Pictures')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.image.mrspic/resources/art/DiskPictures-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.image.mrspic/resources/art/DiskPictures-thumb.jpg'})
		li.addContextMenuItems([('Picture section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.image.mrspic/?folder=DiskPictures&base=' + DiskBase 
		AddDir(plugin_url,li,True)
	except:
		pass
		
	try:
		li = xbmcgui.ListItem('Local Server Pictures')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.image.mrspic/resources/art/LocalServerPictures-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.image.mrspic/resources/art/LocalServerPictures-thumb.jpg'})
		li.addContextMenuItems([('Picture section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.image.mrspic/?folder=LocalServerPictures&base=' + LocalBase
		AddDir(plugin_url,li,True)
	except:
		pass
		
	try:
		if addon.getSetting('GLOBAL_SERVER') == 'true' :
			li = xbmcgui.ListItem('Global Server Pictures')
			#li.setArt( {'fanart' : 'special://home/addons/plugin.image.mrspic/resources/art/GlobalServerPictures-fanart.jpg'})
			li.setArt( {'thumb' : 'special://home/addons/plugin.image.mrspic/resources/art/GlobalServerPictures-thumb.jpg'})
			li.addContextMenuItems([('Picture section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
			plugin_url = 'plugin://plugin.image.mrspic/?folder=GlobalServerPictures&base=' + GlobalBase
			AddDir(plugin_url,li,True)
	except:
		pass
	
	try:
		li = xbmcgui.ListItem('Downloads')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.image.mrspic/resources/art/DownloadPictures-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.image.mrspic/resources/art/DownloadPictures-thumb.jpg'})
		li.addContextMenuItems([('Picture section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.image.mrspic/?folder=DownloadPictures&base=' + DownloadBase
		AddDir(plugin_url,li,True)
	except:
		pass
		
	try:
		li = xbmcgui.ListItem('Settings ... ')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.image.mrspic/resources/art/SettingPictures-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.image.mrspic/resources/art/SettingPictures-thumb.jpg'})
		li.addContextMenuItems([('Picture section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.image.mrspic/?folder=SettingPictures' 
		AddDir(plugin_url,li,False)
	except:
		pass
		
	try:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))	
		xbmcplugin.setContent(int(sys.argv[1]), 'files')
	except:
		xbmcgui.Dialog().ok('ERROR','Fail to construct root menu!')
		
	return
	

	
def CreateFilesFolders(link,base):

	try:
		path = base + link
		L = xbmcvfs.listdir(path)
		common = CommonFunctions
		
	except:	
		xbmcgui.Dialog().ok('ERROR','Fail to connect to server!')
		return
		
	try:
	
		for foldername in L[0] :
								
			li = SetFoldersName(path,foldername)
			SetFolderThumb(li,path,foldername)	
			SetFolderFanart(li,path,foldername)
			SetFolderContextMenu(li,path,foldername)
		
			
			plugin_url = 'plugin://plugin.image.mrspic/?folder=' + link + '/' + foldername + '&base=' + base
			AddDir(plugin_url,li,True)	
			
			
			
	except:
		xbmcgui.Dialog().ok('ERROR','Fail retrieve folders!')	
		pass
	
	try:
		
		for filename in L[1] :
			
			if BadExtension(filename):
				continue 
				
			li = SetInfos(path,filename)
			SetFileThumb(li,path,filename)
			SetFileFanart(li,path,filename)	
			SetFileContextMenu(li,path,filename)
			
			path_url = path + '/' + filename
			AddDir(path_url,li,False)
			

			
	except:
		xbmcgui.Dialog().ok('ERROR','Fail retrieve files!')	
		pass
	
	try:
		
		xbmcplugin.endOfDirectory(int(sys.argv[1]))	
		xbmcplugin.setContent(int(sys.argv[1]), 'files')
		
	except:
		xbmcgui.Dialog().ok('ERROR','Fail to build list!')
		pass
	
	return	

	
####### main ######
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

#ExecuteBat('hfs.exe')

try:
    folder = params['folder']
except:
    folder = ''
	
try:
    base = params['base']
except:
    base = ''
	
#folder = str(sys.argv[2][8:]).replace ('%2f' , '/' ).replace('%20',' ')
#folder = urllib2.unquote(folder)

	
	
if mode == 'ToDownload':
	source   = str(sys.argv[2])
	dest     = str(sys.argv[3])
	DoDownload(source,dest)		
		
elif mode == 'DoFilesQueue':
	queue_path      = str(sys.argv[2])
	queue_filename  = str(sys.argv[3])
	FilesQueue(queue_path,queue_filename)

elif mode == 'DoFolderQueue':
	queue_path      = str(sys.argv[2])
	FolderQueue(queue_path)


else:
	
	if folder == '':
		CreateRoot()
		
	elif folder == 'DiskPictures' or folder == 'LocalServerPictures' or folder == 'GlobalServerPictures' or folder == 'DownloadPictures' :
		CreateFilesFolders('',base)
	
	elif folder == 'SettingPictures':
		xbmc.executebuiltin('Addon.OpenSettings(%s)' % PluginID)
		
	else :
		CreateFilesFolders(folder,base)

##########################################################################################

