/**
 * `.env` 加载（含权限检查与安全敏感变量隔离）。
 *
 * 加载顺序：`XIAOAI_ENV_FILE`（显式指定）→ 否则 `scripts/.env` → 技能根目录 `.env`。
 * 全部使用绝对路径，避免依赖当前工作目录（登录前会 chdir 到状态目录）。
 *
 * 安全约束：
 * - `.env` 通常包含 passToken，读取前先做权限检查；可被同组/其他用户修改时直接拒绝。
 * - `.env` 不得设置安全敏感变量（LOCALAPPDATA/APPDATA/USERPROFILE/HOME/XDG_STATE_HOME、
 *   XIAOAI_ALLOW_INSECURE_STATE_DIR），否则可被用来把缓存目录“洗白”到公共位置或
 *   静默打开不安全开关。这些变量只接受进程环境。
 */

import fs from "node:fs";
import path from "node:path";

import dotenv from "dotenv";

import { ConfigError } from "./errors.js";
import { inspectEnvFile } from "./state.js";

export const ENV_FILE_ENV_VAR = "XIAOAI_ENV_FILE";

/** 不允许由 .env 注入的安全敏感变量。 */
export const SECURITY_ENV_KEYS = [
  "LOCALAPPDATA",
  "APPDATA",
  "USERPROFILE",
  "HOME",
  "XDG_STATE_HOME",
  "ProgramData",
  "PUBLIC",
  "SystemRoot",
  "windir",
  "TEMP",
  "TMP",
  "TMPDIR",
  "XIAOAI_ALLOW_INSECURE_STATE_DIR",
];

/**
 * 计算 .env 候选路径（不检查是否存在）。
 *
 * @param {Record<string, string | undefined>} [env]
 * @param {{ scriptDir: string, skillRoot: string }} roots
 * @returns {string[]}
 */
export function resolveEnvFiles(env = process.env, { scriptDir, skillRoot }) {
  const explicit = String(env[ENV_FILE_ENV_VAR] ?? "").trim();
  if (explicit) {
    return [path.resolve(explicit)];
  }
  return [path.join(scriptDir, ".env"), path.join(skillRoot, ".env")];
}

/**
 * 逐个加载存在的 .env 文件，检查权限，并阻止安全敏感变量注入。
 *
 * @param {{ env?: Record<string, string | undefined>, scriptDir: string, skillRoot: string, warn?: (line: string) => void }} options
 * @returns {string[]} 实际加载的文件列表
 */
export function loadEnvironment(options) {
  const env = options.env ?? process.env;
  const warn = options.warn ?? ((line) => process.stderr.write(`${line}\n`));
  const files = resolveEnvFiles(env, options);
  const loaded = [];

  for (const file of files) {
    let stats;
    try {
      stats = fs.lstatSync(file);
    } catch (error) {
      if (error?.code === "ENOENT") {
        continue;
      }
      throw new ConfigError(`无法检查环境变量文件 ${file}：${error.message}`);
    }
    if (stats.isDirectory()) {
      throw new ConfigError(`环境变量路径是目录：${file}`);
    }

    inspectEnvFile(file, { warn });

    const before = new Map(SECURITY_ENV_KEYS.map((key) => [key, process.env[key]]));
    // quiet: true 避免 dotenv v17 向 stdout 打印提示，破坏「stdout 只有 JSON」的契约。
    const result = dotenv.config({ path: file, quiet: true });
    if (result?.error) {
      throw new ConfigError(`无法读取环境变量文件 ${file}：${result.error.message}`);
    }

    for (const key of SECURITY_ENV_KEYS) {
      if (before.get(key) === undefined && process.env[key] !== undefined) {
        delete process.env[key];
        warn(`⚠️  已忽略 ${file} 中的安全敏感变量 ${key}（请通过进程环境设置）。`);
      }
    }

    loaded.push(file);
  }
  return loaded;
}
