import {
  type PlatformInfo,
  detectPlatform, getPlatformJson, getApiKeyState,
  fail,
} from "./_common.ts";

if (process.argv[2] === "help") {
  console.log("Usage: bun scripts/cli-state.ts\n\nPrint install state, version/update status, and API key status.");
  process.exit(0);
}

const args = process.argv.slice(2);
if (args.length > 0) {
  fail(`unknown argument: ${args[0]}`);
}

const p = detectPlatform();
const cliExists = p.cliSource === "global" || await Bun.file(p.cliPath).exists();
const cliSource: PlatformInfo["cliSource"] = p.cliSource === "global" ? "global" : (cliExists ? "local" : "none");
const platform: PlatformInfo = { ...p, cliSource };

const update = {
  needUpdate: null as boolean | null,
  error: null as string | null,
};

if (cliExists) {
  try {
    const proc = Bun.spawnSync([platform.cliPath, "version"], { stdout: "pipe", stderr: "pipe" });
    const rawVersionOutput = (proc.stdout.toString() + proc.stderr.toString()).trim();

    if (proc.exitCode !== 0) {
      update.error = rawVersionOutput || `${platform.cliPath} version failed with exit code ${proc.exitCode}`;
    } else {
      let versionInfo: unknown;
      try {
        versionInfo = JSON.parse(rawVersionOutput);
      } catch {
        update.error = `${platform.cliPath} version did not return valid JSON: ${rawVersionOutput || "(empty output)"}`;
      }

      if (!update.error) {
        if (!versionInfo || typeof versionInfo !== "object" || Array.isArray(versionInfo)) {
          update.error = `${platform.cliPath} version did not return a JSON object: ${rawVersionOutput || "(empty output)"}`;
        } else {
          const parsed = versionInfo as { need_update?: unknown };
          if (typeof parsed.need_update === "boolean") {
            update.needUpdate = parsed.need_update;
          } else {
            update.error = `${platform.cliPath} version did not return a valid need_update value: ${rawVersionOutput || "(empty output)"}`;
          }
        }
      }
    }
  } catch (error) {
    update.error = error instanceof Error ? error.message : String(error);
  }
}

console.log(JSON.stringify({
  platform: getPlatformJson(platform),
  cliExists,
  update,
  apiKey: await getApiKeyState(platform),
}, null, 2));
