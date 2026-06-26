'use strict';

function buildResultMeaning(status) {
  if (status === 'accepted' || status === 'ready') {
    return {
      status,
      meaning: `${status} 表示 Vox 已接收或已生成外呼任务，不代表通话已完成或目标已达成。`,
      whatHappensNext: 'Vox custom bot 将根据 agent_profile 执行电话。',
      whereToCheckResult: '请在 Vox 平台查看通话结果，或等待后续回调能力。'
    };
  }
  return {
    status,
    meaning: '外呼任务未成功受理。',
    whatHappensNext: '请根据 failureAdvice 修正后重试。',
    whereToCheckResult: '如仍失败，请检查 Vox 平台账号、权限、IP 白名单和接口配置。'
  };
}

function buildFailureAdvice(result = {}) {
  const status = Number(result.httpStatus || 0);
  const body = result.body || {};
  if (status === 401) return advice('auth_failed', '外呼认证失败，请检查 VOX_APP_ID、VOX_SECRET、服务器时间和 HMAC 签名。', false, '检查正式凭证或切换为推广试用模式。');
  if (status === 403) return advice('permission_denied', '账号未授权、接口权限不足或 IP 白名单未配置。', false, '检查 Vox 账号权限、botType=custom 权限和服务器出口 IP 白名单。');
  if (status === 400) return advice('bad_request', `请求参数可能不正确：${body.msg || '请检查手机号、botType、extra JSON 和 agent_profile。'}`, false, '修正参数后重试。');
  if (status === 429) return advice('quota_or_rate_limited', '试用额度、账号额度或调用频率可能已受限。', false, '稍后重试，或注册正式 Vox 企业账号获取正式额度。');
  if (status >= 500) return advice('vox_or_network_error', 'Vox 服务或网络可能暂时异常。', true, '稍后重试一次。');
  return advice('unknown', body.msg || '未知错误。', false, '检查返回体、账号配置和请求参数。');
}

function advice(category, userMessage, canRetry, nextAction) {
  return { category, userMessage, canRetry, nextAction };
}

module.exports = { buildFailureAdvice, buildResultMeaning };
