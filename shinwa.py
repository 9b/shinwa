from jabberbot import JabberBot, botcmd
import traceback
import simplejson as json
import os, sys, zipfile, getopt, traceback, socket
import logging

class ShinwaBot(JabberBot):

    def __init__( self, jid, password, res = None):
        super( ShinwaBot, self).__init__( jid, password, res)
        # create console handler
        chandler = logging.StreamHandler()
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to handler
        chandler.setFormatter(formatter)
        # add handler to logger
        self.log.addHandler(chandler)
        # set level to INFO
        self.log.setLevel(logging.INFO)

        self.users = []
        self.message_queue = []                                                                               
        self.thread_killed = False

    @botcmd
    def mdl_scan(self, mess, args):
        """Scan text for matching IP addresses from the MDL"""

        try:
            from plugins.mdl_scanner import mdl_scanner
        except:
            return "Module failed to load"
        
        obj = mdl_scanner(mess,self)
        return obj.get_results()

    @botcmd
    def translang(self, mess, args):
        """Translate text using Google Translate"""

        try:
            from plugins.translang import translang
        except:
            return "Module failed to load"
        
        obj = translang(mess,self)
        return obj.get_results()

username = 'shinwa@goldfoil'
password = 'password'
bot = ShinwaBot(username,password)
bot.serve_forever()
