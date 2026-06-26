---
name: marketing-pipeline-automation
description: AI-powered content automation pipeline from research to video generation with Claude/OpenAI integration
triggers:
  - automate content creation pipeline
  - generate content from research to video
  - build automated marketing workflow
  - create AI content with video generation
  - set up content automation system
  - use remotion for video content
  - implement AI research to video pipeline
  - automate social media content creation
---

# Marketing Pipeline Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Complete AI-powered content automation system that handles the entire content lifecycle: from researching trending topics, generating multi-format content (articles, scripts), to rendering videos automatically. Built with TypeScript, Next.js, Claude/OpenAI APIs, and Remotion for video generation.

## What It Does

This system provides a fully automated content production pipeline:

- **Auto-Research**: Crawls and analyzes news from TechCrunch, a16z, Twitter, LinkedIn within 24h
- **Multi-Format Content Generation**: Creates content in various formats (Toplist, POV, Case Study, How-to) using Claude 3 or OpenAI
- **Multilingual Support**: Generates content in English and Vietnamese simultaneously
- **Video Rendering**: Automatically converts text content to infographics and short-form videos using Remotion
- **Platform Optimization**: Exports videos optimized for Reels, TikTok, Shorts

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
cp .env.example .env.local
```

## Configuration

Create `.env.local` with the following environment variables:

```bash
# AI Provider APIs
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key

# Research APIs
RAPIDAPI_KEY=your_rapidapi_key

# Database (if applicable)
DATABASE_URL=your_database_connection_string

# Next.js
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## Project Structure

```
marketing-pipeline-share/
├── src/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/             # Core utilities
│   │   ├── ai/          # AI integration (Claude, OpenAI)
│   │   ├── research/    # Content research & crawling
│   │   └── video/       # Remotion video generation
│   └── types/           # TypeScript definitions
├── remotion/            # Video templates
└── public/              # Static assets
```

## Core Usage Patterns

### 1. Research Content Sources

```typescript
import { researchContent } from '@/lib/research/crawler';

interface ResearchOptions {
  keyword: string;
  sources: string[];
  timeframe: '24h' | '7d' | '30d';
  language?: 'en' | 'vi';
}

async function gatherResearch(options: ResearchOptions) {
  const research = await researchContent({
    keyword: options.keyword,
    sources: options.sources || ['techcrunch', 'a16z', 'twitter', 'linkedin'],
    timeframe: options.timeframe,
    maxResults: 20
  });

  return {
    articles: research.articles,
    insights: research.insights,
    statistics: research.statistics,
    trends: research.trends
  };
}

// Usage
const data = await gatherResearch({
  keyword: 'AI automation',
  sources: ['techcrunch', 'twitter'],
  timeframe: '24h'
});
```

### 2. Generate Content with Claude

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

interface ContentGenerationOptions {
  format: 'toplist' | 'pov' | 'case-study' | 'how-to';
  tone: 'expert' | 'friendly' | 'humorous';
  language: 'en' | 'vi';
  researchData: any;
}

async function generateContent(options: ContentGenerationOptions) {
  const prompt = `Based on this research data: ${JSON.stringify(options.researchData)}
  
Create a ${options.format} article in ${options.language} with a ${options.tone} tone.
Include statistics, insights, and actionable takeaways.`;

  const message = await anthropic.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 4096,
    messages: [{
      role: 'user',
      content: prompt
    }]
  });

  return message.content[0].text;
}
```

### 3. Generate Content with OpenAI

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function generateWithOpenAI(
  researchData: any,
  format: string,
  language: string
) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [
      {
        role: 'system',
        content: `You are an expert content creator specializing in ${format} format.`
      },
      {
        role: 'user',
        content: `Create ${format} content in ${language} based on: ${JSON.stringify(researchData)}`
      }
    ],
    temperature: 0.7,
    max_tokens: 3000
  });

  return completion.choices[0].message.content;
}
```

### 4. Video Generation with Remotion

```typescript
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';

interface VideoConfig {
  content: string;
  format: 'reels' | 'tiktok' | 'shorts';
  style: 'minimal' | 'dynamic' | 'professional';
}

async function generateVideo(config: VideoConfig) {
  // Define dimensions based on format
  const dimensions = {
    reels: { width: 1080, height: 1920 },
    tiktok: { width: 1080, height: 1920 },
    shorts: { width: 1080, height: 1920 }
  };

  const bundleLocation = await bundle({
    entryPoint: path.resolve('./remotion/index.ts'),
    webpackOverride: (config) => config
  });

  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: 'ContentVideo',
    inputProps: {
      content: config.content,
      style: config.style
    }
  });

  const outputPath = path.join(process.cwd(), 'public', 'videos', `output-${Date.now()}.mp4`);

  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: outputPath,
    inputProps: {
      content: config.content,
      style: config.style
    }
  });

  return outputPath;
}
```

### 5. Complete Pipeline Integration

```typescript
interface PipelineInput {
  keyword: string;
  format: 'toplist' | 'pov' | 'case-study' | 'how-to';
  languages: ('en' | 'vi')[];
  generateVideo: boolean;
}

async function runContentPipeline(input: PipelineInput) {
  // Step 1: Research
  console.log('🔍 Researching content...');
  const research = await gatherResearch({
    keyword: input.keyword,
    sources: ['techcrunch', 'twitter', 'linkedin'],
    timeframe: '24h'
  });

  // Step 2: Generate content for each language
  console.log('✍️ Generating content...');
  const contents = await Promise.all(
    input.languages.map(lang =>
      generateContent({
        format: input.format,
        tone: 'expert',
        language: lang,
        researchData: research
      })
    )
  );

  // Step 3: Generate video if requested
  let videoPath: string | null = null;
  if (input.generateVideo) {
    console.log('🎬 Rendering video...');
    videoPath = await generateVideo({
      content: contents[0],
      format: 'reels',
      style: 'dynamic'
    });
  }

  return {
    research,
    contents: contents.map((content, i) => ({
      language: input.languages[i],
      content
    })),
    videoPath
  };
}

// Usage
const result = await runContentPipeline({
  keyword: 'AI content automation',
  format: 'toplist',
  languages: ['en', 'vi'],
  generateVideo: true
});
```

## API Routes

### Content Generation API

```typescript
// app/api/content/generate/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { keyword, format, languages } = await req.json();

    const result = await runContentPipeline({
      keyword,
      format,
      languages,
      generateVideo: false
    });

    return NextResponse.json({
      success: true,
      data: result
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}
```

### Video Generation API

```typescript
// app/api/video/render/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { content, format, style } = await req.json();

    const videoPath = await generateVideo({
      content,
      format: format || 'reels',
      style: style || 'dynamic'
    });

    return NextResponse.json({
      success: true,
      videoUrl: `/videos/${path.basename(videoPath)}`
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: error.message },
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

# Render videos (Remotion)
npm run remotion:studio
```

## Common Patterns

### Custom Content Templates

```typescript
interface ContentTemplate {
  name: string;
  structure: string[];
  tone: string;
  hooks: string[];
}

const templates: Record<string, ContentTemplate> = {
  toplist: {
    name: 'Top List',
    structure: ['hook', 'intro', 'items', 'conclusion', 'cta'],
    tone: 'authoritative',
    hooks: ['Surprising statistics', 'Bold claims', 'Questions']
  },
  pov: {
    name: 'Point of View',
    structure: ['perspective', 'argument', 'evidence', 'counterpoint', 'conclusion'],
    tone: 'personal',
    hooks: ['Personal story', 'Controversial take', 'Industry insight']
  }
};

function applyTemplate(content: string, template: ContentTemplate): string {
  // Apply template structure to generated content
  const sections = template.structure.map(section => {
    return `## ${section.toUpperCase()}\n\n${extractSection(content, section)}`;
  });
  
  return sections.join('\n\n');
}
```

### Scheduling Content

```typescript
interface ScheduledPost {
  content: string;
  publishAt: Date;
  platforms: ('facebook' | 'twitter' | 'linkedin')[];
  status: 'scheduled' | 'published' | 'failed';
}

async function scheduleContent(post: ScheduledPost) {
  // Save to database or queue system
  const scheduled = await db.posts.create({
    data: {
      content: post.content,
      publishAt: post.publishAt,
      platforms: post.platforms,
      status: 'scheduled'
    }
  });

  return scheduled;
}
```

### Multi-Platform Video Export

```typescript
async function exportForAllPlatforms(content: string) {
  const formats = ['reels', 'tiktok', 'shorts'] as const;
  
  const videos = await Promise.all(
    formats.map(format =>
      generateVideo({
        content,
        format,
        style: 'dynamic'
      })
    )
  );

  return videos.map((path, i) => ({
    platform: formats[i],
    videoPath: path
  }));
}
```

## Troubleshooting

### API Rate Limits

```typescript
class RateLimiter {
  private requests: number[] = [];
  private maxRequests: number;
  private timeWindow: number;

  constructor(maxRequests: number, timeWindowMs: number) {
    this.maxRequests = maxRequests;
    this.timeWindow = timeWindowMs;
  }

  async checkLimit(): Promise<void> {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.timeWindow);

    if (this.requests.length >= this.maxRequests) {
      const waitTime = this.timeWindow - (now - this.requests[0]);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }

    this.requests.push(now);
  }
}

const claudeLimiter = new RateLimiter(50, 60000); // 50 requests per minute

async function callClaudeWithLimit(prompt: string) {
  await claudeLimiter.checkLimit();
  return await anthropic.messages.create({...});
}
```

### Video Rendering Errors

```typescript
async function safeVideoRender(config: VideoConfig) {
  try {
    return await generateVideo(config);
  } catch (error) {
    console.error('Video rendering failed:', error);
    
    // Fallback to static image generation
    if (error.message.includes('timeout')) {
      console.log('Falling back to static image...');
      return await generateStaticImage(config.content);
    }
    
    throw error;
  }
}
```

### Content Quality Validation

```typescript
function validateContent(content: string): { valid: boolean; issues: string[] } {
  const issues: string[] = [];
  
  if (content.length < 500) {
    issues.push('Content too short (minimum 500 characters)');
  }
  
  if (!content.includes('\n')) {
    issues.push('Content lacks proper formatting');
  }
  
  const urlCount = (content.match(/https?:\/\//g) || []).length;
  if (urlCount === 0) {
    issues.push('No source links included');
  }
  
  return {
    valid: issues.length === 0,
    issues
  };
}
```

## Best Practices

1. **Batch Processing**: Process multiple content pieces in parallel for efficiency
2. **Caching**: Cache research results to avoid redundant API calls
3. **Error Recovery**: Implement retry logic for failed API calls
4. **Content Versioning**: Keep track of generated content versions
5. **Quality Checks**: Always validate generated content before publishing
6. **Resource Management**: Monitor and limit concurrent video rendering jobs
