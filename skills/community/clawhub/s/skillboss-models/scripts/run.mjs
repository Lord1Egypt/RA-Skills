#!/usr/bin/env node

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

Input:
  --prompt <text>      Text prompt
  --text <text>        Text input for TTS
  --size <WxH>         Image/video size
  --duration <sec>     Duration for music/video
  --voice-id <id>      Voice ID for TTS
  --image <url>        Image URL for image-to-video
  --context <text>     Context for chat

Examples:
  run.mjs --models
  run.mjs --models image
  run.mjs --model bedrock/claude-4-5-sonnet --prompt "Explain quantum computing"
  run.mjs --model mm/img --prompt "A sunset"
  run.mjs --task image --prompt "A sunset"
  run.mjs --task chat --prompt "Hello" --prefer price
  run.mjs --task tts --text "Hello world"`);
  process.exit(2);
}

const apiKey = (process.env.SKILLBOSS_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing SKILLBOSS_API_KEY. Get one at https://www.skillboss.co");
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
  if (a === "--size")     { flags.size = args[++i]; continue; }
  if (a === "--duration") { flags.duration = parseInt(args[++i]); continue; }
  if (a === "--voice-id") { flags.voiceId = args[++i]; continue; }
  if (a === "--image")    { flags.image = args[++i]; continue; }
  if (a === "--context")  { flags.context = args[++i]; continue; }
  console.error(`Unknown arg: ${a}`);
  usage();
}

const hasInput = flags.prompt || flags.text;

function buildInputs(type) {
  const inputs = {};
  if (type === "chat" && flags.prompt) {
    inputs.messages = [{ role: "user", content: flags.prompt }];
    if (flags.context) inputs.system = flags.context;
  } else if (type === "tts") {
    if (flags.text) { inputs.text = flags.text; inputs.input = flags.text; }
    inputs.voice_id = flags.voiceId || undefined;
    inputs.voice = flags.voiceId || "alloy";
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

// ── Route: --models ──
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
  endpoint = "/pilot";
  body.discover = true;
  if (flags.keyword) body.keyword = flags.keyword;

} else if (flags.model && hasInput) {
  endpoint = "/run";
  body.model = flags.model;
  body.inputs = buildInputs(inferType(flags.model));

} else if (flags.task && hasInput) {
  endpoint = "/pilot";
  body.type = flags.task;
  if (flags.prefer) body.prefer = flags.prefer;
  body.inputs = buildInputs(flags.task);

} else if (flags.task) {
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

// ── Print result ──
const r = data.result || data;

// Print media URLs for download
const mediaUrl = r.image_url || r.video_url || r.audio_url || r.url
  || r.data?.[0] || r.generated_images?.[0] || null;
if (mediaUrl) {
  console.log(mediaUrl);
} else if (r.choices?.[0]?.message?.content) {
  console.log(r.choices[0].message.content);
} else if (r.content?.[0]?.text) {
  console.log(r.content[0].text);
} else if (r.text) {
  console.log(r.text);
} else {
  console.log(JSON.stringify(data, null, 2));
}
