/**
 * 技能沉淀插件 —— 由 Agent 自主管理技能的创建与编辑。
 *
 * 自动沉淀：若工具调用到达阈值，会拉起后台审查子 Agent，判断本轮对话是否产出了可复用、且值得沉淀为技能的非平凡工作流。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import {
  pluginAppliesToAgent,
  resolveValidAgentAllowlistFromConfig,
} from "./plugin-valid-agent-id.js";
import {
  createAutoReviewer,
  isIndependentAgentRuntime,
  isNotUserSession,
  isSkillReviewSession,
  PLUGIN_TAG,
} from "./src/auto-review.js";
import { SkillManageToolSchema, skillManage } from "./src/skill-manage-tool.js";
import type { SkillManageParams } from "./src/types.js";
import {
  evictBySedimentQuota,
  evictExpiredSediments,
  migrateLegacySedimentDirName,
  migrateLegacySedimentSkills,
  migrateSedimentSubdirSkills,
  renameSedimentPrefixSkills,
  resolveSedimentDirForAgent,
  resolveSkillsDirForAgent,
} from "./src/utils.js";

// 沉淀目录回收默认阈值（用户未在 pluginConfig 中配置时生效）：
//   - TTL       ：超过 10 天未被任何动作触碰的 sediment 自动回收
//   - LRU       ：每个 agent 沉淀目录最多保留 20 个 sediment，超过按 lastTouchedAt 升序回收
//   - Grace     ：新 sediment 自创建起 3 天内豁免 TTL/LRU 回收，新技能保护期
//   - Maturation：sediment 创建满 1 天后视为成熟，可走"时间路径"通过 promote 二次命中守卫
const DEFAULT_SEDIMENT_TTL_DAYS = 10;
const DEFAULT_SEDIMENT_MAX_COUNT = 20;
const DEFAULT_SEDIMENT_GRACE_PERIOD_DAYS = 3;
const DEFAULT_PROMOTE_MATURATION_DAYS = 1;

// ---------------------------------------------------------------------------
// 工具描述
//
// 注：skill_manage 工具仅注册给 skill-review 子 Agent
// ---------------------------------------------------------------------------

const TOOL_DESCRIPTION =
  "Manage skills (create, update, delete, view, list, promote). Skills are reusable procedures stored as SKILL.md files.\n\n" +
  "Skill location tags (shown in `list` output):\n" +
  "  [sediment]        — pending sediment skill (writable: all actions)\n" +
  "  [sediment-active] — released sediment skill, now in skills/ (writable: edit/patch/write_file/remove_file)\n" +
  "  [native]          — user's local skill in skills/ (READ-ONLY)\n" +
  "  [OFFICIAL]        — built-in skill (READ-ONLY)\n\n" +
  "Actions:\n" +
  "  list — list all skills with names and descriptions\n" +
  "  view — read the full SKILL.md content of a skill\n" +
  "  create — create a new skill (full SKILL.md with frontmatter + body); always lands in [sediment]\n" +
  "  patch — find/replace in SKILL.md or supporting files (preferred for fixes); allowed on [sediment] and [sediment-active]\n" +
  "  edit — full SKILL.md rewrite (major overhauls only); allowed on [sediment] and [sediment-active]\n" +
  "  delete — only allowed on [sediment]; refuses [sediment-active]/[native]/[OFFICIAL]\n" +
  "  write_file, remove_file — allowed on [sediment] and [sediment-active]\n" +
  "  promote — activate a [sediment] skill by moving it into skills/ and become a [sediment-active].\n" +
  "            Only allowed on [sediment]\n\n";

// ---------------------------------------------------------------------------
// 自动沉淀：后台技能审查提示词（合并了任务描述 + 行为约束）
// ---------------------------------------------------------------------------

function buildSkillReviewPrompt(opts: { hasPriorHandoff?: boolean } = {}): string {
  const hasPriorHandoff = Boolean(opts.hasPriorHandoff);

  // PRIOR HANDOFF 段：仅在父会话已有上一轮 handoff 时注入。
  const priorHandoffPreamble = hasPriorHandoff
    ? "=== PRIOR HANDOFF ===\n" +
      "Context handed off from the previous review of THIS session.\n" +
      "  · <prior_sediment_handoff> = summary of what was already reviewed / sedimented.\n" +
      "  · Use it to resolve references and recognise extensions of already-sedimented patterns.\n" +
      "  · Do NOT resediment a pattern whose evidence lives ENTIRELY in prior_handoff.\n\n"
    : "";

  return (
    priorHandoffPreamble +
    "Review the converssation and decide whether to create / promote / update a skill.\n\n" +
    "=== STEP 1 — Reusability gate ===\n" +
    "  --- STEP 1.0 — Fast reject ---\n" +
    "  Immediately output `Nothing to save.` (skip STEP 2, jump to STEP 3) when ANY of:\n" +
    "    · The whole exchange is pure planning / discussion / Q&A with no artefact produced.\n" +
    "    · The only output is generic competence: ordinary dataset search, plain SQL writing, vanilla chart generation, metric definition lookup,\n" +
    "      scheduled-task / cron setup, report writing.\n" +
    "    · The fix is a one-shot debugging answer for THIS specific bug with no generalisable rule (unless the same bug class is documented to recur and the fix is class-generic).\n\n" +
    "  --- STEP 1.1 — Reusability check (ALL THREE must hold) ---\n" +
    "  · VALUE: encodes knowledge a generic data-agent would NOT already know — e.g.\n" +
    "    a business-caliber rule, an undocumented schema quirk, a platform pitfall with\n" +
    "    a specific workaround, a multi-step diagnosis sequence with cross-step deps,\n" +
    "    a reusable SQL pattern tied to a named dataset, a charting / REDoc convention\n" +
    "    specific to this org. Generic competence is NEVER enough.\n" +
    "  · TRIGGER: ONE concrete future trigger sentence naming BOTH the artefact AND the specific task variant.\n" +
    "    Good: '当用户要求计算 dau_daily 表中 active_user 的 WoW 同比口径时'.\n" +
    "    Bad:  '当用户要写 SQL 时' / '当用户做实验分析时' / '当用户造数据时'.\n" +
    "  · GENERALITY: the pattern must apply to a CLASS of future tasks, not a single one-off. STRONG-SIGNAL hints:\n" +
    "    1. CORRECTION: [user #N] explicitly flagged the assistant as wrong / off-track, assistant then produced\n" +
    "      a different approach, and a LATER [user #M] accepted it (explicit confirm / built on it / asked a presupposing follow-up).\n" +
    "    2. EXPLICIT systematisation request: 下次都这样 / 记住这个 / 做成模板 / 沉淀一下.\n" +
    "    3. CONFIRMED-SUCCESS language after a multi-step workflow: 很好 / 对了 / 可以了 / 通了 / 查到了 / 终于对了\n" +
    "Output format:\n" +
    "  · Fast-rejected at STEP 1.0 → exactly `Nothing to save.`, SKIP STEP 2, jump to STEP 3.\n" +
    "  · Passed STEP 1.1 → `Reusability: <why non-obvious and class-level>; Trigger: <future trigger sentence with specific artefact>` and continue to STEP 2.\n\n" +
    "=== STEP 2 — create / promote / update a skill ===\n" +
    "Use ONLY the `skill_manage` tool. Workflow:\n" +
    "  1. skill_manage(action='list') — enumerate ALL existing skills (note each one's tag).\n" +
    "  2. For EACH plausibly related candidate:\n" +
    "     skill_manage(action='view') — read its full SKILL.md.\n" +
    "  3. Pick exactly ONE of the four cases below. Cases are checked in order.\n\n" +
    "     === Case A — A [sediment] skill matches the current task (this is the SECOND-HIT signal) ===\n" +
    "     Trigger: ANY [sediment]-tagged candidate covers ≥70% of the current pattern,\n" +
    "     OR its TRIGGER sentence is satisfied by THIS session's evidence.\n" +
    "     Meaning: this sediment has been validated as reusable by a\n" +
    "     real second task. PROMOTE it so the engine auto-loads it from next session.\n" +
    "     → skill_manage(action='promote', name='<the sediment name>',\n" +
    "                    promote_reason='<≤200-char quote from STEP 1 evidence showing this task matched the skill>')\n" +
    "     Then STOP. Do NOT create/edit a near-duplicate.\n" +
    "     If the sediment is mostly right but has a CONCRETE missing step or wrong instruction,\n" +
    "     first patch it, THEN promote in the same review:\n" +
    "         skill_manage(action='patch', ...)  →  skill_manage(action='promote', ...).\n" +
    "     Promote needs the sediment to pass the SECOND-HIT guard. It will be accepted when EITHER:\n" +
    "       (1) the matching [sediment] was created in a DIFFERENT past parent conversation, OR\n" +
    "       (2) the matching [sediment] is already MATURE — created long enough ago (default ≥ 1 day).\n" +
    "     === Case B — A [sediment-active] / [native] / [OFFICIAL] skill already covers ≥70% ===\n" +
    "     Meaning: the engine is already loading something that covers this. Do NOT create a duplicate.\n" +
    "     · [sediment-active] with a CONCRETE gap → skill_manage(action='patch') (smallest possible patch).\n" +
    "     · [sediment-active] with no concrete gap → output `Existing skill <name> already covers this pattern.` and STOP.\n" +
    "     · [native] / [OFFICIAL] (read-only) → output `Existing read-only skill is sufficient: <name>.` and STOP.\n" +
    "     === Case C — No related skill exists ===\n" +
    "     Trigger: STEP 1 passed AND no candidate covers >30% of the pattern.\n" +
    "     → skill_manage(action='create', ...). It will land as [sediment] (pending validation).\n" +
    "     Do NOT promote on first creation — promotion requires a SECOND hit (Case A) in a future review.\n" +
    "     === Case D — Otherwise ===\n" +
    "     If none of A/B/C applies, output `Nothing to save.` and STOP.\n\n" +
    "=== STEP 3 — Sediment handoff ===\n" +
    "Your FINAL message MUST end with ONE <sediment_handoff> block.\n" +
    "  · Merge each section with the prior handoff (when present).\n" +
    "  · Empty section → write `(none)`.\n" +
    "  · Quote user text verbatim; paraphrase fixes in ≤ 20 words.\n" +
    "Template:\n" +
    "<sediment_handoff>\n" +
    "## Skills already sedimented in this or prior reviews\n" +
    "- <skill-name, one-line description>, Do NOT include [native] or [OFFICIAL] skills here.\n" +
    "## User intents (in order)\n" +
    '- "<intent sentence>"\n' +
    "## Workflow shape\n" +
    "<tool-A → tool-B → ... ; collapse repeats ; ≈N steps>\n" +
    "## Key artefacts produced (keep latest version of each)\n" +
    "- <type>: <one-line identity, e.g. SQL on dau_daily / chart=trend_line / file=docs/x.md>\n" +
    "## Notes for the next review\n" +
    "<1-3 sentences, e.g. 'User still refining DAU SQL — wait for stabilisation.'>\n" +
    "</sediment_handoff>\n"
  );
}

// ---------------------------------------------------------------------------
// 插件定义
// ---------------------------------------------------------------------------

const skillSedimentPlugin = {
  id: "skill-sediment",
  name: "Skill Sedimentation",
  description:
    "Agent-managed skill creation and updating. " +
    "Turns successful approaches into reusable procedural knowledge.",

  register(api: OpenClawPluginApi) {
    // Resolve configuration
    const config = (api.pluginConfig ?? {}) as {
      enableAutoReview?: boolean;
      nudgeInterval?: number;
      sedimentTtlDays?: number;
      sedimentMaxCount?: number;
      sedimentGracePeriodDays?: number;
      promoteMaturationDays?: number;
    };
    const enableAutoReview = config.enableAutoReview !== false; // default: true
    const nudgeInterval = config.nudgeInterval;
    const validAgentAllowlist = resolveValidAgentAllowlistFromConfig(api.pluginConfig);

    // 沉淀回收阈值解析：
    const sedimentTtlDays =
      typeof config.sedimentTtlDays === "number"
        ? config.sedimentTtlDays
        : DEFAULT_SEDIMENT_TTL_DAYS;
    const sedimentMaxCount =
      typeof config.sedimentMaxCount === "number"
        ? config.sedimentMaxCount
        : DEFAULT_SEDIMENT_MAX_COUNT;
    const sedimentGracePeriodDays =
      typeof config.sedimentGracePeriodDays === "number"
        ? config.sedimentGracePeriodDays
        : DEFAULT_SEDIMENT_GRACE_PERIOD_DAYS;
    // promoteMaturationDays = 0 显式关闭时间路径（promote 退化为仅跨父会话才放行）。
    const promoteMaturationDays =
      typeof config.promoteMaturationDays === "number"
        ? config.promoteMaturationDays
        : DEFAULT_PROMOTE_MATURATION_DAYS;

    /**
     * 动态解析当前 agent 的技能根目录（含原生 + 官方 + sediment）。
     * 每个 agent 拥有独立的 skills 目录（<agent workspace>/skills）。
     */
    const getSkillsDir = (agentId?: string): string => {
      const cfg = api.runtime.config.loadConfig();
      return resolveSkillsDirForAgent(cfg, agentId);
    };

    /**
     * 动态解析当前 agent 的沉淀目录（`<workspace>/sediment_skills/`）。
     * 这是本插件所有写动作的物理隔离基目录——任何 patch/edit/delete/write_file 操作
     * 都不可能命中该目录之外的技能（包括官方/原生本地技能）。
     * 与 skills/ 同级但独立，核心引擎不会自动扫描此目录。
     */
    const getSedimentDir = (agentId?: string): string => {
      const cfg = api.runtime.config.loadConfig();
      return resolveSedimentDirForAgent(cfg, agentId);
    };

    // 创建自动审查器实例（封装所有会话级状态和钩子处理器）
    const reviewer = createAutoReviewer(api, {
      nudgeInterval,
      buildSkillReviewPrompt,
      getSedimentDir,
    });

    api.logger.info(
      `${PLUGIN_TAG} registered (autoReview: ${enableAutoReview}, nudgeInterval: ${nudgeInterval ?? "(default)"}, ` +
        `sedimentTtlDays: ${sedimentTtlDays === 0 ? "disabled" : sedimentTtlDays}, ` +
        `sedimentMaxCount: ${sedimentMaxCount === 0 ? "disabled" : sedimentMaxCount}, ` +
        `sedimentGracePeriodDays: ${sedimentGracePeriodDays <= 0 ? "disabled" : sedimentGracePeriodDays}, ` +
        `promoteMaturationDays: ${promoteMaturationDays <= 0 ? "disabled" : promoteMaturationDays})`,
    );
    {
      const rawAllowlistEnv = process.env["OPENCLAW_SKILL_SEDIMENT_MODEL_ALLOWLIST"];
      if (!rawAllowlistEnv || !rawAllowlistEnv.trim()) {
        api.logger.info(
          `${PLUGIN_TAG} model allowlist NOT configured via Apollo (env OPENCLAW_SKILL_SEDIMENT_MODEL_ALLOWLIST is empty) ` +
            `— fail-open: auto-review will trigger for ALL models`,
        );
      } else {
        api.logger.info(`${PLUGIN_TAG} model allowlist active: ${rawAllowlistEnv.trim()}`);
      }
    }
    if (validAgentAllowlist !== null) {
      api.logger.info(
        `${PLUGIN_TAG} validAgentId allowlist active (${validAgentAllowlist.length} id(s)): ${validAgentAllowlist.join(", ")}`,
      );
    }

    // ──────────────────────────────────────────────────────────────────
    // 启动时一次性迁移历史数据（四阶段，按顺序执行）：
    //   Phase 0: 把 <workspace>/sediment-skills/（连字符旧名）整体迁到
    //            <workspace>/sediment_skills/（下划线新名），必须最先执行
    //   Phase 1: 把 <skills>/sediment-* 移到 <workspace>/sediment_skills/<stripped>
    //   Phase 2: 把 <skills>/sediment/* 移到 <workspace>/sediment_skills/<name>
    //   Phase 3: 对 <sediment_skills>/sediment-* 原地重命名，剥掉 sediment- 前缀
    // 插件注册时立即对默认 agent 执行迁移；后续其他 agent 首次调用时按需触发。
    // ──────────────────────────────────────────────────────────────────

    /** 已完成迁移的 skillsDir 集合（避免重复扫描）。 */
    const migratedDirs = new Set<string>();

    /** 记录单阶段迁移结果日志。 */
    const logMigrationResult = (
      phase: string,
      skillsDir: string,
      result: {
        moved: string[];
        conflicts: string[];
        errors: Array<{ name: string; error: string }>;
      },
    ): void => {
      const movedCount = result.moved.length;
      const conflictCount = result.conflicts.length;
      const errorCount = result.errors.length;
      if (movedCount > 0 || conflictCount > 0 || errorCount > 0) {
        const movedSample = result.moved.slice(0, 5).join(", ");
        const conflictSample = result.conflicts.slice(0, 5).join(", ");
        api.logger.info(
          `${PLUGIN_TAG} ${phase} on '${skillsDir}': ` +
            `moved=${movedCount}${movedSample ? ` [${movedSample}]` : ""}, ` +
            `conflicts=${conflictCount}${conflictSample ? ` [${conflictSample}]` : ""}, ` +
            `errors=${errorCount}`,
        );
        for (const e of result.errors) {
          api.logger.warn(`${PLUGIN_TAG} ${phase} error on '${e.name}': ${e.error}`);
        }
      } else {
        api.logger.debug?.(`${PLUGIN_TAG} ${phase} on '${skillsDir}': nothing to migrate`);
      }
    };

    /** 统一的回收日志：与 logMigrationResult 风格一致，便于排查。 */
    const logEvictResult = (
      action: string,
      sedimentDir: string,
      result: {
        evicted: string[];
        skipped: Array<{ name: string; reason: string }>;
        errors: Array<{ name: string; error: string }>;
      },
    ): void => {
      const ec = result.evicted.length;
      const sc = result.skipped.length;
      const errc = result.errors.length;
      if (ec === 0 && errc === 0) {
        // skipped 数量大也不打 info（grace period 命中是常态），降噪
        api.logger.debug?.(
          `${PLUGIN_TAG} ${action} on '${sedimentDir}': nothing to evict (skipped=${sc})`,
        );
        return;
      }
      const evictedSample = result.evicted.slice(0, 5).join(", ");
      api.logger.info(
        `${PLUGIN_TAG} ${action} on '${sedimentDir}': ` +
          `evicted=${ec}${evictedSample ? ` [${evictedSample}]` : ""}, skipped=${sc}, errors=${errc}`,
      );
      for (const e of result.errors) {
        api.logger.warn(`${PLUGIN_TAG} ${action} error on '${e.name}': ${e.error}`);
      }
    };

    const runMigrationOnce = (skillsDir: string, sedimentDir: string): void => {
      if (migratedDirs.has(skillsDir)) {
        return;
      }
      migratedDirs.add(skillsDir);
      try {
        // Phase 0: <workspace>/sediment-skills/* → <workspace>/sediment_skills/*
        // 必须最先执行：让后续 Phase 1-3 看到统一的下划线目录布局
        const p0 = migrateLegacySedimentDirName(skillsDir);
        logMigrationResult("dir rename (phase 0)", skillsDir, p0);

        // Phase 1: <skills>/sediment-* → <workspace>/sediment_skills/<stripped>
        const p1 = migrateLegacySedimentSkills(skillsDir);
        logMigrationResult("legacy migration (phase 1)", skillsDir, p1);

        // Phase 2: <skills>/sediment/* → <workspace>/sediment_skills/<name>
        const p2 = migrateSedimentSubdirSkills(skillsDir);
        logMigrationResult("subdir migration (phase 2)", skillsDir, p2);

        // Phase 3: <sediment_skills>/sediment-* → <sediment_skills>/<stripped>
        const p3 = renameSedimentPrefixSkills(sedimentDir);
        logMigrationResult("prefix rename (phase 3)", sedimentDir, p3);

        // Phase 4 (TTL 回收): 把 lastTouchedAt 超过 sedimentTtlDays 的死沉淀清掉。
        if (sedimentTtlDays > 0) {
          const ttl = evictExpiredSediments(sedimentDir, sedimentTtlDays, sedimentGracePeriodDays);
          logEvictResult(`ttl eviction (${sedimentTtlDays}d)`, sedimentDir, ttl);
        }
      } catch (err) {
        api.logger.warn(
          `${PLUGIN_TAG} sediment migration failed on '${skillsDir}': ${String(err)}`,
        );
      }
    };
    // 插件注册时立即对默认 agent 执行迁移
    {
      const cfg = api.runtime.config.loadConfig();
      const defaultSkillsDir = resolveSkillsDirForAgent(cfg, undefined);
      const defaultSedimentDir = resolveSedimentDirForAgent(cfg, undefined);
      runMigrationOnce(defaultSkillsDir, defaultSedimentDir);
    }

    // ──────────────────────────────────────────────────────────────────
    // 监听 llm_input / llm_output，按 sessionKey 缓存 LLM 模型信息 + 累计 token 用量。
    // ──────────────────────────────────────────────────────────────────

    api.on("llm_input", (_event: unknown, ctx: unknown) => {
      if (isIndependentAgentRuntime()) {
        return;
      }
      reviewer.handleLlmInput(_event, ctx);
    });

    api.on("llm_output", (_event: unknown, ctx: unknown) => {
      if (isIndependentAgentRuntime()) {
        return;
      }
      reviewer.handleLlmOutput(_event, ctx);
    });

    // ──────────────────────────────────────────────────────────────────
    // 注册 skill_manage 工具
    //
    // 工厂层守卫：只对 skill-review 子 Agent 暴露此工具。其他 session（含
    // 主 Agent、其他子 Agent）调用 resolvePluginTools 时工厂返回 null，
    // 工具的 schema/description 不会进入它们的 LLM 上下文。
    // ──────────────────────────────────────────────────────────────────

    api.registerTool(
      (toolCtx) => {
        // 仅 skill-review subagent 可见；其他 session 完全感知不到此工具。
        if (!isSkillReviewSession(toolCtx?.sessionKey)) {
          return null;
        }
        return {
          name: "skill_manage",
          label: "Skill Manage",
          description: TOOL_DESCRIPTION,
          parameters: SkillManageToolSchema,
          async execute(_toolCallId: string, params: unknown) {
            const typedParams = params as SkillManageParams;
            api.logger.info(
              `${PLUGIN_TAG} skill_manage called: action=${typedParams.action}, name=${typedParams.name ?? "(none)"}, agentId=${toolCtx?.agentId ?? "(none)"}`,
            );

            const skillsDir = getSkillsDir(toolCtx?.agentId);
            const sedimentDir = getSedimentDir(toolCtx?.agentId);
            // 非默认 agent 首次调用时按需触发一次性历史数据迁移。
            runMigrationOnce(skillsDir, sedimentDir);

            // 工厂层守卫（参见上方 isSkillReviewSession 分支）已保证只有 review subagent
            // 能进入此 execute；这里不再做二次身份判定，避免引入 dead branch。
            // 写动作主要落在 sediment_skills/ 隔离目录；sediment-active 技能（已 release
            // 到 skills/）也在原位被修改。skillsDir 用于 list/view 合并展示与 sediment-active 查找。
            // 反查当前 review subagent 所属的父会话 sessionKey：
            //   - createSkill 用它写入 sediment 的 "createdInParentSession"（出生证明）
            //   - promoteSkill 用它实施"跨父会话守卫"（同一父会话内拒绝 self-promote）
            // 反查失败（undefined）时：
            //   - create 路径会让 sediment 不带出生证明，将来 promote 走 fail-open（兼容老数据）
            //   - promote 路径 A（跨父会话）无法判定，但路径 B（时间成熟）仍可独立放行
            const parentSessionKey = reviewer.getParentSessionKeyForReview(toolCtx?.sessionKey);

            const result = skillManage(typedParams, {
              sedimentDir,
              skillsDir,
              // promote 动作需要把 agentId 写进 __skill_meta__.json，对齐 starter
              // moveSealSkillToSkills 的行为；缺省时 meta.agentId 会留空。
              agentId: toolCtx?.agentId,
              parentSessionKey,
              // promote 守卫的"时间成熟期"阈值（天）。
              // 详见 src/skill-manage-tool.ts SkillDirs.promoteMaturationDays。
              promoteMaturationDays,
              // 安全扫描器异常上报：避免 fail-closed 策略悄无声息地降级为 fail-open。
              // 见 src/skill-manage-tool.ts 中 securityScanSkill 的实现。
              onScanError: (err) => {
                api.logger.warn(
                  `${PLUGIN_TAG} security scan threw unexpectedly for action=${typedParams.action}, name=${typedParams.name ?? "(none)"}: ${String(err)}`,
                );
              },
              // promote 物理迁移的"双残留"等状态告警
              onCriticalError: (msg) => {
                api.logger.error(
                  `${PLUGIN_TAG} ${msg} (action=${typedParams.action}, name=${typedParams.name ?? "(none)"})`,
                );
              },
            });

            const text = result.success
              ? (result.message ?? "Operation completed.")
              : `Error: ${result.error}`;

            api.logger.info(
              `${PLUGIN_TAG} skill_manage result: success=${result.success}, action=${typedParams.action}, name=${typedParams.name ?? "(none)"}${result.path ? `, path=${result.path}` : ""}${!result.success && result.error ? `, error=${result.error}` : ""}${result.rejectionTag ? `, tag=${result.rejectionTag}` : ""}`,
            );
            if (!result.success && result.rejectionTag) {
              api.logger.warn(
                `${PLUGIN_TAG} [${result.rejectionTag}] action=${typedParams.action}, name=${typedParams.name ?? "(none)"}, agentId=${toolCtx?.agentId ?? "(none)"}, parentSessionKey=${parentSessionKey ?? "(none)"}`,
              );
            }

            // 对写入类动作输出额外的摘要日志，便于事后排查具体改了什么
            if (result.success) {
              const act = typedParams.action;
              const skillName = typedParams.name ?? "(none)";
              if (act === "create") {
                const descSnippet = (typedParams.content ?? "").slice(0, 200).replace(/\n/g, " ");
                api.logger.info(
                  `${PLUGIN_TAG} skill_manage detail: created '${skillName}', content preview: ${descSnippet}`,
                );
                // 配额回收：刚 create 完检查数量上限。
                if (sedimentMaxCount > 0) {
                  try {
                    const lru = evictBySedimentQuota(
                      sedimentDir,
                      sedimentMaxCount,
                      sedimentGracePeriodDays,
                    );
                    if (lru.evicted.length > 0 || lru.errors.length > 0) {
                      logEvictResult(`lru eviction (cap=${sedimentMaxCount})`, sedimentDir, lru);
                    }
                  } catch (err) {
                    api.logger.warn(
                      `${PLUGIN_TAG} lru eviction failed after create '${skillName}': ${String(err)}`,
                    );
                  }
                }
              } else if (act === "edit") {
                const contentLen = (typedParams.content ?? "").length;
                const descSnippet = (typedParams.content ?? "").slice(0, 200).replace(/\n/g, " ");
                api.logger.info(
                  `${PLUGIN_TAG} skill_manage detail: edited '${skillName}', new content (${contentLen} chars) preview: ${descSnippet}`,
                );
              } else if (act === "patch") {
                const oldSnippet = (typedParams.old_string ?? "")
                  .slice(0, 120)
                  .replace(/\n/g, "\\n");
                const newSnippet = (typedParams.new_string ?? "")
                  .slice(0, 120)
                  .replace(/\n/g, "\\n");
                const targetFile = typedParams.file_path ?? "SKILL.md";
                api.logger.info(
                  `${PLUGIN_TAG} skill_manage detail: patched '${skillName}' (${targetFile}), old="${oldSnippet}", new="${newSnippet}"`,
                );
              } else if (act === "delete") {
                api.logger.info(`${PLUGIN_TAG} skill_manage detail: deleted '${skillName}'`);
              } else if (act === "write_file") {
                const fileLen = (typedParams.file_content ?? "").length;
                api.logger.info(
                  `${PLUGIN_TAG} skill_manage detail: wrote file '${typedParams.file_path}' in '${skillName}' (${fileLen} chars)`,
                );
              } else if (act === "remove_file") {
                api.logger.info(
                  `${PLUGIN_TAG} skill_manage detail: removed file '${typedParams.file_path}' from '${skillName}'`,
                );
              } else if (act === "promote") {
                const reasonSnippet = (typedParams.promote_reason ?? "")
                  .slice(0, 200)
                  .replace(/\n/g, " ");
                api.logger.info(
                  `${PLUGIN_TAG} skill_manage detail: promoted '${skillName}' to skills/, reason: ${reasonSnippet}`,
                );
              }
            }

            // 跟踪 review session 的 skill_manage 调用，用于完成时输出结果摘要。
            reviewer.trackReviewAction(
              toolCtx?.sessionKey,
              typedParams.action,
              result.success,
              result.path,
              typedParams.name,
            );

            // Build full result text including hints and extra info
            const parts = [text];
            if (result.hint) {
              parts.push(`\nHint: ${result.hint}`);
            }
            if (result.path) {
              parts.push(`Path: ${result.path}`);
            }
            if (result.file_preview) {
              parts.push(`\nFile preview:\n${result.file_preview}`);
            }
            if (result.skill_content) {
              parts.push(`\n${result.skill_content}`);
            }
            if (result.available_files && result.available_files.length > 0) {
              parts.push(
                `\nAvailable files:\n${result.available_files.map((f) => `  - ${f}`).join("\n")}`,
              );
            }

            return {
              content: [{ type: "text", text: parts.join("\n") }],
              details: result,
            };
          },
        };
      },
      { name: "skill_manage" },
    );

    // ──────────────────────────────────────────────────────────────────
    // 会话结束时清理状态，避免 Map 无界增长导致内存泄漏。
    // ──────────────────────────────────────────────────────────────────

    api.on("session_end", (_event: unknown, ctx: unknown) => {
      const cx = ctx as { sessionId?: string; sessionKey?: string };
      reviewer.cleanupSession(cx.sessionKey ?? cx.sessionId, cx.sessionId);
    });

    api.on("before_reset", (_event: unknown, ctx: unknown) => {
      const cx = ctx as { sessionId?: string; sessionKey?: string };
      reviewer.cleanupSession(cx.sessionKey ?? cx.sessionId, cx.sessionId);
    });

    // ──────────────────────────────────────────────────────────────────
    // 自动沉淀：在 agent_end 阶段触发后台审查
    // ──────────────────────────────────────────────────────────────────

    if (enableAutoReview) {
      api.on("agent_end", async (event: unknown, ctx: unknown) => {
        try {
          const cx = ctx as {
            sessionKey?: string;
            sessionId?: string;
            agentId?: string;
            trigger?: string;
          };

          // skill-review 子 Agent 完成时，必须放行进入 spawnSkillReview 的 Gate 1 路径，
          // 以执行埋点上报、锁释放与 aimi 后端 hi 消息上报逻辑。不能被三层过滤拦截。
          const isReviewCompletion = isSkillReviewSession(cx.sessionKey);

          if (!isReviewCompletion) {
            if (isIndependentAgentRuntime()) {
              api.logger.info(`${PLUGIN_TAG} agent_end: SKIPPED — independent agent runtime`);
              return;
            }

            if (isNotUserSession(cx.sessionKey)) {
              api.logger.info(
                `${PLUGIN_TAG} agent_end: SKIPPED — non-user session (sessionKey="${cx.sessionKey}")`,
              );
              return;
            }

            if (!pluginAppliesToAgent(cx.agentId, validAgentAllowlist)) {
              api.logger.info(
                `${PLUGIN_TAG} agent_end: SKIPPED — agentId not in validAgentId (agentId="${cx.agentId ?? ""}")`,
              );
              return;
            }
          }

          api.logger.info(
            `${PLUGIN_TAG} agent_end: evaluating session=${cx.sessionKey ?? "unknown"}${isReviewCompletion ? " (review completion)" : ""}`,
          );

          await reviewer.handleAgentEnd(event, ctx);
        } catch (err) {
          api.logger.warn(`${PLUGIN_TAG} agent_end hook error: ${String(err)}`);
        }
      });

      api.on("subagent_ended", async (event: unknown) => {
        await reviewer.handleSubagentEnded(event);
      });
    }
  },
};

export default skillSedimentPlugin;
