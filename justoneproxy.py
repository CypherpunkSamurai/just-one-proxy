import re
import requests
import random
from io import BytesIO, SEEK_END, SEEK_SET


# Config
proxy_file_url = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt"
proxy_regex = r'\d+\.\d+\.\d+\.\d+\:\d+'

def _read_32bytes(stream_response) -> str:
    """
        Read the stream bytes content
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

def _get_range(url):
    """
        Returns the Content Size in Bytes
    """
    r = requests.head(url, headers={"Accept-Encoding": "None"})
    if not 'Content-Length' in r.headers:
        #raise Exception("Content Length header not found...")
        return 1024*10
    return int(r.headers['Content-Length'])
    

def get_proxy(url=proxy_file_url):
    # generate a random range
    bytes_range = [ random.choice(range(0, _get_range(url) - 32)) ]
    bytes_range.append(bytes_range[0] + 32)
    #
    print("File Range: %s" % _get_range(url))
    print("Requested Content: %s" % bytes_range)
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
            # Return the proxy
            return proxy[0]
    return None
