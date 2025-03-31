'''cm_exporter.py
This script scrapes modem data from a web interface and exposes it to Prometheus.
It uses the requests library to handle HTTP requests and BeautifulSoup for parsing HTML.
It requires the following environment variables to be set:
- USERNAME: The username for modem login (default: "admin")
- PASSWORD: The password for modem login (default: "admin")
- HTTP_SERVER_PORT: The port for the HTTP server (default: 8000)
- MODEM_IP_ADDRESS: The IP address of the modem (default: 192.168.100.1)
- MODEM_LOGIN_PATH: The URL for modem login (default: "/GenieLogin.asp")
- MODEM_LOGIN_FORM_PATH: The URL for modem login form submission (default: "/goform/GenieLogin")
- MODEM_DATA_URL: The URL for modem data (default: "/DocsisStatus.asp")
- SCRAPE_INTERVAL: The interval for scraping data (default: 60 seconds)'''

from prometheus_client import start_http_server, Gauge
import re
import requests
from requests.auth import HTTPBasicAuth
import time
from bs4 import BeautifulSoup
import config


# Configuration
username = config.USERNAME
password = config.PASSWORD
http_server_port = config.HTTP_SERVER_PORT
scrape_interval = config.SCRAPE_INTERVAL
modem_login_url = config.MODEM_LOGIN_URL
modem_login_form_url = config.MODEM_LOGIN_FORM_URL
modem_data_url = config.MODEM_DATA_URL

# Prometheus metrics for modem information
modem_info_gauge = Gauge('modem_info', 'Modem Information',
                         ['vendor', 'model', 'hardware_version', 'serial_number', 'mac_address', 'firmware_version', 'cm_ipv4_address'])
downstream_frequency_gauge = Gauge('downstream_frequency', 'Downstream Frequency', ['channel', 'mac_address'])
downstream_power_gauge = Gauge('downstream_power', 'Downstream Power', ['channel', 'mac_address'])
downstream_snr_gauge = Gauge('downstream_snr', 'Downstream SNR', ['channel', 'mac_address'])
upstream_power_gauge = Gauge('upstream_power', 'Upstream Power', ['channel', 'mac_address'])
upstream_frequency_gauge = Gauge('upstream_frequency', 'Upstream Frequency', ['channel', 'mac_address'])
upstream_symbol_rate_gauge = Gauge('upstream_symbol_rate', 'Upstream Symbol Rate', ['channel', 'mac_address'])


def scrape_and_update_metrics():
    '''update the Prometheus metrics by scraping the modem data'''



# Start Prometheus HTTP server
start_http_server(http_server_port)
print("Prometheus metrics server started on port:", http_server_port)

# Main loop to periodically scrape data and update metrics
while True:
    scrape_and_update_metrics()
    time.sleep(scrape_interval)
