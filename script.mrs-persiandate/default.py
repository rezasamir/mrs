
import xbmc,xbmcgui
import jalali


day = str(xbmc.getInfoLabel('System.Date(dd)'))
month = str(xbmc.getInfoLabel('System.Date(mm)'))
year = str(xbmc.getInfoLabel('System.Date(yyyy)'))
weekday = str(xbmc.getInfoLabel('System.Date(ddd)'))
	
st = str(year+'-'+month+'-'+day)
jl = str(jalali.Gregorian(st).persian_string())  # jl means jalali !!

jl_year_r = jl.find('-')           # find the year in the stirng . e.g : 1394 in 1394-6-25
jl_year = str(jl[0:jl_year_r])

jl_day_l = jl.rfind('-')+1          # find the day in the stirng . e.g : 25 in 1394-6-25
jl_day = str(jl[jl_day_l:])


jl_month_l = jl.find('-')+1                  #####################################################################################
jl_month_r = jl.rfind('-')                   #   Find the number of month in the string . e.g : 1394-6-25 . The output is : 6    #
jl_month = str(jl[jl_month_l:jl_month_r])    #####################################################################################


if jl_month == '1' :
	maah = "فروردین"
elif jl_month == '2' :
	maah = "اردیبهشت"
elif jl_month == '3' :
	maah = "خرداد"
elif jl_month == '4' :
	maah = "تیر"
elif jl_month == '5' :
	maah = "مرداد"
elif jl_month == '6' :
	maah = "شهریور"
elif jl_month == '7' :
	maah = "مهر"
elif jl_month == '8' :
	maah = "آبان"
elif jl_month == '9' :
	maah = "آذر"
elif jl_month == '10' :
	maah = "دی"
elif jl_month == '11' :
	maah = "بهمن"
elif jl_month == '12' :
	maah = "اسفند"
else :
	maah = "" 


		
if weekday == 'Sat' :
	roozehafte = "شنبه"
elif weekday == 'Sun' :
	roozehafte = "یکشنبه"
elif weekday == 'Mon' :
	roozehafte = "دوشنبه"
elif weekday == 'Tue' :
	roozehafte = "سه شنبه"
elif weekday == 'Wed' :
	roozehafte = "چهارشنبه"
elif weekday == 'Thu' :
	roozehafte = "پنج شنبه"
elif weekday == 'Fri' :
	roozehafte = "جمعه"
else :
	roozehafte = weekday



xbmcgui.Window(10000).setProperty( 'tarikh' , roozehafte + ' ' + jl_day + ' ' + maah + ' ' + jl_year )  # set the 'tarikh' property for home windows (Home.xml)








