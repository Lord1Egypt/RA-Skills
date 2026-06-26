'use strict';

const DENY_RULES = [
  { pattern: /验证码|短信码|动态码|密码|银行卡号|CVV|支付密码|账户密码/, reason: '不能通过电话索要验证码、密码、银行卡或账户凭证。' },
  { pattern: /冒充|假装|伪装.*(银行|公安|警察|法院|检察院|政府|客服)/, reason: '不能冒充机构或他人身份发起电话。' },
  { pattern: /转账|汇款|打钱|投资.*保证|稳赚|高收益|内幕消息/, reason: '不能发起诱导转账或高风险投资相关电话。' },
  { pattern: /威胁|恐吓|吓唬|辱骂|骚扰|不还.*后果|上门闹/, reason: '不能发起威胁、骚扰或违法催收性质的电话。' },
  { pattern: /虚假|骗|诈骗|套取|钓鱼/, reason: '不能发起欺骗、套取信息或诈骗性质的电话。' }
];

const CLARIFY_RULES = [
  { pattern: /贷款|借款|还款|账单|逾期|金融|保险|理财|股票|基金/, reason: '电话涉及金融事项，请确保只做合规通知，不索要密码、验证码、转账或投资操作。' },
  { pattern: /诊断|处方|治疗方案|药量|医疗建议|法律意见|诉讼策略/, reason: '电话涉及专业建议，请限定为预约、提醒或信息收集，不提供医疗、法律或金融结论。' }
];

function checkSafety(intent = {}) {
  const text = [intent.rawPrompt, intent.goal, intent.role, intent.background, intent.constraint]
    .filter(Boolean)
    .join(' ');

  for (const rule of DENY_RULES) {
    if (rule.pattern.test(text)) {
      if (/验证码|短信码|动态码|密码|银行卡号|CVV|支付密码|账户密码/.test(rule.pattern.source) && isNegativeCredentialBoundary(text)) {
        continue;
      }
      if (isNegativeBoundary(text, rule.pattern)) {
        continue;
      }
      return { ok: false, action: 'deny', reason: rule.reason };
    }
  }

  for (const rule of CLARIFY_RULES) {
    if (rule.pattern.test(text) && !isNegativeBoundary(text, rule.pattern)) {
      return { ok: true, action: 'allow_with_constraint', reason: rule.reason };
    }
  }

  return { ok: true, action: 'allow', reason: '' };
}

function isNegativeCredentialBoundary(text) {
  return /(不要|不能|不得|不允许|禁止|避免)[^。；;\n]{0,16}(验证码|短信码|动态码|密码|银行卡|账户凭证)|(验证码|短信码|动态码|密码|银行卡|账户凭证)[^。；;\n]{0,16}(不要|不能|不得|不允许|禁止|避免)/.test(text);
}

function isNegativeBoundary(text, pattern) {
  const clauses = String(text || '').split(/[。；;\n]/);
  return clauses.some((clause) => pattern.test(clause) && /(不|不要|不能|不得|禁止|避免|不提供|不做|不讨论|不聊|拒绝|不要涉及|不能涉及)/.test(clause));
}

module.exports = { checkSafety };
