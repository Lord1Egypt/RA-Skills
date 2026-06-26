#!/usr/bin/env node
import { argv, exit, stdout } from 'node:process';

const DEFAULT_PROMPT = 'elegant wedding invitation design, soft watercolor botanical florals in blush pink and ivory, delicate gold foil accents, romantic garden aesthetic, sophisticated layout with space for typography, cream paper texture, refined and timeless, high-end stationery photography, soft natural light';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(args) {
  let prompt = null;
  let size = 'portrait';
  let tokenFlag = null;
  let ref = null;

  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--size') {
      size = args[++i];
    } else if (a === '--token') {
      tokenFlag = args[++i];
    } else if (a === '--ref') {
      ref = args[++i];
    } else if (a.startsWith('--size=')) {
      size = a.slice('--size='.length);
    } else if (a.startsWith('--token=')) {
      tokenFlag = a.slice('--token='.length);
    } else if (a.startsWith('--ref=')) {
      ref = a.slice('--ref='.length);
    } else if (!a.startsWith('--') && prompt === null) {
      prompt = a;
    }
  }

  return { prompt, size, tokenFlag, ref };
}

async function main() {
  const { prompt, size, tokenFlag, ref } = parseArgs(argv.slice(2));

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = prompt || DEFAULT_PROMPT;
  const dims = SIZES[size] || SIZES.portrait;

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
    body.inherit_params = {
      collection_uuid: ref,
      picture_uuid: ref,
    };
  }

  console.error(`→ Submitting task (${dims.width}×${dims.height})...`);

  let res;
  try {
    res = await fetch('https://api.talesofai.com/v3/make_image', {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
  } catch (err) {
    console.error(`✗ Request failed: ${err.message}`);
    exit(1);
  }

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    console.error(`✗ make_image failed: HTTP ${res.status} ${text}`);
    exit(1);
  }

  const raw = await res.text();
  let taskUuid;
  const trimmed = raw.trim();
  try {
    const parsed = JSON.parse(trimmed);
    if (typeof parsed === 'string') {
      taskUuid = parsed;
    } else if (parsed && typeof parsed === 'object' && parsed.task_uuid) {
      taskUuid = parsed.task_uuid;
    } else {
      taskUuid = trimmed.replace(/^"|"$/g, '');
    }
  } catch {
    taskUuid = trimmed.replace(/^"|"$/g, '');
  }

  if (!taskUuid) {
    console.error('✗ No task_uuid returned');
    exit(1);
  }

  console.error(`→ Task: ${taskUuid}`);
  console.error('→ Polling...');

  const maxAttempts = 90;
  for (let i = 0; i < maxAttempts; i++) {
    await new Promise((r) => setTimeout(r, 2000));

    let pollRes;
    try {
      pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
        method: 'GET',
        headers,
      });
    } catch (err) {
      console.error(`  poll error: ${err.message}`);
      continue;
    }

    if (!pollRes.ok) {
      console.error(`  poll HTTP ${pollRes.status}`);
      continue;
    }

    let data;
    try {
      data = await pollRes.json();
    } catch {
      continue;
    }

    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') {
      if (i % 5 === 0) console.error(`  [${i + 1}/${maxAttempts}] ${status}`);
      continue;
    }

    const url =
      (Array.isArray(data.artifacts) && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (url) {
      stdout.write(url + '\n');
      exit(0);
    }

    console.error(`✗ Task finished with status "${status}" but no image URL.`);
    console.error(JSON.stringify(data, null, 2));
    exit(1);
  }

  console.error('✗ Timed out after 90 attempts (~3 minutes).');
  exit(1);
}

main().catch((err) => {
  console.error(`✗ ${err.message}`);
  exit(1);
});
