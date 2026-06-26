/**
 * WaQuanquaner Skill 配置文件
 *
 * 所有可配置项集中管理，方便自定义部署
 */

module.exports = {
  /** 推荐数据接口地址 */
  COMPACT_API_URL: process.env.COMPACT_API_URL || 'https://waquanquaner.cn/api/v1/activities/channel/skill_compact',

  /** API 请求超时时间（毫秒） */
  TIMEOUT: 15000,

  /** 中转页 URL */
  LANDING_PAGE_URL: process.env.LANDING_PAGE_URL || 'https://waquanquaner.cn/go',

  /** 平台映射 */
  PLATFORMS: {
    eleme: {
      name: '饿了么',
      emoji: '🔵',
      keywords: ['饿了么', 'eleme', '饿了'],
    },
    meituan: {
      name: '美团',
      emoji: '🟡',
      keywords: ['美团', 'meituan', '点评'],
    },
    jingdong: {
      name: '京东',
      emoji: '🔴',
      keywords: ['京东', 'jingdong', 'JD'],
    },
  },

  /** 触发关键词（用户输入匹配） */
  TRIGGER_KEYWORDS: [
    '外卖红包', '外卖优惠', '外卖券', '外卖优惠券',
    '省钱', '点外卖省钱', '外卖省钱',
    '领券', '外卖领券', '领红包',
    '红包', '优惠活动',
    '点外卖', '叫外卖', '外卖', '外卖神券',
    '满减红包', '美团外卖', '饿了么外卖', '京东外卖',
    '挖券券', '挖券券儿', '吃什么',
  ],

  /** 平台+类型组合触发词 */
  PLATFORM_TRIGGERS: {
    eleme: ['饿了么红包', '饿了么优惠', '饿了么券', '饿了么领券'],
    meituan: ['美团红包', '美团优惠', '美团券', '美团领券', '美团外卖'],
    jingdong: ['京东红包', '京东优惠', '京东券', '京东外卖'],
  },

  /** 渲染格式 */
  FORMATS: {
    WECHAT: 'wechat',      // 微信文本
    FEISHU: 'feishu',      // 飞书消息卡片
    TEXT: 'text',          // 纯文本（终端/日志）
  },
};
