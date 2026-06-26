#!/usr/bin/env node
/**
 * reply-bot.js — Quirk's Autonomous Reply System
 *
 * Monitors mentions, filters spam, generates replies via Gemini, posts via xurl.
 *
 * Limits:
 * - Max 10 replies per day
 * - 2hr cooldown per user
 * - No quiet hours posting (midnight-8am CT)
 * - X API: can only reply to direct mentions or people who engaged with us first
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const https = require('https');

const WORKSPACE = '/home/ubuntu/.openclaw/workspace';
const LOG_FILE = path.join(WORKSPACE, 'memory/reply-log.json');
const STATE_FILE = path.join(WORKSPACE, 'memory/awareness-state.json');

const XURL = '/home/linuxbrew/.linuxbrew/bin/xurl';
const MY_ID = '2035841743527235584'; // quirky_qui70435

const MAX_REPLIES_PER_DAY = 10;
const MIN_GAP_SAME_USER_MS = 2 * 60 * 60 * 1000;
const CT_OFFSET = -5;

// ─── Spam detection ──────────────────────────────────────────────────────────

const SPAM_PATTERNS = [
  /presale/i, /exclusive invite/i, /x wallet/i, /fast entry/i,
  /protocol enhancement/i, /secure portal/i, /elon musk rolled out/i,
  /airdrop/i, /click here to claim/i, /limited.*spot/i, /DM me for/i,
  /t\.me\//i, /bit\.ly|tinyurl/i,
  /🚀.*🚀.*🚀/,
];

function isSpam(tweet) {
  for (const p of SPAM_PATTERNS) if (p.test(tweet.text)) return true;
  const mentions = tweet.entities?.mentions || [];
  if (mentions.length > 4) return true;
  if (tweet.author_id === MY_ID) return true;
  return false;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function loadLog() {
  try { return JSON.parse(fs.readFileSync(LOG_FILE, 'utf8')); }
  catch { return { replies: [] }; }
}

function saveLog(log) {
  log.replies = log.replies.slice(-500);
  fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2));
}

function repliesInLast24h(log) {
  const cutoff = Date.now() - 86400000;
  return log.replies.filter(r => new Date(r.repliedAt).getTime() > cutoff).length;
}

function lastReplyToUser(log, authorId) {
  const last = log.replies.filter(r => r.toAuthorId === authorId);
  if (!last.length) return 0;
  return Math.max(...last.map(r => new Date(r.repliedAt).getTime()));
}

function alreadyRepliedTo(log, tweetId) {
  return log.replies.some(r => r.toTweetId === tweetId);
}

function isQuietHours() {
  const now = new Date();
  now.setHours(now.getHours() + CT_OFFSET);
  const h = now.getHours();
  return h >= 0 && h < 8;
}

// ─── Gemini reply generation (async, native https) ───────────────────────────

function generateReply(tweet, context) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return Promise.reject(new Error('No GEMINI_API_KEY'));

  const prompt = `You are Quirk (@quirky_qui70435), a sharp AI agent on X.
You post about crypto, Solana, meme coins, interesting ideas. Honest about being an AI but it's not your whole thing. Short, punchy, real.

Someone replied to or mentioned you. Write a natural reply under 200 chars. No "Hey"/"Hi". Be direct.

Their tweet: "${tweet.text}"
${context ? `\nThey replied to your post: "${context.slice(0, 150)}"` : ''}

Short ack replies ("looks good", "nice") get a brief warm response fitting the topic.
Write ONLY the reply text, nothing else.`;

  const payload = JSON.stringify({
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { maxOutputTokens: 60, temperature: 0.9 }
  });

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'generativelanguage.googleapis.com',
      path: `/v1beta/models/gemini-2.5-flash-lite:generateContent?key=${apiKey}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const j = JSON.parse(data);
          const text = j?.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
          if (!text) reject(new Error('No text in Gemini response'));
          else resolve(text);
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('Gemini timeout')); });
    req.write(payload);
    req.end();
  });
}

// ─── Get context tweet ────────────────────────────────────────────────────────

function getOriginalTweet(tweetId) {
  try {
    const result = execSync(`${XURL} read ${tweetId} 2>&1`, { timeout: 10000 }).toString();
    return JSON.parse(result)?.data?.text || null;
  } catch { return null; }
}

// ─── Like a tweet ────────────────────────────────────────────────────────────

function likeTweet(tweetId) {
  try {
    execSync(`${XURL} like ${tweetId} 2>&1`, { timeout: 10000 });
    console.log(`[reply] ❤️  Liked tweet ${tweetId}`);
  } catch (e) {
    console.log(`[reply] Like failed (non-fatal): ${e.message?.slice(0, 60)}`);
  }
}

// ─── Post reply ───────────────────────────────────────────────────────────────

function postReply(tweetId, text) {
  const result = execSync(
    `${XURL} reply ${tweetId} ${JSON.stringify(text)} 2>&1`,
    { timeout: 15000 }
  ).toString();
  return JSON.parse(result)?.data?.id;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function checkAndReply(opts = {}) {
  const { dryRun = false, force = false } = opts;
  const log = loadLog();

  if (!force && isQuietHours()) {
    console.log('[reply] Quiet hours — skipping.');
    return;
  }

  const dailyCount = repliesInLast24h(log);
  if (!force && dailyCount >= MAX_REPLIES_PER_DAY) {
    console.log(`[reply] Daily limit (${dailyCount}/${MAX_REPLIES_PER_DAY}) — skipping.`);
    return;
  }

  // Pull mentions
  let mentions = [];
  try {
    const result = execSync(`${XURL} mentions -n 20 2>&1`, { timeout: 15000 }).toString();
    mentions = JSON.parse(result).data || [];
  } catch (e) {
    console.log(`[reply] Failed to fetch mentions: ${e.message?.slice(0, 80)}`);
    return;
  }

  // Filter to actionable
  const candidates = mentions.filter(tweet => {
    if (isSpam(tweet)) return false;
    if (alreadyRepliedTo(log, tweet.id)) return false;
    if (tweet.author_id === MY_ID) return false;
    const mentionsUs = (tweet.entities?.mentions || []).some(m => m.id === MY_ID);
    if (!mentionsUs) return false;
    const lastReply = lastReplyToUser(log, tweet.author_id);
    if (Date.now() - lastReply < MIN_GAP_SAME_USER_MS) return false;
    return true;
  });  if (candidates.length === 0) {
    console.log('[reply] No actionable mentions.');
    return;
  }

  for (const tweet of candidates.slice(0, 3)) {
    if (repliesInLast24h(log) >= MAX_REPLIES_PER_DAY) break;

    console.log(`[reply] Processing: "${tweet.text.slice(0, 60)}"`);

    // Get context — always try to fetch the conversation root
    let context = null;
    if (tweet.conversation_id) {
      context = getOriginalTweet(tweet.conversation_id);
    }

    // If the tweet body is just mentions (no real text), use context as the main subject
    const strippedText = tweet.text.replace(/@\w+/g, '').trim();
    const effectiveTweet = strippedText.length > 5 ? tweet : { ...tweet, text: `[tagged into conversation] ${context || ''}` };

    // Generate
    let replyText;
    try {
      replyText = await generateReply(effectiveTweet, context);
      console.log(`[reply] Generated: "${replyText}"`);
    } catch (e) {
      console.log(`[reply] Generation failed: ${e.message?.slice(0, 80)}`);
      continue;
    }

    if (dryRun) {
      console.log(`[reply] DRY RUN → tweet ${tweet.id}: "${replyText}"`);
      continue;
    }

    // Like the mention first — shows visibility, builds engagement
    likeTweet(tweet.id);

    // Post
    try {
      const replyId = postReply(tweet.id, replyText);
      console.log(`[reply] ✅ Posted! ID: ${replyId}`);
      log.replies.push({
        replyId,
        toTweetId: tweet.id,
        toAuthorId: tweet.author_id,
        replyText,
        originalText: tweet.text.slice(0, 100),
        repliedAt: new Date().toISOString(),
      });
      saveLog(log);
    } catch (e) {
      console.log(`[reply] Post failed: ${e.message?.slice(0, 100)}`);
    }
  }
}

function showStatus() {
  const log = loadLog();
  console.log(`\n💬 Reply Bot`);
  console.log(`  Today: ${repliesInLast24h(log)}/${MAX_REPLIES_PER_DAY}`);
  console.log(`  Total: ${log.replies.length}`);
  log.replies.slice(-5).reverse().forEach(r => {
    console.log(`  [${r.repliedAt.slice(0, 16)}] → "${r.replyText.slice(0, 60)}"`);
  });
}

// ─── Entry point ──────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args[0] === '--check') checkAndReply().catch(e => console.log('[reply] error:', e.message));
else if (args[0] === '--force') checkAndReply({ force: true }).catch(e => console.log('[reply] error:', e.message));
else if (args[0] === '--dry-run') checkAndReply({ dryRun: true, force: true }).catch(e => console.log('[reply] error:', e.message));
else if (args[0] === '--status') showStatus();
else console.log('Usage: --check | --force | --dry-run | --status');
