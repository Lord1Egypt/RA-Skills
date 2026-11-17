import { spawn } from "node:child_process";
import { lookup as dnsLookup } from "node:dns/promises";
import {
  chmod,
  mkdir,
  mkdtemp,
  readFile,
  readdir,
  rm,
  stat,
} from "node:fs/promises";
import { BlockList, isIP } from "node:net";
import os from "node:os";
import path from "node:path";
import { resolveYtDlp } from "./yt-dlp.mjs";

const MAXIMUM_MEDIA_BYTES = 512 * 1024 * 1024;
const MAXIMUM_METADATA_BYTES = 4 * 1024 * 1024;
const MAXIMUM_STDERR_BYTES = 512 * 1024;
const MAXIMUM_SUBTITLE_BYTES = 8 * 1024 * 1024;
const SUPPORTED_MEDIA_EXTENSIONS = new Set([
  "flac",
  "m4a",
  "mp3",
  "mp4",
  "mpeg",
  "ogg",
  "wav",
  "webm",
]);
const SUBTITLE_FORMATS = new Set(["json3", "srt", "ttml", "vtt"]);
const AUTHENTICATED_AVAILABILITY = new Set([
  "needs_auth",
  "needs_subscription",
  "premium_only",
  "private",
  "subscriber_only",
]);
const LIVE_STATUSES = new Set(["is_live", "is_upcoming", "post_live"]);
const XIAOYUZHOU_HOSTS = new Set(["www.xiaoyuzhoufm.com", "xiaoyuzhoufm.com"]);
const XIAOYUZHOU_EPISODE_PATH = /^\/episode\/[0-9a-f]{24}\/?$/iu;
export const REMOTE_ASR_CONSENT_MESSAGE =
  "Remote ASR consent is required. No media was uploaded. After the user explicitly agrees to send this media over HTTPS to AudioFlow at https://asr.audioflow123.com and to a signed HTTPS object-storage URL for transcription, rerun with --allow-remote-asr. AudioFlow deletes the uploaded media as soon as transcription reaches a terminal state, before returning that result. If immediate best-effort deletion is interrupted, the private storage bucket's mandatory lifecycle removes the object within 2–3 days.";
const MEDIA_FORMAT_SELECTOR = [
  "bestaudio[ext=m4a]",
  "bestaudio[ext=webm]",
  "bestaudio[ext=mp3]",
  "bestaudio[ext=mpeg]",
  "bestaudio[ext=ogg]",
  "bestaudio[ext=flac]",
  "bestaudio[ext=wav]",
  "best[ext=m4a]",
  "best[ext=mp3]",
  "best[ext=mpeg]",
  "best[ext=ogg]",
  "best[ext=flac]",
  "best[ext=wav]",
  "best[ext=mp4]",
  "best[ext=webm]",
].join("/");

const PRIVATE_ADDRESSES = new BlockList();
for (const [network, prefix] of [
  ["0.0.0.0", 8],
  ["10.0.0.0", 8],
  ["100.64.0.0", 10],
  ["127.0.0.0", 8],
  ["169.254.0.0", 16],
  ["172.16.0.0", 12],
  ["192.0.0.0", 24],
  ["192.0.2.0", 24],
  ["192.168.0.0", 16],
  ["198.18.0.0", 15],
  ["198.51.100.0", 24],
  ["203.0.113.0", 24],
  ["224.0.0.0", 4],
  ["240.0.0.0", 4],
]) {
  PRIVATE_ADDRESSES.addSubnet(network, prefix, "ipv4");
}
for (const [network, prefix] of [
  ["::", 128],
  ["::1", 128],
  ["100::", 64],
  ["2001:db8::", 32],
  ["fc00::", 7],
  ["fe80::", 10],
  ["ff00::", 8],
]) {
  PRIVATE_ADDRESSES.addSubnet(network, prefix, "ipv6");
}

function asObject(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? value
    : {};
}

export function validateVideoUrl(source) {
  let url;
  try {
    url = new URL(source);
  } catch {
    throw new Error("The media URL is invalid.");
  }
  const hostname = url.hostname.toLowerCase();
  if (
    url.protocol !== "https:" ||
    url.port !== "" ||
    url.username !== "" ||
    url.password !== "" ||
    url.hash !== "" ||
    hostname === "localhost" ||
    hostname.endsWith(".localhost") ||
    hostname.endsWith(".local") ||
    hostname.endsWith(".internal") ||
    isIP(hostname.replace(/^\[|\]$/gu, "")) !== 0
  ) {
    throw new Error("A public HTTPS single-media URL is required.");
  }
  if (
    XIAOYUZHOU_HOSTS.has(hostname) &&
    !XIAOYUZHOU_EPISODE_PATH.test(url.pathname)
  ) {
    throw new Error("A public Xiaoyuzhou episode URL is required.");
  }
  return url;
}

function isPublicAddress(address, family) {
  const type = family === 6 || family === "IPv6" ? "ipv6" : "ipv4";
  return !PRIVATE_ADDRESSES.check(address, type);
}

async function assertPublicHostname(url, lookupImpl, signal) {
  if (signal?.aborted) {
    throw new Error("The transcription timed out or was interrupted.");
  }
  let addresses;
  try {
    addresses = await lookupImpl(url.hostname, { all: true, verbatim: true });
  } catch {
    throw new Error("The media host could not be verified.");
  }
  if (
    addresses.length === 0 ||
    addresses.some(({ address, family }) => !isPublicAddress(address, family))
  ) {
    throw new Error("The media host did not resolve to public addresses.");
  }
  if (signal?.aborted) {
    throw new Error("The transcription timed out or was interrupted.");
  }
}

function sanitizedEnvironment(environment) {
  const result = { ...environment };
  delete result.AUDIOFLOW_TOKEN;
  return result;
}

function baseYtDlpArguments() {
  return [
    "--ignore-config",
    "--no-config-locations",
    "--no-plugin-dirs",
    "--no-cookies",
    "--no-playlist",
    "--no-cache-dir",
    "--no-remote-components",
    "--no-js-runtimes",
    "--js-runtimes",
    `node:${process.execPath}`,
    "--no-mark-watched",
    "--abort-on-error",
    "--no-warnings",
    "--no-progress",
    "--color",
    "never",
    "--socket-timeout",
    "30",
    "--retries",
    "3",
    "--fragment-retries",
    "3",
  ];
}

export async function runYtDlp(
  executable,
  argumentsList,
  {
    signal,
    maximumStdoutBytes = MAXIMUM_METADATA_BYTES,
    environment = process.env,
    spawnImpl = spawn,
  } = {},
) {
  return await new Promise((resolve, reject) => {
    let child;
    let settled = false;
    let stderrBytes = 0;
    const stdout = [];
    let stdoutBytes = 0;
    const finish = (error, value) => {
      if (settled) return;
      settled = true;
      signal?.removeEventListener("abort", abort);
      if (error === undefined) resolve(value);
      else reject(error);
    };
    const abort = () => {
      child?.kill("SIGKILL");
      finish(
        new Error(
          signal?.aborted
            ? "The transcription timed out or was interrupted."
            : "The media downloader output was too large.",
        ),
      );
    };
    try {
      child = spawnImpl(executable, argumentsList, {
        env: sanitizedEnvironment(environment),
        shell: false,
        stdio: ["ignore", "pipe", "pipe"],
        windowsHide: true,
      });
    } catch {
      finish(new Error("The media downloader could not be started."));
      return;
    }
    signal?.addEventListener("abort", abort, { once: true });
    child.stdout?.on("data", (chunk) => {
      stdoutBytes += chunk.byteLength;
      if (stdoutBytes > maximumStdoutBytes) {
        abort();
        return;
      }
      stdout.push(Buffer.from(chunk));
    });
    child.stderr?.on("data", (chunk) => {
      stderrBytes += chunk.byteLength;
      if (stderrBytes > MAXIMUM_STDERR_BYTES) abort();
    });
    child.once("error", () => {
      finish(new Error("The media downloader could not be started."));
    });
    child.once("close", (code) => {
      if (code !== 0) {
        finish(new Error("The public media page could not be processed."));
        return;
      }
      finish(undefined, Buffer.concat(stdout).toString("utf8"));
    });
    if (signal?.aborted) abort();
  });
}

function parseMetadata(text) {
  let value;
  try {
    value = JSON.parse(text);
  } catch {
    throw new Error("The media site returned invalid metadata.");
  }
  const metadata = asObject(value);
  if (Object.keys(metadata).length === 0) {
    throw new Error("The media site returned invalid metadata.");
  }
  if (metadata._type === "playlist" || Array.isArray(metadata.entries)) {
    throw new Error("Media playlists are not supported.");
  }
  if (
    metadata.is_live === true ||
    LIVE_STATUSES.has(String(metadata.live_status ?? "").toLowerCase())
  ) {
    throw new Error("Live and upcoming media are not supported.");
  }
  if (
    AUTHENTICATED_AVAILABILITY.has(
      String(metadata.availability ?? "").toLowerCase(),
    )
  ) {
    throw new Error("Media that require login or payment are not supported.");
  }
  const formats = Array.isArray(metadata.formats) ? metadata.formats : [];
  if (
    metadata.has_drm === true ||
    metadata._has_drm === true ||
    (formats.length > 0 &&
      formats.every((format) => asObject(format).has_drm === true))
  ) {
    throw new Error("DRM-protected media are not supported.");
  }
  return metadata;
}

function ignoredSubtitleLanguage(language) {
  return /^(?:comments?|danmaku|live[_-]?chat)$/iu.test(language);
}

function subtitleLanguages(value) {
  return Object.entries(asObject(value))
    .filter(
      ([language, tracks]) =>
        !ignoredSubtitleLanguage(language) &&
        Array.isArray(tracks) &&
        tracks.length > 0,
    )
    .map(([language]) => language);
}

function normalizedLanguage(language) {
  return language
    .trim()
    .replaceAll("_", "-")
    .replace(/-orig$/iu, "")
    .toLowerCase();
}

function chooseLanguage(languages, desiredLanguage) {
  if (!desiredLanguage)
    return languages.length === 1 ? languages[0] : undefined;
  const desired = normalizedLanguage(desiredLanguage);
  const exact = languages.filter(
    (language) => normalizedLanguage(language) === desired,
  );
  if (exact.length === 1) return exact[0];
  const desiredBase = desired.split("-")[0];
  const baseMatches = languages.filter(
    (language) => normalizedLanguage(language).split("-")[0] === desiredBase,
  );
  return baseMatches.length === 1 ? baseMatches[0] : undefined;
}

export function selectSubtitleTrack(metadata, requestedLanguage) {
  const manualLanguages = subtitleLanguages(metadata.subtitles);
  const automaticLanguages = subtitleLanguages(metadata.automatic_captions);
  const originalAutomatic = automaticLanguages.filter((language) =>
    /-orig$/iu.test(language),
  );
  const eligibleAutomatic =
    originalAutomatic.length > 0 ? originalAutomatic : automaticLanguages;

  const requested = requestedLanguage?.trim();
  const webpageLanguage =
    typeof metadata.language === "string" ? metadata.language.trim() : "";
  const languagePreferences = [requested, webpageLanguage]
    .filter(Boolean)
    .filter(
      (language, index, languages) =>
        languages.findIndex(
          (candidate) =>
            normalizedLanguage(candidate) === normalizedLanguage(language),
        ) === index,
    );

  for (const desiredLanguage of languagePreferences) {
    const manualLanguage = chooseLanguage(manualLanguages, desiredLanguage);
    if (manualLanguage !== undefined) {
      return Object.freeze({ source: "manual", language: manualLanguage });
    }
    const automaticLanguage = chooseLanguage(
      eligibleAutomatic,
      desiredLanguage,
    );
    if (automaticLanguage !== undefined) {
      return Object.freeze({
        source: "automatic",
        language: automaticLanguage,
      });
    }
  }

  if (manualLanguages.length === 1) {
    return Object.freeze({ source: "manual", language: manualLanguages[0] });
  }
  if (eligibleAutomatic.length === 1) {
    return Object.freeze({
      source: "automatic",
      language: eligibleAutomatic[0],
    });
  }
  return undefined;
}

function decodeEntities(value) {
  const named = new Map([
    ["amp", "&"],
    ["apos", "'"],
    ["gt", ">"],
    ["lt", "<"],
    ["nbsp", " "],
    ["quot", '"'],
  ]);
  return value.replace(
    /&(?:#(\d+)|#x([0-9a-f]+)|([a-z]+));/giu,
    (match, decimal, hexadecimal, name) => {
      if (decimal !== undefined) return String.fromCodePoint(Number(decimal));
      if (hexadecimal !== undefined) {
        return String.fromCodePoint(Number.parseInt(hexadecimal, 16));
      }
      return named.get(name.toLowerCase()) ?? match;
    },
  );
}

function cleanCueText(value) {
  return decodeEntities(
    value
      .replace(/<br\s*\/?>/giu, "\n")
      .replace(/<[^>]+>/gu, "")
      .replace(/\{\\[^}]+\}/gu, "")
      .replaceAll("\u200b", ""),
  )
    .split(/\r?\n/u)
    .map((line) => line.trim())
    .filter(Boolean);
}

function appendDistinct(lines, candidate) {
  for (const line of candidate) {
    if (lines.at(-1) !== line) lines.push(line);
  }
}

function timedSubtitleText(value) {
  const input = value.replace(/^\uFEFF/u, "").split(/\r?\n/u);
  const output = [];
  let skipBlock = false;
  for (let index = 0; index < input.length; index += 1) {
    const line = input[index].trim();
    if (line === "") {
      skipBlock = false;
      continue;
    }
    if (/^(?:NOTE|REGION|STYLE)(?:\s|$)/u.test(line)) {
      skipBlock = true;
      continue;
    }
    if (skipBlock || /^WEBVTT(?:\s|$)/u.test(line)) continue;
    if (/^X-TIMESTAMP-MAP=/u.test(line)) continue;
    if (/^\d+$/u.test(line) && /-->/u.test(input[index + 1] ?? "")) {
      continue;
    }
    if (/-->/u.test(line)) continue;
    appendDistinct(output, cleanCueText(line));
  }
  return output.join("\n");
}

function json3SubtitleText(value) {
  let body;
  try {
    body = JSON.parse(value);
  } catch {
    throw new Error("The downloaded subtitle was invalid.");
  }
  const output = [];
  for (const event of Array.isArray(body.events) ? body.events : []) {
    const text = (Array.isArray(event.segs) ? event.segs : [])
      .map((segment) => (typeof segment.utf8 === "string" ? segment.utf8 : ""))
      .join("");
    appendDistinct(output, cleanCueText(text));
  }
  return output.join("\n");
}

function ttmlSubtitleText(value) {
  const output = [];
  const paragraphs = value.matchAll(/<p(?:\s[^>]*)?>([\s\S]*?)<\/p>/giu);
  for (const paragraph of paragraphs) {
    appendDistinct(output, cleanCueText(paragraph[1]));
  }
  return output.join("\n");
}

export function subtitleToText(value, extension) {
  if (Buffer.byteLength(value, "utf8") > MAXIMUM_SUBTITLE_BYTES) {
    throw new Error("The downloaded subtitle was too large.");
  }
  const normalizedExtension = extension.toLowerCase();
  const text =
    normalizedExtension === "json3"
      ? json3SubtitleText(value)
      : normalizedExtension === "ttml"
        ? ttmlSubtitleText(value)
        : timedSubtitleText(value);
  if (text.trim() === "") {
    throw new Error("The downloaded subtitle was empty.");
  }
  return text;
}

function exactLanguagePattern(language) {
  return `^(?:${language.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&")})$`;
}

async function regularFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isFile())
    .map((entry) => path.join(directory, entry.name));
}

async function downloadSubtitle(
  executable,
  url,
  track,
  directory,
  { signal, runYtDlpImpl, environment },
) {
  await mkdir(directory, { mode: 0o700 });
  const sourceOption =
    track.source === "manual" ? "--write-subs" : "--write-auto-subs";
  await runYtDlpImpl(
    executable,
    [
      ...baseYtDlpArguments(),
      "--skip-download",
      sourceOption,
      "--sub-langs",
      exactLanguagePattern(track.language),
      "--sub-format",
      "srt/vtt/ttml/json3/best",
      "--output",
      path.join(directory, "subtitle.%(ext)s"),
      "--",
      url.href,
    ],
    { signal, maximumStdoutBytes: 64 * 1024, environment },
  );
  const files = await regularFiles(directory);
  const candidates = files
    .map((filePath) => ({
      extension: path.extname(filePath).slice(1).toLowerCase(),
      filePath,
    }))
    .filter(({ extension }) => SUBTITLE_FORMATS.has(extension))
    .sort(
      (left, right) =>
        ["srt", "vtt", "ttml", "json3"].indexOf(left.extension) -
        ["srt", "vtt", "ttml", "json3"].indexOf(right.extension),
    );
  const candidate = candidates[0];
  if (candidate === undefined) {
    throw new Error("The selected subtitle could not be downloaded.");
  }
  const fileStat = await stat(candidate.filePath);
  if (fileStat.size <= 0 || fileStat.size > MAXIMUM_SUBTITLE_BYTES) {
    throw new Error("The downloaded subtitle was empty or too large.");
  }
  return subtitleToText(
    await readFile(candidate.filePath, "utf8"),
    candidate.extension,
  );
}

async function downloadMedia(
  executable,
  url,
  directory,
  { signal, runYtDlpImpl, environment },
) {
  await mkdir(directory, { mode: 0o700 });
  await runYtDlpImpl(
    executable,
    [
      ...baseYtDlpArguments(),
      "--format",
      MEDIA_FORMAT_SELECTOR,
      "--max-filesize",
      "512M",
      "--output",
      path.join(directory, "media.%(ext)s"),
      "--",
      url.href,
    ],
    { signal, maximumStdoutBytes: 64 * 1024, environment },
  );
  for (const filePath of await regularFiles(directory)) {
    const extension = path.extname(filePath).slice(1).toLowerCase();
    if (!SUPPORTED_MEDIA_EXTENSIONS.has(extension)) continue;
    const fileStat = await stat(filePath);
    if (
      fileStat.size > 0 &&
      Number.isSafeInteger(fileStat.size) &&
      fileStat.size <= MAXIMUM_MEDIA_BYTES
    ) {
      return filePath;
    }
  }
  throw new Error(
    "No AudioFlow-compatible media format was available. FFmpeg may add support; do not install it without the user's explicit approval.",
  );
}

async function inspectVideo(
  executable,
  url,
  { signal, runYtDlpImpl, environment },
) {
  const output = await runYtDlpImpl(
    executable,
    [
      ...baseYtDlpArguments(),
      "--skip-download",
      "--dump-single-json",
      "--extractor-args",
      "youtube:skip=translated_subs",
      "--",
      url.href,
    ],
    { signal, maximumStdoutBytes: MAXIMUM_METADATA_BYTES, environment },
  );
  return parseMetadata(output);
}

async function removeTemporaryDirectory(directory) {
  try {
    await rm(directory, { force: true, recursive: true });
  } catch {
    // Cleanup is best effort and must not encourage a paid ASR retry.
  }
}

export async function resolveRemoteInput({
  allowRemoteAsr = false,
  allowToolDownload = false,
  source,
  language,
  signal,
  progress = () => {},
  environment = process.env,
  lookupImpl = dnsLookup,
  resolveYtDlpImpl = resolveYtDlp,
  runYtDlpImpl = runYtDlp,
  temporaryBase = os.tmpdir(),
}) {
  const url = validateVideoUrl(source);
  const forceAudio = XIAOYUZHOU_HOSTS.has(url.hostname.toLowerCase());
  await assertPublicHostname(url, lookupImpl, signal);
  progress("Preparing the verified media downloader...\n");
  const executable = await resolveYtDlpImpl({
    allowDownload: allowToolDownload,
    signal,
    environment,
  });
  progress(
    forceAudio
      ? "Checking the Xiaoyuzhou episode media...\n"
      : "Checking the media page for existing subtitles...\n",
  );
  const metadata = await inspectVideo(executable, url, {
    signal,
    runYtDlpImpl,
    environment,
  });
  const temporaryDirectory = await mkdtemp(
    path.join(temporaryBase, "audioflow-remote-"),
  );
  await chmod(temporaryDirectory, 0o700);
  let retained = false;
  try {
    const track = forceAudio
      ? undefined
      : selectSubtitleTrack(metadata, language);
    if (track !== undefined) {
      try {
        const text = await downloadSubtitle(
          executable,
          url,
          track,
          path.join(temporaryDirectory, "subtitle"),
          { signal, runYtDlpImpl, environment },
        );
        progress("Using an existing subtitle; AudioFlow ASR was not called.\n");
        return Object.freeze({ kind: "subtitle", text });
      } catch (error) {
        if (signal?.aborted) throw error;
        progress(
          "The existing subtitle was unusable; remote ASR would be required.\n",
        );
      }
    }
    if (!allowRemoteAsr) {
      throw new Error(REMOTE_ASR_CONSENT_MESSAGE);
    }
    if (forceAudio) {
      progress("Downloading Xiaoyuzhou episode audio for transcription.\n");
    } else {
      progress(
        "No reliable original-language subtitle was found; downloading compatible media.\n",
      );
    }
    const filePath = await downloadMedia(
      executable,
      url,
      path.join(temporaryDirectory, "media"),
      { signal, runYtDlpImpl, environment },
    );
    retained = true;
    let cleaned = false;
    return Object.freeze({
      kind: "media",
      filePath,
      cleanup: async () => {
        if (cleaned) return;
        cleaned = true;
        await removeTemporaryDirectory(temporaryDirectory);
      },
    });
  } finally {
    if (!retained) {
      await removeTemporaryDirectory(temporaryDirectory);
    }
  }
}
