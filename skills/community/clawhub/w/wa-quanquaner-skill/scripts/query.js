/**
 * WaQuanquaner - 数据查询引擎
 *
 * 从服务器获取今日推荐数据
 * 依赖：Node.js 内置 http/https 模块（无需第三方依赖）
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');
const config = require('./config');

/**
 * 发送 HTTP GET 请求
 * @param {string} urlStr - 请求 URL
 * @param {number} timeout - 超时时间（毫秒）
 * @returns {Promise<object>} 解析后的 JSON 响应
 */
function httpGet(urlStr, timeout = config.TIMEOUT) {
  return new Promise((resolve, reject) => {
    let parsedUrl;
    try {
      parsedUrl = new URL(urlStr);
    } catch (e) {
      return reject(new Error('无效的 URL: ' + urlStr));
    }

    const client = parsedUrl.protocol === 'https:' ? https : http;
    const req = client.get(urlStr, { timeout }, (res) => {
      // 处理重定向
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpGet(res.headers.location, timeout).then(resolve).catch(reject);
      }

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (res.statusCode >= 400) {
            reject(new Error('API 返回错误 ' + res.statusCode + ': ' + (json.message || data.substring(0, 200))));
          } else {
            resolve(json);
          }
        } catch (e) {
          reject(new Error('JSON 解析失败: ' + e.message));
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('请求超时 (' + timeout + 'ms)'));
    });
  });
}

/**
 * 获取今日推荐数据
 *
 * 返回：
 *   { date, landing: {url, text}, highlights: [{emoji, platform, name, hook, reason}],
 *     freshness_hint, footer_hint }
 *
 * @param {object} [options]
 * @param {string} [options.compactApiUrl] - 自定义数据接口地址
 * @returns {Promise<{success: boolean, compact: object|null, message: string}>}
 */
async function fetchCompact(options = {}) {
  const apiUrl = options.compactApiUrl || config.COMPACT_API_URL;

  try {
    const response = await httpGet(apiUrl);

    // 验证核心字段
    if (response && response.landing && response.landing.url) {
      return {
        success: true,
        compact: {
          channel: response.channel || 'skill_compact',
          date: response.date || new Date().toISOString().split('T')[0],
          landing: response.landing,
          highlights: Array.isArray(response.highlights) ? response.highlights : [],
          freshness_hint: response.freshness_hint || '',
          footer_hint: response.footer_hint || '',
        },
        message: '',
      };
    }

    return {
      success: false,
      compact: null,
      message: response.message || '推荐数据格式异常',
    };
  } catch (error) {
    return {
      success: false,
      compact: null,
      message: error.message,
    };
  }
}

// CLI 直接执行
if (require.main === module) {
  (async () => {
    console.log('正在查询外卖优惠活动...\n');
    const result = await fetchCompact();

    if (!result.success) {
      console.log('❌ 查询失败:', result.message);
      process.exit(1);
    }

    const c = result.compact;
    console.log('✅ 查询成功\n');
    console.log('🔗 ' + c.landing.text + ': ' + c.landing.url);
    if (c.highlights.length > 0) {
      console.log('\n💡 今日必领:');
      for (const h of c.highlights) {
        console.log('  ' + h.emoji + ' ' + h.platform + '·' + h.name + '（' + h.reason + '）');
        console.log('    → ' + h.hook);
      }
    }
  })();
}

module.exports = {
  fetchCompact,
  httpGet,
};
