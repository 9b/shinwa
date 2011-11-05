import urlparse, time, urllib2, string, StringIO, csv

class mdl_scanner():
    def __init__(self,mess,bot):
        text = mess.getBody()
        
        bot.send_simple_reply(mess, "== Downloading MDL ==")
        listing = self.get_list(mess,"http://www.malwaredomainlist.com/mdlcsv.php")
        bot.send_simple_reply(mess, "== Downloaded List ==")
        
        bot.send_simple_reply(mess, "== Parsing List ==")
        parsed = self.parse_list(mess,listing)
        bot.send_simple_reply(mess, "== List Parsed ==")
        
        bot.send_simple_reply(mess, "== Checking Blob ==")
        check = self.check_blob(mess,text, parsed)
        
        if len(check) == 0:
            self._results = "No attackers found"
        else:
            self._results = "Following found on the MDL:\n" + ",".join(check)
            
    def get_results(self):
        return self._results
    
    def get_list(self,mess,url):
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()

        data_stream = StringIO.StringIO(data)
        reader = csv.reader(data_stream, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        return reader

    def parse_list(self,mess,listing):
        ips = []
        for row in listing:
            try:
                ip = string.strip(row[2])
                ips.append(ip)
            except:
                continue

        return self.f7(ips)

    def check_blob(self,mess,data, ips):
        check = []
        for ip in ips:	
            if(len(ip) > 4):
                result = data.find(str(ip.strip()))
                if(result >= 0):
                    check.append(ip.strip())

        check = self.f7(check)
        return check

    def f7(self,seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if x not in seen and not seen_add(x)]
