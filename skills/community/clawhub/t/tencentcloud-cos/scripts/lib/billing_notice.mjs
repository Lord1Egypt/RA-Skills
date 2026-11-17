#!/usr/bin/env node
/**
 * 数据万象（CI）/ 智能检索（MetaInsight）计费提示协议。
 *
 * 仅在严格模式（KIKI=1）下生效：首次执行计费类动作时暂停，产出
 * requestBillingNotice 客户端交互请求；配套工作台确认后，将原 invokeClient
 * 工具结果作为 --billing-confirmation 回填，本模块记录确认状态并放行原动作。
 *
 * 与 CI 开通协议同原则：
 * - 回执只是「用户已知悉计费」的确认记录，不是云上授权凭证；
 * - 确认状态文件只保存非敏感的确认标记，不保存任何凭证；
 * - 公开模式不拦截，费用由 SKILL.md 的静态说明兜底。
 */

import { existsSync, readFileSync, writeFileSync, chmodSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { isStrictMode } from './ci_client.mjs';

export const BILLING_NOTICE_CONTRACT_VERSION = 1;
export const BILLING_NOTICE_SKILL = 'tencentcloud-cos';
export const BILLING_NOTICE_ACTION = 'requestBillingNotice';

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

/**
 * cos_node.mjs 中会产生数据万象 / 智能检索费用的动作。
 * 只读状态查询（describe-* / list-* / ci-service-status）与 COS 存储操作不在此列。
 */
export const BILLED_ACTIONS = Object.freeze([
  // 同步图片处理与 AI 图片处理
  'image-info',
  'image-thumbnail',
  'image-crop',
  'image-rotate',
  'image-format',
  'watermark-font',
  'assess-quality',
  'ai-super-resolution',
  'ai-pic-matting',
  'ai-qrcode',
  // 同步内容识别
  'recognize-image',
  'ocr-general',
  // 文档处理
  'create-doc-to-pdf-job',
  'doc-preview',
  'doc-preview-html-url',
  // 媒体处理
  'create-media-smart-cover-job',
  'media-transcode-job',
  'media-snapshot',
  'media-info',
  // 内容审核
  'audit-image',
  'audit-image-job',
  'audit-video-job',
  'audit-audio-job',
  'audit-text-job',
  'audit-document-job',
  // 智能语音
  'speech-recognition-job',
  'tts-job',
  'noise-reduction-job',
  'voice-separate-job',
  // 文件处理
  'file-hash',
  'file-compress-job',
  'file-uncompress-job',
  // MetaInsight 数据集写入与检索
  'create-dataset',
  'create-dataset-binding',
  'create-file-meta-index',
  'image-search-pic',
  'image-search-text',
  'face-search',
  'dataset-simple-query',
  'hybrid-search',
  'video-search',
  // 快捷功能（内部创建数据集并绑定）
  'create-knowledge-base',
]);

/** ci_api.mjs 中的计费类检索 / 识别命令。 */
export const BILLED_CI_API_COMMANDS = Object.freeze([
  'simple-query',
  'image-search',
  'doc-search',
  'video-search',
  'face-search',
  'face-clip-search',
  'get-ai-media-info',
  'image-analysis',
  'image-exif',
]);

/**
 * 计费动作判定。ci-request 扩展入口不拦截：开通等价请求必须优先进入开通预检流程，
 * 且 SKILL.md 已要求优先使用已封装的专用 action（均在上方集合内）。
 */
export function isBilledAction(action) {
  const name = String(action || '');
  return BILLED_ACTIONS.includes(name) || BILLED_CI_API_COMMANDS.includes(name);
}

function getAckStatePath(env = process.env) {
  const override = String(env.TENCENT_COS_BILLING_STATE_FILE || '').trim();
  return override || resolve(skillRoot, '.billing-notice-ack.json');
}

/** 读取确认标记；文件缺失或内容不合法都视为未确认，不做任何猜测。 */
export function readBillingAck(env = process.env) {
  const statePath = getAckStatePath(env);
  if (!existsSync(statePath)) return null;
  try {
    const parsed = JSON.parse(readFileSync(statePath, 'utf-8'));
    if (
      parsed &&
      parsed.version === BILLING_NOTICE_CONTRACT_VERSION &&
      typeof parsed.ackedAt === 'string' &&
      parsed.ackedAt.trim()
    ) {
      return { ackedAt: parsed.ackedAt, statePath };
    }
  } catch {
    // fall through: treat unreadable state as not acknowledged
  }
  return null;
}

/**
 * 校验工作台回填的原始 invokeClient 工具结果。
 * 字段集合固定且 status 必须为 confirmed；cancelled 等其他回执不放行。
 */
export function validateBillingNoticeConfirmation(value) {
  let decision = value;
  if (typeof value === 'string' && value.length <= 4096) {
    try { decision = JSON.parse(value); } catch { decision = null; }
  }
  const fields = ['type', 'version', 'status', 'toolCallId'];
  if (!decision || typeof decision !== 'object' || Array.isArray(decision)
    || Object.keys(decision).length !== fields.length || !fields.every(key => Object.hasOwn(decision, key))
    || decision.type !== 'billing_notice_decision'
    || decision.version !== BILLING_NOTICE_CONTRACT_VERSION
    || decision.status !== 'confirmed'
    || typeof decision.toolCallId !== 'string' || !decision.toolCallId.trim()
    || decision.toolCallId !== decision.toolCallId.trim() || decision.toolCallId.length > 512) {
    const error = new Error('billing notice requires the confirmed result of the original client interaction');
    error.code = 'InvalidBillingNoticeConfirmation';
    throw error;
  }
  return { ...decision };
}

/**
 * 记录确认标记（权限 600）。写入失败不阻断已确认的执行，仅返回 ackPersisted=false。
 */
export function recordBillingAck(decision, env = process.env) {
  const statePath = getAckStatePath(env);
  const payload = {
    version: BILLING_NOTICE_CONTRACT_VERSION,
    ackedAt: new Date().toISOString(),
    toolCallId: decision.toolCallId,
  };
  try {
    writeFileSync(statePath, `${JSON.stringify(payload, null, 2)}\n`, { mode: 0o600 });
    chmodSync(statePath, 0o600);
    return { ackPersisted: true, statePath };
  } catch {
    return { ackPersisted: false, statePath };
  }
}

/** 生成版本化的客户端交互请求；command 固定序列化，调用方不得改写。 */
export function buildBillingNoticeRequest(trigger) {
  const interaction = {
    type: 'billing_notice',
    version: BILLING_NOTICE_CONTRACT_VERSION,
    status: 'requires_confirmation',
    trigger: String(trigger || ''),
  };
  return {
    interaction,
    // bash stdout 只有模型可见，UI 流可能只拿到长度摘要；必须经 invokeClient 原样转发。
    clientAction: {
      skill: BILLING_NOTICE_SKILL,
      command: JSON.stringify({ action: BILLING_NOTICE_ACTION, ...interaction }),
    },
  };
}

/**
 * 计费提示门禁判定。返回：
 * - null：无需拦截（非严格模式、非计费动作、已确认过，或 TENCENT_COS_BILLING_ACK=1）
 * - { billingStatus: 'confirmed', ackPersisted }：回执有效，已记录确认，放行
 * - { billingStatus: 'requires_confirmation', interaction, clientAction }：暂停并下发交互
 */
export function evaluateBillingNotice({ action, confirmation, env = process.env }) {
  if (!isStrictMode(env)) return null;
  if (!isBilledAction(action)) return null;
  // 自动化 / 非交互环境显式跳过；等价于用户已在环境层面知悉计费。
  if (String(env.TENCENT_COS_BILLING_ACK || '').trim() === '1') return null;
  if (confirmation !== undefined) {
    const decision = validateBillingNoticeConfirmation(confirmation);
    const ack = recordBillingAck(decision, env);
    return { billingStatus: 'confirmed', toolCallId: decision.toolCallId, ackPersisted: ack.ackPersisted };
  }
  if (readBillingAck(env)) return null;
  return { billingStatus: 'requires_confirmation', ...buildBillingNoticeRequest(action) };
}
