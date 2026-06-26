function extractPhoneNumber(input) {
  if (typeof input !== 'string') return null;

  const match = input.match(/1\d{10}/);
  return match ? match[0] : null;
}

function stripPhoneNumber(input, phoneNumber) {
  if (!phoneNumber) return input;
  return input.replace(phoneNumber, ' ');
}

function stripCommandPhrases(input) {
  return input
    .replace(/[，,。！？!?.]/g, ' ')
    .replace(/请?给/g, ' ')
    .replace(/发(一个)?通知/g, ' ')
    .replace(/打电话(通知|提醒)?/g, ' ')
    .replace(/电话(通知|提醒)/g, ' ')
    .replace(/通知(一下|下)?/g, ' ')
    .replace(/提醒(一下|下)?/g, ' ')
    .replace(/告诉他/g, ' ')
    .replace(/告诉她/g, ' ')
    .replace(/告诉对方/g, ' ')
    .replace(/麻烦/g, ' ')
    .replace(/一下/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function ensureSentenceEnding(text) {
  if (!text) return text;
  return /[。！？!?.]$/.test(text) ? text : `${text}。`;
}

function buildNotificationText(content) {
  if (!content) return null;
  const normalized = content.replace(/^[:：,，\s]+/, '').trim();
  if (!normalized) return null;
  return `您好，提醒您${ensureSentenceEnding(normalized)}`;
}

function buildRequestId(prefix = 'notif') {
  const now = new Date();
  const parts = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0'),
    String(now.getHours()).padStart(2, '0'),
    String(now.getMinutes()).padStart(2, '0'),
    String(now.getSeconds()).padStart(2, '0'),
  ];

  return `${prefix}-${parts.join('')}`;
}

function parseChatToNotification(input, options = {}) {
  if (typeof input !== 'string' || input.trim() === '') {
    throw new Error('请填写要通知的电话和通知内容，例如：给<接收手机号>发通知，明天10点开会。');
  }

  const phoneNumber = extractPhoneNumber(input);
  if (!phoneNumber) {
    throw new Error('缺少要通知的电话。请让用户填写接收手机号后再继续，例如：给<接收手机号>发通知，明天10点开会。');
  }

  const withoutPhone = stripPhoneNumber(input, phoneNumber);
  const content = stripCommandPhrases(withoutPhone);
  const notificationText = buildNotificationText(content);

  if (!notificationText) {
    throw new Error('缺少要通知的内容。请让用户填写电话接通后要播报的通知内容，例如：给该手机号发通知，明天10点开会。');
  }

  const parsed = {
    callee: phoneNumber,
    requestId: options.requestId || buildRequestId(options.requestPrefix),
    notificationText,
    notificationTimes: options.notificationTimes == null ? 2 : options.notificationTimes,
    sourceText: input,
  };

  return parsed;
}

module.exports = {
  extractPhoneNumber,
  buildNotificationText,
  buildRequestId,
  parseChatToNotification,
};
