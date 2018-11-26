import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

form = '''<!DOCTYPE html>
<title>Currency converter</title>
<form method="GET">
    <label>USD:
        <input name="amount">
    </label>
    <br>
    <button type="submit">Convert</button>
</form>
<label>RUB: {}
</label>
'''
app_id = 'd9c2bf6c2918467d88fab5f3abc8fb1f'

def get_exchange_rate():
    url = "https://openexchangerates.org/api/latest.json?app_id={}".format(app_id)
    response = requests.get(url)
    if response.status_code == 200:
           return response.json()["rates"]['RUB']

class Converter(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        result = ""

        parsed_path = urlparse(self.path)
        queries = parse_qs(parsed_path.query)
        if queries:
            amount = queries["amount"][0]
            result = str(float(amount) * float(get_exchange_rate()))
        mesg = form.format(result)
        self.wfile.write(mesg.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Converter)
    httpd.serve_forever()
