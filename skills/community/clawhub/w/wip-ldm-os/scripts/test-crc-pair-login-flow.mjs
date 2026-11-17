import { readFileSync } from "node:fs";

const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");
const loginFiles = [
  "src/hosted-mcp/app/kaleidoscope-login.html",
  "src/hosted-mcp/demo/login.html",
];

function assertContains(source, needle, label) {
  if (!source.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assertNotContains(source, needle, label) {
  if (source.includes(needle)) {
    throw new Error(`${label} must not contain: ${needle}`);
  }
}

function assertBefore(source, first, second, label) {
  const firstIndex = source.indexOf(first);
  const secondIndex = source.indexOf(second);
  if (firstIndex === -1 || secondIndex === -1 || firstIndex >= secondIndex) {
    throw new Error(`${label} expected "${first}" before "${second}"`);
  }
}

function extractServerNextSanitizer(source) {
  const consts = [
    source.match(/const PAIR_NEXT_REGEX = .+;/)?.[0],
    source.match(/const REMOTE_CONTROL_NEXT_REGEX = .+;/)?.[0],
    source.match(/const DEMO_NEXT_REGEX = .+;/)?.[0],
  ];
  if (consts.some((line) => !line)) {
    throw new Error("server sanitizer test could not extract next regex constants");
  }
  const start = source.indexOf("function sanitizeCrcPairNext(raw)");
  const end = source.indexOf("// POST /api/qr-login", start);
  if (start === -1 || end === -1) {
    throw new Error("server sanitizer test could not extract sanitizeCrcPairNext");
  }
  return Function(`${consts.join("\n")}\n${source.slice(start, end)}\nreturn sanitizeCrcPairNext;`)();
}

function assertSanitizedNext(sanitize, value, expected) {
  const actual = sanitize(value);
  if (actual !== expected) {
    throw new Error(`sanitizeCrcPairNext(${JSON.stringify(value)}) expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

assertContains(server, "const PAIR_NEXT_REGEX = /^\\/pair\\/[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$/;", "server pair regex");
assertContains(server, "const REMOTE_CONTROL_NEXT_REGEX = /^\\/codex-remote-control\\/", "server remote-control regex");
assertContains(server, "const DEMO_NEXT_REGEX = /^\\/demo$/;", "server demo regex");
assertContains(server, "purpose,           // \"pair\" | null", "server stores pair purpose");
assertContains(server, "next: next || null, // sanitized `/pair/<CODE>`, `/codex-remote-control/<UUID>`, `/demo`, or null", "server stores sanitized next");
assertContains(server, "DEMO_NEXT_REGEX.test(decoded)", "server allows demo next");
assertContains(server, "json(res, 200, { status: \"approved\", agentId: entry.agentId });", "server strips desktop pair status");
assertContains(server, "json(res, 200, { ok: true, next: entry.next });", "server returns next to phone approve");
assertContains(server, "tenantId: entry.tenantId || null,", "server returns QR login tenant");
assertContains(server, "const verifiedIdentity = identityForApiKey(apiKey);", "server canonicalizes QR approval identity");

const sanitizeCrcPairNext = extractServerNextSanitizer(server);
assertSanitizedNext(sanitizeCrcPairNext, "/demo", "/demo");
assertSanitizedNext(sanitizeCrcPairNext, "/demo/", null);
assertSanitizedNext(sanitizeCrcPairNext, "/demo/../admin", null);
assertSanitizedNext(sanitizeCrcPairNext, "//evil.com", null);
assertSanitizedNext(sanitizeCrcPairNext, "https://evil", null);
assertSanitizedNext(sanitizeCrcPairNext, "/demoX", null);

for (const file of loginFiles) {
  const html = readFileSync(file, "utf8");
  assertContains(html, "var DEMO_NEXT_REGEX = /^\\/demo$/;", `${file} demo regex`);
  assertContains(html, "function defaultLocalPasskeysOn()", `${file} has local passkey default helper`);
  assertContains(html, "return isMobileDevice();", `${file} defaults local passkeys on for mobile`);
  assertContains(html, "function getLocalPasskeysPreference()", `${file} has local passkey preference helper`);
  assertContains(html, "if (stored === 'on' || stored === 'off') return stored;", `${file} respects stored local passkey preference`);
  assertContains(html, "function needsCustomQR() {\n  return !isLocalPasskeysOn();\n}", `${file} uses QR whenever local passkeys are off`);
  assertNotContains(html, "return !isMobileDevice() && !isSafariDesktop() && !isLocalPasskeysOn();", `${file} must not gate QR by browser or mobile status`);
  assertContains(html, "DEMO_NEXT_REGEX.test(raw)", `${file} allowlists demo next`);
  assertContains(html, "function storeDemoHandoffIfNeeded(next, identity, isNewAccount)", `${file} demo handoff helper`);
  assertContains(html, "sessionStorage.setItem('lesa-token', identity.apiKey);", `${file} stores demo token`);
  assertContains(html, "sessionStorage.setItem('lesa-agent', identity.agentId);", `${file} stores demo agent`);
  assertContains(html, "if (identity.tenantId) sessionStorage.setItem('lesa-tenant', identity.tenantId);", `${file} stores demo tenant`);
  assertContains(html, "if (isNewAccount) sessionStorage.setItem('lesa-new-account', 'true');", `${file} stores demo new-account flag conditionally`);
  assertContains(html, "tenantId: result.tenantId,", `${file} sends tenant to QR approval`);
  assertContains(html, "storeDemoHandoffIfNeeded(data.next, data, qrLoginMode === 'register');", `${file} QR status stores demo handoff`);
  assertContains(html, "storeDemoHandoffIfNeeded('/demo', data, qrLoginMode === 'register');", `${file} plain QR success keeps demo handoff`);
  assertContains(html, "storeDemoHandoffIfNeeded('/demo', result, true);", `${file} plain create success keeps demo handoff`);
  assertContains(html, "storeDemoHandoffIfNeeded('/demo', result, false);", `${file} plain sign-in success keeps demo handoff`);
  if (html.includes('onclick="sessionStorage.clear();"')) {
    throw new Error(`${file} Try the Demo button must not clear sessionStorage`);
  }
  assertContains(html, "followPairNextIfPresent(approveResponse, result, true)", `${file} create account marks new account`);
  assertContains(html, "followPairNextIfPresent(approveResponse, result, false)", `${file} sign-in does not mark new account`);
  assertContains(html, "function isPairNextOnDesktop()", `${file} desktop pair helper`);
  assertContains(html, "} else if (isPairNextOnDesktop()) {", `${file} auto-start desktop pair QR`);
  assertContains(html, "startQrLogin('', 'signin');", `${file} pair QR uses sign-in mode`);
  assertContains(html, "if (approveResponse && typeof approveResponse.next === 'string' && isWhitelistedNext(approveResponse.next))", `${file} consumes approve next`);
  assertContains(html, "if (urlNext && PAIR_NEXT_REGEX.test(urlNext))", `${file} desktop pair approved branch`);
  assertBefore(html, "if (isPairNextOnDesktop() && !qrSessionMode)", "if (needsCustomQR() && !qrSessionMode)", `${file} create button forces pair QR before normal QR fallback`);
}

const appLogin = readFileSync("src/hosted-mcp/app/kaleidoscope-login.html", "utf8");
assertContains(appLogin, "Local passkeys are on by default on mobile devices.", "app login mobile tooltip copy");
assertContains(appLogin, "This device's passkeys are used for login and device sync.", "app login mobile tooltip current-device copy");
assertContains(appLogin, "Turn this off to use or save passkeys on a different device.", "app login mobile tooltip off copy");
assertContains(appLogin, "Local passkeys are off by default on desktop.", "app login desktop tooltip copy");
assertContains(appLogin, "Your mobile device's passkeys are used for login and device sync.", "app login desktop tooltip mobile-device copy");
assertContains(appLogin, "Turn this on to use or save passkeys on this computer.", "app login desktop tooltip on copy");
assertNotContains(appLogin, "phone's passkeys", "app login tooltip must not say phone passkeys");
assertNotContains(appLogin, "mobile devices' passkeys", "app login tooltip must not use plural possessive");

console.log("crc pair login flow checks passed");
