import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import {
  chmod,
  lstat,
  mkdir,
  mkdtemp,
  readdir,
  rename,
  rm,
  rmdir,
  stat,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, isAbsolute, join, normalize, resolve } from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export const RELEASE_VERSION = "v0.1.1";
export const RELEASE_ARCHIVE_URL =
  "https://github.com/Theorvane/proxmox-mcp/releases/download/v0.1.1/proxmox-mcp-0.1.1.tar.gz";
export const RELEASE_CHECKSUM_URL = `${RELEASE_ARCHIVE_URL}.sha256`;
const ARCHIVE_ROOT = "proxmox-mcp-0.1.1";
const REQUIRED_ENVIRONMENT = [
  "PROXMOX_BASE_URL",
  "PROXMOX_TOKEN_ID",
  "PROXMOX_TOKEN_SECRET",
];

function requiredCredentials(environment) {
  for (const name of REQUIRED_ENVIRONMENT) {
    if (!environment[name])
      throw new Error(`Missing required environment variable: ${name}`);
  }
  return environment;
}

function safeInstallDirectory(directory) {
  if (!directory || !isAbsolute(directory))
    throw new Error("Installation directory must be an absolute path");
  const absolute = resolve(directory);
  if (absolute === resolve("/") || absolute === resolve(tmpdir()))
    throw new Error("Refusing an unsafe installation directory");
  return absolute;
}

export function createInstallPlan(directory, environment) {
  requiredCredentials(environment);
  const installDirectory = safeInstallDirectory(directory);
  return Object.freeze({
    releaseVersion: RELEASE_VERSION,
    archiveUrl: RELEASE_ARCHIVE_URL,
    checksumUrl: RELEASE_CHECKSUM_URL,
    installDirectory,
    command: join(installDirectory, "proxmox-mcp"),
    cwd: installDirectory,
  });
}

function checksumFromFile(checksumFile) {
  const match = checksumFile
    .toString("utf8")
    .match(/^([a-fA-F0-9]{64})\s+\*?proxmox-mcp-0\.1\.1\.tar\.gz\s*$/m);
  if (!match) throw new Error("Release checksum file has an invalid format");
  return match[1].toLowerCase();
}

function verifyChecksum(archive, checksumFile) {
  const actual = createHash("sha256").update(archive).digest("hex");
  if (actual !== checksumFromFile(checksumFile))
    throw new Error("Release archive checksum verification failed");
}

function assertSafeArchiveEntries(entries) {
  if (!entries.length) throw new Error("Release archive is empty");
  for (const entry of entries) {
    const normalized = normalize(entry);
    if (
      !entry ||
      entry.includes("\\") ||
      entry.startsWith("/") ||
      normalized === ".." ||
      normalized.startsWith(`..${"/"}`) ||
      !normalized.startsWith(`${ARCHIVE_ROOT}/`)
    ) {
      throw new Error("Release archive contains an unsafe archive entry");
    }
  }
}

async function assertDestinationAvailable(directory) {
  try {
    await lstat(directory);
    throw new Error("Installation directory must not already exist");
  } catch (error) {
    if (error?.code === "ENOENT") return;
    else throw error;
  }
}

export async function validateInstallPlan(directory, environment) {
  const plan = createInstallPlan(directory, environment);
  await assertDestinationAvailable(plan.installDirectory);
  return plan;
}

function containsProxmoxRegistration(value) {
  if (Array.isArray(value)) return value.some(containsProxmoxRegistration);
  if (!value || typeof value !== "object") return false;
  if (value.name === "proxmox-mcp") return true;
  return Object.entries(value).some(
    ([key, child]) =>
      key === "proxmox-mcp" || containsProxmoxRegistration(child),
  );
}

async function assertRegistrationAvailable(dependencies) {
  const result = await dependencies.run("openclaw", ["mcp", "list", "--json"]);
  if (result.exitCode !== 0)
    throw new Error(
      "Unable to determine whether proxmox-mcp is already registered",
    );
  try {
    if (containsProxmoxRegistration(JSON.parse(result.stdout)))
      throw new Error(
        "proxmox-mcp is already registered; replacement is intentionally not supported by this installer",
      );
  } catch (error) {
    if (error instanceof SyntaxError)
      throw new Error("OpenClaw returned an invalid MCP registration list");
    throw error;
  }
}

export async function defaultDownload(url, fetchImpl = fetch) {
  let response;
  try {
    response = await fetchImpl(url, { redirect: "follow" });
  } catch {
    throw new Error("Unable to download the pinned release artifact");
  }
  if (!response.ok)
    throw new Error(
      `Unable to download the pinned release artifact (${response.status})`,
    );
  let finalUrl;
  try {
    finalUrl = new URL(response.url);
  } catch {
    throw new Error(
      "Release download did not resolve to a secure HTTPS destination",
    );
  }
  if (finalUrl.protocol !== "https:")
    throw new Error(
      "Release download did not resolve to a secure HTTPS destination",
    );
  return Buffer.from(await response.arrayBuffer());
}

async function defaultListArchiveEntries(archive, workDirectory = tmpdir()) {
  const archivePath = join(workDirectory, "release.tar.gz");
  await writeFile(archivePath, archive, { mode: 0o600 });
  try {
    const { stdout } = await execFileAsync("tar", ["-tzf", archivePath], {
      encoding: "utf8",
    });
    return stdout.split("\n").filter(Boolean);
  } finally {
    await rm(archivePath, { force: true });
  }
}

async function defaultExtractArchive(
  archive,
  destination,
  workDirectory = tmpdir(),
) {
  const archivePath = join(workDirectory, "release.tar.gz");
  const extracted = join(workDirectory, "extracted");
  await writeFile(archivePath, archive, { mode: 0o600 });
  await mkdir(extracted, { mode: 0o700 });
  try {
    await execFileAsync("tar", ["-C", extracted, "-xzf", archivePath]);
    const root = join(extracted, ARCHIVE_ROOT);
    const rootInfo = await stat(root);
    if (!rootInfo.isDirectory())
      throw new Error("Release archive has an unexpected layout");
    for (const entry of await readdir(root))
      await rename(join(root, entry), join(destination, entry));
    await chmod(join(destination, "proxmox-mcp"), 0o755);
  } finally {
    await rm(archivePath, { force: true });
    await rm(extracted, { recursive: true, force: true });
  }
}

async function defaultRun(command, args, options = {}) {
  try {
    const { stdout, stderr } = await execFileAsync(command, args, options);
    return { exitCode: 0, stdout, stderr };
  } catch (error) {
    return {
      exitCode: error.code ?? 1,
      stdout: error.stdout ?? "",
      stderr: error.stderr ?? "",
    };
  }
}

const defaults = {
  download: defaultDownload,
  listArchiveEntries: defaultListArchiveEntries,
  extractArchive: defaultExtractArchive,
  run: defaultRun,
};

async function assertStagedArtifact(stageDirectory) {
  const entries = await readdir(stageDirectory);
  if (!entries.length)
    throw new Error("Release archive extracted no installable files");
  const command = await lstat(join(stageDirectory, "proxmox-mcp"));
  if (!command.isFile() || command.isSymbolicLink())
    throw new Error(
      "Release archive did not provide a safe proxmox-mcp executable",
    );
  return entries;
}

async function compensatePromotedFiles(directory, createdEntries) {
  for (const entry of createdEntries) {
    if (
      entry === "." ||
      entry === ".." ||
      entry.includes("/") ||
      entry.includes("\\")
    )
      continue;
    await rm(join(directory, entry), { recursive: true, force: true });
  }
  try {
    await rmdir(directory);
  } catch (error) {
    if (error?.code !== "ENOTEMPTY" && error?.code !== "ENOENT") throw error;
  }
}

export async function install(directory, environment, dependencies = defaults) {
  const credentials = requiredCredentials(environment);
  const plan = await validateInstallPlan(directory, credentials);
  await mkdir(dirname(plan.installDirectory), { recursive: true, mode: 0o700 });

  const [archive, checksumFile] = await Promise.all([
    dependencies.download(plan.archiveUrl),
    dependencies.download(plan.checksumUrl),
  ]);
  verifyChecksum(archive, checksumFile);

  const stageDirectory = await mkdtemp(
    join(dirname(plan.installDirectory), ".proxmox-mcp-stage-"),
  );
  try {
    assertSafeArchiveEntries(
      await dependencies.listArchiveEntries(archive, stageDirectory),
    );
    await dependencies.extractArchive(archive, stageDirectory, stageDirectory);
    const createdEntries = await assertStagedArtifact(stageDirectory);
    await assertRegistrationAvailable(dependencies);
    await assertDestinationAvailable(plan.installDirectory);
    await rename(stageDirectory, plan.installDirectory);
    try {
      const result = await dependencies.run("openclaw", [
        "mcp",
        "add",
        "proxmox-mcp",
        "--command",
        plan.command,
        "--cwd",
        plan.cwd,
        "--env",
        `PROXMOX_BASE_URL=${credentials.PROXMOX_BASE_URL}`,
        "--env",
        `PROXMOX_TOKEN_ID=${credentials.PROXMOX_TOKEN_ID}`,
        "--env",
        `PROXMOX_TOKEN_SECRET=${credentials.PROXMOX_TOKEN_SECRET}`,
      ]);
      if (result.exitCode !== 0)
        throw new Error("OpenClaw MCP registration failed");
    } catch (error) {
      await compensatePromotedFiles(plan.installDirectory, createdEntries);
      throw error;
    }
  } finally {
    await rm(stageDirectory, { recursive: true, force: true });
  }
  return plan;
}
