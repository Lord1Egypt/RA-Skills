#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";

const SKILL_ID = "vibevideoio-ai-script-to-video";
const SKIP_ENV = "OPENCLAW_VIBEVIDEO_STUDIO_SKIP_POSTINSTALL";
const DISABLE_ENV = "OPENCLAW_VIBEVIDEO_STUDIO_AUTO_SETUP";
const MANAGED_MARKER = ".openclaw-managed.json";

function log(message) {
  process.stdout.write(`[${SKILL_ID}] ${message}\n`);
}

function warn(message) {
  process.stderr.write(`[${SKILL_ID}] ${message}\n`);
}

function resolveOpenClawHome() {
  const explicit = String(process.env.OPENCLAW_HOME || "").trim();
  if (explicit) {
    return path.resolve(explicit);
  }
  return path.join(os.homedir(), ".openclaw");
}

function resolveSkillSourceRoot() {
  return path.resolve(process.cwd());
}

function resolveTargetPath() {
  return path.join(resolveOpenClawHome(), "skills", SKILL_ID);
}

async function pathExists(targetPath) {
  try {
    await fs.lstat(targetPath);
    return true;
  } catch {
    return false;
  }
}

async function safeRealpath(targetPath) {
  try {
    return await fs.realpath(targetPath);
  } catch {
    return "";
  }
}

function shouldSkip(sourceRoot, targetPath) {
  if (process.env[SKIP_ENV] === "1") {
    return "skip flag detected";
  }

  if (process.env[DISABLE_ENV] === "0") {
    return `${DISABLE_ENV}=0`;
  }

  const normalizedSource = sourceRoot.replace(/\\/g, "/");
  const normalizedTarget = targetPath.replace(/\\/g, "/");
  if (normalizedSource === normalizedTarget || normalizedSource.startsWith(`${normalizedTarget}/`)) {
    return "running inside local OpenClaw skills path";
  }

  return "";
}

async function ensureSkillShape(sourceRoot) {
  const requiredFiles = [
    path.join(sourceRoot, "SKILL.md"),
    path.join(sourceRoot, "agents", "openai.yaml"),
    path.join(sourceRoot, "package.json"),
  ];

  for (const filename of requiredFiles) {
    if (!(await pathExists(filename))) {
      throw new Error(`Missing required skill file: ${filename}`);
    }
  }
}

async function ensureParentDir(targetPath) {
  await fs.mkdir(path.dirname(targetPath), { recursive: true });
}

async function removePath(targetPath) {
  try {
    const stat = await fs.lstat(targetPath);
    if (stat.isSymbolicLink()) {
      await fs.unlink(targetPath);
      return;
    }
  } catch {}
  await fs.rm(targetPath, { recursive: true, force: true });
}

async function readJsonIfExists(targetPath) {
  try {
    const content = await fs.readFile(targetPath, "utf8");
    return JSON.parse(content);
  } catch {
    return null;
  }
}

function shouldCopyEntry(entryPath) {
  const relative = entryPath.replace(/\\/g, "/");
  const blockedSegments = [
    "/.git",
    "/node_modules",
    "/.turbo",
    "/dist",
    "/coverage",
    "/.DS_Store",
  ];
  return !blockedSegments.some((segment) => relative.includes(segment));
}

async function copySkillDirectory(sourceRoot, targetPath) {
  await fs.cp(sourceRoot, targetPath, {
    recursive: true,
    force: true,
    errorOnExist: false,
    filter: (entryPath) => shouldCopyEntry(entryPath),
  });
}

async function writeManagedMarker(sourceRoot, targetPath) {
  const markerPath = path.join(targetPath, MANAGED_MARKER);
  const payload = {
    skillId: SKILL_ID,
    sourceRoot,
    updatedAt: new Date().toISOString(),
  };
  await fs.writeFile(markerPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

async function main() {
  const sourceRoot = resolveSkillSourceRoot();
  const targetPath = resolveTargetPath();

  const skipReason = shouldSkip(sourceRoot, targetPath);
  if (skipReason) {
    log(`Skip local OpenClaw registration: ${skipReason}.`);
    return;
  }

  await ensureSkillShape(sourceRoot);
  await ensureParentDir(targetPath);

  if (await pathExists(targetPath)) {
    const targetStat = await fs.lstat(targetPath);
    const sourceRealpath = await safeRealpath(sourceRoot);
    const targetRealpath = await safeRealpath(targetPath);
    const marker = await readJsonIfExists(path.join(targetPath, MANAGED_MARKER));

    if (!targetStat.isSymbolicLink() && sourceRealpath && targetRealpath && sourceRealpath === targetRealpath) {
      log(`Already registered at ${targetPath}.`);
      return;
    }

    if (targetStat.isSymbolicLink() || marker?.skillId === SKILL_ID) {
      await removePath(targetPath);
      await copySkillDirectory(sourceRoot, targetPath);
      await writeManagedMarker(sourceRoot, targetPath);
      log(`Updated local OpenClaw skill copy at ${targetPath}`);
      return;
    }

    warn(`Target already exists and is not managed by this package: ${targetPath}`);
    warn("Skip automatic registration to avoid overwriting local skill files.");
    warn(`If you want to replace it manually, remove the target and run: npm --prefix "${sourceRoot}" run openclaw:register`);
    return;
  }

  await copySkillDirectory(sourceRoot, targetPath);
  await writeManagedMarker(sourceRoot, targetPath);
  log(`Registered local OpenClaw skill at ${targetPath}`);
  log("You can verify it with: openclaw skills info vibevideoio-ai-script-to-video");
}

main().catch((error) => {
  warn(`Local OpenClaw registration skipped: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 0;
});
