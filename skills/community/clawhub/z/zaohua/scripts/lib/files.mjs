import { mkdir, readFile, readdir, rename, stat, writeFile } from "node:fs/promises";
import path from "node:path";

export async function pathExists(target) {
  try {
    await stat(target);
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

export async function readText(target) {
  try {
    return await readFile(target, "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") return "";
    throw error;
  }
}

export async function readJson(target) {
  const raw = await readText(target);
  if (!raw) return { value: null, error: "missing" };
  try {
    return { value: JSON.parse(raw), error: null };
  } catch (error) {
    return { value: null, error: error instanceof Error ? error.message : "invalid_json" };
  }
}

export async function writeText(target, content) {
  await mkdir(path.dirname(target), { recursive: true });
  await writeFile(target, content.endsWith("\n") ? content : `${content}\n`, "utf8");
}

export async function writeJson(target, value) {
  await mkdir(path.dirname(target), { recursive: true });
  const temporary = `${target}.tmp-${process.pid}`;
  await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  await rename(temporary, target);
}

export async function assertEmptyDirectory(target) {
  if (!(await pathExists(target))) {
    await mkdir(target, { recursive: true });
    return;
  }
  const entries = await readdir(target);
  if (entries.length > 0) throw new Error(`Output directory is not empty: ${target}`);
}

export async function listFilesRecursive(root, options = {}) {
  const ignoredNames = new Set(options.ignoredNames ?? [".DS_Store", ".git", "node_modules"]);
  const output = [];

  async function visit(current, relative) {
    const entries = await readdir(current, { withFileTypes: true });
    entries.sort((a, b) => a.name.localeCompare(b.name));
    for (const entry of entries) {
      if (ignoredNames.has(entry.name)) continue;
      const absolute = path.join(current, entry.name);
      const childRelative = relative ? `${relative}/${entry.name}` : entry.name;
      if (entry.isDirectory()) await visit(absolute, childRelative);
      else if (entry.isFile()) output.push({ absolute, relative: childRelative.replaceAll("\\", "/") });
    }
  }

  await visit(root, "");
  return output;
}

export function normalizeLanguage(value) {
  if (value === "zh" || value === "zh-CN") return "zh-CN";
  if (value === "en" || value === "en-US") return "en";
  throw new Error(`Unsupported language: ${value}`);
}

export function assertSlug(value) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value) || value.length > 80) {
    throw new Error("Slug must contain lowercase letters, digits, and single hyphens only.");
  }
  return value;
}

export function portableRelativePath(value) {
  const normalized = value.replaceAll("\\", "/").replace(/^\/+/, "");
  if (!normalized || normalized.split("/").some((part) => part === ".." || part === ".")) {
    throw new Error(`Unsafe relative path: ${value}`);
  }
  return normalized;
}
