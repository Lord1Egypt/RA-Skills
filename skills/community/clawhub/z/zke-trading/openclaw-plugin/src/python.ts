import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import type { PluginConfig } from "./types.js";

const execFileAsync = promisify(execFile);

function defaultTradingHome(): string {
  return process.env.ZKE_TRADING_HOME || path.join(homedir(), ".zke-trading");
}

function defaultPythonBin(tradingHome: string): string {
  const venvPython = path.join(tradingHome, ".venv", "bin", "python");
  if (existsSync(venvPython)) return venvPython;
  return process.env.ZKE_TRADING_PYTHON || "python3";
}

export function resolveRuntime(config?: PluginConfig) {
  const tradingHome = config?.tradingHome || defaultTradingHome();
  const pythonBin = config?.pythonBin?.trim()
    ? config.pythonBin.trim()
    : defaultPythonBin(tradingHome);

  return {
    tradingHome,
    pythonBin,
    mainPy: path.join(tradingHome, "main.py"),
  };
}

function extractLastJsonBlock(text: string): any {
  const trimmed = text.trim();
  if (!trimmed) return null;

  try {
    return JSON.parse(trimmed);
  } catch {
    // continue
  }

  const candidates: string[] = [];
  const objectStart = trimmed.lastIndexOf("{");
  const arrayStart = trimmed.lastIndexOf("[");

  if (objectStart >= 0) candidates.push(trimmed.slice(objectStart));
  if (arrayStart >= 0) candidates.push(trimmed.slice(arrayStart));

  for (const c of candidates) {
    try {
      return JSON.parse(c);
    } catch {
      // continue
    }
  }

  throw new Error(`Could not parse JSON from CLI output:\n${trimmed}`);
}

export async function runMainJson(
  argv: string[],
  config?: PluginConfig
): Promise<any> {
  const runtime = resolveRuntime(config);

  if (!existsSync(runtime.mainPy)) {
    throw new Error(`main.py not found: ${runtime.mainPy}`);
  }

  const { stdout, stderr } = await execFileAsync(
    runtime.pythonBin,
    [runtime.mainPy, ...argv],
    {
      cwd: runtime.tradingHome,
      maxBuffer: 10 * 1024 * 1024,
      env: {
        ...process.env,
      },
    }
  );

  const merged = [stdout, stderr].filter(Boolean).join("\n").trim();
  if (!merged) return { ok: true };

  return extractLastJsonBlock(merged);
}
