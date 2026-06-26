import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import type { WTTCommandExecutionContext } from "./types.js";

type PackageLike = {
  name?: string;
  version?: string;
};

async function readCurrentPackage(): Promise<PackageLike> {
  const here = dirname(fileURLToPath(import.meta.url));
  const packagePath = join(here, "..", "..", "package.json");
  const raw = await readFile(packagePath, "utf8");
  const parsed = JSON.parse(raw) as PackageLike;
  return parsed;
}

export async function handleVersionCommand(ctx: WTTCommandExecutionContext): Promise<string> {
  try {
    const pkg = await readCurrentPackage();
    const pluginName = pkg.name || "@cecwxf/wtt";
    const pluginVersion = pkg.version || "unknown";
    const account = ctx.account?.accountId || ctx.accountId || "default";

    return [
      "WTT Plugin 版本信息",
      `- package: ${pluginName}`,
      `- version: ${pluginVersion}`,
      `- account: ${account}`,
      "提示：如需升级可执行 /wtt update",
    ].join("\n");
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return `读取 WTT Plugin 版本失败：${msg}`;
  }
}
