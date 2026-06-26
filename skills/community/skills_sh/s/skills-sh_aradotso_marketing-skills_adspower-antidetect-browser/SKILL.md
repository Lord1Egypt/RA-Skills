---
name: adspower-antidetect-browser
description: Manage AdsPower antidetect browser profiles for multi-account marketing automation and campaigns
triggers:
  - "create adspower browser profile"
  - "manage multiple browser profiles for marketing"
  - "set up antidetect browser automation"
  - "configure adspower profiles for campaigns"
  - "automate multi-account browser sessions"
  - "use adspower api for browser control"
  - "launch adspower profiles programmatically"
  - "manage browser fingerprints for marketing"
---

# AdsPower Antidetect Browser Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

AdsPower is an antidetect browser platform that allows marketing teams to manage multiple browser profiles with unique fingerprints for multi-account operations, ad campaigns, and automation workflows. Each profile has isolated cookies, storage, and unique browser fingerprints to prevent account association and detection.

## Installation

AdsPower requires the desktop application installed on your system:

1. Download AdsPower from the official website
2. Install the application for your operating system (Windows/macOS)
3. Launch AdsPower and create an account
4. Enable API access in Settings → API Settings

## API Access

AdsPower provides a local HTTP API (default port: 50325) for programmatic control.

### Base Configuration

```python
import requests
import os

# AdsPower local API endpoint
ADSPOWER_API_BASE = "http://localhost:50325/api/v1"

# Optional: If using cloud API
ADSPOWER_API_KEY = os.getenv("ADSPOWER_API_KEY")
```

```javascript
const axios = require('axios');

const ADSPOWER_API_BASE = 'http://localhost:50325/api/v1';
const API_KEY = process.env.ADSPOWER_API_KEY;
```

## Core Operations

### Create Browser Profile

```python
def create_profile(name, group_id=None, fingerprint_config=None):
    """Create a new browser profile"""
    url = f"{ADSPOWER_API_BASE}/user/create"
    
    payload = {
        "name": name,
        "group_id": group_id or "0",
        "domain_name": "",
        "open_urls": [],
        "repeat_config": fingerprint_config or []
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data.get("code") == 0:
        return data["data"]["id"]
    else:
        raise Exception(f"Failed to create profile: {data.get('msg')}")

# Usage
profile_id = create_profile(
    name="Campaign_Profile_1",
    group_id="marketing_team"
)
print(f"Created profile: {profile_id}")
```

```javascript
async function createProfile(name, groupId = '0') {
  const response = await axios.post(`${ADSPOWER_API_BASE}/user/create`, {
    name: name,
    group_id: groupId,
    domain_name: '',
    open_urls: []
  });
  
  if (response.data.code === 0) {
    return response.data.data.id;
  }
  throw new Error(`Failed to create profile: ${response.data.msg}`);
}

// Usage
const profileId = await createProfile('Campaign_Profile_1', 'marketing_team');
console.log(`Created profile: ${profileId}`);
```

### Launch Browser Profile

```python
def start_profile(profile_id, launch_args=None):
    """Launch a browser profile and return connection details"""
    url = f"{ADSPOWER_API_BASE}/browser/start"
    
    params = {
        "user_id": profile_id,
        "launch_args": launch_args or []
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get("code") == 0:
        return {
            "ws_endpoint": data["data"]["ws"]["puppeteer"],
            "selenium_endpoint": data["data"]["ws"]["selenium"],
            "debug_port": data["data"]["debug_port"]
        }
    else:
        raise Exception(f"Failed to start profile: {data.get('msg')}")

# Usage
connection = start_profile(profile_id)
print(f"WebSocket: {connection['ws_endpoint']}")
```

```javascript
async function startProfile(profileId) {
  const response = await axios.get(`${ADSPOWER_API_BASE}/browser/start`, {
    params: { user_id: profileId }
  });
  
  if (response.data.code === 0) {
    return {
      wsEndpoint: response.data.data.ws.puppeteer,
      seleniumEndpoint: response.data.data.ws.selenium,
      debugPort: response.data.data.debug_port
    };
  }
  throw new Error(`Failed to start profile: ${response.data.msg}`);
}
```

### Close Browser Profile

```python
def stop_profile(profile_id):
    """Close a running browser profile"""
    url = f"{ADSPOWER_API_BASE}/browser/stop"
    
    params = {"user_id": profile_id}
    response = requests.get(url, params=params)
    data = response.json()
    
    return data.get("code") == 0

# Usage
stop_profile(profile_id)
```

## Automation Integration

### With Selenium

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def connect_selenium(profile_id):
    """Connect Selenium to AdsPower profile"""
    connection = start_profile(profile_id)
    
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "debuggerAddress", 
        f"127.0.0.1:{connection['debug_port']}"
    )
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Usage
driver = connect_selenium(profile_id)
driver.get("https://example.com")
# Perform automation tasks
driver.quit()
stop_profile(profile_id)
```

### With Puppeteer

```javascript
const puppeteer = require('puppeteer-core');

async function connectPuppeteer(profileId) {
  const connection = await startProfile(profileId);
  
  const browser = await puppeteer.connect({
    browserWSEndpoint: connection.wsEndpoint,
    defaultViewport: null
  });
  
  return browser;
}

// Usage
(async () => {
  const browser = await connectPuppeteer(profileId);
  const page = await browser.newPage();
  await page.goto('https://example.com');
  // Perform automation tasks
  await browser.disconnect();
  await stopProfile(profileId);
})();
```

### With Playwright

```python
from playwright.sync_api import sync_playwright

def connect_playwright(profile_id):
    """Connect Playwright to AdsPower profile"""
    connection = start_profile(profile_id)
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(connection['ws_endpoint'])
        return browser

# Usage
browser = connect_playwright(profile_id)
page = browser.new_page()
page.goto("https://example.com")
# Perform automation tasks
browser.close()
stop_profile(profile_id)
```

## Profile Management

### List All Profiles

```python
def list_profiles(group_id=None, page=1, page_size=100):
    """Get all browser profiles"""
    url = f"{ADSPOWER_API_BASE}/user/list"
    
    params = {
        "page": page,
        "page_size": page_size
    }
    if group_id:
        params["group_id"] = group_id
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get("code") == 0:
        return data["data"]["list"]
    return []

# Usage
profiles = list_profiles(group_id="marketing_team")
for profile in profiles:
    print(f"{profile['user_id']}: {profile['name']}")
```

### Update Profile Configuration

```python
def update_profile(profile_id, updates):
    """Update profile settings"""
    url = f"{ADSPOWER_API_BASE}/user/update"
    
    payload = {
        "user_id": profile_id,
        **updates
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    return data.get("code") == 0

# Usage
update_profile(profile_id, {
    "name": "Updated_Campaign_Profile",
    "remark": "Main account for Facebook ads"
})
```

### Delete Profile

```python
def delete_profile(profile_id):
    """Delete a browser profile"""
    url = f"{ADSPOWER_API_BASE}/user/delete"
    
    params = {"user_ids": [profile_id]}
    response = requests.post(url, json=params)
    data = response.json()
    
    return data.get("code") == 0
```

## Common Patterns

### Campaign Profile Automation

```python
import time

class CampaignAutomation:
    def __init__(self, profile_ids):
        self.profile_ids = profile_ids
    
    def run_campaign_tasks(self, task_function):
        """Execute tasks across multiple profiles"""
        for profile_id in self.profile_ids:
            try:
                print(f"Starting profile {profile_id}")
                driver = connect_selenium(profile_id)
                
                # Execute custom task
                task_function(driver)
                
                driver.quit()
                stop_profile(profile_id)
                
                # Delay between profiles
                time.sleep(5)
                
            except Exception as e:
                print(f"Error with profile {profile_id}: {e}")
                stop_profile(profile_id)

# Usage
def post_ad_campaign(driver):
    driver.get("https://ads.platform.com")
    # Perform ad posting logic
    pass

automation = CampaignAutomation([profile_id, profile_id_2])
automation.run_campaign_tasks(post_ad_campaign)
```

### Profile Pool Manager

```python
class ProfilePool:
    def __init__(self, group_name):
        self.group_name = group_name
        self.active_profiles = {}
    
    def get_available_profile(self):
        """Get next available profile from pool"""
        profiles = list_profiles(group_id=self.group_name)
        
        for profile in profiles:
            profile_id = profile['user_id']
            if profile_id not in self.active_profiles:
                connection = start_profile(profile_id)
                self.active_profiles[profile_id] = connection
                return profile_id, connection
        
        raise Exception("No available profiles in pool")
    
    def release_profile(self, profile_id):
        """Release profile back to pool"""
        if profile_id in self.active_profiles:
            stop_profile(profile_id)
            del self.active_profiles[profile_id]

# Usage
pool = ProfilePool("marketing_team")
profile_id, connection = pool.get_available_profile()
# Use profile
pool.release_profile(profile_id)
```

### Batch Profile Creation

```python
def create_campaign_profiles(campaign_name, count=10):
    """Create multiple profiles for a campaign"""
    profile_ids = []
    
    for i in range(count):
        profile_name = f"{campaign_name}_Profile_{i+1}"
        profile_id = create_profile(
            name=profile_name,
            group_id=campaign_name
        )
        profile_ids.append(profile_id)
        print(f"Created: {profile_name} ({profile_id})")
    
    return profile_ids

# Usage
campaign_profiles = create_campaign_profiles("BlackFriday2026", count=5)
```

## Fingerprint Configuration

### Custom Fingerprint Settings

```python
def create_profile_with_fingerprint(name, config):
    """Create profile with specific fingerprint configuration"""
    url = f"{ADSPOWER_API_BASE}/user/create"
    
    payload = {
        "name": name,
        "group_id": "0",
        "fingerprint_config": {
            "ua": config.get("user_agent"),
            "language": config.get("language", "en-US"),
            "timezone": config.get("timezone", "America/New_York"),
            "webrtc": config.get("webrtc", "proxy"),
            "location": config.get("location", "ask"),
            "canvas": config.get("canvas", "noise"),
        }
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data.get("code") == 0:
        return data["data"]["id"]
    raise Exception(f"Failed to create profile: {data.get('msg')}")

# Usage
fingerprint_config = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "language": "en-US,en;q=0.9",
    "timezone": "America/Los_Angeles",
    "webrtc": "proxy"
}

profile_id = create_profile_with_fingerprint(
    "Custom_Fingerprint_Profile",
    fingerprint_config
)
```

## Troubleshooting

### Connection Issues

```python
def check_api_status():
    """Verify AdsPower API is accessible"""
    try:
        response = requests.get(f"{ADSPOWER_API_BASE}/status", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

if not check_api_status():
    print("AdsPower API not accessible. Ensure the application is running.")
```

### Profile Not Starting

```python
def safe_start_profile(profile_id, max_retries=3):
    """Start profile with retry logic"""
    for attempt in range(max_retries):
        try:
            connection = start_profile(profile_id)
            return connection
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    
    raise Exception(f"Failed to start profile after {max_retries} attempts")
```

### Clean Up Stuck Profiles

```python
def force_close_all_profiles():
    """Close all running browser profiles"""
    profiles = list_profiles()
    for profile in profiles:
        profile_id = profile['user_id']
        try:
            stop_profile(profile_id)
            print(f"Closed profile: {profile_id}")
        except Exception as e:
            print(f"Error closing {profile_id}: {e}")
```

## Environment Variables

```bash
# Optional: For cloud API access
export ADSPOWER_API_KEY="your_api_key_here"

# Custom API port if not using default
export ADSPOWER_API_PORT="50325"
```

## Best Practices

1. **Always close profiles** after use to free resources
2. **Add delays** between profile launches to avoid detection
3. **Use profile groups** to organize campaigns and teams
4. **Monitor active profiles** to prevent resource exhaustion
5. **Implement error handling** for network and API failures
6. **Rotate profiles** regularly for long-running campaigns
7. **Back up important profiles** and fingerprint configurations
