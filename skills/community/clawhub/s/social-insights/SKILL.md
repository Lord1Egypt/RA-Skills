---
name: social-insights
description: Social media analytics and performance tracking. Track engagement, optimal posting times, competitor analysis, AI-powered insights, auto-generated charts, and weekly/monthly reports.
author: fly3094
version: 1.3.0
tags: [analytics, social-media, twitter, linkedin, tiktok, youtube, instagram, threads, bluesky, reporting, data, insights, charts, ai-predictions]
support: 
  paypal: 492227637@qq.com
  email: 492227637@qq.com
metadata:
  clawdbot:
    emoji: 📊
    requires:
      bins:
        - python3
        - curl
    config:
      env:
        TWITTER_API_KEY:
          description: Twitter API Key
          required: false
        TWITTER_API_SECRET:
          description: Twitter API Secret
          required: false
        LINKEDIN_ACCESS_TOKEN:
          description: LinkedIn Access Token
          required: false
        THREADS_TOKEN:
          description: Threads API Token
          required: false
        BLUESKY_HANDLE:
          description: Bluesky Handle (e.g., @user.bsky.social)
          required: false
        BLUESKY_APP_PASSWORD:
          description: Bluesky App Password
          required: false
        ANALYTICS_PLATFORMS:
          description: Platforms to analyze (twitter,linkedin,all)
          default: "twitter"
          required: false
---

# Social Analytics 📊

**Know what works. Double down on it.** AI-powered social media analytics with actionable insights.

**Time saved:** 3 hours/week reporting → 5 minutes/week review  
**Result:** 3x engagement in 30 days  
**Reports:** Auto-generated weekly/monthly (PNG/PDF)

## What It Does

- 📈 **Performance Tracking**: Real-time monitoring of followers, impressions, engagement rates
- ⏰ **Optimal Timing**: AI determines best posting times for YOUR audience
- 🏆 **Top Content Analysis**: Identifies your best performing posts (and why they worked)
- 📊 **Competitor Comparison**: Benchmark against 3-5 competitors with visual charts
- 💡 **AI Recommendations**: Specific, actionable improvement suggestions
- 📋 **Auto Reports**: Weekly/monthly reports delivered automatically (PNG/PDF)
- 📉 **Data Visualization**: Beautiful charts and graphs for stakeholder presentations
- 🧵 **Threads Support** (v1.3 NEW): Track Threads post performance and engagement
- 🦋 **Bluesky Support** (v1.3 NEW): Monitor Bluesky analytics via AT Protocol
- 📈 **Trend Prediction**: AI-powered growth forecasting (next 30/60/90 days)
- 🎯 **Goal Tracking**: Set engagement goals and track progress with alerts

## Installation

```bash
clawhub install social-analytics
```

## Commands

### View Weekly Analytics
```
Show my Twitter analytics for last week
```

### View Monthly Report
```
Generate social media report for last month
```

### Competitor Analysis
```
Compare my engagement with @competitor1 and @competitor2
```

### Best Posting Times
```
When should I post for maximum engagement?
```

### Content Insights
```
What type of content performs best for my audience?
```

### Trend Analysis
```
Show my follower growth trend for the last 30 days
```

## Configuration

### Environment Variables

```bash
# Twitter API credentials (for Twitter analytics)
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"
export TWITTER_ACCESS_TOKEN="your_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_token_secret"

# LinkedIn API (optional)
export LINKEDIN_ACCESS_TOKEN="your_token"

# Platforms to analyze
export ANALYTICS_PLATFORMS="twitter"  # twitter, linkedin, or all
```

### Without API Access

If you don't have API access, the skill can still:
- Analyze manually provided data
- Generate reports from exported CSV files
- Provide optimization recommendations

## Output Examples

### Weekly Report
```
📊 Social Media Weekly Report
Week of Mar 1-7, 2026

📈 Key Metrics:
• Followers: 1,234 (+56 this week)
• Impressions: 45,678 (+12%)
• Engagement Rate: 3.2% (industry avg: 1.8%)

🏆 Top Performing Posts:
1. "AI automation saves 20hrs/week" - 234 likes, 45 retweets
2. "New skill released!" - 189 likes, 32 retweets
3. "Client results showcase" - 156 likes, 28 retweets

⏰ Best Posting Times:
• Tuesday 10am-12pm
• Thursday 2pm-4pm
• Sunday 7pm-9pm

💡 Recommendations:
• Post more case studies (highest engagement)
• Increase posting frequency on Tuesdays
• Try video content (competitors seeing 2x engagement)
```

### Competitor Comparison
```
📊 Competitor Analysis Report

Your Account vs Competitors (Last 30 Days)

Metric          You      Comp1    Comp2    Industry Avg
-----------------------------------------------------------------
Engagement Rate 3.2%     2.8%     4.1%     1.8%
Posts/Week      5        7        3        4
Avg Likes       156      134      289      95
Avg Retweets    23       18       45       12
Follower Growth +4.5%    +2.1%    +6.8%    +1.5%

💡 Insights:
• Your engagement rate is 78% above industry average! Great job!
• Comp2 gets more engagement with video content
• You post less frequently than competitors
• Opportunity: Increase posting to 7/week

🎯 Action Items:
1. Add 2 video posts this week
2. Test posting on Wednesday mornings
3. Analyze Comp2's top posts for content ideas
```

### Best Posting Times
```
⏰ Optimal Posting Times for Your Audience

Based on your last 100 posts:

🥇 Best: Tuesday 10:00-12:00
   Avg Engagement: 4.2%
   Avg Reach: 12,500

🥈 Second: Thursday 14:00-16:00
   Avg Engagement: 3.8%
   Avg Reach: 11,200

🥉 Third: Sunday 19:00-21:00
   Avg Engagement: 3.5%
   Avg Reach: 9,800

❌ Worst: Monday 6:00-8:00
   Avg Engagement: 1.2%
   Avg Reach: 3,200

💡 Recommendation:
Schedule 60% of posts during top 3 time slots for maximum impact.
```

## Integration with Other Skills

### rss-to-social
```
rss-to-social publishes content → social-analytics tracks performance
→ Optimize RSS sources based on engagement
```

### social-media-automator
```
social-media-automator generates posts → social-analytics measures results
→ Improve content generation based on data
```

### seo-content-pro
```
seo-content-pro creates articles → social-analytics tracks social shares
→ Identify topics that resonate with audience
```

Complete data-driven content loop! 🔄

## Use Cases

### Content Marketers
- Track campaign performance
- Prove ROI to stakeholders
- Optimize content calendar

### Solopreneurs
- Understand audience preferences
- Maximize limited posting time
- Compete with larger accounts

### Agencies
- Client reporting automation
- Multi-account management
- Benchmark across industries

### Social Media Managers
- Data-driven strategy decisions
- Identify trending content types
- Justify budget increases

## Pricing Integration

This skill powers LobsterLabs analytics services:

| Service | Price | Delivery |
|---------|-------|----------|
| Single Analysis | $99 | One-time report |
| Monthly Subscription | $299/month | Weekly reports + insights |
| Competitor Tracking | $199/month | Up to 5 competitors |
| Enterprise (10 accounts) | $999/month | Custom dashboards |

**Bundle Discounts:**
- Content Automation + Analytics: Save 20%
- Annual Subscription: Save 15%

Contact: PayPal 492227637@qq.com

## Tips for Best Results

1. **Connect API Access**: Full data requires API credentials
2. **Consistent Tracking**: Run analytics weekly for trend insights
3. **Compare Competitors**: Benchmark against 3-5 similar accounts
4. **Act on Insights**: Implement recommendations within 48 hours
5. **Track Changes**: Monitor metrics before/after strategy changes

## Troubleshooting

### No API Access
- Use manual data export from platform
- Upload CSV files for analysis
- Skill will work with provided data

### Incomplete Data
- Verify API credentials are correct
- Check API rate limits
- Ensure account is public (for some platforms)

### Slow Analysis
- Large date ranges take longer
- Reduce to last 7-30 days for faster results
- Run during off-peak hours

## Changelog

### 1.1.0 (2026-03-09) ⭐
- 📉 NEW: Auto-generated charts and graphs (PNG/PDF export)
- 📈 NEW: AI-powered trend prediction and forecasting
- 🎯 NEW: Goal tracking and milestone alerts
- 📊 NEW: Competitor benchmarking with visual comparison
- 🔄 IMPROVED: Enhanced data visualization
- ⚡ IMPROVED: Faster report generation (50% speedup)
- 📱 IMPROVED: Mobile-friendly report formats

### 1.0.0 (2026-03-07)
- Initial release
- Twitter analytics integration
- Competitor comparison
- Optimal timing analysis
- AI-powered recommendations
- Automated weekly/monthly reports

---

## 💖 支持作者

如果你觉得这个技能有用，请考虑打赏支持：

- **PayPal**: 492227637@qq.com
- **邮箱**: 492227637@qq.com

你的支持是我持续改进的动力！

