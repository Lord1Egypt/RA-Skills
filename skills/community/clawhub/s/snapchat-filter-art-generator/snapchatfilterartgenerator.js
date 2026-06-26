#!/usr/bin/env node
import process from 'node:process';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_PROMPT = 'Selfie photo with classic Snapchat-style filter overlay, puppy dog ears and tongue or flower crown with sparkles, blown-out front-flash lighting, slightly low-resolution early-iPhone camera quality, 2016 throwback aesthetic, youthful casual vibe, mirror selfie or arm-extended phone selfie composition';

function parseArgs(argv) {
  const args = { size: 'portrait', token: null, ref: null, prompt: null };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') { args.size = argv[++i]; }
    else if (a === '--token') { args.token = argv[++i]; }
    else if (a === '--ref') { args.ref = argv[++i]; }
    else if (a === '--help' || a === '-h') { args.help = true; }
    else { rest.push(a); }
  }
  if (rest.length > 0) args.prompt = rest.join(' ');
  return args;
}

function printHelp() {
  console.log(`Snapchat Filter Art Generator

Usage:
  node snapchatfilterartgenerator.js "your prompt" --token YOUR_TOKEN [options]

Options:
  --size <portrait|landscape|square|tall>   Image size (default: portrait)
  --token <token>                            Neta API token (required)
  --ref <picture_uuid>                       Reference image UUID for style inheritance
  -h, --help                                 Show this help

Get a free trial token at: https://www.neta.art/open/
`);
}

async function main() {
  const argv = process.argv.slice(2);
  const args = parseArgs(argv);

  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const PROMPT = args.prompt || DEFAULT_PROMPT;
  const TOKEN = args.token;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const size = SIZES[args.size] || SIZES.portrait;

  const headers = {
    'x-token': TOKEN,
    'x-platform': 'nieta-app/web',
    'content-type': 'application/json',
  };

  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width: size.width,
    height: size.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (args.ref) {
    body.inherit_params = {
      collection_uuid: args.ref,
      picture_uuid: args.ref,
    };
  }

  console.error(`→ Submitting task (${size.width}×${size.height})...`);

  let createRes;
  try {
    createRes = await fetch('https://api.talesofai.com/v3/make_image', {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
  } catch (e) {
    console.error(`✗ Request failed: ${e.message}`);
    process.exit(1);
  }

  if (!createRes.ok) {
    const text = await createRes.text();
    console.error(`✗ make_image failed: ${createRes.status} ${text}`);
    process.exit(1);
  }

  const rawText = await createRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(rawText);
    if (typeof parsed === 'string') {
      taskUuid = parsed;
    } else if (parsed && typeof parsed === 'object' && parsed.task_uuid) {
      taskUuid = parsed.task_uuid;
    } else {
      taskUuid = rawText.replace(/^"|"$/g, '');
    }
  } catch {
    taskUuid = rawText.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error('✗ No task_uuid returned');
    process.exit(1);
  }

  console.error(`→ Task ${taskUuid} queued. Polling...`);

  const maxAttempts = 90;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    let pollRes;
    try {
      pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
        method: 'GET',
        headers,
      });
    } catch (e) {
      console.error(`  poll error (${attempt}): ${e.message}`);
      continue;
    }

    if (!pollRes.ok) {
      console.error(`  poll ${attempt}: HTTP ${pollRes.status}`);
      continue;
    }

    let data;
    try {
      data = await pollRes.json();
    } catch (e) {
      console.error(`  poll ${attempt}: invalid JSON`);
      continue;
    }

    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      if (attempt % 5 === 0) console.error(`  ...still ${status} (${attempt}/${maxAttempts})`);
      continue;
    }

    let url = null;
    if (Array.isArray(data.artifacts) && data.artifacts.length > 0 && data.artifacts[0].url) {
      url = data.artifacts[0].url;
    } else if (data.result_image_url) {
      url = data.result_image_url;
    }

    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`✗ Task finished with status "${status}" but no image URL.`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('✗ Timed out after 90 polls (~3 minutes).');
  process.exit(1);
}

main().catch((e) => {
  console.error(`✗ Unexpected error: ${e.message}`);
  process.exit(1);
});
