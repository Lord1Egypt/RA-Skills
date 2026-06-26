/**
 * MedTravel China — 30s Ad v2 (Reference-to-Video edition)
 *
 * v1 vs v2:
 *   v1 used Vidu text2video (4 independent shots, no character continuity).
 *   v2 generates ONE character reference image with FLUX, then uses Vidu's
 *   reference2video so the same protagonist appears in all 4 scenes.
 *
 * Pipeline:
 *   0. FLUX-2-Pro generates a portrait of the protagonist → upload to R2
 *   1. Submit 4 Vidu reference2video tasks (parallel), all using the same
 *      reference image, audio disabled (we'll add BGM in post)
 *   2. Poll all in parallel until success
 *   3. Download each clip → upload to R2 demo/medical-tourism-ad/v2/
 *   4. ffmpeg concat → silent 30s
 *   5. ffmpeg drawtext → brand overlays per shot
 *   6. Upload final to R2: demo/medical-tourism-ad/v2/final.mp4
 *
 * Usage:
 *   npx tsx make-xpilot-ad.ts
 */
import "dotenv/config";
import { config as loadEnv } from "dotenv";
loadEnv({ path: ".env.local" });

import { put } from "./lib/r2";
import { writeFileSync, readFileSync, mkdtempSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { execFileSync } from "child_process";
import ffmpegPath from "ffmpeg-static";
import { submitImage, pollImage } from "./lib/wavespeed";

const VIDU_KEY = process.env.VIDU_API_KEY;
if (!VIDU_KEY) {
  console.error("ERROR: VIDU_API_KEY is not set");
  process.exit(1);
}
if (!process.env.WAVESPEED_API_KEY) {
  console.error("ERROR: WAVESPEED_API_KEY is not set");
  process.exit(1);
}

const VIDU_BASE = "https://api.vidu.com/ent/v2";

// ─── Storyboard ─────────────────────────────────────────────────────────────

const REFERENCE_PROMPT =
  "Photorealistic portrait of a friendly middle-aged American man, age 50, " +
  "salt-and-pepper hair, warm genuine smile, wearing a casual light blue " +
  "button-up shirt, soft natural window lighting, neutral cream background, " +
  "professional photography, sharp focus on face, 4K high detail";

const SHOTS: { name: string; duration: number; prompt: string }[] = [
  {
    name: "shot-1-sticker-shock",
    duration: 8,
    prompt:
      "The man sits at a wooden kitchen table at night under warm lamp light, " +
      "looking down at a stack of medical bills and dental treatment estimates, " +
      "his face showing worry and stress. Cool moonlight from a window in the " +
      "background, rainy city skyline outside. Cinematic, shallow depth of field, " +
      "slow push-in on his concerned face.",
  },
  {
    name: "shot-2-nanning-clinic",
    duration: 8,
    prompt:
      "The man stands in the bright, ultra-modern lobby of a dental clinic in " +
      "Nanning, China. Floor-to-ceiling windows with warm morning sunlight, " +
      "polished wood and white marble floors, lush tropical plants. A friendly " +
      "Chinese dental coordinator in a crisp white coat warmly welcomes him at " +
      "a sleek reception desk. Modern 3D dental imaging equipment visible in " +
      "background. Cinematic, warm professional lighting.",
  },
  {
    name: "shot-3-bama-wellness",
    duration: 8,
    prompt:
      "The man relaxes on a bamboo lounge chair on a wooden deck in Bama, " +
      "Guangxi, holding a small cup of green tea, eyes closed peacefully. " +
      "Behind him: misty karst mountains of Guilin, distant rice terraces, soft " +
      "morning fog rising. Warm golden hour light, peaceful and healing " +
      "atmosphere, cinematic wide shot.",
  },
  {
    name: "shot-4-detian-triumph",
    duration: 6,
    prompt:
      "The man stands smiling confidently with bright white teeth in front of " +
      "the spectacular Detian Waterfall on the China-Vietnam border. Lush " +
      "green jungle and massive cascading waterfall behind him, mist in the " +
      "air, golden hour light, slight lens flare. He raises his arms in joyful " +
      "triumph. Slow motion, triumphant cinematic ending.",
  },
];

// Brand overlay text — timing matches concatenated video (cumulative seconds)
const OVERLAYS = [
  { start: 1, end: 7, text: "Dental work shouldn't cost a fortune" },
  { start: 9, end: 15, text: "MedTravel China  |  Premium care in Guangxi" },
  { start: 17, end: 23, text: "Heal in paradise" },
  { start: 24.5, end: 29.5, text: "Save 60-70%   20-year warranty   medtravel.jytech.us" },
];

// ─── Reference image generation ────────────────────────────────────────────

async function generateReferenceImage(): Promise<string> {
  console.log("→ Generating protagonist reference image (Wavespeed Seedream 4.5)...");

  // Submit
  const task = await submitImage("bytedance/seedream-v4.5", REFERENCE_PROMPT);
  const pollUrl = task.urls?.get || task.id;
  console.log(`  ✓ Submitted: ${pollUrl}`);

  // Poll
  const startedAt = Date.now();
  const TIMEOUT_MS = 5 * 60 * 1000;
  let imageUrl: string | undefined;

  while (Date.now() - startedAt < TIMEOUT_MS) {
    await new Promise((r) => setTimeout(r, 3000));
    try {
      const polled = await pollImage(pollUrl);
      if (polled.status === "completed" && polled.outputs?.[0]) {
        imageUrl = polled.outputs[0];
        break;
      }
      if (polled.status === "failed") {
        throw new Error("Image generation failed");
      }
    } catch (e) {
      console.log(`  ! poll error: ${e instanceof Error ? e.message : e}`);
    }
  }
  if (!imageUrl) throw new Error("Image generation timed out");

  console.log(`  ✓ Image generated: ${imageUrl}`);

  // Download and mirror to R2 (Wavespeed URLs may also be short-lived)
  const dlRes = await fetch(imageUrl);
  if (!dlRes.ok) throw new Error(`Failed to download generated image: ${dlRes.status}`);
  const buf = Buffer.from(await dlRes.arrayBuffer());
  console.log(`  ✓ Downloaded ${(buf.length / 1024).toFixed(0)} KB`);

  const uploaded = await put("demo/medical-tourism-ad/v2/reference-protagonist.png", buf, {
    contentType: "image/png",
    addRandomSuffix: false,
  });
  console.log(`  ✓ R2: ${uploaded.url}`);
  return uploaded.url;
}

// ─── Vidu reference2video ──────────────────────────────────────────────────

async function submit(prompt: string, duration: number, referenceUrl: string): Promise<string> {
  const res = await fetch(`${VIDU_BASE}/reference2video`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${VIDU_KEY}`,
    },
    body: JSON.stringify({
      model: "viduq2-pro",
      images: [referenceUrl],
      prompt,
      duration,
      aspect_ratio: "16:9",
      resolution: "720p",
      movement_amplitude: "auto",
      audio: false, // we'll add BGM in post
    }),
  });
  if (!res.ok) {
    throw new Error(`Vidu submit failed (${res.status}): ${await res.text()}`);
  }
  const data = (await res.json()) as { task_id: string };
  return data.task_id;
}

type PollResult = { url: string; cover_url?: string; credits?: number };

async function poll(taskId: string, label: string): Promise<PollResult> {
  const startedAt = Date.now();
  const TIMEOUT_MS = 15 * 60 * 1000;
  let lastState = "";

  while (Date.now() - startedAt < TIMEOUT_MS) {
    await new Promise((r) => setTimeout(r, 5000));

    let res: Response;
    try {
      res = await fetch(`${VIDU_BASE}/tasks/${taskId}/creations`, {
        headers: { Authorization: `Token ${VIDU_KEY}` },
      });
    } catch {
      continue;
    }
    if (!res.ok) continue;

    const data = (await res.json()) as {
      state: string;
      err_code?: string;
      credits?: number;
      creations?: { id: string; url: string; cover_url?: string }[];
    };

    if (data.state !== lastState) {
      const elapsed = Math.round((Date.now() - startedAt) / 1000);
      console.log(`  [${label}] [${elapsed}s] state=${data.state}`);
      lastState = data.state;
    }

    if (data.state === "success") {
      const c = data.creations?.[0];
      if (!c) throw new Error(`Task ${taskId} success but no creations`);
      return { url: c.url, cover_url: c.cover_url, credits: data.credits };
    }
    if (data.state === "failed") {
      throw new Error(`Task ${taskId} failed: ${data.err_code || "unknown"}`);
    }
  }
  throw new Error(`Task ${taskId} timed out after 15min`);
}

// ─── Brand overlay (ffmpeg drawtext) ───────────────────────────────────────

function buildDrawtextFilter(): string {
  // macOS Helvetica path
  const fontFile = "/System/Library/Fonts/Helvetica.ttc";

  return OVERLAYS.map((o) => {
    // Escape: ' (apostrophe), : (colon), \\ (backslash) — drawtext text needs careful escaping
    const text = o.text.replace(/'/g, "\\'").replace(/:/g, "\\:");
    return [
      `drawtext=fontfile=${fontFile}`,
      `text='${text}'`,
      `fontcolor=white`,
      `fontsize=42`,
      `box=1`,
      `boxcolor=black@0.55`,
      `boxborderw=18`,
      `x=(w-text_w)/2`,
      `y=h-160`,
      `enable='between(t,${o.start},${o.end})'`,
    ].join(":");
  }).join(",");
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function main() {
  console.log("=== MedTravel China — 30s Ad v2 (Reference-to-Video) ===\n");
  const overallStart = Date.now();

  // Step 0: Generate reference image
  const referenceUrl = await generateReferenceImage();

  // Step 1: Submit 4 in parallel
  console.log("\n→ Submitting 4 reference2video shots in parallel...");
  const taskIds = await Promise.all(
    SHOTS.map(async (s) => {
      const id = await submit(s.prompt, s.duration, referenceUrl);
      console.log(`  ✓ ${s.name}: task_id=${id}`);
      return id;
    }),
  );

  // Step 2: Poll all in parallel
  console.log("\n→ Polling all tasks (parallel)...");
  const results = await Promise.all(
    taskIds.map((id, i) => poll(id, SHOTS[i].name)),
  );

  // Step 3: Download + R2
  const tmp = mkdtempSync(join(tmpdir(), "xpilot-ad-"));
  const localPaths: string[] = [];
  let totalCredits = 0;
  const r2Urls: string[] = [];

  for (let i = 0; i < SHOTS.length; i++) {
    const shot = SHOTS[i];
    const result = results[i];
    totalCredits += result.credits || 0;

    console.log(`\n→ Processing ${shot.name} (${result.credits} credits)...`);
    const dlRes = await fetch(result.url);
    if (!dlRes.ok) throw new Error(`Download failed: ${dlRes.status}`);
    const buf = Buffer.from(await dlRes.arrayBuffer());
    console.log(`  ✓ Downloaded ${(buf.length / 1024 / 1024).toFixed(2)} MB`);

    const localPath = join(tmp, `${shot.name}.mp4`);
    writeFileSync(localPath, buf);
    localPaths.push(localPath);

    const uploaded = await put(
      `demo/medical-tourism-ad/v2/${shot.name}.mp4`,
      buf,
      { contentType: "video/mp4", addRandomSuffix: false },
    );
    r2Urls.push(uploaded.url);
    console.log(`  ✓ R2: ${uploaded.url}`);
  }

  // Step 4: Concat
  console.log("\n→ Concatenating with ffmpeg...");
  const listPath = join(tmp, "concat.txt");
  writeFileSync(
    listPath,
    localPaths.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join("\n"),
  );
  const concatLocal = join(tmp, "concat.mp4");
  const ffmpeg = ffmpegPath || "ffmpeg";

  try {
    execFileSync(
      ffmpeg,
      ["-f", "concat", "-safe", "0", "-i", listPath, "-c", "copy", "-y", concatLocal],
      { stdio: "pipe" },
    );
    console.log("  ✓ Concat (stream copy)");
  } catch {
    console.log("  ! Stream copy failed, re-encoding...");
    execFileSync(
      ffmpeg,
      [
        "-f", "concat", "-safe", "0", "-i", listPath,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-an",
        "-y", concatLocal,
      ],
      { stdio: "pipe" },
    );
    console.log("  ✓ Concat (re-encoded)");
  }

  // Step 5: Brand overlays
  console.log("\n→ Adding brand text overlays...");
  const finalLocal = join(tmp, "medtravel-final.mp4");
  const drawtextFilter = buildDrawtextFilter();

  execFileSync(
    ffmpeg,
    [
      "-i", concatLocal,
      "-vf", drawtextFilter,
      "-c:v", "libx264", "-preset", "fast", "-crf", "20",
      "-an",
      "-y", finalLocal,
    ],
    { stdio: "pipe" },
  );
  console.log("  ✓ Overlays added");

  const finalBuf = readFileSync(finalLocal);
  console.log(`  ✓ Final size: ${(finalBuf.length / 1024 / 1024).toFixed(2)} MB`);

  const finalUploaded = await put(
    "demo/medical-tourism-ad/v2/medtravel-final.mp4",
    finalBuf,
    { contentType: "video/mp4", addRandomSuffix: false },
  );

  // Summary
  const totalSec = Math.round((Date.now() - overallStart) / 1000);
  console.log("\n========================================");
  console.log("✓ MedTravel China v2 ad complete");
  console.log("========================================");
  console.log(`Total time:    ${Math.floor(totalSec / 60)}m ${totalSec % 60}s`);
  console.log(`Total credits: ${totalCredits} (≈ $${(totalCredits / 100).toFixed(2)})`);
  console.log(`Reference:     ${referenceUrl}`);
  console.log("\nIndividual shots:");
  for (let i = 0; i < r2Urls.length; i++) {
    console.log(`  ${SHOTS[i].name}: ${r2Urls[i]}`);
  }
  console.log(`\n🎬 Final ad: ${finalUploaded.url}`);
}

main().catch((e) => {
  console.error("\nFatal error:", e);
  process.exit(1);
});
