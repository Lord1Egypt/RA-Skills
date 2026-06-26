#!/usr/bin/env node
// Steampunk Art Generator — powered by Neta AI (api.talesofai.com)

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = 'portrait';
let tokenFlag = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--token' && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === '--size' && args[i + 1]) {
    size = args[++i];
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
  prompt = 'steampunk portrait, Victorian era brass gears and clockwork machinery, leather and copper aesthetic, ornate goggles, steam-powered devices, industrial fantasy, dramatic gaslight lighting, detailed mechanical embellishments, rich warm tones';
}

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const dims = SIZES[size] ?? SIZES.portrait;

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
    width: dims.width,
    height: dims.height,
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
    console.error(`✗ Image request failed (${res.status}): ${text}`);
    process.exit(1);
  }

  const data = await res.json();
  const taskUuid = typeof data === 'string' ? data : data.task_uuid;

  if (!taskUuid) {
    console.error('✗ No task_uuid in response:', JSON.stringify(data));
    process.exit(1);
  }

  console.error(`Generating image (task: ${taskUuid})...`);

  // Poll for result
  const MAX_ATTEMPTS = 90;
  const POLL_INTERVAL_MS = 2000;

  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));

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
      console.error('✗ No image URL in result:', JSON.stringify(result));
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
