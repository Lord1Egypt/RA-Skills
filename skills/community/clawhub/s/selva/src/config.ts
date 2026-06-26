import { mkdir, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";

export interface SelvaCliConfig {
  apiKey?: string;
}

let apiBaseUrl = "https://api.useselva.com";

export function configPath() {
  return path.join(homedir(), "selva", "config.json");
}

export async function readConfig(): Promise<SelvaCliConfig> {
  const filePath = configPath();

  try {
    const raw = await readFile(filePath, "utf8");
    return JSON.parse(raw) as SelvaCliConfig;
  } catch {
    return {};
  }
}

export async function writeConfig(next: SelvaCliConfig) {
  const filePath = configPath();
  const dir = path.dirname(filePath);
  await mkdir(dir, { recursive: true });
  await writeFile(filePath, JSON.stringify(next, null, 2), "utf8");
}

export async function requireApiKey() {
  const config = await readConfig();
  if (!config.apiKey) {
    throw new Error("API key not found. Run: selva register");
  }
  return config.apiKey;
}

export function setApiBaseUrl(value: string) {
  apiBaseUrl = value.replace(/\/$/, "");
}

export async function resolveBaseUrl() {
  return apiBaseUrl;
}
