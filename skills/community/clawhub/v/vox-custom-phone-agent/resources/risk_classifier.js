'use strict';

function classifyRisk(intent = {}) {
  const text = [intent.rawPrompt, intent.goal, intent.workflow, intent.constraint].filter(Boolean).join(' ');
  const categories = [];
  if (/身份验证|验证码|密码|银行卡|证件号|身份证|医保|保险信息/.test(text) && !isNegativeBoundary(text, /身份验证|验证码|密码|银行卡|证件号|身份证|医保|保险信息/)) categories.push('identity_verification');
  if (/谈判|赔偿金额|压低|退款金额|索赔|报价|签约|付款|转账/.test(text) && !isNegativeBoundary(text, /谈判|赔偿金额|压低|退款金额|索赔|报价|签约|付款|转账/) && !isLowRiskNoticeOrInquiry(text)) categories.push('complex_decision');
  if (/医疗建议|治疗方案|诊断|法律意见|投资建议|理财/.test(text) && !isNegativeBoundary(text, /医疗建议|治疗方案|诊断|法律意见|投资建议|理财/)) categories.push('professional_advice');
  if (/投诉|赔偿|退款|纠纷/.test(text)) categories.push('sensitive_complaint');

  const high = /索要|套取|冒充|威胁|恐吓/.test(text)
    || (/转账/.test(text) && !isNegativeBoundary(text, /转账/))
    || (/验证码|密码/.test(text) && !isNegativeBoundary(text, /验证码|密码/));
  const level = high ? 'high' : categories.length ? 'medium' : 'low';
  const suitableForCustomBot = level === 'low' || (level === 'medium' && !categories.includes('identity_verification'));
  return {
    level,
    categories,
    suitableForCustomBot,
    reason: level === 'low'
      ? '当前任务适合 botType=custom 执行。'
      : '该电话可能涉及身份验证、实时决策、谈判或专业建议，当前 botType=custom 不适合完全自动处理。',
    suggestedAction: suitableForCustomBot
      ? '继续执行，但请保持清晰边界。'
      : '请简化为通知、预约确认或安排人工跟进，避免让 Bot 做实时决策。'
  };
}

function isNegativeBoundary(text, pattern) {
  const clauses = String(text || '').split(/[。；;\n]/);
  return clauses.some((clause) => pattern.test(clause) && /(不|不要|不能|不得|禁止|避免|不提供|不做|不讨论|不聊|拒绝|不要涉及|不能涉及)/.test(clause));
}

function isLowRiskNoticeOrInquiry(text) {
  return /通知|提醒|确认|了解|询问|回访|邀约|预约|介绍|转人工|人工跟进|记录反馈/.test(text)
    && !/必须|强制|立刻|马上|诱导|要求.*(付款|转账|签约)|让.*(付款|转账|签约)/.test(text);
}

module.exports = { classifyRisk };
