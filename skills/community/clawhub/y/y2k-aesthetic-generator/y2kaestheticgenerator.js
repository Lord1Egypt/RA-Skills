#!/usr/bin/env node
// Y2K Aesthetic Generator — Neta AI image generation CLI

const DEFAULT_PROMPT = "Y2K aesthetic portrait, early 2000s digital camera flash photography, slightly overblown highlights, low-res nostalgic quality, vibrant saturated colors, butterfly clips, frosted lip gloss, low-rise denim, chunky sneakers, candid pose, 2000s mall photo booth vibe, soft grain, nostalgic dreamy mood";

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

function parseArgs(argv) {
  const args = { prompt: null, size: "portrait", token: null, ref: null };
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === "--size")       { args.size  = rest[++i]; }
    else if (a === "--token") { args.token = rest[++i]; }
    else if (a === "--ref")   { args.ref   = rest[++i]; }
    else if (a === "--help" || a === "-h") { args.help = true; }
    else if (!a.startsWith("--") && args.prompt === null) { args.prompt = a; }
  }
  return args;
}

function printHelp() {
  console.log(`Y2K Aesthetic Generator

Usage:
  node y2kaestheticgenerator.js "<prompt>" [options]

Options:
  --size <portrait|landscape|square|tall>   Output size (default: portrait)
  --token <TOKEN>                           Neta API token (required)
  --ref <picture_uuid>                      Reference image UUID for style inheritance
  --help, -h                                Show this help

Get a free token at: https://www.neta.art/open/
`);
}

async function createTask({ token, prompt, width, height, ref }) {
  const body = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };
  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  const res = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers: {
      "x-token": token,
      "x-platform": "nieta-app/web",
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`make_image failed: ${res.status} ${res.statusText} ${text}`);
  }

  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) {
    const data = await res.json();
    if (typeof data === "string") return data;
    if (data && data.task_uuid) return data.task_uuid;
    throw new Error(`Unexpected response: ${JSON.stringify(data)}`);
  }
  const text = (await res.text()).trim().replace(/^"|"$/g, "");
  if (!text) throw new Error("Empty task_uuid response");
  return text;
}

async function pollTask({ token, taskUuid }) {
  const url = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise(r => setTimeout(r, 2000));
    const res = await fetch(url, {
      headers: {
        "x-token": token,
        "x-platform": "nieta-app/web",
        "content-type": "application/json",
      },
    });
    if (!res.ok) continue;
    const data = await res.json();
    const status = data.task_status;
    if (status === "PENDING" || status === "MODERATION") continue;
    const artifactUrl =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;
    if (artifactUrl) return artifactUrl;
    throw new Error(`Task ended without image. Status: ${status}. Response: ${JSON.stringify(data)}`);
  }
  throw new Error("Timed out waiting for image (180s)");
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) { printHelp(); process.exit(0); }

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = args.prompt || DEFAULT_PROMPT;
  const sizeKey = (args.size || "portrait").toLowerCase();
  const dims = SIZES[sizeKey];
  if (!dims) {
    console.error(`✗ Invalid --size: ${args.size}. Use one of: ${Object.keys(SIZES).join(", ")}`);
    process.exit(1);
  }

  try {
    const taskUuid = await createTask({
      token: TOKEN,
      prompt: PROMPT,
      width: dims.width,
      height: dims.height,
      ref: args.ref,
    });
    const imageUrl = await pollTask({ token: TOKEN, taskUuid });
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error(`✗ ${err.message || err}`);
    process.exit(1);
  }
}

main();
