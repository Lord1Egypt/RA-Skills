#!/usr/bin/env node
import { realpathSync } from 'node:fs';
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { execFile, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import { sanitizeFileName } from './utils.mjs';
import { getNotebookBooks, getBookmarks, getReviews } from './api.mjs';
import { getGatewayNotebookBooks, getGatewayBookmarks, getGatewayReviews } from './gateway.mjs';
import { buildBookmarkEntries, buildReviewEntries, comparableBookmarkEntry, comparableReviewEntry, collectBookmarkIds, collectReviewIds } from './entries.mjs';
import { buildMarkdownFromApi, writeBook } from './render.mjs';
import { extractComparableMapsFromMarkdown, extractIds } from './markdown-parser.mjs';
import { computeMergeStats } from './merge.mjs';
import { loadState, saveState } from './state.mjs';
import { runWithApiSessionRetry } from './session.mjs';
import { normalizeCookieSource } from './browser-mode.mjs';
import {
  WereadGatewayAuthError,
  WereadGatewayMissingKeyError,
  WereadGatewayUnavailableError,
  WereadGatewayUpgradeError,
} from './errors.mjs';

const DEFAULT_OUTPUT = process.env.WEREAD_OUTPUT || path.resolve(process.cwd(), 'out', 'weread');
const DEFAULT_CDP = process.env.WEREAD_CDP_URL || 'http://127.0.0.1:9222';
const DEFAULT_TAGS = (process.env.WEREAD_TAGS || 'reading,weread').split(',').map((x) => x.trim()).filter(Boolean);
const DEFAULT_API_BACKEND = process.env.WEREAD_API_BACKEND || 'gateway';
const DEFAULT_GATEWAY_SKILL_VERSION = process.env.WEREAD_GATEWAY_SKILL_VERSION || '1.0.3';
const ROOT_DIR = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const execFileAsync = promisify(execFile);
const API_KEY_HELP = '获取 API Key：打开微信读书 App 最新版 -> 我的 -> 右上角设置按钮 -> 微信读书 Skill -> 快速配置第 2 步 -> 获取 API Key';

export function parseArgs(argv) {
  if (argv.includes('--help') || argv.includes('-h')) {
    return { help: true };
  }
  const args = {
    all: false,
    book: null,
    bookId: null,
    author: null,
    output: DEFAULT_OUTPUT,
    cdp: DEFAULT_CDP,
    limit: null,
    force: false,
    tags: DEFAULT_TAGS,
    cookie: process.env.WEREAD_COOKIE || null,
    cookieExplicit: false,
    cookieFrom: 'manual',
    cookieFromExplicit: false,
    mode: process.env.WEREAD_IMPORT_MODE || 'api',
    apiBackend: DEFAULT_API_BACKEND,
    gatewayApiKey: process.env.WEREAD_API_KEY || '',
    gatewaySkillVersion: DEFAULT_GATEWAY_SKILL_VERSION,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--all') args.all = true;
    else if (arg === '--book') args.book = argv[++i] || null;
    else if (arg === '--book-id') args.bookId = argv[++i] || null;
    else if (arg === '--author') args.author = argv[++i] || null;
    else if (arg === '--output') args.output = argv[++i] || DEFAULT_OUTPUT;
    else if (arg === '--cdp') args.cdp = argv[++i] || DEFAULT_CDP;
    else if (arg === '--limit') args.limit = Number(argv[++i] || '0') || null;
    else if (arg === '--force') args.force = true;
    else if (arg === '--tags') args.tags = String(argv[++i] || '').split(',').map((x) => x.trim()).filter(Boolean);
    else if (arg === '--cookie') {
      args.cookie = argv[++i] || null;
      args.cookieExplicit = true;
    }
    else if (arg === '--cookie-from') {
      args.cookieFrom = argv[++i] || 'manual';
      args.cookieFromExplicit = true;
    }
    else if (arg === '--mode') args.mode = argv[++i] || 'api';
    else if (arg === '--api-backend') args.apiBackend = argv[++i] || DEFAULT_API_BACKEND;
    else if (arg === '--no-gateway') args.apiBackend = 'web';
    else if (arg === '--gateway-skill-version') args.gatewaySkillVersion = argv[++i] || DEFAULT_GATEWAY_SKILL_VERSION;
  }
  args.cookieFrom = normalizeCookieSource(args.cookieFrom);
  const apiBackendExplicit = argv.includes('--api-backend') || argv.includes('--no-gateway');
  const legacyBackendRequested = args.cookieFromExplicit || args.cookieExplicit;
  if (!apiBackendExplicit && legacyBackendRequested) {
    args.apiBackend = 'web';
    args.legacyBackendRequested = true;
  } else {
    args.legacyBackendRequested = false;
  }
  args.apiBackend = String(args.apiBackend || 'gateway').toLowerCase();
  if (!['gateway', 'web'].includes(args.apiBackend)) throw new Error('无效的 --api-backend，请使用 gateway 或 web');
  if (!args.all && !args.book && !args.bookId) throw new Error('请指定 --all、--book <标题> 或 --book-id <ID>');
  return args;
}

export function helpText() {
  return `weread-import

默认使用微信读书官方 Gateway 导出划线与想法。

推荐命令：
  bash ./scripts/run.sh --all --output "/path/to/Reading"
  bash ./scripts/run.sh --book "自卑与超越" --output "/path/to/Reading"

Gateway 配置：
  ${API_KEY_HELP}
  export WEREAD_API_KEY=<你的apikey>

缺少 WEREAD_API_KEY 时可选：
  1. 在 App 获取 API Key 并配置后重试：export WEREAD_API_KEY=<你的apikey>
  2. 使用受管浏览器旧链路：追加 --no-gateway --cookie-from browser-managed
  3. 复用已有调试 Chrome：追加 --no-gateway --cookie-from browser-live
  4. 使用手动 Cookie：追加 --no-gateway --cookie '...'

旧链路兼容：
  显式传入 --cookie-from 或 --cookie 时，默认按旧 web 后端执行。
  如需强制 Gateway，可传 --api-backend gateway；此时 cookie 参数会被忽略。

常用参数：
  --all
  --book <title>
  --book-id <id>
  --output <dir>
  --api-backend <gateway|web>
  --no-gateway
  --cookie-from <manual|browser-live|browser-managed>
  --cookie <cookie>
  --force
  --tags <a,b,c>
`;
}

async function importOneBookByApi(book, outputDir, cookie, options = {}) {
  const detailFetchOptions = options.detailFetchJson ? { fetchJson: options.detailFetchJson } : {};
  const loadBookmarks = options.getBookmarks || ((bookId) => getBookmarks(cookie, bookId, detailFetchOptions));
  const loadReviews = options.getReviews || ((bookId) => getReviews(cookie, bookId, detailFetchOptions));
  const bookmarks = await loadBookmarks(book.bookId);
  const reviews = await loadReviews(book.bookId);
  const outputTitle = options.outputTitle || book.title;
  const fileName = `${sanitizeFileName(outputTitle)}.md`;
  const filePath = path.join(outputDir, fileName);
  let existing = '';
  try { existing = await fs.readFile(filePath, 'utf8'); } catch {}
  const prevBookmarkIds = extractIds(existing, 'bookmarkId');
  const prevReviewIds = extractIds(existing, 'reviewId');
  const nextBookmarkIds = collectBookmarkIds(bookmarks);
  const nextReviewIds = collectReviewIds(reviews);

  const previousStatePath = path.join(outputDir, '.weread-import-state.json');
  let previousBookState = null;
  try {
    const previousStateRaw = await fs.readFile(previousStatePath, 'utf8');
    const previousState = JSON.parse(previousStateRaw);
    previousBookState = previousState?.books?.[book.bookId] || null;
  } catch {}

  const nextBookmarkEntryMap = new Map(buildBookmarkEntries(bookmarks).map((entry) => {
    const normalized = comparableBookmarkEntry(entry);
    return [normalized.id, normalized];
  }));
  const nextReviewEntryMap = new Map(buildReviewEntries(reviews).map((entry) => {
    const normalized = comparableReviewEntry(entry);
    return [normalized.id, normalized];
  }));

  const fallbackComparableMaps = existing ? extractComparableMapsFromMarkdown(existing) : { bookmarkEntryMap: {}, reviewEntryMap: {} };
  const prevBookmarkEntryMap = new Map(Object.entries(previousBookState?.bookmarkEntryMap || fallbackComparableMaps.bookmarkEntryMap || {}));
  const prevReviewEntryMap = new Map(Object.entries(previousBookState?.reviewEntryMap || fallbackComparableMaps.reviewEntryMap || {}));

  const markdown = buildMarkdownFromApi(book, bookmarks, reviews, existing, options);
  const writeResult = await writeBook(outputDir, outputTitle, markdown);
  return {
    title: book.title,
    filePath: writeResult.filePath,
    merged: Boolean(existing),
    mergeStats: {
      bookmarks: computeMergeStats(prevBookmarkIds, nextBookmarkIds, prevBookmarkEntryMap, nextBookmarkEntryMap),
      reviews: computeMergeStats(prevReviewIds, nextReviewIds, prevReviewEntryMap, nextReviewEntryMap),
    },
    bookmarkCount: bookmarks.length,
    reviewCount: reviews.length,
    bookmarkIds: nextBookmarkIds,
    reviewIds: nextReviewIds,
    bookmarkEntryMap: Object.fromEntries(nextBookmarkEntryMap),
    reviewEntryMap: Object.fromEntries(nextReviewEntryMap),
    mode: options.backend || 'api',
  };
}

export function assignOutputTitles(books) {
  const baseCounts = new Map();
  for (const book of books) {
    const baseName = sanitizeFileName(book.title);
    baseCounts.set(baseName, (baseCounts.get(baseName) || 0) + 1);
  }

  const usedBaseNames = new Set();
  const outputTitles = new Map();
  books.forEach((book, index) => {
    const baseName = sanitizeFileName(book.title);
    if (baseCounts.get(baseName) === 1 && !usedBaseNames.has(baseName)) {
      usedBaseNames.add(baseName);
      outputTitles.set(book, book.title);
      return;
    }

    const stableId = book.bookId || String(index + 1);
    let outputTitle = `${book.title} (${stableId})`;
    let outputBaseName = sanitizeFileName(outputTitle);
    let suffix = 2;
    while (usedBaseNames.has(outputBaseName)) {
      outputTitle = `${book.title} (${stableId}-${suffix})`;
      outputBaseName = sanitizeFileName(outputTitle);
      suffix += 1;
    }
    usedBaseNames.add(outputBaseName);
    outputTitles.set(book, outputTitle);
  });
  return outputTitles;
}

async function resolveBooksForImport(args, cookie, loaders = {}) {
  const loadNotebookBooks = loaders.getNotebookBooks || (() => getNotebookBooks(cookie));
  if (args.all) {
    const books = await loadNotebookBooks();
    return args.limit ? books.slice(0, args.limit) : books;
  }
  if (args.bookId) {
    return [{ bookId: args.bookId, title: args.book || args.bookId, author: args.author || '', sort: 0 }];
  }
  if (args.book) {
    const books = await loadNotebookBooks();
    const filtered = books.filter((b) => b.title.includes(args.book));
    if (!filtered.length) throw new Error(`笔记本中未找到匹配「${args.book}」的书籍`);
    return args.limit ? filtered.slice(0, args.limit) : filtered;
  }
  throw new Error('无法确定要导入的书籍，请使用 --all、--book 或 --book-id');
}

async function importBooks(args, books, loadBookData, backendLabel, session = {}, sessionManager = null) {
  const state = await loadState(args.output);
  const outputTitles = assignOutputTitles(books);
  sessionManager?.markBasicValidated?.();
  if (books.length && sessionManager?.ensureDetailReady) {
    await sessionManager?.ensureDetailReady(books[0].bookId);
  }
  const results = [];
  let skipped = 0;
  for (const book of books) {
    const prev = state.data.books?.[book.bookId];
    const currentStamp = Number(book.sort || 0);
    const outputTitle = outputTitles.get(book) || book.title;
    const expectedFileName = `${sanitizeFileName(outputTitle)}.md`;
    if (!args.force && prev && Number(prev.lastNoteUpdate || 0) >= currentStamp && prev.fileName === expectedFileName) {
      skipped += 1;
      console.log(`Skipped [${backendLabel}]: ${book.title} (unchanged)`);
      continue;
    }
    const res = await importOneBookByApi(book, args.output, session.cookie, {
      tags: args.tags,
      outputTitle,
      detailFetchJson: session.detailFetchJson,
      getBookmarks: (bookId) => loadBookData.getBookmarks(bookId, session),
      getReviews: (bookId) => loadBookData.getReviews(bookId, session),
      backend: backendLabel,
    });
    const prevBookmarkIds = Array.isArray(prev?.bookmarkIds) ? prev.bookmarkIds : [];
    const prevReviewIds = Array.isArray(prev?.reviewIds) ? prev.reviewIds : [];
    const addedBookmarkIds = res.bookmarkIds.filter((id) => !prevBookmarkIds.includes(id));
    const addedReviewIds = res.reviewIds.filter((id) => !prevReviewIds.includes(id));
    state.data.books[book.bookId] = {
      title: book.title,
      author: book.author || '',
      fileName: path.basename(res.filePath),
      lastNoteUpdate: currentStamp,
      lastImportedAt: new Date().toISOString(),
      bookmarkIds: res.bookmarkIds,
      reviewIds: res.reviewIds,
      bookmarkEntryMap: res.bookmarkEntryMap || {},
      reviewEntryMap: res.reviewEntryMap || {},
      bookmarkCount: res.bookmarkCount,
      reviewCount: res.reviewCount,
      lastDelta: { addedBookmarks: addedBookmarkIds.length, addedReviews: addedReviewIds.length },
      lastMergeStats: res.mergeStats || null,
      mode: backendLabel,
    };
    results.push(res);
    const delta = state.data.books[book.bookId].lastDelta;
    const mergeInfo = res.mergeStats ? `, merge(bookmarks a/u/r/d=${res.mergeStats.bookmarks.added}/${res.mergeStats.bookmarks.updated}/${res.mergeStats.bookmarks.retained}/${res.mergeStats.bookmarks.deleted}; reviews a/u/r/d=${res.mergeStats.reviews.added}/${res.mergeStats.reviews.updated}/${res.mergeStats.reviews.retained}/${res.mergeStats.reviews.deleted})` : '';
    console.log(`Imported [${backendLabel}]: ${res.title} -> ${res.filePath} (${res.merged ? 'merged' : 'new'}, highlights=${res.bookmarkCount}, reviews=${res.reviewCount}, +bookmarks=${delta.addedBookmarks}, +reviews=${delta.addedReviews}${mergeInfo})`);
  }
  await saveState(state);
  console.log(`Done. Imported ${results.length} book(s) by ${backendLabel}. Skipped ${skipped} unchanged book(s).`);
}

async function importViaWeb(args, session, sessionManager) {
  const books = await resolveBooksForImport(args, session.cookie);
  return importBooks(args, books, {
    getBookmarks(bookId, currentSession) {
      const detailFetchOptions = currentSession.detailFetchJson ? { fetchJson: currentSession.detailFetchJson } : {};
      return getBookmarks(currentSession.cookie, bookId, detailFetchOptions);
    },
    getReviews(bookId, currentSession) {
      const detailFetchOptions = currentSession.detailFetchJson ? { fetchJson: currentSession.detailFetchJson } : {};
      return getReviews(currentSession.cookie, bookId, detailFetchOptions);
    },
  }, 'web', session, sessionManager);
}

function gatewayOptions(args) {
  return {
    apiKey: args.gatewayApiKey,
    skillVersion: args.gatewaySkillVersion,
  };
}

async function importViaGateway(args) {
  const options = gatewayOptions(args);
  const books = await resolveBooksForImport(args, null, {
    getNotebookBooks: () => getGatewayNotebookBooks(options),
  });
  return importBooks(args, books, {
    getBookmarks: (bookId) => getGatewayBookmarks(bookId, options),
    getReviews: (bookId) => getGatewayReviews(bookId, options),
  }, 'gateway');
}

function webFallbackArgs(args) {
  const next = { ...args, apiBackend: 'web' };
  if (!next.cookieFromExplicit && !next.cookie) {
    next.cookieFrom = 'browser-managed';
  }
  return next;
}

function noGatewayCommandHint(argv, cookieFrom = 'browser-managed') {
  const hasNoGateway = argv.includes('--no-gateway');
  const hasCookieFrom = argv.includes('--cookie-from');
  const parts = ['bash ./scripts/run.sh'];
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--api-backend') {
      i += 1;
      continue;
    }
    if (arg === '--cookie-from') {
      i += 1;
      continue;
    }
    parts.push(arg.includes(' ') ? JSON.stringify(arg) : arg);
  }
  if (!hasNoGateway) parts.push('--no-gateway');
  if (!hasCookieFrom || cookieFrom) parts.push(`--cookie-from ${cookieFrom}`);
  return parts.join(' ');
}

function withGatewayConfigHint(error, argv) {
  if (!(error instanceof WereadGatewayMissingKeyError)) return error;
  return new WereadGatewayMissingKeyError([
    '未配置 WEREAD_API_KEY，默认 Gateway 后端无法运行。',
    '',
    '可选操作：',
    `1. 在 App 获取 API Key 并配置后重试：${API_KEY_HELP}；然后执行 export WEREAD_API_KEY=<你的apikey>`,
    `2. 使用受管浏览器旧链路：${noGatewayCommandHint(argv, 'browser-managed')}`,
    `3. 复用已有调试 Chrome：${noGatewayCommandHint(argv, 'browser-live')}`,
    "4. 使用手动 Cookie：追加 --no-gateway --cookie '完整 cookie 字符串'，或设置 WEREAD_COOKIE 后加 --no-gateway",
    '',
    'Gateway 优势：减少浏览器登录态/CDP 依赖，更适合默认导入和定时同步。',
    'Agent 规则：不要自行切换到 Cookie；只有用户明确选择旧链路时才使用 --no-gateway。',
  ].join('\n'));
}

async function runWebBackend(args) {
  const webArgs = webFallbackArgs(args);
  if (args.legacyBackendRequested) {
    console.warn('Using backend=web because --cookie/--cookie-from was provided. 配置 WEREAD_API_KEY 后可删除旧链路参数，使用默认 Gateway。');
  }
  await ensureManagedBrowserForWebBackend(webArgs);
  return runWithApiSessionRetry(webArgs, (session, sessionManager) => importViaWeb(webArgs, session, sessionManager));
}

async function isCdpReady(cdpUrl) {
  try {
    const res = await fetch(new URL('/json/version', cdpUrl), { signal: AbortSignal.timeout(1000) });
    return res.ok;
  } catch {
    return false;
  }
}

function cdpPort(cdpUrl) {
  try {
    return new URL(cdpUrl).port || '9222';
  } catch {
    return '9222';
  }
}

async function ensureManagedBrowserForWebBackend(args) {
  if (args.cookieFrom !== 'browser-managed') return;
  if (await isCdpReady(args.cdp)) return;
  const scriptPath = path.join(ROOT_DIR, 'scripts', 'open-chrome-debug.sh');
  console.warn('正在启动受管 Chrome 作为 web 兜底...');
  const child = spawn('bash', [scriptPath, cdpPort(args.cdp)], {
    detached: true,
    stdio: 'ignore',
  });
  child.unref();
  for (let i = 0; i < 10; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    if (await isCdpReady(args.cdp)) {
      await waitForManagedLoginWarmup(args.cdp);
      return;
    }
  }
  throw new Error('受管 Chrome CDP 启动超时，无法使用 web 兜底。请稍后重试，或手动启动 Chrome 后使用 --cookie-from browser-live。');
}

async function waitForManagedLoginWarmup(cdpUrl) {
  const scriptPath = path.join(ROOT_DIR, 'scripts', 'wait-browser-managed-ready.mjs');
  try {
    await execFileAsync('node', [
      scriptPath,
      '--cdp',
      cdpUrl,
      '--timeout-ms',
      process.env.WEREAD_BROWSER_READY_TIMEOUT_MS || '8000',
    ]);
  } catch {
    // The session acquisition path will surface the actionable login error.
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(helpText());
    return;
  }
  if (args.apiBackend === 'web') {
    return runWebBackend(args);
  }
  if (args.cookieFromExplicit || args.cookieExplicit) {
    console.warn('Using backend=gateway; --cookie/--cookie-from only apply to web backend and will be ignored.');
  }
  try {
    console.log('Using backend=gateway');
    return await importViaGateway(args);
  } catch (error) {
    if (
      error instanceof WereadGatewayMissingKeyError
      || error instanceof WereadGatewayAuthError
      || error instanceof WereadGatewayUpgradeError
    ) {
      throw withGatewayConfigHint(error, process.argv.slice(2));
    }
    if (error instanceof WereadGatewayUnavailableError) {
      console.warn(`Gateway unavailable, falling back to web backend: ${error.message}`);
      const webArgs = webFallbackArgs(args);
      console.warn(`Using backend=web (cookie-from=${webArgs.cookieFrom})`);
      return runWebBackend(webArgs);
    }
    throw error;
  }
}

function isDirectCliEntry() {
  if (!process.argv[1]) return false;
  const currentFile = fileURLToPath(import.meta.url);
  try {
    return realpathSync(process.argv[1]) === realpathSync(currentFile);
  } catch {
    return process.argv[1] === currentFile;
  }
}

if (isDirectCliEntry()) {
  main().catch((err) => {
    console.error(err.stack || String(err));
    process.exitCode = 1;
  });
}
