#!/usr/bin/env node

const API_BASE = "https://api.heybossai.com/v1";

function usage() {
  console.error(`Usage: run.mjs <command> [options]

Commands:
  models [type]        List models (chat, image, video, tts, stt, music)
  run <model> <prompt> Call a model directly
  task <type> <prompt> Auto-select best model for a task
  tasks                List task types

Examples:
  run.mjs models
  run.mjs models image
  run.mjs run bedrock/claude-4-5-sonnet "Explain quantum computing"
  run.mjs run mm/img "A sunset over mountains"
  run.mjs task image "A sunset"
  run.mjs task chat "Hello"`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const apiKey = (process.env.SKILLBOSS_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing SKILLBOSS_API_KEY. Get one at https://www.skillboss.co");
  process.exit(1);
}

const cmd = args[0];

if (cmd === "models") {
  const body = { api_key: apiKey };
  if (args[1]) body.types = args[1];

  const resp = await fetch(`${API_BASE}/models`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Failed (${resp.status}): ${text}`);
  }
  console.log(JSON.stringify(await resp.json(), null, 2));

} else if (cmd === "run" && args[1] && args[2]) {
  const model = args[1];
  const prompt = args[2];

  const inputs = model.match(/tts|speech|eleven/i)
    ? { text: prompt, input: prompt, voice: "alloy" }
    : model.match(/whisper|stt/i)
    ? { text: prompt }
    : model.match(/img|image|flux|gemini.*image|video|veo/i)
    ? { prompt }
    : { messages: [{ role: "user", content: prompt }] };

  const resp = await fetch(`${API_BASE}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key: apiKey, model, inputs }),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`API failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  if (data._balance_warning) {
    const w = data._balance_warning;
    console.error(`[skillboss] ${typeof w === "string" ? w : w.message || JSON.stringify(w)}`);
  }

  const r = data.result || data;
  const url = r.image_url || r.video_url || r.audio_url || r.url
    || r.data?.[0] || r.generated_images?.[0] || null;
  if (url) {
    console.log(url);
  } else if (r.choices?.[0]?.message?.content) {
    console.log(r.choices[0].message.content);
  } else if (r.content?.[0]?.text) {
    console.log(r.content[0].text);
  } else if (r.text) {
    console.log(r.text);
  } else {
    console.log(JSON.stringify(data, null, 2));
  }

} else if (cmd === "task" && args[1] && args[2]) {
  const type = args[1];
  const prompt = args[2];

  const inputs = type === "tts"
    ? { text: prompt, input: prompt, voice: "alloy" }
    : type === "chat"
    ? { messages: [{ role: "user", content: prompt }] }
    : { prompt };

  const resp = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key: apiKey, type, inputs }),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`API failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  if (data._balance_warning) {
    const w = data._balance_warning;
    console.error(`[skillboss] ${typeof w === "string" ? w : w.message || JSON.stringify(w)}`);
  }

  const r = data.result || data;
  const url = r.image_url || r.video_url || r.audio_url || r.url
    || r.data?.[0] || r.generated_images?.[0] || null;
  if (url) {
    console.log(url);
  } else if (r.choices?.[0]?.message?.content) {
    console.log(r.choices[0].message.content);
  } else if (r.content?.[0]?.text) {
    console.log(r.content[0].text);
  } else if (r.text) {
    console.log(r.text);
  } else {
    console.log(JSON.stringify(data, null, 2));
  }

} else if (cmd === "tasks") {
  const resp = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key: apiKey, discover: true }),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Failed (${resp.status}): ${text}`);
  }
  console.log(JSON.stringify(await resp.json(), null, 2));

} else {
  console.error(`Unknown command: ${cmd}`);
  usage();
}
