---
name: he4rt-marketing-extension
description: Chrome extension that passively captures X/Twitter GraphQL responses to track community engagement and export structured JSON for analytics ingestion.
triggers:
  - how do I track Twitter engagement for my community
  - set up the He4rt marketing extension to capture X analytics
  - export Twitter GraphQL data for community tracking
  - capture Twitter likes and replies for analytics
  - integrate X engagement data with my Laravel backend
  - track who interacts with my Twitter account
  - monitor community engagement on X/Twitter
  - build a Twitter analytics dashboard with this extension
---

# He4rt Marketing Extension Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

The He4rt Marketing Extension is a Chrome browser extension that passively intercepts X/Twitter GraphQL API responses to capture community engagement metrics. It's designed for community managers who need granular engagement data that Twitter's native analytics don't provide — like bulk engagement exports, consistent community member interactions, reply tracking across posts, and favoriter lists.

The extension runs in the background while you browse X, captures GraphQL responses, deduplicates data, and exports structured JSON ready for ingestion into a Laravel backend (or any analytics system).

## Installation

1. **Clone or Download**: Get the extension files into a local directory
2. **Load in Chrome**:
   - Navigate to `chrome://extensions/`
   - Enable **Developer mode** (toggle in top right)
   - Click **Load unpacked**
   - Select the extension directory
3. **Verify**: The He4rt Analytics icon should appear in your extensions toolbar

## Architecture

The extension uses three core scripts:

- **`interceptor.js`**: Runs in MAIN world (page context) to patch `window.fetch()` and intercept GraphQL responses
- **`content.js`**: Runs in ISOLATED world (extension context) to bridge page → background via `chrome.runtime.sendMessage`
- **`background.js`**: Service worker that filters, consolidates, deduplicates, and stores captured data

Communication flow:
```
X.com page → interceptor.js (fetch patch) → postMessage → content.js → chrome.runtime → background.js → chrome.storage
```

## Key Workflows

### 1. Start Tracking an Account

Open the extension popup and set the Twitter handle to track:

```javascript
// In popup.js - setting tracked handle
document.getElementById('trackBtn').addEventListener('click', async () => {
  const handle = document.getElementById('handleInput').value.trim().replace('@', '');
  
  await chrome.storage.local.set({ trackedHandle: handle });
  
  // Notify background script
  chrome.runtime.sendMessage({ 
    type: 'SET_TRACKED_HANDLE', 
    handle 
  });
});
```

**User action**: Type the handle (e.g., `He4rtDevs`) and click "Track"

### 2. Passive Data Capture

Once tracking is active, browse normally on x.com:

- **Scroll the tracked account's profile** → Captures `UserTweets` endpoint (tweets + metrics)
- **Click on a tweet's like count** → Captures `Favoriters` endpoint (users who liked)
- **Open individual tweets** → Captures `TweetDetail` endpoint (replies)
- **Visit the profile** → Captures `UserByScreenName` endpoint (profile data)

The extension automatically filters for the tracked handle and stores relevant data.

### 3. Export Captured Data

Click "Export JSON" in the popup to download structured data:

```javascript
// In popup.js - export logic
document.getElementById('exportBtn').addEventListener('click', async () => {
  const response = await chrome.runtime.sendMessage({ type: 'EXPORT_JSON' });
  
  const blob = new Blob([JSON.stringify(response.data, null, 2)], { 
    type: 'application/json' 
  });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `x-${response.trackedHandle}-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  
  URL.revokeObjectURL(url);
});
```

## Captured Data Structure

### Export JSON Schema

```json
{
  "tracked_account": {
    "screen_name": "He4rtDevs",
    "name": "He4rt Developers",
    "rest_id": "1098020856431824897",
    "followers_count": 20945,
    "following_count": 1250,
    "statuses_count": 2178,
    "description": "Community bio...",
    "verified": false
  },
  "exported_at": "2026-05-19T00:15:00.000Z",
  "tweets": [
    {
      "tweet_id": "2056491987205865474",
      "text": "Tweet content...",
      "type": "original",
      "created_at": "2026-05-18T23:30:00.000Z",
      "metrics": {
        "favorite_count": 8,
        "retweet_count": 4,
        "reply_count": 2,
        "quote_count": 1,
        "bookmark_count": 0,
        "view_count": 354
      },
      "hashtags": ["He4rtDevelopers"],
      "user_mentions": [{"screen_name": "He4rtDevs", "id": "..."}],
      "media_count": 2,
      "source": "Twitter for iPhone"
    }
  ],
  "community_replies": [
    {
      "tweet_id": "2056491988000000001",
      "author": {
        "screen_name": "community_member",
        "rest_id": "123456789",
        "followers_count": 150,
        "verified": false
      },
      "text": "Reply text...",
      "in_reply_to_tweet_id": "2056491987205865474",
      "created_at": "2026-05-19T00:00:00.000Z"
    }
  ],
  "favoriters_by_tweet": {
    "2056491987205865474": [
      {
        "rest_id": "987654321",
        "screen_name": "engaged_user",
        "name": "Display Name",
        "followers_count": 500,
        "following": true,
        "followed_by": true,
        "verified": false
      }
    ]
  },
  "summary": {
    "total_tweets": 20,
    "total_original": 15,
    "total_retweets": 3,
    "total_replies": 2,
    "total_community_replies": 45,
    "total_likes": 500,
    "total_views": 15000,
    "avg_likes_per_original": 33,
    "avg_views_per_original": 1000,
    "unique_engagers": 87,
    "top_tweet_by_likes": "2052386746126553531",
    "top_tweet_by_views": "2051468028299153703"
  }
}
```

## Integration with Backend (Laravel Example)

### Ingestion Command

```php
<?php

namespace App\Console\Commands;

use App\Models\TwitterAccount;
use App\Models\Tweet;
use App\Models\CommunityEngagement;
use Illuminate\Console\Command;

class IngestTwitterAnalytics extends Command
{
    protected $signature = 'analytics:ingest {file}';
    protected $description = 'Ingest exported JSON from He4rt Analytics extension';

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
            ['rest_id' => $data['tracked_account']['rest_id']],
            [
                'screen_name' => $data['tracked_account']['screen_name'],
                'name' => $data['tracked_account']['name'],
                'followers_count' => $data['tracked_account']['followers_count'],
                'following_count' => $data['tracked_account']['following_count'] ?? null,
                'statuses_count' => $data['tracked_account']['statuses_count'],
                'description' => $data['tracked_account']['description'] ?? null,
                'verified' => $data['tracked_account']['verified'] ?? false,
            ]
        );

        $this->info("Updated account: @{$account->screen_name}");

        // Upsert tweets
        foreach ($data['tweets'] as $tweetData) {
            Tweet::updateOrCreate(
                ['tweet_id' => $tweetData['tweet_id']],
                [
                    'twitter_account_id' => $account->id,
                    'text' => $tweetData['text'],
                    'type' => $tweetData['type'],
                    'created_at' => $tweetData['created_at'],
                    'favorite_count' => $tweetData['metrics']['favorite_count'],
                    'retweet_count' => $tweetData['metrics']['retweet_count'],
                    'reply_count' => $tweetData['metrics']['reply_count'],
                    'quote_count' => $tweetData['metrics']['quote_count'],
                    'view_count' => $tweetData['metrics']['view_count'] ?? null,
                    'hashtags' => json_encode($tweetData['hashtags'] ?? []),
                    'media_count' => $tweetData['media_count'] ?? 0,
                ]
            );
        }

        $this->info("Ingested {$data['summary']['total_tweets']} tweets");

        // Track community replies
        foreach ($data['community_replies'] ?? [] as $reply) {
            CommunityEngagement::updateOrCreate(
                [
                    'tweet_id' => $reply['tweet_id'],
                    'author_rest_id' => $reply['author']['rest_id'],
                ],
                [
                    'author_screen_name' => $reply['author']['screen_name'],
                    'engagement_type' => 'reply',
                    'in_reply_to_tweet_id' => $reply['in_reply_to_tweet_id'],
                    'followers_count' => $reply['author']['followers_count'],
                    'engaged_at' => $reply['created_at'],
                ]
            );
        }

        // Track favoriters
        foreach ($data['favoriters_by_tweet'] ?? [] as $tweetId => $users) {
            foreach ($users as $user) {
                CommunityEngagement::updateOrCreate(
                    [
                        'tweet_id' => $tweetId,
                        'author_rest_id' => $user['rest_id'],
                        'engagement_type' => 'like',
                    ],
                    [
                        'author_screen_name' => $user['screen_name'],
                        'followers_count' => $user['followers_count'],
                        'is_mutual' => $user['following'] && $user['followed_by'],
                        'engaged_at' => now(), // Approximate
                    ]
                );
            }
        }

        $this->info("Tracked {$data['summary']['unique_engagers']} unique engagers");
        $this->info("Ingestion complete!");

        return 0;
    }
}
```

### Database Schema Example

```php
// Migration for tweets table
Schema::create('tweets', function (Blueprint $table) {
    $table->id();
    $table->string('tweet_id')->unique();
    $table->foreignId('twitter_account_id')->constrained();
    $table->text('text');
    $table->enum('type', ['original', 'retweet', 'reply', 'quote']);
    $table->integer('favorite_count')->default(0);
    $table->integer('retweet_count')->default(0);
    $table->integer('reply_count')->default(0);
    $table->integer('quote_count')->default(0);
    $table->integer('view_count')->nullable();
    $table->json('hashtags')->nullable();
    $table->integer('media_count')->default(0);
    $table->timestamps();
    
    $table->index('created_at');
});

// Migration for community_engagements table
Schema::create('community_engagements', function (Blueprint $table) {
    $table->id();
    $table->string('tweet_id');
    $table->string('author_rest_id');
    $table->string('author_screen_name');
    $table->enum('engagement_type', ['like', 'reply', 'retweet', 'quote']);
    $table->string('in_reply_to_tweet_id')->nullable();
    $table->integer('followers_count')->nullable();
    $table->boolean('is_mutual')->default(false);
    $table->timestamp('engaged_at')->nullable();
    $table->timestamps();
    
    $table->unique(['tweet_id', 'author_rest_id', 'engagement_type']);
    $table->index('author_screen_name');
});
```

## Extension Development Patterns

### Adding Custom GraphQL Endpoint Parsing

To capture additional endpoints, modify `background.js`:

```javascript
// In background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GRAPHQL_RESPONSE') {
    const { url, data, trackedHandle } = message;

    // Custom endpoint: Retweeters
    if (url.includes('Retweeters')) {
      const retweeters = extractRetweeters(data);
      const tweetId = extractTweetIdFromUrl(url);
      
      chrome.storage.local.get(['retweetersByTweet'], (result) => {
        const existing = result.retweetersByTweet || {};
        existing[tweetId] = retweeters;
        
        chrome.storage.local.set({ retweetersByTweet: existing });
      });
    }
  }
});

function extractRetweeters(data) {
  try {
    const timeline = data?.data?.retweeters_timeline?.timeline;
    const entries = timeline?.instructions?.find(i => i.type === 'TimelineAddEntries')?.entries || [];
    
    return entries
      .filter(e => e.entryId.startsWith('user-'))
      .map(e => {
        const user = e.content?.itemContent?.user_results?.result?.legacy;
        return {
          rest_id: user?.id_str,
          screen_name: user?.screen_name,
          name: user?.name,
          followers_count: user?.followers_count,
        };
      })
      .filter(u => u.rest_id);
  } catch (e) {
    console.error('Error extracting retweeters:', e);
    return [];
  }
}
```

### Custom Export Filters

Filter exported data programmatically:

```javascript
// Export only high-performing tweets
async function exportHighPerformers(minLikes = 10, minViews = 1000) {
  const response = await chrome.runtime.sendMessage({ type: 'EXPORT_JSON' });
  const data = response.data;
  
  data.tweets = data.tweets.filter(t => 
    t.metrics.favorite_count >= minLikes && 
    t.metrics.view_count >= minViews
  );
  
  // Recalculate summary
  data.summary.total_tweets = data.tweets.length;
  data.summary.total_likes = data.tweets.reduce((sum, t) => sum + t.metrics.favorite_count, 0);
  
  return data;
}
```

### Webhook Integration (Auto-Push)

Instead of manual exports, push to an API endpoint:

```javascript
// In background.js - add periodic sync
chrome.alarms.create('syncAnalytics', { periodInMinutes: 60 });

chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === 'syncAnalytics') {
    const data = await buildExportJSON();
    
    // Push to your API
    fetch(process.env.HE4RT_API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.HE4RT_API_TOKEN}`,
      },
      body: JSON.stringify(data),
    })
    .then(res => console.log('Synced analytics:', res.status))
    .catch(err => console.error('Sync failed:', err));
  }
});
```

## Troubleshooting

### Extension Not Capturing Data

**Symptom**: Popup shows 0 tweets captured after browsing

**Solutions**:
1. **Check tracked handle**: Open popup → verify handle is set correctly (no @ symbol)
2. **Verify you're on x.com**: Extension only runs on `*://x.com/*` and `*://twitter.com/*`
3. **Inspect console**: Right-click extension icon → Inspect popup → check Console for errors
4. **Check background service worker**: `chrome://extensions/` → He4rt Analytics → "service worker" link → check logs
5. **Reload extension**: Toggle off/on in `chrome://extensions/`

### Favoriters Not Captured

**Symptom**: `favoriters_by_tweet` is empty in export

**Cause**: Must manually click on the like count to trigger the `Favoriters` GraphQL request

**Solution**: 
- Click the "X likes" text on a tweet (not the heart icon)
- Wait for modal to load
- Scroll through the list of users
- Extension captures all visible users

### Duplicate Tweets in Export

**Symptom**: Same `tweet_id` appears multiple times

**Cause**: Bug in deduplication logic in `background.js`

**Solution**: Check `consolidateTweets()` function uses proper Map-based deduplication:

```javascript
function consolidateTweets(tweets) {
  const map = new Map();
  
  tweets.forEach(tweet => {
    if (!map.has(tweet.tweet_id)) {
      map.set(tweet.tweet_id, tweet);
    }
  });
  
  return Array.from(map.values());
}
```

### CSP Errors in Console

**Symptom**: `Refused to execute inline script` errors

**Cause**: X.com's Content Security Policy blocks inline scripts

**Solution**: Ensure `interceptor.js` uses `"world": "MAIN"` in `manifest.json`:

```json
{
  "content_scripts": [
    {
      "matches": ["*://x.com/*", "*://twitter.com/*"],
      "js": ["interceptor.js"],
      "run_at": "document_start",
      "world": "MAIN"
    }
  ]
}
```

### Extension Breaks X.com Functionality

**Symptom**: X.com stops loading tweets or errors out

**Cause**: `fetch()` patch breaking original requests

**Solution**: Ensure `interceptor.js` properly clones and passes through responses:

```javascript
const originalFetch = window.fetch;
window.fetch = async function(...args) {
  const response = await originalFetch.apply(this, args);
  
  // Clone before reading (response can only be read once)
  const clonedResponse = response.clone();
  
  // Process clone, return original
  processGraphQLResponse(args[0], clonedResponse);
  
  return response; // Original unmodified
};
```

## Environment Variables

When integrating with backend APIs, use environment variables:

```javascript
// For Chrome extensions, use chrome.storage for config
chrome.storage.sync.get(['apiEndpoint', 'apiToken'], (config) => {
  const API_ENDPOINT = config.apiEndpoint || 'https://hub.heartdevs.com/api/analytics';
  const API_TOKEN = config.apiToken || '';
  
  // Use in fetch calls
});
```

Set via options page:

```javascript
// options.js
document.getElementById('saveConfig').addEventListener('click', () => {
  const apiEndpoint = document.getElementById('apiEndpoint').value;
  const apiToken = document.getElementById('apiToken').value;
  
  chrome.storage.sync.set({ apiEndpoint, apiToken }, () => {
    alert('Configuration saved!');
  });
});
```

## Best Practices

1. **Respect Rate Limits**: Don't auto-scroll aggressively; capture data during normal browsing
2. **Privacy**: Only track public data; never capture DMs or private account data
3. **Data Hygiene**: Regularly export and clear old data to prevent storage bloat
4. **Testing**: Test on a secondary account before tracking production community accounts
5. **Version Control**: Keep `manifest.json` version synced with releases for update tracking
