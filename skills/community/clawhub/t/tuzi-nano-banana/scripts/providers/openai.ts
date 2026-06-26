import path from "node:path";
import { readFile } from "node:fs/promises";
import type { CliArgs } from "../types";

export function getDefaultModel(): string {
  return process.env.OPENAI_IMAGE_MODEL || "gpt-image-1.5";
}

function resolutionToSize(resolution: string): string {
  if (resolution === "4K" || resolution === "2K") return "1536x1024";
  return "1024x1024";
}

type OpenAIImageResponse = { data: Array<{ url?: string; b64_json?: string }> };

export async function generateImage(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const baseURL = process.env.OPENAI_BASE_URL || "https://api.openai.com/v1";
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error("OPENAI_API_KEY is required");

  const size = resolutionToSize(args.resolution);

  if (args.inputImage) {
    const form = new FormData();
    form.append("model", model);
    form.append("prompt", prompt);
    form.append("size", size);
    const bytes = await readFile(args.inputImage);
    const filename = path.basename(args.inputImage);
    const blob = new Blob([bytes], { type: "image/png" });
    form.append("image[]", blob, filename);

    const res = await fetch(`${baseURL}/images/edits`, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}` },
      body: form,
    });
    if (!res.ok) throw new Error(`OpenAI API error: ${await res.text()}`);
    const result = (await res.json()) as OpenAIImageResponse;
    return extractImage(result);
  }

  const res = await fetch(`${baseURL}/images/generations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ model, prompt, size }),
  });
  if (!res.ok) throw new Error(`OpenAI API error: ${await res.text()}`);
  const result = (await res.json()) as OpenAIImageResponse;
  return extractImage(result);
}

async function extractImage(result: OpenAIImageResponse): Promise<Uint8Array> {
  const img = result.data[0];
  if (img?.b64_json) return Uint8Array.from(Buffer.from(img.b64_json, "base64"));
  if (img?.url) {
    const res = await fetch(img.url);
    if (!res.ok) throw new Error("Failed to download image");
    return new Uint8Array(await res.arrayBuffer());
  }
  throw new Error("No image in response");
}
