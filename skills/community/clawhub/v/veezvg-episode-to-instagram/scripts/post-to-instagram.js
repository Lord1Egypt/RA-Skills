#!/usr/bin/env node
/**
 * post-to-instagram.js — Prepare an Instagram post/Reel draft via OpenClaw browser automation.
 *
 * Usage:
 *   node post-to-instagram.js <media-path-or-dir> <caption-text-file> [--dry-run] [--post] [--type post|reel|auto]
 *
 * Supported inputs:
 * - A directory of images for a carousel/feed post
 * - A single image for a feed post
 * - A single .mp4/.mov file for a Reel/video post
 *
 * Notes:
 * - OpenClaw browser uploads only accept files staged under /tmp/openclaw/uploads.
 * - The script stops before publishing unless --post is explicitly passed.
 * - Instagram's UI changes often, so this script prefers resilient fallbacks over a single hard-coded route.
 */

const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const mediaInput = process.argv[2];
const captionFile = process.argv[3];
const dryRun = process.argv.includes('--dry-run');
const doPost = process.argv.includes('--post');

const typeIndex = process.argv.indexOf('--type');
const requestedType = typeIndex >= 0 ? process.argv[typeIndex + 1] : 'auto';

const IMAGE_EXTENSIONS = new Set(['.png', '.jpg', '.jpeg']);
const VIDEO_EXTENSIONS = new Set(['.mp4', '.mov', '.m4v']);
const OPENCLAW_UPLOAD_ROOT = '/tmp/openclaw/uploads';
const VIDEO_DRAFT_SCRIPT = path.resolve(__dirname, 'prepare-instagram-video-draft.js');
const PREVIEW_CAPTURE_SCRIPT = path.resolve(__dirname, 'capture-instagram-preview.js');

if (!mediaInput || !captionFile) {
  console.error(
    'Usage: node post-to-instagram.js <media-path-or-dir> <caption-text-file> [--dry-run] [--post] [--type post|reel|auto]'
  );
  process.exit(1);
}

if (!['auto', 'post', 'reel'].includes(requestedType || '')) {
  console.error('Invalid --type value. Expected post, reel, or auto.');
  process.exit(1);
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function run(cmd, options = {}) {
  const { allowFailure = false } = options;
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
  } catch (error) {
    if (allowFailure) {
      return {
        ok: false,
        stdout: (error.stdout || '').toString().trim(),
        stderr: (error.stderr || '').toString().trim(),
        error
      };
    }
    console.error(`Command failed: ${cmd}`);
    console.error((error.stderr || error.message || '').toString());
    throw error;
  }
}

function browser(args, options = {}) {
  const cmd = `openclaw browser ${args.map(shellQuote).join(' ')}`;
  return run(cmd, options);
}

function runNodeScript(scriptPath, args) {
  const result = spawnSync('node', [scriptPath, ...args], {
    encoding: 'utf8'
  });

  const stdout = (result.stdout || '').trim();
  const stderr = (result.stderr || '').trim();

  if (result.status !== 0) {
    const error = new Error(`Script failed: ${path.basename(scriptPath)}`);
    error.details = {
      scriptPath,
      args,
      stdout,
      stderr,
      exitCode: result.status
    };
    throw error;
  }

  return {
    stdout,
    stderr
  };
}

function parseJsonFromText(text) {
  const trimmed = String(text || '').trim();
  if (!trimmed) return null;

  try {
    return JSON.parse(trimmed);
  } catch {}

  const lines = trimmed.split('\n').map((line) => line.trim()).filter(Boolean);
  for (let index = lines.length - 1; index >= 0; index -= 1) {
    try {
      return JSON.parse(lines[index]);
    } catch {}
  }

  return null;
}

function parseOpenedTargetId(openOutput) {
  const match = String(openOutput || '').match(/\bid:\s*([A-Z0-9]+)/i);
  return match ? match[1] : '';
}

function capturePreview(targetId) {
  if (!fs.existsSync(PREVIEW_CAPTURE_SCRIPT)) {
    return {
      ok: false,
      error: `Missing preview capture helper: ${PREVIEW_CAPTURE_SCRIPT}`
    };
  }

  const helperArgs = [];
  if (targetId) {
    helperArgs.push('--target-id', targetId);
  }

  try {
    const helperRun = runNodeScript(PREVIEW_CAPTURE_SCRIPT, helperArgs);
    const parsed = parseJsonFromText(helperRun.stdout);
    if (!parsed || !parsed.ok || !parsed.screenshotPath) {
      return {
        ok: false,
        error: helperRun.stdout || helperRun.stderr || 'Preview capture helper did not return a screenshot path.'
      };
    }
    return {
      ok: true,
      screenshot: parsed.screenshotPath,
      helper: parsed
    };
  } catch (error) {
    const details = error.details || {};
    return {
      ok: false,
      error: details.stdout || details.stderr || error.message || String(error)
    };
  }
}

function ensureFile(filePath) {
  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    throw new Error(`Expected file does not exist: ${filePath}`);
  }
}

function collectMedia(inputPath) {
  const resolvedInput = path.resolve(inputPath);
  if (!fs.existsSync(resolvedInput)) {
    throw new Error(`Media path does not exist: ${resolvedInput}`);
  }

  const stat = fs.statSync(resolvedInput);
  if (stat.isDirectory()) {
    const files = fs
      .readdirSync(resolvedInput)
      .filter((entry) => IMAGE_EXTENSIONS.has(path.extname(entry).toLowerCase()))
      .sort()
      .map((entry) => path.join(resolvedInput, entry));

    if (files.length === 0) {
      throw new Error(`No image files found in directory: ${resolvedInput}`);
    }

    return {
      mediaKind: 'images',
      sourceType: 'directory',
      files
    };
  }

  if (!stat.isFile()) {
    throw new Error(`Unsupported media input: ${resolvedInput}`);
  }

  const extension = path.extname(resolvedInput).toLowerCase();
  if (VIDEO_EXTENSIONS.has(extension)) {
    return {
      mediaKind: 'video',
      sourceType: 'file',
      files: [resolvedInput]
    };
  }

  if (IMAGE_EXTENSIONS.has(extension)) {
    return {
      mediaKind: 'images',
      sourceType: 'file',
      files: [resolvedInput]
    };
  }

  throw new Error(`Unsupported media extension: ${extension}`);
}

function deducePostType(mediaKind, explicitType) {
  if (explicitType && explicitType !== 'auto') {
    return explicitType;
  }
  return mediaKind === 'video' ? 'reel' : 'post';
}

function sanitizeBaseName(filePath, index) {
  const ext = path.extname(filePath).toLowerCase();
  const stem = path
    .basename(filePath, path.extname(filePath))
    .replace(/[^a-zA-Z0-9._-]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
  const safeStem = stem || `upload-${index + 1}`;
  return `${String(index + 1).padStart(2, '0')}-${safeStem}${ext}`;
}

function stageUploads(files) {
  fs.mkdirSync(OPENCLAW_UPLOAD_ROOT, { recursive: true });
  const stageDir = path.join(OPENCLAW_UPLOAD_ROOT, `instagram-${Date.now()}`);
  fs.mkdirSync(stageDir, { recursive: true });

  const stagedFiles = files.map((filePath, index) => {
    ensureFile(filePath);
    const destination = path.join(stageDir, sanitizeBaseName(filePath, index));
    fs.copyFileSync(filePath, destination);
    return destination;
  });

  return { stageDir, stagedFiles };
}

function browserEval(fnSource, options = {}) {
  return browser(['evaluate', '--fn', fnSource], options);
}

function browserWait(ms) {
  browser(['wait', '--time', String(ms)], { allowFailure: true });
}

function interactiveSnapshot() {
  return browser(['snapshot', '--interactive', '--compact', '--depth', '6']);
}

function snapshotEntries(snapshotText) {
  return String(snapshotText || '')
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const refMatch = line.match(/\[ref=(e\d+)\]/);
      const quoted = line.match(/"([^"]+)"/);
      return {
        raw: line,
        ref: refMatch ? refMatch[1] : null,
        label: quoted ? quoted[1] : '',
        labelLower: quoted ? quoted[1].toLowerCase() : ''
      };
    });
}

function findRef(snapshotText, candidates) {
  const entries = snapshotEntries(snapshotText);
  const normalizedCandidates = candidates.map((candidate) => String(candidate).toLowerCase());

  for (const candidate of normalizedCandidates) {
    const exact = entries.find((entry) => entry.ref && entry.labelLower === candidate);
    if (exact) return exact.ref;

    const startsWith = entries.find((entry) => entry.ref && entry.labelLower.startsWith(candidate + ' '));
    if (startsWith) return startsWith.ref;

    const contains = entries.find((entry) => entry.ref && entry.labelLower.includes(candidate));
    if (contains) return contains.ref;
  }

  return null;
}

function findExactRef(snapshotText, candidates) {
  const entries = snapshotEntries(snapshotText);
  const normalizedCandidates = candidates.map((candidate) => String(candidate).toLowerCase());
  const match = entries.find((entry) => entry.ref && normalizedCandidates.includes(entry.labelLower));
  return match ? match.ref : null;
}

function clickRef(ref) {
  return browser(['click', ref]);
}

function ensureCreateModalOpen(postType) {
  let snapshot = interactiveSnapshot();
  const createAlreadyOpen = findExactRef(snapshot, ['select from computer', 'try again']);
  if (createAlreadyOpen) {
    return snapshot;
  }

  let createRef = findExactRef(snapshot, ['new post create', 'new post']);
  if (!createRef) {
    createRef = findRef(snapshot, ['create']);
  }
  if (!createRef) {
    const bodyText = browserEval('() => document.body ? document.body.innerText : ""', { allowFailure: true });
    if (String(bodyText).includes('Log in') || String(bodyText).includes('Password')) {
      throw new Error('Instagram login is required in the OpenClaw browser profile before automation can continue.');
    }
    throw new Error('Could not find Instagram Create/New post entrypoint.');
  }

  clickRef(createRef);
  browserWait(1500);
  snapshot = interactiveSnapshot();

  const postCandidates = postType === 'reel'
    ? ['reel', 'video reel', 'post post', 'post']
    : ['post post', 'post', 'photo'];
  let postRef = findExactRef(snapshot, postCandidates);
  if (!postRef) {
    postRef = findRef(snapshot, postCandidates);
  }
  if (!postRef) {
    return snapshot;
  }

  clickRef(postRef);
  browserWait(1500);
  return interactiveSnapshot();
}

function uploadResponseState(result) {
  if (typeof result === 'string') {
    return {
      ok: true,
      stdout: result,
      stderr: ''
    };
  }

  const combined = `${result.stdout || ''}\n${result.stderr || ''}`;
  if (/Cannot transfer files larger than 50Mb/i.test(combined)) {
    return {
      ok: false,
      fatal: true,
      stdout: result.stdout,
      stderr: result.stderr
    };
  }

  if (/gateway timeout/i.test(combined)) {
    return {
      ok: true,
      pending: true,
      stdout: result.stdout,
      stderr: result.stderr
    };
  }

  return {
    ok: false,
    stdout: result.stdout,
    stderr: result.stderr
  };
}

function tryDirectUpload(stagedFiles) {
  return uploadResponseState(
    browser(['upload', '--element', 'input[type="file"]', ...stagedFiles], { allowFailure: true })
  );
}

function tryArmedUpload(stagedFiles) {
  const armed = browser(['upload', ...stagedFiles], { allowFailure: true });
  if (!armed.ok) {
    return uploadResponseState(armed);
  }

  const fn = `() => {
    const clickNode = (node) => {
      if (!node || typeof node.dispatchEvent !== 'function') return false;
      node.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      return true;
    };
    const nodes = Array.from(document.querySelectorAll('button, div[role="button"], span'))
      .map((node) => node.closest('button, div[role="button"]') || node)
      .filter(Boolean);
    const labels = [
      'Select from computer',
      'Select From Computer',
      'Select from device',
      'Choose from computer'
    ];
    for (const label of labels) {
      const match = nodes.find((node) => (node.textContent || '').includes(label));
      if (match) {
        clickNode(match);
        return 'clicked:' + label;
      }
    }
    return 'chooser-trigger-not-found';
  }`;

  const clickResult = browserEval(fn, { allowFailure: true });
  const clickText = typeof clickResult === 'string' ? clickResult : clickResult.stdout;
  return {
    ok: !(clickResult && clickResult.ok === false) && clickText !== 'chooser-trigger-not-found',
    stdout: clickText,
    stderr: typeof clickResult === 'string' ? '' : clickResult.stderr
  };
}

function waitForComposerReady(mediaKind) {
  const timeoutMs = mediaKind === 'video' ? 180000 : 60000;
  const startedAt = Date.now();
  let lastSnapshot = '';

  while (Date.now() - startedAt < timeoutMs) {
    lastSnapshot = interactiveSnapshot();
    const fieldState = captionFieldState();
    const fieldStateText = typeof fieldState === 'string' ? fieldState : fieldState.stdout || '';

    if (lastSnapshot.includes('Try again') || lastSnapshot.toLowerCase().includes('something went wrong')) {
      return { ok: false, reason: 'instagram-upload-error', snapshot: lastSnapshot };
    }

    if (fieldStateText.includes('"kind":"textarea"') || fieldStateText.includes('"kind":"editable"')) {
      return { ok: true, snapshot: lastSnapshot, fieldState: fieldStateText };
    }

    if (findExactRef(lastSnapshot, ['next', 'continue', 'done', 'share', 'publish'])) {
      return { ok: true, snapshot: lastSnapshot, fieldState: fieldStateText };
    }

    browserWait(5000);
  }

  return { ok: false, reason: 'timeout-waiting-for-composer', snapshot: lastSnapshot };
}

function advanceComposer() {
  const snapshot = interactiveSnapshot();
  const ref = findExactRef(snapshot, ['next', 'continue', 'done']);
  if (ref) {
    clickRef(ref);
    return `clicked-ref:${ref}`;
  }

  const fn = `() => {
    const clickNode = (node) => {
      if (!node || typeof node.dispatchEvent !== 'function') return false;
      node.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      return true;
    };
    const labels = ['Next', 'Continue', 'Done'];
    const nodes = Array.from(document.querySelectorAll('button, div[role="button"]'))
      .filter(Boolean);
    for (const label of labels) {
      const match = nodes.find((node) => (node.textContent || '').trim() === label);
      if (match) {
        clickNode(match);
        return 'clicked:' + label;
      }
    }
    return 'not-found';
  }`;

  return browserEval(fn, { allowFailure: true });
}

function preferOriginalCrop() {
  const snapshot = interactiveSnapshot();
  const ref = findExactRef(snapshot, ['select crop']);
  if (ref) {
    clickRef(ref);
    return `clicked-ref:${ref}`;
  }

  const fn = `() => {
    const clickNode = (node) => {
      if (!node || typeof node.dispatchEvent !== 'function') return false;
      node.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      return true;
    };
    const nodes = Array.from(document.querySelectorAll('button, div[role="button"]')).filter(Boolean);
    const match = nodes.find((node) => {
      const text = (node.textContent || '').trim();
      const aria = node.getAttribute('aria-label') || '';
      return text === 'Select crop' || aria === 'Select crop';
    });
    if (match) {
      clickNode(match);
      return 'clicked:Select crop';
    }
    return 'not-found';
  }`;

  return browserEval(fn, { allowFailure: true });
}

function captionFieldState() {
  const fn = `() => {
    const textarea = document.querySelector('textarea[aria-label*="caption" i]')
      || document.querySelector('textarea[placeholder*="caption" i]')
      || document.querySelector('textarea');
    if (textarea) {
      return JSON.stringify({
        kind: 'textarea',
        value: textarea.value || '',
        placeholder: textarea.getAttribute('placeholder') || ''
      });
    }

    const editable = Array.from(document.querySelectorAll('[contenteditable="true"]')).find((node) => {
      const label = node.getAttribute('aria-label') || '';
      const placeholder = node.getAttribute('data-placeholder') || '';
      const text = (node.textContent || '').trim();
      return /caption/i.test(label) || /caption/i.test(placeholder) || text === '';
    });

    if (editable) {
      return JSON.stringify({
        kind: 'editable',
        value: editable.textContent || ''
      });
    }

    return JSON.stringify({ kind: 'missing' });
  }`;

  return browserEval(fn, { allowFailure: true });
}

function fillCaption(caption) {
  const fn = `() => {
    const caption = ${JSON.stringify(caption)};
    const textarea = document.querySelector('textarea[aria-label*="caption" i]')
      || document.querySelector('textarea[placeholder*="caption" i]')
      || document.querySelector('textarea');

    if (textarea) {
      const proto = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')
        || Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
      if (proto && proto.set) {
        proto.set.call(textarea, caption);
      } else {
        textarea.value = caption;
      }
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      textarea.dispatchEvent(new Event('change', { bubbles: true }));
      return JSON.stringify({ ok: true, kind: 'textarea', preview: textarea.value.slice(0, 80) });
    }

    const editable = Array.from(document.querySelectorAll('[contenteditable="true"]')).find((node) => {
      const label = node.getAttribute('aria-label') || '';
      const placeholder = node.getAttribute('data-placeholder') || '';
      const text = (node.textContent || '').trim();
      return /caption/i.test(label) || /caption/i.test(placeholder) || text === '';
    });

    if (editable) {
      editable.focus();
      editable.textContent = caption;
      editable.dispatchEvent(new InputEvent('input', { bubbles: true, data: caption, inputType: 'insertText' }));
      editable.dispatchEvent(new Event('change', { bubbles: true }));
      return JSON.stringify({ ok: true, kind: 'editable', preview: (editable.textContent || '').slice(0, 80) });
    }

    return JSON.stringify({ ok: false, error: 'caption-field-not-found' });
  }`;

  return browserEval(fn);
}

function clickShare() {
  const snapshot = interactiveSnapshot();
  const ref = findExactRef(snapshot, ['share', 'publish', 'post']);
  if (ref) {
    clickRef(ref);
    return `clicked-ref:${ref}`;
  }

  const fn = `() => {
    const clickNode = (node) => {
      if (!node || typeof node.dispatchEvent !== 'function') return false;
      node.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
      node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      return true;
    };
    const labels = ['Share', 'Post', 'Publish'];
    const nodes = Array.from(document.querySelectorAll('button, div[role="button"]'))
      .filter(Boolean);
    for (const label of labels) {
      const match = nodes.find((node) => (node.textContent || '').trim() === label);
      if (match) {
        clickNode(match);
        return 'clicked:' + label;
      }
    }
    return 'not-found';
  }`;

  return browserEval(fn);
}

function handleVideoDraft({ stagedFiles, captionFilePath, captionText, doPostNow, targetId }) {
  if (!fs.existsSync(VIDEO_DRAFT_SCRIPT)) {
    throw new Error(`Missing video draft helper: ${VIDEO_DRAFT_SCRIPT}`);
  }

  const helperArgs = [stagedFiles[0], captionFilePath];
  if (targetId) {
    helperArgs.push('--target-id', targetId);
  }
  if (doPostNow) {
    helperArgs.push('--post');
  }

  const helperRun = runNodeScript(VIDEO_DRAFT_SCRIPT, helperArgs);
  const parsed = parseJsonFromText(helperRun.stdout);
  if (!parsed || !parsed.ok) {
    throw new Error(`Video draft helper did not return a success payload: ${helperRun.stdout || helperRun.stderr}`);
  }

  console.log(`  Video draft helper upload result: ${parsed.uploadResult}`);
  console.log(`  Video draft helper crop result: ${parsed.cropResult}`);
  console.log(`  Video draft helper caption kind: ${parsed.captionKind}`);
  if (parsed.screenshot) {
    console.log(`  Preview: ${parsed.screenshot}`);
  }

  if (!doPostNow) {
    console.log('\n========================================');
    console.log('==> STOPPED BEFORE POSTING');
    console.log('==> Review the preview screenshot path above');
    console.log('==> Run with --post flag to actually publish');
    console.log('========================================');
  }

  console.log(
    JSON.stringify({
      status: doPostNow ? 'posted' : 'preview',
      postType: 'reel',
      mediaKind: 'video',
      stagedFiles,
      captionFile: captionFilePath,
      caption: captionText,
      screenshot: parsed.screenshot,
      helper: parsed
    })
  );
}

function main() {
  const media = collectMedia(mediaInput);
  const postType = deducePostType(media.mediaKind, requestedType);
  const caption = fs.readFileSync(captionFile, 'utf8').trim();
  const { stageDir, stagedFiles } = stageUploads(media.files);

  console.log(`==> Found ${media.files.length} media file(s)`);
  console.log(`==> Media kind: ${media.mediaKind}`);
  console.log(`==> Composer type: ${postType}`);
  console.log(`==> Caption length: ${caption.length} chars`);
  console.log(`==> Staged for OpenClaw upload: ${stageDir}`);

  if (dryRun) {
    console.log('\n==> DRY RUN — not opening Instagram.');
    stagedFiles.forEach((filePath, index) => console.log(`  ${index + 1}. ${filePath}`));
    console.log(`\n==> Caption:\n${caption}`);
    return;
  }

  console.log('==> Starting OpenClaw browser...');
  browser(['start']);

  console.log('==> Opening Instagram...');
  const openOutput = browser(['open', 'https://www.instagram.com/']);
  const targetId = parseOpenedTargetId(openOutput);
  browserWait(3000);

  console.log('==> Opening the create flow...');
  const modalSnapshot = ensureCreateModalOpen(postType);
  const selectFromComputerRef = findExactRef(modalSnapshot, ['select from computer']);
  const retryRef = findExactRef(modalSnapshot, ['try again']);
  console.log(
    `  Create modal state: ${selectFromComputerRef ? 'select-from-computer-visible' : retryRef ? 'retry-visible' : 'opened'}`
  );
  if (!selectFromComputerRef && retryRef) {
    throw new Error('Instagram create modal opened in an error state before upload.');
  }

  if (!selectFromComputerRef && !retryRef) {
    console.log('  Create modal snapshot did not show the upload button yet; continuing with direct file input detection.');
  }

  browserWait(1500);

  if (media.mediaKind === 'video') {
    console.log('==> Preparing video draft via CDP-backed helper...');
    handleVideoDraft({
      stagedFiles,
      captionFilePath: path.resolve(captionFile),
      captionText: caption,
      doPostNow: doPost,
      targetId
    });
    return;
  }

  console.log('==> Uploading media...');
  let uploadResult = tryDirectUpload(stagedFiles);
  if (uploadResult && uploadResult.ok === false) {
    console.log('  Direct input upload failed, falling back to armed chooser...');
    uploadResult = tryArmedUpload(stagedFiles);
  }

  if (uploadResult && uploadResult.ok === false) {
    throw new Error(
      `OpenClaw upload failed. stdout=${uploadResult.stdout || '(empty)'} stderr=${uploadResult.stderr || '(empty)'}`
    );
  }

  console.log(`  Upload result: ${typeof uploadResult === 'string' ? uploadResult : uploadResult.stdout || 'ok'}`);

  console.log('==> Waiting for Instagram to ingest the upload...');
  const composerState = waitForComposerReady(media.mediaKind);
  if (!composerState.ok) {
    throw new Error(
      `Instagram did not reach a stable composer state: ${composerState.reason}. Snapshot=${composerState.snapshot || '(empty)'}`
    );
  }

  console.log('==> Preserving original crop/aspect ratio...');
  const cropResult = preferOriginalCrop();
  const cropText = typeof cropResult === 'string' ? cropResult : cropResult.stdout || '';
  if (cropText && cropText !== 'not-found') {
    console.log(`  Crop result: ${cropText}`);
    browserWait(1000);
  } else {
    console.log('  Crop toggle not found; leaving Instagram default crop as-is.');
  }

  for (let index = 0; index < 5; index += 1) {
    const fieldState = captionFieldState();
    const fieldStateText = typeof fieldState === 'string' ? fieldState : fieldState.stdout || '';
    if (fieldStateText.includes('"kind":"textarea"')) {
      break;
    }
    if (fieldStateText.includes('"kind":"editable"')) {
      break;
    }

    const nextResult = advanceComposer();
    const nextText = typeof nextResult === 'string' ? nextResult : nextResult.stdout || '';
    if (!nextText || nextText === 'not-found') {
      break;
    }
    console.log(`  Advanced composer: ${nextText}`);
    browserWait(2500);
  }

  console.log('==> Filling caption...');
  const captionResult = fillCaption(caption);
  console.log(`  Caption result: ${captionResult}`);
  if (!String(captionResult).includes('"ok":true')) {
    throw new Error(`Caption did not stick in the Instagram composer: ${captionResult}`);
  }

  browserWait(1000);

  console.log('==> Capturing preview screenshot...');
  const preview = capturePreview(targetId);
  const screenshot = preview.ok ? preview.screenshot : null;
  if (screenshot) {
    console.log(`  Preview: ${screenshot}`);
  } else {
    console.log(`  Preview capture skipped: ${preview.error}`);
  }

  if (!doPost) {
    console.log('\n========================================');
    console.log('==> STOPPED BEFORE POSTING');
    console.log('==> Review the preview screenshot path above');
    console.log('==> Run with --post flag to actually publish');
    console.log('========================================');
    console.log(
      JSON.stringify({
        status: 'preview',
        postType,
        mediaKind: media.mediaKind,
        stagedFiles,
        originalFiles: media.files,
        captionFile: path.resolve(captionFile),
        caption,
        screenshot,
        previewHelper: preview.ok ? preview.helper : { ok: false, error: preview.error }
      })
    );
    return;
  }

  console.log('==> Waiting for Share/Post button...');
  browser(['wait', '--text', 'Share', '--timeout-ms', '60000'], { allowFailure: true });

  console.log('==> Publishing...');
  const shareResult = clickShare();
  console.log(`  Share result: ${shareResult}`);
  if (shareResult === 'not-found') {
    throw new Error('Could not find Share/Post/Publish button in the Instagram composer.');
  }

  console.log(
    JSON.stringify({
      status: 'posted',
      postType,
      mediaKind: media.mediaKind,
      stagedFiles,
      originalFiles: media.files,
      captionFile: path.resolve(captionFile),
      caption,
      screenshot,
      previewHelper: preview.ok ? preview.helper : { ok: false, error: preview.error },
      shareResult
    })
  );
}

try {
  main();
} catch (error) {
  console.error('Error:', error.message || error);
  process.exit(1);
}
