#!/usr/bin/env node
import { argv, exit, stdout, stderr } from 'node:process';

const DEFAULT_PROMPT = 'vintage retro travel poster illustration, 1950s tourism advertising style, bold flat colors, stylized landmarks and scenery, art deco typography space, screen-printed texture, WPA national park poster aesthetic, golden age of travel, nostalgic composition, clean geometric shapes, muted palette with pops of saturated color';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(args) {
  const out = { prompt: null, size: 'portrait', token: null, ref: null };
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--size') { out.size = args[++i]; }
    else if (a === '--token') { out.token = args[++i]; }
    else if (a === '--ref') { out.ref = args[++i]; }
    else if (!a.startsWith('--')) { positional.push(a); }
  }
  if (positional.length > 0) out.prompt = positional.join(' ');
  return out;
}

async function submitTask({ prompt, width, height, token, ref }) {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };
  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }
  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: {
      'x-token': token,
      'x-platform': 'nieta-app/web',
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`submit failed: ${res.status} ${text}`);
  }
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    const data = await res.json();
    if (typeof data === 'string') return data;
    if (data && data.task_uuid) return data.task_uuid;
    throw new Error(`unexpected submit response: ${JSON.stringify(data)}`);
  }
  const text = (await res.text()).trim().replace(/^"|"$/g, '');
  return text;
}

async function pollTask(taskUuid, token) {
  for (let i = 0; i < 90; i++) {
    await new Promise((r) => setTimeout(r, 2000));
    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers: {
        'x-token': token,
        'x-platform': 'nieta-app/web',
        'content-type': 'application/json',
      },
    });
    if (!res.ok) continue;
    const data = await res.json();
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') continue;
    if (Array.isArray(data.artifacts) && data.artifacts.length > 0 && data.artifacts[0].url) {
      return data.artifacts[0].url;
    }
    if (data.result_image_url) return data.result_image_url;
    throw new Error(`task ended without image: ${JSON.stringify(data)}`);
  }
  throw new Error('timed out after 90 attempts');
}

async function main() {
  const { prompt: promptArg, size, token: tokenFlag, ref } = parseArgs(argv.slice(2));
  const TOKEN = tokenFlag;
  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    exit(1);
  }
  const prompt = promptArg || DEFAULT_PROMPT;
  const dims = SIZES[size] || SIZES.portrait;
  stderr.write(`→ Submitting task (${dims.width}×${dims.height})...\n`);
  const taskUuid = await submitTask({ prompt, width: dims.width, height: dims.height, token: TOKEN, ref });
  stderr.write(`→ Task ${taskUuid}, polling...\n`);
  const url = await pollTask(taskUuid, TOKEN);
  stdout.write(url + '\n');
  exit(0);
}

main().catch((err) => {
  console.error(`\n✗ ${err.message}`);
  exit(1);
});
