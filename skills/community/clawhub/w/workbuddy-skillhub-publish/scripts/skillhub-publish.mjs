#!/usr/bin/env node

import { createHash, randomUUID } from "node:crypto";
import { spawn } from "node:child_process";
import { access, mkdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import { homedir, tmpdir } from "node:os";
import { join, resolve } from "node:path";

const SKILLHUB_URL = process.env.SKILLHUB_PUBLISH_URL || "https://skillhub.cn/dashboard/publish";
const SKILLHUB_DASHBOARD_URL = "https://skillhub.cn/dashboard";
const DEFAULT_CHANGELOG = "优化 SkillHub 自动发布流程、浏览器操作和结果回读。";
const REQUIRED_FILES = ["SKILL.md", "manifest.yaml", "LICENSE"];
const ZIP_EXCLUDES = [
  ".git/*", ".factory/*", ".playwright-cli/*", "dist/*", "node_modules/*", "output/*", ".gitignore", ".DS_Store", "LICENSE", "LICENSE-CONTENT",
  ".env", ".env.*", ".keep", "*/.keep", "icon-source.svg", "*/icon-source.svg", "*/__pycache__/*", "*.pyc", "*.pem", "*.key", "*.p12", "*.pfx",
];

function fail(code, message, details = {}) {
  const error = new Error(message);
  error.code = code;
  error.details = details;
  throw error;
}

export function validateBridgeUrl(value = process.env.EASY_WEBBRIDGE_URL || "http://127.0.0.1:17777") {
  let url;
  try { url = new URL(value); } catch { fail("invalid-bridge-url", "EASY_WEBBRIDGE_URL 必须是本机 Easy WebBridge 的 HTTP 地址"); }
  const loopback = url.hostname === "127.0.0.1" || url.hostname === "[::1]" || url.hostname === "::1";
  if (url.protocol !== "http:" || !loopback || url.username || url.password
      || (url.pathname !== "" && url.pathname !== "/") || url.search || url.hash) {
    fail("invalid-bridge-url", "EASY_WEBBRIDGE_URL 仅允许无凭据、无路径、无查询或片段的 http://127.0.0.1 或 http://[::1] 地址");
  }
  return url.origin;
}

export function validateSkillhubUrl(value = SKILLHUB_URL) {
  let url;
  try { url = new URL(value); } catch { fail("invalid-publish-url", "SKILLHUB_PUBLISH_URL 必须是 SkillHub 页面 HTTPS 地址"); }
  if (url.protocol !== "https:" || url.hostname !== "skillhub.cn" || url.username || url.password || url.port) {
    fail("invalid-publish-url", "SKILLHUB_PUBLISH_URL 仅允许无凭据的 https://skillhub.cn 页面");
  }
  return url.href;
}

function print(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function parseArgs(argv) {
  const [command = "help", ...rest] = argv;
  const positional = [];
  const flags = {};
  for (let index = 0; index < rest.length; index += 1) {
    const item = rest[index];
    if (!item.startsWith("--")) {
      positional.push(item);
      continue;
    }
    const key = item.slice(2).replaceAll("-", "_");
    if (["submit", "fill_only", "close_tab", "update"].includes(key)) {
      flags[key] = true;
      continue;
    }
    const value = rest[index + 1];
    if (!value || value.startsWith("--")) fail("invalid-args", `${item} 需要一个值`);
    flags[key] = value;
    index += 1;
  }
  return { command, positional, flags };
}

function usage() {
  process.stdout.write(`workbuddy SkillHub skill 自动发布\n\n用法：\n  node scripts/skillhub-publish.mjs validate <skill-dir>\n  node scripts/skillhub-publish.mjs plan <skill-dir>\n  node scripts/skillhub-publish.mjs package <skill-dir>\n  node scripts/skillhub-publish.mjs preflight\n  node scripts/skillhub-publish.mjs publish <skill-dir> --browser-id <id>\n  node scripts/skillhub-publish.mjs publish <skill-dir> --display-name <name> [--update] [--fill-only] [--close-tab]\n  node scripts/skillhub-publish.mjs readback <skill-dir> --browser-id <id>\n  node scripts/skillhub-publish.mjs self-test\n\npublish 默认完成上传、填表并点击提交；更新已有条目时加 --update。只有显式 --fill-only 才停在提交前。\n`);
}

function shouldSubmit(flags) {
  if (flags.submit && flags.fill_only) fail("invalid-args", "--submit 和 --fill-only 不能同时使用");
  return !flags.fill_only;
}

function scalar(value) {
  const text = String(value ?? "").trim();
  if ((text.startsWith("\"") && text.endsWith("\"")) || (text.startsWith("'") && text.endsWith("'"))) {
    return text.slice(1, -1).replaceAll('\\"', '"').replaceAll("''", "'");
  }
  if (text === "true") return true;
  if (text === "false") return false;
  if (text === "null" || text === "~") return null;
  return text;
}

// Skill manifests only need a small, dependency-free YAML reader: top-level
// scalars and lists. Nested runtime metadata is preserved as an opaque value.
function parseManifestYaml(text) {
  const result = {};
  let listKey = null;
  for (const rawLine of String(text).split(/\r?\n/)) {
    const line = rawLine.replace(/\s+#.*$/, "");
    if (!line.trim() || line.trim().startsWith("#")) continue;
    const listItem = line.match(/^\s+-\s*(.*)$/);
    if (listItem && listKey) {
      if (!Array.isArray(result[listKey])) result[listKey] = [];
      result[listKey].push(scalar(listItem[1]));
      continue;
    }
    const pair = line.match(/^([A-Za-z0-9_-]+):(?:\s*(.*))?$/);
    if (!pair) {
      listKey = null;
      continue;
    }
    const [, key, rawValue = ""] = pair;
    if (!rawValue.trim()) {
      result[key] = [];
      listKey = key;
    } else {
      result[key] = scalar(rawValue);
      listKey = null;
    }
  }
  return result;
}

function parseFrontmatter(text) {
  const match = String(text).match(/^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)/);
  return match ? parseManifestYaml(match[1]) : null;
}

function isInside(root, path) {
  const resolvedRoot = resolve(root);
  const resolvedPath = resolve(path);
  return resolvedPath === resolvedRoot || resolvedPath.startsWith(`${resolvedRoot}/`);
}

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

async function pngInfo(path) {
  const buffer = await readFile(path);
  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  if (buffer.length < 24 || !buffer.subarray(0, 8).equals(signature) || buffer.toString("ascii", 12, 16) !== "IHDR") {
    fail("invalid-icon", `图标不是有效 PNG：${path}`);
  }
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20), bytes: buffer.length };
}

function semver(value) {
  return typeof value === "string" && /^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$/.test(value);
}

async function validateSkill(inputDir) {
  const dir = resolve(inputDir || ".");
  const info = await stat(dir).catch(() => null);
  if (!info?.isDirectory()) fail("skill-not-found", `Skill 目录不存在：${dir}`);
  const missing = [];
  for (const name of REQUIRED_FILES) if (!(await exists(join(dir, name)))) missing.push(name);
  if (missing.length) fail("missing-file", `缺少必需文件：${missing.join(", ")}`, { missing });

  const manifestText = await readFile(join(dir, "manifest.yaml"), "utf8");
  const manifest = parseManifestYaml(manifestText);
  const skillText = await readFile(join(dir, "SKILL.md"), "utf8");
  const frontmatter = parseFrontmatter(skillText);
  if (!frontmatter?.name || !frontmatter?.description) fail("invalid-skill", "SKILL.md 必须包含 name 和 description frontmatter");
  const slug = String(manifest.slug || manifest.name || frontmatter.name || "").trim();
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug) || slug.length > 64) fail("invalid-slug", `slug 必须是小写短横线格式：${slug}`);
  const version = String(manifest.version || "").trim();
  if (!semver(version)) fail("invalid-version", `version 必须是 x.y.z 格式：${version}`);
  const description = String(manifest.description || frontmatter.description || "").trim();
  if (!description) fail("invalid-description", "manifest.yaml 缺少 description");
  if ([...description].length > 1024) fail("invalid-description", "description 不能超过 1024 个字符");

  const declaredIcon = manifest.icon == null ? "" : String(manifest.icon).trim();
  const iconCandidates = declaredIcon ? [declaredIcon] : ["icon-512.png", "assets/icon-512.png"];
  let iconRelative = null;
  for (const candidate of iconCandidates) {
    if (isInside(dir, resolve(dir, candidate)) && await exists(resolve(dir, candidate))) {
      iconRelative = candidate;
      break;
    }
  }
  if (!iconRelative) fail("missing-icon", `缺少 512×512 PNG 图标（支持 icon-512.png 或 assets/icon-512.png）`);
  const iconPath = resolve(dir, iconRelative);
  const icon = await pngInfo(iconPath);
  if (icon.width !== 512 || icon.height !== 512) fail("invalid-icon", `图标必须是 512×512 PNG，当前为 ${icon.width}×${icon.height}`, { icon });

  const warnings = [];
  if (!(await exists(join(dir, "agents", "openai.yaml")))) warnings.push("未找到 agents/openai.yaml（SkillHub 仍可发布，但建议补齐界面元数据）");
  if (!(await exists(join(dir, "README.md")))) warnings.push("未找到 README.md（不影响 SkillHub 运行）");
  return {
    dir,
    slug,
    displayName: String(manifest.display_name || manifest.name || slug),
    version,
    description,
    license: String(manifest.license || ""),
    iconPath,
    iconRelative,
    icon,
    manifest,
    warnings,
  };
}

async function runProcess(command, args, options = {}) {
  return new Promise((resolveProcess, reject) => {
    const child = spawn(command, args, { ...options, stdio: ["ignore", "pipe", "pipe"] });
    const stdout = [];
    const stderr = [];
    child.stdout.on("data", (chunk) => stdout.push(chunk));
    child.stderr.on("data", (chunk) => stderr.push(chunk));
    child.on("error", reject);
    child.on("close", (code, signal) => resolveProcess({ code, signal, stdout: Buffer.concat(stdout).toString(), stderr: Buffer.concat(stderr).toString() }));
  });
}

async function packageSkill(inputDir, validation = null) {
  const checked = validation || await validateSkill(inputDir);
  const distDir = join(checked.dir, "dist");
  await mkdir(distDir, { recursive: true });
  const zipPath = join(distDir, `${checked.slug}-${checked.version}.zip`);
  await rm(zipPath, { force: true });
  const excludes = ZIP_EXCLUDES.flatMap((pattern) => ["-x", pattern]);
  const zipped = await runProcess("zip", ["-X", "-q", "-r", zipPath, ".", ...excludes], { cwd: checked.dir });
  if (zipped.code !== 0) fail("package-failed", `zip 打包失败：${zipped.stderr.trim() || `exit ${zipped.code}`}`);
  const listed = await runProcess("unzip", ["-Z1", zipPath]);
  if (listed.code !== 0) fail("package-failed", `无法读取 zip 内容：${listed.stderr.trim()}`);
  const entries = listed.stdout.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
  // SkillHub currently rejects LICENSE as an uploaded archive entry. The
  // repository still requires and validates it, but the platform package
  // deliberately omits it.
  for (const required of ["SKILL.md", "manifest.yaml", checked.iconRelative]) {
    if (!entries.includes(required)) fail("package-failed", `zip 缺少 ${required}`);
  }
  const digest = createHash("sha256").update(await readFile(zipPath)).digest("hex");
  return { ...checked, zipPath, zipBytes: (await stat(zipPath)).size, sha256: digest, entries };
}

async function readBridgeToken() {
  if (process.env.EASY_WEBBRIDGE_TOKEN) return process.env.EASY_WEBBRIDGE_TOKEN.trim();
  const path = process.env.EASY_WEBBRIDGE_TOKEN_FILE || join(homedir(), ".easy-webbridge", "bridge-token");
  const token = await readFile(path, "utf8").catch(() => "");
  if (!token.trim()) fail("needs-user-action", `找不到 Easy WebBridge token：${path}`);
  return token.trim();
}

async function bridgeRequest(path, init = {}, { auth = true } = {}) {
  const bridgeUrl = validateBridgeUrl();
  const headers = { Accept: "application/json", ...(init.body !== undefined ? { "Content-Type": "application/json" } : {}), ...(init.headers || {}) };
  if (auth) headers.Authorization = `Bearer ${await readBridgeToken()}`;
  const response = await fetch(`${bridgeUrl}${path}`, { ...init, headers, redirect: "error" });
  const body = await response.json().catch(() => ({}));
  if (!response.ok || body.ok === false) fail(response.status === 401 ? "needs-user-action" : "bridge-error", body.error || `Easy WebBridge HTTP ${response.status}`);
  return body;
}

async function bridgeCommand(browserId, action, args = {}, timeoutMs = 30_000) {
  const body = await bridgeRequest(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, {
    method: "POST",
    body: JSON.stringify({ action, args, timeoutMs }),
  });
  return body.result ?? body;
}

async function preflight() {
  const bridgeUrl = validateBridgeUrl();
  const health = await bridgeRequest("/health", {}, { auth: false }).catch((error) => {
    fail("needs-user-action", `Easy WebBridge 未运行：${bridgeUrl}`, { cause: error.message });
  });
  const response = await bridgeRequest("/v1/browsers");
  const browsers = (response.browsers || []).filter((item) => item.online !== false).map((item) => ({
    browserId: String(item.browserId || item.id || ""),
    displayName: String(item.displayName || item.name || item.browserId || ""),
    platform: item.platform || null,
  }));
  return { ok: true, runtime: { url: bridgeUrl, service: health.service || "easy-webbridge" }, browsers };
}

function chooseBrowser(browsers, flags) {
  const requestedId = flags.browser_id ? String(flags.browser_id) : "";
  const requestedName = flags.display_name ? String(flags.display_name) : "";
  if (!requestedId && !requestedName) fail("needs-user-action", "必须指定 --browser-id 或 --display-name，不能猜登录账号");
  const found = browsers.find((browser) => (requestedId && browser.browserId === requestedId) || (requestedName && browser.displayName === requestedName));
  if (!found) fail("needs-user-action", `指定浏览器不在线：${requestedId || requestedName}`);
  return found;
}

function snapshotText(snapshot) {
  return String(snapshot?.text || "");
}

function findInteractive(snapshot, labels, { partial = false, role = null } = {}) {
  const expected = labels.map((item) => String(item));
  return (snapshot?.interactive || []).find((item) => {
    if (item.visible === false || item.disabled === true || (role && item.role !== role)) return false;
    const text = String(item.text || "").trim();
    return expected.some((label) => partial ? text.includes(label) : text === label);
  }) || null;
}

function requireUniqueInteractive(snapshot, labels, options = {}) {
  const expected = labels.map((item) => String(item));
  const matches = (snapshot?.interactive || []).filter((item) => {
    if (item.visible === false || item.disabled === true || (options.role && item.role !== options.role)) return false;
    const text = String(item.text || "").trim();
    return expected.some((label) => options.partial ? text.includes(label) : text === label);
  });
  if (matches.length > 1) fail("needs-user-action", `页面按钮不唯一：${labels.join(" / ")}`);
  return matches[0] || null;
}

async function clickLabel(browserId, tabId, snapshot, labels, options = {}) {
  let element = options.unique ? requireUniqueInteractive(snapshot, labels, options) : findInteractive(snapshot, labels, options);
  if (!element?.ref) {
    // The current publish page uses a div-based layout rather than <form>.
    // Its submit button is below the icon area and outside the viewport after
    // icon upload. Discover the exact rendered control, scroll it into view,
    // then obtain a fresh semantic reference; never click a hidden old ref.
    const deadline = Date.now() + (options.readyTimeoutMs ?? 15_000);
    let state = null;
    do {
      const stateText = await evaluate(browserId, tabId, `(() => { const normalize = value => String(value || '').replace(/\\s+/g, ' ').trim(); const labels = ${JSON.stringify(labels)}.map(normalize); const partial = ${Boolean(options.partial)}; const role = ${JSON.stringify(options.role || null)}; const matches = [...document.querySelectorAll('button,[role="button"],[role="tab"]')].filter(item => { const style = getComputedStyle(item); const actualRole = item.getAttribute('role') || (item.tagName === 'BUTTON' ? 'button' : null); const text = normalize(item.innerText || item.textContent); return (!role || actualRole === role) && item.getClientRects().length && style.display !== 'none' && style.visibility !== 'hidden' && !item.closest('[hidden],[inert]') && labels.some(label => partial ? text.includes(label) : text === label); }); const element = matches.length === 1 ? matches[0] : null; const disabled = Boolean(element?.disabled || element?.getAttribute('aria-disabled') === 'true'); if (element && !disabled) element.scrollIntoView({block:'center',inline:'center',behavior:'instant'}); return JSON.stringify({count:matches.length,disabled}); })()`);
      state = typeof stateText === "string" ? JSON.parse(stateText) : null;
      if (state?.count > 1) fail("needs-user-action", `页面按钮不唯一：${labels.join(" / ")}`);
      if (state?.count === 1 && !state.disabled) break;
      if (Date.now() >= deadline) break;
      await new Promise(resolveWait => setTimeout(resolveWait, 250));
    } while (Date.now() <= deadline);
    if (state?.count !== 1 || state.disabled) fail("needs-user-action", `页面未找到唯一可用按钮：${labels.join(" / ")}`);
    const fresh = await bridgeCommand(browserId, "snapshot", {
      tabId, visibility: "visible", roles: options.role ? [options.role] : ["button", "tab"], text: labels,
      textMode: "matched", maxElements: 40, maxTextLength: 2_000,
    });
    element = options.unique ? requireUniqueInteractive(fresh, labels, options) : findInteractive(fresh, labels, options);
  }
  if (!element?.ref) fail("needs-user-action", `页面未找到按钮：${labels.join(" / ")}`);
  await bridgeCommand(browserId, "click", { selector: element.ref, tabId, ...(options.mode ? { mode: options.mode } : {}) });
}

async function trustedClickLabel(browserId, tabId, label) {
  const code = `(() => { const label = ${JSON.stringify(label)}; const element = [...document.querySelectorAll("button,[role=tab]")].find((item) => (item.textContent || "").trim() === label); if (!element) return null; element.scrollIntoView({ block: "center", inline: "center" }); const rect = element.getBoundingClientRect(); return JSON.stringify({x: rect.x + rect.width / 2, y: rect.y + rect.height / 2}); })()`;
  const value = await evaluate(browserId, tabId, code);
  if (typeof value !== "string" || !value) fail("needs-user-action", `页面未找到可点击的按钮：${label}`);
  const point = JSON.parse(value);
  for (const type of ["mousePressed", "mouseReleased"]) {
    await bridgeCommand(browserId, "cdp", { tabId, method: "Input.dispatchMouseEvent", params: { type, x: point.x, y: point.y, button: "left", clickCount: 1 } });
  }
}

async function takeSnapshot(browserId, tabId) {
  let lastError = null;
  for (let attempt = 0; attempt < 8; attempt += 1) {
    try {
      return await bridgeCommand(browserId, "snapshot", { tabId, visibility: "visible", textMode: "page", maxElements: 200, maxTextLength: 24_000 });
    } catch (error) {
      lastError = error;
      if (!/frame with id .* removed|no such frame|target closed/i.test(String(error?.message || error))) throw error;
      await new Promise((resolveWait) => setTimeout(resolveWait, 500 + attempt * 250));
    }
  }
  throw lastError || new Error("SkillHub 页面快照失败");
}

async function waitSnapshot(browserId, tabId, predicate, timeoutMs = 20_000) {
  const deadline = Date.now() + timeoutMs;
  let latest = null;
  do {
    latest = await takeSnapshot(browserId, tabId);
    if (predicate(latest)) return latest;
    await new Promise((resolveWait) => setTimeout(resolveWait, 350));
  } while (Date.now() < deadline);
  return latest;
}

async function evaluate(browserId, tabId, code) {
  return bridgeCommand(browserId, "evaluate", { tabId, code });
}

async function assertSkillhubPage(browserId, tabId) {
  let actualUrl;
  try { actualUrl = await evaluate(browserId, tabId, "window.location.href"); } catch {
    fail("needs-user-action", "无法核验当前页面地址，已停止 SkillHub 操作");
  }
  try { validateSkillhubUrl(actualUrl); } catch {
    fail("needs-user-action", "当前页面已离开 https://skillhub.cn，已停止 SkillHub 操作");
  }
  return actualUrl;
}

async function publishFailureDetails(browserId, tabId, snapshotTextValue) {
  // SkillHub renders the toast title (for example, “提交失败”) separately
  // from its description, which contains the API error code/message. Page
  // snapshots may expose only the title, so inspect visible alert/toast
  // containers and retain their complete text for diagnostics.
  const rendered = await evaluate(browserId, tabId, `(() => {
    const visible = element => { const style = getComputedStyle(element); return element.getClientRects().length > 0 && style.display !== 'none' && style.visibility !== 'hidden'; };
    const candidates = [...document.querySelectorAll('[role="alert"],[data-sonner-toast],[data-radix-toast-root],[aria-live="assertive"],[aria-live="polite"]')].filter(visible);
    const relevant = candidates.filter(element => /提交失败|更新失败|不允许的文件类型/i.test(element.innerText || element.textContent || ''));
    return JSON.stringify(relevant.map(element => String(element.innerText || element.textContent || '').replace(/\\s+/g, ' ').trim()).filter(Boolean).slice(-5));
  })()`);
  let toastLines = [];
  try { toastLines = JSON.parse(typeof rendered === "string" ? rendered : "[]"); } catch {}
  const snapshotLines = String(snapshotTextValue || "").split(/\r?\n/).map(line => line.trim()).filter(Boolean);
  const combined = [...toastLines, ...snapshotLines].filter((line, index, all) => all.indexOf(line) === index).join(" | ").slice(0, 2_000);
  return combined || "页面未提供更具体的失败说明";
}

async function waitForFileInput(browserId, tabId, selector, timeoutMs = 15_000) {
  const deadline = Date.now() + timeoutMs;
  do {
    const present = await evaluate(browserId, tabId, `Boolean(document.querySelector(${JSON.stringify(selector)}))`).catch(() => false);
    if (present === true) return;
    await new Promise((resolveWait) => setTimeout(resolveWait, 300));
  } while (Date.now() < deadline);
  fail("needs-user-action", `页面未生成文件选择框：${selector}`);
}

export function zipUploadPageState(documentRef, expectedSlug, requiredFiles) {
  const text = String(documentRef.body?.innerText || '');
  const lines = text.split(/\r?\n/).map(line => line.trim());
  const parsing = /正在解析文件/.test(text);
  const failure = text.match(/[^\n]*(?:解析失败|解压失败|无法解析|ZIP\s*(?:文件)?格式错误|无效的\s*ZIP)[^\n]*/i)?.[0]?.trim() || null;
  const fileCount = Number(text.match(/已选择\s+([1-9]\d*)\s+个文件/)?.[1] || 0);
  const foundRequired = requiredFiles.filter(name => lines.some(line => line === name || (name === 'SKILL.md' && /^SKILL\.md\s*[（(]必需[）)]$/.test(line))));
  const slugValue = String(documentRef.querySelector('#skill-slug')?.value || '').trim();
  const slugMismatch = Boolean(expectedSlug && slugValue && slugValue !== expectedSlug);
  const slugConfirmed = !expectedSlug || slugValue === expectedSlug;
  return { ready: !parsing && !failure && slugConfirmed && !slugMismatch && fileCount >= requiredFiles.length && foundRequired.length === requiredFiles.length,
    parsing, failure, fileCount, foundRequired, slugValue, slugConfirmed, slugMismatch };
}

async function uploadZip(browserId, tabId, zipPath, { expectedSlug, requiredFiles = ['SKILL.md','manifest.yaml'], timeoutMs = 90_000, pollMs = 300 } = {}) {
  // The update dialog can appear before its asynchronously loaded file input.
  const selector = 'input[type="file"][accept*=".zip"]';
  await waitForFileInput(browserId, tabId, selector, 30_000);
  try {
    return await bridgeCommand(browserId, "upload", { selector, files: [zipPath], tabId }, 60_000);
  } catch (error) {
    // onChange clears the native input before asynchronous ZIP parsing finishes.
    // A cleared input or spinner alone is not evidence the package was accepted.
    if (!/^File selection changed:\s*expected\s+1\s+files,\s*selected\s+0$/i.test(String(error?.message || error).trim())) throw error;
    const started = Date.now(), deadline = started + timeoutMs;
    let state = null;
    do {
      try {
        const raw = await evaluate(browserId, tabId, `JSON.stringify((${zipUploadPageState.toString()})(document, ${JSON.stringify(expectedSlug || '')}, ${JSON.stringify(requiredFiles)}))`);
        state = typeof raw === 'string' ? JSON.parse(raw) : raw;
      } catch { state = { unreadable: true }; }
      if (state?.ready) return { acceptedByPage: true, selectionClearedAfterChange: true, parseEvidence: state };
      if (state?.failure || state?.slugMismatch) break;
      if (Date.now() >= deadline) break;
      await new Promise((resolveWait) => setTimeout(resolveWait, Math.min(pollMs, Math.max(1, deadline - Date.now()))));
    } while (Date.now() < deadline);
    error.details = { ...(error.details || {}), zipParseEvidence: state, zipParseElapsedMs: Date.now() - started, zipParseTimeoutMs: timeoutMs };
    throw error;
  }
}

async function uploadImage(browserId, tabId, selector, imagePath) {
  try {
    return await bridgeCommand(browserId, "upload", { selector, files: [imagePath], tabId }, 60_000);
  } catch (error) {
    // The crop dialog reads the image and clears the input synchronously.
    if (!/File selection changed: expected 1 files, selected 0/i.test(String(error?.message || error))) throw error;
    const deadline = Date.now() + 15_000;
    do {
      const text = await evaluate(browserId, tabId, "document.body?.innerText || ''").catch(() => "");
      if (/上传 Skill 图标|裁剪/.test(String(text))) return { acceptedByPage: true, selectionClearedAfterChange: true };
      await new Promise((resolveWait) => setTimeout(resolveWait, 300));
    } while (Date.now() < deadline);
    throw error;
  }
}

async function verifyPublishFields(browserId, tabId, fields) {
  const labels = {
    "#skill-slug": "Slug",
    "#skill-displayName": "Skill 名称",
    "#skill-summaryZh": "Skill 描述",
    "#skill-version": "版本号",
    "#skill-changelog": "变更说明",
  };
  for (const [selector, expected] of fields) {
    const actual = await evaluate(browserId, tabId, `(() => { const element = document.querySelector(${JSON.stringify(selector)}); return element && "value" in element ? String(element.value || "") : null; })()`);
    if (typeof actual !== "string" || actual.trim() !== String(expected).trim()) {
      fail("needs-user-action", `SkillHub ${labels[selector] || selector} 未成功写入，请检查表单后重试`);
    }
  }
}

async function findOrOpenSkillhubTab(browserId, targetUrl = SKILLHUB_URL) {
  // Reuse the selected browser profile's login state, while owning our own
  // tab and group. A user's dashboard or another publisher's form is never
  // navigated, activated, or closed by this CLI.
  const session = `workbuddy-skillhub-${randomUUID()}`;
  const opened = await bridgeCommand(browserId, "navigate", { url: targetUrl, newTab: true, session, groupTitle: "workbuddy SkillHub" });
  const tabId = Number(opened.tabId ?? opened.id);
  try {
    if (!Number.isInteger(tabId)) fail("bridge-error", "Easy WebBridge 没有返回新标签页 ID");
    // Some EasyBR WebBridge builds create and group the tab successfully but
    // return an empty session-filtered list. Verify ownership by the exact ID
    // returned from our newTab navigation instead of treating that index as
    // authoritative.
    const tabs = await bridgeCommand(browserId, "list_tabs");
    if (!Array.isArray(tabs) || !tabs.some(tab => Number(tab.id) === tabId)) {
      fail("bridge-error", "Easy WebBridge 返回的标签不属于本次 SkillHub 任务组");
    }
  } catch (error) {
    await bridgeCommand(browserId, "close_session", { session }).catch(() => undefined);
    throw error;
  }
  return { tabId, created: true, session };
}

function dashboardHasVersion(text, slug, version) {
  const start = String(text).indexOf(`slug: ${slug}`);
  return start >= 0 && String(text).slice(start, start + 600).includes(`V ${version}`);
}

async function ensureUpdateForm(browserId, tabId, slug, targetVersion) {
  for (let page = 1; page <= 20; page += 1) {
    await bridgeCommand(browserId, "cdp", { tabId, method: "Page.navigate", params: { url: `${SKILLHUB_DASHBOARD_URL}?page=${page}` } });
    await assertSkillhubPage(browserId, tabId);
    const pageIndicator = new RegExp(`\\b${page}\\s*\\/\\s*\\d+\\b`);
    const snapshot = await waitSnapshot(browserId, tabId, (value) => {
      const text = snapshotText(value);
      return /请先登录|立即登录|login|sign in/i.test(text)
        || (/管理你发布的所有团队 Skills/.test(text) && pageIndicator.test(text) && (/slug:/.test(text) || /暂无已发布|暂无 Skill/.test(text)));
    });
    await assertSkillhubPage(browserId, tabId);
    const text = snapshotText(snapshot);
    if (/请先登录|立即登录|login|sign in/i.test(text) && !/退出登录|logout/i.test(text)) {
      fail("needs-user-action", "SkillHub 页面要求登录，请先在指定 EasyBR 环境登录");
    }
    if (!pageIndicator.test(text)) fail("needs-user-action", `SkillHub 第 ${page} 页加载超时，停止更新以免点错条目`);
    const code = `(() => { const expected = ${JSON.stringify(`slug: ${slug}`)}; const slugNode = [...document.querySelectorAll('*')].find((item) => (item.textContent || '').trim() === expected); const card = slugNode?.closest('a'); const update = card && [...card.querySelectorAll('*')].find((item) => (item.textContent || '').trim() === '更新'); if (!card || !update) return null; const text = card.innerText || card.textContent || ''; const version = text.match(/\\bV\\s*(\\d+\\.\\d+\\.\\d+(?:[-+][0-9A-Za-z.-]+)?)/i)?.[1] || null; const status = ['安全审核中', '待审核', '审核中', '已发布', '已下架'].find((item) => text.includes(item)) || null; const image = [...card.querySelectorAll('img')].find((item) => /^https?:\\/\\//i.test(item.currentSrc || item.src || '')); update.scrollIntoView({ block: 'center', inline: 'center' }); const rect = update.getBoundingClientRect(); return JSON.stringify({ version, status, iconUrl: image?.currentSrc || image?.src || null, point: { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 } }); })()`;
    const entryText = await evaluate(browserId, tabId, code);
    if (typeof entryText === "string" && entryText) {
      const entry = JSON.parse(entryText);
      if (entry.version === targetVersion) return { alreadyCurrent: true, ...entry, page };
      const point = entry.point;
      await assertSkillhubPage(browserId, tabId);
      for (const type of ["mousePressed", "mouseReleased"]) {
        await bridgeCommand(browserId, "cdp", { tabId, method: "Input.dispatchMouseEvent", params: { type, x: point.x, y: point.y, button: "left", clickCount: 1 } });
      }
      let form = await waitSnapshot(browserId, tabId, (value) => /更新 Skill/.test(snapshotText(value)) && /上传新版本文件/.test(snapshotText(value)), 8_000);
      if (/更新 Skill/.test(snapshotText(form)) && /上传新版本文件/.test(snapshotText(form))) return { snapshot: form, existing: entry, page };
      // The dashboard action is a span inside a card link. A native CDP click
      // can occasionally be swallowed while the dashboard is still settling;
      // inspect the live page first, then retry the same visible control once.
      let bodyText = await evaluate(browserId, tabId, "document.body?.innerText || ''").catch(() => "");
      if (/更新 Skill/.test(String(bodyText)) && /上传新版本文件/.test(String(bodyText))) {
        form = await takeSnapshot(browserId, tabId);
        return { snapshot: form, existing: entry, page };
      }
      await evaluate(browserId, tabId, `(() => { const expected = ${JSON.stringify(`slug: ${slug}`)}; const node = [...document.querySelectorAll('*')].find(item => (item.textContent || '').trim() === expected); const card = node?.closest('a'); const action = card && [...card.querySelectorAll('*')].find(item => (item.textContent || '').trim() === '更新'); if (!action) return false; action.click(); return true; })()`);
      form = await waitSnapshot(browserId, tabId, (value) => /更新 Skill/.test(snapshotText(value)) && /上传新版本文件/.test(snapshotText(value)), 12_000);
      bodyText = await evaluate(browserId, tabId, "document.body?.innerText || ''").catch(() => "");
      if (/更新 Skill/.test(String(bodyText)) && /上传新版本文件/.test(String(bodyText))) {
        form = await takeSnapshot(browserId, tabId);
        return { snapshot: form, existing: entry, page };
      }
      fail("needs-user-action", `已找到 ${slug}，但更新表单没有打开`);
    }
    const hasNext = await evaluate(browserId, tabId, `(() => { const button = [...document.querySelectorAll('button')].find((item) => (item.textContent || '').trim() === '下一页'); return Boolean(button && !button.disabled); })()`);
    if (hasNext !== true) break;
  }
  fail("needs-user-action", `“我的 Skills”中未找到 ${slug}，不能使用 --update`);
}

async function ensurePublishForm(browserId, tabId) {
  let snapshot = await waitSnapshot(browserId, tabId, (value) => /发布新技能|发布 Skill|最快上架|请先登录|立即登录|login|sign in/i.test(snapshotText(value)));
  await assertSkillhubPage(browserId, tabId);
  const text = snapshotText(snapshot);
  if (/请先登录|立即登录|login|sign in/i.test(text) && !/退出登录|logout/i.test(text)) {
    fail("needs-user-action", "SkillHub 页面要求登录，请先在指定 EasyBR 环境登录");
  }
  if (!/发布新技能/.test(text)) {
    await clickLabel(browserId, tabId, snapshot, ["发布 Skill\n最快上架", "最快上架"], { partial: true });
    snapshot = await waitSnapshot(browserId, tabId, (value) => /发布新技能/.test(snapshotText(value)));
    await assertSkillhubPage(browserId, tabId);
  }
  if (!/发布新技能/.test(snapshotText(snapshot))) fail("needs-user-action", "未进入 SkillHub 发布表单，请检查页面是否改版");
  return snapshot;
}

async function uploadIcon(browserId, tabId, iconPath, { replace = false } = {}) {
  await assertSkillhubPage(browserId, tabId);
  let snapshot = await takeSnapshot(browserId, tabId);
  const currentText = snapshotText(snapshot);
  const previousUrl = replace ? await waitIconUrl(browserId, tabId, "", 2_000) : null;
  if (!replace && /已上传 Skill 图标|已选图标|图标审核中/.test(currentText)) {
    const existingUrl = await waitIconUrl(browserId, tabId);
    if (existingUrl) return existingUrl;
  }
  // Radix tabs activate on pointer events; a DOM-only click may leave preset selected.
  await clickLabel(browserId, tabId, snapshot, ["自定义"], { mode: "native", role: "tab" });
  for (let attempt = 0; attempt < 3; attempt += 1) {
    const selected = await evaluate(browserId, tabId, `Boolean([...document.querySelectorAll('[role="tab"]')].find(item => (item.textContent || "").trim() === "自定义" && item.getAttribute("aria-selected") === "true"))`);
    if (selected) break;
    if (attempt === 2) fail("needs-user-action", "SkillHub 自定义图标标签未激活");
    await new Promise(resolveWait => setTimeout(resolveWait, 350));
    await clickLabel(browserId, tabId, await takeSnapshot(browserId, tabId), ["自定义"], { mode: "native", role: "tab" });
  }
  snapshot = await takeSnapshot(browserId, tabId);
  // ZIP also has a “重新上传（清空）” label; page-text substring matches
  // cannot prove that the exact icon upload control is ready.
  await clickLabel(browserId, tabId, snapshot, ["点击上传图片", "重新上传"]);
  const dialog = await waitSnapshot(browserId, tabId, (value) => /上传 Skill 图标|点击选择图片/.test(snapshotText(value)));
  if (!dialog || !/上传/.test(snapshotText(dialog))) fail("needs-user-action", "图标上传窗口未打开");
  const imageSelector = 'input[type="file"][accept*="image"]';
  await waitForFileInput(browserId, tabId, imageSelector);
  await assertSkillhubPage(browserId, tabId);
  await uploadImage(browserId, tabId, imageSelector, iconPath);
  const cropReady = await waitSnapshot(browserId, tabId, (value) => Boolean(findInteractive(value, ["上传"])), 20_000);
  if (!cropReady) fail("needs-user-action", "SkillHub 未完成图标读取或裁剪");
  await clickLabel(browserId, tabId, cropReady, ["上传"]);
  const saved = await waitSnapshot(browserId, tabId, (value) => /重新上传|已上传 Skill 图标|已选图标|图标审核中/.test(snapshotText(value)), 30_000);
  if (!saved) fail("needs-user-action", "SkillHub 图标上传未完成");
  const iconUrl = await waitIconUrl(browserId, tabId, previousUrl || "");
  if (!iconUrl) fail("needs-user-action", "图标状态已变化，但尚未读取到 SkillHub 远程图标地址");
  return iconUrl;
}

async function waitIconUrl(browserId, tabId, excludedUrl = "", timeoutMs = 20_000) {
  const code = `(() => { const panels = [...document.querySelectorAll('[role="tabpanel"]')].filter((panel) => panel.getClientRects().length); const image = panels.flatMap((panel) => [...panel.querySelectorAll('img')]).find((item) => { const src = item.currentSrc || item.src || ''; const alt = (item.alt || '').trim(); const text = item.closest('[role="tabpanel"]')?.textContent || ''; return item.getClientRects().length && /^https?:\\/\\//i.test(src) && (alt.includes('已上传 Skill 图标') || alt.includes('已选图标') || text.includes('重新上传') || text.includes('图标审核中')); }); return image?.currentSrc || image?.src || null; })()`;
  const deadline = Date.now() + timeoutMs;
  do {
    const value = await evaluate(browserId, tabId, code).catch(() => null);
    if (typeof value === "string" && /^https?:\/\//i.test(value) && value !== excludedUrl) return value;
    await new Promise((resolveWait) => setTimeout(resolveWait, 350));
  } while (Date.now() < deadline);
  return null;
}

async function publishSkill(inputDir, flags) {
  const publishUrl = validateSkillhubUrl();
  const checked = await validateSkill(inputDir);
  const packaged = await packageSkill(inputDir, checked);
  const runtime = await preflight();
  const browser = chooseBrowser(runtime.browsers, flags);
  const updateMode = Boolean(flags.update);
  const submitNow = shouldSubmit(flags);
  const opened = await findOrOpenSkillhubTab(browser.browserId, updateMode ? SKILLHUB_DASHBOARD_URL : publishUrl);
  const { browserId, displayName } = browser;
  let failed = false;
  try {
    const updateState = updateMode ? await ensureUpdateForm(browserId, opened.tabId, packaged.slug, packaged.version) : null;
    if (updateState) await assertSkillhubPage(browserId, opened.tabId);
    if (updateState?.alreadyCurrent) {
      print({
        ok: true,
        status: "already_current",
        skill: packaged.slug,
        displayName: packaged.displayName,
        version: packaged.version,
        browserId,
        browserName: displayName,
        tabId: opened.tabId,
        zip: { path: packaged.zipPath, bytes: packaged.zipBytes, sha256: packaged.sha256 },
        icon: { path: packaged.iconPath, url: updateState.iconUrl || null },
        fieldsFilled: [],
        mode: "update",
        platformStatus: updateState.status,
        submitRequired: false,
      });
      return;
    }
    let snapshot = updateMode ? updateState.snapshot : await ensurePublishForm(browserId, opened.tabId);
    await assertSkillhubPage(browserId, opened.tabId);
    // Recheck immediately before the first package upload in case navigation
    // changed after the form became ready.
    await assertSkillhubPage(browserId, opened.tabId);
    await uploadZip(browserId, opened.tabId, packaged.zipPath, { expectedSlug: packaged.slug, requiredFiles: ["SKILL.md", "manifest.yaml"] });
    const changelog = String(flags.changelog || DEFAULT_CHANGELOG);
    const displayNameValue = String(flags.skill_name || packaged.displayName);
    const fields = [
      ["#skill-displayName", displayNameValue],
      ["#skill-summaryZh", packaged.description],
      ["#skill-version", packaged.version],
      ["#skill-changelog", changelog],
    ];
    if (!updateMode) fields.unshift(["#skill-slug", packaged.slug]);
    else {
      const currentSlug = await evaluate(browserId, opened.tabId, `(() => { const element = document.querySelector('#skill-slug'); return element && 'value' in element ? String(element.value || '') : null; })()`);
      if (currentSlug !== packaged.slug) fail("needs-user-action", `SkillHub 更新表单 slug 不一致：页面 ${currentSlug || "<空>"}，本地 ${packaged.slug}`);
    }
    for (const [selector, value] of fields) {
      await assertSkillhubPage(browserId, opened.tabId);
      await bridgeCommand(browserId, "fill", { selector, value, tabId: opened.tabId });
    }
    await verifyPublishFields(browserId, opened.tabId, fields);
    const iconUrl = await uploadIcon(browserId, opened.tabId, packaged.iconPath, { replace: updateMode });
    snapshot = await takeSnapshot(browserId, opened.tabId);
    const result = {
      ok: true,
      status: submitNow ? "submitting" : "awaiting_confirmation",
      skill: packaged.slug,
      displayName: displayNameValue,
      version: packaged.version,
      browserId,
      browserName: displayName,
      tabId: opened.tabId,
      zip: { path: packaged.zipPath, bytes: packaged.zipBytes, sha256: packaged.sha256 },
      icon: { path: packaged.iconPath, url: iconUrl },
      fieldsFilled: fields.map(([selector]) => selector),
      mode: updateMode ? "update" : "create",
      submitRequired: !submitNow,
    };
    if (!submitNow) {
      print(result);
      return;
    }
    await assertSkillhubPage(browserId, opened.tabId);
    await clickLabel(browserId, opened.tabId, snapshot, [updateMode ? "更新 Skill" : "提交审核"], { role: "button", unique: true, mode: "dom" });
    let after = await waitSnapshot(browserId, opened.tabId, (value) => {
      const text = snapshotText(value);
      return /确认发布|待审核|审核中|提交成功|更新成功|提交失败|更新失败|需要完成实名认证|不允许的文件类型|版本\s+[^\n]+已存在|under review|pending review/i.test(text)
        || (updateMode && dashboardHasVersion(text, packaged.slug, packaged.version));
    }, 30_000);
    let confirmation = snapshotText(after).replaceAll("图标审核中", "");
    if (/确认发布/.test(confirmation) && /同名 slug|命名空间/.test(confirmation)) {
      await assertSkillhubPage(browserId, opened.tabId);
      await clickLabel(browserId, opened.tabId, after, ["确认发布"]);
      after = await waitSnapshot(browserId, opened.tabId, (value) => /待审核|审核中|提交成功|更新成功|提交失败|更新失败|需要完成实名认证|不允许的文件类型|under review|pending review/i.test(snapshotText(value)), 30_000);
      confirmation = snapshotText(after).replaceAll("图标审核中", "");
    }
    if (updateMode && dashboardHasVersion(confirmation, packaged.slug, packaged.version)) {
      print({ ...result, status: /待审核|审核中/.test(confirmation) ? "under_review" : "listed", platformStatus: /待审核|审核中/.test(confirmation) ? "审核中" : "已发布", submitRequired: false });
      return;
    }
    if (/需要完成实名认证/.test(confirmation)) fail("needs-user-action", "SkillHub 要求完成实名认证，请先完成认证");
    if (/提交失败|更新失败|不允许的文件类型/i.test(confirmation)) {
      const detail = await publishFailureDetails(browserId, opened.tabId, confirmation);
      fail("needs-user-action", `SkillHub 返回${updateMode ? "更新" : "提交"}失败：${detail}`);
    }
    if (!/待审核|审核中|提交成功|更新成功|under review|pending review/i.test(confirmation)) fail("uncertain", `已点击${updateMode ? "更新" : "提交"}，但页面没有出现 SkillHub 确认文案`);
    print({ ...result, status: /待审核|审核中|under review|pending review/i.test(confirmation) ? "under_review" : "submitted", submitRequired: false });
  } catch (error) {
    failed = true;
    throw error;
  } finally {
    // Explicit successful fill-only previews may keep their tab. Failures
    // always clean their task-owned tab and group, even during a preview.
    if (opened.session && (failed || flags.close_tab || !flags.fill_only)) {
      await bridgeCommand(browserId, "close_tab", { tabId: opened.tabId }).catch(() => undefined);
      await bridgeCommand(browserId, "close_session", { session: opened.session }).catch(() => undefined);
    }
  }
}

// Read-only reconciliation of the selected SkillHub account's complete skill list.
export function readDashboardCard(documentRef, slug) {
  const exact = `slug: ${slug}`;
  const candidates = new Map();
  for (const node of [...documentRef.querySelectorAll('*')].filter(item => (item.textContent || '').trim() === exact)) {
    let found = null;
    for (let card = node; card && card !== documentRef.body; card = card.parentElement) {
      const text = String(card.innerText || card.textContent || '').replace(/\s+/g, ' ').trim();
      const labels = text.match(/\bslug\s*:\s*[a-z0-9][a-z0-9-]*/gi) || [];
      if (labels.length > 1) break;
      const version = text.match(/\bV\s*(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)/i)?.[1] || null;
      const status = ['安全审核中','待审核','审核中','已发布','已上架','已通过','已下架','已驳回','审核未通过'].find(value => text.includes(value)) || null;
      // Slug text is often a small child node; ascend to its row before reading status/version.
      if (labels.length === 1) {
        found = {card, version, status};
        if (version || status) break;
      }
    }
    if (!found) continue;
    let iconUrl = null, url = null;
    for (let parent = found.card; parent && parent !== documentRef.body; parent = parent.parentElement) {
      const text = String(parent.innerText || parent.textContent || '');
      if ((text.match(/\bslug\s*:/gi) || []).length > 1) break;
      const image = [...parent.querySelectorAll('img')].find(item => /^https?:\/\//.test(item.currentSrc || item.src || ''));
      if (image) iconUrl = image.currentSrc || image.src;
      const link = [...parent.querySelectorAll('a')].find(item => /\/skills\/[^/]+\//.test(item.href || ''));
      if (link) url = link.href;
    }
    candidates.set(found.card, {version:found.version, status:found.status, iconUrl, url});
  }
  if (candidates.size > 1) throw new Error('SkillHub exact slug has multiple cards');
  return [...candidates.values()][0] || null;
}

export function dashboardReadbackResult(slug, entry, scannedPages) {
  const pages = Array.isArray(scannedPages) ? scannedPages : [];
  const total = pages[0]?.totalPages;
  const complete = Number.isSafeInteger(total) && total > 0 && pages.length === total
    && pages.every((item, index) => item.page === index + 1 && item.totalPages === total
      && item.hasNext === (index < total - 1));
  if (entry) {
    const status = entry.status === '已发布' || entry.status === '已上架' || entry.status === '已通过'
      ? 'listed' : /审核/.test(entry.status || '') || entry.status === '待审核'
        ? 'under_review' : ['已下架', '已驳回'].includes(entry.status) ? 'unlisted' : 'unknown';
    return {ok:true,status,skill:slug,version:entry.version || null,
      ...(entry.status ? {platformStatus:entry.status} : {}),icon:{url:entry.iconUrl || null},url:entry.url || SKILLHUB_DASHBOARD_URL,
      ...(entry.url ? {owner:new URL(entry.url).pathname.split('/')[2]} : {}),
      ...(status === 'unknown' ? {reason:'条目已找到，但页面状态无法确认'} : {})};
  }
  if (complete) return {ok:true,status:'absent',skill:slug,version:null};
  return {ok:true,status:'unknown',skill:slug,version:null,reason:'未能确认已完整读取 SkillHub 全部列表页'};
}

async function cleanupOwnedSession(browserId, opened) {
  const errors = [];
  try { await bridgeCommand(browserId, 'close_tab', {tabId: opened.tabId}); } catch { errors.push('close_tab'); }
  try { await bridgeCommand(browserId, 'close_session', {session: opened.session}); } catch { errors.push('close_session'); }
  let remaining;
  try {
    const all = await bridgeCommand(browserId, 'list_tabs');
    const own = await bridgeCommand(browserId, 'list_tabs', {session: opened.session});
    if (!Array.isArray(all) || !Array.isArray(own)) fail('cleanup-pending', '无法确认本次任务页面已关闭');
    remaining = all.filter(tab => Number(tab.id ?? tab.tabId) === opened.tabId || tab.session === opened.session).length + own.length;
  } catch { fail('cleanup-pending', '关闭后回读标签列表失败'); }
  if (remaining) fail('cleanup-pending', `本次任务仍有 ${remaining} 条页面记录，需要清理后回读`);
  return {verified:true,remaining:0,...(errors.length ? {recovered:errors} : {})};
}

async function readbackSkill(inputDir, flags) {
  const checked = await validateSkill(inputDir);
  const browser = chooseBrowser((await preflight()).browsers, flags);
  const opened = await findOrOpenSkillhubTab(browser.browserId, `${SKILLHUB_DASHBOARD_URL}?page=1`);
  let result = {ok:true,status:'unknown',skill:checked.slug,version:null,reason:'尚未确认列表读取完整'};
  const scannedPages = [];
  try {
    for (let page=1; page<=100; page++) {
      if (page>1) {
        const advanced = await evaluate(browser.browserId, opened.tabId, `(() => { const buttons = [...document.querySelectorAll('button')].filter(b => b.textContent.trim() === '下一页' && !b.disabled); if (buttons.length !== 1) return false; buttons[0].click(); return true; })()`);
        if (advanced !== true) fail('needs-user-action', '无法可靠切换 SkillHub 后台分页');
      }
      const pageReady = snap => /管理你发布|我的\s*Skills|请先登录|立即登录/.test(snapshotText(snap))
        && new RegExp('(?:\\b|第)'+page+'\\s*(?:\\/|页)').test(snapshotText(snap));
      const snapshot = await waitSnapshot(browser.browserId, opened.tabId, pageReady);
      if (!pageReady(snapshot)) break;
      const raw = await evaluate(browser.browserId, opened.tabId, `(() => { const text=document.body?.innerText||''; const next=[...document.querySelectorAll('button')].find(item=>(item.textContent||'').trim()==='下一页'); const counter=text.match(/(?:第\\s*)?(\\d+)\\s*\\/\\s*(\\d+)|第\\s*(\\d+)\\s*页(?:\\s*共\\s*(\\d+)\\s*页)?/); const page=counter?Number(counter[1]||counter[3]):null; const totalPages=counter?(counter[2]||counter[4]?Number(counter[2]||counter[4]):null):null; return JSON.stringify({login:/请先登录|立即登录/.test(text)&&!/退出登录/.test(text),entry:(${readDashboardCard.toString()})(document,${JSON.stringify(checked.slug)}),hasNext:Boolean(next&&!next.disabled),page,totalPages}); })()`);
      const data = typeof raw === 'string' ? JSON.parse(raw) : raw;
      if (data.login) fail('needs-user-action','请先在指定 Easy WebBridge 环境登录 SkillHub');
      if (data.entry) {
        result = dashboardReadbackResult(checked.slug, data.entry, []);
        break;
      }
      if (data.page !== page || !Number.isSafeInteger(data.totalPages) || data.totalPages < page) break;
      scannedPages.push({page,totalPages:data.totalPages,hasNext:data.hasNext});
      if (!data.hasNext) break;
      if (page === 100) fail('needs-user-action','后台分页超出回读上限');
    }
    if (result.status === 'unknown') result = dashboardReadbackResult(checked.slug, null, scannedPages);
  } finally {
    result.cleanup = await cleanupOwnedSession(browser.browserId, opened);
  }
  return print(result);
}

async function commandMain(command, positional, flags) {
  if (command === "help") return usage();
  if (command === "self-test") return selfTest();
  if (command === "preflight") return print(await preflight());
  const dir = positional[0];
  if (!dir) fail("invalid-args", `${command} 需要 Skill 目录路径`);
  if (command === "validate") {
    const checked = await validateSkill(dir);
    return print({ ok: true, status: "validated", skill: checked.slug, displayName: checked.displayName, version: checked.version, icon: checked.icon, warnings: checked.warnings });
  }
  if (command === "plan") {
    const checked = await validateSkill(dir);
    return print({ ok: true, status: "validated", skill: checked.slug, version: checked.version, steps: ["校验 SKILL.md、manifest.yaml、LICENSE 和 512×512 PNG 图标", "生成不含 .git、dist、过程目录和凭据的 ZIP", "复用已登录 SkillHub 浏览器上传 ZIP、图标并填写表单", "默认点击提交并回读平台状态；显式 --fill-only 才停在提交前"], warnings: checked.warnings });
  }
  if (command === "package") {
    const packaged = await packageSkill(dir);
    return print({ ok: true, status: "packaged", skill: packaged.slug, version: packaged.version, zip: { path: packaged.zipPath, bytes: packaged.zipBytes, sha256: packaged.sha256 }, entries: packaged.entries });
  }
  if (command === "publish") return publishSkill(dir, flags);
  if (command === "readback") return readbackSkill(dir, flags);
  fail("invalid-args", `未知命令：${command}`);
}

async function zipUploadContractSelfTest() {
  const originalFetch = globalThis.fetch;
  const originalToken = process.env.EASY_WEBBRIDGE_TOKEN;
  let inputReads = 0, uploadCalls = 0, parseReads = 0, rejectUpload = false;
  process.env.EASY_WEBBRIDGE_TOKEN = 'offline-zip-self-test-token';
  globalThis.fetch = async (url, init) => {
    if (!String(url).endsWith('/commands')) fail('self-test-failed', 'ZIP tests must not access a real service');
    const call = JSON.parse(init.body);
    let payload;
    if (call.action === 'evaluate' && call.args.code.includes('document.querySelector') && call.args.code.includes('input[type') && call.args.code.includes('.zip')) {
      inputReads += 1;
      payload = {ok:true,result:inputReads > 1};
    } else if (call.action === 'upload') {
      uploadCalls += 1;
      if (inputReads < 2) fail('self-test-failed', 'ZIP upload started before its asynchronously loaded input was ready');
      payload = rejectUpload
        ? {ok:false,error:'File selection changed: expected 1 files, selected 0'}
        : {ok:true,result:{uploaded:true}};
    } else if (call.action === 'evaluate') {
      parseReads += 1;
      payload = {ok:true,result:{ready:true,parsing:false,failure:null,slugMismatch:false,fileCount:3,foundRequired:['SKILL.md','manifest.yaml'],slugValue:'demo-skill'}};
    } else fail('self-test-failed', `Unexpected ZIP-test command: ${call.action}`);
    return new Response(JSON.stringify(payload), {headers:{'Content-Type':'application/json'}});
  };
  try {
    const files = ['SKILL.md','manifest.yaml'];
    const validDoc = {body:{innerText:'已选择 3 个文件\nSKILL.md\nmanifest.yaml'},querySelector:() => ({value:'demo-skill'})};
    const validState = zipUploadPageState(validDoc,'demo-skill',files);
    const parsingState = zipUploadPageState({body:{innerText:'正在解析文件\n已选择 3 个文件\nSKILL.md\nmanifest.yaml'},querySelector:() => ({value:'demo-skill'})},'demo-skill',files);
    const emptySlugState = zipUploadPageState({body:{innerText:'已选择 3 个文件\nSKILL.md\nmanifest.yaml'},querySelector:() => ({value:''})},'demo-skill',files);
    const wrongSlugState = zipUploadPageState({body:{innerText:'已选择 3 个文件\nSKILL.md\nmanifest.yaml'},querySelector:() => ({value:'other-skill'})},'demo-skill',files);
    const failedState = zipUploadPageState({body:{innerText:'ZIP 解析失败\n已选择 3 个文件\nSKILL.md\nmanifest.yaml'},querySelector:() => ({value:'demo-skill'})},'demo-skill',files);
    if (!validState.ready || parsingState.ready || emptySlugState.ready || emptySlugState.slugConfirmed || emptySlugState.slugMismatch || !wrongSlugState.slugMismatch || !failedState.failure) fail('self-test-failed','ZIP parse readiness must require completed parsing, matching slug, and required files');
    const uploaded = await uploadZip('offline-zip-test', 1, '/tmp/demo.zip', {expectedSlug:'demo-skill',requiredFiles:files,timeoutMs:20,pollMs:1});
    if (!uploaded.uploaded || inputReads < 2 || uploadCalls !== 1) fail('self-test-failed','ZIP input wait must finish before upload');
    inputReads = 0; uploadCalls = 0; parseReads = 0; rejectUpload = true;
    const reconciled = await uploadZip('offline-zip-test', 1, '/tmp/demo.zip', {expectedSlug:'demo-skill',requiredFiles:files,timeoutMs:20,pollMs:1});
    if (!reconciled.acceptedByPage || !reconciled.parseEvidence?.ready || parseReads !== 1) fail('self-test-failed','cleared ZIP input is accepted only after page parse evidence');
  } finally {
    globalThis.fetch = originalFetch;
    if (originalToken === undefined) delete process.env.EASY_WEBBRIDGE_TOKEN;
    else process.env.EASY_WEBBRIDGE_TOKEN = originalToken;
  }
}

async function securityContractSelfTest() {
  const originalFetch = globalThis.fetch;
  const originalBridgeUrl = process.env.EASY_WEBBRIDGE_URL;
  const originalToken = process.env.EASY_WEBBRIDGE_TOKEN;
  const originalTokenFile = process.env.EASY_WEBBRIDGE_TOKEN_FILE;
  let fetchCalls = 0;
  try {
    for (const value of ["https://127.0.0.1:17777", "http://example.com", "http://127.0.0.1:17777/api", "http://user:pass@127.0.0.1:17777", "http://127.0.0.1:17777/?x=1"]) {
      let rejected = false;
      try { validateBridgeUrl(value); } catch (error) { rejected = error.code === "invalid-bridge-url"; }
      if (!rejected) fail("self-test-failed", `非法 Bridge 地址未被拒绝：${value}`);
    }
    if (validateBridgeUrl("http://127.0.0.1:17777") !== "http://127.0.0.1:17777"
      || validateBridgeUrl("http://[::1]:17777/") !== "http://[::1]:17777") fail("self-test-failed", "合法 loopback Bridge 地址必须可用");

    process.env.EASY_WEBBRIDGE_URL = "https://bridge.example.com";
    delete process.env.EASY_WEBBRIDGE_TOKEN;
    process.env.EASY_WEBBRIDGE_TOKEN_FILE = join(tmpdir(), `missing-bridge-token-${randomUUID()}`);
    globalThis.fetch = async () => { fetchCalls += 1; throw new Error("remote request must not happen"); };
    let rejectedBeforeTokenRead = false;
    try { await bridgeRequest("/health"); } catch (error) { rejectedBeforeTokenRead = error.code === "invalid-bridge-url"; }
    if (!rejectedBeforeTokenRead || fetchCalls !== 0) fail("self-test-failed", "远程 Bridge 必须在读取 token 和发出请求前拒绝");

    for (const value of ["http://skillhub.cn/dashboard/publish", "https://skillhub.cn.example.com/publish", "https://user@skillhub.cn/publish", "https://skillhub.cn:8443/publish"]) {
      let rejected = false;
      try { validateSkillhubUrl(value); } catch (error) { rejected = error.code === "invalid-publish-url"; }
      if (!rejected) fail("self-test-failed", `非法 SkillHub 投稿地址未被拒绝：${value}`);
    }
    if (validateSkillhubUrl("https://skillhub.cn/dashboard/publish") !== "https://skillhub.cn/dashboard/publish") fail("self-test-failed", "官方 SkillHub HTTPS 地址应被接受");

    process.env.EASY_WEBBRIDGE_URL = "http://127.0.0.1:17777";
    process.env.EASY_WEBBRIDGE_TOKEN = "offline-security-test-token";
    globalThis.fetch = async (url, init) => {
      fetchCalls += 1;
      if (String(url) !== "http://127.0.0.1:17777/health" || init.redirect !== "error") fail("self-test-failed", "Bridge 请求必须使用 loopback 且拒绝 HTTP 重定向");
      return new Response(JSON.stringify({ ok: true }), { headers: { "Content-Type": "application/json" } });
    };
    await bridgeRequest("/health");
    if (fetchCalls !== 1) fail("self-test-failed", "合法本机 Bridge 请求未执行");

    fetchCalls = 0;
    globalThis.fetch = async (url, init) => {
      fetchCalls += 1;
      if (init.redirect !== "error") fail("self-test-failed", "preflight 请求必须拒绝重定向");
      if (String(url) === "http://127.0.0.1:17777/health") return new Response(JSON.stringify({ ok: true, service: "test-bridge" }), { headers: { "Content-Type": "application/json" } });
      if (String(url) === "http://127.0.0.1:17777/v1/browsers") return new Response(JSON.stringify({ ok: true, browsers: [{ browserId: "test-browser", displayName: "Test", online: true }] }), { headers: { "Content-Type": "application/json" } });
      fail("self-test-failed", `preflight 请求地址意外：${url}`);
    };
    const ready = await preflight();
    if (ready.runtime.url !== "http://127.0.0.1:17777" || ready.runtime.service !== "test-bridge"
      || ready.browsers.length !== 1 || ready.browsers[0].browserId !== "test-browser" || fetchCalls !== 2) {
      fail("self-test-failed", "preflight 成功必须返回校验后的 Bridge URL 和在线浏览器");
    }

    fetchCalls = 0;
    globalThis.fetch = async () => {
      fetchCalls += 1;
      return new Response("unavailable", { status: 503 });
    };
    let healthFailure = null;
    try { await preflight(); } catch (error) { healthFailure = error; }
    if (healthFailure?.code !== "needs-user-action" || !healthFailure.message.includes("http://127.0.0.1:17777") || fetchCalls !== 1) {
      fail("self-test-failed", "preflight 健康检查失败必须返回含本机地址的预期错误");
    }

    process.env.EASY_WEBBRIDGE_URL = "https://bridge.example.com";
    delete process.env.EASY_WEBBRIDGE_TOKEN;
    process.env.EASY_WEBBRIDGE_TOKEN_FILE = join(tmpdir(), `missing-preflight-token-${randomUUID()}`);
    fetchCalls = 0;
    globalThis.fetch = async () => { fetchCalls += 1; throw new Error("preflight must reject before fetch"); };
    let preflightRejectedBeforeTokenRead = false;
    try { await preflight(); } catch (error) { preflightRejectedBeforeTokenRead = error.code === "invalid-bridge-url"; }
    if (!preflightRejectedBeforeTokenRead || fetchCalls !== 0) fail("self-test-failed", "非法地址的 preflight 必须在读取 token 前拒绝");
  } finally {
    globalThis.fetch = originalFetch;
    if (originalBridgeUrl === undefined) delete process.env.EASY_WEBBRIDGE_URL; else process.env.EASY_WEBBRIDGE_URL = originalBridgeUrl;
    if (originalToken === undefined) delete process.env.EASY_WEBBRIDGE_TOKEN; else process.env.EASY_WEBBRIDGE_TOKEN = originalToken;
    if (originalTokenFile === undefined) delete process.env.EASY_WEBBRIDGE_TOKEN_FILE; else process.env.EASY_WEBBRIDGE_TOKEN_FILE = originalTokenFile;
  }
}

async function selfTest() {
  if (!shouldSubmit({})) fail("self-test-failed", "publish 应默认提交");
  if (shouldSubmit({ fill_only: true })) fail("self-test-failed", "--fill-only 应停在提交前");
  const dir = join(tmpdir(), `easy-skillhub-self-test-${Date.now()}`);
  await mkdir(join(dir, "assets"), { recursive: true });
  await mkdir(join(dir, ".factory"), { recursive: true });
  await mkdir(join(dir, ".playwright-cli"), { recursive: true });
  await mkdir(join(dir, "dist"), { recursive: true });
  await mkdir(join(dir, "output"), { recursive: true });
  const png = Buffer.alloc(24);
  Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]).copy(png, 0);
  png.write("IHDR", 12, "ascii");
  png.writeUInt32BE(512, 16);
  png.writeUInt32BE(512, 20);
  await writeFile(join(dir, "SKILL.md"), "---\nname: demo-skill\ndescription: A demo skill for self test.\n---\n\n# Demo\n");
  await writeFile(join(dir, "manifest.yaml"), "name: demo-skill\ndisplay_name: Demo Skill\nslug: demo-skill\nversion: 1.2.3\ndescription: Demo Skill\nicon: assets/icon-512.png\nlicense: MIT\n");
  await writeFile(join(dir, "LICENSE"), "MIT\n");
  await writeFile(join(dir, "LICENSE-CONTENT"), "Third-party content terms\n");
  await writeFile(join(dir, "assets", "icon-512.png"), png);
  await writeFile(join(dir, ".gitignore"), "dist/\n");
  await writeFile(join(dir, ".env"), "SHOULD_NOT_BE_PACKAGED=1\n");
  await writeFile(join(dir, "assets", ".keep"), "");
  await writeFile(join(dir, "assets", "icon-source.svg"), "<svg/>\n");
  await writeFile(join(dir, ".factory", "progress.json"), "{}\n");
  await writeFile(join(dir, ".playwright-cli", "page.yml"), "debug\n");
  await writeFile(join(dir, "dist", "old.zip"), "old\n");
  await writeFile(join(dir, "output", "result.json"), "{}\n");
  try {
    const checked = await validateSkill(dir);
    const packaged = await packageSkill(dir, checked);
    const bad = packaged.entries.some((entry) => entry.startsWith(".git/") || entry.startsWith("dist/") || entry.startsWith(".factory/") || entry.startsWith(".playwright-cli/") || entry.startsWith("output/") || entry === ".gitignore" || entry === ".env" || entry.endsWith("/.keep") || entry.endsWith("/icon-source.svg") || entry === "icon-source.svg" || entry.includes("/__pycache__/") || entry.endsWith(".pyc"));
    if (bad) fail("self-test-failed", "zip 包含被排除的过程文件");
    if (packaged.entries.includes("LICENSE")) fail("self-test-failed", "SkillHub 上传包不应包含 LICENSE");
    if (packaged.entries.includes("LICENSE-CONTENT")) fail("self-test-failed", "SkillHub 上传包不应包含 LICENSE-CONTENT");
    await securityContractSelfTest();
    await zipUploadContractSelfTest();
    await browserContractSelfTest();
    print({ ok: true, status: "passed", tests: ["Bridge accepts only credential-free HTTP loopback and rejects remote URLs before token read", "Bridge fetch refuses redirects", "SkillHub submission URL is restricted to credential-free HTTPS skillhub.cn", "preflight returns validated URL and browsers, reports health failures, and rejects invalid URL before token read", "actual page URL is checked before upload and submit; offsite navigation stops actions", "publish submits by default", "--fill-only pauses before submit", "manifest and frontmatter", "512×512 PNG", "ZIP required entries", "ZIP excludes process files, LICENSE, and LICENSE-CONTENT", "delayed ZIP file input is awaited and accepted parse is verified", "readback inspects card ancestors and reports absent only after complete pagination", "owned sessions never borrow user tabs", "page text snapshots", "offscreen submit scrolls then uses a fresh unique role=button ref with one DOM-backed click", "disabled and ambiguous submit controls stop", "foreign tab result is rejected and cleaned up", "owned loading tab with uncommitted URL"], zipBytes: packaged.zipBytes });
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

// Offline regression of the actual browser-command helpers. No live browser,
// account, or platform write is involved in self-test.
async function browserContractSelfTest() {
  const dashboardBody = {};
  const row = {innerText:'Skill\nslug: demo-skill\nV 1.2.3\n已上架',textContent:'Skill\nslug: demo-skill\nV 1.2.3\n已上架',parentElement:dashboardBody,querySelectorAll:() => []};
  const slugNode = {innerText:'slug: demo-skill',textContent:'slug: demo-skill',parentElement:row,querySelectorAll:() => []};
  const card = readDashboardCard({body:dashboardBody,querySelectorAll:() => [slugNode]},'demo-skill');
  if (card?.version !== '1.2.3' || card.status !== '已上架') fail('self-test-failed','readback must inspect the card ancestor of an exact slug node');
  if (dashboardReadbackResult('demo-skill',{version:null,status:null},[]).status !== 'unknown') fail('self-test-failed','unrecognized card status must not be reported absent');
  if (dashboardReadbackResult('demo-skill',null,[{page:1,totalPages:2,hasNext:true}]).status !== 'unknown') fail('self-test-failed','partial pagination must remain unknown');
  if (dashboardReadbackResult('demo-skill',null,[{page:1,totalPages:2,hasNext:true},{page:2,totalPages:2,hasNext:false}]).status !== 'absent') fail('self-test-failed','absent requires verified complete pagination');
  if (dashboardReadbackResult('demo-skill',null,[{page:1,totalPages:2,hasNext:true},{page:3,totalPages:2,hasNext:false}]).status !== 'unknown') fail('self-test-failed','skipped page must not establish absence');
  const originalFetch = globalThis.fetch;
  const originalToken = process.env.EASY_WEBBRIDGE_TOKEN;
  const calls = [];
  let scrolled = false;
  let ambiguous = false;
  let foreignTab = false;
  let pendingUrl = false;
  let currentPageUrl = "https://skillhub.cn/dashboard/publish";
  let lastNavigation = null;
  const button = { innerText: "提交审核", textContent: "提交审核", tagName: "BUTTON", disabled: false,
    getClientRects: () => [{}], closest: () => null, getAttribute: () => null,
    scrollIntoView: () => { scrolled = true; },
  };
  process.env.EASY_WEBBRIDGE_TOKEN = "offline-self-test-token";
  globalThis.fetch = async (url, init) => {
    if (!String(url).endsWith("/commands")) fail("self-test-failed", "离线测试不应访问真实网络");
    const call = JSON.parse(init.body);
    calls.push(call);
    let result = {};
    if (call.action === "navigate") { lastNavigation = call.args; result = { tabId: 88 }; }
    else if (call.action === "list_tabs") result = [{ id: foreignTab ? 777 : 88, url: pendingUrl ? "" : lastNavigation.url }];
    else if (call.action === "evaluate") {
      if (call.args.code === "window.location.href") result = currentPageUrl;
      else {
        const document = { querySelectorAll: () => ambiguous ? [button, button] : [button] };
        result = new Function("document", "getComputedStyle", `return ${call.args.code}`)(document, () => ({ display: "block", visibility: "visible" }));
      }
    } else if (call.action === "snapshot") {
      result = { text: "发布新技能", interactive: scrolled ? [{ ref: "@fresh-submit", text: "提交审核", role: "button", visible: true, disabled: button.disabled }] : [] };
    }
    return new Response(JSON.stringify({ ok: true, result }), { headers: { "Content-Type": "application/json" } });
  };
  try {
    const first = await findOrOpenSkillhubTab("offline-test");
    const second = await findOrOpenSkillhubTab("offline-test", SKILLHUB_DASHBOARD_URL);
    if (first.session === second.session || calls.some(call => call.action === "activate_tab" || call.action === "cdp")) fail("self-test-failed", "发布器不得导航借用用户或其他任务标签");
    if (calls.filter(call => call.action === "navigate").some(call => call.args.newTab !== true || !call.args.session)) fail("self-test-failed", "发布器必须创建独立任务组");
    if (!calls.some(call => call.action === "list_tabs")) fail("self-test-failed", "创建任务标签后必须回读验证返回的标签 ID");
    pendingUrl = true;
    const loadingOwned = await findOrOpenSkillhubTab("offline-test");
    if (loadingOwned.tabId !== 88) fail("self-test-failed", "owned loading tab must be accepted before URL commits");
    pendingUrl = false;
    await assertSkillhubPage("offline-test", first.tabId); // page ready
    await assertSkillhubPage("offline-test", first.tabId); // immediately before package upload
    currentPageUrl = "https://skillhub.cn.attacker.invalid/upload";
    let offsiteBeforeUploadBlocked = false;
    const actionsBeforeOffsiteGuard = calls.length;
    try { await assertSkillhubPage("offline-test", first.tabId); } catch (error) { offsiteBeforeUploadBlocked = error.code === "needs-user-action"; }
    if (!offsiteBeforeUploadBlocked || calls.slice(actionsBeforeOffsiteGuard).some(call => call.action === "upload" || call.action === "click")) fail("self-test-failed", "站外页面必须在上传前停止，不能上传文件或点击");
    currentPageUrl = "https://skillhub.cn/dashboard/publish";
    await assertSkillhubPage("offline-test", first.tabId); // immediately before submit
    currentPageUrl = "https://attacker.invalid/submit";
    let offsiteBeforeSubmitBlocked = false;
    const actionsBeforeSubmitGuard = calls.length;
    try { await assertSkillhubPage("offline-test", first.tabId); } catch (error) { offsiteBeforeSubmitBlocked = error.code === "needs-user-action"; }
    if (!offsiteBeforeSubmitBlocked || calls.slice(actionsBeforeSubmitGuard).some(call => call.action === "click")) fail("self-test-failed", "提交前页面变为站外时必须停止，不得点击提交");
    currentPageUrl = "https://skillhub.cn/dashboard/publish";
    await takeSnapshot("offline-test", first.tabId);
    const snapshotCall = calls.at(-1);
    if (snapshotCall.args.textMode !== "page") fail("self-test-failed", "页面状态快照必须保留 page 文本");
    await clickLabel("offline-test", first.tabId, { interactive: [{ ref: "@old-hidden", text: "提交审核", role: "button", visible: false }] }, ["提交审核"], { role: "button", unique: true, mode: "dom" });
    const submitClick = calls.at(-1);
    const submitSnapshot = calls.slice(0, -1).reverse().find((call) => call.action === "snapshot");
    if (!scrolled || submitClick.action !== "click" || submitClick.args.selector !== "@fresh-submit" || submitClick.args.mode !== "dom" || JSON.stringify(submitSnapshot?.args.roles) !== JSON.stringify(["button"])) fail("self-test-failed", "离屏提交必须滚动后用新鲜、唯一的 role=button ref 执行一次 DOM-backed click");
    const countBeforeDuplicate = calls.filter((call) => call.action === "click").length;
    let duplicateBlocked = false;
    try {
      await clickLabel("offline-test", first.tabId, { interactive: [
        { ref: "@submit-one", text: "提交审核", role: "button", visible: true, disabled: false },
        { ref: "@submit-two", text: "提交审核", role: "button", visible: true, disabled: false },
      ] }, ["提交审核"], { role: "button", unique: true, mode: "dom" });
    } catch (error) { duplicateBlocked = error.code === "needs-user-action"; }
    if (!duplicateBlocked || calls.filter((call) => call.action === "click").length !== countBeforeDuplicate) fail("self-test-failed", "重复提交按钮必须在点击前阻塞");
    for (const mode of ["disabled", "ambiguous"]) {
      scrolled = false; button.disabled = mode === "disabled"; ambiguous = mode === "ambiguous";
      const count = calls.filter(call => call.action === "click").length;
      let blocked = false;
      try { await clickLabel("offline-test", first.tabId, { interactive: [] }, ["提交审核"], { readyTimeoutMs: 0, role: "button", unique: true, mode: "dom" }); }
      catch (error) { blocked = error.code === "needs-user-action"; }
      if (!blocked || calls.filter(call => call.action === "click").length !== count) fail("self-test-failed", "禁用或歧义按钮不得点击");
    }
    foreignTab = true;
    let rejected = false;
    try { await findOrOpenSkillhubTab("offline-test"); } catch (error) { rejected = error.code === "bridge-error"; }
    if (!rejected || calls.at(-1).action !== "close_session" || calls.at(-1).args.session !== lastNavigation.session) fail("self-test-failed", "错误标签必须阻塞并仅清理自己的组");
  } finally {
    globalThis.fetch = originalFetch;
    if (originalToken === undefined) delete process.env.EASY_WEBBRIDGE_TOKEN;
    else process.env.EASY_WEBBRIDGE_TOKEN = originalToken;
  }
}

const { command, positional, flags } = parseArgs(process.argv.slice(2));
commandMain(command, positional, flags).catch((error) => {
  print({ ok: false, status: error.code || "failed", error: error.message, details: error.details || undefined });
  process.exitCode = 1;
});
