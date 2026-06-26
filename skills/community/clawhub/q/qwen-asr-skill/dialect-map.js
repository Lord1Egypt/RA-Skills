/**
 * 方言名称映射配置
 * 支持多种方言名称输入方式，统一映射到模型识别的标准名称
 */

module.exports = {
  // 方言别名映射
  dialectAliases: {
    // 粤语
    '粤语': 'Cantonese',
    '广东话': 'Cantonese',
    '广府话': 'Cantonese',
    '白话': 'Cantonese',
    'yue': 'Cantonese',
    'cantonese': 'Cantonese',
    'Cantonese-HK': 'Cantonese',
    'Cantonese-GD': 'Cantonese',
    '香港粤语': 'Cantonese',
    '广东粤语': 'Cantonese',
    
    // 四川话
    '四川话': 'Sichuan',
    '川语': 'Sichuan',
    '川话': 'Sichuan',
    '巴蜀语': 'Sichuan',
    'sichuan': 'Sichuan',
    
    // 东北话
    '东北话': 'Dongbei',
    '东北官话': 'Dongbei',
    'dongbei': 'Dongbei',
    
    // 河南话
    '河南话': 'Henan',
    '豫语': 'Henan',
    'henan': 'Henan',
    
    // 山东话
    '山东话': 'Shandong',
    '鲁语': 'Shandong',
    'shandong': 'Shandong',
    
    // 陕西话
    '陕西话': 'Shaanxi',
    '秦语': 'Shaanxi',
    '关中话': 'Shaanxi',
    'shaanxi': 'Shaanxi',
    
    // 山西话
    '山西话': 'Shanxi',
    '晋语': 'Shanxi',
    'shanxi': 'Shanxi',
    
    // 湖南话
    '湖南话': 'Hunan',
    '湘语': 'Hunan',
    'hunan': 'Hunan',
    
    // 湖北话
    '湖北话': 'Hubei',
    '楚语': 'Hubei',
    'hubei': 'Hubei',
    
    // 安徽话
    '安徽话': 'Anhui',
    '徽语': 'Anhui',
    'anhui': 'Anhui',
    
    // 福建话
    '福建话': 'Fujian',
    '闽语': 'Fujian',
    'fujian': 'Fujian',
    
    // 闽南语
    '闽南语': 'Minnan',
    '闽南话': 'Minnan',
    '台语': 'Minnan',
    '台湾话': 'Minnan',
    'minnan': 'Minnan',
    
    // 吴语
    '吴语': 'Wu',
    '吴越语': 'Wu',
    '江浙话': 'Wu',
    '上海话': 'Wu',
    '苏州话': 'Wu',
    'wu': 'Wu',
    
    // 江西话
    '江西话': 'Jiangxi',
    '赣语': 'Jiangxi',
    'jiangxi': 'Jiangxi',
    
    // 甘肃话
    '甘肃话': 'Gansu',
    '陇语': 'Gansu',
    'gansu': 'Gansu',
    
    // 贵州话
    '贵州话': 'Guizhou',
    '黔语': 'Guizhou',
    'guizhou': 'Guizhou',
    
    // 河北话
    '河北话': 'Hebei',
    '冀语': 'Hebei',
    'hebei': 'Hebei',
    
    // 宁夏话
    '宁夏话': 'Ningxia',
    '宁语': 'Ningxia',
    'ningxia': 'Ningxia',
    
    // 天津话
    '天津话': 'Tianjin',
    'tianjin': 'Tianjin',
    
    // 云南话
    '云南话': 'Yunnan',
    '滇语': 'Yunnan',
    'yunnan': 'Yunnan',
    
    // 浙江话
    '浙江话': 'Zhejiang',
    '浙语': 'Zhejiang',
    'zhejiang': 'Zhejiang',
    
    // 普通话
    '普通话': 'Chinese',
    '国语': 'Chinese',
    '汉语': 'Chinese',
    '中文': 'Chinese',
    'zh': 'Chinese',
    'chinese': 'Chinese',
    'mandarin': 'Chinese',
    
    // 英语
    '英语': 'English',
    '英文': 'English',
    'en': 'English',
    'english': 'English',
    
    // 其他常见语言
    '日语': 'Japanese',
    '日文': 'Japanese',
    'ja': 'Japanese',
    'japanese': 'Japanese',
    
    '韩语': 'Korean',
    '韩文': 'Korean',
    'ko': 'Korean',
    'korean': 'Korean',
    
    '法语': 'French',
    'fr': 'French',
    'french': 'French',
    
    '德语': 'German',
    'de': 'German',
    'german': 'German',
    
    '西班牙语': 'Spanish',
    'es': 'Spanish',
    'spanish': 'Spanish',
    
    '俄语': 'Russian',
    'ru': 'Russian',
    'russian': 'Russian',
    
    '泰语': 'Thai',
    'th': 'Thai',
    'thai': 'Thai',
    
    '越南语': 'Vietnamese',
    'vi': 'Vietnamese',
    'vietnamese': 'Vietnamese',
  },
  
  // 方言代码映射
  dialectCodes: {
    'zh-CN': 'Chinese',
    'zh-HK': 'Cantonese',
    'zh-TW': 'Minnan',
    'zh-YUE': 'Cantonese',
    'zh-WUU': 'Wu',
    'zh-MIN': 'Minnan',
  },
  
  /**
   * 标准化方言名称
   * @param {string} dialect - 输入的方言名称
   * @returns {string} 标准化后的方言名称
   */
  normalize: function(dialect) {
    if (!dialect) return null;
    
    const lowerDialect = dialect.trim().toLowerCase();
    
    // 先检查别名映射
    for (const [alias, standard] of Object.entries(this.dialectAliases)) {
      if (alias.toLowerCase() === lowerDialect) {
        return standard;
      }
    }
    
    // 检查方言代码
    if (this.dialectCodes[dialect]) {
      return this.dialectCodes[dialect];
    }
    
    // 如果没有匹配，尝试模糊匹配
    for (const [alias, standard] of Object.entries(this.dialectAliases)) {
      if (lowerDialect.includes(alias.toLowerCase())) {
        return standard;
      }
    }
    
    // 没有匹配，返回原输入
    return dialect;
  },
  
  /**
   * 获取支持的方言列表
   * @returns {Array} 方言列表
   */
  getSupportedDialects: function() {
    const dialects = new Set();
    
    // 添加所有标准方言名称
    Object.values(this.dialectAliases).forEach(dialect => dialects.add(dialect));
    
    return Array.from(dialects).sort();
  },
  
  /**
   * 获取方言的所有别名
   * @param {string} standardDialect - 标准方言名称
   * @returns {Array} 别名列表
   */
  getAliases: function(standardDialect) {
    const aliases = [];
    
    for (const [alias, standard] of Object.entries(this.dialectAliases)) {
      if (standard === standardDialect) {
        aliases.push(alias);
      }
    }
    
    return aliases;
  }
};