#!/usr/bin/env node
/**
 * Skroller - Social Media Content Collection
 * 
 * Uses Playwright for browser automation across social platforms.
 * Handles content collection, filtering, and export.
 * 
 * ⚖️ COMPLIANCE NOTICE:
 * - Review platform ToS before use
 * - Respect rate limits and robots.txt
 * - Comply with GDPR/CCPA for personal data
 * - Use only for permitted purposes (research, analysis)
 * - Do not collect personal data at scale without consent
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Platform-specific selectors and logic
const PLATFORMS = {
  twitter: {
    url: (query) => query.startsWith('@') 
      ? `https://twitter.com/${query}`
      : `https://twitter.com/search?q=${encodeURIComponent(query)}&f=live`,
    postSelector: '[data-testid="tweet"]',
    extract: async (el) => ({
      text: await el.$eval('[data-testid="tweetText"]', e => e.textContent || '').catch(() => ''),
      author: await el.$eval('[data-testid="User-Name"]', e => e.textContent || '').catch(() => ''),
      timestamp: await el.$eval('time', e => e.getAttribute('dateTime') || '').catch(() => ''),
      likes: await el.$eval('[data-testid="like"]', e => e.textContent || '0').catch(() => '0'),
      retweets: await el.$eval('[data-testid="retweet"]', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a[href*="/status/"]', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 1500
  },
  reddit: {
    url: (query) => `https://www.reddit.com/search/?q=${encodeURIComponent(query)}`,
    postSelector: '[data-testid="post-container"]',
    extract: async (el) => ({
      text: await el.$eval('[data-testid="post-title"]', e => e.textContent || '').catch(() => ''),
      author: await el.$eval('[data-testid="post-author"]', e => e.textContent || '').catch(() => ''),
      timestamp: await el.$eval('time', e => e.getAttribute('dateTime') || '').catch(() => ''),
      likes: await el.$eval('[data-testid="vote-count"]', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a[href*="/comments/"]', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 1000
  },
  instagram: {
    url: (query) => query.startsWith('@')
      ? `https://www.instagram.com/${query.replace('@', '')}/`
      : `https://www.instagram.com/explore/tags/${query.replace('#', '')}/`,
    postSelector: 'article',
    extract: async (el) => ({
      text: await el.$eval('a[href*="/p/"]', e => e.getAttribute('aria-label') || '').catch(() => ''),
      author: await el.$eval('a[href*="/"]', e => e.getAttribute('aria-label') || '').catch(() => ''),
      likes: await el.$eval('span', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a[href*="/p/"]', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 2000
  },
  tiktok: {
    url: (query) => `https://www.tiktok.com/search?q=${encodeURIComponent(query)}`,
    postSelector: '[data-e2e="search-post"]',
    extract: async (el) => ({
      text: await el.$eval('[data-e2e="search-post-desc"]', e => e.textContent || '').catch(() => ''),
      author: await el.$eval('[data-e2e="search-post-author"]', e => e.textContent || '').catch(() => ''),
      likes: await el.$eval('[data-e2e="search-post-like"]', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 2500
  },
  linkedin: {
    url: (query) => `https://www.linkedin.com/search/results/content/?keywords=${encodeURIComponent(query)}`,
    postSelector: 'div.ember-view[data-id]',
    extract: async (el) => ({
      text: await el.$eval('span[dir="ltr"]', e => e.textContent || '').catch(() => ''),
      author: await el.$eval('a[href*="/in/"]', e => e.textContent || '').catch(() => ''),
      timestamp: await el.$eval('span[aria-label]', e => e.getAttribute('aria-label') || '').catch(() => ''),
      likes: await el.$eval('button[aria-label*="Like"]', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a[href*="/posts/"]', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 2000
  },
  youtube: {
    url: (query) => `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`,
    postSelector: 'ytd-video-renderer',
    extract: async (el) => ({
      text: await el.$eval('#video-title', e => e.getAttribute('title') || '').catch(() => ''),
      author: await el.$eval('#channel-name', e => e.textContent || '').catch(() => ''),
      views: await el.$eval('#metadata-line', e => e.textContent || '').catch(() => ''),
      url: await el.$eval('#video-title', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 1500
  },
  producthunt: {
    url: (query) => `https://www.producthunt.com/search?q=${encodeURIComponent(query)}`,
    postSelector: '[data-test="search-result"]',
    extract: async (el) => ({
      text: await el.$eval('[data-test="headline"]', e => e.textContent || '').catch(() => ''),
      author: await el.$eval('[data-test="user-name"]', e => e.textContent || '').catch(() => ''),
      votes: await el.$eval('[data-test="vote-button"]', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a[href*="/posts/"]', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 1500
  },
  medium: {
    url: (query) => `https://medium.com/search?q=${encodeURIComponent(query)}`,
    postSelector: 'article',
    extract: async (el) => ({
      text: await el.$eval('[data-testid="post-title"]', e => e.textContent || '').catch(() => ''),
      author: await el.$eval('[data-testid="post-author-name"]', e => e.textContent || '').catch(() => ''),
      timestamp: await el.$eval('time', e => e.getAttribute('dateTime') || '').catch(() => ''),
      claps: await el.$eval('[data-testid="clap-count"]', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a[data-testid="post-title"]', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 1500
  },
  github: {
    url: (query) => `https://github.com/search?q=${encodeURIComponent(query)}&type=issues`,
    postSelector: 'li.Box-row',
    extract: async (el) => ({
      text: await el.$eval('a.title', e => e.textContent || '').catch(() => ''),
      author: await el.$eval('a.author', e => e.textContent || '').catch(() => ''),
      timestamp: await el.$eval('relative-time', e => e.getAttribute('datetime') || '').catch(() => ''),
      comments: await el.$eval('[aria-label*="comment"]', e => e.textContent || '0').catch(() => '0'),
      url: await el.$eval('a.title', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 1000
  },
  pinterest: {
    url: (query) => `https://www.pinterest.com/search/pins/?q=${encodeURIComponent(query)}`,
    postSelector: '[data-grid-item]',
    extract: async (el) => ({
      text: await el.$eval('[data-pin-title]', e => e.getAttribute('data-pin-title') || '').catch(() => ''),
      author: await el.$eval('[data-pin-user]', e => e.getAttribute('data-pin-user') || '').catch(() => ''),
      saves: await el.$eval('[data-save-count]', e => e.getAttribute('data-save-count') || '0').catch(() => '0'),
      url: await el.$eval('a[href*="/pin/"]', e => e.href || '').catch(() => '')
    }),
    scrollDelay: 2000
  }
};

// Load seen posts for deduplication
function loadSeenPosts() {
  const seenPath = path.join(process.cwd(), '.skroller-seen.json');
  if (fs.existsSync(seenPath)) {
    return JSON.parse(fs.readFileSync(seenPath, 'utf8'));
  }
  return {};
}

// Save seen posts
function saveSeenPosts(seen) {
  const seenPath = path.join(process.cwd(), '.skroller-seen.json');
  fs.writeFileSync(seenPath, JSON.stringify(seen, null, 2));
}

// Parse command line arguments
function parseArgs(args) {
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1];
      if (key === 'limit' || key === 'minLikes') {
        parsed[key] = parseInt(value || '0');
      } else if (key === 'screenshot' || key === 'dedupe') {
        parsed[key] = value === 'true' || value === undefined;
      } else {
        parsed[key] = value;
      }
      i++;
    }
  }
  return parsed;
}

// Format output
function formatOutput(posts, format, query, platform) {
  switch (format) {
    case 'csv': {
      const headers = ['id', 'author', 'text', 'timestamp', 'likes', 'url'];
      const rows = posts.map(p => 
        [p.id || '', p.author || '', p.text || '', p.timestamp || '', p.likes || p.votes || p.points || '0', p.url || '']
        .map(f => `"${f.replace(/"/g, '""')}"`).join(',')
      );
      return [headers.join(','), ...rows].join('\n');
    }
    
    case 'markdown': {
      let md = `## ${platform.toUpperCase()} Posts: "${query}" (${new Date().toISOString().split('T')[0]})\n\n`;
      posts.forEach(p => {
        md += `### ${p.author || 'Unknown'} - ${p.likes || p.votes || p.points || '0'} engagement\n`;
        md += `${p.text || ''}\n\n`;
        md += `[View post](${p.url || '#'})\n\n---\n\n`;
      });
      return md;
    }
    
    case 'json':
    default:
      return JSON.stringify({
        platform,
        query,
        collectedAt: new Date().toISOString(),
        posts
      }, null, 2);
  }
}

// Extract engagement number from post data
function extractEngagement(post) {
  const engagement = post.likes || post.votes || post.points || post.claps || post.saves || '0';
  return parseInt(engagement.replace(/[^0-9]/g, '')) || 0;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  
  const platform = args.platform?.toLowerCase();
  if (!platform || !PLATFORMS[platform]) {
    console.error('Error: --platform required');
    console.error('Supported: twitter, reddit, instagram, tiktok, linkedin, youtube, producthunt, medium, github, pinterest');
    process.exit(1);
  }
  
  const query = args.query || args.profile || '';
  const limit = args.limit || 50;
  const minLikes = args.minLikes || 0;
  const format = args.format || 'json';
  const output = args.output || `${platform}-${Date.now()}.${format}`;
  const screenshot = args.screenshot === true;
  const dedupe = args.dedupe === true;
  
  const seen = dedupe ? loadSeenPosts() : {};
  const config = fs.existsSync('.skroller-config.json') 
    ? JSON.parse(fs.readFileSync('.skroller-config.json', 'utf8'))
    : { scrollDelay: PLATFORMS[platform].scrollDelay };
  
  console.log(`Starting skroller for ${platform}...`);
  console.log(`Query: ${query || 'feed'}`);
  console.log(`Limit: ${limit} posts`);
  console.log(`Output: ${output} (${format})`);
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const url = PLATFORMS[platform].url(query);
  await page.goto(url, { waitUntil: 'networkidle' });
  
  const posts = [];
  const postSet = new Set();
  
  // Scroll and collect
  while (posts.length < limit) {
    const elements = await page.$$(PLATFORMS[platform].postSelector);
    
    for (const el of elements) {
      const data = await PLATFORMS[platform].extract(el);
      const postId = data.url || `${data.author}-${data.timestamp}`;
      
      if (dedupe && seen[postId]) continue;
      if (postSet.has(postId)) continue;
      
      // Apply engagement filter
      const likeCount = extractEngagement(data);
      if (likeCount < minLikes) continue;
      
      posts.push({ ...data, id: postId });
      postSet.add(postId);
      
      if (posts.length >= limit) break;
    }
    
    if (posts.length >= limit) break;
    
    // Scroll down
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(config.scrollDelay || PLATFORMS[platform].scrollDelay);
    
    // Optional: screenshot for debugging
    if (screenshot && posts.length % 10 === 0) {
      await page.screenshot({ path: `skroller-${posts.length}.png` });
    }
  }
  
  await browser.close();
  
  // Mark as seen
  if (dedupe) {
    posts.forEach(p => {
      if (p.id) seen[p.id] = true;
    });
    saveSeenPosts(seen);
  }
  
  // Write output
  const content = formatOutput(posts, format, query, platform);
  fs.writeFileSync(output, content);
  
  console.log(`\nCollected ${posts.length} posts`);
  console.log(`Saved to: ${output}`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
