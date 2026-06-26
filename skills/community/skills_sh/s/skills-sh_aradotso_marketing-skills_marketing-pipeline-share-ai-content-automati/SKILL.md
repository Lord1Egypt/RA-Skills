---
name: marketing-pipeline-share-ai-content-automation
description: Automated AI content pipeline from research to video generation using Claude/OpenAI and Remotion
triggers:
  - automate content creation with AI research and video generation
  - set up AI content pipeline with Claude and Remotion
  - automatically research and generate social media content
  - create automated content workflow from research to video
  - build AI-powered content automation system
  - generate videos and posts from AI research automatically
  - implement automated marketing content pipeline
  - scrape news and auto-generate content with AI
---

# Marketing Pipeline Share - AI Content Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill enables AI coding agents to use **marketing-pipeline-share**, an automated content pipeline that performs research, generates scripts, and creates videos using AI (Claude 3, OpenAI) and Remotion. The system crawls news sources, analyzes trends, generates multi-format content (blog posts, social media), and renders videos automatically.

## What It Does

- **Auto-Research**: Crawls TechCrunch, a16z, Twitter/X, LinkedIn for recent content (24h window)
- **AI Content Generation**: Uses Claude/OpenAI to create content in multiple formats (Toplist, POV, Case Study, How-to)
- **Multi-language**: Generates Vietnamese and English versions simultaneously
- **Video Rendering**: Converts content to videos using Remotion for Reels/TikTok/Shorts
- **Full Automation**: Keyword → Research → Content → Video in one pipeline

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

## Environment Configuration

Create `.env` file with required API keys:

```bash
# AI Provider Keys
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key

# Research APIs
RAPIDAPI_KEY=your_rapidapi_key

# Database (if applicable)
DATABASE_URL=your_database_connection_string

# Remotion (Video Rendering)
REMOTION_LICENSE_KEY=your_remotion_license

# Optional: Social Media APIs
FACEBOOK_PAGE_TOKEN=your_facebook_token
TWITTER_API_KEY=your_twitter_api_key
```

## Project Structure

```
marketing-pineline-share/
├── src/
│   ├── research/          # Auto-crawling and data extraction
│   ├── content/           # AI content generation logic
│   ├── video/             # Remotion video rendering
│   ├── api/               # API routes (Next.js)
│   └── utils/             # Helper functions
├── pages/                 # Next.js pages
├── public/                # Static assets
└── remotion/              # Remotion video compositions
```

## Core Features and Usage

### 1. Auto-Research Module

Crawl and analyze news sources for fresh content:

```typescript
import { autoResearch } from './src/research/crawler';

interface ResearchConfig {
  keyword: string;
  sources: string[];
  timeframe: string; // '24h', '7d', etc.
  language?: 'en' | 'vi';
}

async function performResearch(config: ResearchConfig) {
  const results = await autoResearch({
    keyword: config.keyword,
    sources: config.sources || ['techcrunch', 'a16z', 'twitter'],
    timeframe: config.timeframe,
    maxResults: 50
  });

  // Returns structured data with insights
  return {
    articles: results.articles,
    insights: results.insights,
    trends: results.trends,
    statistics: results.statistics
  };
}

// Example usage
const research = await performResearch({
  keyword: 'AI marketing automation',
  sources: ['techcrunch', 'linkedin'],
  timeframe: '24h',
  language: 'en'
});
```

### 2. AI Content Generation

Generate content in multiple formats using Claude or OpenAI:

```typescript
import { generateContent } from './src/content/generator';
import Anthropic from '@anthropic-ai/sdk';

interface ContentConfig {
  format: 'toplist' | 'pov' | 'case-study' | 'how-to';
  tone: 'professional' | 'friendly' | 'humorous';
  language: 'en' | 'vi' | 'both';
  researchData: any;
}

async function createContent(config: ContentConfig) {
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const prompt = buildPrompt(config);

  const message = await anthropic.messages.create({
    model: 'claude-3-opus-20240229',
    max_tokens: 4096,
    messages: [{
      role: 'user',
      content: prompt
    }]
  });

  return {
    content: message.content,
    format: config.format,
    metadata: {
      wordCount: message.content[0].text.split(' ').length,
      generatedAt: new Date()
    }
  };
}

// Generate bilingual content
const content = await createContent({
  format: 'toplist',
  tone: 'professional',
  language: 'both',
  researchData: research
});
```

### 3. Video Rendering with Remotion

Convert content to video format:

```typescript
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';

interface VideoConfig {
  content: string;
  template: 'reels' | 'tiktok' | 'youtube-shorts';
  aspectRatio: '9:16' | '16:9' | '1:1';
}

async function generateVideo(config: VideoConfig) {
  const compositionId = getCompositionId(config.template);
  const bundleLocation = await bundle(
    path.join(process.cwd(), 'remotion/index.ts')
  );

  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: compositionId
  });

  const outputPath = path.join(
    process.cwd(),
    'public',
    'videos',
    `${Date.now()}.mp4`
  );

  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: outputPath,
    inputProps: {
      content: config.content,
      aspectRatio: config.aspectRatio
    }
  });

  return {
    videoPath: outputPath,
    duration: composition.durationInFrames / composition.fps
  };
}

// Render video for TikTok
const video = await generateVideo({
  content: content.content,
  template: 'tiktok',
  aspectRatio: '9:16'
});
```

### 4. Complete Pipeline Execution

End-to-end automation:

```typescript
import { runContentPipeline } from './src/pipeline';

interface PipelineConfig {
  keyword: string;
  contentFormats: string[];
  outputFormats: ('text' | 'video' | 'image')[];
  autoPublish?: boolean;
}

async function executeFullPipeline(config: PipelineConfig) {
  console.log(`Starting pipeline for: ${config.keyword}`);

  // Step 1: Research
  const research = await performResearch({
    keyword: config.keyword,
    sources: ['techcrunch', 'a16z', 'twitter'],
    timeframe: '24h'
  });

  // Step 2: Generate content for each format
  const contentPieces = await Promise.all(
    config.contentFormats.map(format =>
      createContent({
        format: format as any,
        tone: 'professional',
        language: 'both',
        researchData: research
      })
    )
  );

  // Step 3: Render videos if requested
  const videos = config.outputFormats.includes('video')
    ? await Promise.all(
        contentPieces.map(content =>
          generateVideo({
            content: content.content,
            template: 'reels',
            aspectRatio: '9:16'
          })
        )
      )
    : [];

  // Step 4: Auto-publish (optional)
  if (config.autoPublish) {
    await publishToSocialMedia(contentPieces, videos);
  }

  return {
    research,
    content: contentPieces,
    videos,
    summary: {
      articlesAnalyzed: research.articles.length,
      contentGenerated: contentPieces.length,
      videosCreated: videos.length
    }
  };
}

// Execute complete pipeline
const result = await executeFullPipeline({
  keyword: 'AI marketing trends 2024',
  contentFormats: ['toplist', 'how-to', 'pov'],
  outputFormats: ['text', 'video'],
  autoPublish: false
});
```

## API Routes (Next.js)

### Start Research Job

```typescript
// pages/api/research/start.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { keyword, sources, timeframe } = req.body;

  try {
    const jobId = await startResearchJob({
      keyword,
      sources,
      timeframe
    });

    res.status(200).json({ jobId, status: 'started' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

### Generate Content

```typescript
// pages/api/content/generate.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { researchId, format, language } = req.body;

  try {
    const content = await createContent({
      format,
      tone: 'professional',
      language,
      researchData: await getResearchData(researchId)
    });

    res.status(200).json({ content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

### Render Video

```typescript
// pages/api/video/render.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { contentId, template, aspectRatio } = req.body;

  try {
    const content = await getContent(contentId);
    const video = await generateVideo({
      content: content.text,
      template,
      aspectRatio
    });

    res.status(200).json({ videoUrl: video.videoPath });
  } catch (error) {
    res.status(500).json({ error: error.message });
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
npm start

# Render Remotion videos
npm run render
```

## Common Patterns

### Pattern 1: Scheduled Content Generation

```typescript
import cron from 'node-cron';

// Run daily at 9 AM
cron.schedule('0 9 * * *', async () => {
  const keywords = ['AI trends', 'marketing automation', 'social media'];

  for (const keyword of keywords) {
    await executeFullPipeline({
      keyword,
      contentFormats: ['toplist', 'how-to'],
      outputFormats: ['text', 'video'],
      autoPublish: true
    });
  }
});
```

### Pattern 2: Custom Content Templates

```typescript
interface CustomTemplate {
  name: string;
  structure: string[];
  minSections: number;
  includeStats: boolean;
}

function buildCustomPrompt(template: CustomTemplate, research: any): string {
  return `
You are a content creator. Create a ${template.name} with the following structure:
${template.structure.map((s, i) => `${i + 1}. ${s}`).join('\n')}

${template.includeStats ? 'Include relevant statistics and data.' : ''}

Based on this research data:
${JSON.stringify(research.insights)}

Write engaging, SEO-optimized content.
  `.trim();
}
```

### Pattern 3: Multi-Platform Video Export

```typescript
const platforms = [
  { name: 'tiktok', ratio: '9:16', maxDuration: 60 },
  { name: 'reels', ratio: '9:16', maxDuration: 90 },
  { name: 'youtube-shorts', ratio: '9:16', maxDuration: 60 },
  { name: 'linkedin', ratio: '1:1', maxDuration: 120 }
];

async function exportToAllPlatforms(content: string) {
  return await Promise.all(
    platforms.map(platform =>
      generateVideo({
        content,
        template: platform.name as any,
        aspectRatio: platform.ratio as any
      })
    )
  );
}
```

## Troubleshooting

### API Rate Limits

```typescript
import pRetry from 'p-retry';

async function callAPIWithRetry(apiFunction: () => Promise<any>) {
  return pRetry(apiFunction, {
    retries: 3,
    onFailedAttempt: error => {
      console.log(
        `Attempt ${error.attemptNumber} failed. Retries left: ${error.retriesLeft}`
      );
    }
  });
}
```

### Video Rendering Memory Issues

```typescript
// Adjust Remotion memory settings
const video = await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: 'h264',
  outputLocation: outputPath,
  chromiumOptions: {
    headless: true,
    gl: 'angle'
  },
  envVariables: {
    NODE_OPTIONS: '--max-old-space-size=4096'
  }
});
```

### Claude API Timeout

```typescript
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  timeout: 60000, // 60 seconds
  maxRetries: 2
});
```

### Content Quality Validation

```typescript
function validateContent(content: string): boolean {
  const minLength = 500;
  const hasStructure = content.includes('\n\n');
  const hasKeywords = true; // Implement keyword check

  return (
    content.length >= minLength &&
    hasStructure &&
    hasKeywords
  );
}
```

## Best Practices

1. **Always validate research data** before content generation
2. **Cache research results** to avoid redundant API calls
3. **Use queues** for video rendering to manage server resources
4. **Implement rate limiting** for all external API calls
5. **Store generated content** in database for reuse and tracking
6. **Test video templates** before bulk rendering
7. **Monitor AI costs** with usage tracking middleware

This skill provides comprehensive automation for content marketing workflows, from research through video production.
