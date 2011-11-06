from urllib2 import urlopen
from urllib import urlencode
import sys, json

class translang():
    def __init__(self,mess,bot):
        self._key = "AIzaSyAUS1tZRU3e4hTbVDmacJLoDLdZW8_EeIE"
        self._target = None
        self._q = None
        self._translated = None
        self._text = mess.getBody()
        
        self.parse_input()
        self.translate()
        
    def get_results(self):
        return self._translated
        
    def parse_input(self):
        command,self._q,self._target = self._text.split("\"")
        self._target = self._target.lstrip()
           
    def translate(self):
        base_url = "https://www.googleapis.com/language/translate/v2?"
        params = urlencode(( ('key',self._key),('target',self._target),('q',self._q) ))
        url = base_url + params
        content = urlopen(url).read()
        
        try:
            trans_dict = json.loads(content)
        except AttributeError:
            trans_dict = json.read(content)
            
        data = trans_dict.get("data")
        translations = data.get("translations")
        self._translated = translations[0].get("translatedText")
