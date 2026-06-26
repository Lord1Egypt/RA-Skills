/**
 * ai.js — Email AI summarization (supports DeepSeek / OpenAI compatible APIs)
 */

const { get } = require('./config');

function getApiConfig() {
  return {
    key: get('ai_api_key', ''),
    base: get('ai_api_base', 'https://api.deepseek.com'),
    model: get('ai_model', 'deepseek-chat'),
  };
}

async function summarizeEmail(from, subject, body) {
  const prompt = `你是邮件助手。请用中文简洁解读以下邮件，包括：
1. 一句话概述
2. 是否需要用户处理/回复
3. 重要程度（🔴紧急/🟡一般/🟢无需关注）

发件人: ${from}
主题: ${subject}
正文:
${body || '(无法读取正文)'}`;

  const api = getApiConfig();
  if (!api.key) return fallback(from, subject);

  try {
    const res = await fetch(`${api.base}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${api.key}`,
      },
      body: JSON.stringify({
        model: api.model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 500,
        temperature: 0.3,
      }),
    });

    if (!res.ok) return fallback(from, subject);
    const data = await res.json();
    return data.choices?.[0]?.message?.content || fallback(from, subject);
  } catch {
    return fallback(from, subject);
  }
}

async function summarizeBatch(emails) {
  if (!emails.length) return '';

  const emailList = emails.map((e, i) =>
    `[${i + 1}] 发件人: ${e.from || e.fromAddr || '未知'}\n主题: ${e.subject || '(无主题)'}\n正文摘要: ${(e.body || '').substring(0, 200)}`
  ).join('\n\n');

  const prompt = `你是邮件助手。以下是用户收到的 ${emails.length} 封邮件。请生成简洁的邮件总结：

1. 总体概述（2-3句话）
2. 按重要程度分类：
   - 🔴 需要处理/回复的邮件（列出具体邮件和建议动作）
   - 🟡 值得关注的信息
   - 🟢 可忽略的（广告、通知等，提一下数量）

邮件列表：
${emailList}

请用中文输出，简洁明了。`;

  const api = getApiConfig();
  if (!api.key) return '';

  try {
    const res = await fetch(`${api.base}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${api.key}`,
      },
      body: JSON.stringify({
        model: api.model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 1500,
        temperature: 0.3,
      }),
    });

    if (!res.ok) return '';
    const data = await res.json();
    return data.choices?.[0]?.message?.content || '';
  } catch {
    return '';
  }
}

function fallback(from, subject) {
  return `来自 ${from} 的邮件\n主题: ${subject}\n(AI 解读暂时不可用)`;
}

module.exports = { summarizeEmail, summarizeBatch };
