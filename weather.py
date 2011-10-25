# -*- coding: utf-8 -*-
import urllib2

def getWeather(city,lang="fi"):
    """
    Returns a string about weather in the selected city.
    Language may be selected with lang attribute.
    """
    url = "http://www.google.com/ig/api?hl="+lang+"&weather=" + urllib2.quote(city)
    try:
        f = urllib2.urlopen(url)
    except:
        return None
    s = f.read()

    clouds = s.split("<current_conditions><condition data=\"")[-1].split("\"")[0]
    temp = s.split("<temp_c data=\"")[-1].split("\"")[0]
    wind = s.split("<wind_condition data=\"")[-1].split("\"")[0]

    if clouds == "<?xml version=":
        return None

    return city+": "+temp+" astetta, "+clouds+", "+wind+"."