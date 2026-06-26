/**
 * WaQuanquaner 🧧 — 外卖红包实时挖掘助手
 *
 * 一个轻量级的 Agent Skill，用于查询美团/饿了么/京东外卖平台的
 * 最新红包和优惠活动，一个链接挖取当日所有隐藏活动。
 *
 * 零依赖：仅使用 Node.js 内置模块
 *
 * 用法:
 *   const { WaQuanquaner } = require('WaQuanquaner-skill');
 *   const wqq = new WaQuanquaner();
 *   const result = await wqq.query();
 *   console.log(result.text);
 */

const queryMod = require('./scripts/query');
const { renderCompactFromApi } = require('./scripts/render');
const { parseInput } = require('./scripts/triggers');
const config = require('./scripts/config');

class WaQuanquaner {
  /**
   * @param {object} options
   * @param {string} [options.defaultFormat] - 默认渲染格式 (wechat/feishu/text)
   * @param {string} [options.compactApiUrl] - 自定义数据接口地址
   */
  constructor(options = {}) {
    this.defaultFormat = options.defaultFormat || config.FORMATS.WECHAT;
    this.compactApiUrl = options.compactApiUrl || config.COMPACT_API_URL;
  }

  /**
   * 检查用户输入是否触发查询
   * @param {string} input - 用户自然语言输入
   * @returns {{ triggered: boolean, platform: string|null }}
   */
  shouldTrigger(input) {
    const result = parseInput(input);
    return {
      triggered: result.triggered,
      platform: result.platform,
    };
  }

  /**
   * 查询外卖优惠活动
   * @param {object} [options]
   * @param {string} [options.platform] - 筛选平台 (eleme/meituan/jingdong)
   * @param {string} [options.format] - 渲染格式 (wechat/feishu/text)
   * @returns {Promise<{success: boolean, text: string, data: object}>}
   */
  async query(options = {}) {
    const format = options.format || this.defaultFormat;

    const result = await queryMod.fetchCompact({
      compactApiUrl: this.compactApiUrl,
    });

    if (!result.success) {
      return {
        success: false,
        text: '外卖优惠服务暂时不可用，请稍后重试 🙏\n(' + result.message + ')',
        data: result,
      };
    }

    const text = renderCompactFromApi(result.compact, format);

    return {
      success: true,
      text: text,
      data: {
        compact: result.compact,
      },
    };
  }

  /**
   * 一站式处理：解析输入 → 查询 → 渲染
   * @param {string} input - 用户自然语言输入
   * @param {object} [options]
   * @param {string} [options.format] - 渲染格式
   * @returns {Promise<{handled: boolean, text: string}>}
   */
  async handleInput(input, options = {}) {
    const parsed = parseInput(input);

    if (!parsed.triggered) {
      return { handled: false, text: '' };
    }

    const result = await this.query({
      format: options.format || this.defaultFormat,
    });

    return { handled: true, text: result.text };
  }
}

// CLI 模式
if (require.main === module) {
  (async () => {
    const args = process.argv.slice(2);
    const format = args.includes('--feishu') ? 'feishu'
      : args.includes('--text') ? 'text'
      : 'wechat';

    const wqq = new WaQuanquaner();

    if (args[0] && !args[0].startsWith('--')) {
      // 解析自然语言输入
      const result = await wqq.handleInput(args.join(' '), { format });
      if (result.handled) {
        console.log(result.text);
      } else {
        console.log('未匹配到外卖优惠查询意图。试试：外卖红包、饿了么优惠、美团外卖券');
      }
    } else {
      // 直接查询
      const result = await wqq.query({ format });
      console.log(result.text);
    }
  })();
}

module.exports = {
  WaQuanquaner,
  fetchCompact: queryMod.fetchCompact,
  renderCompactFromApi: renderCompactFromApi,
  parseInput: parseInput,
  config: config,
};
