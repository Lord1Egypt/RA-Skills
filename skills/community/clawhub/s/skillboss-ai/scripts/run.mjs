#!/usr/bin/env node

import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = join(__dirname, "..", "config.json");
const API_BASE = "https://api.heybossai.com/v1";

function usage() {
  console.error(`Usage: run.mjs [options]

Run 50+ AI models — chat, image, video, TTS, STT, music, search, and more.

Models:
  --models             List all available models
  --models <type>      List models by type (chat, image, video, tts, ...)

Direct call (specify model):
  --model <id>         Model ID (e.g. bedrock/claude-4-5-sonnet, mm/img)

Smart call (auto-select best model for a task):
  --task <type>        Task type: chat, image, video, tts, stt, music, ...
  --tasks              List available task types
  --tasks --keyword X  Search tasks by keyword
  --prefer <strategy>  price | quality | balanced (default)

Input/output:
  --prompt <text>      Text prompt
  --text <text>        Text input for TTS
  --file <path>        Audio file for STT
  --output <path>      Save result to file
  --size <WxH>         Image/video size
  --duration <sec>     Duration for music/video
  --voice-id <id>      Voice ID for TTS
  --image <url>        Image URL for image-to-video
  --context <text>     Context for chat

Examples:
  run.mjs --models
  run.mjs --models image
  run.mjs --model bedrock/claude-4-5-sonnet --prompt "Explain quantum computing"
  run.mjs --model mm/img --prompt "A sunset" --output sunset.png
  run.mjs --task image --prompt "A sunset" --output sunset.png
  run.mjs --task chat --prompt "Hello" --prefer price
  run.mjs --task tts --text "Hello world" --output hello.mp3`);
  process.exit(2);
}

function getApiKey() {
  const envKey = (process.env.SKILLBOSS_API_KEY ?? "").trim();
  if (envKey) return envKey;

  try {
    const config = JSON.parse(readFileSync(CONFIG_PATH, "utf8"));
    if (config.apiKey && config.apiKey !== "YOUR_API_KEY_HERE" && !config.apiKey.includes("...")) {
      return config.apiKey;
    }
  } catch {}

  console.error("Missing SKILLBOSS_API_KEY. Run: node auth.mjs trial");
  process.exit(1);
}

// Parse args
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const flags = {};
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--models")   { flags.models = args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true; continue; }
  if (a === "--model")    { flags.model = args[++i]; continue; }
  if (a === "--tasks")    { flags.tasks = true; continue; }
  if (a === "--task")     { flags.task = args[++i]; continue; }
  if (a === "--keyword")  { flags.keyword = args[++i]; continue; }
  if (a === "--prefer")   { flags.prefer = args[++i]; continue; }
  if (a === "--limit")    { flags.limit = parseInt(args[++i]); continue; }
  if (a === "--prompt")   { flags.prompt = args[++i]; continue; }
  if (a === "--text")     { flags.text = args[++i]; continue; }
  if (a === "--file")     { flags.file = args[++i]; continue; }
  if (a === "--output")   { flags.output = args[++i]; continue; }
  if (a === "--size")     { flags.size = args[++i]; continue; }
  if (a === "--duration") { flags.duration = parseInt(args[++i]); continue; }
  if (a === "--voice-id") { flags.voiceId = args[++i]; continue; }
  if (a === "--image")    { flags.image = args[++i]; continue; }
  if (a === "--context")  { flags.context = args[++i]; continue; }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const apiKey = getApiKey();
const hasInput = flags.prompt || flags.text || flags.file;

function buildInputs(type) {
  const inputs = {};
  if (type === "chat" && flags.prompt) {
    inputs.messages = [{ role: "user", content: flags.prompt }];
    if (flags.context) inputs.system = flags.context;
  } else if (type === "tts") {
    if (flags.text) { inputs.text = flags.text; inputs.input = flags.text; }
    inputs.voice_id = flags.voiceId || undefined;
    inputs.voice = flags.voiceId || "alloy";
  } else if (type === "stt" && flags.file) {
    const filePath = resolve(flags.file);
    inputs.audio_data = readFileSync(filePath).toString("base64");
    inputs.filename = basename(filePath);
  } else {
    if (flags.prompt) inputs.prompt = flags.prompt;
    if (flags.image) inputs.image = flags.image;
    if (flags.size) inputs.size = flags.size;
    if (flags.duration) inputs.duration = flags.duration;
  }
  return inputs;
}

function inferType(model) {
  if (!model) return null;
  if (/whisper|stt/i.test(model)) return "stt";
  if (/tts|speech|eleven/i.test(model)) return "tts";
  return "chat";
}

// ── Route: --models (list available models) ──
if (flags.models) {
  const modelsBody = { api_key: apiKey };
  if (typeof flags.models === "string") modelsBody.types = flags.models;

  const resp = await fetch(`${API_BASE}/models`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(modelsBody),
  });
  if (!resp.ok) {
    console.error(`Failed (${resp.status}): ${await resp.text().catch(() => "")}`);
    process.exit(1);
  }
  console.log(JSON.stringify(await resp.json(), null, 2));
  process.exit(0);
}

// ── Build POST body ──
const headers = { "Content-Type": "application/json" };
const body = { api_key: apiKey };
let endpoint;

if (flags.tasks) {
  // List task types
  endpoint = "/pilot";
  body.discover = true;
  if (flags.keyword) body.keyword = flags.keyword;

} else if (flags.model && hasInput) {
  // Direct model call → /run
  endpoint = "/run";
  body.model = flags.model;
  body.inputs = buildInputs(inferType(flags.model));

} else if (flags.task && hasInput) {
  // Smart execute → /pilot
  endpoint = "/pilot";
  body.type = flags.task;
  if (flags.prefer) body.prefer = flags.prefer;
  body.inputs = buildInputs(flags.task);

} else if (flags.task) {
  // Recommendations → /pilot
  endpoint = "/pilot";
  body.type = flags.task;
  if (flags.prefer) body.prefer = flags.prefer;
  if (flags.limit) body.limit = flags.limit;

} else {
  usage();
}

// ── Call API ──
const resp = await fetch(`${API_BASE}${endpoint}`, {
  method: "POST",
  headers,
  body: JSON.stringify(body),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  console.error(`API failed (${resp.status}): ${text}`);
  process.exit(1);
}

const data = await resp.json();

if (data._balance_warning) {
  const w = data._balance_warning;
  console.error(`[skillboss] ${typeof w === "string" ? w : w.message || JSON.stringify(w)}`);
}

// ── Save output file ──
if (flags.output && hasInput) {
  const inner = data.result || data;
  const url = inner.image_url || inner.video_url || inner.audio_url || inner.url
    || inner.data?.[0] || inner.generated_images?.[0] || null;

  if (url) {
    const dl = await fetch(url);
    if (dl.ok) {
      writeFileSync(flags.output, Buffer.from(await dl.arrayBuffer()));
      console.error(`Saved to ${flags.output}`);
    }
  } else if (inner.audio_base64) {
    writeFileSync(flags.output, Buffer.from(inner.audio_base64, "base64"));
    console.error(`Saved to ${flags.output}`);
  }
}

// ── Print result ──
const r = data.result || data;
if (r.choices?.[0]?.message?.content) {
  console.log(r.choices[0].message.content);
} else if (r.content?.[0]?.text) {
  console.log(r.content[0].text);
} else if (r.text) {
  console.log(r.text);
} else {
  console.log(JSON.stringify(data, null, 2));
}
