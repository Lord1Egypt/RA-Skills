import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { a as isAgentBootstrapEvent } from "/home/irtual/.npm-global/lib/node_modules/openclaw/dist/internal-hooks-4i4Rq3Qq.js";
import { r as resolveHookConfig } from "/home/irtual/.npm-global/lib/node_modules/openclaw/dist/config-DiksYOxU.js";
import { t as createSubsystemLogger } from "/home/irtual/.npm-global/lib/node_modules/openclaw/dist/subsystem-Cgmckbux.js";

const execFileAsync = promisify(execFile);
const HOOK_KEY = "super-memori-session-start";
const log = createSubsystemLogger("hooks/super-memori-session-start");
const DEFAULT_COMMAND = "cd /home/irtual/.openclaw/workspace/skills/super_memori && ./startup-self-check.sh --json --repair --report-file /home/irtual/.openclaw/workspace/memory/index-state/startup-self-check-last.json";
const DEFAULT_LEDGER = "/home/irtual/.openclaw/workspace/memory/index-state/session-start-hook-ledger.json";
const DEFAULT_REPORT = "/home/irtual/.openclaw/workspace/memory/index-state/startup-self-check-last.json";
const DEFAULT_MAX_LEDGER_ENTRIES = 400;

async function fileExists(target) {
  try {
    await fs.access(target);
    return true;
  } catch {
    return false;
  }
}

async function readJsonSafe(file, fallback) {
  try {
    return JSON.parse(await fs.readFile(file, "utf8"));
  } catch {
    return fallback;
  }
}

async function writeJson(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function normalizePositiveInt(value, fallback) {
  return typeof value === "number" && Number.isFinite(value) && value > 0 ? Math.trunc(value) : fallback;
}

function summarizeReport(report) {
  if (!report || typeof report !== "object") return "startup self-check report unavailable";
  const status = typeof report.status === "string" ? report.status : "UNKNOWN";
  const repaired = report.repaired === true ? "yes" : "no";
  const smoke = report.smoke_query_ok === true ? "ok" : report.smoke_query_ok === false ? "failed" : "unknown";
  const warnings = Array.isArray(report.warnings) ? report.warnings : [];
  const warningText = warnings.length > 0 ? warnings.join("; ") : "none";
  return `status=${status}; repaired=${repaired}; smoke_query=${smoke}; warnings=${warningText}`;
}

async function runCommand(command, cwd) {
  return await execFileAsync("bash", ["-lc", command], {
    cwd,
    timeout: 15 * 60 * 1000,
    maxBuffer: 4 * 1024 * 1024
  });
}

async function ensureLedgerEntry(params) {
  const ledger = await readJsonSafe(params.ledgerFile, { version: 1, sessions: {} });
  if (!ledger || typeof ledger !== "object") return { shouldRun: true, ledger: { version: 1, sessions: {} } };
  if (!ledger.sessions || typeof ledger.sessions !== "object") ledger.sessions = {};
  const existing = ledger.sessions[params.sessionId];
  if (existing && typeof existing === "object") return { shouldRun: false, ledger, existing };
  return { shouldRun: true, ledger };
}

function trimLedgerSessions(sessions, maxEntries) {
  const entries = Object.entries(sessions).sort((a, b) => {
    const aTs = typeof a[1]?.handledAt === "string" ? Date.parse(a[1].handledAt) : 0;
    const bTs = typeof b[1]?.handledAt === "string" ? Date.parse(b[1].handledAt) : 0;
    return bTs - aTs;
  });
  return Object.fromEntries(entries.slice(0, maxEntries));
}

const superMemoriSessionStartHook = async (event) => {
  if (!isAgentBootstrapEvent(event)) return;
  const context = event.context || {};
  const cfg = context.cfg;
  const hookConfig = resolveHookConfig(cfg, HOOK_KEY);
  if (!hookConfig || hookConfig.enabled === false) return;

  const workspaceDir = typeof context.workspaceDir === "string" && context.workspaceDir.trim() ? context.workspaceDir : "/home/irtual/.openclaw/workspace";
  const sessionId = typeof context.sessionId === "string" && context.sessionId.trim() ? context.sessionId.trim() : "";
  const sessionKey = typeof context.sessionKey === "string" && context.sessionKey.trim() ? context.sessionKey.trim() : event.sessionKey;
  if (!sessionId) {
    log.warn("skipping: missing sessionId on agent:bootstrap event", { sessionKey });
    return;
  }

  const command = typeof hookConfig.command === "string" && hookConfig.command.trim() ? hookConfig.command.trim() : DEFAULT_COMMAND;
  const ledgerFile = typeof hookConfig.ledgerFile === "string" && hookConfig.ledgerFile.trim() ? hookConfig.ledgerFile.trim() : DEFAULT_LEDGER;
  const reportFile = typeof hookConfig.reportFile === "string" && hookConfig.reportFile.trim() ? hookConfig.reportFile.trim() : DEFAULT_REPORT;
  const injectBootstrapReport = hookConfig.injectBootstrapReport !== false;
  const maxLedgerEntries = normalizePositiveInt(hookConfig.maxLedgerEntries, DEFAULT_MAX_LEDGER_ENTRIES);

  const ledgerState = await ensureLedgerEntry({ ledgerFile, sessionId });
  if (!ledgerState.shouldRun) {
    if (injectBootstrapReport && await fileExists(reportFile) && Array.isArray(context.bootstrapFiles)) {
      const report = await readJsonSafe(reportFile, null);
      context.bootstrapFiles = [
        ...context.bootstrapFiles,
        {
          name: "TOOLS.md",
          path: reportFile,
          content: `# Super Memori Session-Start Report\n\nThis session was already handled by the enforceable session-start hook for sessionId ${sessionId}.\n\nLatest known report summary: ${summarizeReport(report)}\n`,
          missing: false
        }
      ];
    }
    return;
  }

  let runStatus = "ok";
  let exitCode = 0;
  let stdout = "";
  let stderr = "";
  try {
    const result = await runCommand(command, workspaceDir);
    stdout = result.stdout ?? "";
    stderr = result.stderr ?? "";
  } catch (error) {
    runStatus = "failed";
    exitCode = typeof error?.code === "number" ? error.code : 1;
    stdout = typeof error?.stdout === "string" ? error.stdout : "";
    stderr = typeof error?.stderr === "string" ? error.stderr : String(error);
    log.warn("session-start self-check command failed", { sessionId, sessionKey, exitCode });
  }

  const report = await readJsonSafe(reportFile, null);
  ledgerState.ledger.sessions[sessionId] = {
    sessionKey,
    handledAt: new Date().toISOString(),
    status: runStatus,
    exitCode,
    reportFile,
    reportStatus: report && typeof report.status === "string" ? report.status : null
  };
  ledgerState.ledger.sessions = trimLedgerSessions(ledgerState.ledger.sessions, maxLedgerEntries);
  await writeJson(ledgerFile, ledgerState.ledger);

  if (injectBootstrapReport && Array.isArray(context.bootstrapFiles)) {
    const summary = summarizeReport(report);
    const trailer = [
      "# Super Memori Session-Start Report",
      "",
      `This session was enforceably checked at bootstrap for sessionId ${sessionId}.`,
      `Hook status: ${runStatus}`,
      `Command exit code: ${exitCode}`,
      `Report summary: ${summary}`,
      stderr.trim() ? "" : "",
      stderr.trim() ? `stderr: ${stderr.trim().slice(0, 1200)}` : ""
    ].filter(Boolean).join("\n");
    context.bootstrapFiles = [
      ...context.bootstrapFiles,
      {
        name: "TOOLS.md",
        path: reportFile,
        content: trailer,
        missing: false
      }
    ];
  }
};

export default superMemoriSessionStartHook;
