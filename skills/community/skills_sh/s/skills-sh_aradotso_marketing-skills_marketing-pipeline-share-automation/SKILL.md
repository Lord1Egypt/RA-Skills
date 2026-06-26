---
name: marketing-pipeline-share-automation
description: Automated content pipeline from research to video generation using AI (Claude/OpenAI) and Remotion
triggers:
  - how do I automate content creation with AI
  - set up an automated marketing pipeline
  - generate videos from articles automatically
  - crawl news sources and create content
  - use Claude and OpenAI for content generation
  - automate research to video workflow
  - build an AI content creation system
  - create multilingual marketing content with AI
---

# Marketing Pipeline Share - AI Content Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This TypeScript-based system automates the entire content creation workflow: from researching trending topics across news sources (TechCrunch, a16z, Twitter/X, LinkedIn) to generating articles in multiple formats and languages, then rendering them as videos using Remotion.

## What It Does

- **Auto-Research**: Crawls real-time data from major tech/business news sources
- **AI Content Generation**: Creates articles in various formats (toplists, POV, case studies, how-tos) using Claude 3 or OpenAI
- **Multi-language Support**: Generates content in English and Vietnamese simultaneously
- **Video Rendering**: Automatically converts articles to videos/infographics optimized for Reels, TikTok, Shorts
- **Next.js Interface**: Web UI for managing the entire pipeline

## Installation

```bash
# Clone the repository
git clone https://github.com/pennydinh/marketing-pineline-share.git
cd marketing-pineline-share

# Install dependencies
npm install
# or
yarn install
# or
pnpm install
```

## Environment Configuration

Create a `.env.local` file in the root directory:

```env
# AI APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_claude_key

# RapidAPI for news/data crawling
RAPIDAPI_KEY=your_rapidapi_key

# Remotion (for video rendering)
REMOTION_LICENSE_KEY=your_remotion_license

# Next.js
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## Project Structure

```
marketing-pineline-share/
├── app/                    # Next.js app directory
├── components/             # React components
├── lib/
│   ├── ai/                # AI integration (Claude, OpenAI)
│   ├── crawler/           # News crawling logic
│   ├── content/           # Content generation templates
│   └── video/             # Remotion video rendering
├── public/                # Static assets
└── remotion/              # Remotion video compositions
```

## Core Usage Patterns

### 1. Research & Content Generation Pipeline

```typescript
import { researchTopic } from '@/lib/crawler/research';
import { generateContent } from '@/lib/ai/content-generator';

// Research a topic from multiple sources
async function createContent(keyword: string) {
  // Step 1: Crawl and analyze recent data
  const researchData = await researchTopic({
    keyword,
    sources: ['techcrunch', 'a16z', 'twitter', 'linkedin'],
    timeframe: '24h'
  });

  // Step 2: Generate article using AI
  const content = await generateContent({
    research: researchData,
    format: 'toplist', // or 'pov', 'case-study', 'how-to'
    languages: ['en', 'vi'],
    tone: 'professional', // or 'friendly', 'humorous'
    aiProvider: 'claude' // or 'openai'
  });

  return content;
}
```

### 2. Using Claude for Content Generation

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function generateWithClaude(prompt: string, research: any) {
  const message = await anthropic.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 4096,
    messages: [
      {
        role: 'user',
        content: `Based on this research data: ${JSON.stringify(research)}
        
        ${prompt}
        
        Create engaging content that is data-backed and trend-focused.`
      }
    ],
  });

  return message.content[0].text;
}
```

### 3. Using OpenAI Alternative

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function generateWithOpenAI(prompt: string, research: any) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [
      {
        role: 'system',
        content: 'You are an expert content creator specializing in marketing and tech trends.'
      },
      {
        role: 'user',
        content: `Research data: ${JSON.stringify(research)}\n\n${prompt}`
      }
    ],
    temperature: 0.7,
  });

  return completion.choices[0].message.content;
}
```

### 4. News Crawling Implementation

```typescript
import axios from 'axios';

async function crawlTechCrunch(keyword: string) {
  const options = {
    method: 'GET',
    url: 'https://techcrunch-api.p.rapidapi.com/search',
    params: { query: keyword, limit: '10' },
    headers: {
      'X-RapidAPI-Key': process.env.RAPIDAPI_KEY,
      'X-RapidAPI-Host': 'techcrunch-api.p.rapidapi.com'
    }
  };

  const response = await axios.request(options);
  return response.data;
}

async function aggregateResearch(keyword: string) {
  const [techcrunch, twitter, linkedin] = await Promise.all([
    crawlTechCrunch(keyword),
    crawlTwitter(keyword),
    crawlLinkedIn(keyword)
  ]);

  // Analyze and extract insights
  return {
    articles: [...techcrunch, ...twitter, ...linkedin],
    insights: extractInsights([...techcrunch, ...twitter, ...linkedin]),
    trending: identifyTrends([...techcrunch, ...twitter, ...linkedin])
  };
}
```

### 5. Video Generation with Remotion

```typescript
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import { ArticleComposition } from '@/remotion/ArticleComposition';

async function renderArticleVideo(article: any) {
  // Bundle the Remotion project
  const bundleLocation = await bundle({
    entryPoint: './remotion/index.ts',
    webpackOverride: (config) => config,
  });

  // Select composition
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: 'ArticleVideo',
    inputProps: {
      title: article.title,
      content: article.content,
      style: 'reels' // or 'tiktok', 'shorts'
    },
  });

  // Render video
  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: `out/${article.id}.mp4`,
  });
}
```

### 6. Remotion Composition Example

```typescript
// remotion/ArticleComposition.tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';

export const ArticleComposition: React.FC<{
  title: string;
  content: string;
  style: 'reels' | 'tiktok' | 'shorts';
}> = ({ title, content, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = Math.min(1, frame / fps);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#1a1a1a',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div style={{ opacity, padding: 40 }}>
        <h1 style={{ color: 'white', fontSize: 48 }}>{title}</h1>
        <p style={{ color: '#aaa', fontSize: 24, marginTop: 20 }}>
          {content}
        </p>
      </div>
    </AbsoluteFill>
  );
};
```

### 7. Complete Pipeline API Route

```typescript
// app/api/generate/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { keyword, format, languages } = await req.json();

    // Step 1: Research
    const research = await researchTopic({
      keyword,
      sources: ['techcrunch', 'twitter'],
      timeframe: '24h'
    });

    // Step 2: Generate content
    const articles = await Promise.all(
      languages.map(lang =>
        generateContent({
          research,
          format,
          language: lang,
          aiProvider: 'claude'
        })
      )
    );

    // Step 3: Render videos
    const videos = await Promise.all(
      articles.map(article => renderArticleVideo(article))
    );

    return NextResponse.json({
      success: true,
      articles,
      videos
    });
  } catch (error) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

## Running the Application

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Render Remotion videos
npm run remotion:render
```

## Content Format Templates

### Toplist Format

```typescript
const toplistPrompt = `
Create a toplist article about ${keyword}.
Include:
- 5-10 items with compelling headlines
- Data-backed reasoning for each item
- Recent examples (within 24h if possible)
- Actionable takeaways
`;
```

### POV (Point of View) Format

```typescript
const povPrompt = `
Write a POV article on ${keyword}.
Structure:
- Strong opening statement
- Personal/industry perspective
- Contrarian or unique angle
- Supporting evidence from research
- Call to action
`;
```

### Case Study Format

```typescript
const caseStudyPrompt = `
Create a case study about ${keyword}.
Include:
- Company/situation background
- Challenge statement
- Solution approach
- Results with metrics
- Key learnings
`;
```

## Troubleshooting

### API Rate Limits

```typescript
// Implement retry logic with exponential backoff
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, i) * 1000)
      );
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Video Rendering Memory Issues

```typescript
// Use smaller chunks and stream rendering
const renderConfig = {
  codec: 'h264',
  concurrency: 1, // Reduce for memory constraints
  everyNthFrame: 1,
  numberOfGifLoops: 0,
};
```

### Multi-language Content Quality

```typescript
// Use language-specific models or instructions
const languageConfigs = {
  en: { model: 'claude-3-5-sonnet-20241022', tone: 'professional' },
  vi: { model: 'claude-3-5-sonnet-20241022', tone: 'friendly' }
};
```

## Performance Optimization

```typescript
// Cache research results
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.REDIS_URL,
  token: process.env.REDIS_TOKEN,
});

async function getCachedResearch(keyword: string) {
  const cached = await redis.get(`research:${keyword}`);
  if (cached) return cached;

  const fresh = await researchTopic({ keyword });
  await redis.setex(`research:${keyword}`, 3600, JSON.stringify(fresh));
  return fresh;
}
```

This system enables end-to-end content automation, from discovering trending topics to publishing ready-to-use video content across multiple platforms.
