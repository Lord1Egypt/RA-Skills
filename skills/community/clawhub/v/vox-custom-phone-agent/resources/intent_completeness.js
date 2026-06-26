'use strict';

const { isValidPhone } = require('./phone_validator');
const { VOICE_OPTIONS_TEXT } = require('./voice_type_selector');
const { checkBusinessContext } = require('./business_context_rules');

const USE_MODE_TEXT = '请选择使用方式：1 先用推广试用体验一次；2 使用正式账号/注册 Vox 企业账号后接入。回复“试用”或“正式注册”即可。';

function checkCompleteness(intent = {}) {
  const missing = [];
  if (!intent.useMode || !/^(trial|formal)$/.test(String(intent.useMode))) missing.push('useMode');
  if (!intent.callee || !isValidPhone(intent.callee)) missing.push('callee');
  if (!intent.goal || String(intent.goal).trim().length < 4) missing.push('goal');
  if (!intent.role || String(intent.role).trim().length < 2) missing.push('role');
  const businessContext = checkBusinessContext(intent);
  const isTrial = intent.useMode === 'trial';
  if (!isTrial && !businessContext.complete) missing.push('businessContext');
  if (!intent.voiceType || !/^[0-4]$/.test(String(intent.voiceType))) missing.push('voiceType');

  return {
    complete: missing.length === 0,
    missing,
    businessContext,
    question: missing.length ? buildFollowUpQuestion(missing, intent) : ''
  };
}

function buildFollowUpQuestion(missing, intent = {}) {
  if (missing.includes('useMode')) return addKnownContext(USE_MODE_TEXT, intent);

  if (intent.useMode === 'trial') {
    return addKnownContext(buildSingleTrialQuestion(missing, intent), intent);
  }

  const items = [];
  if (missing.includes('callee')) items.push('要拨打的手机号');
  if (missing.includes('goal')) items.push('这通电话希望达成的具体目标，例如通知、预约确认、回访或邀约');
  if (missing.includes('role')) items.push('Bot 应以什么身份联系对方，例如客服、课程顾问、招聘助理、会议通知助理或商务经理');
  if (missing.includes('voiceType')) items.push('要使用的音色');
  if (missing.includes('businessContext')) items.push('更具体的业务背景，例如事项内容、时间、对象、处理边界或不满意时的跟进方式');

  if (items.length === 1) {
    if (missing[0] === 'callee') return addKnownContext('请提供要拨打的手机号。', intent);
    if (missing[0] === 'goal') return addKnownContext('请说明这通电话希望达成什么目标，例如通知、预约确认、回访或邀约。', intent);
    if (missing[0] === 'voiceType') return addKnownContext(VOICE_OPTIONS_TEXT, intent);
    if (missing[0] === 'businessContext') return addKnownContext(checkBusinessContext(intent).question, intent);
    return addKnownContext('请说明 Bot 应以什么身份联系对方，例如客服、课程顾问、招聘助理、会议通知助理或商务经理。', intent);
  }

  const topTwo = items.slice(0, 2);
  return addKnownContext(`请补充两个信息：${topTwo.join('；')}。`, intent);
}

function buildSingleTrialQuestion(missing, intent = {}) {
  if (missing.includes('callee')) return '请提供要拨打的手机号。';
  if (missing.includes('goal')) return '请说明这通试用电话希望达成什么目标。';
  if (missing.includes('role')) return '请说明 Bot 应以什么身份联系对方，例如客服、课程顾问或通知助理。';
  if (missing.includes('voiceType')) return VOICE_OPTIONS_TEXT;
  if (missing.includes('businessContext')) return checkBusinessContext(intent).question;
  return '请补充这通试用电话的关键信息。';
}

function addKnownContext(question, intent = {}) {
  const known = [];
  if (intent.scenario) known.push(`任务：${intent.scenario}`);
  if (intent.goal) known.push(`目标：${intent.goal}`);
  if (intent.role) known.push(`建议 Bot 身份：${intent.role}`);
  if (!known.length) return question;
  return `${question}\n\n当前已识别到：\n- ${known.join('\n- ')}`;
}

module.exports = { USE_MODE_TEXT, checkCompleteness, buildFollowUpQuestion, buildSingleTrialQuestion };
