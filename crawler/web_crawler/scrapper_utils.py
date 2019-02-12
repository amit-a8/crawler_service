import requests
import re 
#from bs4 import BeautifulSoup

def process_request_GET(url, payload=None, proxy_credential=None, timeout=None):
    proxy, wait_settings = None, (240, 237)
    if timeout is not None:
        wait_settings = (timeout, timeout+3)
    
    UA_string = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    user_agent = {'User-Agent': UA_string}
    return requests.get(
        url, params=payload, headers=user_agent,
        proxies=proxy, timeout=wait_settings,
        verify=False
    )
