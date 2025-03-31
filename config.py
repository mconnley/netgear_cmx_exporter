'''config class'''
import os

USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "admin")
HTTP_SERVER_PORT = int(os.getenv("HTTP_SERVER_PORT", "8000"))
SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", "60"))
MODEM_IP_ADDRESS = os.getenv("MODEM_IP_ADDRESS", "192.168.100.1")
MODEM_LOGIN_URL = f"http://{MODEM_IP_ADDRESS}{os.getenv("MODEM_LOGIN_PATH", "/GenieLogin.asp")}"
MODEM_LOGIN_FORM_URL = f"http://{MODEM_IP_ADDRESS}{os.getenv("MODEM_LOGIN_FORM_PATH", "/goform/GenieLogin")}"
MODEM_DATA_URL = f"http://{MODEM_IP_ADDRESS}{os.getenv("MODEM_DATA_PATH", "/DocsisStatus.asp")}"
