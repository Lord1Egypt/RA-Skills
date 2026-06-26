# Rate Limits & Best Practices

Platform rate limits and responsible automation practices.

## ⚖️ Legal & Ethical Guidelines

**Responsible Automation:**
- Rate limits exist to protect platform infrastructure—respect them
- "Anti-bot avoidance" is for legitimate automation, not evasion
- Do not bypass authentication or access controls
- Do not use techniques to hide automated activity from platforms
- If a platform blocks your access, stop and reassess your use case

**Compliance Checklist:**
- ✅ Platform ToS reviewed and understood
- ✅ robots.txt respected
- ✅ Rate limits within acceptable bounds
- ✅ Personal data handled per GDPR/CCPA
- ✅ Use case is permitted (research, analysis, etc.)
- ✅ No data resale or commercial redistribution
- ✅ No harassment, spam, or manipulation

**When in Doubt:**
- Use official APIs when available
- Contact platform for partnership/data access
- Consult legal counsel for commercial use cases

---

## Rate Limits by Platform

| Platform | Unauthenticated | Authenticated | Notes |
|----------|----------------|---------------|-------|
| Twitter/X | ~100 req/hour | ~300 req/hour | Varies by endpoint |
| Reddit | 60 req/min | 60 req/min | OAuth required for API |
| Instagram | ~50 req/hour | ~100 req/hour | Aggressive detection |
| TikTok | ~30 req/hour | ~60 req/hour | Heavy JS rendering |
| LinkedIn | Login required | ~50 req/hour | Professional content |
| YouTube | 1000 units/day | 1000 units/day | API quota system |

---

## Delay Guidelines

### Conservative (Safe)
```javascript
{
  scrollDelay: 3000,      // 3s between scrolls
  requestDelay: 5000,     // 5s between requests
  sessionLimit: 50,       // Max posts per session
  dailyLimit: 200         // Max posts per day
}
```

### Moderate (Balanced)
```javascript
{
  scrollDelay: 1500,      // 1.5s between scrolls
  requestDelay: 2000,     // 2s between requests
  sessionLimit: 100,      // Max posts per session
  dailyLimit: 500         // Max posts per day
}
```

### Aggressive (Risk)
```javascript
{
  scrollDelay: 800,       // 0.8s between scrolls
  requestDelay: 1000,     // 1s between requests
  sessionLimit: 200,      // Max posts per session
  dailyLimit: 1000        // Max posts per day
}
```

**Recommendation:** Start conservative, adjust based on results.

---

## Anti-Bot Avoidance

### User Agent Rotation
```javascript
const userAgents = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
];

// Rotate randomly
const ua = userAgents[Math.floor(Math.random() * userAgents.length)];
```

### Random Delays
```javascript
// Add randomness to delays
function randomDelay(base, variance) {
  return base + (Math.random() * variance);
}

await page.waitForTimeout(randomDelay(1500, 500));
```

### Mouse Movement Simulation
```javascript
// Simulate human mouse movement
await page.mouse.move(Math.random() * 100, Math.random() * 100);
await page.waitForTimeout(100);
await page.mouse.move(Math.random() * 200, Math.random() * 200);
```

### Proxy Rotation
For high-volume scraping:
- Use residential proxies
- Rotate every 10-20 requests
- Services: Bright Data, Oxylabs, Smartproxy

---

## Session Management

### Cookie Persistence
```javascript
// Save cookies between sessions
const cookies = await page.context().cookies();
fs.writeFileSync('cookies.json', JSON.stringify(cookies));

// Load cookies
const savedCookies = JSON.parse(fs.readFileSync('cookies.json'));
await page.context().addCookies(savedCookies);
```

### Fingerprint Consistency
- Use same browser profile
- Maintain consistent viewport
- Don't rotate user agents mid-session
- Keep timezone consistent

---

## Error Handling

### Common Errors
```
429 Too Many Requests - Slow down, add delays
403 Forbidden - Possible IP ban, rotate proxy
401 Unauthorized - Login expired, refresh auth
Timeout - Increase wait times, check selectors
```

### Retry Logic
```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}
```

---

## Legal Considerations

### ToS Compliance
- Review each platform's Terms of Service
- Most prohibit automated scraping
- Use for research/fair use only
- Don't redistribute scraped data commercially

### robots.txt
Check `https://<platform>/robots.txt`:
- Respect Disallow directives
- Some platforms allow certain paths

### Data Privacy
- Don't collect personal data at scale
- Anonymize stored data
- GDPR/CCPA compliance if storing EU/CA data
- Delete data when no longer needed

---

## Monitoring & Alerting

### Usage Tracking
```javascript
// Track requests per platform
const usage = {
  twitter: { count: 0, lastReset: Date.now() },
  reddit: { count: 0, lastReset: Date.now() }
};

// Reset hourly
if (Date.now() - usage.twitter.lastReset > 3600000) {
  usage.twitter.count = 0;
  usage.twitter.lastReset = Date.now();
}
```

### Alerts
- Set threshold alerts (e.g., >80% of limit)
- Log all 429 responses
- Monitor success rate
- Track selector changes (sudden drop in matches)

---

## Production Checklist

Before running at scale:
- [ ] Review ToS for target platform
- [ ] Test with conservative delays
- [ ] Verify selectors work
- [ ] Set up error logging
- [ ] Configure rate limit tracking
- [ ] Have fallback (API) ready
- [ ] Consider legal implications
- [ ] Document data usage
