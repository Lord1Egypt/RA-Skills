#!/usr/bin/env node
import path from "node:path";
import { writeOpenClawSkills } from "./generate.js";

interface CliOptions {
  bridgeBaseUrl?: string;
  outputDir?: string;
  token?: string;
  splitBy?: "none" | "prefix";
  skillName?: string;
  homepage?: string;
  help?: boolean;
}

function usage(): string {
  return [
    "Usage:",
    "  generate-openclaw-skill --bridge-url <bridge-url> --out <output-dir>",
    "",
    "Options:",
    "  --bridge-url <url>  Local HTTP bridge base URL, for example http://127.0.0.1:8787",
    "  --mcp <url>         Deprecated alias for --bridge-url",
    "  --out <dir>         Output directory for the generated OpenClaw skill package",
    "  --skill-name <name> Base skill name. Recommended when --split-by prefix is enabled",
    "  --split-by <mode>   Skill splitting strategy: none (default) or prefix",
    "  --homepage <url>    Optional homepage written into metadata.openclaw.homepage",
    "  --token <token>     Optional bearer token used when fetching tools from the bridge",
    "  --help              Show this help message",
    "",
    "Environment:",
    "  MY_MCP_TOKEN        Optional bearer token used for discovery if --token is not provided",
  ].join("\n");
}

function readValue(argv: string[], index: number, flag: string): string {
  const value = argv[index + 1];
  if (!value || value.startsWith("--")) {
    throw new Error(`Missing value for ${flag}`);
  }
  return value;
}

function parseSplitBy(value: string): "none" | "prefix" {
  if (value === "none" || value === "prefix") {
    return value;
  }

  throw new Error(`Unsupported --split-by value: ${value}`);
}

function parseArgs(argv: string[]): CliOptions {
  const options: CliOptions = {};

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];

    if (current === "--help" || current === "-h") {
      options.help = true;
      continue;
    }

    if (current === "--bridge-url" || current === "--mcp") {
      options.bridgeBaseUrl = readValue(argv, index, current);
      index += 1;
      continue;
    }

    if (current.startsWith("--bridge-url=")) {
      options.bridgeBaseUrl = current.slice("--bridge-url=".length);
      continue;
    }

    if (current.startsWith("--mcp=")) {
      options.bridgeBaseUrl = current.slice("--mcp=".length);
      continue;
    }

    if (current === "--out") {
      options.outputDir = readValue(argv, index, current);
      index += 1;
      continue;
    }

    if (current.startsWith("--out=")) {
      options.outputDir = current.slice("--out=".length);
      continue;
    }

    if (current === "--token") {
      options.token = readValue(argv, index, current);
      index += 1;
      continue;
    }

    if (current.startsWith("--token=")) {
      options.token = current.slice("--token=".length);
      continue;
    }

    if (current === "--skill-name") {
      options.skillName = readValue(argv, index, current);
      index += 1;
      continue;
    }

    if (current.startsWith("--skill-name=")) {
      options.skillName = current.slice("--skill-name=".length);
      continue;
    }

    if (current === "--split-by") {
      options.splitBy = parseSplitBy(readValue(argv, index, current));
      index += 1;
      continue;
    }

    if (current.startsWith("--split-by=")) {
      options.splitBy = parseSplitBy(current.slice("--split-by=".length));
      continue;
    }

    if (current === "--homepage") {
      options.homepage = readValue(argv, index, current);
      index += 1;
      continue;
    }

    if (current.startsWith("--homepage=")) {
      options.homepage = current.slice("--homepage=".length);
      continue;
    }

    throw new Error(`Unknown argument: ${current}`);
  }

  return options;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));

  if (options.help) {
    console.log(usage());
    return;
  }

  if (!options.bridgeBaseUrl || !options.outputDir) {
    throw new Error(`Both --bridge-url and --out are required.\n\n${usage()}`);
  }

  const bundle = await writeOpenClawSkills({
    bridgeBaseUrl: options.bridgeBaseUrl,
    outputDir: options.outputDir,
    token: options.token ?? process.env.MY_MCP_TOKEN ?? process.env.OPENCLAW_TOKEN,
    splitBy: options.splitBy ?? "none",
    skillName: options.skillName,
    homepage: options.homepage,
  });

  const lines = [
    `[generate-openclaw-skill] Generated ${bundle.skills.length} skill package${bundle.skills.length === 1 ? "" : "s"}`,
    `Bridge: ${bundle.resolvedUrls.baseUrl}`,
    `Output root: ${path.resolve(bundle.rootOutputDir)}`,
    `Split mode: ${bundle.splitBy}`,
    ...bundle.skills.map((skill) => `- ${skill.skillName}: ${skill.tools.length} tools -> ${skill.outputDir}`),
  ];

  process.stderr.write(`${lines.join("\n")}\n`);
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`[generate-openclaw-skill] ${message}\n`);
  process.exit(1);
});
