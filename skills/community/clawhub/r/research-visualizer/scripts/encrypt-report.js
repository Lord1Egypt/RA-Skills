#!/usr/bin/env node
/**
 * Encrypt an HTML report for privacy-preserving hosting.
 *
 * The output is a self-contained HTML "viewer" page that:
 * 1. Reads the AES-256-GCM decryption key from the URL fragment (#key=...)
 * 2. Decrypts the embedded ciphertext using Web Crypto API
 * 3. Renders the original report in the page
 *
 * The key never leaves the browser (URL fragments are not sent to servers).
 * Even if the hosting storage is compromised, the content remains encrypted.
 *
 * Usage:
 *   node encrypt-report.js --input report.html --output encrypted.html
 *   → prints the key to stdout for URL construction
 *
 *   node encrypt-report.js --input report.html --output encrypted.html --json
 *   → prints JSON { "file": "encrypted.html", "key": "base64url..." }
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function parseArgs() {
  const args = process.argv.slice(2);
  let input = null, output = null, json = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input' || args[i] === '-i') input = args[++i];
    if (args[i] === '--output' || args[i] === '-o') output = args[++i];
    if (args[i] === '--json') json = true;
  }
  return { input, output, json };
}

function base64urlEncode(buf) {
  return Buffer.from(buf).toString('base64url');
}

function encrypt(plaintext, key) {
  const iv = crypto.randomBytes(12); // 96-bit IV for AES-GCM
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf-8'), cipher.final()]);
  const authTag = cipher.getAuthTag(); // 128-bit auth tag
  return { iv, encrypted, authTag };
}

function generateViewerHTML(ciphertextBase64, ivBase64, authTagBase64, title) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title || 'Encrypted Research Report'}</title>
<meta name="robots" content="noindex, nofollow">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0f; color: #e0e0e8; min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
  }
  .loader {
    text-align: center; padding: 40px;
  }
  .loader h2 { font-size: 18px; margin-bottom: 12px; }
  .loader p { color: #8888a0; font-size: 14px; }
  .spinner {
    width: 36px; height: 36px; border: 3px solid #1e1e2e;
    border-top-color: #6c5ce7; border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .error { color: #ff6b6b; }
  .lock-icon { font-size: 48px; margin-bottom: 16px; }
</style>
</head>
<body>
<div class="loader" id="status">
  <div class="spinner"></div>
  <h2>Decrypting Report...</h2>
  <p>Your data never leaves your browser</p>
</div>

<script>
(async function() {
  const status = document.getElementById('status');

  function showError(msg) {
    status.innerHTML = '<div class="lock-icon">🔒</div><h2 class="error">' + msg + '</h2><p>The decryption key is missing or invalid.</p>';
  }

  // Extract key from URL fragment
  const hash = window.location.hash.slice(1);
  const params = new URLSearchParams(hash);
  const keyB64 = params.get('key');

  if (!keyB64) {
    showError('No decryption key found in URL');
    return;
  }

  try {
    // Decode key from base64url
    const keyBytes = Uint8Array.from(atob(keyB64.replace(/-/g,'+').replace(/_/g,'/')), c => c.charCodeAt(0));

    // Import AES key
    const cryptoKey = await crypto.subtle.importKey(
      'raw', keyBytes, { name: 'AES-GCM' }, false, ['decrypt']
    );

    // Decode ciphertext components
    const iv = Uint8Array.from(atob('${ivBase64}'), c => c.charCodeAt(0));
    const authTag = Uint8Array.from(atob('${authTagBase64}'), c => c.charCodeAt(0));
    const ciphertext = Uint8Array.from(atob('${ciphertextBase64}'), c => c.charCodeAt(0));

    // Combine ciphertext + authTag (Web Crypto expects them concatenated)
    const combined = new Uint8Array(ciphertext.length + authTag.length);
    combined.set(ciphertext);
    combined.set(authTag, ciphertext.length);

    // Decrypt
    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: iv },
      cryptoKey,
      combined
    );

    // Render decrypted HTML
    const html = new TextDecoder().decode(decrypted);
    document.open();
    document.write(html);
    document.close();

  } catch (e) {
    showError('Decryption failed');
    console.error('Decryption error:', e);
  }
})();
</script>
</body>
</html>`;
}

function main() {
  const { input, output, json } = parseArgs();

  if (!input || !output) {
    console.error('Usage: node encrypt-report.js --input <report.html> --output <encrypted.html> [--json]');
    process.exit(1);
  }

  const plaintext = fs.readFileSync(path.resolve(input), 'utf-8');

  // Generate random 256-bit key
  const key = crypto.randomBytes(32);
  const keyB64url = base64urlEncode(key);

  // Encrypt
  const { iv, encrypted, authTag } = encrypt(plaintext, key);

  // Extract title from HTML if possible
  const titleMatch = plaintext.match(/<title>(.*?)<\/title>/i);
  const title = titleMatch ? titleMatch[1] : 'Encrypted Research Report';

  // Generate viewer HTML
  const viewerHTML = generateViewerHTML(
    encrypted.toString('base64'),
    iv.toString('base64'),
    authTag.toString('base64'),
    title
  );

  fs.writeFileSync(path.resolve(output), viewerHTML, 'utf-8');

  if (json) {
    console.log(JSON.stringify({ file: output, key: keyB64url }));
  } else {
    console.log(keyB64url);
  }
}

main();
