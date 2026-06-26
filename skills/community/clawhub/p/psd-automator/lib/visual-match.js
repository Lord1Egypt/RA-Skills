import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import sharp from "sharp";

const MAX_CANDIDATES = 5;
const IMAGE_EXT_RE = /\.(png|jpe?g|gif|webp)$/i;

// Comparison size for aspect-ratio-aware matching.
// Using "contain" keeps both images' layouts intact instead of cropping.
const COMPARE_LONG_EDGE = 256;

function clamp01(value) {
  if (value < 0) return 0;
  if (value > 1) return 1;
  return value;
}

/**
 * Load image pixels at a standardized size while PRESERVING aspect ratio.
 * Both images are scaled so their long edge = targetLongEdge, then padded
 * with white to fill a square canvas. This avoids the content-destructive
 * "cover" crop that the old algorithm used.
 */
async function loadComparableRaw(imagePath, targetLongEdge) {
  return sharp(imagePath)
    .resize(targetLongEdge, targetLongEdge, {
      fit: "contain",
      background: { r: 255, g: 255, b: 255 },
    })
    .grayscale()
    .raw()
    .toBuffer();
}

/**
 * Normalised Mean-Squared-Error between two same-length raw pixel buffers.
 * Returns 0..1 where 0 = identical.
 */
function nrmse(a, b) {
  const len = Math.min(a.length, b.length);
  if (len === 0) return 1;
  let sum = 0;
  for (let i = 0; i < len; i += 1) {
    const d = a[i] - b[i];
    sum += d * d;
  }
  return Math.sqrt(sum / len) / 255;
}

/**
 * Simple histogram intersection (8-bin greyscale).
 * Returns 0..1 where 1 = identical histograms.
 */
function histogramIntersection(a, b) {
  const bins = 8;
  const binWidth = 256 / bins;
  const histA = new Float64Array(bins);
  const histB = new Float64Array(bins);
  for (let i = 0; i < a.length; i += 1) {
    histA[Math.min(Math.floor(a[i] / binWidth), bins - 1)] += 1;
  }
  for (let i = 0; i < b.length; i += 1) {
    histB[Math.min(Math.floor(b[i] / binWidth), bins - 1)] += 1;
  }
  // Normalise to sum=1
  const sumA = a.length || 1;
  const sumB = b.length || 1;
  let intersection = 0;
  for (let i = 0; i < bins; i += 1) {
    intersection += Math.min(histA[i] / sumA, histB[i] / sumB);
  }
  return intersection;
}

function scoreToReason(score) {
  if (score >= 0.85) return "Strong visual match (pixel + histogram).";
  if (score >= 0.70) return "Medium visual match.";
  return "Weak visual match.";
}

export async function rankImagesByVisualSimilarity(params) {
  const referenceImagePath = String(params.referenceImagePath || "").trim();
  const candidatePaths = Array.isArray(params.candidatePaths) ? params.candidatePaths : [];
  if (!referenceImagePath || candidatePaths.length === 0) {
    return [];
  }

  const refRaw = await loadComparableRaw(referenceImagePath, COMPARE_LONG_EDGE);

  const ranked = [];
  for (const candidatePath of candidatePaths) {
    try {
      const candRaw = await loadComparableRaw(candidatePath, COMPARE_LONG_EDGE);
      const pixelDist = nrmse(refRaw, candRaw);
      const histSim = histogramIntersection(refRaw, candRaw);
      // Pixel similarity (60%) + histogram similarity (40%)
      const score = clamp01((1 - pixelDist) * 0.6 + histSim * 0.4);
      ranked.push({
        path: candidatePath,
        score,
        reason: scoreToReason(score),
      });
    } catch (_err) {
      // Ignore unreadable images and continue ranking.
    }
  }

  ranked.sort((a, b) => b.score - a.score);
  return ranked.slice(0, MAX_CANDIDATES);
}

/**
 * Compute a content-based pixel hash for each image in a directory.
 * Uses raw pixel data (resized to a small fixed size) so that metadata
 * or JPEG re-encoding jitter doesn't cause false positives.
 * Also scans the "images/" subdirectory (Photoshop Save-for-Web convention).
 */
export async function snapshotDirectoryHashes(dirPath) {
  const result = new Map();
  if (!dirPath || !fs.existsSync(dirPath)) return result;

  const dirsToScan = [dirPath];
  const imagesSub = path.join(dirPath, "images");
  if (fs.existsSync(imagesSub)) {
    try {
      if (fs.statSync(imagesSub).isDirectory()) dirsToScan.push(imagesSub);
    } catch { /* ignore */ }
  }

  for (const dir of dirsToScan) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of entries) {
      if (!entry.isFile() || !IMAGE_EXT_RE.test(entry.name)) continue;
      const filePath = path.join(dir, entry.name);
      try {
        const raw = await sharp(filePath)
          .resize(64, 64, { fit: "fill" })
          .raw()
          .toBuffer();
        const hash = createHash("sha256").update(raw).digest("hex");
        result.set(filePath, hash);
      } catch {
        // skip unreadable files
      }
    }
  }
  return result;
}

/**
 * Given before/after hash snapshots, return the list of files whose
 * pixel content changed (or that are newly added).
 */
export function findChangedFiles(before, after) {
  const changed = [];
  for (const [filePath, hash] of after) {
    const oldHash = before.get(filePath);
    if (!oldHash || oldHash !== hash) {
      changed.push(filePath);
    }
  }
  return changed;
}
