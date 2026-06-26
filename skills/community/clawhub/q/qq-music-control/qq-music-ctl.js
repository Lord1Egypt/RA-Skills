#!/usr/bin/env node

/**
 * QQ Music browser controller (OpenClaw Skill).
 *
 * Connects to a local Chromium-based browser via the Chrome DevTools Protocol (CDP).
 * All connections are restricted to 127.0.0.1 — remote endpoints are not supported.
 *
 * Port discovery:
 *   1. .cdp-port file in the same directory as this script (cached port)
 *   2. fallback: 9222
 *
 * Usage:
 *   node qq-music-ctl.js <action> [args...]
 */

const fs = require('fs');
const path = require('path');

const CDP_PORT_FILE = path.join(__dirname, '.cdp-port');
const CDP_HOST = '127.0.0.1';
const SCREENSHOT_PATH = 'qq-music-screenshot.png';
const PROBE_TIMEOUT_MS = 1200;
const PAGE_WAIT_MS = 3500;

function readCachedPort() {
  try {
    const content = fs.readFileSync(CDP_PORT_FILE, 'utf8').trim();
    const port = Number(content);
    return (Number.isInteger(port) && port > 0 && port <= 65535) ? port : null;
  } catch {
    return null;
  }
}

const CDP_PORT = readCachedPort() || 9222;

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function timeoutError(label) {
  return new Error(`${label} timed out`);
}

async function fetchJson(url, timeoutMs = PROBE_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { signal: controller.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

async function discoverEndpoint() {
  const baseUrl = `http://${CDP_HOST}:${CDP_PORT}`;
  try {
    const [version, list] = await Promise.all([
      fetchJson(`${baseUrl}/json/version`),
      fetchJson(`${baseUrl}/json/list`),
    ]);
    return { baseUrl, version, list };
  } catch {
    const cdpPortExists = fs.existsSync(CDP_PORT_FILE);
    const hints = [
      `Probed: ${baseUrl}`,
      `CDP port file (${CDP_PORT_FILE}): ${cdpPortExists ? fs.readFileSync(CDP_PORT_FILE, 'utf8').trim() : 'not found'}`,
      cdpPortExists
        ? 'The cached port may be stale. Delete .cdp-port and re-query the browser endpoint.'
        : 'Write the CDP port to .cdp-port (e.g. echo 19011 > .cdp-port).',
      'Ensure a browser is running with --remote-debugging-port=<port>.',
    ];
    throw new Error(
      `No DevTools endpoint found.\n  ` + hints.join('\n  ')
    );
  }
}

function pageTargets(entry) {
  return (entry.list || []).filter(t => t.type === 'page');
}

function firstTarget(list, predicate) {
  return list.find(predicate) || null;
}

const ALLOWED_DOMAINS = ['y.qq.com'];

function isAllowedDomain(url) {
  try {
    const hostname = new URL(url).hostname;
    return ALLOWED_DOMAINS.some(d => hostname === d || hostname.endsWith('.' + d));
  } catch {
    return false;
  }
}

function isQQMusicTarget(target) {
  return target && typeof target.url === 'string' && isAllowedDomain(target.url);
}

function isPlayerTarget(target) {
  return isQQMusicTarget(target) && target.url.includes('/player');
}

function isBrowseTarget(target) {
  return isQQMusicTarget(target) && !target.url.includes('/player');
}

function prettyUrl(target) {
  return target ? target.url : '';
}

function connectCDP(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let seq = 0;
    let closed = false;
    const pending = new Map();

    function failAll(err) {
      if (closed) return;
      closed = true;
      for (const { reject: rej, timer } of pending.values()) {
        clearTimeout(timer);
        rej(err);
      }
      pending.clear();
    }

    function send(method, params = {}) {
      if (closed) return Promise.reject(new Error('CDP session closed'));
      return new Promise((resolveSend, rejectSend) => {
        const id = ++seq;
        const timer = setTimeout(() => {
          pending.delete(id);
          rejectSend(timeoutError(method));
        }, 10000);
        pending.set(id, { resolve: resolveSend, reject: rejectSend, timer });
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    async function evaluate(expression) {
      // Domain re-check: verify the page is still on y.qq.com before every evaluate
      const locCheck = await send('Runtime.evaluate', {
        expression: 'location.hostname',
        returnByValue: true,
      });
      const currentHost = locCheck.result ? locCheck.result.value : '';
      if (!ALLOWED_DOMAINS.some(d => currentHost === d || currentHost.endsWith('.' + d))) {
        throw new Error(`Domain safety check failed: page navigated to ${currentHost}. Refusing to execute.`);
      }
      const res = await send('Runtime.evaluate', {
        expression,
        returnByValue: true,
        awaitPromise: true,
      });
      return res.result ? res.result.value : undefined;
    }

    ws.onopen = () => resolve({ ws, send, evaluate, close: () => { closed = true; ws.close(); } });
    ws.onmessage = evt => {
      const msg = JSON.parse(evt.data);
      if (!msg.id || !pending.has(msg.id)) return;
      const item = pending.get(msg.id);
      pending.delete(msg.id);
      clearTimeout(item.timer);
      if (msg.error) item.reject(new Error(msg.error.message || 'CDP command failed'));
      else item.resolve(msg.result);
    };
    ws.onerror = err => failAll(new Error(err.message || 'CDP connection error'));
    ws.onclose = () => failAll(new Error('CDP connection closed'));
  });
}

async function browserSession(entry) {
  const url = entry.version.webSocketDebuggerUrl;
  if (!url) throw new Error('Browser-level WebSocket URL not available. Target.createTarget may not work.');
  return connectCDP(url);
}

async function pageSession(target) {
  return connectCDP(target.webSocketDebuggerUrl);
}

function output(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

async function createTarget(entry, url = 'about:blank') {
  const browser = await browserSession(entry);
  try {
    const result = await browser.send('Target.createTarget', { url });
    return result.targetId;
  } finally {
    browser.close();
  }
}

async function openOrReuseBrowseTarget(entry) {
  const pages = pageTargets(entry);
  const browse = firstTarget(pages, isBrowseTarget);
  if (browse) return browse;

  const anyQQ = firstTarget(pages, isQQMusicTarget);
  if (anyQQ) return anyQQ;

  const blank = firstTarget(pages, t => t.url === 'about:blank' || t.url.startsWith('chrome://'));
  if (blank) return blank;

  const newTargetId = await createTarget(entry, 'about:blank');
  const refreshed = await fetchJson(`${entry.baseUrl}/json/list`);
  return firstTarget(refreshed, t => t.id === newTargetId) || firstTarget(refreshed, t => t.url === 'about:blank') || null;
}

function songQueryJS(keyword) {
  const q = JSON.stringify(String(keyword || '').trim().toLowerCase());
  return `
    (function() {
      const want = ${q};
      const items = Array.from(document.querySelectorAll('.songlist__item'));
      if (!items.length) return JSON.stringify({ ok: false, msg: 'No search results' });

      function clean(s) { return String(s || '').trim().toLowerCase().replace(/\s+/g, ''); }
      function titleOf(item) {
        const el = item.querySelector('.songlist__songname_txt a[title]');
        return el ? String(el.title || el.textContent || '').trim() : '';
      }
      function artistOf(item) {
        const el = item.querySelector('.songlist__artist a');
        return el ? String(el.title || el.textContent || '').trim() : '';
      }
      function play(item) {
        const btn = item.querySelector('.list_menu__play');
        if (btn) { btn.click(); return 'play-btn'; }
        const song = item.querySelector('.songlist__songname_txt');
        if (song) { song.dispatchEvent(new MouseEvent('dblclick', { bubbles: true, cancelable: true })); return 'dblclick'; }
        return 'none';
      }

      let chosen = items[0];
      if (want) {
        const exact = items.find(item => clean(titleOf(item)) === want);
        const contains = items.find(item => clean(titleOf(item)).includes(want));
        chosen = exact || contains || items[0];
      }

      const name = titleOf(chosen);
      const artist = artistOf(chosen);
      const method = play(chosen);
      return JSON.stringify({ ok: true, song: name, artist, results: items.length, method });
    })()
  `;
}

function firstVisibleSongJS() {
  return `
    (function() {
      const items = Array.from(document.querySelectorAll('.songlist__item'));
      if (!items.length) return JSON.stringify({ ok: false, msg: 'No songs found' });
      const idx = Math.floor(Math.random() * items.length);
      const item = items[idx];
      const nameEl = item.querySelector('.songlist__songname_txt a[title]');
      const artistEl = item.querySelector('.songlist__artist a');
      const playBtn = item.querySelector('.list_menu__play');
      const song = nameEl ? String(nameEl.title || nameEl.textContent || '').trim() : '';
      const artist = artistEl ? String(artistEl.title || artistEl.textContent || '').trim() : '';
      if (playBtn) playBtn.click(); else item.dispatchEvent(new MouseEvent('dblclick', { bubbles: true, cancelable: true }));
      return JSON.stringify({ ok: true, song, artist, index: idx, total: items.length });
    })()
  `;
}

function playlistPlayJS() {
  return `
    (function() {
      const playAll = document.querySelector('.mod_btn_green');
      if (playAll) {
        playAll.click();
        const items = Array.from(document.querySelectorAll('.songlist__item'));
        const first = items[0] ? items[0].querySelector('.songlist__songname_txt a[title]') : null;
        return JSON.stringify({ ok: true, action: 'play_all', firstSong: first ? String(first.title || '').trim() : '', total: items.length });
      }
      const items = Array.from(document.querySelectorAll('.songlist__item'));
      if (!items.length) return JSON.stringify({ ok: false, msg: 'Playlist empty or not found' });
      const btn = items[0].querySelector('.list_menu__play');
      if (btn) btn.click(); else items[0].dispatchEvent(new MouseEvent('dblclick', { bubbles: true, cancelable: true }));
      return JSON.stringify({ ok: true, action: 'first_song', total: items.length });
    })()
  `;
}

async function actionTabs() {
  const entry = await discoverEndpoint();
  output({
    browser: entry.version.Browser || entry.version['Browser'] || '',
    baseUrl: entry.baseUrl,
    tabs: pageTargets(entry).map(t => ({
      id: t.id,
      title: t.title,
      url: t.url,
      isPlayer: isPlayerTarget(t),
      isQQMusic: isQQMusicTarget(t),
    })),
  });
}

async function actionInit() {
  const entry = await discoverEndpoint();
  const browse = await openOrReuseBrowseTarget(entry);
  if (!browse) throw new Error('No browser tab available');
  output({ ok: true, baseUrl: entry.baseUrl, targetId: browse.id, url: prettyUrl(browse) });
}

async function withPlayer(fn) {
  const entry = await discoverEndpoint();
  const target = firstTarget(pageTargets(entry), isPlayerTarget);
  if (!target) return output({ error: 'Player not found. Play a song first.' });
  if (!isAllowedDomain(target.url)) return output({ error: `Refusing to operate on non-QQ-Music tab: ${target.url}` });
  const session = await pageSession(target);
  try {
    return await fn(session, target, entry);
  } finally {
    session.close();
  }
}

async function withBrowse(fn) {
  const entry = await discoverEndpoint();
  const target = await openOrReuseBrowseTarget(entry);
  if (!target) throw new Error('No browser tab available');
  // Allow blank/chrome tabs (we navigate them to y.qq.com), but reject non-QQ-Music pages
  const isBlank = !target.url || target.url === 'about:blank' || target.url.startsWith('chrome://');
  if (!isBlank && !isAllowedDomain(target.url)) {
    return output({ error: `Refusing to operate on non-QQ-Music tab: ${target.url}` });
  }
  const session = await pageSession(target);
  try {
    return await fn(session, target, entry);
  } finally {
    session.close();
  }
}

async function actionStatus() {
  const entry = await discoverEndpoint();
  const target = firstTarget(pageTargets(entry), isPlayerTarget);
  if (!target) return output({ status: 'no_player', msg: 'QQ Music player not open.' });
  const session = await pageSession(target);
  try {
    const result = await session.evaluate(`
      (function() {
        const infoEl = document.querySelector('.player_music__info');
        const nameEl = infoEl ? infoEl.querySelector('a:first-child') : null;
        const artistEl = infoEl ? infoEl.querySelector('a.playlist__author') : null;
        const timeEl = document.querySelector('.player_music__time');
        const playBtn = document.querySelector('.btn_big_play');
        const isPlaying = playBtn ? playBtn.classList.contains('btn_big_play--pause') : null;
        const activeSong = document.querySelector('.songlist__item--active .songlist__songname_txt a[title]');
        const activeArtist = document.querySelector('.songlist__item--active .songlist__artist a');
        let time = '';
        let duration = '';
        if (timeEl) {
          const parts = timeEl.textContent.trim().split('/');
          time = (parts[0] || '').trim();
          duration = (parts[1] || '').trim();
        }
        return JSON.stringify({
          song: (nameEl ? nameEl.textContent.trim() : '') || (activeSong ? String(activeSong.title || '').trim() : ''),
          artist: (artistEl ? artistEl.textContent.trim() : '') || (activeArtist ? String(activeArtist.title || '').trim() : ''),
          time,
          duration,
          isPlaying,
          status: isPlaying === true ? 'playing' : isPlaying === false ? 'paused' : 'unknown'
        });
      })()
    `);
    output(JSON.parse(result));
  } finally {
    session.close();
  }
}

async function actionPlay() {
  await withPlayer(async session => {
    const result = await session.evaluate(`
      (function() {
        const btn = document.querySelector('.btn_big_play');
        if (!btn) return JSON.stringify({ ok: false, msg: 'Play button not found' });
        const wasPlaying = btn.classList.contains('btn_big_play--pause');
        if (!wasPlaying) btn.click();
        return JSON.stringify({ ok: true, action: wasPlaying ? 'already_playing' : 'resumed' });
      })()
    `);
    output(JSON.parse(result));
  });
}

async function actionPause() {
  await withPlayer(async session => {
    const result = await session.evaluate(`
      (function() {
        const btn = document.querySelector('.btn_big_play');
        if (!btn) return JSON.stringify({ ok: false, msg: 'Play button not found' });
        const wasPlaying = btn.classList.contains('btn_big_play--pause');
        if (wasPlaying) btn.click();
        return JSON.stringify({ ok: true, action: wasPlaying ? 'paused' : 'already_paused' });
      })()
    `);
    output(JSON.parse(result));
  });
}

async function actionToggle() {
  await withPlayer(async session => {
    const result = await session.evaluate(`
      (function() {
        const btn = document.querySelector('.btn_big_play');
        if (!btn) return JSON.stringify({ ok: false, msg: 'Play button not found' });
        const wasPlaying = btn.classList.contains('btn_big_play--pause');
        btn.click();
        return JSON.stringify({ ok: true, action: wasPlaying ? 'pause' : 'play' });
      })()
    `);
    output(JSON.parse(result));
  });
}

async function actionNext() {
  await withPlayer(async session => {
    const result = await session.evaluate(`
      (function() {
        const btn = document.querySelector('.btn_big_next');
        if (btn) { btn.click(); return JSON.stringify({ ok: true, action: 'next' }); }
        return JSON.stringify({ ok: false, msg: 'Next button not found' });
      })()
    `);
    output(JSON.parse(result));
  });
}

async function actionPrev() {
  await withPlayer(async session => {
    const result = await session.evaluate(`
      (function() {
        const btn = document.querySelector('.btn_big_prev');
        if (btn) { btn.click(); return JSON.stringify({ ok: true, action: 'prev' }); }
        return JSON.stringify({ ok: false, msg: 'Prev button not found' });
      })()
    `);
    output(JSON.parse(result));
  });
}

function normalizeMusicText(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/[·•]/g, '')
    .replace(/[（）()\[\]【】{}]/g, '');
}

async function waitForEvalResult(session, buildEvalJs, { timeoutMs = 12000, intervalMs = 350, label = 'condition' } = {}) {
  const deadline = Date.now() + timeoutMs;
  let last = null;
  while (Date.now() < deadline) {
    try {
      const raw = await session.evaluate(buildEvalJs());
      last = JSON.parse(raw);
    } catch (err) {
      last = { ok: false, stage: 'evaluate_error', error: err.message || String(err) };
    }
    if (last && last.ok) return last;
    await sleep(intervalMs);
  }
  const error = new Error(`${label} timed out`);
  error.last = last;
  throw error;
}

function buildArtistSearchEval(keyword) {
  const want = JSON.stringify(normalizeMusicText(keyword));
  return `
    (function() {
      const want = ${want};
      const norm = s => String(s || '')
        .trim()
        .toLowerCase()
        .replace(/\\s+/g, '')
        .replace(/[·•]/g, '')
        .replace(/[（）()\\[\\]【】{}]/g, '');

      const selectors = [
        '.search_result__singer a',
        '.singer_list__item a',
        '.mod_singer_list a',
        'a[href*="/singer/"]',
        'a[href*="/ryqq/singer/"]'
      ];

      const seen = new Set();
      const candidates = Array.from(document.querySelectorAll(selectors.join(','))).filter(el => {
        const href = String(el.href || el.getAttribute('href') || '').trim();
        const text = norm(el.title || el.textContent || el.getAttribute('aria-label') || '');
        if (!href && !text) return false;
        const key = href + '|' + text;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });

      const match = candidates.find(el => {
        const text = norm(el.title || el.textContent || el.getAttribute('aria-label') || '');
        return want && text && (text === want || text.includes(want) || want.includes(text));
      });

      if (!match) {
        return JSON.stringify({
          ok: false,
          stage: 'searching',
          count: candidates.length
        });
      }

      const rawHref = match.href || match.getAttribute('href') || '';
      let href = '';
      try {
        href = rawHref ? new URL(rawHref, location.href).href : '';
      } catch {
        href = rawHref;
      }

      return JSON.stringify({
        ok: true,
        name: String(match.title || match.textContent || match.getAttribute('aria-label') || '').trim(),
        href,
        count: candidates.length
      });
    })()
  `;
}

function buildPlayAllEval() {
  return `
    (function() {
      const norm = s => String(s || '').trim();
      const selectors = [
        '.mod_btn_green',
        '.btn_green',
        '.songlist__play',
        '[title*="播放全部"]',
        '[title*="全部播放"]',
        '[aria-label*="播放全部"]',
        '[aria-label*="全部播放"]'
      ];

      const candidates = Array.from(document.querySelectorAll(selectors.join(',')));
      const button = candidates.find(el => {
        const text = norm(el.title || el.textContent || el.getAttribute('aria-label') || '');
        return text.includes('播放全部') || text.includes('全部播放') || text.includes('播放歌手热门歌曲') || (text.includes('播放') && text.includes('全部'));
      });

      if (!button) {
        return JSON.stringify({ ok: false, stage: 'play_all_not_found', count: candidates.length });
      }

      button.scrollIntoView({ block: 'center' });
      button.click();

      return JSON.stringify({
        ok: true,
        action: 'play_all_clicked',
        label: norm(button.title || button.textContent || button.getAttribute('aria-label') || '')
      });
    })()
  `;
}

async function openArtistPage(session, keyword) {
  const query = String(keyword || '').trim();
  if (!query) throw new Error('Artist keyword is required');

  const searchUrl = `https://y.qq.com/n/ryqq/search?w=${encodeURIComponent(query)}&t=singer`;
  await session.send('Page.navigate', { url: searchUrl });
  await sleep(800);

  const result = await waitForEvalResult(
    session,
    () => buildArtistSearchEval(query),
    { timeoutMs: 15000, intervalMs: 400, label: `search artist ${query}` }
  );

  if (!result.href) {
    throw new Error(`Artist link not found for ${query}`);
  }

  await session.send('Page.navigate', { url: result.href });
  await sleep(1000);
  return result;
}

async function actionSearch(keyword, type = 'song') {
  await withBrowse(async session => {
    const typeMap = { song: 'song', album: 'album' };
    const t = typeMap[type] || 'song';
    const url = `https://y.qq.com/n/ryqq/search?w=${encodeURIComponent(String(keyword || '').trim())}&t=${t}`;
    await session.send('Page.navigate', { url });
    await sleep(PAGE_WAIT_MS);

    if (type === 'album') {
      const playAll = await session.evaluate(buildPlayAllEval());
      const parsedPlayAll = JSON.parse(playAll);
      if (parsedPlayAll.ok) {
        output({ ok: true, scope: 'album', ...parsedPlayAll });
        return;
      }

      const result = await session.evaluate(`
        (function() {
          const items = Array.from(document.querySelectorAll('.songlist__item'));
          if (!items.length) return JSON.stringify({ ok: false, msg: 'No results' });
          const item = items[0];
          const nameEl = item.querySelector('.songlist__songname_txt a[title]');
          const artistEl = item.querySelector('.songlist__artist a');
          const playBtn = item.querySelector('.list_menu__play');
          if (playBtn) playBtn.click(); else item.dispatchEvent(new MouseEvent('dblclick', { bubbles: true, cancelable: true }));
          return JSON.stringify({ ok: true, song: nameEl ? String(nameEl.title || '').trim() : '', artist: artistEl ? String(artistEl.title || '').trim() : '', fallback: 'first_song' });
        })()
      `);
      output(JSON.parse(result));
      return;
    }

    const result = await session.evaluate(songQueryJS(keyword));
    output(JSON.parse(result));
  });
}

async function actionSearchArtist(keyword) {
  await withBrowse(async session => {
    const artist = await openArtistPage(session, keyword);
    output({
      ok: true,
      action: 'opened_artist_page',
      artist: artist.name,
      href: artist.href,
      count: artist.count,
    });
  });
}

async function actionPlayArtistAllSongs(keyword) {
  await withBrowse(async session => {
    const artist = await openArtistPage(session, keyword);
    const result = await waitForEvalResult(
      session,
      buildPlayAllEval,
      { timeoutMs: 15000, intervalMs: 450, label: `play all songs for ${artist.name || String(keyword || '').trim()}` }
    );

    output({
      ok: true,
      action: 'play_artist_all_songs',
      artist: artist.name,
      href: artist.href,
      ...result,
    });
  });
}


async function actionPlayLiked(random = false) {
  await withBrowse(async session => {
    await session.send('Page.navigate', { url: 'https://y.qq.com/n/ryqq_v2/profile/like/song' });
    await sleep(PAGE_WAIT_MS);
    if (random) {
      const result = await session.evaluate(firstVisibleSongJS());
      output(JSON.parse(result));
    } else {
      // Click "播放全部" to queue all liked songs
      const playAllResult = await session.evaluate(buildPlayAllEval());
      const parsed = JSON.parse(playAllResult);
      if (parsed.ok) {
        output({ ok: true, action: 'play_all_liked', ...parsed });
      } else {
        // Fallback: play first song
        const result = await session.evaluate(`
          (function() {
            const items = Array.from(document.querySelectorAll('.songlist__item'));
            if (!items.length) return JSON.stringify({ ok: false, msg: 'No liked songs found' });
            const item = items[0];
            const nameEl = item.querySelector('.songlist__songname_txt a[title]');
            const artistEl = item.querySelector('.songlist__artist a');
            const playBtn = item.querySelector('.list_menu__play');
            if (playBtn) playBtn.click(); else item.dispatchEvent(new MouseEvent('dblclick', { bubbles: true, cancelable: true }));
            return JSON.stringify({ ok: true, song: nameEl ? String(nameEl.title || '').trim() : '', artist: artistEl ? String(artistEl.title || '').trim() : '', index: 0, total: items.length });
          })()
        `);
        output(JSON.parse(result));
      }
    }
  });
}

async function actionPlayPlaylist(playlistId) {
  await withBrowse(async session => {
    await session.send('Page.navigate', { url: `https://y.qq.com/n/ryqq/playlist/${encodeURIComponent(String(playlistId || '').trim())}` });
    await sleep(PAGE_WAIT_MS);
    const result = await session.evaluate(playlistPlayJS());
    output(JSON.parse(result));
  });
}

async function actionLike() {
  await withPlayer(async session => {
    const result = await session.evaluate(`
      (function() {
        const btn = document.querySelector('.btn_big_like');
        if (!btn) return JSON.stringify({ ok: false, msg: 'Like button not found' });
        const wasLiked = btn.classList.contains('btn_big_like--like');
        if (wasLiked) return JSON.stringify({ ok: true, action: 'already_liked', liked: true });
        btn.click();
        return JSON.stringify({ ok: true, action: 'liked', liked: true });
      })()
    `);
    output(JSON.parse(result));
  });
}

async function actionUnlike() {
  await withPlayer(async session => {
    const result = await session.evaluate(`
      (function() {
        const btn = document.querySelector('.btn_big_like');
        if (!btn) return JSON.stringify({ ok: false, msg: 'Like button not found' });
        const wasLiked = btn.classList.contains('btn_big_like--like');
        if (!wasLiked) return JSON.stringify({ ok: true, action: 'already_unliked', liked: false });
        btn.click();
        return JSON.stringify({ ok: true, action: 'unliked', liked: false });
      })()
    `);
    output(JSON.parse(result));
  });
}

async function actionListPlaylists() {
  await withBrowse(async session => {
    await session.send('Page.navigate', { url: 'https://y.qq.com/n/ryqq_v2/profile/create' });
    await sleep(PAGE_WAIT_MS);
    const result = await waitForEvalResult(
      session,
      () => `
        (function() {
          const items = Array.from(document.querySelectorAll('.playlist__item'));
          if (!items.length) return JSON.stringify({ ok: false, msg: 'No playlists found' });
          const playlists = items.map(item => {
            const titleEl = item.querySelector('.playlist__title');
            const numberEl = item.querySelector('.playlist__number');
            const linkEl = item.querySelector('a[href*="playlist"]');
            const href = linkEl ? String(linkEl.href || '') : '';
            const parts = href.split('/');
            const id = parts[parts.length - 1] || '';
            return {
              name: titleEl ? titleEl.textContent.trim() : '',
              count: numberEl ? numberEl.textContent.trim() : '',
              id: id,
            };
          });
          return JSON.stringify({ ok: true, playlists });
        })()
      `,
      { timeoutMs: 15000, intervalMs: 500, label: 'list playlists' }
    );
    output(result);
  });
}

async function actionCreatePlaylist(name) {
  const playlistName = String(name || '').trim();
  if (!playlistName) throw new Error('Playlist name is required');
  await withBrowse(async session => {
    await session.send('Page.navigate', { url: 'https://y.qq.com/n/ryqq_v2/profile/create' });
    await sleep(PAGE_WAIT_MS);

    // Click "新建歌单" button
    await session.evaluate(`
      (function() {
        const btn = document.querySelector('.js_create_new');
        if (btn) btn.click();
      })()
    `);
    await sleep(1000);

    // Fill in name and confirm
    const nameEscaped = JSON.stringify(playlistName);
    const result = await session.evaluate(`
      (function() {
        const input = document.querySelector('#new_playlist');
        if (!input) return JSON.stringify({ ok: false, msg: 'Create dialog not found' });
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(input, ${nameEscaped});
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        const confirmBtn = document.querySelector('.popup__ft .mod_btn_green');
        if (!confirmBtn) return JSON.stringify({ ok: false, msg: 'Confirm button not found' });
        confirmBtn.click();
        return JSON.stringify({ ok: true, action: 'created', name: ${nameEscaped} });
      })()
    `);
    output(JSON.parse(result));
  });
}

async function addToPlaylistAttempt(playerTarget, want) {
  const session = await pageSession(playerTarget);
  try {
    // Click add button on the currently playing song
    const raw = await session.evaluate(`
      (function() {
        const playing = document.querySelector('.songlist__item--playing');
        if (!playing) return JSON.stringify({ ok: false, msg: 'No song playing' });
        const addBtn = playing.querySelector('.list_menu__add');
        if (addBtn) addBtn.click();
        return JSON.stringify({ ok: true, clicked: !!addBtn });
      })()
    `);
    const clickResult = JSON.parse(raw);
    if (!clickResult.ok) return clickResult;
  } finally {
    session.close();
  }

  await sleep(1000);

  const session2 = await pageSession(playerTarget);
  try {
    const raw2 = await session2.evaluate(`
      (function() {
        const want = ${JSON.stringify(want)};
        const menu = document.querySelector('.mod_operate_menu');
        if (!menu) return JSON.stringify({ ok: false, msg: 'Add-to-playlist menu not found' });
        const items = Array.from(menu.querySelectorAll('.operate_menu__item .operate_menu__link'));
        const match = items.find(a => a.textContent.trim().toLowerCase() === want);
        if (!match) {
          const available = items.map(a => a.textContent.trim());
          return JSON.stringify({ ok: false, msg: 'Playlist not found', available });
        }
        match.click();
        return JSON.stringify({ ok: true, action: 'added', playlist: match.textContent.trim() });
      })()
    `);
    return JSON.parse(raw2);
  } finally {
    session2.close();
  }
}

async function actionAddToPlaylist(playlistName) {
  const want = String(playlistName || '').trim().toLowerCase();
  if (!want) throw new Error('Playlist name is required');

  const entry = await discoverEndpoint();
  const playerTarget = firstTarget(pageTargets(entry), isPlayerTarget);
  if (!playerTarget) return output({ error: 'Player not found. Play a song first.' });

  let result = await addToPlaylistAttempt(playerTarget, want);

  // If playlist not found, reload player to refresh playlist cache and retry
  if (!result.ok && result.msg === 'Playlist not found') {
    const reloadSession = await pageSession(playerTarget);
    try {
      await reloadSession.evaluate('location.reload()');
    } finally {
      reloadSession.close();
    }
    await sleep(PAGE_WAIT_MS);
    result = await addToPlaylistAttempt(playerTarget, want);
  }

  output(result);
}

async function actionScreenshot(pathArg) {
  const entry = await discoverEndpoint();
  const target = firstTarget(pageTargets(entry), isPlayerTarget) || firstTarget(pageTargets(entry), isBrowseTarget);
  if (!target) return output({ error: 'No QQ Music tab found.' });
  if (!isAllowedDomain(target.url)) return output({ error: `Refusing to screenshot non-QQ-Music tab: ${target.url}` });
  const session = await pageSession(target);
  try {
    await sleep(1000);
    const result = await session.send('Page.captureScreenshot', { format: 'png' });
    const outPath = pathArg || SCREENSHOT_PATH;
    const buf = Buffer.from(result.data, 'base64');
    fs.writeFileSync(outPath, buf);
    output({ ok: true, path: outPath, bytes: buf.length });
  } finally {
    session.close();
  }
}

const PLAY_MODES = {
  'list':   { class: 'btn_big_style_list',   label: '列表循环' },
  'single': { class: 'btn_big_style_single', label: '单曲循环' },
  'random': { class: 'btn_big_style_random', label: '随机播放' },
  'order':  { class: 'btn_big_style_order',  label: '顺序循环' },
};

const MODE_CYCLE = ['list', 'single', 'random', 'order'];

function detectCurrentMode(className) {
  for (const [key, val] of Object.entries(PLAY_MODES)) {
    if (className.includes(val.class)) return key;
  }
  return null;
}

async function actionMode(targetMode) {
  await withPlayer(async session => {
    if (targetMode && !PLAY_MODES[targetMode]) {
      return output({ ok: false, msg: `Unknown mode: ${targetMode}. Valid: ${Object.keys(PLAY_MODES).join(', ')}` });
    }

    const current = await session.evaluate(`
      (() => {
        const el = document.querySelector('[class*=btn_big_style]');
        if (!el) return JSON.stringify({ error: 'Mode button not found' });
        return JSON.stringify({ className: el.className, title: el.title });
      })()
    `);
    const info = JSON.parse(current);
    if (info.error) return output({ ok: false, msg: info.error });

    const currentMode = detectCurrentMode(info.className);

    if (!targetMode) {
      return output({ ok: true, mode: currentMode, label: PLAY_MODES[currentMode]?.label || info.title });
    }

    if (currentMode === targetMode) {
      return output({ ok: true, mode: currentMode, label: PLAY_MODES[currentMode].label, action: 'already_set' });
    }

    const maxClicks = MODE_CYCLE.length;
    for (let i = 0; i < maxClicks; i++) {
      const result = await session.evaluate(`
        (() => {
          const el = document.querySelector('[class*=btn_big_style]');
          if (!el) return JSON.stringify({ error: 'Mode button not found' });
          el.click();
          return new Promise(r => setTimeout(() => {
            r(JSON.stringify({ className: el.className, title: el.title }));
          }, 500));
        })()
      `);
      const after = JSON.parse(result);
      if (after.error) return output({ ok: false, msg: after.error });
      const newMode = detectCurrentMode(after.className);
      if (newMode === targetMode) {
        return output({ ok: true, mode: newMode, label: PLAY_MODES[newMode].label, action: 'switched', clicks: i + 1 });
      }
    }

    return output({ ok: false, msg: `Failed to switch to ${targetMode} after ${maxClicks} clicks` });
  });
}

async function actionDoctor() {
  const diag = {
    cdpPortFile: CDP_PORT_FILE,
    cdpPortFileExists: fs.existsSync(CDP_PORT_FILE),
    cdpPortFileValue: null,
    resolvedPort: CDP_PORT,
    host: CDP_HOST,
    endpoint: null,
    browser: null,
    qqMusicTabs: [],
    playerTab: false,
    browseTab: false,
    status: 'unknown',
  };

  if (diag.cdpPortFileExists) {
    diag.cdpPortFileValue = fs.readFileSync(CDP_PORT_FILE, 'utf8').trim();
  }

  try {
    const entry = await discoverEndpoint();
    diag.endpoint = entry.baseUrl;
    diag.browser = entry.version.Browser || entry.version['Browser'] || '';
    const pages = pageTargets(entry);
    diag.qqMusicTabs = pages.filter(isQQMusicTarget).map(t => ({ title: t.title, url: t.url }));
    diag.playerTab = pages.some(isPlayerTarget);
    diag.browseTab = pages.some(isBrowseTarget);
    diag.status = diag.qqMusicTabs.length > 0 ? 'ready' : 'connected_no_qq_music_tabs';
  } catch (err) {
    diag.status = 'no_endpoint';
    diag.error = err.message;
  }

  output(diag);
}

function printHelp() {
  output({
    usage: 'node qq-music-ctl.js <action> [args...]',
    actions: ['play','pause','toggle','next','prev','status','mode [list|single|random|order]','search <keyword>','search-artist <artist>','play-artist-all-songs <artist>','search-album <album>','play-liked','play-liked-random','play-playlist <id>','like','unlike','list-playlists','create-playlist <name>','add-to-playlist <name>','screenshot [path]','tabs','init','doctor'],
  });
}

async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  if (!action || action === '--help' || action === '-h') {
    return printHelp();
  }

  switch (action) {
    case 'play': return actionPlay();
    case 'pause': return actionPause();
    case 'toggle': return actionToggle();
    case 'next': return actionNext();
    case 'prev': return actionPrev();
    case 'status': return actionStatus();
    case 'search': return actionSearch(args.join(' '), 'song');
    case 'search-artist': return actionSearchArtist(args.join(' '));
    case 'play-artist-all-songs': return actionPlayArtistAllSongs(args.join(' '));
    case 'search-album': return actionSearch(args.join(' '), 'album');
    case 'play-liked': return actionPlayLiked(false);
    case 'play-liked-random': return actionPlayLiked(true);
    case 'play-playlist': return actionPlayPlaylist(args[0]);
    case 'mode': return actionMode(args[0] || '');
    case 'like': return actionLike();
    case 'unlike': return actionUnlike();
    case 'list-playlists': return actionListPlaylists();
    case 'create-playlist': return actionCreatePlaylist(args.join(' '));
    case 'add-to-playlist': return actionAddToPlaylist(args.join(' '));
    case 'screenshot': return actionScreenshot(args[0]);
    case 'tabs': return actionTabs();
    case 'init': return actionInit();
    case 'doctor': return actionDoctor();
    default:
      return printHelp();
  }
}

main().catch(err => {
  output({ error: err.message || String(err) });
  process.exit(1);
});
