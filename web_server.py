import RPi.GPIO as GPIO
import os
import time
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.0.7'  # Change this to your Raspberry Pi IP address
host_port = 8000


class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        html = '''
           <html>
           <body style="width:960px; margin: 20px auto;">
           <h1>Bienvenido a la puerta de mi casa</h1>
           <p>Current GPU temperature is {}</p>
           <p>Turn LED: <a href="/timbrar">Espiche para timbrar</a>
           <script>
               document.getElementById("led-status").innerHTML="{}";
           </script>
           </body>
           </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        status = ''
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        servo1 = GPIO.PWM(11, 50)
        servo1.start(0)
        if self.path=='/':
            servo1.ChangeDutyCycle(2)
            time.sleep(1)
        elif self.path=='/timbrar':
            servo1.ChangeDutyCycle(7)
            time.sleep(3)
            servo1.ChangeDutyCycle(2)
            time.sleep(1)
            servo1.ChangeDutyCycle(0)
            status='Timbrando, porfavor espere'
        else:
            servo1.stop()
            GPIO.cleanup()
            print("Adiós")
        self.wfile.write(html.format(temp[5:], status).encode("utf-8"))


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()