#!/usr/bin/env node

import { createHash, randomBytes, randomUUID } from "node:crypto";
import { readFile, rename, mkdir, unlink, writeFile, chmod, realpath } from "node:fs/promises";
import { createServer } from "node:net";
import { basename, join, resolve } from "node:path";
import { homedir } from "node:os";

const SKILL_VERSION = "2.3.1";
const SKILL_VARIANT = "production";
const CLIENT_NAME = "Suno.cn Music Skill";
const DEFAULT_BASE_URL = "https://mcp.suno.cn";
const BASE_URL = (process.env.SUNO_CN_MCP_URL || DEFAULT_BASE_URL).replace(/\/+$/, "");
const CONFIG_DIR = resolve(process.env.SUNO_CN_CONFIG_DIR || join(homedir(), ".suno-cn"));
const CREDENTIALS_PATH = join(CONFIG_DIR, "credentials.json");
const PENDING_OPERATION_PATH = join(CONFIG_DIR, "pending-operation.json");
const SKILL_KEY_PATTERN = /^sks_[0-9a-f]{64}$/;
const ALLOWED_METHODS = new Set(["GET", "POST"]);
const SENSITIVE_FIELD_PATTERN = /token|authorization|skill_key|api_key|credential/i;

class ClientError extends Error {
  constructor(error, message, options = {}) {
    super(message);
    this.name = "ClientError";
    this.error = error;
    this.status = options.status;
    this.action = options.action;
    this.details = options.details;
  }
}

function redactString(value) {
  return value
    .replace(/sks_[0-9a-f]{64}/gi, "sks_********")
    .replace(/\bsk-[A-Za-z0-9_-]{8,}\b/g, "sk-********")
    .replace(/(Bearer\s+)[A-Za-z0-9._-]+/gi, "$1********");
}

function redact(value, key = "") {
  if (/token|authorization|skill_key|api_key|credential/i.test(key)) {
    return "********";
  }
  if (typeof value === "string") {
    return redactString(value);
  }
  if (Array.isArray(value)) {
    return value.map((item) => redact(item));
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([childKey, childValue]) => [childKey, redact(childValue, childKey)]));
  }
  return value;
}

function printJSON(value) {
  process.stdout.write(`${JSON.stringify(redact(value), null, 2)}\n`);
}

async function loadCredentials() {
  try {
    const parsed = JSON.parse(await readFile(CREDENTIALS_PATH, "utf8"));
    if (!SKILL_KEY_PATTERN.test(parsed.skill_key || "") || typeof parsed.client_instance_id !== "string") {
      throw new ClientError("invalid_local_credentials", "本地授权凭证损坏，请执行 auth logout 后重新授权");
    }
    return parsed;
  } catch (error) {
    if (error?.code === "ENOENT") {
      return null;
    }
    if (error instanceof ClientError) {
      throw error;
    }
    throw new ClientError("invalid_local_credentials", "无法读取本地授权凭证，请执行 auth logout 后重新授权");
  }
}

async function loadSkillKeyForLogout() {
  try {
    const parsed = JSON.parse(await readFile(CREDENTIALS_PATH, "utf8"));
    return SKILL_KEY_PATTERN.test(parsed?.skill_key || "") ? parsed.skill_key : "";
  } catch (error) {
    if (error?.code === "ENOENT" || error instanceof SyntaxError) return "";
    throw new ClientError("invalid_local_credentials", "无法读取本地授权凭证，未执行退出授权");
  }
}

async function savePrivateJSON(pathname, value) {
  await mkdir(CONFIG_DIR, { recursive: true, mode: 0o700 });
  const temporaryPath = `${pathname}.${process.pid}.tmp`;
  await writeFile(temporaryPath, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  await chmod(temporaryPath, 0o600).catch(() => undefined);
  await rename(temporaryPath, pathname);
  await chmod(pathname, 0o600).catch(() => undefined);
}

function createSkillCredentials() {
  return {
    version: 1,
    skill_key: `sks_${randomBytes(32).toString("hex")}`,
    client_instance_id: randomUUID(),
    created_at: new Date().toISOString(),
  };
}

// 内核释放进程锁，避免强制退出留下永久文件锁；端口碰撞仅会让不同目录串行。
async function withCredentialLock(operation) {
  await mkdir(CONFIG_DIR, { recursive: true, mode: 0o700 });
  const directory = await realpath(CONFIG_DIR);
  const identity = process.platform === "win32" ? directory.toLowerCase() : directory;
  const port = 12000 + createHash("sha256").update(identity).digest().readUInt16BE(0) % 16000;
  const deadline = Date.now() + 35_000;
  let lock;
  while (!lock) {
    const candidate = createServer(socket => socket.destroy());
    try {
      await new Promise((resolveListen, rejectListen) => {
        candidate.once("error", rejectListen);
        candidate.listen({ host: "127.0.0.1", port, exclusive: true }, resolveListen);
      });
      lock = candidate;
    } catch (error) {
      candidate.close();
      if (error?.code !== "EADDRINUSE" || Date.now() >= deadline) {
        throw new ClientError("credentials_busy", "授权状态正在更新，请稍后重试");
      }
      await new Promise(resolvePromise => setTimeout(resolvePromise, 100));
    }
  }
  try {
    return await operation();
  } finally {
    await new Promise(resolveClose => lock.close(resolveClose));
  }
}

function legacyCredential() {
  const value = (process.env.SUNO_CN_API_KEY || "").trim();
  return value ? { kind: "legacy", value } : null;
}

async function fetchResponse(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeout || 30_000);
  try {
    const response = await fetch(`${BASE_URL}${path}`, { ...options, signal: controller.signal });
    const raw = await response.text();
    let payload = null;
    if (raw) {
      try {
        payload = JSON.parse(raw);
      } catch {
        payload = { message: raw };
      }
    }
    return { response, payload };
  } catch (error) {
    if (error?.name === "AbortError") {
      throw new ClientError("request_timeout", "请求超时，请稍后重试");
    }
    throw new ClientError("network_error", "网络连接失败，请检查网络或代理设置");
  } finally {
    clearTimeout(timeout);
  }
}

async function fetchJSON(path, options = {}) {
  const { response, payload } = await fetchResponse(path, options);
  if (!response.ok) {
    const errorType = payload?.error_type || payload?.error || `http_${response.status}`;
    throw new ClientError(errorType, payload?.message || payload?.error || `请求失败（HTTP ${response.status}）`, {
      status: response.status,
      action: payload?.action,
      details: payload,
    });
  }
  return payload;
}

async function querySkillStatus(credentials) {
  return fetchJSON("/mcp/auth/status", {
    method: "GET",
    headers: { Authorization: `Bearer ${credentials.skill_key}` },
  });
}

function publicAuthorizationResult(result) {
  const output = { status: result.status };
  if (result.status === "authorized") {
    output.authorized_at = result.authorized_at;
    output.expires_at = result.expires_at;
  }
  if (result.expires_in) {
    output.expires_in = result.expires_in;
  }
  if (result.authorization_url) {
    output.message = "请在网页完成登录和授权";
    output.action = { type: "open_url", url: result.authorization_url };
  }
  return output;
}

async function clearSkillCredentials() {
  try {
    await unlink(CREDENTIALS_PATH);
  } catch (error) {
    if (error?.code !== "ENOENT") {
      throw new ClientError("credential_reset_failed", "无法更新本地授权，请执行 auth logout 后重试");
    }
  }
}

async function clearPendingOperation() {
  try {
    await unlink(PENDING_OPERATION_PATH);
  } catch (error) {
    if (error?.code !== "ENOENT") {
      throw new ClientError("pending_operation_reset_failed", "无法清除待恢复操作，请检查本地配置目录权限");
    }
  }
}

function containsSensitiveField(value) {
  if (!value || typeof value !== "object") return false;
  if (Array.isArray(value)) return value.some((item) => containsSensitiveField(item));
  return Object.entries(value).some(([key, childValue]) =>
    SENSITIVE_FIELD_PATTERN.test(key) || containsSensitiveField(childValue),
  );
}

function buildPendingDescriptor(method, pathname, body, operation) {
  if (operation) return operation;
  if (containsSensitiveField(body)) {
    return { kind: "unavailable", method, pathname, reason: "sensitive_request" };
  }
  return { kind: "request", method, pathname, body: body ?? null };
}

function pendingOperationSummary(record) {
  const state = record.state === "executing" ? "unknown" : record.state;
  return {
    id: record.id,
    state,
    method: record.operation.method,
    path: record.operation.pathname,
    created_at: record.created_at,
    replayable: record.operation.kind !== "unavailable",
  };
}

async function loadPendingOperation() {
  try {
    const parsed = JSON.parse(await readFile(PENDING_OPERATION_PATH, "utf8"));
    const valid = parsed?.version === 1
      && typeof parsed.id === "string"
      && typeof parsed.state === "string"
      && typeof parsed.created_at === "string"
      && parsed.operation
      && typeof parsed.operation.kind === "string"
      && ALLOWED_METHODS.has(parsed.operation.method)
      && typeof parsed.operation.pathname === "string";
    if (!valid) {
      throw new ClientError("invalid_pending_operation", "本地待恢复操作损坏，请执行 purchase clear 后重新发起任务");
    }
    validateAPIPath(parsed.operation.pathname);
    return parsed;
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    if (error instanceof ClientError) throw error;
    throw new ClientError("invalid_pending_operation", "无法读取本地待恢复操作，请执行 purchase clear 后重新发起任务");
  }
}

async function savePendingOperation(method, pathname, body, operation, purchaseAction) {
  const record = {
    version: 1,
    id: randomUUID(),
    state: "awaiting_purchase",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    operation: buildPendingDescriptor(method, pathname, body, operation),
    purchase_action: purchaseAction,
  };
  await savePrivateJSON(PENDING_OPERATION_PATH, record);
  return pendingOperationSummary(record);
}

async function updatePendingOperation(record, state) {
  const updated = { ...record, state, updated_at: new Date().toISOString() };
  await savePrivateJSON(PENDING_OPERATION_PATH, updated);
  return updated;
}

function isPaymentRequired(error) {
  return error instanceof ClientError
    && error.status === 402
    && (error.error === "insufficient_credits" || error.details?.error_type === "insufficient_credits");
}

async function startAuthorization(options = {}) {
  return withCredentialLock(async () => {
    const current = await loadCredentials();
    if (options.expectedKey && current?.skill_key !== options.expectedKey) {
      throw new ClientError("credentials_changed", "授权已由另一进程更新，请确认后重试当前操作");
    }
    const credentials = options.rotate || !current ? createSkillCredentials() : current;
    const result = await fetchJSON("/mcp/auth/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skill_key: credentials.skill_key,
        client_instance_id: credentials.client_instance_id,
        client_name: CLIENT_NAME,
        skill_version: SKILL_VERSION,
      }),
    });
    await savePrivateJSON(CREDENTIALS_PATH, credentials);
    return publicAuthorizationResult(result);
  });
}

async function resolveBusinessCredential() {
  const credentials = await loadCredentials();
	if (credentials) {
		const status = await querySkillStatus(credentials);
		if (status.status !== "authorized") {
			const pending = await startAuthorization({ rotate: status.status === "denied" || status.status === "expired", expectedKey: credentials.skill_key });
      throw new ClientError("authorization_required", "请先在网页完成账号授权", { action: pending.action, details: pending });
    }
    return { kind: "skill", value: credentials.skill_key };
  }
  const legacy = legacyCredential();
  if (legacy) {
    return legacy;
  }
  const pending = await startAuthorization();
  throw new ClientError("authorization_required", "请先在网页完成账号授权", { action: pending.action, details: pending });
}

function validateAPIPath(pathname) {
  if (!pathname.startsWith("/mcp/api/")) {
    throw new ClientError("invalid_path", "只允许调用 /mcp/api/ 下的业务接口");
  }
  return pathname;
}

async function authorizedRequest(method, pathname, body, options = {}) {
  method = method.toUpperCase();
  if (!ALLOWED_METHODS.has(method)) {
    throw new ClientError("invalid_method", "只允许 GET 或 POST 请求");
  }
  validateAPIPath(pathname);
  const credential = await resolveBusinessCredential();
  const headers = { Authorization: `Bearer ${credential.value}` };
  if (body != null && !options.multipart) {
    headers["Content-Type"] = "application/json";
  }
  try {
    return await fetchJSON(pathname, {
      method,
      headers,
      body: body == null || options.multipart ? body : JSON.stringify(body),
      timeout: options.timeout || 120_000,
    });
  } catch (error) {
    if (error instanceof ClientError && credential.kind === "skill"
      && error.details?.reauthorize !== false
      && ["authorization_required", "login_expired", "permission_context_invalid"].includes(error.error)) {
      const pending = await startAuthorization({ rotate: true, expectedKey: credential.value });
      const message = error.error === "permission_context_invalid"
        ? "团队权限上下文无效，请重新完成网页授权"
        : "Skill 授权已失效，请重新完成网页授权";
      throw new ClientError("authorization_required", message, { action: pending.action });
    }
    if (error instanceof ClientError && error.status === 401 && credential.kind === "legacy") {
      throw new ClientError("legacy_api_key_invalid", "旧版 API Key 无效，请移除环境变量后使用网页授权");
    }
    if (isPaymentRequired(error) && options.persistPaymentOperation !== false) {
      const pending = await savePendingOperation(method, pathname, body, options.operation, error.action);
      error.details = { ...error.details, pending_operation: pending };
    }
    throw error;
  }
}

async function authStatus() {
  const credentials = await loadCredentials();
  if (credentials) {
    return querySkillStatus(credentials);
  }
  if (legacyCredential()) {
    return { status: "authorized", mode: "legacy_api_key" };
  }
  return { status: "authorization_required", message: "尚未授权，请执行 auth start" };
}

async function authComplete(timeoutSeconds = 180) {
  const credentials = await loadCredentials();
  if (!credentials) {
    throw new ClientError("authorization_not_started", "尚未发起授权，请先执行 auth start");
  }
  const safeTimeout = Number.isFinite(timeoutSeconds) ? Math.min(Math.max(timeoutSeconds, 1), 600) : 180;
  const deadline = Date.now() + safeTimeout * 1000;
  while (Date.now() < deadline) {
    const status = await querySkillStatus(credentials);
    if (status.status === "authorized" || status.status === "denied" || status.status === "expired") {
      return status;
    }
    await new Promise((resolvePromise) => setTimeout(resolvePromise, 2000));
  }
  throw new ClientError("authorization_timeout", "等待授权超时，请确认网页操作后重试 auth complete");
}

async function authLogout() {
  return withCredentialLock(async () => {
    const skillKey = await loadSkillKeyForLogout();
    if (skillKey) {
      await fetchJSON("/mcp/auth/binding", {
        method: "DELETE",
        headers: { Authorization: `Bearer ${skillKey}` },
      });
    }
    await clearSkillCredentials();
    await clearPendingOperation();
    return { status: "logged_out", message: "Skill 授权已撤销，本地凭证已清除" };
  });
}

function parseJSONObject(raw) {
  if (!raw) {
    return {};
  }
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
      throw new Error("not object");
    }
    return parsed;
  } catch {
    throw new ClientError("invalid_json", "请求体必须是 JSON 对象");
  }
}

async function uploadFile(pathname, filePath, fields = {}, requestOptions = {}) {
  const absolutePath = resolve(filePath);
  let data;
  try {
    data = await readFile(absolutePath);
  } catch {
    throw new ClientError("file_not_found", "无法读取上传文件");
  }
  const form = new FormData();
  form.append("file", new Blob([data]), basename(absolutePath));
  for (const [field, value] of Object.entries(fields)) {
    if (value !== undefined && value !== "") {
      form.append(field, String(value));
    }
  }
  return authorizedRequest("POST", pathname, form, {
    multipart: true,
    timeout: 180_000,
    persistPaymentOperation: requestOptions.persistPaymentOperation,
    operation: { kind: "upload", method: "POST", pathname, file_path: absolutePath, fields },
  });
}

async function purchaseStatus() {
  const pending = await loadPendingOperation();
  const account = await authorizedRequest("GET", "/mcp/api/user", null, { persistPaymentOperation: false });
  if (!pending) {
    return { status: "no_pending_operation", account, message: "没有待恢复的收费操作" };
  }
  return {
    status: pending.state === "executing" || pending.state === "unknown"
      ? "result_unknown"
      : "confirmation_required",
    account,
    pending: pendingOperationSummary(pending),
    message: pending.state === "executing" || pending.state === "unknown"
      ? "上次执行结果不确定，请先查询任务列表，确认未提交后再重新发起"
      : `余额已刷新，请先征得用户确认，再执行 purchase retry ${pending.id}`,
  };
}

async function replayPendingOperation(record) {
  const operation = record.operation;
  if (operation.kind === "request") {
    return authorizedRequest(operation.method, operation.pathname, operation.body, { persistPaymentOperation: false });
  }
  if (operation.kind === "upload") {
    return uploadFile(operation.pathname, operation.file_path, operation.fields, { persistPaymentOperation: false });
  }
  throw new ClientError("manual_retry_required", "该请求包含敏感字段，未保存请求体；购买后请由用户确认并重新发起原任务");
}

async function retryPendingOperation(operationID) {
  const pending = await loadPendingOperation();
  if (!pending || pending.id !== operationID) {
    throw new ClientError("pending_operation_not_found", "未找到对应的待恢复操作");
  }
  if (pending.state === "executing" || pending.state === "unknown") {
    throw new ClientError("operation_state_unknown", "上次执行结果不确定，请先查询任务列表，禁止直接重试");
  }
  if (pending.state !== "awaiting_purchase") {
    throw new ClientError("pending_operation_not_retryable", "当前待恢复操作不可重试，请重新发起任务");
  }
  if (pending.operation.kind === "unavailable") {
    throw new ClientError("manual_retry_required", "该请求包含敏感字段，购买后请由用户确认并重新发起原任务");
  }

  const executing = await updatePendingOperation(pending, "executing");
  try {
    const result = await replayPendingOperation(executing);
    await clearPendingOperation();
    return { status: "completed", operation_id: operationID, result };
  } catch (error) {
    let state = "failed";
    if (isPaymentRequired(error)) state = "awaiting_purchase";
    if (error instanceof ClientError && ["network_error", "request_timeout"].includes(error.error)) state = "unknown";
    const updated = await updatePendingOperation(executing, state);
    if (state === "unknown") {
      throw new ClientError("operation_state_unknown", "请求结果不确定，请先查询任务列表，禁止直接重试", {
        details: { pending_operation: pendingOperationSummary(updated) },
      });
    }
    if (error instanceof ClientError) {
      error.details = { ...error.details, pending_operation: pendingOperationSummary(updated) };
    }
    throw error;
  }
}

function usage() {
  return {
    commands: [
      "auth status|start|complete [timeout_seconds]|logout",
      "account",
      "purchase status|retry <operation_id>|clear",
      "request GET|POST /mcp/api/... [json_object]",
      "upload-reference <file> <operation> [title] [mode]",
      "upload-tool <file>",
      "version",
    ],
  };
}

async function main(args) {
  const [command, ...rest] = args;
  if (!command || command === "help" || command === "--help") {
    return usage();
  }
  if (command === "version") {
    const variantQuery = SKILL_VARIANT === "test" ? "?variant=test" : "";
    return fetchJSON(`/mcp/skill/version${variantQuery}`, { method: "GET" });
  }
	if (command === "auth") {
		const [action, value] = rest;
		if (action === "status") return authStatus();
		if (action === "start") {
			const current = await loadCredentials();
			if (!current) return startAuthorization();
			const status = await querySkillStatus(current);
			if (status.status === "authorized") return status;
			return startAuthorization({ rotate: status.status === "denied" || status.status === "expired", expectedKey: current.skill_key });
		}
    if (action === "complete") return authComplete(Number.parseInt(value || "180", 10));
    if (action === "logout") return authLogout();
    throw new ClientError("invalid_command", "auth 仅支持 status、start、complete、logout");
  }
  if (command === "account") {
    return authorizedRequest("GET", "/mcp/api/user");
  }
  if (command === "purchase") {
    const [action, operationID = ""] = rest;
    if (action === "status") return purchaseStatus();
    if (action === "retry") return retryPendingOperation(operationID);
    if (action === "clear") {
      await clearPendingOperation();
      return { status: "cleared", message: "待恢复操作已清除" };
    }
    throw new ClientError("invalid_command", "purchase 仅支持 status、retry、clear");
  }
  if (command === "request") {
    const [method = "", pathname = "", rawBody = ""] = rest;
    return authorizedRequest(method, pathname, method.toUpperCase() === "POST" ? parseJSONObject(rawBody) : null);
  }
  if (command === "upload-reference") {
    const [filePath, operation, title = "", mode = ""] = rest;
    if (!filePath || !["extend", "add_vocals", "add_instrumental", "cover", "add_stem"].includes(operation)) {
      throw new ClientError("invalid_upload", "请提供 MP3 文件和有效 operation");
    }
    return uploadFile("/mcp/api/upload", filePath, { operation, title, mode });
  }
  if (command === "upload-tool") {
    const [filePath] = rest;
    if (!filePath) throw new ClientError("invalid_upload", "请提供要上传的文件");
    return uploadFile("/mcp/api/tool/upload", filePath);
  }
  throw new ClientError("invalid_command", "未知命令，请执行 --help 查看用法");
}

try {
  printJSON(await main(process.argv.slice(2)));
} catch (error) {
  if (error instanceof ClientError) {
    printJSON({
      status: "error",
      error: error.error,
      message: error.message,
      action: error.action,
      details: error.details,
    });
  } else {
    printJSON({ status: "error", error: "unexpected_error", message: "执行失败，请稍后重试" });
  }
  process.exitCode = 1;
}
