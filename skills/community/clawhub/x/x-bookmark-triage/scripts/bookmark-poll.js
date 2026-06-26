#!/usr/bin/env node
/**
 * knowledge-intake/bookmark-poll.js
 * 
 * Polls X bookmarks for the authenticated user via OAuth 2.0 User Context.
 * Fetches up to 20 most recent bookmarks, dedupes, triages each.
 * 
 * Requires:
 *   X_OAUTH2_REFRESH_TOKEN  — from user's OAuth 2.0 flow
 *   X_OAUTH2_CLIENT_ID      — app client ID
 *   X_OAUTH2_CLIENT_SECRET  — app client secret
 * 
 * Run via cron: watsonflow-bookmark-poll (twice daily)
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.resolve(__dirname, '../../..');
const TOKEN_CACHE = path.join(WORKSPACE, 'data/x-oauth2-token-cache.json');

// ── OAuth 2.0 token management ───────────────────────────────────────────────

function loadTokenCache() {
  try {
    return JSON.parse(fs.readFileSync(TOKEN_CACHE, 'utf8'));
  } catch {
    return null;
  }
}

function saveTokenCache(data) {
  fs.mkdirSync(path.dirname(TOKEN_CACHE), { recursive: true });
  fs.writeFileSync(TOKEN_CACHE, JSON.stringify({
    ...data,
    cached_at: Date.now()
  }, null, 2));
}

function getAccessToken() {
  const CLIENT_ID = process.env.X_OAUTH2_CLIENT_ID;
  const CLIENT_SECRET = process.env.X_OAUTH2_CLIENT_SECRET;
  const REFRESH_TOKEN = process.env.X_OAUTH2_REFRESH_TOKEN;

  if (!CLIENT_ID || !CLIENT_SECRET || !REFRESH_TOKEN) {
    throw new Error('Missing X_OAUTH2_CLIENT_ID, X_OAUTH2_CLIENT_SECRET, or X_OAUTH2_REFRESH_TOKEN');
  }

  // Check cache — tokens last 2 hours, use if <90 min old
  const cache = loadTokenCache();
  if (cache?.access_token && (Date.now() - cache.cached_at) < 90 * 60 * 1000) {
    console.log('[bookmark-poll] Using cached access token');
    return cache.access_token;
  }

  console.log('[bookmark-poll] Refreshing access token...');
  const params = new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: REFRESH_TOKEN,
    client_id: CLIENT_ID,
  });

  const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64');
  const res = spawnSync('curl', [
    '-s', '-X', 'POST',
    'https://api.x.com/2/oauth2/token',
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

  // Save new refresh token if rotated
  if (data.refresh_token && data.refresh_token !== REFRESH_TOKEN) {
    console.log('[bookmark-poll] ⚠️  Refresh token rotated — update X_OAUTH2_REFRESH_TOKEN in plist');
    // Save to a file for the next run (protect with 0o600)
    fs.writeFileSync(
      path.join(WORKSPACE, 'data/x-oauth2-new-refresh-token.txt'),
      data.refresh_token,
      { mode: 0o600 }
    );
    // Update in-memory env so subsequent runs in same process use new token
    process.env.X_OAUTH2_REFRESH_TOKEN = data.refresh_token;
  }

  saveTokenCache(data);
  return data.access_token;
}

// ── Bookmark fetch ───────────────────────────────────────────────────────────

function fetchBookmarks(accessToken) {
  console.log('[bookmark-poll] Fetching bookmarks...');

  // First get authenticated user ID
  const meRes = spawnSync('curl', [
    '-s', '-w', '\n%{http_code}',
    'https://api.x.com/2/users/me',
    '-H', `Authorization: Bearer ${accessToken}`
  ]);

  const meOutput = meRes.stdout.toString();
  const meLines = meOutput.trim().split('\n');
  const meStatus = parseInt(meLines[meLines.length - 1]);
  const meBody = meLines.slice(0, -1).join('\n');
  
  if (meStatus >= 400) {
    throw new Error(`[bookmark-poll] X API error ${meStatus}: ${meBody}`);
  }

  const meData = JSON.parse(meBody);
  if (!meData.data?.id) {
    throw new Error(`Could not get user ID: ${JSON.stringify(meData)}`);
  }

  const userId = meData.data.id;
  console.log(`[bookmark-poll] User: ${meData.data.username} (${userId})`);

  // Fetch bookmarks
  const bookmarksRes = spawnSync('curl', [
    '-s', '-w', '\n%{http_code}',
    `https://api.x.com/2/users/${userId}/bookmarks?max_results=20&tweet.fields=text,author_id,created_at,entities&expansions=author_id&user.fields=username,name`,
    '-H', `Authorization: Bearer ${accessToken}`
  ]);

  const bookmarksOutput = bookmarksRes.stdout.toString();
  const bookmarksLines = bookmarksOutput.trim().split('\n');
  const bookmarksStatus = parseInt(bookmarksLines[bookmarksLines.length - 1]);
  const bookmarksBody = bookmarksLines.slice(0, -1).join('\n');
  
  if (bookmarksStatus >= 400) {
    console.error(`[bookmark-poll] X API error ${bookmarksStatus}: ${bookmarksBody}`);
    return [];
  }

  const bookmarksData = JSON.parse(bookmarksBody);

  if (!bookmarksData.data) {
    console.log('[bookmark-poll] No bookmarks found or API error:', JSON.stringify(bookmarksData));
    return [];
  }

  // Build author lookup
  const authors = {};
  for (const user of bookmarksData.includes?.users || []) {
    authors[user.id] = user;
  }

  const bookmarks = bookmarksData.data.map(tweet => {
    const author = authors[tweet.author_id] || {};
    return {
      url: `https://x.com/${author.username || 'i'}/status/${tweet.id}`,
      tweetId: tweet.id,
      text: tweet.text,
      author: author.username ? `@${author.username}` : null,
      authorName: author.name || null,
    };
  });

  return { bookmarks, userId };
}

// ── Unbookmark ───────────────────────────────────────────────────────────────

function deleteBookmark(accessToken, userId, tweetId) {
  const res = spawnSync('curl', [
    '-s', '-X', 'DELETE',
    `https://api.x.com/2/users/${userId}/bookmarks/${tweetId}`,
    '-H', `Authorization: Bearer ${accessToken}`
  ]);
  try {
    const data = JSON.parse(res.stdout.toString());
    return data?.data?.deleted === true;
  } catch {
    return false;
  }
}

// ── Main ─────────────────────────────────────────────────────────────────────

(async () => {
  console.log('[bookmark-poll] Starting bookmark sweep...');

  let accessToken;
  try {
    accessToken = getAccessToken();
  } catch (e) {
    console.error('[bookmark-poll] Auth failed:', e.message);
    process.exit(1);
  }

  let bookmarks;
  let userId;
  try {
    ({ bookmarks, userId } = fetchBookmarks(accessToken));
  } catch (e) {
    console.error('[bookmark-poll] Bookmark fetch failed:', e.message);
    process.exit(1);
  }

  console.log(`[bookmark-poll] Found ${bookmarks.length} bookmarks`);

  let triaged = 0;
  let skipped = 0;
  let unbookmarked = 0;

  for (const bookmark of bookmarks) {
    console.log(`[bookmark-poll] → ${bookmark.url}`);
    const result = spawnSync('node', [
      path.join(__dirname, 'triage-url.js'),
      bookmark.url,
      '--source', 'bookmark poll'
    ], {
      env: process.env,
      timeout: 45000
    });

    const out = result.stdout?.toString() || '';
    const err = result.stderr?.toString() || '';

    if (out.includes('Already seen')) {
      skipped++;
      // Still unbookmark already-seen items — they were captured in a prior run
      if (bookmark.tweetId && userId) {
        const deleted = deleteBookmark(accessToken, userId, bookmark.tweetId);
        if (deleted) unbookmarked++;
      }
    } else if (result.status === 0) {
      triaged++;
      // Unbookmark after successful triage
      if (bookmark.tweetId && userId) {
        const deleted = deleteBookmark(accessToken, userId, bookmark.tweetId);
        if (deleted) {
          unbookmarked++;
          console.log(`[bookmark-poll] 🗑️  Unbookmarked: ${bookmark.tweetId}`);
        } else {
          console.warn(`[bookmark-poll] ⚠️  Unbookmark failed for: ${bookmark.tweetId}`);
        }
      }
      // Brief pause between triage calls to avoid rate limits
      spawnSync('sleep', ['2']);
    } else {
      console.error(`[bookmark-poll] Triage failed for ${bookmark.url}:`, err.slice(0, 200));
    }
  }

  console.log(`[bookmark-poll] Done. Triaged: ${triaged}, Skipped (seen): ${skipped}, Unbookmarked: ${unbookmarked}`);

  // Emit summary to bus (if available)
  const emitScript = path.join(WORKSPACE, 'scripts', 'emit-event.sh');
  if (fs.existsSync(emitScript)) {
    spawnSync('bash', [
      emitScript,
      'bookmark-poll', 'bookmark_sweep_complete',
      `Bookmark sweep: ${triaged} triaged, ${skipped} skipped`,
      JSON.stringify({ triaged, skipped, total: bookmarks.length }),
      'knowledge'
    ], { env: process.env });
  } else {
    console.log('[bookmark-poll] emit-event.sh not available — skipping bus event');
  }
})();
