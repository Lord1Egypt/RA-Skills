/**
 * Minimal Wavespeed.ai client for the protagonist reference image step.
 * Self-contained — only the t2i submit + poll path is implemented.
 */
const WAVESPEED_BASE = "https://api.wavespeed.ai/api/v3";

export interface WavespeedTask {
  id: string;
  status: "created" | "processing" | "completed" | "failed";
  outputs: string[];
  error?: string;
  urls?: { get?: string };
}

function getApiKey(): string {
  const key = process.env.WAVESPEED_API_KEY;
  if (!key) throw new Error("WAVESPEED_API_KEY is not set");
  return key;
}

export async function submitImage(modelId: string, prompt: string): Promise<WavespeedTask> {
  const key = getApiKey();
  const encoded = encodeURIComponent(modelId);
  const res = await fetch(`${WAVESPEED_BASE}/${encoded}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt, aspect_ratio: "1:1" }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Wavespeed submit failed (${res.status}): ${text}`);
  const json = JSON.parse(text) as { code: number; message?: string; data: WavespeedTask };
  if (json.code !== 200) throw new Error(`Wavespeed: ${json.message ?? "unknown error"}`);
  return json.data;
}

export async function pollImage(pollUrl: string): Promise<WavespeedTask> {
  const key = getApiKey();
  const url = pollUrl.startsWith("http") ? pollUrl : `${WAVESPEED_BASE}/predictions/${pollUrl}`;
  const res = await fetch(url, { headers: { Authorization: `Bearer ${key}` } });
  const text = await res.text();
  if (!res.ok) {
    // "not finished" is the provider's idiomatic "still processing" reply
    if (text.toLowerCase().includes("not finished")) {
      return { id: "", status: "processing", outputs: [] };
    }
    throw new Error(`Wavespeed poll failed (${res.status}): ${text}`);
  }
  const json = JSON.parse(text) as { code: number; message?: string; data: WavespeedTask };
  if (json.code !== 200) throw new Error(`Wavespeed: ${json.message ?? "unknown error"}`);
  return json.data;
}
