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
import shutil
import time
import subprocess


######################### Global Variables:
PluginID            ='plugin.video.mrsvid'
addon               = xbmcaddon.Addon(PluginID)
addonpath           = addon.getAddonInfo('path')
common              = CommonFunctions
mode                = str(sys.argv[1])
DiskBase            = 'D:/temp/disk/videos'
LocalBase           = addon.getSetting('LOCAL_PROTOCOL') + '://' + addon.getSetting('LOCAL_USER') + ':' + addon.getSetting('LOCAL_PASS') + '@' + addon.getSetting('LOCAL_SERVER') + '/' + addon.getSetting('LOCAL_FOLDER')
GlobalBase          = 'ftps://test:test@192.168.1.3/videos'
DownloadBase        = 'D:/temp/downloads/videos'




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
		#listitem.setArt( {'fanart' : 'special://home/addons/plugin.video.mrsvid/resources/art/default-fanart.jpg'})
				
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
			
		if str(extension) == 'jpg' or str(extension) == 'txt' or str(extension) == 'xml' or str(extension) == 'srt' or str(extension) == 'db' or str(extension) == 'cache' or str(extension) == 'ini':  ###### txt for folder comments ! db for thumbs.db which generates automatically by windows!
			return True  
				
		elif '-trailer' in file_name :
			return True
			
		else:
			return False
		
	except :
		return False


		
def SetInfos(path_link,file_name):

	infos = {}	
	title = [file_name]
	nfopath = str(path_link + '/' + file_name + '.xml')
	trailerpath = str(path_link + '/' + file_name + '-trailer.mp4')
	filepath = str(path_link + '/' + file_name )
	
	try:
		x = xbmcvfs.File(nfopath).read() 
		x = common.parseDOM(x, Lang())
		title = common.parseDOM(x, "title")
		
		if title == [] or title == [''] :
			title = [file_name]
		genre = common.parseDOM(x, "genre")
		if genre == [] :
			genre = ['']
		year = common.parseDOM(x, "year")
		if year == [] :
			year = ['']
		director = common.parseDOM(x, "director")
		if director == [] :
			director = ['']
		writer = common.parseDOM(x, "writer")
		if writer == [] :
			writer = ['']
		plot = common.parseDOM(x, "plot")
		if plot == [] :
			plot = ['']
		cast = common.parseDOM(x, "cast")
		if cast == [] :
			cast = ['']
			
		infos = {'Title' : title[0] , 'Genre': genre[0] , 'Year': year[0], 'Cast' : cast , 'Director': director[0], 'Writer': writer[0],'Plot' : plot[0] }
		
		infos.update({'Trailer' : trailerpath })
		infos.update({'size' : xbmcvfs.File(filepath).size() })
		listitem = xbmcgui.ListItem(title[0])
		listitem.setInfo('video' , infos )
		listitem.setProperty('title',title[0])
		listitem.setProperty('size' , str(xbmcvfs.File(filepath).size()/1000000 ) + ' MB' )
		
	except :
		infos.update({'Trailer' : trailerpath })
		infos.update({'size' : xbmcvfs.File(filepath).size() })
		listitem = xbmcgui.ListItem(title[0])
		listitem.setInfo('video', infos )
		listitem.setProperty('title',title[0])
		listitem.setProperty('size' , str(xbmcvfs.File(filepath).size()/1000000 ) + ' MB' )

		
	return listitem
	
	
	
def FileExtension(file_name):

	try:
		extension_pos = file_name.rfind('.')
		extension = file_name[extension_pos+1:]
		return extension
		
	except:
		return 'mp4'
	
	

def SetFileContextMenu(listitem,path_link,file_name):

	try:
		path_url = path_link + '/' + file_name
		contextMenuItems = []
		L = xbmcvfs.listdir(path_link)
		
		if file_name == listitem.getProperty('title'):
			download_args = path_url + "," + DownloadBase + '/' + file_name
		else :
			download_args = path_url + "," + DownloadBase + '/' + listitem.getProperty('title') + '.' + FileExtension(file_name)
		
		contextMenuItems.append(('Play', 'Action(Play)'))
		contextMenuItems.append(('Play from here','XBMC.RunScript(special://home/addons/plugin.video.mrsvid/addon.py,DoFilesQueue,' + path_link +"," + file_name + ")'"))
		
		if FileExtension(file_name)!= 'strm':  ### skip lives!
			filesize = listitem.getProperty('size')
			contextMenuItems.append(('Download [size:%s]' %filesize,'XBMC.RunScript(special://home/addons/plugin.video.mrsvid/addon.py,ToDownload,' + download_args + ")'"))
		
		if file_name +'-trailer.mp4' in L[1]:  
			trailerpath = path_url + '-trailer.mp4'
			contextMenuItems.append(('Watch trailer', 'PlayMedia(' + trailerpath + ")'"))
			
			if file_name == listitem.getProperty('title'):
				trailer_download_args = trailerpath + "," + DownloadBase + '/' + file_name +'-trailer.mp4'
			else:
				trailer_download_args = trailerpath + "," + DownloadBase + '/' + listitem.getProperty('title') + '-trailer.mp4' 
			contextMenuItems.append(('Download trailer', 'XBMC.RunScript(special://home/addons/plugin.video.mrsvid/addon.py,ToDownload,' + trailer_download_args + ")'"))
			
		
		contextMenuItems.append(('Movie information', 'Action(Info)'))
		contextMenuItems.append(('Video section settings', 'Addon.OpenSettings(%s)' % PluginID))
		
		
		listitem.addContextMenuItems(contextMenuItems, replaceItems=True)		
	except:
		pass
		
	return



def SetFolderContextMenu(listitem,path_link,folder_name):

	try:
		contextMenuItems = []
		path_url = path_link + '/' + folder_name
		
		contextMenuItems.append(('Play all','XBMC.RunScript(special://home/addons/plugin.video.mrsvid/addon.py,DoFolderQueue,' + path_url + ")'"))
		contextMenuItems.append(('Video section settings', 'Addon.OpenSettings(%s)' % PluginID))
		
		
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
		filesize = str(xbmcvfs.File(source_file).size()/1000000 ) + ' MB'		
		dp = xbmcgui.DialogProgress()
		dp.create("Downloading File - File size: %s" %filesize,"Destination path:",dest)
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
		li = xbmcgui.ListItem('Disk Videos')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.video.mrsvid/resources/art/DiskVideos-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.video.mrsvid/resources/art/DiskVideos-thumb.jpg'})
		li.addContextMenuItems([('Video section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.video.mrsvid/?folder=DiskVideos&base=' + DiskBase 
		AddDir(plugin_url,li,True)
	except:
		pass
		
	try:
		li = xbmcgui.ListItem('Local Server Videos')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.video.mrsvid/resources/art/LocalServerVideos-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.video.mrsvid/resources/art/LocalServerVideos-thumb.jpg'})
		li.addContextMenuItems([('Video section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.video.mrsvid/?folder=LocalServerVideos&base=' + LocalBase
		AddDir(plugin_url,li,True)
	except:
		pass
		
	try:
		if addon.getSetting('GLOBAL_SERVER') == 'true' :
			li = xbmcgui.ListItem('Global Server Videos')
			#li.setArt( {'fanart' : 'special://home/addons/plugin.video.mrsvid/resources/art/GlobalServerVideos-fanart.jpg'})
			li.setArt( {'thumb' : 'special://home/addons/plugin.video.mrsvid/resources/art/GlobalServerVideos-thumb.jpg'})
			li.addContextMenuItems([('Video section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
			plugin_url = 'plugin://plugin.video.mrsvid/?folder=GlobalServerVideos&base=' + GlobalBase
			AddDir(plugin_url,li,True)
	except:
		pass
	
	try:
		li = xbmcgui.ListItem('Downloads')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.video.mrsvid/resources/art/DownloadVideos-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.video.mrsvid/resources/art/DownloadVideos-thumb.jpg'})
		li.addContextMenuItems([('Video section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.video.mrsvid/?folder=DownloadVideos&base=' + DownloadBase
		AddDir(plugin_url,li,True)
	except:
		pass	
	
	try:
		li = xbmcgui.ListItem('Settings ... ')
		#li.setArt( {'fanart' : 'special://home/addons/plugin.video.mrsvid/resources/art/SettingVideos-fanart.jpg'})
		li.setArt( {'thumb' : 'special://home/addons/plugin.video.mrsvid/resources/art/SettingVideos-thumb.jpg'})
		li.addContextMenuItems([('Video section settings','Addon.OpenSettings(%s)' % PluginID)], replaceItems=True)	
		plugin_url = 'plugin://plugin.video.mrsvid/?folder=SettingVideos' 
		AddDir(plugin_url,li,False)
	except:
		pass
		
	try:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))	
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
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
			
			plugin_url = 'plugin://plugin.video.mrsvid/?folder=' + link + '/' + foldername + '&base=' + base
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
		xbmcgui.Window(10025).setProperty( 'path' ,link) #for insert folder label on the top of video windows (myvideonav.xml)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))	
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		
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
		
	elif folder == 'DiskVideos' or folder == 'LocalServerVideos' or folder == 'GlobalServerVideos' or folder == 'DownloadVideos' :
		CreateFilesFolders('',base)
	
	elif folder == 'SettingVideos':
		xbmc.executebuiltin('Addon.OpenSettings(%s)' % PluginID)
		
	else :
		CreateFilesFolders(folder,base)

##########################################################################################

