/**
 * skill_manage 工具 —— 由 Agent 自主管理技能的创建与编辑。
 *
 * 允许 Agent 创建、更新、删除技能，把成功方法沉淀为可复用的过程知识。
 * 新技能写入托管目录（<agent workspace>/sediment_skills/），与 skills/ 同级。
 * OpenClaw 核心引擎不会自动加载 sediment_skills/ 下的技能，
 * 沉淀技能需经后续迁移到 skills/ 才会被自动发现。
 *
 * 支持动作：
 *   create      —— 创建新技能（SKILL.md + 目录结构）
 *   edit        —— 覆盖 SKILL.md 内容（整文件重写）
 *   patch       —— 在 SKILL.md 或附属文件中定点查找替换
 *   delete      —— 删除整个技能
 *   write_file  —— 写入/覆盖附属文件（references/templates/scripts/assets）
 *   remove_file —— 删除技能中的附属文件
 */

import fs from "node:fs";
import path from "node:path";
import { Type } from "@sinclair/typebox";
import { scanSkill, shouldAllowInstall, formatScanReport } from "./skills-guard.js";
import type {
  SedimentMeta,
  SkillEditRecord,
  SkillLocation,
  SkillManageParams,
  SkillManageResult,
  SkillMeta,
  SkillMetaAction,
  SkillSource,
} from "./types.js";
import {
  atomicWriteText,
  findSimilarSkills,
  findSkill,
  isLocalSkill,
  isOfficialSkill,
  isSedimentOrigin,
  listSkillFiles,
  normalizeFrontmatterDescription,
  parseFrontmatter,
  promoteSedimentSkill,
  readSedimentMeta,
  readSkillMeta,
  resolveSkillDir,
  SEDIMENT_META_FILENAME,
  SKILL_META_FILENAME,
  validateContentSize,
  validateFilePath,
  validateFileSize,
  validateFrontmatter,
  validateName,
  validateWithinDir,
  writeSedimentMeta,
  writeSkillMeta,
} from "./utils.js";

// ---------------------------------------------------------------------------
// 工具参数的 TypeBox Schema
// ---------------------------------------------------------------------------

export const SkillManageToolSchema = Type.Object(
  {
    action: Type.Unsafe<string>({
      type: "string",
      enum: [
        "create",
        "patch",
        "edit",
        "delete",
        "write_file",
        "remove_file",
        "view",
        "list",
        "promote",
      ],
      description: "The action to perform.",
    }),
    name: Type.Optional(
      Type.String({
        description:
          "Skill name (lowercase, hyphens/underscores, max 64 chars). " +
          "Required for create/patch/edit/delete/write_file/remove_file/view. " +
          "Optional for 'list' (omit to list all skills).",
      }),
    ),
    content: Type.Optional(
      Type.String({
        description:
          "Full SKILL.md content (YAML frontmatter + markdown body). " +
          "Required for 'create' and 'edit'. For 'edit', read the skill " +
          "first with skill_view() and provide the complete updated text.",
      }),
    ),
    old_string: Type.Optional(
      Type.String({
        description:
          "Text to find in the file (required for 'patch'). Must be unique " +
          "unless replace_all=true. Include enough surrounding context to " +
          "ensure uniqueness.",
      }),
    ),
    new_string: Type.Optional(
      Type.String({
        description:
          "Replacement text (required for 'patch'). Can be empty string " +
          "to delete the matched text.",
      }),
    ),
    replace_all: Type.Optional(
      Type.Boolean({
        description:
          "For 'patch': replace all occurrences instead of requiring a unique match (default: false).",
      }),
    ),
    file_path: Type.Optional(
      Type.String({
        description:
          "Path to a supporting file within the skill directory. " +
          "For 'write_file'/'remove_file': required, must be under references/, " +
          "templates/, scripts/, or assets/. " +
          "For 'patch': optional, defaults to SKILL.md if omitted.",
      }),
    ),
    file_content: Type.Optional(
      Type.String({
        description: "Content for the file. Required for 'write_file'.",
      }),
    ),
    promote_reason: Type.Optional(
      Type.String({
        description:
          "Required for 'promote'. The review subagent's reusability evidence " +
          "explaining why this sediment skill should be activated " +
          "(e.g., a brief quote of the current task that matched the skill). " +
          "Recorded in __sediment_meta__.json and __skill_meta__.json for audit.",
      }),
    ),
  },
  { additionalProperties: false },
);

// ---------------------------------------------------------------------------
// Frontmatter name 同步
// ---------------------------------------------------------------------------

/**
 * 确保 SKILL.md 内容中 frontmatter 的 `name` 字段与最终目录名一致。
 *
 * 当 Agent 传入的 content 中 frontmatter name 与实际目录名不一致时，
 * 将 frontmatter 中的 name 同步为目录名，否则 list 显示的名字和
 * findSkill 按目录名匹配的名字不一致，导致后续 view/patch/edit 找不到技能。
 */
function syncFrontmatterName(content: string, expectedName: string): string {
  const fm = parseFrontmatter(content);
  if (!fm || fm.name === expectedName) {
    // frontmatter 解析失败（后续 validateFrontmatter 会拦截）或 name 已一致
    return content;
  }

  // 仅在 frontmatter 区块内替换 name 行，避免误改 body 中的同名行。
  // frontmatter 位于首个 `---` 和第二个 `\n---\n` 之间。
  const closingMatch = content.slice(3).match(/\n---\s*\n/);
  if (!closingMatch || closingMatch.index === undefined) {
    return content;
  }
  const fmEndOffset = 3 + closingMatch.index; // frontmatter 文本结束位置（不含 \n---\n）
  const fmSection = content.slice(0, fmEndOffset);
  const rest = content.slice(fmEndOffset);

  // 替换 frontmatter 中的 name 行
  const updatedFm = fmSection.replace(/^name\s*:.*$/m, `name: ${expectedName}`);
  return updatedFm + rest;
}

// ---------------------------------------------------------------------------
// 安全扫描辅助逻辑
// ---------------------------------------------------------------------------

/**
 * 对沉淀技能目录执行静态安全扫描并应用 install policy。
 *
 * 策略说明：
 * - sediment 与 sediment-active 都按 "agent-created" 信任级别扫描——
 *   sediment-active 虽然已经 release 到 skills/，但内容仍然由 review subagent
 *   自动产出，没有人工二次审核，因此延续最严策略；不放宽是为了避免"先 release
 *   再 patch 注入恶意"的绕过。如果未来要降级，应同时引入"二次人工签发"机制。
 * - 扫描器异常不再静默吞掉：会通过 onScanError 回调上报（见 P-K），
 *   避免 fail-closed 安全策略悄无声息地降级为 fail-open。
 */
function securityScanSkill(
  skillDir: string,
  opts: {
    location: "sediment" | "skills";
    onScanError?: (err: unknown) => void;
  },
): string | undefined {
  try {
    // 当前对两类位置使用同一信任级别；保留 location 参数是为了未来分级扩展时
    // 不需要再改函数签名（同时让调用方读起来更清楚扫的是哪种技能）。
    void opts.location;
    const result = scanSkill(skillDir, "agent-created");
    const [allowed, reason] = shouldAllowInstall(result);

    if (allowed === false) {
      const report = formatScanReport(result);
      return `Security scan blocked this skill (${reason}):\n${report}`;
    }
    if (allowed === null) {
      // "ask" 判定：对于 agent-created 技能，按阻断处理并返回报告
      const report = formatScanReport(result);
      return `Security scan blocked this skill (${reason}):\n${report}`;
    }
  } catch (err) {
    // 扫描器自身异常不应导致 fail-open（写动作未经扫描就放行）。
    // 通过回调上报，让调用层用 logger.warn 或 metric 记录；
    // 同时返回错误串拒绝写入，宁可"误拒"也不"漏审"。
    opts.onScanError?.(err);
    return `Security scan failed unexpectedly and the write was refused as a precaution: ${String(err)}`;
  }
  return undefined;
}

// ---------------------------------------------------------------------------
// 元数据辅助逻辑
// ---------------------------------------------------------------------------

/**
 * 更新元数据。修改细节与 starter 透传字段被分离到两个文件：
 *
 *  1. `__skill_meta__.json`（{@link SkillMeta}）—— starter 写入并透传给前端 / 平台 API。
 *     本插件**只接力刷新 `installedAt`**，让平台 listSkills 能感知"刚被 review
 *     subagent 改过"；其它字段全部沿用 `...existing` 原样透传，避免擦除 starter 在
 *     启用迁移阶段写入的 source / originSource / id / code / enname 等平台路由字段。
 *     注意：旧版本曾把 createdAt / updatedAt / lastAction / revisionCount / editHistory
 *     也写在这里，新实现不再写入；老数据由 {@link readSedimentMeta} 在首次读取时
 *     自动迁移并从老文件中剥离。
 *
 *  2. `__sediment_meta__.json`（{@link SedimentMeta}）—— 本插件私有的修改细节。
 *     starter 不感知、不读、不透传。这是出于两点考虑：
 *      - 避免无用信息扩散：editHistory 等字段对前端无意义，无谓增大透传 payload。
 *      - 避免数据泄露：修改预览（patch 的 old/new 字符串）可能含敏感内容，不该
 *        随平台接口外泄。
 */
function updateMeta(
  skillDir: string,
  action: SkillMetaAction,
  summary?: string,
  parentSessionKey?: string,
): void {
  const now = new Date().toISOString();

  // ---- 1) 更新对外 __skill_meta__.json：仅刷新 installedAt，其余 starter 字段透传 ----
  const existingSkillMeta = readSkillMeta(skillDir);
  const skillMeta: SkillMeta = {
    ...existingSkillMeta,
    source: existingSkillMeta?.source ?? "LOCAL_GENERATED",
    installedAt: now,
  };
  writeSkillMeta(skillDir, skillMeta);

  // ---- 2) 更新私有 __sediment_meta__.json：本插件管理的修改细节 ----
  // readSedimentMeta 会做老文件兼容迁移，如果老 __skill_meta__.json 仍残留
  // createdAt 等旧字段，会被自动萃取并剥离，再返回 SedimentMeta。
  const existingSediment = readSedimentMeta(skillDir);

  const record: SkillEditRecord = { action, at: now };
  if (summary) {
    record.summary = summary;
  }
  // 保留全部历史，不做条数截断
  const prevHistory = existingSediment?.editHistory ?? [];
  const editHistory = [record, ...prevHistory];

  // createdInParentSession：出生证明语义
  // - 其它 action：保留 existingSediment.createdInParentSession 原值。
  let createdInParentSession = existingSediment?.createdInParentSession;
  if (parentSessionKey) {
    if (action === "create") {
      createdInParentSession = parentSessionKey;
    } else if (
      createdInParentSession === undefined &&
      (action === "edit" ||
        action === "patch" ||
        action === "write_file" ||
        action === "remove_file")
    ) {
      createdInParentSession = parentSessionKey;
    }
  }

  const sedimentMeta: SedimentMeta = {
    // 保留 promote 路径写入的 promotedAt/By/Reason、reviewMatchedCount 等
    // 长期字段，避免本次写动作把它们静默擦除。
    ...existingSediment,
    createdAt: existingSediment?.createdAt ?? now,
    updatedAt: now,
    // lastTouchedAt 是 TTL/LRU 回收的排序键：任何写动作都顺手刷一次，让活跃 sediment 自然延寿，死沉淀自然落到队尾被回收。
    lastTouchedAt: now,
    lastAction: action,
    revisionCount: (existingSediment?.revisionCount ?? 0) + 1,
    editHistory,
    // 显式赋值（即便等于 existing，也透传 spread 后的值），保证 undefined 不会把 spread 已有的字段覆盖掉。
    ...(createdInParentSession !== undefined ? { createdInParentSession } : {}),
  };
  writeSedimentMeta(skillDir, sedimentMeta);
}

// ---------------------------------------------------------------------------
// 核心动作实现
// ---------------------------------------------------------------------------

/**
 * skill_manage 的目录上下文：
 * - `sedimentDir`：所有写动作的主基目录（`<agent workspace>/sediment_skills`），
 *   与 skills/ 同级。OpenClaw 核心引擎不会扫描此目录。
 *   注意：sediment-active 技能（已 release 到 skills/，但 originSource === "SEDIMENT"）
 *   也会被本插件原地修改在 skills/ 下；路径展示时按所在目录分别相对化
 *   （见 displayBase 用法）。
 * - `skillsDir`：可选，仅用于 list/view 等只读动作的全量扫描以及 sediment-active
 *   技能的查找；省略时退化为只看沉淀目录。
 * - `onScanError`：安全扫描器自身抛错时的回调（见 P-K）。调用方应在此输出
 *   logger.warn 或上报 metric，避免扫描故障被静默吞掉。
 */
export interface SkillDirs {
  sedimentDir: string;
  skillsDir?: string;
  onScanError?: (err: unknown) => void;
  /**关键失败回调：promote 物理迁移进入"无法自洽回滚"的脏状态时触发。*/
  onCriticalError?: (msg: string) => void;
  /**
   * 当前会话的 agentId。
   */
  agentId?: string;
  /**
   * 当前 skill_manage 调用所属 review subagent 的**父会话** sessionKey。
   *  1. `createSkill` → 透传到 `updateMeta`，在 sediment 创建时把 parentSessionKey
   *     写入 `__sediment_meta__.json.createdInParentSession`（出生证明）。
   *  2. `promoteSkill` → 与 sediment 的 `createdInParentSession` 比较，
   *     实施"跨父会话守卫"：同一父会话内禁止 self-promote。
   */
  parentSessionKey?: string;
  /** promote 的"时间成熟期"（单位：天）。*/
  promoteMaturationDays?: number;
}

const DEFAULT_PROMOTE_MATURATION_DAYS = 1;

function createSkill(name: string, content: string, dirs: SkillDirs): SkillManageResult {
  let err = validateName(name);
  if (err) {
    return { success: false, error: err };
  }

  err = validateFrontmatter(content);
  if (err) {
    return { success: false, error: err };
  }

  err = validateContentSize(content);
  if (err) {
    return { success: false, error: err };
  }

  // 同步 frontmatter 中的 name 字段与最终目录名一致（防止 list/findSkill 名字不一致）。
  content = syncFrontmatterName(content, name);
  // 把 description 块标量（>- / |- 等）折叠成单行 single-quoted，保持磁盘格式干净。
  content = normalizeFrontmatterDescription(content);

  // 重名冲突检查：
  //  1. 沉淀目录（sedimentDir）内同名 → 拒绝（本插件操作范围内的真重名）
  //  2. skills/ 下同名：
  //     - originSource === "SEDIMENT" → 已 release 的沉淀技能（sediment-active），建议用 edit/patch
  //     - 其它来源（native/official/seal）→ 跨域重名，建议改名以免日后启用迁移失败
  //  注：create 本身只往 sedimentDir 落盘，跨目录检查仅做"防呆提示"，
  //      并不代表本插件去管理 skills/ 下的非沉淀技能。
  const existing = findSkill(name, dirs.sedimentDir);
  if (existing) {
    return {
      success: false,
      error: `A skill named '${name}' already exists at ${existing}.`,
      hint: `Use action='view' to inspect it, then action='patch' or action='edit' to update.`,
    };
  }
  if (dirs.skillsDir) {
    const inSkills = findSkill(name, dirs.skillsDir);
    if (inSkills) {
      if (isSedimentOrigin(inSkills)) {
        return {
          success: false,
          error:
            `A sediment-active skill named '${name}' already exists at ${inSkills}. ` +
            `It was previously released from sediment_skills/ and is still managed by this plugin.`,
          hint: `Use action='view' to inspect it, then action='patch' or action='edit' to update.`,
        };
      }
      return {
        success: false,
        error:
          `A skill named '${name}' already exists at ${inSkills} ` +
          `(not of sediment origin — managed by another source: native/official/seal). ` +
          `Creating a sediment skill with the same name would conflict on enable-migration.`,
        hint: `Choose a different name for your sediment skill.`,
      };
    }
  }

  // [Opt-6] 模糊去重检查：描述词袋重叠 ≥ 0.7
  // 在 skillsDir 全量扫描（含原生 skill），让 agent 知道是否已有相似的官方技能可用。
  // 同时扫描 sedimentDir，避免在同一隔离目录下创建重复沉淀技能。
  const fm = parseFrontmatter(content);
  const newDesc = fm?.description ?? "";
  const similarScanRoot = dirs.skillsDir ?? dirs.sedimentDir;
  let similarSkills = findSimilarSkills(name, newDesc, similarScanRoot);
  // 如果 skillsDir 和 sedimentDir 不同，额外扫描沉淀目录
  if (dirs.sedimentDir !== similarScanRoot) {
    similarSkills = similarSkills.concat(findSimilarSkills(name, newDesc, dirs.sedimentDir));
  }
  if (similarSkills.length > 0) {
    const suggestions = similarSkills
      .map((s) => {
        return `  - '${s.name}' (desc similarity: ${(s.descSimilarity * 100).toFixed(0)}%)`;
      })
      .join("\n");
    return {
      success: false,
      error: `Found similar existing skill(s) — consider updating instead of creating a duplicate:\n${suggestions}`,
      hint:
        `Use action='view' to inspect the existing skill, ` +
        `then action='patch' or action='edit' to update it. ` +
        `If you're sure this is a distinct skill, rewrite the description to reduce overlap.`,
    };
  }

  // 创建技能目录（位于 sedimentDir 下）。create 动作仅允许落到沉淀目录。
  const skillDir = resolveSkillDir(dirs.sedimentDir, name);
  fs.mkdirSync(path.dirname(skillDir), { recursive: true });
  try {
    fs.mkdirSync(skillDir);
  } catch (mkErr) {
    if ((mkErr as NodeJS.ErrnoException).code === "EEXIST") {
      return {
        success: false,
        error:
          `Race detected: skill '${name}' was just created by a concurrent operation ` +
          `(directory appeared between the duplicate-check and mkdir steps).`,
        hint: `Re-run action='list' to refresh, then use action='view' / 'edit' / 'patch' on the existing skill.`,
      };
    }
    throw mkErr;
  }

  // 原子写入 SKILL.md
  const skillMd = path.join(skillDir, "SKILL.md");
  atomicWriteText(skillMd, content);

  // 安全扫描：若被拦截则回滚
  // create 永远落在 sediment_skills/ → location: "sediment"
  const scanError = securityScanSkill(skillDir, {
    location: "sediment",
    onScanError: dirs.onScanError,
  });
  if (scanError) {
    fs.rmSync(skillDir, { recursive: true, force: true });
    return { success: false, error: scanError };
  }

  // 写入元数据（附带完整 description）
  const descPreview = fm?.description ? `: ${fm.description}` : "";
  updateMeta(skillDir, "create", `created skill '${name}'${descPreview}`, dirs.parentSessionKey);

  // 路径展示：相对于技能所在目录展示，避免 sediment_skills 下技能出现 "../" 前缀
  const displayBase = dirs.sedimentDir;
  const result: SkillManageResult = {
    success: true,
    message: `Skill '${name}' created.`,
    path: path.relative(displayBase, skillDir),
    skill_md: skillMd,
  };
  result.hint =
    `To add reference files, templates, or scripts, use ` +
    `skill_manage(action='write_file', name='${name}', file_path='references/example.md', file_content='...')`;

  return result;
}

/**
 * 写动作的统一前置校验：定位"本插件可写"的技能并应用 defense-in-depth 守卫。
 *
 * 可写性判定（满足任一即可写）：
 * 1. 路径在 `dirs.sedimentDir`（<workspace>/sediment_skills/）下——沉淀阶段、未启用
 * 2. 路径在 `dirs.skillsDir`（<workspace>/skills/）下，且 meta `originSource === "SEDIMENT"`
 *    ——已被 starter 的 enable_seal_skill 接口启用迁移过来的"沉淀血统"技能
 *
 * 关键安全保证：
 * - 先在 sedimentDir 查找；命中即按沉淀路径处理
 * - 未命中时再在 skillsDir 查找，必须满足 `originSource === "SEDIMENT"` 才放行
 *   原生/官方/seal 来源的技能 originSource ≠ "SEDIMENT"（或缺失），一律拒绝
 * - `isOfficialSkill` 兜底：source === "OFFICIAL" 永远拒绝（防御 meta 被篡改）
 *
 * @returns 命中时返回 { ok: true, skillDir, location }，location 标记技能位置便于调用方决策
 */
function locateSedimentSkill(
  name: string,
  dirs: SkillDirs,
):
  | { ok: true; skillDir: string; location: "sediment" | "skills" }
  | { ok: false; result: SkillManageResult } {
  // [Phase 1] 先在沉淀目录查找
  let existing = findSkill(name, dirs.sedimentDir);
  let location: "sediment" | "skills" = "sediment";

  // [Phase 2] 沉淀目录没命中，且配置了 skillsDir，则在已启用目录查找
  if (!existing && dirs.skillsDir) {
    const inSkills = findSkill(name, dirs.skillsDir);
    if (inSkills && isLocalSkill(inSkills, dirs.skillsDir)) {
      // 关键权限校验：必须 originSource === "SEDIMENT" 才允许操作
      if (!isSedimentOrigin(inSkills)) {
        return {
          ok: false,
          result: {
            success: false,
            error:
              `Skill '${name}' exists in the skills directory but is not of sediment origin ` +
              `(originSource ≠ "SEDIMENT"). ` +
              `This plugin only manages sediment skills (in sediment_skills/) and ` +
              `sediment-originated skills already enabled into skills/. ` +
              `Use action='view' to read it.`,
          },
        };
      }
      existing = inSkills;
      location = "skills";
    }
  }

  if (!existing) {
    return {
      ok: false,
      result: {
        success: false,
        error:
          `Sediment skill '${name}' not found. ` +
          `This plugin can only modify skills under sediment_skills/ ` +
          `or sediment-originated skills (originSource="SEDIMENT") under skills/. ` +
          `Use skill_manage(action='list') to see available sediment skills, ` +
          `or action='create' to add a new one.`,
      },
    };
  }

  // 防御：路径必须确实位于其声称的根目录内（symlink 防护）
  const expectedRoot = location === "sediment" ? dirs.sedimentDir : dirs.skillsDir!;
  if (!isLocalSkill(existing, expectedRoot)) {
    return {
      ok: false,
      result: {
        success: false,
        error: `Skill '${name}' resolved outside the expected directory and cannot be modified.`,
      },
    };
  }

  // OFFICIAL 兜底拒绝
  if (isOfficialSkill(existing)) {
    return {
      ok: false,
      result: {
        success: false,
        error: `Skill '${name}' is marked as OFFICIAL and cannot be modified. Use action='view' to read it.`,
      },
    };
  }

  return { ok: true, skillDir: existing, location };
}

function editSkill(name: string, content: string, dirs: SkillDirs): SkillManageResult {
  // 与 createSkill 对齐：先做名称合法性校验，避免后续依赖 locateSedimentSkill 返回
  // 模糊的 "not found" 错误，且防止非法字符在路径拼接前流入。
  let err = validateName(name);
  if (err) {
    return { success: false, error: err };
  }

  err = validateFrontmatter(content);
  if (err) {
    return { success: false, error: err };
  }

  err = validateContentSize(content);
  if (err) {
    return { success: false, error: err };
  }

  const located = locateSedimentSkill(name, dirs);
  if (!located.ok) {
    return located.result;
  }
  const existing = located.skillDir;

  // 同步 frontmatter 中的 name 字段与目录名一致（与 createSkill 行为对齐）。
  // 全量重写时如果传入内容里 frontmatter.name 与目录名不一致，会导致
  // list/findSkill/去重检查等依赖 frontmatter.name 的功能与磁盘目录名脱节。
  content = syncFrontmatterName(content, name);
  // 把 description 块标量（>- / |- 等）折叠成单行 single-quoted，与 create 对齐。
  content = normalizeFrontmatterDescription(content);

  const skillMd = path.join(existing, "SKILL.md");

  // 先备份，便于回滚
  let originalContent: string | undefined;
  try {
    originalContent = fs.readFileSync(skillMd, "utf-8");
  } catch {
    // 原文件不存在，无需备份
  }

  atomicWriteText(skillMd, content);

  // 安全扫描：若被拦截则回滚
  const scanError = securityScanSkill(existing, {
    location: located.location,
    onScanError: dirs.onScanError,
  });
  if (scanError) {
    if (originalContent !== undefined) {
      atomicWriteText(skillMd, originalContent);
    }
    return { success: false, error: scanError };
  }

  // 附带完整新内容（跳过 frontmatter，保留正文全文与原始换行）
  const editBodyStart = content.indexOf("\n---\n");
  const editBody = editBodyStart >= 0 ? content.slice(editBodyStart + 5).trim() : content;
  // 透传 parentSessionKey：让 updateMeta 在原戳缺失时补打 createdInParentSession，
  // 配合 promoteSkill 的 fail-closed 守卫，避免老 sediment 永远无法 promote 的死循环。
  updateMeta(
    existing,
    "edit",
    `full rewrite (${content.length} chars): ${editBody}`,
    dirs.parentSessionKey,
  );

  // 路径展示：sediment 在 sedimentDir 下、sediment-active 在 skillsDir 下，
  // 分别相对各自根计算，避免出现 "../skills/..." 的别扭前缀。
  const displayBase =
    located.location === "sediment" ? dirs.sedimentDir : (dirs.skillsDir ?? dirs.sedimentDir);
  return {
    success: true,
    message: `Skill '${name}' updated.`,
    path: path.relative(displayBase, existing),
  };
}

function patchSkill(
  name: string,
  oldString: string,
  newString: string,
  dirs: SkillDirs,
  filePath?: string,
  replaceAll = false,
): SkillManageResult {
  if (!oldString) {
    return { success: false, error: "old_string is required for 'patch'." };
  }
  if (newString === undefined || newString === null) {
    return {
      success: false,
      error: "new_string is required for 'patch'. Use an empty string to delete matched text.",
    };
  }

  const located = locateSedimentSkill(name, dirs);
  if (!located.ok) {
    return located.result;
  }
  const existing = located.skillDir;

  let target: string;

  if (filePath) {
    const fileErr = validateFilePath(filePath);
    if (fileErr) {
      return { success: false, error: fileErr };
    }
    target = path.join(existing, filePath);
    const withinErr = validateWithinDir(target, existing);
    if (withinErr) {
      return { success: false, error: withinErr };
    }
  } else {
    target = path.join(existing, "SKILL.md");
  }

  if (!fs.existsSync(target)) {
    return {
      success: false,
      error: `File not found: ${path.relative(existing, target)}`,
    };
  }

  const content = fs.readFileSync(target, "utf-8");

  // 简单查找替换（不做模糊匹配，保持行为可预期）
  const occurrences = content.split(oldString).length - 1;

  if (occurrences === 0) {
    const preview = content.slice(0, 500) + (content.length > 500 ? "..." : "");
    return {
      success: false,
      error: `old_string not found in ${filePath ?? "SKILL.md"}. Ensure the text matches exactly.`,
      file_preview: preview,
    };
  }

  if (occurrences > 1 && !replaceAll) {
    return {
      success: false,
      error:
        `Found ${occurrences} occurrences of old_string. ` +
        "Set replace_all=true to replace all, or provide more context to make the match unique.",
    };
  }

  const newContent = replaceAll
    ? content.split(oldString).join(newString)
    : content.replace(oldString, newString);

  // 校验内容大小限制
  const targetLabel = filePath ?? "SKILL.md";
  const sizeErr = validateContentSize(newContent, targetLabel);
  if (sizeErr) {
    return { success: false, error: sizeErr };
  }

  // 若 patch 的是 SKILL.md，需要确保 frontmatter 结构仍合法
  if (!filePath) {
    const fmErr = validateFrontmatter(newContent);
    if (fmErr) {
      return {
        success: false,
        error: `Patch would break SKILL.md structure: ${fmErr}`,
      };
    }
  }

  const originalContent = content;
  atomicWriteText(target, newContent);

  // 安全扫描：若被拦截则回滚
  const scanError = securityScanSkill(existing, {
    location: located.location,
    onScanError: dirs.onScanError,
  });
  if (scanError) {
    atomicWriteText(target, originalContent);
    return { success: false, error: scanError };
  }

  const matchCount = replaceAll ? occurrences : 1;
  // 附带完整 old → new 变更内容（保留原始换行，不做长度截断）
  // 透传 parentSessionKey
  updateMeta(
    existing,
    "patch",
    `patched ${targetLabel} (${matchCount} replacement${matchCount > 1 ? "s" : ""}): "${oldString}" → "${newString}"`,
    dirs.parentSessionKey,
  );

  return {
    success: true,
    message: `Patched ${targetLabel} in skill '${name}' (${matchCount} replacement${matchCount > 1 ? "s" : ""}).`,
  };
}

function deleteSkill(name: string, dirs: SkillDirs): SkillManageResult {
  const located = locateSedimentSkill(name, dirs);
  if (!located.ok) {
    return located.result;
  }
  const existing = located.skillDir;

  // sediment-active 技能（已迁移到 skills/ 的沉淀血统技能）视为"已 release"，
  // 不允许从本插件 delete；如需移除，请走 starter 的 disable 流程。
  // 仅允许删除仍在沉淀目录（sediment_skills/）下的技能。
  if (located.location === "skills") {
    return {
      success: false,
      error:
        `Skill '${name}' has been activated (located in skills/) and cannot be deleted by this tool. ` +
        "Use the starter disable flow to remove an activated sediment skill.",
    };
  }

  fs.rmSync(existing, { recursive: true, force: true });

  // 清理空的分类目录（仅在沉淀目录下做）
  const parent = path.dirname(existing);
  if (parent !== dirs.sedimentDir && fs.existsSync(parent)) {
    try {
      const remaining = fs.readdirSync(parent);
      if (remaining.length === 0) {
        fs.rmdirSync(parent);
      }
    } catch {
      // 忽略清理过程中的错误
    }
  }

  return {
    success: true,
    message: `Skill '${name}' deleted.`,
  };
}

/**
 * 将一条沉淀技能从 sediment_skills/ 升级（promote）到 skills/，
 * 写入与 starter `moveSealSkillToSkills()` 等价的 `__skill_meta__.json`，
 * 让 OpenClaw 核心引擎从下一次会话起自动加载该技能。
 *
 */
function promoteSkill(name: string, reason: string, dirs: SkillDirs): SkillManageResult {
  // ---- 1) 名称合法性 ----
  const nameErr = validateName(name);
  if (nameErr) {
    return { success: false, error: nameErr };
  }

  // ---- 2) 必须配置 skillsDir ----
  if (!dirs.skillsDir) {
    return {
      success: false,
      error:
        "promote requires skillsDir to be configured. " +
        "This action moves a sediment skill into the engine-loaded skills directory.",
    };
  }

  // ---- 3) 必须在 sediment_skills/ 下命中 ----
  const sourceDir = findSkill(name, dirs.sedimentDir);
  if (!sourceDir || !isLocalSkill(sourceDir, dirs.sedimentDir)) {
    // 给出更精确的错误：是不是已经 promote 过了（sediment-active）？
    if (dirs.skillsDir) {
      const maybeActive = findSkill(name, dirs.skillsDir);
      if (maybeActive && isSedimentOrigin(maybeActive)) {
        return {
          success: false,
          error:
            `Skill '${name}' has already been promoted (originSource="SEDIMENT" in skills/). ` +
            `Use action='edit' or action='patch' to update it instead.`,
        };
      }
      if (maybeActive) {
        return {
          success: false,
          error:
            `A skill named '${name}' already exists in skills/ but is not of sediment origin. ` +
            `Cannot promote.`,
        };
      }
    }
    return {
      success: false,
      error:
        `Sediment skill '${name}' not found under sediment_skills/. ` +
        `Use action='list' to see promotable sediment skills.`,
    };
  }

  // ---- 4) 目标不能已存在 ----
  const targetDir = path.join(dirs.skillsDir, name);
  if (fs.existsSync(targetDir)) {
    return {
      success: false,
      error:
        `Target skills/${name} already exists and would be overwritten. ` +
        `Refusing to promote to avoid clobbering an existing skill.`,
    };
  }

  // ---- 5) 升级前再扫一次安全 ----
  const scanError = securityScanSkill(sourceDir, {
    location: "sediment",
    onScanError: dirs.onScanError,
  });
  if (scanError) {
    return { success: false, error: scanError };
  }

  // ---- 6) 二次命中守卫：两条独立验证路径，任一通过即放行 ----
  //
  //   路径 A（跨父会话）：sediment 的出生证明存在，且不等于当前 parentSessionKey。
  //                      需要 parentSessionKey 存在才能判定。
  //   路径 B（时间成熟）：sediment 距 createdAt 已超过 promoteMaturationDays（默认 1 天）。
  //                      不依赖 parentSessionKey，独立判定。
  const sedimentMeta = readSedimentMeta(sourceDir);
  const createdInParent = sedimentMeta?.createdInParentSession;

  // 路径 A：跨父会话验证（需要 parentSessionKey 存在才能判定）
  const passedCrossSession =
    !!dirs.parentSessionKey &&
    createdInParent !== undefined &&
    createdInParent !== dirs.parentSessionKey;

  // 路径 B：时间成熟验证（不依赖 parentSessionKey）
  const maturationDays = dirs.promoteMaturationDays ?? DEFAULT_PROMOTE_MATURATION_DAYS;
  const createdAtMs = sedimentMeta?.createdAt ? Date.parse(sedimentMeta.createdAt) : NaN;
  // maturationDays=0 显式关闭时间路径；createdAt 缺失或解析失败时也不放行（避免 NaN 比较返回 true 假阳性）。
  const ageDays =
    Number.isFinite(createdAtMs) && createdAtMs > 0 ? (Date.now() - createdAtMs) / 86_400_000 : NaN;
  const passedMaturation =
    maturationDays > 0 && Number.isFinite(ageDays) && ageDays >= maturationDays;

  if (!passedCrossSession && !passedMaturation) {
    // 失败原因分类，方便给出对症 hint
    const ageDesc = Number.isFinite(ageDays)
      ? `${ageDays.toFixed(1)} day(s) old`
      : `unknown age (no valid createdAt in sediment meta)`;
    const maturationDesc =
      maturationDays > 0
        ? `requires ${maturationDays} day(s)`
        : `time-maturation path is disabled (promoteMaturationDays=0)`;

    // parentSessionKey 缺失：路径 A 无法判定，路径 B 也未通过
    if (!dirs.parentSessionKey) {
      return {
        success: false,
        error:
          `Cannot promote skill '${name}': the current review subagent's parent session ` +
          `is unknown (activeReviews lookup failed), so cross-session verification is impossible; ` +
          `and the sediment is not yet mature (${ageDesc}, ${maturationDesc}).`,
        hint:
          `Two ways to unlock promote:\n` +
          `  (A) Cross-session: retry when the parent session identity is available.\n` +
          `  (B) Time-based: wait until the sediment is at least ${maturationDays} day(s) old ` +
          `(createdAt=${sedimentMeta?.createdAt ?? "unknown"}).`,
        rejectionTag: "SECOND_HIT_REJECTED:no-parent-session",
      };
    }

    if (createdInParent === undefined) {
      // 老 sediment 缺出生证明，且尚未成熟 —— 这种情况现在很少见
      // （老数据一般 createdAt 都很久远），但理论上仍可能出现。
      return {
        success: false,
        error:
          `Cannot promote skill '${name}': it lacks the 'createdInParentSession' marker ` +
          `(legacy sediment) and is not yet mature (${ageDesc}, ${maturationDesc}). ` +
          `Cross-task reusability cannot be verified — refusing to promote.`,
        hint:
          `Either wait for the sediment to mature (createdAt + ${maturationDays} day(s)), ` +
          `or have a different parent conversation match it via the second-hit path. ` +
          `Refining via 'edit' in THIS conversation will only re-stamp 'createdInParentSession' ` +
          `to the current parent — it will not unlock promote.`,
        rejectionTag: "SECOND_HIT_REJECTED:legacy-not-mature",
      };
    }

    // 已有出生证明、且等于当前 parentSessionKey、且尚未成熟 —— 经典 self-validation 拒绝场景
    return {
      success: false,
      error:
        `Cannot promote skill '${name}': it was CREATED in this very same parent session ` +
        `(parentSessionKey="${dirs.parentSessionKey}") and has not reached the ` +
        `maturation period yet (${ageDesc}, ${maturationDesc}). ` +
        `promote requires either a SECOND hit from a DIFFERENT parent session, ` +
        `or the sediment to mature over time (whichever comes first).`,
      hint:
        `Two ways to unlock promote:\n` +
        `  (A) Cross-session: a FUTURE review subagent in a DIFFERENT parent conversation ` +
        `independently matches this sediment against a new task.\n` +
        `  (B) Time-based: wait until the sediment is at least ${maturationDays} day(s) old ` +
        `(createdAt=${sedimentMeta?.createdAt ?? "unknown"}), then a re-match in any session can promote.\n` +
        `Refining via 'patch' / 'edit' in THIS conversation does NOT advance either path. ` +
        `Stop trying to promote in this review; output 'Nothing to save.' instead.`,
      rejectionTag: "SECOND_HIT_REJECTED:same-parent-not-mature",
    };
  }

  // ---- 7) 物理迁移 + 写双 meta ----
  try {
    const moved = promoteSedimentSkill(dirs.sedimentDir, dirs.skillsDir, name, {
      by: "auto",
      reason,
      agentId: dirs.agentId,
      // 透传关键失败回调：在双残留等需人工介入的脏状态下，让上层 logger.error 抓到。
      onCriticalError: dirs.onCriticalError,
    });
    return {
      success: true,
      message:
        `Skill '${name}' promoted from sediment_skills/ to skills/ ` +
        `at ${moved.promotedAt}. It will be loaded by the engine on next session.`,
      path: path.relative(dirs.skillsDir, moved.to),
      hint:
        `Future updates can still be made via action='edit' or action='patch'; ` +
        `originSource is set to "SEDIMENT" so this plugin retains write access.`,
    };
  } catch (err) {
    return {
      success: false,
      error: `Failed to promote skill '${name}': ${err instanceof Error ? err.message : String(err)}`,
    };
  }
}

function writeFile(
  name: string,
  filePath: string,
  fileContent: string,
  dirs: SkillDirs,
): SkillManageResult {
  const filePathErr = validateFilePath(filePath);
  if (filePathErr) {
    return { success: false, error: filePathErr };
  }

  if (fileContent === undefined || fileContent === null) {
    return { success: false, error: "file_content is required." };
  }

  // 校验大小限制
  const sizeErr = validateFileSize(fileContent);
  if (sizeErr) {
    return { success: false, error: sizeErr };
  }
  const contentSizeErr = validateContentSize(fileContent, filePath);
  if (contentSizeErr) {
    return { success: false, error: contentSizeErr };
  }

  const located = locateSedimentSkill(name, dirs);
  if (!located.ok) {
    return located.result;
  }
  const existing = located.skillDir;

  const target = path.join(existing, filePath);
  const withinErr = validateWithinDir(target, existing);
  if (withinErr) {
    return { success: false, error: withinErr };
  }

  fs.mkdirSync(path.dirname(target), { recursive: true });

  // 先备份，便于回滚
  let originalContent: string | undefined;
  try {
    originalContent = fs.readFileSync(target, "utf-8");
  } catch {
    // 原文件不存在
  }

  atomicWriteText(target, fileContent);

  // 安全扫描：若被拦截则回滚
  const scanError = securityScanSkill(existing, {
    location: located.location,
    onScanError: dirs.onScanError,
  });
  if (scanError) {
    if (originalContent !== undefined) {
      atomicWriteText(target, originalContent);
    } else {
      try {
        fs.unlinkSync(target);
      } catch {
        // 忽略删除失败
      }
    }
    return { success: false, error: scanError };
  }

  // 透传 parentSessionKey
  updateMeta(
    existing,
    "write_file",
    `wrote '${filePath}' (${fileContent.length} chars)`,
    dirs.parentSessionKey,
  );

  // 路径展示：与 editSkill 对齐——sediment 在 sedimentDir，sediment-active 在 skillsDir。
  const displayBase =
    located.location === "sediment" ? dirs.sedimentDir : (dirs.skillsDir ?? dirs.sedimentDir);
  return {
    success: true,
    message: `File '${filePath}' written to skill '${name}'.`,
    path: path.relative(displayBase, target),
  };
}

function removeFile(name: string, filePath: string, dirs: SkillDirs): SkillManageResult {
  const filePathErr = validateFilePath(filePath);
  if (filePathErr) {
    return { success: false, error: filePathErr };
  }

  const located = locateSedimentSkill(name, dirs);
  if (!located.ok) {
    return located.result;
  }
  const existing = located.skillDir;

  const target = path.join(existing, filePath);
  const withinErr = validateWithinDir(target, existing);
  if (withinErr) {
    return { success: false, error: withinErr };
  }

  if (!fs.existsSync(target)) {
    const available = listSkillFiles(existing);
    return {
      success: false,
      error: `File '${filePath}' not found in skill '${name}'.`,
      available_files: available.length > 0 ? available : undefined,
    };
  }

  fs.unlinkSync(target);

  // 清理空的子目录
  const parent = path.dirname(target);
  if (parent !== existing && fs.existsSync(parent)) {
    try {
      const remaining = fs.readdirSync(parent);
      if (remaining.length === 0) {
        fs.rmdirSync(parent);
      }
    } catch {
      // 忽略清理错误
    }
  }

  // 透传 parentSessionKey
  updateMeta(existing, "remove_file", `removed '${filePath}'`, dirs.parentSessionKey);

  return {
    success: true,
    message: `File '${filePath}' removed from skill '${name}'.`,
  };
}

// ---------------------------------------------------------------------------
// 只读动作：view / list
// ---------------------------------------------------------------------------

/**
 * 查看指定技能的完整 SKILL.md 内容。
 */
function viewSkill(name: string, dirs: SkillDirs): SkillManageResult {
  // 搜索顺序与 locateSedimentSkill 对齐：先 sediment_skills/ 后 skills/。
  // 防止"两边同时存在"（如 starter 启用迁移失败导致残留）时，view 看到的
  // 文件与 patch/edit 改到的文件不是同一份。
  let existing = findSkill(name, dirs.sedimentDir);
  if (!existing && dirs.skillsDir && dirs.skillsDir !== dirs.sedimentDir) {
    existing = findSkill(name, dirs.skillsDir);
  }
  if (!existing) {
    return { success: false, error: `Skill '${name}' not found.` };
  }

  const skillMd = path.join(existing, "SKILL.md");
  if (!fs.existsSync(skillMd)) {
    return { success: false, error: `Skill '${name}' exists but has no SKILL.md file.` };
  }

  const content = fs.readFileSync(skillMd, "utf-8");
  const files = listSkillFiles(existing);
  // starter 透传字段（source / originSource）从 __skill_meta__.json 读
  const meta = readSkillMeta(existing);
  // 修订/最近动作/更新时间是本插件私有字段，从 __sediment_meta__.json 读
  const sediment = readSedimentMeta(existing);
  const source = meta?.source;
  const isOfficial = source === "OFFICIAL";
  const inSediment = isLocalSkill(existing, dirs.sedimentDir);
  const isSedimentActivated = !inSediment && !isOfficial && meta?.originSource === "SEDIMENT";

  // 计算 location（语义与 listSkills 保持一致），同时驱动展示标签和返回字段
  //  - OFFICIAL          → 只读
  //  - sediment          → 物理位于 sediment_skills/，可写
  //  - sediment-active   → 已迁移到 skills/，但 originSource === SEDIMENT，仍可写
  //  - native            → skills/ 下其它来源，只读
  const location: SkillLocation = isOfficial
    ? "official"
    : inSediment
      ? "sediment"
      : isSedimentActivated
        ? "sediment-active"
        : "native";

  const metaParts: string[] = [];
  switch (location) {
    case "official":
      metaParts.push("[OFFICIAL — read-only]");
      break;
    case "sediment":
      metaParts.push("[sediment — editable]");
      break;
    case "sediment-active":
      metaParts.push("[sediment-active — editable]");
      break;
    case "native":
      metaParts.push("[native — read-only]");
      break;
  }
  if (sediment?.revisionCount != null) {
    metaParts.push(`revisions: ${sediment.revisionCount}`);
  }
  if (sediment?.lastAction) {
    metaParts.push(`last action: ${sediment.lastAction}`);
  }
  if (sediment?.updatedAt) {
    metaParts.push(`updated: ${sediment.updatedAt}`);
  }

  // 仅当 view 命中的是 [sediment] 时刷新 lastTouchedAt：
  // - 这是 LRU 回收的活跃度信号——被 review subagent 主动 view 即视为"有兴趣"
  // - sediment-active / native / official 由原 updateMeta 路径或外部管理，不在此处刷
  // - best-effort：写失败不影响 view 返回；下次 view/写动作会再次尝试
  if (location === "sediment" && sediment) {
    try {
      const now = new Date().toISOString();
      writeSedimentMeta(existing, {
        ...sediment,
        // updatedAt 表示"修改时间"语义不变；lastTouchedAt 才是访问时间
        lastTouchedAt: now,
      });
    } catch {
      // 静默忽略；活跃度刷新失败不该让用户的 view 跟着失败
    }
  }
  const metaSuffix = metaParts.length > 0 ? ` (${metaParts.join(", ")})` : "";

  return {
    success: true,
    message: `Skill '${name}'${metaSuffix} content:`,
    path: existing,
    skill_content: content,
    source,
    location,
    available_files: files.length > 0 ? files : undefined,
  };
}

/**
 * 列出 skillsDir 和 sedimentDir 下的所有技能。
 *
 * 分别扫描 `dirs.skillsDir`（原生 + 官方技能）和 `dirs.sedimentDir`（沉淀技能），
 * 并在每条结果上打来源 tag：
 * - `[sediment]`：位于 `dirs.sedimentDir` 内，可被本插件修改
 * - `[OFFICIAL]`：metadata `source === "OFFICIAL"`，只读
 * - `[native]`：其余位置（用户/IDE/全局放进来的本地技能），本插件不会修改
 *
 * 由于 sedimentDir（<workspace>/sediment_skills）与 skillsDir（<workspace>/skills）同级，
 * 需要分别扫描两个目录。
 * 若未配置 `skillsDir`（极少见），只列出沉淀目录。
 */
function listSkills(dirs: SkillDirs): SkillManageResult {
  const skillsDir = dirs.skillsDir ?? dirs.sedimentDir;
  if (!fs.existsSync(skillsDir) && !fs.existsSync(dirs.sedimentDir)) {
    return {
      success: true,
      message: "No skills found (skills directory does not exist).",
      skills: [],
    };
  }

  const skills: Array<{
    name: string;
    description: string;
    path: string;
    source?: SkillSource | string;
    revisionCount?: number;
    /** 见 {@link SkillLocation}。 */
    location: SkillLocation;
  }> = [];

  // 路径展示：相对于各扫描根展示，避免 sediment_skills 下的技能出现 "../" 前缀
  function displayPath(fullPath: string, isUnderSediment: boolean): string {
    const base = isUnderSediment ? dirs.sedimentDir : (dirs.skillsDir ?? dirs.sedimentDir);
    return path.relative(base, fullPath);
  }

  function scan(dir: string, isUnderSediment: boolean): void {
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
        // 这是一个技能目录
        const meta = readSkillMeta(fullPath);
        const source = meta?.source;
        // revisionCount 已迁出到 __sediment_meta__.json
        const revisionCount = readSedimentMeta(fullPath)?.revisionCount;
        const inSediment = isUnderSediment || isLocalSkill(fullPath, dirs.sedimentDir);
        const isSedimentActivated =
          !inSediment && meta?.originSource === "SEDIMENT" && source !== "OFFICIAL";
        const location: SkillLocation =
          source === "OFFICIAL"
            ? "official"
            : inSediment
              ? "sediment"
              : isSedimentActivated
                ? "sediment-active"
                : "native";
        try {
          const content = fs.readFileSync(skillMd, "utf-8");
          const fm = parseFrontmatter(content);
          skills.push({
            name: fm?.name ?? entry.name,
            description: fm?.description ?? "(no description)",
            path: displayPath(fullPath, inSediment),
            source,
            revisionCount,
            location,
          });
        } catch {
          skills.push({
            name: entry.name,
            description: "(failed to parse)",
            path: displayPath(fullPath, inSediment),
            source,
            revisionCount,
            location,
          });
        }
      } else {
        // 可能是 category 目录（skills/ 下的），继续递归
        scan(fullPath, isUnderSediment);
      }
    }
  }

  // 扫描 skills/ 目录（原生 + 官方技能）
  scan(skillsDir, false);
  // 扫描 sediment_skills/ 目录（沉淀技能）
  if (dirs.sedimentDir !== skillsDir) {
    scan(dirs.sedimentDir, true);
  }

  if (skills.length === 0) {
    return {
      success: true,
      message: "No skills found in the managed skills directory.",
      skills: [],
    };
  }

  // 格式化为可读文本，标记位置 / 修改次数
  const lines = skills.map((s) => {
    const tags: string[] = [];
    if (s.location === "official") {
      tags.push("OFFICIAL");
    } else if (s.location === "sediment") {
      tags.push("sediment");
    } else if (s.location === "sediment-active") {
      tags.push("sediment-active");
    } else {
      tags.push("native");
    }
    if (s.revisionCount != null && s.revisionCount > 1) {
      tags.push(`rev ${s.revisionCount}`);
    }
    const tagStr = ` [${tags.join(", ")}]`;
    return `- ${s.name}${tagStr}: ${s.description} (${s.path})`;
  });

  return {
    success: true,
    message: `Found ${skills.length} skill(s):\n${lines.join("\n")}`,
    skills,
  };
}

// ---------------------------------------------------------------------------
// 主入口
// ---------------------------------------------------------------------------

/**
 * 执行一次 skill_manage 动作并返回结果对象。
 *
 * @param dirs - 目录上下文。`sedimentDir`（<workspace>/sediment_skills）是写动作的唯一基目录（物理隔离）；
 *               `skillsDir`（<workspace>/skills）是 view/list 的展示根（含原生 + 官方）以及模糊去重扫描范围。
 */
export function skillManage(params: SkillManageParams, dirs: SkillDirs): SkillManageResult {
  const { action, name } = params;

  // list 和 view 不在此处校验 name（list 不需要，view 在下面单独校验）；
  // 其余动作都需要 name。
  if (action !== "list" && action !== "view" && !name) {
    return {
      success: false,
      error: `'name' is required for action '${action}'.`,
    };
  }

  let result: SkillManageResult;

  switch (action) {
    case "create": {
      if (!name) {
        return { success: false, error: `'name' is required for action 'create'.` };
      }
      if (!params.content) {
        return {
          success: false,
          error:
            "content is required for 'create'. Provide the full SKILL.md text (frontmatter + body).",
        };
      }
      result = createSkill(name, params.content, dirs);
      break;
    }
    case "edit": {
      if (!name) {
        return { success: false, error: `'name' is required for action 'edit'.` };
      }
      if (!params.content) {
        return {
          success: false,
          error: "content is required for 'edit'. Provide the full updated SKILL.md text.",
        };
      }
      result = editSkill(name, params.content, dirs);
      break;
    }
    case "patch": {
      if (!name) {
        return { success: false, error: `'name' is required for action 'patch'.` };
      }
      if (!params.old_string) {
        return {
          success: false,
          error: "old_string is required for 'patch'. Provide the text to find.",
        };
      }
      if (params.new_string === undefined) {
        return {
          success: false,
          error: "new_string is required for 'patch'. Use empty string to delete matched text.",
        };
      }
      result = patchSkill(
        name,
        params.old_string,
        params.new_string,
        dirs,
        params.file_path,
        params.replace_all,
      );
      break;
    }
    case "delete": {
      if (!name) {
        return { success: false, error: `'name' is required for action 'delete'.` };
      }
      result = deleteSkill(name, dirs);
      break;
    }
    case "write_file": {
      if (!name) {
        return { success: false, error: `'name' is required for action 'write_file'.` };
      }
      if (!params.file_path) {
        return {
          success: false,
          error: "file_path is required for 'write_file'. Example: 'references/api-guide.md'",
        };
      }
      if (params.file_content === undefined) {
        return {
          success: false,
          error: "file_content is required for 'write_file'.",
        };
      }
      result = writeFile(name, params.file_path, params.file_content, dirs);
      break;
    }
    case "remove_file": {
      if (!name) {
        return { success: false, error: `'name' is required for action 'remove_file'.` };
      }
      if (!params.file_path) {
        return {
          success: false,
          error: "file_path is required for 'remove_file'.",
        };
      }
      result = removeFile(name, params.file_path, dirs);
      break;
    }
    case "view": {
      if (!name) {
        return {
          success: false,
          error: "name is required for 'view'. Provide the skill name to inspect.",
        };
      }
      result = viewSkill(name, dirs);
      break;
    }
    case "list": {
      result = listSkills(dirs);
      break;
    }
    case "promote": {
      if (!name) {
        return { success: false, error: `'name' is required for action 'promote'.` };
      }
      const reason = (params.promote_reason ?? "").trim();
      if (!reason) {
        return {
          success: false,
          error:
            "promote_reason is required for 'promote'. " +
            "Quote the current task evidence that proves this sediment skill is reusable.",
        };
      }
      result = promoteSkill(name, reason, dirs);
      break;
    }
    default: {
      result = {
        success: false,
        error: `Unknown action '${action}'. Use: create, edit, patch, delete, write_file, remove_file, view, list, promote`,
      };
    }
  }

  return result;
}
