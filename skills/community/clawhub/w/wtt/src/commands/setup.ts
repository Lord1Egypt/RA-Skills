import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";

import type { WTTCommandExecutionContext } from "./types.js";

type JsonObject = Record<string, unknown>;

function asObject(value: unknown): JsonObject {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as JsonObject;
}

function getConfigPath(): string {
  const fromEnv = process.env.OPENCLAW_CONFIG_PATH?.trim();
  if (fromEnv) return fromEnv;
  return path.join(os.homedir(), ".openclaw", "openclaw.json");
}

function mergeWttConfig(
  raw: JsonObject,
  params: { agentId: string; token: string; cloudUrl: string },
): JsonObject {
  const next: JsonObject = { ...raw };

  const plugins = asObject(next.plugins);
  const entries = asObject(plugins.entries);
  entries.wtt = {
    ...asObject(entries.wtt),
    enabled: true,
  };
  plugins.entries = entries;

  // Cleanup legacy load path that can cause duplicate plugin-id warning:
  // global plugin (/opt/wtt-plugin) + config plugin (extensions/wtt).
  const load = asObject(plugins.load);
  const rawPaths = Array.isArray(load.paths)
    ? load.paths.filter((v): v is string => typeof v === "string")
    : [];
  const filteredPaths = rawPaths.filter((v) => v.trim() !== "/opt/wtt-plugin");
  if (filteredPaths.length > 0) {
    load.paths = filteredPaths;
    plugins.load = load;
  } else {
    delete load.paths;
    if (Object.keys(load).length > 0) plugins.load = load;
    else delete plugins.load;
  }

  next.plugins = plugins;

  const commands = asObject(next.commands);
  const allowFrom = asObject(commands.allowFrom);
  const existingAllow = Array.isArray(allowFrom.wtt)
    ? allowFrom.wtt.filter((v): v is string => typeof v === "string")
    : [];
  const mergedAllow = existingAllow.includes("*") ? existingAllow : [...existingAllow, "*"];
  allowFrom.wtt = mergedAllow;
  commands.allowFrom = allowFrom;
  next.commands = commands;

  const channels = asObject(next.channels);
  const wtt = asObject(channels.wtt);
  const accounts = asObject(wtt.accounts);
  const currentDefault = asObject(accounts.default);

  accounts.default = {
    ...currentDefault,
    enabled: true,
    cloudUrl: params.cloudUrl,
    agentId: params.agentId,
    token: params.token,
    slashCompat: true,
    slashCompatWttPrefixOnly: true,
    slashBypassMentionGate: true,
    taskExecutorScope: "pipeline_only",
    p2pE2EEnabled: false,
  };

  wtt.accounts = accounts;
  channels.wtt = wtt;
  next.channels = channels;

  return next;
}

export async function handleSetupCommand(
  command: { agentId: string; token: string; cloudUrl?: string },
  ctx: WTTCommandExecutionContext,
): Promise<string> {
  const cloudUrl = (command.cloudUrl || ctx.account?.cloudUrl || "https://www.waxbyte.com").trim();
  if (!command.agentId || !command.token) {
    return "参数缺失：用法 @wtt setup <agent_id> <agent_token> [cloudUrl]";
  }

  const configPath = getConfigPath();

  let existing: JsonObject = {};
  try {
    const rawText = await fs.readFile(configPath, "utf8");
    existing = asObject(JSON.parse(rawText));
  } catch (error) {
    const code = (error as NodeJS.ErrnoException | undefined)?.code;
    if (code !== "ENOENT") {
      return `写入失败：无法读取 ${configPath}（${String((error as Error).message || error)}）`;
    }

    await fs.mkdir(path.dirname(configPath), { recursive: true });
  }

  const merged = mergeWttConfig(existing, {
    agentId: command.agentId.trim(),
    token: command.token.trim(),
    cloudUrl,
  });

  const tempPath = `${configPath}.tmp-${Date.now()}`;
  await fs.writeFile(tempPath, `${JSON.stringify(merged, null, 2)}\n`, "utf8");
  await fs.rename(tempPath, configPath);

  return [
    "✅ WTT 配置已写入 openclaw.json",
    `config: ${configPath}`,
    `agentId: ${command.agentId.trim()}`,
    `cloudUrl: ${cloudUrl}`,
    "下一步：执行 /restart 使配置生效",
  ].join("\n");
}
