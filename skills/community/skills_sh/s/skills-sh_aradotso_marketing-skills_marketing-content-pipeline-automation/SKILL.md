---
name: marketing-content-pipeline-automation
description: Automated AI content pipeline for research, scriptwriting, posting, and video generation using Claude/OpenAI and Remotion
triggers:
  - how do I automate content creation with AI research
  - generate video content from text automatically
  - set up an AI marketing content pipeline
  - create multilingual content with Claude and OpenAI
  - auto-post content to social media platforms
  - crawl news sources for content research
  - render videos from blog posts using Remotion
  - build an end-to-end content automation system
---

# Marketing Content Pipeline Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill enables AI coding agents to work with the Ultimate AI Content Pipeline - an end-to-end content automation system that handles research, content generation, video rendering, and auto-posting. The system crawls news sources, generates multilingual content using Claude/OpenAI, and renders videos using Remotion.

## What This Project Does

The Marketing Content Pipeline automates the entire content creation workflow:

1. **Auto-Research**: Crawls TechCrunch, a16z, Twitter/X, LinkedIn for trending topics
2. **AI Content Generation**: Creates articles in multiple formats (listicles, POV, case studies, how-tos) using Claude 3 or OpenAI
3. **Multilingual Output**: Generates content in English and Vietnamese simultaneously
4. **Video Rendering**: Converts written content into infographics and short-form videos using Remotion
5. **Auto-Publishing**: Posts content to social media platforms automatically

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

# Set up environment variables
cp .env.example .env
```

## Environment Configuration

Create a `.env` file with the following variables:

```env
# AI Provider Keys
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Research API Keys
RAPIDAPI_KEY=your_rapidapi_key_here
TWITTER_API_KEY=your_twitter_api_key_here

# Database (if applicable)
DATABASE_URL=your_database_connection_string

# Remotion (for video rendering)
REMOTION_AWS_ACCESS_KEY_ID=your_aws_key
REMOTION_AWS_SECRET_ACCESS_KEY=your_aws_secret

# Social Media Auto-Post
FACEBOOK_ACCESS_TOKEN=your_fb_token
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
```

## Key Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run research crawler
npm run crawl

# Generate content from keyword
npm run generate -- --keyword "AI trends 2024"

# Render video from content
npm run render-video -- --content-id 123

# Auto-post content
npm run publish -- --content-id 123 --platforms facebook,linkedin
```

## Project Structure

```
marketing-pineline-share/
├── src/
│   ├── crawlers/          # News source crawlers
│   ├── generators/        # AI content generation
│   ├── renderers/         # Video rendering with Remotion
│   ├── publishers/        # Social media posting
│   ├── utils/            # Helper functions
│   └── app/              # Next.js pages and API routes
├── config/               # Configuration files
└── public/              # Static assets
```

## Core API Usage

### 1. Research & Crawling

```typescript
import { crawlTechCrunch, crawlTwitterTrends } from './src/crawlers';

// Crawl TechCrunch for AI-related articles
const techCrunchData = await crawlTechCrunch({
  keyword: 'artificial intelligence',
  timeRange: '24h',
  limit: 10
});

// Get trending topics from Twitter
const twitterTrends = await crawlTwitterTrends({
  category: 'technology',
  region: 'us'
});

// Combine and analyze research data
const researchInsights = {
  sources: [...techCrunchData, ...twitterTrends],
  insights: analyzeData(techCrunchData, twitterTrends)
};
```

### 2. AI Content Generation

```typescript
import { generateContent } from './src/generators';
import { Anthropic } from '@anthropic-ai/sdk';
import OpenAI from 'openai';

// Using Claude for content generation
const claudeClient = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const content = await generateContent({
  client: claudeClient,
  provider: 'claude',
  model: 'claude-3-opus-20240229',
  format: 'listicle', // or 'pov', 'case-study', 'how-to'
  keyword: 'AI marketing automation',
  researchData: researchInsights,
  languages: ['en', 'vi'],
  tone: 'professional' // or 'friendly', 'humorous'
});

// Using OpenAI alternative
const openaiClient = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

const contentOpenAI = await generateContent({
  client: openaiClient,
  provider: 'openai',
  model: 'gpt-4-turbo-preview',
  format: 'how-to',
  keyword: 'content automation',
  researchData: researchInsights,
  languages: ['en'],
  tone: 'friendly'
});
```

### 3. Video Rendering with Remotion

```typescript
import { renderVideo } from './src/renderers';
import { bundle } from '@remotion/bundler';
import { renderMedia } from '@remotion/renderer';

// Render video from content
const videoOutput = await renderVideo({
  contentId: content.id,
  contentText: content.body.en,
  style: 'infographic', // or 'talking-head', 'text-animation'
  platform: 'instagram-reel', // or 'tiktok', 'youtube-shorts'
  aspectRatio: '9:16',
  duration: 30 // seconds
});

// Advanced Remotion rendering
const bundleLocation = await bundle({
  entryPoint: './src/renderers/VideoComposition.tsx',
  webpackOverride: (config) => config
});

const videoPath = await renderMedia({
  composition: {
    id: 'ContentVideo',
    width: 1080,
    height: 1920,
    fps: 30,
    durationInFrames: 900 // 30 seconds at 30fps
  },
  serveUrl: bundleLocation,
  codec: 'h264',
  outputLocation: `out/${content.id}.mp4`,
  inputProps: {
    title: content.title,
    highlights: content.keyPoints,
    backgroundStyle: 'gradient'
  }
});
```

### 4. Auto-Publishing to Social Platforms

```typescript
import { publishToFacebook, publishToLinkedIn } from './src/publishers';

// Publish to Facebook Page
const fbPost = await publishToFacebook({
  accessToken: process.env.FACEBOOK_ACCESS_TOKEN,
  pageId: 'your-page-id',
  content: {
    message: content.body.en,
    link: content.sourceUrl,
    mediaUrls: [videoPath]
  },
  scheduled: false // or schedule with timestamp
});

// Publish to LinkedIn
const linkedInPost = await publishToLinkedIn({
  accessToken: process.env.LINKEDIN_ACCESS_TOKEN,
  content: {
    text: content.body.en,
    mediaUrns: [uploadedMediaUrn],
    visibility: 'PUBLIC'
  }
});

// Batch publish to multiple platforms
import { batchPublish } from './src/publishers';

const publishResults = await batchPublish({
  contentId: content.id,
  platforms: ['facebook', 'linkedin', 'twitter'],
  scheduleTime: new Date('2024-12-25T10:00:00Z')
});
```

## Complete Workflow Example

```typescript
import { 
  crawlMultipleSources, 
  generateContent, 
  renderVideo, 
  batchPublish 
} from './src';

async function runContentPipeline(keyword: string) {
  try {
    // Step 1: Research
    console.log('🔍 Researching topic...');
    const research = await crawlMultipleSources({
      keyword,
      sources: ['techcrunch', 'twitter', 'linkedin'],
      timeRange: '24h'
    });

    // Step 2: Generate Content
    console.log('✍️ Generating content...');
    const content = await generateContent({
      client: new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY }),
      provider: 'claude',
      model: 'claude-3-opus-20240229',
      format: 'listicle',
      keyword,
      researchData: research,
      languages: ['en', 'vi'],
      tone: 'professional'
    });

    // Step 3: Render Video
    console.log('🎬 Rendering video...');
    const video = await renderVideo({
      contentId: content.id,
      contentText: content.body.en,
      style: 'infographic',
      platform: 'instagram-reel'
    });

    // Step 4: Publish
    console.log('📤 Publishing...');
    const results = await batchPublish({
      contentId: content.id,
      videoPath: video.path,
      platforms: ['facebook', 'linkedin'],
      scheduleTime: new Date(Date.now() + 3600000) // 1 hour from now
    });

    console.log('✅ Pipeline completed!', results);
    return { content, video, results };

  } catch (error) {
    console.error('❌ Pipeline failed:', error);
    throw error;
  }
}

// Execute pipeline
runContentPipeline('AI content automation 2024');
```

## API Routes (Next.js)

```typescript
// pages/api/generate-content.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { generateContent } from '@/src/generators';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { keyword, format, languages } = req.body;

  try {
    const content = await generateContent({
      client: new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY }),
      provider: 'claude',
      model: 'claude-3-opus-20240229',
      format,
      keyword,
      languages,
      tone: 'professional'
    });

    res.status(200).json({ success: true, content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

// pages/api/render-video.ts
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { contentId, style, platform } = req.body;

  try {
    const video = await renderVideo({
      contentId,
      style,
      platform
    });

    res.status(200).json({ success: true, videoUrl: video.url });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

## Configuration Patterns

### Custom Content Templates

```typescript
// config/content-templates.ts
export const contentTemplates = {
  listicle: {
    structure: [
      'Hook introduction',
      'Context and relevance',
      'List items (5-10)',
      'Conclusion with CTA'
    ],
    tone: 'engaging'
  },
  pov: {
    structure: [
      'Personal angle',
      'Supporting arguments',
      'Counterarguments',
      'Conclusion'
    ],
    tone: 'opinionated'
  },
  'case-study': {
    structure: [
      'Problem statement',
      'Solution approach',
      'Implementation details',
      'Results and metrics',
      'Key learnings'
    ],
    tone: 'analytical'
  }
};
```

### Video Style Presets

```typescript
// config/video-presets.ts
export const videoPresets = {
  'instagram-reel': {
    width: 1080,
    height: 1920,
    fps: 30,
    duration: 30,
    codec: 'h264'
  },
  'tiktok': {
    width: 1080,
    height: 1920,
    fps: 30,
    duration: 60,
    codec: 'h264'
  },
  'youtube-shorts': {
    width: 1080,
    height: 1920,
    fps: 60,
    duration: 60,
    codec: 'h264'
  }
};
```

## Common Troubleshooting

### API Rate Limits

```typescript
// Implement retry logic with exponential backoff
import { retry } from './src/utils/retry';

const content = await retry(
  () => generateContent(options),
  {
    maxAttempts: 3,
    delay: 1000,
    backoff: 'exponential'
  }
);
```

### Video Rendering Errors

```typescript
// Check Remotion setup
try {
  const video = await renderVideo(options);
} catch (error) {
  if (error.message.includes('ffmpeg')) {
    console.error('FFmpeg not installed. Run: brew install ffmpeg');
  } else if (error.message.includes('AWS')) {
    console.error('Check AWS credentials in .env file');
  }
  throw error;
}
```

### Content Quality Issues

```typescript
// Add validation and refinement
import { validateContent, refineContent } from './src/utils/validation';

let content = await generateContent(options);

if (!validateContent(content)) {
  console.log('Refining content...');
  content = await refineContent(content, {
    criteria: ['readability', 'seo', 'engagement']
  });
}
```

### Publishing Failures

```typescript
// Handle platform-specific errors
import { retryPublish } from './src/publishers/retry';

try {
  await publishToFacebook(options);
} catch (error) {
  if (error.code === 'OAUTH_ERROR') {
    console.error('Access token expired. Refresh token required.');
  } else if (error.code === 'RATE_LIMIT') {
    await retryPublish(() => publishToFacebook(options), {
      delay: 60000 // Wait 1 minute
    });
  }
}
```

## Best Practices

1. **Always validate research data** before passing to AI generators
2. **Use environment variables** for all API keys and secrets
3. **Implement caching** for research results to avoid redundant API calls
4. **Schedule content publishing** during peak engagement hours
5. **Monitor API usage** to stay within rate limits
6. **Test video renders locally** before deploying to production
7. **Keep multilingual content synchronized** across all platforms
