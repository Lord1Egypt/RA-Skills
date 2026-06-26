#!/usr/bin/env node
import https from 'https';

const args = process.argv.slice(2);

let prompt = null;
let size = 'portrait';
let tokenFlag = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--size' && args[i + 1]) {
    size = args[++i];
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
  prompt = 'a beautiful watercolor painting portrait, soft translucent washes of color, visible paper texture, wet-on-wet blending, delicate brushstrokes, luminous pastel hues, fine art watercolor illustration style';
}

const sizes = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const { width, height } = sizes[size] || sizes.portrait;

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
      headers: { ...HEADERS },
    };

    let bodyStr;
    if (body) {
      bodyStr = JSON.stringify(body);
      options.headers['content-length'] = Buffer.byteLength(bodyStr);
    }

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data.trim());
        }
      });
    });

    req.on('error', reject);
    if (bodyStr) req.write(bodyStr);
    req.end();
  });
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  const makeBody = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (refUuid) {
    makeBody.inherit_params = {
      collection_uuid: refUuid,
      picture_uuid: refUuid,
    };
  }

  const makeRes = await request('POST', 'https://api.talesofai.com/v3/make_image', makeBody);

  const taskUuid = typeof makeRes === 'string' ? makeRes : makeRes.task_uuid;
  if (!taskUuid) {
    console.error('✗ Failed to get task_uuid from API response:', JSON.stringify(makeRes));
    process.exit(1);
  }

  const pollUrl = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  const maxAttempts = 90;

  for (let i = 0; i < maxAttempts; i++) {
    await sleep(2000);
    const pollRes = await request('GET', pollUrl);
    const status = pollRes.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url =
      (pollRes.artifacts && pollRes.artifacts[0] && pollRes.artifacts[0].url) ||
      pollRes.result_image_url;

    if (url) {
      console.log(url);
      process.exit(0);
    } else {
      console.error('✗ Task finished but no image URL found:', JSON.stringify(pollRes));
      process.exit(1);
    }
  }

  console.error('✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch((err) => {
  console.error('✗ Unexpected error:', err.message);
  process.exit(1);
});
