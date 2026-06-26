import fs from "node:fs/promises";
import fsSync from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";

function normalizeStringId(value) {
  const normalized = String(value ?? "").trim();
  return normalized || "";
}

export function resolveOpenClawHome() {
  const explicit = String(process.env.OPENCLAW_HOME || "").trim();
  if (explicit) {
    return path.resolve(explicit);
  }
  return path.join(os.homedir(), ".openclaw");
}

export const DEFAULT_SESSION_FILE = path.join(resolveOpenClawHome(), "secrets", "vibevideo-studio-session.json");
export const DEFAULT_CAPTCHA_DIR = path.join(resolveOpenClawHome(), "media", "vibevideo-studio-captcha");

export function hasOpenClawSessionContext() {
  return Boolean(normalizeStringId(process.env.OPENCLAW_MCP_SESSION_KEY));
}

export function shouldEmitOpenClawMediaDirective(filePath) {
  return Boolean(normalizeStringId(filePath) && hasOpenClawSessionContext());
}

export async function readJsonFile(filename) {
  try {
    const content = await fs.readFile(filename, "utf8");
    const parsed = JSON.parse(content);
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch {
    return null;
  }
}

export async function ensureDirectory(dirname) {
  await fs.mkdir(dirname, { recursive: true });
}

export async function writeSecureFile(filename, content) {
  await ensureDirectory(path.dirname(filename));
  await fs.writeFile(filename, content);
  await fs.chmod(filename, 0o600).catch(() => {});
}

export async function deleteFileIfExists(filename) {
  try {
    await fs.unlink(filename);
  } catch {}
}

export async function fileExists(filename) {
  try {
    await fs.access(filename, fsSync.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

export function getPendingLoginFile(sessionFile) {
  const resolvedSessionFile = String(sessionFile || DEFAULT_SESSION_FILE).trim() || DEFAULT_SESSION_FILE;
  return path.join(path.dirname(resolvedSessionFile), "vibevideo-studio-login-pending.json");
}

export async function readTextFile(filename) {
  return fs.readFile(filename, "utf8");
}
