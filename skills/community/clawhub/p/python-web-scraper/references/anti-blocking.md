# Anti-Blocking Strategies

## Rate Limiting

### Proxy rotation (free)
```python
import random

PROXIES = [
    "http://proxy1:8080",
    "http://proxy2:8080",
]

session = requests.Session()
session.proxies = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}
```

### Proxy rotation (paid — recommended for production)
```bash
# Use services like BrightData, SmartProxy, Oxylabs, ScrapingBee
# They handle IP rotation, CAPTCHAs, and headless browsers
```

## User-Agent Rotation

```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/131.0.6778.135 Mobile Safari/537.36",
]

headers = {"User-Agent": random.choice(USER_AGENTS)}
```

## Session & Cookie Persistence

```python
session = requests.Session()
# Add common headers
session.headers.update({
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
})
```

## Detecting Blocking

Check these signals to know if you're being blocked:

1. **HTTP 429** — Too Many Requests → increase delays
2. **HTTP 403** — Forbidden → rotate IP/UA
3. **HTTP 503** — Rate limited server-side → back off
4. **CAPTCHA in response** → need solving service
5. **Empty/placeholder HTML** → JS-rendered or bot detected
6. **Different page title/content** than browser shows → check User-Agent

## Handling CAPTCHAs

```python
# Option 1: 2Captcha service (paid)
# import requests
# response = requests.post('https://2captcha.com/in.php', {
#     'key': 'YOUR_API_KEY',
#     'method': 'base64',
#     'body': image_base64,
# })

# Option 2: Use a scraping API that handles it
# BrightData, ScrapingBee, ScraperAPI — all handle CAPTCHAs

# Option 3: Manual — print CAPTCHA image for human solving
```

## Chrome DevTools Protocol (CDP) Tricks (Selenium)

```python
# Bypass webdriver detection
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });
    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
    });
    """
})
```


## Quick Reference

| Problem | Solution |
|---------|----------|
| 429 Too Many Requests | Add 2-5s delay between requests |
| 403 Forbidden | Rotate User-Agent + IP proxy |
| Empty HTML | Check JS rendering (Selenium) |
| CAPTCHA | Use solving service or scraping API |
| IP banned | Switch proxy/VPN |
| Slow site | Reduce concurrency, increase timeout |
| Login wall | Session cookies + headers |
