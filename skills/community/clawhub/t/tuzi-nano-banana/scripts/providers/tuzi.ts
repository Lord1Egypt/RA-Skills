import path from "node:path";
import { readFile } from "node:fs/promises";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "gemini-3-pro-image-preview";

export function getDefaultModel(): string {
  return process.env.TUZI_IMAGE_MODEL || DEFAULT_MODEL;
}

function getApiKey(): string | null {
  return process.env.TUZI_API_KEY || null;
}

function getBaseUrl(): string {
  const base = process.env.TUZI_BASE_URL || "https://api.tu-zi.com/v1";
  return base.replace(/\/+$/g, "");
}

const QUALITY_MODELS = ["gemini-3.1-flash-image-preview", "gemini-3-pro-image-preview"];

function supportsQuality(model: string): boolean {
  return QUALITY_MODELS.some((id) => model === id);
}

function resolutionToQuality(resolution: string): string {
  if (resolution === "4K") return "4k";
  if (resolution === "2K") return "2k";
  return "1k";
}

type SyncResponse = { data: Array<{ url?: string; b64_json?: string; revised_prompt?: string }> };

async function downloadImage(url: string): Promise<Uint8Array> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to download image: ${res.status}`);
  return new Uint8Array(await res.arrayBuffer());
}

async function readImageAsBase64DataUrl(p: string): Promise<string> {
  const buf = await readFile(p);
  const ext = path.extname(p).toLowerCase();
  let mime = "image/png";
  if (ext === ".jpg" || ext === ".jpeg") mime = "image/jpeg";
  else if (ext === ".webp") mime = "image/webp";
  else if (ext === ".gif") mime = "image/gif";
  return `data:${mime};base64,${buf.toString("base64")}`;
}

export async function generateImage(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const apiKey = getApiKey();
  if (!apiKey) throw new Error("TUZI_API_KEY is required. Get one at https://api.tu-zi.com/token");

  const baseURL = getBaseUrl();
  const body: Record<string, unknown> = {
    model,
    prompt,
    response_format: "url",
  };

  if (supportsQuality(model)) {
    body.quality = resolutionToQuality(args.resolution);
  }

  if (args.inputImage) {
    body.image = [await readImageAsBase64DataUrl(args.inputImage)];
  }

  console.log(`Generating image with Tuzi (${model})...`);

  const res = await fetch(`${baseURL}/images/generations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Tuzi API error (${res.status}): ${err}`);
  }

  const result = (await res.json()) as SyncResponse;
  const img = result.data?.[0];

  if (img?.revised_prompt?.includes("PROHIBITED_CONTENT"))
    throw new Error("Content rejected: contains prohibited content");
  if (img?.revised_prompt?.includes("NO_IMAGE"))
    throw new Error("Model did not generate an image. Try a more explicit prompt.");

  if (img?.url) {
    if (img.url.startsWith("data:")) {
      const b64 = img.url.split(",")[1]!;
      return Uint8Array.from(Buffer.from(b64, "base64"));
    }
    return downloadImage(img.url);
  }
  if (img?.b64_json) return Uint8Array.from(Buffer.from(img.b64_json, "base64"));

  throw new Error("No image in response");
}
