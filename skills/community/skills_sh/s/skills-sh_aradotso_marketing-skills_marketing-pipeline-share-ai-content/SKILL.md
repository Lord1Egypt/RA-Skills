---
name: marketing-pipeline-share-ai-content
description: Automated content creation pipeline with AI research, multi-format writing, and video generation using Claude/OpenAI and Remotion
triggers:
  - "set up automated content pipeline"
  - "generate content from research to video"
  - "create AI-powered marketing content automatically"
  - "build content automation workflow"
  - "scrape news and generate blog posts with AI"
  - "automate content creation with Claude and OpenAI"
  - "render videos from text content automatically"
  - "set up marketing content generation system"
---

# Marketing Pipeline Share - AI Content Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill enables AI coding agents to work with the Ultimate AI Content Pipeline - a comprehensive TypeScript-based system that automates the entire content creation workflow from research and scriptwriting to video generation and publishing.

## What It Does

The Marketing Pipeline Share project provides:

- **Auto-Research**: Crawls and analyzes real-time data from TechCrunch, a16z, Twitter/X, LinkedIn
- **AI Content Generation**: Creates multi-format content (blog posts, case studies, how-tos) using Claude 3 and OpenAI
- **Multi-Language Support**: Generates content in both English and Vietnamese
- **Video Generation**: Automatically renders videos and infographics using Remotion
- **Platform Optimization**: Exports content optimized for Reels, TikTok, Shorts

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

## Configuration

Create a `.env.local` file in the root directory with required API keys:

```env
# AI Provider Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_claude_key
RAPIDAPI_KEY=your_rapidapi_key

# Optional Configurations
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Project Structure

```
marketing-pineline-share/
├── src/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/
│   │   ├── ai/          # AI integration (OpenAI, Claude)
│   │   ├── scraper/     # Web scraping modules
│   │   ├── video/       # Remotion video generation
│   │   └── utils/       # Utility functions
│   └── types/           # TypeScript type definitions
├── public/              # Static assets
└── remotion/            # Video templates
```

## Core API Usage

### 1. Research & Data Scraping

```typescript
import { scrapeNews } from '@/lib/scraper/news-scraper';

// Scrape latest news from multiple sources
async function gatherResearch(keyword: string) {
  const sources = ['techcrunch', 'a16z', 'twitter', 'linkedin'];
  
  const results = await scrapeNews({
    keyword,
    sources,
    timeRange: '24h',
    maxResults: 50
  });
  
  return results;
}
```

### 2. AI Content Generation with Claude

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function generateContent(research: any[], format: string) {
  const prompt = `Based on the following research data, create a ${format} article:
  
Research: ${JSON.stringify(research)}

Requirements:
- Engaging headline
- Data-backed insights
- SEO optimized
- Include statistics and quotes`;

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

### 3. OpenAI Integration Alternative

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function generateWithGPT(topic: string, tone: string) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [
      {
        role: 'system',
        content: `You are a professional content writer. Write in a ${tone} tone.`
      },
      {
        role: 'user',
        content: `Create a comprehensive article about: ${topic}`
      }
    ],
    temperature: 0.7,
    max_tokens: 2000
  });
  
  return completion.choices[0].message.content;
}
```

### 4. Multi-Language Content Generation

```typescript
interface ContentRequest {
  keyword: string;
  format: 'toplist' | 'pov' | 'case-study' | 'how-to';
  languages: ('en' | 'vi')[];
  tone: 'expert' | 'friendly' | 'humorous';
}

async function generateMultiLanguageContent(request: ContentRequest) {
  const research = await gatherResearch(request.keyword);
  const contents: Record<string, string> = {};
  
  for (const lang of request.languages) {
    const prompt = buildPrompt(research, request.format, lang, request.tone);
    
    const content = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 4096,
      messages: [{ role: 'user', content: prompt }]
    });
    
    contents[lang] = content.content[0].text;
  }
  
  return contents;
}

function buildPrompt(research: any[], format: string, lang: string, tone: string): string {
  const langInstructions = lang === 'vi' 
    ? 'Write in Vietnamese language'
    : 'Write in English language';
    
  return `${langInstructions}. Tone: ${tone}. Format: ${format}.
  
Research data: ${JSON.stringify(research)}

Create engaging content with clear structure, data-backed insights, and actionable takeaways.`;
}
```

### 5. Video Generation with Remotion

```typescript
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';

interface VideoConfig {
  content: string;
  title: string;
  platform: 'reels' | 'tiktok' | 'shorts';
}

async function generateVideo(config: VideoConfig) {
  // Define aspect ratios per platform
  const dimensions = {
    reels: { width: 1080, height: 1920 },
    tiktok: { width: 1080, height: 1920 },
    shorts: { width: 1080, height: 1920 }
  };
  
  const bundled = await bundle({
    entryPoint: path.join(process.cwd(), 'remotion/index.ts'),
    webpackOverride: (config) => config,
  });
  
  const composition = await selectComposition({
    serveUrl: bundled,
    id: 'ContentVideo',
    inputProps: {
      title: config.title,
      content: config.content,
      ...dimensions[config.platform]
    },
  });
  
  await renderMedia({
    composition,
    serveUrl: bundled,
    codec: 'h264',
    outputLocation: `out/${config.platform}-${Date.now()}.mp4`,
  });
}
```

### 6. Complete Pipeline Workflow

```typescript
interface PipelineConfig {
  keyword: string;
  format: string;
  languages: string[];
  tone: string;
  generateVideo: boolean;
  platforms?: string[];
}

async function runContentPipeline(config: PipelineConfig) {
  try {
    // Step 1: Research
    console.log('🔍 Starting research phase...');
    const research = await gatherResearch(config.keyword);
    
    // Step 2: Generate Content
    console.log('✍️ Generating content...');
    const contents = await generateMultiLanguageContent({
      keyword: config.keyword,
      format: config.format as any,
      languages: config.languages as any,
      tone: config.tone as any
    });
    
    // Step 3: Generate Videos (if requested)
    if (config.generateVideo && config.platforms) {
      console.log('🎬 Rendering videos...');
      for (const lang of config.languages) {
        for (const platform of config.platforms) {
          await generateVideo({
            content: contents[lang],
            title: config.keyword,
            platform: platform as any
          });
        }
      }
    }
    
    // Step 4: Return results
    return {
      success: true,
      research,
      contents,
      message: 'Content pipeline completed successfully'
    };
    
  } catch (error) {
    console.error('Pipeline error:', error);
    throw error;
  }
}

// Usage example
runContentPipeline({
  keyword: 'AI Marketing Trends 2024',
  format: 'toplist',
  languages: ['en', 'vi'],
  tone: 'expert',
  generateVideo: true,
  platforms: ['reels', 'tiktok', 'shorts']
});
```

## Next.js API Routes

### Content Generation Endpoint

```typescript
// src/app/api/generate/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { keyword, format, languages, tone } = body;
    
    // Validate input
    if (!keyword || !format) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }
    
    // Run pipeline
    const result = await runContentPipeline({
      keyword,
      format,
      languages: languages || ['en'],
      tone: tone || 'professional',
      generateVideo: false
    });
    
    return NextResponse.json(result);
    
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Video Rendering Endpoint

```typescript
// src/app/api/render-video/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { content, title, platform } = await request.json();
    
    await generateVideo({ content, title, platform });
    
    return NextResponse.json({
      success: true,
      message: 'Video rendered successfully',
      path: `out/${platform}-${Date.now()}.mp4`
    });
    
  } catch (error) {
    return NextResponse.json(
      { error: 'Video rendering failed' },
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

## Common Patterns

### Pattern 1: Batch Content Generation

```typescript
async function batchGenerateContent(keywords: string[]) {
  const results = [];
  
  for (const keyword of keywords) {
    const content = await runContentPipeline({
      keyword,
      format: 'how-to',
      languages: ['en', 'vi'],
      tone: 'friendly',
      generateVideo: false
    });
    
    results.push(content);
    
    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  return results;
}
```

### Pattern 2: Content Scheduling

```typescript
interface ScheduledContent {
  content: string;
  publishDate: Date;
  platforms: string[];
}

async function scheduleContent(config: ScheduledContent) {
  // Store in database with publish date
  const scheduled = {
    ...config,
    status: 'scheduled',
    createdAt: new Date()
  };
  
  // Queue for automatic publishing
  // Implementation depends on your queue system
  return scheduled;
}
```

### Pattern 3: Custom Format Templates

```typescript
const formatTemplates = {
  toplist: {
    structure: ['intro', 'items', 'conclusion'],
    minItems: 5,
    includeStats: true
  },
  'case-study': {
    structure: ['problem', 'solution', 'results', 'takeaways'],
    includeQuotes: true,
    minLength: 1500
  },
  'how-to': {
    structure: ['intro', 'steps', 'tips', 'conclusion'],
    includeVisuals: true,
    stepByStep: true
  }
};

function getFormatPrompt(format: string): string {
  const template = formatTemplates[format];
  return `Create content following this structure: ${template.structure.join(' → ')}`;
}
```

## Troubleshooting

### API Rate Limits

```typescript
// Implement exponential backoff
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      if (error.status === 429 && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000;
        console.log(`Rate limited, retrying in ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Video Rendering Memory Issues

```typescript
// Process videos in chunks
async function renderVideosInChunks(configs: VideoConfig[], chunkSize = 3) {
  for (let i = 0; i < configs.length; i += chunkSize) {
    const chunk = configs.slice(i, i + chunkSize);
    await Promise.all(chunk.map(config => generateVideo(config)));
    
    // Clear memory between chunks
    if (global.gc) global.gc();
  }
}
```

### Content Quality Validation

```typescript
function validateContent(content: string): boolean {
  const minLength = 500;
  const hasHeadline = content.includes('#') || content.length > 0;
  const hasStructure = content.split('\n\n').length >= 3;
  
  return content.length >= minLength && hasHeadline && hasStructure;
}

async function generateWithValidation(config: ContentRequest) {
  let attempts = 0;
  const maxAttempts = 3;
  
  while (attempts < maxAttempts) {
    const content = await generateContent(config);
    
    if (validateContent(content)) {
      return content;
    }
    
    attempts++;
    console.log(`Content validation failed, retry ${attempts}/${maxAttempts}`);
  }
  
  throw new Error('Failed to generate valid content');
}
```

## Environment Variables Reference

```env
# Required
OPENAI_API_KEY=          # OpenAI API key for GPT models
ANTHROPIC_API_KEY=       # Anthropic API key for Claude
RAPIDAPI_KEY=            # RapidAPI key for web scraping

# Optional
NEXT_PUBLIC_APP_URL=     # Base URL for the application
NODE_ENV=                # development | production
VIDEO_OUTPUT_DIR=        # Custom video output directory
MAX_CONCURRENT_RENDERS=  # Limit concurrent video renders (default: 3)
```

## Best Practices

1. **Always validate input**: Check keywords and parameters before processing
2. **Implement rate limiting**: Respect API limits for Claude/OpenAI
3. **Cache research data**: Avoid redundant scraping within 24h
4. **Monitor costs**: Track API usage for budget control
5. **Test video renders**: Verify output before batch generation
6. **Use environment variables**: Never hardcode API keys
7. **Handle errors gracefully**: Implement retry logic and fallbacks
8. **Optimize prompts**: Iterate on prompts for better content quality
