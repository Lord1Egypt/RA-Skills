---
name: social-media-automator
description: Automatically generate social media posts from articles. Supports Twitter, LinkedIn, Instagram, TikTok, YouTube Shorts, Threads, and Bluesky. Perfect for content repurposing.
author: fly3094
version: 1.2.0
support: 
  paypal: 492227637@qq.com
  email: 492227637@qq.com
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["curl"]},"install":[{"kind":"npm","package":"threads-api"},{"kind":"npm","package":"@atproto/api"}]}}
---

# Social Media Automator 📱

**One article → 20+ social posts.** Transform long-form content into platform-perfect posts in seconds.

**Time saved:** 2 hours/post → 2 minutes/post  
**Platforms:** Twitter, LinkedIn, Instagram, TikTok, YouTube Shorts

## What It Does

- 📄 **Article Analysis**: Extracts key points, quotes, and data from any article/URL
- 🐦 **Twitter Thread**: Generates 3-10 tweet threads with viral hooks
- 💼 **LinkedIn Post**: Creates professional long-form posts (1000-1300 chars)
- 📸 **Instagram Caption**: Writes engaging captions with 10-15 hashtags
- 🎵 **TikTok/Shorts Script**: 30-60 second video scripts with hook optimization
- 🖼️ **AI Image Prompts**: DALL-E 3/Canva prompts for post visuals
- 📅 **Scheduling**: Buffer/Hootsuite ready formats
- 🔄 **A/B Variations**: 3-5 versions per platform for testing

## Commands

### Generate All Posts
```
Create social media posts from "[article URL or text]"
```

### Twitter Thread Only
```
Generate Twitter thread from "[article]" - 5 tweets
```

### LinkedIn Post Only
```
Create LinkedIn post from "[article]"
```

### With Scheduling
```
Generate posts from "[article]" and schedule for next week
```

### TikTok/Shorts Script
```
Create TikTok script from "[article]" - 60 seconds
```

### With Image Prompts
```
Generate posts from "[article]" with AI image prompts
```

## Output Format

### Twitter Thread (3-10 tweets)
- Hook tweet (attention-grabbing)
- Key points (1 per tweet)
- Data/statistics highlighted
- Call-to-action on final tweet
- Relevant hashtags (2-3 per tweet)

### LinkedIn Post
- Professional tone
- 1000-1300 characters
- Line breaks for readability
- 3-5 industry hashtags
- Engagement question at end

### Instagram Caption
- Casual, engaging tone
- 150-200 characters
- 10-15 relevant hashtags
- Emoji usage
- Story idea suggestions

### TikTok/YouTube Shorts Script
- Hook (first 3 seconds)
- Main content (30-60 seconds)
- Call-to-action
- Trending hashtag suggestions
- Visual direction notes

### AI Image Prompts
- DALL-E 3 optimized prompts
- Canva design suggestions
- Aspect ratio recommendations
- Style references

## Configuration

Optional environment variables:
- `DEFAULT_PLATFORM`: Default platform (twitter|linkedin|instagram|all)
- `THREAD_LENGTH`: Default Twitter thread length (default: 5)
- `INCLUDE_EMOJIS`: Add emojis to posts (true|false, default: true)
- `HASHTAG_COUNT`: Number of hashtags (default: 3)

## Example Usage

**User**: Generate Twitter thread from my article "10 Best AI Automation Tools" - 7 tweets

**Assistant**: 
1. Analyzing article content...
2. Extracting 7 key points...
3. Writing hook tweet...
4. Generating thread with engagement hooks...
5. Adding relevant hashtags...

✅ Twitter thread ready!

**Tweet 1/7**: 
Stop wasting hours on repetitive tasks 🛑

I analyzed 50+ AI automation tools. These 10 will save you 20+ hours/week.

Thread 🧵👇

#AI #Automation #Productivity

**Tweet 2/7**: 
1. Zapier - The gold standard for no-code automation

Connects 6,000+ apps. Perfect for beginners.

Starts at $19.99/mo

...

## Use Cases

### Content Marketers
- Turn 1 blog post into 2 weeks of social content
- Maintain consistent posting schedule
- Test different messaging

### Solopreneurs
- Automate your entire social presence
- Focus on creation, not distribution
- Build audience while you sleep

### Agencies
- Scale content delivery for clients
- White-label social media management
- Charge $500-2000/mo for this service

## Integration with SEO Content Engine

This skill works perfectly with the SEO Content Engine:

1. Write article with SEO Content Engine
2. Generate social posts with Social Media Automator
3. Schedule and publish
4. Drive traffic back to your content

Full content automation loop! 🔄

## Pricing Integration

This skill powers LobsterLabs social media services:
- Single article → social posts: $50
- Monthly social pack (4 articles): $300
- Full social media management: $800-1500/month

Contact: PayPal 492227637@qq.com

## Tips for Best Results

1. **Provide context**: Tell the skill your target audience
2. **Specify tone**: Professional, casual, or humorous
3. **Add examples**: Share posts you like for style reference
4. **Review before posting**: AI is great, but add your voice
5. **Use image prompts**: Generate visuals for higher engagement
6. **Test variations**: Use A/B test versions to optimize performance

## New in v1.0.0

### 🎵 TikTok/YouTube Shorts Support
- 30-60 second video scripts
- Hook optimization for first 3 seconds
- Trending hashtag suggestions
- Visual direction notes

### 🖼️ AI Image Generation
- DALL-E 3 optimized prompts
- Canva design templates
- Aspect ratio recommendations
- Style references (minimalist, bold, corporate, etc.)

### 📊 Enhanced Analytics Integration
- Post performance tracking
- Best time to post recommendations
- Engagement rate optimization
- Competitor benchmarking

### 🔄 A/B Testing Variations
- 3-5 post variations per platform
- Different hooks and CTAs
- Hashtag set variations
- Optimal posting time suggestions

## Integration with rss-to-social

This skill works great with the **rss-to-social** skill:
- rss-to-social: Auto-monitor RSS feeds and post on schedule
- social-media-automator: Manual post generation from specific articles

Use both for complete content automation!

## Changelog

### 1.0.0 (2026-03-09) ⭐
- 🎵 NEW: TikTok/YouTube Shorts script generation
- 🖼️ NEW: AI image prompts (DALL-E 3, Canva)
- 📊 NEW: Enhanced analytics integration
- 🔄 NEW: A/B testing variations (3-5 versions)
- 📈 NEW: Post performance tracking
- ⏰ NEW: Best time to post recommendations
- 🎨 IMPROVED: Instagram story suggestions
- 🏷️ IMPROVED: Hashtag optimization algorithm

### 0.2.0 (2026-03-07)
- Added integration with rss-to-social skill
- Improved hashtag suggestions
- Better platform-specific formatting
- Added A/B testing variations

### 0.1.0 (2026-03-06)
- Initial release
- Twitter thread generation
- LinkedIn post creation
- Instagram caption support
- Hashtag suggestions

---

## 💖 支持作者

如果你觉得这个技能有用，请考虑打赏支持：

- **PayPal**: 492227637@qq.com
- **邮箱**: 492227637@qq.com

你的支持是我持续改进的动力！

