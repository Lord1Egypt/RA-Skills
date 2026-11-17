import { spawn } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { createReadStream } from "node:fs";
import { chmod, mkdir, open, rename, stat, unlink } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

export const YT_DLP_VERSION = "2026.07.04";

const MAXIMUM_BINARY_BYTES = 64 * 1024 * 1024;
const MAXIMUM_REDIRECTS = 5;
const DOWNLOAD_TIMEOUT_MS = 2 * 60_000;
const MANAGED_VERSION_TIMEOUT_MS = 60_000;
const VERSION_TIMEOUT_MS = 10_000;
const RELEASE_BASE_URL = `https://github.com/yt-dlp/yt-dlp/releases/download/${YT_DLP_VERSION}/`;
const MANUAL_INSTALL_URL = "https://github.com/yt-dlp/yt-dlp/wiki/Installation";
const RELEASE_HOSTS = new Set([
  "github.com",
  "objects.githubusercontent.com",
  "release-assets.githubusercontent.com",
]);
const INSTALLS = new Map();

const ASSETS = Object.freeze({
  "darwin-arm64": Object.freeze({
    filename: "yt-dlp_macos",
    sha256: "498bd0dae17855c599d371d68ec5bafc439a9d8640e838be25c765a9792f261b",
  }),
  "darwin-x64": Object.freeze({
    filename: "yt-dlp_macos",
    sha256: "498bd0dae17855c599d371d68ec5bafc439a9d8640e838be25c765a9792f261b",
  }),
  "linux-arm64-glibc": Object.freeze({
    filename: "yt-dlp_linux_aarch64",
    sha256: "b6ce97646773070d7a7ffd6bbbdcaecb47c48483909c54c915bf08a7a9b5e0b1",
  }),
  "linux-arm64-musl": Object.freeze({
    filename: "yt-dlp_musllinux_aarch64",
    sha256: "9a6a4de88f35dc68c1763945fbb417e092ebd9afc5d66052ac31b68d405a12a7",
  }),
  "linux-x64-glibc": Object.freeze({
    filename: "yt-dlp_linux",
    sha256: "6bbb3d314cde4febe36e5fa1d55462e29c974f63444e707871834f6d8cc210ae",
  }),
  "linux-x64-musl": Object.freeze({
    filename: "yt-dlp_musllinux",
    sha256: "f7439ec2e3ffe69e06ac233f83f0d9687b89105939129bddcbf74e5de0f2b40e",
  }),
  "win32-arm64": Object.freeze({
    filename: "yt-dlp_arm64.exe",
    sha256: "1525690b037ecc0bb677e38e7147b0025179cbc9a8d0c57264e3100b18099280",
  }),
  "win32-x64": Object.freeze({
    filename: "yt-dlp.exe",
    sha256: "52fe3c26dcf71fbdc85b528589020bb0b8e383155cfa81b64dd447bbe35e24b8",
  }),
});

function isMuslRuntime() {
  try {
    const report = process.report?.getReport();
    return report?.header?.glibcVersionRuntime === undefined;
  } catch {
    return false;
  }
}

export function selectYtDlpAsset({
  platform = process.platform,
  arch = process.arch,
  libc = platform === "linux" && isMuslRuntime() ? "musl" : "glibc",
} = {}) {
  const key =
    platform === "linux"
      ? `${platform}-${arch}-${libc}`
      : `${platform}-${arch}`;
  const asset = ASSETS[key];
  if (asset === undefined) {
    throw new Error(
      `This platform needs a manual yt-dlp installation: ${MANUAL_INSTALL_URL}`,
    );
  }
  return asset;
}

export function isAcceptedYtDlpVersion(value) {
  const match = /^(\d{4}\.\d{2}\.\d{2})(?:[.+-].*)?$/u.exec(value.trim());
  return match !== null && match[1] >= YT_DLP_VERSION;
}

function cacheBaseDirectory(platform, environment, homeDirectory) {
  const pathApi = platform === "win32" ? path.win32 : path.posix;
  if (platform === "win32") {
    const localAppData = environment.LOCALAPPDATA?.trim();
    return localAppData && pathApi.isAbsolute(localAppData)
      ? localAppData
      : pathApi.join(homeDirectory, "AppData", "Local");
  }
  if (platform === "darwin") {
    return pathApi.join(homeDirectory, "Library", "Caches");
  }
  const xdgCache = environment.XDG_CACHE_HOME?.trim();
  return xdgCache && pathApi.isAbsolute(xdgCache)
    ? xdgCache
    : pathApi.join(homeDirectory, ".cache");
}

export function ytDlpCacheDirectory({
  platform = process.platform,
  environment = process.env,
  homeDirectory = os.homedir(),
} = {}) {
  const pathApi = platform === "win32" ? path.win32 : path.posix;
  return pathApi.join(
    cacheBaseDirectory(platform, environment, homeDirectory),
    "transcribe-media",
    "yt-dlp",
    YT_DLP_VERSION,
  );
}

function sanitizedEnvironment(environment) {
  const result = { ...environment };
  delete result.AUDIOFLOW_TOKEN;
  return result;
}

export async function probeYtDlpVersion(
  command,
  {
    signal,
    environment = process.env,
    spawnImpl = spawn,
    timeoutMs = VERSION_TIMEOUT_MS,
  } = {},
) {
  return await new Promise((resolve) => {
    let stdout = "";
    let settled = false;
    let child;
    const finish = (value) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      signal?.removeEventListener("abort", abort);
      resolve(value);
    };
    const abort = () => {
      child?.kill("SIGKILL");
      finish(undefined);
    };
    const timeout = setTimeout(abort, timeoutMs);
    try {
      child = spawnImpl(command, ["--version"], {
        env: sanitizedEnvironment(environment),
        shell: false,
        stdio: ["ignore", "pipe", "ignore"],
        windowsHide: true,
      });
    } catch {
      finish(undefined);
      return;
    }
    signal?.addEventListener("abort", abort, { once: true });
    child.stdout?.setEncoding("utf8");
    child.stdout?.on("data", (chunk) => {
      stdout += chunk;
      if (Buffer.byteLength(stdout, "utf8") > 64 * 1024) abort();
    });
    child.once("error", () => finish(undefined));
    child.once("close", (code) => {
      const version = stdout.trim().split(/\r?\n/u)[0];
      finish(code === 0 && version ? version : undefined);
    });
    if (signal?.aborted) abort();
  });
}

async function sha256File(filePath) {
  const fileStat = await stat(filePath);
  if (
    !fileStat.isFile() ||
    fileStat.size <= 0 ||
    fileStat.size > MAXIMUM_BINARY_BYTES
  ) {
    return undefined;
  }
  const hash = createHash("sha256");
  for await (const chunk of createReadStream(filePath)) hash.update(chunk);
  return hash.digest("hex");
}

async function verifyManagedBinary(
  filePath,
  asset,
  { signal, probeVersionImpl, environment },
) {
  try {
    if ((await sha256File(filePath)) !== asset.sha256) return false;
    await chmod(filePath, 0o700);
    const version = await probeVersionImpl(filePath, {
      signal,
      environment,
      timeoutMs: MANAGED_VERSION_TIMEOUT_MS,
    });
    return version === YT_DLP_VERSION;
  } catch {
    return false;
  }
}

function validateReleaseUrl(url) {
  if (
    url.protocol !== "https:" ||
    url.port !== "" ||
    url.username !== "" ||
    url.password !== "" ||
    url.hash !== "" ||
    !RELEASE_HOSTS.has(url.hostname.toLowerCase())
  ) {
    throw new Error("The yt-dlp release redirect was rejected.");
  }
  if (
    url.hostname.toLowerCase() === "github.com" &&
    !url.pathname.startsWith(
      `/yt-dlp/yt-dlp/releases/download/${YT_DLP_VERSION}/`,
    )
  ) {
    throw new Error("The yt-dlp release URL was rejected.");
  }
}

async function fetchReleaseAsset(url, { fetchImpl, signal }) {
  let current = new URL(url);
  for (
    let redirectCount = 0;
    redirectCount <= MAXIMUM_REDIRECTS;
    redirectCount += 1
  ) {
    validateReleaseUrl(current);
    const response = await fetchImpl(current, {
      headers: { "User-Agent": "AudioFlow-Transcribe/1.1" },
      redirect: "manual",
      signal,
    });
    if ([301, 302, 303, 307, 308].includes(response.status)) {
      const location = response.headers.get("location");
      if (location === null || redirectCount === MAXIMUM_REDIRECTS) {
        await response.body?.cancel();
        throw new Error("The yt-dlp release redirected too many times.");
      }
      await response.body?.cancel();
      current = new URL(location, current);
      continue;
    }
    if (response.status !== 200 || response.body === null) {
      await response.body?.cancel();
      throw new Error("The yt-dlp release could not be downloaded.");
    }
    const contentLengthHeader = response.headers.get("content-length");
    const contentLength = Number(contentLengthHeader);
    if (
      contentLengthHeader !== null &&
      Number.isFinite(contentLength) &&
      (contentLength <= 0 || contentLength > MAXIMUM_BINARY_BYTES)
    ) {
      await response.body.cancel();
      throw new Error("The yt-dlp release was too large.");
    }
    return response;
  }
  throw new Error("The yt-dlp release redirected too many times.");
}

async function writeAll(fileHandle, chunk) {
  const buffer = Buffer.from(chunk);
  let offset = 0;
  while (offset < buffer.length) {
    const { bytesWritten } = await fileHandle.write(
      buffer,
      offset,
      buffer.length - offset,
      null,
    );
    if (bytesWritten <= 0) throw new Error("The yt-dlp cache write failed.");
    offset += bytesWritten;
  }
}

async function downloadAssetToFile(asset, filePath, options) {
  const downloadSignal = options.signal
    ? AbortSignal.any([
        options.signal,
        AbortSignal.timeout(DOWNLOAD_TIMEOUT_MS),
      ])
    : AbortSignal.timeout(DOWNLOAD_TIMEOUT_MS);
  const response = await fetchReleaseAsset(
    new URL(asset.filename, RELEASE_BASE_URL),
    { ...options, signal: downloadSignal },
  );
  const handle = await open(filePath, "wx", 0o600);
  const hash = createHash("sha256");
  let size = 0;
  try {
    for await (const chunk of response.body) {
      size += chunk.byteLength;
      if (size > MAXIMUM_BINARY_BYTES) {
        throw new Error("The yt-dlp release was too large.");
      }
      hash.update(chunk);
      await writeAll(handle, chunk);
    }
    await handle.sync();
  } finally {
    await handle.close();
  }
  if (size <= 0 || hash.digest("hex") !== asset.sha256) {
    throw new Error("The yt-dlp release failed its SHA-256 check.");
  }
  await chmod(filePath, 0o700);
}

async function removeExactFile(filePath) {
  try {
    await unlink(filePath);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
}

async function publishVerifiedFile(temporaryPath, finalPath, verifyFinal) {
  try {
    await rename(temporaryPath, finalPath);
    return;
  } catch (error) {
    if (error?.code !== "EEXIST" && error?.code !== "EPERM") throw error;
  }
  if (await verifyFinal()) return;
  await removeExactFile(finalPath);
  try {
    await rename(temporaryPath, finalPath);
  } catch (error) {
    if (!(await verifyFinal())) throw error;
  }
}

export async function installYtDlpAsset(
  asset,
  {
    cacheDirectory,
    signal,
    fetchImpl = fetch,
    probeVersionImpl = probeYtDlpVersion,
    environment = process.env,
  },
) {
  const finalPath = path.join(cacheDirectory, asset.filename);
  if (
    await verifyManagedBinary(finalPath, asset, {
      signal,
      probeVersionImpl,
      environment,
    })
  ) {
    return finalPath;
  }

  const existing = INSTALLS.get(finalPath);
  if (existing !== undefined) return await existing;

  const install = (async () => {
    await mkdir(cacheDirectory, { mode: 0o700, recursive: true });
    await chmod(cacheDirectory, 0o700);
    if (
      await verifyManagedBinary(finalPath, asset, {
        signal,
        probeVersionImpl,
        environment,
      })
    ) {
      return finalPath;
    }
    const temporaryPath = path.join(
      cacheDirectory,
      `.${asset.filename}.${process.pid}.${randomUUID()}.download`,
    );
    try {
      await downloadAssetToFile(asset, temporaryPath, { fetchImpl, signal });
      const verifyFinal = async () =>
        await verifyManagedBinary(finalPath, asset, {
          signal,
          probeVersionImpl,
          environment,
        });
      await publishVerifiedFile(temporaryPath, finalPath, verifyFinal);
      if (!(await verifyFinal())) {
        await removeExactFile(finalPath);
        throw new Error("The cached yt-dlp executable was invalid.");
      }
      return finalPath;
    } finally {
      await removeExactFile(temporaryPath);
    }
  })();
  INSTALLS.set(finalPath, install);
  try {
    return await install;
  } finally {
    INSTALLS.delete(finalPath);
  }
}

export async function resolveYtDlp({
  allowDownload = false,
  signal,
  platform = process.platform,
  arch = process.arch,
  libc,
  environment = process.env,
  homeDirectory = os.homedir(),
  cacheDirectory,
  fetchImpl = fetch,
  probeVersionImpl = probeYtDlpVersion,
} = {}) {
  const systemVersion = await probeVersionImpl("yt-dlp", {
    signal,
    environment,
  });
  if (systemVersion !== undefined && isAcceptedYtDlpVersion(systemVersion)) {
    return "yt-dlp";
  }
  if (signal?.aborted) {
    throw new Error("The transcription timed out or was interrupted.");
  }
  const asset = selectYtDlpAsset({ platform, arch, libc });
  const targetDirectory =
    cacheDirectory ??
    ytDlpCacheDirectory({ platform, environment, homeDirectory });
  const managedPath = path.join(targetDirectory, asset.filename);
  if (
    await verifyManagedBinary(managedPath, asset, {
      signal,
      probeVersionImpl,
      environment,
    })
  ) {
    return managedPath;
  }
  if (!allowDownload) {
    throw new Error(
      `yt-dlp is unavailable and no tool was downloaded. After the user explicitly approves downloading the pinned official yt-dlp ${YT_DLP_VERSION} release to ${targetDirectory}, rerun with --allow-tool-download. Alternatively, install it manually from ${MANUAL_INSTALL_URL}`,
    );
  }
  try {
    return await installYtDlpAsset(asset, {
      cacheDirectory: targetDirectory,
      signal,
      fetchImpl,
      probeVersionImpl,
      environment,
    });
  } catch {
    throw new Error(
      `yt-dlp is unavailable. Install it manually from ${MANUAL_INSTALL_URL}`,
    );
  }
}
