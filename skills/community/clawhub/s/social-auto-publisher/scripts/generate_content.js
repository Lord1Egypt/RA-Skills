#!/usr/bin/env node
/**
 * AI Content Generator
 * Automatically generates social media content optimized for multiple platforms based on a topic
 *
 * Usage:
 *   node scripts/generate_content.js --topic "How AI is changing content creation" --platforms "xiaohongshu,weibo,twitter"
 *   node scripts/generate_content.js --auto-topic --platforms "xiaohongshu"
 */

const fs = require('fs');
const path = require('path');

// ─── Argument Parsing ─────────────────────────────────────────────
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

// ─── Platform Content Templates ─────────────────────────────────────────
const PLATFORM_TEMPLATES = {
  xiaohongshu: {
    name: 'Xiaohongshu',
    titleMaxLen: 20,
    bodyMaxLen: 1000,
    tagCount: { min: 5, max: 10 },
    style: 'Xiaohongshu recommendation style',
    format: (topic, tone) => ({
      role: 'system',
      content: `You are an expert at creating viral Xiaohongshu posts. Please generate a Xiaohongshu post based on the following topic.
Requirements:
- Title: 15-20 characters, use numbers and emojis, embed keywords
- Body: Grab attention in the first 3 sentences, leave blank lines between paragraphs, include 2-3 emojis per paragraph
- 5-10 precise hashtags (combination of high-traffic keywords + long-tail keywords)
- End with an engagement prompt (save/like/comment)
- Tone: ${tone || 'authentic sharing'}`,
      userPrompt: `Topic: ${topic}`,
    }),
  },
  weibo: {
    name: 'Weibo',
    titleMaxLen: 0, // Weibo does not use a separate title
    bodyMaxLen: 140,
    tagCount: { min: 2, max: 5 },
    style: 'Weibo style',
    format: (topic, tone) => ({
      role: 'system',
      content: `You are an expert at Weibo content creation. Please generate a Weibo post based on the following topic.
Requirements:
- 140 characters or fewer, concise and impactful
- 2-3 double-hash topic tags
- Use emojis appropriately
- Tone: ${tone || 'approachable and engaging'}`,
      userPrompt: `Topic: ${topic}`,
    }),
  },
  twitter: {
    name: 'Twitter',
    titleMaxLen: 0,
    bodyMaxLen: 280,
    tagCount: { min: 1, max: 3 },
    style: 'Twitter thread',
    format: (topic, tone) => ({
      role: 'system',
      content: `You are an expert at Twitter content creation. Please generate a tweet based on the following topic.
Requirements:
- English tweet within 280 characters
- 1-3 hashtags
- Include a hook, an insight, and a call-to-action
- Tone: ${tone || 'insightful and engaging'}`,
      userPrompt: `Topic: ${topic}`,
    }),
  },
};

// ─── Trend Tracking ─────────────────────────────────────────────
async function fetchHotTopics() {
  try {
    const { execSync } = require('child_process');
    const result = execSync(
      'node -e "const https=require(\'https\');https.get(\'https://newsnow.busiyi.world/api/hottest\',r=>{let d=\'\';r.on(\'data\',c=>d+=c);r.on(\'end\',()=>console.log(d))})"',
      { timeout: 10000 }
    ).toString();
    const data = JSON.parse(result);
    return (data.items || data.data || []).slice(0, 10).map(i => i.title || i.name || i);
  } catch {
    // Fallback: return static trending topics
    console.error('[warn] Failed to fetch trending topics, using default topics');
    return [
      'How AI tools are transforming content creation',
      '2026 social media operations trends',
      'How to build a personal brand from scratch',
    ];
  }
}

// ─── Content Output Formatting ───────────────────────────────────────
function formatOutput(topic, platforms, tone) {
  const result = {
    generatedAt: new Date().toISOString(),
    topic,
    tone: tone || 'default',
    platforms: {},
  };

  const platformList = platforms.split(',').map(p => p.trim());
  for (const platform of platformList) {
    const tpl = PLATFORM_TEMPLATES[platform];
    if (!tpl) {
      console.error(`[error] Unsupported platform: ${platform}`);
      continue;
    }

    // Generate content structure (actual AI generation is handled by the caller using openai or other models)
    result.platforms[platform] = {
      platform: tpl.name,
      prompt: tpl.format(topic, tone),
      constraints: {
        titleMaxLen: tpl.titleMaxLen,
        bodyMaxLen: tpl.bodyMaxLen,
        tagCount: tpl.tagCount,
      },
    };
  }

  return result;
}

// ─── Main Process ───────────────────────────────────────────────
async function main() {
  const opts = parseArgs();

  if (!opts.topic && !opts['auto-topic']) {
    console.error('Usage: node generate_content.js --topic "Topic" --platforms "xiaohongshu,weibo,twitter"');
    console.error('   or: node generate_content.js --auto-topic --platforms "xiaohongshu"');
    process.exit(1);
  }

  const platforms = opts.platforms || 'xiaohongshu';
  let topic = opts.topic;

  if (opts['auto-topic']) {
    const hotTopics = await fetchHotTopics();
    topic = hotTopics[0];
    console.log(`[info] Auto-selected topic: ${topic}`);
  }

  const output = formatOutput(topic, platforms, opts.tone);
  const count = opts.count ? parseInt(opts.count) : 1;

  // Output JSON
  const json = JSON.stringify(output, null, 2);
  console.log(json);

  // Save to file
  const outputDir = path.join(__dirname, '..', '..', '..', 'output');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
  const filename = `content_${Date.now()}.json`;
  fs.writeFileSync(path.join(outputDir, filename), json);
  console.error(`[info] Content saved: ${path.join(outputDir, filename)}`);
}

main().catch(err => {
  console.error('[error]', err.message);
  process.exit(1);
});