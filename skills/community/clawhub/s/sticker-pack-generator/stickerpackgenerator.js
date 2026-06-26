#!/usr/bin/env node
import https from 'https';

const args = process.argv.slice(2);

function getFlag(flag, hasValue = true) {
  const idx = args.indexOf(flag);
  if (idx === -1) return undefined;
  return hasValue ? args[idx + 1] : true;
}

const PROMPT = args.find(a => !a.startsWith('--') && args.indexOf(a) === args.findIndex(x => x === a) && args[args.indexOf(a) - 1] !== '--size' && args[args.indexOf(a) - 1] !== '--token' && args[args.indexOf(a) - 1] !== '--ref');
const sizeFlag = getFlag('--size') || 'square';
const tokenFlag = getFlag('--token');
const refFlag = getFlag('--ref');

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

if (!PROMPT) {
  console.error('\n✗ Prompt required. Usage: node stickerpackgenerator.js "your prompt" --token YOUR_TOKEN');
  process.exit(1);
}

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const { width, height } = SIZES[sizeFlag] || SIZES.square;

const HEADERS = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

function request(method, url, body) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method,
      headers: HEADERS,
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(data.trim()); }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (refFlag) {
    body.inherit_params = { collection_uuid: refFlag, picture_uuid: refFlag };
  }

  const makeRes = await request('POST', 'https://api.talesofai.com/v3/make_image', body);

  let taskUuid;
  if (typeof makeRes === 'string') {
    taskUuid = makeRes;
  } else if (makeRes && makeRes.task_uuid) {
    taskUuid = makeRes.task_uuid;
  } else {
    console.error('✗ Unexpected response from make_image:', JSON.stringify(makeRes));
    process.exit(1);
  }

  const MAX_ATTEMPTS = 90;
  for (let i = 0; i < MAX_ATTEMPTS; i++) {
    await sleep(2000);
    const pollRes = await request('GET', `https://api.talesofai.com/v1/artifact/task/${taskUuid}`);
    const status = pollRes.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url = (pollRes.artifacts && pollRes.artifacts[0] && pollRes.artifacts[0].url) || pollRes.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    } else {
      console.error('✗ Task completed but no image URL found:', JSON.stringify(pollRes));
      process.exit(1);
    }
  }

  console.error('✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch(err => {
  console.error('✗ Error:', err.message || err);
  process.exit(1);
});
