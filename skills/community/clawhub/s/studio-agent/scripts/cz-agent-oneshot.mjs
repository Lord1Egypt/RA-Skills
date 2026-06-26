#!/usr/bin/env node

import { randomUUID } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process, { env as hostEnv } from "node:process";
import {
  clearWorkspaceSelection,
  getStudioWorkspaceState,
  hasReusableDiscoveryCache,
  refreshStudioWorkspaces,
  resolveAutoDiscoveryInput,
  selectWorkspace,
} from "./clickzetta-discovery.mjs";
import { runProxyOneShot } from "./cz-agent-proxy.mjs";
import {
  isRecord,
  asTrimmedString,
  writeJsonAndExit,
} from "./utils.mjs";

const SKILL_KEY = "studio-agent";
const DEFAULT_CONFIG_PATH = "~/.openclaw/clawdbot.json";
const SETUP_CONFIG_FILE = "studio-agent.config.json";
const SETUP_COMMANDS = [
  `cp skills/studio-agent/studio-agent.config.example.json ${SETUP_CONFIG_FILE}`,
  `node skills/studio-agent/scripts/configure-skill.mjs validate --input ${SETUP_CONFIG_FILE}`,
  `node skills/studio-agent/scripts/configure-skill.mjs apply --input ${SETUP_CONFIG_FILE} --replace --restart`,
];

const ALLOWED_RUNTIME_ENV_KEYS = [
  "OPENCLAW_STATE_DIR",
  "CZ_STUDIO_JDBC_URL",
  "CZ_STUDIO_JDBC",
  "CZ_STUDIO_DOMAIN",
  "CZ_STUDIO_USERNAME",
  "CZ_STUDIO_PASSWORD",
  "CZ_STUDIO_INSTANCE_ID",
  "CZ_STUDIO_INSTANCE_NAME",
  "CZ_STUDIO_API_GATEWAY",
  "CZ_AGENT_WS_URL",
  "CZ_AGENT_TOKEN",
  "CZ_USER_ID",
  "CZ_TENANT_ID",
  "CZ_INSTANCE_ID",
  "CZ_INSTANCE_NAME",
  "CZ_PROJECT_ID",
  "CZ_PROJECT_NAME",
  "CZ_WORKSPACE",
  "CZ_WORKSPACE_ID",
  "CZ_USERNAME",
  "CZ_SESSION_ID",
  "CZ_CONVERSATION_ID",
  "CZ_CONVERSATION_TITLE",
  "CZ_AUTO_CREATE_CONVERSATION",
  "CZ_REQUEST_TIMEOUT_SECONDS",
  "CZ_STOP_GRACE_SECONDS",
  "CZ_STARTUP_CONNECT_TIMEOUT_SECONDS",
  "CZ_RECONNECT_MAX_ATTEMPTS",
  "CZ_ALWAYS_ALLOW_TOOLS",
  "CZ_INTERRUPT_DECISION_MODE",
  "CZ_EMIT_ASSISTANT_DELTAS",
];

function usage() {
  return [
    "Studio Agent one-shot runner",
    "",
    "Usage:",
    "  node skills/studio-agent/scripts/cz-agent-oneshot.mjs --input <text> [options]",
    "",
    "Options:",
    "  --input <text>                    User input to send (required)",
    "  --config <path>                  OpenClaw config path (default ~/.openclaw/clawdbot.json)",
    "  --request-id <id>                Override request id (default req-<uuid>)",
    "  --request-timeout-seconds <n>    Proxy request timeout (default 120)",
    "  --startup-timeout-seconds <n>    Proxy startup connect timeout (default 12)",
    "  --hard-timeout-seconds <n>       Total process timeout (default request+startup+8)",
    "  --raw-events                     Include parsed proxy events in output JSON",
    "  -h, --help                       Show this help",
  ].join("\n");
}


function expandHome(inputPath) {
  const raw = asTrimmedString(inputPath);
  if (!raw) {
    return raw;
  }
  if (raw.startsWith("~/")) {
    return path.join(os.homedir(), raw.slice(2));
  }
  return raw;
}

function normalizeWhitespace(value) {
  return value.replace(/\s+/g, " ").trim();
}

function splitWorkspaceCommandTarget(value) {
  const trimmed = normalizeWhitespace(value);
  if (!trimmed) {
    return undefined;
  }

  const separators = [" 然后 ", "，然后", ", then ", " and then ", "，再", " 再", "。然后"];
  let target = trimmed;
  for (const separator of separators) {
    const index = target.indexOf(separator);
    if (index > 0) {
      target = target.slice(0, index).trim();
      break;
    }
  }

  return target.replace(/[。！!？?；;,，]+$/g, "").trim() || undefined;
}

function extractWorkspaceSwitchTarget(input) {
  const text = normalizeWhitespace(input);
  const patterns = [
    /^(?:请)?(?:帮我)?切换(?:到|至|成|为)?\s*(?:workspace|工作区)?\s*[:：]?\s*(.+)$/i,
    /^(?:请)?(?:帮我)?(?:切到|改到|改成|使用)\s*(?:workspace|工作区)?\s*[:：]?\s*(.+)$/i,
    /^(?:请)?(?:帮我)?(?:workspace|工作区)\s*(?:切换到|切到|改到|改成|设为|设置为)\s*[:：]?\s*(.+)$/i,
    /^(?:please\s+)?switch(?:\s+to)?\s+workspace\s+(.+)$/i,
    /^(?:please\s+)?use\s+workspace\s+(.+)$/i,
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match?.[1]) {
      return splitWorkspaceCommandTarget(match[1]);
    }
  }
  return undefined;
}

function parseWorkspaceCommand(input) {
  const text = asTrimmedString(input);
  if (!text) {
    return null;
  }

  const normalized = normalizeWhitespace(text);
  const lower = normalized.toLowerCase();
  const mentionsWorkspace = lower.includes("workspace") || normalized.includes("工作区");
  if (!mentionsWorkspace) {
    return null;
  }

  // If the input contains action verbs that indicate a remote operation
  // (e.g. "在 workspace 里执行 SQL"), skip local workspace handling
  // and let the remote agent process it.
  const remoteActionPattern =
    /(?:执行|运行|创建|删除|查询|提交|编辑|修改|导入|导出|分析)\s/i;
  const remoteActionPatternEn =
    /\b(?:execute|run|create|delete|query|submit|edit|import|export|analyze)\s/i;
  if (remoteActionPattern.test(normalized) || remoteActionPatternEn.test(lower)) {
    return null;
  }

  if (
    /(?:刷新|更新).*(?:workspace|工作区).*(?:列表)?/i.test(normalized) ||
    /(?:workspace|工作区).*(?:列表)?.*(?:刷新|更新)/i.test(normalized) ||
    /\brefresh\s+workspaces?\b/i.test(lower) ||
    /\brefresh\s+workspace\s+list\b/i.test(lower)
  ) {
    return { type: "refresh" };
  }

  if (
    /(?:恢复默认|重置|清除).*(?:workspace|工作区)/i.test(normalized) ||
    /\breset\s+workspace\b/i.test(lower) ||
    /\bclear\s+workspace\b/i.test(lower)
  ) {
    return { type: "reset" };
  }

  const switchTarget = extractWorkspaceSwitchTarget(normalized);
  if (switchTarget) {
    return { type: "switch", target: switchTarget };
  }

  if (
    /(?:列出|查看|显示).*(?:workspace|工作区)/i.test(normalized) ||
    /有哪些.*(?:workspace|工作区)/i.test(normalized) ||
    /哪些.*(?:workspace|工作区)/i.test(normalized) ||
    /\blist\s+workspaces?\b/i.test(lower) ||
    /\bshow\s+workspaces?\b/i.test(lower)
  ) {
    return { type: "list" };
  }

  if (
    /(?:当前|现在).*(?:workspace|工作区)/i.test(normalized) ||
    /\bcurrent\s+workspace\b/i.test(lower) ||
    /\bactive\s+workspace\b/i.test(lower)
  ) {
    return { type: "current" };
  }

  return null;
}

function parsePositiveInt(value, fallback) {
  const text = asTrimmedString(value);
  if (!text) {
    return fallback;
  }
  const parsed = Number.parseInt(text, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return fallback;
  }
  return parsed;
}

function parseArgs(argv) {
  const args = [...argv];
  const opts = {
    input: undefined,
    configPath: DEFAULT_CONFIG_PATH,
    requestId: undefined,
    requestTimeoutSeconds: 120,
    startupTimeoutSeconds: 12,
    hardTimeoutSeconds: undefined,
    rawEvents: false,
    help: false,
  };

  while (args.length > 0) {
    const arg = args.shift();
    if (!arg) {
      continue;
    }
    if (arg === "-h" || arg === "--help") {
      opts.help = true;
      return opts;
    }
    if (arg === "--raw-events") {
      opts.rawEvents = true;
      continue;
    }
    if (arg === "--input") {
      opts.input = args.shift();
      continue;
    }
    if (arg === "--config") {
      opts.configPath = args.shift();
      continue;
    }
    if (arg === "--request-id") {
      opts.requestId = args.shift();
      continue;
    }
    if (arg === "--request-timeout-seconds") {
      opts.requestTimeoutSeconds = parsePositiveInt(args.shift(), opts.requestTimeoutSeconds);
      continue;
    }
    if (arg === "--startup-timeout-seconds") {
      opts.startupTimeoutSeconds = parsePositiveInt(args.shift(), opts.startupTimeoutSeconds);
      continue;
    }
    if (arg === "--hard-timeout-seconds") {
      opts.hardTimeoutSeconds = parsePositiveInt(args.shift(), opts.hardTimeoutSeconds);
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }

  return opts;
}

function loadSkillEnv(configPath) {
  const fullPath = path.resolve(expandHome(configPath));
  if (!fs.existsSync(fullPath)) {
    return { configPath: fullPath, env: {} };
  }
  const raw = fs.readFileSync(fullPath, "utf8");
  const parsed = JSON.parse(raw);
  const skillConfig = parsed?.skills?.entries?.[SKILL_KEY];
  const env = isRecord(skillConfig?.env) ? { ...skillConfig.env } : {};
  const apiKey = asTrimmedString(skillConfig?.apiKey);
  const envJdbc = asTrimmedString(env.CZ_STUDIO_JDBC_URL);
  if (apiKey && envJdbc && apiKey !== envJdbc) {
    // apiKey is the UI-facing field; sync env to match and persist
    env.CZ_STUDIO_JDBC_URL = apiKey;
    try {
      parsed.skills.entries[SKILL_KEY].env.CZ_STUDIO_JDBC_URL = apiKey;
      fs.writeFileSync(fullPath, `${JSON.stringify(parsed, null, 2)}\n`, "utf8");
    } catch {
      // best-effort sync; runtime still uses apiKey
    }
  } else if (apiKey) {
    env.CZ_STUDIO_JDBC_URL = apiKey;
  }
  return { configPath: fullPath, env };
}

function collectEnv(skillEnv, opts) {
  const env = {};
  for (const key of ALLOWED_RUNTIME_ENV_KEYS) {
    const text = asTrimmedString(hostEnv[key]);
    if (text !== undefined) {
      env[key] = text;
    }
  }
  for (const [key, value] of Object.entries(skillEnv)) {
    if (!key.startsWith("CZ_")) {
      continue;
    }
    const text = asTrimmedString(value);
    if (text !== undefined) {
      env[key] = text;
    }
  }

  env.CZ_REQUEST_TIMEOUT_SECONDS = String(opts.requestTimeoutSeconds);
  env.CZ_STARTUP_CONNECT_TIMEOUT_SECONDS = String(opts.startupTimeoutSeconds);
  if (!asTrimmedString(env.CZ_INTERRUPT_DECISION_MODE)) {
    env.CZ_INTERRUPT_DECISION_MODE = "auto_approve";
  }
  if (!asTrimmedString(env.CZ_EMIT_ASSISTANT_DELTAS)) {
    env.CZ_EMIT_ASSISTANT_DELTAS = "false";
  }

  return env;
}

async function resolveRuntimeEnv(skillEnv, opts) {
  const env = collectEnv(skillEnv, opts);
  if (asTrimmedString(env.CZ_AGENT_WS_URL)) {
    return { env };
  }

  const autoInput = resolveAutoDiscoveryInput({}, env);
  if (!autoInput) {
    return { env };
  }

  const discovered = await getStudioWorkspaceState(autoInput);
  for (const [key, value] of Object.entries(discovered.env)) {
    env[key] = value;
  }
  return {
    env,
    autoInput,
    workspaceState: discovered,
  };
}


function createProtocolError(message, extra = {}) {
  return {
    ok: false,
    error: {
      code: "PROTOCOL_ERROR",
      message,
    },
    ...extra,
  };
}

function createSetupHint(configPath) {
  return {
    setup: {
      required: true,
      config_path: configPath ?? null,
      commands: [...SETUP_COMMANDS],
    },
  };
}

function describeWorkspace(workspace) {
  if (!workspace || !isRecord(workspace)) {
    return "未选择";
  }
  const workspaceName = asTrimmedString(workspace.showName) ?? asTrimmedString(workspace.projectName) ?? "未命名";
  const workspaceId = asTrimmedString(workspace.workspaceId) ?? "n/a";
  const projectId = asTrimmedString(workspace.projectId) ?? "n/a";
  return `${workspaceName} | workspaceId=${workspaceId} | projectId=${projectId}`;
}

function formatWorkspaceListContent(state) {
  const workspaces = Array.isArray(state.workspaces) ? state.workspaces : [];
  const maxVisible = 50;
  const currentKey =
    asTrimmedString(state.selectedWorkspace?.workspaceId) ??
    asTrimmedString(state.selectedWorkspace?.projectId) ??
    describeWorkspace(state.selectedWorkspace);

  const lines = [];
  lines.push(`当前 workspace: ${describeWorkspace(state.selectedWorkspace)}`);
  if (state.selectedBy === "configured") {
    lines.push("来源: 用户配置的 workspace");
  } else if (state.selectedBy === "persisted") {
    lines.push("来源: 已持久化的用户选择");
  } else {
    lines.push("来源: 默认第一个可用 workspace");
  }
  lines.push(`共 ${workspaces.length} 个可用 workspace:`);
  for (const [index, workspace] of workspaces.slice(0, maxVisible).entries()) {
    const workspaceKey =
      asTrimmedString(workspace.workspaceId) ?? asTrimmedString(workspace.projectId) ?? describeWorkspace(workspace);
    const marker = workspaceKey === currentKey ? " [current]" : "";
    lines.push(`${index + 1}. ${describeWorkspace(workspace)}${marker}`);
  }
  if (workspaces.length > maxVisible) {
    lines.push(`仅展示前 ${maxVisible} 个；如果要切换，直接说“切换到 workspace <名称或ID>”即可。`);
  }
  return lines.join("\n");
}

function buildWorkspaceCommandResult(content, requestId) {
  return {
    ok: true,
    content,
    conversation_id: null,
    request_id: requestId,
    event: {
      event: "assistant_final",
      op_type: "local_workspace",
      complete: true,
    },
  };
}

async function maybeHandleWorkspaceCommand(command, autoInput, state, requestId) {
  if (!command || !autoInput) {
    return null;
  }

  if (command.type === "current") {
    return buildWorkspaceCommandResult(formatWorkspaceListContent(state).split("\n").slice(0, 2).join("\n"), requestId);
  }

  if (command.type === "list") {
    const refreshedState = await getStudioWorkspaceState(autoInput, { requireWorkspaces: true });
    return buildWorkspaceCommandResult(formatWorkspaceListContent(refreshedState), requestId);
  }

  if (command.type === "refresh") {
    const refreshedState = await refreshStudioWorkspaces(autoInput);
    return buildWorkspaceCommandResult(`已刷新 workspace 列表。\n${formatWorkspaceListContent(refreshedState)}`, requestId);
  }

  if (command.type === "reset") {
    clearWorkspaceSelection(autoInput);
    const refreshedState = await getStudioWorkspaceState(autoInput, { requireWorkspaces: true, useCache: true });
    return buildWorkspaceCommandResult(
      `已恢复默认 workspace。\n当前 workspace: ${describeWorkspace(refreshedState.selectedWorkspace)}`,
      requestId,
    );
  }

  if (command.type === "switch") {
    if (state.selectedBy === "configured") {
      return buildWorkspaceCommandResult(
        `当前已通过配置固定 workspace: ${describeWorkspace(state.selectedWorkspace)}\n如需修改，请更新 studio-agent 配置中的 workspace/workspaceId/projectId 后重新 apply。`,
        requestId,
      );
    }
    const selection = await selectWorkspace(autoInput, command.target);
    if (selection.ok) {
      return buildWorkspaceCommandResult(
        `已切换到 workspace: ${describeWorkspace(selection.workspace)}`,
        requestId,
      );
    }

    const matches = Array.isArray(selection.matches) ? selection.matches : [];
    if (matches.length === 0) {
      const stateWithWorkspaces = selection.state ?? state;
      return buildWorkspaceCommandResult(
        `没有找到匹配的 workspace: ${command.target}\n${formatWorkspaceListContent(stateWithWorkspaces)}`,
        requestId,
      );
    }

    const lines = [`workspace "${command.target}" 匹配到多个候选，请指定更精确的名称或 id:`];
    for (const workspace of matches) {
      lines.push(`- ${describeWorkspace(workspace)}`);
    }
    return buildWorkspaceCommandResult(lines.join("\n"), requestId);
  }

  return null;
}

async function run() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    process.stdout.write(`${usage()}\n`);
    return;
  }

  const input = asTrimmedString(opts.input);
  if (!input) {
    writeJsonAndExit(createProtocolError("missing --input"), 1);
    return;
  }

  const requestId = asTrimmedString(opts.requestId) ?? `req-${randomUUID()}`;
  const workspaceCommand = parseWorkspaceCommand(input);

  let loaded;
  try {
    loaded = loadSkillEnv(opts.configPath);
  } catch (error) {
    writeJsonAndExit(
      createProtocolError("studio-agent skill env is missing in OpenClaw config", {
        detail: error instanceof Error ? error.message : String(error),
        ...createSetupHint(expandHome(opts.configPath)),
      }),
      1,
    );
    return;
  }

  const hintEnv = collectEnv(loaded.env, opts);
  const autoInput = resolveAutoDiscoveryInput({}, hintEnv);
  const showSlowConnectHint =
    !asTrimmedString(hintEnv.CZ_AGENT_WS_URL) &&
    Boolean(autoInput) &&
    !hasReusableDiscoveryCache(autoInput);
  const slowConnectTimer = showSlowConnectHint
    ? setTimeout(() => {
        process.stderr.write(
          "[studio-agent] 首次连接或 token 刷新中，正在登录 ClickZetta 并初始化 Studio，通常会比后续请求慢几秒。\n",
        );
      }, 1000)
    : null;

  let resolvedRuntime;
  try {
    resolvedRuntime = await resolveRuntimeEnv(loaded.env, opts);
  } catch (error) {
    if (slowConnectTimer) {
      clearTimeout(slowConnectTimer);
    }
    writeJsonAndExit(
      {
        ok: false,
        error: {
          code: "DISCOVERY_ERROR",
          message: `runtime discovery failed: ${error instanceof Error ? error.message : String(error)}`,
        },
        ...createSetupHint(expandHome(opts.configPath)),
      },
      1,
    );
    return;
  } finally {
    if (slowConnectTimer) {
      clearTimeout(slowConnectTimer);
    }
  }

  const env = resolvedRuntime.env;
  if (!asTrimmedString(env.CZ_AGENT_WS_URL) && !resolvedRuntime.autoInput) {
    writeJsonAndExit(
      createProtocolError("studio-agent is not configured", {
        detail: "Set CZ_STUDIO_JDBC_URL in the Skills page, or configure studio-agent via configure-skill.mjs.",
        ...createSetupHint(expandHome(opts.configPath)),
      }),
      1,
    );
    return;
  }
  const workspaceResult = await maybeHandleWorkspaceCommand(
    workspaceCommand,
    resolvedRuntime.autoInput,
    resolvedRuntime.workspaceState,
    requestId,
  );
  if (workspaceResult) {
    writeJsonAndExit(workspaceResult, 0);
    return;
  }

  const hardTimeoutSeconds =
    opts.hardTimeoutSeconds ?? opts.requestTimeoutSeconds + opts.startupTimeoutSeconds + 8;
  const hardTimeoutMs = hardTimeoutSeconds * 1000;
  const base = {
    request_id: requestId,
    config_path: loaded.configPath,
    diagnostics: {
      exit_code: 0,
      signal: null,
      stderr_tail: "",
    },
  };

  let result;
  try {
    result = await runProxyOneShot({
      env,
      requestId,
      conversationId: asTrimmedString(env.CZ_CONVERSATION_ID),
      userInput: input,
      hardTimeoutMs,
    });
  } catch (error) {
    writeJsonAndExit(
      {
        ok: false,
        error: {
          code: "TIMEOUT",
          message: error instanceof Error ? error.message : String(error),
        },
        ...base,
      },
      1,
    );
    return;
  }

  const events = Array.isArray(result?.events) ? result.events : [];
  const finalEvent = result?.finalEvent;
  const errorEvent = result?.errorEvent;

  if (finalEvent) {
    writeJsonAndExit(
      {
        ok: true,
        content: finalEvent.content ?? "",
        conversation_id: finalEvent.conversation_id ?? null,
        event: {
          event: finalEvent.event,
          op_type: finalEvent.op_type,
          complete: finalEvent.complete,
        },
        ...(opts.rawEvents ? { events } : {}),
        ...base,
      },
      0,
    );
    return;
  }

  if (errorEvent) {
    writeJsonAndExit(
      {
        ok: false,
        error: errorEvent.error ?? {
          code: "REMOTE_ERROR",
          message: "proxy returned error event without details",
        },
        conversation_id: errorEvent.conversation_id ?? null,
        ...(opts.rawEvents ? { events } : {}),
        ...base,
      },
      1,
    );
    return;
  }

  writeJsonAndExit(
    {
      ok: false,
      error: {
        code: "REMOTE_ERROR",
        message: "proxy returned neither assistant_final nor error",
      },
      ...(opts.rawEvents ? { events } : {}),
      ...base,
    },
    1,
  );
}

run().catch((error) => {
  writeJsonAndExit(
    createProtocolError(`unexpected runner error: ${error instanceof Error ? error.message : String(error)}`),
    1,
  );
});
