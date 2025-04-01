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
- MODEM_INFO_PATH: The URL for modem information (default: "/RouterStatus.asp")
- MODEM_DATA_URL: The URL for modem data (default: "/DocsisStatus.asp")
- SCRAPE_INTERVAL: The interval for scraping data (default: 60 seconds)'''

from prometheus_client import start_http_server, Gauge
import re
import requests
import time
import urllib.parse
from bs4 import BeautifulSoup
import config


# Configuration
username = config.USERNAME
password = urllib.parse.quote_plus(config.PASSWORD)
http_server_port = config.HTTP_SERVER_PORT
scrape_interval = config.SCRAPE_INTERVAL
modem_login_url = config.MODEM_LOGIN_URL
modem_login_form_url = config.MODEM_LOGIN_FORM_URL
modem_info_url = config.MODEM_INFO_URL
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
    session = requests.Session()
    login_info = session.get(modem_login_url)
    login_info_soup = BeautifulSoup(login_info.text, 'html.parser')
    modem_model = login_info_soup.find('meta', attrs={'name': 'description'}).get('content')
    web_token = login_info_soup.find('input', attrs={'name': 'webToken'}).get('value')
    payload = 'loginUsername=' + username + '&loginPassword=' + password + '&webToken=' + web_token
    authorization_info = session.post(modem_login_form_url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    if authorization_info.status_code != 200:
        print("Login failed")
        return
    modem_info = session.get(modem_info_url)
    if modem_info.status_code != 200:
        print("Failed to retrieve modem information")
        return
    modem_info_soup = BeautifulSoup(modem_info.text, 'html.parser')
    modem_info_tags = modem_info_soup.find_all('script', string=re.compile(r'tagValueList'))
    modem_info_tag_value_lists = []
    for script in modem_info_tags:
        script_text = script.string
        tag_value_list_matches = re.findall(r"var tagValueList\s*=\s*'([^']+)'", script_text)
        for match in tag_value_list_matches:
            modem_info_tag_value_lists.append(match)

    modem_info_raw = modem_info_tag_value_lists[0].split('|')
    vendor = "NETGEAR"
    hardware_version = modem_info_raw[0]
    serial_number = modem_info_raw[2]
    mac_address = modem_info_raw[4]
    firmware_version = modem_info_raw[1]
    cm_ipv4_address = modem_info_raw[6]
    modem_info_gauge.labels(vendor=vendor, model=modem_model, hardware_version=hardware_version,
                            serial_number=serial_number, mac_address=mac_address,
                            firmware_version=firmware_version, cm_ipv4_address=cm_ipv4_address).set(1)

    modem_data = session.get(modem_data_url)
    if modem_data.status_code != 200:
        print("Failed to retrieve modem data")
        return
    modem_data_soup = BeautifulSoup(modem_data.text, 'html.parser')

# Start Prometheus HTTP server
start_http_server(http_server_port)
print("Prometheus metrics server started on port:", http_server_port)

# Main loop to periodically scrape data and update metrics
while True:
    scrape_and_update_metrics()
    time.sleep(scrape_interval)
