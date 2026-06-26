/**
 * MedTravel ad — final assembly with narration + BGM + branded overlays.
 *
 * Pulls the already-generated v2 clips from R2 (NO Vidu spend), then:
 *   1. Generate 4 narration clips via OpenAI TTS (nova voice)
 *   2. Synthesize a soft ambient pad with ffmpeg sine waves
 *   3. Concat the 4 video shots
 *   4. Add top descriptive captions + bottom emerald-green brand overlays
 *   5. Mix audio: pad + narration delayed to each shot's start
 *   6. Compose final video with audio
 *   7. Upload to R2
 *
 * Iterate freely — this script never spends Vidu credits.
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

// Use Replicate for TTS (Kokoro 82M — fast, high quality, simple text input)
const REPLICATE_KEY = process.env.REPLICATE_API_KEY;
if (!REPLICATE_KEY) {
  console.error("ERROR: REPLICATE_API_KEY is not set");
  process.exit(1);
}

// Read shots back from R2 — uses your own bucket's public URL.
// This must match where make-xpilot-ad.ts uploaded them.
const R2_PUBLIC_URL = process.env.R2_PUBLIC_URL?.replace(/\/$/, "");
if (!R2_PUBLIC_URL) {
  console.error("ERROR: R2_PUBLIC_URL is not set");
  process.exit(1);
}
const R2_BASE = `${R2_PUBLIC_URL}/demo/medical-tourism-ad/v2`;

// ─── Storyboard ─────────────────────────────────────────────────────────────

type Shot = {
  file: string;       // R2 filename
  startSec: number;   // when this shot starts in the final video
  topCaption: string; // descriptive caption at top
  brandText: string;  // brand tagline at bottom
  narration: string;  // TTS voiceover for this shot
};

const SHOTS: Shot[] = [
  {
    file: "shot-1-sticker-shock",
    startSec: 0,
    topCaption: "The problem: U.S. dental costs",
    brandText: "Quality care should not cost a fortune",
    narration:
      "Dental implants in the United States can cost over twenty-five thousand dollars per tooth.",
  },
  {
    file: "shot-2-nanning-clinic",
    startSec: 8,
    topCaption: "MedTravel China — Nanning",
    brandText: "Premium clinics, German technology",
    narration:
      "MedTravel China brings you to Nanning, where world-class clinics use the same German equipment.",
  },
  {
    file: "shot-3-bama-wellness",
    startSec: 16,
    topCaption: "Recover in paradise — Bama & Guilin",
    brandText: "Healing landscapes, traditional wellness",
    narration:
      "Recover in paradise. Bama and Guilin offer healing landscapes and traditional wellness retreats.",
  },
  {
    file: "shot-4-detian-triumph",
    startSec: 24,
    topCaption: "Your new smile awaits",
    brandText: "Save 60-70 percent  ·  20-year warranty  ·  medtravel.jytech.us",
    narration:
      "Save up to seventy percent with a twenty-year warranty. Visit medtravel dot jytech dot us.",
  },
];

const TOTAL_DURATION = 30;

// ─── OpenAI TTS ─────────────────────────────────────────────────────────────

async function generateNarration(text: string, outPath: string): Promise<void> {
  // Use Replicate Kokoro (jaaari/kokoro) with synchronous "Prefer: wait" mode.
  // Community models require version-based predictions endpoint.
  const KOKORO_VERSION =
    "f559560eb822dc509045f3921a1921234918b91739db4bf3daab2169b71c7a13";
  const res = await fetch("https://api.replicate.com/v1/predictions", {
    method: "POST",
    headers: {
      Authorization: `Token ${REPLICATE_KEY}`,
      "Content-Type": "application/json",
      Prefer: "wait",
    },
    body: JSON.stringify({
      version: KOKORO_VERSION,
      input: {
        text,
        voice: "af_bella", // American Female - warm tone
        speed: 1.0,
      },
    }),
  });
  if (!res.ok) {
    throw new Error(`Replicate TTS failed (${res.status}): ${await res.text()}`);
  }
  const data = (await res.json()) as { output?: string | string[]; error?: string; status?: string };
  if (data.error) throw new Error(`Replicate error: ${data.error}`);

  const audioUrl = Array.isArray(data.output) ? data.output[0] : data.output;
  if (!audioUrl) throw new Error(`No audio output (status=${data.status})`);

  const audioRes = await fetch(audioUrl);
  if (!audioRes.ok) throw new Error(`Failed to download TTS audio: ${audioRes.status}`);
  const buf = Buffer.from(await audioRes.arrayBuffer());
  writeFileSync(outPath, buf);
}

// ─── Drawtext escape ────────────────────────────────────────────────────────

const FONT_FILE = "/System/Library/Fonts/Helvetica.ttc";

function escDrawtext(s: string): string {
  // Order matters: escape backslash first, then chars that have meaning
  // either inside text='...' or at the filtergraph level (commas/semicolons
  // separate filters even inside quotes).
  return s
    .replace(/\\/g, "\\\\")
    .replace(/'/g, "\\'")
    .replace(/:/g, "\\:")
    .replace(/%/g, "\\%")
    .replace(/,/g, "\\,")
    .replace(/;/g, "\\;");
}

/**
 * Build video filter graph as a list of (drawtext, label) chains so commas
 * inside text= can never break filter parsing. Returns the chain string AND
 * the final output label to use in the outer filter_complex.
 */
function buildVideoChains(): { chains: string; outLabel: string } {
  const chains: string[] = [];
  let prevLabel = "0:v";
  let counter = 0;

  const drawtext = (
    text: string,
    fontsize: number,
    boxcolor: string,
    y: string,
    start: number,
    end: number,
  ): string =>
    [
      `drawtext=fontfile=${FONT_FILE}`,
      `text='${escDrawtext(text)}'`,
      `fontcolor=white`,
      `fontsize=${fontsize}`,
      `box=1`,
      `boxcolor=${boxcolor}`,
      `boxborderw=16`,
      `x=(w-text_w)/2`,
      `y=${y}`,
      `enable='between(t\\,${start}\\,${end})'`,
    ].join(":");

  for (const shot of SHOTS) {
    const start = shot.startSec + 0.5;
    const end = Math.min(shot.startSec + 7.5, TOTAL_DURATION - 0.2);

    // Top descriptive caption
    counter++;
    const topLabel = `v${counter}`;
    chains.push(
      `[${prevLabel}]${drawtext(shot.topCaption, 32, "black@0.55", "60", start, end)}[${topLabel}]`,
    );
    prevLabel = topLabel;

    // Bottom brand text in emerald green
    counter++;
    const bottomLabel = `v${counter}`;
    chains.push(
      `[${prevLabel}]${drawtext(shot.brandText, 38, "0x10b981@0.85", "h-160", start, end)}[${bottomLabel}]`,
    );
    prevLabel = bottomLabel;
  }

  return { chains: chains.join(";"), outLabel: prevLabel };
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function main() {
  const overallStart = Date.now();
  const tmp = mkdtempSync(join(tmpdir(), "xpilot-ad-fin-"));
  const ffmpeg = ffmpegPath || "ffmpeg";

  // 1. Download 4 video shots from R2
  console.log("→ Downloading 4 shots from R2...");
  const localVideoPaths: string[] = [];
  for (const shot of SHOTS) {
    const url = `${R2_BASE}/${shot.file}.mp4`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    const localPath = join(tmp, `${shot.file}.mp4`);
    writeFileSync(localPath, buf);
    localVideoPaths.push(localPath);
    console.log(`  ✓ ${shot.file}`);
  }

  // 2. Generate 4 narration clips with Replicate Kokoro
  console.log("\n→ Generating 4 narration clips (Replicate Kokoro, voice=af_bella)...");
  const narrationPaths: string[] = [];
  for (let i = 0; i < SHOTS.length; i++) {
    const shot = SHOTS[i];
    if (i > 0) {
      // Replicate rate limit: 6 req/min with burst of 1 for accounts < $5 credit.
      // 11s delay keeps us safely under the limit.
      console.log("  · waiting 11s for Replicate rate limit...");
      await new Promise((r) => setTimeout(r, 11000));
    }
    const out = join(tmp, `narration-${shot.file}.mp3`);
    await generateNarration(shot.narration, out);
    const size = readFileSync(out).length;
    console.log(`  ✓ ${shot.file}: ${(size / 1024).toFixed(0)} KB`);
    narrationPaths.push(out);
  }

  // 3. Concat the 4 video shots (no audio)
  console.log("\n→ Concatenating 4 video shots...");
  const listPath = join(tmp, "concat.txt");
  writeFileSync(
    listPath,
    localVideoPaths.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join("\n"),
  );
  const concatLocal = join(tmp, "concat.mp4");
  execFileSync(
    ffmpeg,
    ["-f", "concat", "-safe", "0", "-i", listPath, "-c", "copy", "-an", "-y", concatLocal],
    { stdio: "pipe" },
  );
  console.log("  ✓ Done");

  // 4. Compose final: video filters + audio mix in one ffmpeg pass
  console.log("\n→ Composing final video (overlays + narration + ambient pad)...");
  const finalLocal = join(tmp, "medtravel-final.mp4");
  const { chains: videoChains, outLabel: videoOutLabel } = buildVideoChains();

  // Build filter_complex:
  //   [0:v]drawtext=...[v]
  //   [1:a]adelay=0|0[n1]
  //   [2:a]adelay=8000|8000[n2]
  //   [3:a]adelay=16000|16000[n3]
  //   [4:a]adelay=24000|24000[n4]
  //   sine pads → mix → soft pad
  //   [n1][n2][n3][n4][pad]amix=inputs=5[aout]
  const audioParts: string[] = [];
  for (let i = 0; i < SHOTS.length; i++) {
    const delayMs = SHOTS[i].startSec * 1000;
    audioParts.push(`[${i + 1}:a]adelay=${delayMs}|${delayMs},volume=1.6[n${i}]`);
  }
  // Three sine waves forming a soft C-major triad pad (C4, E4, G4)
  audioParts.push(
    `[5:a][6:a][7:a]amix=inputs=3:duration=first,volume=0.35,lowpass=f=900,afade=t=in:d=2:curve=qsin,afade=t=out:st=28:d=2:curve=qsin[pad]`,
  );
  audioParts.push(
    `[n0][n1][n2][n3][pad]amix=inputs=5:duration=longest:dropout_transition=0,alimiter=limit=0.95[aout]`,
  );

  const filterComplex = `${videoChains};${audioParts.join(";")}`;

  execFileSync(
    ffmpeg,
    [
      "-i", concatLocal,
      "-i", narrationPaths[0],
      "-i", narrationPaths[1],
      "-i", narrationPaths[2],
      "-i", narrationPaths[3],
      "-f", "lavfi", "-t", "30", "-i", "sine=frequency=261.63",
      "-f", "lavfi", "-t", "30", "-i", "sine=frequency=329.63",
      "-f", "lavfi", "-t", "30", "-i", "sine=frequency=392.00",
      "-filter_complex", filterComplex,
      "-map", `[${videoOutLabel}]`,
      "-map", "[aout]",
      "-c:v", "libx264", "-preset", "fast", "-crf", "20",
      "-c:a", "aac", "-b:a", "192k",
      "-shortest",
      "-y", finalLocal,
    ],
    { stdio: "pipe" },
  );

  const finalBuf = readFileSync(finalLocal);
  console.log(`  ✓ Final size: ${(finalBuf.length / 1024 / 1024).toFixed(2)} MB`);

  // 5. Upload to R2
  const finalUploaded = await put(
    "demo/medical-tourism-ad/v2/medtravel-final.mp4",
    finalBuf,
    { contentType: "video/mp4", addRandomSuffix: false },
  );

  const totalSec = Math.round((Date.now() - overallStart) / 1000);
  console.log("\n========================================");
  console.log(`✓ Done in ${totalSec}s`);
  console.log("========================================");
  console.log(`🎬 Final ad: ${finalUploaded.url}`);
}

main().catch((e) => {
  if (e instanceof Error && "stderr" in e) {
    console.error("\nffmpeg stderr:");
    console.error((e as { stderr?: Buffer }).stderr?.toString());
  }
  console.error("\nFatal:", e instanceof Error ? e.message : e);
  process.exit(1);
});
