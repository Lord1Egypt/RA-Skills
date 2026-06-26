---
name: he4rt-twitter-engagement-tracker
description: Chrome extension that passively captures X/Twitter GraphQL responses to track community engagement and export structured JSON for analytics ingestion.
triggers:
  - track twitter engagement for my community
  - capture x.com graphql responses for analytics
  - set up twitter community engagement tracking
  - export twitter engagement data to json
  - monitor twitter followers and likes passively
  - integrate twitter analytics with my backend
  - build chrome extension for twitter tracking
  - analyze twitter community engagement metrics
---

# He4rt Twitter Engagement Tracker

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Browser extension that passively captures X/Twitter GraphQL responses to track community engagement. Intercepts native Twitter API calls to extract tweets, likes, replies, and user interactions without hitting rate limits. Exports structured JSON for backend ingestion.

## What It Does

- **Passive capture**: Intercepts GraphQL responses as you browse X/Twitter normally
- **Community tracking**: Monitors tweets, replies, likes, and engagement for specific handles
- **Zero rate limits**: Uses data the browser already receives, no additional API calls
- **Structured export**: Produces clean JSON with tweets, metrics, favoriters, and engagement summaries
- **Backend-ready**: Designed for ingestion into Laravel/database systems

### Key GraphQL Endpoints Captured

| Endpoint | Data Extracted |
|----------|----------------|
| `UserTweets` | All tweets from tracked handle with full metrics |
| `Favoriters` | Users who liked specific tweets (with mutual follow status) |
| `TweetDetail` | Reply threads and engagement details |
| `UserByScreenName` | Profile data (followers, bio, verification) |

## Installation

### Load the Extension

1. Clone or download this project
2. Open Chrome/Brave and navigate to `chrome://extensions/`
3. Enable **Developer mode** (top right toggle)
4. Click **Load unpacked** and select the project directory
5. Pin the extension icon to your toolbar for easy access

### Project Structure

```
he4rt-analytics/
├── manifest.json        # Manifest V3 config
├── interceptor.js       # MAIN world - patches window.fetch()
├── content.js           # ISOLATED world - bridge to background
├── background.js        # Service worker - data processing
├── popup.html/css/js    # Extension UI
└── icons/              # Extension icons (16, 48, 128px)
```

## Key Concepts

### Three-Context Architecture

```javascript
// 1. MAIN world (interceptor.js) - Access to window.fetch
const originalFetch = window.fetch;
window.fetch = function(...args) {
  return originalFetch.apply(this, args).then(response => {
    const cloned = response.clone();
    cloned.json().then(data => {
      window.postMessage({
        type: 'TWITTER_GRAPHQL_RESPONSE',
        url: args[0],
        data: data
      }, '*');
    });
    return response;
  });
};

// 2. ISOLATED world (content.js) - Bridge to extension
window.addEventListener('message', (event) => {
  if (event.data.type === 'TWITTER_GRAPHQL_RESPONSE') {
    chrome.runtime.sendMessage({
      type: 'GRAPHQL_INTERCEPTED',
      payload: event.data
    });
  }
});

// 3. Background (background.js) - Data processing
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GRAPHQL_INTERCEPTED') {
    processGraphQLResponse(message.payload);
  }
});
```

## Configuration

### manifest.json

```json
{
  "manifest_version": 3,
  "name": "He4rt Analytics",
  "version": "1.0",
  "permissions": [
    "storage",
    "activeTab"
  ],
  "host_permissions": [
    "https://x.com/*",
    "https://twitter.com/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["https://x.com/*", "https://twitter.com/*"],
      "js": ["content.js"],
      "run_at": "document_start"
    },
    {
      "matches": ["https://x.com/*", "https://twitter.com/*"],
      "js": ["interceptor.js"],
      "run_at": "document_start",
      "world": "MAIN"
    }
  ],
  "action": {
    "default_popup": "popup.html"
  }
}
```

### Setting Tracked Handle

```javascript
// In popup.js or background.js
async function setTrackedHandle(screenName) {
  await chrome.storage.local.set({ 
    trackedHandle: screenName.replace('@', '')
  });
}

// Retrieve tracked handle
async function getTrackedHandle() {
  const result = await chrome.storage.local.get(['trackedHandle']);
  return result.trackedHandle || null;
}
```

## Core Implementation

### Intercepting GraphQL Responses (interceptor.js)

```javascript
// Inject into MAIN world to access window.fetch
(function() {
  const originalFetch = window.fetch;
  
  window.fetch = function(...args) {
    const url = args[0];
    
    return originalFetch.apply(this, args).then(response => {
      // Only process Twitter GraphQL endpoints
      if (typeof url === 'string' && url.includes('api.x.com/graphql')) {
        const clonedResponse = response.clone();
        
        clonedResponse.json().then(data => {
          // Extract endpoint name from URL
          const endpoint = url.match(/\/graphql\/[^\/]+\/([^?]+)/)?.[1] || 'unknown';
          
          // Post to content script
          window.postMessage({
            type: 'TWITTER_GRAPHQL_RESPONSE',
            url: url,
            endpoint: endpoint,
            data: data,
            timestamp: Date.now()
          }, '*');
        }).catch(() => {
          // Non-JSON response, ignore
        });
      }
      
      return response;
    });
  };
})();
```

### Bridging to Background (content.js)

```javascript
// Listen for messages from MAIN world
window.addEventListener('message', (event) => {
  if (event.source !== window) return;
  if (event.data.type !== 'TWITTER_GRAPHQL_RESPONSE') return;
  
  // Forward to background script
  chrome.runtime.sendMessage({
    type: 'GRAPHQL_INTERCEPTED',
    payload: event.data
  });
});

// Optional: Log confirmation
chrome.runtime.sendMessage({
  type: 'GRAPHQL_INTERCEPTED',
  payload: event.data
}, (response) => {
  console.log('Data forwarded to background:', response);
});
```

### Processing and Storage (background.js)

```javascript
// Store captured data
let capturedTweets = new Map(); // tweet_id -> tweet object
let capturedFavoriters = new Map(); // tweet_id -> array of users
let capturedReplies = [];
let trackedHandle = null;

// Load tracked handle on startup
chrome.storage.local.get(['trackedHandle'], (result) => {
  trackedHandle = result.trackedHandle;
});

// Process incoming GraphQL responses
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GRAPHQL_INTERCEPTED') {
    const { endpoint, data, url } = message.payload;
    
    switch(endpoint) {
      case 'UserTweets':
        processTweets(data, url);
        break;
      case 'Favoriters':
        processFavoriters(data, url);
        break;
      case 'TweetDetail':
        processReplies(data);
        break;
      case 'UserByScreenName':
        processUserProfile(data);
        break;
    }
    
    sendResponse({ status: 'processed' });
  }
  
  return true; // Keep message channel open
});

function processTweets(data, url) {
  // Navigate Twitter's nested response structure
  const instructions = data?.data?.user?.result?.timeline_v2?.timeline?.instructions || [];
  
  for (const instruction of instructions) {
    if (instruction.type === 'TimelineAddEntries') {
      for (const entry of instruction.entries || []) {
        const tweet = extractTweetFromEntry(entry);
        if (tweet && shouldTrack(tweet)) {
          capturedTweets.set(tweet.tweet_id, tweet);
        }
      }
    }
  }
}

function extractTweetFromEntry(entry) {
  const content = entry.content?.itemContent?.tweet_results?.result;
  if (!content) return null;
  
  const legacy = content.legacy;
  if (!legacy) return null;
  
  const user = content.core?.user_results?.result?.legacy;
  const screenName = user?.screen_name;
  
  return {
    tweet_id: content.rest_id,
    text: legacy.full_text,
    created_at: legacy.created_at,
    author_screen_name: screenName,
    metrics: {
      favorite_count: legacy.favorite_count,
      retweet_count: legacy.retweet_count,
      reply_count: legacy.reply_count,
      quote_count: legacy.quote_count,
      bookmark_count: legacy.bookmark_count,
      view_count: parseInt(content.views?.count || '0')
    },
    hashtags: (legacy.entities?.hashtags || []).map(h => h.text),
    user_mentions: (legacy.entities?.user_mentions || []).map(m => ({
      screen_name: m.screen_name,
      name: m.name
    })),
    media_count: (legacy.entities?.media || []).length,
    is_retweet: !!legacy.retweeted_status_result,
    source: legacy.source
  };
}

function shouldTrack(tweet) {
  return trackedHandle && 
         tweet.author_screen_name?.toLowerCase() === trackedHandle.toLowerCase();
}

function processFavoriters(data, url) {
  // Extract tweet ID from URL
  const tweetId = url.match(/variables=.*"tweetId"%3A"(\d+)"/)?.[1];
  if (!tweetId) return;
  
  const entries = data?.data?.favoriters_timeline?.timeline?.instructions?.[0]?.entries || [];
  const users = [];
  
  for (const entry of entries) {
    const user = entry.content?.itemContent?.user_results?.result;
    if (!user) continue;
    
    const legacy = user.legacy;
    users.push({
      rest_id: user.rest_id,
      screen_name: legacy.screen_name,
      name: legacy.name,
      followers_count: legacy.followers_count,
      following: legacy.following,
      followed_by: legacy.followed_by,
      verified: user.is_blue_verified || legacy.verified
    });
  }
  
  if (!capturedFavoriters.has(tweetId)) {
    capturedFavoriters.set(tweetId, []);
  }
  capturedFavoriters.get(tweetId).push(...users);
}
```

### Building Export JSON

```javascript
function buildExportJSON() {
  const tweets = Array.from(capturedTweets.values());
  
  // Separate by type
  const originalTweets = tweets.filter(t => !t.is_retweet);
  const retweets = tweets.filter(t => t.is_retweet);
  
  // Build favoriters map
  const favoritersByTweet = {};
  capturedFavoriters.forEach((users, tweetId) => {
    favoritersByTweet[tweetId] = users;
  });
  
  // Calculate summary stats
  const totalLikes = originalTweets.reduce((sum, t) => sum + t.metrics.favorite_count, 0);
  const totalViews = originalTweets.reduce((sum, t) => sum + t.metrics.view_count, 0);
  
  const topTweetByLikes = originalTweets.sort((a, b) => 
    b.metrics.favorite_count - a.metrics.favorite_count
  )[0]?.tweet_id;
  
  const topTweetByViews = originalTweets.sort((a, b) => 
    b.metrics.view_count - a.metrics.view_count
  )[0]?.tweet_id;
  
  // Count unique engagers
  const uniqueEngagers = new Set();
  capturedFavoriters.forEach(users => {
    users.forEach(u => uniqueEngagers.add(u.rest_id));
  });
  capturedReplies.forEach(r => uniqueEngagers.add(r.author.rest_id));
  
  return {
    tracked_account: {
      screen_name: trackedHandle,
      // Additional profile data if captured
    },
    exported_at: new Date().toISOString(),
    tweets: tweets,
    community_replies: capturedReplies,
    favoriters_by_tweet: favoritersByTweet,
    summary: {
      total_tweets: tweets.length,
      total_original: originalTweets.length,
      total_retweets: retweets.length,
      total_community_replies: capturedReplies.length,
      total_likes: totalLikes,
      total_views: totalViews,
      avg_likes_per_original: originalTweets.length > 0 ? 
        Math.round(totalLikes / originalTweets.length) : 0,
      avg_views_per_original: originalTweets.length > 0 ? 
        Math.round(totalViews / originalTweets.length) : 0,
      unique_engagers: uniqueEngagers.size,
      top_tweet_by_likes: topTweetByLikes,
      top_tweet_by_views: topTweetByViews
    }
  };
}

// Trigger download
function downloadJSON() {
  const json = buildExportJSON();
  const blob = new Blob([JSON.stringify(json, null, 2)], { 
    type: 'application/json' 
  });
  const url = URL.createObjectURL(blob);
  
  const filename = `x-${trackedHandle}-${new Date().toISOString().split('T')[0]}.json`;
  
  chrome.downloads.download({
    url: url,
    filename: filename,
    saveAs: true
  });
}
```

## Popup UI Implementation

### popup.js - UI Logic

```javascript
document.addEventListener('DOMContentLoaded', async () => {
  const handleInput = document.getElementById('handle-input');
  const trackBtn = document.getElementById('track-btn');
  const exportBtn = document.getElementById('export-btn');
  const statsDiv = document.getElementById('stats');
  
  // Load current tracked handle
  const { trackedHandle } = await chrome.storage.local.get(['trackedHandle']);
  if (trackedHandle) {
    handleInput.value = trackedHandle;
    loadStats();
  }
  
  // Set tracked handle
  trackBtn.addEventListener('click', async () => {
    const handle = handleInput.value.trim().replace('@', '');
    if (!handle) return;
    
    await chrome.storage.local.set({ trackedHandle: handle });
    
    // Notify background script
    chrome.runtime.sendMessage({ 
      type: 'SET_TRACKED_HANDLE', 
      handle: handle 
    });
    
    trackBtn.textContent = 'Tracking!';
    setTimeout(() => trackBtn.textContent = 'Track', 1000);
    
    loadStats();
  });
  
  // Export JSON
  exportBtn.addEventListener('click', () => {
    chrome.runtime.sendMessage({ type: 'EXPORT_JSON' }, (response) => {
      if (response?.success) {
        exportBtn.textContent = 'Exported!';
        setTimeout(() => exportBtn.textContent = 'Export JSON', 2000);
      }
    });
  });
  
  // Load and display stats
  async function loadStats() {
    const response = await chrome.runtime.sendMessage({ type: 'GET_STATS' });
    
    statsDiv.innerHTML = `
      <div class="stat-item">
        <span class="stat-label">Tweets Captured:</span>
        <span class="stat-value">${response.total_tweets}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Total Likes:</span>
        <span class="stat-value">${response.total_likes}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Total Views:</span>
        <span class="stat-value">${response.total_views}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Unique Engagers:</span>
        <span class="stat-value">${response.unique_engagers}</span>
      </div>
    `;
  }
  
  // Refresh stats every 5 seconds
  setInterval(loadStats, 5000);
});
```

## Backend Integration

### Laravel Ingestion Example

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\TwitterAccount;
use App\Models\Tweet;
use App\Models\CommunityEngagement;

class IngestTwitterAnalytics extends Command
{
    protected $signature = 'twitter:ingest {file}';
    protected $description = 'Ingest Twitter analytics JSON export';

    public function handle()
    {
        $path = $this->argument('file');
        
        if (!file_exists($path)) {
            $this->error("File not found: {$path}");
            return 1;
        }
        
        $data = json_decode(file_get_contents($path), true);
        
        // Upsert tracked account
        $account = TwitterAccount::updateOrCreate(
            ['screen_name' => $data['tracked_account']['screen_name']],
            [
                'name' => $data['tracked_account']['name'] ?? null,
                'rest_id' => $data['tracked_account']['rest_id'] ?? null,
                'followers_count' => $data['tracked_account']['followers_count'] ?? 0,
                'statuses_count' => $data['tracked_account']['statuses_count'] ?? 0,
            ]
        );
        
        // Upsert tweets
        foreach ($data['tweets'] as $tweetData) {
            Tweet::updateOrCreate(
                ['tweet_id' => $tweetData['tweet_id']],
                [
                    'twitter_account_id' => $account->id,
                    'text' => $tweetData['text'],
                    'created_at' => $tweetData['created_at'],
                    'favorite_count' => $tweetData['metrics']['favorite_count'],
                    'retweet_count' => $tweetData['metrics']['retweet_count'],
                    'reply_count' => $tweetData['metrics']['reply_count'],
                    'view_count' => $tweetData['metrics']['view_count'],
                    'is_retweet' => $tweetData['is_retweet'],
                    'hashtags' => json_encode($tweetData['hashtags']),
                ]
            );
        }
        
        // Track community engagement
        foreach ($data['favoriters_by_tweet'] as $tweetId => $users) {
            foreach ($users as $user) {
                CommunityEngagement::updateOrCreate(
                    [
                        'tweet_id' => $tweetId,
                        'user_rest_id' => $user['rest_id'],
                        'type' => 'like',
                    ],
                    [
                        'user_screen_name' => $user['screen_name'],
                        'user_name' => $user['name'],
                        'followers_count' => $user['followers_count'],
                        'is_mutual' => $user['following'] && $user['followed_by'],
                        'is_verified' => $user['verified'],
                    ]
                );
            }
        }
        
        foreach ($data['community_replies'] as $reply) {
            CommunityEngagement::updateOrCreate(
                [
                    'tweet_id' => $reply['tweet_id'],
                    'user_rest_id' => $reply['author']['rest_id'],
                    'type' => 'reply',
                ],
                [
                    'user_screen_name' => $reply['author']['screen_name'],
                    'in_reply_to_tweet_id' => $reply['in_reply_to_tweet_id'],
                ]
            );
        }
        
        $this->info("Imported {$data['summary']['total_tweets']} tweets");
        $this->info("Tracked {$data['summary']['unique_engagers']} unique engagers");
        
        return 0;
    }
}
```

### Node.js/Express API Endpoint

```javascript
const express = require('express');
const app = express();

app.post('/api/analytics/ingest', express.json({ limit: '50mb' }), async (req, res) => {
  const data = req.body;
  
  try {
    // Upsert account
    const account = await db.twitterAccounts.upsert({
      where: { screen_name: data.tracked_account.screen_name },
      update: data.tracked_account,
      create: data.tracked_account
    });
    
    // Batch insert tweets
    const tweets = data.tweets.map(t => ({
      ...t,
      account_id: account.id,
      metrics: JSON.stringify(t.metrics),
      hashtags: JSON.stringify(t.hashtags)
    }));
    
    await db.tweets.createMany({
      data: tweets,
      skipDuplicates: true
    });
    
    // Process engagement
    const engagements = [];
    
    for (const [tweetId, users] of Object.entries(data.favoriters_by_tweet)) {
      users.forEach(user => {
        engagements.push({
          tweet_id: tweetId,
          user_rest_id: user.rest_id,
          user_screen_name: user.screen_name,
          type: 'like',
          is_mutual: user.following && user.followed_by
        });
      });
    }
    
    await db.communityEngagement.createMany({
      data: engagements,
      skipDuplicates: true
    });
    
    res.json({
      success: true,
      summary: data.summary
    });
    
  } catch (error) {
    console.error('Ingestion error:', error);
    res.status(500).json({ error: error.message });
  }
});
```

## Common Usage Patterns

### Pattern 1: Daily Engagement Snapshot

```javascript
// Automate daily capture and export
// In background.js, add scheduled task
chrome.alarms.create('daily-export', {
  when: Date.now() + 1000,
  periodInMinutes: 1440 // 24 hours
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'daily-export') {
    const json = buildExportJSON();
    
    // Send to backend API instead of downloading
    fetch('https://api.heartdevs.com/analytics/ingest', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.API_KEY}`
      },
      body: JSON.stringify(json)
    });
    
    // Clear captured data after successful export
    capturedTweets.clear();
    capturedFavoriters.clear();
    capturedReplies = [];
  }
});
```

### Pattern 2: Multi-Handle Tracking

```javascript
// Track multiple accounts simultaneously
let trackedHandles = new Set();

async function addTrackedHandle(handle) {
  const handles = await chrome.storage.local.get(['trackedHandles']) || { trackedHandles: [] };
  handles.trackedHandles.push(handle);
  await chrome.storage.local.set({ trackedHandles: handles.trackedHandles });
  trackedHandles = new Set(handles.trackedHandles);
}

function shouldTrack(tweet) {
  return trackedHandles.has(tweet.author_screen_name?.toLowerCase());
}

// Export per handle
function buildExportJSON(handle) {
  const tweets = Array.from(capturedTweets.values())
    .filter(t => t.author_screen_name?.toLowerCase() === handle.toLowerCase());
  
  // ... rest of export logic
}
```

### Pattern 3: Real-time Metrics Display

```javascript
// In popup.js - show live tweet feed
async function renderTweetFeed() {
  const response = await chrome.runtime.sendMessage({ type: 'GET_RECENT_TWEETS', limit: 10 });
  
  const feedHtml = response.tweets.map(tweet => `
    <div class="tweet-card">
      <div class="tweet-text">${escapeHtml(tweet.text)}</div>
      <div class="tweet-metrics">
        <span>❤️ ${tweet.metrics.favorite_count}</span>
        <span>🔄 ${tweet.metrics.retweet_count}</span>
        <span>👁️ ${tweet.metrics.view_count}</span>
      </div>
    </div>
  `).join('');
  
  document.getElementById('tweet-feed').innerHTML = feedHtml;
}
```

## Troubleshooting

### Extension Not Capturing Data

**Check injection**:
```javascript
// In console on x.com, verify interceptor loaded
console.log(window.fetch.toString());
// Should show patched function, not native code
```

**Verify content script injection**:
```javascript
// In popup.js, check active tab
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  console.log('Current URL:', tabs[0].url);
  // Must be x.com or twitter.com
});
```

**Storage permissions**:
```javascript
// Test storage access
chrome.storage.local.set({ test: 'value' }, () => {
  chrome.storage.local.get(['test'], (result) => {
    console.log('Storage test:', result.test);
  });
});
```

### GraphQL Responses Not Parsing

**Log raw responses**:
```javascript
// In background.js
chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'GRAPHQL_INTERCEPTED') {
    console.log('Raw endpoint:', message.payload.endpoint);
    console.log('Raw data:', JSON.stringify(message.payload.data, null, 2));
  }
});
```

**Twitter API structure changes**:
```javascript
// Add defensive parsing
function safeExtract(obj, path, defaultValue = null) {
  try {
    return path.split('.').reduce((acc, part) => acc?.[part], obj) ?? defaultValue;
  } catch {
    return defaultValue;
  }
}

// Usage
const tweetText = safeExtract(entry, 'content.itemContent.tweet_results.result.legacy.full_text', '');
```

### Export File Too Large

**Implement pagination**:
```javascript
function buildExportJSON(page = 1, pageSize = 100) {
  const tweets = Array.from(capturedTweets.values());
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  
  return {
    page: page,
    total_pages: Math.ceil(tweets.length / pageSize),
    tweets: tweets.slice(start, end),
    // ... rest of structure
  };
}
```

**Compression**:
```javascript
// Use gzip compression for large exports
import pako from 'pako';

function downloadCompressedJSON() {
  const json = JSON.stringify(buildExportJSON());
  const compressed = pako.gzip(json);
  const blob = new Blob([compressed], { type: 'application/gzip' });
  // ... download logic
}
```

### Performance Issues

**Debounce storage writes**:
```javascript
let saveTimeout;
function debouncedSave() {
  clearTimeout(saveTimeout);
  saveTimeout = setTimeout(() => {
    chrome.storage.local.set({
      tweets: Array.from(capturedTweets.entries()),
      favoriters: Array.from(capturedFavoriters.entries())
    });
  }, 5000); // Save every 5 seconds max
}
```

**Memory management**:
```javascript
// Auto-clear old data
const MAX_TWEETS = 1000;
function addTweet(tweet) {
  if (capturedTweets.size >= MAX_TWEETS) {
    // Remove oldest tweet
    const oldest = Array.from(capturedTweets.keys())[0];
    capturedTweets.delete(oldest);
  }
  capturedTweets.set(tweet.tweet_id, tweet);
}
```

## Advanced Features

### Webhook Auto-Push

```javascript
// In background.js - send data immediately on capture
const WEBHOOK_URL = 'https://api.heartdevs.com/webhook/twitter';

async function pushToWebhook(data) {
  try {
    const response = await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': await getApiKey() // Store in chrome.storage
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      console.error('Webhook failed:', await response.text());
    }
  } catch (error) {
    console.error('Webhook error:', error);
  }
}

// Push new tweets immediately
function processTweets(data, url) {
  const tweets = extractTweetsFromData(data);
  
  tweets.forEach(tweet => {
    if (!capturedTweets.has(tweet.tweet_id)) {
      capturedTweets.set(tweet.tweet_id, tweet);
      
      // Push to webhook
      pushToWebhook({
        type: 'new_tweet',
        tweet: tweet,
        captured_at: new Date().toISOString()
      });
    }
  });
}
```

### Engagement Scoring

```javascript
function calculateEngagementScore(tweet) {
  const weights = {
    like: 1,
    retweet: 5,
    reply: 10,
    quote: 15
  };
  
  const rawScore = 
    (tweet.metrics.favorite_count * weights.like) +
    (tweet.metrics.retweet_count * weights.retweet) +
    (tweet.metrics.reply_count * weights.reply) +
    (tweet.metrics.quote_count * weights.quote);
  
  // Normalize by followers
  const normalizedScore = rawScore / Math.log10(tweet.author_followers_count + 10);
  
  return Math.round(normalizedScore * 100) / 100;
}

// Add scores to export
function buildExportJSON() {
