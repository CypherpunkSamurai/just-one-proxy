import re
import requests
import random
from io import BytesIO, SEEK_END, SEEK_SET


# Config
proxy_file_url = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"
proxy_regex = r'\d+\.\d+\.\d+\.\d+\:\d+'

def _read_32bytes(stream_response) -> str:
    """
        Read the stream bytes content
        
        This reads 32 bytes from the response stream
    """
    # 
    content_bytes = BytesIO()
    # Get the content starting offset
    _start = content_bytes.tell()
    _bytes_to_read = 32
    _end = _start + _bytes_to_read
    # read
    _current = content_bytes.seek(0, SEEK_END)
    while(_current < _end):
        try:
            _current += content_bytes.write(next(stream_response))
        except StopIteration:
            break
    # seek to start
    content_bytes.seek(_start)
    # return the bytes
    return content_bytes.read(_bytes_to_read).decode('utf-8')
    

def get_proxy(url=proxy_file_url):
    """
      Syntax:
          get_proxy(url="your_raw_git_file_url")
        
        Retuns:
          "192.168.0.0:5000"
    """
    # generate a random range
    bytes_range = [ random.choice(range(1,9)) * (10**random.choice(range(0,5))) ]
    bytes_range.append(bytes_range[0] + 32)
    # set range
    headers = {
        "Range": "bytes=%s-%s" % (bytes_range[0], bytes_range[1]),
        "Accept-Encoding": "None", # important
    }
    # Stream the Response
    with requests.get(url, headers=headers, stream=True) as r:
        chunk_size = 64
        content = _read_32bytes(r.iter_content(chunk_size))
    # parse proxy from the content
    if content:
        proxy = re.findall(proxy_regex, content)
        if proxy:
            return proxy[0]
    return None
