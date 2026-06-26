import path from "node:path";
import { readFile } from "node:fs/promises";
import { execSync } from "node:child_process";
import type { CliArgs } from "../types";

export function getDefaultModel(): string {
  return process.env.GOOGLE_IMAGE_MODEL || "gemini-3-pro-image-preview";
}

function getApiKey(): string | null {
  return process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY || null;
}

function getBaseUrl(): string {
  const base = process.env.GOOGLE_BASE_URL || "https://generativelanguage.googleapis.com";
  return base.replace(/\/+$/g, "");
}

function buildUrl(pathname: string): string {
  const base = getBaseUrl();
  const cleaned = pathname.replace(/^\/+/g, "");
  if (base.endsWith("/v1beta")) return `${base}/${cleaned}`;
  return `${base}/v1beta/${cleaned}`;
}

function getHttpProxy(): string | null {
  return process.env.https_proxy || process.env.HTTPS_PROXY ||
    process.env.http_proxy || process.env.HTTP_PROXY ||
    process.env.ALL_PROXY || null;
}

async function postJson<T>(pathname: string, body: unknown): Promise<T> {
  const apiKey = getApiKey();
  if (!apiKey) throw new Error("GOOGLE_API_KEY or GEMINI_API_KEY is required");

  const url = buildUrl(pathname);
  const proxy = getHttpProxy();

  if (proxy) {
    const bodyStr = JSON.stringify(body);
    const proxyArgs = `-x "${proxy}"`;
    const result = execSync(
      `curl -s --connect-timeout 30 --max-time 300 ${proxyArgs} "${url}" -H "Content-Type: application/json" -H "x-goog-api-key: ${apiKey}" -d @-`,
      { input: bodyStr, maxBuffer: 100 * 1024 * 1024, timeout: 310000 },
    );
    const parsed = JSON.parse(result.toString()) as any;
    if (parsed.error) throw new Error(`Google API error (${parsed.error.code}): ${parsed.error.message}`);
    return parsed as T;
  }

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": apiKey },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Google API error (${res.status}): ${err}`);
  }
  return (await res.json()) as T;
}

async function readImageAsBase64(p: string): Promise<{ data: string; mimeType: string }> {
  const buf = await readFile(p);
  const ext = path.extname(p).toLowerCase();
  let mimeType = "image/png";
  if (ext === ".jpg" || ext === ".jpeg") mimeType = "image/jpeg";
  else if (ext === ".gif") mimeType = "image/gif";
  else if (ext === ".webp") mimeType = "image/webp";
  return { data: buf.toString("base64"), mimeType };
}

export async function generateImage(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const parts: Array<{ text?: string; inlineData?: { data: string; mimeType: string } }> = [];

  if (args.inputImage) {
    const { data, mimeType } = await readImageAsBase64(args.inputImage);
    parts.push({ inlineData: { data, mimeType } });
  }
  parts.push({ text: prompt });

  console.log(`Generating image with Google Gemini (${model}), resolution ${args.resolution}...`);

  const response = await postJson<{
    candidates?: Array<{ content?: { parts?: Array<{ inlineData?: { data?: string } }> } }>;
  }>(`models/${model}:generateContent`, {
    contents: [{ role: "user", parts }],
    generationConfig: {
      responseModalities: ["IMAGE"],
      imageConfig: { imageSize: args.resolution },
    },
  });

  for (const candidate of response.candidates || []) {
    for (const part of candidate.content?.parts || []) {
      const data = part.inlineData?.data;
      if (typeof data === "string" && data.length > 0)
        return Uint8Array.from(Buffer.from(data, "base64"));
    }
  }

  throw new Error("No image in response");
}
