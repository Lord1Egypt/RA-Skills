import path from "node:path";
import { readFile } from "node:fs/promises";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "google/nano-banana-pro";
const POLL_INTERVAL_MS = 2000;
const MAX_POLL_MS = 300_000;

export function getDefaultModel(): string {
  return process.env.REPLICATE_IMAGE_MODEL || DEFAULT_MODEL;
}

function getBaseUrl(): string {
  return (process.env.REPLICATE_BASE_URL || "https://api.replicate.com").replace(/\/+$/g, "");
}

async function readImageAsDataUrl(p: string): Promise<string> {
  const buf = await readFile(p);
  const ext = path.extname(p).toLowerCase();
  let mime = "image/png";
  if (ext === ".jpg" || ext === ".jpeg") mime = "image/jpeg";
  else if (ext === ".gif") mime = "image/gif";
  else if (ext === ".webp") mime = "image/webp";
  return `data:${mime};base64,${buf.toString("base64")}`;
}

type PredictionResponse = { id: string; status: string; output: unknown; error: string | null; urls?: { get?: string } };

export async function generateImage(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const apiToken = process.env.REPLICATE_API_TOKEN;
  if (!apiToken) throw new Error("REPLICATE_API_TOKEN is required");

  const [ownerName, version] = model.split(":");
  const parts = ownerName!.split("/");
  if (parts.length !== 2 || !parts[0] || !parts[1])
    throw new Error(`Invalid Replicate model: "${model}". Expected "owner/name"`);

  const input: Record<string, unknown> = { prompt, output_format: "png" };
  if (args.inputImage) input.image = await readImageAsDataUrl(args.inputImage);

  const baseUrl = getBaseUrl();
  const headers: Record<string, string> = {
    Authorization: `Bearer ${apiToken}`,
    "Content-Type": "application/json",
    Prefer: "wait=60",
  };

  const body: Record<string, unknown> = { input };
  let url: string;
  if (version) {
    url = `${baseUrl}/v1/predictions`;
    body.version = version;
  } else {
    url = `${baseUrl}/v1/models/${parts[0]}/${parts[1]}/predictions`;
  }

  console.log(`Generating image with Replicate (${model})...`);

  const res = await fetch(url, { method: "POST", headers, body: JSON.stringify(body) });
  if (!res.ok) throw new Error(`Replicate API error (${res.status}): ${await res.text()}`);

  let prediction = (await res.json()) as PredictionResponse;

  if (prediction.status !== "succeeded") {
    if (!prediction.urls?.get) throw new Error("No poll URL returned");
    const start = Date.now();
    while (Date.now() - start < MAX_POLL_MS) {
      await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));
      const pollRes = await fetch(prediction.urls!.get!, { headers: { Authorization: `Bearer ${apiToken}` } });
      if (!pollRes.ok) throw new Error(`Replicate poll error: ${await pollRes.text()}`);
      prediction = (await pollRes.json()) as PredictionResponse;
      if (prediction.status === "succeeded") break;
      if (prediction.status === "failed" || prediction.status === "canceled")
        throw new Error(`Replicate ${prediction.status}: ${prediction.error}`);
    }
    if (prediction.status !== "succeeded") throw new Error("Replicate prediction timed out");
  }

  const output = prediction.output;
  let outputUrl: string;
  if (typeof output === "string") outputUrl = output;
  else if (Array.isArray(output) && typeof output[0] === "string") outputUrl = output[0];
  else throw new Error(`Unexpected output format: ${JSON.stringify(output)}`);

  const imgRes = await fetch(outputUrl);
  if (!imgRes.ok) throw new Error("Failed to download image");
  return new Uint8Array(await imgRes.arrayBuffer());
}
