#!/usr/bin/env node
/**
 * Unified Publishing Entry
 * Automatically selects the publishing method (API / browser automation) based on the platform
 *
 * Usage:
 *   node scripts/publish.js --platform xiaohongshu --content-file ./output/post.json
 *   node scripts/publish.js --platforms "weibo,twitter" --content-file ./output/post.json
 *   node scripts/publish.js --platform xiaohongshu --content-file ./output/post.json --dry-run
 */

const fs = require('fs');
const weibo = require('./utils/weibo');
const twitter = require('./utils/twitter');
const xiaohongshu = require('./utils/xiaohongshu');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace(/^--/, '');
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : 'true';
      opts[key] = val;
      if (val !== 'true') i++;
    }
  }
  return opts;
}

function loadContent(contentFile) {
  if (!fs.existsSync(contentFile)) {
    console.error(`[error] File does not exist: ${contentFile}`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(contentFile, 'utf-8'));
}

function getPlatformContent(loaded, platform) {
  // Supports two formats: { platforms: { xiaohongshu: {...} } } or direct { title, body, tags }
  if (loaded.platforms && loaded.platforms[platform]) {
    return {
      ...loaded.platforms[platform],
      topic: loaded.topic,
      title: loaded.platforms[platform].title || loaded.title,
      body: loaded.platforms[platform].body || loaded.body,
      tags: loaded.platforms[platform].tags || loaded.tags,
    };
  }
  return loaded;
}

async function publishToXiaohongshu(content, dryRun) {
  const commands = xiaohongshu.buildPublishCommands(content);
  console.log('[xiaohongshu] Publishing command sequence:');
  for (const cmd of commands) {
    console.log(`  Step ${cmd.step}: ${cmd.description}`);
    console.log(`  Command: ${cmd.command}`);
  }

  if (dryRun) {
    console.log('[xiaohongshu] [DRY RUN] Did not actually publish');
    return { success: true, dryRun: true, steps: commands.length };
  }

  // Actual publishing is performed by the AI executing the browser act sequence
  console.log('[xiaohongshu] Please execute the above commands in a browser environment');
  return { success: true, steps: commands.length, note: 'Requires manual execution in browser' };
}

async function publishToWeibo(content, dryRun) {
  const text = weibo.formatContent(content);
  console.log(`[weibo] Content (${text.length} characters): ${text}`);

  if (dryRun) {
    console.log('[weibo] [DRY RUN] Did not actually publish');
    return { success: true, dryRun: true };
  }

  const appKey = process.env.WEIBO_APP_KEY;
  const accessToken = process.env.WEIBO_ACCESS_TOKEN;

  if (appKey && accessToken) {
    const req = await weibo.publishViaApi(content, { appKey, accessToken });
    console.log(`[weibo] API Publishing: ${req.method} ${req.url}`);
    // The actual HTTP request should be executed by the caller
    return { success: true, method: 'api', request: req };
  }

  // Fallback to browser mode
  const commands = weibo.buildBrowserCommands(content);
  console.log('[weibo] Cookie mode publishing commands:');
  for (const cmd of commands) {
    console.log(`  Step ${cmd.step}: ${cmd.description || cmd.action}`);
    console.log(`  Command: ${cmd.command}`);
  }
  return { success: true, method: 'browser', note: 'Requires manual execution in browser' };
}

async function publishToTwitter(content, dryRun) {
  const tweets = twitter.buildThread(content);
  console.log(`[twitter] Tweet thread (${tweets.length} tweets):`);
  tweets.forEach((t, i) => {
    console.log(`  [${i + 1}/${tweets.length}] (${t.text.length} characters) ${t.text.slice(0, 80)}...`);
  });

  if (dryRun) {
    console.log('[twitter] [DRY RUN] Did not actually publish');
    return { success: true, dryRun: true };
  }

  const apiKey = process.env.TWITTER_API_KEY;
  const apiSecret = process.env.TWITTER_API_SECRET;
  const accessToken = process.env.TWITTER_ACCESS_TOKEN;
  const accessSecret = process.env.TWITTER_ACCESS_SECRET;

  if (!apiKey || !accessToken) {
    console.log('[twitter] API credentials not configured; outputting content for manual operation');
    return { success: false, error: 'missing_credentials', tweets };
  }

  // Build API request information
  console.log('[twitter] API publishing ready');
  return {
    success: true,
    method: 'api',
    tweets: tweets.map((t, i) => ({
      index: i,
      text: t.text,
      replyTo: i > 0 ? '{previous_tweet_id}' : null,
    })),
  };
}

async function main() {
  const opts = parseArgs();
  const platformsStr = opts.platform || opts.platforms || '';
  const platforms = platformsStr.split(',').map(p => p.trim()).filter(Boolean);

  if (platforms.length === 0 || !opts['content-file']) {
    console.error('Usage: node publish.js --platform xiaohongshu --content-file <path> [--dry-run]');
    console.error('   or: node publish.js --platforms "weibo,twitter" --content-file <path>');
    process.exit(1);
  }

  const dryRun = !!opts['dry-run'];
  const loaded = loadContent(opts['content-file']);

  const results = {};
  for (const platform of platforms) {
    console.log(`\n─── Publishing to ${platform.toUpperCase()} ───`);
    const content = getPlatformContent(loaded, platform);

    switch (platform) {
      case 'xiaohongshu':
        results[platform] = await publishToXiaohongshu(content, dryRun);
        break;
      case 'weibo':
        results[platform] = await publishToWeibo(content, dryRun);
        break;
      case 'twitter':
        results[platform] = await publishToTwitter(content, dryRun);
        break;
      default:
        console.error(`[error] Unsupported platform: ${platform}`);
    }
  }

  console.log('\n─── Publishing Results ───');
  console.log(JSON.stringify(results, null, 2));
}

main().catch(err => {
  console.error('[error]', err.message);
  process.exit(1);
});