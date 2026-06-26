import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSIONS_DIR = path.join(__dirname, '..', '..', 'data', 'sessions');

fs.mkdirSync(SESSIONS_DIR, { recursive: true });

/**
 * Import cookies from various browser export formats into Reach's session store.
 *
 * Supported formats:
 * - 'playwright' — Raw JSON array of Playwright cookie objects (native format)
 * - 'editthiscookie' — Chrome EditThisCookie extension JSON export
 * - 'netscape' — Netscape/curl cookies.txt format
 * - 'auto' — Detect format from file content
 *
 * @param {string} service - Service name (e.g., 'upwork', 'cantina')
 * @param {string} filePath - Path to the cookie file
 * @param {string} [format='auto'] - Cookie file format
 * @returns {object} { success, service, cookieCount, outputPath }
 */
export function importCookies(service, filePath, format = 'auto') {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Cookie file not found: ${filePath}`);
  }

  const raw = fs.readFileSync(filePath, 'utf-8').trim();

  if (format === 'auto') {
    format = detectFormat(raw);
    console.log(`[cookie-import] Detected format: ${format}`);
  }

  let cookies;

  switch (format) {
    case 'playwright':
      cookies = parsePlaywright(raw);
      break;
    case 'editthiscookie':
      cookies = parseEditThisCookie(raw);
      break;
    case 'netscape':
      cookies = parseNetscape(raw);
      break;
    default:
      throw new Error(`Unknown cookie format: ${format}. Use: playwright, editthiscookie, netscape, or auto`);
  }

  if (!cookies || cookies.length === 0) {
    throw new Error('No cookies parsed from file');
  }

  // Validate all cookies have required fields
  cookies = cookies.filter(c => c.name && c.domain);

  const safeName = service.replace(/[^a-zA-Z0-9_.-]/g, '_');
  const outputPath = path.join(SESSIONS_DIR, `cookies-${safeName}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(cookies, null, 2));

  console.log(`[cookie-import] Saved ${cookies.length} cookies for ${service} → ${outputPath}`);

  return {
    success: true,
    service,
    cookieCount: cookies.length,
    outputPath,
  };
}

/**
 * Detect the cookie file format from its content.
 */
function detectFormat(raw) {
  // Try JSON first
  if (raw.startsWith('[') || raw.startsWith('{')) {
    try {
      const parsed = JSON.parse(raw);
      const arr = Array.isArray(parsed) ? parsed : [parsed];

      if (arr.length === 0) return 'playwright';

      const first = arr[0];

      // EditThisCookie has 'storeId', 'id', or 'hostOnly' fields
      if ('storeId' in first || 'id' in first || 'hostOnly' in first) {
        return 'editthiscookie';
      }

      // Playwright format has 'sameSite' as a string enum
      if ('sameSite' in first && typeof first.sameSite === 'string') {
        return 'playwright';
      }

      // Default JSON to playwright format
      return 'playwright';
    } catch {
      // Not valid JSON, fall through
    }
  }

  // Netscape format starts with comments or domain lines
  if (raw.startsWith('# Netscape') || raw.startsWith('# HTTP Cookie') || /^[.\w]/.test(raw)) {
    return 'netscape';
  }

  throw new Error('Could not detect cookie format. Specify format explicitly: playwright, editthiscookie, or netscape');
}

/**
 * Parse Playwright-format cookies (already native).
 */
function parsePlaywright(raw) {
  const parsed = JSON.parse(raw);
  const arr = Array.isArray(parsed) ? parsed : [parsed];

  return arr.map(c => ({
    name: c.name,
    value: c.value,
    domain: c.domain,
    path: c.path || '/',
    expires: c.expires || -1,
    httpOnly: c.httpOnly || false,
    secure: c.secure || false,
    sameSite: normalizeSameSite(c.sameSite),
  }));
}

/**
 * Parse EditThisCookie extension JSON format (Chrome/Edge).
 *
 * EditThisCookie exports:
 * [{ "domain": ".example.com", "expirationDate": 1234567890, "hostOnly": false,
 *    "httpOnly": true, "name": "session", "path": "/", "sameSite": "unspecified",
 *    "secure": true, "session": false, "storeId": "0", "value": "abc123", "id": 1 }]
 */
function parseEditThisCookie(raw) {
  const parsed = JSON.parse(raw);
  const arr = Array.isArray(parsed) ? parsed : [parsed];

  return arr.map(c => ({
    name: c.name,
    value: c.value,
    domain: c.domain,
    path: c.path || '/',
    expires: c.expirationDate || -1,
    httpOnly: c.httpOnly || false,
    secure: c.secure || false,
    sameSite: normalizeSameSite(c.sameSite),
  }));
}

/**
 * Parse Netscape/curl cookies.txt format.
 *
 * Each line: domain\tflag\tpath\tsecure\texpires\tname\tvalue
 * Lines starting with # are comments.
 */
function parseNetscape(raw) {
  const lines = raw.split('\n');
  const cookies = [];

  for (const line of lines) {
    const trimmed = line.trim();

    // Skip comments and empty lines
    if (!trimmed || trimmed.startsWith('#')) continue;

    const parts = trimmed.split('\t');
    if (parts.length < 7) continue;

    const [domain, , cookiePath, secure, expires, name, value] = parts;

    cookies.push({
      name,
      value: value || '',
      domain,
      path: cookiePath || '/',
      expires: expires === '0' ? -1 : parseInt(expires, 10),
      httpOnly: false,
      secure: secure.toUpperCase() === 'TRUE',
      sameSite: 'Lax',
    });
  }

  return cookies;
}

/**
 * Normalize sameSite value to Playwright's expected format.
 */
function normalizeSameSite(value) {
  if (!value || value === 'unspecified' || value === 'no_restriction') return 'None';
  const lower = String(value).toLowerCase();
  if (lower === 'lax') return 'Lax';
  if (lower === 'strict') return 'Strict';
  if (lower === 'none') return 'None';
  return 'Lax';
}

/**
 * Print user instructions for exporting cookies from a browser.
 *
 * @param {string} browser - 'chrome' | 'firefox' | 'manual'
 * @returns {string} Instructions text
 */
export function getExportInstructions(browser = 'chrome') {
  const instructions = {
    chrome: `
=== Export Cookies from Chrome/Edge ===

Option 1: EditThisCookie Extension (easiest)
  1. Install "EditThisCookie" from the Chrome Web Store
  2. Go to the site you want cookies from (e.g., upwork.com)
  3. Log in to your account
  4. Click the EditThisCookie icon in the toolbar
  5. Click the export button (looks like a box with an arrow)
  6. Save the JSON to a file
  7. Import: node src/cli.js import-cookies <service> /path/to/cookies.json

Option 2: DevTools (no extension needed)
  1. Go to the site and log in
  2. Open DevTools (F12)
  3. Go to Application tab → Cookies
  4. Manually copy cookie values, or use this console snippet:
     copy(JSON.stringify(
       document.cookie.split(';').map(c => {
         const [name, ...v] = c.trim().split('=');
         return { name, value: v.join('='), domain: location.hostname, path: '/' };
       })
     ));
  5. Paste into a .json file
  6. Import: node src/cli.js import-cookies <service> /path/to/cookies.json
`.trim(),

    firefox: `
=== Export Cookies from Firefox ===

Option 1: Cookie Quick Manager Extension
  1. Install "Cookie Quick Manager" from Firefox Add-ons
  2. Go to the site and log in
  3. Click the extension icon
  4. Select the domain
  5. Export as JSON
  6. Import: node src/cli.js import-cookies <service> /path/to/cookies.json

Option 2: cookies.txt Export
  1. Install "cookies.txt" extension
  2. Go to the site and log in
  3. Click the extension icon → "Current Site"
  4. Save the cookies.txt file
  5. Import: node src/cli.js import-cookies <service> /path/to/cookies.txt netscape
`.trim(),

    manual: `
=== Manual Cookie Import ===

Create a JSON file with this format (Playwright cookie format):
[
  {
    "name": "session_id",
    "value": "abc123...",
    "domain": ".example.com",
    "path": "/",
    "expires": -1,
    "httpOnly": true,
    "secure": true,
    "sameSite": "Lax"
  }
]

Then import: node src/cli.js import-cookies <service> /path/to/cookies.json
`.trim(),
  };

  return instructions[browser] || instructions.manual;
}
