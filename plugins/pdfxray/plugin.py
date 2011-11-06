import urlparse, time, urllib2, string, StringIO, csv, shutil, os, json, socket
from lib.malobjclass import *
from lib.object_builder import * 

class pdfxray():
    def __init__(self,mess,bot):
        self._results = None
        self._url = None
        self._fileName = None
        self._dir = "/var/www/pdf_sandbox/files/"
	self._report_dir = "/var/www/pdf_sandbox/reports/"
	self._server_addr = None
        self._text = mess.getBody()
	self._bot = bot
	self._mess = mess
        
        self.parse_input()
        self.download_file()
	self.get_address()
	self.generate_report()
            
    def parse_input(self):
        command,raw_url,format_url = self._text.split(" ")
	self._url = format_url[1:-1]
    
    def download_file(self, fileName=None):
	url = self._url
        self._bot.send_simple_reply(self._mess, "== Downloading PDF ==")
        def getFileName(url,openUrl):
            if 'Content-Disposition' in openUrl.info():
                # If the response has Content-Disposition, try to get filename from it
                cd = dict(map(
                    lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                    openUrl.info().split(';')))
                if 'filename' in cd:
                    filename = cd['filename'].strip("\"'")
                    if filename: return filename
            # if no filename was found above, parse it out of the final URL.
            return os.path.basename(urlparse.urlsplit(openUrl.url)[2])
    
        r = urllib2.urlopen(urllib2.Request(url))
        try:
            self._fileName = fileName or getFileName(url,r)
            with open(self._dir + self._fileName, 'wb') as f:
                shutil.copyfileobj(r,f)
        finally:
            r.close()
            
        self._bot.send_simple_reply(self._mess, "== Downloaded PDF ==")
	
    def get_address(self):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	self._server_addr = s.getsockname()[0]
	s.close()
        
    def generate_report(self):
        self._bot.send_simple_reply(self._mess, "== Creating PDF X-RAY Report ==")
        path = self._dir + self._fileName
	
	output = build_obj(path)
	pdf = jPdf(json.loads(output))
	pdf.make_report(pdf,self._report_dir)
	self._report_url = "http://" + self._server_addr + "/pdf_sandbox/reports/" + pdf.file_md5 + "_report.html"
	self._bot.send_simple_reply(self._mess, "== Report Created ==")
	
    def get_results(self):
	return self._report_url
