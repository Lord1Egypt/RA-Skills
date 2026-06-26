import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { asStellaError, shouldRetryGemini } from "../errors";

const MODEL = "gemini-3.1-flash-image-preview";
const STELLA_SELFIE_DIR = path.join(
  os.homedir(),
  ".openclaw",
  "workspace",
  "stella-selfie"
);

export type Resolution = "1K" | "2K" | "4K";

export interface GeminiGenerateOptions {
  prompt: string;
  referenceImages: string[];
  resolution: Resolution;
  count: number;
  apiKey?: string;
}

export interface GeminiResult {
  imageData: Buffer;
  mimeType: string;
  revisedPrompt?: string;
  outputPath: string;
}

function getApiKey(provided?: string): string {
  const key = provided || process.env.GEMINI_API_KEY;
  if (!key) {
    throw new Error(
      "GEMINI_API_KEY is not set. Set it in your environment (e.g. OpenClaw skills.entries.*.env/apiKey) or for local testing use .env.local / --api-key."
    );
  }
  return key;
}

function readImageAsBase64(
  filePath: string
): { data: string; mimeType: string } {
  const ext = path.extname(filePath).toLowerCase();
  const mimeMap: Record<string, string> = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
  };
  const mimeType = mimeMap[ext] || "image/jpeg";
  const data = fs.readFileSync(filePath).toString("base64");
  return { data, mimeType };
}

function buildContents(
  prompt: string,
  referenceImages: string[]
): object[] {
  if (referenceImages.length === 0) {
    // Text-to-image: single text part
    return [{ text: prompt }];
  }

  // Image editing: reference images first, then prompt
  const parts: object[] = [];

  for (const imgPath of referenceImages) {
    const { data, mimeType } = readImageAsBase64(imgPath);
    parts.push({
      inlineData: { data, mimeType },
    });
  }

  parts.push({ text: prompt });

  return [{ parts }];
}

/**
 * Generate images using Gemini gemini-3.1-flash-image-preview.
 * Returns an array of results (one per requested image).
 */
export async function generateWithGemini(
  options: GeminiGenerateOptions
): Promise<GeminiResult[]> {
  const { prompt, referenceImages, resolution, count, apiKey } = options;
  let key: string;
  try {
    key = getApiKey(apiKey);
  } catch (err) {
    throw asStellaError("gemini", err);
  }

  // Dynamic import to avoid loading the SDK when not needed
  const { GoogleGenAI } = await import("@google/genai");

  const ai = new GoogleGenAI({ apiKey: key });

  const contents = buildContents(prompt, referenceImages);

  const results: GeminiResult[] = [];
  fs.mkdirSync(STELLA_SELFIE_DIR, { recursive: true });

  for (let i = 0; i < count; i++) {
    const generateConfig = {
      responseModalities: ["TEXT", "IMAGE"],
      // imageConfig is a newer API field not yet reflected in SDK types
      imageConfig: { imageSize: resolution },
    };

    const maxAttempts = 3;
    let lastErr: unknown;
    let response: any = null;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        response = await ai.models.generateContent({
          model: MODEL,
          contents,
          config: generateConfig as object,
        });
        break;
      } catch (err) {
        lastErr = err;
        if (!shouldRetryGemini(err)) {
          throw asStellaError("gemini", err);
        }
        // Small backoff for transient API/network errors
        const delayMs = 500 * attempt;
        await new Promise((r) => setTimeout(r, delayMs));
      }
    }

    if (!response) {
      if (lastErr) throw asStellaError("gemini", lastErr);
      throw asStellaError(
        "gemini",
        new Error(`Gemini generateContent failed after ${maxAttempts} attempts`)
      );
    }

    let imageData: Buffer | null = null;
    let mimeType = "image/png";
    let revisedPrompt: string | undefined;

    const candidate = response.candidates?.[0];
    if (!candidate?.content?.parts) {
      // Some transient responses can be empty; retry a couple times before failing.
      // Re-run the full request to avoid partial/invalid payloads.
      let retried = false;
      for (let attempt = 1; attempt <= 2; attempt++) {
        retried = true;
        await new Promise((r) => setTimeout(r, 400 * attempt));
        let r2: any;
        try {
          r2 = await ai.models.generateContent({
            model: MODEL,
            contents,
            config: generateConfig as object,
          });
        } catch (err) {
          if (!shouldRetryGemini(err)) {
            throw asStellaError("gemini", err);
          }
          continue;
        }
        const c2 = r2.candidates?.[0];
        if (c2?.content?.parts) {
          response = r2;
          break;
        }
      }

      const cFinal = response.candidates?.[0];
      if (!cFinal?.content?.parts) {
        throw asStellaError(
          "gemini",
          new Error(
          "Gemini returned no content parts (after retry). Try again; this is often transient."
          )
        );
      }
    }

    const finalCandidate = response.candidates?.[0];
    for (const part of finalCandidate.content.parts) {
      if (part.text) {
        revisedPrompt = part.text;
      } else if (part.inlineData) {
        // The SDK types inlineData as Blob; at runtime the data field is base64 string
        const blob = part.inlineData as unknown as {
          data: string | Uint8Array;
          mimeType?: string;
        };
        mimeType = blob.mimeType || "image/png";
        if (typeof blob.data === "string") {
          imageData = Buffer.from(blob.data, "base64");
        } else if (blob.data) {
          imageData = Buffer.from(blob.data as Uint8Array);
        }
      }
    }

    if (!imageData) {
      throw asStellaError(
        "gemini",
        new Error("Gemini returned no image data in response")
      );
    }

    const ext = mimeType.split("/")[1] || "png";
    // Use process.hrtime for sub-millisecond uniqueness when count > 1
    const [, ns] = process.hrtime();
    const outputPath = path.join(
      STELLA_SELFIE_DIR,
      `stella-${Date.now()}-${ns}-${i}.${ext}`
    );
    fs.writeFileSync(outputPath, imageData);

    results.push({ imageData, mimeType, revisedPrompt, outputPath });
  }

  return results;
}
