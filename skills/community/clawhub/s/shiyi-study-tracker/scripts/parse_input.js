/**
 * parse_input.js
 * 消息解析 + 多模态图片识别（自由标签模式）。
 *
 * 与朱批录的核心差异：
 *   - 不预设科目映射，标签完全由 AI 自由生成
 *   - 识别前查 tag_library 注入已有标签（提升复用率）
 *   - 识别后写 tag_library（积累词库）
 *   - 支持所有考试类型
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const { handleOnboarding, isSetupDone, getExamKey, getExamName, handleChangeExam } = require('./onboarding');
const { getTagsForPrompt, updateTagLibrary }  = require('./tag_library');
const { resolveExam }                          = require('../assets/exam_prompts');
const { handleReviewReply }                    = require('./review_reminder');

// ─── 识别 prompt ──────────────────────────────────────────────

function buildPrompt(examKey, examName, tagHint) {
  const { prompt: examContext } = resolveExam(examName || examKey);

  return `
你是一个考试备考助手，正在分析用户发来的错题截图。
考试类型：${examName || examKey}

${examContext}

${tagHint ? tagHint + '\n' : ''}
请从图片中提取以下信息，严格以 JSON 格式返回，不要有任何额外说明。

重要：所有字段必须完整输出，禁止使用省略号截断内容。

{
  "section": "科目/大类（如 Verbal、高等数学、阅读理解）",
  "question_type": "题目类型（如 Text Completion、T/F/NG、选择题）",
  "knowledge_point": "具体知识点或考点（尽量具体，优先复用已有标签）",
  "question_text": "【完整】题目文字；图形题写规律描述；图表题写标题+核心数据",
  "visual_description": "【完整】图形/图表的详细视觉描述，纯文字题填 null",
  "answer": "正确答案，图片中若不可见则填 null",
  "user_annotation": "用户手写批注，没有填 null",
  "error_reason": "知识点不会 / 粗心 / 时间不够 / 概念混淆 / 无法判断",
  "keywords": ["知识点标签，最多3个，优先复用已有标签"]
}

如果图片模糊无法识别，返回：{"error": "图片无法识别"}
`.trim();
}

// ─── 图片识别 ─────────────────────────────────────────────────

async function parseImageInput(imageBase64, caption, agentCall) {
  if (typeof agentCall !== 'function') {
    return {
      success:         false,
      error:           'no_vision',
      fallback_prompt: '没识别出来，可以把题目文字复制过来发给我，一样能整理。',
    };
  }

  const examKey  = getExamKey();
  const examName = getExamName();
  const tagHint  = getTagsForPrompt(examKey);
  const prompt   = buildPrompt(examKey, examName, tagHint);
  const fullPrompt = caption
    ? `${prompt}\n\n用户附带说明：「${caption}」`
    : prompt;

  try {
    const raw    = await agentCall({ image: imageBase64, text: fullPrompt });
    const parsed = JSON.parse((raw || '').replace(/```json|```/g, '').trim());
    if (parsed.error) throw new Error(parsed.error);

    // 写入词库
    updateTagLibrary(examKey, {
      question_type:   parsed.question_type,
      knowledge_point: parsed.knowledge_point,
    });

    return {
      success:            true,
      date:               new Date().toISOString().slice(0, 10),
      source:             'image',
      exam:               examKey,
      exam_name:          examName,
      section:            parsed.section            ?? '',
      question_type:      parsed.question_type      ?? '',
      knowledge_point:    parsed.knowledge_point    ?? '',
      question_text:      parsed.question_text      ?? '',
      visual_description: parsed.visual_description ?? null,
      answer:             parsed.answer             ?? null,
      user_annotation:    caption || parsed.user_annotation || null,
      error_reason:       parsed.error_reason       ?? '未说明',
      keywords:           parsed.keywords           ?? [],
      raw_image_b64:      imageBase64,
      status:             '待二刷',
      needs_confirm:      buildConfirmPrompt(parsed),
    };
  } catch (e) {
    return {
      success:         false,
      error:           e.message,
      fallback_prompt: '没识别出来，可以把题目文字复制过来发给我，一样能整理。',
    };
  }
}

function buildConfirmPrompt(parsed) {
  if (!parsed.section)      return '这道题是哪个科目/模块？';
  if (!parsed.error_reason || parsed.error_reason === '无法判断') {
    return '这道题是知识点没掌握、粗心，还是时间不够？';
  }
  return null;
}

// ─── 文字消息处理 ─────────────────────────────────────────────

function detectMood(text) {
  if (/太累|好烦|没用|放弃|崩了/.test(text))      return '低落';
  if (/没时间|来不及|考试快|好焦虑|压力/.test(text)) return '焦虑';
  if (/不错|还行|有进步|感觉好|状态好/.test(text))  return '良好';
  return '中性';
}

function extractWrongCount(text) {
  const patterns = [
    /错[了]?\s*(\d+)\s*[道题个]/,
    /(\d+)\s*[道题个]?\s*[错误不对]/,
    /(\d+)\s*错/,
  ];
  for (const p of patterns) {
    const m = text.match(p);
    if (m) return parseInt(m[1], 10);
  }
  return null;
}

/**
 * 快捷录入：科目-题型-原因-状态
 * 如：Verbal-Text Completion-词汇量不足-待二刷
 */
function parseQuickEntry(text) {
  const parts = text.split(/[-—·/]/);
  if (parts.length < 2) return null;

  const section = parts[0].trim();
  if (section.length > 30 || section.length < 1) return null;
  // 至少第二段有内容才认为是快捷格式
  if (!parts[1]?.trim()) return null;

  const examKey      = getExamKey();
  const question_type = parts[1]?.trim() || '';
  const reasonRaw    = parts[2]?.trim() || '';
  const statusRaw    = parts[3]?.trim() || '';

  const error_reason = /不会|不懂|没学|不清楚/.test(reasonRaw) ? '知识点不会'
    : /粗心|看错|算错|选反/.test(reasonRaw) ? '粗心'
    : /时间|没做完|蒙/.test(reasonRaw) ? '时间不够'
    : /混淆|分不清|搞混/.test(reasonRaw) ? '概念混淆'
    : (reasonRaw || '未说明');

  const status = /掌握|会了|搞懂/.test(statusRaw) ? '已掌握' : '待二刷';

  // 写入词库
  updateTagLibrary(examKey, { question_type, knowledge_point: reasonRaw });

  return {
    source:         'quick',
    date:           new Date().toISOString().slice(0, 10),
    exam:           examKey,
    exam_name:      getExamName(),
    section,
    question_type,
    knowledge_point: reasonRaw,
    question_text:  text,
    error_reason,
    keywords:       [section, question_type].filter(Boolean).slice(0, 2),
    status,
    needs_confirm:  null,
  };
}

/**
 * 解析导出筛选指令。
 */
function parseExportCommand(text) {
  if (!/导出|错题本|生成报告/.test(text)) return null;

  const pending = /待二刷|未掌握/.test(text);

  let days = null;
  const dm = text.match(/最近\s*(\d+)\s*天/);
  const wm = text.match(/最近\s*(\d+)\s*周/);
  const mm = text.match(/最近\s*(\d+)\s*个?月/);
  if (dm) days = parseInt(dm[1]);
  if (wm) days = parseInt(wm[1]) * 7;
  if (mm) days = parseInt(mm[1]) * 30;
  if (/上周|本周|这周/.test(text)) days = 7;
  if (/本月|这个月/.test(text))   days = 30;
  if (/两周/.test(text))          days = 14;

  // 科目/section 匹配（自由文本，取"的"前面的词）
  const sectionMatch = text.match(/导出(.+?)的错题/);
  const sectionFilter = sectionMatch ? sectionMatch[1].replace(/只|最近\S+/, '').trim() : null;

  return { _export: true, pendingOnly: pending, sectionFilter, daysFilter: days };
}

function parseStudyInput(message) {
  // 快捷录入
  const quick = parseQuickEntry(message);
  if (quick) return quick;

  return {
    date:                new Date().toISOString().slice(0, 10),
    source:              'text',
    exam:                getExamKey(),
    exam_name:           getExamName(),
    raw_message:         message,
    mood:                detectMood(message),
    wrong_count:         extractWrongCount(message),
    has_exam:            /做了|做完|刷了|套题|整套|一套/.test(message),
    skip_today:          /没做|没时间|跳过|明天补|休息/.test(message),
    needs_clarification: null,
  };
}

// ─── 统一入口 ─────────────────────────────────────────────────

async function handleMessage(message, { agentCall, sendMessage } = {}) {
  const text = message.text ?? message.caption ?? '';

  // 换考试指令
  if (/换考试|切换考试|改考试/.test(text) && sendMessage) {
    await handleChangeExam(sendMessage);
    return { _change_exam: true };
  }

  // Onboarding 拦截
  if (!isSetupDone()) {
    const consumed = await handleOnboarding(text, sendMessage);
    if (consumed) return { _onboarding: true };
  }

  // 二刷回复拦截
  if (message.type === 'text' && sendMessage) {
    const reviewReply = handleReviewReply(text);
    if (reviewReply !== null) {
      await sendMessage(reviewReply);
      return { _review: true };
    }
  }

  // 图片
  if (message.type === 'image') {
    return parseImageInput(message.imageBase64, message.caption ?? '', agentCall);
  }

  // 导出筛选
  const exportCmd = parseExportCommand(text);
  if (exportCmd) return exportCmd;

  // 普通文字
  return parseStudyInput(text);
}

module.exports = { handleMessage, parseStudyInput, parseImageInput, parseExportCommand };
