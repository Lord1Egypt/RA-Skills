#!/usr/bin/env node
/**
 * knowledge-intake/backlog-sweep.js
 *
 * One-time (or manual) sweep of all bookmarks for the authenticated user, paginating
 * back as far as the API allows. Triages each unseen URL and unbookmarks
 * after successful capture.
 *
 * Usage:
 *   node backlog-sweep.js [--dry-run] [--limit 50] [--delay 3]
 *
 * Options:
 *   --dry-run     Fetch and list URLs but don't triage or unbookmark
 *   --limit N     Stop after N bookmarks (default: unlimited)
 *   --delay N     Seconds between triage calls (default: 3)
 *   --no-unbookmark  Triage but skip unbookmarking
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.resolve(__dirname, '../../..');
const TOKEN_CACHE = path.join(WORKSPACE, 'data/x-oauth2-token-cache.json');
const SEEN_FILE = path.join(WORKSPACE, 'data/knowledge-intake-seen.json');
const SECRETS_FILE = process.env.X_OAUTH2_SECRETS_FILE || path.join(WORKSPACE, '..', '..', 'secrets', 'x-oauth2-credentials.json');

// Load refresh token from secrets file if not in env
// client_id + client_secret must come from plist env (or be passed in)
function loadSecretsToEnv() {
  if (!process.env.X_OAUTH2_REFRESH_TOKEN) {
    try {
      const s = JSON.parse(fs.readFileSync(SECRETS_FILE, 'utf8'));
      if (s.refresh_token) process.env.X_OAUTH2_REFRESH_TOKEN = s.refresh_token;
    } catch {}
  }
}

// ── Args ─────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const NO_UNBOOKMARK = args.includes('--no-unbookmark');
const limitIdx = args.indexOf('--limit');
const LIMIT = limitIdx >= 0 ? parseInt(args[limitIdx + 1]) : Infinity;
const delayIdx = args.indexOf('--delay');
const DELAY_SEC = delayIdx >= 0 ? parseInt(args[delayIdx + 1]) : 3;

// ── Token management ─────────────────────────────────────────────────────────
function getAccessToken() {
  const CLIENT_ID = process.env.X_OAUTH2_CLIENT_ID;
  const CLIENT_SECRET = process.env.X_OAUTH2_CLIENT_SECRET;
  const REFRESH_TOKEN = process.env.X_OAUTH2_REFRESH_TOKEN;

  if (!CLIENT_ID || !CLIENT_SECRET || !REFRESH_TOKEN) {
    throw new Error('Missing X_OAUTH2_CLIENT_ID, X_OAUTH2_CLIENT_SECRET, or X_OAUTH2_REFRESH_TOKEN');
  }

  let cache;
  try { cache = JSON.parse(fs.readFileSync(TOKEN_CACHE, 'utf8')); } catch {}
  if (cache?.access_token && (Date.now() - cache.cached_at) < 90 * 60 * 1000) {
    return cache.access_token;
  }

  const params = new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: REFRESH_TOKEN,
    client_id: CLIENT_ID,
  });
  const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64');
  const res = spawnSync('curl', [
    '-s', '-X', 'POST', 'https://api.x.com/2/oauth2/token',
    '-H', `Authorization: Basic ${credentials}`,
    '-H', 'Content-Type: application/x-www-form-urlencoded',
    '-d', params.toString()
  ]);
  const data = JSON.parse(res.stdout.toString());
  if (!data.access_token) {
    if (data.error === 'invalid_grant') {
      throw new Error(`Token refresh failed (invalid_grant). Your refresh token has rotated. New token saved to: data/x-oauth2-new-refresh-token.txt — update X_OAUTH2_REFRESH_TOKEN in your env and restart.`);
    }
    throw new Error(`Token refresh failed: ${JSON.stringify(data)}`);
  }

  if (data.refresh_token && data.refresh_token !== REFRESH_TOKEN) {
    console.log('⚠️  Refresh token rotated — update X_OAUTH2_REFRESH_TOKEN in plist');
    fs.writeFileSync(
      path.join(WORKSPACE, 'data/x-oauth2-new-refresh-token.txt'),
      data.refresh_token,
      { mode: 0o600 }
    );
    // Update in-memory env so subsequent runs in same process use new token
    process.env.X_OAUTH2_REFRESH_TOKEN = data.refresh_token;
  }
  fs.mkdirSync(path.dirname(TOKEN_CACHE), { recursive: true });
  fs.writeFileSync(TOKEN_CACHE, JSON.stringify({ ...data, cached_at: Date.now() }, null, 2));
  return data.access_token;
}

// ── User ID ──────────────────────────────────────────────────────────────────
function getUserId(accessToken) {
  const res = spawnSync('curl', [
    '-s', 'https://api.x.com/2/users/me',
    '-H', `Authorization: Bearer ${accessToken}`
  ]);
  const data = JSON.parse(res.stdout.toString());
  if (!data.data?.id) throw new Error(`Could not get user ID: ${JSON.stringify(data)}`);
  return { userId: data.data.id, username: data.data.username };
}

// ── Fetch one page of bookmarks ───────────────────────────────────────────────
function fetchBookmarkPage(accessToken, userId, paginationToken) {
  let url = `https://api.x.com/2/users/${userId}/bookmarks?max_results=100&tweet.fields=text,author_id,created_at,entities&expansions=author_id&user.fields=username,name`;
  if (paginationToken) url += `&pagination_token=${paginationToken}`;

  const res = spawnSync('curl', [
    '-s', '-w', '\n%{http_code}', url,
    '-H', `Authorization: Bearer ${accessToken}`
  ]);

  const output = res.stdout.toString();
  const lines = output.trim().split('\n');
  const statusCode = parseInt(lines[lines.length - 1]);
  const body = lines.slice(0, -1).join('\n');
  
  if (statusCode >= 400) {
    throw new Error(`X API error ${statusCode}: ${body}`);
  }

  const data = JSON.parse(body);
  const authors = {};
  for (const user of data.includes?.users || []) {
    authors[user.id] = user;
  }

  const bookmarks = (data.data || []).map(tweet => {
    const author = authors[tweet.author_id] || {};
    return {
      url: `https://x.com/${author.username || 'i'}/status/${tweet.id}`,
      tweetId: tweet.id,
      text: tweet.text,
      author: author.username ? `@${author.username}` : null,
    };
  });

  return {
    bookmarks,
    nextToken: data.meta?.next_token || null,
    resultCount: data.meta?.result_count || 0,
  };
}

// ── Unbookmark ────────────────────────────────────────────────────────────────
function deleteBookmark(accessToken, userId, tweetId) {
  const res = spawnSync('curl', [
    '-s', '-X', 'DELETE',
    `https://api.x.com/2/users/${userId}/bookmarks/${tweetId}`,
    '-H', `Authorization: Bearer ${accessToken}`
  ]);
  try {
    return JSON.parse(res.stdout.toString())?.data?.deleted === true;
  } catch { return false; }
}

// ── Seen check ────────────────────────────────────────────────────────────────
function hasSeen(url) {
  try {
    return JSON.parse(fs.readFileSync(SEEN_FILE, 'utf8')).urls.includes(url);
  } catch { return false; }
}

// ── Sleep ─────────────────────────────────────────────────────────────────────
function sleep(sec) {
  spawnSync('sleep', [String(sec)]);
}

// ── Main ──────────────────────────────────────────────────────────────────────
(async () => {
  loadSecretsToEnv();
  console.log(`[backlog-sweep] Starting full bookmark sweep${DRY_RUN ? ' (DRY RUN)' : ''}...`);
  if (LIMIT !== Infinity) console.log(`[backlog-sweep] Limit: ${LIMIT}`);

  let accessToken;
  try { accessToken = getAccessToken(); }
  catch (e) { console.error('[backlog-sweep] Auth failed:', e.message); process.exit(1); }

  const { userId, username } = getUserId(accessToken);
  console.log(`[backlog-sweep] Authenticated as @${username} (${userId})`);

  let page = 0;
  let nextToken = null;
  let totalFetched = 0;
  let totalTriaged = 0;
  let totalSkipped = 0;
  let totalUnbookmarked = 0;
  let totalFailed = 0;
  let done = false;

  while (!done) {
    page++;
    console.log(`\n[backlog-sweep] Page ${page}${nextToken ? ` (token: ${nextToken.slice(0, 12)}...)` : ''}...`);

    let pageData;
    try {
      pageData = fetchBookmarkPage(accessToken, userId, nextToken);
    } catch (e) {
      console.error('[backlog-sweep] Page fetch failed:', e.message);
      break;
    }

    if (pageData.bookmarks.length === 0) {
      console.log('[backlog-sweep] No more bookmarks.');
      break;
    }

    console.log(`[backlog-sweep] Got ${pageData.bookmarks.length} bookmarks this page`);

    for (const bookmark of pageData.bookmarks) {
      if (totalFetched >= LIMIT) { done = true; break; }
      totalFetched++;

      const alreadySeen = hasSeen(bookmark.url);
      console.log(`[backlog-sweep] [${totalFetched}] ${alreadySeen ? '(seen) ' : ''}${bookmark.url}`);

      if (DRY_RUN) continue;

      if (alreadySeen) {
        totalSkipped++;
        // Still unbookmark — captured in a prior run
        if (!NO_UNBOOKMARK && bookmark.tweetId) {
          if (deleteBookmark(accessToken, userId, bookmark.tweetId)) {
            totalUnbookmarked++;
            console.log(`[backlog-sweep] 🗑️  Unbookmarked (pre-seen): ${bookmark.tweetId}`);
          }
        }
        continue;
      }

      // Triage
      const result = spawnSync('node', [
        path.join(__dirname, 'triage-url.js'),
        bookmark.url,
        '--source', 'backlog sweep'
      ], { env: process.env, timeout: 60000 });

      const out = result.stdout?.toString() || '';
      const alreadySeenNow = out.includes('Already seen');

      if (alreadySeenNow) {
        // Was in seen cache — captured before, still unbookmark
        totalSkipped++;
        if (!NO_UNBOOKMARK && bookmark.tweetId) {
          if (deleteBookmark(accessToken, userId, bookmark.tweetId)) {
            totalUnbookmarked++;
            console.log(`[backlog-sweep] 🗑️  Unbookmarked (seen): ${bookmark.tweetId}`);
          }
        }
      } else if (result.status === 0) {
        totalTriaged++;
        if (!NO_UNBOOKMARK && bookmark.tweetId) {
          if (deleteBookmark(accessToken, userId, bookmark.tweetId)) {
            totalUnbookmarked++;
            console.log(`[backlog-sweep] 🗑️  Unbookmarked: ${bookmark.tweetId}`);
          }
        }
      } else {
        totalFailed++;
        console.error(`[backlog-sweep] ⚠️  Failed: ${bookmark.url}`);
        if (result.stderr) console.error(result.stderr.toString().slice(0, 200));
      }

      sleep(DELAY_SEC);
    }

    nextToken = pageData.nextToken;
    if (!nextToken) break;

    // Pause between pages to respect rate limits
    console.log('[backlog-sweep] Pausing 5s between pages...');
    sleep(5);
  }

  console.log(`
[backlog-sweep] ═══ Sweep Complete ═══
  Total fetched : ${totalFetched}
  Triaged       : ${totalTriaged}
  Skipped (seen): ${totalSkipped}
  Unbookmarked  : ${totalUnbookmarked}
  Failed        : ${totalFailed}
  Dry run       : ${DRY_RUN}
`);

  // Emit to bus (if available)
  const emitScript = path.join(WORKSPACE, 'scripts', 'emit-event.sh');
  if (fs.existsSync(emitScript)) {
    spawnSync('bash', [
      emitScript,
      'backlog-sweep', 'backlog_sweep_complete',
      `Backlog sweep: ${totalTriaged} triaged, ${totalSkipped} skipped, ${totalUnbookmarked} unbookmarked`,
      JSON.stringify({ totalFetched, totalTriaged, totalSkipped, totalUnbookmarked, totalFailed }),
      'knowledge'
    ], { env: process.env });
  } else {
    console.log('[backlog-sweep] emit-event.sh not available — skipping bus event');
  }
})();
