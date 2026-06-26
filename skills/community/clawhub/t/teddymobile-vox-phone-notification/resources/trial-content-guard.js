const TRIAL_MAX_CONTENT_LENGTH = 100;

const TRIAL_NOTIFICATION_PREFIX =
  'TeddyMobile Vox 试用通知：';

const URL_PATTERNS = [
  /https?:\/\/\S+/i,
  /www\.\S+/i,
  /\b[a-z0-9-]+(?:\.[a-z0-9-]+)+\b/i,
];

const CONTACT_PATTERNS = [
  /1[3-9]\d{9}/,
  /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/i,
  /(?:微信|vx|v信|wechat)[:：\s]?[a-z0-9_-]{5,}/i,
  /(?:QQ|qq)[:：\s]?\d{5,12}/,
];

const BLOCKED_TERMS = [
  '转账',
  '汇款',
  '银行卡',
  '验证码',
  '密码',
  '动态码',
  '贷款',
  '借款',
  '中奖',
  '返利',
  '投资',
  '理财',
  '博彩',
  '赌博',
  '下注',
  '加微信',
  '加群',
  '点击链接',
  '下载APP',
  '账号异常',
  '冻结账户',
  '公安',
  '法院',
  '客服',
  '冒充',
  '威胁',
  '恐吓',
];

function normalizeText(text) {
  return String(text || '')
    .replace(/^您好，?提醒您/, '')
    .replace(/\s+/g, ' ')
    .replace(/[~`^*_+=|\\<>[\]{}]/g, '')
    .trim();
}

function containsPattern(text, patterns) {
  return patterns.some((pattern) => pattern.test(text));
}

function containsBlockedTerm(text) {
  const normalized = text.toLowerCase();
  return BLOCKED_TERMS.some((term) => normalized.includes(term.toLowerCase()));
}

function validateTrialContent(text) {
  const content = normalizeText(text);

  if (content.length < 2) {
    return {
      ok: false,
      code: 'CONTENT_TOO_SHORT',
      message: 'Trial content is too short.',
    };
  }

  if (containsPattern(content, URL_PATTERNS)) {
    return {
      ok: false,
      code: 'BLOCKED_URL',
      message: 'Trial content cannot include links or domains.',
    };
  }

  if (containsPattern(content, CONTACT_PATTERNS)) {
    return {
      ok: false,
      code: 'BLOCKED_CONTACT',
      message: 'Trial content cannot include phone numbers, email, WeChat, or QQ.',
    };
  }

  if (/\d{7,}/.test(content)) {
    return {
      ok: false,
      code: 'BLOCKED_LONG_NUMBER',
      message: 'Trial content cannot include long number sequences.',
    };
  }

  if (containsBlockedTerm(content)) {
    return {
      ok: false,
      code: 'BLOCKED_TERM',
      message: 'Trial content contains high-risk terms.',
    };
  }

  return {
    ok: true,
    content: content.slice(0, TRIAL_MAX_CONTENT_LENGTH),
  };
}

function buildTrialNotificationText(text) {
  const result = validateTrialContent(text);

  if (!result.ok) return result;

  return {
    ok: true,
    content: result.content,
    notificationText: `${TRIAL_NOTIFICATION_PREFIX}${result.content}`,
  };
}

module.exports = {
  TRIAL_MAX_CONTENT_LENGTH,
  validateTrialContent,
  buildTrialNotificationText,
};
