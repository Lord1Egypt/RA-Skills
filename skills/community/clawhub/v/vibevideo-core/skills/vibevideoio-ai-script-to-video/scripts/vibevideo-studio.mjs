#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import readline from "node:readline/promises";
import {
  DEFAULT_CAPTCHA_DIR,
  DEFAULT_SESSION_FILE,
  deleteFileIfExists,
  ensureDirectory,
  fileExists,
  getPendingLoginFile,
  hasOpenClawSessionContext,
  readJsonFile,
  readTextFile,
  shouldEmitOpenClawMediaDirective,
  writeSecureFile
} from "./vibevideo-studio-local.mjs";

const SITE_PRESETS = {
  bollo: {
    key: "bollo",
    label: "bollo.video",
    apiBase: "https://bollo.video/api",
    webBase: "https://bollo.video",
    locale: "zh"
  },
  vibevideo: {
    key: "vibevideo",
    label: "vibevideo.io",
    apiBase: "https://vibevideo.io/api",
    webBase: "https://vibevideo.io",
    locale: "en"
  }
};

const DEFAULT_SITE_KEY = "bollo";
const DEFAULT_ASPECT_RATIO = "16:9";
const DEFAULT_TIMEOUT_SECONDS = 900;
const DEFAULT_POLL_INTERVAL_SECONDS = 3;
const PENDING_CAPTCHA_TTL_MS = 10 * 60 * 1000;
const PENDING_EMAIL_CODE_TTL_MS = 15 * 60 * 1000;

function isInteractive() {
  return Boolean(process.stdin.isTTY && process.stdout.isTTY);
}

function trimTrailingSlash(value) {
  return String(value || "").replace(/\/+$/, "");
}

function joinUrl(base, pathname) {
  return `${trimTrailingSlash(base)}${pathname.startsWith("/") ? pathname : `/${pathname}`}`;
}

function normalizeToken(value) {
  const trimmed = String(value || "").trim();
  if (!trimmed) {
    return "";
  }
  return trimmed.startsWith("Bearer ") ? trimmed.slice("Bearer ".length).trim() : trimmed;
}

function normalizeSite(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (!normalized) {
    return DEFAULT_SITE_KEY;
  }
  if (["bollo", "cn", "china", "zh", "bollo.video"].includes(normalized)) {
    return "bollo";
  }
  if (["vibevideo", "intl", "international", "en", "vibevideo.io"].includes(normalized)) {
    return "vibevideo";
  }
  return DEFAULT_SITE_KEY;
}

function normalizeLocale(value, fallback) {
  const normalized = String(value || "").trim().toLowerCase();
  if (["zh", "en", "ja"].includes(normalized)) {
    return normalized;
  }
  return String(fallback || "zh").trim().toLowerCase() || "zh";
}

function normalizeStyleMode(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (["auto-realistic", "auto_realistic", "realistic", "ai-realistic", "recommend-realistic"].includes(normalized)) {
    return "auto-realistic";
  }
  if (["auto-anime", "auto_animation", "auto-animation", "anime", "animation", "ai-animation", "recommend-animation"].includes(normalized)) {
    return "auto-anime";
  }
  if (["manual", "custom"].includes(normalized)) {
    return "manual";
  }
  return "";
}

function normalizeCommand(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (!normalized) {
    return "";
  }
  if (["projects", "list-projects", "list_projects"].includes(normalized)) {
    return "projects";
  }
  if (["create", "create-episode", "create_episode"].includes(normalized)) {
    return "create-episode";
  }
  if (["login", "logout"].includes(normalized)) {
    return normalized;
  }
  return "";
}

function isImageDataUrl(value) {
  return /^data:image\/[a-z0-9.+-]+;base64,/i.test(String(value || "").trim());
}

function shouldInlineCaptchaMediaForCurrentOutput() {
  return hasOpenClawSessionContext() || !isInteractive();
}

function detectLocaleFromText(text, fallback) {
  const source = String(text || "");
  if (/[\u3400-\u9fff]/u.test(source)) {
    return "zh";
  }
  return normalizeLocale(fallback, "en");
}

function deriveTitle(text, locale) {
  const normalized = String(text || "").replace(/\s+/g, " ").trim();
  if (!normalized) {
    return locale === "zh" ? "未命名剧集" : "Untitled Episode";
  }
  return normalized.slice(0, locale === "zh" ? 30 : 60);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseArgs(argv) {
  const parsed = {
    command: "",
    free: [],
    text: "",
    file: "",
    title: "",
    site: "",
    apiBase: "",
    webBase: "",
    locale: "",
    sessionFile: DEFAULT_SESSION_FILE,
    token: "",
    email: "",
    subUserEmail: "",
    captchaText: "",
    verificationCode: "",
    projectId: "",
    styleMode: "",
    style: "",
    aspectRatio: "",
    timeoutSeconds: DEFAULT_TIMEOUT_SECONDS,
    pollIntervalSeconds: DEFAULT_POLL_INTERVAL_SECONDS,
    json: false,
    noSave: false,
    noInlineMedia: false,
    help: false
  };

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    if (!current.startsWith("--")) {
      if (!parsed.command) {
        const command = normalizeCommand(current);
        if (command) {
          parsed.command = command;
          continue;
        }
      }
      parsed.free.push(current);
      continue;
    }

    const [rawKey, rawInlineValue] = current.split("=", 2);
    const key = rawKey;
    const inlineValue = rawInlineValue ?? null;
    const consumeValue = () => {
      if (inlineValue !== null) {
        return inlineValue;
      }
      index += 1;
      return argv[index] ?? "";
    };

    if (key === "--help") {
      parsed.help = true;
      continue;
    }
    if (key === "--json") {
      parsed.json = true;
      continue;
    }
    if (key === "--no-save") {
      parsed.noSave = true;
      continue;
    }
    if (key === "--no-inline-media") {
      parsed.noInlineMedia = true;
      continue;
    }
    if (key === "--text") {
      parsed.text = consumeValue();
      continue;
    }
    if (key === "--file") {
      parsed.file = consumeValue();
      continue;
    }
    if (key === "--title") {
      parsed.title = consumeValue();
      continue;
    }
    if (key === "--site") {
      parsed.site = consumeValue();
      continue;
    }
    if (key === "--api-base") {
      parsed.apiBase = consumeValue();
      continue;
    }
    if (key === "--web-base") {
      parsed.webBase = consumeValue();
      continue;
    }
    if (key === "--locale") {
      parsed.locale = consumeValue();
      continue;
    }
    if (key === "--session-file") {
      parsed.sessionFile = consumeValue();
      continue;
    }
    if (key === "--token") {
      parsed.token = consumeValue();
      continue;
    }
    if (key === "--email") {
      parsed.email = consumeValue();
      continue;
    }
    if (key === "--sub-user-email") {
      parsed.subUserEmail = consumeValue();
      continue;
    }
    if (key === "--captcha-text") {
      parsed.captchaText = consumeValue();
      continue;
    }
    if (key === "--verification-code") {
      parsed.verificationCode = consumeValue();
      continue;
    }
    if (key === "--project-id") {
      parsed.projectId = consumeValue();
      continue;
    }
    if (key === "--style-mode") {
      parsed.styleMode = consumeValue();
      continue;
    }
    if (key === "--style") {
      parsed.style = consumeValue();
      continue;
    }
    if (key === "--aspect-ratio") {
      parsed.aspectRatio = consumeValue();
      continue;
    }
    if (key === "--timeout") {
      parsed.timeoutSeconds = Number.parseInt(consumeValue(), 10) || DEFAULT_TIMEOUT_SECONDS;
      continue;
    }
    if (key === "--poll-interval") {
      parsed.pollIntervalSeconds = Number.parseInt(consumeValue(), 10) || DEFAULT_POLL_INTERVAL_SECONDS;
      continue;
    }
  }

  if (!parsed.command && parsed.free.length > 0) {
    parsed.command = "create-episode";
  }

  if (!parsed.text && parsed.free.length > 0 && parsed.command === "create-episode") {
    parsed.text = parsed.free.join(" ");
  }

  return parsed;
}

function normalizeStringId(value) {
  const normalized = String(value ?? "").trim();
  return normalized || "";
}

function isPathInside(parentDir, candidatePath) {
  const parent = path.resolve(String(parentDir || "").trim() || ".");
  const candidate = path.resolve(String(candidatePath || "").trim() || ".");
  if (parent === candidate) {
    return true;
  }
  const relative = path.relative(parent, candidate);
  return Boolean(relative) && !relative.startsWith("..") && !path.isAbsolute(relative);
}

function sanitizeCaptchaFilePath(filename) {
  const normalized = String(filename || "").trim();
  if (!normalized) {
    return "";
  }
  if (!isPathInside(DEFAULT_CAPTCHA_DIR, normalized)) {
    throw createApiError(`Refusing to use CAPTCHA file outside ${DEFAULT_CAPTCHA_DIR}`);
  }
  return path.resolve(normalized);
}

function parseTimestampMs(value) {
  const normalized = String(value || "").trim();
  if (!normalized) {
    return 0;
  }
  const parsed = Date.parse(normalized);
  return Number.isFinite(parsed) ? parsed : 0;
}

function isPendingLoginStateFresh(pendingState) {
  if (!pendingState || typeof pendingState !== "object") {
    return false;
  }

  const stage = normalizeStringId(pendingState.stage);
  const now = Date.now();
  if (stage === "awaiting_captcha") {
    const issuedAt = parseTimestampMs(pendingState.captchaIssuedAt || pendingState.createdAt);
    return Boolean(
      issuedAt &&
      now - issuedAt <= PENDING_CAPTCHA_TTL_MS &&
      normalizeStringId(pendingState.captchaId) &&
      normalizeStringId(pendingState.captchaFile)
    );
  }

  if (stage === "awaiting_email_code") {
    const sentAt = parseTimestampMs(pendingState.emailCodeSentAt);
    return Boolean(
      sentAt &&
      now - sentAt <= PENDING_EMAIL_CODE_TTL_MS &&
      normalizeStringId(pendingState.loginEmail)
    );
  }

  return false;
}

async function maybeSendCaptchaToCurrentConversation(session, captchaFile) {
  const safeCaptchaFile = sanitizeCaptchaFilePath(captchaFile);
  if (!safeCaptchaFile) {
    return {
      attempted: false,
      delivered: false,
      reason: "captcha image unavailable"
    };
  }
  if (shouldEmitOpenClawMediaDirective(safeCaptchaFile)) {
    return {
      attempted: true,
      delivered: true,
      reason: "attached via MEDIA protocol",
      channel: "webchat"
    };
  }
  return {
    attempted: false,
    delivered: false,
    reason: session.locale === "zh"
      ? "当前不会自动向外部会话发消息；请使用 CLI 输出的 MEDIA 行或宿主消息工具发送验证码图片。"
      : "Automatic outbound delivery is disabled; use the CLI MEDIA output or the host conversation message tool to send the CAPTCHA image."
  };
}

async function writePendingLoginState(filename, payload) {
  await writeSecureFile(filename, `${JSON.stringify(payload, null, 2)}\n`);
}

function getSitePreset(siteKey) {
  return SITE_PRESETS[normalizeSite(siteKey)] || SITE_PRESETS[DEFAULT_SITE_KEY];
}

function getSiteHostname(siteKey) {
  try {
    return new URL(getSitePreset(siteKey).webBase).hostname.toLowerCase();
  } catch {
    return "";
  }
}

function doesBaseBelongToSite(value, siteKey) {
  const raw = String(value || "").trim();
  if (!raw) {
    return false;
  }
  try {
    const hostname = new URL(trimTrailingSlash(raw)).hostname.toLowerCase();
    return Boolean(hostname) && hostname === getSiteHostname(siteKey);
  } catch {
    return false;
  }
}

function resolveSiteBoundApiBase(value, siteKey) {
  const preset = getSitePreset(siteKey);
  return doesBaseBelongToSite(value, siteKey)
    ? trimTrailingSlash(value)
    : trimTrailingSlash(preset.apiBase);
}

function resolveSiteBoundWebBase(value, siteKey) {
  const preset = getSitePreset(siteKey);
  return doesBaseBelongToSite(value, siteKey)
    ? trimTrailingSlash(value)
    : trimTrailingSlash(preset.webBase);
}

function hasSavedAuthenticatedSession(savedSession) {
  return Boolean(
    savedSession &&
    typeof savedSession === "object" &&
    normalizeToken(savedSession.token) &&
    normalizeSite(savedSession.siteKey)
  );
}

function shouldPinToSavedAuthenticatedSession(args, savedSession) {
  return Boolean(
    hasSavedAuthenticatedSession(savedSession) &&
    args?.command &&
    args.command !== "login" &&
    !String(args.token || "").trim()
  );
}

function collectSavedSessionSiteConflicts(args, savedSession) {
  if (!shouldPinToSavedAuthenticatedSession(args, savedSession)) {
    return [];
  }

  const conflicts = [];
  const savedSite = normalizeSite(savedSession.siteKey);

  const providedSite = String(args.site || "").trim() ? normalizeSite(args.site) : "";
  if (providedSite && providedSite !== savedSite) {
    conflicts.push("site");
  }

  const providedApiBase = normalizeComparableUrl(args.apiBase);
  if (providedApiBase && !doesBaseBelongToSite(providedApiBase, savedSite)) {
    conflicts.push("api base");
  }

  const providedWebBase = normalizeComparableUrl(args.webBase);
  if (providedWebBase && !doesBaseBelongToSite(providedWebBase, savedSite)) {
    conflicts.push("web base");
  }

  return conflicts;
}

function buildResolvedSession(args, savedSession) {
  const pinToSavedSession = shouldPinToSavedAuthenticatedSession(args, savedSession);
  const siteKey = normalizeSite(
    pinToSavedSession
      ? savedSession?.siteKey
      : (args.site || savedSession?.siteKey || DEFAULT_SITE_KEY)
  );
  const preset = getSitePreset(siteKey);
  const savedApiBase = resolveSiteBoundApiBase(savedSession?.apiBase, siteKey);
  const savedWebBase = resolveSiteBoundWebBase(savedSession?.webBase, siteKey);
  return {
    siteKey,
    siteLabel: preset.label,
    apiBase: trimTrailingSlash(
      pinToSavedSession
        ? savedApiBase
        : (String(args.apiBase || "").trim() ? resolveSiteBoundApiBase(args.apiBase, siteKey) : savedApiBase)
    ),
    webBase: trimTrailingSlash(
      pinToSavedSession
        ? savedWebBase
        : (String(args.webBase || "").trim() ? resolveSiteBoundWebBase(args.webBase, siteKey) : savedWebBase)
    ),
    locale: normalizeLocale(args.locale || savedSession?.locale || preset.locale, preset.locale),
    sessionFile: args.sessionFile || DEFAULT_SESSION_FILE,
    token: normalizeToken(args.token || savedSession?.token || ""),
    tokenId: String(savedSession?.tokenId || "").trim(),
    loginEmail: String(savedSession?.loginEmail || "").trim(),
    subUserEmail: String(savedSession?.subUserEmail || "").trim()
  };
}

function buildRequestHeaders(session, { auth = true, locale, contentType = "application/json" } = {}) {
  const headers = {
    Accept: "application/json",
    "X-Request-Locale": normalizeLocale(locale || session.locale, session.locale)
  };
  if (contentType) {
    headers["Content-Type"] = contentType;
  }
  if (auth && session.token) {
    headers.Authorization = `Bearer ${normalizeToken(session.token)}`;
  }
  return headers;
}

function createApiError(message, extras = {}) {
  const error = new Error(message);
  Object.assign(error, extras);
  return error;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let payload = null;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {}

  if (!response.ok) {
    const message = payload?.error_message || payload?.detail || text || `HTTP ${response.status}`;
    throw createApiError(`HTTP ${response.status}: ${message}`, {
      status: response.status,
      payload
    });
  }

  return payload;
}

async function requestStandard(session, pathname, { method = "GET", body, auth = true, locale } = {}) {
  const payload = await requestJson(joinUrl(session.apiBase, pathname), {
    method,
    headers: buildRequestHeaders(session, { auth, locale }),
    body: body === undefined ? undefined : JSON.stringify(body)
  });

  if (!payload || typeof payload !== "object") {
    throw createApiError(`Invalid JSON response from ${pathname}`);
  }
  if (typeof payload.error_code === "number" && payload.error_code !== 0) {
    throw createApiError(payload.error_message || `API error ${payload.error_code} from ${pathname}`, {
      status: payload.error_code === 401 ? 401 : undefined,
      payload
    });
  }
  return payload;
}

function isAuthError(error) {
  if (!error) {
    return false;
  }
  if (error.status === 401) {
    return true;
  }
  const message = String(error.message || "").toLowerCase();
  return message.includes("unauthorized") || message.includes("http 401");
}

async function promptValue(rl, label, defaultValue = "", { optional = false } = {}) {
  const suffix = defaultValue ? ` [${defaultValue}]` : "";
  const answer = (await rl.question(`${label}${suffix}: `)).trim();
  if (answer) {
    return answer;
  }
  if (defaultValue) {
    return defaultValue;
  }
  if (optional) {
    return "";
  }
  return promptValue(rl, label, defaultValue, { optional });
}

async function promptChoice(rl, label, options, defaultIndex = 0) {
  process.stdout.write(`${label}\n`);
  options.forEach((option, index) => {
    const marker = index === defaultIndex ? "*" : " ";
    process.stdout.write(` ${marker} ${index + 1}. ${option.label}\n`);
  });
  const raw = (await rl.question(`Choose [${defaultIndex + 1}]: `)).trim();
  const numeric = raw ? Number.parseInt(raw, 10) : defaultIndex + 1;
  if (Number.isFinite(numeric) && numeric >= 1 && numeric <= options.length) {
    return options[numeric - 1].value;
  }
  const matched = options.find((option) => option.value === raw);
  if (matched) {
    return matched.value;
  }
  return options[defaultIndex].value;
}

async function promptMultiline(rl, label) {
  process.stdout.write(`${label}\n`);
  process.stdout.write("Finish with a single dot on its own line.\n");
  const lines = [];
  while (true) {
    const line = await rl.question("> ");
    if (line === ".") {
      break;
    }
    lines.push(line);
  }
  return lines.join("\n").trim();
}

async function maybeReadStdin() {
  if (process.stdin.isTTY) {
    return "";
  }
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

function mimeTypeToExtension(mimeType) {
  const normalized = String(mimeType || "").trim().toLowerCase();
  if (!normalized) {
    return "";
  }
  if (normalized === "image/svg+xml") {
    return "svg";
  }
  if (normalized === "image/jpeg") {
    return "jpg";
  }
  if (normalized.startsWith("image/")) {
    return normalized.slice("image/".length).replace(/[^a-z0-9]+/g, "") || "";
  }
  return "";
}

function detectImageExtension(buffer) {
  if (!buffer || buffer.length === 0) {
    return "";
  }
  if (
    buffer.length >= 8 &&
    buffer[0] === 0x89 &&
    buffer[1] === 0x50 &&
    buffer[2] === 0x4e &&
    buffer[3] === 0x47 &&
    buffer[4] === 0x0d &&
    buffer[5] === 0x0a &&
    buffer[6] === 0x1a &&
    buffer[7] === 0x0a
  ) {
    return "png";
  }
  if (buffer.length >= 3 && buffer[0] === 0xff && buffer[1] === 0xd8 && buffer[2] === 0xff) {
    return "jpg";
  }
  if (buffer.length >= 6) {
    const header = buffer.subarray(0, 6).toString("ascii");
    if (header === "GIF87a" || header === "GIF89a") {
      return "gif";
    }
  }
  if (buffer.length >= 12) {
    const riff = buffer.subarray(0, 4).toString("ascii");
    const webp = buffer.subarray(8, 12).toString("ascii");
    if (riff === "RIFF" && webp === "WEBP") {
      return "webp";
    }
  }
  const leadingText = buffer.subarray(0, Math.min(buffer.length, 256)).toString("utf8").trimStart();
  if (leadingText.startsWith("<svg") || leadingText.startsWith("<?xml")) {
    return "svg";
  }
  return "";
}

function decodeCaptchaImage(imageValue) {
  const raw = String(imageValue || "").trim();
  if (!raw) {
    throw createApiError("Received empty CAPTCHA image payload");
  }

  if (raw.startsWith("data:")) {
    const commaIndex = raw.indexOf(",");
    if (commaIndex === -1) {
      throw createApiError("Received malformed CAPTCHA data URL");
    }
    const header = raw.slice("data:".length, commaIndex);
    const payload = raw.slice(commaIndex + 1);
    const [mimeType = ""] = header.split(";", 1);
    const isBase64 = /(?:^|;)base64(?:;|$)/i.test(header);
    const buffer = isBase64
      ? Buffer.from(payload, "base64")
      : Buffer.from(decodeURIComponent(payload), "utf8");

    if (buffer.length === 0) {
      throw createApiError("Decoded CAPTCHA image is empty");
    }
    return {
      buffer,
      extension: mimeTypeToExtension(mimeType) || detectImageExtension(buffer) || "png"
    };
  }

  const buffer = Buffer.from(raw, "base64");
  if (buffer.length === 0) {
    throw createApiError("Decoded CAPTCHA image is empty");
  }
  return {
    buffer,
    extension: detectImageExtension(buffer) || "png"
  };
}

function extensionToMimeType(extension) {
  const normalized = String(extension || "").trim().toLowerCase().replace(/^\./, "");
  if (normalized === "png") {
    return "image/png";
  }
  if (normalized === "jpg" || normalized === "jpeg") {
    return "image/jpeg";
  }
  if (normalized === "gif") {
    return "image/gif";
  }
  if (normalized === "webp") {
    return "image/webp";
  }
  if (normalized === "svg") {
    return "image/svg+xml";
  }
  return normalized ? `image/${normalized}` : "application/octet-stream";
}

async function resolveCaptchaMediaReference(captchaFile, captchaDataUrl) {
  const explicitDataUrl = String(captchaDataUrl || "").trim();
  if (isImageDataUrl(explicitDataUrl)) {
    return explicitDataUrl;
  }
  const safeCaptchaFile = sanitizeCaptchaFilePath(captchaFile);
  if (!safeCaptchaFile) {
    return "";
  }
  return safeCaptchaFile;
}

async function writeCaptchaImage(sessionFile, base64Image) {
  const captchaDir = DEFAULT_CAPTCHA_DIR;
  const { buffer, extension } = decodeCaptchaImage(base64Image);
  const filename = path.join(captchaDir, `captcha-${Date.now()}.${extension}`);
  await ensureDirectory(captchaDir);
  await fs.writeFile(filename, buffer);
  await fs.chmod(filename, 0o600).catch(() => {});
  return filename;
}

async function fetchCaptcha(session) {
  const payload = await requestJson(joinUrl(session.apiBase, "/auth/captcha/generate"), {
    method: "GET",
    headers: buildRequestHeaders(session, { auth: false, locale: session.locale, contentType: null })
  });
  if (!payload?.captcha_id || !payload?.image_base64) {
    throw createApiError("Failed to fetch CAPTCHA image");
  }
  return payload;
}

async function sendEmailCode(session, { email, subUserEmail, captchaId, captchaText }) {
  return requestStandard(session, "/auth/email-code/send", {
    method: "POST",
    auth: false,
    body: {
      email,
      captcha_id: captchaId,
      captcha_text: captchaText,
      is_sub_user: Boolean(subUserEmail),
      sub_user_email: subUserEmail || undefined
    }
  });
}

async function verifyEmailCode(session, { email, subUserEmail, verificationCode }) {
  return requestStandard(session, "/auth/email-code/verify", {
    method: "POST",
    auth: false,
    body: {
      email,
      verification_code: verificationCode,
      is_sub_user: Boolean(subUserEmail),
      sub_user_email: subUserEmail || undefined
    }
  });
}

async function listProjects(session) {
  const payload = await requestStandard(session, "/projects");
  return Array.isArray(payload.data) ? payload.data : [];
}

async function createEpisode(session, body) {
  const payload = await requestStandard(session, "/scripts/create_async", {
    method: "POST",
    body
  });
  const videoId = String(payload?.data?.video_id || "").trim();
  if (!videoId) {
    throw createApiError("Script creation succeeded but video_id is missing");
  }
  return {
    videoId,
    queryId: String(payload?.data?.query_id || "").trim()
  };
}

async function getScriptTaskStatus(session, videoId) {
  const encoded = encodeURIComponent(videoId);
  const payload = await requestStandard(session, `/scripts/task_status?video_id=${encoded}&step=create_script`, {
    method: "GET"
  });
  return payload.data || {};
}

async function expireCurrentToken(session) {
  if (!session.tokenId) {
    return { revoked: false, remoteAttempted: false };
  }
  try {
    await requestStandard(session, `/access/tokens/${encodeURIComponent(session.tokenId)}`, {
      method: "PUT",
      body: {
        expires_at: new Date().toISOString()
      }
    });
    return { revoked: true, remoteAttempted: true };
  } catch {
    return { revoked: false, remoteAttempted: true };
  }
}

function buildProjectUrl(session, project) {
  const params = new URLSearchParams({
    projectId: String(project.project_id || "")
  });
  if (project.name) {
    params.set("projectName", String(project.name));
  }
  return `${trimTrailingSlash(session.webBase)}/${session.locale}/projects/videos?${params.toString()}`;
}

function buildEpisodeUrl(session, videoId, project) {
  const params = new URLSearchParams({
    video_id: String(videoId || "")
  });
  if (project?.project_id) {
    params.set("enter_from", "projects");
    params.set("projectId", String(project.project_id));
  }
  if (project?.name) {
    params.set("projectName", String(project.name));
  }
  return `${trimTrailingSlash(session.webBase)}/${session.locale}/comic/elements?${params.toString()}`;
}

function formatTable(headers, rows) {
  const widths = headers.map((header, headerIndex) => {
    const columnValues = rows.map((row) => String(row[headerIndex] ?? ""));
    const maxValueLength = columnValues.reduce((max, value) => Math.max(max, value.length), 0);
    return Math.max(header.length, maxValueLength);
  });

  const renderRow = (cells) =>
    cells
      .map((cell, index) => String(cell ?? "").padEnd(widths[index], " "))
      .join(" | ");

  const separator = widths.map((width) => "-".repeat(width)).join("-|-");
  return [renderRow(headers), separator, ...rows.map(renderRow)].join("\n");
}

function buildCreateEpisodeResultContext(session, {
  locale,
  queryId = "",
  videoId = "",
  title = "",
  styleMode = "",
  style = "",
  aspectRatio = "",
  selectedProject = null
} = {}) {
  return {
    site_key: session.siteKey,
    site_label: session.siteLabel,
    locale: locale || session.locale,
    query_id: queryId,
    video_id: videoId,
    title,
    style_mode: styleMode,
    style: style || "",
    aspect_ratio: aspectRatio,
    project_id: selectedProject?.project_id || "",
    project_name: selectedProject?.name || "",
    project_url: selectedProject?.project_id ? buildProjectUrl({ ...session, locale: locale || session.locale }, selectedProject) : "",
    episode_url: videoId ? buildEpisodeUrl({ ...session, locale: locale || session.locale }, videoId, selectedProject) : ""
  };
}

function printHelp() {
  const lines = [
    "Usage:",
    "  vibevideo-studio.mjs login [--site bollo|vibevideo] [--email owner@example.com] [--sub-user-email sub@example.com]",
    "  vibevideo-studio.mjs projects",
    "  vibevideo-studio.mjs create-episode --text \"...\" [--title \"...\"] [--style-mode auto-realistic|auto-anime|manual]",
    "  vibevideo-studio.mjs logout",
    "",
    "Options:",
    "  --site            Choose bollo.video or vibevideo.io. Default: bollo.video",
    "  --session-file    Override saved session path",
    "  --no-save         Keep the login session in memory only for this run",
    "  --json            Print JSON payloads instead of human-readable text",
    "  --no-inline-media Never print MEDIA: attachments; expose local file paths only",
    "  --timeout         Episode polling timeout in seconds",
    "  --poll-interval   Episode polling interval in seconds",
    "",
    "Create episode options:",
    "  --file            Read script text from a local file",
    "  --project-id      Save into an existing Studio project; omit for unclassified",
    "  --aspect-ratio    Example: 16:9, 9:16, 1:1",
    "  --style-mode      auto-realistic | auto-anime | manual",
    "  --style           Manual style text when --style-mode manual is used",
    "",
    "Examples:",
    "  node vibevideo-studio.mjs login --site bollo",
    "  node vibevideo-studio.mjs login --captcha-text abcd",
    "  node vibevideo-studio.mjs login --verification-code 123456",
    "  node vibevideo-studio.mjs projects",
    "  node vibevideo-studio.mjs create-episode --file /tmp/script.txt --style-mode auto-realistic --aspect-ratio 16:9",
    "  cat /tmp/script.txt | node vibevideo-studio.mjs create-episode --style-mode auto-anime",
    "  node vibevideo-studio.mjs logout"
  ];
  process.stdout.write(`${lines.join("\n")}\n`);
}

function printResult(args, data) {
  if (args.json) {
    process.stdout.write(`${JSON.stringify({ error_code: 0, data, error_message: "" }, null, 2)}\n`);
    return;
  }

  if (data.kind === "login") {
    process.stdout.write(`Logged in to ${data.site_label} as ${data.login_email}${data.sub_user_email ? ` (sub-user: ${data.sub_user_email})` : ""}.\n`);
    process.stdout.write(`Session saved: ${data.session_file}\n`);
    process.stdout.write(`Token ID: ${data.token_id || "n/a"}\n`);
    return;
  }

  if (data.kind === "login-captcha-required") {
    process.stdout.write(`CAPTCHA is required for ${data.site_label} login.\n`);
    if (data.captcha_delivery?.delivered && data.captcha_delivery?.channel && data.captcha_delivery.channel !== "webchat") {
      process.stdout.write("The CAPTCHA image has been sent to the current chat channel.\n");
    } else if (!args.noInlineMedia && data.captcha_media_ref && shouldInlineCaptchaMediaForCurrentOutput()) {
      process.stdout.write("The CAPTCHA image is attached below.\n");
      process.stdout.write(`MEDIA:${data.captcha_media_ref}\n`);
    } else if (!args.noInlineMedia && shouldEmitOpenClawMediaDirective(data.captcha_file)) {
      process.stdout.write("The CAPTCHA image is attached below in the current OpenClaw conversation.\n");
      process.stdout.write(`MEDIA:${data.captcha_media_ref || data.captcha_file}\n`);
    } else if (data.captcha_delivery?.delivered) {
      process.stdout.write("The CAPTCHA image has been prepared for the current OpenClaw conversation.\n");
    } else {
      process.stdout.write(`CAPTCHA image saved to: ${data.captcha_file}\n`);
      if (data.captcha_delivery?.reason) {
        process.stdout.write(`Auto-send unavailable: ${data.captcha_delivery.reason}\n`);
      }
    }
    process.stdout.write(`${data.next_step}\n`);
    return;
  }

  if (data.kind === "login-email-code-required") {
    process.stdout.write(`Email verification code is required for ${data.site_label} login.\n`);
    if (data.login_email) {
      process.stdout.write(`Email: ${data.login_email}${data.sub_user_email ? ` (sub-user: ${data.sub_user_email})` : ""}\n`);
    }
    process.stdout.write(`${data.next_step}\n`);
    return;
  }

  if (data.kind === "projects") {
    if (!data.projects.length) {
      process.stdout.write(`No Studio projects found on ${data.site_label}.\n`);
      return;
    }
    const rows = data.projects.map((project) => [
      project.project_id,
      project.name || "Untitled",
      String(project.video_count ?? 0),
      project.url
    ]);
    process.stdout.write(`${formatTable(["Project ID", "Name", "Videos", "URL"], rows)}\n`);
    return;
  }

  if (data.kind === "create-episode") {
    process.stdout.write(`Episode draft created on ${data.site_label}.\n`);
    process.stdout.write(`Video ID: ${data.video_id}\n`);
    process.stdout.write(`Aspect ratio: ${data.aspect_ratio}\n`);
    process.stdout.write(`Style mode: ${data.style_mode}\n`);
    if (data.project_name) {
      process.stdout.write(`Project: ${data.project_name} (${data.project_id})\n`);
      process.stdout.write(`Project URL: ${data.project_url}\n`);
    } else {
      process.stdout.write("Project: Unclassified\n");
    }
    process.stdout.write(`Episode URL: ${data.episode_url}\n`);
    return;
  }

  if (data.kind === "logout") {
    process.stdout.write(`Logged out from ${data.site_label || "saved session"}.\n`);
    process.stdout.write(`Session cleared: ${data.session_file}\n`);
    if (data.remote_attempted) {
      process.stdout.write(`Remote token revoke: ${data.remote_revoked ? "attempted and updated" : "attempted but skipped/failed"}\n`);
    }
  }
}

async function ensureSession(args, rl) {
  const savedSession = await readJsonFile(args.sessionFile || DEFAULT_SESSION_FILE);
  const savedSessionConflicts = collectSavedSessionSiteConflicts(args, savedSession);
  if (savedSessionConflicts.length > 0) {
    const savedSiteLabel = SITE_PRESETS[normalizeSite(savedSession?.siteKey)]?.label || "saved site";
    throw createApiError(
      `Saved login state is pinned to ${savedSiteLabel}. Ignore the conflicting ${savedSessionConflicts.join(", ")} arguments or run \`login\` again to switch sites.`
    );
  }
  const session = buildResolvedSession(args, savedSession);
  if (
    hasSavedAuthenticatedSession(savedSession) &&
    (
      normalizeSite(savedSession?.siteKey) !== session.siteKey ||
      trimTrailingSlash(savedSession?.apiBase || "") !== session.apiBase ||
      trimTrailingSlash(savedSession?.webBase || "") !== session.webBase ||
      normalizeLocale(savedSession?.locale || "", session.locale) !== session.locale
    )
  ) {
    await writeSecureFile(session.sessionFile, `${JSON.stringify({
      ...savedSession,
      siteKey: session.siteKey,
      apiBase: session.apiBase,
      webBase: session.webBase,
      locale: session.locale,
      token: session.token,
      tokenId: session.tokenId,
      loginEmail: session.loginEmail,
      subUserEmail: session.subUserEmail,
      savedAt: savedSession?.savedAt || new Date().toISOString()
    }, null, 2)}\n`);
  }
  if (session.token) {
    return session;
  }
  if (!isInteractive()) {
    throw createApiError(`No saved session found. Run login first or provide --token. Session file: ${session.sessionFile}`);
  }
  process.stdout.write("No saved session found. Starting login.\n");
  const loginPayload = await performLogin(args, rl, { quiet: true });
  return loginPayload.session;
}

function buildResolvedPendingSession(args, pendingState, savedSession) {
  const pendingLikeSession = pendingState ? {
    siteKey: pendingState.siteKey,
    apiBase: pendingState.apiBase,
    webBase: pendingState.webBase,
    locale: pendingState.locale,
    loginEmail: pendingState.loginEmail,
    subUserEmail: pendingState.subUserEmail
  } : savedSession;
  return buildResolvedSession({
    ...args,
    site: args.site || pendingState?.siteKey || args.site,
    locale: args.locale || pendingState?.locale || args.locale
  }, pendingLikeSession);
}

function shouldStartFreshLogin(args) {
  return Boolean(
    String(args.email || "").trim() ||
    String(args.subUserEmail || "").trim() ||
    String(args.site || "").trim() ||
    String(args.apiBase || "").trim() ||
    String(args.webBase || "").trim() ||
    String(args.locale || "").trim()
  );
}

function hasPendingLoginContinuationInput(args) {
  return Boolean(
    String(args.captchaText || "").trim() ||
    String(args.verificationCode || "").trim()
  );
}

function normalizeComparableUrl(value) {
  return trimTrailingSlash(String(value || "")).toLowerCase();
}

function normalizeComparableLocale(value, fallback = "zh") {
  return normalizeLocale(value, fallback).toLowerCase();
}

function collectPendingContextConflicts(args, pendingState) {
  if (!pendingState || typeof pendingState !== "object") {
    return [];
  }

  const conflicts = [];
  const providedEmail = String(args.email || "").trim().toLowerCase();
  const pendingEmail = String(pendingState.loginEmail || "").trim().toLowerCase();
  if (providedEmail && pendingEmail && providedEmail !== pendingEmail) {
    conflicts.push("owner email");
  }

  const providedSubUserEmail = String(args.subUserEmail || "").trim().toLowerCase();
  const pendingSubUserEmail = String(pendingState.subUserEmail || "").trim().toLowerCase();
  if (providedSubUserEmail && providedSubUserEmail !== pendingSubUserEmail) {
    conflicts.push("sub-user email");
  }

  const providedSite = String(args.site || "").trim() ? normalizeSite(args.site) : "";
  const pendingSite = String(pendingState.siteKey || "").trim() ? normalizeSite(pendingState.siteKey) : "";
  if (providedSite && pendingSite && providedSite !== pendingSite) {
    conflicts.push("site");
  }

  const providedApiBase = normalizeComparableUrl(args.apiBase);
  const pendingApiBase = normalizeComparableUrl(pendingState.apiBase);
  if (providedApiBase && pendingApiBase && providedApiBase !== pendingApiBase) {
    conflicts.push("api base");
  }

  const providedWebBase = normalizeComparableUrl(args.webBase);
  const pendingWebBase = normalizeComparableUrl(pendingState.webBase);
  if (providedWebBase && pendingWebBase && providedWebBase !== pendingWebBase) {
    conflicts.push("web base");
  }

  const providedLocale = String(args.locale || "").trim()
    ? normalizeComparableLocale(args.locale, pendingState.locale || "zh")
    : "";
  const pendingLocale = String(pendingState.locale || "").trim()
    ? normalizeComparableLocale(pendingState.locale, "zh")
    : "";
  if (providedLocale && pendingLocale && providedLocale !== pendingLocale) {
    conflicts.push("locale");
  }

  return conflicts;
}

function resolvePendingLoginResume(args, pendingState) {
  const hasContinuationInput = hasPendingLoginContinuationInput(args);
  if (!pendingState) {
    return {
      shouldResume: false,
      missingPending: hasContinuationInput,
      conflicts: []
    };
  }

  if (!hasContinuationInput) {
    return {
      shouldResume: !shouldStartFreshLogin(args),
      missingPending: false,
      conflicts: []
    };
  }

  const conflicts = collectPendingContextConflicts(args, pendingState);
  return {
    shouldResume: conflicts.length === 0,
    missingPending: false,
    conflicts
  };
}

async function performLogin(args, rl, options = {}) {
  const savedSession = await readJsonFile(args.sessionFile || DEFAULT_SESSION_FILE);
  const pendingFile = getPendingLoginFile(args.sessionFile || DEFAULT_SESSION_FILE);
  const rawPendingState = await readJsonFile(pendingFile);
  const currentPendingState = isPendingLoginStateFresh(rawPendingState) ? rawPendingState : null;
  if (rawPendingState && !currentPendingState) {
    await deleteFileIfExists(pendingFile);
  }
  const pendingResume = resolvePendingLoginResume(args, currentPendingState);
  if (pendingResume.missingPending) {
    throw createApiError(
      "No pending login state was found for the provided CAPTCHA or email verification code. Start login again without continuation flags to fetch a fresh CAPTCHA."
    );
  }
  if (pendingResume.conflicts.length > 0) {
    throw createApiError(
      `The provided continuation arguments do not match the current pending login (${pendingResume.conflicts.join(", ")}). Continue with the same login context or start a new login without continuation flags.`
    );
  }
  const shouldResumePending = pendingResume.shouldResume;
  const baseSession = buildResolvedPendingSession(args, shouldResumePending ? currentPendingState : null, savedSession);
  const siteKey = args.site
    ? normalizeSite(args.site)
    : currentPendingState?.siteKey && shouldResumePending
      ? normalizeSite(currentPendingState.siteKey)
      : isInteractive()
        ? await promptChoice(rl, "Choose login site", [
            { label: "bollo.video (China, default)", value: "bollo" },
            { label: "vibevideo.io (International)", value: "vibevideo" }
          ], 0)
        : baseSession.siteKey;
  const preset = SITE_PRESETS[siteKey];
  const session = buildResolvedSession({
    ...args,
    site: siteKey,
    apiBase: args.apiBase || (shouldResumePending ? currentPendingState?.apiBase : ""),
    webBase: args.webBase || (shouldResumePending ? currentPendingState?.webBase : ""),
    locale: args.locale || (shouldResumePending ? currentPendingState?.locale : "") || preset.locale
  }, savedSession);

  const email = String(args.email || "").trim() || String(shouldResumePending ? currentPendingState?.loginEmail : "").trim() || (isInteractive() ? await promptValue(rl, "Owner email") : "");
  if (!email) {
    throw createApiError("Owner email is required");
  }
  const subUserEmail = String(args.subUserEmail || "").trim() || String(shouldResumePending ? currentPendingState?.subUserEmail : "").trim() || (isInteractive() ? await promptValue(rl, "Sub-user email (optional)", "", { optional: true }) : "");

  let pendingState = shouldResumePending ? currentPendingState : null;
  if (!pendingState || pendingState.stage !== "awaiting_email_code") {
    const pendingCaptchaFile = String(pendingState?.captchaFile || "").trim();
    const pendingCaptchaDataUrl = String(pendingState?.captchaImageDataUrl || "").trim();
    const pendingCaptchaUsable = Boolean(
      pendingCaptchaDataUrl ||
      (pendingCaptchaFile && await fileExists(pendingCaptchaFile))
    );
    const shouldReuseCaptcha = Boolean(
      pendingState &&
      pendingState.stage === "awaiting_captcha" &&
      pendingState.captchaId &&
      pendingCaptchaFile &&
      pendingCaptchaUsable &&
      shouldResumePending
    );

    let captchaId = String(pendingState?.captchaId || "").trim();
    let captchaFile = pendingCaptchaFile;
    let captchaDataUrl = pendingCaptchaDataUrl;

    if (!shouldReuseCaptcha) {
      const captchaPayload = await fetchCaptcha(session);
      captchaId = String(captchaPayload.captcha_id || "").trim();
      captchaFile = await writeCaptchaImage(session.sessionFile, captchaPayload.image_base64);
      captchaDataUrl = String(captchaPayload.image_base64 || "").trim();
      pendingState = {
        stage: "awaiting_captcha",
        siteKey: session.siteKey,
        apiBase: session.apiBase,
        webBase: session.webBase,
        locale: session.locale,
        loginEmail: email,
        subUserEmail: subUserEmail || "",
        captchaId,
        captchaFile,
        captchaImageDataUrl: captchaDataUrl,
        createdAt: new Date().toISOString(),
        captchaIssuedAt: new Date().toISOString()
      };
      await writePendingLoginState(pendingFile, pendingState);
    }

    if (!options.quiet && captchaFile && isInteractive()) {
      process.stdout.write(`CAPTCHA image saved to: ${captchaFile}\n`);
    }

    const captchaText = String(args.captchaText || "").trim() || (isInteractive() ? await promptValue(rl, "Type CAPTCHA text from the image") : "");
    if (!captchaText) {
      const captchaDelivery = captchaFile ? await maybeSendCaptchaToCurrentConversation(session, captchaFile) : { attempted: false, delivered: false, reason: "captcha image unavailable" };
      const captchaMediaRef = args.noInlineMedia ? "" : await resolveCaptchaMediaReference(captchaFile, captchaDataUrl);
      return {
        session: null,
        result: {
          kind: "login-captcha-required",
          site_key: session.siteKey,
          site_label: session.siteLabel,
          locale: session.locale,
          login_email: email,
          sub_user_email: subUserEmail || "",
          captcha_file: captchaFile,
          captcha_media_ref: captchaMediaRef,
          captcha_delivery: captchaDelivery,
          pending_file: pendingFile,
          next_step: session.locale === "zh"
            ? "请直接回复验证码字符，然后重新运行 `login --captcha-text <验证码>`，我会继续发送邮箱验证码。"
            : "Reply with the CAPTCHA text, then rerun `login --captcha-text <captcha>` so I can send the email verification code."
        }
      };
    }

    try {
      await sendEmailCode(session, {
        email,
        subUserEmail,
        captchaId,
        captchaText
      });
    } catch (error) {
      await deleteFileIfExists(pendingFile);
      throw createApiError(`${error instanceof Error ? error.message : String(error)}. CAPTCHA expired or was incorrect; start login again to get a fresh image.`);
    }

    pendingState = {
      stage: "awaiting_email_code",
      siteKey: session.siteKey,
      apiBase: session.apiBase,
      webBase: session.webBase,
      locale: session.locale,
      loginEmail: email,
      subUserEmail: subUserEmail || "",
      createdAt: pendingState?.createdAt || new Date().toISOString(),
      emailCodeSentAt: new Date().toISOString()
    };
    await writePendingLoginState(pendingFile, pendingState);
  }

  const verificationCode = String(args.verificationCode || "").trim() || (isInteractive() ? await promptValue(rl, "Email verification code") : "");
  if (!verificationCode) {
    return {
      session: null,
      result: {
        kind: "login-email-code-required",
        site_key: session.siteKey,
        site_label: session.siteLabel,
        locale: session.locale,
        login_email: email,
        sub_user_email: subUserEmail || "",
        pending_file: pendingFile,
        next_step: session.locale === "zh"
          ? "邮箱验证码已发送。请回复验证码，然后重新运行 `login --verification-code <验证码>` 完成登录。"
          : "The email verification code has been sent. Reply with the code, then rerun `login --verification-code <code>` to finish login."
      }
    };
  }

  const verifyPayload = await verifyEmailCode(session, {
    email,
    subUserEmail,
    verificationCode
  });

  const accessToken = normalizeToken(verifyPayload?.data?.access_token || "");
  if (!accessToken) {
    throw createApiError("Login succeeded but access token is missing");
  }

  const storedSession = {
    siteKey: session.siteKey,
    apiBase: session.apiBase,
    webBase: session.webBase,
    locale: session.locale,
    token: accessToken,
    tokenId: String(verifyPayload?.data?.token_id || "").trim(),
    loginEmail: email,
    subUserEmail: subUserEmail || "",
    savedAt: new Date().toISOString()
  };

  if (!args.noSave) {
    await writeSecureFile(session.sessionFile, `${JSON.stringify(storedSession, null, 2)}\n`);
  }
  await deleteFileIfExists(pendingFile);

  return {
    session: {
      ...storedSession,
      siteLabel: session.siteLabel,
      sessionFile: session.sessionFile
    },
    result: {
      kind: "login",
      site_key: session.siteKey,
      site_label: session.siteLabel,
      api_base: session.apiBase,
      web_base: session.webBase,
    locale: session.locale,
    login_email: email,
      sub_user_email: subUserEmail || "",
      token_id: storedSession.tokenId,
      session_file: session.sessionFile,
      token_saved: !args.noSave
    }
  };
}

async function runLogin(args, rl, options = {}) {
  const payload = await performLogin(args, rl, options);
  return payload.result;
}

async function runProjects(args, rl) {
  const data = await runWithSession(args, rl, async (session) => {
    const projects = await listProjects(session);
    return {
      kind: "projects",
      site_key: session.siteKey,
      site_label: session.siteLabel,
      locale: session.locale,
      projects: projects.map((project) => ({
        ...project,
        url: buildProjectUrl(session, project)
      }))
    };
  });
  return data;
}

async function chooseProject(args, rl, session) {
  const projects = await listProjects(session);
  if (args.projectId) {
    const matched = projects.find((project) => String(project.project_id) === String(args.projectId));
    return matched || { project_id: args.projectId, name: "" };
  }
  if (!isInteractive()) {
    return null;
  }
  const options = [
    { label: "Unclassified", value: "" },
    ...projects.map((project) => ({
      label: `${project.name || "Untitled"} (${project.project_id})`,
      value: String(project.project_id)
    }))
  ];
  const selectedProjectId = await promptChoice(rl, "Choose target Studio project", options, 0);
  if (!selectedProjectId) {
    return null;
  }
  return projects.find((project) => String(project.project_id) === selectedProjectId) || null;
}

async function readScriptInput(args, rl, session) {
  if (args.file) {
    return readTextFile(path.resolve(args.file));
  }
  if (String(args.text || "").trim()) {
    return String(args.text).trim();
  }
  const stdin = await maybeReadStdin();
  if (String(stdin || "").trim()) {
    return String(stdin).trim();
  }
  if (isInteractive()) {
    const locale = session?.locale || "en";
    return promptMultiline(rl, locale === "zh" ? "粘贴剧本内容" : "Paste the script content");
  }
  return "";
}

async function chooseStyleMode(args, rl) {
  const normalized = normalizeStyleMode(args.styleMode);
  if (normalized) {
    return normalized;
  }
  if (!isInteractive()) {
    return "auto-realistic";
  }
  return promptChoice(rl, "Choose style mode", [
    { label: "AI recommend realistic", value: "auto-realistic" },
    { label: "AI recommend animation", value: "auto-anime" },
    { label: "Manual style", value: "manual" }
  ], 0);
}

async function chooseAspectRatio(args, rl) {
  const provided = String(args.aspectRatio || "").trim();
  if (provided) {
    return provided;
  }
  if (!isInteractive()) {
    return DEFAULT_ASPECT_RATIO;
  }
  return promptChoice(rl, "Choose aspect ratio", [
    { label: "16:9", value: "16:9" },
    { label: "9:16", value: "9:16" },
    { label: "1:1", value: "1:1" },
    { label: "4:3", value: "4:3" },
    { label: "3:4", value: "3:4" }
  ], 0);
}

async function waitForEpisodeReady(session, videoId, timeoutSeconds, pollIntervalSeconds) {
  const deadline = Date.now() + Math.max(30, timeoutSeconds) * 1000;
  const intervalMs = Math.max(1, pollIntervalSeconds) * 1000;

  while (Date.now() < deadline) {
    const status = await getScriptTaskStatus(session, videoId);
    if (status.success) {
      return status;
    }
    await sleep(intervalMs);
  }

  throw createApiError(`Timed out after ${timeoutSeconds}s waiting for create_script`, {
    status: 408
  });
}

async function runCreateEpisode(args, rl) {
  return runWithSession(args, rl, async (session) => {
    const text = String(await readScriptInput(args, rl, session) || "").trim();
    if (!text) {
      throw createApiError("Script text is required. Use --text, --file, stdin, or interactive input.");
    }

    const effectiveLocale = normalizeLocale(args.locale || session.locale, detectLocaleFromText(text, session.locale));
    const styleMode = await chooseStyleMode(args, rl);
    const aspectRatio = await chooseAspectRatio(args, rl);
    const title = String(args.title || "").trim() || deriveTitle(text, effectiveLocale);
    const selectedProject = await chooseProject(args, rl, session);

    let manualStyle = String(args.style || "").trim();
    if (styleMode === "manual" && !manualStyle && isInteractive()) {
      manualStyle = await promptValue(rl, "Manual style");
    }
    if (styleMode === "manual" && !manualStyle) {
      throw createApiError("Manual style text is required when --style-mode manual is used.");
    }

    const requestBody = {
      prompt: text,
      title,
      aspect_ratio: aspectRatio,
      project_id: selectedProject?.project_id || undefined,
      use_auto_style: styleMode !== "manual",
      auto_style_category: styleMode === "auto-anime" ? "anime" : styleMode === "auto-realistic" ? "realistic" : undefined,
      style: styleMode === "manual" ? manualStyle : undefined
    };

    let videoId = "";
    let queryId = "";
    try {
      const created = await createEpisode({
        ...session,
        locale: effectiveLocale
      }, requestBody);
      videoId = created.videoId;
      queryId = created.queryId;

      await waitForEpisodeReady({
        ...session,
        locale: effectiveLocale
      }, videoId, args.timeoutSeconds, args.pollIntervalSeconds);

      return {
        kind: "create-episode",
        ...buildCreateEpisodeResultContext(session, {
          locale: effectiveLocale,
          queryId,
          videoId,
          title,
          styleMode,
          style: manualStyle || "",
          aspectRatio,
          selectedProject
        })
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      throw createApiError(message, {
        ...(error && typeof error === "object" ? error : {}),
        data: {
          kind: "create-episode-failed",
          ...buildCreateEpisodeResultContext(session, {
            locale: effectiveLocale,
            queryId,
            videoId,
            title,
            styleMode,
            style: manualStyle || "",
            aspectRatio,
            selectedProject
          })
        }
      });
    }
  });
}

async function runLogout(args) {
  const savedSession = await readJsonFile(args.sessionFile || DEFAULT_SESSION_FILE);
  const session = buildResolvedSession(args, savedSession);
  const revokeResult = session.token ? await expireCurrentToken(session) : { revoked: false, remoteAttempted: false };
  await deleteFileIfExists(session.sessionFile);
  await deleteFileIfExists(getPendingLoginFile(session.sessionFile));
  return {
    kind: "logout",
    site_key: session.siteKey,
    site_label: session.siteLabel,
    session_file: session.sessionFile,
    remote_attempted: revokeResult.remoteAttempted,
    remote_revoked: revokeResult.revoked
  };
}

async function runWithSession(args, rl, runner) {
  let session = await ensureSession(args, rl);
  try {
    return await runner(session);
  } catch (error) {
    if (isInteractive() && !args.token && isAuthError(error)) {
      process.stdout.write("Saved session is no longer valid. Starting login again.\n");
      await deleteFileIfExists(session.sessionFile);
      const loginPayload = await performLogin(args, rl, { quiet: true });
      session = buildResolvedSession(args, {
        siteKey: loginPayload.session.siteKey,
        apiBase: loginPayload.session.apiBase,
        webBase: loginPayload.session.webBase,
        locale: loginPayload.session.locale,
        loginEmail: loginPayload.session.loginEmail,
        subUserEmail: loginPayload.session.subUserEmail,
        tokenId: loginPayload.session.tokenId,
        token: loginPayload.session.token
      });
      return runner(session);
    }
    throw error;
  }
}

function printError(args, error) {
  const message = error instanceof Error
    ? error.message
    : (error && typeof error === "object" && typeof error.message === "string" ? error.message : String(error));
  const errorData = error && typeof error === "object" ? error.data || null : null;
  if (args.json) {
    process.stderr.write(`${JSON.stringify({ error_code: 1, data: errorData, error_message: message }, null, 2)}\n`);
    return;
  }
  process.stderr.write(`${message}\n`);
  if (errorData?.kind === "create-episode-failed") {
    process.stderr.write(`Video ID: ${errorData.video_id || "n/a"}\n`);
    process.stderr.write(`Title: ${errorData.title || "n/a"}\n`);
    process.stderr.write(`Aspect ratio: ${errorData.aspect_ratio || "n/a"}\n`);
    process.stderr.write(`Style mode: ${errorData.style_mode || "n/a"}\n`);
    process.stderr.write(`Project: ${errorData.project_name ? `${errorData.project_name} (${errorData.project_id || "n/a"})` : (errorData.project_id || "Unclassified")}\n`);
    if (errorData.query_id) {
      process.stderr.write(`Query ID: ${errorData.query_id}\n`);
    }
    if (errorData.project_url) {
      process.stderr.write(`Project URL: ${errorData.project_url}\n`);
    }
    if (errorData.episode_url) {
      process.stderr.write(`Episode URL: ${errorData.episode_url}\n`);
    }
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.command) {
    printHelp();
    return;
  }

  const rl = isInteractive() ? readline.createInterface({ input: process.stdin, output: process.stdout }) : null;
  try {
    let result;
    if (args.command === "login") {
      result = await runLogin(args, rl);
    } else if (args.command === "projects") {
      result = await runProjects(args, rl);
    } else if (args.command === "create-episode") {
      result = await runCreateEpisode(args, rl);
    } else if (args.command === "logout") {
      result = await runLogout(args);
    } else {
      throw createApiError(`Unsupported command: ${args.command}`);
    }
    printResult(args, result);
  } finally {
    await rl?.close();
  }
}

main().catch((error) => {
  const args = parseArgs(process.argv.slice(2));
  printError(args, error);
  process.exitCode = 1;
});
