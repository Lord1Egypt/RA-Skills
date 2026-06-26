import { spawn } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import type { WTTCommandExecutionContext } from "./types.js";

type CommandRunResult = {
  code: number;
  stdout: string;
  stderr: string;
  timedOut: boolean;
};

async function runCommand(cmd: string, args: string[], timeoutMs: number): Promise<CommandRunResult> {
  return new Promise((resolve) => {
    const child = spawn(cmd, args, {
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";
    let finished = false;

    child.stdout.on("data", (chunk) => {
      stdout += String(chunk ?? "");
    });
    child.stderr.on("data", (chunk) => {
      stderr += String(chunk ?? "");
    });

    const timer = setTimeout(() => {
      if (finished) return;
      finished = true;
      child.kill("SIGTERM");
      resolve({ code: 124, stdout, stderr, timedOut: true });
    }, timeoutMs);

    child.on("error", (err) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      resolve({ code: 1, stdout, stderr: `${stderr}\n${String(err?.message ?? err)}`.trim(), timedOut: false });
    });

    child.on("close", (code) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      resolve({ code: code ?? 1, stdout, stderr, timedOut: false });
    });
  });
}

function compactOutput(value: string, maxLen: number): string {
  const text = String(value || "").trim();
  if (!text) return "";
  if (text.length <= maxLen) return text;
  return `${text.slice(0, maxLen - 1)}…`;
}

function getConfigPath(): string {
  const fromEnv = process.env.OPENCLAW_CONFIG_PATH?.trim();
  if (fromEnv) return fromEnv;
  return path.join(os.homedir(), ".openclaw", "openclaw.json");
}

async function cleanupLegacyWttLoadPath(): Promise<{ changed: boolean; error?: string }> {
  const configPath = getConfigPath();
  let parsed: Record<string, unknown>;
  try {
    const text = await fs.readFile(configPath, "utf8");
    parsed = JSON.parse(text) as Record<string, unknown>;
  } catch (error) {
    const code = (error as NodeJS.ErrnoException | undefined)?.code;
    if (code === "ENOENT") return { changed: false };
    return { changed: false, error: String((error as Error).message || error) };
  }

  const plugins = (parsed.plugins && typeof parsed.plugins === "object" && !Array.isArray(parsed.plugins))
    ? (parsed.plugins as Record<string, unknown>)
    : {};
  const load = (plugins.load && typeof plugins.load === "object" && !Array.isArray(plugins.load))
    ? (plugins.load as Record<string, unknown>)
    : {};
  const rawPaths = Array.isArray(load.paths)
    ? load.paths.filter((v): v is string => typeof v === "string")
    : [];

  const filtered = rawPaths.filter((v) => v.trim() !== "/opt/wtt-plugin");
  if (filtered.length === rawPaths.length) return { changed: false };

  if (filtered.length > 0) {
    load.paths = filtered;
    plugins.load = load;
  } else {
    delete load.paths;
    if (Object.keys(load).length > 0) plugins.load = load;
    else delete plugins.load;
  }

  parsed.plugins = plugins;

  const tmp = `${configPath}.tmp-${Date.now()}`;
  await fs.writeFile(tmp, `${JSON.stringify(parsed, null, 2)}\n`, "utf8");
  await fs.rename(tmp, configPath);
  return { changed: true };
}

function scheduleGatewayRestart(): void {
  // Delay a little so command response can be delivered before gateway restarts.
  const script = "sleep 2; openclaw gateway restart >/tmp/wtt-plugin-update.log 2>&1";
  const child = spawn("sh", ["-lc", script], {
    detached: true,
    stdio: "ignore",
    env: process.env,
  });
  child.unref();
}

function outputOf(result: CommandRunResult): string {
  return `${result.stdout || ""}\n${result.stderr || ""}`.trim();
}

function hasUnknownWttChannelError(result: CommandRunResult): boolean {
  const text = outputOf(result).toLowerCase();
  return text.includes("unknown channel id: wtt")
    || (text.includes("channels.wtt") && text.includes("invalid config"));
}

function isPluginAlreadyExistsError(result: CommandRunResult): boolean {
  return outputOf(result).toLowerCase().includes("plugin already exists");
}

function hasScopedZipMissingError(result: CommandRunResult): boolean {
  const text = outputOf(result).toLowerCase();
  return text.includes("enoent")
    && text.includes("openclaw-clawhub-package")
    && text.includes("@cecwxf/wtt.zip");
}

function shQuote(value: string): string {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`;
}

async function runUpdate(cmd: string): Promise<CommandRunResult> {
  return runCommand(cmd, ["plugins", "update", "wtt"], 180_000);
}

async function runInstall(cmd: string): Promise<CommandRunResult> {
  return runCommand(cmd, ["plugins", "install", "@cecwxf/wtt@latest"], 180_000);
}

async function runInstallViaNpmPack(cmd: string): Promise<CommandRunResult> {
  const script = [
    "set -e",
    "tmp=$(mktemp -d)",
    "pkg=$(cd \"$tmp\" && npm pack @cecwxf/wtt@latest --silent)",
    `${shQuote(cmd)} plugins install \"$tmp/$pkg\" --pin`,
  ].join("; ");

  return runCommand("sh", ["-lc", script], 240_000);
}

async function runDoctorFix(cmd: string): Promise<CommandRunResult> {
  return runCommand(cmd, ["doctor", "--fix", "--non-interactive", "--yes"], 180_000);
}

export async function handleUpdateCommand(_ctx: WTTCommandExecutionContext): Promise<string> {
  const cmd = process.env.OPENCLAW_BIN?.trim() || "openclaw";

  // Path A: preferred and idempotent for existing installs
  let update = await runUpdate(cmd);
  if (update.code !== 0 && hasUnknownWttChannelError(update)) {
    const repair = await runDoctorFix(cmd);
    if (repair.code === 0) {
      update = await runUpdate(cmd);
    } else {
      const detail = compactOutput(outputOf(repair), 800);
      return [
        "WTT 插件升级失败：自动修复配置未成功。",
        detail ? `doctor 详情: ${detail}` : "doctor 详情: 无",
        "请手动执行：openclaw doctor --fix，然后重试 /wtt update",
      ].join("\n");
    }
  }

  if (update.code === 0) {
    const cleanup = await cleanupLegacyWttLoadPath();
    scheduleGatewayRestart();
    const summary = compactOutput(outputOf(update), 260);
    const lines = [
      "WTT 插件已升级（update 模式）。",
      "网关将在约 2 秒后自动重启。",
      "重启期间短暂离线属正常，恢复后可用 /wtt help 验证。",
    ];
    if (cleanup.changed) lines.push("已清理 legacy load.path: /opt/wtt-plugin（避免 duplicate plugin id 警告）。");
    else if (cleanup.error) lines.push(`配置清理提示: ${cleanup.error}`);
    if (summary) lines.push(`update: ${summary}`);
    return lines.join("\n");
  }

  // Path B: fallback for old/non-tracked installs
  let install = await runInstall(cmd);
  let installMode: "install" | "npm-pack" = "install";

  if (install.code !== 0 && hasUnknownWttChannelError(install)) {
    const repair = await runDoctorFix(cmd);
    if (repair.code === 0) {
      install = await runInstall(cmd);
    } else {
      const detail = compactOutput(outputOf(repair), 800);
      return [
        "WTT 插件升级失败：自动修复配置未成功。",
        detail ? `doctor 详情: ${detail}` : "doctor 详情: 无",
        "请手动执行：openclaw doctor --fix，然后重试 /wtt update",
      ].join("\n");
    }
  }

  // Scoped package install fallback for OpenClaw versions that fail on @scope zip path.
  if (install.code !== 0 && hasScopedZipMissingError(install)) {
    const packed = await runInstallViaNpmPack(cmd);
    if (packed.code === 0) {
      install = packed;
      installMode = "npm-pack";
    } else {
      const detail = compactOutput(outputOf(packed), 800);
      return [
        "WTT 插件升级失败：检测到 scoped 包下载链路异常，自动 fallback 也失败。",
        detail ? `fallback 详情: ${detail}` : "fallback 详情: 无",
        "请手动执行：npm pack @cecwxf/wtt@latest && openclaw plugins install <tgz> --pin",
      ].join("\n");
    }
  }

  if (install.code !== 0 && isPluginAlreadyExistsError(install)) {
    const uninstall = await runCommand(cmd, ["plugins", "uninstall", "wtt"], 120_000);
    if (uninstall.code === 0) {
      install = await runInstall(cmd);
      installMode = "install";
      if (install.code !== 0 && hasScopedZipMissingError(install)) {
        const packed = await runInstallViaNpmPack(cmd);
        if (packed.code === 0) {
          install = packed;
          installMode = "npm-pack";
        } else {
          const detail = compactOutput(outputOf(packed), 800);
          return [
            "WTT 插件升级失败：卸载旧目录后重装触发 scoped 包下载异常，fallback 失败。",
            detail ? `fallback 详情: ${detail}` : "fallback 详情: 无",
            "请手动执行：npm pack @cecwxf/wtt@latest && openclaw plugins install <tgz> --pin",
          ].join("\n");
        }
      }
    } else {
      const detail = compactOutput(outputOf(uninstall), 800);
      return [
        "WTT 插件升级失败：检测到已安装旧目录，且自动卸载失败。",
        detail ? `uninstall 详情: ${detail}` : "uninstall 详情: 无",
        "请手动执行：openclaw plugins uninstall wtt，再重试 /wtt update",
      ].join("\n");
    }
  }

  if (install.code !== 0) {
    const reason = install.timedOut
      ? "超时（180s）"
      : `退出码 ${install.code}`;
    const detail = compactOutput(outputOf(install), 800);
    return [
      `WTT 插件升级失败：${reason}`,
      detail ? `详情: ${detail}` : "详情: 无",
      "你可以稍后重试：/wtt update",
    ].join("\n");
  }

  const cleanup = await cleanupLegacyWttLoadPath();
  scheduleGatewayRestart();

  const installSummary = compactOutput(outputOf(install), 260);
  const modeLabel = installMode === "npm-pack" ? "npm pack fallback 模式" : "install 模式";
  const lines = [
    `WTT 插件已升级到 latest（${modeLabel}）。`,
    "网关将在约 2 秒后自动重启。",
    "重启期间短暂离线属正常，恢复后可用 /wtt help 验证。",
  ];
  if (cleanup.changed) lines.push("已清理 legacy load.path: /opt/wtt-plugin（避免 duplicate plugin id 警告）。");
  else if (cleanup.error) lines.push(`配置清理提示: ${cleanup.error}`);
  if (installSummary) lines.push(`install: ${installSummary}`);
  return lines.join("\n");
}
