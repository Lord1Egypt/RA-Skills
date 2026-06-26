#!/usr/bin/env node

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = "portrait";
let tokenFlag = null;
let ref = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--token" && i + 1 < args.length) {
    tokenFlag = args[++i];
  } else if (args[i] === "--size" && i + 1 < args.length) {
    size = args[++i];
  } else if (args[i] === "--ref" && i + 1 < args.length) {
    ref = args[++i];
  } else if (!prompt && !args[i].startsWith("--")) {
    prompt = args[i];
  }
}

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

if (!prompt) {
  prompt = "a beautiful stained glass art panel, luminous jewel-toned colors, bold dark lead lines separating glass segments, radiant light shining through translucent colored glass, intricate detailed glasswork pattern, cathedral window aesthetic";
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const chosen = SIZES[size] || SIZES.portrait;

const headers = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
  width: chosen.width,
  height: chosen.height,
  meta: { entrance: "PICTURE,VERSE" },
  context_model_series: "8_image_edit",
};

if (ref) {
  body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
}

console.error(`\n◈ Stained Glass Art Generator`);
console.error(`  Prompt: "${prompt}"`);
console.error(`  Size:   ${size} (${chosen.width}×${chosen.height})`);
if (ref) console.error(`  Ref:    ${ref}`);
console.error("");

async function createTask() {
  const res = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error(`✗ API error ${res.status}: ${text}`);
    process.exit(1);
  }

  const data = await res.json();

  if (typeof data === "string") return data;
  if (data.task_uuid) return data.task_uuid;

  console.error("✗ Unexpected response:", JSON.stringify(data));
  process.exit(1);
}

async function pollTask(taskUuid) {
  const maxAttempts = 90;
  const interval = 2000;

  for (let i = 0; i < maxAttempts; i++) {
    await new Promise((r) => setTimeout(r, interval));

    const res = await fetch(
      `https://api.talesofai.com/v1/artifact/task/${taskUuid}`,
      { headers }
    );

    if (!res.ok) {
      console.error(`✗ Poll error ${res.status}`);
      continue;
    }

    const data = await res.json();
    const status = data.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      console.error(`  ⏳ ${status}… (${i + 1}/${maxAttempts})`);
      continue;
    }

    const url =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (url) {
      console.log(url);
      return;
    }

    console.error("✗ No image URL in response:", JSON.stringify(data));
    process.exit(1);
  }

  console.error("✗ Timed out waiting for image generation.");
  process.exit(1);
}

try {
  const taskUuid = await createTask();
  console.error(`  Task: ${taskUuid}`);
  await pollTask(taskUuid);
} catch (err) {
  console.error(`✗ ${err.message}`);
  process.exit(1);
}
