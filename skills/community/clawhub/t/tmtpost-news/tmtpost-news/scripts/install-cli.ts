import {
  detectPlatform, downloadAndInstallCli, runCliVersion, parseCliVersionJson, fail,
  DEFAULT_CHECKSUM_URL,
} from "./_common.ts";

let forceInstall = false;
for (const arg of process.argv.slice(2)) {
  if (arg === "help" || arg === "--help" || arg === "-h") {
    console.log("Usage: bun scripts/install-cli.ts [--force]\n\nDownload the current-platform CLI into the skill directory and verify it.");
    process.exit(0);
  }
  if (arg === "--force") {
    forceInstall = true;
    continue;
  }
  fail(`unknown argument: ${arg}`);
}

const p = detectPlatform({ preferGlobal: !forceInstall });

if (p.cliSource === "global") {
  const rawVersionOutput = await runCliVersion(p.cliPath);
  const versionInfo = parseCliVersionJson(rawVersionOutput, `${p.cliPath} version`);
  const currentVersion = versionInfo.current_version ?? null;
  const latestVersion = versionInfo.latest_version ?? null;

  console.log(JSON.stringify({
    installed: true,
    source: "global",
    platform: { os: p.os, arch: p.arch, cliPath: p.cliPath },
    downloadUrl: null,
    currentVersion,
    latestVersion,
    rawVersionOutput,
    note: "Using globally installed CLI. No download needed.",
  }, null, 2));
  process.exit(0);
}

const downloadUrl = p.cliDownloadUrl;

const { rawVersionOutput, versionInfo } = await downloadAndInstallCli(downloadUrl, p.cliPath, DEFAULT_CHECKSUM_URL);
const currentVersion = versionInfo.current_version ?? null;
const latestVersion = versionInfo.latest_version ?? null;

console.log(JSON.stringify({
  installed: true,
  source: "local",
  platform: { os: p.os, arch: p.arch, cliPath: p.cliPath },
  downloadUrl,
  currentVersion,
  latestVersion,
  rawVersionOutput,
}, null, 2));
