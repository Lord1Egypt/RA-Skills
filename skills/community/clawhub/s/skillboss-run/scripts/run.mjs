#!/usr/bin/env node

function usage() {
  console.error(`Usage: run.mjs <command> [options]

Commands:
  models [type]        List models (chat, image, video, tts, stt, music)
  run <model> <prompt> Call a model directly
  task <type> <prompt> Auto-select best model for a task
  tasks                List task types`);
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

  const resp = await fetch("https://api.heybossai.com/v1/models", {
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
  const resp = await fetch("https://api.heybossai.com/v1/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      model: args[1],
      inputs: args[1].match(/tts|speech|eleven/i)
        ? { text: args[2], input: args[2], voice: "alloy" }
        : args[1].match(/whisper|stt/i)
        ? { text: args[2] }
        : args[1].match(/img|image|flux|gemini.*image|video|veo/i)
        ? { prompt: args[2] }
        : { messages: [{ role: "user", content: args[2] }] },
    }),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`API failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  const r = data.result || data;
  const url = r.image_url || r.video_url || r.audio_url || r.url || null;
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
  const inputs = type === "tts"
    ? { text: args[2], input: args[2], voice: "alloy" }
    : type === "chat"
    ? { messages: [{ role: "user", content: args[2] }] }
    : { prompt: args[2] };

  const resp = await fetch("https://api.heybossai.com/v1/pilot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key: apiKey, type, inputs }),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`API failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  const r = data.result || data;
  const url = r.image_url || r.video_url || r.audio_url || r.url || null;
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
  const resp = await fetch("https://api.heybossai.com/v1/pilot", {
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
