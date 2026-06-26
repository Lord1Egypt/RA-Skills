# Threat Intelligence APIs Reference

This document lists available threat intelligence APIs for Skill Scan integration.

## Free APIs (No API Key Required)

### Abuse.ch URLhaus

**Purpose**: Check if a domain/IP is associated with malware distribution

**API Endpoint**: `https://urlhaus-api.abuse.ch/v1/host/`

**Example Usage**:
```python
import urllib.request
import urllib.parse
import json

def check_urlhaus(host):
    url = "https://urlhaus-api.abuse.ch/v1/host/"
    data = urllib.parse.urlencode({"host": host}).encode()
    req = urllib.request.Request(url, data)
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            if result.get("query_status") == "ok" and result.get("abuse_confidence"):
                return {"status": "malicious", "source": "abuse.ch"}
    except Exception as e:
        print(f"Error: {e}")
    
    return {"status": "unknown"}
```

**Rate Limits**: None documented (be respectful)

**Documentation**: https://urlhaus-api.abuse.ch/

---

### AbuseIPDB

**Purpose**: IP address reputation checking

**API Endpoint**: `https://api.abuseipdb.com/api/v2/check`

**Authentication**: API Key required (free tier available)

**Example Usage**:
```python
import requests

def check_abuseipdb(ip, api_key):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        'Key': api_key,
        'Accept': 'application/json'
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }
    
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    
    if data['data'].get('abuseConfidenceScore', 0) > 50:
        return {"status": "suspicious", "score": data['data']['abuseConfidenceScore']}
    
    return {"status": "clean"}
```

**Rate Limits**: 1,000 requests/day (free tier)

**Get API Key**: https://www.abuseipdb.com/api

---

## Free APIs (API Key Required)

### VirusTotal

**Purpose**: Comprehensive malware/URL/domain scanning

**API Endpoint**: `https://www.virustotal.com/api/v3/domains/{domain}`

**Authentication**: API Key required

**Example Usage**:
```python
import requests

def check_virustotal(domain, api_key):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {
        'x-apikey': api_key
    }
    
    resp = requests.get(url, headers=headers)
    data = resp.json()
    
    stats = data['data']['attributes']['last_analysis_stats']
    malicious = stats.get('malicious', 0)
    
    if malicious > 0:
        return {"status": "malicious", "malicious_count": malicious}
    
    return {"status": "clean"}
```

**Rate Limits**: 
- Free: 4 requests/minute, 500 requests/day
- Premium: Higher limits

**Get API Key**: https://www.virustotal.com/gui/join-us

---

### AlienVault OTX

**Purpose**: Open threat intelligence sharing platform

**API Endpoint**: `https://otx.alienvault.com/api/v1/indicators/domain/{domain}`

**Authentication**: API Key required

**Example Usage**:
```python
import requests

def check_otx(domain, api_key):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general"
    headers = {
        'X-OTX-API-KEY': api_key
    }
    
    resp = requests.get(url, headers=headers)
    data = resp.json()
    
    if data.get('pulse_info', {}).get('count', 0) > 0:
        return {"status": "suspicious", "pulses": data['pulse_info']['count']}
    
    return {"status": "unknown"}
```

**Rate Limits**: Varies by account type

**Get API Key**: https://otx.alienvault.com/accounts/register

---

### Google Safe Browsing

**Purpose**: Check if a URL is flagged as unsafe by Google

**API Endpoint**: `https://safebrowsing.googleapis.com/v4/threatMatches:find`

**Authentication**: API Key required

**Example Usage**:
```python
import requests

def check_safebrowsing(url, api_key):
    endpoint = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {
        "client": {
            "clientId": "skill-scan",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    
    resp = requests.post(f"{endpoint}?key={api_key}", json=payload)
    data = resp.json()
    
    if 'matches' in data:
        return {"status": "malicious", "threats": data['matches']}
    
    return {"status": "clean"}
```

**Rate Limits**: 10,000 requests/day (free tier)

**Get API Key**: https://developers.google.com/safe-browsing/v4/get-started

---

## Local Blacklists

### Built-in Domain Blacklist

Maintain a local list of known malicious domains:

```python
BLACKLIST_DOMAINS = [
    "malware.com",
    "evil.com",
    # Add more as discovered
]

def check_local_blacklist(domain):
    if domain in BLACKLIST_DOMAINS:
        return {"status": "malicious", "source": "local_blacklist"}
    return {"status": "unknown"}
```

### Update Sources

- https://github.com/StevenBlack/hosts
- https://github.com/PolishFiltersTeam/KADhosts
- https://github.com/AdAway/adaway.github.io

---

## API Integration Strategy

### Recommended Flow

```python
def comprehensive_check(domain, api_keys):
    results = {}
    
    # 1. Check local blacklist (fastest)
    results['local'] = check_local_blacklist(domain)
    if results['local']['status'] == 'malicious':
        return results
    
    # 2. Check free APIs (no auth)
    results['urlhaus'] = check_urlhaus(domain)
    if results['urlhaus']['status'] == 'malicious':
        return results
    
    # 3. Check authenticated APIs (slower)
    if api_keys.get('virustotal'):
        results['virustotal'] = check_virustotal(domain, api_keys['virustotal'])
    
    if api_keys.get('abuseipdb'):
        # Extract IP from domain first
        ip = resolve_domain(domain)
        results['abuseipdb'] = check_abuseipdb(ip, api_keys['abuseipdb'])
    
    # 4. Aggregate results
    return aggregate_results(results)

def aggregate_results(results):
    malicious_count = sum(1 for r in results.values() if r.get('status') == 'malicious')
    
    if malicious_count > 0:
        return {"status": "malicious", "details": results}
    elif any(r.get('status') == 'suspicious' for r in results.values()):
        return {"status": "suspicious", "details": results}
    else:
        return {"status": "clean", "details": results}
```

---

## Best Practices

1. **Rate Limiting**: Respect API
   - Add delays between requests
   - Cache results when possible

2. **Error Handling**: Handle API failures gracefully
   - Timeouts
   - Rate limit responses (429)
   - Invalid responses

3. **Privacy**: Don't send sensitive domains to third-party APIs
   - Use local checks for internal domains
   - Consider self-hosted threat intel

4. **Updates**: Keep blacklists and patterns updated
   - Schedule regular updates
   - Subscribe to threat intel feeds

---

## Configuration Example

Create a config file at `~/.skill-scan/config.json`:

```json
{
  "api_keys": {
    "virustotal": "YOUR_VT_API_KEY",
    "abuseipdb": "YOUR_ABUSEIPDB_API_KEY",
    "otx": "YOUR_OTX_API_KEY",
    "safebrowsing": "YOUR_GOOGLE_API_KEY"
  },
  "settings": {
    "timeout": 5,
    "cache_results": true,
    "cache_ttl": 86400,
    "rate_limit_delay": 1
  }
}
```

Load in script:

```python
import json
import os

def load_config():
    config_path = os.path.expanduser("~/.skill-scan/config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {"api_keys": {}, "settings": {}}
```

---

## Testing

Test API integrations:

```bash
# Test URLhaus
curl -X POST https://urlhaus-api.abuse.ch/v1/host/ \
  -d "host=google.com"

# Test VirusTotal (replace API_KEY)
curl --request GET \
  --url https://www.virustotal.com/api/v3/domains/google.com \
  --header 'x-apikey: API_KEY'
```

---

## Contributing Threat Intel

If you discover malicious domains:

1. **Report to Abuse.ch**: https://abuse.ch/report/
2. **Report to AbuseIPDB**: https://www.abuseipdb.com/report
3. **Report to VirusTotal**: https://www.virustotal.com/gui/file/upload
4. **Add to local blacklist**: Submit PR to this repo

---

**Last Updated**: 2026-03-09
**Version**: 1.0.0
