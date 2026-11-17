#!/usr/bin/env node

import { randomUUID } from "node:crypto";
import { constants as fsConstants } from "node:fs";
import { lstat, mkdir, open, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { loadAudioflowToken } from "./credentials.mjs";

const API_ORIGIN = "https://asr.audioflow123.com";
const SPEECH_PATH = "/v1/audio/speech";
const MAXIMUM_TEXT_CHARACTERS = 4096;
const MAXIMUM_STDIN_BYTES = 64 * 1024;
const MAXIMUM_RESPONSE_BYTES = 64 * 1024;
const MAXIMUM_AUDIO_BYTES = 32 * 1024 * 1024;
const VOICE_BY_LANGUAGE = Object.freeze({
  zh: "longanlingxin",
  en: "longanlingxin",
});
const RESULT_HOSTS = new Set([
  "dashscope-result.oss-cn-beijing.aliyuncs.com",
  "dashscope-result-bj.oss-cn-beijing.aliyuncs.com",
]);

function printHelp() {
  process.stdout.write(
    "Read text aloud with AudioFlow TTS\n\n" +
      "Usage:\n" +
      "  printf 'Hello' | node read-aloud.mjs [--speed <0.5-2.0>] [--output </absolute/file.mp3>]\n\n" +
      "Text is read from standard input so it is not exposed in process arguments.\n",
  );
}

export function parseArguments(argumentsList) {
  const options = { speed: 1, outputPath: undefined };
  for (let index = 0; index < argumentsList.length; index += 2) {
    const name = argumentsList[index];
    const value = argumentsList[index + 1];
    if (
      value === undefined ||
      value.startsWith("--") ||
      (name !== "--speed" && name !== "--output")
    ) {
      throw new Error("Unknown or incomplete read-aloud argument.");
    }
    if (name === "--speed") {
      const speed = Number(value);
      if (!Number.isFinite(speed) || speed < 0.5 || speed > 2) {
        throw new Error("--speed must be a number between 0.5 and 2.0.");
      }
      options.speed = speed;
    } else {
      const outputPath = path.resolve(value);
      if (!path.isAbsolute(value) || path.extname(outputPath) !== ".mp3") {
        throw new Error("--output must be an absolute path ending in .mp3.");
      }
      options.outputPath = outputPath;
    }
  }
  return Object.freeze(options);
}

async function readStandardInput(input = process.stdin) {
  input.setEncoding("utf8");
  let text = "";
  for await (const chunk of input) {
    text += chunk;
    if (Buffer.byteLength(text, "utf8") > MAXIMUM_STDIN_BYTES) {
      throw new Error("The input text is too large.");
    }
  }
  return text;
}

function validateText(text) {
  if (typeof text !== "string" || text.trim().length === 0) {
    throw new Error("The input text must not be empty.");
  }
  if (Array.from(text).length > MAXIMUM_TEXT_CHARACTERS) {
    throw new Error(
      `The input text must not exceed ${MAXIMUM_TEXT_CHARACTERS} Unicode characters.`,
    );
  }
  return text;
}

async function readBoundedJson(response) {
  const text = await response.text();
  if (Buffer.byteLength(text, "utf8") > MAXIMUM_RESPONSE_BYTES) {
    throw new Error("The AudioFlow TTS response was too large.");
  }
  try {
    const value = JSON.parse(text);
    if (typeof value !== "object" || value === null || Array.isArray(value)) {
      throw new Error("invalid");
    }
    return value;
  } catch {
    throw new Error("The AudioFlow TTS response was invalid.");
  }
}

function safeErrorCode(body) {
  const code = body?.error?.code;
  return typeof code === "string" && /^[a-z_]{1,64}$/u.test(code)
    ? code
    : "request_failed";
}

function parseSpeechResponse(body) {
  if (
    body.object !== "audio.speech" ||
    body.format !== "mp3" ||
    (body.language !== "zh" && body.language !== "en") ||
    !Number.isSafeInteger(body.expires_at) ||
    body.expires_at <= Math.floor(Date.now() / 1000) ||
    !Number.isSafeInteger(body.usage?.characters) ||
    body.usage.characters <= 0 ||
    typeof body.url !== "string"
  ) {
    throw new Error("The AudioFlow TTS response was invalid.");
  }
  let audioUrl;
  try {
    audioUrl = new URL(body.url);
  } catch {
    throw new Error("The AudioFlow TTS response was invalid.");
  }
  if (
    audioUrl.protocol !== "https:" ||
    !RESULT_HOSTS.has(audioUrl.hostname) ||
    audioUrl.username !== "" ||
    audioUrl.password !== "" ||
    audioUrl.port !== "" ||
    audioUrl.hash !== ""
  ) {
    throw new Error("The AudioFlow TTS response was invalid.");
  }
  return Object.freeze({
    audioUrl,
    language: body.language,
    voice: VOICE_BY_LANGUAGE[body.language],
    characters: body.usage.characters,
    expiresAt: body.expires_at,
  });
}

function isMp3(bytes) {
  return (
    bytes.length >= 3 &&
    ((bytes[0] === 0x49 && bytes[1] === 0x44 && bytes[2] === 0x33) ||
      (bytes[0] === 0xff && (bytes[1] & 0xe0) === 0xe0))
  );
}

async function downloadAudio(fetchImpl, audioUrl, signal) {
  let response;
  try {
    response = await fetchImpl(audioUrl, {
      method: "GET",
      headers: { accept: "audio/mpeg" },
      redirect: "error",
      signal,
    });
  } catch {
    throw new Error("The synthesized audio download failed.");
  }
  if (response.status !== 200) {
    await response.body?.cancel();
    throw new Error("The synthesized audio download failed.");
  }
  const contentLengthHeader = response.headers.get("content-length");
  const contentLength = Number(contentLengthHeader);
  if (
    contentLengthHeader !== null &&
    Number.isFinite(contentLength) &&
    (contentLength <= 0 || contentLength > MAXIMUM_AUDIO_BYTES)
  ) {
    await response.body?.cancel();
    throw new Error("The synthesized audio was invalid.");
  }
  const bytes = new Uint8Array(await response.arrayBuffer());
  if (bytes.length === 0 || bytes.length > MAXIMUM_AUDIO_BYTES || !isMp3(bytes)) {
    throw new Error("The synthesized audio was invalid.");
  }
  return bytes;
}

async function defaultOutputPath() {
  const directory = path.join(os.tmpdir(), "read-aloud");
  await mkdir(directory, { recursive: true, mode: 0o700 });
  if (process.platform !== "win32") {
    const info = await lstat(directory);
    if (!info.isDirectory() || info.isSymbolicLink() || (info.mode & 0o077) !== 0) {
      throw new Error("The read-aloud output directory is not private.");
    }
  }
  return path.join(directory, `${randomUUID()}.mp3`);
}

async function writePrivateFile(outputPath, bytes) {
  const handle = await open(
    outputPath,
    fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_WRONLY,
    0o600,
  );
  let complete = false;
  try {
    await handle.writeFile(bytes);
    await handle.sync();
    complete = true;
  } finally {
    await handle.close();
    if (!complete) await rm(outputPath, { force: true });
  }
}

export async function synthesizeAndDownload(
  { text, speed = 1, outputPath },
  {
    fetchImpl = fetch,
    credentialOptions = {},
    requestSignal = AbortSignal.timeout(310_000),
    downloadSignal = AbortSignal.timeout(60_000),
  } = {},
) {
  const input = validateText(text);
  if (!Number.isFinite(speed) || speed < 0.5 || speed > 2) {
    throw new Error("speed must be a number between 0.5 and 2.0.");
  }
  if (outputPath !== undefined) {
    try {
      await lstat(outputPath);
      const error = new Error("The output file already exists.");
      error.code = "EEXIST";
      throw error;
    } catch (error) {
      if (!(error && typeof error === "object" && error.code === "ENOENT")) {
        throw error;
      }
    }
  }
  const configured = await loadAudioflowToken(credentialOptions);
  if (configured === null) {
    throw new Error(
      "AudioFlow is not connected. Run `node scripts/auth.mjs begin` first.",
    );
  }
  let response;
  try {
    response = await fetchImpl(new URL(SPEECH_PATH, API_ORIGIN), {
      method: "POST",
      headers: {
        authorization: `Bearer ${configured.token}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ input, speed }),
      redirect: "error",
      signal: requestSignal,
    });
  } catch {
    throw new Error("The AudioFlow TTS request failed.");
  }
  const body = await readBoundedJson(response);
  if (response.status !== 200) {
    throw new Error(
      `AudioFlow TTS failed (HTTP ${response.status}, ${safeErrorCode(body)}).`,
    );
  }
  const speech = parseSpeechResponse(body);
  const bytes = await downloadAudio(fetchImpl, speech.audioUrl, downloadSignal);
  const destination = outputPath ?? (await defaultOutputPath());
  await writePrivateFile(destination, bytes);
  return Object.freeze({
    path: destination,
    format: "mp3",
    language: speech.language,
    voice: speech.voice,
    characters: speech.characters,
    expires_at: speech.expiresAt,
  });
}

export async function main(argumentsList = process.argv.slice(2)) {
  if (argumentsList.includes("--help") || argumentsList.includes("-h")) {
    printHelp();
    return;
  }
  const options = parseArguments(argumentsList);
  const text = await readStandardInput();
  const result = await synthesizeAndDownload({ text, ...options });
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

const entrypoint = process.argv[1];
if (
  entrypoint !== undefined &&
  import.meta.url === pathToFileURL(path.resolve(entrypoint)).href
) {
  main().catch((error) => {
    process.stderr.write(
      `${error instanceof Error ? error.message : "Read aloud failed."}\n`,
    );
    process.exitCode = 1;
  });
}
