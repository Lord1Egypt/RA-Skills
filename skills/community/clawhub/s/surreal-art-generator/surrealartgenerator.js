#!/usr/bin/env node
import process from 'node:process';

const API_BASE = 'https://api.talesofai.com';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_PROMPT = 'surreal dreamlike scene, absurd and imaginative composition, impossible physics, melting forms, floating objects, vivid otherworldly colors, hyper-detailed, dali-inspired, magritte-inspired, cinematic lighting, high resolution';

function parseArgs(argv) {
  const args = { prompt: null, size: 'square', token: null, ref: null };
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--size') { args.size = rest[++i]; }
    else if (a === '--token') { args.token = rest[++i]; }
    else if (a === '--ref') { args.ref = rest[++i]; }
    else if (!a.startsWith('--') && args.prompt === null) { args.prompt = a; }
  }
  return args;
}

async function main() {
  const { prompt: userPrompt, size, token: tokenFlag, ref } = parseArgs(process.argv);

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = userPrompt && userPrompt.trim().length > 0
    ? `${userPrompt}, ${DEFAULT_PROMPT}`
    : DEFAULT_PROMPT;

  const dims = SIZES[size] || SIZES.square;

  const headers = {
    'x-token': TOKEN,
    'x-platform': 'nieta-app/web',
    'content-type': 'application/json',
  };

  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width: dims.width,
    height: dims.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  console.error(`→ Submitting prompt (${dims.width}×${dims.height})...`);

  const submitRes = await fetch(`https://api.talesofai.com/v3/make_image`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!submitRes.ok) {
    const text = await submitRes.text();
    console.error(`✗ Submit failed: ${submitRes.status} ${text}`);
    process.exit(1);
  }

  const submitText = await submitRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(submitText);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = submitText.trim().replace(/^"|"$/g, '');
  }

  if (!taskUuid) {
    console.error(`✗ No task_uuid in response: ${submitText}`);
    process.exit(1);
  }

  console.error(`→ Task ${taskUuid} queued. Polling...`);

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, { headers });
    if (!pollRes.ok) {
      const t = await pollRes.text();
      console.error(`✗ Poll failed: ${pollRes.status} ${t}`);
      process.exit(1);
    }
    const data = await pollRes.json();
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }
    const url = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    }
    console.error(`✗ Task ended (${status}) without an image URL.`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('✗ Timed out waiting for task to finish.');
  process.exit(1);
}

main().catch((err) => {
  console.error(`✗ ${err.message || err}`);
  process.exit(1);
});
