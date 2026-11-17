/**
 * Jev 判定策略（纯函数，可离线测试）。
 *
 * 判定目标：小爱音箱的每条语音转写，是否应转发给外部 AI Agent 处理。
 *
 * 一次 Jev 调用携带两道 noul 题（共享同一段 state）：
 * - shouldForward：应转发给外部 AI Agent 的概率（0-1）；
 * - isNativeCapability：小爱音箱原生即可完成的概率（0-1）。
 *
 * 决策规则（按挡位）：
 *   forward = shouldForward ≥ forwardThreshold
 *             AND NOT (isNativeCapability ≥ nativeVeto AND shouldForward < explicitIntent)
 * 即：达到转发阈值才转发；但“明显是小爱原生任务”会被否决，
 * 除非转发意图高到「显式豁免线」（用户明确点名要外部 AI 处理）。
 *
 * 挡位同时决定发给 Jev 的判定说明文案：宽松挡倾向转发，
 * 严格挡仅在高置信度或用户明确点名时转发。
 */

import { JevError } from "./errors.js";

/** 判定问题 ID：Jev 响应的 answers 以此为键。 */
export const JEV_QUESTION_FORWARD = "shouldForward";
export const JEV_QUESTION_NATIVE = "isNativeCapability";

/**
 * 挡位矩阵。
 * - forwardThreshold：转发所需的最低「应转发」概率；
 * - nativeVeto：「原生可完成」概率达到该值即否决；
 * - explicitIntent：应转发概率达到该值时豁免原生否决（用户明确点名外部 AI）。
 */
export const JEV_DECISION_GEAR = {
  loose: { forwardThreshold: 0.35, nativeVeto: 0.9, explicitIntent: 0.9 },
  balanced: { forwardThreshold: 0.6, nativeVeto: 0.8, explicitIntent: 0.9 },
  strict: { forwardThreshold: 0.8, nativeVeto: 0.6, explicitIntent: 0.95 },
};

/** 小爱音箱原生能力描述（进入 state，供判定模型对照）。 */
export const XIAOAI_NATIVE_ABILITIES =
  "控制智能家居家电（开关灯/空调/窗帘等）、播放或暂停音乐、调节音量、查询天气、设置闹钟与提醒、简单寒暄闲聊";

/** 外部 AI Agent 能力描述（进入 state，供判定模型对照）。 */
export const AGENT_ABILITIES =
  "开放域知识问答、写作/翻译/总结、复杂推理与规划、代码相关任务、多步骤任务编排，以及其他超出音箱原生能力的请求";

const FORWARD_INSTRUCTIONS = {
  loose:
    "判断这条语音是否应该转发给外部 AI Agent 处理。只要不是明确由小爱音箱原生完成的指令，就倾向于转发，包括内容不清晰但可能需要智能处理的请求。",
  balanced:
    "判断这条语音是否应该转发给外部 AI Agent 处理。小爱音箱原生可完成的指令（控制家电、播放音乐、查天气、设闹钟、闲聊）不应转发；只有需要外部 AI 能力、或用户明确要求 AI 助手处理时才转发。",
  strict:
    "判断这条语音是否应该转发给外部 AI Agent 处理。仅当用户明确要求外部 AI 助手处理，或任务明显超出小爱音箱原生能力且需要复杂智能时才转发；不确定时倾向不转发。",
};

const NATIVE_INSTRUCTIONS =
  "判断这条语音是否属于小爱音箱原生即可完成的任务（控制家电、播放音乐、查天气、设闹钟、闲聊等）。原生可完成则概率应接近 1。";

/**
 * 构造发送给 Jev 的 state（背景与待判断内容）。
 *
 * 注意：state 只包含完成判定所必需的转写文本与能力边界说明，
 * 不包含账号、设备、位置等任何额外信息。
 *
 * @param {{ query: string, prefix?: string, prefixMatched?: boolean }} options
 */
export function buildJevState({ query, prefix = "", prefixMatched = false }) {
  const lines = [
    "场景：用户正在与小米小爱音箱对话，需要决定这条语音由音箱原生处理，还是转发给外部 AI Agent。",
    `用户对音箱说：「${query}」`,
  ];
  if (prefixMatched && prefix) {
    lines.push(`用户使用了专用触发前缀「${prefix}」，这通常表示希望交给外部 AI 助手处理。`);
  } else {
    lines.push("用户未使用任何触发前缀。");
  }
  lines.push(`小爱音箱原生能力：${XIAOAI_NATIVE_ABILITIES}。`);
  lines.push(`外部 AI Agent 能力：${AGENT_ABILITIES}。`);
  return lines.join("\n");
}

/**
 * 构造一次 Jev 判定调用的 questions（两道 noul 题）。
 *
 * @param {"loose" | "balanced" | "strict"} level
 */
export function buildJevQuestions(level) {
  const gearLevel = JEV_DECISION_GEAR[level] ? level : "balanced";
  return {
    [JEV_QUESTION_FORWARD]: {
      type: "noul",
      instructions: FORWARD_INSTRUCTIONS[gearLevel],
    },
    [JEV_QUESTION_NATIVE]: {
      type: "noul",
      instructions: NATIVE_INSTRUCTIONS,
    },
  };
}

/**
 * 从 Jev 响应的单个答案中提取 noul 概率（0-1）。
 *
 * 宽容解析：优先读 noul 字段（文档约定），兼容 probability / p 变体。
 *
 * @param {unknown} answer
 * @param {string} questionId
 * @returns {number}
 */
export function extractNoul(answer, questionId) {
  const probability =
    typeof answer === "object" && answer !== null
      ? answer.noul ?? answer.probability ?? answer.p
      : undefined;
  if (typeof probability !== "number" || !Number.isFinite(probability) || probability < 0 || probability > 1) {
    throw new JevError(`Jev 响应缺少问题「${questionId}」的有效概率`, { category: "protocol" });
  }
  return probability;
}

/**
 * 依据挡位策略对一次 Jev 响应做转发决策。
 *
 * @param {{ shouldForward: number, isNativeCapability: number }} probabilities
 * @param {"loose" | "balanced" | "strict"} level
 * @param {{ decisionThreshold?: number }} [options] decisionThreshold 覆盖挡位默认阈值
 */
export function decideForward(probabilities, level, options = {}) {
  const gearLevel = JEV_DECISION_GEAR[level] ? level : "balanced";
  const gear = JEV_DECISION_GEAR[gearLevel];
  const threshold = typeof options.decisionThreshold === "number" ? options.decisionThreshold : gear.forwardThreshold;

  const shouldForward = probabilities.shouldForward;
  const isNativeCapability = probabilities.isNativeCapability;

  const meetsThreshold = shouldForward >= threshold;
  const nativeVetoed = isNativeCapability >= gear.nativeVeto && shouldForward < gear.explicitIntent;

  let reason;
  if (!meetsThreshold) {
    reason = `应转发概率 ${formatProb(shouldForward)} < 阈值 ${formatProb(threshold)}`;
  } else if (nativeVetoed) {
    reason = `原生能力否决（原生概率 ${formatProb(isNativeCapability)} ≥ ${formatProb(gear.nativeVeto)}，且应转发概率 ${formatProb(shouldForward)} < 显式豁免线 ${formatProb(gear.explicitIntent)}）`;
  } else {
    reason = `应转发概率 ${formatProb(shouldForward)} ≥ 阈值 ${formatProb(threshold)}`;
  }

  return {
    forward: meetsThreshold && !nativeVetoed,
    reason,
    shouldForward,
    isNativeCapability,
    threshold,
    level: gearLevel,
    nativeVetoed,
  };
}

function formatProb(value) {
  return Number(value).toFixed(2);
}
