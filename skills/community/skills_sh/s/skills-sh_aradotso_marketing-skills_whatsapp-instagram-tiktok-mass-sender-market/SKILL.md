---
name: whatsapp-instagram-tiktok-mass-sender-marketing
description: Automated social media mass messaging and group marketing system for WhatsApp, Instagram, and TikTok customer acquisition
triggers:
  - how do I scrape TikTok followers automatically
  - setup Instagram mass DM sender
  - automate WhatsApp group marketing messages
  - extract competitor followers from social media
  - bulk send messages on Instagram and TikTok
  - configure automated social media lead generation
  - scrape hashtag users from Instagram
  - automate TikTok comment interactions
---

# WhatsApp Instagram TikTok Mass Sender Marketing

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This project provides automated mass messaging and group marketing capabilities across WhatsApp, Instagram, and TikTok platforms. It enables scraping competitor followers, hashtag-based user extraction, automated engagement (likes, comments, follows), and bulk direct messaging for customer acquisition and traffic generation.

## What It Does

- **Competitor Follower Scraping**: Extract follower lists from competitor accounts on Instagram and TikTok
- **Hashtag & Keyword Targeting**: Find users posting or engaging with specific hashtags/keywords
- **Automated Engagement**: Auto-follow, auto-like, auto-comment on target user content
- **Bulk Messaging**: Send personalized direct messages at scale across platforms
- **AI-Powered Filtering**: Filter users by demographics, engagement level, account quality
- **Multi-Account Management**: Operate multiple accounts simultaneously for matrix marketing
- **WhatsApp Group Marketing**: Bulk send to WhatsApp groups and contacts

## Installation

This is a commercial/proprietary system accessed through the vendor's platform rather than self-hosted code. Based on the repository structure:

### Access Setup

1. **Register for Service**
   ```bash
   # Visit official platform
   https://sites.google.com/view/facebook-script-custom/
   ```

2. **Technical Support Channel**
   ```bash
   # Online support
   https://sites.google.com/view/instagram-keyword-hashtag-lead/
   ```

3. **Account Configuration**
   ```javascript
   // Typical configuration structure for multi-platform automation
   const config = {
     platforms: ['instagram', 'tiktok', 'whatsapp'],
     accounts: [
       {
         platform: 'instagram',
         username: process.env.IG_USERNAME,
         password: process.env.IG_PASSWORD,
         proxy: process.env.IG_PROXY
       },
       {
         platform: 'tiktok',
         username: process.env.TT_USERNAME,
         password: process.env.TT_PASSWORD,
         proxy: process.env.TT_PROXY
       }
     ],
     automation: {
       delayBetweenActions: 3000, // ms
       dailyFollowLimit: 150,
       dailyMessageLimit: 50,
       randomizeDelays: true
     }
   };
   ```

## Key Features & API Patterns

### 1. Follower Scraping

```javascript
// Scrape competitor followers on Instagram
const scraperConfig = {
  targetAccount: '@competitor_username',
  platform: 'instagram',
  filters: {
    minFollowers: 100,
    maxFollowers: 10000,
    activeWithinDays: 30,
    location: 'United States',
    verifiedOnly: false
  },
  maxResults: 5000
};

// Execute scrape
async function scrapeFollowers(config) {
  const results = await api.scrape({
    type: 'followers',
    target: config.targetAccount,
    platform: config.platform,
    filters: config.filters,
    limit: config.maxResults
  });
  
  return results.users; // Array of user objects
}
```

### 2. Hashtag-Based Lead Generation

```javascript
// Find users by hashtag on TikTok
const hashtagConfig = {
  hashtags: ['#skincare', '#beautyproducts', '#antiaging'],
  platform: 'tiktok',
  filters: {
    engagement: 'high', // high/medium/low
    accountAge: 90, // days
    followerRange: [500, 50000]
  },
  limit: 3000
};

async function getHashtagUsers(config) {
  const users = await api.extractByHashtag({
    tags: config.hashtags,
    platform: config.platform,
    filters: config.filters,
    maxUsers: config.limit
  });
  
  // AI filtering
  const filtered = await api.aiFilter(users, {
    detectGender: true,
    estimateAge: true,
    removeBusinessAccounts: false,
    removeBots: true
  });
  
  return filtered;
}
```

### 3. Automated Engagement

```javascript
// Auto-engage with scraped users
const engagementConfig = {
  users: [], // Array from scraping
  actions: {
    follow: true,
    like: { enabled: true, postsCount: 3 },
    comment: { 
      enabled: true, 
      templates: [
        "Love this! 😍",
        "Amazing content! 🔥",
        "Great post! 💯"
      ],
      randomize: true
    }
  },
  timing: {
    delayBetweenUsers: [5000, 15000], // Random delay range (ms)
    dailyLimit: 100,
    stopOnError: false
  }
};

async function autoEngage(config) {
  for (const user of config.users) {
    try {
      if (config.actions.follow) {
        await api.follow(user.username);
        await delay(random(config.timing.delayBetweenUsers));
      }
      
      if (config.actions.like.enabled) {
        const posts = await api.getUserPosts(user.username, config.actions.like.postsCount);
        for (const post of posts) {
          await api.like(post.id);
          await delay(random(2000, 5000));
        }
      }
      
      if (config.actions.comment.enabled) {
        const comment = randomChoice(config.actions.comment.templates);
        await api.comment(posts[0].id, comment);
      }
      
      await delay(random(config.timing.delayBetweenUsers));
    } catch (error) {
      console.error(`Error engaging with ${user.username}:`, error);
      if (config.timing.stopOnError) break;
    }
  }
}
```

### 4. Bulk Direct Messaging

```javascript
// Mass DM campaign
const dmConfig = {
  recipients: [], // User list from scraping
  message: {
    text: "Hi {name}! 👋 Noticed you're into {interest}. Check out our exclusive offer: {link}",
    variables: {
      link: process.env.LANDING_PAGE_URL,
      interest: 'skincare' // Dynamic per user
    },
    personalize: true
  },
  schedule: {
    messagesPerHour: 10,
    startTime: '09:00',
    endTime: '18:00',
    timezone: 'America/New_York'
  },
  tracking: {
    enabled: true,
    trackClicks: true,
    trackReplies: true
  }
};

async function sendBulkDMs(config) {
  const queue = [...config.recipients];
  
  while (queue.length > 0) {
    const batch = queue.splice(0, config.schedule.messagesPerHour);
    
    for (const user of batch) {
      const personalizedMsg = config.message.text
        .replace('{name}', user.name || user.username)
        .replace('{interest}', user.interests?.[0] || config.message.variables.interest)
        .replace('{link}', config.message.variables.link);
      
      await api.sendDM({
        to: user.username,
        message: personalizedMsg,
        platform: user.platform,
        trackingId: config.tracking.enabled ? generateTrackingId(user) : null
      });
      
      await delay(random(5000, 10000));
    }
    
    // Wait before next batch
    if (queue.length > 0) {
      await delay(3600000 / config.schedule.messagesPerHour);
    }
  }
}
```

### 5. WhatsApp Group Marketing

```javascript
// WhatsApp bulk sending
const whatsappConfig = {
  mode: 'group', // 'group' or 'individual'
  groups: [
    { id: 'group-id-1', name: 'Marketing Group' },
    { id: 'group-id-2', name: 'Sales Team' }
  ],
  message: {
    text: "🎉 New Product Launch! Check it out: {link}",
    media: {
      type: 'image',
      url: process.env.PRODUCT_IMAGE_URL
    }
  },
  schedule: {
    sendAt: '2026-06-01T10:00:00Z',
    timezone: 'UTC'
  }
};

async function sendWhatsAppBulk(config) {
  if (config.mode === 'group') {
    for (const group of config.groups) {
      await api.whatsapp.sendToGroup({
        groupId: group.id,
        text: config.message.text.replace('{link}', process.env.LANDING_PAGE_URL),
        media: config.message.media,
        scheduleTime: config.schedule.sendAt
      });
      
      await delay(random(30000, 60000)); // Delay between groups
    }
  }
}
```

## Configuration Best Practices

### Environment Variables

```bash
# Platform Credentials
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
TT_USERNAME=your_tiktok_username
TT_PASSWORD=your_tiktok_password
WA_PHONE=your_whatsapp_number

# Proxies (recommended to avoid bans)
IG_PROXY=http://proxy1.example.com:8080
TT_PROXY=http://proxy2.example.com:8080

# Campaign Settings
LANDING_PAGE_URL=https://yoursite.com/offer
PRODUCT_IMAGE_URL=https://yoursite.com/product.jpg
DAILY_FOLLOW_LIMIT=150
DAILY_MESSAGE_LIMIT=50
```

### Rate Limiting & Safety

```javascript
// Recommended rate limits to avoid platform detection
const safeLimits = {
  instagram: {
    followsPerHour: 20,
    likesPerHour: 60,
    commentsPerHour: 15,
    dmsPerHour: 10,
    dailyFollowLimit: 150,
    dailyUnfollowLimit: 150
  },
  tiktok: {
    followsPerHour: 30,
    likesPerHour: 100,
    commentsPerHour: 20,
    dmsPerHour: 15
  },
  whatsapp: {
    messagesPerHour: 30,
    groupsPerHour: 5
  }
};

// Implement delays
function getRandomDelay(min = 3000, max = 8000) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
```

## Common Patterns

### Pattern 1: Competitor Traffic Hijacking

```javascript
// Complete workflow: Scrape → Filter → Engage → Convert
async function competitorHijackingCampaign() {
  // Step 1: Scrape competitor followers
  const followers = await scrapeFollowers({
    targetAccount: '@main_competitor',
    platform: 'instagram',
    filters: { minFollowers: 500, maxFollowers: 20000 },
    maxResults: 2000
  });
  
  // Step 2: AI filter for quality
  const qualified = await api.aiFilter(followers, {
    removeBusinessAccounts: true,
    removeBots: true,
    estimateAge: true,
    ageRange: [18, 45]
  });
  
  // Step 3: Soft engagement
  await autoEngage({
    users: qualified.slice(0, 100), // Start with 100
    actions: {
      follow: true,
      like: { enabled: true, postsCount: 2 }
    },
    timing: { dailyLimit: 100 }
  });
  
  // Step 4: Wait 24-48h, then DM engaged users
  setTimeout(async () => {
    const engaged = await api.getFollowBacks(qualified);
    await sendBulkDMs({
      recipients: engaged,
      message: {
        text: "Hey {name}! Saw you follow @main_competitor. We have a better deal 😊 {link}"
      }
    });
  }, 86400000 * 2); // 48 hours
}
```

### Pattern 2: Hashtag-Based Funnel

```javascript
// Find hot leads via trending hashtags
async function hashtagFunnel() {
  const leads = await getHashtagUsers({
    hashtags: ['#needthis', '#wheretobuy', '#recommendations'],
    platform: 'tiktok',
    filters: { engagement: 'high' },
    limit: 1000
  });
  
  // Immediate soft touch
  await autoEngage({
    users: leads,
    actions: {
      follow: true,
      like: { enabled: true, postsCount: 1 },
      comment: { 
        enabled: true,
        templates: ["Check your DMs! 💌"]
      }
    }
  });
  
  // Same-day DM with solution
  await sendBulkDMs({
    recipients: leads,
    message: {
      text: "Hi! Saw your post about {interest}. We've got exactly what you need: {link}"
    },
    schedule: { messagesPerHour: 20 }
  });
}
```

### Pattern 3: Multi-Platform Matrix

```javascript
// Coordinate campaigns across IG + TikTok + WhatsApp
async function multiPlatformBlitz() {
  const igUsers = await scrapeFollowers({
    targetAccount: '@competitor_ig',
    platform: 'instagram',
    maxResults: 1000
  });
  
  const ttUsers = await getHashtagUsers({
    hashtags: ['#productniche'],
    platform: 'tiktok',
    limit: 1000
  });
  
  // Parallel engagement
  await Promise.all([
    autoEngage({ users: igUsers, actions: { follow: true, like: { enabled: true, postsCount: 2 } } }),
    autoEngage({ users: ttUsers, actions: { follow: true, comment: { enabled: true } } })
  ]);
  
  // Collect phone numbers from bio scraping (if available)
  const phoneNumbers = await api.extractPhoneNumbers([...igUsers, ...ttUsers]);
  
  // WhatsApp retargeting
  if (phoneNumbers.length > 0) {
    await api.whatsapp.sendBulk({
      recipients: phoneNumbers,
      message: "Special offer for our social followers! {link}"
    });
  }
}
```

## Troubleshooting

### Issue: Account Getting Banned/Restricted

**Solution**: Implement stricter rate limits and human-like behavior

```javascript
// Add randomization and longer delays
const conservativeConfig = {
  delayBetweenActions: [10000, 30000], // 10-30 seconds
  dailyFollowLimit: 50, // Reduce from 150
  dailyMessageLimit: 20, // Reduce from 50
  randomizeDelays: true,
  useProxy: true,
  rotateProxies: true,
  sessionDuration: [1800000, 3600000] // 30-60 min sessions
};

// Add session breaks
async function engageWithBreaks(users) {
  const sessionSize = 20;
  for (let i = 0; i < users.length; i += sessionSize) {
    const batch = users.slice(i, i + sessionSize);
    await autoEngage({ users: batch });
    
    // Break between sessions (15-30 min)
    if (i + sessionSize < users.length) {
      await delay(random(900000, 1800000));
    }
  }
}
```

### Issue: Low DM Response Rate

**Solution**: Improve message personalization and timing

```javascript
// Better personalization
async function improvePersonalization(user) {
  const recentPosts = await api.getUserPosts(user.username, 5);
  const interests = await api.extractInterests(recentPosts);
  
  const templates = {
    skincare: "Hey {name}! Your skin looks amazing in your recent posts! Have you tried {product}?",
    fitness: "Hi {name}! Loved your workout content. Check out our fitness supplement: {link}",
    fashion: "Hey {name}! Your style is 🔥 You'd love our new collection: {link}"
  };
  
  const category = interests[0] || 'general';
  return templates[category] || templates.general;
}

// Send at optimal times
const optimalTimes = {
  instagram: ['10:00', '14:00', '19:00'], // Peak engagement hours
  tiktok: ['12:00', '17:00', '21:00']
};
```

### Issue: Scraping Returns Duplicate Users

**Solution**: Implement deduplication

```javascript
// Deduplicate across campaigns
const seenUsers = new Set();

function deduplicateUsers(users) {
  return users.filter(user => {
    const key = `${user.platform}:${user.username}`;
    if (seenUsers.has(key)) return false;
    seenUsers.add(key);
    return true;
  });
}

// Persist to avoid re-contacting
const fs = require('fs');
function saveContactedUsers(users) {
  const existing = JSON.parse(fs.readFileSync('contacted.json', 'utf8') || '[]');
  const updated = [...existing, ...users.map(u => u.username)];
  fs.writeFileSync('contacted.json', JSON.stringify([...new Set(updated)]));
}
```

### Issue: API Rate Limits from Platform

**Solution**: Use proxy rotation and account rotation

```javascript
// Proxy rotation
const proxyPool = [
  process.env.PROXY_1,
  process.env.PROXY_2,
  process.env.PROXY_3
];

let currentProxyIndex = 0;

function getNextProxy() {
  const proxy = proxyPool[currentProxyIndex];
  currentProxyIndex = (currentProxyIndex + 1) % proxyPool.length;
  return proxy;
}

// Account rotation for high-volume
const accountPool = [
  { username: process.env.IG_USER_1, password: process.env.IG_PASS_1 },
  { username: process.env.IG_USER_2, password: process.env.IG_PASS_2 }
];

async function distributeLoad(users, action) {
  const perAccount = Math.ceil(users.length / accountPool.length);
  
  for (let i = 0; i < accountPool.length; i++) {
    const batch = users.slice(i * perAccount, (i + 1) * perAccount);
    await api.switchAccount(accountPool[i]);
    await action(batch);
  }
}
```

## Legal & Ethical Considerations

**Important**: This type of automation may violate platform Terms of Service. Use responsibly:

- Respect user privacy and platform policies
- Implement opt-out mechanisms in DMs
- Comply with anti-spam regulations (CAN-SPAM, GDPR)
- Use only for legitimate business purposes
- Monitor and respect platform rate limits
- Ensure proxy/account usage complies with local laws

```javascript
// Add opt-out footer to all DMs
const compliantMessage = `
${originalMessage}

---
Reply STOP to opt out of future messages.
`;

// Track opt-outs
async function checkOptOut(username) {
  const optOuts = JSON.parse(fs.readFileSync('optouts.json', 'utf8') || '[]');
  return optOuts.includes(username);
}
```
