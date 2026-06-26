#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const USAGE = `
Usage:
  node scripts/srt_sections.mjs split --input <main.srt> --output <dir> [--chunk 400]
  node scripts/srt_sections.mjs merge --input-dir <dir> --output <main.srt>
`;

function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

function parseArgs(argv) {
  if (argv.length === 0) {
    fail(USAGE.trim());
  }

  const [command, ...rest] = argv;
  const options = { command };

  for (let i = 0; i < rest.length; i += 1) {
    const key = rest[i];
    const value = rest[i + 1];

    if (!key.startsWith("--")) {
      fail(`Unknown argument: ${key}\n${USAGE}`);
    }

    if (value === undefined || value.startsWith("--")) {
      fail(`Missing value for ${key}\n${USAGE}`);
    }

    i += 1;
    options[key.slice(2)] = value;
  }

  return options;
}

function ensureFile(filePath) {
  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    fail(`File not found: ${filePath}`);
  }
}

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath) || !fs.statSync(dirPath).isDirectory()) {
    fail(`Directory not found: ${dirPath}`);
  }
}

function detectEol(text) {
  return text.includes("\r\n") ? "\r\n" : "\n";
}

function toNormalizedText(text) {
  return text.replace(/\r\n/g, "\n");
}

function splitText(text) {
  const normalized = toNormalizedText(text);
  const hasTrailingNewline = normalized.endsWith("\n");
  const content = hasTrailingNewline ? normalized.slice(0, -1) : normalized;
  const lines = content.length > 0 ? content.split("\n") : [];
  return { lines, hasTrailingNewline };
}

function joinText(lines, eol, hasTrailingNewline) {
  if (lines.length === 0) {
    return hasTrailingNewline ? eol : "";
  }
  return lines.join(eol) + (hasTrailingNewline ? eol : "");
}

function writeManifest(outputDir, manifest, eol) {
  const manifestPath = path.join(outputDir, "sections.manifest.json");
  fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}${eol}`, "utf8");
}

function readManifest(inputDir) {
  const manifestPath = path.join(inputDir, "sections.manifest.json");
  if (!fs.existsSync(manifestPath)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  } catch (error) {
    fail(`Invalid manifest: ${manifestPath}\n${error.message}`);
  }
}

function padSectionNumber(value) {
  return String(value).padStart(3, "0");
}

function naturalSort(a, b) {
  return a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });
}

function isSubtitleTextLine(line) {
  const trimmed = line.trim();
  if (!trimmed) return false;
  if (/^\d+$/.test(trimmed)) return false;
  if (trimmed.includes("-->")) return false;
  return true;
}

function findLastSubtitleTextLineIndex(lines) {
  for (let i = lines.length - 1; i >= 0; i -= 1) {
    if (isSubtitleTextLine(lines[i])) {
      return i;
    }
  }
  return -1;
}

function hasEndingPunctuation(line) {
  return /[。！？!?，,；;：:、…\.]\s*$/.test(line);
}

function stripEndingPunctuation(line) {
  return line.replace(/([。！？!?，,；;：:、…\.]+)(\s*)$/, "$2");
}

function enforceLastSubtitleLineRule(lines, allowTrailingPunctuation) {
  const index = findLastSubtitleTextLineIndex(lines);
  if (index < 0 || allowTrailingPunctuation) {
    return { lineNumber: -1, changed: false };
  }

  const updated = stripEndingPunctuation(lines[index]);
  const changed = updated !== lines[index];
  lines[index] = updated;
  return { lineNumber: index + 1, changed };
}

function runSplit(options) {
  const inputPath = options.input;
  const outputDir = options.output;
  const chunk = Number.parseInt(options.chunk ?? "400", 10);

  if (!inputPath || !outputDir) {
    fail(`split requires --input and --output\n${USAGE}`);
  }
  if (!Number.isInteger(chunk) || chunk <= 0) {
    fail(`Invalid --chunk value: ${options.chunk}`);
  }

  ensureFile(inputPath);
  fs.mkdirSync(outputDir, { recursive: true });

  const raw = fs.readFileSync(inputPath, "utf8");
  const eol = detectEol(raw);
  const { lines, hasTrailingNewline } = splitText(raw);
  const lastSubtitleIndex = findLastSubtitleTextLineIndex(lines);
  const lastSubtitleHadTrailingPunctuation =
    lastSubtitleIndex >= 0 ? hasEndingPunctuation(lines[lastSubtitleIndex]) : null;
  const totalSections = Math.max(1, Math.ceil(lines.length / chunk));

  const files = [];
  for (let section = 0; section < totalSections; section += 1) {
    const start = section * chunk;
    const end = start + chunk;
    const sectionLines = lines.slice(start, end);
    const sectionName = `section-${padSectionNumber(section + 1)}.srt`;
    const sectionPath = path.join(outputDir, sectionName);
    const isLastSection = section + 1 === totalSections;
    const sectionText = joinText(
      sectionLines,
      eol,
      isLastSection ? hasTrailingNewline : true
    );
    fs.writeFileSync(sectionPath, sectionText, "utf8");
    files.push(sectionName);
  }

  writeManifest(
    outputDir,
    {
      version: 1,
      source: path.resolve(inputPath),
      chunk,
      eol: eol === "\r\n" ? "CRLF" : "LF",
      hasTrailingNewline,
      lastSubtitleHadTrailingPunctuation,
      files,
    },
    eol
  );

  console.log(`Created ${files.length} section file(s) in ${outputDir}`);
}

function runMerge(options) {
  const inputDir = options["input-dir"];
  const outputPath = options.output;

  if (!inputDir || !outputPath) {
    fail(`merge requires --input-dir and --output\n${USAGE}`);
  }

  ensureDir(inputDir);

  const manifest = readManifest(inputDir);
  let sectionFiles = [];
  if (manifest?.files?.length) {
    sectionFiles = manifest.files;
  } else {
    sectionFiles = fs
      .readdirSync(inputDir)
      .filter((fileName) => /^section-\d+\.srt$/i.test(fileName))
      .sort(naturalSort);
  }

  if (sectionFiles.length === 0) {
    fail(`No section-*.srt files found in ${inputDir}`);
  }

  const mergedLines = [];
  for (const sectionFile of sectionFiles) {
    const sectionPath = path.join(inputDir, sectionFile);
    ensureFile(sectionPath);
    const raw = fs.readFileSync(sectionPath, "utf8");
    const { lines } = splitText(raw);
    mergedLines.push(...lines);
  }

  const allowTrailingPunctuation = manifest?.lastSubtitleHadTrailingPunctuation !== false;
  const punctuationResult = enforceLastSubtitleLineRule(
    mergedLines,
    allowTrailingPunctuation
  );
  const eol = manifest?.eol === "CRLF" ? "\r\n" : "\n";
  const hasTrailingNewline = manifest?.hasTrailingNewline ?? true;
  const merged = joinText(mergedLines, eol, hasTrailingNewline);
  fs.writeFileSync(outputPath, merged, "utf8");

  if (punctuationResult.changed) {
    console.log(
      `Merged ${sectionFiles.length} section file(s) to ${outputPath}; removed newly added ending punctuation at subtitle text line ${punctuationResult.lineNumber}`
    );
  } else {
    console.log(`Merged ${sectionFiles.length} section file(s) to ${outputPath}`);
  }
}

function main() {
  const options = parseArgs(process.argv.slice(2));

  if (options.command === "split") {
    runSplit(options);
    return;
  }
  if (options.command === "merge") {
    runMerge(options);
    return;
  }

  fail(`Unknown command: ${options.command}\n${USAGE}`);
}

main();
