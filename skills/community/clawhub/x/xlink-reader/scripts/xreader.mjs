#!/usr/bin/env node
import fs from 'fs';
import os from 'os';
import path from 'path';
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);
const HOME = os.homedir();
const NEW_AUTH_PATH = path.join(HOME, '.config', 'xreader', 'session.json');
const LEGACY_AUTH_PATH = path.join(HOME, '.config', 'xfetch', 'session.json');

function printHelp() {
  console.log(`x-reader

Usage:
  node skills/x-reader/scripts/xreader.mjs [--mode summary|full] [--thread] [--debug] <x-url>

Options:
  --mode <mode>   summary (default) or full
  --thread        read full thread via xreach (explicit only)
  --debug         launch Playwright headed for article extraction
  --help          show help
`);
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function safeReadJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return null;
  }
}

function saveJsonPrivate(filePath, obj) {
  ensureDir(filePath);
  fs.writeFileSync(filePath, JSON.stringify(obj, null, 2), { mode: 0o600 });
  try { fs.chmodSync(filePath, 0o600); } catch {}
}

function loadAuth() {
  const primary = safeReadJson(NEW_AUTH_PATH);
  if (primary?.authToken && primary?.ct0) {
    return { ...primary, path: NEW_AUTH_PATH, migrated: false };
  }

  const legacy = safeReadJson(LEGACY_AUTH_PATH);
  if (legacy?.authToken && legacy?.ct0) {
    const migrated = {
      authToken: legacy.authToken,
      ct0: legacy.ct0,
      migratedFrom: LEGACY_AUTH_PATH,
      migratedAt: new Date().toISOString(),
    };
    saveJsonPrivate(NEW_AUTH_PATH, migrated);
    return { ...migrated, path: NEW_AUTH_PATH, migrated: true };
  }

  return null;
}

async function runXreach(args) {
  const { stdout } = await execFileAsync('xreach', args, { maxBuffer: 20 * 1024 * 1024 });
  return JSON.parse(stdout);
}

async function resolveUrl(inputUrl) {
  const res = await fetch(inputUrl, {
    method: 'GET',
    redirect: 'follow',
    headers: { 'user-agent': 'Mozilla/5.0 x-reader/1.0' },
  });
  return res.url || inputUrl;
}

function parseArgs(argv) {
  let mode = 'summary';
  let debug = false;
  let thread = false;
  let url = null;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else if (arg === '--debug') {
      debug = true;
    } else if (arg === '--thread') {
      thread = true;
    } else if (arg === '--mode') {
      mode = argv[++i] || 'summary';
    } else if (!url) {
      url = arg;
    }
  }

  if (!url) {
    printHelp();
    process.exit(1);
  }

  return { mode, debug, thread, url };
}

function pickSummaryText(text, mode) {
  if (!text) return '';
  const clean = text.replace(/\s+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  if (mode === 'full') return clean;
  return clean.slice(0, 2200);
}

function normalizeTweet(data, requestedUrl, canonicalUrl, mode) {
  const text = data.full_text || data.text || '';
  return {
    ok: true,
    type: 'tweet',
    url: requestedUrl,
    canonicalUrl,
    source: 'xreach',
    author: {
      name: data.user?.name || null,
      screenName: data.user?.screenName || null,
      restId: data.user?.restId || null,
    },
    publishedAt: data.createdAt || null,
    title: null,
    text,
    contentText: mode === 'full' ? text : null,
    contentMarkdown: null,
    summaryText: pickSummaryText(text, mode),
    stats: {
      replies: data.replyCount ?? null,
      retweets: data.retweetCount ?? null,
      likes: data.likeCount ?? null,
      quotes: data.quoteCount ?? null,
      views: data.viewCount ?? null,
      bookmarks: data.bookmarkCount ?? null,
    },
    fallback: false,
    warnings: [],
  };
}

function normalizeThread(items, requestedUrl, canonicalUrl, mode) {
  const normalizedItems = (Array.isArray(items) ? items : []).map((item) => ({
    id: item.id || null,
    publishedAt: item.createdAt || null,
    conversationId: item.conversationId || null,
    inReplyToTweetId: item.inReplyToTweetId || null,
    text: item.full_text || item.text || '',
    author: {
      name: item.user?.name || null,
      screenName: item.user?.screenName || null,
      restId: item.user?.restId || null,
    },
    stats: {
      replies: item.replyCount ?? null,
      retweets: item.retweetCount ?? null,
      likes: item.likeCount ?? null,
      quotes: item.quoteCount ?? null,
      views: item.viewCount ?? null,
      bookmarks: item.bookmarkCount ?? null,
    },
  }));

  const root = normalizedItems[0] || null;
  const rootAuthorId = root?.author?.restId || null;
  const rootAuthorHandle = root?.author?.screenName || null;
  let filtered = normalizedItems;
  const warnings = [];

  if (rootAuthorId || rootAuthorHandle) {
    filtered = normalizedItems.filter((item) => {
      if (rootAuthorId && item.author?.restId) return item.author.restId === rootAuthorId;
      if (rootAuthorHandle && item.author?.screenName) return item.author.screenName === rootAuthorHandle;
      return false;
    });
  }

  if (filtered.length === 0) filtered = normalizedItems;
  if (filtered.length < normalizedItems.length) warnings.push('non_author_replies_filtered');

  const rootId = root?.id || null;
  const rootConversationId = root?.conversationId || rootId || null;
  const isLikelyReplyByAuthor = (item) => {
    if (!item?.text) return false;
    if (!/^@\w+/.test(item.text.trim())) return false;
    if (rootId && item.id === rootId) return false;
    if (item.conversationId && rootConversationId && item.conversationId !== rootConversationId) return true;
    if (item.inReplyToTweetId && rootId && item.inReplyToTweetId !== rootId) return true;
    return true;
  };
  const beforeReplyFilter = filtered.length;
  filtered = filtered.filter((item) => !isLikelyReplyByAuthor(item));
  if (filtered.length === 0) filtered = normalizedItems;
  if (filtered.length < beforeReplyFilter) warnings.push('author_reply_noise_filtered');

  const ts = (value) => {
    const n = Date.parse(value || '');
    return Number.isNaN(n) ? 0 : n;
  };
  filtered = filtered.sort((a, b) => ts(a.publishedAt) - ts(b.publishedAt));

  if (rootId && filtered.some((item) => item.id === rootId)) {
    const rootIndex = filtered.findIndex((item) => item.id === rootId);
    filtered = filtered.slice(rootIndex);
  }

  const joined = filtered.map((item) => item.text).filter(Boolean).join('\n\n---\n\n');
  return {
    ok: true,
    type: 'thread',
    url: requestedUrl,
    canonicalUrl,
    source: 'xreach',
    author: filtered[0]?.author || root?.author || { name: null, screenName: null, restId: null },
    publishedAt: filtered[0]?.publishedAt || root?.publishedAt || null,
    title: null,
    text: mode === 'full' ? joined : null,
    contentText: mode === 'full' ? joined : null,
    contentMarkdown: null,
    summaryText: pickSummaryText(joined, mode),
    items: mode === 'full'
      ? filtered
      : filtered.map(({ id, publishedAt, text, author }) => ({ id, publishedAt, text, author })),
    itemCount: filtered.length,
    fallback: false,
    warnings,
  };
}

async function extractArticleWithPlaywright(articleUrl, auth, mode, debug) {
  let chromium;
  try {
    ({ chromium } = await import('playwright'));
  } catch {
    return {
      ok: false,
      type: 'article',
      source: 'playwright',
      error: 'playwright_not_installed',
      message: 'Install Playwright in the x-reader skill directory before reading X article pages.',
    };
  }

  const browser = await chromium.launch({ headless: !debug });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    locale: 'en-US',
  });

  await context.addCookies([
    {
      name: 'auth_token',
      value: auth.authToken,
      domain: '.x.com',
      path: '/',
      httpOnly: true,
      secure: true,
      sameSite: 'Lax',
    },
    {
      name: 'ct0',
      value: auth.ct0,
      domain: '.x.com',
      path: '/',
      httpOnly: false,
      secure: true,
      sameSite: 'Lax',
    },
  ]);

  const page = await context.newPage();
  const warnings = [];
  try {
    await page.goto(articleUrl, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1500);

    const result = await page.evaluate(() => {
      const textOf = (el) => (el?.innerText || el?.textContent || '').trim();
      const normalize = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/\n{3,}/g, '\n\n').replace(/[ \t]+\n/g, '\n').trim();
      const badPatterns = [
        /^show more$/i,
        /^show less$/i,
        /^copy link$/i,
        /^share$/i,
        /^follow$/i,
        /^subscribe$/i,
        /^advertisement$/i,
        /^sign up$/i,
        /^log in$/i,
        /^view keyboard shortcuts/i,
        /^to view keyboard shortcuts/i,
        /^what’s happening$/i,
        /^what's happening$/i,
        /^trending$/i,
        /^for you$/i,
        /^messages$/i,
        /^notifications$/i,
        /^home$/i,
        /^premium$/i,
        /^grok$/i,
      ];
      const scoreNode = (node) => {
        if (!node) return -1;
        const text = normalize(textOf(node));
        if (text.length < 200) return -1;
        const pCount = node.querySelectorAll('p').length;
        const headingCount = node.querySelectorAll('h1,h2,h3').length;
        const codeCount = node.querySelectorAll('pre,code').length;
        const articleHints = [node.matches?.('article') ? 1 : 0, node.querySelector('article') ? 1 : 0].reduce((a, b) => a + b, 0);
        return text.length + pCount * 120 + headingCount * 80 + codeCount * 40 + articleHints * 300;
      };
      const isUsefulBlock = (text) => {
        const t = normalize(text);
        if (!t) return false;
        if (t.length < 30) return false;
        if (badPatterns.some((re) => re.test(t))) return false;
        if (/^https?:\/\//i.test(t) && t.length < 120) return false;
        if (/^[@#][\w\u4e00-\u9fff]/.test(t) && t.length < 80) return false;
        if (/公众号|wechat/i.test(t) && t.length < 120 && !/```|↓|http|https/.test(t)) return false;
        if (/前字节|万人社群|欢迎互粉|进几百人免费/i.test(t)) return false;
        return true;
      };
      const dedupe = (items) => {
        const seen = new Set();
        const out = [];
        for (const item of items) {
          const key = normalize(item)
            .replace(/^```[\s\S]*?\n/, '```\n')
            .replace(/\n```$/, '\n```')
            .replace(/^##\s+/, '')
            .replace(/^-\s+/, '')
            .replace(/^>\s+/, '');
          if (!key || seen.has(key)) continue;
          seen.add(key);
          out.push(normalize(item));
        }
        return out;
      };

      const candidates = [
        ...Array.from(document.querySelectorAll('article, main, section, div')),
      ];
      let root = document.body;
      let bestScore = -1;
      for (const node of candidates) {
        const score = scoreNode(node);
        if (score > bestScore) {
          bestScore = score;
          root = node;
        }
      }

      const title =
        normalize(textOf(document.querySelector('h1'))) ||
        document.querySelector('meta[property="og:title"]')?.getAttribute('content') ||
        document.title ||
        null;

      const authorMeta = document.querySelector('meta[name="author"]')?.getAttribute('content') || null;
      const timeEl = document.querySelector('time');
      const publishedAt = timeEl?.getAttribute('datetime') || null;

      const blockSelector = 'h1,h2,h3,h4,p,pre,blockquote,li,div[dir="auto"],section div';
      const rawBlocks = Array.from(root.querySelectorAll(blockSelector)).map((el) => {
        const text = normalize(textOf(el));
        const tag = (el.tagName || '').toLowerCase();
        return { text, tag };
      });

      const filtered = dedupe(rawBlocks.filter((b) => {
        if (!isUsefulBlock(b.text)) return false;
        if (/^(markdown|javascript|typescript|json|bash|shell)$/i.test(b.text)) return false;
        return true;
      }).map((b) => {
        if (b.tag === 'pre') return '```\n' + b.text + '\n```';
        if (/^h[1-4]$/.test(b.tag)) return '## ' + b.text;
        if (b.tag === 'li') return '- ' + b.text;
        if (b.tag === 'blockquote') return '> ' + b.text;
        return b.text;
      }));

      const compacted = [];
      for (const block of filtered) {
        const prev = compacted[compacted.length - 1] || '';
        const base = block.replace(/^## /, '').replace(/^- /, '').replace(/^> /, '').trim();
        const prevBase = prev.replace(/^## /, '').replace(/^- /, '').replace(/^> /, '').trim();
        if (base && prevBase && (base === prevBase || base.includes(prevBase) || prevBase.includes(base))) continue;
        compacted.push(block);
      }

      const classifyBlock = (block) => {
        const plain = block.replace(/^## /, '').replace(/^- /, '').replace(/^> /, '').trim();
        const isCode = /^```[\s\S]*```$/.test(block);
        const hasQuestion = /[？?]/.test(plain);
        const hasDefinition = /(是指|是什么|区别|趋势|策略|方法|步骤|关键|建议|总结|结论|原因|目标)/.test(plain);
        const hasExampleSignals = /(User-agent:|schema\.org|FAQPage|acceptedAnswer|git clone|npm install|clawhub install|https?:\/\/)/i.test(plain);
        const looksTemplate = /\bURL\b|产品\/服务A|产品\/服务B|核心教程|案例研究/.test(plain);
        const looksAuthorCard = /^(follow|关注)$/i.test(plain) || /@\w+/.test(plain) || /(AI创业者|知识付费|个人视角|AI视频合伙人|公众号|wechat)/i.test(plain);
        return {
          block,
          plain,
          isCode,
          hasQuestion,
          hasDefinition,
          hasExampleSignals,
          looksTemplate,
          looksAuthorCard,
          score:
            (hasDefinition ? 5 : 0) +
            (hasQuestion ? 3 : 0) +
            (!isCode ? 2 : 0) +
            (hasExampleSignals ? -3 : 0) +
            (looksTemplate ? -4 : 0) +
            (looksAuthorCard ? -6 : 0) +
            Math.min(Math.floor(plain.length / 120), 3),
        };
      };

      const ranked = compacted.map(classifyBlock);
      const bestSummaryBlocks = ranked
        .filter((x) => x.plain.length >= 40)
        .filter((x) => !x.looksAuthorCard)
        .filter((x) => !(x.isCode && x.hasExampleSignals))
        .sort((a, b) => b.score - a.score)
        .slice(0, 12)
        .sort((a, b) => compacted.indexOf(a.block) - compacted.indexOf(b.block))
        .map((x) => x.block);

      const summaryBlocks = bestSummaryBlocks.length ? bestSummaryBlocks : compacted.slice(0, 12);
      const contentText = normalize(compacted.map((x) => x.replace(/^## /, '').replace(/^- /, '').replace(/^> /, '').replace(/^```\n([\s\S]*?)\n```$/, '$1')).join('\n\n')) || normalize(textOf(root));
      const contentMarkdown = normalize(compacted.join('\n\n'));
      const summaryText = normalize(summaryBlocks.map((x) => x.replace(/^## /, '').replace(/^- /, '').replace(/^> /, '').replace(/^```\n([\s\S]*?)\n```$/, '$1')).join('\n\n'));

      return {
        title: normalize(title),
        author: authorMeta,
        publishedAt,
        contentText,
        contentMarkdown,
        summaryText,
      };

    });

    if (!result.contentText || result.contentText.length < 120) {
      warnings.push('article_content_short');
    }

    return {
      ok: true,
      type: 'article',
      url: articleUrl,
      canonicalUrl: page.url(),
      source: 'playwright',
      extractionMode: 'dom',
      author: {
        name: result.author,
        screenName: null,
      },
      publishedAt: result.publishedAt,
      title: result.title,
      text: null,
      contentText: mode === 'full' ? result.contentText : null,
      contentMarkdown: mode === 'full' ? result.contentMarkdown : null,
      summaryText: mode === 'full' ? pickSummaryText(result.contentText, mode) : pickSummaryText(result.summaryText || result.contentText, 'summary'),
      fallback: false,
      warnings,
    };
  } finally {
    await page.close().catch(() => {});
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
  }
}

async function main() {
  const { mode, debug, thread, url } = parseArgs(process.argv.slice(2));
  const auth = loadAuth();
  if (!auth) {
    console.log(JSON.stringify({
      ok: false,
      error: 'auth_missing',
      message: `Missing auth file. Expected ${NEW_AUTH_PATH} (legacy fallback: ${LEGACY_AUTH_PATH}).`,
    }, null, 2));
    process.exit(2);
  }

  let canonicalUrl = url;
  let resolvedToArticle = false;
  if (/^https?:\/\/t\.co\//i.test(url)) {
    canonicalUrl = await resolveUrl(url);
    resolvedToArticle = /x\.com\/i\/article\//i.test(canonicalUrl);
  }

  if (/x\.com\/i\/article\//i.test(canonicalUrl)) {
    const article = await extractArticleWithPlaywright(canonicalUrl, auth, mode, debug);
    console.log(JSON.stringify(article, null, 2));
    return;
  }

  try {
    if (thread) {
      const threadData = await runXreach(['thread', canonicalUrl, '--json']);
      const out = normalizeThread(threadData?.items || threadData, url, canonicalUrl, mode);
      console.log(JSON.stringify(out, null, 2));
      return;
    }

    const tweet = await runXreach(['tweet', canonicalUrl, '--json']);
    let articleUrl = null;
    const tweetText = tweet.full_text || tweet.text || '';
    if (/^https?:\/\/t\.co\//i.test(tweetText.trim())) {
      try {
        const maybe = await resolveUrl(tweetText.trim());
        if (/x\.com\/i\/article\//i.test(maybe)) articleUrl = maybe;
      } catch {}
    }

    if (articleUrl) {
      const article = await extractArticleWithPlaywright(articleUrl, auth, mode, debug);
      if (article.ok) {
        article.requestedUrl = url;
        article.tweet = normalizeTweet(tweet, url, canonicalUrl, 'summary');
        console.log(JSON.stringify(article, null, 2));
        return;
      }

      const fallback = normalizeTweet(tweet, url, canonicalUrl, mode);
      fallback.fallback = true;
      fallback.warnings.push('article_extraction_failed');
      fallback.articleUrl = articleUrl;
      fallback.articleError = article;
      console.log(JSON.stringify(fallback, null, 2));
      return;
    }

    const out = normalizeTweet(tweet, url, canonicalUrl, mode);
    if (resolvedToArticle) out.warnings.push('resolved_url_changed');
    console.log(JSON.stringify(out, null, 2));
  } catch (error) {
    console.log(JSON.stringify({
      ok: false,
      error: 'xread_failed',
      message: error?.message || String(error),
      url,
      canonicalUrl,
    }, null, 2));
    process.exit(1);
  }
}

main();
