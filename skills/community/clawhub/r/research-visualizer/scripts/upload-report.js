#!/usr/bin/env node
/**
 * Upload generated HTML report to a2ui.me with client-side encryption.
 *
 * Flow:
 *   1. Generate report HTML (via generate-report.js)
 *   2. Encrypt HTML → viewer page with embedded ciphertext
 *   3. Upload encrypted viewer to R2/API
 *   4. Output full URL with decryption key in fragment
 *
 * The decryption key is ONLY in the URL fragment (#key=...) which is never
 * sent to the server. Even if R2 storage is compromised, content stays private.
 *
 * Usage:
 *   node upload-report.js --file report.html
 *   node upload-report.js --file report.html --slug custom-name
 *
 * Environment variables:
 *   A2UI_R2_BUCKET     — Cloudflare R2 bucket name (primary mode)
 *   A2UI_API_KEY       — API key for a2ui.me upload endpoint (fallback)
 *   A2UI_UPLOAD_URL    — Upload endpoint (default: https://a2ui.me/api/upload)
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const https = require('https');
const http = require('http');
const { execSync } = require('child_process');

function parseArgs() {
  const args = process.argv.slice(2);
  let file = null, slug = null, noEncrypt = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file' || args[i] === '-f') file = args[++i];
    if (args[i] === '--slug' || args[i] === '-s') slug = args[++i];
    if (args[i] === '--no-encrypt') noEncrypt = true;
  }
  return { file, slug, noEncrypt };
}

function generateSlug() {
  return crypto.randomBytes(8).toString('base64url');
}

// --- Encryption ---
function encryptHTML(html) {
  const key = crypto.randomBytes(32);
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(html, 'utf-8'), cipher.final()]);
  const authTag = cipher.getAuthTag();

  const keyB64url = key.toString('base64url');
  const titleMatch = html.match(/<title>(.*?)<\/title>/i);
  const title = titleMatch ? titleMatch[1] : 'Encrypted Research Report';

  const viewerHTML = generateViewerHTML(
    encrypted.toString('base64'),
    iv.toString('base64'),
    authTag.toString('base64'),
    title
  );

  return { viewerHTML, keyB64url };
}

function generateViewerHTML(ciphertextB64, ivB64, authTagB64, title) {
  // Escape for safe embedding
  const escTitle = title.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escTitle}</title>
<meta name="robots" content="noindex, nofollow">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:#0a0a0f;color:#e0e0e8;min-height:100vh;margin:0}
.err-wrap{display:flex;align-items:center;justify-content:center;min-height:100vh}
.error{color:#ff6b6b;text-align:center;padding:40px}
.lock-icon{font-size:48px;margin-bottom:16px}
</style>
</head>
<body>
<div id="_v" style="display:none"></div>
<script>
(async function(){
var s=document.getElementById('_v');
function err(m){s.outerHTML='<div class="err-wrap"><div class="error"><div class="lock-icon">\\u{1F512}</div><h2>'+m+'</h2><p style="color:#8888a0;margin-top:8px;font-size:14px">The decryption key is missing or invalid.<br>Make sure you use the complete URL including the #key=... part.</p></div></div>'}
var h=location.hash.slice(1),p=new URLSearchParams(h),k=p.get('key');
if(!k){err('No decryption key found');return}
try{
var kb=Uint8Array.from(atob(k.replace(/-/g,'+').replace(/_/g,'/')),function(c){return c.charCodeAt(0)});
var ck=await crypto.subtle.importKey('raw',kb,{name:'AES-GCM'},false,['decrypt']);
var iv=Uint8Array.from(atob('${ivB64}'),function(c){return c.charCodeAt(0)});
var at=Uint8Array.from(atob('${authTagB64}'),function(c){return c.charCodeAt(0)});
var ct=Uint8Array.from(atob('${ciphertextB64}'),function(c){return c.charCodeAt(0)});
var cb=new Uint8Array(ct.length+at.length);cb.set(ct);cb.set(at,ct.length);
var dec=await crypto.subtle.decrypt({name:'AES-GCM',iv:iv},ck,cb);
var html=new TextDecoder().decode(dec);
document.open();document.write(html);document.close()
}catch(e){err('Decryption failed');console.error(e)}
})();
</script>
</body>
</html>`;
}

// --- Upload via R2 (wrangler) ---
async function uploadViaR2(content, slug) {
  const bucket = process.env.A2UI_R2_BUCKET;
  const key = `r/${slug}.html`;
  const tmpFile = path.join(require('os').tmpdir(), `report-${slug}.html`);
  fs.writeFileSync(tmpFile, content, 'utf-8');

  try {
    execSync(`npx wrangler r2 object put ${bucket}/${key} --file="${tmpFile}" --content-type="text/html" --remote`, {
      stdio: 'pipe',
      env: { ...process.env },
    });
    fs.unlinkSync(tmpFile);
    return `https://r.a2ui.me/${key}`;
  } catch (err) {
    fs.unlinkSync(tmpFile);
    throw new Error(`R2 upload failed: ${err.message}`);
  }
}

// --- Upload via API ---
async function uploadViaAPI(content, slug) {
  const apiUrl = process.env.A2UI_UPLOAD_URL || 'https://a2ui.me/api/upload';
  const apiKey = process.env.A2UI_API_KEY;
  if (!apiKey) throw new Error('A2UI_API_KEY required');

  const body = JSON.stringify({ html: content, slug });
  const url = new URL(apiUrl);
  const mod = url.protocol === 'https:' ? https : http;

  return new Promise((resolve, reject) => {
    const req = mod.request({
      hostname: url.hostname, port: url.port, path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try { resolve(JSON.parse(data).url || `https://r.a2ui.me/r/${slug}.html`); }
          catch { resolve(`https://r.a2ui.me/r/${slug}.html`); }
        } else {
          reject(new Error(`Upload failed: HTTP ${res.statusCode} — ${data}`));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// --- Upload via public API (zero-config) ---
const PUBLIC_API_URL = 'https://openclaw-research-viz.fcyaoquan.workers.dev/api/upload';

async function uploadViaPublicAPI(content, slug) {
  const body = JSON.stringify({ html: content, slug });
  const url = new URL(PUBLIC_API_URL);
  const mod = url.protocol === 'https:' ? https : http;

  return new Promise((resolve, reject) => {
    const req = mod.request({
      hostname: url.hostname, port: url.port, path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try { resolve(JSON.parse(data).url); }
          catch { resolve(`https://r.a2ui.me/r/${slug}.html`); }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// --- Local fallback ---
function saveLocally(content, slug) {
  const outDir = path.resolve(__dirname, '..', 'output');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  const outFile = path.join(outDir, `${slug}.html`);
  fs.writeFileSync(outFile, content, 'utf-8');
  return outFile;
}

// --- Main ---
async function main() {
  const { file, slug: userSlug, noEncrypt } = parseArgs();

  if (!file) {
    console.error('Usage: node upload-report.js --file <report.html> [--slug <name>] [--no-encrypt]');
    process.exit(1);
  }

  const html = fs.readFileSync(path.resolve(file), 'utf-8');
  const slug = userSlug || generateSlug();

  let uploadContent, keyB64url;

  if (noEncrypt) {
    uploadContent = html;
    keyB64url = null;
  } else {
    const result = encryptHTML(html);
    uploadContent = result.viewerHTML;
    keyB64url = result.keyB64url;
  }

  let baseUrl;

  if (process.env.A2UI_R2_BUCKET) {
    // Priority 1: Direct R2 upload (for skill author/admin)
    baseUrl = await uploadViaR2(uploadContent, slug);
  } else if (process.env.A2UI_API_KEY) {
    // Priority 2: Authenticated API upload
    baseUrl = await uploadViaAPI(uploadContent, slug);
  } else {
    // Priority 3: Public API (zero-config, works for everyone)
    try {
      baseUrl = await uploadViaPublicAPI(uploadContent, slug);
    } catch (err) {
      // Fallback: save locally
      const localPath = saveLocally(uploadContent, slug);
      baseUrl = `file://${localPath}`;
      console.error(`Upload failed (${err.message}). Saved locally: ${localPath}`);
    }
  }

  // Append key fragment if encrypted
  const fullUrl = keyB64url ? `${baseUrl}#key=${keyB64url}` : baseUrl;
  console.log(fullUrl);
}

main().catch(err => { console.error(err.message); process.exit(1); });
