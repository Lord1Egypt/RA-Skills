import path from "node:path";
import process from "node:process";
import { homedir } from "node:os";
import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import type { CliArgs, Provider } from "./types";

function parseArgs(argv: string[]): CliArgs {
  const out: CliArgs = {
    prompt: null,
    filename: null,
    inputImage: null,
    resolution: "1K",
    provider: null,
    model: null,
    apiKey: null,
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;

    if (a === "--prompt" || a === "-p") {
      out.prompt = argv[++i] ?? null;
      continue;
    }
    if (a === "--filename" || a === "-f") {
      out.filename = argv[++i] ?? null;
      continue;
    }
    if (a === "--input-image" || a === "-i") {
      out.inputImage = argv[++i] ?? null;
      continue;
    }
    if (a === "--resolution" || a === "-r") {
      const v = argv[++i]?.toUpperCase();
      if (v === "1K" || v === "2K" || v === "4K") out.resolution = v;
      else throw new Error(`Invalid resolution: ${v}. Use 1K, 2K, or 4K`);
      continue;
    }
    if (a === "--provider") {
      const v = argv[++i] as Provider;
      if (!["google", "openai", "dashscope", "replicate", "tuzi"].includes(v))
        throw new Error(`Invalid provider: ${v}`);
      out.provider = v;
      continue;
    }
    if (a === "--model" || a === "-m") {
      out.model = argv[++i] ?? null;
      continue;
    }
    if (a === "--api-key" || a === "-k") {
      out.apiKey = argv[++i] ?? null;
      continue;
    }
    if (a.startsWith("-")) throw new Error(`Unknown option: ${a}`);
  }

  return out;
}

async function loadEnvFile(p: string): Promise<Record<string, string>> {
  try {
    const content = await readFile(p, "utf8");
    const env: Record<string, string> = {};
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const idx = trimmed.indexOf("=");
      if (idx === -1) continue;
      const key = trimmed.slice(0, idx).trim();
      let val = trimmed.slice(idx + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'")))
        val = val.slice(1, -1);
      env[key] = val;
    }
    return env;
  } catch {
    return {};
  }
}

async function loadEnv(): Promise<void> {
  const homeEnv = await loadEnvFile(path.join(homedir(), ".tuzi-skills", ".env"));
  const cwdEnv = await loadEnvFile(path.join(process.cwd(), ".tuzi-skills", ".env"));
  for (const [k, v] of Object.entries(homeEnv)) {
    if (!process.env[k]) process.env[k] = v;
  }
  for (const [k, v] of Object.entries(cwdEnv)) {
    if (!process.env[k]) process.env[k] = v;
  }
}

function detectProvider(args: CliArgs): Provider {
  if (args.provider) return args.provider;
  if (args.apiKey) return "google";

  const hasTuzi = !!process.env.TUZI_API_KEY;
  const hasGoogle = !!(process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY);
  const hasOpenai = !!process.env.OPENAI_API_KEY;
  const hasDashscope = !!process.env.DASHSCOPE_API_KEY;
  const hasReplicate = !!process.env.REPLICATE_API_TOKEN;

  const available = [
    hasTuzi && "tuzi",
    hasGoogle && "google",
    hasOpenai && "openai",
    hasDashscope && "dashscope",
    hasReplicate && "replicate",
  ].filter(Boolean) as Provider[];

  if (available.length >= 1) return available[0]!;

  throw new Error(
    "No API key found. Set TUZI_API_KEY, GOOGLE_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, DASHSCOPE_API_KEY, or REPLICATE_API_TOKEN.\n" +
    "Or pass --api-key for direct Google Gemini access."
  );
}

async function autoDetectResolution(inputImagePath: string, explicitResolution: "1K" | "2K" | "4K"): Promise<"1K" | "2K" | "4K"> {
  if (explicitResolution !== "1K") return explicitResolution;
  try {
    const { execSync } = await import("node:child_process");
    const result = execSync(`identify -format "%w %h" "${inputImagePath}" 2>/dev/null`, { encoding: "utf8" }).trim();
    const [w, h] = result.split(" ").map(Number);
    if (!w || !h) return "1K";
    const maxDim = Math.max(w, h);
    if (maxDim >= 3000) return "4K";
    if (maxDim >= 1500) return "2K";
    return "1K";
  } catch {
    return "1K";
  }
}

type ProviderModule = {
  getDefaultModel: () => string;
  generateImage: (prompt: string, model: string, args: CliArgs) => Promise<Uint8Array>;
};

async function loadProviderModule(provider: Provider): Promise<ProviderModule> {
  if (provider === "google") return (await import("./providers/google")) as ProviderModule;
  if (provider === "dashscope") return (await import("./providers/dashscope")) as ProviderModule;
  if (provider === "replicate") return (await import("./providers/replicate")) as ProviderModule;
  if (provider === "tuzi") return (await import("./providers/tuzi")) as ProviderModule;
  return (await import("./providers/openai")) as ProviderModule;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (!args.prompt) {
    console.error("Error: --prompt is required");
    process.exit(1);
  }
  if (!args.filename) {
    console.error("Error: --filename is required");
    process.exit(1);
  }

  await loadEnv();

  if (args.apiKey) {
    process.env.GEMINI_API_KEY = args.apiKey;
  }

  if (args.inputImage) {
    try {
      await access(args.inputImage);
    } catch {
      console.error(`Error: Input image not found: ${args.inputImage}`);
      process.exit(1);
    }
    args.resolution = await autoDetectResolution(args.inputImage, args.resolution);
    console.log(`Loaded input image: ${args.inputImage}`);
    console.log(`Resolution: ${args.resolution}`);
  }

  const provider = detectProvider(args);
  const providerModule = await loadProviderModule(provider);
  const model = args.model || providerModule.getDefaultModel();

  const outputPath = path.resolve(args.filename);
  await mkdir(path.dirname(outputPath), { recursive: true });

  console.log(`Using ${provider} / ${model}`);

  let imageData: Uint8Array;
  try {
    imageData = await providerModule.generateImage(args.prompt, model, args);
  } catch (e) {
    console.error("Generation failed, retrying...");
    imageData = await providerModule.generateImage(args.prompt, model, args);
  }

  await writeFile(outputPath, imageData);
  console.log(`\nImage saved: ${outputPath}`);
}

main().catch((e) => {
  console.error(e instanceof Error ? e.message : String(e));
  process.exit(1);
});
