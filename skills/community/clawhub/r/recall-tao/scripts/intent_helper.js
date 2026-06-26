/**
 * 意图识别辅助函数
 * 用于判断用户消息意图，匹配回复模板
 * 
 * 意图类型：
 * - price_inquiry: 询价
 * - stock_inquiry: 问库存
 * - bargain: 砍价
 * - urge_shipping: 催发货
 * - product_inquiry: 产品咨询
 * - positive_interaction: 好评/互动
 * - other: 其他
 */

const INTENT_PATTERNS = {
  price_inquiry: {
    keywords: ['多少钱', '价格', '怎么卖', '多少', '费用', '收费', '报价', '价钱', '什么价', '卖多少'],
    priority: 1
  },
  stock_inquiry: {
    keywords: ['有货吗', '还有吗', '库存', '有没有', '缺货', '补货', '有吗', '没货', '断货'],
    priority: 1
  },
  bargain: {
    keywords: ['便宜点', '打折', '优惠', '少点', '降价', '打个折', '便宜一点', '优惠点', '能少吗', '便宜吗'],
    priority: 1
  },
  urge_shipping: {
    keywords: ['发货了吗', '什么时候发', '发了没', '物流', '快递', '到哪了', '几天到', '什么时候发货', '发货'],
    priority: 1
  },
  product_inquiry: {
    keywords: ['什么口味', '成分', '保质期', '规格', '重量', '包装', '怎么吃', '好吃吗', '什么味道', '多大的'],
    priority: 2
  },
  positive_interaction: {
    keywords: ['好吃', '好看', '喜欢', '推荐', '不错', '赞', '棒', '厉害', '太好了', '完美', '支持'],
    priority: 3
  }
};

/**
 * 识别消息意图
 * @param {string} message 用户消息
 * @returns {object} { intent: string, confidence: number, matchedKeywords: string[] }
 */
function detectIntent(message) {
  if (!message || typeof message !== 'string') {
    return { intent: 'other', confidence: 0, matchedKeywords: [] };
  }
  
  const normalizedMsg = message.toLowerCase();
  let bestMatch = { intent: 'other', confidence: 0, matchedKeywords: [] };
  
  for (const [intent, config] of Object.entries(INTENT_PATTERNS)) {
    const matchedKeywords = config.keywords.filter(kw => normalizedMsg.includes(kw));
    
    if (matchedKeywords.length > 0) {
      // 计算置信度：匹配关键词数量 / 消息长度 * 权重
      const confidence = (matchedKeywords.length / Math.max(message.length, 1)) * 100;
      
      if (confidence > bestMatch.confidence || 
          (confidence > 0 && config.priority < (INTENT_PATTERNS[bestMatch.intent]?.priority || 99))) {
        bestMatch = {
          intent,
          confidence: Math.min(confidence * 10, 100), // 放大置信度
          matchedKeywords
        };
      }
    }
  }
  
  return bestMatch;
}

/**
 * 生成回复内容
 * @param {string} intent 意图类型
 * @param {object} context 上下文 { author, products, replyStyle }
 * @returns {string} 回复内容
 */
function generateReply(intent, context = {}) {
  const { author = '亲', products = [], replyStyle = '活泼' } = context;
  
  const templates = {
    price_inquiry: () => {
      if (products.length > 0) {
        const p = products[0];
        return `${p.name}现在售价${p.price}哦～ 点击链接直接下单：${p.link} 🛒 有任何问题随时问我！`;
      }
      return '亲，欢迎咨询价格！请告诉我您想了解哪个产品，我来为您详细介绍～ 💕';
    },
    
    stock_inquiry: () => {
      if (products.length > 0) {
        const p = products[0];
        if (p.stock > 0) {
          return `有货哦！目前还有${p.stock}件，手慢无～ 赶紧下单：${p.link} 🔥`;
        }
        return '宝宝不好意思，这款暂时缺货了😢 已经在补货啦，关注我们第一时间通知你！';
      }
      return '亲，大部分商品都有现货哦！具体哪款您想了解？我来帮您确认库存～ 📦';
    },
    
    bargain: () => {
      return '宝宝，价格已经是最优惠啦，真的没办法再低了😭 不过关注我们，活动期间会有折扣哦！💕';
    },
    
    urge_shipping: () => {
      return '亲，您的订单正在处理中，我们会尽快安排发货的！感谢您的耐心等待 🙏 有问题随时问我哦～';
    },
    
    product_inquiry: () => {
      return '感谢您的咨询！更多产品详情可以查看商品页面哦～ 有任何问题随时问我！💕';
    },
    
    positive_interaction: () => {
      return '谢谢宝宝的喜欢！❤️ 你的支持是我们最大的动力～ 下次还要来哦！🎉';
    },
    
    other: () => {
      return null; // 返回 null 表示需要 AI 自由生成
    }
  };
  
  const template = templates[intent] || templates.other;
  return template();
}

// 导出函数（如果在 Node 环境）
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { detectIntent, generateReply, INTENT_PATTERNS };
}
