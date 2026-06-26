import fs from "node:fs";
import path from "node:path";

function resolveProjectRoot(rootDir?: string): string {
  if (rootDir) return rootDir;

  const currentDir = path.resolve(__dirname, "..");
  const configPath = path.join(currentDir, "config");
  if (fs.existsSync(configPath)) return currentDir;
  return path.resolve(currentDir, "..");
}

export function loadJsonConfig<T>(fileName: string, rootDir?: string): T {
  const projectRoot = resolveProjectRoot(rootDir);
  const configPath = path.join(projectRoot, "config", fileName);
  return JSON.parse(fs.readFileSync(configPath, "utf8")) as T;
}
