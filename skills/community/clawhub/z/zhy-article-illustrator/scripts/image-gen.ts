#!/usr/bin/env bun
/**
 * image-gen.ts — 图像生成 CLI
 *
 * 用法：
 *   bun run scripts/image-gen.ts -p "prompt" -o out.png
 *   bun run scripts/image-gen.ts --prompt-file p.md -o out.png --ar 16:9
 *   bun run scripts/image-gen.ts -p "text" -o out.png --ref src.png
 *   bun run scripts/image-gen.ts -p "text" -o out.png --provider xiaomi --model gemini-3.1-flash-image-preview
 *
 * 环境变量从技能根目录 .env 读取：
 *   IMAGE_PROVIDER / IMAGE_MODEL / IMAGE_BASE_URL / IMAGE_API_KEY / IMAGE_SIZE
 *   XIAOMI_API_KEY / XIAOMI_BASE_URL / XIAOMI_IMAGE_SIZE
 *   GEMINI_API_KEY / GOOGLE_API_KEY
 *   OPENAI_API_KEY
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, dirname, join } from "node:path";

type Provider = "gemini" | "google" | "xiaomi" | "openai" | "auto";
type ResolvedProvider = "google" | "xiaomi" | "openai";
type GeminiProvider = "google" | "xiaomi";

interface Args {
  prompt: string;
  output: string;
  ar: string;
  ref: string | null;
  provider: Provider;
  model: string | null;
  baseUrl: string | null;
  apiKey: string | null;
  imageSize: string | null;
  hd: boolean;
  quiet: boolean;
}

interface GenResult {
  output: string;
  provider: string;
  model: string;
}

interface GeminiPart {
  inlineData?: { data?: string; mimeType?: string };
  inline_data?: { data?: string; mime_type?: string };
}

function loadEnv(): void {
  const envPath = resolve(process.cwd(), ".env");
  if (!existsSync(envPath)) return;

  const lines = readFileSync(envPath, "utf-8").split("\n");
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq < 0) continue;
    const key = trimmed.slice(0, eq).trim();
    const val = trimmed.slice(eq + 1).trim().replace(/^["']|["']$/g, "");
    if (key && !(key in process.env)) {
      process.env[key] = val;
    }
  }
}

function parseArgs(): Args {
  const argv = process.argv.slice(2);

  if (argv.includes("--help") || argv.includes("-h")) {
    console.log(`
image-gen.ts — 图像生成 CLI

用法：
  bun run scripts/image-gen.ts -p <prompt> -o <output.png> [选项]

必填：
  -p, --prompt <text>        提示词文本
  --prompt-file <path>       从文件读取提示词（与 -p 二选一）
  -o, --output <path>        输出图片路径（.png / .jpg）

选项：
  --ar <ratio>               宽高比，如 16:9 | 4:3 | 1:1（默认 16:9）
  --ref <path>               参考图片路径（仅 Gemini 多模态支持）
  --provider <name>          强制指定 provider：gemini | google | xiaomi | openai（默认自动检测）
  --model <name>             指定模型名称
  --base-url <url>           指定 Gemini 原生代理或 Xiaomi 基础地址
  --api-key <key>            临时覆盖 API Key
  --image-size <value>       图片清晰度/尺寸标识（如 Xiaomi 的 1K）
  --hd                       高质量模式（OpenAI dall-e-3 时有效）
  --quiet                    安静模式：只输出文件路径

环境变量（来自技能根目录 .env）：
  IMAGE_PROVIDER / IMAGE_MODEL / IMAGE_BASE_URL / IMAGE_API_KEY / IMAGE_SIZE
  XIAOMI_API_KEY / XIAOMI_BASE_URL / XIAOMI_IMAGE_SIZE
  GEMINI_API_KEY / GOOGLE_API_KEY
  OPENAI_API_KEY
`);
    process.exit(0);
  }

  let prompt = "";
  let output = "";
  let ar = "16:9";
  let ref: string | null = null;
  let provider: Provider = "auto";
  let model: string | null = null;
  let baseUrl: string | null = null;
  let apiKey: string | null = null;
  let imageSize: string | null = null;
  let hd = false;
  let quiet = false;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case "-p":
      case "--prompt":
        prompt = argv[++i] ?? "";
        break;
      case "--prompt-file": {
        const pf = argv[++i] ?? "";
        if (!existsSync(pf)) {
          console.error(`错误：找不到提示词文件 ${pf}`);
          process.exit(1);
        }
        prompt = readFileSync(pf, "utf-8").trim();
        break;
      }
      case "-o":
      case "--output":
        output = argv[++i] ?? "";
        break;
      case "--ar":
        ar = argv[++i] ?? "16:9";
        break;
      case "--ref":
        ref = argv[++i] ?? null;
        break;
      case "--provider":
        provider = (argv[++i] ?? "auto") as Provider;
        break;
      case "--model":
        model = argv[++i] ?? null;
        break;
      case "--base-url":
        baseUrl = argv[++i] ?? null;
        break;
      case "--api-key":
        apiKey = argv[++i] ?? null;
        break;
      case "--image-size":
        imageSize = argv[++i] ?? null;
        break;
      case "--hd":
        hd = true;
        break;
      case "--quiet":
        quiet = true;
        break;
    }
  }

  if (!prompt) {
    console.error("错误：必须提供 -p/--prompt 或 --prompt-file");
    process.exit(1);
  }
  if (!output) {
    console.error("错误：必须提供 -o/--output");
    process.exit(1);
  }

  return { prompt, output, ar, ref, provider, model, baseUrl, apiKey, imageSize, hd, quiet };
}

function detectProvider(preferred: Provider): ResolvedProvider {
  const configuredProvider = (process.env.IMAGE_PROVIDER ?? "").trim().toLowerCase();
  const configuredBaseUrl = (process.env.IMAGE_BASE_URL ?? process.env.XIAOMI_BASE_URL ?? "").trim().toLowerCase();

  if (preferred === "gemini" || preferred === "google") return "google";
  if (preferred === "xiaomi") return "xiaomi";
  if (preferred === "openai") return "openai";

  if (configuredProvider === "gemini" || configuredProvider === "google") return "google";
  if (configuredProvider === "xiaomi") return "xiaomi";
  if (configuredProvider === "openai") return "openai";
  if (configuredBaseUrl.includes("vip.123everything.com")) return "xiaomi";

  const xiaomiKey = process.env.XIAOMI_API_KEY ?? "";
  const googleKey = process.env.IMAGE_API_KEY ?? process.env.GOOGLE_API_KEY ?? process.env.GEMINI_API_KEY ?? "";
  const openaiKey = process.env.OPENAI_API_KEY ?? "";

  if (xiaomiKey) return "xiaomi";
  if (googleKey) return "google";
  if (openaiKey) return "openai";

  console.error("错误：未找到可用生图配置。请配置 IMAGE_PROVIDER/IMAGE_API_KEY，或 XIAOMI_API_KEY，或 GEMINI_API_KEY/GOOGLE_API_KEY，或 OPENAI_API_KEY");
  process.exit(1);
}

function getConfiguredModel(provider: ResolvedProvider, cliModel: string | null): string {
  if (cliModel) return cliModel;

  const envModel = (process.env.IMAGE_MODEL ?? "").trim();
  if (envModel) return envModel;

  if (provider === "xiaomi") return "gemini-3.1-flash-image-preview";
  if (provider === "google") return "gemini-2.5-flash-image-preview";
  return "gpt-image-1";
}

function getGeminiBaseUrl(provider: GeminiProvider, cliBaseUrl: string | null): string {
  const providerDefault = provider === "xiaomi"
    ? (process.env.XIAOMI_BASE_URL ?? "https://vip.123everything.com/v1beta")
    : "https://generativelanguage.googleapis.com/v1beta";
  const base = (cliBaseUrl ?? process.env.IMAGE_BASE_URL ?? providerDefault).trim();
  return base.replace(/\/+$/, "");
}

function getGeminiApiKey(provider: GeminiProvider, cliApiKey: string | null): string {
  if (provider === "xiaomi") {
    return (cliApiKey ?? process.env.XIAOMI_API_KEY ?? process.env.IMAGE_API_KEY ?? "").trim();
  }
  return (cliApiKey ?? process.env.IMAGE_API_KEY ?? process.env.GOOGLE_API_KEY ?? process.env.GEMINI_API_KEY ?? "").trim();
}

function getGeminiImageSize(provider: GeminiProvider, cliImageSize: string | null): string | null {
  const fallback = provider === "xiaomi" ? (process.env.XIAOMI_IMAGE_SIZE ?? "1K") : "";
  const size = (cliImageSize ?? process.env.IMAGE_SIZE ?? fallback).trim();
  return size || null;
}

function getOpenAiApiKey(cliApiKey: string | null): string {
  return (cliApiKey ?? process.env.IMAGE_API_KEY ?? process.env.OPENAI_API_KEY ?? "").trim();
}

function getReferencePart(provider: GeminiProvider, ref: string): object {
  if (!existsSync(ref)) {
    console.error(`错误：参考图片不存在 ${ref}`);
    process.exit(1);
  }

  const refData = readFileSync(ref);
  const ext = ref.split(".").pop()?.toLowerCase() ?? "png";
  const mimeMap: Record<string, string> = {
    png: "image/png",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    webp: "image/webp",
  };
  const mimeType = mimeMap[ext] ?? "image/png";
  const data = refData.toString("base64");

  if (provider === "xiaomi") {
    return {
      inline_data: {
        mime_type: mimeType,
        data,
      },
    };
  }

  return {
    inlineData: {
      mimeType,
      data,
    },
  };
}

async function geminiGen(
  prompt: string,
  output: string,
  ar: string,
  ref: string | null,
  model: string,
  base: string,
  apiKey: string,
  provider: GeminiProvider,
  imageSize: string | null,
): Promise<void> {
  const url = `${base}/models/${model}:generateContent?key=${apiKey}`;
  const parts: object[] = [];

  if (ref) {
    parts.push(getReferencePart(provider, ref));
  }

  const fullPrompt = provider === "xiaomi" ? prompt : `${prompt}\n\nAspect ratio: ${ar}`;
  parts.push({ text: fullPrompt });

  const imageConfig: Record<string, string> = { aspectRatio: ar };
  if (imageSize) {
    imageConfig.imageSize = imageSize;
  }

  const body = {
    contents: [{ role: "user", parts }],
    generationConfig: {
      responseModalities: ["IMAGE", "TEXT"],
      imageConfig,
    },
  };

  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (provider === "xiaomi") {
    headers.Authorization = `Bearer ${apiKey}`;
  }

  const resp = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Gemini API 错误 ${resp.status}: ${err}`);
  }

  const data = await resp.json() as {
    candidates?: Array<{
      content?: {
        parts?: GeminiPart[];
      };
    }>;
  };

  const candidate = data.candidates?.[0];
  const imgPart = candidate?.content?.parts?.find((p) => p.inlineData?.data || p.inline_data?.data);
  const base64Data = imgPart?.inlineData?.data ?? imgPart?.inline_data?.data;

  if (!base64Data) {
    throw new Error("Gemini 响应中未找到图片数据");
  }

  const imgBuffer = Buffer.from(base64Data, "base64");
  mkdirSync(dirname(resolve(output)), { recursive: true });
  writeFileSync(output, imgBuffer);
}

async function imagenGen(prompt: string, output: string, ar: string, model: string, base: string, apiKey: string): Promise<void> {
  const url = `${base}/models/${model}:predict?key=${apiKey}`;

  const body = {
    instances: [{ prompt }],
    parameters: {
      sampleCount: 1,
      aspectRatio: ar,
    },
  };

  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Imagen API 错误 ${resp.status}: ${err}`);
  }

  const data = await resp.json() as {
    predictions?: Array<{ bytesBase64Encoded?: string }>;
  };

  const imgData = data.predictions?.[0]?.bytesBase64Encoded;
  if (!imgData) {
    throw new Error("Imagen 响应中未找到图片数据");
  }

  const imgBuffer = Buffer.from(imgData, "base64");
  mkdirSync(dirname(resolve(output)), { recursive: true });
  writeFileSync(output, imgBuffer);
}

async function runGeminiProvider(provider: GeminiProvider, args: Args): Promise<GenResult> {
  const model = getConfiguredModel(provider, args.model);
  const baseUrl = getGeminiBaseUrl(provider, args.baseUrl);
  const apiKey = getGeminiApiKey(provider, args.apiKey);
  const imageSize = getGeminiImageSize(provider, args.imageSize);

  if (!apiKey) {
    if (provider === "xiaomi") {
      throw new Error("缺少 Xiaomi API Key。请配置 XIAOMI_API_KEY，或 IMAGE_API_KEY");
    }
    throw new Error("缺少 Gemini API Key。请配置 IMAGE_API_KEY，或 GEMINI_API_KEY / GOOGLE_API_KEY");
  }

  if (provider === "google" && model.includes("imagen")) {
    await imagenGen(args.prompt, args.output, args.ar, model, baseUrl, apiKey);
  } else {
    await geminiGen(args.prompt, args.output, args.ar, args.ref, model, baseUrl, apiKey, provider, imageSize);
  }

  return { output: args.output, provider, model };
}

function oaSize(ar: string, model: string): string {
  if (model === "dall-e-3") {
    if (ar === "1:1") return "1024x1024";
    if (ar === "16:9") return "1792x1024";
    if (ar === "9:16") return "1024x1792";
    return "1792x1024";
  }

  if (ar === "1:1") return "1024x1024";
  if (ar === "4:3") return "1536x1024";
  if (ar === "3:4") return "1024x1536";
  if (ar === "16:9") return "1536x1024";
  if (ar === "9:16") return "1024x1536";
  return "1536x1024";
}

async function runOpenai(args: Args): Promise<GenResult> {
  const apiKey = getOpenAiApiKey(args.apiKey);
  if (!apiKey) {
    throw new Error("缺少 OpenAI API Key。请配置 OPENAI_API_KEY 或 IMAGE_API_KEY");
  }

  const model = getConfiguredModel("openai", args.model);
  const size = oaSize(args.ar, model);

  const reqBody: Record<string, unknown> = {
    model,
    prompt: args.prompt,
    n: 1,
    size,
    response_format: "b64_json",
  };

  if (model === "dall-e-3") {
    reqBody.quality = args.hd ? "hd" : "standard";
  }

  const resp = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(reqBody),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`OpenAI API 错误 ${resp.status}: ${err}`);
  }

  const data = await resp.json() as {
    data?: Array<{ b64_json?: string; url?: string }>;
  };

  const item = data.data?.[0];
  let imgBuffer: Buffer;

  if (item?.b64_json) {
    imgBuffer = Buffer.from(item.b64_json, "base64");
  } else if (item?.url) {
    const imgResp = await fetch(item.url);
    if (!imgResp.ok) throw new Error(`下载图片失败 ${imgResp.status}`);
    imgBuffer = Buffer.from(await imgResp.arrayBuffer());
  } else {
    throw new Error("OpenAI 响应中未找到图片数据");
  }

  mkdirSync(dirname(resolve(args.output)), { recursive: true });
  writeFileSync(args.output, imgBuffer);

  return { output: args.output, provider: "openai", model };
}

async function main(): Promise<void> {
  loadEnv();
  const args = parseArgs();
  const provider = detectProvider(args.provider);

  let result: GenResult;
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      if (provider === "google" || provider === "xiaomi") {
        result = await runGeminiProvider(provider, args);
      } else {
        result = await runOpenai(args);
      }

      if (args.quiet) {
        console.log(result.output);
      } else {
        console.log(JSON.stringify({ success: true, ...result }, null, 2));
      }
      return;
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err));
      if (!args.quiet) {
        console.error(`[尝试 ${attempt}/2] 失败：${lastError.message}`);
      }
    }
  }

  if (args.quiet) {
    process.exit(1);
  } else {
    console.log(JSON.stringify({ success: false, error: lastError?.message ?? "未知错误" }, null, 2));
    process.exit(1);
  }
}

main();
