# -*- coding: utf-8 -*-
import xbmc, xbmcgui, subprocess, os, time, sys, urllib, re
import xbmcplugin, xbmcaddon
#from urllib import quote_plus

__scriptname__ = "Bluray and 3D players"
__scriptID__      = "plugin.multimedia.players"
__author__ = "Plesken"
__url__ = "http://systems-design.pl"
__credits__ = ""
__addon__ = xbmcaddon.Addon(__scriptID__)

__language__ = __addon__.getLocalizedString
_ = sys.modules[ "__main__" ].__language__

# Shared resources
BASE_RESOURCE_PATH = os.path.join( __addon__.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import xbmc3Dplayer, pLog, connection

#action = ''
_log = pLog.pLog()
movie = xbmc.getInfoLabel("ListItem.FileNameAndPath")

TAB_PREFS = {'prog': 'None',
             'mediainfo': 'None',
             'file1': 'None',
             'file2': 'None',
             'input': 'None',
             'output': 'None',
             'audio': 'None',
             'audnum': 0,
             'subtitle': 'None',
             'subnum': 0,
             'subsize': 0,
             'subenc': 'None',
             'subcolor': 'None',
             'subparallax': 0,
             'switcher': 'false',
             'switcherexp': 'false'}


class Switcher(xbmcgui.WindowXMLDialog):
    def __init__(self, strXMLname, strFallbackPath, strDefaultName, forceFallback=0):
        addon = xbmcaddon.Addon(__scriptID__)
        self.player = xbmc3Dplayer.StereoscopicPlayer()
        self.conn = connection.Connection()
        TAB_PREFS['prog'] = addon.getSetting('player_location')
        TAB_PREFS['mediainfo'] = addon.getSetting('mediainfo_location')
        TAB_PREFS['file1'] = '"' + xbmc.getInfoLabel("ListItem.FileNameAndPath") + '"'
        TAB_PREFS['output'] = self.player.getOutputFormat(addon.getSetting('output_video'))
        TAB_PREFS['audio'] = self.getLang()
        TAB_PREFS['subtitle'] = self.getLang()
        TAB_PREFS['subsize'] = addon.getSetting('subtitle_size')
        TAB_PREFS['subenc'] = addon.getSetting('subtitle_coding')
        TAB_PREFS['subcolor'] =  addon.getSetting('subtitle_color')
        TAB_PREFS['subparallax'] = addon.getSetting('subtitle_parallax')
        TAB_PREFS['switcher'] = addon.getSetting('chooser')
        TAB_PREFS['switcherexp'] = addon.getSetting('chooser_exp')       


    def onInit(self):
        pass
  
    
    def onAction(self, action):
        if action == 1001:
            self.play2D()
        if action == 1002:
            self.play3D()
        if action == 2002:
            self.playBluray(1, movie)
        if action == 2003:
            dialog = xbmcgui.Dialog()
            dialog.ok("XBMC Player Info", "This option is not supported yet.")
            self.close()


  
    def onClick(self, controlID):
        if controlID == 101 or controlID == 201:
            self.onAction(1001)
        if controlID == 102:
            self.onAction(1002)
        if controlID == 202:
            self.onAction(2002)
        if controlID == 203:
            self.onAction(2003)


  
    def onFocus(self, controlID):
        pass


  
    def play2D(self):
        pathMovie = self.conn.connection(movie)
        xbmcPlayer = xbmc.Player()
        if os.path.isfile(pathMovie):
            #xbmc.executebuiltin('XBMC.PlayMedia(' + pathMovie + ')')
            xbmcPlayer.play(movie)
        elif pathMovie != '':
            #xbmc.executebuiltin('XBMC.PlayMedia(' + pathMovie + ')')
            xbmcPlayer.play(movie)
        self.conn.exit(movie)
        self.close()
    
    
    def play3D(self):
        if TAB_PREFS['switcherexp'] == 'true':
            is3DFile = open('/tmp/is3D', 'w')
            is3DFile.write('true')
            is3DFile.close()
        #pathMovie = self.conn.connection(movie)
        #check = self.player.checkFile(self.mediainfoLocation, pathMovie)
        #TAB_PREFS['input'] = self.player.checkFile(TAB_PREFS['mediainfo'], pathMovie)
        ##_log.info('Input video: ' + check)
        if TAB_PREFS['switcherexp'] == 'true':
            xbmcPlayer = xbmc.Player()
        #if check == '':
        #    videoInput = self.inputSettings()
        #    self.player.playStereoUnknown(self.playerLocation, pathMovie, videoInput, self.outputVideo, self.audioLang, self.subtitleLang, self.subtitleSize, self.subtitleCoding, self.subtitleColor, self.subtitleParallax, optExp3D)
        #    if TAB_PREFS['switcherexp'] == 'true':
                #xbmc.executebuiltin('XBMC.PlayMedia(' + pathMovie + ')')
        #        xbmcPlayer.play(pathMovie)
        #else:
        #    self.player.playStereo(self.playerLocation, check, pathMovie, self.outputVideo, self.audioLang, self.subtitleLang, self.subtitleSize, self.subtitleCoding, self.subtitleColor, self.subtitleParallax, optExp3D)
        #    if TAB_PREFS['switcherexp'] == 'true':
                #xbmc.executebuiltin('XBMC.PlayMedia(' + pathMovie + ')')
        #        xbmcPlayer.play(pathMovie)
        #self.conn.exit(movie)
        self.player.playStereo(TAB_PREFS)
        if TAB_PREFS['switcherexp'] == 'true':
            try:
                os.remove('/tmp/is3D')
            except:
                pass
        self.close()
    


    def inputSettings(self):
        videoInput = '2D left'
        format = '2D mono|3D Over/Under|3D HALF Over/Under|3D Side-By-Side|3D HALF Side-By-Side|3D rows|3D Dual Stream'
        menu = format.split('|')
        size_menu = len(menu)
        dialog = xbmcgui.Dialog()
        choice = dialog.select(_(55020), menu)
        for i in range(size_menu):
            if choice == i:
                videoInput = menu[i]
        return videoInput
  
  
    
    def playBluray(self, mode, fileLocation):
        self.close()
        _log.info('Prepare to play bluray')
        bd = xbmcBDplayer.BluRay()
        conn = connection.Connection()
        if mode == 1:
            pathMovie = conn.connection(fileLocation)
            bd.getIntBluRayISO(pathMovie)
        elif mode == 2:
            pathMovie = conn.connection(fileLocation)
            bd.getIntBluRayFile(pathMovie)      
      
  
  
    def getLang(self):
        lang = 'english'
        fileConf = os.getenv("HOME") + '/.xbmc/userdata/guisettings.xml'
        if os.path.isfile(fileConf):
            tmpfile = open(fileConf, 'r').read()
            tabFile = tmpfile.split('\n')
            for line in tabFile:
                expr = re.match(r'^.*?<language>(.*?)</language>.*$', line, re.M|re.I)
                if expr:
                    ll = expr.group(1)
                    lang = ll.lower()
        return lang
  

try:
    os.remove('/tmp/is3D')
except:
    pass
  
extensionFiles = ('.mkv', '.wmv', '.avi', '.mp4', '.mp2', '.m2v', '.mpv', '.mpg', '.ts', '.m2ts', '.rmvb')
extensionISO = ('.iso')
extensionDVD = ('.ifo', '.vob')
extensionBD = ('.bdmv')

if filter(movie.lower().endswith, extensionFiles):
    _log.info('Odpalam')
    switcher = Switcher("switcherFiles.xml", __addon__.getAddonInfo('path'), "Default")
    switcher.doModal()
    del Switcher
elif filter(movie.lower().endswith, extensionISO):
    switcher = Switcher("switcherISO.xml", __addon__.getAddonInfo('path'), "Default")
    switcher.doModal()
    del Switcher  
elif filter(movie.lower().endswith, extensionDVD):
    self.play2D()
elif filter(movie.lower().endswith, extensionBD):
    sw = Switcher("switcherISO.xml", __addon__.getAddonInfo('path'), "Default")
    sw.playBluray(2, movie)
else:
    xbmc.executebuiltin('XBMC.ActivateWindow(' + movie + ')')
