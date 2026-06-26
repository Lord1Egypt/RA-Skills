/**
 * WaQuanquaner - 渲染引擎
 *
 * 将推荐数据渲染为不同渠道的输出格式：
 * - 微信文本：适合微信聊天/小程序消息
 * - 飞书消息卡片：适合飞书群聊
 * - 纯文本：适合终端/日志
 */

const config = require('./config');

/**
 * 渲染极简聚焦输出
 *
 * 输出结构：
 *   - 核心链接 + "一个链接挖取当日所有隐藏活动"
 *   - 亮点活动预告
 *   - 趣味提示
 *   - 行动引导
 *
 * @param {object} compactData - 推荐数据
 *   { date, landing: {url, text}, highlights: [{emoji, platform, name, hook, reason}],
 *     freshness_hint, footer_hint }
 * @param {string} [format='wechat'] - 渲染格式
 * @returns {string} 渲染后的文本
 */
function renderCompactFromApi(compactData, format) {
  if (!compactData || !compactData.landing) {
    return renderEmpty(format || 'wechat');
  }

  const fmt = format || 'wechat';

  if (fmt === 'feishu') {
    return renderCompactFeishu(compactData);
  }

  if (fmt === 'text') {
    return renderCompactText(compactData);
  }

  // 默认 wechat 格式
  return renderCompactWechat(compactData);
}

/**
 * 微信格式渲染（极简聚焦）
 */
function renderCompactWechat(data) {
  const date = formatDateChinese(data.date);

  let output = '🧧 今日外卖隐藏红包已挖出！（' + date + '）\n\n';

  // 核心中转链接
  output += '🔗 ' + data.landing.text + '：\n';
  output += '   ' + data.landing.url + '\n\n';

  output += '👆 一个链接，挖取当日所有隐藏活动\n';

  // 亮点活动
  if (data.highlights && data.highlights.length > 0) {
    output += '\n💡 今日必领：\n';
    for (const h of data.highlights) {
      const reasonTag = h.reason ? '（' + h.reason + '）' : '';
      output += '   ' + h.emoji + ' ' + h.platform + '·' + h.name + reasonTag + '\n';
      output += '      → ' + h.hook + '\n';
    }
  }

  // 趣味提示
  if (data.freshness_hint) {
    output += '\n💬 ' + data.freshness_hint + '\n';
  }

  // 行动引导
  if (data.footer_hint) {
    output += '\n' + data.footer_hint;
  }

  return output;
}

/**
 * 飞书消息卡片格式渲染（极简聚焦）
 */
function renderCompactFeishu(data) {
  const elements = [];

  // 核心链接
  elements.push({
    tag: 'div',
    text: {
      tag: 'lark_md',
      content: '**🔗 ' + escapeFeishuMd(data.landing.text) + '**\n[' + escapeFeishuMd(data.landing.url) + '](' + escapeFeishuMd(data.landing.url) + ')\n\n一个链接，挖取当日所有隐藏活动',
    },
  });

  // 亮点活动
  if (data.highlights && data.highlights.length > 0) {
    elements.push({ tag: 'hr' });
    let md = '**💡 今日必领**\n';
    for (const h of data.highlights) {
      const reasonTag = h.reason ? '（' + escapeFeishuMd(h.reason) + '）' : '';
      md += h.emoji + ' **' + escapeFeishuMd(h.platform) + '·' + escapeFeishuMd(h.name) + '**' + reasonTag + '\n';
      md += '→ ' + escapeFeishuMd(h.hook) + '\n';
    }
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: md } });
  }

  // 趣味提示
  if (data.freshness_hint) {
    elements.push({ tag: 'hr' });
    elements.push({
      tag: 'div',
      text: { tag: 'lark_md', content: '💬 ' + escapeFeishuMd(data.freshness_hint) },
    });
  }

  // 行动引导
  if (data.footer_hint) {
    elements.push({ tag: 'hr' });
    elements.push({
      tag: 'note',
      elements: [{ tag: 'plain_text', content: data.footer_hint }],
    });
  }

  const card = {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: '🧧 今日外卖隐藏红包' },
      template: 'orange',
    },
    elements: elements,
  };

  return JSON.stringify(card, null, 2);
}

/**
 * 纯文本格式渲染（极简聚焦）
 */
function renderCompactText(data) {
  let output = '今日外卖隐藏红包 (' + (data.date || '') + ')\n\n';

  output += '核心链接: ' + data.landing.url + '\n';
  output += '  → ' + data.landing.text + '\n';
  output += '  → 一个链接，挖取当日所有隐藏活动\n';

  if (data.highlights && data.highlights.length > 0) {
    output += '\n今日必领:\n';
    for (let i = 0; i < data.highlights.length; i++) {
      const h = data.highlights[i];
      const reasonTag = h.reason ? ' [' + h.reason + ']' : '';
      output += '  ' + (i + 1) + '. ' + h.platform + '·' + h.name + reasonTag + '\n';
      output += '     → ' + h.hook + '\n';
    }
  }

  if (data.freshness_hint) {
    output += '\n' + data.freshness_hint + '\n';
  }

  if (data.footer_hint) {
    output += '\n' + data.footer_hint + '\n';
  }

  return output;
}

/**
 * 将日期字符串格式化为中文（4月10日）
 * @param {string} dateStr - ISO 日期字符串 (2026-04-10)
 * @returns {string}
 */
function formatDateChinese(dateStr) {
  if (!dateStr) {
    return new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' });
  }
  try {
    const d = new Date(dateStr + 'T00:00:00');
    return d.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' });
  } catch (e) {
    return dateStr;
  }
}

/**
 * 渲染空结果
 */
function renderEmpty(format) {
  const messages = {
    wechat: '🔍 今天暂时没有新的外卖优惠活动，明天再来看看吧！\n\n💡 也可以试试直接在饿了么/美团 App 里搜「外卖红包」',
    feishu: JSON.stringify({
      config: { wide_screen_mode: true },
      header: {
        title: { tag: 'plain_text', content: '🧧 外卖红包速报' },
        template: 'orange',
      },
      elements: [{
        tag: 'markdown',
        content: '今天暂时没有新的外卖优惠活动，明天再来看看吧！\n也可以试试直接在饿了么/美团 App 里搜「外卖红包」',
      }],
    }, null, 2),
    text: '[暂无活动] 今天没有新的外卖优惠活动',
  };
  return messages[format] || messages.text;
}

/**
 * 转义飞书 markdown 特殊字符
 */
function escapeFeishuMd(text) {
  if (!text) return '';
  return text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// CLI 直接执行
if (require.main === module) {
  const { fetchCompact } = require('./query');

  (async () => {
    const format = process.argv[2] || 'wechat';
    console.log('查询中...\n');

    const result = await fetchCompact();
    if (!result.success) {
      console.log('查询失败:', result.message);
      process.exit(1);
    }

    console.log(renderCompactFromApi(result.compact, format));
  })();
}

module.exports = {
  renderCompactFromApi,
  renderEmpty,
  formatDateChinese,
};
