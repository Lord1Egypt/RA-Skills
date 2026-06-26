#!/usr/bin/env bun

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { spawn } from "node:child_process";

type Args = {
  articlePath: string;
  slug: string | null;
  density: string | null;
  aspectRatio: string | null;
  promptProfile: string | null;
  textLanguage: string | null;
  englishTerms: string[];
  imageProvider: string | null;
  imageModel: string | null;
  imageBaseUrl: string | null;
  apiKey: string | null;
  imageSize: string | null;
  configPath: string | null;
  upload: boolean;
  concurrency: number;
  reuseExisting: boolean;
};

type PlanResult = {
  success: boolean;
  article_path: string;
  config_path: string | null;
  slug: string;
  illustrations_dir: string;
  visual_bible_path: string;
  outline_path: string;
  prompt_count: number;
  prompt_profile: string;
  image_provider: string;
  image_model: string;
  image_size?: string;
};

type OutlineImage = {
  index: number;
  position: string;
  title: string;
  imageType: string;
  filename: string;
  altText: string;
};

type ImageRun = {
  index: number;
  title: string;
  filename: string;
  altText: string;
  promptPath: string;
  outputPath: string;
  relativePath: string;
  success: boolean;
  uploadedUrl: string | null;
  skipped: boolean;
  error: string | null;
  position: string;
};

function printHelp(): void {
  console.log(`
illustrate-article.ts - One-click article illustration pipeline

Usage:
  node scripts/illustrate-article.ts --article <article.md> [options]

Required:
  --article <path>                 Markdown article path

Planning options:
  --slug <value>                  Output slug
  --density <value>               minimal | balanced | rich
  --ar, --aspect-ratio <value>    Aspect ratio
  --prompt-profile <value>        Prompt profile, default nano-banana
  --text-language <value>         Default visible text language
  --english-terms <csv>           Comma-separated English whitelist
  --term <value>                  Repeatable English whitelist term
  --image-provider <value>        Provider label, default gemini
  --image-model <value>           Model label
  --image-base-url <value>        Gemini relay base URL
  --api-key <value>               Temporary API key passed to image-gen
  --image-size <value>            Image size / clarity label
  --config <path>                 Optional .zhy-illustrator.yml path

Pipeline options:
  --upload                        Upload successful images to Qiniu
  --concurrency <n>               Parallel image generation count, default 3
  --reuse-existing                Skip image generation for existing files

Outputs:
  - illustrations/<slug>/visual-bible.md
  - illustrations/<slug>/outline.md
  - illustrations/<slug>/prompts/*.prompt.md
  - illustrations/<slug>/*.png
  - article.illustrated.md
`);
}

function parseArgs(): Args {
  const argv = process.argv.slice(2);
  if (argv.includes("--help") || argv.includes("-h")) {
    printHelp();
    process.exit(0);
  }

  let articlePath = "";
  let slug: string | null = null;
  let density: string | null = null;
  let aspectRatio: string | null = null;
  let promptProfile: string | null = null;
  let textLanguage: string | null = null;
  const englishTerms: string[] = [];
  let imageProvider: string | null = null;
  let imageModel: string | null = null;
  let imageBaseUrl: string | null = null;
  let apiKey: string | null = null;
  let imageSize: string | null = null;
  let configPath: string | null = null;
  let upload = false;
  let concurrency = 3;
  let reuseExisting = false;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case "--article":
        articlePath = argv[++i] ?? "";
        break;
      case "--slug":
        slug = argv[++i] ?? null;
        break;
      case "--density":
        density = argv[++i] ?? null;
        break;
      case "--ar":
      case "--aspect-ratio":
        aspectRatio = argv[++i] ?? null;
        break;
      case "--prompt-profile":
        promptProfile = argv[++i] ?? null;
        break;
      case "--text-language":
        textLanguage = argv[++i] ?? null;
        break;
      case "--english-terms": {
        const raw = argv[++i] ?? "";
        for (const item of raw.split(",")) {
          const value = item.trim();
          if (value) englishTerms.push(value);
        }
        break;
      }
      case "--term": {
        const value = (argv[++i] ?? "").trim();
        if (value) englishTerms.push(value);
        break;
      }
      case "--image-provider":
        imageProvider = argv[++i] ?? null;
        break;
      case "--image-model":
        imageModel = argv[++i] ?? null;
        break;
      case "--image-base-url":
        imageBaseUrl = argv[++i] ?? null;
        break;
      case "--api-key":
        apiKey = argv[++i] ?? null;
        break;
      case "--image-size":
        imageSize = argv[++i] ?? null;
        break;
      case "--config":
        configPath = argv[++i] ?? null;
        break;
      case "--upload":
        upload = true;
        break;
      case "--concurrency":
        concurrency = Math.max(1, Number.parseInt(argv[++i] ?? "3", 10) || 3);
        break;
      case "--reuse-existing":
        reuseExisting = true;
        break;
    }
  }

  if (!articlePath) {
    console.error("错误：必须提供 --article <path>");
    process.exit(1);
  }

  return {
    articlePath,
    slug,
    density,
    aspectRatio,
    promptProfile,
    textLanguage,
    englishTerms,
    imageProvider,
    imageModel,
    imageBaseUrl,
    apiKey,
    imageSize,
    configPath,
    upload,
    concurrency,
    reuseExisting,
  };
}

function runScript(scriptPath: string, args: string[], extraEnv: Record<string, string> = {}): Promise<{ stdout: string; stderr: string; code: number }> {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(process.execPath, [scriptPath, ...args], {
      stdio: ["ignore", "pipe", "pipe"],
      env: { ...process.env, ...extraEnv },
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += String(chunk);
    });
    child.stderr.on("data", (chunk) => {
      stderr += String(chunk);
    });
    child.on("error", reject);
    child.on("close", (code) => {
      resolvePromise({ stdout, stderr, code: code ?? 1 });
    });
  });
}

async function runPlanning(args: Args): Promise<PlanResult> {
  const scriptPath = resolve("scripts", "plan-illustrations.ts");
  const cmdArgs = ["--article", resolve(args.articlePath)];
  if (args.slug) cmdArgs.push("--slug", args.slug);
  if (args.density) cmdArgs.push("--density", args.density);
  if (args.aspectRatio) cmdArgs.push("--aspect-ratio", args.aspectRatio);
  if (args.promptProfile) cmdArgs.push("--prompt-profile", args.promptProfile);
  if (args.textLanguage) cmdArgs.push("--text-language", args.textLanguage);
  if (args.imageProvider) cmdArgs.push("--image-provider", args.imageProvider);
  if (args.imageModel) cmdArgs.push("--image-model", args.imageModel);
  if (args.imageBaseUrl) cmdArgs.push("--image-base-url", args.imageBaseUrl);
  if (args.imageSize) cmdArgs.push("--image-size", args.imageSize);
  if (args.configPath) cmdArgs.push("--config", resolve(args.configPath));
  for (const term of args.englishTerms) {
    cmdArgs.push("--term", term);
  }

  const result = await runScript(scriptPath, cmdArgs);
  if (result.code !== 0) {
    throw new Error(result.stderr || result.stdout || "规划脚本执行失败");
  }
  return JSON.parse(result.stdout) as PlanResult;
}

function parseOutline(outlinePath: string): OutlineImage[] {
  const text = readFileSync(outlinePath, "utf-8");
  const lines = text.split(/\r?\n/);
  const images: OutlineImage[] = [];
  let current: Partial<OutlineImage> | null = null;

  for (const line of lines) {
    const trimmed = line.trim();
    const imageMatch = /^## Image (\d+)/.exec(trimmed);
    if (imageMatch) {
      if (current?.index && current.position && current.title && current.imageType && current.filename && current.altText) {
        images.push(current as OutlineImage);
      }
      current = { index: Number.parseInt(imageMatch[1], 10) };
      continue;
    }
    if (!current || !trimmed.startsWith("- ")) continue;

    const idx = trimmed.indexOf(":");
    if (idx < 0) continue;
    const key = trimmed.slice(2, idx).trim();
    const value = trimmed.slice(idx + 1).trim();
    if (key === "position") current.position = value;
    else if (key === "title") current.title = value;
    else if (key === "image_type") current.imageType = value;
    else if (key === "filename") current.filename = value;
    else if (key === "alt_text") current.altText = value;
  }

  if (current?.index && current.position && current.title && current.imageType && current.filename && current.altText) {
    images.push(current as OutlineImage);
  }

  return images;
}

function toPosixPath(pathValue: string): string {
  return pathValue.replace(/\\/g, "/");
}

function buildRuns(plan: PlanResult, outlineImages: OutlineImage[]): ImageRun[] {
  const promptsDir = join(plan.illustrations_dir, "prompts");
  return outlineImages.map((item) => ({
    index: item.index,
    title: item.title,
    filename: item.filename,
    altText: item.altText,
    promptPath: join(promptsDir, item.filename.replace(/\.(png|jpg|jpeg|webp)$/i, ".prompt.md")),
    outputPath: join(plan.illustrations_dir, item.filename),
    relativePath: toPosixPath(join("illustrations", plan.slug, item.filename)),
    success: false,
    uploadedUrl: null,
    skipped: false,
    error: null,
    position: item.position,
  }));
}

async function runPool<T>(items: T[], concurrency: number, worker: (item: T) => Promise<void>): Promise<void> {
  const queue = [...items];
  const runners = Array.from({ length: Math.min(concurrency, items.length) }, async () => {
    while (queue.length) {
      const item = queue.shift();
      if (!item) return;
      await worker(item);
    }
  });
  await Promise.all(runners);
}

async function generateImages(plan: PlanResult, runs: ImageRun[], args: Args, aspectRatio: string): Promise<void> {
  const scriptPath = resolve("scripts", "image-gen.ts");
  await runPool(runs, args.concurrency, async (run) => {
    if (args.reuseExisting && existsSync(run.outputPath)) {
      run.success = true;
      run.skipped = true;
      return;
    }

    const cmdArgs = [
      "--prompt-file",
      run.promptPath,
      "--output",
      run.outputPath,
      "--ar",
      aspectRatio,
      "--provider",
      args.imageProvider ?? plan.image_provider,
      "--model",
      args.imageModel ?? plan.image_model,
    ];

    if (args.imageBaseUrl) {
      cmdArgs.push("--base-url", args.imageBaseUrl);
    }
    if (args.apiKey) {
      cmdArgs.push("--api-key", args.apiKey);
    }
    if (args.imageSize) {
      cmdArgs.push("--image-size", args.imageSize);
    } else if (plan.image_size) {
      cmdArgs.push("--image-size", plan.image_size);
    }

    const result = await runScript(scriptPath, cmdArgs);
    if (result.code === 0 && existsSync(run.outputPath)) {
      run.success = true;
    } else {
      run.error = (result.stderr || result.stdout || "图片生成失败").trim();
    }
  });
}

async function uploadImages(plan: PlanResult, runs: ImageRun[]): Promise<void> {
  const scriptPath = resolve("scripts", "qiniu-upload.ts");
  for (const run of runs) {
    if (!run.success) continue;
    const remoteKey = toPosixPath(join("illustrations", plan.slug, run.filename));
    const result = await runScript(
      scriptPath,
      ["--file", run.outputPath, "--key", remoteKey],
      { QINIU_OUTPUT_JSON: "1" },
    );
    if (result.code !== 0 && !result.stdout.includes("---JSON---")) {
      run.error = (run.error ? `${run.error}; ` : "") + (result.stderr || result.stdout || "上传失败").trim();
      continue;
    }

    const marker = "---JSON---";
    const markerIndex = result.stdout.lastIndexOf(marker);
    if (markerIndex < 0) {
      run.error = (run.error ? `${run.error}; ` : "") + "上传结果缺少 JSON 输出";
      continue;
    }

    const jsonText = result.stdout.slice(markerIndex + marker.length).trim();
    try {
      const parsed = JSON.parse(jsonText) as Array<{ success: boolean; url?: string; error?: string }>;
      const first = parsed[0];
      if (first?.success && first.url) {
        run.uploadedUrl = first.url;
      } else {
        run.error = (run.error ? `${run.error}; ` : "") + (first?.error ?? "上传失败");
      }
    } catch (error) {
      run.error = (run.error ? `${run.error}; ` : "") + `上传 JSON 解析失败: ${String(error)}`;
    }
  }
}

function parseAspectRatio(outlinePath: string): string {
  const text = readFileSync(outlinePath, "utf-8");
  const match = text.match(/^aspect_ratio:\s*(.+)$/m);
  return match?.[1]?.trim() || "16:9";
}

function buildSnippet(run: ImageRun): string {
  if (run.success) {
    const target = run.uploadedUrl ?? run.relativePath;
    return `![${run.altText}](${target})`;
  }
  return `<!-- IMAGE PLACEHOLDER: ${run.filename} - ${run.title}${run.error ? ` - ${run.error.replace(/\s+/g, " ")}` : ""} -->`;
}

function createIllustratedArticle(articlePath: string, slug: string, runs: ImageRun[]): string {
  const lines = readFileSync(articlePath, "utf-8").split(/\r?\n/);
  const firstH2Index = lines.findIndex((line) => line.trim().startsWith("## "));
  const introEnd = firstH2Index >= 0 ? firstH2Index : lines.length;
  const sectionStarts: Array<{ title: string; start: number; end: number }> = [];

  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    if (!trimmed.startsWith("## ")) continue;
    const title = trimmed.slice(3).trim();
    let end = lines.length;
    for (let j = i + 1; j < lines.length; j++) {
      if (lines[j].trim().startsWith("## ")) {
        end = j;
        break;
      }
    }
    sectionStarts.push({ title, start: i, end });
  }

  const introRuns = runs.filter((run) => run.position.includes("文章开头导语之后"));
  const bySection = new Map<string, ImageRun[]>();
  for (const run of runs) {
    if (run.position.includes("章节《")) {
      const match = /章节《(.+)》之后/.exec(run.position);
      if (match) {
        const key = match[1];
        const list = bySection.get(key) ?? [];
        list.push(run);
        bySection.set(key, list);
      }
    }
  }

  const output: string[] = [];
  output.push(...lines.slice(0, introEnd));
  if (introRuns.length) {
    output.push("");
    for (const run of introRuns) {
      output.push(buildSnippet(run));
    }
  }

  let cursor = introEnd;
  for (const section of sectionStarts) {
    output.push(...lines.slice(cursor, section.end));
    const sectionRuns = bySection.get(section.title) ?? [];
    if (sectionRuns.length) {
      output.push("");
      for (const run of sectionRuns) {
        output.push(buildSnippet(run));
      }
    }
    cursor = section.end;
  }

  if (cursor < lines.length) {
    output.push(...lines.slice(cursor));
  }

  const articleDir = dirname(articlePath);
  const illustratedPath = join(articleDir, "article.illustrated.md");
  writeFileSync(illustratedPath, `${output.join("\n").replace(/\n{3,}/g, "\n\n").trimEnd()}\n`, "utf-8");
  return illustratedPath;
}

async function main(): Promise<void> {
  const args = parseArgs();
  const articlePath = resolve(args.articlePath);
  if (!existsSync(articlePath)) {
    console.error(`错误：文章不存在 ${articlePath}`);
    process.exit(1);
  }

  const plan = await runPlanning(args);
  const outlineImages = parseOutline(plan.outline_path);
  const aspectRatio = args.aspectRatio ?? parseAspectRatio(plan.outline_path);
  const runs = buildRuns(plan, outlineImages);

  mkdirSync(plan.illustrations_dir, { recursive: true });
  await generateImages(plan, runs, args, aspectRatio);
  if (args.upload) {
    await uploadImages(plan, runs);
  }

  const illustratedArticlePath = createIllustratedArticle(articlePath, plan.slug, runs);
  const uploadedUrls = runs.map((run) => run.uploadedUrl).filter((value): value is string => Boolean(value));
  const summary = {
    success: true,
    article_path: articlePath,
    illustrated_article_path: illustratedArticlePath,
    visual_bible_path: plan.visual_bible_path,
    outline_path: plan.outline_path,
    illustrations_dir: plan.illustrations_dir,
    image_count: runs.filter((run) => run.success).length,
    failed_count: runs.filter((run) => !run.success).length,
    uploaded_urls: uploadedUrls,
    failed_images: runs
      .filter((run) => !run.success)
      .map((run) => ({ filename: run.filename, error: run.error })),
  };

  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
