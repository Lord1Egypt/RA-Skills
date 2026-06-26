import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

const __filename = fileURLToPath(import.meta.url);
export const projectRoot = path.resolve(path.dirname(__filename), "..");

dotenv.config({ path: path.join(projectRoot, ".env"), quiet: true });

export const config = {
  curatedAihotUrl: process.env.CURATED_AIHOT_URL || process.env.AIHOT_URL || "https://aihot.virxact.com/",
  curatedAihotLimit: Number.parseInt(process.env.CURATED_AIHOT_LIMIT || process.env.AIHOT_LIMIT || "3", 10),
  wechatAppId: process.env.WECHAT_APPID || "",
  wechatAppSecret: process.env.WECHAT_APPSECRET || "",
  wechatAuthor: process.env.WECHAT_AUTHOR || "",
  wechatCreationSource: process.env.WECHAT_CREATION_SOURCE || "个人观点，仅供参考",
  wechatThumbMediaId: process.env.WECHAT_THUMB_MEDIA_ID || "",
  allowStaticCoverFallback: (process.env.ALLOW_STATIC_COVER_FALLBACK ?? "0") === "1",
  defaultCoverPath: process.env.DEFAULT_COVER_PATH || "assets/default-cover.jpg",
  dryRun: (process.env.DRY_RUN ?? "1") !== "0"
};

export const dataDir = path.join(projectRoot, "data");
export const sourcesDir = path.join(dataDir, "sources");
export const generatedDir = path.join(dataDir, "generated");
export const coversDir = path.join(dataDir, "covers");
export const imagesDir = path.join(dataDir, "images");
export const uploadImagesDir = path.join(dataDir, "upload-images");
export const statePath = path.join(dataDir, "state.json");
export const pendingPath = path.join(dataDir, "pending.json");

export function ensureDirs() {
  for (const dir of [dataDir, sourcesDir, generatedDir, coversDir, imagesDir, uploadImagesDir]) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

export function resolveProjectPath(inputPath) {
  if (!inputPath) return "";
  return path.isAbsolute(inputPath) ? inputPath : path.join(projectRoot, inputPath);
}
