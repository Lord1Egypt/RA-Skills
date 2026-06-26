# Skrape — Implementation Patterns (JavaScript)

## robots.txt Verification (First Step)

```javascript
const https = require('https');
const http = require('http');
const { URL } = require('url');

function verifyRobotsAccess(url, agentLabel = '*') {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const robotsUrl = `${parsed.protocol}//${parsed.host}/robots.txt`;
    
    const fetchRobots = (protocol) => {
      return new Promise((resolve, reject) => {
        protocol.get(robotsUrl, (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            try {
              const allowed = evaluateRobotsRules(data, agentLabel, parsed.pathname);
              resolve(allowed);
            } catch (e) {
              resolve(true); // Missing robots.txt = permitted
            }
          });
        }).on('error', () => resolve(true));
      });
    };
    
    fetchRobots(parsed.protocol === 'https:' ? https : http)
      .then(resolve)
      .catch(() => resolve(true));
  });
}

function evaluateRobotsRules(content, agentLabel, path) {
  const lines = content.split('\n');
  let activeAgent = null;
  let blockedPaths = [];
  let allowedPaths = [];
  
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    
    const [key, value] = trimmed.split(':', 2).map(s => s.trim());
    
    if (key?.toLowerCase() === 'user-agent') {
      if (activeAgent !== null && agentMatches(activeAgent, agentLabel)) {
        for (const p of blockedPaths) {
          if (path.startsWith(p)) return false;
        }
      }
      activeAgent = value;
      blockedPaths = [];
      allowedPaths = [];
    } else if (key?.toLowerCase() === 'disallow') {
      if (value) blockedPaths.push(value);
    } else if (key?.toLowerCase() === 'allow') {
      if (value) allowedPaths.push(value);
    }
  }
  
  // Evaluate final user-agent block
  if (activeAgent !== null && agentMatches(activeAgent, agentLabel)) {
    for (const p of blockedPaths) {
      if (path.startsWith(p)) return false;
    }
  }
  
  return true;
}

function agentMatches(ruleAgent, requestAgent) {
  if (ruleAgent === '*') return true;
  return ruleAgent.toLowerCase() === requestAgent.toLowerCase();
}
```

## Connection Manager

```javascript
const https = require('https');
const http = require('http');
const { URL } = require('url');

function buildConnectionManager(contactEmail) {
  const agentOptions = {
    keepAlive: true,
    maxSockets: 1,
    timeout: 30000,
  };
  
  const httpsAgent = new https.Agent(agentOptions);
  const httpAgent = new http.Agent(agentOptions);
  
  return {
    userAgent: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (contact: ${contactEmail})`,
    accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    acceptLanguage: 'en-US,en;q=0.9',
    httpsAgent,
    httpAgent,
    
    get(url) {
      return new Promise((resolve, reject) => {
        const parsed = new URL(url);
        const protocol = parsed.protocol === 'https:' ? https : http;
        const agent = parsed.protocol === 'https:' ? this.httpsAgent : this.httpAgent;
        
        const req = protocol.get(url, {
          headers: {
            'User-Agent': this.userAgent,
            'Accept': this.accept,
            'Accept-Language': this.acceptLanguage,
          },
          agent,
        }, (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            resolve({
              status: res.statusCode,
              headers: res.headers,
              text: data,
            });
          });
        });
        
        req.on('error', reject);
        req.setTimeout(30000, () => {
          req.destroy();
          reject(new Error('Request timeout'));
        });
      });
    },
  };
}
```

## Throttled Request Handler

```javascript
const { Console } = require('console');

const logger = new Console({
  stdout: process.stdout,
  stderr: process.stderr,
});

async function executeThrottledRequest(manager, url, baseDelay = 2.0, attemptLimit = 5) {
  /** Execute with throttling, backoff strategy, and audit logging. */
  
  for (let attempt = 0; attempt < attemptLimit; attempt++) {
    // Courteous pause with randomization
    const pause = baseDelay + Math.random() * 0.5;
    await wait(pause * 1000);
    
    const response = await manager.get(url);
    
    // Audit record
    logger.info(`SCRAPE url=${url} status=${response.status}`);
    
    // Inspect rate limit indicators
    const remaining = response.headers['x-ratelimit-remaining'];
    if (remaining && parseInt(remaining, 10) < 5) {
      logger.warn(`Rate limit depleted: ${remaining} remaining`);
      await wait(10000); // Preventive slowdown
    }
    
    // Handle 429 responses
    if (response.status === 429) {
      const retryAfter = response.headers['retry-after'];
      const pauseDuration = retryAfter && !isNaN(parseInt(retryAfter, 10)) 
        ? parseInt(retryAfter, 10) * 1000 
        : 60000;
      logger.warn(`429 received, pausing ${pauseDuration / 1000}s`);
      await wait(pauseDuration);
      continue;
    }
    
    // Success or client error (skip retry for 4xx except 429)
    if (response.status < 500) {
      return response;
    }
    
    // Server error: progressive backoff
    const pauseDuration = Math.min(Math.pow(2, attempt) * 1000 + Math.random() * 1000, 60000);
    logger.warn(`5xx error, retry in ${(pauseDuration / 1000).toFixed(1)}s`);
    await wait(pauseDuration);
  }
  
  throw new Error(`Failed after ${attemptLimit} attempts: ${url}`);
}

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

## Complete Workflow

```javascript
const { verifyRobotsAccess, buildConnectionManager, executeThrottledRequest } = require('./scrape');

async function runScraper() {
  const contact = 'your-email@example.com';
  const target = 'https://example.com/products';
  
  // 1. Verify robots.txt
  const permitted = await verifyRobotsAccess(target);
  if (!permitted) {
    throw new Error('Blocked by robots.txt');
  }
  
  // 2. Initialize connection manager
  const manager = buildConnectionManager(contact);
  
  // 3. Execute throttled request
  const response = await executeThrottledRequest(manager, target);
  
  // 4. Process (implement your logic)
  console.log(`Retrieved ${response.text.length} bytes`);
}

runScraper().catch(console.error);
```
