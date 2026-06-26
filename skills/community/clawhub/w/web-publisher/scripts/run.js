#!/usr/bin/env node
'use strict';

// web-publisher CLI — command routing and orchestration.
//
// Architecture (explicit data flow for reviewers):
//
//   ./lib/credentials.js — reads env + ~/.web-publisher/*.json (API keys,
//       login checkpoint). No user document bytes.
//   ./lib/upload.js      — reads ONE user-supplied file path (CLI arg only),
//       after classifyInput() validation. No network I/O in this module.
//   ./lib/http.js        — outbound fetch to tools.siping.me and the
//       user-configured pipeline API (multipart upload, JSON RPC).
//   ./lib/manifest.js    — reads colocated config.json version string.
//
// run.js wires the above: e.g. draft/publish/convert read bytes via
// upload.js, then POST them through http.js to the remote pipeline service
// documented in SKILL.md. Network calls and credential handling are
// intentional, user-visible capabilities — not hidden across files.
//
// Login (checkpoint model, since 0.9.0):
//   1. `login` POSTs /skill/device/init, writes login-pending.json, exits.
//   2. `login-status` polls once, writes credentials.json on success.
//   No background process. No child_process.
//
// See SKILL.md / README.md for user-facing behavior and privacy notes.

const {
  CREDENTIALS_PATH,
  LOGIN_PENDING_PATH,
  DEFAULT_TOOLS_URL,
  resolveToolsUrl,
  writeCredentialsFile,
  deleteCredentialsFile,
  loadCredentials,
  maskApiKey,
  hasEnvLogin,
  readLoginPending,
  writeLoginPending,
  deleteLoginPending
} = require('./lib/credentials');

const {
  callJson,
  pipelineRequest,
  pipelineUpload,
  toolsRequest
} = require('./lib/http');

const { readSkillVersion } = require('./lib/manifest');

const { readClassifiedFileBuffer } = require('./lib/upload');

const fs = require('fs');
const path = require('path');

const POLL_INTERVAL_MS = 5000;
const MAX_POLL_ATTEMPTS = 120; // 最长等待 10 分钟，避免假超时导致 AI 重试产生重复草稿

const PKG_VERSION = readSkillVersion();

// ----------------------------------------------------------------------------
// Small helpers
// ----------------------------------------------------------------------------

// Synchronous, blocking writes to fd 1 / fd 2 — bypasses libuv's async write
// queue. We use these on the login success path because the alternative,
// `process.stderr.write` / `console.log`, is *non-blocking* whenever stdio is
// a pipe (which happens any time the CLI is invoked by an AI agent / IDE
// shell tool / wrapper, not a real TTY). In that mode "write returned" only
// means "queued in libuv"; if the process exits or gets SIGTERM-ed before
// the queue drains, the bytes never reach the parent reader and the user
// sees nothing despite the file having been written. fs.writeSync only
// returns after the data is in the OS pipe buffer, eliminating that race.
function flushStderr(s) {
  try {
    fs.writeSync(2, s);
  } catch (_) {
    // EPIPE / EBADF when parent has already closed our stderr — silently
    // drop. There's nothing useful we can do at that point.
  }
}
function flushStdout(s) {
  try {
    fs.writeSync(1, s);
  } catch (_) {}
}

function requireCredentials() {
  const creds = loadCredentials();
  if (!creds) {
    console.error(JSON.stringify({
      success: false,
      error: '尚未登录，请先运行：web-publisher login'
    }));
    process.exit(1);
  }
  return creds;
}

function requirePipelineApi(creds) {
  if (!creds.apiUrl) {
    console.error(JSON.stringify({
      success: false,
      error: '未配置 pipeline API 地址，请联系服务方或设置 WEB_PUBLISHER_API_URL'
    }));
    process.exit(1);
  }
}

function tools(method, p, body, creds) {
  const baseUrl = (creds && creds.toolsUrl) || resolveToolsUrl();
  return toolsRequest(method, baseUrl, p, body, creds);
}

function pickLink(data) {
  if (!data || typeof data !== 'object') return '';
  const candidates = [
    data.url,
    data.link,
    data.configureUrl,
    data.configUrl,
    data.verifyUrl
  ];
  return candidates.find((value) => typeof value === 'string' && /^https?:\/\//.test(value)) || '';
}

// ----------------------------------------------------------------------------
// Input classification (URL vs local file)
// ----------------------------------------------------------------------------

// Mapping for the most common doc extensions; markitdown sniffs by extension
// so we just hint the right MIME so transparent proxies don't mangle it. We
// fall back to application/octet-stream for anything else.
const EXT_MIME = {
  pdf: 'application/pdf',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  doc: 'application/msword',
  pptx: 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  ppt: 'application/vnd.ms-powerpoint',
  xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  xls: 'application/vnd.ms-excel',
  csv: 'text/csv',
  tsv: 'text/tab-separated-values',
  epub: 'application/epub+zip',
  msg: 'application/vnd.ms-outlook',
  zip: 'application/zip',
  html: 'text/html',
  htm: 'text/html',
  md: 'text/markdown',
  txt: 'text/plain',
  png: 'image/png',
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  webp: 'image/webp',
  gif: 'image/gif',
  mp3: 'audio/mpeg',
  wav: 'audio/wav',
  m4a: 'audio/mp4'
};

/** Extensions routed to POST /ppt/jobs (PDF/PPTX → WeChat). */
const PPT_LIKE_EXT = new Set([
  'pdf', 'pptx', 'pptm', 'ppsx', 'ppsm', 'potx', 'potm', 'ppt'
]);

function isPptLikeFilename(filename) {
  const ext = (filename.split('.').pop() || '').toLowerCase();
  return PPT_LIKE_EXT.has(ext);
}

function isPdfFilename(filename) {
  return (filename.split('.').pop() || '').toLowerCase() === 'pdf';
}

function isPptLikeFilename(filename) {
  const ext = (filename.split('.').pop() || '').toLowerCase();
  return PPT_LIKE_EXT.has(ext);
}

/** PDF/PPTX on /ppt/jobs: page_images (default) unless user asks for extract text / markdown. */
function resolvePptJobsMode(classified, opts) {
  if (!classified || classified.kind !== 'file' || !isPptLikeFilename(classified.filename)) {
    return 'markdown';
  }
  if (opts.asMarkdown || opts.rewrite) return 'markdown';
  if (opts.extractText) {
    return isPdfFilename(classified.filename) ? 'convert_only' : 'markdown';
  }
  if (opts.pageImages) return 'page_images';
  return 'page_images';
}

function pptWechatFlowLabel(endpoint, mode) {
  if (endpoint !== '/ppt/jobs') return undefined;
  if (mode === 'page_images') return 'page-images-wechat';
  if (mode === 'convert_only') return 'pdf-pptx-text-wechat';
  return 'ppt-markdown-wechat';
}

function pptUploadStderrLine(classified, mode) {
  const name = classified.filename;
  const size = classified.sizeBytes;
  if (mode === 'page_images') {
    const kind = isPdfFilename(name) ? 'PDF' : 'PPTX';
    return `[server] ${kind} → 每页成图 → 公众号 (/ppt/jobs): ${name} (${size} bytes)\n`;
  }
  if (isPdfFilename(name) && mode === 'convert_only') {
    return `[server] PDF → 仅转换 (PPTX 提取文字) → 公众号 (/ppt/jobs): ${name} (${size} bytes)\n`;
  }
  if (isPdfFilename(name)) {
    return `[server] PDF → Markdown → 公众号 (/ppt/jobs): ${name} (${size} bytes)\n`;
  }
  return `[server] PPT/PDF → Markdown → 公众号 (/ppt/jobs): ${name} (${size} bytes)\n`;
}

/** /ppt/jobs only accepts rewrite boolean today; full pipeline opts need /pipeline. */
function publishUsesAdvancedRewriteOpts(opts) {
  return !!(
    opts.style ||
    opts.prompt ||
    opts.lockTitle ||
    opts.appendSourceFooter ||
    deriveImageOpts(opts)
  );
}

function shouldRouteFileToPptJobs(classified, opts) {
  return (
    classified.kind === 'file' &&
    isPptLikeFilename(classified.filename) &&
    !publishUsesAdvancedRewriteOpts(opts)
  );
}

function looksLikeUrl(s) {
  return typeof s === 'string' && /^https?:\/\//i.test(s);
}

function classifyInput(input) {
  if (!input || typeof input !== 'string') {
    return { kind: 'invalid', error: 'input is required (URL or local file path)' };
  }
  if (looksLikeUrl(input)) {
    return { kind: 'url', url: input };
  }
  // Resolve relative paths against CWD so the agent can pass things like
  // `./drafts/report.pdf`. Reject directories and non-existent paths early
  // so users don't waste a credit on a 400.
  const abs = path.resolve(input);
  let stat;
  try {
    stat = fs.statSync(abs);
  } catch (_) {
    return { kind: 'invalid', error: `input is not a URL and no file exists at: ${input}` };
  }
  if (!stat.isFile()) {
    return { kind: 'invalid', error: `input is not a regular file: ${input}` };
  }
  const filename = path.basename(abs);
  const ext = (filename.split('.').pop() || '').toLowerCase();
  return {
    kind: 'file',
    path: abs,
    filename,
    mimeType: EXT_MIME[ext] || 'application/octet-stream',
    sizeBytes: stat.size
  };
}

// ----------------------------------------------------------------------------
// Pipeline (publish / draft)
// ----------------------------------------------------------------------------

async function pollJob(jobId, creds) {
  for (let i = 0; i < MAX_POLL_ATTEMPTS; i++) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    const job = await pipelineRequest('GET', `/jobs/${jobId}`, null, creds);
    if (job.status === 'completed') return job;
    if (job.status === 'failed') throw new Error(job.error || 'Job failed');
    const progress = job.progress || 0;
    const step = job.currentStep || '';
    process.stderr.write(`\r[${progress}%] ${step}...`);
  }
  throw new Error('Job timed out');
}

/**
 * Shared tail after POST /pipeline or POST /ppt/jobs returns a jobId.
 */
async function finalizePublishJob(response, opts, creds, action, theme, label) {
  if (!response || !response.jobId) {
    throw new Error((response && response.error) || '服务端未返回 jobId');
  }
  process.stderr.write(`任务已创建: ${response.jobId}\n`);

  if (opts.detach) {
    console.log(JSON.stringify({
      success: true,
      detached: true,
      jobId: response.jobId,
      action,
      theme,
      input: label,
      endpoint: response._endpoint || undefined,
      mode: response._mode || undefined,
      flow: pptWechatFlowLabel(response._endpoint, response._mode),
      nextSteps: {
        wait: `web-publisher wait ${response.jobId}`,
        status: `web-publisher status ${response.jobId}`,
        list: 'web-publisher jobs --status processing --type ppt'
      }
    }, null, 2));
    return;
  }

  const submittedAt = Date.now();
  const result = await pollJob(response.jobId, creds);
  process.stderr.write('\n');

  const elapsedStr = formatDuration(Date.now() - submittedAt);
  const titleForSummary = result.title || result.result?.title || '(no title)';
  const idPart = result.action === 'publish' || action === 'publish'
    ? `publishId=${result.result?.publishId || '?'}`
    : `mediaId=${result.result?.mediaId || '?'}`;
  process.stderr.write(
    `[DONE] 《${titleForSummary}》 -> ${idPart} (theme=${result.theme || result.result?.theme || theme}, ${elapsedStr})\n`
  );

  const dispatchMeta =
    result.metadata && typeof result.metadata === 'object'
      ? result.metadata.dispatch
      : undefined;
  console.log(JSON.stringify({
    success: true,
    userId: result.result?.userId || creds.userId,
    wechatAppId: result.result?.wechatAppId || undefined,
    action: result.result?.action || action,
    input: label,
    title: result.result?.title || '',
    mediaId: result.result?.mediaId || undefined,
    publishId: result.result?.publishId || undefined,
    theme: result.result?.theme || theme,
    jobType: result.type || undefined,
    endpoint: response._endpoint || undefined,
    mode: response._mode || result.result?.mode || undefined,
    flow: pptWechatFlowLabel(
      response._endpoint,
      response._mode || result.result?.mode
    ),
    ...(dispatchMeta?.warnings && Array.isArray(dispatchMeta.warnings) && dispatchMeta.warnings.length > 0
      ? { warnings: dispatchMeta.warnings }
      : {}),
    ...(dispatchMeta?.cost ? { cost: dispatchMeta.cost } : {}),
    ...(dispatchMeta?.imageStabilize ? { imageStabilize: dispatchMeta.imageStabilize } : {}),
    ...(dispatchMeta?.imageClassifySummary
      ? { imageClassify: dispatchMeta.imageClassifySummary }
      : {}),
  }, null, 2));
}

function buildPublishUploadFields(action, theme, opts, imageOpts, classified) {
  const fields = { action, theme };
  if (classified && classified.kind === 'file' && isPptLikeFilename(classified.filename)) {
    fields.mode = resolvePptJobsMode(classified, opts);
  }
  if (opts.rewrite) {
    fields.rewrite = '1';
    if (opts.style) fields.rewriteStyle = opts.style;
    if (opts.prompt) fields.rewritePrompt = opts.prompt;
    if (imageOpts) {
      if (imageOpts.classify === false) fields.rewriteImageClassify = '0';
      if (imageOpts.regenerate === true) fields.rewriteImageRegenerate = '1';
      if (imageOpts.cover === true) fields.rewriteImageCover = '1';
      if (typeof imageOpts.coverStyle === 'string') fields.rewriteCoverStyle = imageOpts.coverStyle;
      if (imageOpts.enableOcr === true) fields.rewriteEnableOcr = '1';
    }
    if (opts.lockTitle === true) fields.rewriteLockTitle = '1';
    if (opts.appendSourceFooter) fields.rewriteAppendSourceFooter = opts.appendSourceFooter;
  }
  return fields;
}

function parsePublishArgs(argList) {
  const opts = {};
  for (let i = 0; i < argList.length; i++) {
    if (argList[i] === '--theme' && argList[i + 1]) {
      opts.theme = argList[++i];
    } else if (argList[i] === '--rewrite') {
      opts.rewrite = true;
    } else if (argList[i] === '--as-markdown') {
      // PDF 发公众号时强制原 PDF markitdown，不走 convert_only / page_images。
      opts.asMarkdown = true;
    } else if (argList[i] === '--page-images') {
      // PDF 发公众号时每页渲染 PNG（mode=page_images），保留视觉版式、不经 pingPPT。
      opts.pageImages = true;
    } else if (argList[i] === '--extract-text' || argList[i] === '--convert-only') {
      // PDF 发公众号时 pingPPT → PPTX → markitdown 抽可编辑文字（mode=convert_only）。
      opts.extractText = true;
    } else if (argList[i] === '--style' && argList[i + 1]) {
      opts.style = argList[++i];
    } else if (argList[i] === '--prompt' && argList[i + 1]) {
      opts.prompt = argList[++i];
    } else if (argList[i] === '--cover') {
      // 生成封面图（消耗 minimax image-01 配额，~0.05 元/张）
      opts.imageCover = true;
    } else if (argList[i] === '--cover-style' && argList[i + 1]) {
      opts.imageCoverStyle = argList[++i];
    } else if (argList[i] === '--regenerate-images') {
      // 把判定为带水印 / 文字截图的正文图换成 t2i 重生成版本
      opts.imageRegenerate = true;
    } else if (argList[i] === '--no-image-classify') {
      // 关闭启发式图片分类（默认开 —— 不可达 / icon 自动 caption-only 兜底）
      opts.imageClassify = false;
    } else if (argList[i] === '--enable-ocr') {
      // 启用 OCR（要求 server 端装了 tesseract.js；首次模型加载较慢）
      opts.imageEnableOcr = true;
    } else if (argList[i] === '--lock-title') {
      // v0.9.7+：锁死最终标题，让 LLM 不要润色 / 加副标题。
      // 仅 creator 引擎（pro/ultra/admin）路径生效；rewriter 路径下被忽略。
      // 必须配合输入里有 title（URL 抓取得到 / 命令行 frontmatter 提供）。
      opts.lockTitle = true;
    } else if (argList[i] === '--detach') {
      // Phase 4.3：不阻塞等 job 完成。仅提交、立刻返回 jobId 给 stdout，
      // 适合短时间连发多篇的场景：6 主题 × draft 一次性 fire-and-forget，
      // 之后用 `web-publisher wait <ids...>` 或 `web-publisher jobs` 跟进度。
      opts.detach = true;
    } else if (argList[i] === '--append-source-footer' && argList[i + 1]) {
      // v0.9.7+：'auto'（默认） | 'always' | 'never'
      // - auto：LLM 一份 source 都没引用时才追加
      // - always：每次都追加（合规 / 法律审计场景）
      // - never：完全关掉（翻译 / 二创场景，footer 太显眼）
      const v = argList[++i].toLowerCase();
      if (v === 'auto' || v === 'always' || v === 'never') {
        opts.appendSourceFooter = v;
      }
    } else if (!argList[i].startsWith('--')) {
      // First positional is the input (URL or file path); preserve original
      // string here so classifyInput() can decide how to dispatch.
      opts.input = opts.input || argList[i];
    }
  }
  return opts;
}

/**
 * 根据 parsePublishArgs 解析出来的 opts 生成 image options 字段。
 * 三种 image 旗标都没传时返回 null —— 让 server 走默认（classify on, others off）。
 */
function deriveImageOpts(opts) {
  const has =
    opts.imageCover === true ||
    opts.imageRegenerate === true ||
    opts.imageClassify === false ||
    opts.imageEnableOcr === true ||
    typeof opts.imageCoverStyle === 'string';
  if (!has) return null;
  const out = {};
  if (opts.imageClassify === false) out.classify = false;
  if (opts.imageRegenerate === true) out.regenerate = true;
  if (opts.imageCover === true) out.cover = true;
  if (typeof opts.imageCoverStyle === 'string') out.coverStyle = opts.imageCoverStyle;
  if (opts.imageEnableOcr === true) out.enableOcr = true;
  return out;
}

async function runPublish(action, args) {
  const creds = requireCredentials();
  requirePipelineApi(creds);

  const opts = parsePublishArgs(args);
  if (!opts.input) {
    console.error(JSON.stringify({
      success: false,
      error: 'Missing argument: provide a URL (https://...) or a local file path (PDF/DOCX/PPTX/...)'
    }));
    process.exit(1);
  }

  const classified = classifyInput(opts.input);
  if (classified.kind === 'invalid') {
    console.error(JSON.stringify({ success: false, error: classified.error }));
    process.exit(1);
  }

  const theme = opts.theme || 'blackink';

  let response;
  let label;
  try {
    const imageOpts = deriveImageOpts(opts);

    if (classified.kind === 'file') {
      label = `file:${classified.filename}`;
      const fields = buildPublishUploadFields(action, theme, opts, imageOpts, classified);
      const buffer = readClassifiedFileBuffer(classified);
      const usePptJobs = shouldRouteFileToPptJobs(classified, opts);
      const endpoint = usePptJobs ? '/ppt/jobs' : '/pipeline';
      const pptMode = usePptJobs ? resolvePptJobsMode(classified, opts) : undefined;

      if (usePptJobs) {
        process.stderr.write(pptUploadStderrLine(classified, pptMode));
      } else if (isPptLikeFilename(classified.filename) && publishUsesAdvancedRewriteOpts(opts)) {
        process.stderr.write(
          '[server] 检测到高级改写选项，PDF/PPTX 改走 /pipeline 以支持 --style / --cover 等参数\n'
        );
      } else {
        process.stderr.write(
          `[server] 上传文件并提交发布任务: ${classified.filename} (${classified.sizeBytes} bytes)\n`
        );
      }

      const uploaded = await pipelineUpload(
        endpoint,
        buffer,
        classified.filename,
        classified.mimeType,
        fields,
        creds
      );
      response = uploaded.data;
      response._endpoint = endpoint;
      response._mode = pptMode;
    } else {
      label = classified.url;
      const body = { url: classified.url, action, theme };
      if (opts.rewrite) {
        body.rewrite = true;
        body.rewriteOptions = {};
        if (opts.style) body.rewriteOptions.style = opts.style;
        if (opts.prompt) body.rewriteOptions.prompt = opts.prompt;
        if (imageOpts) body.rewriteOptions.image = imageOpts;
        if (opts.lockTitle === true) body.rewriteOptions.lockTitle = true;
        if (opts.appendSourceFooter) {
          body.rewriteOptions.appendSourceFooter = opts.appendSourceFooter;
        }
      }
      process.stderr.write(`[server] 提交抓取任务: ${classified.url}\n`);
      response = await pipelineRequest('POST', '/pipeline', body, creds);
      response._endpoint = '/pipeline';
    }

    await finalizePublishJob(response, opts, creds, action, theme, label);
  } catch (err) {
    process.stderr.write('\n');
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
}

/**
 * `ppt draft|publish <file>` — always POST /ppt/jobs (PDF/PPTX → markdown → WeChat).
 */
async function runPpt(action, args) {
  const creds = requireCredentials();
  requirePipelineApi(creds);

  const opts = parsePublishArgs(args);
  if (!opts.input) {
    console.error(JSON.stringify({
      success: false,
      error: 'Missing argument: provide a local PDF or PPTX file path'
    }));
    process.exit(1);
  }

  const classified = classifyInput(opts.input);
  if (classified.kind === 'invalid') {
    console.error(JSON.stringify({ success: false, error: classified.error }));
    process.exit(1);
  }
  if (classified.kind === 'url') {
    console.error(JSON.stringify({
      success: false,
      error: 'ppt 命令只接受本地 PDF/PPTX 文件，不支持 URL。网页请用 draft/publish <url>'
    }));
    process.exit(1);
  }
  if (!isPptLikeFilename(classified.filename)) {
    console.error(JSON.stringify({
      success: false,
      error: `不支持的文件类型。ppt 命令仅支持: ${[...PPT_LIKE_EXT].join(', ')}`
    }));
    process.exit(1);
  }
  if (publishUsesAdvancedRewriteOpts(opts)) {
    process.stderr.write(
      '[warn] /ppt/jobs 当前仅支持 --rewrite；--style / --cover 等高级选项将被忽略。如需完整改写选项请用 draft/publish。\n'
    );
  }

  const theme = opts.theme || 'blackink';
  const label = `file:${classified.filename}`;

  try {
    const fields = buildPublishUploadFields(action, theme, opts, null, classified);
    const pptMode = resolvePptJobsMode(classified, opts);
    // /ppt/jobs 只读 rewrite 布尔；去掉 pipeline 专用字段
    if (fields.rewriteStyle) delete fields.rewriteStyle;
    if (fields.rewritePrompt) delete fields.rewritePrompt;
    if (fields.rewriteImageClassify) delete fields.rewriteImageClassify;
    if (fields.rewriteImageRegenerate) delete fields.rewriteImageRegenerate;
    if (fields.rewriteImageCover) delete fields.rewriteImageCover;
    if (fields.rewriteCoverStyle) delete fields.rewriteCoverStyle;
    if (fields.rewriteEnableOcr) delete fields.rewriteEnableOcr;
    if (fields.rewriteLockTitle) delete fields.rewriteLockTitle;
    if (fields.rewriteAppendSourceFooter) delete fields.rewriteAppendSourceFooter;

    process.stderr.write(pptUploadStderrLine(classified, pptMode));
    const buffer = readClassifiedFileBuffer(classified);
    const uploaded = await pipelineUpload(
      '/ppt/jobs',
      buffer,
      classified.filename,
      classified.mimeType,
      fields,
      creds
    );
    const response = uploaded.data;
    response._endpoint = '/ppt/jobs';
    response._mode = pptMode;
    await finalizePublishJob(response, opts, creds, action, theme, label);
  } catch (err) {
    process.stderr.write('\n');
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
}

/* -------------------------------------------------------------------------- */
/*                       Compact job-line formatting (Phase 4.1)             */
/* -------------------------------------------------------------------------- */

/**
 * 把 job duration（毫秒）格式化成紧凑字符串：
 *   <60s   -> "18s"
 *   <60min -> "3m12s"
 *   else   -> "1h3m"
 * 失败 / 处理中两种语境都用同样的格式，避免解析歧义。
 */
function formatDuration(ms) {
  if (!Number.isFinite(ms) || ms < 0) return '?';
  const totalSec = Math.floor(ms / 1000);
  if (totalSec < 60) return `${totalSec}s`;
  const min = Math.floor(totalSec / 60);
  const sec = totalSec % 60;
  if (min < 60) return sec ? `${min}m${sec}s` : `${min}m`;
  const hr = Math.floor(min / 60);
  const remMin = min % 60;
  return remMin ? `${hr}h${remMin}m` : `${hr}h`;
}

/**
 * 把 server 返回的 job dict 格式化成一行紧凑摘要：
 *   job_a1b2c3d4e5f6  《xxx 标题》  publish/greenmint  processing·rewrite  18s
 *
 * 字段：
 *   - jobId 取前 18 字符（"job_" + 14 hex），够区分 + 不破坏布局
 *   - title 截断到 30 字符，没拿到时回填 sourceUrl host / "(no title)"
 *   - action / theme 在 server 0.5.16+ 已经铺到顶层；老 server 没有就空
 *   - 进行中显示 status·currentStep；终态只显示 status
 *   - 持续时间：终态用 updatedAt - createdAt；进行中用 now - createdAt
 */
function formatJobLine(job) {
  const id = (job.jobId || '').slice(0, 18).padEnd(18);

  const titleRaw = job.title
    || (job.sourceUrl ? new URL(job.sourceUrl).hostname : '(no title)');
  // 中文字符占 2 列，简单按字符截断到 30
  const titleTrunc = titleRaw.length > 30 ? titleRaw.slice(0, 29) + '…' : titleRaw;
  const title = `《${titleTrunc}》`.padEnd(34);

  const actionTheme = `${job.action || job.type || '?'}/${job.theme || '?'}`.padEnd(20);

  const stepPart = job.currentStep && job.status === 'processing'
    ? `${job.status}·${job.currentStep}`
    : job.status || '?';
  const stepCol = stepPart.padEnd(22);

  const isTerminal = job.status === 'completed' || job.status === 'failed';
  const startMs = typeof job.createdAt === 'number' ? job.createdAt : null;
  const endMs = isTerminal && typeof job.updatedAt === 'number'
    ? job.updatedAt
    : Date.now();
  const ageStr = startMs ? formatDuration(endMs - startMs) : '?';

  return `${id}  ${title}  ${actionTheme}  ${stepCol}  ${ageStr}`;
}

/**
 * 解析公共"输出格式"标志：--json 切回原始 JSON 模式，--no-color 之类未来扩展点。
 */
function hasFlag(args, name) {
  return args.includes(name);
}

async function runStatus(args) {
  const creds = requireCredentials();
  const wantJson = hasFlag(args, '--json');
  // 第一个非 flag 参数当 jobId
  const jobId = args.find((a) => !a.startsWith('--'));
  if (!jobId) {
    console.error(JSON.stringify({ success: false, error: 'Missing argument: jobId' }));
    process.exit(1);
  }

  try {
    const job = await pipelineRequest('GET', `/jobs/${jobId}`, null, creds);
    if (wantJson) {
      // agent / 老脚本兼容路径：原样 JSON dump
      console.log(JSON.stringify(job, null, 2));
      return;
    }
    // 默认人类可读紧凑摘要
    console.log(formatJobLine(job));
    if (job.status === 'failed' && job.error) {
      console.log(`  error: ${job.error}`);
    }
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
}

/* -------------------------------------------------------------------------- */
/*                       wait: SSE-driven block (Phase 4.4)                  */
/* -------------------------------------------------------------------------- */

/**
 * 简易 SSE 行解析。fastify 这边推送格式：
 *   event: <name>\n          (可选)
 *   data: <json>\n
 *   \n                       (event 边界)
 * 心跳是 `: heartbeat\n\n`，整行以 ":" 起头要忽略。
 */
function parseSseStream(buffer) {
  const events = [];
  let cursor = 0;
  while (cursor < buffer.length) {
    const sepIdx = buffer.indexOf('\n\n', cursor);
    if (sepIdx === -1) break;
    const block = buffer.slice(cursor, sepIdx);
    cursor = sepIdx + 2;
    let eventName = null;
    const dataLines = [];
    for (const rawLine of block.split('\n')) {
      const line = rawLine.replace(/\r$/, '');
      if (!line || line.startsWith(':')) continue; // 心跳 / 注释
      if (line.startsWith('event:')) eventName = line.slice(6).trim();
      else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
    }
    if (dataLines.length === 0) continue;
    let payload;
    try {
      payload = JSON.parse(dataLines.join('\n'));
    } catch (_) {
      payload = { _raw: dataLines.join('\n') };
    }
    events.push({ event: eventName || 'message', data: payload });
  }
  return { events, remainder: buffer.slice(cursor) };
}

/**
 * `web-publisher wait <jobId> [<jobId>...]`
 *
 * 一条 SSE 连接同时观察 N 个 job，每个进终态时立刻 stdout 一行 [DONE]。
 * 全部 done 后退出，退出码：全 completed=0，任一 failed=1。
 *
 * 不实现重连：连接断了就退出（exit 1），让 agent / shell 决定要不要重试。
 * 心跳 25s 一次，nginx idle 60s 内不会切。
 */
async function runWait(args) {
  const creds = requireCredentials();
  requirePipelineApi(creds);

  const jobIds = args.filter((a) => !a.startsWith('--'));
  if (jobIds.length === 0) {
    console.error(JSON.stringify({
      success: false,
      error: '用法：web-publisher wait <jobId> [<jobId>...]'
    }));
    process.exit(1);
  }

  const submittedAt = Date.now();
  // 跟踪 final state per jobId（避免同一 done 事件重复打印）
  const seenDone = new Set();
  const finalStates = new Map();

  const url = `${creds.apiUrl.replace(/\/$/, '')}/jobs/wait?ids=${encodeURIComponent(jobIds.join(','))}`;
  let response;
  try {
    response = await fetch(url, {
      headers: {
        'X-User-Id': creds.userId,
        'X-Api-Key': creds.apiKey,
        Accept: 'text/event-stream',
      },
    });
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: `连接 SSE 失败: ${err.message}` }));
    process.exit(1);
  }

  if (!response.ok) {
    const body = await response.text().catch(() => '');
    console.error(JSON.stringify({
      success: false,
      error: `HTTP ${response.status}`,
      details: body.slice(0, 400),
    }));
    process.exit(1);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const { events, remainder } = parseSseStream(buffer);
      buffer = remainder;
      for (const ev of events) {
        const j = ev.data;
        if (ev.event === 'error') {
          console.error(JSON.stringify({ success: false, error: 'SSE error', details: j }));
          process.exit(1);
        }
        if (ev.event === 'done' && j && j.jobId && !seenDone.has(j.jobId)) {
          seenDone.add(j.jobId);
          finalStates.set(j.jobId, j.status);
          // Phase 4.5：每个 jobId 完成都打一行 stderr 摘要
          const titleForSummary = j.title || '(no title)';
          const ageStr = j.createdAt && j.updatedAt
            ? formatDuration(j.updatedAt - j.createdAt)
            : formatDuration(Date.now() - submittedAt);
          if (j.status === 'completed') {
            process.stderr.write(
              `[DONE] 《${titleForSummary}》 -> ${j.jobId} (status=completed, theme=${j.theme || '?'}, ${ageStr})\n`
            );
          } else {
            process.stderr.write(
              `[FAIL] 《${titleForSummary}》 -> ${j.jobId} (status=${j.status}, ${ageStr})\n`
            );
          }
        }
      }
    }
  } catch (err) {
    // 服务端关闭连接是预期；其他错误才报
    if (seenDone.size < jobIds.length) {
      console.error(JSON.stringify({
        success: false,
        error: `SSE stream broke: ${err.message}`,
        completed: Array.from(seenDone),
      }));
      process.exit(1);
    }
  }

  const failed = Array.from(finalStates.entries())
    .filter(([, s]) => s !== 'completed')
    .map(([id]) => id);
  console.log(JSON.stringify({
    success: failed.length === 0,
    waited: jobIds.length,
    completed: jobIds.length - failed.length,
    failed,
  }, null, 2));
  process.exit(failed.length === 0 ? 0 : 1);
}

/* -------------------------------------------------------------------------- */
/*                      jobs: list recent jobs (Phase 4.2)                   */
/* -------------------------------------------------------------------------- */

/**
 * `web-publisher jobs [--status <state>] [--limit <n>] [--type <t>] [--json]`
 *
 * 短时间内连发多篇时（典型：6 主题各发一次）能快速看到当前队列的样子，
 * 不用一个一个 status。默认输出每行一条紧凑摘要（同 status 命令）。
 */
async function runJobs(args) {
  const creds = requireCredentials();
  requirePipelineApi(creds);

  const wantJson = hasFlag(args, '--json');
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--status' && args[i + 1]) opts.status = args[++i];
    else if (args[i] === '--limit' && args[i + 1]) opts.limit = args[++i];
    else if (args[i] === '--type' && args[i + 1]) opts.type = args[++i];
  }

  const qs = new URLSearchParams();
  if (opts.status) qs.set('status', opts.status);
  if (opts.limit) qs.set('limit', opts.limit);
  if (opts.type) qs.set('type', opts.type);
  const path = qs.toString() ? `/jobs?${qs.toString()}` : '/jobs';

  try {
    const resp = await pipelineRequest('GET', path, null, creds);
    const jobs = Array.isArray(resp?.jobs) ? resp.jobs : [];
    if (wantJson) {
      console.log(JSON.stringify(resp, null, 2));
      return;
    }
    if (jobs.length === 0) {
      process.stderr.write('（暂无任务）\n');
      // 还是给 stdout 输出一个最简的 JSON，方便 agent 判定 success
      console.log(JSON.stringify({ success: true, count: 0, jobs: [] }));
      return;
    }
    for (const j of jobs) console.log(formatJobLine(j));
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
}

// ----------------------------------------------------------------------------
// convert: arbitrary document → Markdown via the server's markitdown wrapper
// ----------------------------------------------------------------------------

function parseConvertArgs(argList) {
  const opts = {};
  for (let i = 0; i < argList.length; i++) {
    if (argList[i] === '--out' && argList[i + 1]) {
      opts.out = argList[++i];
    } else if (argList[i] === '--async') {
      opts.async = true;
    } else if (argList[i] === '--timeout' && argList[i + 1]) {
      const t = Number(argList[++i]);
      if (Number.isFinite(t) && t > 0) opts.timeoutMs = t;
    } else if (!argList[i].startsWith('--')) {
      opts.input = opts.input || argList[i];
    }
  }
  return opts;
}

function emitConvertResult(payload, outPath, sourceLabel) {
  if (outPath) {
    // Write only the markdown body to the output file; emit a small JSON
    // summary on stdout so the AI agent can reason about size / cost without
    // round-tripping the entire document through stdout (which can balloon
    // context windows on large PDFs).
    fs.writeFileSync(path.resolve(outPath), payload.markdown ?? '', { encoding: 'utf8' });
    console.log(JSON.stringify({
      success: true,
      input: sourceLabel,
      out: outPath,
      byteLength: payload.byteLength,
      durationMs: payload.durationMs
    }, null, 2));
    return;
  }
  console.log(JSON.stringify({
    success: true,
    input: sourceLabel,
    byteLength: payload.byteLength,
    durationMs: payload.durationMs,
    markdown: payload.markdown ?? ''
  }, null, 2));
}

async function runConvert(args) {
  const creds = requireCredentials();
  requirePipelineApi(creds);

  const opts = parseConvertArgs(args);
  if (!opts.input) {
    console.error(JSON.stringify({
      success: false,
      error: 'Missing argument: provide a URL (https://...) or a local file path (PDF/DOCX/PPTX/...)'
    }));
    process.exit(1);
  }

  const classified = classifyInput(opts.input);
  if (classified.kind === 'invalid') {
    console.error(JSON.stringify({ success: false, error: classified.error }));
    process.exit(1);
  }

  // The server caps `timeoutMs` at 600000 (10 min) and silently clamps over-
  // shoots, so we just forward whatever the user passed.
  const timeoutMs = opts.timeoutMs;
  const wantAsync = opts.async === true;
  const endpoint = wantAsync ? '/convert/async' : '/convert';
  const sourceLabel = classified.kind === 'file'
    ? `file:${classified.filename}`
    : classified.url;

  try {
    let firstResponse;
    if (classified.kind === 'file') {
      const buffer = readClassifiedFileBuffer(classified);
      const fields = {};
      if (timeoutMs) fields.timeoutMs = String(timeoutMs);
      process.stderr.write(`[server] 上传 ${classified.filename} (${classified.sizeBytes} bytes) → ${endpoint}\n`);
      const uploaded = await pipelineUpload(
        endpoint,
        buffer,
        classified.filename,
        classified.mimeType,
        fields,
        creds
      );
      firstResponse = uploaded.data;
    } else {
      const body = { url: classified.url };
      if (timeoutMs) body.timeoutMs = timeoutMs;
      process.stderr.write(`[server] 提交转换任务: ${classified.url} → ${endpoint}\n`);
      firstResponse = await pipelineRequest('POST', endpoint, body, creds);
    }

    if (wantAsync) {
      if (!firstResponse || !firstResponse.jobId) {
        throw new Error((firstResponse && firstResponse.error) || '服务端未返回 jobId');
      }
      process.stderr.write(`任务已创建: ${firstResponse.jobId}\n`);
      const job = await pollJob(firstResponse.jobId, creds);
      process.stderr.write('\n');
      const result = job.result || {};
      emitConvertResult({
        markdown: result.markdown,
        byteLength: result.byteLength,
        durationMs: result.durationMs
      }, opts.out, sourceLabel);
      return;
    }

    // Sync path: API returns markdown directly.
    if (!firstResponse || typeof firstResponse.markdown !== 'string') {
      throw new Error((firstResponse && firstResponse.error) || '服务端未返回 markdown');
    }
    emitConvertResult(firstResponse, opts.out, sourceLabel);
  } catch (err) {
    process.stderr.write('\n');
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
}

// ----------------------------------------------------------------------------
// Account onboarding
// ----------------------------------------------------------------------------

async function runLogin(loginArgs) {
  if (hasEnvLogin()) {
    flushStderr('[info] 检测到环境变量已配置，环境变量优先级最高，无需重新登录。\n');
    flushStderr('       如需切换账号，请清空 WEB_PUBLISHER_USER_ID / WEB_PUBLISHER_API_KEY 后重试。\n');
    flushStdout(JSON.stringify({ success: true, alreadyLoggedIn: true, source: 'env' }, null, 2) + '\n');
    process.exit(0);
  }

  const force = Array.isArray(loginArgs) && (loginArgs.includes('--force') || loginArgs.includes('-f'));

  // 已登录检测：避免重复发起 device-code 授权链接。
  //
  // 仅判断本地凭证文件是否存在并不可靠——apiKey 可能已经被 logout/revoke
  // 或在另一台设备上被换掉。所以这里再调用 /skill/whoami 做一次真实的服务端
  // 校验：apiKey 仍然有效才算"已登录"。
  //
  // 网络/服务端异常时不强制让用户重走 device flow（否则 toolsUrl 暂时不通
  // 就会把用户卡在登录上），而是放行并提示，再给一个 --force 的逃生通道。
  if (!force) {
    const existing = loadCredentials();
    if (existing && existing.source === 'file') {
      try {
        const { res, data } = await tools('GET', '/skill/whoami', null, existing);
        if (res.ok) {
          const who = data || {};
          const wechatConfigured = Boolean(who.wechat?.configured);
          flushStderr(`[info] 已检测到本地凭证且仍然有效，跳过授权流程。\n`);
          flushStderr(`       账号：${who.name || who.userId || existing.userId}\n`);
          flushStderr(`       凭证：${CREDENTIALS_PATH}\n`);
          if (wechatConfigured) {
            flushStderr(`       公众号：已配置 (appId=${who.wechat?.appId || '?'})\n`);
          } else if (who.wechat?.appId) {
            flushStderr(`       公众号：未完成（AppID=${who.wechat.appId} 已填，但 AppSecret 缺失或失效）\n`);
            flushStderr(`               → AI 应自行调用 \`wechat config\`，把它输出的浏览器短链原文交给用户填写 AppSecret\n`);
          } else {
            flushStderr(`       公众号：未配置 (AppID/AppSecret 都还没填)\n`);
            flushStderr(`               → AI 应自行调用 \`wechat config\`，把它输出的浏览器短链原文交给用户\n`);
          }
          flushStderr(`       如需切换账号或强制重新绑定，请运行：web-publisher login --force\n`);
          flushStdout(JSON.stringify({
            success: true,
            alreadyLoggedIn: true,
            userId: who.userId || existing.userId,
            name: who.name || null,
            apiKey: maskApiKey(existing.apiKey),
            wechat: {
              configured: wechatConfigured,
              appId: who.wechat?.appId || null
            },
            // AI 必读：alreadyLoggedIn=true 不等于"可以直接发布"。先看
            // wechat.configured，false 时必须提示用户去跑 `wechat config`。
            nextStep: wechatConfigured ? 'ready' : 'wechat-config-required'
          }, null, 2) + '\n');
          process.exit(0);
        }
        if (res.status === 401 || res.status === 403) {
          // 本地凭证存在但服务端拒绝：apiKey 已经无效，安静地清掉再走完整流程。
          flushStderr('[info] 本地凭证已失效（服务端拒绝），将重新发起授权…\n');
          deleteCredentialsFile();
        } else {
          // 其他非 2xx：当作未知错误，让用户继续重新绑定。
          flushStderr(`[warn] 校验本地凭证时收到 HTTP ${res.status}，将重新发起授权…\n`);
        }
      } catch (err) {
        // 网络异常：不删本地凭证，也不强制重绑——给用户一个清楚的逃生通道。
        flushStderr(`[warn] 无法连接服务端校验本地凭证（${err.message || err}），跳过授权流程。\n`);
        flushStderr(`       如需强制重新绑定，请运行：web-publisher login --force\n`);
        flushStdout(JSON.stringify({
          success: true,
          alreadyLoggedIn: true,
          verified: false,
          userId: existing.userId,
          apiKey: maskApiKey(existing.apiKey)
        }, null, 2) + '\n');
        process.exit(0);
      }
    }
  } else {
    flushStderr('[info] --force 已指定，将忽略本地凭证并重新发起授权。\n');
  }

  const toolsUrl = resolveToolsUrl().replace(/\/$/, '');

  const initResp = await callJson('POST', `${toolsUrl}/skill/device/init`, {}, {
    clientName: 'web-publisher-cli',
    clientVersion: PKG_VERSION
  });
  if (!initResp.res.ok) {
    console.error(JSON.stringify({
      success: false,
      error: initResp.data?.error || `device/init failed: ${initResp.res.status}`
    }));
    process.exit(1);
  }
  const { deviceCode, userCode, verifyUrl, expiresInSec } = initResp.data;
  const expiresAt = Date.now() + expiresInSec * 1000;

  // ---- 0.9.x 关键设计：checkpoint file，没有后台进程 ----
  //
  // 0.7.x blocked in foreground for 5 minutes → agent shells truncated output.
  // 0.8.x used a detached daemon (child_process) → harder to audit, extra failure modes.
  // 0.9.x checkpoint file: login writes pending JSON and exits; after the user
  //   confirms in the browser, login-status polls once and writes credentials.
  //
  // 优点：
  //   - 前台 ~0.3s 退出，wrapper 不会截断
  //   - 没有 child_process / detached 进程 / PID 文件 / SIGTERM trap
  //   - 没有 daemon 崩溃后留下的 stale-poller 状态
  //   - login-status 是验证登录是否完成的 single source of truth
  // 代价：
  //   - 用户 / AI 必须主动调一次 login-status；但 SKILL.md 的 AI 流程本来就
  //     这么写，所以 agent 用例零变化

  try {
    writeLoginPending({
      deviceCode,
      expiresAt,
      userCode,
      toolsUrl,
      startedAt: new Date().toISOString()
    });
  } catch (err) {
    // checkpoint 写不出来（磁盘满 / 权限问题）→ 直接报错让用户感知，
    // 否则后面 login-status 没有 deviceCode 没法 poll，体验更糟。
    console.error(JSON.stringify({
      success: false,
      error: `无法写入登录 checkpoint 文件 ${LOGIN_PENDING_PATH}：${err.message || err}`
    }));
    process.exit(1);
  }

  flushStderr('\n请在浏览器中打开以下链接，确认绑定到你的账号：\n');
  flushStderr(`  ${verifyUrl}\n`);
  flushStderr(`  绑定码：${userCode}\n`);
  flushStderr(`  有效期：${Math.round(expiresInSec / 60)} 分钟\n`);
  flushStderr('\n');
  flushStderr(`等用户在浏览器点完"确认绑定"后，运行下面任意一条命令完成登录：\n`);
  flushStderr(`  web-publisher login-status     ← 推荐。会自动拉取凭证并写入 ${CREDENTIALS_PATH}\n`);
  flushStderr(`  web-publisher whoami           ← 仅在已 login-status 成功后查询账号信息\n`);

  flushStdout(JSON.stringify({
    success: true,
    pendingCheckpoint: true,
    verifyUrl,
    userCode,
    expiresInSec,
    expiresAt,
    pendingPath: LOGIN_PENDING_PATH,
    credentialsPath: CREDENTIALS_PATH,
    instruction: '[AI必读] 请把 verifyUrl 完整 URL 原文交给用户，并附上 userCode。用户在浏览器点击确认后，调用 `web-publisher login-status` 完成登录（这条命令会做一次性 device-code 轮询并写入凭证）。不要再 await 这条 login 命令本身——它已经返回了。'
  }, null, 2) + '\n');

  process.exit(0);
}

// ----------------------------------------------------------------------------
// login-status (0.9.x checkpoint model)
// ----------------------------------------------------------------------------
//
// Decision tree:
//   1. Have credentials? → call /skill/whoami
//        ok          → state='logged-in'
//        401/403     → state='invalid-credentials' (apiKey revoked / rotated)
//        other / err → state='logged-in-unverified'
//   2. Have a pending checkpoint?
//        a. Date.now() > expiresAt → delete checkpoint, state='expired-pending'
//        b. POST /skill/device/poll (one-shot)
//              status='pending'   → state='awaiting-browser-confirm'
//              status='bound'     → write credentials.json, delete checkpoint,
//                                   state='logged-in' (re-run whoami below)
//              410                → delete checkpoint, state='expired-pending'
//              network err / 5xx  → state='polling-failed' (do NOT delete
//                                   checkpoint — caller can retry)
//   3. Neither → state='not-logged-in'.
//
// Exit code: 0 for logged-in / awaiting-browser-confirm (both healthy
// in-flight states); 1 otherwise.
async function runLoginStatus() {
  const status = {
    success: true,
    state: 'unknown',
    credentialsPath: CREDENTIALS_PATH,
    pendingPath: LOGIN_PENDING_PATH
  };

  const existing = loadCredentials();
  if (existing) {
    await fillStatusFromExisting(status, existing);
    emitStatus(status);
    return;
  }

  const pending = readLoginPending();
  if (!pending) {
    status.state = 'not-logged-in';
    status.note = '没有本地凭证，也没有进行中的登录请求，请运行：web-publisher login';
    emitStatus(status);
    return;
  }

  // Pending checkpoint exists.
  status.userCode = pending.userCode || null;
  status.startedAt = pending.startedAt || null;
  status.expiresAt = pending.expiresAt || null;

  if (typeof pending.expiresAt === 'number' && Date.now() > pending.expiresAt) {
    deleteLoginPending();
    status.state = 'expired-pending';
    status.note = `上一次 login 的 device-code 已过期（${new Date(pending.expiresAt).toISOString()}），请重新运行：web-publisher login`;
    emitStatus(status);
    return;
  }

  const toolsUrl = (pending.toolsUrl || resolveToolsUrl()).replace(/\/$/, '');
  let pollResp;
  try {
    pollResp = await callJson('POST', `${toolsUrl}/skill/device/poll`, {}, { deviceCode: pending.deviceCode });
  } catch (err) {
    status.state = 'polling-failed';
    status.note = `调用 /skill/device/poll 失败（${err.message || err}），稍后重试 login-status；或重新运行 login`;
    emitStatus(status);
    return;
  }

  if (pollResp.res.status === 410) {
    deleteLoginPending();
    status.state = 'expired-pending';
    status.note = pollResp.data?.error || '绑定码已过期或已被消费，请重新运行：web-publisher login';
    emitStatus(status);
    return;
  }

  if (!pollResp.res.ok) {
    status.state = 'polling-failed';
    status.note = `服务端返回 HTTP ${pollResp.res.status}；checkpoint 文件保留，稍后重试 login-status`;
    emitStatus(status);
    return;
  }

  const pollData = pollResp.data || {};
  if (pollData.status === 'pending') {
    status.state = 'awaiting-browser-confirm';
    status.note = '已检测到进行中的登录请求，但用户尚未在浏览器点击"确认绑定"。请催用户去浏览器完成授权，然后再次运行 login-status。';
    emitStatus(status);
    return;
  }

  if (pollData.status === 'bound') {
    let persisted = false;
    let persistError = null;
    try {
      writeCredentialsFile({
        userId: pollData.userId,
        apiKey: pollData.apiKey,
        apiUrl: pollData.apiUrl || '',
        toolsUrl: pollData.toolsUrl || toolsUrl,
        boundAt: new Date().toISOString()
      });
      persisted = true;
    } catch (err) {
      persistError = err;
    }

    if (persisted) {
      // Only retire the checkpoint after credentials.json is on disk.
      deleteLoginPending();
      // Re-load credentials and run the standard whoami + wechat-config check
      // so this branch produces exactly the same shape (state +
      // wechat.configured) as the "already had credentials" path. This is
      // what tells the AI whether to greet the user with "可以发布了" or with
      // "下一步：wechat config"——bound itself doesn't tell us anything about
      // the user's WeChat AppID/AppSecret state.
      const reloaded = loadCredentials();
      if (reloaded) {
        await fillStatusFromExisting(status, reloaded);
      } else {
        // Should be unreachable—we just wrote the file. If it happens, fall
        // back to a minimal logged-in payload so the user at least sees the
        // success and can debug locally.
        status.state = 'logged-in-unverified';
        status.userId = pollData.userId;
        status.name = pollData.name || null;
        status.apiKey = maskApiKey(pollData.apiKey);
        status.note = `凭证刚写入但 reload 失败；请手动运行 whoami / wechat status 验证`;
      }
    } else {
      status.state = 'persist-failed';
      status.userId = pollData.userId;
      status.note = `服务端已绑定，但写入 ${CREDENTIALS_PATH} 失败：${persistError?.message || persistError}。本次会话仍可临时使用环境变量：WEB_PUBLISHER_USER_ID='${pollData.userId}' WEB_PUBLISHER_API_KEY='${pollData.apiKey}'`;
    }
    emitStatus(status);
    return;
  }

  status.state = 'polling-failed';
  status.note = `服务端返回未知 status='${pollData.status}'，checkpoint 文件保留，稍后重试 login-status`;
  emitStatus(status);
}

async function fillStatusFromExisting(status, existing) {
  try {
    const { res, data } = await tools('GET', '/skill/whoami', null, existing);
    if (res.ok) {
      const who = data || {};
      const accountLabel = who.name || who.userId || existing.userId;
      const wechatConfigured = Boolean(who.wechat?.configured);

      status.userId = who.userId || existing.userId;
      status.name = who.name || null;
      status.apiKey = maskApiKey(existing.apiKey);
      status.source = existing.source;
      status.wechat = {
        configured: wechatConfigured,
        appId: who.wechat?.appId || null
      };

      // 拆开 "凭证有效" 和 "可以发布" 这两件事——AI 拿 logged-in 不能直接喊
      // "可以发文章了"，必须先看 wechat.configured。logged-in-no-wechat 是
      // 一个完全合法的中间态：账号已绑定，但还没接入公众号 AppID/AppSecret，
      // draft / publish 必然失败。
      if (wechatConfigured) {
        status.state = 'logged-in';
        status.note = `已登录，账号 = ${accountLabel}；公众号已配置（appId=${who.wechat?.appId || '?'}），可以使用 draft / publish / convert`;
      } else {
        status.state = 'logged-in-no-wechat';
        // 区分 "AppID 有 + AppSecret 缺" 和 "什么都没填"——前者文案要明确告诉用户
        // AppID 已留过，否则容易误以为之前填的东西丢了。
        const wechatGap = who.wechat?.appId
          ? `AppID=${who.wechat.appId} 已填，但 AppSecret 缺失或失效`
          : `AppID/AppSecret 都还没填`;
        status.note = `已登录，账号 = ${accountLabel}；但公众号配置不完整（${wechatGap}）。`
          + `下一步请由 AI agent 调用 \`scripts/run.js wechat config\`，把它输出的浏览器短链交给用户。`
          + `用户在浏览器里完成填写后再调一次 login-status 验证。`;
      }
      return;
    }
    if (res.status === 401 || res.status === 403) {
      status.state = 'invalid-credentials';
      status.userId = existing.userId;
      status.note = '本地凭证存在但服务端拒绝（apiKey 已失效），请运行：web-publisher login --force';
      return;
    }
    status.state = 'logged-in-unverified';
    status.userId = existing.userId;
    status.note = `whoami 返回 HTTP ${res.status}，凭证可能仍然有效；微信公众号配置状态未知`;
  } catch (err) {
    status.state = 'logged-in-unverified';
    status.userId = existing.userId;
    status.note = `无法连接服务端校验：${err.message || err}；微信公众号配置状态未知`;
  }
}

function emitStatus(status) {
  flushStderr(`login-status: ${status.state}\n`);
  if (status.note) flushStderr(`  ${status.note}\n`);
  if (status.userId) flushStderr(`  userId: ${status.userId}\n`);
  if (status.name) flushStderr(`  name:   ${status.name}\n`);
  if (status.wechat) {
    if (status.wechat.configured) {
      flushStderr(`  wechat: configured (appId=${status.wechat.appId || '?'})\n`);
    } else if (status.wechat.appId) {
      flushStderr(`  wechat: incomplete — AppID=${status.wechat.appId} 已填，AppSecret 缺失或失效\n`);
      flushStderr(`          → AI 应自行调用 \`wechat config\`（不是把命令贴给用户），把它输出的浏览器短链原文交给用户\n`);
    } else {
      flushStderr(`  wechat: NOT configured (AppID/AppSecret 都还没填)\n`);
      flushStderr(`          → AI 应自行调用 \`wechat config\`（不是把命令贴给用户），把它输出的浏览器短链原文交给用户\n`);
    }
  }
  if (status.userCode) flushStderr(`  userCode: ${status.userCode}\n`);
  if (status.expiresAt) flushStderr(`  expiresAt: ${new Date(status.expiresAt).toISOString()}\n`);

  flushStdout(JSON.stringify(status, null, 2) + '\n');
  // Healthy in-flight / "登录链路本身没问题" 的几个状态都返回 exit 0：
  //   - logged-in              凭证有效 + 公众号已配置（可以直接 publish）
  //   - logged-in-no-wechat    凭证有效但还没接公众号（需 wechat config 但
  //                            login 这一步本身是成功的）
  //   - awaiting-browser-confirm  device-code 还在 TTL 内等用户点确认
  // 其他都是 exit 1，方便外层 `set -e`。
  const ok = status.state === 'logged-in'
    || status.state === 'logged-in-no-wechat'
    || status.state === 'awaiting-browser-confirm';
  process.exit(ok ? 0 : 1);
}

async function runLogout() {
  const creds = loadCredentials();
  if (!creds) {
    process.stderr.write('当前未登录，无需注销。\n');
    return;
  }
  if (creds.source === 'env') {
    process.stderr.write('当前使用环境变量登录，请清除 WEB_PUBLISHER_USER_ID / WEB_PUBLISHER_API_KEY 环境变量。\n');
    return;
  }
  try {
    await tools('POST', '/skill/revoke', {}, creds);
  } catch (err) {
    process.stderr.write(`[warn] 远端撤销失败：${err.message}（仍会清理本地凭证）\n`);
  }
  deleteCredentialsFile();
  process.stderr.write('已清理本地凭证。\n');
  console.log(JSON.stringify({ success: true }, null, 2));
}

async function runWhoami() {
  const creds = requireCredentials();
  const { res, data } = await tools('GET', '/skill/whoami', null, creds);
  if (!res.ok) {
    console.error(JSON.stringify({ success: false, error: data?.error || `HTTP ${res.status}` }));
    process.exit(1);
  }

  // plan 字段是 Phase 0 之后服务端透传的：{ role, label, isAdmin, rewriteEngine }。
  // 老版本服务端可能没这字段，做防御式 fallback。`rewriteEngine` 直接告诉用户/AI
  // 当前等级走的是 markdown-ai-creator（创作合成）还是 markdown-ai-rewriter（伪改写）。
  const plan = data.plan && typeof data.plan === 'object' ? data.plan : null;
  if (plan) {
    const labelText = plan.label || plan.role || '未知';
    // isAdmin 是独立 flag，可叠加在任意 role 上（用于测试 / 让某个普通用户解锁 creator
    // 引擎）。只在 role !== 'admin' 时再追加 (管理员) 后缀，避免「管理员 (管理员)」。
    const adminMark = plan.isAdmin && plan.role !== 'admin' ? ' (管理员)' : '';
    const engine = plan.rewriteEngine || 'rewriter';
    process.stderr.write(`当前等级: ${labelText}${adminMark} · rewrite 引擎: ${engine}\n`);
  }

  console.log(JSON.stringify({
    success: true,
    source: creds.source,
    userId: data.userId,
    name: data.name,
    phone: data.phone,
    apiKey: data.apiKey,
    plan,
    wechat: data.wechat,
    credits: data.credits
  }, null, 2));
}

async function runWechatConfig() {
  const creds = requireCredentials();
  const { res, data } = await tools('POST', '/skill/wechat/link', {}, creds);
  if (!res.ok) {
    console.error(JSON.stringify({ success: false, error: data?.error || `HTTP ${res.status}` }));
    process.exit(1);
  }
  const link = pickLink(data);
  if (!link) {
    console.error(JSON.stringify({
      success: false,
      error: '服务器没有返回可打开的 AppID/AppSecret 配置短链',
      responseKeys: data && typeof data === 'object' ? Object.keys(data) : []
    }, null, 2));
    process.exit(1);
  }
  const serverIps = Array.isArray(data.serverIps) ? data.serverIps : [];
  process.stderr.write('\n请在浏览器中打开以下链接填写 AppID / AppSecret：\n');
  process.stderr.write(`  ${link}\n`);
  process.stderr.write(`  有效期: ${Math.round((data.expiresInSec || 600) / 60)} 分钟\n`);
  if (serverIps.length > 0) {
    process.stderr.write('\n⚠️  填写表单的同时，请到微信公众平台后台把以下服务器 IP\n');
    process.stderr.write('    加入"IP 白名单"，否则发布文章时微信会以"invalid IP"拒绝：\n');
    for (const ip of serverIps) process.stderr.write(`      ${ip}\n`);
    process.stderr.write('    入口：mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单\n');
  } else {
    process.stderr.write('\n[warn] 服务端未返回服务器 IP 列表（WECHAT_SERVER_IPS 可能没在 prod .env 里设置）；\n');
    process.stderr.write('       请提醒用户向管理员确认服务器出口 IP，并自行加入微信公众平台 IP 白名单。\n');
  }

  // 把 IP 白名单的指令烤进 instruction 字段：单纯依靠 stdout 的 serverIps[] 字段
  // AI 容易当成可选信息忽略；明确写在 instruction 里 AI 才会一并转达。
  const ipBlock = serverIps.length > 0
    ? `\n\n同时，请明确告诉用户：填表单的同时必须到微信公众平台后台 (mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单) 把以下 IP 加入白名单，否则文章发布时微信会以 "invalid IP" 拒绝调用：${serverIps.map(ip => `\n  - ${ip}`).join('')}`
    : `\n\n注意：服务端未返回服务器 IP 列表，请提醒用户向管理员获取服务器出口 IP，并自行加入微信公众平台 IP 白名单（mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单），否则发布会失败。`;

  console.log(JSON.stringify({
    success: true,
    url: link,
    serverIps,
    instruction: `[AI必读] 两件事都必须做完，缺一不可：（1）把下面这个完整 URL 原文粘贴给用户，不要改写、不要只输出 Markdown 超链接文字、不要用"点击此处"替代。用户需要在浏览器中打开这个 URL 填写 AppID/AppSecret。URL：${link}${ipBlock}`
  }, null, 2));
}

async function runWechatStatus() {
  const creds = requireCredentials();
  const { res, data } = await tools('GET', '/skill/whoami', null, creds);
  if (!res.ok) {
    console.error(JSON.stringify({ success: false, error: data?.error || `HTTP ${res.status}` }));
    process.exit(1);
  }
  console.log(JSON.stringify({
    success: true,
    configured: data.wechat?.configured ?? false,
    appId: data.wechat?.appId ?? null
  }, null, 2));
}

async function runWrapperConfig() {
  const creds = requireCredentials();
  const { res, data } = await tools('POST', '/skill/wrapper/link', {}, creds);
  if (!res.ok) {
    console.error(JSON.stringify({ success: false, error: data?.error || `HTTP ${res.status}` }));
    process.exit(1);
  }
  const link = pickLink(data);
  if (!link) {
    console.error(JSON.stringify({
      success: false,
      error: '服务器没有返回可打开的页眉/页脚配置短链',
      responseKeys: data && typeof data === 'object' ? Object.keys(data) : []
    }, null, 2));
    process.exit(1);
  }
  process.stderr.write('\n请在浏览器中打开以下链接编辑页眉/页脚：\n');
  process.stderr.write(`  ${link}\n`);
  process.stderr.write(`  有效期: ${Math.round((data.expiresInSec || 600) / 60)} 分钟\n`);
  console.log(JSON.stringify({
    success: true,
    url: link,
    instruction: `[AI必读] 你必须把下面这个完整 URL 原文粘贴给用户，不要改写、不要只输出 Markdown 超链接文字、不要用"点击此处"替代。用户需要在浏览器中打开这个 URL 填写页眉/页脚。URL：${link}`
  }, null, 2));
}

async function runWrapperStatus() {
  const creds = requireCredentials();
  const { res, data } = await tools('GET', '/skill/wrapper/status', null, creds);
  if (!res.ok) {
    console.error(JSON.stringify({ success: false, error: data?.error || `HTTP ${res.status}` }));
    process.exit(1);
  }
  console.log(JSON.stringify({
    success: true,
    configured: data.configured,
    enabled: data.enabled,
    headerLen: data.headerLen,
    footerLen: data.footerLen,
    version: data.version,
    updatedAt: data.updatedAt
  }, null, 2));
}

async function runWrapperToggle(enabled) {
  const creds = requireCredentials();
  const { res, data } = await tools('POST', '/skill/wrapper/toggle', { enabled }, creds);
  if (!res.ok) {
    console.error(JSON.stringify({ success: false, error: data?.error || `HTTP ${res.status}` }));
    process.exit(1);
  }
  process.stderr.write(`页眉页脚已${enabled ? '启用' : '关闭'}。\n`);
  console.log(JSON.stringify({ success: true, enabled: data.enabled }, null, 2));
}

// ----------------------------------------------------------------------------
// Help / dispatch
// ----------------------------------------------------------------------------

function showHelp() {
  console.log(`
web-publisher v${PKG_VERSION} — 将网页文章 / 本地文档发布到微信公众号

账号管理（首次使用）:
  login [--force]    生成一次性授权链接；命令立即返回，把 deviceCode 写到
                     ~/.web-publisher/login-pending.json 等待用户在浏览器
                     完成授权。已登录时会自动跳过；--force 可强制重新绑定。
  login-status       完成登录的"第二步"：读取 pending 文件 -> 一次性轮询服
                     务端 -> 写凭证。也用于查询当前状态：not-logged-in /
                     awaiting-browser-confirm / logged-in / expired-pending
                     / invalid-credentials / polling-failed。是 login 之后
                     验证是否绑定成功的唯一命令。
  logout             撤销当前 apiKey 并清除本地凭证
  whoami             查看当前账号、apiKey（已脱敏）与微信配置状态

公众号配置:
  wechat config      生成一次性短链，在浏览器里填写 AppID/AppSecret
  wechat status      查看是否已配置微信公众号

页眉页脚（专业版及以上可用，每篇文章自动加前后内容）:
  wrapper config     生成一次性短链，在浏览器里编辑页眉/页脚
  wrapper status     查看页眉页脚字数与是否启用
  wrapper on         启用页眉页脚（要求已配置页眉或页脚）
  wrapper off        关闭页眉页脚（保留已存内容，下次开启即可恢复）

发布（<input> 可以是 URL 或本地文件路径，本地文件支持 PDF/DOCX/PPTX/XLSX/EPUB/...）:
  draft   <input>    保存为草稿
  publish <input>    直接发布
  ppt draft <file>   PDF/PPTX → 公众号草稿（POST /ppt/jobs）
  ppt publish <file> PDF/PPTX → 直接发布公众号
                     PDF 默认每页成图；--extract-text PPTX 抽文字；--as-markdown 直接 markitdown。
                     PPTX 走 markitdown。带 --style / --cover 等高级改写时改走 /pipeline。
  status  <jobId>    查询任务状态（默认紧凑摘要；--json 输出原始 JSON）
  jobs               列出最近任务（紧凑摘要）
                     选项: --status pending|processing|completed|failed
                          --type pipeline|ppt|convert  --limit <n>  --json
  wait <id> [id...]  阻塞等待一个或多个任务完成（消费 SSE 流）
                     全部 completed 退出码 0；任一 failed 退出码 1。

并发发布（短时间发多篇时强烈推荐）:
  draft / publish 加 --detach：提交后立刻返回 jobId，不在前台 poll。
  例：6 主题各 draft 一份再统一等：
      for t in default blackink greenmint orangesun purplerain redruby; do
        web-publisher draft "$URL" --theme $t --detach
      done | jq -r '.jobId' > /tmp/jids
      web-publisher wait $(cat /tmp/jids)

文档转 Markdown（不发布，只把任意文档拿成 markdown 文本）:
  convert <input>    本地文件 / URL → markdown
                     选项: --out <file> 写到文件; --async 走异步任务;
                          --timeout <ms> 单次转换上限（封顶 600000）

发布选项:
  --theme <id>       主题（默认: blackink）
                     可选: blackink(墨黑) / default(默认) / orangesun(橙日)
                           redruby(红宝石) / greenmint(薄荷绿) / purplerain(紫雨)
  --rewrite          启用 AI 改写（PDF 会自动切到 markdown 模式）
  --as-markdown      PDF 发公众号时强制原 PDF markitdown（不经 pingPPT）
  --page-images      PDF 每页渲染 PNG（与默认相同，显式指定时用）
  --extract-text     PDF 发公众号时 pingPPT→PPTX 抽可编辑文字（--convert-only 同义）
  --style <style>    改写风格: casual / formal / technical / creative
  --prompt <text>    自定义改写提示

图片处理选项（仅 creator 引擎生效，需 pro/ultra/admin 等级；要求 --rewrite 同时开启）:
  --cover                    生成封面图（消耗 minimax image-01 配额，~ 0.05 元/张；
                             v0.9.7+ 起 server 会把 t2i URL 下载到本地图床
                             避免 24h 后图片过期）
  --cover-style <text>       封面图风格 hint，例如 "赛博朋克 霓虹"
  --regenerate-images        把疑似带水印 / 文字截图 的正文图换成 t2i 重生成
  --no-image-classify        关闭启发式分类（默认开 —— 不可达 / icon 自动 caption-only）
  --enable-ocr               启用 OCR 增强水印识别（首次模型加载较慢，~30s）

标题与引用（v0.9.7+，仅 creator 引擎，要求 --rewrite）:
  --lock-title               锁死最终标题（适用于热搜稿、SEO 命题作文场景）。
                             prompt 里加硬约束 + sanitize 后保险替换 H1，
                             即使 LLM 改了标题也会被强制改回。要求输入有 title。
  --append-source-footer <auto|always|never>
                             控制文末"原文"链接列表追加策略，默认 auto：
                             - auto：LLM 一份 source 都没引用时才追加
                             - always：每次都追加（合规 / 法律审计场景）
                             - never：完全关掉（翻译 / 二创场景）

成本与诊断（v0.9.7+ 自动展示）:
  draft/publish 完成时返回里会带：
  - cost.estimatedRMB   本次预估花费（粗略，仅 LLM tokens + t2i 图片单价）
  - cost.tokens.total   LLM 实际 token 数
  - cost.imagesGenerated 本次生成了几张图（cover + regenerate）
  - warnings[]          markdown-ai-creator 的告警，如截断 / lockTitle 改写
  - imageStabilize     {downloaded, failed, skipped} —— 临时图床转存结果
  - imageClassify      {safe, has-watermark, ...} —— 启发式分类摘要

计费（与 /pipeline 一致）:
  draft / publish / convert 各 1 credit；失败不扣；不发用户通知

环境变量（可选，优先级高于本地凭证文件）:
  WEB_PUBLISHER_TOOLS_URL  账号 API 地址（默认 ${DEFAULT_TOOLS_URL}）
  WEB_PUBLISHER_API_URL    pipeline API 地址（登录后会自动写入凭证）
  WEB_PUBLISHER_USER_ID    用户 ID（如 usr_xxxx）
  WEB_PUBLISHER_API_KEY    API Key

凭证文件: ${CREDENTIALS_PATH} (mode 0600)
`);
}

const command = process.argv[2];
const subcommand = process.argv[3];
const args = process.argv.slice(3);

(async () => {
  try {
    switch (command) {
      case 'login':
        await runLogin(args);
        break;
      case 'login-status':
        await runLoginStatus();
        break;
      case 'logout':
        await runLogout();
        break;
      case 'whoami':
        await runWhoami();
        break;
      case 'wechat':
        if (subcommand === 'config') {
          await runWechatConfig();
        } else if (subcommand === 'status') {
          await runWechatStatus();
        } else {
          console.error(JSON.stringify({ success: false, error: `Unknown wechat subcommand: ${subcommand || '(none)'}\n用法：web-publisher wechat config|status` }));
          process.exit(1);
        }
        break;
      case 'wrapper':
        if (subcommand === 'config') {
          await runWrapperConfig();
        } else if (subcommand === 'status') {
          await runWrapperStatus();
        } else if (subcommand === 'on' || subcommand === 'enable') {
          await runWrapperToggle(true);
        } else if (subcommand === 'off' || subcommand === 'disable') {
          await runWrapperToggle(false);
        } else {
          console.error(JSON.stringify({ success: false, error: `Unknown wrapper subcommand: ${subcommand || '(none)'}\n用法：web-publisher wrapper config|status|on|off` }));
          process.exit(1);
        }
        break;
      case 'publish':
        await runPublish('publish', args);
        break;
      case 'draft':
        await runPublish('draft', args);
        break;
      case 'ppt':
        if (subcommand === 'draft') {
          await runPpt('draft', args.slice(1));
        } else if (subcommand === 'publish') {
          await runPpt('publish', args.slice(1));
        } else {
          console.error(JSON.stringify({
            success: false,
            error: `Unknown ppt subcommand: ${subcommand || '(none)'}\n用法：web-publisher ppt draft|publish <PDF|PPTX>`
          }));
          process.exit(1);
        }
        break;
      case 'convert':
        await runConvert(args);
        break;
      case 'status':
        await runStatus(args);
        break;
      case 'jobs':
        await runJobs(args);
        break;
      case 'wait':
        await runWait(args);
        break;
      case 'help':
      case '--help':
      case '-h':
      case undefined:
        showHelp();
        break;
      default:
        console.error(JSON.stringify({ success: false, error: `Unknown command: ${command}` }));
        process.exit(1);
    }
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: err.message || String(err) }));
    process.exit(1);
  }
})();
