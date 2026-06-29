/**
 * 技能沉淀插件的通用工具函数。
 *
 * 包含原子写文件、路径安全校验、YAML frontmatter 校验与解析、
 * 以及技能元数据读写等能力。
 */

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import type { OpenClawConfig } from "openclaw/plugin-sdk";
import {
  normalizeAgentId,
  resolveAgentWorkspaceDir,
  resolveDefaultAgentId,
} from "openclaw/plugin-sdk";
import type {
  SedimentMeta,
  SkillEditRecord,
  SkillFrontmatter,
  SkillMeta,
  SkillPrerequisites,
} from "./types.js";
import {
  ALLOWED_SUBDIRS,
  MAX_DESCRIPTION_LENGTH,
  MAX_NAME_LENGTH,
  MAX_SKILL_CONTENT_CHARS,
  MAX_SKILL_FILE_BYTES,
  VALID_NAME_RE,
  VALID_PLATFORMS,
} from "./types.js";

// ---------------------------------------------------------------------------
// 路径解析
// ---------------------------------------------------------------------------

/**
 * 沉淀技能保存目录名。
 *
 * 所有由 skill_manage 工具创建/编辑的技能都隔离在 `<agent workspace>/sediment_skills/` 下，
 * 与 `<agent workspace>/skills/` 同级，物理隔离确保：
 * 1. OpenClaw 核心引擎的技能加载器不会自动发现沉淀技能（仅扫描 skills/ 直接子目录）；
 * 2. 插件无法触及原生/官方技能目录（如 `<skills>/<official>/`）。
 */
export const SEDIMENT_DIR_NAME = "sediment_skills";

/**
 * 按 agent 解析技能根目录：`<agent workspace>/skills`。
 *
 * 该目录是 list/view 等只读动作的扫描根，包含原生/官方技能。
 * 写动作请使用 {@link resolveSedimentDirForAgent}。
 *
 * 与 {@link resolveAgentWorkspaceDir} 对齐，每个 agent 拥有独立的技能存储目录。
 */
export function resolveSkillsDirForAgent(cfg: OpenClawConfig, agentId: string | undefined): string {
  const id =
    typeof agentId === "string" && agentId.trim()
      ? normalizeAgentId(agentId)
      : resolveDefaultAgentId(cfg);
  return path.join(resolveAgentWorkspaceDir(cfg, id), "skills");
}

/**
 * 按 agent 解析技能沉淀目录：`<agent workspace>/sediment_skills`。
 *
 * 与 `<agent workspace>/skills/` 同级，OpenClaw 核心引擎不会扫描此目录，
 * 确保沉淀技能在未迁移到 skills/ 之前不会被自动加载。
 *
 * 这是 skill_manage 工具所有写动作（create/edit/patch/delete/write_file/remove_file）
 * 的唯一基目录。物理隔离原生/官方技能，确保插件无法修改非沉淀技能。
 */
export function resolveSedimentDirForAgent(
  cfg: OpenClawConfig,
  agentId: string | undefined,
): string {
  const id =
    typeof agentId === "string" && agentId.trim()
      ? normalizeAgentId(agentId)
      : resolveDefaultAgentId(cfg);
  return path.join(resolveAgentWorkspaceDir(cfg, id), SEDIMENT_DIR_NAME);
}

/**
 * 构建技能目录路径（位于指定基目录之下）。
 */
export function resolveSkillDir(baseDir: string, name: string): string {
  return path.join(baseDir, name);
}

// ---------------------------------------------------------------------------
// Gateway 重启后内存中的会话级审查状态（水位线、handoff 上下文）会全部丢失，
// 导致同一长会话被重复审查、重复沉淀。
// 解决方案：在 sediment_skills/ 下维护一个 `.review_checkpoint.json` 文件，
// 仅在 review 完成推进水位线时写入，启动时一次性加载恢复。

/** checkpoint 文件名（点开头，对 listSedimentSkillStats 等扫描不可见）。 */
export const REVIEW_CHECKPOINT_FILENAME = ".review_checkpoint.json";

/** checkpoint 文件格式版本。 */
const CHECKPOINT_VERSION = 1;

/** checkpoint 条目的默认 TTL（3 天）。超过此时间的条目在加载时丢弃。 */
const CHECKPOINT_ENTRY_TTL_MS = 3 * 86_400_000;

/** checkpoint 文件中单个会话的持久化字段。 */
export interface CheckpointEntry {
  lastReviewedToolCalls: number;
  lastReviewedTurns: number;
  lastSedimentedMessageCount: number;
  lastSedimentHandoff: string | null;
  /** 上次触发 review 的时间戳（epoch ms）。持久化以保证频繁重启时冷却计时器不失效。 */
  lastSpawnedAt: number;
  /** 写入时间（ISO 8601），用于 TTL 清理。 */
  savedAt: string;
}

/** checkpoint 文件的完整结构。 */
interface CheckpointFile {
  version: number;
  sessions: Record<string, CheckpointEntry>;
}

/**
 * 解析 checkpoint 文件路径。
 */
export function resolveCheckpointPath(sedimentDir: string): string {
  return path.join(sedimentDir, REVIEW_CHECKPOINT_FILENAME);
}

/**
 * 从磁盘加载 checkpoint，返回有效（未过期）的条目。
 *
 * - 文件不存在 / 解析失败 → 返回空 Map（静默降级，不阻塞启动）
 * - 自动丢弃超过 TTL 的陈旧条目
 */
export function loadCheckpoint(sedimentDir: string): Map<string, CheckpointEntry> {
  const result = new Map<string, CheckpointEntry>();
  const filePath = resolveCheckpointPath(sedimentDir);

  let raw: string;
  try {
    raw = fs.readFileSync(filePath, "utf-8");
  } catch {
    return result; // 文件不存在，正常情况
  }

  let data: CheckpointFile;
  try {
    data = JSON.parse(raw) as CheckpointFile;
  } catch {
    return result; // 文件损坏，静默降级
  }

  if (data.version !== CHECKPOINT_VERSION || !data.sessions) {
    return result;
  }

  const now = Date.now();
  for (const [key, entry] of Object.entries(data.sessions)) {
    // TTL 清理：丢弃过期条目
    const savedMs = Date.parse(entry.savedAt);
    if (Number.isNaN(savedMs) || now - savedMs > CHECKPOINT_ENTRY_TTL_MS) {
      continue;
    }
    // 基本类型校验（防御损坏数据）
    if (
      typeof entry.lastReviewedToolCalls !== "number" ||
      typeof entry.lastReviewedTurns !== "number" ||
      typeof entry.lastSedimentedMessageCount !== "number"
    ) {
      continue;
    }
    // 兼容旧 checkpoint 文件：lastSpawnedAt 可能不存在，规范化为 number（缺失时默认 0）。
    if (typeof entry.lastSpawnedAt !== "number") {
      entry.lastSpawnedAt = 0;
    }
    result.set(key, entry);
  }

  return result;
}

/**
 * 将单个会话的水位线状态保存到 checkpoint 文件。
 *
 * 采用 read-merge-write 模式：读取现有文件 → 合并/覆盖目标 key → 原子写回。
 * 同时顺手清理过期条目，保持文件精简。
 *
 * 写入失败静默降级（仅日志），不影响主流程。
 */
export function saveCheckpointEntry(
  sedimentDir: string,
  sessionKey: string,
  entry: CheckpointEntry,
): void {
  const filePath = resolveCheckpointPath(sedimentDir);

  // 读取现有数据
  let data: CheckpointFile = { version: CHECKPOINT_VERSION, sessions: {} };
  try {
    const raw = fs.readFileSync(filePath, "utf-8");
    const parsed = JSON.parse(raw) as CheckpointFile;
    if (parsed.version === CHECKPOINT_VERSION && parsed.sessions) {
      data = parsed;
    }
  } catch {
    // 文件不存在或损坏，从空开始
  }

  // 合并目标条目
  data.sessions[sessionKey] = entry;

  // 顺手清理过期条目
  const now = Date.now();
  for (const [key, e] of Object.entries(data.sessions)) {
    const savedMs = Date.parse(e.savedAt);
    if (Number.isNaN(savedMs) || now - savedMs > CHECKPOINT_ENTRY_TTL_MS) {
      delete data.sessions[key];
    }
  }

  // 原子写入
  atomicWriteText(filePath, JSON.stringify(data, null, 2) + "\n");
}

/**
 * 从 checkpoint 文件中删除指定会话的条目。
 */
export function removeCheckpointEntry(sedimentDir: string, sessionKey: string): void {
  const filePath = resolveCheckpointPath(sedimentDir);

  let data: CheckpointFile;
  try {
    const raw = fs.readFileSync(filePath, "utf-8");
    data = JSON.parse(raw) as CheckpointFile;
  } catch {
    return; // 文件不存在或损坏，无需清理
  }

  if (data.version !== CHECKPOINT_VERSION || !data.sessions) {
    return;
  }

  if (!(sessionKey in data.sessions)) {
    return; // 条目不存在，无需写入
  }

  delete data.sessions[sessionKey];
  atomicWriteText(filePath, JSON.stringify(data, null, 2) + "\n");
}

// ---------------------------------------------------------------------------
// 校验辅助函数
// ---------------------------------------------------------------------------

/**
 * 校验技能名。合法返回 undefined，不合法返回错误信息。
 */
export function validateName(name: string): string | undefined {
  if (!name) {
    return "Skill name is required.";
  }
  if (name.length > MAX_NAME_LENGTH) {
    return `Skill name exceeds ${MAX_NAME_LENGTH} characters.`;
  }
  if (!VALID_NAME_RE.test(name)) {
    return (
      `Invalid skill name '${name}'. Use lowercase letters, numbers, ` +
      "hyphens, dots, and underscores. Must start with a letter or digit."
    );
  }
  return undefined;
}

/**
 * 从内容中提取原始 YAML 区块（位于起止 `---` 之间）。
 * 成功返回 `{ yaml, ... }`，失败返回错误字符串。
 */
function extractFrontmatterBlock(
  content: string,
): { yaml: string; endIndex: number; endMatch: RegExpMatchArray } | string {
  if (!content.trim()) {
    return "Content cannot be empty.";
  }
  if (!content.startsWith("---")) {
    return "SKILL.md must start with YAML frontmatter (---). See existing skills for format.";
  }

  const endMatch = content.slice(3).match(/\n---\s*\n/);
  if (!endMatch || endMatch.index === undefined) {
    return "SKILL.md frontmatter is not closed. Ensure you have a closing '---' line.";
  }

  return { yaml: content.slice(3, endMatch.index + 3), endIndex: endMatch.index, endMatch };
}

/**
 * 解析 YAML frontmatter 中的简单键值对。
 * 同时支持收集列表项（例如 `  - xxx`），挂到最近出现的 key 下。
 *
 * 支持一层嵌套：缩进的子 key（如 `  commands:` 下的 `    - npm`）
 * 会被存储为 `parentKey.childKey` 的复合键（例如 `prerequisites.commands`）。
 */
function parseYamlFields(yamlContent: string): Map<string, string | string[]> {
  const fields = new Map<string, string | string[]>();
  let currentKey: string | undefined;
  /** 当前顶层 key（用于嵌套子 key 的复合键构建）。 */
  let parentKey: string | undefined;

  for (const line of yamlContent.split("\n")) {
    // 缩进的子 key: value（2+ 空格开头，支持一层嵌套）
    const nestedKvMatch = line.match(/^(\s{2,})(\w[\w-]*)\s*:\s*(.*)/);
    if (nestedKvMatch && parentKey) {
      const childKey = nestedKvMatch[2];
      const val = nestedKvMatch[3].trim().replace(/^["']|["']$/g, "");
      const compositeKey = `${parentKey}.${childKey}`;

      const inlineList = val.match(/^\[(.*)\]$/);
      if (inlineList) {
        fields.set(
          compositeKey,
          inlineList[1]
            .split(",")
            .map((s) => s.trim().replace(/^["']|["']$/g, ""))
            .filter(Boolean),
        );
      } else if (val === "" || val === "[]") {
        fields.set(compositeKey, val === "[]" ? [] : "");
      } else {
        fields.set(compositeKey, val);
      }
      currentKey = compositeKey;
      continue;
    }

    // 顶层 key: value
    const kvMatch = line.match(/^(\w[\w-]*)\s*:\s*(.*)/);
    if (kvMatch) {
      const key = kvMatch[1];
      const val = kvMatch[2].trim().replace(/^["']|["']$/g, "");

      // 行内列表：`platforms: [linux, macos]`
      const inlineList = val.match(/^\[(.*)\]$/);
      if (inlineList) {
        fields.set(
          key,
          inlineList[1]
            .split(",")
            .map((s) => s.trim().replace(/^["']|["']$/g, ""))
            .filter(Boolean),
        );
      } else if (val === "" || val === "[]") {
        // 空值：后续可能跟着列表项或嵌套子 key
        fields.set(key, val === "[]" ? [] : "");
      } else {
        fields.set(key, val);
      }
      currentKey = key;
      parentKey = key;
      continue;
    }

    // 当前 key 下的列表项：`  - value`
    const listMatch = line.match(/^\s+-\s+(.*)/);
    if (listMatch && currentKey) {
      const existing = fields.get(currentKey);
      const item = listMatch[1].trim().replace(/^["']|["']$/g, "");
      if (Array.isArray(existing)) {
        existing.push(item);
      } else {
        // 第一个列表项：把单值转成数组
        fields.set(currentKey, [item]);
      }
    }
  }
  return fields;
}

/**
 * 读取 SKILL.md 并提取 frontmatter 中的 `description` 字段
 */
export function readSkillMdDescription(skillDir: string): string {
  const skillMdPath = path.join(skillDir, "SKILL.md");
  let content: string;
  try {
    content = fs.readFileSync(skillMdPath, "utf-8");
  } catch {
    return "";
  }
  const block = extractFrontmatterBlock(content);
  if (typeof block === "string") {
    // 字符串表示解析错误（无 frontmatter / 未闭合等），按 starter 同样降级为空。
    return "";
  }
  const fields = parseYamlFields(block.yaml);
  const desc = fields.get("description");
  if (typeof desc === "string") {
    return desc;
  }
  if (Array.isArray(desc)) {
    return desc.join(", ");
  }
  return "";
}

/**
 * 校验 SKILL.md 是否具备合法的 YAML frontmatter（含必填字段）。
 * 合法返回 undefined，不合法返回错误信息。
 *
 * 这里使用轻量级 frontmatter 解析，不引入完整 YAML 依赖。
 * 会校验结构、必填字段（name/description）及可选扩展字段
 * （platforms/prerequisites/compatibility/version/tags）。
 */
export function validateFrontmatter(content: string): string | undefined {
  const block = extractFrontmatterBlock(content);
  if (typeof block === "string") {
    return block;
  }

  const fields = parseYamlFields(block.yaml);

  // --- 必填字段 ---
  if (!fields.has("name")) {
    return "Frontmatter must include 'name' field.";
  }
  if (!fields.has("description")) {
    return "Frontmatter must include 'description' field.";
  }
  const desc = fields.get("description") ?? "";
  const descStr = typeof desc === "string" ? desc : Array.isArray(desc) ? desc.join(", ") : "";
  if (descStr.length > MAX_DESCRIPTION_LENGTH) {
    return `Description exceeds ${MAX_DESCRIPTION_LENGTH} characters.`;
  }

  // --- 可选字段：platforms 校验 ---
  if (fields.has("platforms")) {
    const platforms = fields.get("platforms");
    if (platforms !== undefined && platforms !== "") {
      const platformList = Array.isArray(platforms) ? platforms : [platforms as string];
      for (const p of platformList) {
        if (!VALID_PLATFORMS.has(p.toLowerCase())) {
          return `Unknown platform '${p}'. Allowed: ${[...VALID_PLATFORMS].sort().join(", ")}`;
        }
      }
    }
  }

  // --- 可选字段：version 格式校验 ---
  if (fields.has("version")) {
    const ver = fields.get("version");
    if (typeof ver === "string" && ver && !/^[\w][\w.\-+]*$/.test(ver)) {
      return `Invalid version format '${ver}'. Use semver-like strings (e.g. '1.0.0', '2024.1').`;
    }
  }

  // frontmatter 后必须有正文内容
  const body = content.slice(block.endIndex + 3 + block.endMatch[0].length).trim();
  if (!body) {
    return "SKILL.md must have content after the frontmatter (instructions, procedures, etc.).";
  }

  return undefined;
}

/**
 * 解析 SKILL.md 并提取结构化 frontmatter。
 *
 * 解析成功返回 `SkillFrontmatter`，失败返回 undefined。
 * 建议先调用 `validateFrontmatter()` 做合法性校验。
 */
export function parseFrontmatter(content: string): SkillFrontmatter | undefined {
  const block = extractFrontmatterBlock(content);
  if (typeof block === "string") {
    return undefined;
  }

  const fields = parseYamlFields(block.yaml);

  const name = fields.get("name");
  const description = fields.get("description");
  if (typeof name !== "string" || typeof description !== "string") {
    return undefined;
  }

  const result: SkillFrontmatter = { name, description };

  // platforms 字段
  const platforms = fields.get("platforms");
  if (platforms !== undefined) {
    result.platforms = Array.isArray(platforms) ? platforms : [platforms as string];
  }

  // prerequisites：支持两种格式：
  //   1. 简单列表：`prerequisites:\n  - npm\n  - node` → commands
  //   2. 嵌套结构：`prerequisites:\n  commands:\n    - npm\n  env_vars:\n    - NODE_ENV`
  //      嵌套子 key 由 parseYamlFields 存储为 `prerequisites.commands` 等复合键。
  const prereqs = fields.get("prerequisites");
  if (prereqs !== undefined) {
    const prereqCommands = fields.get("prerequisites.commands");
    const prereqEnvVars = fields.get("prerequisites.env_vars");

    if (prereqCommands !== undefined || prereqEnvVars !== undefined) {
      // 嵌套结构：从复合键组装
      const assembled: SkillPrerequisites = {};
      if (Array.isArray(prereqCommands)) {
        assembled.commands = prereqCommands;
      }
      if (Array.isArray(prereqEnvVars)) {
        assembled.env_vars = prereqEnvVars;
      }
      result.prerequisites = assembled;
    } else if (Array.isArray(prereqs)) {
      // 简单列表：视为 commands
      result.prerequisites = { commands: prereqs };
    }
  }

  // compatibility 字段
  const compat = fields.get("compatibility");
  if (typeof compat === "string" && compat) {
    result.compatibility = compat;
  }

  // version 字段
  const version = fields.get("version");
  if (typeof version === "string" && version) {
    result.version = version;
  }

  // tags 字段
  const tags = fields.get("tags");
  if (tags !== undefined) {
    result.tags = Array.isArray(tags) ? tags : [tags as string];
  }

  return result;
}

export function normalizeFrontmatterDescription(content: string): string {
  const block = extractFrontmatterBlock(content);
  if (typeof block === "string") {
    return content; // 无合法 frontmatter，交给上层 validate 拦截
  }

  const yaml = block.yaml;
  const lines = yaml.split("\n");

  // 定位顶层 `description:` 行（必须无缩进，避免误伤嵌套字段）。
  let descLineIdx = -1;
  let indicatorMatch: RegExpMatchArray | null = null;
  for (let i = 0; i < lines.length; i += 1) {
    const m = lines[i].match(/^description\s*:\s*([>|])([+-]?)\s*$/);
    if (m) {
      descLineIdx = i;
      indicatorMatch = m;
      break;
    }
  }
  if (descLineIdx < 0 || !indicatorMatch) {
    return content; // 没有块标量形式的 description，无需归一化
  }

  // 收集块标量正文行：从下一行起，缩进 > 0（描述行无缩进，正文必须缩进）或空行；
  // 一旦出现无缩进非空行就跳出（说明 description 区段已结束）。
  const bodyLines: string[] = [];
  let endIdx = descLineIdx + 1;
  while (endIdx < lines.length) {
    const ln = lines[endIdx];
    if (ln.trim().length === 0) {
      bodyLines.push("");
      endIdx += 1;
      continue;
    }
    if (/^\s/.test(ln)) {
      bodyLines.push(ln);
      endIdx += 1;
      continue;
    }
    break;
  }

  // 折叠：所有非空行 trim 后用单空格拼接；空行（段落分隔）也用单空格代替
  const folded = bodyLines
    .map((l) => l.trim())
    .filter((l) => l.length > 0)
    .join(" ")
    .replace(/\s+/g, " ")
    .trim();

  const quoted = `'${folded.replace(/'/g, "''")}'`;

  const rebuilt = [
    ...lines.slice(0, descLineIdx),
    `description: ${quoted}`,
    ...lines.slice(endIdx),
  ].join("\n");

  // 还原到完整 SKILL.md：替换 frontmatter 区段，body 完全不动。
  const closingDelim = block.endMatch[0]; // "\n---\n"
  const body = content.slice(block.endIndex + 3 + closingDelim.length);
  return `---${rebuilt}${closingDelim}${body}`;
}

/**
 * 校验内容字符数是否超过上限。
 */
export function validateContentSize(content: string, label = "SKILL.md"): string | undefined {
  if (content.length > MAX_SKILL_CONTENT_CHARS) {
    return (
      `${label} content is ${content.length.toLocaleString()} characters ` +
      `(limit: ${MAX_SKILL_CONTENT_CHARS.toLocaleString()}). ` +
      "Consider splitting into a smaller SKILL.md with supporting files " +
      "in references/ or templates/."
    );
  }
  return undefined;
}

/**
 * 校验 write_file/remove_file 使用的文件路径。
 * 必须位于允许的子目录下，且不能逃逸技能目录。
 */
export function validateFilePath(filePath: string): string | undefined {
  if (!filePath) {
    return "file_path is required.";
  }

  // 防止路径穿越
  if (hasTraversalComponent(filePath)) {
    return "Path traversal ('..') is not allowed.";
  }

  const normalized = path.normalize(filePath);
  const parts = normalized.split(path.sep).filter(Boolean);

  if (parts.length === 0 || !ALLOWED_SUBDIRS.has(parts[0])) {
    const allowed = [...ALLOWED_SUBDIRS].sort().join(", ");
    return `File must be under one of: ${allowed}. Got: '${filePath}'`;
  }

  if (parts.length < 2) {
    return `Provide a file path, not just a directory. Example: '${parts[0]}/myfile.md'`;
  }

  return undefined;
}

/**
 * 按字节校验文件内容大小。
 */
export function validateFileSize(content: string): string | undefined {
  const contentBytes = Buffer.byteLength(content, "utf-8");
  if (contentBytes > MAX_SKILL_FILE_BYTES) {
    return (
      `File content is ${contentBytes.toLocaleString()} bytes ` +
      `(limit: ${MAX_SKILL_FILE_BYTES.toLocaleString()} bytes / 1 MiB). ` +
      "Consider splitting into smaller files."
    );
  }
  return undefined;
}

// ---------------------------------------------------------------------------
// 路径安全
// ---------------------------------------------------------------------------

/**
 * 检查路径中是否包含路径穿越片段（如 ..）。
 */
export function hasTraversalComponent(filePath: string): boolean {
  const normalized = path.normalize(filePath);
  const parts = normalized.split(path.sep);
  return parts.some((p) => p === "..");
}

/**
 * 校验解析后的路径是否仍位于给定基目录内。
 * 安全返回 undefined，不安全返回错误信息。
 */
export function validateWithinDir(target: string, baseDir: string): string | undefined {
  const resolvedTarget = path.resolve(target);
  const resolvedBase = path.resolve(baseDir);

  if (!resolvedTarget.startsWith(resolvedBase + path.sep) && resolvedTarget !== resolvedBase) {
    return `Path escapes the skill directory: ${target}`;
  }
  return undefined;
}

/**
 * 判断技能目录是否为官方内置技能（__skill_meta__.json 中 source === "OFFICIAL"）。
 * 官方技能只能查询，不能修改或删除。
 */
export function isOfficialSkill(skillDir: string): boolean {
  const meta = readSkillMeta(skillDir);
  return meta?.source === "OFFICIAL";
}

/**
 * 判断技能是否"源自沉淀"。
 *
 * 适用场景：技能已被 starter 的 enable_seal_skill 接口从
 * `<workspace>/sediment_skills/` 迁移到 `<workspace>/skills/`，
 * 此时 source 已被改写为 "PERSONAL"，但 originSource 仍保留为 "SEDIMENT"。
 *
 * 本插件以此字段为权威依据，授权 skill_manage 工具继续修改这类技能。
 */
export function isSedimentOrigin(skillDir: string): boolean {
  const meta = readSkillMeta(skillDir);
  return meta?.originSource === "SEDIMENT";
}

/**
 * 判断技能路径是否位于托管技能目录内。
 */
export function isLocalSkill(skillPath: string, skillsDir: string): boolean {
  try {
    const resolved = path.resolve(skillPath);
    const resolvedBase = path.resolve(skillsDir);
    return resolved.startsWith(resolvedBase + path.sep) || resolved === resolvedBase;
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// 原子文件操作
// ---------------------------------------------------------------------------

/**
 * 以原子方式写入文本文件。
 *
 * 通过“同目录临时文件 + fs.renameSync()”确保目标文件不会处于半写入状态。
 */
export function atomicWriteText(filePath: string, content: string): void {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });

  const tmpName = `.${path.basename(filePath)}.tmp.${crypto.randomBytes(4).toString("hex")}`;
  const tmpPath = path.join(dir, tmpName);

  try {
    fs.writeFileSync(tmpPath, content, "utf-8");
    fs.renameSync(tmpPath, filePath);
  } catch (err) {
    // 写入失败时清理临时文件
    try {
      fs.unlinkSync(tmpPath);
    } catch {
      // 忽略临时文件清理错误
    }
    throw err;
  }
}

// ---------------------------------------------------------------------------
// 技能元数据
//
// 文件分工（重要）：
//  - __skill_meta__.json   ：starter 写入并透传给外部接口（前端/平台 API）。
//                            本插件只允许"接力刷新" installedAt，不再注入修改细节。
//  - __sediment_meta__.json：本插件私有的修改细节（修改历史、修订次数、最近动作等）。
//                            starter 不感知、不读、不透传，避免无用信息扩散和敏感
//                            修改预览泄露。
//
// 历史数据迁移：旧版本曾把修改细节写在 __skill_meta__.json 里。
// readSedimentMeta 在新文件不存在时，会从老文件中"萃取"这些字段写到新文件，
// 并把它们从老文件中清除，确保升级后第一次读写就完成迁移。
// ---------------------------------------------------------------------------

/** starter 与本插件共享的对外元数据文件名。 */
export const SKILL_META_FILENAME = "__skill_meta__.json";

/** 本插件私有的修改细节文件名（不会被 starter 透传）。 */
export const SEDIMENT_META_FILENAME = "__sediment_meta__.json";

/** 老版本曾写在 __skill_meta__.json 中的本插件私有字段，用于一次性迁移与剥离。 */
const LEGACY_SEDIMENT_FIELDS = [
  "createdAt",
  "updatedAt",
  "lastAction",
  "revisionCount",
  "editHistory",
] as const;

/**
 * 在技能目录下写入对外元数据文件（`__skill_meta__.json`）。
 */
export function writeSkillMeta(skillDir: string, meta: SkillMeta): void {
  const metaPath = path.join(skillDir, SKILL_META_FILENAME);
  atomicWriteText(metaPath, JSON.stringify(meta, null, 2) + "\n");
}

/**
 * 从技能目录读取对外元数据文件。若不存在则返回 undefined。
 */
export function readSkillMeta(skillDir: string): SkillMeta | undefined {
  const metaPath = path.join(skillDir, SKILL_META_FILENAME);
  try {
    const content = fs.readFileSync(metaPath, "utf-8");
    return JSON.parse(content) as SkillMeta;
  } catch {
    return undefined;
  }
}

/**
 * 写入本插件私有的修改细节文件（`__sediment_meta__.json`）。
 *
 * 该文件不会被 starter 透传给外部接口；只承载创建时间、修订次数、修改历史、
 * 最近动作等本插件内部信息。
 */
export function writeSedimentMeta(skillDir: string, meta: SedimentMeta): void {
  const metaPath = path.join(skillDir, SEDIMENT_META_FILENAME);
  atomicWriteText(metaPath, JSON.stringify(meta, null, 2) + "\n");
}

/**
 * 读取本插件私有的修改细节文件。
 *
 * 若文件不存在但旧版 `__skill_meta__.json` 中残留私有字段（createdAt /
 * updatedAt / lastAction / revisionCount / editHistory），会执行一次迁移：
 *   1. 把残留字段拷贝到新文件 `__sediment_meta__.json`；
 *   2. 从 `__skill_meta__.json` 中删除这些字段，只保留 starter 关心的对外字段。
 *
 * 迁移失败（如磁盘错误）会静默退化为返回从老文件提取的内存对象，确保读路径
 * 永远不会因为迁移失败而崩溃；下次写入时 updateMeta 会再次尝试写入新文件。
 */
export function readSedimentMeta(skillDir: string): SedimentMeta | undefined {
  const metaPath = path.join(skillDir, SEDIMENT_META_FILENAME);
  try {
    const content = fs.readFileSync(metaPath, "utf-8");
    return JSON.parse(content) as SedimentMeta;
  } catch {
    // 新文件不存在，尝试从老文件迁移
  }

  const legacy = readSkillMeta(skillDir);
  if (!legacy) {
    return undefined;
  }

  // 从老文件中提取本插件私有字段
  const extracted: Partial<SedimentMeta> = {};
  let hasAny = false;
  for (const field of LEGACY_SEDIMENT_FIELDS) {
    const value = (legacy as Record<string, unknown>)[field];
    if (value !== undefined) {
      (extracted as Record<string, unknown>)[field] = value;
      hasAny = true;
    }
  }
  if (!hasAny) {
    return undefined;
  }

  // 兜底必填字段（极旧的 meta 可能两个时间字段都缺）
  const now = new Date().toISOString();
  const migrated: SedimentMeta = {
    createdAt: typeof extracted.createdAt === "string" ? extracted.createdAt : now,
    updatedAt: typeof extracted.updatedAt === "string" ? extracted.updatedAt : now,
    lastAction: extracted.lastAction,
    revisionCount: extracted.revisionCount,
    editHistory: extracted.editHistory,
  };

  // 落盘迁移：写新文件 + 从老文件剥离私有字段
  try {
    writeSedimentMeta(skillDir, migrated);
    const stripped: Record<string, unknown> = { ...legacy };
    for (const field of LEGACY_SEDIMENT_FIELDS) {
      delete stripped[field];
    }
    writeSkillMeta(skillDir, stripped as SkillMeta);
  } catch {
    // 迁移失败仍返回内存对象，避免读路径崩溃；下次写入时会再次尝试。
  }

  return migrated;
}

// ---------------------------------------------------------------------------
// 技能目录操作
// ---------------------------------------------------------------------------

/**
 * 在指定基目录中按名称递归查找技能。
 *
 * 递归搜索父目录名匹配且包含 SKILL.md 的目录。
 * - 写动作（create/edit/patch/...）传入 sedimentDir，确保只能命中沉淀技能。
 * - 只读动作（list/view）可传入 skillsDir 以扫描全部（含原生）技能。
 *
 * @returns 命中的技能目录绝对路径；找不到返回 undefined。
 */
export function findSkill(name: string, baseDir: string): string | undefined {
  if (!fs.existsSync(baseDir)) {
    return undefined;
  }

  // 递归搜索包含 SKILL.md 的目录
  function search(dir: string): string | undefined {
    let entries: fs.Dirent[];
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return undefined;
    }

    for (const entry of entries) {
      if (entry.name.startsWith(".")) {
        continue;
      }
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        if (entry.name === name) {
          // 检查该目录是否包含 SKILL.md
          const skillMd = path.join(fullPath, "SKILL.md");
          if (fs.existsSync(skillMd)) {
            return fullPath;
          }
        }
        // 继续递归，兼容 category/skill 结构
        const found = search(fullPath);
        if (found) {
          return found;
        }
      }
    }
    return undefined;
  }

  return search(baseDir);
}

/**
 * 列出技能目录下允许子目录中的可用文件。
 */
export function listSkillFiles(skillDir: string): string[] {
  const available: string[] = [];
  for (const subdir of ALLOWED_SUBDIRS) {
    const subdirPath = path.join(skillDir, subdir);
    if (!fs.existsSync(subdirPath)) {
      continue;
    }
    const walk = (dir: string): void => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const full = path.join(dir, entry.name);
        if (entry.isFile()) {
          available.push(path.relative(skillDir, full));
        } else if (entry.isDirectory()) {
          walk(full);
        }
      }
    };
    walk(subdirPath);
  }
  return available;
}

// ---------------------------------------------------------------------------
// 去重检测
// ---------------------------------------------------------------------------

/**
 * 将技能名拆分为语义词组（按分隔符拆分，转小写）。
 *
 * 示例：
 *   "deploy-k8s-workflow" → ["deploy", "k8s", "workflow"]
 *   "k8s.deploy"          → ["k8s", "deploy"]
 */
export function nameToWords(name: string): Set<string> {
  // 按连字符、下划线、点分割
  const parts = name.split(/[-._]+/).filter((s) => s.length > 0);
  return new Set(parts.map((s) => s.toLowerCase()));
}

/**
 * 计算两组词的 Jaccard 相似系数（交集/并集）。
 * 返回 [0, 1]，1 表示完全相同。
 */
export function wordOverlap(a: Set<string>, b: Set<string>): number {
  // 任一词集为空时视为不可比较，返回 0（防止空集 vs 空集误报 100%）
  if (a.size === 0 || b.size === 0) {
    return 0;
  }
  let intersection = 0;
  for (const w of a) {
    if (b.has(w)) {
      intersection++;
    }
  }
  const union = a.size + b.size - intersection;
  return union === 0 ? 0 : intersection / union;
}

/**
 * 描述相似度比较时忽略的高频停用词。
 * 这些词在技能描述中极其常见，不携带区分语义。
 */
const DESC_STOP_WORDS = new Set([
  "the",
  "and",
  "for",
  "with",
  "that",
  "this",
  "from",
  "into",
  "using",
  "used",
  "use",
  "data",
  "tool",
  "tools",
  "based",
  "will",
  "can",
  "are",
  "has",
  "have",
  "been",
  "when",
  "which",
  "also",
  "not",
  "but",
  "all",
  "more",
  "other",
  "each",
  "any",
  "how",
  "about",
  "such",
  "than",
  "then",
  "its",
  "over",
  "between",
  "after",
  "before",
  "through",
]);

/** 从描述文本提取有效词集（去除短词和停用词）。 */
function extractDescriptionWords(text: string): Set<string> {
  const words = text
    .toLowerCase()
    .split(/\W+/)
    .filter((w) => w.length > 2 && !DESC_STOP_WORDS.has(w));
  return new Set(words);
}

/** 描述词集的最低有效词数——词太少时不做相似度比较（避免小词集巧合重叠）。 */
const MIN_DESC_WORDS = 3;

/**
 * 文本相似度：基于词袋的 Jaccard 系数（去除停用词）。
 * 当任一描述的有效词数不足 MIN_DESC_WORDS 时返回 0，避免小样本误判。
 */
export function descriptionSimilarity(a: string, b: string): number {
  const wordsA = extractDescriptionWords(a);
  const wordsB = extractDescriptionWords(b);
  // 有效词过少时不做比较，避免小词集巧合重叠导致高相似度
  if (wordsA.size < MIN_DESC_WORDS || wordsB.size < MIN_DESC_WORDS) {
    return 0;
  }
  return wordOverlap(wordsA, wordsB);
}

/** 去重检查发现的相似技能。 */
export interface SimilarSkill {
  name: string;
  path: string;
  descSimilarity: number;
}

/**
 * 扫描已有技能，返回与新技能描述高度相似的候选列表。
 *
 * 判定阈值：描述词袋重叠（Jaccard）≥ 0.7 → 视为潜在重复。
 * 不比较名称相似度——技能名称往往很短且词汇高度重叠（如都含 "config"、
 * "setup" 等通用词），基于名称的去重误判率极高。
 *
 * @param _newName 新技能名（保留参数以保持调用兼容，不再用于比较）
 * @param newDescription 新技能的 description 字段
 * @param skillsDir 托管技能目录
 * @returns 相似技能列表（可能为空）
 */
export function findSimilarSkills(
  _newName: string,
  newDescription: string,
  skillsDir: string,
): SimilarSkill[] {
  if (!fs.existsSync(skillsDir)) {
    return [];
  }

  // 没有描述则无法比较，直接放行
  if (!newDescription) {
    return [];
  }

  const DESC_THRESHOLD = 0.7;
  const similar: SimilarSkill[] = [];

  function scan(dir: string): void {
    let entries: fs.Dirent[];
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }

    for (const entry of entries) {
      // 跳过点开头条目，以及 starter 透传文件 / 本插件私有文件
      if (
        entry.name.startsWith(".") ||
        entry.name === SKILL_META_FILENAME ||
        entry.name === SEDIMENT_META_FILENAME
      ) {
        continue;
      }
      const fullPath = path.join(dir, entry.name);
      if (!entry.isDirectory()) {
        continue;
      }

      const skillMd = path.join(fullPath, "SKILL.md");
      if (fs.existsSync(skillMd)) {
        // 仅比较描述相似度（需要解析 frontmatter）
        let descSim = 0;
        try {
          const content = fs.readFileSync(skillMd, "utf-8");
          const fm = parseFrontmatter(content);
          if (fm?.description) {
            descSim = descriptionSimilarity(newDescription, fm.description);
          }
        } catch {
          // 解析失败，跳过
        }

        if (descSim >= DESC_THRESHOLD) {
          similar.push({
            name: entry.name,
            path: path.relative(skillsDir, fullPath),
            descSimilarity: descSim,
          });
        }
      } else {
        // 可能是 category 目录，继续递归
        scan(fullPath);
      }
    }
  }

  scan(skillsDir);
  return similar;
}

// ---------------------------------------------------------------------------
// 历史数据迁移
//
// 四阶段迁移（按执行顺序）：
//   Phase 0 — migrateLegacySedimentDirName()
//     把整体目录 <workspace>/sediment-skills/（连字符旧名）迁移到
//     <workspace>/sediment_skills/（下划线新名 = SEDIMENT_DIR_NAME）。
//     必须最先执行，确保后续 Phase 1-3 的目标目录已就位。
//
//   Phase 1 — migrateLegacySedimentSkills()
//     把散落在 <skills>/ 根目录下的 sediment-* 技能移入 <workspace>/sediment_skills/，
//     同时剥掉 "sediment-" 前缀（目录名 + SKILL.md frontmatter name）。
//
//   Phase 2 — migrateSedimentSubdirSkills()
//     把 <skills>/sediment/ 子目录下的技能移入 <workspace>/sediment_skills/，
//     如目录名仍以 "sediment-" 开头则剥掉前缀。
//
//   Phase 3 — renameSedimentPrefixSkills()
//     对已在 <workspace>/sediment_skills/ 下但目录名仍以 "sediment-" 开头的技能，
//     原地重命名去掉前缀，并同步 SKILL.md frontmatter name。
// ---------------------------------------------------------------------------

/**
 * 旧的沉淀技能目录名（连字符形式）。仅用于 Phase 0 一次性迁移识别历史数据；
 * 当前所有写动作都使用 {@link SEDIMENT_DIR_NAME}（下划线形式）。
 */
const LEGACY_SEDIMENT_DIR_NAME_HYPHEN = "sediment-skills";

/** 一次迁移结果摘要（仅供日志使用）。 */
export interface SedimentMigrationResult {
  /** 实际移动/重命名的技能（旧名 → 新名）。 */
  moved: string[];
  /** 因目标已存在而跳过的技能名列表（保留在原位）。 */
  conflicts: string[];
  /** 迁移过程中遇到的错误（按目录名）。 */
  errors: Array<{ name: string; error: string }>;
}

/**
 * 从 `sediment-xxx` 形式的名字中剥掉 `sediment-` 前缀。
 * 若剥掉后为空（理论上不会），返回原名。
 */
function stripSedimentPrefix(name: string): string {
  const stripped = name.replace(/^sediment-/, "");
  return stripped || name;
}

/**
 * 更新 SKILL.md 中 frontmatter 的 `name` 字段：
 * 如果当前 name 以 `sediment-` 开头，则剥掉前缀。
 *
 * 仅在 frontmatter 区块内替换，不影响正文。
 * 若文件不存在或解析失败则静默跳过。
 */
function stripSedimentPrefixInSkillMd(skillMdPath: string): void {
  let content: string;
  try {
    content = fs.readFileSync(skillMdPath, "utf-8");
  } catch {
    return;
  }

  const fm = parseFrontmatter(content);
  if (!fm || !fm.name.startsWith("sediment-")) {
    return;
  }

  const newName = stripSedimentPrefix(fm.name);
  // 仅在 frontmatter 区块内替换 name 行
  const closingMatch = content.slice(3).match(/\n---\s*\n/);
  if (!closingMatch || closingMatch.index === undefined) {
    return;
  }
  const fmEndOffset = 3 + closingMatch.index;
  const fmSection = content.slice(0, fmEndOffset);
  const rest = content.slice(fmEndOffset);
  const updatedFm = fmSection.replace(/^name\s*:.*$/m, `name: ${newName}`);
  atomicWriteText(skillMdPath, updatedFm + rest);
}

/**
 * 解析沉淀技能目标目录：`<agent workspace>/sediment_skills`。
 *
 * 供迁移函数使用，从 skillsDir 推导出同级的 sediment_skills 目录。
 */
function resolveSedimentTargetDir(skillsDir: string): string {
  // skillsDir = <workspace>/skills → sedimentTarget = <workspace>/sediment_skills
  return path.join(path.dirname(skillsDir), SEDIMENT_DIR_NAME);
}

/**
 * Phase 0：把整体目录从 `<workspace>/sediment-skills/`（连字符旧名）
 * 迁移到 `<workspace>/sediment_skills/`（下划线新名 = {@link SEDIMENT_DIR_NAME}）。
 *
 * 历史背景：早期版本使用连字符目录名 `sediment-skills`，后续统一为
 * 下划线 `sediment_skills`。本阶段一次性搬运历史用户的旧目录数据。
 *
 * 必须在 Phase 1-3 之前执行：因为 Phase 1/2 写入 / Phase 3 重命名都依赖
 * 新目录 `sediment_skills/` 存在，否则旧数据可能与新数据并存形成两套副本。
 *
 * 设计要点：
 * - 仅当旧目录 `<workspace>/sediment-skills/` 存在且为目录时才介入。
 * - 逐个技能子目录（含 SKILL.md）搬运到 `<workspace>/sediment_skills/<name>`。
 * - 目标已存在则跳过（保留旧位置不动），避免误覆盖新数据。
 * - 非技能目录（不含 SKILL.md）原样跳过，保持旧目录不被破坏性删除。
 * - 全部子项搬运后旧目录若变为空，主动 rmdir；否则保留旧目录原状。
 * - 函数幂等：旧目录不存在时直接返回。
 *
 * 注意：本函数不剥任何 "sediment-" 前缀（那是 Phase 1/2/3 的职责），
 * 仅做"目录名 hyphen→underscore"这一种迁移；技能内部的目录名 / SKILL.md
 * 名字均原样保留，由后续阶段统一处理。
 *
 * @param skillsDir agent 的 skills 根目录（用于推导 workspace 根 → 旧/新目录路径）
 * @returns 迁移摘要（用于日志输出）
 */
export function migrateLegacySedimentDirName(skillsDir: string): SedimentMigrationResult {
  const result: SedimentMigrationResult = { moved: [], conflicts: [], errors: [] };

  // workspace 根目录 = skillsDir 的父目录
  const workspaceDir = path.dirname(skillsDir);
  const oldDir = path.join(workspaceDir, LEGACY_SEDIMENT_DIR_NAME_HYPHEN);
  const newDir = path.join(workspaceDir, SEDIMENT_DIR_NAME);

  // 防御：旧名 === 新名时（理论上不可能）直接退出，避免自我搬运
  if (oldDir === newDir) {
    return result;
  }

  if (!fs.existsSync(oldDir)) {
    return result;
  }

  // 必须是目录；如果是普通文件（被用户错放）不动它，避免误删
  let oldStat: fs.Stats;
  try {
    oldStat = fs.statSync(oldDir);
  } catch (err) {
    result.errors.push({ name: LEGACY_SEDIMENT_DIR_NAME_HYPHEN, error: String(err) });
    return result;
  }
  if (!oldStat.isDirectory()) {
    return result;
  }

  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(oldDir, { withFileTypes: true });
  } catch (err) {
    result.errors.push({ name: "(readdir)", error: String(err) });
    return result;
  }

  for (const entry of entries) {
    if (!entry.isDirectory()) {
      // 非目录项（隐藏文件、临时文件等）原样跳过
      continue;
    }
    const sourceDir = path.join(oldDir, entry.name);
    // 仅迁移真正的技能目录（包含 SKILL.md）；其他子目录跳过
    if (!fs.existsSync(path.join(sourceDir, "SKILL.md"))) {
      continue;
    }

    const targetDir = path.join(newDir, entry.name);
    if (fs.existsSync(targetDir)) {
      result.conflicts.push(entry.name);
      continue;
    }

    try {
      fs.mkdirSync(newDir, { recursive: true });
      fs.renameSync(sourceDir, targetDir);
      result.moved.push(`sediment-skills/${entry.name} → ${SEDIMENT_DIR_NAME}/${entry.name}`);
    } catch (err) {
      result.errors.push({ name: entry.name, error: String(err) });
    }
  }

  // 全部技能搬运后，旧目录若已空则尝试 rmdir 清理；非空（含 conflicts/非技能项）保留原状
  try {
    const remaining = fs.readdirSync(oldDir);
    if (remaining.length === 0) {
      fs.rmdirSync(oldDir);
    }
  } catch {
    // 清理失败不影响迁移结果，静默忽略（下次启动可重试）
  }

  return result;
}

/**
 * Phase 1：把 `<skillsDir>/sediment-*` 形态的旧版沉淀技能迁移到
 * `<workspace>/sediment_skills/<stripped-name>`，同时剥掉 "sediment-" 前缀。
 *
 * 示例：`<skills>/sediment-deploy-k8s/` → `<workspace>/sediment_skills/deploy-k8s/`
 *       SKILL.md 中 `name: sediment-deploy-k8s` → `name: deploy-k8s`
 *
 * 设计要点：
 * - 仅针对名字以 `sediment-` 开头且目录内确实包含 SKILL.md 的子目录。
 * - 使用 `fs.renameSync` 做原子级别的移动。
 * - 目标已存在则跳过（保留原位置），避免误覆盖。
 * - 函数幂等：旧目录不存在或已无 sediment-* 子目录时不做任何事。
 *
 * @param skillsDir agent 的 skills 根目录
 * @returns 迁移摘要（用于日志输出）
 */
export function migrateLegacySedimentSkills(skillsDir: string): SedimentMigrationResult {
  const result: SedimentMigrationResult = { moved: [], conflicts: [], errors: [] };

  if (!fs.existsSync(skillsDir)) {
    return result;
  }

  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  } catch (err) {
    result.errors.push({ name: "(readdir)", error: String(err) });
    return result;
  }

  const sedimentTarget = resolveSedimentTargetDir(skillsDir);

  for (const entry of entries) {
    if (!entry.isDirectory()) {
      continue;
    }
    if (!entry.name.startsWith("sediment-")) {
      continue;
    }
    // 防御：避免把已知的目录根名当成单个技能误迁移：
    // - "sediment"           → Phase 2 处理的旧子目录布局根
    // - SEDIMENT_DIR_NAME    → 当前下划线根目录名 (sediment_skills)
    // - LEGACY_SEDIMENT_DIR_NAME_HYPHEN → Phase 0 处理的连字符旧根 (sediment-skills)
    //   仅在用户曾把旧根错放到 skills/ 下时才触发；正常情况下旧根在 workspace/。
    if (
      entry.name === "sediment" ||
      entry.name === SEDIMENT_DIR_NAME ||
      entry.name === LEGACY_SEDIMENT_DIR_NAME_HYPHEN
    ) {
      continue;
    }
    const sourceDir = path.join(skillsDir, entry.name);
    // 仅迁移真正的技能目录（包含 SKILL.md）
    if (!fs.existsSync(path.join(sourceDir, "SKILL.md"))) {
      continue;
    }

    const newName = stripSedimentPrefix(entry.name);
    const targetDir = path.join(sedimentTarget, newName);
    if (fs.existsSync(targetDir)) {
      result.conflicts.push(entry.name);
      continue;
    }

    try {
      fs.mkdirSync(sedimentTarget, { recursive: true });
      fs.renameSync(sourceDir, targetDir);
      // 同步 SKILL.md 中的 name 字段
      stripSedimentPrefixInSkillMd(path.join(targetDir, "SKILL.md"));
      result.moved.push(`${entry.name} → ${newName}`);
    } catch (err) {
      result.errors.push({ name: entry.name, error: String(err) });
    }
  }

  return result;
}

/**
 * Phase 2：把 `<skillsDir>/sediment/` 下的旧版沉淀技能迁移到
 * `<workspace>/sediment_skills/`。
 *
 * 这是处理从 `skills/sediment/` 子目录布局迁移到 `sediment_skills/` 同级目录布局。
 * 如果目录名仍以 `sediment-` 开头，则同时剥掉前缀。
 *
 * 示例：`<skills>/sediment/deploy-k8s/` → `<workspace>/sediment_skills/deploy-k8s/`
 *       `<skills>/sediment/sediment-deploy-k8s/` → `<workspace>/sediment_skills/deploy-k8s/`
 *
 * 设计要点：
 * - 仅处理 sediment/ 子目录下的一级子目录（包含 SKILL.md）。
 * - 目标已存在则跳过。
 * - 函数幂等。
 * - 迁移完成后如果 sediment/ 目录为空，不主动删除（避免意外）。
 *
 * @param skillsDir agent 的 skills 根目录
 * @returns 迁移摘要（用于日志输出）
 */
export function migrateSedimentSubdirSkills(skillsDir: string): SedimentMigrationResult {
  const result: SedimentMigrationResult = { moved: [], conflicts: [], errors: [] };

  const oldSedimentRoot = path.join(skillsDir, "sediment");
  if (!fs.existsSync(oldSedimentRoot)) {
    return result;
  }

  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(oldSedimentRoot, { withFileTypes: true });
  } catch (err) {
    result.errors.push({ name: "(readdir)", error: String(err) });
    return result;
  }

  const sedimentTarget = resolveSedimentTargetDir(skillsDir);

  for (const entry of entries) {
    if (!entry.isDirectory()) {
      continue;
    }
    const sourceDir = path.join(oldSedimentRoot, entry.name);
    // 仅迁移真正的技能目录（包含 SKILL.md）
    if (!fs.existsSync(path.join(sourceDir, "SKILL.md"))) {
      continue;
    }

    // 如果目录名仍以 sediment- 开头，剥掉前缀
    const newName = entry.name.startsWith("sediment-")
      ? stripSedimentPrefix(entry.name)
      : entry.name;
    const targetDir = path.join(sedimentTarget, newName);
    if (fs.existsSync(targetDir)) {
      result.conflicts.push(entry.name);
      continue;
    }

    try {
      fs.mkdirSync(sedimentTarget, { recursive: true });
      fs.renameSync(sourceDir, targetDir);
      // 如果剥了前缀，同步 SKILL.md 中的 name 字段
      if (newName !== entry.name) {
        stripSedimentPrefixInSkillMd(path.join(targetDir, "SKILL.md"));
      }
      result.moved.push(`sediment/${entry.name} → ${newName}`);
    } catch (err) {
      result.errors.push({ name: entry.name, error: String(err) });
    }
  }

  return result;
}

/**
 * Phase 3：对已在 `<workspace>/sediment_skills/` 下但目录名仍以 `sediment-` 开头的技能，
 * 原地重命名去掉前缀，并同步 SKILL.md frontmatter name。
 *
 * 示例：`<workspace>/sediment_skills/sediment-deploy-k8s/` → `<workspace>/sediment_skills/deploy-k8s/`
 *       SKILL.md 中 `name: sediment-deploy-k8s` → `name: deploy-k8s`
 *
 * 设计要点：
 * - 仅处理 sedimentDir 下的一级子目录。
 * - 目标已存在则跳过。
 * - 函数幂等。
 *
 * @param sedimentDir 沉淀技能目录（<workspace>/sediment_skills/）
 * @returns 迁移摘要（用于日志输出）
 */
export function renameSedimentPrefixSkills(sedimentDir: string): SedimentMigrationResult {
  const result: SedimentMigrationResult = { moved: [], conflicts: [], errors: [] };

  if (!fs.existsSync(sedimentDir)) {
    return result;
  }

  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(sedimentDir, { withFileTypes: true });
  } catch (err) {
    result.errors.push({ name: "(readdir)", error: String(err) });
    return result;
  }

  for (const entry of entries) {
    if (!entry.isDirectory()) {
      continue;
    }
    if (!entry.name.startsWith("sediment-")) {
      continue;
    }
    const sourceDir = path.join(sedimentDir, entry.name);
    // 仅处理真正的技能目录
    if (!fs.existsSync(path.join(sourceDir, "SKILL.md"))) {
      continue;
    }

    const newName = stripSedimentPrefix(entry.name);
    const targetDir = path.join(sedimentDir, newName);
    if (fs.existsSync(targetDir)) {
      result.conflicts.push(entry.name);
      continue;
    }

    try {
      fs.renameSync(sourceDir, targetDir);
      stripSedimentPrefixInSkillMd(path.join(targetDir, "SKILL.md"));
      result.moved.push(`${entry.name} → ${newName}`);
    } catch (err) {
      result.errors.push({ name: entry.name, error: String(err) });
    }
  }

  return result;
}

// ---------------------------------------------------------------------------
// 沉淀技能升级（promote）
export interface PromoteSedimentOptions {
  /** 升级触发方：review subagent 自动 vs 用户手动（保留 user 以便未来兼容）。 */
  by: "auto" | "user";
  /**
   * review subagent 引用的"二次召回证据"。
   */
  reason?: string;
  agentId?: string;
  /**
   * 关键失败回调：当物理迁移进入"无法自洽回滚"的双残留分支时调用，
   * 让上层用 `logger.error` 或 metric 抓住，避免脏状态被静默吞掉。
   */
  onCriticalError?: (msg: string) => void;
}

/** promote 成功后的返回信息。 */
export interface PromoteSedimentResult {
  /** 升级前的绝对路径（sediment_skills/<name>）。 */
  from: string;
  /** 升级后的绝对路径（skills/<name>）。 */
  to: string;
  /** 升级时间戳（ISO 8601），与写入 meta 的值一致。 */
  promotedAt: string;
}

/**
 * 把一条沉淀技能从 sediment_skills/ 物理迁移到 skills/，并以"严格对齐
 * starter `SkillMetaFile` 契约"的方式重写 `__skill_meta__.json`；升级证据
 * 等插件扩展字段全部进 `__sediment_meta__.json`。
 */
export function promoteSedimentSkill(
  sedimentDir: string,
  skillsDir: string,
  name: string,
  opts: PromoteSedimentOptions,
): PromoteSedimentResult {
  const from = path.join(sedimentDir, name);
  const to = path.join(skillsDir, name);

  // 源目录必须存在且包含 SKILL.md（基本完整性校验；业务守卫由调用方完成）
  if (!fs.existsSync(path.join(from, "SKILL.md"))) {
    throw new Error(`Sediment skill not found or missing SKILL.md: ${name}`);
  }
  // 目标不允许已存在——避免覆盖原生/官方/已启用技能。
  if (fs.existsSync(to)) {
    throw new Error(`Target skill already exists in skills/: ${name}`);
  }

  // 物理移动：优先走 rename（同分区下是原子操作，没有"cp 成功但 rm 失败"导致
  // 沉淀和正式两边同时存在的中间态）；仅当跨设备 EXDEV 时降级到 cp+rm，
  // 且 rm 失败时反向回滚刚刚 cp 出去的 target，避免 sediment_skills/ 与
  // skills/ 同时存在同名目录污染后续 list + 触发 starter loader 歧义。
  fs.mkdirSync(skillsDir, { recursive: true });
  try {
    fs.renameSync(from, to);
  } catch (renameErr) {
    const code = (renameErr as NodeJS.ErrnoException).code;
    if (code !== "EXDEV") {
      throw renameErr;
    }
    // 跨设备/挂载点：降级到 cp + rm 的两阶段原子语义模拟。
    fs.cpSync(from, to, { recursive: true, force: true });
    try {
      fs.rmSync(from, { recursive: true, force: true });
    } catch (rmErr) {
      // 关键回滚：cp 已成功但 rm 失败，必须把 target 删掉恢复"只有 from 存在"的
      // 初始状态——否则同一技能名会同时出现在 sediment_skills/ 和 skills/ 下，
      // 触发 starter loader 重复加载 + 后续 promote 因 "Target skill already
      // exists" 永远失败。
      // 先告警（已进入回滚分支）：此时状态可能短暂双残留，需要监控关注。
      opts.onCriticalError?.(
        `SEDIMENT_PROMOTE_CRITICAL: cp succeeded but rmSync(from) failed; entering rollback ` +
          `(name="${name}", from="${from}", to="${to}", rmErr=${String(rmErr)})`,
      );
      let rollbackErr: unknown;
      try {
        fs.rmSync(to, { recursive: true, force: true });
      } catch (rbErr) {
        rollbackErr = rbErr;
      }
      if (rollbackErr !== undefined) {
        // 最严重场景：from 残留 + to 也残留，必须人工介入。
        // 用 MANUAL_INTERVENTION_REQUIRED 前缀让监控/日志告警容易识别。
        opts.onCriticalError?.(
          `SEDIMENT_PROMOTE_DOUBLE_RESIDUE MANUAL_INTERVENTION_REQUIRED: ` +
            `both sediment_skills/${name} and skills/${name} may remain on disk ` +
            `(from="${from}", to="${to}", rmErr=${String(rmErr)}, rollbackErr=${String(rollbackErr)}). ` +
            `Operator must delete one of the two directories to recover.`,
        );
      }
      throw new Error(`promote rollback: cp succeeded but rm failed for ${from}: ${String(rmErr)}`);
    }
  }

  const now = new Date().toISOString();

  // 1) 刷新对外 __skill_meta__.json：**严格对齐** starter `SkillMetaFile` 契约。
  const newMeta: SkillMeta = {
    // starter SkillMetaFile 必填字段
    id: null,
    code: name,
    name: name,
    enname: name,
    version: "",
    type: "PRIVATE",
    source: "PERSONAL",
    installedAt: now,
    // starter SkillMetaFile 可选字段
    originSource: "SEDIMENT",
    desc: readSkillMdDescription(to),
    agentId: opts.agentId ?? "",
    url: "",
    packagePath: "",
    extraInfo: null,
  };
  writeSkillMeta(to, newMeta);

  // 2) 刷新本插件私有的 __sediment_meta__.json：保留历史，标注 promote 这次动作
  const sedimentMeta = readSedimentMeta(to) || { createdAt: now, updatedAt: now };
  // 显式标注类型，避免对象字面量把 action 推断成宽 `string`，
  // 导致与 `SkillEditRecord[]` 拼接时类型不兼容（与 updateMeta 处的写法一致）。
  const promoteRecord: SkillEditRecord = {
    action: "promote",
    at: now,
    summary: opts.reason
      ? `promote(by=${opts.by}): ${opts.reason.slice(0, 200)}`
      : `promote(by=${opts.by})`,
  };
  const updatedSediment: SedimentMeta = {
    ...sedimentMeta,
    updatedAt: now,
    lastAction: "promote",
    revisionCount: (sedimentMeta.revisionCount ?? 0) + 1,
    promotedAt: now,
    promotedBy: opts.by,
    ...(opts.reason ? { promotedReason: opts.reason } : {}),
    editHistory: [promoteRecord, ...(sedimentMeta.editHistory ?? [])],
    // 二次召回计数：promote 是"沉淀被 review subagent 第二次命中并采用"的强信号，
    // 这里 +1 让 reviewMatchedCount 成为可观测的"热门技能"指标。
    // 与 SedimentMeta.reviewMatchedCount 声明语义对齐；目前仅在 promote 路径写入，
    // 未来若引入"view 命中也计一次"语义可在此基础上扩展。
    reviewMatchedCount: (sedimentMeta.reviewMatchedCount ?? 0) + 1,
  };
  writeSedimentMeta(to, updatedSediment);

  return { from, to, promotedAt: now };
}

/** 单条 sediment 的快照（用于回收排序与统计）。 */
export interface SedimentSkillStat {
  /** 技能名（即 sediment_skills/<name>）。 */
  name: string;
  /** 技能目录绝对路径。 */
  dir: string;
  /** 创建时间（ISO 8601），缺省时返回目录 mtime 的 ISO。 */
  createdAt: string;
  /** "最近被触碰"时间（ISO 8601），用于 LRU 排序：lastTouchedAt → updatedAt → createdAt。 */
  lastTouchedAt: string;
  /** 是否已被 promote（理论上 sediment_skills/ 下不该存在该情况，作防御使用）。 */
  promoted: boolean;
}

/** 回收动作返回的摘要。 */
export interface EvictResult {
  /** 实际删除的 sediment 名称列表。 */
  evicted: string[];
  /** 因豁免规则（grace period / promoted）被跳过的名称列表（含原因）。 */
  skipped: Array<{ name: string; reason: string }>;
  /** 删除/读取失败的明细。 */
  errors: Array<{ name: string; error: string }>;
}

/**
 * 列出 sediment_skills/ 下所有 sediment 技能的统计快照。
 */
export function listSedimentSkillStats(sedimentDir: string): SedimentSkillStat[] {
  if (!fs.existsSync(sedimentDir)) {
    return [];
  }
  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(sedimentDir, { withFileTypes: true });
  } catch {
    return [];
  }

  const stats: SedimentSkillStat[] = [];
  for (const entry of entries) {
    if (!entry.isDirectory() || entry.name.startsWith(".")) {
      continue;
    }
    const dir = path.join(sedimentDir, entry.name);
    if (!fs.existsSync(path.join(dir, "SKILL.md"))) {
      continue;
    }
    // 缺省时间统一回落到目录的 mtime（极旧/外部拷贝进来的 sediment）
    let fallbackIso: string;
    try {
      fallbackIso = fs.statSync(dir).mtime.toISOString();
    } catch {
      fallbackIso = new Date().toISOString();
    }
    const meta = readSedimentMeta(dir);
    const createdAt = meta?.createdAt ?? fallbackIso;
    const lastTouchedAt = meta?.lastTouchedAt ?? meta?.updatedAt ?? createdAt;
    stats.push({
      name: entry.name,
      dir,
      createdAt,
      lastTouchedAt,
      promoted: Boolean(meta?.promotedAt),
    });
  }
  return stats;
}

/** 安全删除一个 sediment 目录；失败时把错误写入 result.errors。 */
function safeRemoveSedimentDir(dir: string, name: string, result: EvictResult): boolean {
  try {
    fs.rmSync(dir, { recursive: true, force: true });
    result.evicted.push(name);
    return true;
  } catch (err) {
    result.errors.push({ name, error: String(err) });
    return false;
  }
}

/**
 * 判断一个 sediment 是否处于"创建豁免窗口"。
 *
 * @param graceMs 豁免窗口（毫秒）；调用方负责把 days 换算为 ms。
 *                ≤0 表示禁用豁免——任何 sediment 创建后立即可被回收。
 */
function isWithinGracePeriod(stat: SedimentSkillStat, nowMs: number, graceMs: number): boolean {
  if (graceMs <= 0) {
    return false;
  }
  const createdMs = Date.parse(stat.createdAt);
  if (Number.isNaN(createdMs)) {
    return false;
  }
  return nowMs - createdMs < graceMs;
}

/**
 * TTL 回收：删除 lastTouchedAt 距今超过 ttlDays 的 sediment。
 */
export function evictExpiredSediments(
  sedimentDir: string,
  ttlDays: number,
  gracePeriodDays: number,
): EvictResult {
  const result: EvictResult = { evicted: [], skipped: [], errors: [] };
  if (!Number.isFinite(ttlDays) || ttlDays <= 0) {
    return result;
  }

  const nowMs = Date.now();
  const ttlMs = ttlDays * 86_400_000;
  const graceMs = Number.isFinite(gracePeriodDays) ? gracePeriodDays * 86_400_000 : 0;
  const stats = listSedimentSkillStats(sedimentDir);

  for (const stat of stats) {
    if (stat.promoted) {
      result.skipped.push({ name: stat.name, reason: "already promoted" });
      continue;
    }
    if (isWithinGracePeriod(stat, nowMs, graceMs)) {
      result.skipped.push({ name: stat.name, reason: "within grace period" });
      continue;
    }
    const touchedMs = Date.parse(stat.lastTouchedAt);
    if (Number.isNaN(touchedMs)) {
      result.skipped.push({ name: stat.name, reason: "lastTouchedAt unparseable" });
      continue;
    }
    if (nowMs - touchedMs <= ttlMs) {
      continue; // 仍在 TTL 内，正常存活
    }
    safeRemoveSedimentDir(stat.dir, stat.name, result);
  }

  return result;
}

/**
 * LRU 配额回收：当 sediment 数量超过 maxCount 时，按 lastTouchedAt 升序
 * 依次删除最旧的，直到回到 maxCount 以内（含等于）。
 */
export function evictBySedimentQuota(
  sedimentDir: string,
  maxCount: number,
  gracePeriodDays: number,
): EvictResult {
  const result: EvictResult = { evicted: [], skipped: [], errors: [] };
  if (!Number.isFinite(maxCount) || maxCount <= 0) {
    return result;
  }

  const stats = listSedimentSkillStats(sedimentDir);
  if (stats.length <= maxCount) {
    return result;
  }

  const nowMs = Date.now();
  const graceMs = Number.isFinite(gracePeriodDays) ? gracePeriodDays * 86_400_000 : 0;
  // 把候选按"可删优先级"排序：lastTouchedAt 越早越优先删
  // （已 promote / grace period 内的不进入候选池，单独 skip）
  const candidates: SedimentSkillStat[] = [];
  for (const stat of stats) {
    if (stat.promoted) {
      result.skipped.push({ name: stat.name, reason: "already promoted" });
      continue;
    }
    if (isWithinGracePeriod(stat, nowMs, graceMs)) {
      result.skipped.push({ name: stat.name, reason: "within grace period" });
      continue;
    }
    candidates.push(stat);
  }

  candidates.sort((a, b) => {
    const ta = Date.parse(a.lastTouchedAt);
    const tb = Date.parse(b.lastTouchedAt);
    // 不可解析时间排到最前，优先回收
    const na = Number.isNaN(ta) ? -Infinity : ta;
    const nb = Number.isNaN(tb) ? -Infinity : tb;
    return na - nb;
  });

  // 需要把"目录现存数量"压回 maxCount；已被 skip 的不算可减容量
  // remaining = stats.length - evicted.length；当 remaining > maxCount 时继续删
  let remaining = stats.length;
  for (const victim of candidates) {
    if (remaining <= maxCount) {
      break;
    }
    if (safeRemoveSedimentDir(victim.dir, victim.name, result)) {
      remaining -= 1;
    }
  }

  return result;
}

// ---------------------------------------------------------------------------
// 会话消息精简（用于 skill-review 子 Agent 的上下文注入）
// ---------------------------------------------------------------------------

/** 精简后上下文的硬上限（字符数），超过后从最早轮次开始裁剪。 */
const CONDENSED_CONTEXT_MAX_CHARS = 150_000;

/** toolCall 参数摘要的截断长度。 */
const TOOL_PARAM_SUMMARY_MAX = 150;

/**
 * 普通工具调用中单个字符串值（如 regex / query / pattern）的截断阈值。
 */
const TOOL_PARAM_STRING_VALUE_MAX = 120;

/**
 * toolResult 预览的"成功路径"截断长度（按工具类型差异化）。
 *
 * - read_file：仍以"读了哪个文件"为主信号；给 150 字符的文件头预览
 * - list_files / list_dir：目录摘要 → 适中
 * - execute_command：成功输出大多是 noise，给 300；失败走 error 表
 * - search_files / list_code_definition_names：匹配摘要 → 中等
 * - apply_diff / write_to_file / search_and_replace：结果通常很短 → 少量即可
 * - 其他工具：默认值
 */
const TOOL_RESULT_PREVIEW_LIMITS: Record<string, number> = {
  read_file: 150,
  list_files: 100,
  list_dir: 100,
  execute_command: 300,
  search_files: 200,
  list_code_definition_names: 200,
  apply_diff: 100,
  write_to_file: 100,
  search_and_replace: 100,
};
const TOOL_RESULT_PREVIEW_DEFAULT = 100;

/**
 * toolResult 预览的"失败路径"截断长度（isError === true 时使用）。
 *
 * 失败信息（stack trace / 报错原文）是 review 沉淀里**最有价值**的证据之一：
 * "踩坑 → 看到这个报错 → 改成那个方案" 是经典的可沉淀模式。
 */
const TOOL_RESULT_ERROR_PREVIEW_LIMITS: Record<string, number> = {
  read_file: 400,
  list_files: 400,
  list_dir: 400,
  execute_command: 1200,
  search_files: 600,
  list_code_definition_names: 600,
  apply_diff: 400,
  write_to_file: 400,
  search_and_replace: 400,
};
const TOOL_RESULT_ERROR_PREVIEW_DEFAULT = 600;

/**
 * 修改类工具：其 toolCall arguments 中的关键字段（diff/content/replace）才是 review
 * Agent 真正需要看到的"改了什么"，因此走单独路径，给更长的字段预览。
 */
const MUTATION_TOOLS = new Set(["apply_diff", "write_to_file", "search_and_replace"]);

/** mutation 工具中需要保留较多内容的字段。 */
const MUTATION_KEY_FIELDS = new Set(["diff", "content", "replace", "search"]);

/**
 * mutation 关键字段的预览长度（字符数）。
 *
 * 500 字符 ≈ 15~20 行 diff，对中等规模重构（30~50 行）会被截断成"半个 patch"，
 * 让 review 看不清完整改动。提到 1500（≈ 50~70 行）覆盖绝大多数单次 apply_diff。
 */
const MUTATION_FIELD_PREVIEW_MAX = 1500;

// ---------------------------------------------------------------------------
// 自然语言文本（user / assistant text）的去噪与压缩参数
//
// 设计目标：review subagent 关心的是「工作流模式 / 踩坑路径 / 解决方案」，
// 不关心：① agent 的过程独白（"我自己拍板..."）② 给用户的最终业务输出
// （表格、emoji 装饰、洞察总结）③ 业务数据列表枚举。
// 因此对自然语言文本块设置软上限并做模式化降噪：
//
//   - USER_TEXT_MAX：粘贴的需求/PRD 通常较长，保留较多
//   - NORMAL_ASSISTANT_TEXT_MAX：中间过程的 assistant 推理叙述，按软上限截断
//   - FINAL_ASSISTANT_TEXT_MAX：最后一条 assistant 通常是给用户的业务回复，
//     对沉淀价值最低，给最严的上限
// ---------------------------------------------------------------------------

/** user 消息纯文本块的软上限。 */
const USER_TEXT_MAX = 4000;

/**
 * user 文本去重的最小长度阈值。
 */
const USER_DEDUP_MIN_CHARS = 150;

/** 中间轮次 assistant 纯文本块的软上限（推理叙述，中等预算）。 */
const NORMAL_ASSISTANT_TEXT_MAX = 3000;

/** 最后一条 assistant 文本块的软上限（业务回复装饰，最严预算）。 */
const FINAL_ASSISTANT_TEXT_MAX = 4000;

/** 头/尾保留的字符数比例。 */
const TEXT_HEAD_RATIO = 0.5;
const TEXT_TAIL_RATIO = 0.25;

/**
 * "业务数据列表"模式的识别阈值：
 * 行内出现 ≥ N 段「文本(数字单位)」、且总长 ≥ M 字符 → 视为长枚举，整段折叠。
 * 例如："悬崖秋千坠亡(263w)、淘宝免单(201w)、头像(131w)、..."
 */
const ENUM_PATTERN_MIN_HITS = 6;
const ENUM_PATTERN_MIN_CHARS = 200;
/** 全局正则：匹配 `中文/英文短语(数字+可选单位w/万/亿/k/m)`。 */
const ENUM_ITEM_RE = /[\u4e00-\u9fff\w\-]{1,30}\s*[（(]\s*\d[\d.,]*\s*[wWkKmM万亿]?\s*[)）]/g;

/**
 * user 消息中可能被附加的系统注入尾巴（如 `System: ... Exec completed (xxx, code 0) ::`），
 * 这些对 review 沉淀完全无价值，剥离掉以免占用上下文预算。
 * 匹配从 `\nSystem:` 开头到下一个空行或文本结束的整段。
 */
const USER_SYSTEM_NOISE_RE = /\n+System:\s*\[[^\]]+\][^\n]*(?:\n(?!\n)[^\n]*)*/g;

/**
 * 单条剥离规则；kind 用于埋点（observe stripper 命中频次）。
 */
interface EnvelopeStripper {
  kind: string;
  re: RegExp;
  /**
   * 替换函数（默认返回空串）。timestamp 类规则可保留紧凑形态
   * （如 `(14:56) `）以维持时序信号；纯元数据类规则一律置空。
   */
  replace?: (match: string, ...groups: string[]) => string;
}

const USER_ENVELOPE_STRIPPERS: EnvelopeStripper[] = [
  // 1. <relevant_memories>…</relevant_memories>（含嵌套子标签，整块剔除）
  { kind: "memories", re: /<relevant_memories>[\s\S]*?<\/relevant_memories>\s*/g },

  // 2. Sender (untrusted metadata): ```json {…}```
  { kind: "sender_meta", re: /Sender \(untrusted metadata\):\s*```json[\s\S]*?```\s*/g },

  // 3. 多行 System: [...] 回调（Exec completed / Pre-compaction flush 等）
  {
    kind: "system_callback",
    re: /(?:^|\n)System:\s*\[[^\]]+\][\s\S]*?(?=\n\n|\n\[(?:user|assistant|toolResult) #|$)/g,
  },

  // 4. /new /reset 会话启动模板（仅匹配开头，避免误伤用户引述）
  {
    kind: "session_startup",
    re: /^A new session was started via \/new or \/reset[\s\S]*?Do not mention[^.\n]*\.\s*(?:Current time:[^\n]*\n?)?\s*/,
  },

  // 5. 行首时间戳 `[Sat 2026-05-16 16:11 GMT+8]` → `(16:11) ` 紧凑形态
  {
    kind: "timestamp",
    re: /\[(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) \d{4}-\d{2}-\d{2} (\d{2}:\d{2}) GMT[+\-]\d+\]\s*/g,
    replace: (_m, hhmm) => `(${hhmm}) `,
  },

  // 6. 残留的内嵌系统标签
  { kind: "inline_tag", re: /<(system-reminder|truncation_hint)>[\s\S]*?<\/\1>\s*/g },

  // 7. Pre-compaction memory flush 指令
  {
    kind: "pre_compaction",
    re: /Pre-compaction memory flush\.[\s\S]*?(?:Current time:[^\n]*)?\s*(?=\n\n|\n\[|$)/g,
  },

  // 8. 裸的 `Current time: ...` 残留行
  {
    kind: "current_time",
    re: /(?:^|\n)Current time:[^\n]*\n?/g,
  },

  // 9. IDE 注入：<additional_data>…</additional_data>
  { kind: "additional_data", re: /<additional_data>[\s\S]*?<\/additional_data>\s*/g },

  // 10. IDE 注入：<open_and_recently_viewed_files>…</open_and_recently_viewed_files>
  //     （独立出现或 additional_data 残漏时兜底）
  {
    kind: "open_files",
    re: /<open_and_recently_viewed_files>[\s\S]*?<\/open_and_recently_viewed_files>\s*/g,
  },

  // 11. IDE 注入：<recently_modified_files>…</recently_modified_files>
  {
    kind: "modified_files",
    re: /<recently_modified_files>[\s\S]*?<\/recently_modified_files>\s*/g,
  },
];

/** 剥壳结果：含真实文本 + 每类剥离命中次数 + 剥掉的总字符数。 */
export interface UserEnvelopeStripResult {
  /** 剥壳并 trim 后的真实用户文本。 */
  actualUserText: string;
  /** 每类 stripper 命中次数（仅含 >0 项）。 */
  strippedKinds: Record<string, number>;
  /** 剥掉的总字符数（原文长度 - 剥壳后长度）。 */
  strippedChars: number;
  /** 剥壳后是否仍有实质内容（非空 + 非纯空白）。 */
  hadRealContent: boolean;
}

/**
 * 从 user raw text 中剥离所有 channel runtime 注入的元数据壳层，返回真实用户文本 + 剥离统计。
 *
 * @internal Exported for testing only.
 */
export function extractActualUserText(rawText: string): UserEnvelopeStripResult {
  const originalLen = rawText.length;
  let text = rawText;
  const strippedKinds: Record<string, number> = {};

  for (const stripper of USER_ENVELOPE_STRIPPERS) {
    let hits = 0;
    const replaceFn = stripper.replace;
    text = text.replace(stripper.re, (match: string, ...args: unknown[]): string => {
      hits++;
      if (!replaceFn) return "";
      const groups = args.filter((a): a is string => typeof a === "string");
      return replaceFn(match, ...groups);
    });
    if (hits > 0) {
      strippedKinds[stripper.kind] = hits;
    }
  }

  const actualUserText = text.trim();
  return {
    actualUserText,
    strippedKinds,
    strippedChars: originalLen - actualUserText.length,
    hadRealContent: actualUserText.length > 0,
  };
}

/**
 * 从一条消息的 content 块中提取纯文本。
 *
 * 兼容两种常见消息格式：
 *   - `content: string`（纯文本）
 *   - `content: Array<{ type: "text", text: string } | ...>`（Anthropic 风格）
 */
export function extractTextFromContent(content: unknown): string {
  if (typeof content === "string") {
    return content;
  }
  if (!Array.isArray(content)) {
    return "";
  }
  const parts: string[] = [];
  for (const block of content) {
    if (!block || typeof block !== "object") {
      continue;
    }
    const b = block as { type?: string; text?: string };
    if (b.type === "text" && typeof b.text === "string") {
      parts.push(b.text);
    }
  }
  return parts.join("\n");
}

/**
 * 将 toolCall 的参数对象压缩为简短摘要字符串。
 *
 * 示例：`{ path: "/very/long/path/to/file.ts", content: "..." }`
 *   → `path="/very/long/path/to/file.ts", content="…"`（截断至 ~200 字符）
 */
function summarizeToolParams(input: unknown): string {
  if (!input || typeof input !== "object") {
    return typeof input === "string" ? truncate(input, TOOL_PARAM_SUMMARY_MAX) : "";
  }
  const entries = Object.entries(input as Record<string, unknown>);
  if (entries.length === 0) {
    return "";
  }
  const parts: string[] = [];
  let totalLen = 0;
  for (const [key, val] of entries) {
    const valStr =
      typeof val === "string"
        ? val.length > TOOL_PARAM_STRING_VALUE_MAX
          ? `"${val.slice(0, TOOL_PARAM_STRING_VALUE_MAX)}…"`
          : `"${val}"`
        : (JSON.stringify(val) ?? "");
    const part = `${key}=${valStr}`;
    if (totalLen + part.length > TOOL_PARAM_SUMMARY_MAX && parts.length > 0) {
      parts.push("…");
      break;
    }
    parts.push(part);
    totalLen += part.length + 2; // +2 for ", "
  }
  return parts.join(", ");
}

// ---------------------------------------------------------------------------
// T5 — 工具噪音黑名单：整段丢弃（toolCall + toolResult 一起跳过）
const NOISE_TOOL_NAMES = new Set<string>(["memory_get", "memory_search", "memory_list"]);

// ---------------------------------------------------------------------------
// T1 — execute_command / bash 类裸命令工具的语义提取

/** 当 command 字符串短于此阈值时不做语义化，直接走原通道。 */
const EXEC_SEMANTIC_TRIGGER_CHARS = 80;

/** 语义摘要的最长输出长度（含 `command=…` 包装）。 */
const EXEC_SEMANTIC_SUMMARY_MAX = 100;

/**
 * 已知 shell 动词白名单。命中后会优先用动词 + 第一个非 flag 实参做摘要；
 * 未命中走兜底（取 `;` / `&&` / `|` 前的第一个 token）。
 */
// 按用途分组：search/list/text-view/io/net/scm/pkg/build/fs/proc/transfer/text-proc/container/ops
// prettier-ignore
const SHELL_VERB_WHITELIST = new Set([
  "grep", "rg", "ag", "find", "fd",                                  // search
  "ls", "tree", "stat", "wc", "du", "df",                            // list / stat
  "cat", "head", "tail", "less", "more", "echo", "printf", "test",   // text view / io
  "curl", "wget", "ping",                                            // net
  "git", "gh",                                                       // scm
  "npm", "pnpm", "yarn", "bun", "node", "python", "python3",         // pkg / runtime
  "make", "cmake", "go", "cargo", "java", "javac",                   // build
  "cd", "pwd", "mkdir", "rm", "mv", "cp", "ln", "chmod", "chown",    // fs
  "ps", "kill", "top", "lsof", "ss", "netstat",                      // proc / net-stat
  "ssh", "scp", "rsync", "tar", "zip", "unzip",                      // transfer / archive
  "awk", "sed", "sort", "uniq", "cut", "tr", "xargs", "tee",         // text-proc
  "docker", "kubectl",                                               // container
  "openclaw", "clawd", "op", "fly", "launchctl",                     // ops
]);

/**
 * 把 shell command 抽成"动词 + 关键参数"的语义摘要。
 */
function summarizeShellCommand(cmd: string): string {
  const tokens: string[] = [];
  const tokRe = /"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)'|(\S+)/g;
  let m: RegExpExecArray | null;
  while ((m = tokRe.exec(cmd)) !== null) {
    tokens.push(m[1] !== undefined ? `"${m[1]}"` : m[2] !== undefined ? `'${m[2]}'` : m[3]);
  }
  if (tokens.length === 0) return cmd.slice(0, EXEC_SEMANTIC_SUMMARY_MAX);

  // 找到第一个"裸"管道/分隔符 token（引号内的 `|` 已被打包进同一个 token 不会被命中）
  const SEPARATORS = new Set([";", "&&", "||", "|", "2>&1", ">", ">>", "<"]);
  let firstSegTokens = tokens;
  for (let i = 0; i < tokens.length; i++) {
    if (SEPARATORS.has(tokens[i])) {
      firstSegTokens = tokens.slice(0, i);
      break;
    }
  }
  if (firstSegTokens.length === 0) firstSegTokens = tokens;

  const verb = firstSegTokens[0];
  // 2. 抽第一个"关键参数"：跳过 flag（- / -- 开头）和环境赋值（KEY=val）
  let firstArg = "";
  for (let i = 1; i < firstSegTokens.length; i++) {
    const t = firstSegTokens[i];
    if (!t || t.startsWith("-")) continue;
    if (/^[A-Z_][A-Z0-9_]*=/.test(t)) continue;
    firstArg = t;
    break;
  }

  // 3. 若白名单命中且有第一个关键参数，渲染语义形态；否则用动词 + 长度提示
  let summary: string;
  if (firstArg) {
    summary = `${verb} ${firstArg}`;
  } else if (SHELL_VERB_WHITELIST.has(verb)) {
    summary = verb;
  } else {
    // 兜底：保留首 60 字符让人能看出大致 shape
    summary = firstSegTokens.join(" ").slice(0, 60);
  }
  // 命令原文比摘要长太多 → 追加省略号提示后面被吞了
  if (cmd.length > summary.length + 20) summary += " …";
  return summary.slice(0, EXEC_SEMANTIC_SUMMARY_MAX);
}

/** exec 类工具的参数摘要：命中 command 字段且长度超阈值时走语义化路径。*/
function summarizeExecToolParams(input: unknown): string {
  if (!input || typeof input !== "object") return summarizeToolParams(input);
  const obj = input as Record<string, unknown>;
  const cmd = typeof obj.command === "string" ? obj.command : "";
  if (!cmd || cmd.length <= EXEC_SEMANTIC_TRIGGER_CHARS) {
    // 短命令保留原貌
    return summarizeToolParams(input);
  }

  const parts: string[] = [`command=${summarizeShellCommand(cmd)}`];
  // 把其他非 command 字段（cwd / timeout / env 等）一并附上，避免丢上下文
  for (const [k, v] of Object.entries(obj)) {
    if (k === "command") continue;
    if (v == null) continue;
    const valStr =
      typeof v === "string"
        ? v.length > TOOL_PARAM_STRING_VALUE_MAX
          ? `"${v.slice(0, TOOL_PARAM_STRING_VALUE_MAX)}…"`
          : `"${v}"`
        : (JSON.stringify(v) ?? "");
    parts.push(`${k}=${valStr}`);
  }
  return parts.join(", ");
}

/** 命中本集合的工具走 exec 语义化摘要（替代默认 summarizeToolParams）。 */
const EXEC_SEMANTIC_TOOLS = new Set(["execute_command", "exec", "bash", "shell", "run_command"]);

/** 截断字符串至指定长度，末尾加省略号。 */
function truncate(s: string, max: number): string {
  if (s.length <= max) {
    return s;
  }
  return s.slice(0, max) + "…";
}

/**
 * 折叠"业务数据列表"模式：行内出现 ≥ ENUM_PATTERN_MIN_HITS 段
 * 短语+(数字单位) 形式 → 整行替换为占位提示。
 *
 * 仅作用于"形如长枚举"的行，对正常段落（包含解释性句子的）无影响。
 * 对沉淀技能而言，业务数据本身没有任何复用价值，去掉后能腾出大量预算。
 */
function collapseEnumLines(text: string): string {
  const lines = text.split("\n");
  const out: string[] = [];
  for (const line of lines) {
    if (line.length < ENUM_PATTERN_MIN_CHARS) {
      out.push(line);
      continue;
    }
    const matches = line.match(ENUM_ITEM_RE);
    if (matches && matches.length >= ENUM_PATTERN_MIN_HITS) {
      out.push(`[business-data list elided: ${matches.length} items, ${line.length} chars]`);
    } else {
      out.push(line);
    }
  }
  return out.join("\n");
}

// ---------------------------------------------------------------------------
// 代码块折叠：识别 Markdown fenced code block（```lang ... ```）并压缩长代码块

/** 代码块折叠的行数阈值：超过此行数才折叠，短代码块原样保留。 */
const CODE_BLOCK_COLLAPSE_MIN_LINES = 10;

/** 代码块折叠的字符数阈值：即使行数未达标，超过此字符数也触发折叠。 */
const CODE_BLOCK_COLLAPSE_MIN_CHARS = 400;

/** 折叠时保留的头部行数。 */
const CODE_BLOCK_HEAD_LINES = 4;

/** 折叠时保留的尾部行数。 */
const CODE_BLOCK_TAIL_LINES = 2;

function collapseCodeBlocks(text: string): string {
  // 匹配完整的 fenced code block：开头 ``` + 可选语言标记，结尾独立 ```
  // 使用非贪婪匹配，支持多个代码块
  return text.replace(
    /^( {0,3})(`{3,})([^\n`]*)\n([\s\S]*?)\n\1\2[^\S\n]*$/gm,
    (match, _indent: string, _fence: string, lang: string, body: string) => {
      const langTag = lang.trim();
      const lines = body.split("\n");
      const totalLines = lines.length;
      const totalChars = body.length;

      // 短代码块不折叠
      if (
        totalLines < CODE_BLOCK_COLLAPSE_MIN_LINES &&
        totalChars < CODE_BLOCK_COLLAPSE_MIN_CHARS
      ) {
        return match;
      }

      const headLines = lines.slice(0, CODE_BLOCK_HEAD_LINES);
      const tailLines = lines.slice(-CODE_BLOCK_TAIL_LINES);
      const collapsedLines = totalLines - CODE_BLOCK_HEAD_LINES - CODE_BLOCK_TAIL_LINES;
      const collapsedChars = totalChars - headLines.join("\n").length - tailLines.join("\n").length;

      // 如果折叠后反而没省多少（折叠行数 ≤ 2），不折叠
      if (collapsedLines <= 2) {
        return match;
      }

      const langLabel = langTag ? `\`\`\`${langTag}` : "```";
      return (
        `${langLabel}\n` +
        headLines.join("\n") +
        `\n... [${collapsedLines} lines, ${collapsedChars} chars collapsed]\n` +
        tailLines.join("\n") +
        "\n```"
      );
    },
  );
}

/**
 * 对自然语言文本块做"头+尾"压缩。短于软上限时原样返回。
 *
 * 头/尾保留比例由 TEXT_HEAD_RATIO / TEXT_TAIL_RATIO 控制，中间替换为
 * `…[N chars elided]…` 占位。这样既保留任务起始上下文（头），又保留
 * 结论/最终状态（尾），最大化 review subagent 的可读信号。
 */
function compressLongText(text: string, softMax: number): string {
  if (text.length <= softMax) {
    return text;
  }
  const headLen = Math.floor(softMax * TEXT_HEAD_RATIO);
  const tailLen = Math.floor(softMax * TEXT_TAIL_RATIO);
  const elided = text.length - headLen - tailLen;
  if (elided <= 0) {
    return text;
  }
  return (
    text.slice(0, headLen) +
    `\n…[${elided.toLocaleString()} chars elided]…\n` +
    text.slice(-tailLen)
  );
}

/**
 * user 消息的去噪 + 压缩流水线（升级版，2026-05 优化）：
 *   1. 剥离 channel runtime 注入的元数据壳层
 *   2. 残留的 USER_SYSTEM_NOISE_RE 单行 System 尾巴兜底
 *   3. 折叠业务数据长枚举行
 *   4. 折叠长代码块（SQL/脚本等）
 *   5. 头+尾保留压缩
 */
function denoiseUserText(text: string): string {
  const { actualUserText } = extractActualUserText(text);
  const tailStripped = actualUserText.replace(USER_SYSTEM_NOISE_RE, "").trim();
  const collapsed = collapseCodeBlocks(collapseEnumLines(tailStripped));
  return compressLongText(collapsed, USER_TEXT_MAX);
}

/**
 * assistant 文本块的去噪 + 压缩。
 *
 * @param softMax 软上限（最后一条 assistant 应使用 FINAL_ASSISTANT_TEXT_MAX，
 *   其余使用 NORMAL_ASSISTANT_TEXT_MAX）。最后一条通常是面向用户的最终业务回复，
 *   对沉淀价值最低，给最严的上限。
 */
function denoiseAssistantText(text: string, softMax: number): string {
  const collapsed = collapseCodeBlocks(collapseEnumLines(text));
  return compressLongText(collapsed, softMax);
}

/**
 * 修改类工具的参数摘要。保留 path 全文 + 关键 diff/content 字段长预览，
 * 让下游 review Agent 能看到"改了什么"，而不是被截断到 50 字符的失真内容。
 */
function summarizeMutationToolParams(input: unknown): string {
  if (!input || typeof input !== "object") {
    return typeof input === "string" ? truncate(input, MUTATION_FIELD_PREVIEW_MAX) : "";
  }
  const entries = Object.entries(input as Record<string, unknown>);
  if (entries.length === 0) {
    return "";
  }
  const parts: string[] = [];
  for (const [key, val] of entries) {
    if (key === "path" && typeof val === "string") {
      parts.push(`path="${val}"`);
      continue;
    }
    if (MUTATION_KEY_FIELDS.has(key) && typeof val === "string") {
      const lineCount = val.split("\n").length;
      const preview = truncate(val, MUTATION_FIELD_PREVIEW_MAX);
      parts.push(`${key}=<${lineCount} lines, ${val.length} chars>\n${preview}`);
      continue;
    }
    // 其他字段走轻量摘要（与 summarizeToolParams 风格一致）
    const valStr =
      typeof val === "string"
        ? val.length > TOOL_PARAM_STRING_VALUE_MAX
          ? `"${val.slice(0, TOOL_PARAM_STRING_VALUE_MAX)}…"`
          : `"${val}"`
        : (JSON.stringify(val) ?? "");
    parts.push(`${key}=${valStr}`);
  }
  return parts.join(", ");
}

/**
 * 稳定序列化对象（key 排序），用于生成 toolResult 去重 key。
 * 不依赖 JSON.stringify 的 key 顺序，保证语义相同的参数生成相同 key。
 *
 * 注意：null/undefined 分支必须排在 `typeof obj !== "object"` 之前 ——
 * 因为 `typeof null === "object"`，否则 null 会落到下面的 `Object.keys(null)` 报错。
 */
function stableStringify(obj: unknown): string {
  if (obj === null || obj === undefined) {
    return JSON.stringify(obj) ?? "null";
  }
  if (typeof obj !== "object") {
    return JSON.stringify(obj);
  }
  if (Array.isArray(obj)) {
    return `[${obj.map(stableStringify).join(",")}]`;
  }
  const keys = Object.keys(obj as Record<string, unknown>).sort();
  const parts = keys.map(
    (k) => `${JSON.stringify(k)}:${stableStringify((obj as Record<string, unknown>)[k])}`,
  );
  return `{${parts.join(",")}}`;
}

/**
 * 预扫描 messages，建立 toolCallId → { name, args } 索引。
 * 用于 toolResult 阶段反查 toolCall 参数做去重 key（不能用 toolResult.content
 * 自身做 key —— 它可能因时间戳/换行差异而变动）。
 *
 * 兼容多种 id 字段命名：openclaw 规范用 `id`，部分上游格式（OpenAI/Anthropic
 * 派生）会落到 `toolCallId` 或 `tool_call_id`。任一存在即可索引。
 */
function indexToolCalls(messages: unknown[]): Map<string, { name: string; args: unknown }> {
  const idx = new Map<string, { name: string; args: unknown }>();
  for (const m of messages) {
    if (!m || typeof m !== "object") continue;
    const msg = m as Record<string, unknown>;
    if (msg.role !== "assistant" || !Array.isArray(msg.content)) continue;
    for (const block of msg.content as Array<Record<string, unknown>>) {
      if (block?.type !== "toolCall") continue;
      const callId =
        (typeof block.id === "string" && block.id) ||
        (typeof block.toolCallId === "string" && block.toolCallId) ||
        (typeof block.tool_call_id === "string" && block.tool_call_id) ||
        "";
      if (!callId) continue;
      idx.set(callId, {
        name: typeof block.name === "string" ? block.name : "unknown",
        args: block.arguments,
      });
    }
  }
  return idx;
}

/**
 * 格式化单条 assistant 消息的 content 块。
 *
 * openclaw 规范格式：
 * - `type: "text"` → 保留全文
 * - `type: "toolCall"` → `→ tool: name(param_summary)`
 * - `type: "thinking"` → 跳过
 * - 其他 → 跳过
 */
/**
 * @param textSoftMax 单个 text 子块的软上限（按 assistant 在序列中位置传入：
 *   最后一条用 FINAL_ASSISTANT_TEXT_MAX，中间用 NORMAL_ASSISTANT_TEXT_MAX）。
 *   仅作用于 text 子块；toolCall 行原样保留，避免误伤工具调用轨迹。
 */
/**
 * 跨 turn 共享的 toolCall 去重上下文。由 buildCondensedContext 维护并传入，
 * 让多条 assistant 消息之间能识别出"同一个 (toolName, args)"被反复调用的情况
 */
interface ToolCallDedupContext {
  /** dedupKey → 首次出现时所属 assistant turn 的 1-based 序号。 */
  seen: Map<string, number>;
  /** 命中去重的次数（仅用于本次压缩过程内部统计）。 */
  dedupedCount: number;
  /** T5 — 因命中 NOISE_TOOL_NAMES 被整段丢弃的 toolCall 子块数。 */
  droppedNoiseCount: number;
}

function formatAssistantContent(
  content: unknown,
  textSoftMax: number,
  /** 当前 assistant turn 的 1-based 序号（即将写入 turns 数组的那个位置）。 */
  turnNumber: number,
  /** 跨 turn 共享的 toolCall 去重上下文；不传则不去重（向后兼容）。 */
  dedupCtx?: ToolCallDedupContext,
): string {
  if (typeof content === "string") {
    return denoiseAssistantText(content, textSoftMax);
  }
  if (!Array.isArray(content)) {
    return "";
  }
  const lines: string[] = [];
  for (const block of content) {
    if (!block || typeof block !== "object") {
      continue;
    }
    const b = block as {
      type?: string;
      text?: string;
      name?: string;
      arguments?: unknown;
    };

    switch (b.type) {
      case "text":
        if (b.text) {
          // 仅对 text 子块做去噪/压缩；mixed text+toolCall 时 toolCall 行不受影响
          lines.push(denoiseAssistantText(b.text, textSoftMax));
        }
        break;
      case "toolCall": {
        const name = b.name ?? "unknown";

        // T5 — 噪音工具：整段丢弃，不写任何占位。
        if (NOISE_TOOL_NAMES.has(name)) {
          if (dedupCtx) dedupCtx.droppedNoiseCount++;
          break;
        }

        // 跨 turn 去重：同一 (toolName, stable(args)) 的 toolCall，第二次起压成引用
        if (dedupCtx) {
          const dedupKey = `${name}:${stableStringify(b.arguments)}`;
          const firstSeen = dedupCtx.seen.get(dedupKey);
          if (firstSeen !== undefined) {
            lines.push(`→ tool: ${name} (same call as turn #${firstSeen})`);
            dedupCtx.dedupedCount++;
            break;
          }
          dedupCtx.seen.set(dedupKey, turnNumber);
        }

        // 三类工具走差异化摘要：
        let paramSummary: string;
        if (MUTATION_TOOLS.has(name)) {
          paramSummary = summarizeMutationToolParams(b.arguments);
        } else if (EXEC_SEMANTIC_TOOLS.has(name)) {
          paramSummary = summarizeExecToolParams(b.arguments);
        } else {
          paramSummary = summarizeToolParams(b.arguments);
        }
        lines.push(`→ tool: ${name}(${paramSummary})`);
        break;
      }
      case "thinking":
        // 完全跳过内部推理
        break;
      default:
        // 跳过未知类型
        break;
    }
  }
  return lines.join("\n");
}

/**
 * 格式化单条 toolResult 消息为精简预览。
 *
 * openclaw 规范格式：`{ role: "toolResult", toolCallId, toolName, content, isError }`
 * content 可以是 `string` 或 `Array<{ type: "text"; text: string }>`。
 *
 * 输出格式：`← toolName [N chars] preview_text…`
 * 预览长度按工具类型差异化（见 TOOL_RESULT_PREVIEW_LIMITS）。
 *
 * @param msg toolResult 消息原始对象
 * @param overrideToolName 可选的外部解析出的 toolName。
 *   传入场景：调用方通过 toolCallId 反查 toolCall 拿到了更准确的 name
 *   （如 msg.toolName 缺失或为空时）。这样可保证：
 *     - 输出前缀 `← <name>` 与去重引用 `← <name> (same as turn #N)` 一致
 *     - TOOL_RESULT_PREVIEW_LIMITS 查表命中正确的工具策略
 */
function formatToolResult(msg: Record<string, unknown>, overrideToolName?: string): string {
  if (msg.role !== "toolResult") {
    return "";
  }

  const toolName =
    overrideToolName ?? (typeof msg.toolName === "string" ? msg.toolName : "unknown");

  let fullText = "";
  if (typeof msg.content === "string") {
    fullText = msg.content;
  } else if (Array.isArray(msg.content)) {
    fullText = (msg.content as Array<{ type?: string; text?: string }>)
      .map((c) => c.text ?? "")
      .join("");
  }

  // 完全 0 信息的 toolResult（成功路径且 trim 后无任何内容）直接丢弃。
  const isError = Boolean(msg.isError);
  if (!isError && fullText.trim().length === 0) {
    return "";
  }

  // error 路径用更宽松的预览上限
  const previewMax = isError
    ? (TOOL_RESULT_ERROR_PREVIEW_LIMITS[toolName] ?? TOOL_RESULT_ERROR_PREVIEW_DEFAULT)
    : (TOOL_RESULT_PREVIEW_LIMITS[toolName] ?? TOOL_RESULT_PREVIEW_DEFAULT);
  const errorTag = isError ? " [error]" : "";
  return `← ${toolName}${errorTag} [${fullText.length} chars] ${truncate(fullText.replace(/\n/g, " "), previewMax)}`;
}

/** 计算 toolResult 输出预览的"内容去重 key"。*/
const TOOL_RESULT_CONTENT_DEDUP_KEY_PREFIX_CHARS = 200;
/** 小于此长度的 toolResult 不参与内容去重（短结果重复成本低，加去重反而增加复杂度）。 */
const TOOL_RESULT_CONTENT_DEDUP_MIN_CHARS = 80;

function computeToolResultContentKey(
  toolName: string,
  fullText: string,
  isError: boolean,
): string | "" {
  if (isError) return ""; // 错误永不去重
  if (fullText.length < TOOL_RESULT_CONTENT_DEDUP_MIN_CHARS) return "";
  const normalized = fullText
    .slice(0, TOOL_RESULT_CONTENT_DEDUP_KEY_PREFIX_CHARS)
    .replace(/\s+/g, " ")
    .trim();
  if (!normalized) return "";
  return `${toolName}::${normalized}`;
}

/** 单条精简后消息的内部表示。 */
type TurnKind = "user" | "assistant" | "toolResult";

/** T3 — toolResult 内容去重上下文。在 buildCondensedContext 内部创建并贯穿单次调用。 */
interface ToolResultContentDedupContext {
  /** content-key → 首次出现的 turn 序号（1-based） */
  seen: Map<string, number>;
  /** 命中内容去重的次数（不含 call-level 去重） */
  dedupedCount: number;
  /** 因 0 信息被静默丢弃的 toolResult 数（T4） */
  droppedEmptyCount: number;
  /** T5 — 因命中 NOISE_TOOL_NAMES 被整段丢弃的 toolResult 数。 */
  droppedNoiseCount: number;
}
interface FormattedTurn {
  kind: TurnKind;
  text: string;
  /**
   * 分组 ID。assistant 与其后紧跟的所有 toolResult 共享同一 groupId，
   * user 独立成组。裁剪时按 group 为最小单位，避免出现孤儿 toolResult。
   */
  groupId: number;
  /**
   * 1-based 原始序号（裁剪前生成时即固定，不随裁剪变化）。
   * 用于 toolResult 去重的 `(same as turn #N)` 引用与输出阶段
   * `[kind #N]` 标签保持一致，让被引用的 turn 即便被裁掉，
   * 下游也能从相邻保留 turn 的编号推断原始位置。
   */
  origIndex: number;
}

/** 将连续 turns 按 groupId 分桶。 */
function partitionByGroup(turns: FormattedTurn[]): FormattedTurn[][] {
  const groups: FormattedTurn[][] = [];
  let current: FormattedTurn[] = [];
  let currentId = -1;
  for (const t of turns) {
    if (t.groupId !== currentId) {
      if (current.length > 0) groups.push(current);
      current = [];
      currentId = t.groupId;
    }
    current.push(t);
  }
  if (current.length > 0) groups.push(current);
  return groups;
}

/**
 * 单条 turn 在最终输出中占用的字符数。
 *
 * 必须与 buildCondensedContext 输出阶段使用的格式保持一致：
 *   `[${kind} #${origIndex}]\n${text}` + `\n\n` 分隔符
 * 否则裁剪触发条件会与实际输出长度脱钩，导致超限。
 */
function turnLen(t: FormattedTurn): number {
  // `[kind #N]\n` 长度 = 4(`[ ]\n`) + kind.length + 2(` #`) + N 的位数
  return 4 + t.kind.length + 2 + String(t.origIndex).length + t.text.length + 2;
}

/** 整组 turns 的总字符数。 */
function groupLen(g: FormattedTurn[]): number {
  let sum = 0;
  for (const t of g) sum += turnLen(t);
  return sum;
}

/**
 * 将从 `getSessionMessages()` 获取的原始消息数组精简为紧凑文本，
 * 供 skill-review 子 Agent 作为上下文使用。
 *
 * 基于 openclaw 规范消息格式（role: "user" | "assistant" | "toolResult"）精简：
 *   - user 消息：剥离 `System: ... Exec completed ...` 等系统注入尾巴，
 *     折叠业务数据长枚举行，按 USER_TEXT_MAX 做"头+尾"软上限压缩
 *   - assistant text：折叠业务数据长枚举行，按软上限做"头+尾"压缩。
 *     最后一条 assistant 通常是面向用户的最终业务回复，使用最严的
 *     FINAL_ASSISTANT_TEXT_MAX；其余使用 NORMAL_ASSISTANT_TEXT_MAX。
 *     注意：仅 text 子块被压缩，混排在同一条消息中的 toolCall 行原样保留，
 *     不会误伤工具调用轨迹。
 *   - assistant toolCall：压缩为 `→ tool: name(param_summary)`；
 *     mutation 类工具（apply_diff / write_to_file / search_and_replace）走更长的
 *     字段预览，保留 diff/content 主体（500 字符 + 行数统计）
 *   - assistant thinking：完全移除
 *   - toolResult 消息：压缩为 `← toolName [N chars] preview…`；
 *     若同一 (toolName, args) 已出现过，替换为 `← toolName (same as turn #N)` 引用
 *   - 元数据/session/model_change 等非消息条目：跳过
 *
 * 输出为按 `[user #N]` / `[assistant #N]` / `[toolResult #N]` 标记的紧凑消息列表。
 * 若总长度超过 CONDENSED_CONTEXT_MAX_CHARS，按 group 为单位裁剪 middle，
 * 保证 assistant + toolResult 不被分开（避免孤儿 toolResult）。仍超限时
 * 从 head 尾部按 group 裁剪。
 */
export function buildCondensedContext(messages: unknown[]): string {
  if (!Array.isArray(messages) || messages.length === 0) {
    return "(empty session)";
  }

  // ---- 预处理：建立 toolCallId → 参数索引（用于 toolResult 去重 key） ----
  const toolCallIndex = indexToolCalls(messages);

  // ---- 预处理：定位"最后一条 assistant 消息"在原始数组中的索引 ----
  // 该位置的 assistant text 通常是面向用户的最终业务回复（含表格/洞察/装饰），
  // 对沉淀技能价值最低，使用更严的软上限 FINAL_ASSISTANT_TEXT_MAX。
  let lastAssistantOrigIdx = -1;
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i];
    if (m && typeof m === "object" && (m as { role?: unknown }).role === "assistant") {
      lastAssistantOrigIdx = i;
      break;
    }
  }

  // ---- 第一遍：messages → FormattedTurn[]（带 groupId + 三类去重） ----
  const turns: FormattedTurn[] = [];

  /** toolResult 去重：dedupKey → 首次出现的 turn 序号（1-based）。 */
  const seenToolResults = new Map<string, number>();
  /**
   * user 文本去重：归一化后的 text → 首次出现的 turn 序号。
   */
  const seenUserTexts = new Map<string, number>();
  /** toolCall 跨 turn 去重上下文（在 formatAssistantContent 内部使用）。 */
  const toolCallDedupCtx: ToolCallDedupContext = {
    seen: new Map(),
    dedupedCount: 0,
    droppedNoiseCount: 0,
  };
  /** toolResult 内容去重 + 空结果丢弃 + 噪音工具丢弃统计 */
  const toolResultContentDedupCtx: ToolResultContentDedupContext = {
    seen: new Map(),
    dedupedCount: 0,
    droppedEmptyCount: 0,
    droppedNoiseCount: 0,
  };

  let groupCounter = 0;
  let lastKind: TurnKind | null = null;

  for (let i = 0; i < messages.length; i++) {
    const m = messages[i];
    if (!m || typeof m !== "object") continue;
    const msg = m as Record<string, unknown>;
    const role = msg.role as string | undefined;
    if (!role) continue;

    switch (role) {
      case "user": {
        const userTextRaw = extractTextFromContent(msg.content);
        if (!userTextRaw.trim()) break;

        // P1 — 先做 envelope 剥离拿到真实用户文本，再决定后续处理路径
        const stripResult = extractActualUserText(userTextRaw);
        if (!stripResult.hadRealContent) {
          break;
        }

        const userText = denoiseUserText(userTextRaw);
        if (!userText.trim()) break;
        let finalText = userText;
        if (userText.length >= USER_DEDUP_MIN_CHARS) {
          const firstSeen = seenUserTexts.get(userText);
          if (firstSeen !== undefined) {
            finalText = `[user content same as turn #${firstSeen}, ${userText.length} chars elided]`;
          } else {
            seenUserTexts.set(userText, turns.length + 1);
          }
        }

        groupCounter++;
        turns.push({
          kind: "user",
          text: finalText,
          groupId: groupCounter,
          origIndex: turns.length + 1,
        });
        lastKind = "user";
        break;
      }
      case "assistant": {
        const textSoftMax =
          i === lastAssistantOrigIdx ? FINAL_ASSISTANT_TEXT_MAX : NORMAL_ASSISTANT_TEXT_MAX;
        const formatted = formatAssistantContent(
          msg.content,
          textSoftMax,
          turns.length + 1,
          toolCallDedupCtx,
        );
        if (!formatted.trim()) break;
        groupCounter++;
        turns.push({
          kind: "assistant",
          text: formatted,
          groupId: groupCounter,
          origIndex: turns.length + 1,
        });
        lastKind = "assistant";
        break;
      }
      case "toolResult": {
        // 兼容多种 id 字段命名（与 indexToolCalls 保持一致）
        const toolCallId =
          (typeof msg.toolCallId === "string" && msg.toolCallId) ||
          (typeof msg.tool_call_id === "string" && msg.tool_call_id) ||
          "";
        const callInfo = toolCallId ? toolCallIndex.get(toolCallId) : undefined;
        const toolName =
          callInfo?.name ?? (typeof msg.toolName === "string" ? msg.toolName : "unknown");

        // T5 — 噪音工具：整段丢弃，不写任何占位。
        if (NOISE_TOOL_NAMES.has(toolName)) {
          toolResultContentDedupCtx.droppedNoiseCount++;
          break;
        }

        // 去重 key 的优先级（call-level）：
        //   1. 命中 callInfo → 用 (toolName, stable(args))，最准确
        //   2. 仅有 toolCallId → 用 (toolName, #id)，至少能识别同一次调用的重复回放
        //   3. 都没有 → 不参与 call-level 去重（避免所有 anonymous toolResult 互相误判）
        let dedupKey = "";
        if (callInfo) {
          dedupKey = `${toolName}:${stableStringify(callInfo.args)}`;
        } else if (toolCallId) {
          dedupKey = `${toolName}:#${toolCallId}`;
        }

        const firstSeenTurn = dedupKey ? seenToolResults.get(dedupKey) : undefined;

        let text: string;
        if (firstSeenTurn !== undefined) {
          // Call-level 命中（相同入参）—— 最强信号
          const errorTag = msg.isError ? " [error]" : "";
          text = `← ${toolName}${errorTag} (same as turn #${firstSeenTurn})`;
        } else {
          // 提前算好 fullText 与 isError，给 T3 内容去重使用
          let fullText = "";
          if (typeof msg.content === "string") {
            fullText = msg.content;
          } else if (Array.isArray(msg.content)) {
            fullText = (msg.content as Array<{ type?: string; text?: string }>)
              .map((c) => c.text ?? "")
              .join("");
          }
          const isError = Boolean(msg.isError);

          // 完全 0 信息的成功 toolResult（trim 后为空）直接跳过
          if (!isError && fullText.trim().length === 0) {
            toolResultContentDedupCtx.droppedEmptyCount++;
            break; // 不更新 lastKind：保持 group 归属指向真正最近一条
          }

          // T3 — 内容级去重：成功路径且长度过阈值才参与
          const contentKey = computeToolResultContentKey(toolName, fullText, isError);
          const firstSeenByContent = contentKey
            ? toolResultContentDedupCtx.seen.get(contentKey)
            : undefined;
          if (firstSeenByContent !== undefined) {
            text = `← ${toolName} [${fullText.length} chars] (same output as toolResult #${firstSeenByContent})`;
            toolResultContentDedupCtx.dedupedCount++;
          } else {
            // 正常渲染：把解析得到的 toolName 传入，避免 formatToolResult 内部因
            // msg.toolName 缺失而退化成 "unknown"——保证输出前缀、去重引用、
            // TOOL_RESULT_PREVIEW_LIMITS 三处看到的 toolName 一致。
            text = formatToolResult(msg, toolName);
            // text 为空表示 msg 不符合 toolResult 规范（理论上前面 T4 早拦了，
            // 但 schema 不规范的边界仍可能命中）—— 跳过本条不更新 lastKind。
            if (!text) break;
            if (contentKey) {
              toolResultContentDedupCtx.seen.set(contentKey, turns.length + 1);
            }
          }
          // 不管走 T3 命中还是正常渲染，都把 call-level dedupKey 也记一次，
          // 让后续真正"相同入参"的回放仍能命中更强的 call-level 路径。
          if (dedupKey) {
            seenToolResults.set(dedupKey, turns.length + 1);
          }
        }

        // toolResult 与上一条 assistant/toolResult 共享 groupId（保证不出现孤儿
        // toolResult 被裁剪时丢掉所属的 assistant 调用）；否则独立成组。
        const groupId =
          lastKind === "assistant" || lastKind === "toolResult" ? groupCounter : ++groupCounter;
        turns.push({
          kind: "toolResult",
          text,
          groupId,
          origIndex: turns.length + 1,
        });
        lastKind = "toolResult";
        break;
      }
      default:
        break;
    }
  }

  if (turns.length === 0) {
    return "(empty session)";
  }

  // ---- 第二遍：按 group 裁剪 ----
  const groups = partitionByGroup(turns);

  // head：第一个 group + 紧随其后的所有非 user group（用户首轮需求 + 第一轮回应）
  let headEnd = 0;
  for (let i = 1; i < groups.length; i++) {
    if (groups[i][0].kind === "user") break;
    headEnd = i;
  }

  let total = 0;
  for (const g of groups) total += groupLen(g);

  // 优先从 middle 区域（headEnd+1 开始）的最前面整组删除，至少保留 1 个 tail group
  while (total > CONDENSED_CONTEXT_MAX_CHARS && groups.length - headEnd - 1 > 1) {
    const removed = groups.splice(headEnd + 1, 1)[0];
    total -= groupLen(removed);
  }

  // 兜底：裁完 middle 仍超限时，从 head 尾部按 group 裁剪（保留至少首组）
  while (total > CONDENSED_CONTEXT_MAX_CHARS && headEnd > 0) {
    const removed = groups.splice(headEnd, 1)[0];
    total -= groupLen(removed);
    headEnd--;
  }

  // ---- 输出 ----
  // [kind #N] 中的 N 用裁剪前固定的 origIndex，与 toolResult 去重写入的
  // `(same as turn #N)` 中的 N 一致，使引用即便被裁掉也能在保留的相邻 turn
  // 中找到上下文（编号会出现跳号 = 中间被裁了）。
  let retainedUserTurns = 0;
  const lines: string[] = [];
  for (const g of groups) {
    for (const t of g) {
      if (t.kind === "user") retainedUserTurns++;
      lines.push(`[${t.kind} #${t.origIndex}]\n${t.text}`);
    }
  }
  const body = lines.join("\n\n");

  return `${body}\n`;
}
