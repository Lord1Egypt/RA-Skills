#!/usr/bin/env node
import https from "https";

const args = process.argv.slice(2);

const prompt =
  args.find((a) => !a.startsWith("--")) ||
  "webtoon manhwa style character portrait, clean crisp line art, highly expressive large eyes, vibrant saturated colors, smooth cel shading, dynamic pose, modern Korean webtoon aesthetic, white background, full body or bust";

const sizeFlag = args[args.indexOf("--size") + 1] || "portrait";
const tokenFlag = args[args.indexOf("--token") + 1] || null;
const refFlag = args.includes("--ref") ? args[args.indexOf("--ref") + 1] : null;

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error("\n✗ Token required. Pass via: --token YOUR_TOKEN");
  console.error("  Get yours at: https://www.neta.art/open/");
  process.exit(1);
}

const SIZES = {
  square: [1024, 1024],
  portrait: [832, 1216],
  landscape: [1216, 832],
  tall: [704, 1408],
};

const [width, height] = SIZES[sizeFlag] || SIZES.portrait;

function request(method, url, body) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method,
      headers: {
        "x-token": TOKEN,
        "x-platform": "nieta-app/web",
        "content-type": "application/json",
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data.trim());
        }
      });
    });

    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  const body = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };

  if (refFlag) {
    body.inherit_params = {
      collection_uuid: refFlag,
      picture_uuid: refFlag,
    };
  }

  const makeRes = await request(
    "POST",
    "https://api.talesofai.com/v3/make_image",
    body
  );

  const taskUuid =
    typeof makeRes === "string"
      ? makeRes
      : makeRes.task_uuid || makeRes;

  if (!taskUuid || typeof taskUuid !== "string") {
    console.error("✗ Failed to get task UUID:", JSON.stringify(makeRes));
    process.exit(1);
  }

  for (let i = 0; i < 90; i++) {
    await sleep(2000);
    const poll = await request(
      "GET",
      `https://api.talesofai.com/v1/artifact/task/${taskUuid}`
    );

    const status = poll.task_status;
    if (status === "PENDING" || status === "MODERATION") continue;

    const url =
      poll.artifacts?.[0]?.url || poll.result_image_url;

    if (url) {
      console.log(url);
      process.exit(0);
    } else {
      console.error("✗ Task finished but no image URL found:", JSON.stringify(poll));
      process.exit(1);
    }
  }

  console.error("✗ Timed out waiting for image generation.");
  process.exit(1);
}

main().catch((err) => {
  console.error("✗ Unexpected error:", err.message);
  process.exit(1);
});
