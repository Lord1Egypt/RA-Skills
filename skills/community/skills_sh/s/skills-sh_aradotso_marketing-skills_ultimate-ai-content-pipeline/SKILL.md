---
name: ultimate-ai-content-pipeline
description: Automated content pipeline from research to video generation using Claude/OpenAI and Remotion
triggers:
  - how do I automate content creation from research to video
  - use ultimate ai content pipeline for marketing automation
  - generate content with claude and remotion integration
  - set up automated content research and video rendering
  - create marketing content pipeline with ai
  - build content automation system with openai
  - automate content workflow from scraping to video
  - integrate remotion video generation with ai content
---

# Ultimate AI Content Pipeline

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Ultimate AI Content Pipeline is a comprehensive TypeScript-based content automation system that handles the entire content creation workflow: from automated news research and data crawling, to AI-powered content generation (using Claude 3 and OpenAI), to automatic video rendering with Remotion. The system supports multiple content formats, bilingual output (English/Vietnamese), and multi-platform video optimization.

## Installation

### Prerequisites

```bash
node >= 18.x
npm or yarn
```

### Clone and Install

```bash
git clone https://github.com/pennydinh/marketing-pineline-share.git
cd marketing-pineline-share
npm install
# or
yarn install
```

### Environment Configuration

Create a `.env.local` file in the root directory:

```env
# AI Provider Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_claude_key

# Research/Scraping APIs
RAPIDAPI_KEY=your_rapidapi_key

# Content Sources
TECHCRUNCH_RSS_URL=https://techcrunch.com/feed/
A16Z_API_ENDPOINT=https://a16z.com/api/posts

# Remotion Configuration
REMOTION_AWS_ACCESS_KEY_ID=your_aws_key
REMOTION_AWS_SECRET_ACCESS_KEY=your_aws_secret

# Next.js Configuration
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### Start Development Server

```bash
npm run dev
# or
yarn dev
```

Access the application at `http://localhost:3000`

## Core Features and Usage

### 1. Auto-Research Content Scraping

The system automatically crawls and analyzes fresh content from multiple sources:

```typescript
// lib/research/scraper.ts
import { scraperConfig } from '@/config/sources';

interface ResearchResult {
  title: string;
  content: string;
  source: string;
  publishedAt: Date;
  insights: string[];
}

export async function autoResearch(
  keyword: string,
  timeframe: '24h' | '7d' = '24h'
): Promise<ResearchResult[]> {
  const sources = [
    'techcrunch',
    'a16z',
    'twitter',
    'linkedin'
  ];
  
  const results = await Promise.all(
    sources.map(source => 
      fetchFromSource(source, keyword, timeframe)
    )
  );
  
  return analyzeInsights(results.flat());
}

async function fetchFromSource(
  source: string,
  keyword: string,
  timeframe: string
): Promise<ResearchResult[]> {
  const config = scraperConfig[source];
  
  const response = await fetch(config.endpoint, {
    headers: {
      'X-RapidAPI-Key': process.env.RAPIDAPI_KEY!,
      'X-RapidAPI-Host': config.host
    }
  });
  
  return parseSourceData(await response.json(), source);
}
```

### 2. AI Content Generation

Generate content in multiple formats using Claude or OpenAI:

```typescript
// lib/ai/content-generator.ts
import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';

type ContentFormat = 'toplist' | 'pov' | 'case-study' | 'how-to';
type Language = 'en' | 'vi';
type Tone = 'expert' | 'friendly' | 'humorous';

interface ContentRequest {
  keyword: string;
  format: ContentFormat;
  language: Language;
  tone: Tone;
  researchData: ResearchResult[];
}

export async function generateContent(
  request: ContentRequest,
  provider: 'claude' | 'openai' = 'claude'
): Promise<string> {
  const prompt = buildPrompt(request);
  
  if (provider === 'claude') {
    return generateWithClaude(prompt);
  }
  return generateWithOpenAI(prompt);
}

async function generateWithClaude(prompt: string): Promise<string> {
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });
  
  const message = await anthropic.messages.create({
    model: 'claude-3-opus-20240229',
    max_tokens: 4096,
    messages: [{
      role: 'user',
      content: prompt
    }]
  });
  
  return message.content[0].type === 'text' 
    ? message.content[0].text 
    : '';
}

async function generateWithOpenAI(prompt: string): Promise<string> {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
  });
  
  const completion = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [{
      role: 'user',
      content: prompt
    }],
    max_tokens: 4096
  });
  
  return completion.choices[0].message.content || '';
}

function buildPrompt(request: ContentRequest): string {
  const { keyword, format, language, tone, researchData } = request;
  
  const insights = researchData
    .map(r => `- ${r.title}: ${r.insights.join(', ')}`)
    .join('\n');
  
  return `
You are a ${tone} content creator writing in ${language}.
Create a ${format} article about "${keyword}".

Recent research insights:
${insights}

Requirements:
- ${language === 'vi' ? 'Viết bằng tiếng Việt' : 'Write in English'}
- Tone: ${tone}
- Format: ${format}
- Include data and statistics from research
- Engaging and actionable
- 1500-2000 words
`;
}
```

### 3. Remotion Video Generation

Automatically render videos from content:

```typescript
// lib/video/renderer.ts
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';

interface VideoConfig {
  content: string;
  format: 'reels' | 'tiktok' | 'shorts';
  duration: number;
}

export async function renderVideo(
  config: VideoConfig
): Promise<string> {
  const bundleLocation = await bundle(
    path.join(process.cwd(), 'remotion/index.ts')
  );
  
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: 'ContentVideo',
    inputProps: {
      content: config.content,
      format: config.format
    }
  });
  
  const outputPath = path.join(
    process.cwd(),
    'public/videos',
    `video-${Date.now()}.mp4`
  );
  
  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: outputPath,
    inputProps: {
      content: config.content,
      format: config.format
    }
  });
  
  return outputPath;
}

// Get video dimensions for platform
export function getPlatformDimensions(
  format: VideoConfig['format']
): { width: number; height: number } {
  const dimensions = {
    reels: { width: 1080, height: 1920 },
    tiktok: { width: 1080, height: 1920 },
    shorts: { width: 1080, height: 1920 }
  };
  
  return dimensions[format];
}
```

### 4. Complete Pipeline Orchestration

```typescript
// lib/pipeline/orchestrator.ts
import { autoResearch } from '@/lib/research/scraper';
import { generateContent } from '@/lib/ai/content-generator';
import { renderVideo } from '@/lib/video/renderer';

interface PipelineConfig {
  keyword: string;
  format: ContentFormat;
  language: Language;
  tone: Tone;
  generateVideo: boolean;
  videoFormat?: 'reels' | 'tiktok' | 'shorts';
}

export async function runContentPipeline(
  config: PipelineConfig
) {
  // Step 1: Research
  console.log('🔍 Starting research...');
  const researchData = await autoResearch(config.keyword, '24h');
  
  // Step 2: Generate Content
  console.log('✍️ Generating content...');
  const content = await generateContent({
    keyword: config.keyword,
    format: config.format,
    language: config.language,
    tone: config.tone,
    researchData
  });
  
  // Step 3: Generate Video (optional)
  let videoPath: string | null = null;
  if (config.generateVideo && config.videoFormat) {
    console.log('🎬 Rendering video...');
    videoPath = await renderVideo({
      content,
      format: config.videoFormat,
      duration: 60
    });
  }
  
  return {
    content,
    videoPath,
    researchSources: researchData.length,
    metadata: {
      keyword: config.keyword,
      format: config.format,
      createdAt: new Date()
    }
  };
}
```

## API Routes (Next.js)

### POST /api/pipeline/run

```typescript
// app/api/pipeline/run/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { runContentPipeline } from '@/lib/pipeline/orchestrator';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const result = await runContentPipeline({
      keyword: body.keyword,
      format: body.format || 'toplist',
      language: body.language || 'en',
      tone: body.tone || 'expert',
      generateVideo: body.generateVideo || false,
      videoFormat: body.videoFormat
    });
    
    return NextResponse.json({
      success: true,
      data: result
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
```

### GET /api/research/:keyword

```typescript
// app/api/research/[keyword]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { autoResearch } from '@/lib/research/scraper';

export async function GET(
  request: NextRequest,
  { params }: { params: { keyword: string } }
) {
  const timeframe = request.nextUrl.searchParams.get('timeframe') as '24h' | '7d' || '24h';
  
  const results = await autoResearch(params.keyword, timeframe);
  
  return NextResponse.json({
    keyword: params.keyword,
    timeframe,
    results,
    count: results.length
  });
}
```

## Common Patterns

### Batch Content Generation

```typescript
// lib/utils/batch-generator.ts
import { runContentPipeline } from '@/lib/pipeline/orchestrator';

export async function batchGenerate(
  keywords: string[],
  baseConfig: Partial<PipelineConfig>
) {
  const results = [];
  
  for (const keyword of keywords) {
    try {
      const result = await runContentPipeline({
        keyword,
        format: baseConfig.format || 'toplist',
        language: baseConfig.language || 'en',
        tone: baseConfig.tone || 'expert',
        generateVideo: false
      });
      
      results.push({ keyword, success: true, result });
    } catch (error) {
      results.push({ 
        keyword, 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
    
    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  return results;
}
```

### Schedule Automated Posts

```typescript
// lib/scheduler/content-scheduler.ts
import { schedule } from 'node-cron';
import { runContentPipeline } from '@/lib/pipeline/orchestrator';

export function scheduleContentGeneration(
  config: PipelineConfig,
  cronExpression: string = '0 9 * * *' // Daily at 9 AM
) {
  return schedule(cronExpression, async () => {
    console.log('⏰ Running scheduled content generation...');
    
    try {
      const result = await runContentPipeline(config);
      console.log('✅ Content generated successfully');
      
      // Auto-post to platform (implement your logic)
      await postToSocialMedia(result);
    } catch (error) {
      console.error('❌ Scheduled generation failed:', error);
    }
  });
}
```

## Troubleshooting

### API Rate Limits

```typescript
// lib/utils/rate-limiter.ts
export class RateLimiter {
  private queue: Array<() => Promise<any>> = [];
  private processing = false;
  private delay: number;
  
  constructor(requestsPerMinute: number) {
    this.delay = 60000 / requestsPerMinute;
  }
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      });
      
      this.processQueue();
    });
  }
  
  private async processQueue() {
    if (this.processing || this.queue.length === 0) return;
    
    this.processing = true;
    const fn = this.queue.shift()!;
    
    await fn();
    await new Promise(resolve => setTimeout(resolve, this.delay));
    
    this.processing = false;
    this.processQueue();
  }
}

// Usage
const limiter = new RateLimiter(10); // 10 requests per minute

await limiter.execute(() => 
  generateContent({ /* config */ })
);
```

### Video Rendering Memory Issues

If Remotion crashes during rendering:

```typescript
// Reduce concurrency in remotion.config.ts
export default {
  concurrency: 1, // Lower from default
  timeout: 300000, // Increase timeout
  chromiumDisableWebSecurity: true,
  envVariables: {
    NODE_OPTIONS: '--max-old-space-size=4096'
  }
};
```

### Claude/OpenAI Token Limits

```typescript
// lib/ai/token-manager.ts
export function splitContentIntoChunks(
  content: string,
  maxTokens: number = 3000
): string[] {
  const words = content.split(' ');
  const chunks: string[] = [];
  let currentChunk: string[] = [];
  
  for (const word of words) {
    currentChunk.push(word);
    
    // Rough estimate: 1 token ≈ 0.75 words
    if (currentChunk.length * 0.75 >= maxTokens) {
      chunks.push(currentChunk.join(' '));
      currentChunk = [];
    }
  }
  
  if (currentChunk.length > 0) {
    chunks.push(currentChunk.join(' '));
  }
  
  return chunks;
}
```

### Error Handling Best Practices

```typescript
// lib/utils/error-handler.ts
export class PipelineError extends Error {
  constructor(
    message: string,
    public stage: 'research' | 'generation' | 'rendering',
    public originalError?: Error
  ) {
    super(message);
    this.name = 'PipelineError';
  }
}

export async function safeExecute<T>(
  fn: () => Promise<T>,
  stage: PipelineError['stage']
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    throw new PipelineError(
      `Failed at ${stage} stage`,
      stage,
      error instanceof Error ? error : undefined
    );
  }
}
```

## Configuration Reference

### Content Format Templates

```typescript
// config/templates.ts
export const contentTemplates = {
  toplist: {
    structure: ['intro', 'items', 'conclusion'],
    minItems: 5,
    maxItems: 10
  },
  pov: {
    structure: ['hook', 'perspective', 'evidence', 'conclusion'],
    tone: ['opinionated', 'analytical']
  },
  'case-study': {
    structure: ['problem', 'solution', 'results', 'learnings'],
    requiresData: true
  },
  'how-to': {
    structure: ['overview', 'steps', 'tips', 'conclusion'],
    minSteps: 3
  }
};
```

### Platform Video Specs

```typescript
// config/video-specs.ts
export const platformSpecs = {
  reels: {
    width: 1080,
    height: 1920,
    fps: 30,
    maxDuration: 90,
    codec: 'h264'
  },
  tiktok: {
    width: 1080,
    height: 1920,
    fps: 30,
    maxDuration: 60,
    codec: 'h264'
  },
  shorts: {
    width: 1080,
    height: 1920,
    fps: 30,
    maxDuration: 60,
    codec: 'h264'
  }
};
```
