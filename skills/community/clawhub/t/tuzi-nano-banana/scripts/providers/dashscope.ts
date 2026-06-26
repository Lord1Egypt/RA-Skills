import type { CliArgs } from "../types";

export function getDefaultModel(): string {
  return process.env.DASHSCOPE_IMAGE_MODEL || "z-image-turbo";
}

function resolutionToSize(resolution: string): string {
  if (resolution === "4K" || resolution === "2K") return "1536*1536";
  return "1024*1024";
}

export async function generateImage(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const apiKey = process.env.DASHSCOPE_API_KEY;
  if (!apiKey) throw new Error("DASHSCOPE_API_KEY is required");

  if (args.inputImage) throw new Error("Image editing is not supported with DashScope. Use --provider google or --provider tuzi.");

  const baseUrl = (process.env.DASHSCOPE_BASE_URL || "https://dashscope.aliyuncs.com").replace(/\/+$/g, "");
  const size = resolutionToSize(args.resolution);

  console.log(`Generating image with DashScope (${model})...`);

  const res = await fetch(`${baseUrl}/api/v1/services/aigc/multimodal-generation/generation`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      input: { messages: [{ role: "user", content: [{ text: prompt }] }] },
      parameters: { prompt_extend: false, size },
    }),
  });

  if (!res.ok) throw new Error(`DashScope API error (${res.status}): ${await res.text()}`);

  const result = await res.json() as {
    output?: { result_image?: string; choices?: Array<{ message?: { content?: Array<{ image?: string }> } }> };
  };

  let imageData: string | null = result.output?.result_image ?? null;
  if (!imageData) {
    const content = result.output?.choices?.[0]?.message?.content;
    if (content) for (const item of content) { if (item.image) { imageData = item.image; break; } }
  }
  if (!imageData) throw new Error("No image in response");

  if (imageData.startsWith("http")) {
    const imgRes = await fetch(imageData);
    if (!imgRes.ok) throw new Error("Failed to download image");
    return new Uint8Array(await imgRes.arrayBuffer());
  }
  return Uint8Array.from(Buffer.from(imageData, "base64"));
}
