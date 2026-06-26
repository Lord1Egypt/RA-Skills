---
name: marketing-pipeline-ai-content-automation
description: Automate end-to-end content creation from research to video generation using AI (Claude/OpenAI) and Remotion
triggers:
  - how do I automate content creation with AI
  - set up an AI content pipeline with research and video generation
  - generate marketing content automatically from keywords
  - create videos from text using Remotion and AI
  - build an automated content workflow with Claude and OpenAI
  - research and generate blog posts with AI automatically
  - automate social media content creation pipeline
  - generate multilingual content with AI research
---

# Marketing Pipeline AI Content Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill enables AI coding agents to work with the Ultimate AI Content Pipeline, a comprehensive TypeScript-based system that automates content creation from research through video generation. The pipeline automatically scrapes news sources, generates content in multiple formats and languages, and renders videos using Remotion.

## What This Project Does

The Marketing Pipeline automates the entire content creation workflow:

1. **Auto-Research**: Crawls real-time data from TechCrunch, a16z, Twitter/X, LinkedIn
2. **AI Content Generation**: Creates articles in multiple formats (toplist, POV, case study, how-to) using Claude/OpenAI
3. **Multilingual Support**: Generates content in English and Vietnamese simultaneously
4. **Video Rendering**: Automatically creates infographics and short-form videos using Remotion
5. **Platform Optimization**: Outputs content optimized for Reels, TikTok, Shorts

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

```bash
# AI Provider Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_claude_key_here

# Research APIs
RAPIDAPI_KEY=your_rapidapi_key_here

# Database (if applicable)
DATABASE_URL=your_database_connection_string

# Remotion License (if applicable)
REMOTION_LICENSE_KEY=your_remotion_license_key

# Next.js Configuration
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## Project Structure

```
marketing-pineline-share/
├── src/
│   ├── app/              # Next.js app router pages
│   ├── components/       # React components
│   ├── lib/
│   │   ├── ai/          # AI integration (Claude, OpenAI)
│   │   ├── research/    # Content scraping & research
│   │   ├── video/       # Remotion video generation
│   │   └── utils/       # Utility functions
│   └── types/           # TypeScript type definitions
├── public/              # Static assets
└── remotion/            # Remotion video templates
```

## Running the Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Access the application at `http://localhost:3000`

## Core API Patterns

### 1. Content Research Module

```typescript
// src/lib/research/scraper.ts
import axios from 'axios';

interface ResearchResult {
  title: string;
  content: string;
  source: string;
  publishedAt: Date;
  insights: string[];
}

export async function scrapeNews(keyword: string): Promise<ResearchResult[]> {
  const sources = [
    'techcrunch',
    'a16z',
    'twitter',
    'linkedin'
  ];
  
  const results: ResearchResult[] = [];
  
  for (const source of sources) {
    const response = await axios.get(
      `https://api.rapidapi.com/news/${source}`,
      {
        headers: {
          'X-RapidAPI-Key': process.env.RAPIDAPI_KEY,
          'X-RapidAPI-Host': 'news-api.rapidapi.com'
        },
        params: {
          q: keyword,
          sortBy: 'publishedAt',
          language: 'en',
          pageSize: 10
        }
      }
    );
    
    results.push(...response.data.articles);
  }
  
  return results;
}

export async function extractInsights(articles: ResearchResult[]): Promise<string[]> {
  const insights = articles.flatMap(article => {
    // Extract key data points, statistics, trends
    const patterns = [
      /\d+%/g,  // Percentages
      /\$\d+[BM]/g,  // Financial figures
      /\d+ (million|billion|thousand)/gi  // Large numbers
    ];
    
    return patterns.flatMap(pattern => 
      article.content.match(pattern) || []
    );
  });
  
  return [...new Set(insights)];
}
```

### 2. AI Content Generation

```typescript
// src/lib/ai/content-generator.ts
import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

interface ContentConfig {
  format: 'toplist' | 'pov' | 'case-study' | 'how-to';
  tone: 'expert' | 'friendly' | 'humorous';
  language: 'en' | 'vi';
  keywords: string[];
  research: string;
}

export async function generateContentClaude(config: ContentConfig): Promise<string> {
  const prompt = buildPrompt(config);
  
  const message = await anthropic.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 4096,
    messages: [
      {
        role: 'user',
        content: prompt
      }
    ]
  });
  
  return message.content[0].type === 'text' 
    ? message.content[0].text 
    : '';
}

export async function generateContentOpenAI(config: ContentConfig): Promise<string> {
  const prompt = buildPrompt(config);
  
  const completion = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [
      {
        role: 'system',
        content: 'You are an expert content creator specializing in marketing and tech content.'
      },
      {
        role: 'user',
        content: prompt
      }
    ],
    temperature: 0.7,
    max_tokens: 4096
  });
  
  return completion.choices[0]?.message?.content || '';
}

function buildPrompt(config: ContentConfig): string {
  const formatInstructions = {
    'toplist': 'Create a numbered list article with at least 5 items',
    'pov': 'Write from a unique perspective or opinion piece',
    'case-study': 'Analyze a real-world example with data and outcomes',
    'how-to': 'Provide step-by-step instructions'
  };
  
  const toneInstructions = {
    'expert': 'Use professional, authoritative language',
    'friendly': 'Use conversational, approachable tone',
    'humorous': 'Include light humor and entertaining elements'
  };
  
  return `
Create a ${config.format} article in ${config.language} language.

Tone: ${toneInstructions[config.tone]}
Format: ${formatInstructions[config.format]}

Keywords to include: ${config.keywords.join(', ')}

Research data to incorporate:
${config.research}

Requirements:
- Include relevant statistics and data points
- Make it engaging and actionable
- Optimize for SEO
- Include a strong introduction and conclusion
${config.language === 'vi' ? '- Use natural Vietnamese expressions' : ''}
  `.trim();
}
```

### 3. Multilingual Content Generation

```typescript
// src/lib/ai/multilingual.ts
import { generateContentClaude } from './content-generator';
import type { ContentConfig } from './content-generator';

export async function generateMultilingualContent(
  baseConfig: Omit<ContentConfig, 'language'>
): Promise<{ en: string; vi: string }> {
  const [englishContent, vietnameseContent] = await Promise.all([
    generateContentClaude({ ...baseConfig, language: 'en' }),
    generateContentClaude({ ...baseConfig, language: 'vi' })
  ]);
  
  return {
    en: englishContent,
    vi: vietnameseContent
  };
}
```

### 4. Video Generation with Remotion

```typescript
// src/lib/video/renderer.ts
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';
import { writeFile } from 'fs/promises';

interface VideoConfig {
  content: string;
  title: string;
  format: 'reels' | 'tiktok' | 'shorts';
  duration?: number;
}

const formatDimensions = {
  reels: { width: 1080, height: 1920 },
  tiktok: { width: 1080, height: 1920 },
  shorts: { width: 1080, height: 1920 }
};

export async function generateVideo(config: VideoConfig): Promise<string> {
  // Bundle the Remotion project
  const bundleLocation = await bundle({
    entryPoint: path.resolve('./remotion/index.ts'),
    webpackOverride: (config) => config,
  });
  
  // Get composition
  const compositionId = 'ContentVideo';
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: compositionId,
    inputProps: {
      title: config.title,
      content: config.content,
    },
  });
  
  // Set output path
  const outputPath = path.join(
    process.cwd(), 
    'public', 
    'videos', 
    `${Date.now()}-${config.format}.mp4`
  );
  
  // Render video
  await renderMedia({
    composition: {
      ...composition,
      ...formatDimensions[config.format],
      durationInFrames: config.duration || 300, // 10 seconds at 30fps
    },
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: outputPath,
    inputProps: {
      title: config.title,
      content: config.content,
    },
  });
  
  return outputPath;
}
```

### 5. Remotion Video Template

```typescript
// remotion/compositions/ContentVideo.tsx
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from 'remotion';
import React from 'react';

export interface ContentVideoProps {
  title: string;
  content: string;
}

export const ContentVideo: React.FC<ContentVideoProps> = ({ title, content }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  // Parse content into bullet points or sections
  const points = content.split('\n').filter(line => line.trim());
  
  const opacity = Math.min(1, frame / 30);
  const scale = Math.min(1, frame / 20);
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a1a' }}>
      {/* Title Sequence */}
      <Sequence from={0} durationInFrames={60}>
        <AbsoluteFill
          style={{
            justifyContent: 'center',
            alignItems: 'center',
            opacity,
            transform: `scale(${scale})`,
          }}
        >
          <h1
            style={{
              color: 'white',
              fontSize: 80,
              fontWeight: 'bold',
              textAlign: 'center',
              padding: '0 100px',
            }}
          >
            {title}
          </h1>
        </AbsoluteFill>
      </Sequence>
      
      {/* Content Points */}
      {points.slice(0, 5).map((point, index) => (
        <Sequence
          key={index}
          from={60 + index * 45}
          durationInFrames={45}
        >
          <ContentPoint text={point} index={index} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const ContentPoint: React.FC<{ text: string; index: number }> = ({ text, index }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(1, frame / 15);
  const translateY = Math.max(0, 50 - frame * 2);
  
  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: '100px',
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start' }}>
        <span
          style={{
            color: '#00d9ff',
            fontSize: 60,
            fontWeight: 'bold',
            marginRight: 20,
          }}
        >
          {index + 1}.
        </span>
        <p
          style={{
            color: 'white',
            fontSize: 48,
            lineHeight: 1.4,
            margin: 0,
          }}
        >
          {text}
        </p>
      </div>
    </AbsoluteFill>
  );
};
```

### 6. Complete Pipeline Orchestration

```typescript
// src/lib/pipeline/orchestrator.ts
import { scrapeNews, extractInsights } from '../research/scraper';
import { generateMultilingualContent } from '../ai/multilingual';
import { generateVideo } from '../video/renderer';

interface PipelineConfig {
  keyword: string;
  format: 'toplist' | 'pov' | 'case-study' | 'how-to';
  tone: 'expert' | 'friendly' | 'humorous';
  generateVideo: boolean;
  videoFormats?: ('reels' | 'tiktok' | 'shorts')[];
}

export async function runContentPipeline(config: PipelineConfig) {
  console.log(`Starting pipeline for keyword: ${config.keyword}`);
  
  // Step 1: Research
  console.log('Step 1: Scraping news sources...');
  const articles = await scrapeNews(config.keyword);
  const insights = await extractInsights(articles);
  
  const researchData = articles
    .map(a => `${a.title}: ${a.content.slice(0, 200)}`)
    .join('\n\n');
  
  // Step 2: Generate Content
  console.log('Step 2: Generating multilingual content...');
  const content = await generateMultilingualContent({
    format: config.format,
    tone: config.tone,
    keywords: [config.keyword, ...insights.slice(0, 5)],
    research: researchData,
  });
  
  // Step 3: Generate Videos (if enabled)
  let videos: Record<string, string[]> = { en: [], vi: [] };
  
  if (config.generateVideo && config.videoFormats) {
    console.log('Step 3: Generating videos...');
    
    for (const lang of ['en', 'vi'] as const) {
      for (const format of config.videoFormats) {
        const videoPath = await generateVideo({
          content: content[lang],
          title: config.keyword,
          format,
        });
        
        videos[lang].push(videoPath);
      }
    }
  }
  
  return {
    research: {
      articles: articles.length,
      insights,
    },
    content,
    videos,
    timestamp: new Date(),
  };
}
```

## API Routes (Next.js)

```typescript
// src/app/api/generate/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { runContentPipeline } from '@/lib/pipeline/orchestrator';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const result = await runContentPipeline({
      keyword: body.keyword,
      format: body.format || 'toplist',
      tone: body.tone || 'friendly',
      generateVideo: body.generateVideo || false,
      videoFormats: body.videoFormats || ['reels'],
    });
    
    return NextResponse.json(result);
  } catch (error) {
    console.error('Pipeline error:', error);
    return NextResponse.json(
      { error: 'Pipeline execution failed' },
      { status: 500 }
    );
  }
}
```

## Usage Example

```typescript
// Example: Using the pipeline from a component
import { useState } from 'react';

export default function ContentGenerator() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  
  const generateContent = async () => {
    setLoading(true);
    
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keyword: 'AI marketing automation',
          format: 'toplist',
          tone: 'expert',
          generateVideo: true,
          videoFormats: ['reels', 'tiktok'],
        }),
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <button onClick={generateContent} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Content'}
      </button>
      
      {result && (
        <div>
          <h2>English Content</h2>
          <pre>{result.content.en}</pre>
          
          <h2>Vietnamese Content</h2>
          <pre>{result.content.vi}</pre>
          
          <h2>Generated Videos</h2>
          <ul>
            {result.videos.en.map((video, i) => (
              <li key={i}><a href={video}>Video {i + 1}</a></li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

## Common Patterns

### Batch Content Generation

```typescript
// Generate multiple pieces of content from different keywords
async function batchGenerate(keywords: string[]) {
  const results = await Promise.allSettled(
    keywords.map(keyword =>
      runContentPipeline({
        keyword,
        format: 'toplist',
        tone: 'friendly',
        generateVideo: false,
      })
    )
  );
  
  return results
    .filter(r => r.status === 'fulfilled')
    .map(r => (r as PromiseFulfilledResult<any>).value);
}
```

### Custom Video Templates

```typescript
// Register custom Remotion compositions
// remotion/index.ts
import { registerRoot } from 'remotion';
import { ContentVideo } from './compositions/ContentVideo';
import { InfographicVideo } from './compositions/InfographicVideo';

registerRoot(() => (
  <>
    <Composition
      id="ContentVideo"
      component={ContentVideo}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="InfographicVideo"
      component={InfographicVideo}
      durationInFrames={450}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
));
```

## Troubleshooting

### API Rate Limits
```typescript
// Implement retry logic with exponential backoff
async function apiCallWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      if (error.status === 429 && i < maxRetries - 1) {
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, i) * 1000)
        );
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Memory Issues with Video Rendering
```typescript
// Render videos sequentially instead of parallel
async function renderVideosSequentially(configs: VideoConfig[]) {
  const results = [];
  for (const config of configs) {
    const path = await generateVideo(config);
    results.push(path);
    // Allow memory cleanup between renders
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  return results;
}
```

### Missing Environment Variables
```typescript
// Validate environment on startup
const requiredEnvVars = [
  'OPENAI_API_KEY',
  'ANTHROPIC_API_KEY',
  'RAPIDAPI_KEY',
];

requiredEnvVars.forEach(varName => {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
});
```

## Performance Optimization

```typescript
// Cache research results to avoid redundant API calls
import NodeCache from 'node-cache';

const researchCache = new NodeCache({ stdTTL: 3600 }); // 1 hour

export async function scrapeNewsWithCache(keyword: string) {
  const cached = researchCache.get<ResearchResult[]>(keyword);
  if (cached) return cached;
  
  const results = await scrapeNews(keyword);
  researchCache.set(keyword, results);
  return results;
}
```

This skill provides comprehensive coverage of the Marketing Pipeline AI Content Automation system, enabling AI agents to effectively assist developers in implementing automated content creation workflows.
