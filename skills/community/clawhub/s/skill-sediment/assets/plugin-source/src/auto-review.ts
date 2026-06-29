/**
 * 自动沉淀模块 —— 管理后台技能审查的完整生命周期。
 *
 * 职责：
 *   - 会话级状态管理（工具调用水位线、LLM 模型/token 缓存、并发锁）
 *   - 6 道 Gate 门控判断是否拉起后台审查子 Agent
 *   - review 完成后的埋点上报、锁释放
 *   - 会话结束时的状态清理
 *
 * 通过 {@link createAutoReviewer} 工厂函数创建实例，返回钩子处理器供 index.ts 绑定。
 */

import {
  parseSessionKey,
  postUbaEvent,
  reportSession,
  sendUserQueryWhitelistHiMessage,
} from "openclaw/plugin-sdk";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import type { CheckpointEntry } from "./utils.js";
import {
  buildCondensedContext,
  extractActualUserText,
  extractTextFromContent,
  loadCheckpoint,
  removeCheckpointEntry,
  saveCheckpointEntry,
} from "./utils.js";

// ---------------------------------------------------------------------------
// 常量
// ---------------------------------------------------------------------------

export const PLUGIN_TAG = "[skill-sediment]";

/** 默认阈值：自上次审查以来新增工具调用累计轮次达到 15+ 时触发审查。 */
const SKILL_NUDGE_INTERVAL = 15;

/** 子 Agent 会话后缀标记（用于避免递归触发）。 */
const SUBAGENT_SESSION_TAIL = "subagent:skill-review";

/** 同一 sessionKey 下活跃 review 的超时时间（2 分钟后视为僵死）。 */
const ACTIVE_REVIEW_TIMEOUT_MS = 120_000;

/** Gate 6：累计 userTurns 必须 ≥ 该值才允许触发审查。 */
const MIN_TOTAL_USER_TURNS = 2;

/** Gate 6：至少新增多少个 userTurns 才触发审查。 */
const MIN_NEW_TURNS = 1;

/** Gate 3：会话持续时间必须超过该阈值才触发审查。 */
const MIN_SESSION_DURATION_MS = 5_000;

/** Gate 3（扩展）：距离上一次 review Agent 触发的最小时间间隔。 */
const MIN_REVIEW_SPAWN_INTERVAL_MS = 30_000;

/** handledReviewSessions 惰性清理的最小间隔（5 分钟），避免每次写入都遍历。 */
const HANDLED_REVIEW_SWEEP_INTERVAL_MS = 300_000;

/** handledReviewSessions 条目的 TTL。review 完成后两条路径的时间差通常在毫秒级，10 分钟足以覆盖任何极端延迟场景。 */
const HANDLED_REVIEW_TTL_MS = 600_000;

const UBA_EVENT_KEY = "skill_sediment_skill_sediment_v1_IMPRESSION";

/**
 * 模型白名单（自动 review 仅在父会话使用白名单模型时触发）。
 * 同时兼容带 / 不带 provider 前缀的写法（如 `anthropic/claude-4.6-Opus` 或 `claude-4.6-Opus`）
 * 兜底策略（fail-open）：env 缺失或解析后白名单为空时，**不限制任何模型**。
 */
function getModelAllowlistFromEnv(): Set<string> | null {
  const raw = process.env["OPENCLAW_SKILL_SEDIMENT_MODEL_ALLOWLIST"];
  if (!raw || !raw.trim()) {
    return null;
  }
  const allowlist = new Set<string>();
  for (const item of raw.split(/[,;\n]+/)) {
    const id = item.trim().toLowerCase();
    if (!id) {
      continue;
    }
    allowlist.add(id);
    const slashIdx = id.indexOf("/");
    if (slashIdx > 0 && slashIdx < id.length - 1) {
      allowlist.add(id.slice(slashIdx + 1));
    }
  }
  return allowlist.size > 0 ? allowlist : null;
}

export function isModelAllowed(model: string | undefined): boolean {
  const allowlist = getModelAllowlistFromEnv();
  // fail-open：未配置或解析后为空时不限制
  if (allowlist === null) {
    return true;
  }
  if (!model) {
    return false;
  }
  const normalized = model.trim().toLowerCase();
  if (allowlist.has(normalized)) {
    return true;
  }
  // 反向匹配：实际 model 带 provider 前缀，但白名单条目无前缀
  const slashIdx = normalized.indexOf("/");
  if (slashIdx > 0 && slashIdx < normalized.length - 1) {
    if (allowlist.has(normalized.slice(slashIdx + 1))) {
      return true;
    }
  }
  return false;
}

/**
 * Gate 5 工具调用计数的Apollo黑名单：命中的工具不计入 nudgeInterval 阈值。
 */
export function getExcludedToolNames(): Set<string> {
  const result = new Set<string>();
  const raw = process.env["OPENCLAW_SKILL_SEDIMENT_TOOL_EXCLUDES"];
  if (!raw || !raw.trim()) {
    return result;
  }
  for (const item of raw.split(/[,;\n]+/)) {
    const name = item.trim().toLowerCase();
    if (name) {
      result.add(name);
    }
  }
  return result;
}

// ---------------------------------------------------------------------------
// 会话级状态类型
// ---------------------------------------------------------------------------

/**
 * 自动沉淀的会话级状态：
 * - lastReviewedToolCalls：已审查到的工具调用水位线
 * - lastReviewedTurns：已审查到的用户轮次水位线
 * - lastSpawnedAt：上一次成功拉起 review 子 Agent 的时间戳（毫秒）
 */
interface SessionSkillState {
  lastReviewedToolCalls: number;
  lastReviewedTurns: number;
  lastSpawnedAt: number;
  /**
   * 沉淀切片水位线：parentMessages 数组中已被上一次 review 看过的截止索引。
   */
  lastSedimentedMessageCount: number;
  /**
   * 上一次 review 子 Agent 在最终消息里输出的 <sediment_handoff> 块原文。
   */
  lastSedimentHandoff: string | undefined;
}

/**
 * 会话级 LLM 模型 + token 用量缓存。
 * 通过 llm_output 钩子捕获最近一次使用的 model，并累加整个会话的 token 消耗量。
 */
interface SessionModelInfo {
  model: string;
  tokensInput: number;
  tokensOutput: number;
  tokensCacheRead: number;
  tokensCacheWrite: number;
}

/**
 * 并发锁：同一 sessionKey 下同时只允许一个 review 在运行，防止竞态创建同名技能。
 */
interface ActiveReviewInfo {
  spawnedAt: number;
  reviewSessionKey: string;
  parentAgentId: string;
  parentSessionId: string;
  parentSessionKey: string;
  /**
   * 本次拉起 review 时父会话的消息总数。
   * 完成回调命中 <sediment_handoff> 时把它写回父 state.lastSedimentedMessageCount，
   * 推进切片水位线。
   */
  pendingSedimentCount: number;
  /**
   * 父会话 sessionStates 的 stableKey，便于完成回调直接定位父 state。
   */
  parentStableKey: string;
}

/**
 * review session 的 skill_manage 调用计数。
 *
 * - actions: 所有"会改变磁盘状态"的成功调用总数（creates+edits+patches+deletes+writeFiles+removeFiles+promotes）。
 * - views:   只读调用次数（list/view），不计入 actions。
 * - 其余字段对应 SkillManageAction 中七类写操作的细分计数，用于埋点和 outcome label。
 */
interface ReviewActionCounts {
  actions: number;
  creates: number;
  edits: number;
  patches: number;
  deletes: number;
  writeFiles: number;
  removeFiles: number;
  promotes: number;
  views: number;
  skillNames: Set<string>;
}

// ---------------------------------------------------------------------------
// 辅助函数
// ---------------------------------------------------------------------------

/**
 * 统计消息数组中的"真实"用户轮次。
 *
 * 仅按 `role === "user"` 计数会把 runtime / channel / IDE 注入的伪 user 消息
 * 也算上（pre-compaction flush、/new /reset 模板、Sender metadata、relevant_memories、
 * additional_data 等），导致 Gate 6 / Gate 6.1 的真实性判断失守：
 *   - 用户实际只发了 1 句，但被假 user 凑数判定为 ≥ 2 轮 → 误触发 review
 *   - 用户没发新消息，runtime 注入了假 user → 误判"有新增" → 重复 review 同一段
 *
 * 修复：每条 role=user 都先用 {@link extractActualUserText} 剥离所有 envelope，
 * 仅当 hadRealContent 为 true（剥光后仍有实质内容）才计入。
 * 与 {@link buildCondensedContext} 输出的 `retainedUserTurns` 语义保持一致。
 */
function countUserTurns(messages: unknown[]): number {
  if (!Array.isArray(messages)) {
    return 0;
  }
  let n = 0;
  for (const m of messages) {
    if (!m || typeof m !== "object") {
      continue;
    }
    if ((m as { role?: unknown }).role !== "user") {
      continue;
    }
    const rawText = extractTextFromContent((m as { content?: unknown }).content);
    if (!rawText.trim()) {
      continue;
    }
    const { hadRealContent } = extractActualUserText(rawText);
    if (hadRealContent) {
      n += 1;
    }
  }
  return n;
}

/**
 * 统计 assistant 消息中**成功**的工具调用次数。
 */
function countToolCalls(messages: unknown[], excludes: ReadonlySet<string> = new Set()): number {
  if (!Array.isArray(messages)) {
    return 0;
  }

  // 预扫描：收集所有失败的 toolCallId
  const failedCallIds = new Set<string>();
  for (const m of messages) {
    if (!m || typeof m !== "object") {
      continue;
    }
    const msg = m as { role?: unknown; isError?: unknown; toolCallId?: unknown };
    if (msg.role !== "toolResult") {
      continue;
    }
    if (msg.isError && typeof msg.toolCallId === "string" && msg.toolCallId) {
      failedCallIds.add(msg.toolCallId);
    }
  }

  let n = 0;
  for (const m of messages) {
    if (!m || typeof m !== "object") {
      continue;
    }
    const msg = m as { role?: unknown; content?: unknown };
    if (msg.role !== "assistant") {
      continue;
    }

    if (Array.isArray(msg.content)) {
      for (const block of msg.content) {
        if (
          !block ||
          typeof block !== "object" ||
          (block as { type?: unknown }).type !== "toolCall"
        ) {
          continue;
        }
        // 排除失败的 toolCall
        if (failedCallIds.size > 0) {
          const id = (block as { toolCallId?: unknown }).toolCallId;
          if (typeof id === "string" && failedCallIds.has(id)) {
            continue;
          }
        }
        // 排除黑名单工具
        if (excludes.size > 0) {
          const name = (block as { name?: unknown }).name;
          if (typeof name === "string" && excludes.has(name.trim().toLowerCase())) {
            continue;
          }
        }
        n += 1;
      }
    }
  }
  return n;
}

/**
 * 判断当前会话是否为非用户会话（subagent / cron / group chat），
 * 若是则跳过技能沉淀相关逻辑，避免污染内部任务上下文。
 */
export function isNotUserSession(sessionKey: string | undefined): boolean {
  const key = sessionKey?.toLowerCase() ?? "";
  if (key.includes("subagent") || key.includes("cron")) {
    return true;
  }
  // Group chat sessions (including ACP-forwarded): skip skill sedimentation
  if (key.includes(":group:")) {
    return true;
  }
  return false;
}

/** 与 session-new-reporter 中 Apollo independent_agent_map 结构一致 */
interface IndependentAgentConfig {
  bizId: string;
  SERVICE_ID: string;
}

/**
 * 读取 starter 注入的 `OPENCLAW_INDEPENDENT_AGENT_MAP`（JSON 数组），
 * 与 {@link isIndependentAgentRuntime} 搭配判断当前容器是否为独立 Agent 实例。
 */
function getIndependentAgentMap(): IndependentAgentConfig[] {
  const raw = process.env["OPENCLAW_INDEPENDENT_AGENT_MAP"];
  if (!raw) {
    return [];
  }
  try {
    return JSON.parse(raw) as IndependentAgentConfig[];
  } catch {
    return [];
  }
}

/**
 * 当前进程是否为 Apollo independent_agent_map 中的独立 Agent（按 SERVICE_ID 命中且存在 bizId）。
 * 独立 Agent 上跳过技能沉淀，与主实例隔离。
 */
export function isIndependentAgentRuntime(): boolean {
  const serviceId = (process.env.SERVICE_ID ?? "").trim();
  if (!serviceId) {
    return false;
  }
  const matched = getIndependentAgentMap().find((item) => item.SERVICE_ID === serviceId);
  return Boolean(matched?.bizId);
}

/**
 * 判断 session key 是否属于本插件拉起的 skill-review 子 Agent 会话。
 */
export function isSkillReviewSession(sessionKey: string | undefined): boolean {
  return Boolean(sessionKey?.includes(SUBAGENT_SESSION_TAIL));
}

/**
 * 让出微/宏任务队列若干轮，等待 llm_output 钩子的 fire-and-forget handler 完成。
 */
async function waitForLlmOutputDrain(): Promise<void> {
  await new Promise<void>((resolve) => setImmediate(resolve));
  await new Promise<void>((resolve) => setImmediate(resolve));
}

/** 从 reviewActionCounts 构建人类可读的 outcome 标签，供日志和埋点复用。 */
function buildOutcomeLabel(counts: ReviewActionCounts | undefined): string {
  if (counts && counts.actions > 0) {
    return (
      `skill changes made (` +
      `creates=${counts.creates}, ` +
      `edits=${counts.edits}, ` +
      `patches=${counts.patches}, ` +
      `deletes=${counts.deletes}, ` +
      `write_files=${counts.writeFiles}, ` +
      `remove_files=${counts.removeFiles}, ` +
      `promotes=${counts.promotes}, ` +
      `views=${counts.views})`
    );
  }
  return `nothing to save (views=${counts?.views ?? 0})`;
}

/**
 * 发送 review_completed UBA 埋点并检查响应业务码。
 */
function sendReviewCompletedEvent(
  api: OpenClawPluginApi,
  attrs: {
    parentAgentId: string;
    parentSessionKey: string;
    parentSessionId: string;
    reviewSessionKey: string;
    reason: string;
    outcomeLabel: string;
    durationMs: number;
    // 写动作七维度细分（与 ReviewActionCounts / outcomeLabel 保持一致）。
    creates: number;
    edits: number;
    patches: number;
    deletes: number;
    writeFiles: number;
    removeFiles: number;
    promotes: number;
    skillNames: string[];
    model?: string;
    tokensInput?: number;
    tokensOutput?: number;
    tokensCacheRead?: number;
    tokensCacheWrite?: number;
  },
): void {
  const { channel } = parseSessionKey(attrs.parentSessionKey);
  // 调试日志：上报前打印关键字段，便于在线上日志中核对取数情况。
  api.logger.info(
    `${PLUGIN_TAG} sending UBA event: ` +
      `parentSession=${attrs.parentSessionKey}, reviewSession=${attrs.reviewSessionKey}, ` +
      `outcome=${attrs.outcomeLabel}, model="${attrs.model ?? ""}", ` +
      `tokens(input=${attrs.tokensInput ?? 0}, output=${attrs.tokensOutput ?? 0}, ` +
      `cacheRead=${attrs.tokensCacheRead ?? 0}, cacheWrite=${attrs.tokensCacheWrite ?? 0})`,
  );
  void postUbaEvent(UBA_EVENT_KEY, {
    agent_id: attrs.parentAgentId,
    session_key: attrs.parentSessionKey,
    session_id: attrs.parentSessionId,
    channel,
    review_session_key: attrs.reviewSessionKey,
    skill_reason: attrs.reason,
    outcome: attrs.outcomeLabel,
    duration_ms: attrs.durationMs,
    skill_creates: attrs.creates,
    skill_edits: attrs.edits,
    skill_patches: attrs.patches,
    // 细分字段：UBA 平台若未建对应列会自动忽略，不会阻断上报；
    // 已建列时可用于细分写动作分布（删除 / 文件级别变更 / 二次召回升级）。
    skill_deletes: attrs.deletes,
    skill_write_files: attrs.writeFiles,
    skill_remove_files: attrs.removeFiles,
    skill_promotes: attrs.promotes,
    skill_name: attrs.skillNames.join(","),
    llm_model: attrs.model ?? "",
    tokens_input: attrs.tokensInput ?? 0,
    tokens_output: attrs.tokensOutput ?? 0,
    tokens_cache_read: attrs.tokensCacheRead ?? 0,
    tokens_cache_write: attrs.tokensCacheWrite ?? 0,
  })
    .then(async (resp: Response) => {
      try {
        const body = (await resp.json()) as { code?: number; success?: boolean; msg?: string };
        if (body.success && body.code === 0) {
          api.logger.info(
            `${PLUGIN_TAG} UBA event sent (session=${attrs.parentSessionKey}, outcome=${attrs.outcomeLabel})`,
          );
        } else {
          api.logger.warn(
            `${PLUGIN_TAG} UBA event rejected: code=${body.code}, msg=${body.msg ?? ""}`,
          );
        }
      } catch {
        api.logger.warn(`${PLUGIN_TAG} UBA event response parse failed (status=${resp.status})`);
      }
    })
    .catch((err: unknown) => {
      api.logger.warn(`${PLUGIN_TAG} UBA event failed: ${String(err)}`);
    });
}

/**
 * 把 review 子 Agent 完成事件上报到 aimi 后端：
 *   第一层：拉起过 review 子 Agent 就调用 reportSession 注册到 aimi 后端，保证后续能回溯到完整对话记录（无条件触发）。
 *   第二层：仅当 review 真正产出技能变更（creates > 0 || promotes > 0）时才发 hi 消息通知接收方（白名单），减少噪声。
 */
function reportReviewToAimi(
  api: OpenClawPluginApi,
  attrs: {
    /** review 子 Agent 自己的 sessionKey。 */
    reviewSessionKey: string;
    /** review 子 Agent 自己的 sessionId。 */
    reviewSessionId: string | undefined;
    /** review 子 Agent 自己的 agentId。 */
    reviewAgentId: string | undefined;
    /** 父会话信息。 */
    parentInfo: ActiveReviewInfo;
    /** 是否产出技能变更（counts.creates > 0 || counts.promotes > 0）。false 时只发 reportSession，不发 hi。 */
    hasSkillChanges: boolean;
    /** 调试日志：outcome 标签 + actions 数（用于排查"为什么没发 hi"）。 */
    outcomeLabel: string;
    actions: number;
    /** 用于日志标注是哪条路径调用的（"gate1" / "subagent_ended"）。 */
    pathTag: string;
  },
): void {
  const { reviewSessionKey, reviewSessionId, reviewAgentId, parentInfo, hasSkillChanges } = attrs;

  // 必要标识缺失 → 无法可靠上报，直接降级（仅记日志，不影响埋点路径）。
  if (!reviewSessionId || !reviewAgentId) {
    api.logger.warn(
      `${PLUGIN_TAG} reportSession skipped (${attrs.pathTag}) — missing review identity ` +
        `(reviewSessionId=${reviewSessionId ?? "(none)"}, reviewAgentId=${reviewAgentId ?? "(none)"}, ` +
        `session=${reviewSessionKey})`,
    );
    return;
  }

  // 重入保护：调用方（Gate 1 / subagent_ended）通过 handledReviewSessions 互斥，
  // 同一 reviewSessionKey 在 helper 这一层只会进一次，无需额外 in-flight 标记。
  void reportSession(
    reviewSessionId,
    reviewSessionKey,
    reviewAgentId,
    "技能自动审查",
    { type: "subAgent" },
    "subagent_session_create_skill_review",
  )
    .then(() => {
      if (!hasSkillChanges) {
        api.logger.info(
          `${PLUGIN_TAG} sendUserQueryWhitelistHiMessage skipped (${attrs.pathTag}) — no skill changes ` +
            `(session=${reviewSessionKey}, outcome=${attrs.outcomeLabel})`,
        );
        return;
      }
      void sendUserQueryWhitelistHiMessage({
        sessionKey: reviewSessionKey,
        sessionId: reviewSessionId,
        content: "技能自动审查",
        channel: "subagent_session_create_skill_review",
        agentId: reviewAgentId,
        whitelistKind: "subAgentSkillReview",
        bannerHtml: `<font color="warning">skill-review subAgent 上报</font>`,
        target: "SubAgentSkillReview",
      }).catch((err: unknown) => {
        const msg = err instanceof Error ? err.message : String(err);
        api.logger.warn(
          `${PLUGIN_TAG} sendUserQueryWhitelistHiMessage(subAgentSkillReview) failed ` +
            `(${attrs.pathTag}, session=${reviewSessionKey}): ${msg}`,
        );
      });
    })
    .catch((err: unknown) => {
      const msg = err instanceof Error ? err.message : String(err);
      api.logger.warn(
        `${PLUGIN_TAG} reportSession failed (${attrs.pathTag}, session=${reviewSessionKey}): ${msg}`,
      );
    });
  api.logger.info(
    `${PLUGIN_TAG} reportSession dispatched (${attrs.pathTag}) for review session=${reviewSessionKey} ` +
      `(hasSkillChanges=${hasSkillChanges}, actions=${attrs.actions})`,
  );
}

// ---------------------------------------------------------------------------
// 工厂函数：创建自动审查实例
// ---------------------------------------------------------------------------

export interface AutoReviewerOptions {
  nudgeInterval?: number;
  /**
   * 后台审查子 Agent 的系统提示词构建函数。
   * 当 `hasPriorHandoff` 为 true 时，prompt 会增加 prior_sediment_handoff 段，
   * 并提醒 LLM 不要重复沉淀"证据全在 prior handoff"的旧片段。
   */
  buildSkillReviewPrompt: (opts: { hasPriorHandoff: boolean }) => string;
  /**
   * 沉淀目录路径解析函数。
   * 用于定位 checkpoint 文件（`<sedimentDir>/.review_checkpoint.json`）。
   * 传入 agentId 返回对应 agent 的 sedimentDir。
   */
  getSedimentDir: (agentId?: string) => string;
}

/**
 * 创建自动审查器实例。
 */
export function createAutoReviewer(api: OpenClawPluginApi, opts: AutoReviewerOptions) {
  const nudgeInterval = opts.nudgeInterval ?? SKILL_NUDGE_INTERVAL;
  const { buildSkillReviewPrompt, getSedimentDir } = opts;

  // Gate 5 工具名黑名单：实例化时一次性解析 env，整个 reviewer 生命周期内复用。
  const excludedToolNames = getExcludedToolNames();

  // ─── 会话级状态 ──────────────────────────────────────────────────

  const sessionStates = new Map<string, SessionSkillState>();

  // 启动时从 checkpoint 文件恢复上次持久化的水位线状态。
  // 仅恢复 sessionStates（review 水位线 + handoff 上下文），其余 Map 要么关联已死的
  // review 子 Agent 进程，要么会被自然重新填充，无需持久化。
  try {
    const restored = loadCheckpoint(getSedimentDir());
    for (const [key, entry] of restored) {
      sessionStates.set(key, {
        lastReviewedToolCalls: entry.lastReviewedToolCalls,
        lastReviewedTurns: entry.lastReviewedTurns,
        // 从 checkpoint 恢复真实的触发时间戳，保证频繁重启时冷却计时器不失效。
        // 兼容旧 checkpoint 文件（无此字段时回退到 0）。
        lastSpawnedAt: entry.lastSpawnedAt ?? 0,
        lastSedimentedMessageCount: entry.lastSedimentedMessageCount,
        lastSedimentHandoff: entry.lastSedimentHandoff ?? undefined,
      });
    }
    if (restored.size > 0) {
      api.logger.info(
        `${PLUGIN_TAG} checkpoint: restored ${restored.size} session state(s) from disk`,
      );
    }
  } catch (err) {
    // 恢复失败不阻塞启动——等价于全新启动，所有水位线从 0 开始。
    api.logger.warn(`${PLUGIN_TAG} checkpoint: failed to restore session states: ${String(err)}`);
  }

  const sessionModelInfo = new Map<string, SessionModelInfo>();
  const activeReviews = new Map<string, ActiveReviewInfo>();
  const reviewActionCounts = new Map<string, ReviewActionCounts>();

  /**
   * review 子 Agent 自身的 (sessionId, agentId)，按 reviewSessionKey 索引。
   */
  const reviewSessionIdentities = new Map<string, { sessionId: string; agentId: string }>();

  /**
   * 存储最近一次使用的模型名。
   */
  const parentSessionModel = new Map<string, string>();

  /**
   * 显式互斥标志：记录已被处理过的 review sessionKey。
   * Gate 1 路径（agent_end）和 subagent_ended 路径都会尝试处理同一个 review session 的完成事件，
   * 先到的路径将 reviewSessionKey 加入此 Map，后到的路径检测到已存在则跳过。
   */
  const handledReviewSessions = new Map<string, number>();

  let lastHandledReviewSweepAt = 0;

  // ─── 内部辅助 ──────────────────────────────────────────────────

  function getSessionState(key: string): SessionSkillState {
    let state = sessionStates.get(key);
    if (!state) {
      state = {
        lastReviewedToolCalls: 0,
        lastReviewedTurns: 0,
        lastSpawnedAt: 0,
        lastSedimentedMessageCount: 0,
        lastSedimentHandoff: undefined,
      };
      sessionStates.set(key, state);
    }
    return state;
  }

  /**
   * 抓取 review 子 Agent 最终消息中的 <sediment_handoff> 块，并把父 state 的
   * 水位线 + handoff 文本一起推进。
   */
  async function captureHandoffAndAdvance(
    reviewSessionKey: string,
    parentInfo: ActiveReviewInfo,
  ): Promise<void> {
    let finalText = "";
    try {
      const { messages: reviewMessages } = await api.runtime.subagent.getSessionMessages({
        sessionKey: reviewSessionKey,
      });
      if (!Array.isArray(reviewMessages)) {
        api.logger.warn(
          `${PLUGIN_TAG} handoff capture: getSessionMessages returned non-array ` +
            `(reviewSession=${reviewSessionKey})`,
        );
        return;
      }
      // 找最后一条 assistant 消息，抽出其 text 内容。
      for (let i = reviewMessages.length - 1; i >= 0; i--) {
        const m = reviewMessages[i] as { role?: unknown; content?: unknown } | undefined;
        if (!m || typeof m !== "object" || m.role !== "assistant") {
          continue;
        }
        if (typeof m.content === "string") {
          finalText = m.content;
        } else if (Array.isArray(m.content)) {
          finalText = (m.content as Array<{ type?: string; text?: string }>)
            .filter((c) => !c.type || c.type === "text")
            .map((c) => c.text ?? "")
            .join("");
        }
        break;
      }
    } catch (err) {
      api.logger.warn(
        `${PLUGIN_TAG} handoff capture failed to fetch review messages ` +
          `(reviewSession=${reviewSessionKey}): ${String(err)}`,
      );
      return;
    }

    if (!finalText) {
      api.logger.warn(
        `${PLUGIN_TAG} handoff capture: review session had no assistant text ` +
          `(reviewSession=${reviewSessionKey}); watermark NOT advanced`,
      );
      return;
    }

    // 匹配 <sediment_handoff>...</sediment_handoff>，取最后一次出现（防止 LLM
    // 在解释段里也写了示例标签）。
    const matches = [...finalText.matchAll(/<sediment_handoff>([\s\S]*?)<\/sediment_handoff>/gi)];
    const last = matches[matches.length - 1];
    if (!last) {
      api.logger.warn(
        `${PLUGIN_TAG} handoff capture: review output did NOT contain <sediment_handoff> ` +
          `(reviewSession=${reviewSessionKey}, finalText=${finalText.length}chars); ` +
          `watermark NOT advanced (review will re-evaluate same region next time)`,
      );
      return;
    }
    // 防御性截断：上限 3000 字符（prompt 要求 ≤1500，留 2x 缓冲）。
    const HANDOFF_HARD_CAP = 3000;
    let handoff = last[1].trim();
    if (handoff.length > HANDOFF_HARD_CAP) {
      handoff = `${handoff.slice(0, HANDOFF_HARD_CAP)}\n...(truncated from ${last[1].length} chars)`;
      api.logger.info(
        `${PLUGIN_TAG} handoff capture: truncated oversized handoff ` +
          `(${last[1].length} → ${HANDOFF_HARD_CAP} chars, reviewSession=${reviewSessionKey})`,
      );
    }

    const parentState = sessionStates.get(parentInfo.parentStableKey);
    if (!parentState) {
      // 父 state 已被 session_end 清掉——父会话可能已结束。无需推进，下次新会话从 0 重来。
      api.logger.info(
        `${PLUGIN_TAG} handoff capture: parent state already cleaned up, skipping watermark advance ` +
          `(parentKey=${parentInfo.parentStableKey})`,
      );
      return;
    }
    parentState.lastSedimentedMessageCount = parentInfo.pendingSedimentCount;
    parentState.lastSedimentHandoff = handoff;

    // 水位线推进成功——持久化到 checkpoint 文件，防止重启后丢失。
    try {
      saveCheckpointEntry(getSedimentDir(), parentInfo.parentStableKey, {
        lastReviewedToolCalls: parentState.lastReviewedToolCalls,
        lastReviewedTurns: parentState.lastReviewedTurns,
        lastSedimentedMessageCount: parentState.lastSedimentedMessageCount,
        lastSedimentHandoff: parentState.lastSedimentHandoff ?? null,
        lastSpawnedAt: parentState.lastSpawnedAt,
        savedAt: new Date().toISOString(),
      });
    } catch (err) {
      // 持久化失败不影响主流程——内存中的水位线已推进，仅重启时可能回退。
      api.logger.warn(
        `${PLUGIN_TAG} checkpoint save failed (parent=${parentInfo.parentStableKey}): ${String(err)}`,
      );
    }

    api.logger.info(
      `${PLUGIN_TAG} handoff captured (${handoff.length} chars); ` +
        `advanced watermark for parent=${parentInfo.parentStableKey} to messageCount=${parentInfo.pendingSedimentCount}`,
    );
  }

  /** 惰性清理过期的 handledReviewSessions 条目。 */
  function sweepHandledReviewSessions(): void {
    const now = Date.now();
    if (now - lastHandledReviewSweepAt < HANDLED_REVIEW_SWEEP_INTERVAL_MS) {
      return;
    }
    lastHandledReviewSweepAt = now;
    for (const [key, ts] of handledReviewSessions) {
      if (now - ts > HANDLED_REVIEW_TTL_MS) {
        handledReviewSessions.delete(key);
      }
    }
  }

  // ─── spawnSkillReview ──────────────────────────────────────────

  /**
   * 评估"刚结束的一轮对话"是否值得拉起后台技能审查。
   * 当所有门都通过时，通过 getSessionMessages 获取父会话消息，
   * 经 buildCondensedContext 精简后注入 message，拉起后台子 Agent 执行审查。
   */
  async function spawnSkillReview(event: unknown, ctx: unknown): Promise<void> {
    const ev = event as {
      messages?: unknown[];
      success?: boolean;
      error?: string;
      durationMs?: number;
    };
    const cx = ctx as {
      sessionId?: string;
      sessionKey?: string;
      agentId?: string;
    };

    // Gate 1：跳过非用户会话（subagent / cron / group chat）。
    if (isNotUserSession(cx.sessionKey)) {
      api.logger.info(`${PLUGIN_TAG} SKIP — non-user session (key=${cx.sessionKey})`);
      // 显式互斥：通过 handledReviewSessions 标志位与 subagent_ended hook 互斥——
      // 先到的路径将 reviewSessionKey 加入 Set，后到的路径检测到已存在则跳过，
      // 避免重复埋点和重复 hi 消息上报。
      if (isSkillReviewSession(cx.sessionKey)) {
        // 显式互斥检查：如果 subagent_ended 已经处理过，跳过
        if (handledReviewSessions.has(cx.sessionKey!)) {
          api.logger.debug?.(
            `${PLUGIN_TAG} agent_end/gate1: skipping — already handled by subagent_ended ` +
              `(session=${cx.sessionKey})`,
          );
          return;
        }
        // 写入前顺手 sweep（自带 5 分钟节流），保证条目按 TTL 清理。
        sweepHandledReviewSessions();
        // 显式互斥锚点：在 await 之前占位，确保 subagent_ended 端在本路径执行
        const reviewKey = cx.sessionKey!;
        handledReviewSessions.set(reviewKey, Date.now());

        // ── 阶段 A：尚未上报，失败可安全回滚让 subagent_ended 重做 ──
        try {
          await waitForLlmOutputDrain();
        } catch (err) {
          handledReviewSessions.delete(reviewKey);
          api.logger.warn(
            `${PLUGIN_TAG} agent_end/gate1 phaseA aborted: ${String(err)} ` +
              `(released handled flag for ${reviewKey}; subagent_ended will retry)`,
          );
          return;
        }

        // ── 阶段 B：开始消费 + 上报。任何错误都不能让 subagent_ended 重做。 ──
        try {
          // 输出 review 结果摘要：有没有实际产出技能变更
          const counts = reviewActionCounts.get(reviewKey);
          reviewActionCounts.delete(reviewKey);
          const gate1OutcomeLabel = buildOutcomeLabel(counts);
          api.logger.info(
            `${PLUGIN_TAG} review outcome: ${gate1OutcomeLabel} (session=${reviewKey})`,
          );

          // 反查父会话信息（用于上报安全检查 + 埋点关联）
          let gate1ParentInfo: ActiveReviewInfo | undefined;
          let gate1ParentLockKey: string | undefined;
          for (const [key, info] of activeReviews) {
            if (info.reviewSessionKey === reviewKey) {
              gate1ParentInfo = info;
              gate1ParentLockKey = key;
              break;
            }
          }

          // 上报到 aimi 后端：
          //   第一层：拉起过 review 子 Agent，就把会话注册到 aimi 后端，保证后续可回溯到完整对话记录
          //   第二层：仅当 review 真正产出技能变更时才发 hi 消息通知，减少噪声。
          const hasSkillChanges = Boolean(counts && (counts.creates > 0 || counts.promotes > 0));
          if (gate1ParentInfo) {
            reportReviewToAimi(api, {
              reviewSessionKey: reviewKey,
              reviewSessionId: cx.sessionId,
              reviewAgentId: cx.agentId,
              parentInfo: gate1ParentInfo,
              hasSkillChanges,
              outcomeLabel: gate1OutcomeLabel,
              actions: counts?.actions ?? 0,
              pathTag: "gate1",
            });
          } else {
            api.logger.info(
              `${PLUGIN_TAG} reportSession skipped (gate1) — no parent info found ` +
                `(session=${reviewKey}, likely orphan review session not spawned by this plugin)`,
            );
          }
          // 无条件清理 identity（与 reviewActionCounts 的 delete 时机对齐）
          reviewSessionIdentities.delete(reviewKey);

          if (gate1ParentInfo && gate1ParentLockKey) {
            // 抓取 <sediment_handoff> 并推进父 state 水位线（fail-safe：未命中不推进）。
            await captureHandoffAndAdvance(reviewKey, gate1ParentInfo);

            // 埋点: review_completed（Gate 1 路径）
            const gate1ModelInfo = sessionModelInfo.get(reviewKey);
            sessionModelInfo.delete(reviewKey);
            sendReviewCompletedEvent(api, {
              parentAgentId: gate1ParentInfo.parentAgentId,
              parentSessionKey: gate1ParentInfo.parentSessionKey,
              parentSessionId: gate1ParentInfo.parentSessionId,
              reviewSessionKey: reviewKey,
              reason: ev.error ?? "agent_end",
              outcomeLabel: gate1OutcomeLabel,
              durationMs: ev.durationMs ?? 0,
              creates: counts?.creates ?? 0,
              edits: counts?.edits ?? 0,
              patches: counts?.patches ?? 0,
              deletes: counts?.deletes ?? 0,
              writeFiles: counts?.writeFiles ?? 0,
              removeFiles: counts?.removeFiles ?? 0,
              promotes: counts?.promotes ?? 0,
              skillNames: counts ? [...counts.skillNames] : [],
              model: gate1ModelInfo?.model,
              tokensInput: gate1ModelInfo?.tokensInput,
              tokensOutput: gate1ModelInfo?.tokensOutput,
              tokensCacheRead: gate1ModelInfo?.tokensCacheRead,
              tokensCacheWrite: gate1ModelInfo?.tokensCacheWrite,
            });

            activeReviews.delete(gate1ParentLockKey);
            api.logger.info(
              `${PLUGIN_TAG} agent_end: released review lock for parent session=${gate1ParentLockKey}`,
            );
          }
        } catch (err) {
          // 阶段 B 失败：reportReviewToAimi 可能已发出上报，不能让 subagent_ended重做。
          api.logger.warn(
            `${PLUGIN_TAG} agent_end/gate1 phaseB error (NOT rolling back handled flag to avoid ` +
              `duplicate reports; activeReviews lock will be reaped by Gate 4 timeout): ${String(err)}`,
          );
        }
      }
      return;
    }

    // Gate 1.5：仅当父会话最近一次 LLM 调用使用了 Apollo 下发白名单中的模型时，才触发后续审查。
    const parentKeyForModelCheck = cx.sessionKey ?? cx.sessionId;
    const currentModel = parentKeyForModelCheck
      ? parentSessionModel.get(parentKeyForModelCheck)
      : undefined;
    if (!isModelAllowed(currentModel)) {
      api.logger.info(
        `${PLUGIN_TAG} SKIP — model not in Apollo allowlist ` +
          `(model="${currentModel ?? "(unknown)"}", session=${parentKeyForModelCheck ?? "unknown"})`,
      );
      return;
    }

    // Gate 2：本轮执行必须成功（O(1)）
    if (!ev.success) {
      api.logger.info(`${PLUGIN_TAG} SKIP — session not successful (error=${ev.error ?? "none"})`);
      return;
    }

    // Gate 3：会话持续时间必须超过阈值（过短的会话不太可能产出值得沉淀的工作流）（O(1)）
    if (ev.durationMs !== undefined && ev.durationMs < MIN_SESSION_DURATION_MS) {
      api.logger.info(
        `${PLUGIN_TAG} SKIP — session too short (durationMs=${ev.durationMs} < ${MIN_SESSION_DURATION_MS})`,
      );
      return;
    }

    const stableKey = cx.sessionKey ?? cx.sessionId ?? "unknown";
    const now = Date.now();

    const state = getSessionState(stableKey);

    // Gate 3（扩展）：距离上一次 review Agent 触发必须超过最小间隔（O(1)）
    if (state.lastSpawnedAt > 0 && now - state.lastSpawnedAt < MIN_REVIEW_SPAWN_INTERVAL_MS) {
      api.logger.info(
        `${PLUGIN_TAG} SKIP — too soon since last review spawn ` +
          `(elapsed=${now - state.lastSpawnedAt}ms < ${MIN_REVIEW_SPAWN_INTERVAL_MS}ms)`,
      );
      return;
    }

    // Gate 4：并发锁——同一 sessionKey 下只允许一个活跃 review 子 Agent（O(1)）
    const existing = activeReviews.get(stableKey);
    if (existing) {
      if (now - existing.spawnedAt < ACTIVE_REVIEW_TIMEOUT_MS) {
        api.logger.info(
          `${PLUGIN_TAG} SKIP — active review already running ` +
            `(session=${existing.reviewSessionKey}, age=${now - existing.spawnedAt}ms)`,
        );
        return;
      }
      // 超时的 review 视为僵死，清除锁并继续。
      api.logger.warn(
        `${PLUGIN_TAG} active review timed out after ${now - existing.spawnedAt}ms, ` +
          `clearing stale lock (session=${existing.reviewSessionKey})`,
      );
      // 清理僵死 review 残留的状态，防止 sessionModelInfo / reviewActionCounts /
      // reviewSessionIdentities 泄漏。session_end 对 review 会话跳过了这三项清理
      // （交给埋点路径消费），但超时意味着埋点路径不会再消费它们，必须在此处主动回收。
      sessionModelInfo.delete(existing.reviewSessionKey);
      reviewActionCounts.delete(existing.reviewSessionKey);
      reviewSessionIdentities.delete(existing.reviewSessionKey);
      activeReviews.delete(stableKey);
    }

    const messages = ev.messages ?? [];

    // Gate 5：增量工具调用计数——自上次审查以来新增的 toolCalls 是否达到阈值（O(n) 消息遍历）
    const toolCalls = countToolCalls(messages, excludedToolNames);
    const userTurns = countUserTurns(messages);

    // Compaction 安全：compaction 会压缩/合并消息，导致当前计数低于水位线。
    // 检测到倒挂时重置水位线到当前值，本轮跳过，下一轮从新水位开始增量计数。
    if (toolCalls < state.lastReviewedToolCalls || userTurns < state.lastReviewedTurns) {
      api.logger.info(
        `${PLUGIN_TAG} watermark reset (likely compaction): ` +
          `toolCalls=${toolCalls} (was ${state.lastReviewedToolCalls}), ` +
          `userTurns=${userTurns} (was ${state.lastReviewedTurns})`,
      );
      state.lastReviewedToolCalls = toolCalls;
      state.lastReviewedTurns = userTurns;
      return;
    }

    const newToolCalls = toolCalls - state.lastReviewedToolCalls;

    if (newToolCalls < nudgeInterval) {
      api.logger.info(
        `${PLUGIN_TAG} SKIP — newToolCalls=${newToolCalls} < nudgeInterval=${nudgeInterval} ` +
          `(total=${toolCalls}, lastReviewed=${state.lastReviewedToolCalls})`,
      );
      return;
    }

    // Gate 6.1：累计 userTurns 必须 ≥ MIN_TOTAL_USER_TURNS。
    if (userTurns < MIN_TOTAL_USER_TURNS) {
      api.logger.info(`${PLUGIN_TAG} SKIP — total userTurns=${userTurns} < MIN_TOTAL_USER_TURNS`);
      return;
    }

    // Gate 6：增量审查——仅在有足够新增用户轮次时触发（O(n) 消息遍历）
    if (userTurns < state.lastReviewedTurns + MIN_NEW_TURNS) {
      api.logger.info(
        `${PLUGIN_TAG} SKIP — insufficient new user turns ` +
          `(current=${userTurns}, lastReviewed=${state.lastReviewedTurns}, need +${MIN_NEW_TURNS})`,
      );
      return;
    }

    // 所有门通过前的最后一道 fail-fast 校验：parentKey 必须存在。
    // 必须放在水位线/时间戳提交之前，否则 sessionKey 缺失时会污染 state，
    // 导致后续同一 fallback key（sessionId / "unknown"）下次 review 被错误跳过。
    const parentKey = cx.sessionKey;
    if (!parentKey) {
      api.logger.info(`${PLUGIN_TAG} SKIP — no sessionKey available for parent session`);
      return;
    }

    // 所有门通过：拉起后台审查，更新水位线和触发时间戳
    state.lastReviewedTurns = userTurns;
    state.lastReviewedToolCalls = toolCalls;
    state.lastSpawnedAt = now;

    // 插入 UUID 段，避免多 session 并发时不同父会话在相同 userTurns 触发 review 撞 key。
    const reviewUuid = crypto.randomUUID();
    const reviewSessionKey = `agent:${cx.agentId ?? "main"}:${SUBAGENT_SESSION_TAIL}:${reviewUuid}:t${userTurns}`;

    // 读取（在锁建立前先快照）上一次 review 留下的 handoff 文本 + 已沉淀水位线。
    const priorHandoff = state.lastSedimentHandoff;
    const priorMessageCount = state.lastSedimentedMessageCount;

    api.logger.info(
      `${PLUGIN_TAG} spawning background skill review ` +
        `(toolCalls=${toolCalls}, userTurns=${userTurns}, ` +
        `priorWatermark=${priorMessageCount}, priorHandoff=${priorHandoff ? `${priorHandoff.length}chars` : "(none)"}, ` +
        `reviewSession=${reviewSessionKey})`,
    );

    // Fire-and-forget：异步拉起审查子 Agent
    void (async () => {
      try {
        // 1) 获取父会话完整消息
        const { messages: parentMessages } = await api.runtime.subagent.getSessionMessages({
          sessionKey: parentKey,
        });

        // 2) 按水位线切片：
        //    - 若有 priorMessageCount > 0：拼 [head(1 条 anchor user)] + tail [priorMessageCount, end)
        //    - 否则：原样全量传入
        //    head 保留首条 user 作为"会话起点诉求"锚点，让 review LLM 始终能看到用户真正想做什么，避免只看到中段对话时误判 trigger。
        let slicedMessages: unknown[] = parentMessages;
        let sliceDescription = `full(${parentMessages.length})`;
        if (
          priorMessageCount > 0 &&
          priorMessageCount < parentMessages.length &&
          Array.isArray(parentMessages)
        ) {
          const head = parentMessages.slice(0, 1);
          const tail = parentMessages.slice(priorMessageCount);
          // 避免 anchor 与 tail 第一条重合（极端：priorMessageCount=1 时切重）
          slicedMessages = tail[0] === head[0] ? tail : ([...head, ...tail] as unknown[]);
          sliceDescription = `head(1)+tail[${priorMessageCount},${parentMessages.length})=${slicedMessages.length}`;
        }

        // 3) 精简为紧凑文本上下文
        const condensed = buildCondensedContext(slicedMessages);
        api.logger.info(
          `${PLUGIN_TAG} condensed context built: ${condensed.length} chars ` +
            `(messages: ${sliceDescription})`,
        );

        // 4) 拼装最终 message：可选 prior_sediment_handoff 块 + conversation_context
        const finalMessage = priorHandoff
          ? `<prior_sediment_handoff>\n${priorHandoff}\n</prior_sediment_handoff>\n\n${condensed}`
          : condensed;

        // 5) 注册并发锁（包含水位线推进所需的字段）
        activeReviews.set(stableKey, {
          spawnedAt: now,
          reviewSessionKey,
          parentAgentId: cx.agentId ?? "",
          parentSessionId: cx.sessionId ?? "",
          parentSessionKey: cx.sessionKey ?? "",
          pendingSedimentCount: parentMessages.length,
          parentStableKey: stableKey,
        });

        // 6) 拉起审查子 Agent
        await api.runtime.subagent.run({
          sessionKey: reviewSessionKey,
          message: finalMessage,
          extraSystemPrompt: buildSkillReviewPrompt({ hasPriorHandoff: Boolean(priorHandoff) }),
          lane: "subagent",
          deliver: false,
          idempotencyKey: `skill-review:${parentKey ?? "unknown"}:turns-${userTurns}`,
        });
        api.logger.info(`${PLUGIN_TAG} background review dispatched (session=${reviewSessionKey})`);
      } catch (err) {
        // 失败时释放并发锁
        activeReviews.delete(stableKey);
        api.logger.warn(`${PLUGIN_TAG} background review failed: ${String(err)}`);
      }
    })();
  }

  // ─── 返回钩子处理器 ──────────────────────────────────────────────

  return {
    /**
     * 反查给定 review subagent 的父会话 sessionKey。
     *
     * 用于 `index.ts` 在 `skill_manage` 工具 execute 中把父会话身份透传给
     * `SkillDirs.parentSessionKey`，供：
     *   - `createSkill` 写入 sediment 的 `createdInParentSession`（出生证明）
     *   - `promoteSkill` 实施"跨父会话守卫"
     */
    getParentSessionKeyForReview(reviewSessionKey: string | undefined): string | undefined {
      if (!reviewSessionKey) {
        return undefined;
      }
      for (const info of activeReviews.values()) {
        if (info.reviewSessionKey === reviewSessionKey) {
          return info.parentSessionKey || undefined;
        }
      }
      return undefined;
    },

    /** 跟踪 review session 的 skill_manage 调用计数。由 skill_manage 工具执行后调用。 */
    trackReviewAction(
      sessionKey: string | undefined,
      action: string,
      success: boolean,
      resultPath: string | undefined,
      paramName: string | undefined,
    ): void {
      if (!isSkillReviewSession(sessionKey)) {
        return;
      }
      const key = sessionKey!;
      const counts: ReviewActionCounts = reviewActionCounts.get(key) ?? {
        actions: 0,
        creates: 0,
        edits: 0,
        patches: 0,
        deletes: 0,
        writeFiles: 0,
        removeFiles: 0,
        promotes: 0,
        views: 0,
        skillNames: new Set<string>(),
      };
      if (action === "list" || action === "view") {
        counts.views += 1;
      } else if (success) {
        counts.actions += 1;
        switch (action) {
          case "create":
            counts.creates += 1;
            break;
          case "edit":
            counts.edits += 1;
            break;
          case "patch":
            counts.patches += 1;
            break;
          case "delete":
            counts.deletes += 1;
            break;
          case "write_file":
            counts.writeFiles += 1;
            break;
          case "remove_file":
            counts.removeFiles += 1;
            break;
          case "promote":
            counts.promotes += 1;
            break;
          // 其它未知 action 不细分（actions 已 +1，但不归类）。
        }
        // 优先使用 typedParams.name（纯技能名），回退到 result.path 的 basename。
        //
        // 注意：result.path 在不同 action 下含义不同（且都不适合直接当作技能名）：
        //   - create/edit: path.relative(displayBase, skillDir) → "foo" 或 "category/foo"
        //     （displayBase 取沉淀目录或正式目录，视技能落点而定；当目录存在 category 嵌套时
        //     会出现带斜杠的复合路径，例如 "sediment/foo"）
        //   - write_file: path.relative(displayBase, target) → "foo/references/x.md" (含文件子路径)
        //   - view: 绝对路径（但 view 走 views 分支，不会进入此处）
        //   - patch/delete/remove_file: 未设置
        // 历史实现 `resultPath ?? paramName` 会把上述复合路径写入 skillNames，
        // 导致最终 skill_name 埋点出现 "sediment/xxx" 或 "xxx/references/y.md" 等异常值。
        let actualName = paramName;
        if (!actualName && resultPath) {
          // 回退场景：取 path 的最后一段（technically 目录名），并去除可能残留的 sediment- 前缀
          const segments = resultPath.split(/[/\\]/).filter(Boolean);
          actualName = segments[segments.length - 1]?.replace(/^sediment-/, "");
        }
        if (actualName) {
          counts.skillNames.add(actualName);
        }
      }
      reviewActionCounts.set(key, counts);
    },

    /**
     * llm_input 钩子处理器：在请求构造阶段就把 model 写入缓存。
     */
    handleLlmInput(_event: unknown, ctx: unknown): void {
      const ev = _event as { model?: string };
      const cx = ctx as { sessionId?: string; sessionKey?: string };
      const stableKey = cx.sessionKey ?? cx.sessionId;
      if (!stableKey) {
        return;
      }
      // 仅父会话路径：subagent / cron / group 不参与白名单判断
      if (isSkillReviewSession(stableKey) || isNotUserSession(stableKey)) {
        return;
      }
      if (ev.model) {
        parentSessionModel.set(stableKey, ev.model);
      }
    },

    /** llm_output 钩子处理器：按 sessionKey 缓存 LLM 模型信息 + 累计 token 用量。 */
    handleLlmOutput(_event: unknown, ctx: unknown): void {
      const ev = _event as {
        model?: string;
        usage?: {
          input?: number;
          output?: number;
          cacheRead?: number;
          cacheWrite?: number;
          total?: number;
        };
      };
      const cx = ctx as { sessionId?: string; sessionKey?: string; agentId?: string };
      const stableKey = cx.sessionKey ?? cx.sessionId;
      if (!stableKey) {
        return;
      }

      // 父会话路径：仅缓存最近一次 model 名，用于 spawnSkillReview 的 Gate 0 白名单判断。
      if (!isSkillReviewSession(stableKey)) {
        if (!isNotUserSession(stableKey) && ev.model) {
          parentSessionModel.set(stableKey, ev.model);
        }
        return;
      }

      // 记录 review 子 Agent 自己的 (sessionId, agentId)，供 subagent_ended 路径反查使用。
      // 只在第一次见到该 reviewSessionKey 时写入；后续 streaming 事件不重复覆盖（开销 O(1)）。
      // 缺 sessionId / agentId 时直接跳过——subagent_ended 路径会自行降级日志告警。
      if (cx.sessionId && cx.agentId && !reviewSessionIdentities.has(stableKey)) {
        reviewSessionIdentities.set(stableKey, {
          sessionId: cx.sessionId,
          agentId: cx.agentId,
        });
      }

      const existing = sessionModelInfo.get(stableKey);
      // model 名称：有值时更新，无值时保留上一次记录的 model（某些 streaming 中间事件可能不带 model）。
      // 关键：即使 model 暂时为空，也要继续累加 usage —— 否则 token 会丢失。
      const model = ev.model || existing?.model || "";
      const addInput = ev.usage?.input ?? 0;
      const addOutput = ev.usage?.output ?? 0;
      const addCacheRead = ev.usage?.cacheRead ?? 0;
      const addCacheWrite = ev.usage?.cacheWrite ?? 0;
      const next: SessionModelInfo = {
        model,
        tokensInput: (existing?.tokensInput ?? 0) + addInput,
        tokensOutput: (existing?.tokensOutput ?? 0) + addOutput,
        tokensCacheRead: (existing?.tokensCacheRead ?? 0) + addCacheRead,
        tokensCacheWrite: (existing?.tokensCacheWrite ?? 0) + addCacheWrite,
      };
      sessionModelInfo.set(stableKey, next);

      // 调试日志：review 子 Agent 触发时输出，便于核对埋点字段是否取到。
      // 注：此处已在 isSkillReviewSession 守卫之后，无需再次检查。
      api.logger.debug?.(
        `${PLUGIN_TAG} llm_output captured for review session=${stableKey}: ` +
          `model="${model}", usagePresent=${ev.usage !== undefined}, ` +
          `delta(input=${addInput}, output=${addOutput}, cacheRead=${addCacheRead}, cacheWrite=${addCacheWrite}), ` +
          `total(input=${next.tokensInput}, output=${next.tokensOutput}, cacheRead=${next.tokensCacheRead}, cacheWrite=${next.tokensCacheWrite})`,
      );
    },

    /** session_end / before_reset 钩子处理器：清理会话级状态。 */
    cleanupSession(stableKey: string | undefined, sessionId: string | undefined): void {
      if (stableKey) {
        // skill-review 子 Agent 的 session_end 可能先于 agent_end / subagent_ended 触发，
        // 如果此时清理 sessionModelInfo 和 reviewActionCounts，埋点路径读到的就是 undefined，
        // 导致 llm_model/tokens_*/outcome/creates 等字段全部为默认空值。
        // 因此对 skill-review 会话跳过这两项清理，交给埋点路径消费后自行 delete。
        const isReview = isSkillReviewSession(stableKey);
        sessionStates.delete(stableKey);
        if (!isReview) {
          // 同步清理 checkpoint 文件中对应条目，避免重启后恢复已结束会话的水位线。
          // review 子会话的 key 不在 checkpoint 中，无需清理。
          try {
            removeCheckpointEntry(getSedimentDir(), stableKey);
          } catch {
            // 静默降级：checkpoint 清理失败不影响主流程，过期条目会被 TTL 自动回收。
          }
          // 注：reviewSessionIdentities 按 review subagent sessionKey 索引，
          // 父会话清理路径（!isReview 分支）下 stableKey 恒为父会话 key，与
          // identities 的索引域不相交——无需在此清理。Identity 清理由埋点路径
          // （Gate 1 phaseB / subagent_ended / Gate 4 超时）三端各自负责。
          sessionModelInfo.delete(stableKey);
          reviewActionCounts.delete(stableKey);
        }
        // 注意：不在此处清理 activeReviews——父会话的 session_end 可能先于 review
        // 子 Agent 完成（agent_end / subagent_ended）触发。如果此时删除 activeReviews
        // 条目，完成路径将无法反查 parentInfo，导致 aimi 上报和 UBA 埋点静默丢失。
        // activeReviews 的生命周期完全由完成路径（Gate 1 / subagent_ended）和
        // Gate 4 超时清理管理，条目最多存活 ACTIVE_REVIEW_TIMEOUT_MS，不会无界增长。
        parentSessionModel.delete(stableKey);
        // 注意：不在此处清理 handledReviewSessions——session_end 可能在 agent_end 和
        // subagent_ended 之间触发，过早删除互斥标志会导致后到的路径重复处理并发送重复埋点。
        // handledReviewSessions 使用 TTL 惰性清理（sweepHandledReviewSessions）。
        api.logger.debug?.(
          `${PLUGIN_TAG} session cleanup: session=${stableKey}${isReview ? " (kept modelInfo+actionCounts for telemetry)" : ""}`,
        );
      }
      // 兼容：同时尝试按 sessionId 清理（以防旧状态残留）
      if (sessionId && sessionId !== stableKey) {
        sessionStates.delete(sessionId);
        sessionModelInfo.delete(sessionId);
        parentSessionModel.delete(sessionId);
      }
    },

    /** agent_end 钩子处理器：触发后台审查。 */
    handleAgentEnd: spawnSkillReview,

    /** subagent_ended 钩子处理器：记录审查子 Agent 完成日志 + 埋点 + 锁释放。 */
    async handleSubagentEnded(event: unknown): Promise<void> {
      const ev = event as {
        targetSessionKey?: string;
        targetKind?: string;
        reason?: string;
        durationMs?: number;
        outcome?: string;
      };
      // 仅处理本插件创建的 skill-review 子会话
      if (!isSkillReviewSession(ev.targetSessionKey)) {
        return;
      }

      // 让出微任务队列，确保 llm_output 钩子的 fire-and-forget handler
      // 已经把本次 review 的 model + usage 累加到 sessionModelInfo 中。
      await waitForLlmOutputDrain();

      // 显式互斥检查：如果 Gate 1 路径已经处理过，跳过
      if (handledReviewSessions.has(ev.targetSessionKey!)) {
        api.logger.debug?.(
          `${PLUGIN_TAG} subagent_ended: skipping — already handled by gate1 path ` +
            `(session=${ev.targetSessionKey})`,
        );
        return;
      }
      // 写入前顺手 sweep（自带 5 分钟节流），保证条目按 TTL 清理。
      sweepHandledReviewSessions();
      handledReviewSessions.set(ev.targetSessionKey!, Date.now());

      // 从 activeReviews 反查父会话信息，用于埋点关联。
      let parentInfo: ActiveReviewInfo | undefined;
      let parentLockKey: string | undefined;
      for (const [key, info] of activeReviews) {
        if (info.reviewSessionKey === ev.targetSessionKey) {
          parentInfo = info;
          parentLockKey = key;
          break;
        }
      }
      if (!parentInfo) {
        // 顺手清理 identity，与 Gate 4 / Gate 1 路径行为对齐，避免泄漏。
        reviewSessionIdentities.delete(ev.targetSessionKey!);
        api.logger.debug?.(
          `${PLUGIN_TAG} subagent_ended: skipping — no parent info found ` +
            `(activeReviews already cleaned up, session=${ev.targetSessionKey})`,
        );
        return;
      }

      // 抓取 <sediment_handoff> 并推进父 state 水位线（fail-safe：未命中不推进）。
      // 必须放在埋点 + 锁释放之前——captureHandoffAndAdvance 内部走 parentStableKey
      // 反查 sessionStates，与 activeReviews 锁释放顺序无关。
      await captureHandoffAndAdvance(ev.targetSessionKey!, parentInfo);

      // 输出 review 结果摘要
      const counts = reviewActionCounts.get(ev.targetSessionKey!);
      reviewActionCounts.delete(ev.targetSessionKey!);
      const outcomeLabel = buildOutcomeLabel(counts);

      api.logger.info(
        `${PLUGIN_TAG} subagent_ended: skill-review subagent completed ` +
          `(session=${ev.targetSessionKey}, reason=${ev.reason ?? "unknown"}, ` +
          `duration=${ev.durationMs ?? "?"}ms, outcome=${outcomeLabel})`,
      );

      // 上报到 aimi 后端：与 Gate 1 路径对称——subagent_ended 先到时也必须能独立完成上报，
      // 否则会因事件顺序竞态丢上报。reviewSessionIdentities 由 handleLlmOutput 钩子在
      // review session 第一次出 LLM 输出时填入；缺标识则在 helper 内降级为告警日志。
      const identity = reviewSessionIdentities.get(ev.targetSessionKey!);
      reviewSessionIdentities.delete(ev.targetSessionKey!);
      const hasSkillChanges = Boolean(counts && (counts.creates > 0 || counts.promotes > 0));
      reportReviewToAimi(api, {
        reviewSessionKey: ev.targetSessionKey!,
        reviewSessionId: identity?.sessionId,
        reviewAgentId: identity?.agentId,
        parentInfo,
        hasSkillChanges,
        outcomeLabel,
        actions: counts?.actions ?? 0,
        pathTag: "subagent_ended",
      });

      // 埋点: review_completed —— 审查子 Agent 完成时上报
      const modelInfo = sessionModelInfo.get(ev.targetSessionKey!);
      sessionModelInfo.delete(ev.targetSessionKey!);
      sendReviewCompletedEvent(api, {
        parentAgentId: parentInfo.parentAgentId,
        parentSessionKey: parentInfo.parentSessionKey,
        parentSessionId: parentInfo.parentSessionId,
        reviewSessionKey: ev.targetSessionKey ?? "",
        reason: ev.reason ?? "unknown",
        outcomeLabel,
        durationMs: ev.durationMs ?? 0,
        creates: counts?.creates ?? 0,
        edits: counts?.edits ?? 0,
        patches: counts?.patches ?? 0,
        deletes: counts?.deletes ?? 0,
        writeFiles: counts?.writeFiles ?? 0,
        removeFiles: counts?.removeFiles ?? 0,
        promotes: counts?.promotes ?? 0,
        skillNames: counts ? [...counts.skillNames] : [],
        model: modelInfo?.model,
        tokensInput: modelInfo?.tokensInput,
        tokensOutput: modelInfo?.tokensOutput,
        tokensCacheRead: modelInfo?.tokensCacheRead,
        tokensCacheWrite: modelInfo?.tokensCacheWrite,
      });

      // 清除并发锁
      if (parentLockKey) {
        activeReviews.delete(parentLockKey);
        api.logger.debug?.(
          `${PLUGIN_TAG} subagent_ended: released active review lock for session=${parentLockKey}`,
        );
      }
    },
  };
}
