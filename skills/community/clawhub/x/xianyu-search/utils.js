/**
 * 工具函数
 */

/**
 * 解析自然语言中的预算
 * 例如："预算 2300" -> 2300
 */
function parseBudget(text) {
  const patterns = [
    /预算 [^\d]*(\d+)/,
    /(\d+) 元预算/,
    /(\d+) 块预算/,
    /(\d+) 左右/,
    /(\d+) 以内/,
    /(\d+) 以下/,
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return parseInt(match[1]);
    }
  }
  
  return 0;
}

/**
 * 解析自然语言中的成色要求
 */
function parseCondition(text) {
  const conditions = [
    { pattern: /几乎全新 | 九九新 | 99 新/, value: '几乎全新' },
    { pattern: /95 新 | 九五新/, value: '95 新' },
    { pattern: /9 成新 | 九成?新/, value: '9 成新' },
    { pattern: /8 成新 | 八成?新/, value: '8 成新' },
    { pattern: /7 成新 | 七成?新/, value: '7 成新' },
  ];
  
  for (const { pattern, value } of conditions) {
    if (pattern.test(text)) {
      return value;
    }
  }
  
  return '9 成新';
}

/**
 * 解析自然语言中的电池要求
 */
function parseBattery(text) {
  const patterns = [
    /电池 [^\d]*(\d+)/,
    /电池健康 [^\d]*(\d+)/,
    /电池容量 [^\d]*(\d+)/,
    /(\d+)% 电池/,
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return parseInt(match[1]);
    }
  }
  
  return 80;
}

/**
 * 解析自然语言中的平台偏好
 */
function parsePlatform(text) {
  if (/转转/.test(text)) return 'zhuanzhuan';
  if (/拍拍/.test(text)) return 'paipai';
  if (/闲鱼/.test(text)) return 'xianyu';
  if (/全平台 | 所有平台/.test(text)) return 'all';
  return 'xianyu';
}

/**
 * 解析自然语言中的地区偏好
 */
function parseLocation(text) {
  const cities = [
    '北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '重庆',
    '武汉', '西安', '苏州', '天津', '郑州', '长沙', '沈阳', '青岛',
    '宁波', '东莞', '无锡', '佛山', '福州', '厦门', '合肥', '济南',
  ];
  
  for (const city of cities) {
    if (text.includes(city)) {
      return city;
    }
  }
  
  return '';
}

/**
 * 从自然语言中提取搜索配置
 */
function parseSearchConfig(text) {
  // 提取预算
  let budget = parseBudget(text);
  
  // 提取电池要求
  const batteryMin = parseBattery(text);
  
  // 提取成色
  const condition = parseCondition(text);
  
  // 提取平台
  const platform = parsePlatform(text);
  
  // 提取地区
  const location = parseLocation(text);
  
  // 提取关键词 - 更智能的解析
  let keyword = text;
  
  // 移除常见指令词（按长度排序，长的先匹配）
  const stopWords = [
    '帮我看看', '帮我找', '帮我',
    '闲鱼上的', '转转上的', '拍拍上的',
    '闲鱼上', '转转上', '拍拍上',
    '闲鱼', '转转', '拍拍',
    '搜索', '查找', '看看', '有没有',
    '二手', '的', '有', '吗', '呢', '不', '要', '想', '需', '需要',
  ];
  
  for (const word of stopWords) {
    keyword = keyword.replace(word, '');
  }
  
  // 移除预算相关
  keyword = keyword.replace(/预算 [^\d]*(\d+)/g, '');
  keyword = keyword.replace(/(\d+) 元预算/g, '');
  keyword = keyword.replace(/(\d+) 左右/g, '');
  keyword = keyword.replace(/(\d+) 以内/g, '');
  keyword = keyword.replace(/(\d+) 以下/g, '');
  
  // 移除电池相关
  keyword = keyword.replace(/电池 [^\d]*(\d+)/g, '');
  keyword = keyword.replace(/电池健康 [^\d]*(\d+)/g, '');
  keyword = keyword.replace(/(\d+)% 电池/g, '');
  keyword = keyword.replace(/以上/g, '');
  
  // 移除成色相关
  keyword = keyword.replace(/几乎全新 | 九九新 | 99 新/g, '');
  keyword = keyword.replace(/95 新 | 九五新/g, '');
  keyword = keyword.replace(/9 成新 | 九成?新/g, '');
  keyword = keyword.replace(/8 成新 | 八成?新/g, '');
  
  // 移除地区
  if (location) {
    keyword = keyword.replace(location, '');
  }
  
  // 移除信用相关
  keyword = keyword.replace(/信用好 | 信用极好 | 靠谱/g, '');
  
  // 清理：移除多余空格和数字
  keyword = keyword.trim().replace(/\s+/g, ' ');
  keyword = keyword.replace(/\d{3,}/g, '').trim();
  
  // 如果关键词为空，尝试从原文提取产品名称
  if (!keyword || keyword.length < 2) {
    // 尝试匹配常见产品
    const productPatterns = [
      /MacBook[A-Za-z0-9\s]*/i,
      /iPhone[A-Za-z0-9\s]*/i,
      /iPad[A-Za-z0-9\s]*/i,
      /PS[45]/i,
      /Switch/i,
      /Sony[A-Za-z0-9\s]*/i,
      /Canon[A-Za-z0-9\s]*/i,
      /相机 | 镜头 | 电脑 | 手机 | 平板 | 游戏机/i,
    ];
    
    for (const pattern of productPatterns) {
      const match = text.match(pattern);
      if (match) {
        keyword = match[0].trim();
        break;
      }
    }
  }
  
  return {
    keyword: keyword || '二手商品',
    budget,
    budgetMax: budget + 200,
    condition,
    batteryMin,
    platform,
    location,
    requireNoRepair: true,
    requireGoodCredit: /信用好 | 信用极好 | 靠谱/.test(text),
  };
}

/**
 * 格式化价格
 */
function formatPrice(price) {
  if (!price) return '面议';
  return `¥${price.toLocaleString()}`;
}

/**
 * 生成闲鱼搜索链接
 */
function generateXianyuUrl(keyword, priceMin = 0, priceMax = 0) {
  const baseUrl = 'https://www.goofish.com/search';
  const params = new URLSearchParams();
  params.set('q', keyword);
  
  if (priceMin > 0) params.set('price_min', priceMin);
  if (priceMax > 0) params.set('price_max', priceMax);
  
  return `${baseUrl}?${params.toString()}`;
}

/**
 * 生成转转搜索链接
 */
function generateZhuanzhuanUrl(keyword, priceMin = 0, priceMax = 0) {
  return `https://www.zhuanzhuan.com/zz/pc/list?kw=${encodeURIComponent(keyword)}`;
}

/**
 * 生成拍拍搜索链接
 */
function generatePaipaiUrl(keyword) {
  return `https://www.paipai.com/so/0_0_0_0_20_0_0_0?keyword=${encodeURIComponent(keyword)}`;
}

/**
 * 延迟函数
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 随机选择（用于避免频繁请求）
 */
function randomChoice(array) {
  return array[Math.floor(Math.random() * array.length)];
}

module.exports = {
  parseBudget,
  parseCondition,
  parseBattery,
  parsePlatform,
  parseLocation,
  parseSearchConfig,
  formatPrice,
  generateXianyuUrl,
  generateZhuanzhuanUrl,
  generatePaipaiUrl,
  delay,
  randomChoice,
};
