#!/usr/bin/env node

// --- Argument parsing ---
const args = process.argv.slice(2);
let prompt = null;
let size = "portrait";
let token = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--size" && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === "--token" && args[i + 1]) {
    token = args[++i];
  } else if (args[i] === "--ref" && args[i + 1]) {
    refUuid = args[++i];
  } else if (!args[i].startsWith("--") && prompt === null) {
    prompt = args[i];
  }
}

if (!prompt) {
  prompt =
    "1990s high school yearbook portrait photo of a student, professional school photography studio, neutral background, soft studio lighting, formal attire, genuine smile, film grain texture, classic yearbook aesthetic";
}

// --- Token resolution ---
if (!token) {
  console.error(
    '\n✗ Token required. Pass via: --token YOUR_TOKEN'
  );
  process.exit(1);
}

// --- Size map ---
const sizeMap = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const { width, height } = sizeMap[size] || sizeMap.portrait;

// --- Headers ---
const headers = {
  "x-token": token,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

// --- Build request body ---
const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
  width,
  height,
  meta: { entrance: "PICTURE,VERSE" },
  context_model_series: "8_image_edit",
};

if (refUuid) {
  body.inherit_params = {
    collection_uuid: refUuid,
    picture_uuid: refUuid,
  };
}

// --- Submit job ---
async function main() {
  let taskUuid;

  const makeRes = await fetch("https://api.talesofai.cn/v3/make_image", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!makeRes.ok) {
    const text = await makeRes.text();
    console.error(`Error submitting job (${makeRes.status}): ${text}`);
    process.exit(1);
  }

  const makeData = await makeRes.json();

  if (typeof makeData === "string") {
    taskUuid = makeData;
  } else if (makeData && makeData.task_uuid) {
    taskUuid = makeData.task_uuid;
  } else {
    console.error("Unexpected response from make_image:", JSON.stringify(makeData));
    process.exit(1);
  }

  // --- Poll for result ---
  const maxAttempts = 90;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(
      `https://api.talesofai.cn/v1/artifact/task/${taskUuid}`,
      { headers }
    );

    if (!pollRes.ok) {
      const text = await pollRes.text();
      console.error(`Error polling task (${pollRes.status}): ${text}`);
      process.exit(1);
    }

    const pollData = await pollRes.json();
    const status = pollData.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      continue;
    }

    // Done
    const url =
      (pollData.artifacts && pollData.artifacts[0] && pollData.artifacts[0].url) ||
      pollData.result_image_url;

    if (!url) {
      console.error("No image URL in response:", JSON.stringify(pollData));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error("Timed out waiting for image generation.");
  process.exit(1);
}

main().catch((err) => {
  console.error("Fatal error:", err.message || err);
  process.exit(1);
});
