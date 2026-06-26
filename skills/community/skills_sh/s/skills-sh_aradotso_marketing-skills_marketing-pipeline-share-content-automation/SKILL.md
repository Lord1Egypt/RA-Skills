---
name: marketing-pipeline-share-content-automation
description: AI-powered content pipeline that auto-researches, generates scripts, and creates videos with Claude/OpenAI and Remotion
triggers:
  - automate my content creation workflow
  - generate blog posts from trending topics
  - create videos from text content automatically
  - research and write marketing content with AI
  - build a content automation pipeline
  - set up AI content generation system
  - scrape news and generate articles
  - render videos from blog posts with Remotion
---

# Marketing Pipeline Share - AI Content Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

Marketing Pipeline Share is an all-in-one TypeScript-based content automation system that:
- **Auto-researches** trending topics by crawling news sources (TechCrunch, Twitter, LinkedIn)
- **Generates content** in multiple formats (listicles, POV, case studies) using Claude 3/OpenAI
- **Renders videos** automatically from text using Remotion
- **Supports multilingual** content (English/Vietnamese) with customizable tone
- **Provides end-to-end pipeline** from research to publication

This tool transforms a single keyword into full blog posts, social media content, and video assets.

## Installation

```bash
# Clone the repository
git clone https://github.com/pennydinh/marketing-pineline-share.git
cd marketing-pineline-share

# Install dependencies
npm install
# or
yarn install

# Set up environment variables
cp .env.example .env
```

### Required Environment Variables

```bash
# AI Providers
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key

# Data Sources (RapidAPI)
RAPIDAPI_KEY=your_rapidapi_key

# Optional: Custom endpoints
API_BASE_URL=http://localhost:3000
```

## Project Structure

```
marketing-pineline-share/
├── src/
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── lib/
│   │   ├── ai/          # AI integration (Claude, OpenAI)
│   │   ├── scraper/     # Web scraping modules
│   │   ├── content/     # Content generation logic
│   │   └── video/       # Remotion video rendering
│   └── types/           # TypeScript type definitions
├── remotion/            # Video templates
└── public/              # Static assets
```

## Core Features & Usage

### 1. Research & Content Scraping

```typescript
import { researchTopic } from '@/lib/scraper';

// Auto-scrape trending news from multiple sources
async function gatherResearch(keyword: string) {
  const research = await researchTopic({
    keyword,
    sources: ['techcrunch', 'twitter', 'linkedin'],
    timeframe: '24h',
    limit: 20
  });
  
  return {
    articles: research.articles,
    insights: research.insights,
    statistics: research.stats
  };
}
```

### 2. AI Content Generation

```typescript
import { generateContent } from '@/lib/ai/content-generator';

// Generate blog post with Claude/OpenAI
async function createBlogPost(topic: string, research: any) {
  const content = await generateContent({
    provider: 'claude', // or 'openai'
    model: 'claude-3-sonnet-20240229',
    format: 'blog-post', // 'listicle', 'case-study', 'how-to'
    topic,
    research,
    language: 'en', // or 'vi'
    tone: 'professional', // 'friendly', 'humorous'
    length: 'medium' // 'short', 'long'
  });
  
  return {
    title: content.title,
    body: content.body,
    meta: content.metadata,
    images: content.suggestedImages
  };
}
```

### 3. Multi-Format Content Generation

```typescript
import { ContentPipeline } from '@/lib/content/pipeline';

// Generate content in multiple formats from single input
async function generateMultiFormat(keyword: string) {
  const pipeline = new ContentPipeline({
    apiKey: process.env.ANTHROPIC_API_KEY
  });
  
  // Research phase
  await pipeline.research(keyword);
  
  // Generate multiple formats in parallel
  const outputs = await pipeline.generateAll({
    formats: [
      { type: 'blog-post', language: 'en' },
      { type: 'blog-post', language: 'vi' },
      { type: 'social-media', platform: 'linkedin' },
      { type: 'social-media', platform: 'twitter' },
      { type: 'video-script', duration: 60 }
    ]
  });
  
  return outputs;
}
```

### 4. Video Generation with Remotion

```typescript
import { renderVideo } from '@/lib/video/renderer';
import { bundle } from '@remotion/bundler';
import { renderMedia } from '@remotion/renderer';

// Convert blog post to video
async function createVideoFromPost(post: any) {
  const videoConfig = {
    compositionId: 'BlogPostVideo',
    inputProps: {
      title: post.title,
      content: post.body,
      style: 'modern',
      duration: 90 // seconds
    },
    codec: 'h264',
    outputLocation: `./output/${post.slug}.mp4`,
    // Platform-specific ratios
    width: 1080,
    height: 1920 // 9:16 for TikTok/Reels/Shorts
  };
  
  const bundled = await bundle('./src/remotion/index.ts');
  const result = await renderMedia({
    composition: videoConfig,
    serveUrl: bundled,
    codec: 'h264',
    outputLocation: videoConfig.outputLocation
  });
  
  return result;
}
```

## API Endpoints

If running as a Next.js server:

### POST /api/research
```typescript
// Request
{
  "keyword": "AI automation",
  "sources": ["techcrunch", "twitter"],
  "timeframe": "24h"
}

// Response
{
  "articles": [...],
  "insights": [...],
  "trending": true
}
```

### POST /api/generate
```typescript
// Request
{
  "topic": "AI content automation",
  "format": "blog-post",
  "language": "en",
  "research": {...}
}

// Response
{
  "title": "How AI is Transforming Content Creation",
  "body": "...",
  "metadata": {...},
  "images": [...]
}
```

### POST /api/video/render
```typescript
// Request
{
  "content": {...},
  "template": "modern",
  "aspectRatio": "9:16"
}

// Response
{
  "videoUrl": "https://...",
  "thumbnail": "https://...",
  "duration": 90
}
```

## Common Patterns

### Full Pipeline Example

```typescript
import { ContentAutomation } from '@/lib/automation';

async function fullContentPipeline(keyword: string) {
  const automation = new ContentAutomation({
    anthropicKey: process.env.ANTHROPIC_API_KEY,
    openaiKey: process.env.OPENAI_API_KEY,
    rapidApiKey: process.env.RAPIDAPI_KEY
  });
  
  // 1. Research
  console.log('🔍 Researching topic...');
  const research = await automation.research(keyword);
  
  // 2. Generate content
  console.log('✍️ Generating content...');
  const content = await automation.generate({
    topic: keyword,
    research,
    formats: ['blog', 'social', 'video-script']
  });
  
  // 3. Create visuals
  console.log('🎬 Rendering video...');
  const video = await automation.renderVideo({
    script: content.videoScript,
    style: 'professional'
  });
  
  // 4. Export all assets
  return {
    blogPost: content.blog,
    socialPosts: content.social,
    video: video.url,
    publishReady: true
  };
}
```

### Scheduled Content Generation

```typescript
import { CronJob } from 'cron';
import { ContentAutomation } from '@/lib/automation';

// Auto-generate daily content
const dailyContentJob = new CronJob('0 9 * * *', async () => {
  const automation = new ContentAutomation({
    anthropicKey: process.env.ANTHROPIC_API_KEY
  });
  
  const trendingTopics = await automation.getTrendingTopics({
    category: 'marketing',
    count: 3
  });
  
  for (const topic of trendingTopics) {
    const content = await fullContentPipeline(topic);
    await automation.publishToQueue(content);
  }
});

dailyContentJob.start();
```

### Custom Content Templates

```typescript
import { ContentGenerator } from '@/lib/ai/content-generator';

// Create custom content template
const generator = new ContentGenerator({
  provider: 'claude',
  apiKey: process.env.ANTHROPIC_API_KEY
});

const customTemplate = {
  name: 'product-launch',
  structure: [
    { section: 'hook', prompt: 'Create attention-grabbing opening' },
    { section: 'problem', prompt: 'Describe pain points' },
    { section: 'solution', prompt: 'Introduce product benefits' },
    { section: 'features', prompt: 'List 5 key features' },
    { section: 'cta', prompt: 'Strong call-to-action' }
  ],
  tone: 'exciting',
  length: 800
};

const content = await generator.generateFromTemplate(
  customTemplate,
  { product: 'AI Content Tool', audience: 'marketers' }
);
```

## Configuration

### Content Generator Config

```typescript
// src/config/content.ts
export const contentConfig = {
  ai: {
    defaultProvider: 'claude',
    fallbackProvider: 'openai',
    maxTokens: 4000,
    temperature: 0.7
  },
  research: {
    sources: ['techcrunch', 'twitter', 'linkedin', 'producthunt'],
    maxArticles: 20,
    timeframe: '24h'
  },
  video: {
    defaultDuration: 60,
    outputFormat: 'mp4',
    quality: 'high',
    aspectRatios: {
      tiktok: '9:16',
      youtube: '16:9',
      instagram: '1:1'
    }
  }
};
```

### Remotion Video Config

```typescript
// src/remotion/config.ts
export const videoConfig = {
  fps: 30,
  durationInFrames: 90 * 30, // 90 seconds
  width: 1080,
  height: 1920,
  compositions: [
    {
      id: 'BlogPostVideo',
      component: BlogPostComposition,
      defaultProps: {
        theme: 'dark',
        animation: 'smooth'
      }
    }
  ]
};
```

## Troubleshooting

### API Rate Limits
```typescript
// Implement retry logic with exponential backoff
import { retry } from '@/lib/utils/retry';

const content = await retry(
  () => generateContent({ topic, research }),
  { maxAttempts: 3, delayMs: 1000 }
);
```

### Video Rendering Errors
```bash
# Ensure Remotion CLI is installed
npm install -g @remotion/cli

# Check Remotion dependencies
npx remotion versions

# Common fix: Clear bundle cache
rm -rf .remotion
```

### Research Scraping Issues
```typescript
// Handle failed scrapes gracefully
try {
  const research = await researchTopic(keyword);
} catch (error) {
  console.warn('Scraping failed, using fallback');
  // Use cached data or alternative source
  const fallback = await getFallbackResearch(keyword);
}
```

### Memory Issues with Large Content
```typescript
// Process content in chunks
async function processLargeDataset(items: any[]) {
  const chunkSize = 10;
  const results = [];
  
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    const processed = await Promise.all(
      chunk.map(item => generateContent(item))
    );
    results.push(...processed);
  }
  
  return results;
}
```

## Running the Project

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Render single video (CLI)
npx remotion render BlogPostVideo output.mp4 --props='{"title":"My Post"}'
```

## Best Practices

1. **Cache research data** to avoid redundant API calls
2. **Use queue systems** (Bull, BullMQ) for video rendering
3. **Implement webhooks** for async video completion notifications
4. **Store generated content** in database for reuse
5. **Monitor API usage** to stay within rate limits
6. **Version control templates** for consistent output quality

This skill enables AI agents to help developers build complete content automation workflows with research, generation, and video production capabilities.
