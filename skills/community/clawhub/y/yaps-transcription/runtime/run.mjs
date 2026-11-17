#!/usr/bin/env node

// Muse adapter. Discovery is copied verbatim from plugins/shared at build time.
// This adapter writes no diagnostics, credentials, settings, or host permissions.
import { spawn } from "node:child_process";
import { readFile, stat, mkdtemp, rm, writeFile, link, realpath } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export class AdapterError extends Error {
  constructor(code, message, exitCode = 1) {
    super(message);
    this.code = code;
    this.exitCode = exitCode;
  }
}

export function validateArguments(args) {
  if (!Array.isArray(args) || !args.length || args.length > 512
      || args.some((arg) => typeof arg !== "string" || arg.includes("\0"))
      || Buffer.byteLength(JSON.stringify(args)) > 1024 * 1024) {
    throw new AdapterError("invalid_arguments", "Supply a non-empty JSON array of CLI argument strings.", 2);
  }
  return [...args];
}

export async function prepareInvocation(args, discovery, env = process.env) {
  args = validateArguments(args);
  const authStatus = discovery.isAuthStatusCommand(args);
  const gated = discovery.commandRequiresActiveAccount(args);
  const session = await discovery.resolveYapsSession({
    commandArguments: args,
    recoverAccount: authStatus || gated,
    env,
  });
  if (!session.path) {
    const failure = discovery.classifyCliResolutionFailure(session);
    throw new AdapterError(failure.code, failure.message, failure.exitCode);
  }
  // Even unfamiliar auth flags must not reach a credential-reading legacy CLI.
  if (session.authStatusSafety !== "safe") {
    const failure = discovery.diagnoseAccount(session);
    throw new AdapterError(failure.code, failure.message, 78);
  }
  if (authStatus) {
    if (!session.auth) {
      const failure = discovery.diagnoseAccount(session);
      throw new AdapterError(failure.code, failure.message, 78);
    }
    return { result: {
      authenticated: session.auth.authenticated === true,
      status: session.auth.status,
      diagnostic_code: session.auth.diagnosticCode,
      credential_status: "not_accessed",
    } };
  }
  if (gated) {
    const account = discovery.diagnoseAccount(session);
    if (account.code !== "ready") throw new AdapterError(account.code, account.message, 77);
  }
  return {
    command: session.path,
    args: discovery.applyResolvedSettings(args, session.settingsPath, { env }),
    // Do not inherit an identity or automatic MCP consent from another host.
    env: Object.fromEntries(Object.entries(env).filter(([key]) =>
      !key.startsWith("YAPS_MCP_") && !key.startsWith("YAPS_PLUGIN_"))),
  };
}

export function runProcess(command, args, { env = process.env, capture = false, signal } = {}) {
  return new Promise((accept, reject) => {
    if (signal?.aborted) return reject(new AdapterError("cancelled", "The Yaps operation was cancelled.", 130));
    const child = spawn(command, args, {
      env, shell: false, windowsHide: true,
      stdio: capture ? ["ignore", "pipe", "pipe"] : "inherit",
    });
    let bytes = 0;
    const chunks = [];
    let error;
    let killTimer;
    const stop = () => {
      child.kill("SIGTERM");
      killTimer ??= setTimeout(() => child.kill("SIGKILL"), 3000);
      killTimer.unref();
    };
    const onAbort = () => {
      error = new AdapterError("cancelled", "The Yaps operation was cancelled.", 130);
      stop();
    };
    signal?.addEventListener("abort", onAbort, { once: true });
    child.on("error", () => {
      error = new AdapterError("engine_launch_failed", "The verified Yaps helper could not start. Check host permissions and update Yaps if needed.", 127);
    });
    if (capture) {
      child.stdout.on("data", (chunk) => {
        bytes += chunk.length;
        if (bytes > 32 * 1024 * 1024) {
          error = new AdapterError("response_too_large", "The Yaps response exceeded the adapter's 32 MiB limit. Use the saved project in Yaps.");
          stop();
        } else chunks.push(chunk);
      });
      // Do not forward arbitrary engine logs into a structured result or persist them.
      child.stderr.resume();
    }
    child.on("close", (code, childSignal) => {
      clearTimeout(killTimer);
      signal?.removeEventListener("abort", onAbort);
      if (error) return reject(error);
      if (childSignal) return reject(new AdapterError("cancelled", "The Yaps operation ended before completion.", 130));
      accept({ code: code ?? 1, stdout: capture ? Buffer.concat(chunks).toString("utf8") : undefined });
    });
  });
}

export async function runYaps(args, { discovery, capture = false, allowArray = false, signal, execute = runProcess, env } = {}) {
  discovery ??= await import("./yaps-cli-discovery.mjs");
  const invocation = await prepareInvocation(args, discovery, env);
  if (invocation.result) return capture ? invocation.result : { code: 0, result: invocation.result };
  const execution = await execute(invocation.command, invocation.args, { env: invocation.env, capture, signal });
  if (!capture) return execution;
  // Yaps exit codes: 1 error, 2 usage, 3 not_found, 4 conflict, 75 busy,
  // 130 cancelled. Current builds also print {"error","error_code"} on
  // stdout; older builds print plain text on stderr with an empty stdout.
  const exitCode = execution.code === 0 ? 1 : execution.code;
  let result;
  try { result = JSON.parse(execution.stdout); } catch {
    if (execution.code === 130) throw new AdapterError("cancelled", "The Yaps operation was cancelled before completion.", 130);
    throw new AdapterError("invalid_engine_response", `Yaps did not return a JSON result (exit ${execution.code}). Retry the same command through CLI mode to inspect the engine's recovery guidance.`, exitCode);
  }
  if (execution.code !== 0 || !result || (Array.isArray(result) && !allowArray) || typeof result !== "object"
      || result.error || result.success === false) {
    const safeCode = typeof result?.error_code === "string" && /^[a-z0-9_]{1,80}$/.test(result.error_code)
      ? result.error_code : "engine_failed";
    throw new AdapterError(safeCode, `Yaps did not complete the operation (${safeCode}). No successful result was recorded.`, safeCode === "cancelled" ? 130 : exitCode);
  }
  return result;
}

async function requireFile(path) {
  if (typeof path !== "string" || !path.trim() || !await stat(path).then((s) => s.isFile(), () => false)) {
    throw new AdapterError("input_missing", "The selected input must be an existing regular file.", 2);
  }
  return resolve(path);
}

export async function transcribeFile(request, options = {}) {
  return speechFile(request, "txt", options);
}

export async function subtitleFile(request, options = {}) {
  return speechFile(request, "srt", options);
}

function validateSrt(text) {
  const blocks = text.replace(/\r\n/g, "\n").trim().split(/\n\s*\n/);
  let previousEnd = 0;
  for (let index = 0; index < blocks.length; index++) {
    const match = blocks[index].match(/^(\d+)\n(\d{2,}:\d{2}:\d{2},\d{3}) --> (\d{2,}:\d{2}:\d{2},\d{3})\n([\s\S]+)$/);
    const time = (s) => {
      const [h, m, sec, ms] = s.split(/[:,]/).map(Number);
      return m < 60 && sec < 60 ? ((h * 60 + m) * 60 + sec) * 1000 + ms : NaN;
    };
    if (!match || Number(match[1]) !== index + 1 || !match[4].trim()
        || !Number.isSafeInteger(time(match[2])) || !Number.isSafeInteger(time(match[3]))
        || time(match[2]) < previousEnd || time(match[3]) <= time(match[2])) {
      throw new AdapterError("invalid_subtitles", "Yaps returned empty or invalid subtitle cues. No subtitle file was published.");
    }
    previousEnd = time(match[3]);
  }
}

async function speechFile(request, format, { run = runYaps, signal } = {}) {
  const input = await requireFile(request.input);
  if (typeof request.output !== "string" || !request.output.trim()) {
    throw new AdapterError("invalid_output", `Choose a separate .${format} output path.`, 2);
  }
  const output = resolve(request.output);
  if (input === output || extname(output).toLowerCase() !== `.${format}`) {
    throw new AdapterError("invalid_output", `The destination must be a separate .${format} file.`, 2);
  }
  // Exclusive creation at the final write also protects against output races.
  if (await stat(output).then(() => true, (e) => e.code !== "ENOENT")) {
    throw new AdapterError("exists", "The destination already exists or is inaccessible. Choose a new filename.");
  }
  const temp = await mkdtemp(join(tmpdir(), "yaps-muse-transcript-"));
  try {
    const intermediate = join(temp, "transcript.srt");
    const result = await run(["--pretty", "srt", "generate", input, "--output", intermediate], { capture: true, signal });
    if (typeof result.transcript !== "string" || !result.transcript.trim()) {
      throw new AdapterError("no_speech", "Yaps returned no speech. No transcript file was created.");
    }
    if (signal?.aborted) throw new AdapterError("cancelled", "Transcription was cancelled before export.", 130);
    let content = `${result.transcript.trim()}\n`;
    if (format === "srt") {
      const info = await stat(intermediate);
      if (!info.isFile() || info.size > 32 * 1024 * 1024) {
        throw new AdapterError("invalid_subtitles", "The subtitle result is missing or exceeds the adapter's 32 MiB limit.");
      }
      content = await readFile(intermediate, "utf8");
      validateSrt(content);
    }
    const exportTemp = await mkdtemp(join(dirname(output), ".yaps-muse-export-"));
    try {
      const staged = join(exportTemp, `transcript.${format}`);
      await writeFile(staged, content, { flag: "wx", mode: 0o600 });
      // A same-filesystem hard link publishes the completed file atomically and
      // refuses existing files, including symlinks. Never use a replacing rename.
      await link(staged, output);
    } catch (e) {
      throw new AdapterError(e.code === "EEXIST" ? "exists" : "export_failed", "The result could not be saved to that new filename. Existing files were preserved.");
    } finally {
      await rm(exportTemp, { recursive: true, force: true });
    }
    return { output_path: output, engine: result.engine, duration_secs: result.duration_secs, word_count: result.word_count };
  } finally {
    await rm(temp, { recursive: true, force: true });
  }
}

const VIDEO_EXTENSIONS = new Set([".3gp", ".avi", ".flv", ".m2ts", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg", ".mts", ".ts", ".webm", ".wmv"]);

export async function meetingFile(request, { run = runYaps, signal } = {}) {
  const input = await requireFile(request.input);
  const engine = request.engine ?? "auto";
  if (!["auto", "sherpa", "moss"].includes(engine) || (request.speakers !== undefined
      && (!Number.isInteger(request.speakers) || request.speakers < 1 || request.speakers > 20 || engine === "moss"))) {
    throw new AdapterError("invalid_engine_options", "Use auto, sherpa, or moss; a 1-20 speaker hint is available with auto or sherpa.", 2);
  }
  if (request.title !== undefined && (typeof request.title !== "string" || request.title.includes("\0"))) {
    throw new AdapterError("invalid_title", "The meeting title must be text.", 2);
  }
  let temp;
  try {
    let audio = input;
    if (VIDEO_EXTENSIONS.has(extname(input).toLowerCase())) {
      temp = await mkdtemp(join(tmpdir(), "yaps-muse-meeting-"));
      audio = join(temp, "meeting.wav");
      await run(["--pretty", "media", "extract-audio", input, "--format", "wav", "--output", audio], { capture: true, signal });
      await requireFile(audio);
    }
    if (signal?.aborted) throw new AdapterError("cancelled", "Meeting transcription was cancelled.", 130);
    const args = ["--pretty", "meeting", "transcribe", audio, "--engine", engine];
    if (request.speakers !== undefined) args.push("--speakers", String(request.speakers));
    if (request.title !== undefined) args.push("--title", request.title);
    // Yaps persists its own project audio; only our temporary extraction is removed.
    const result = await run(args, { capture: true, signal });
    if (!Array.isArray(result.segments) || !result.segments.length || !result.meeting_id) {
      throw new AdapterError("no_meeting_segments", "Yaps returned no usable meeting transcript. Check Yaps Meetings before retrying, as a project may already exist.");
    }
    return {
      meeting_id: result.meeting_id, title: result.title, engine: result.engine,
      engine_reason: result.engine_reason, duration_secs: result.duration_secs,
      num_speakers: result.num_speakers, segment_count: result.segments.length,
      project_path: result.project_path, audio_path: result.audio_path,
    };
  } finally {
    if (temp) await rm(temp, { recursive: true, force: true });
  }
}

const MAX_REQUEST_BYTES = 1024 * 1024;

// "-" reads the request from stdin, so a host that runs commands on another
// computer (Grok Bot's local-computer execution) can pass JSON through a
// single-quoted heredoc instead of creating a temporary file there first.
async function readStdin(input = process.stdin) {
  const chunks = [];
  let size = 0;
  for await (const chunk of input) {
    size += chunk.length;
    if (size > MAX_REQUEST_BYTES) throw new AdapterError("invalid_request", "A JSON request of at most 1 MiB is required.", 2);
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8");
}

export async function readRequest(path, { stdin } = {}) {
  let text;
  if (path === "-") {
    text = await readStdin(stdin);
  } else {
    if (!path || (await stat(path)).size > MAX_REQUEST_BYTES) throw new AdapterError("invalid_request", "A JSON request file of at most 1 MiB is required.", 2);
    text = await readFile(path, "utf8");
  }
  try { return JSON.parse(text); } catch {
    throw new AdapterError("invalid_request", "The request must contain valid JSON.", 2);
  }
}

const WORKFLOWS = { "transcribe-file": transcribeFile, "srt-file": subtitleFile, "meeting-file": meetingFile };
const ADAPTER_VERBS = new Set(["--", "--args-file", "request", ...Object.keys(WORKFLOWS)]);

// Yaps CLIs newer than 2.4.0 answer `request` themselves; this mirrors that
// surface so a skill can call either one with the same command.
async function requestMode(source, options) {
  const request = await readRequest(source);
  if (Array.isArray(request)) return runYaps(stripRedact(request), options);
  if (request && typeof request === "object" && Object.hasOwn(WORKFLOWS, request.workflow)) {
    const { workflow, ...rest } = request;
    return { code: 0, result: await WORKFLOWS[workflow](rest, { signal: options.signal }) };
  }
  throw new AdapterError("invalid_request", "Send a JSON array of Yaps arguments or a {\"workflow\": ...} object.", 2);
}

// The adapter's own `auth status` is always redacted; older CLIs do not know
// the flag, so drop it rather than forward an unknown option.
export function stripRedact(args) {
  const words = args.filter((arg) => arg !== "--pretty");
  return words.length === 3 && words[0] === "auth" && words[1] === "status" && words[2] === "--redact"
    ? args.filter((arg) => arg !== "--redact") : args;
}

export async function main(argv) {
  const controller = new AbortController();
  const cancel = () => controller.abort();
  process.once("SIGINT", cancel);
  process.once("SIGTERM", cancel);
  try {
    let result;
    if (argv[0] === "request" && argv.length <= 2) {
      const execution = await requestMode(argv[1] ?? "-", { signal: controller.signal });
      result = execution.result;
      process.exitCode = execution.code;
    } else if (argv.length && !ADAPTER_VERBS.has(argv[0])) {
      // Plain Yaps arguments, exactly as the installed CLI would take them.
      const execution = await runYaps(stripRedact(argv), { signal: controller.signal });
      result = execution.result;
      process.exitCode = execution.code;
    } else if (argv[0] === "--" || (argv[0] === "--args-file" && argv.length === 2)) {
      const args = argv[0] === "--" ? argv.slice(1) : await readRequest(argv[1]);
      const execution = await runYaps(args, { signal: controller.signal });
      result = execution.result;
      process.exitCode = execution.code;
    } else if (["transcribe-file", "srt-file", "meeting-file"].includes(argv[0]) && argv.length === 2) {
      const request = await readRequest(argv[1]);
      if (!request || Array.isArray(request) || typeof request !== "object") throw new AdapterError("invalid_request", "The request must contain a JSON object.", 2);
      result = await ({"transcribe-file":transcribeFile, "srt-file":subtitleFile, "meeting-file":meetingFile}[argv[0]])(request, { signal: controller.signal });
    } else {
      throw new AdapterError("usage", "Usage: node run.mjs <Yaps arguments> | request [-|<JSON file>] | -- <Yaps arguments> | --args-file <JSON array file or -> | transcribe-file|srt-file|meeting-file <JSON object file or -> (- reads stdin)", 2);
    }
    if (result !== undefined) process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) {
    const known = error instanceof AdapterError;
    process.stderr.write(`${JSON.stringify({ error_code: known ? error.code : "adapter_failed", error: known ? error.message : "The Yaps adapter could not complete the request. Check file access and the installed Yaps version." })}\n`);
    process.exitCode = known ? error.exitCode : 1;
  } finally {
    process.removeListener("SIGINT", cancel);
    process.removeListener("SIGTERM", cancel);
  }
}

// Node resolves module symlinks, while argv can retain an alias such as macOS
// /tmp or an agent's installed-plugin link. Compare canonical paths on both sides.
const entrypoint = process.argv[1] ? await realpath(resolve(process.argv[1])).catch(() => null) : null;
if (entrypoint && entrypoint === await realpath(fileURLToPath(import.meta.url))) await main(process.argv.slice(2));
