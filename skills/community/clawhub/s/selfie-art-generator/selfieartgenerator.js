#!/usr/bin/env node
// selfieartgenerator.js — Selfie Art Generator

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = 'portrait';
let style = 'cinematic';
let tokenFlag = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--size' && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === '--style' && args[i + 1]) {
    style = args[++i];
  } else if (args[i] === '--token' && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === '--ref' && args[i + 1]) {
    refUuid = args[++i];
  } else if (!args[i].startsWith('--') && prompt === null) {
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
  console.error('\n✗ Prompt required. Usage: node selfieartgenerator.js "your prompt" --token YOUR_TOKEN');
  process.exit(1);
}

// Size map
const SIZE_MAP = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const dimensions = SIZE_MAP[size] || SIZE_MAP.portrait;

const HEADERS = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

// Build request body
const body = {
  storyId: 'DO_NOT_USE',
  jobType: 'universal',
  rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
  width: dimensions.width,
  height: dimensions.height,
  meta: { entrance: 'PICTURE,VERSE' },
  context_model_series: '8_image_edit',
};

if (refUuid) {
  body.inherit_params = {
    collection_uuid: refUuid,
    picture_uuid: refUuid,
  };
}

async function makeImage() {
  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error(`✗ Failed to create image task (${res.status}): ${text}`);
    process.exit(1);
  }

  const data = await res.json();
  const taskUuid = typeof data === 'string' ? data : data.task_uuid;

  if (!taskUuid) {
    console.error('✗ No task_uuid returned from API');
    process.exit(1);
  }

  return taskUuid;
}

async function pollTask(taskUuid) {
  const MAX_ATTEMPTS = 90;
  const POLL_INTERVAL_MS = 2000;

  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));

    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers: HEADERS,
    });

    if (!res.ok) {
      const text = await res.text();
      console.error(`✗ Poll failed (${res.status}): ${text}`);
      process.exit(1);
    }

    const data = await res.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    // Done — extract image URL
    const url =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (!url) {
      console.error('✗ Task completed but no image URL found in response');
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error('✗ Timed out waiting for image generation');
  process.exit(1);
}

const taskUuid = await makeImage();
await pollTask(taskUuid);
