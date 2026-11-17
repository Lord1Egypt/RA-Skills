#!/usr/bin/env node
/*
 * asar-patch.js - surgically inject a (self-contained) skin CSS into a
 * WorkBuddy app.asar WITHOUT a full repack.
 *
 * Why not a full repack (asar.createPackage)?
 *   WorkBuddy ships native modules / executables as UNPACKED files inside
 *   app.asar.unpacked, plus per-platform externals and possibly symlinks.
 *   A full repack would re-pack those into the archive (breaking native
 *   require) or drop foreign-platform files. Too risky.
 *
 * Minimal-surgery approach:
 *   An asar is `[uint32 size][chromium-pickle(header JSON)][body]`.
 *   We only need to APPEND bytes to one packed CSS file, so we:
 *     1. parse the header, find the target CSS (packed),
 *     2. grow its `size` by blockLen,
 *     3. shift every file whose body offset is >= end-of-target by blockLen,
 *     4. write: new header prefix + new header + [body..targetEnd] + block
 *        + [body after targetEnd], streaming from the original file.
 *   Unpacked externals and every other file are left byte-identical.
 *
 * Usage:
 *   node asar-patch.js --theme-dir <skins/id> --marker <id>
 *     (one-shot: auto-locates app.asar, picks the target CSS, writes patched
 *      asar to %TEMP%/wb-dream-skin/_patched.asar)
 *
 *   node asar-patch.js --asar <app.asar> --target <regex> --inject <cssFile> \
 *       --marker <id> --out <new.asar>
 *     (explicit: feed a pre-generated static css)
 *
 * Any omitted arg is auto-detected: --asar defaults to the installed
 * WorkBuddy app.asar; --target defaults to the largest renderer/assets/index-*.css;
 * --out defaults to %TEMP%/wb-dream-skin/_patched.asar; --inject can be replaced
 * by --theme-dir (which runs gen-static-css.js internally).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ASAR = 'C:/Users/qingc/.workbuddy/binaries/node/workspace/node_modules/asar';
const asar = require(ASAR);

// chromium-pickle-js is hoisted to the workspace node_modules (asar depends on it).
let pickle = null;
try { pickle = require(require.resolve('chromium-pickle-js', { paths: [ASAR] })); }
catch (_) { try { pickle = require('C:/Users/qingc/.workbuddy/binaries/node/workspace/node_modules/chromium-pickle-js'); } catch (_) {} }
if (!pickle) { console.error('chromium-pickle-js not found - cannot re-pickle header'); process.exit(1); }

function writeUInt32LE(buf, val, off) { buf.writeUInt32LE(val >>> 0, off); }

// Build an 8-byte asar size prefix: [uint32 payloadLen=4][uint32 headerBufLen]
function makeSizePrefix(headerBufLen) {
  if (pickle) {
    const p = pickle.createEmpty();
    p.writeUInt32(headerBufLen);
    return p.toBuffer(); // exactly 8 bytes
  }
  const b = Buffer.alloc(8);
  writeUInt32LE(b, 4, 0);            // pickle payload length (the uint32 value is 4 bytes)
  writeUInt32LE(b, headerBufLen, 4); // the value = length of the pickled header
  return b;
}

// Build a chromium-pickle-encoded string (used for the header JSON)
function makePickledString(str) {
  if (pickle) {
    const p = pickle.createEmpty();
    p.writeString(str);
    return p.toBuffer(); // [uint32 len][utf8 string]
  }
  const s = Buffer.from(str, 'utf8');
  const len = Buffer.alloc(4);
  writeUInt32LE(len, s.length, 0);
  return Buffer.concat([len, s]);
}

function parseArgs(argv) {
  const a = { asar: null, target: null, inject: null, marker: 'skin', out: null, themeDir: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--asar') a.asar = argv[++i];
    else if (argv[i] === '--target') a.target = argv[++i];
    else if (argv[i] === '--inject') a.inject = argv[++i];
    else if (argv[i] === '--marker') a.marker = argv[++i];
    else if (argv[i] === '--out') a.out = argv[++i];
    else if (argv[i] === '--theme-dir') a.themeDir = argv[++i];
  }
  return a;
}

// Best-effort location of the installed WorkBuddy app.asar.
function findDefaultAsar() {
  const cands = [
    process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, 'Programs', 'WorkBuddy', 'resources', 'app.asar'),
    'C:/Users/qingc/AppData/Local/Programs/WorkBuddy/resources/app.asar',
    'C:/Program Files/WorkBuddy/resources/app.asar',
  ].filter(Boolean);
  for (const c of cands) if (fs.existsSync(c)) return c;
  return null;
}

// Walk the asar header tree (paths use '/' separators).
function walk(node, prefix, out) {
  for (const [name, meta] of Object.entries(node.files || {})) {
    const p = prefix ? prefix + '/' + name : name;
    if (meta.files && !meta.link) walk(meta, p, out); // directory
    else out.push({ path: p, meta });                 // file or link
  }
}

function parseHeader(buf) {
  const sizeBuf = buf.subarray(0, 8);
  let headerBufLen, headerBuf;
  if (pickle) {
    headerBufLen = pickle.createFromBuffer(sizeBuf).createIterator().readUInt32();
  } else {
    headerBufLen = sizeBuf.readUInt32LE(4); // value stored at bytes[4..7]
  }
  headerBuf = buf.subarray(8, 8 + headerBufLen);
  const headerStr = pickle
    ? pickle.createFromBuffer(headerBuf).createIterator().readString()
    : headerBuf.subarray(4).toString('utf8'); // strip 4-byte LE length prefix
  return { headerBufLen, header: JSON.parse(headerStr) };
}

async function main() {
  const a = parseArgs(process.argv.slice(2));

  // --theme-dir replaces --inject: generate the self-contained static css first.
  if (!a.inject && a.themeDir) {
    const tmpCss = path.join(os.tmpdir(), 'wb-dream-skin', 'workbuddy.static.css');
    fs.mkdirSync(path.dirname(tmpCss), { recursive: true });
    console.log('Generating static css from', a.themeDir, '->', tmpCss);
    execFileSync(process.execPath, [path.join(__dirname, 'gen-static-css.js'), '--theme-dir', a.themeDir, '--out', tmpCss], { stdio: 'inherit' });
    a.inject = tmpCss;
  }
  if (!a.asar) a.asar = findDefaultAsar();
  if (!a.asar) { console.error('cannot locate app.asar - pass --asar explicitly'); process.exit(1); }
  if (!a.out) {
    a.out = path.join(os.tmpdir(), 'wb-dream-skin', '_patched.asar');
    fs.mkdirSync(path.dirname(a.out), { recursive: true });
  }
  if (!a.inject) { console.error('need --inject <cssFile> or --theme-dir <dir>'); process.exit(1); }

  const injectCss = fs.readFileSync(a.inject, 'utf8');
  const markerRe = new RegExp('\\/\\* === DREAM-SKIN:' + a.marker + ':(start|end) === \\*\\/');
  if (markerRe.test(injectCss)) {
    console.error('inject css already contains marker - refusing to double-inject'); process.exit(1);
  }
  const block =
    `\n/* === DREAM-SKIN:${a.marker}:start === */\n${injectCss}\n/* === DREAM-SKIN:${a.marker}:end === */\n`;
  const blockBuf = Buffer.from(block, 'utf8');
  const blockLen = blockBuf.length;

  console.log('Reading header of', a.asar);
  const headBuf = fs.readFileSync(a.asar, { length: 8 + (16 << 20) }); // header is small (<16MB)
  const { headerBufLen, header } = parseHeader(headBuf);

  const files = [];
  walk(header, '', files);
  console.log('total entries in header:', files.length);

  let target;
  if (a.target) {
    const targetRe = new RegExp(a.target);
    const matches = files.filter(f => targetRe.test(f.path));
    if (matches.length !== 1) {
      console.error('target match count =', matches.length, '(expected exactly 1). Matches:',
        matches.map(m => m.path).slice(0, 5));
      process.exit(1);
    }
    target = matches[0];
  } else {
    // Auto-select: the main renderer bundle css (largest renderer/assets/index-*.css).
    const cands = files.filter(f => /^renderer\/assets\/index-.*\.css$/.test(f.path));
    if (cands.length === 0) {
      console.error('no renderer/assets/index-*.css found; pass --target explicitly');
      process.exit(1);
    }
    cands.sort((x, y) => parseInt(y.meta.size, 10) - parseInt(x.meta.size, 10));
    target = cands[0];
    console.log('auto-target selected:', target.path, '(of', cands.length, 'candidates, picked largest)');
  }
  if (target.meta.unpacked) {
    console.error('target is an unpacked (external) file - cannot patch via body surgery:', target.path);
    process.exit(1);
  }
  const targetOffset = parseInt(target.meta.offset, 10);
  const targetSize = target.meta.size;
  const targetEnd = targetOffset + targetSize;
  console.log('target:', target.path, 'offset', targetOffset, 'size', targetSize);

  // Shift every packed file that lives after the target in the body.
  let shifted = 0;
  for (const f of files) {
    if (f.meta.offset === undefined) continue; // unpacked / external
    const off = parseInt(f.meta.offset, 10);
    if (off >= targetEnd) { f.meta.offset = String(off + blockLen); shifted++; }
  }
  // Grow target size; drop stale integrity (Electron never verifies asar integrity).
  target.meta.size = targetSize + blockLen;
  delete target.meta.integrity;
  console.log('shifting', shifted, 'file(s) by', blockLen, 'bytes; new target size', target.meta.size);

  // Re-encode header.
  const newHeaderPickled = makePickledString(JSON.stringify(header));
  const newSizePrefix = makeSizePrefix(newHeaderPickled.length);

  const bodyStart = 8 + headerBufLen;
  const targetAbsStart = bodyStart + targetOffset;
  const targetAbsEnd = targetAbsStart + targetSize; // exclusive

  console.log('Writing patched asar ->', a.out);
  await new Promise((resolve, reject) => {
    const ws = fs.createWriteStream(a.out);
    ws.on('error', reject);
    ws.write(newSizePrefix);
    ws.write(newHeaderPickled);
    const r1 = fs.createReadStream(a.asar, { start: bodyStart, end: targetAbsEnd - 1 });
    r1.on('error', reject);
    r1.on('end', () => {
      ws.write(blockBuf);
      const r2 = fs.createReadStream(a.asar, { start: targetAbsEnd });
      r2.on('error', reject);
      r2.on('end', () => { ws.end(); resolve(); });
      r2.pipe(ws, { end: false });
    });
    r1.pipe(ws, { end: false });
  });

  // ---- validate ----
  console.log('Validating output...');
  let vHeaderBufLen, vHeader;
  try {
    const vHead = fs.readFileSync(a.out, { length: 8 + (16 << 20) });
    const r = parseHeader(vHead);
    vHeaderBufLen = r.headerBufLen; vHeader = r.header;
  } catch (e) {
    console.error('VALIDATION FAILED: cannot re-read header -', e.message);
    process.exit(1);
  }
  // confirm the public asar tool can also parse it (same reader Electron uses)
  let hdrOk = true;
  try { asar.getRawHeader(a.out); } catch (e) { hdrOk = false; console.error('asar.getRawHeader threw:', e.message); }
  console.log('public asar.getRawHeader parses:', hdrOk);

  const vFiles = [];
  walk(vHeader, '', vFiles);
  const vTarget = vFiles.find(f => f.path === target.path);
  if (!vTarget) { console.error('VALIDATION FAILED: target missing in new header'); process.exit(1); }
  const vAbs = 8 + vHeaderBufLen + parseInt(vTarget.meta.offset, 10);
  const vSize = vTarget.meta.size;
  const fh = fs.openSync(a.out, 'r');
  const vBuf = Buffer.alloc(vSize);
  fs.readSync(fh, vBuf, 0, vSize, vAbs);
  fs.closeSync(fh);
  const vText = vBuf.toString('utf8');
  const ok = vText.includes(`/* === DREAM-SKIN:${a.marker}:start === */`) &&
             vText.includes('data:image/png;base64,');
  console.log('VALIDATE marker+hero present:', ok, ' new target size:', vSize);
  if (!ok) { console.error('VALIDATION FAILED'); process.exit(1); }
  console.log('PATCH OK');
}

main().then(() => process.exit(0)).catch(e => { console.error('ERROR:', e.message); process.exit(1); });
