#!/usr/bin/env node
/**
 * knowledge-intake/triage-url.js
 * 
 * Fetches a URL (tweet or web page), triages it using Claude,
 * and posts a formatted card to #knowledge-intake.
 * 
 * Usage:
 *   node triage-url.js <url> [--source "manual drop" | "bookmark poll"]
 * 
 * Called by:
 *   - knowledge-intake-listener.js (when Jeremy drops a link in the channel)
 *   - bookmark-poll.js (automated bookmark sweep)
 */

const { execSync, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.resolve(__dirname, '../../..');
const CHANNEL_ID = process.env.KNOWLEDGE_INTAKE_CHANNEL_ID || '1481057788590297302'; // #knowledge-intake
const SEEN_FILE = path.join(WORKSPACE, 'data/knowledge-intake-seen.json');
const BOT_TOKEN = process.env.DISCORD_BOT_TOKEN;

const url = process.argv[2];
const source = process.argv[3] === '--source' ? process.argv[4] : 'manual drop';

if (!url) {
  console.error('Usage: node triage-url.js <url> [--source <label>]');
  process.exit(1);
}

if (!BOT_TOKEN) {
  console.error('Missing DISCORD_BOT_TOKEN');
  process.exit(1);
}

// ── Seen-URL deduplication ───────────────────────────────────────────────────

function loadSeen() {
  try {
    return JSON.parse(fs.readFileSync(SEEN_FILE, 'utf8'));
  } catch {
    return { urls: [] };
  }
}

function markSeen(url) {
  const seen = loadSeen();
  if (!seen.urls.includes(url)) {
    seen.urls.push(url);
    // Keep last 2000 URLs
    if (seen.urls.length > 2000) seen.urls = seen.urls.slice(-2000);
    fs.mkdirSync(path.dirname(SEEN_FILE), { recursive: true });
    fs.writeFileSync(SEEN_FILE, JSON.stringify(seen, null, 2));
  }
}

function hasSeen(url) {
  return loadSeen().urls.includes(url);
}

// ── URL fetching ─────────────────────────────────────────────────────────────

function fetchContent(url) {
  // X/Twitter URLs → fxtwitter
  const tweetMatch = url.match(/(?:x\.com|twitter\.com)\/(\w+)\/status\/(\d+)/);
  if (tweetMatch) {
    const [, username, id] = tweetMatch;
    const apiUrl = `https://api.fxtwitter.com/${username}/status/${id}`;
    try {
      const res = spawnSync('curl', ['-s', '--max-time', '10', apiUrl]);
      const data = JSON.parse(res.stdout.toString());
      const tweet = data.tweet;
      return {
        type: 'tweet',
        handle: `@${tweet.author?.screen_name || username}`,
        title: tweet.author?.name || username,
        content: tweet.text || '',
        url: tweet.url || url,
        media: tweet.media?.photos?.[0]?.url || null,
      };
    } catch (e) {
      console.error('fxtwitter fetch failed:', e.message);
      return null;
    }
  }

  // Web pages → markdown.new proxy
  const fetchUrl = `https://markdown.new/${encodeURIComponent(url)}`;
  try {
    const res = spawnSync('curl', ['-s', '--max-time', '15', '-L', fetchUrl]);
    const text = res.stdout.toString().slice(0, 8000); // cap at 8K chars
    return {
      type: 'web',
      handle: null,
      title: url,
      content: text,
      url,
      media: null,
    };
  } catch (e) {
    console.error('Web fetch failed:', e.message);
    return null;
  }
}

// ── Triage via Claude ────────────────────────────────────────────────────────

function triageContent(fetched, originalUrl) {
  const systemPrompt = `You are a knowledge triage assistant helping curate content into structured knowledge cards.
Your job is to analyze content and produce a structured triage card.
Be concise, opinionated, and specific to the user's primary domains (customize in adapting.md).
Respond ONLY with valid JSON, no markdown fences.`;

  const userPrompt = `Triage this content for relevance to the user's work.

Source type: ${fetched.type}
Handle/Author: ${fetched.handle || 'n/a'}
URL: ${originalUrl}
Content:
${fetched.content.slice(0, 6000)}

Respond with this exact JSON structure:
{
  "title": "Short descriptive title (not just the handle)",
  "miracle": "What's new, surprising, or impressive about this — 1-2 sentences",
  "why_it_matters": "Direct connection to the user's primary domains (customize in adapting.md) — 1-2 sentences. If not relevant, say so plainly.",
  "key_features": ["feature 1", "feature 2"],
  "proposed_action": "Specific next step: Implement X, Create knowledge doc, Add to task queue, or Ignore",
  "tier": 7,
  "tier_label": "Tier 2 — Worth tracking",
  "freshness": "evergreen",
  "topic": "#ai",
  "tags": ["#skill", "#tool"],
  "relevance_summary": "one sentence on why tier was chosen"
}

Tier guide:
9-10: Implement now or this week. Changes how we work.
7-8: Worth a thread + investigation soon.  
5-6: Good knowledge doc, revisit in a sprint.
3-4: Interesting but not directly actionable. Low priority.
1-2: Off-topic, personal, or purely entertainment. Not work-related.

For Tier 1-2 (off-topic/personal): set title to the actual content description, miracle to a one-liner, why_it_matters to "Not work-related — captured and cleared.", key_features to [], proposed_action to "None — captured for reference."

Freshness guide (pick one):
- "evergreen" — conceptual, timeless, still valid in 2 years (e.g. how RAG works, design principles)
- "dated" — still relevant but will age (e.g. current model benchmarks, product roadmaps)
- "expired" — time-sensitive content that's likely already stale (e.g. a sale, a specific drop, breaking news from months ago)

Topic guide (pick ONE primary topic):
- "#ai" — models, agents, LLMs, infrastructure
- "#product" — product design, UX, tools, apps
- "#revenue" — monetization, business models, growth
- "#agent-systems" — Agent systems and infrastructure
- "#personal" — personal interest, entertainment, life stuff
- "#x-strategy" — X/Twitter growth, content strategy, engagement

Tags — pick all that apply (finer-grained than topic): #skill #tool #model #ai #research #community #revenue #security #ux #infra #x-twitter #data #personal #entertainment`;

  try {
    const result = spawnSync('node', [
      '-e',
      `
const https = require('https');
const body = JSON.stringify({
  model: 'claude-haiku-4-5',
  max_tokens: 1024,
  system: ${JSON.stringify(systemPrompt)},
  messages: [{ role: 'user', content: ${JSON.stringify(userPrompt)} }]
});
const req = https.request({
  hostname: 'api.anthropic.com',
  path: '/v1/messages',
  method: 'POST',
  headers: {
    'x-api-key': process.env.ANTHROPIC_DEFAULT_KEY || process.env.ANTHROPIC_API_KEY,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json',
    'content-length': Buffer.byteLength(body)
  }
}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const parsed = JSON.parse(data);
    process.stdout.write(parsed.content[0].text);
  });
});
req.write(body);
req.end();
      `
    ], { env: process.env, timeout: 30000 });

    let raw = result.stdout.toString().trim();
    // Strip markdown code fences if model wrapped the JSON
    raw = raw.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
    const parsed = JSON.parse(raw);
    
    // Validate required fields
    const required = ['title', 'tier', 'freshness', 'topic'];
    for (const field of required) {
      if (!(field in parsed)) {
        console.error(`[triage-url] Missing required field: ${field} — raw: ${raw.slice(0, 200)}`);
        return null;
      }
    }
    
    // Validate tier range
    if (typeof parsed.tier !== 'number' || parsed.tier < 1 || parsed.tier > 10) {
      console.error(`[triage-url] Invalid tier: ${parsed.tier}`);
      parsed.tier = 5;
    }
    
    return parsed;
  } catch (e) {
    console.error('Triage failed:', e.message);
    return null;
  }
}

// ── Discord card formatting ──────────────────────────────────────────────────

function tierEmoji(tier) {
  if (tier >= 9) return '🥇';
  if (tier >= 7) return '🥈';
  if (tier >= 5) return '🥉';
  return '📌';
}

function buildCard(triage, fetched, originalUrl) {
  const emoji = tierEmoji(triage.tier);
  const handle = fetched.handle ? ` ${fetched.handle}` : '';
  const tags = triage.tags?.join(' ') || '';

  const freshnessEmoji = { evergreen: '🌿', dated: '📅', expired: '⏰' }[triage.freshness] || '📅';
  const topic = triage.topic || '';

  // Compact one-liner card for off-topic/personal content
  if (triage.tier <= 2) {
    return `📌 **${triage.title}**${handle} — ${triage.miracle} ${topic} ${tags} <${originalUrl}>`;
  }

  const features = triage.key_features?.length
    ? '\n**Key Features:**\n' + triage.key_features.map(f => `• ${f}`).join('\n')
    : '';

  return `🗂️ **${triage.title}**${handle}

• **The Miracle:** ${triage.miracle}
• **Why it matters:** ${triage.why_it_matters}${features}
• **Proposed Action:** ${triage.proposed_action}
• **Tier:** ${emoji} ${triage.tier_label} (${triage.tier}/10) — ${triage.relevance_summary}
• **Freshness:** ${freshnessEmoji} ${triage.freshness} | **Topic:** ${topic}
• **Tags:** ${tags}
• **Link:** <${originalUrl}>`;
}

// ── Discord post ─────────────────────────────────────────────────────────────

async function postToDiscord(message) {
  const body = JSON.stringify({ content: message });
  
  for (let attempt = 0; attempt < 3; attempt++) {
    const res = spawnSync('curl', [
      '-s', '-X', 'POST',
      `https://discord.com/api/v10/channels/${CHANNEL_ID}/messages`,
      '-H', `Authorization: Bot ${BOT_TOKEN}`,
      '-H', 'Content-Type: application/json',
      '-d', body
    ]);
    
    let data;
    try {
      data = JSON.parse(res.stdout.toString());
    } catch (e) {
      console.error(`[triage-url] Discord response parse error (attempt ${attempt + 1}): ${e.message}`);
      if (attempt < 2) spawnSync('sleep', ['2']);
      continue;
    }
    
    if (data.id) {
      console.log(`✅ Posted to #knowledge-intake: ${data.id}`);
      return true;
    }
    
    // Handle rate limit (429)
    if (data.retry_after) {
      const waitMs = Math.ceil(data.retry_after * 1000) + 100;
      console.log(`[triage-url] Rate limited, waiting ${Math.ceil(waitMs / 1000)}s...`);
      spawnSync('sleep', [String(Math.ceil(waitMs / 1000))]);
      continue;
    }
    
    if (attempt < 2) {
      console.log(`[triage-url] Post attempt ${attempt + 1} failed, retrying...`);
      spawnSync('sleep', ['1']);
    }
  }
  
  console.error('Discord post failed after retries');
  return false;
}

// ── Main ─────────────────────────────────────────────────────────────────────

(async () => {
  console.log(`[triage-url] Processing: ${url} (source: ${source})`);

  if (hasSeen(url)) {
    console.log(`[triage-url] Already seen, skipping: ${url}`);
    process.exit(0);
  }

  const fetched = fetchContent(url);
  if (!fetched) {
    console.error('[triage-url] Could not fetch content');
    process.exit(1);
  }

  const triage = triageContent(fetched, url);
  if (!triage) {
    console.error('[triage-url] Triage failed');
    process.exit(1);
  }

  // Skip very low tier items from bookmark poll only (never skip manual drops)
  const isManualDrop = source.startsWith('manual') || source === 'drop';
  if (!isManualDrop && triage.tier < 5) {
    console.log(`[triage-url] Tier ${triage.tier} — below threshold for automated post, skipping`);
    // Still mark as seen so we don't retry low-tier items
    markSeen(url);
    process.exit(0);
  }

  const card = buildCard(triage, fetched, url);
  
  // Mark as seen BEFORE Discord post — ensures durability even if post fails
  markSeen(url);
  
  const posted = await postToDiscord(card);

  if (posted) {
    // Emit to bus (if available)
    const emitScript = path.join(WORKSPACE, 'scripts', 'emit-event.sh');
    if (fs.existsSync(emitScript)) {
      spawnSync('bash', [
        emitScript,
        'knowledge-intake', 'knowledge_triaged',
        `Triaged: ${triage.title} (Tier ${triage.tier})`,
        JSON.stringify({ url, tier: triage.tier, action: triage.proposed_action }),
        'knowledge'
      ], { env: process.env });
    } else {
      console.log('[x-bookmark-triage] emit-event.sh not available — skipping bus event');
    }
  }
})();
