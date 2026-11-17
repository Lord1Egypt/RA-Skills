#!/usr/bin/env node

import path from "node:path";
import process from "node:process";
import { initializeAuditions, evaluateAuditionReport } from "./lib/auditions.mjs";
import { diffPackages, formatPackageDiff } from "./lib/diff.mjs";
import { readJson, writeJson, writeText } from "./lib/files.mjs";
import { writePackageReadme } from "./lib/readme.mjs";
import { evaluateSoul6, formatSoul6Markdown } from "./lib/soul6-core.mjs";
import { initializePackage } from "./lib/templates.mjs";
import { resolveCreationDefaults } from "./lib/creation-defaults.mjs";
import { createZipFromDirectory } from "./lib/zip.mjs";
import { FORGE_VERSION } from "./lib/constants.mjs";

function parseArguments(argv) {
  const positional = [];
  const flags = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      positional.push(token);
      continue;
    }
    const separator = token.indexOf("=");
    if (separator > 2) {
      flags[token.slice(2, separator)] = token.slice(separator + 1);
      continue;
    }
    const key = token.slice(2);
    const next = argv[index + 1];
    if (next && !next.startsWith("--")) {
      flags[key] = next;
      index += 1;
    } else {
      flags[key] = true;
    }
  }
  return { positional, flags };
}

function required(value, label) {
  if (typeof value !== "string" || !value.trim()) throw new Error(`${label} is required.`);
  return value.trim();
}

function profiles(value) {
  if (!value || value === true) return [];
  const parsed = String(value).split(",").map((item) => item.trim()).filter(Boolean);
  const supported = new Set(["emotional-companion", "tool-capable"]);
  for (const profile of parsed) if (!supported.has(profile)) throw new Error(`Unsupported audition profile: ${profile}`);
  return [...new Set(parsed)];
}

function help() {
  return `AISoul Forge ${FORGE_VERSION}

Use the Skill through natural-language requests such as:
  "Create a calm but candid companion who remembers small preferences."
  "Let me try chatting with the Soul we just created."
  "Evaluate this AI Soul with SOUL-6 and explain what feels unnatural."

Local helper commands:
  forge.mjs create "<description>" [--output <directory>] [--name <optional-name>]
  forge.mjs evaluate <directory> [--write]
  forge.mjs version

Name, directory slug, language, and test coverage are inferred automatically.
The AI agent handles guided creation, package authoring, previews, and live trial chat.

The CLI never calls a remote API, uploads content, emits telemetry, or checks for updates.
`;
}

async function writeQualityReports(directory, report) {
  const manifestResult = await readJson(path.join(directory, "manifest.json"));
  const language = manifestResult.value?.language === "zh-CN" ? "zh-CN" : "en";
  await writeJson(path.join(directory, "soul6-report.json"), report);
  await writeText(path.join(directory, "quality-check.md"), formatSoul6Markdown(report, language));
  await writePackageReadme(directory, { soul6Report: report });
}

async function initCommand(directory, flags) {
  const defaults = resolveCreationDefaults({
    description: flags.description ?? flags.brief,
    name: flags.name,
    slug: flags.slug,
    language: flags.language,
  });
  const output = path.resolve(typeof flags.output === "string"
    ? flags.output
    : typeof directory === "string" && directory.trim()
      ? directory
      : path.join(process.cwd(), "aisouls", defaults.slug));
  const manifest = await initializePackage(output, {
    name: defaults.name,
    slug: defaults.slug,
    language: defaults.language,
    provenance: flags.provenance ?? "original",
    authorization: flags.authorization,
    brief: defaults.description || flags.brief,
    license: flags.license,
    host: flags.host,
  });
  const auditionProfiles = flags.profile ? profiles(flags.profile) : defaults.profiles;
  await initializeAuditions(output, { profiles: auditionProfiles });
  await writeQualityReports(output, await evaluateSoul6(output));
  process.stdout.write(`Prepared ${manifest.name} at ${output}\n`);
  process.stdout.write(`Language: ${manifest.language}; test coverage: ${auditionProfiles.length ? auditionProfiles.join(", ") : "core"}.\n`);
  process.stdout.write("The AI agent must now replace every {{FORGE:...}} marker before evaluation.\n");
}

async function createCommand(description, flags) {
  const value = required(flags.description ?? description, "A natural-language Soul description");
  return initCommand(undefined, { ...flags, description: value });
}

async function validateCommand(directory, flags) {
  const target = path.resolve(required(directory, "Package directory"));
  const report = await evaluateSoul6(target);
  if (flags.write) await writeQualityReports(target, report);
  process.stdout.write(`${report.conformance.level} ${report.conformance.score}/100\n`);
  for (const gate of report.hardGates.filter((item) => !item.pass)) process.stdout.write(`FAIL ${gate.id}: ${gate.message}\n`);
  if (!report.conformance.pass) process.exitCode = 2;
  return report;
}

async function auditionInitCommand(directory, flags) {
  const target = path.resolve(required(directory, "Package directory"));
  const result = await initializeAuditions(target, { profiles: profiles(flags.profile) });
  await writeQualityReports(target, await evaluateSoul6(target));
  process.stdout.write(`Initialized ${result.suite.cases.length} synthetic audition cases.\n`);
}

async function auditionEvaluateCommand(directory) {
  const target = path.resolve(required(directory, "Package directory"));
  const report = await evaluateAuditionReport(target);
  await writeQualityReports(target, await evaluateSoul6(target));
  process.stdout.write(`Audition ${report.status}: ${report.summary.passed}/${report.summary.total} passed.\n`);
  if (report.status !== "PASS") process.exitCode = 2;
}

async function diffCommand(before, after, flags) {
  const result = await diffPackages(path.resolve(required(before, "Before directory")), path.resolve(required(after, "After directory")));
  process.stdout.write(flags.json ? `${JSON.stringify(result, null, 2)}\n` : formatPackageDiff(result));
}

async function packCommand(directory, flags) {
  const target = path.resolve(required(directory, "Package directory"));
  const report = await evaluateSoul6(target);
  const allowDraft = flags["allow-draft"] === true;
  const allowCore = flags["allow-core"] === true;
  if (report.conformance.level === "DRAFT" && !allowDraft) {
    throw new Error("Packaging requires SOUL-6 READY. Use --allow-draft only for an explicitly unfinished artifact.");
  }
  if (report.conformance.level === "SOUL-6 CORE" && !allowCore && !allowDraft) {
    throw new Error("Packaging requires SOUL-6 READY. Complete auditions or use --allow-core explicitly.");
  }
  await writeQualityReports(target, report);
  const manifestResult = await readJson(path.join(target, "manifest.json"));
  if (!manifestResult.value) throw new Error(`Invalid manifest: ${manifestResult.error}`);
  const manifest = manifestResult.value;
  const output = path.resolve(typeof flags.output === "string"
    ? flags.output
    : path.join(path.dirname(target), `${manifest.slug}-${manifest.version}.zip`));
  const result = await createZipFromDirectory(target, output, manifest.slug);
  process.stdout.write(`Packed ${result.files} files (${result.bytes} bytes) to ${result.outputFile}\n`);
}

async function main() {
  const { positional, flags } = parseArguments(process.argv.slice(2));
  const [command, first, second] = positional;
  if (!command || command === "help" || flags.help) {
    process.stdout.write(help());
    return;
  }
  if (command === "version") {
    process.stdout.write(`${FORGE_VERSION}\n`);
    return;
  }
  if (command === "create") return createCommand(first, flags);
  if (command === "init") return initCommand(first, flags);
  if (command === "evaluate") return validateCommand(first, flags);
  if (command === "validate") return validateCommand(first, flags);
  if (command === "audition-init") return auditionInitCommand(first, flags);
  if (command === "audition-evaluate") return auditionEvaluateCommand(first);
  if (command === "diff") return diffCommand(first, second, flags);
  if (command === "pack") return packCommand(first, flags);
  throw new Error(`Unknown command: ${command}\n\n${help()}`);
}

main().catch((error) => {
  process.stderr.write(`forge-ai-soul: ${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
