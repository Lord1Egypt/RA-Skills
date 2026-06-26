import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { asStellaError } from "../errors";

const BASE_URL = "https://api.laozhang.ai/v1beta/models";
const MODEL = "gemini-3.1-flash-image-preview";
const STELLA_SELFIE_DIR = path.join(
  os.homedir(),
  ".openclaw",
  "workspace",
  "stella-selfie"
);

export type Resolution = "1K" | "2K" | "4K";
export type AspectRatio =
  | "1:1"
  | "16:9"
  | "9:16"
  | "4:3"
  | "3:4"
  | "21:9"
  | "3:2"
  | "2:3"
  | "5:4"
  | "4:5";

export interface LaozhangGenerateOptions {
  prompt: string;
  referenceImages: string[];
  resolution: Resolution;
  aspectRatio?: AspectRatio;
  count: number;
  apiKey?: string;
}

export interface LaozhangResult {
  imageData: Buffer;
  mimeType: string;
  outputPath: string;
}

function getApiKey(provided?: string): string {
  const key = provided || process.env.LAOZHANG_API_KEY;
  if (!key) {
    throw new Error(
      "LAOZHANG_API_KEY is not set. Set it in your environment (e.g. OpenClaw skills.entries.*.env/apiKey) or for local testing use .env.local / --api-key."
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

function buildParts(
  prompt: string,
  referenceImages: string[]
): object[] {
  const parts: object[] = [];

  for (const imgPath of referenceImages) {
    if (imgPath.startsWith("http://") || imgPath.startsWith("https://")) {
      const ext = path.extname(new URL(imgPath).pathname).toLowerCase();
      const mimeMap: Record<string, string> = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
      };
      const mimeType = mimeMap[ext] || "image/jpeg";
      parts.push({
        fileData: {
          fileUri: imgPath,
          mimeType,
        },
      });
    } else {
      const { data, mimeType } = readImageAsBase64(imgPath);
      parts.push({
        inlineData: { mime_type: mimeType, data },
      });
    }
  }

  parts.push({ text: prompt });

  return parts;
}

/**
 * Generate images using laozhang.ai Google-native API (gemini-3-pro-image-preview).
 * Supports local file paths (inline_data) and HTTP(S) URLs (fileData.fileUri).
 * Returns an array of results (one per requested image).
 */
export async function generateWithLaozhang(
  options: LaozhangGenerateOptions
): Promise<LaozhangResult[]> {
  const {
    prompt,
    referenceImages,
    resolution,
    aspectRatio = "1:1",
    count,
    apiKey,
  } = options;

  let key: string;
  try {
    key = getApiKey(apiKey);
  } catch (err) {
    throw asStellaError("laozhang", err);
  }

  const endpoint = `${BASE_URL}/${MODEL}:generateContent`;
  const parts = buildParts(prompt, referenceImages);

  const body = {
    contents: [{ parts, role: "user" }],
    generationConfig: {
      responseModalities: ["IMAGE"],
      imageConfig: {
        aspectRatio,
        imageSize: resolution,
      },
    },
  };

  const results: LaozhangResult[] = [];
  fs.mkdirSync(STELLA_SELFIE_DIR, { recursive: true });

  for (let i = 0; i < count; i++) {
    const maxAttempts = 3;
    let lastErr: unknown;
    let responseData: any = null;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      let res: Response;
      try {
        res = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-goog-api-key": key,
          },
          body: JSON.stringify(body),
        });
      } catch (err) {
        lastErr = err;
        const delayMs = 500 * attempt;
        await new Promise((r) => setTimeout(r, delayMs));
        continue;
      }

      if (!res.ok) {
        let errBody: any;
        try {
          errBody = await res.json();
        } catch {
          errBody = { message: `HTTP ${res.status}` };
        }
        const errMsg =
          errBody?.error?.message ||
          errBody?.message ||
          `HTTP ${res.status}`;
        const syntheticErr = Object.assign(new Error(errMsg), {
          status: res.status,
        });
        lastErr = syntheticErr;

        if (res.status >= 500 || res.status === 429) {
          const delayMs = 500 * attempt;
          await new Promise((r) => setTimeout(r, delayMs));
          continue;
        }
        throw asStellaError("laozhang", syntheticErr);
      }

      try {
        responseData = await res.json();
        break;
      } catch (err) {
        lastErr = err;
        const delayMs = 500 * attempt;
        await new Promise((r) => setTimeout(r, delayMs));
      }
    }

    if (!responseData) {
      if (lastErr) throw asStellaError("laozhang", lastErr);
      throw asStellaError(
        "laozhang",
        new Error(`laozhang generateContent failed after ${maxAttempts} attempts`)
      );
    }

    const candidate = responseData?.candidates?.[0];
    if (!candidate?.content?.parts) {
      throw asStellaError(
        "laozhang",
        new Error(
          "laozhang returned no content parts. Try again; this is often transient."
        )
      );
    }

    let imageData: Buffer | null = null;
    let mimeType = "image/png";

    for (const part of candidate.content.parts) {
      if (part.inlineData) {
        mimeType = part.inlineData.mimeType || part.inlineData.mime_type || "image/png";
        const raw = part.inlineData.data;
        if (typeof raw === "string") {
          imageData = Buffer.from(raw, "base64");
        }
      }
    }

    if (!imageData) {
      throw asStellaError(
        "laozhang",
        new Error("laozhang returned no image data in response")
      );
    }

    const ext = mimeType.split("/")[1] || "png";
    const [, ns] = process.hrtime();
    const outputPath = path.join(
      STELLA_SELFIE_DIR,
      `stella-${Date.now()}-${ns}-${i}.${ext}`
    );
    fs.writeFileSync(outputPath, imageData);

    results.push({ imageData, mimeType, outputPath });
  }

  return results;
}
