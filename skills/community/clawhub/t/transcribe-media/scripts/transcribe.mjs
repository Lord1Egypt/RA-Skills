#!/usr/bin/env node

import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { mkdtemp, rm, stat } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { Readable } from "node:stream";
import { setTimeout as delay } from "node:timers/promises";
import { pathToFileURL } from "node:url";
import {
  REMOTE_ASR_CONSENT_MESSAGE,
  resolveRemoteInput,
} from "./remote-media.mjs";
import { loadAudioflowToken } from "./credentials.mjs";

const MAXIMUM_FILE_BYTES = 512 * 1024 * 1024;
const MAXIMUM_RESPONSE_BYTES = 1024 * 1024;
const MAXIMUM_SIGNATURE_BATCH = 32;
const MAXIMUM_FFMPEG_STDERR_BYTES = 8 * 1024;
const CLEANUP_TIMEOUT_MS = 10_000;
const DEFAULT_POLL_INTERVAL_MS = 2_000;
const DEFAULT_TIMEOUT_MS = 30 * 60 * 1_000;
const AUDIOFLOW_BASE_URL = "https://asr.audioflow123.com";
const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/iu;
const RUNNING_STATES = new Set([
  "queued",
  "validating",
  "resolving",
  "downloading",
  "transcoding",
  "submitting",
  "processing",
  "running",
]);
const CONTENT_TYPES = Object.freeze({
  flac: "audio/flac",
  m4a: "audio/mp4",
  mp3: "audio/mpeg",
  mp4: "audio/mp4",
  mpeg: "audio/mpeg",
  ogg: "audio/ogg",
  wav: "audio/wav",
  webm: "audio/webm",
});
const VIDEO_FILE_EXTENSIONS = Object.freeze(new Set(["mp4", "mpeg", "webm"]));
const FFMPEG_INSTALL_MESSAGE =
  "Local video extraction requires FFmpeg. Install FFmpeg and retry.";

function printHelp() {
  process.stdout.write(
    `AudioFlow speech-to-text\n\nUsage:\n  node transcribe.mjs --file <path> [options]\n  node transcribe.mjs --url <https-url> [options]\n\nOptions:\n  --file <path>               Local FLAC, M4A, MP3, MP4, MPEG, OGG, WAV, or WebM file\n  --url <https-url>           Public single-video or podcast-episode URL supported by yt-dlp\n  --language <code>           Preferred source language, for example zh or en\n  --model <name>              ASR model (default: gpt-4o-transcribe-diarize)\n  --provider <name>           auto, qianwen, or bigasr (default: auto)\n  --poll-interval-ms <number> Poll interval (default: 2000)\n  --timeout-ms <number>       Overall timeout (default: 1800000)\n  --allow-remote-asr          Confirm explicit approval for this run's remote media upload\n  --allow-tool-download       Confirm explicit approval to cache the pinned yt-dlp release\n  --help                      Show this help\n`,
  );
}

function parsePositiveInteger(value, name) {
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    throw new Error(`${name} must be a positive integer.`);
  }
  return parsed;
}

function mediaFileExtension(filePath) {
  return path.extname(path.basename(filePath)).slice(1).toLowerCase();
}

async function extractAudioWithFfmpeg(
  filePath,
  { signal, spawnImpl = spawn } = {},
) {
  const temporaryDirectory = await mkdtemp(
    path.join(os.tmpdir(), "audioflow-video-audio-"),
  );
  const outputFilePath = path.join(temporaryDirectory, "media.mp3");
  let ffmpeg;
  let stderr = "";
  let stderrLength = 0;

  const cleanup = async () => {
    if (ffmpeg !== undefined && !ffmpeg.killed) ffmpeg.kill("SIGKILL");
    try {
      await rm(temporaryDirectory, { force: true, recursive: true });
    } catch {
      // Cleanup is best effort and must not replace conversion details.
    }
  };

  const waitForConversion = () =>
    new Promise((resolve, reject) => {
      if (ffmpeg === undefined) {
        reject(new Error("FFmpeg failed to start."));
        return;
      }
      if (signal?.aborted) {
        reject(new Error("The transcription timed out or was interrupted."));
        return;
      }
      const abort = () => {
        ffmpeg.kill("SIGKILL");
        reject(new Error("The transcription timed out or was interrupted."));
      };
      signal?.addEventListener("abort", abort, { once: true });
      ffmpeg.stderr?.on("data", (chunk) => {
        if (stderrLength + chunk.byteLength <= MAXIMUM_FFMPEG_STDERR_BYTES) {
          stderr += chunk.toString();
        }
        stderrLength += chunk.byteLength;
      });
      ffmpeg.once("close", (code) => {
        signal?.removeEventListener("abort", abort);
        if (code === 0) {
          resolve();
          return;
        }
        reject(
          new Error(
            `FFmpeg failed to extract audio from the local video file.${stderr === "" ? "" : ` ${stderr.trim()}`}`,
          ),
        );
      });
      ffmpeg.once("error", (error) => {
        signal?.removeEventListener("abort", abort);
        reject(error);
      });
    });

  try {
    ffmpeg = spawnImpl(
      "ffmpeg",
      [
        "-y",
        "-i",
        filePath,
        "-vn",
        "-ac",
        "1",
        "-codec:a",
        "libmp3lame",
        "-ar",
        "16000",
        "-f",
        "mp3",
        outputFilePath,
      ],
      {
        shell: false,
        windowsHide: true,
        stdio: ["ignore", "ignore", "pipe"],
      },
    );
    await waitForConversion();
    return Object.freeze({
      filePath: outputFilePath,
      cleanup,
    });
  } catch (error) {
    await cleanup();
    if (error instanceof Error && error.code === "ENOENT") {
      throw new Error(FFMPEG_INSTALL_MESSAGE);
    }
    throw error;
  }
}

async function prepareLocalMedia(
  filePath,
  { signal, extractAudioWithFfmpegImpl = extractAudioWithFfmpeg } = {},
) {
  if (!VIDEO_FILE_EXTENSIONS.has(mediaFileExtension(filePath))) {
    return Object.freeze({
      filePath,
      cleanup: async () => {},
    });
  }
  try {
    return await extractAudioWithFfmpegImpl(filePath, { signal });
  } catch (error) {
    if (error instanceof Error && error.code === "ENOENT") {
      throw new Error(FFMPEG_INSTALL_MESSAGE);
    }
    throw error;
  }
}

export function parseArguments(argumentsList) {
  if (argumentsList.includes("--help") || argumentsList.includes("-h")) {
    return { help: true };
  }
  const valueOptions = new Set([
    "--file",
    "--url",
    "--language",
    "--model",
    "--provider",
    "--poll-interval-ms",
    "--timeout-ms",
  ]);
  const booleanOptions = new Set([
    "--allow-remote-asr",
    "--allow-tool-download",
  ]);
  const values = {};
  for (let index = 0; index < argumentsList.length; index += 1) {
    const name = argumentsList[index];
    if (booleanOptions.has(name)) {
      if (values[name] !== undefined) {
        throw new Error(`Duplicate command argument: ${name}.`);
      }
      values[name] = true;
      continue;
    }
    const value = argumentsList[index + 1];
    if (
      name === undefined ||
      value === undefined ||
      !valueOptions.has(name) ||
      value.startsWith("--")
    ) {
      throw new Error("Unknown or incomplete command argument.");
    }
    if (values[name] !== undefined) {
      throw new Error(`Duplicate command argument: ${name}.`);
    }
    values[name] = value;
    index += 1;
  }
  const rawFilePath = values["--file"]?.trim();
  const sourceUrl = values["--url"]?.trim();
  if ((rawFilePath ? 1 : 0) + (sourceUrl ? 1 : 0) !== 1) {
    throw new Error("Exactly one of --file or --url is required.");
  }
  const provider = values["--provider"] ?? "auto";
  if (!new Set(["auto", "qianwen", "bigasr"]).has(provider)) {
    throw new Error("--provider must be auto, qianwen, or bigasr.");
  }
  const model = values["--model"]?.trim() || "gpt-4o-transcribe-diarize";
  if (!/^[A-Za-z0-9._-]{1,128}$/u.test(model)) {
    throw new Error("--model is invalid.");
  }
  const language = values["--language"]?.trim();
  if (
    language !== undefined &&
    !/^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})?$/u.test(language)
  ) {
    throw new Error("--language is invalid.");
  }
  return Object.freeze({
    help: false,
    ...(rawFilePath ? { filePath: path.resolve(rawFilePath) } : { sourceUrl }),
    provider,
    model,
    allowRemoteAsr: values["--allow-remote-asr"] === true,
    allowToolDownload: values["--allow-tool-download"] === true,
    ...(language === undefined ? {} : { language }),
    pollIntervalMs: parsePositiveInteger(
      values["--poll-interval-ms"] ?? DEFAULT_POLL_INTERVAL_MS,
      "--poll-interval-ms",
    ),
    timeoutMs: parsePositiveInteger(
      values["--timeout-ms"] ?? DEFAULT_TIMEOUT_MS,
      "--timeout-ms",
    ),
  });
}

export async function loadConfiguration({
  loadAudioflowTokenImpl = loadAudioflowToken,
} = {}) {
  const credential = await loadAudioflowTokenImpl();
  if (credential === null) {
    throw new Error(
      "AudioFlow authorization is required. Run auth.mjs begin, approve the browser request, then run auth.mjs wait.",
    );
  }
  return Object.freeze({
    token: credential.token,
    baseUrl: AUDIOFLOW_BASE_URL,
  });
}

export async function inspectMedia(filePath) {
  let fileStat;
  try {
    fileStat = await stat(filePath);
  } catch {
    throw new Error("The media file cannot be read.");
  }
  const filename = path.basename(filePath);
  const extension = path.extname(filename).slice(1).toLowerCase();
  const contentType = CONTENT_TYPES[extension];
  if (!fileStat.isFile() || fileStat.size <= 0 || contentType === undefined) {
    throw new Error("The media file type is unsupported or the file is empty.");
  }
  if (
    !Number.isSafeInteger(fileStat.size) ||
    fileStat.size > MAXIMUM_FILE_BYTES
  ) {
    throw new Error("The media file exceeds the 512 MiB limit.");
  }
  return Object.freeze({
    filePath,
    filename,
    contentType,
    sizeBytes: fileStat.size,
  });
}

function asRecord(value) {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Error("The AudioFlow API returned an invalid response.");
  }
  return value;
}

async function readJson(response) {
  const contentLength = Number(response.headers.get("content-length"));
  if (
    Number.isFinite(contentLength) &&
    contentLength > MAXIMUM_RESPONSE_BYTES
  ) {
    throw new Error("The AudioFlow API response was too large.");
  }
  const text = await response.text();
  if (Buffer.byteLength(text, "utf8") > MAXIMUM_RESPONSE_BYTES) {
    throw new Error("The AudioFlow API response was too large.");
  }
  try {
    return asRecord(JSON.parse(text));
  } catch {
    throw new Error("The AudioFlow API returned invalid JSON.");
  }
}

function safeErrorCode(body) {
  try {
    const error = asRecord(body.error);
    return typeof error.code === "string" &&
      /^[a-z0-9_]{1,64}$/u.test(error.code)
      ? ` (${error.code})`
      : "";
  } catch {
    return "";
  }
}

async function requestBackend(
  configuration,
  pathname,
  init,
  expectedStatuses,
  signal,
) {
  const headers = new Headers(init.headers);
  headers.set("Authorization", `Bearer ${configuration.token}`);
  if (init.body !== undefined) headers.set("Content-Type", "application/json");
  let response;
  try {
    response = await fetch(new URL(pathname, configuration.baseUrl), {
      ...init,
      headers,
      redirect: "error",
      signal,
    });
  } catch {
    throw new Error("The AudioFlow API request failed.");
  }
  if (!expectedStatuses.includes(response.status)) {
    let code = "";
    try {
      code = safeErrorCode(await readJson(response));
    } catch {
      // The HTTP status remains sufficient and arbitrary response data stays private.
    }
    if (response.status === 401) {
      throw new Error(
        "AudioFlow authorization is invalid or expired. Start a new browser authorization request.",
      );
    }
    if (response.status === 402) {
      throw new Error(
        "AudioFlow prepaid balance or API key spending limit is insufficient. Add credit or update the key limit in the AudioFlow dashboard.",
      );
    }
    throw new Error(
      `The AudioFlow API returned HTTP ${response.status}${code}.`,
    );
  }
  return response.status === 204 ? undefined : await readJson(response);
}

function parseSignedRequest(value) {
  const request = asRecord(value);
  const rawHeaders = asRecord(request.headers);
  if (
    request.method !== "PUT" ||
    typeof request.url !== "string" ||
    !Number.isSafeInteger(request.content_length) ||
    request.content_length <= 0
  ) {
    throw new Error("The upload signature response is invalid.");
  }
  const headers = {};
  for (const [name, value] of Object.entries(rawHeaders)) {
    if (
      (typeof value !== "string" && typeof value !== "number") ||
      name.toLowerCase() === "authorization"
    ) {
      throw new Error("The upload signature response is invalid.");
    }
    headers[name] = String(value);
  }
  const partNumber = request.part_number;
  if (
    partNumber !== undefined &&
    (!Number.isSafeInteger(partNumber) || partNumber <= 0)
  ) {
    throw new Error("The upload signature response is invalid.");
  }
  return Object.freeze({
    url: request.url,
    contentLength: request.content_length,
    headers: Object.freeze(headers),
    ...(partNumber === undefined ? {} : { partNumber }),
  });
}

function parseSession(value) {
  const session = asRecord(value);
  if (
    typeof session.id !== "string" ||
    !UUID_PATTERN.test(session.id) ||
    session.object !== "audio.upload" ||
    (session.mode !== "single" && session.mode !== "multipart") ||
    !Number.isSafeInteger(session.size_bytes) ||
    session.size_bytes <= 0
  ) {
    throw new Error("The upload session response is invalid.");
  }
  if (
    session.mode === "multipart" &&
    (!Number.isSafeInteger(session.part_size_bytes) ||
      session.part_size_bytes <= 0 ||
      !Number.isSafeInteger(session.part_count) ||
      session.part_count <= 0)
  ) {
    throw new Error("The upload session response is invalid.");
  }
  return Object.freeze({
    id: session.id,
    mode: session.mode,
    sizeBytes: session.size_bytes,
    ...(session.mode === "multipart"
      ? {
          partSizeBytes: session.part_size_bytes,
          partCount: session.part_count,
        }
      : {}),
  });
}

async function createUpload(configuration, media, signal) {
  const body = await requestBackend(
    configuration,
    "/v1/audio/uploads",
    {
      method: "POST",
      body: JSON.stringify({
        filename: media.filename,
        content_type: media.contentType,
        size_bytes: media.sizeBytes,
        mode: "auto",
      }),
    },
    [201],
    signal,
  );
  return parseSession(body);
}

async function refreshSignatures(configuration, uploadId, partNumbers, signal) {
  const body = asRecord(
    await requestBackend(
      configuration,
      `/v1/audio/uploads/${uploadId}/signatures`,
      {
        method: "POST",
        body: JSON.stringify(
          partNumbers === undefined ? {} : { part_numbers: partNumbers },
        ),
      },
      [200],
      signal,
    ),
  );
  if (
    body.id !== uploadId ||
    body.object !== "audio.upload.signatures" ||
    !Array.isArray(body.requests)
  ) {
    throw new Error("The upload signature response is invalid.");
  }
  return body.requests.map(parseSignedRequest);
}

async function getUpload(configuration, uploadId, signal) {
  return asRecord(
    await requestBackend(
      configuration,
      `/v1/audio/uploads/${uploadId}`,
      { method: "GET" },
      [200],
      signal,
    ),
  );
}

async function putFileRange(configuration, request, media, startByte, signal) {
  let signedUrl;
  try {
    signedUrl = new URL(request.url);
  } catch {
    throw new Error("The upload signature response is invalid.");
  }
  if (
    signedUrl.protocol !== "https:" ||
    signedUrl.origin === configuration.baseUrl ||
    signedUrl.username !== "" ||
    signedUrl.password !== "" ||
    signedUrl.hash !== "" ||
    !Number.isSafeInteger(startByte) ||
    startByte < 0 ||
    startByte + request.contentLength > media.sizeBytes
  ) {
    throw new Error("The signed upload target is invalid.");
  }
  const headers = new Headers(request.headers);
  headers.set("Content-Length", String(request.contentLength));
  const fileStream = createReadStream(media.filePath, {
    start: startByte,
    end: startByte + request.contentLength - 1,
  });
  try {
    const response = await fetch(signedUrl, {
      method: "PUT",
      headers,
      body: Readable.toWeb(fileStream),
      duplex: "half",
      redirect: "error",
      signal,
    });
    if (!response.ok) throw new Error(`OSS returned HTTP ${response.status}.`);
    await response.body?.cancel();
  } catch (error) {
    fileStream.destroy();
    if (
      error instanceof Error &&
      /^OSS returned HTTP [0-9]{3}\.$/u.test(error.message)
    )
      throw error;
    throw new Error("The direct OSS upload failed.");
  } finally {
    fileStream.destroy();
  }
}

async function uploadMultipart(configuration, session, media, signal) {
  const state = asRecord(await getUpload(configuration, session.id, signal));
  if (!Array.isArray(state.missing_parts))
    throw new Error("The multipart upload state is invalid.");
  const missingParts = [...state.missing_parts];
  if (
    missingParts.some(
      (partNumber) =>
        !Number.isSafeInteger(partNumber) ||
        partNumber < 1 ||
        partNumber > session.partCount,
    )
  ) {
    throw new Error("The multipart upload state is invalid.");
  }
  for (
    let batchStart = 0;
    batchStart < missingParts.length;
    batchStart += MAXIMUM_SIGNATURE_BATCH
  ) {
    const batch = missingParts.slice(
      batchStart,
      batchStart + MAXIMUM_SIGNATURE_BATCH,
    );
    const requests = await refreshSignatures(
      configuration,
      session.id,
      batch,
      signal,
    );
    const signedParts = new Map(
      requests.map((request) => [request.partNumber, request]),
    );
    if (signedParts.size !== batch.length)
      throw new Error("The multipart signature batch is invalid.");
    for (const partNumber of batch) {
      const request = signedParts.get(partNumber);
      const expectedLength =
        partNumber === session.partCount
          ? media.sizeBytes - session.partSizeBytes * (session.partCount - 1)
          : session.partSizeBytes;
      if (request === undefined || request.contentLength !== expectedLength) {
        throw new Error("The multipart signature batch is invalid.");
      }
      await putFileRange(
        configuration,
        request,
        media,
        (partNumber - 1) * session.partSizeBytes,
        signal,
      );
    }
  }
}

async function verifyUploaded(configuration, session, media, signal) {
  const state = asRecord(await getUpload(configuration, session.id, signal));
  if (session.mode === "single") {
    if (state.uploaded !== true)
      throw new Error("OSS did not confirm the uploaded file.");
    return;
  }
  if (
    !Array.isArray(state.missing_parts) ||
    !Array.isArray(state.uploaded_parts)
  ) {
    throw new Error("The multipart upload state is invalid.");
  }
  let uploadedBytes = 0;
  for (const value of state.uploaded_parts) {
    const part = asRecord(value);
    if (!Number.isSafeInteger(part.size_bytes) || part.size_bytes <= 0) {
      throw new Error("The multipart upload state is invalid.");
    }
    uploadedBytes += part.size_bytes;
  }
  if (state.missing_parts.length !== 0 || uploadedBytes !== media.sizeBytes) {
    throw new Error("OSS did not confirm every uploaded part.");
  }
}

async function submitTranscription(configuration, session, options, signal) {
  const body = asRecord(
    await requestBackend(
      configuration,
      "/v1/audio/transcriptions",
      {
        method: "POST",
        body: JSON.stringify({
          upload_id: session.id,
          model: options.model,
          provider: options.provider,
          response_format: "json",
          stream: false,
          ...(options.language === undefined
            ? {}
            : { language: options.language }),
        }),
      },
      [202],
      signal,
    ),
  );
  if (
    body.id !== session.id ||
    !UUID_PATTERN.test(body.id) ||
    typeof body.status !== "string"
  ) {
    throw new Error("The transcription task response is invalid.");
  }
  return body;
}

async function getTask(configuration, taskId, signal) {
  const body = asRecord(
    await requestBackend(
      configuration,
      `/v1/audio/transcriptions/${taskId}`,
      { method: "GET" },
      [200],
      signal,
    ),
  );
  if (
    body.id !== taskId ||
    !UUID_PATTERN.test(body.id) ||
    typeof body.status !== "string"
  ) {
    throw new Error("The transcription task response is invalid.");
  }
  return body;
}

function transcriptText(task) {
  if (typeof task.text === "string") return task.text;
  const result =
    typeof task.result === "object" &&
    task.result !== null &&
    !Array.isArray(task.result)
      ? task.result
      : {};
  return typeof result.text === "string" ? result.text : undefined;
}

async function cleanup(configuration, pathname, expectedStatuses) {
  try {
    await requestBackend(
      configuration,
      pathname,
      { method: "DELETE" },
      expectedStatuses,
      AbortSignal.timeout(CLEANUP_TIMEOUT_MS),
    );
  } catch {
    // Cleanup is best effort and must not replace the original failure.
  }
}

async function transcribe(options, configuration, media, signal) {
  let uploadId;
  let taskId;
  try {
    const health = asRecord(
      await requestBackend(
        configuration,
        "/healthz",
        { method: "GET" },
        [200],
        signal,
      ),
    );
    if (
      health.status !== "ok" ||
      health.ready !== true ||
      health.shutting_down !== false
    ) {
      throw new Error("The AudioFlow API is not ready.");
    }
    const session = await createUpload(configuration, media, signal);
    uploadId = session.id;
    if (session.sizeBytes !== media.sizeBytes)
      throw new Error("The upload session size does not match the file.");
    process.stderr.write("Uploading media directly to OSS...\n");
    if (session.mode === "single") {
      const requests = await refreshSignatures(
        configuration,
        session.id,
        undefined,
        signal,
      );
      if (
        requests.length !== 1 ||
        requests[0].contentLength !== media.sizeBytes
      ) {
        throw new Error("The single upload signature is invalid.");
      }
      await putFileRange(configuration, requests[0], media, 0, signal);
    } else {
      await uploadMultipart(configuration, session, media, signal);
    }
    await verifyUploaded(configuration, session, media, signal);
    const submitted = await submitTranscription(
      configuration,
      session,
      options,
      signal,
    );
    taskId = submitted.id;
    process.stderr.write("Waiting for transcription...\n");
    let task = submitted;
    while (RUNNING_STATES.has(task.status.toLowerCase())) {
      await delay(options.pollIntervalMs, undefined, { signal });
      task = await getTask(configuration, taskId, signal);
    }
    const text = transcriptText(task);
    if (
      task.status.toLowerCase() !== "succeeded" ||
      text === undefined ||
      text.trim() === ""
    ) {
      throw new Error("The transcription task did not succeed.");
    }
    return text;
  } catch (error) {
    if (taskId !== undefined) {
      await cleanup(configuration, `/v1/audio/transcriptions/${taskId}`, [200]);
    } else if (uploadId !== undefined) {
      await cleanup(configuration, `/v1/audio/uploads/${uploadId}`, [204]);
    }
    if (signal.aborted)
      throw new Error("The transcription timed out or was interrupted.");
    throw error;
  }
}

export async function execute(
  options,
  signal,
  {
    inspectMediaImpl = inspectMedia,
    loadConfigurationImpl = loadConfiguration,
    progress = (message) => process.stderr.write(message),
    resolveRemoteInputImpl = resolveRemoteInput,
    prepareLocalMediaImpl = prepareLocalMedia,
    extractAudioWithFfmpegImpl = extractAudioWithFfmpeg,
    transcribeImpl = transcribe,
  } = {},
) {
  if (options.sourceUrl === undefined) {
    if (!options.allowRemoteAsr) {
      throw new Error(REMOTE_ASR_CONSENT_MESSAGE);
    }
    const prepared = await prepareLocalMediaImpl(options.filePath, {
      signal,
      extractAudioWithFfmpegImpl,
    });
    try {
      const media = await inspectMediaImpl(prepared.filePath);
      return await transcribeImpl(
        options,
        await loadConfigurationImpl(),
        media,
        signal,
      );
    } finally {
      await prepared.cleanup();
    }
  }

  const remote = await resolveRemoteInputImpl({
    allowRemoteAsr: options.allowRemoteAsr,
    allowToolDownload: options.allowToolDownload,
    source: options.sourceUrl,
    language: options.language,
    signal,
    progress,
  });
  if (remote.kind === "subtitle") return remote.text;
  try {
    if (!options.allowRemoteAsr) {
      throw new Error(REMOTE_ASR_CONSENT_MESSAGE);
    }
    const media = await inspectMediaImpl(remote.filePath);
    return await transcribeImpl(
      options,
      await loadConfigurationImpl(),
      media,
      signal,
    );
  } finally {
    await remote.cleanup();
  }
}

export async function main(argumentsList = process.argv.slice(2)) {
  const options = parseArguments(argumentsList);
  if (options.help) {
    printHelp();
    return;
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs);
  const interrupt = () => controller.abort();
  process.once("SIGINT", interrupt);
  process.once("SIGTERM", interrupt);
  try {
    const text = await execute(options, controller.signal);
    process.stdout.write(text.endsWith("\n") ? text : `${text}\n`);
  } finally {
    clearTimeout(timeout);
    process.removeListener("SIGINT", interrupt);
    process.removeListener("SIGTERM", interrupt);
  }
}

const entrypoint = process.argv[1];
if (
  entrypoint !== undefined &&
  import.meta.url === pathToFileURL(path.resolve(entrypoint)).href
) {
  main().catch((error) => {
    process.stderr.write(
      `${error instanceof Error ? error.message : "Transcription failed."}\n`,
    );
    process.exitCode = 1;
  });
}
