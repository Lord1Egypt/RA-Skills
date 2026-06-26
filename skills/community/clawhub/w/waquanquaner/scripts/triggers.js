/**
 * WaQuanquaner - 触发解析器
 * 
 * 解析用户自然语言输入，提取意图和参数
 * 用于判断用户是否在请求外卖优惠查询
 */

const config = require('./config');

/**
 * 解析用户输入
 * @param {string} input - 用户自然语言输入
 * @returns {object} 解析结果
 * 
 * 返回格式：
 * {
 *   triggered: boolean,    // 是否命中触发条件
 *   action: string,        // 动作类型
 *   platform: string|null, // 目标平台 (eleme/meituan/jingdong/null)
 *   format: string,        // 推荐的渲染格式
 *   raw: string            // 原始输入
 * }
 */
function parseInput(input) {
  const result = {
    triggered: false,
    action: 'query_activities',
    platform: null,
    format: config.FORMATS.WECHAT,
    raw: input,
  };

  if (!input || typeof input !== 'string') return result;

  const normalized = input.toLowerCase().trim();

  // 检查平台
  result.platform = detectPlatform(normalized);

  // 检查是否命中触发关键词
  const isTriggered = checkTrigger(normalized, result.platform);
  result.triggered = isTriggered;

  return result;
}

/**
 * 检测目标平台
 * @param {string} text - 标准化后的用户输入
 * @returns {string|null} 平台 key 或 null
 */
function detectPlatform(text) {
  for (const [key, info] of Object.entries(config.PLATFORMS)) {
    for (const kw of info.keywords) {
      if (text.includes(kw.toLowerCase())) return key;
    }
  }
  return null;
}

/**
 * 检查是否命中触发条件
 * @param {string} text - 标准化后的用户输入
 * @param {string|null} detectedPlatform - 已检测到的平台
 * @returns {boolean}
 */
function checkTrigger(text, detectedPlatform) {
  // 1. 通用触发词
  for (const kw of config.TRIGGER_KEYWORDS) {
    if (text.includes(kw.toLowerCase())) return true;
  }

  // 2. 平台+类型组合触发词
  if (detectedPlatform) {
    const platformTriggers = config.PLATFORM_TRIGGERS[detectedPlatform] || [];
    for (const kw of platformTriggers) {
      if (text.includes(kw.toLowerCase())) return true;
    }
  }

  // 3. 仅平台名 + 优惠/红包/券 等词
  if (detectedPlatform) {
    const bonusWords = ['优惠', '红包', '券', '活动', '省钱', '领'];
    for (const bw of bonusWords) {
      if (text.includes(bw)) return true;
    }
  }

  return false;
}

/**
 * 获取触发说明（用于帮助文档）
 * @returns {string}
 */
function getTriggerHelp() {
  let help = '## 触发方式\n\n';
  help += '### 通用查询\n';
  help += '- "有什么外卖红包"\n';
  help += '- "外卖优惠"\n';
  help += '- "点外卖怎么省钱"\n';
  help += '- "领外卖券"\n\n';

  help += '### 指定平台\n';
  for (const [key, info] of Object.entries(config.PLATFORMS)) {
    help += '- "' + info.name + '有什么红包"\n';
    help += '- "' + info.name + '优惠活动"\n';
  }
  help += '\n';

  return help;
}

// CLI 测试
if (require.main === module) {
  const testInputs = [
    '有什么外卖红包',
    '帮我查外卖优惠',
    '饿了么今天有什么红包',
    '美团外卖优惠',
    '京东外卖',
    '点外卖怎么省钱',
    '今天天气怎么样',
    '外卖',
  ];

  console.log('触发解析测试:\n');
  for (const input of testInputs) {
    const result = parseInput(input);
    const status = result.triggered ? '✅' : '❌';
    const platform = result.platform ? config.PLATFORMS[result.platform]?.name : '全部';
    console.log(status + ' "' + input + '" → 平台: ' + platform);
  }
}

module.exports = {
  parseInput,
  detectPlatform,
  checkTrigger,
  getTriggerHelp,
};
