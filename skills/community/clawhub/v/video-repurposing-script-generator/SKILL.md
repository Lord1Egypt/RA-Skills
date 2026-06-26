---
name: video-repurposing-script-generator
description: "Generate platform-specific social scripts from long-form video content. Analyzes YouTube, Loom, webinars and creates TikTok hooks, Instagram Reels, LinkedIn posts, Twitter threads, and email sequences optimized for algorithm engagement. Use when the user needs to repurpose video content, maximize reach across platforms, or automate social media posting."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","YOUTUBE_API_KEY"],"bins":["ffmpeg"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🎬"}}
---

# Video Repurposing Script Generator

## Overview

The Video Repurposing Script Generator transforms long-form video content into platform-optimized social media scripts in seconds. Instead of manually creating separate content for TikTok, Instagram, LinkedIn, Twitter, and email—each with different lengths, hooks, and formatting requirements—this skill analyzes your video and intelligently extracts key moments, generates platform-specific scripts, and applies proven engagement patterns for each channel's algorithm.

**Why this matters:** A single 30-minute webinar or YouTube video can generate 15-20 pieces of social content. Without automation, this takes 3-4 hours of manual work. This skill does it in 2-3 minutes, maintaining quality and platform-specific optimization.

**Integrations:** Works seamlessly with YouTube (via YouTube Data API v3), Loom, Vimeo, Google Drive transcription, Zapier automation, WordPress (via REST API for blog cross-posting), Slack (for team notifications), Buffer (for scheduling), and HubSpot (for email sequence distribution).

---

## Quick Start

### Example 1: YouTube Video to Multi-Platform Content

```
I have a 28-minute YouTube video about "5 AI Productivity Hacks for Remote Teams" 
(URL: https://youtube.com/watch?v=dXxxx). Generate TikTok hooks, Instagram Reels 
captions, and a Twitter thread from the key moments. Focus on actionable tips.
```

**Expected output:** 5 TikTok hooks (15-60 seconds each), 3 Instagram Reels scripts with hashtag strategies, and a 12-tweet thread with timestamps.

### Example 2: Webinar to Email Sequence

```
I recorded a 45-minute webinar on "SaaS Pricing Psychology" (transcription attached). 
Create a 5-email nurture sequence that breaks down the key insights, with subject 
lines optimized for open rates, and include timestamps linking back to the original video.
```

**Expected output:** 5 complete emails with A/B subject line variants, body copy optimized for mobile, CTA buttons, and embedded video timestamps.

### Example 3: Loom Recording to LinkedIn Strategy

```
Loom video: https://loom.com/share/xxxxx (Product demo for a project management tool)
Create 3 LinkedIn posts with different angles: 1) Problem/Solution, 2) Behind-the-scenes, 
3) Customer success story. Include optimal posting times and engagement hooks.
```

**Expected output:** 3 complete LinkedIn posts (1,300 characters each), captions with professional hashtags, optimal posting times by timezone, and engagement prediction scores.

---

## Capabilities

### 1. **Intelligent Video Analysis**
- Automatically transcribes video using OpenAI Whisper API (supports 99+ languages)
- Detects emotional peaks, key statements, and turning points using sentiment analysis
- Identifies speaker pauses, emphasis patterns, and natural segment breaks
- Extracts visual cues (text overlays, graphics, speaker changes) from video frames
- Timestamps all key moments for easy reference and linking

### 2. **Platform-Specific Script Generation**

#### TikTok Hooks (15-60 seconds)
- Creates 5-7 hook variations using proven patterns: "Wait for the plot twist," pattern interrupts, curiosity gaps
- Optimizes for TikTok's algorithm (watch time, replays, shares)
- Includes trending sound recommendations
- Generates captions with trending hashtags (#FYP, #ForYouPage, niche-specific tags)

#### Instagram Reels (30-90 seconds)
- Generates 3-4 complete scripts with visual direction notes
- Includes caption templates with emoji strategies and hashtag placement
- Optimizes for Instagram's Reels algorithm (saves, shares, profile visits)
- Provides music/audio pairing recommendations
- Creates carousel post variants (5-10 slides) for static content

#### LinkedIn Posts (1,200-1,500 characters)
- Creates 3-5 angle variations: thought leadership, industry insights, personal story, educational, announcement
- Optimizes for LinkedIn algorithm (engagement rate, connection growth, recruiter visibility)
- Includes optimal posting times by timezone and day
- Generates professional hashtag strategies (5-8 relevant hashtags)
- Adds CTA variations for different goals (comments, shares, profile visits)

#### Twitter/X Threads (12-20 tweets)
- Generates complete thread with hook tweet + supporting tweets
- Optimizes thread structure: hook → context → key points → call-to-action
- Includes visual/media recommendations (images, GIFs, video embeds)
- Maintains character limits and readability
- Provides engagement prediction and reply-baiting strategies

#### Email Sequences (3-7 emails)
- Creates drip campaigns with A/B subject line variants
- Optimizes for open rates, click rates, and conversions
- Includes video timestamp links for easy viewing
- Generates mobile-responsive HTML templates
- Provides send-time optimization recommendations

### 3. **Algorithm Optimization**
- Applies platform-specific engagement patterns (TikTok: watch time + replays; LinkedIn: comments + shares)
- Generates hook variations targeting different audience segments
- Includes CTA optimization for each platform's primary action
- Provides engagement prediction scores (estimated reach, engagement rate)
- Recommends posting schedules based on audience timezone data

### 4. **Customization & Personalization**
- Tone adjustment: formal, casual, educational, entertaining, motivational
- Industry-specific terminology and examples
- Target audience customization (C-suite, students, entrepreneurs, etc.)
- Brand voice consistency across all platforms
- Hashtag strategy customization (trending vs. evergreen)

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API for transcription and script generation
export OPENAI_API_KEY="sk-proj-xxxxx"

# YouTube API for fetching video metadata and transcripts
export YOUTUBE_API_KEY="AIzaSyDxxxxx"

# Optional: For direct Loom integration
export LOOM_API_KEY="loom_xxxxx"

# Optional: For Buffer scheduling integration
export BUFFER_API_KEY="buffer_xxxxx"

# Optional: For HubSpot email distribution
export HUBSPOT_API_KEY="pat-na1-xxxxx"
```

### Setup Instructions

1. **Get OpenAI API Key:**
   - Visit https://platform.openai.com/api-keys
   - Create new secret key
   - Store in `.env` file: `OPENAI_API_KEY=sk-proj-xxxxx`

2. **Get YouTube API Key:**
   - Go to Google Cloud Console (console.cloud.google.com)
   - Create new project
   - Enable YouTube Data API v3
   - Create API key under Credentials
   - Store in `.env` file: `YOUTUBE_API_KEY=AIzaSyDxxxxx`

3. **Install Dependencies:**
   ```bash
   npm install openai youtube-transcript-api dotenv
   # or
   pip install openai youtube-transcript-api python-dotenv
   ```

4. **Initialize Skill:**
   ```bash
   openclaw init video-repurposing-script-generator
   openclaw config set OPENAI_API_KEY "sk-proj-xxxxx"
   openclaw config set YOUTUBE_API_KEY "AIzaSyDxxxxx"
   ```

### Configuration Options

```yaml
# Optional config.yml for advanced users
video_repurposing:
  transcription:
    language: "en"  # auto-detect or specify
    speaker_identification: true
    
  platforms:
    tiktok:
      enabled: true
      hook_count: 5
      include_sounds: true
      
    instagram:
      enabled: true
      reel_count: 3
      carousel_variants: true
      
    linkedin:
      enabled: true
      post_count: 4
      include_hashtags: true
      timezone: "America/New_York"
      
    twitter:
      enabled: true
      thread_length: 15
      
    email:
      enabled: true
      sequence_length: 5
      
  optimization:
    tone: "professional"  # or casual, educational, entertaining
    target_audience: "entrepreneurs"
    industry: "SaaS"
    brand_voice: "thought-leadership"
```

---

## Example Outputs

### Input: 15-minute YouTube video on "Personal Branding Mistakes"

### Output 1: TikTok Hook Scripts

```
HOOK #1 (Pattern Interrupt):
"Stop building your personal brand the wrong way 🚫"
[Visual: Text overlay on red background]
[Hook: 3 seconds] → [Main content: 45 seconds]
[CTA: "Swipe up for the free guide"]
Trending sounds: "Dramatic reveal" audio
Hashtags: #PersonalBranding #CareerTips #FYP #MistakesIveMade

HOOK #2 (Curiosity Gap):
"I made this personal branding mistake for 5 years..."
[Visual: Speaker talking to camera, concerned expression]
[Hook: 2 seconds] → [Reveal: 50 seconds]
[CTA: "Follow for more career advice"]
Hashtags: #CareerGrowth #PersonalBrand #Entrepreneur

HOOK #3 (Trend Jacking):
[Uses trending TikTok audio: "Wait, that's not right"]
"When you realize your personal brand is hurting your career..."
[Visual: Quick cuts between mistakes and solutions]
[Duration: 45 seconds]
```

### Output 2: LinkedIn Post Angles

```
ANGLE #1 - Thought Leadership:
"I spent 5 years building my personal brand wrong. Here's what I learned.

Building a personal brand isn't about vanity—it's about strategic positioning. 
I made 3 critical mistakes that cost me opportunities:

1️⃣ Being everything to everyone (no niche focus)
2️⃣ Talking AT my audience instead of WITH them
3️⃣ Inconsistent messaging across platforms

The shift happened when I stopped chasing trends and started solving real 
problems for my target audience.

What personal branding mistakes have you made? Share below—I'd love to learn 
from your experience.

#PersonalBranding #CareerDevelopment #Leadership #ProfessionalGrowth"

Optimal posting time: Tuesday 9:00 AM ET
Predicted engagement: 4.2% (high for your network)
Hashtags: #PersonalBranding #CareerDevelopment #Leadership

---

ANGLE #2 - Educational Value:
"Personal Branding 101: The 3 Mistakes Killing Your Career

If you're building a personal brand, avoid these:

❌ Mistake #1: Unclear positioning
Your audience shouldn't have to guess what you do. Be specific about your 
niche, expertise, and unique value.

❌ Mistake #2: Inconsistent voice
Your LinkedIn posts, Twitter, and email should sound like YOU—not a generic 
corporate robot. Consistency builds trust.

❌ Mistake #3: No engagement strategy
Personal branding isn't a broadcast channel. It's a conversation. Reply to 
comments. Ask questions. Build community.

The companies and opportunities that matter? They're watching. Make sure 
you're showing them the best version of yourself.

#PersonalBranding #CareerAdvice #ProfessionalDevelopment"

Optimal posting time: Thursday 10:30 AM ET
Predicted engagement: 3.8%
```

### Output 3: Email Sequence (Day 1)

```
SUBJECT LINE A: "The personal branding mistake I made for 5 years"
SUBJECT LINE B: "Why your personal brand isn't working (and how to fix it)"

---

Email Body:

Hi [First Name],

I made a big mistake when I started building my personal brand.

For 5 years, I was doing everything wrong—and I didn't even know it.

I was:
✗ Trying to appeal to everyone (and connecting with no one)
✗ Sharing generic advice instead of my real perspective
✗ Inconsistent across platforms
✗ Not engaging with my audience

The turning point came when I realized that personal branding isn't about 
being famous. It's about being *known* for something specific.

In the video I just recorded, I break down the 3 biggest mistakes I see 
people making—and exactly how to fix them.

[WATCH THE VIDEO] (Timestamp: 2:34-8:15)

This 6-minute section covers:
• Why "being everything to everyone" kills your brand
• The one thing your audience actually cares about
• How to stay consistent without being boring

I'd love to hear what resonates with you. Hit reply and let me know which 
mistake you're currently making—I read every response.

Talk soon,
[Your Name]

P.S. — If you found this valuable, forward it to someone building their 
personal brand. They'll thank you for it.

---

CTA Button: [WATCH NOW - 6 MIN VIDEO]
CTA Link: [YouTube URL with timestamp]
```

---

## Tips & Best Practices

### 1. **Video Quality Matters**
- Clearer audio = better transcription = better scripts
- Use a decent microphone (even a $30 USB mic makes a difference)
- Minimize background noise for accurate transcription
- Speak clearly and at a moderate pace (the skill handles accents, but clarity helps)

### 2. **Provide Context for Better Results**
```
Instead of just: "Generate TikTok scripts from this video"

Try: "This is a webinar for SaaS founders (target: bootstrapped B2B companies). 
Generate 5 TikTok hooks that emphasize actionable, quick wins. Tone: casual 
but credible. Use trending sounds from the finance/business niche."
```

### 3. **Optimize for Your Audience**
- Specify target audience demographics (age, industry, role)
- Mention your current follower count (helps algorithm predictions)
- Share your engagement rates (skill calibrates content difficulty)
- Note any brand voice guidelines (tone, language, taboo topics)

### 4. **Batch Process Multiple Videos**
- Process 2-3 videos in one session to maintain consistency
- Use the same tone/audience settings across batches
- Build a content calendar by scheduling outputs in advance

### 5. **A/B Test Hook Variations**
- The skill generates 5-7 variations for each platform
- Test 2-3 variations simultaneously
- Track which hooks generate highest engagement
- Share results back with the skill for personalized learning

### 6. **Timestamp Linking Strategy**
- Always include video timestamps in social posts
- Links back to original video boost watch time (YouTube algorithm loves this)
- Increases email click-through rates (people want to see the source)
- LinkedIn timestamps drive profile visits

### 7. **Hashtag Timing**
- Use trending hashtags in first 24 hours (TikTok, Instagram)
- Switch to evergreen hashtags after 48 hours (LinkedIn, Twitter)
- Monitor hashtag performance and adjust strategy
- Ask the skill to research trending hashtags in your niche

### 8. **Email Sequence Timing**
- Send Day 1 email within 24 hours of video publication
- Space Day 2-5 emails 2-3 days apart
- Include timestamps in every email (not just first)
- Test send times based on your audience timezone

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Copyright Infringement:** This skill does not generate content from copyrighted videos you don't own. Always ensure you have rights to repurpose video content.

❌ **Misinformation:** The skill extracts and repurposes only factual statements from your video. It won't fabricate claims or "fill in" missing information.

❌ **Spam/Manipulation:** Generated content follows platform community guidelines. The skill won't create deceptive hooks, clickbait, or engagement-bait that violates platform policies.

❌ **Personal Data Extraction:** If your video contains personal information (names, addresses, emails), the skill will flag these and ask for confirmation before including in scripts.

❌ **Deepfake/Synthetic Media:** This skill