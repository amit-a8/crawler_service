from django.shortcuts import render
from django.http import HttpResponse
import requests
import re
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response 


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

def get_webpage_data(url, level=0):
    url_resp = dict()
    try:
        resp = process_request_GET(url)
        text = resp.text
        if resp.status_code != 200:
            print("unable to get response")
            return {}

        title_regex = re.compile("<title>(.*?)</title>")
        h1_regex = re.compile("<h1>(.*?)</h1>")
        url_resp['h1'] = re.findall(h1_regex,text)
        url_resp['title'] = re.findall(title_regex,text)
        url_resp['links'] = re.findall('"((http|ftp)s?://.*?)"', text) 
        return url_resp

    except requests.exceptions.ConnectionError as e:
        print(e)
        return {}
    
    except requests.exceptions.Timeout as e:
        print(e)
        return {}

    except Exception as e: 
        print(e)
        return {}


def url_resp(request):
    try:
        request_data = dict(request.GET)

        url_to_crawl = request_data.get('url')[0]
        depth = request_data.get('depth')[0]
        data = get_webpage_data(url_to_crawl)
        response = Response(data, status=status.HTTP_200_OK)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response
    except Exception as e:
        print(e)
        return HttpResponse("Please provide url and depth in request param")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

