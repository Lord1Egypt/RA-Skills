import { existsSync } from "node:fs";
import { chmod, mkdir, rename, unlink } from "node:fs/promises";
import { createHash } from "node:crypto";

export const BASE_DOWNLOAD_URL = "https://example.com/tmtpost-cli";
export const DEFAULT_CHECKSUM_URL = `${BASE_DOWNLOAD_URL}/checksums.txt`;

const SCRIPT_DIR = import.meta.dir.replaceAll("\\", "/");
export const SKILL_DIR = SCRIPT_DIR.replace(/\/[^/]+$/, "");

export function fail(msg: string): never {
  console.error(`Error: ${msg}`);
  process.exit(1);
}

export function normalizeApiKey(raw: string): string {
  let key = raw.trim();
  if ((key.startsWith('"') && key.endsWith('"')) || (key.startsWith("'") && key.endsWith("'"))) {
    key = key.slice(1, -1);
  }
  key = key.replace(/^api[\s_-]*key\s*[:=]\s*/i, "");
  return key.trim();
}

function formatError(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

function parentDir(path: string): string {
  const normalized = path.replaceAll("\\", "/");
  const idx = normalized.lastIndexOf("/");
  if (idx === -1) return ".";
  if (idx === 0) return "/";
  return normalized.slice(0, idx);
}

function createTempSiblingPath(path: string, label: string): string {
  return `${path}.${label}.${process.pid}.${Date.now()}`;
}

async function cleanupFile(path: string) {
  await unlink(path).catch(() => {});
}

async function replaceFile(sourcePath: string, targetPath: string) {
  if (process.platform !== "win32") {
    await rename(sourcePath, targetPath);
    return;
  }

  if (!(await Bun.file(targetPath).exists())) {
    await rename(sourcePath, targetPath);
    return;
  }

  const backupPath = createTempSiblingPath(targetPath, "bak");
  await rename(targetPath, backupPath);
  try {
    await rename(sourcePath, targetPath);
  } catch (error) {
    await rename(backupPath, targetPath).catch(() => {});
    throw error;
  }
  await cleanupFile(backupPath);
}

interface CommandResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  output: string;
}

async function runCommand(args: string[], description: string): Promise<CommandResult> {
  let proc: ReturnType<typeof Bun.spawn>;
  try {
    proc = Bun.spawn(args, { stdout: "pipe", stderr: "pipe" });
  } catch (error) {
    fail(`${description} failed to start: ${formatError(error)}`);
  }

  const stdoutPromise = new Response(proc.stdout).text();
  const stderrPromise = new Response(proc.stderr).text();
  const [stdout, stderr, exitCode] = await Promise.all([stdoutPromise, stderrPromise, proc.exited]);
  const output = (stdout + stderr).trim();
  return { stdout, stderr, exitCode, output };
}

async function runCommandOrFail(args: string[], description: string): Promise<string> {
  const { exitCode, output } = await runCommand(args, description);
  if (exitCode !== 0) {
    fail(`${description} failed with exit code ${exitCode}${output ? `: ${output}` : ""}`);
  }
  return output;
}

export interface PlatformInfo {
  os: string;
  arch: string;
  isWindows: boolean;
  cliFilename: string;
  cliPath: string;
  cliSource: "global" | "local" | "none";
  cliDownloadUrl: string;
}

export interface DetectPlatformOptions {
  preferGlobal?: boolean;
}

export function detectPlatform(options: DetectPlatformOptions = {}): PlatformInfo {
  const preferGlobal = options.preferGlobal ?? true;

  let os: string;
  switch (process.platform) {
    case "win32":  os = "windows"; break;
    case "darwin": os = "darwin";  break;
    case "linux":  os = "linux";   break;
    default: fail(`unsupported os: ${process.platform}`);
  }

  let arch: string;
  switch (process.arch) {
    case "arm64": arch = "arm64"; break;
    case "x64":   arch = "amd64"; break;
    default: fail(`unsupported architecture: ${process.arch}`);
  }

  const isWindows = os === "windows";
  const cliFilename = isWindows ? "tmtpost-news-cli.exe" : "tmtpost-news-cli";
  const localCliPath = `${SKILL_DIR}/${cliFilename}`;
  const cliDownloadUrl = `${BASE_DOWNLOAD_URL}/${os}-${arch}/${cliFilename}`;

  let cliPath = localCliPath;
  let cliSource: "global" | "local" | "none" = "none";

  if (existsSync(localCliPath)) {
    cliPath = localCliPath;
    cliSource = "local";
  } else if (preferGlobal) {
    try {
      const whichCmd = isWindows ? "where" : "which";
      const proc = Bun.spawnSync([whichCmd, cliFilename], { stdout: "pipe", stderr: "pipe" });
      if (proc.exitCode === 0) {
        const globalPath = proc.stdout.toString().trim().split(/\r?\n/)[0];
        if (globalPath) {
          const helpProc = Bun.spawnSync([globalPath, "help"], { stdout: "pipe", stderr: "pipe" });
          if (helpProc.exitCode === 0) {
            cliPath = globalPath;
            cliSource = "global";
          }
        }
      }
    } catch {
      // Ignore errors in global detection
    }
  }

  if (cliSource === "none") {
    cliPath = localCliPath;
  }

  return { os, arch, isWindows, cliFilename, cliPath, cliSource, cliDownloadUrl };
}

export function getPlatformJson(p: PlatformInfo) {
  return { os: p.os, arch: p.arch, cliPath: p.cliPath, cliSource: p.cliSource };
}

export async function downloadFile(url: string, outputPath: string) {
  const resp = await fetch(url);
  if (!resp.ok) fail(`download failed: ${resp.status} ${resp.statusText} from ${url}`);
  await mkdir(parentDir(outputPath), { recursive: true });
  await Bun.write(outputPath, resp);
}

export async function runCliVersion(cliPath: string): Promise<string> {
  if (!(await Bun.file(cliPath).exists())) fail(`cli not found at ${cliPath}`);
  if (process.platform !== "win32") {
    await chmod(cliPath, 0o755).catch(() => {});
  }
  return runCommandOrFail([cliPath, "version"], `${cliPath} version`);
}

export interface CliVersionInfo {
  current_version?: string;
  latest_version?: string;
  need_update?: boolean;
  release_notes?: string;
  download_urls?: Record<string, string>;
}

function getPlatformBinaryPath(downloadUrl: string): string {
  let parsedUrl: URL;
  try {
    parsedUrl = new URL(downloadUrl);
  } catch (error) {
    fail(`invalid download url for checksum verification: ${downloadUrl}: ${formatError(error)}`);
  }
  const segments = parsedUrl.pathname.split("/").filter(Boolean);
  if (segments.length < 2) {
    fail(`could not determine platform path from download url: ${downloadUrl}`);
  }
  return `${segments[segments.length - 2]}/${segments[segments.length - 1]}`;
}

async function fetchChecksumForPlatform(checksumUrl: string, downloadUrl: string): Promise<string> {
  const platformBinaryPath = getPlatformBinaryPath(downloadUrl);
  const resp = await fetch(checksumUrl).catch((error: unknown) =>
    fail(`failed to fetch checksums from ${checksumUrl}: ${formatError(error)}`),
  );
  if (!resp.ok) fail(`failed to fetch checksums from ${checksumUrl}: ${resp.status} ${resp.statusText}`);
  const text = await resp.text().catch((error: unknown) =>
    fail(`failed to read checksums from ${checksumUrl}: ${formatError(error)}`),
  );
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    const match = trimmed.match(/^([0-9a-fA-F]{64})\s+(.+)$/);
    if (match) {
      const [, hash, filePath] = match;
      if (filePath === platformBinaryPath) return hash.toLowerCase();
    }
  }
  fail(`no matching checksum found for ${platformBinaryPath} in ${checksumUrl}`);
}

async function computeFileSha256(filePath: string): Promise<string> {
  const fileContent = await Bun.file(filePath).arrayBuffer();
  const hash = createHash("sha256");
  hash.update(Buffer.from(fileContent));
  return hash.digest("hex");
}

export function parseCliVersionJson(raw: string, context: string): CliVersionInfo {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    fail(`${context} did not return valid JSON: ${raw || "(empty output)"}`);
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    fail(`${context} did not return a JSON object: ${raw || "(empty output)"}`);
  }
  return parsed as CliVersionInfo;
}

export interface InstallCliResult {
  rawVersionOutput: string;
  versionInfo: CliVersionInfo;
}

export async function downloadAndInstallCli(
  downloadUrl: string,
  cliPath: string,
  checksumUrl: string,
): Promise<InstallCliResult> {
  const tempPath = createTempSiblingPath(cliPath, "download");
  try {
    await downloadFile(downloadUrl, tempPath);

    const expectedHash = await fetchChecksumForPlatform(checksumUrl, downloadUrl);
    const actualHash = await computeFileSha256(tempPath).catch((error: unknown) =>
      fail(`failed to compute sha256 for ${tempPath}: ${formatError(error)}`),
    );
    if (actualHash !== expectedHash) {
      fail(`checksum verification failed for ${downloadUrl}\n  expected: ${expectedHash}\n  actual:   ${actualHash}`);
    }
    console.error("Checksum verification passed.");

    const rawVersionOutput = await runCliVersion(tempPath);
    const versionInfo = parseCliVersionJson(rawVersionOutput, `${tempPath} version`);
    await replaceFile(tempPath, cliPath);
    if (process.platform !== "win32") {
      await chmod(cliPath, 0o755).catch(() => {});
    }
    return { rawVersionOutput, versionInfo };
  } finally {
    await cleanupFile(tempPath);
  }
}

function extractApiKey(output: string): string | null {
  const match = output.match(/API Key\s*:\s*(.+)$/m);
  if (!match) return null;
  const value = normalizeApiKey(match[1] || "");
  return value || null;
}

function includesMissingApiKeyMessage(output: string): boolean {
  return /未设置 API Key/i.test(output) || /not set/i.test(output);
}

async function ensureCliExecutable(cliPath: string): Promise<void> {
  if (!(await Bun.file(cliPath).exists())) fail(`cli not found at ${cliPath}`);
  if (process.platform !== "win32") {
    await chmod(cliPath, 0o755).catch(() => {});
  }
}

async function runCliCommand(p: PlatformInfo, args: string[]): Promise<CommandResult> {
  await ensureCliExecutable(p.cliPath);
  return runCommand([p.cliPath, ...args], `${p.cliPath} ${args.join(" ")}`);
}

export interface ApiKeyState {
  status: "configured" | "missing" | "error";
  present: boolean;
  error: string | null;
}

export async function getApiKeyState(p: PlatformInfo): Promise<ApiKeyState> {
  if (p.cliSource !== "global" && !(await Bun.file(p.cliPath).exists())) {
    return { status: "error", present: false, error: "CLI not found, cannot check API key." };
  }

  const result = await runCliCommand(p, ["apikey-get"]);
  const rawOutput = result.output;

  if (result.exitCode === 0) {
    const key = extractApiKey(rawOutput);
    return {
      status: key ? "configured" : "error",
      present: !!key,
      error: key ? null : "CLI apikey-get succeeded, but API key could not be parsed from output.",
    };
  }

  if (includesMissingApiKeyMessage(rawOutput) || result.exitCode === 2) {
    return { status: "missing", present: false, error: null };
  }

  return { status: "error", present: false, error: rawOutput || `apikey-get failed with exit code ${result.exitCode}.` };
}
