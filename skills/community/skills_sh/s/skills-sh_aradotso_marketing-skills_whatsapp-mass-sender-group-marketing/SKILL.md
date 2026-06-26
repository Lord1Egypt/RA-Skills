---
name: whatsapp-mass-sender-group-marketing
description: Automate WhatsApp mass messaging, group marketing, and TikTok/Instagram follower extraction for targeted outreach campaigns
triggers:
  - how do i set up whatsapp mass sender
  - automate instagram follower extraction
  - send bulk whatsapp messages to groups
  - extract tiktok competitor followers
  - configure whatsapp marketing automation
  - scrape instagram users by hashtag
  - setup automated social media lead generation
  - bulk message whatsapp contacts
---

# WhatsApp Mass Sender & Group Marketing System

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

This project provides automated tools for multi-platform social media marketing, focusing on:

- **WhatsApp bulk messaging** and group marketing campaigns
- **TikTok & Instagram follower extraction** from competitor accounts
- **Automated engagement** (likes, comments, follows, DMs)
- **Lead filtering** by demographics, activity, and AI-based criteria
- **Cross-platform automation** for social media growth

**Primary use cases:**
- E-commerce stores running targeted outreach
- Marketing agencies managing multiple client accounts
- MCN organizations building follower bases
- Affiliate marketers finding warm leads

## Installation

Based on the project structure, this appears to be a service-based system rather than self-hosted code. Access is provided through:

```bash
# Official website for system access
https://www.facebook18.com

# Technical support and documentation
https://sites.google.com/view/facebook-script-custom/
https://sites.google.com/view/instagram-keyword-hashtag-lead/
```

### Environment Setup

Store credentials securely using environment variables:

```bash
# .env file
WHATSAPP_API_KEY=your_api_key_here
WHATSAPP_PHONE_NUMBER=+1234567890
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
TIKTOK_SESSION_TOKEN=your_session_token
PROXY_SERVER=http://proxy.example.com:8080
```

## Core Features & Configuration

### 1. WhatsApp Mass Messaging

**Bulk message sending to contacts or groups:**

```python
import os
from whatsapp_marketing import MassSender

# Initialize sender
sender = MassSender(
    api_key=os.getenv('WHATSAPP_API_KEY'),
    phone_number=os.getenv('WHATSAPP_PHONE_NUMBER')
)

# Send to contact list
contacts = ['+1234567890', '+0987654321']
message = "🔥 Special offer today only! Check out our new products at example.com"

sender.send_bulk_message(
    recipients=contacts,
    message=message,
    delay_between=5,  # seconds between messages
    randomize_delay=True
)
```

**Group marketing:**

```python
# Send to multiple WhatsApp groups
groups = ['group_id_1', 'group_id_2', 'group_id_3']

sender.send_to_groups(
    group_ids=groups,
    message="Join our exclusive community! Link: example.com/join",
    schedule_time="2026-06-01 10:00:00"  # Optional scheduled send
)
```

### 2. Instagram Follower Extraction

**Extract followers from competitor accounts:**

```python
from instagram_scraper import FollowerExtractor

extractor = FollowerExtractor(
    username=os.getenv('INSTAGRAM_USERNAME'),
    password=os.getenv('INSTAGRAM_PASSWORD'),
    proxy=os.getenv('PROXY_SERVER')
)

# Extract competitor's followers
competitor_followers = extractor.get_followers(
    target_account='competitor_username',
    max_followers=5000,
    filters={
        'min_followers': 100,
        'max_followers': 10000,
        'is_verified': False,
        'has_profile_picture': True
    }
)

# Save to CSV
extractor.export_to_csv(competitor_followers, 'leads.csv')
```

**Hashtag-based lead extraction:**

```python
# Find users posting with specific hashtags
hashtag_leads = extractor.search_by_hashtag(
    hashtags=['fitness', 'workout', 'gym'],
    engagement_filters={
        'min_likes': 50,
        'min_comments': 5,
        'posted_within_days': 30
    },
    max_results=1000
)

# Filter by demographics
filtered_leads = extractor.filter_by_demographics(
    users=hashtag_leads,
    criteria={
        'age_range': [18, 35],
        'gender': 'any',
        'location': ['US', 'UK', 'CA']
    }
)
```

### 3. TikTok User Extraction

**Extract engaged users from competitor videos:**

```python
from tiktok_scraper import TikTokExtractor

tiktok = TikTokExtractor(
    session_token=os.getenv('TIKTOK_SESSION_TOKEN')
)

# Get users who liked/commented on competitor videos
engaged_users = tiktok.extract_engaged_users(
    video_url='https://tiktok.com/@competitor/video/123456789',
    extraction_type='both',  # 'likes', 'comments', or 'both'
    max_users=2000
)

# Extract followers from competitor profile
competitor_followers = tiktok.get_profile_followers(
    username='competitor_username',
    max_followers=10000
)
```

### 4. Automated Engagement

**Auto-follow, like, and comment:**

```python
from social_automation import EngagementBot

bot = EngagementBot(
    platform='instagram',
    credentials={
        'username': os.getenv('INSTAGRAM_USERNAME'),
        'password': os.getenv('INSTAGRAM_PASSWORD')
    }
)

# Configure engagement campaign
campaign = bot.create_campaign(
    name='Competitor Targeting Q2',
    actions={
        'follow': True,
        'like_posts': 3,  # Like 3 recent posts per user
        'comment': True,
        'send_dm': True
    },
    targets=filtered_leads,
    daily_limit=200,  # Max actions per day
    comment_templates=[
        'Great content! 🔥',
        'Love this! 💯',
        'Amazing post! ✨'
    ],
    dm_template='Hi! I love your content. Check out our page @yourpage 🚀'
)

# Start automated engagement
bot.run_campaign(campaign)
```

### 5. Multi-Account Management

**Manage multiple social accounts:**

```python
from account_manager import MultiAccountManager

manager = MultiAccountManager()

# Add accounts
manager.add_account('instagram', {
    'username': 'account1',
    'password': os.getenv('IG_ACCOUNT1_PASSWORD')
})

manager.add_account('instagram', {
    'username': 'account2',
    'password': os.getenv('IG_ACCOUNT2_PASSWORD')
})

# Rotate accounts for actions
manager.distribute_actions(
    action_type='follow',
    targets=competitor_followers,
    actions_per_account=100
)
```

## Common Patterns

### Lead Generation Workflow

```python
# Complete lead generation and outreach workflow
def automated_lead_funnel():
    # 1. Extract leads from multiple sources
    ig_leads = extractor.get_followers('competitor1', max_followers=5000)
    tiktok_leads = tiktok.get_profile_followers('competitor2', max_followers=5000)
    hashtag_leads = extractor.search_by_hashtag(['yourindustry'], max_results=1000)
    
    # 2. Combine and deduplicate
    all_leads = list(set(ig_leads + tiktok_leads + hashtag_leads))
    
    # 3. Filter high-quality leads
    qualified_leads = extractor.filter_by_demographics(
        users=all_leads,
        criteria={
            'min_followers': 200,
            'max_followers': 50000,
            'has_business_account': False,
            'engagement_rate': 0.02  # 2% minimum
        }
    )
    
    # 4. Automated engagement
    bot.create_campaign(
        name='Auto Funnel',
        actions={'follow': True, 'like_posts': 2, 'send_dm': True},
        targets=qualified_leads,
        daily_limit=150
    )
    
    # 5. Export for WhatsApp follow-up
    phone_numbers = extract_phone_numbers(qualified_leads)
    sender.send_bulk_message(
        recipients=phone_numbers,
        message="Special offer for Instagram followers! Use code IG20: example.com"
    )

automated_lead_funnel()
```

### Scheduled Campaign Management

```python
from scheduler import CampaignScheduler

scheduler = CampaignScheduler()

# Schedule daily follower extraction
scheduler.add_task(
    name='Daily Competitor Scrape',
    function=extractor.get_followers,
    args=['competitor_username'],
    kwargs={'max_followers': 500},
    schedule='daily',
    time='09:00'
)

# Schedule engagement waves
scheduler.add_task(
    name='Morning Engagement',
    function=bot.run_campaign,
    schedule='daily',
    time='10:00'
)

scheduler.add_task(
    name='Evening Engagement',
    function=bot.run_campaign,
    schedule='daily',
    time='18:00'
)

scheduler.start()
```

## API Rate Limiting & Safety

**Implement safe usage patterns:**

```python
from safety import RateLimiter, ActionThrottler

# Configure rate limits
limiter = RateLimiter(
    max_follows_per_hour=50,
    max_likes_per_hour=100,
    max_comments_per_hour=30,
    max_dms_per_hour=20
)

# Use throttler in campaigns
throttler = ActionThrottler(limiter)

def safe_engagement(targets):
    for user in targets:
        # Check rate limits before action
        if throttler.can_follow():
            bot.follow_user(user)
            throttler.record_action('follow')
            
        if throttler.can_like():
            bot.like_recent_posts(user, count=2)
            throttler.record_action('like', count=2)
            
        # Random delay to mimic human behavior
        throttler.human_delay(min_seconds=10, max_seconds=30)
```

## Troubleshooting

### Account Suspension Prevention

```python
# Use rotating proxies
from proxy_rotator import ProxyPool

proxy_pool = ProxyPool([
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080'
])

extractor = FollowerExtractor(
    username=os.getenv('INSTAGRAM_USERNAME'),
    password=os.getenv('INSTAGRAM_PASSWORD'),
    proxy_pool=proxy_pool,
    rotate_every_n_requests=50
)
```

### Session Management

```python
# Handle session expiration
try:
    followers = extractor.get_followers('target_account')
except SessionExpiredError:
    extractor.refresh_session()
    followers = extractor.get_followers('target_account')
```

### Data Export & Integration

```python
# Export to multiple formats
from exporters import DataExporter

exporter = DataExporter()

# CSV export
exporter.to_csv(leads, 'leads.csv', columns=['username', 'followers', 'email'])

# JSON export
exporter.to_json(leads, 'leads.json')

# CRM integration (example: HubSpot)
exporter.to_crm(
    leads,
    crm='hubspot',
    api_key=os.getenv('HUBSPOT_API_KEY'),
    custom_fields={'lead_source': 'Instagram Competitor Scrape'}
)
```

## Best Practices

1. **Always respect platform rate limits** to avoid account bans
2. **Use proxy rotation** for large-scale extraction
3. **Randomize delays** between actions (10-60 seconds)
4. **Store credentials securely** in environment variables
5. **Monitor daily action limits** (follows, likes, DMs)
6. **Test campaigns on small groups** before scaling
7. **Comply with GDPR/privacy laws** when collecting user data
8. **Use multiple accounts** to distribute workload

## Support & Documentation

- Official website: https://www.facebook18.com
- Technical guide: https://sites.google.com/view/facebook-script-custom/
- Lead generation docs: https://sites.google.com/view/instagram-keyword-hashtag-lead/

For implementation support, contact the technical team through the official channels listed above.
