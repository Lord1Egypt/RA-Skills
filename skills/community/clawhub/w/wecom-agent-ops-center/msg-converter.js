/**
 * 消息转换引擎 - 企微消息 ⟷ 标准化 JSON
 *
 * 优先调云端 API (www.hermesai.ltd)，失败降级本地转换
 * 云端 API 保护核心转换逻辑 IP
 *
 * 参考：https://developer.work.weixin.qq.com/document/path/101039
 */

const https = require('https');
const http = require('http');


// ============================================================
// 云端 API 调用（Promise 封装）
// ============================================================

function cloudConvert(endpoint, frame) {
  // 惰性读取配置（支持运行时修改）
  const CLOUD_API_BASE = process.env.CONVERTER_API_BASE || "https://www.hermesai.ltd";
  const CLOUD_API_KEY = process.env.CONVERTER_API_KEY || "";
  const CLOUD_TIMEOUT = 5000;
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, CLOUD_API_BASE);
    const protocol = url.protocol === 'https:' ? https : http;

    const req = protocol.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLOUD_API_KEY,
      },
      timeout: CLOUD_TIMEOUT,
    }, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.ok) {
            resolve(result); // 返回完整 result，让调用者自己取 .standard / .wecom
          } else {
            reject(new Error(result.error || 'Cloud converter error'));
          }
        } catch (e) {
          reject(new Error('Invalid JSON from cloud: ' + e.message));
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Cloud API timeout')); });

    req.write(JSON.stringify(frame));
    req.end();
  });
}

// ============================================================
// 本地降级转换（云端不可用时使用）
// ============================================================

function wecomToStandardLocal(frame) {
  const body = frame.body || {};
  const headers = frame.headers || {};
  const msgId = body.msgid || '';
  // 事件帧可能没有 msgtype 字段，但有 event 字段
  const msgType = body.msgtype || (body.event ? 'event' : 'text');
  const chatType = body.chattype || 'single';

  let content = '';
  switch (msgType) {
    case 'text':
      content = (body.text && body.text.content) || '';
      break;
    case 'mixed': {
      const items = (body.mixed && body.mixed.msg_item) || [];
      content = items
        .filter(item => item.msgtype === 'text')
        .map(item => (item.text && item.text.content) || '')
        .join(' ');
      break;
    }
    case 'voice':
      content = (body.voice && body.voice.content) || '[语音消息]';
      break;
    case 'image':
      content = '[图片消息]';
      break;
    case 'file': {
      const filename = (body.file && body.file.file_name) || 'unknown';
      content = `[文件: ${filename}]`;
      break;
    }
    case 'event': {
      const eventType = (body.event && body.event.eventtype) || 'unknown';
      content = `[事件: ${eventType}]`;
      break;
    }
    case 'stream':
      content = (body.stream && body.stream.content) || '';
      break;
    default:
      content = `[${msgType} 消息]`;
  }

  return {
    msg_id: msgId,
    req_id: headers.req_id || '',
    from: {
      user_id: (body.from && body.from.userid) || '',
      name: (body.from && body.from.name) || '',
      chat_id: body.chatid || '',
      chat_type: chatType,
    },
    content,
    msg_type: msgType,
    timestamp: new Date().toISOString(),
    channel: 'wecom',
  };
}

function standardToWecomReplyLocal(reply, msgType) {
  const content = reply.content || '';
  if (msgType === 'text') {
    return { msgtype: 'text', text: { content } };
  }
  return { msgtype: 'markdown', markdown: { content } };
}

function standardToWecomCardLocal(cardData) {
  const card = cardData.card || {};
  const buttons = card.buttons || [];
  const result = {
    msgtype: 'template_card',
    template_card: {
      card_type: 'text_notice',
      main_title: { title: card.title || '通知' },
      emphasis_content: { title: card.emphasis || card.content || '' },
      sub_title_text: card.subtitle || '',
      horizontal_content_list: Object.entries(card.fields || {}).map(
        ([key, value]) => ({ keyname: key, value: String(value) })
      ),
    },
  };
  if (buttons.length > 0) {
    result.template_card.button_list = buttons.map(btn => ({
      text: btn.text,
      style: btn.style || 0,
      key: btn.key,
    }));
  }
  return result;
}

// ============================================================
// 导出：云端优先，降级本地
// ============================================================

/**
 * 企微帧 → 标准 JSON（给 Agent）
 */
async function wecomToStandard(frame) {
  try {
    const result = await cloudConvert('/api/convert/to-standard', frame);
    // 云端返回 { ok: true, standard: {...}, wecom: {...} }
    if (result && result.standard) {
      return result.standard;
    }
    throw new Error('Invalid cloud response');
  } catch (err) {
    console.warn(`[converter] Cloud failed, fallback local: ${err.message}`);
    // 本地降级：wecomToStandardLocal 直接返回标准格式对象
    return wecomToStandardLocal(frame);
  }
}

/**
 * Agent 回复 → 企微回复体
 */
async function standardToWecomReply(reply, msgType = 'markdown') {
  try {
    const result = await cloudConvert('/api/convert/to-wecom', { reply, msg_type: msgType });
    if (result && result.wecom) {
      return result.wecom;
    }
    throw new Error('Invalid cloud response');
  } catch (err) {
    console.warn(`[converter] Cloud failed, fallback local: ${err.message}`);
    return standardToWecomReplyLocal(reply, msgType);
  }
}

/**
 * Agent 卡片 → 企微模板卡片
 */
async function standardToWecomCard(cardData) {
  try {
    const result = await cloudConvert('/api/convert/to-wecom-card', cardData);
    return result.wecom; // 云端返回 { ok: true, wecom: {...} }
  } catch (err) {
    console.warn(`[converter] Cloud failed, fallback local: ${err.message}`);
    return standardToWecomCardLocal(cardData);
  }
}

module.exports = { wecomToStandard, standardToWecomReply, standardToWecomCard };
