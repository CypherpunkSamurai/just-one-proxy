# just-one-proxy
A Python module that will fetch only one proxy from any raw online file

## Why?

I often require a lot of proxies in my api code, a few providers dont allow downloading to hdd. Thus in memory proxy tool was required. Problem being those tools often provide unchecked proxies.

This module was created as a proof-of-concept tool. Getting a proxy often requires downloading a proxy list, this tool reads random bytes from raw text files online (mostly for github public proxies).

## How to Use
1. Clone the repo / Download the `justoneproxy.py` file.
2. import it using
```python
import justoneproxy
```
3. Ask justoneproxy to get a proxy using the `get_proxy(url)` method.
```python
# url is optional

proxy_list_url = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"
proxy = justoneproxy.get_proxy(proxy_list_url)
print(proxy)
```

## Known Bugs
- [ ] Proxy Lists with less content sizes throw errors.
    Currently the range function uses random integers instead of getting the target file size. The patch will be rolled out.
    
- [ ] Tell Me?

## Credits
- Python3
- Requests Documentation
