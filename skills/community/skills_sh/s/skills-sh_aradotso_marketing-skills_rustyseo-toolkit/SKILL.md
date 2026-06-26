---
name: rustyseo-toolkit
description: Cross-platform SEO/GEO toolkit built with Tauri and Rust for crawling, analyzing websites, and parsing server logs without crawl limits
triggers:
  - how do I crawl a website with RustySEO
  - analyze SEO metrics using RustySEO
  - parse nginx or apache logs for SEO insights
  - integrate Google Search Console with RustySEO
  - use RustySEO API connectors for PageSpeed Insights
  - generate keyword clusters and topics with RustySEO
  - run deep crawl with RustySEO headless mode
  - export RustySEO crawl data to CSV or Excel
---

# RustySEO Toolkit

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

RustySEO is a free, cross-platform SEO/GEO toolkit built with Tauri, Rust, Next.js, and TypeScript. It provides comprehensive website crawling, technical SEO analysis, log parsing (Nginx/Apache), AI-powered insights, and integrations with Google Search Console, GA4, PageSpeed Insights, and more. No crawl limits, fully local with optional cloud API integrations.

## Installation

### Desktop Application

Download the latest release for your platform from the [releases page](https://github.com/mascanho/RustySEO/releases):

- **Windows**: `.msi` installer (ignore "Unknown Developer" warning)
- **macOS**: `.dmg` installer (allow in System Preferences > Security & Privacy)
- **Linux**: `.AppImage` or `.deb` package

### Development Setup

```bash
# Clone the repository
git clone https://github.com/mascanho/RustySEO.git
cd RustySEO

# Install dependencies
npm install

# Run in development mode
npm run tauri dev

# Build for production
npm run tauri build
```

### TUI/Headless Mode (Separate Installation)

For terminal-based crawling, install the headless version:

```bash
git clone https://github.com/mascanho/RustySEO-Headless.git
cd RustySEO-Headless
cargo build --release
```

## Core Features

### 1. Website Crawling

**Shallow Crawl (Single Page)**
```typescript
// Example: Trigger shallow crawl programmatically
// Located in: src/components/Crawler.tsx

interface CrawlConfig {
  url: string;
  followLinks: boolean;
  respectRobotsTxt: boolean;
  userAgent: string;
}

const shallowCrawl = async (config: CrawlConfig) => {
  const result = await invoke('shallow_crawl', {
    url: config.url,
    followLinks: false,
    respectRobotsTxt: true
  });
  return result;
};
```

**Deep Crawl (Multiple Pages)**
```typescript
// Example: Deep crawl with concurrency control
const deepCrawl = async (baseUrl: string, maxPages: number = 100) => {
  const result = await invoke('deep_crawl', {
    url: baseUrl,
    maxPages: maxPages,
    concurrency: 5, // Concurrent requests
    delay: 1000 // Milliseconds between requests
  });
  return result;
};
```

**Keyboard Shortcuts**
- `CTRL + D`: Deep Crawl
- `CTRL + S`: Shallow Crawl
- `CTRL + H`: Toggle Sidebar
- `CTRL + L`: Toggle Task Manager

### 2. API Connectors Configuration

RustySEO integrates with multiple APIs. Configure them via the UI (Connectors menu) or directly in the config:

```typescript
// Example: Configure PageSpeed Insights API
// Stored in local SQLite database

interface APIConfig {
  provider: 'pagespeed' | 'gemini' | 'gsc' | 'ga4';
  apiKey: string;
  enabled: boolean;
}

const setAPIKey = async (config: APIConfig) => {
  await invoke('save_api_config', {
    provider: config.provider,
    apiKey: config.apiKey,
    enabled: true
  });
};

// Usage
await setAPIKey({
  provider: 'pagespeed',
  apiKey: process.env.GOOGLE_PAGESPEED_API_KEY || '',
  enabled: true
});
```

**Environment Variables for API Keys**
```bash
# .env.local
GOOGLE_PAGESPEED_API_KEY=your_pagespeed_key_here
GOOGLE_GEMINI_API_KEY=your_gemini_key_here
GOOGLE_GSC_CLIENT_ID=your_oauth_client_id
GOOGLE_GSC_CLIENT_SECRET=your_oauth_client_secret
GOOGLE_GA4_PROPERTY_ID=your_ga4_property_id
```

### 3. Log Analysis (Nginx/Apache)

```typescript
// Example: Parse and analyze server logs
interface LogAnalysisConfig {
  logPath: string;
  logType: 'nginx' | 'apache';
  startDate?: string;
  endDate?: string;
}

const analyzeLogs = async (config: LogAnalysisConfig) => {
  const analysis = await invoke('parse_logs', {
    path: config.logPath,
    logType: config.logType,
    filters: {
      startDate: config.startDate,
      endDate: config.endDate
    }
  });
  
  // Returns: bot traffic, crawl frequency, errors, popular pages
  return analysis;
};

// Usage
const logData = await analyzeLogs({
  logPath: '/var/log/nginx/access.log',
  logType: 'nginx',
  startDate: '2024-01-01',
  endDate: '2024-01-31'
});

console.log(logData.botTraffic); // Googlebot, Bingbot stats
console.log(logData.errorPages); // 404, 500 errors
```

### 4. SEO Analysis & Reporting

```typescript
// Example: Extract SEO metrics from crawl
interface SEOMetrics {
  title: string;
  metaDescription: string;
  h1Tags: string[];
  h2Tags: string[];
  canonicalUrl: string;
  openGraphTags: Record<string, string>;
  structuredData: object[];
  imageCount: number;
  internalLinks: number;
  externalLinks: number;
  wordCount: number;
  loadTime: number;
}

const analyzePage = async (url: string): Promise<SEOMetrics> => {
  const crawlResult = await invoke('shallow_crawl', { url });
  
  return {
    title: crawlResult.title,
    metaDescription: crawlResult.meta_description,
    h1Tags: crawlResult.h1_tags,
    h2Tags: crawlResult.h2_tags,
    canonicalUrl: crawlResult.canonical,
    openGraphTags: crawlResult.og_tags,
    structuredData: crawlResult.structured_data,
    imageCount: crawlResult.images.length,
    internalLinks: crawlResult.internal_links.length,
    externalLinks: crawlResult.external_links.length,
    wordCount: crawlResult.word_count,
    loadTime: crawlResult.load_time_ms
  };
};
```

**Export Data**
```typescript
// Example: Export crawl data to various formats
const exportData = async (format: 'csv' | 'excel' | 'pdf' | 'sheets') => {
  await invoke('export_crawl_data', {
    format: format,
    crawlId: currentCrawlId,
    outputPath: `./exports/crawl-${Date.now()}.${format}`
  });
};

// CSV Export
await exportData('csv');

// Google Sheets (requires GSC OAuth)
await exportData('sheets');
```

### 5. AI Features

**Topic & Keyword Generation**
```typescript
// Example: Generate content topics using AI
interface TopicRequest {
  seed: string;
  count: number;
  model: 'gemini' | 'ollama';
}

const generateTopics = async (request: TopicRequest) => {
  const topics = await invoke('ai_generate_topics', {
    seed: request.seed,
    count: request.count,
    provider: request.model
  });
  return topics;
};

// Usage with Google Gemini
const topics = await generateTopics({
  seed: 'organic gardening tips',
  count: 10,
  model: 'gemini'
});

// Returns: ["Companion Planting Guide", "Composting 101", ...]
```

**Keyword Clustering**
```typescript
// Example: Cluster keywords using ML
const clusterKeywords = async (keywords: string[]) => {
  const clusters = await invoke('cluster_keywords', {
    keywords: keywords,
    minClusterSize: 5,
    algorithm: 'kmeans'
  });
  
  return clusters;
};

const keywords = ["seo tools", "seo software", "website crawler", "site audit"];
const result = await clusterKeywords(keywords);
// Returns: { cluster1: ["seo tools", "seo software"], cluster2: ["website crawler", "site audit"] }
```

**AI Chatbot with Crawl Context**
```typescript
// Example: Query AI about crawled pages
const askChatbot = async (question: string, crawlContext: string) => {
  const response = await invoke('ai_chat', {
    question: question,
    context: crawlContext,
    provider: 'gemini'
  });
  return response;
};

// Usage
const answer = await askChatbot(
  "What are the main SEO issues on this page?",
  JSON.stringify(currentPageData)
);
```

### 6. Google Search Console Integration

```typescript
// Example: Fetch GSC data
interface GSCQuery {
  siteUrl: string;
  startDate: string;
  endDate: string;
  dimensions?: ('query' | 'page' | 'country' | 'device')[];
}

const fetchGSCData = async (query: GSCQuery) => {
  // Requires OAuth2 authentication
  const data = await invoke('gsc_fetch_data', {
    siteUrl: query.siteUrl,
    startDate: query.startDate,
    endDate: query.endDate,
    dimensions: query.dimensions || ['query', 'page']
  });
  
  return data.rows; // { query, clicks, impressions, ctr, position }
};

// Usage
const gscData = await fetchGSCData({
  siteUrl: 'https://example.com',
  startDate: '2024-01-01',
  endDate: '2024-01-31',
  dimensions: ['query', 'page']
});
```

### 7. Schema Generator & Validator

```typescript
// Example: Generate and validate structured data
interface SchemaConfig {
  type: 'Article' | 'Product' | 'LocalBusiness' | 'FAQ';
  data: Record<string, any>;
}

const generateSchema = (config: SchemaConfig) => {
  const schema = {
    "@context": "https://schema.org",
    "@type": config.type,
    ...config.data
  };
  
  return JSON.stringify(schema, null, 2);
};

// Usage
const articleSchema = generateSchema({
  type: 'Article',
  data: {
    headline: 'Complete SEO Guide',
    author: { "@type": "Person", name: "John Doe" },
    datePublished: '2024-01-01',
    image: 'https://example.com/image.jpg'
  }
});

// Validate schema
const validateSchema = async (schemaJson: string) => {
  const validation = await invoke('validate_schema', {
    schema: schemaJson
  });
  return validation.isValid;
};
```

## Common Patterns

### Database Access (SQLite)

```typescript
// Example: Query crawl history
const getCrawlHistory = async (limit: number = 50) => {
  const history = await invoke('get_crawl_history', { limit });
  return history;
};

// Clear crawl logs
const clearLogs = async () => {
  await invoke('clear_crawl_logs');
};
```

### Task Manager

```typescript
// Example: Create and track SEO tasks
interface SEOTask {
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
}

const createTask = async (task: SEOTask) => {
  await invoke('create_task', {
    title: task.title,
    description: task.description,
    priority: task.priority,
    dueDate: task.dueDate
  });
};

// Keyboard shortcut: CTRL + T
```

### Image Optimization

```typescript
// Example: Convert and optimize images
interface ImageOptimizeConfig {
  inputPath: string;
  outputPath: string;
  format: 'webp' | 'avif' | 'jpeg';
  quality: number; // 1-100
}

const optimizeImage = async (config: ImageOptimizeConfig) => {
  await invoke('optimize_image', {
    input: config.inputPath,
    output: config.outputPath,
    format: config.format,
    quality: config.quality
  });
};
```

## Configuration

### User Agent Customization

```typescript
const setUserAgent = async (userAgent: string) => {
  await invoke('set_user_agent', { userAgent });
};

// Respect robots.txt
const setRobotsTxt = async (respect: boolean) => {
  await invoke('set_robots_txt_respect', { respect });
};
```

### Cache Management

```bash
# Keyboard shortcuts
CTRL + /           # Clear cache
CTRL + Shift + /   # Full app reset
```

## Troubleshooting

### Issue: "Unknown Developer" Warning (Windows/Mac)

**Windows**: Settings > Apps > Apps & features > Choose where to get apps > Allow apps from anywhere
**macOS**: System Preferences > Security & Privacy > Open Anyway

### Issue: API Rate Limiting

```typescript
// Add delay between requests
const crawlWithDelay = async (urls: string[], delayMs: number = 2000) => {
  for (const url of urls) {
    await invoke('shallow_crawl', { url });
    await new Promise(resolve => setTimeout(resolve, delayMs));
  }
};
```

### Issue: Large Website Crawling (>100K URLs)

Use the headless/TUI version for better performance:

```bash
# Install RustySEO-Headless
cd RustySEO-Headless
cargo run --release -- --url https://example.com --max-pages 100000
```

### Issue: OAuth2 Authentication Fails

Currently OAuth is server-side. Ensure redirect URIs are configured:

```
Authorized redirect URIs:
http://localhost:3000/api/auth/callback/google
```

### Issue: Local LLM (Ollama) Not Performing Well

Use Google Gemini instead for better AI features:

```typescript
// Switch to Gemini
const config = {
  provider: 'gemini',
  apiKey: process.env.GOOGLE_GEMINI_API_KEY
};
```

## CLI Commands (Headless Mode)

```bash
# Basic crawl
rustyseo-headless --url https://example.com

# Deep crawl with limits
rustyseo-headless --url https://example.com --max-pages 500 --concurrency 10

# Parse logs
rustyseo-headless --parse-logs /var/log/nginx/access.log --log-type nginx

# Export to CSV
rustyseo-headless --url https://example.com --export-csv output.csv
```

## Database Schema

RustySEO stores data in SQLite (`~/.rustyseo/data.db`):

```sql
-- Crawl results table
CREATE TABLE crawls (
  id INTEGER PRIMARY KEY,
  url TEXT NOT NULL,
  title TEXT,
  meta_description TEXT,
  status_code INTEGER,
  load_time_ms INTEGER,
  word_count INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SEO tasks table
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  priority TEXT,
  status TEXT DEFAULT 'pending',
  due_date TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Best Practices

1. **Rate Limiting**: Always add delays between requests to avoid getting blocked
2. **API Keys**: Store in environment variables, never hardcode
3. **Large Crawls**: Use headless mode for sites with >10K pages
4. **OAuth**: Set up proper redirect URIs in Google Cloud Console
5. **AI Features**: Prefer Gemini over local Ollama for production use
6. **Logging**: Enable debug mode for troubleshooting crawl issues

## Resources

- [Official Website](https://www.rustyseo.com)
- [GitHub Repository](https://github.com/mascanho/RustySEO)
- [Headless/TUI Version](https://github.com/mascanho/RustySEO-Headless)
- [Discord Community](https://discord.gg/X49Kj7AT)
- [Google PageSpeed API Docs](https://developers.google.com/speed/docs/insights/v5/get-started)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key)
