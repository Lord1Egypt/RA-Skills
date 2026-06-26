#!/usr/bin/env node
// Vaporwave Art Generator — AI-powered vaporwave image generation via Neta API

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = '';
let size = 'landscape';
let tokenFlag = '';
let refUuid = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--token' && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === '--size' && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === '--ref' && args[i + 1]) {
    refUuid = args[++i];
  } else if (!args[i].startsWith('--')) {
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
  prompt = 'synthwave vaporwave aesthetic, retro 1980s neon colors, pink and purple gradients, glowing neon grid floor, palm trees silhouette, retro computer graphics, chrome reflective surfaces, retrowave sunset, lo-fi dreamy atmosphere, glitch effects, pastel sky';
}

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const { width, height } = SIZES[size] ?? SIZES.landscape;

const HEADERS = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

async function makeImage() {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (refUuid) {
    body.inherit_params = {
      collection_uuid: refUuid,
      picture_uuid: refUuid,
    };
  }

  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error(`✗ Failed to start image generation (${res.status}): ${text}`);
    process.exit(1);
  }

  const data = await res.json();
  const taskUuid = typeof data === 'string' ? data : data.task_uuid;

  if (!taskUuid) {
    console.error('✗ No task_uuid returned:', JSON.stringify(data));
    process.exit(1);
  }

  console.error(`Generating image (task: ${taskUuid})...`);

  // Poll for result
  const maxAttempts = 90;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise(r => setTimeout(r, 2000));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers: HEADERS,
    });

    if (!pollRes.ok) {
      console.error(`✗ Poll failed (${pollRes.status})`);
      process.exit(1);
    }

    const result = await pollRes.json();
    const status = result.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      process.stderr.write('.');
      continue;
    }

    // Done
    process.stderr.write('\n');
    const url =
      result.artifacts?.[0]?.url ??
      result.result_image_url;

    if (!url) {
      console.error('✗ No image URL in response:', JSON.stringify(result));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error('\n✗ Timed out waiting for image generation.');
  process.exit(1);
}

makeImage().catch(err => {
  console.error('✗ Unexpected error:', err.message);
  process.exit(1);
});
