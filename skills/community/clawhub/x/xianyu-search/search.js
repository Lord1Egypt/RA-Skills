#!/usr/bin/env node

/**
 * 闲鱼搜索技能 - 主搜索脚本
 * 支持搜索闲鱼、转转、拍拍等二手平台
 */

const CONFIG = {
  platforms: {
    xianyu: {
      name: '闲鱼',
      baseUrl: 'https://www.goofish.com',
      searchUrl: (keyword) => `https://www.goofish.com/search?q=${encodeURIComponent(keyword)}`,
      itemUrl: (itemId) => `https://www.goofish.com/item?id=${itemId}`,
      homeUrl: 'https://www.goofish.com',
      safetyUrl: 'https://www.goofish.com/safety',
      helpUrl: 'https://www.goofish.com/help',
    },
    zhuanzhuan: {
      name: '转转',
      baseUrl: 'https://www.zhuanzhuan.com',
      searchUrl: (keyword) => `https://www.zhuanzhuan.com/zz/pc/list?kw=${encodeURIComponent(keyword)}`,
      itemUrl: (itemId) => `https://www.zhuanzhuan.com/pc/detail?id=${itemId}`,
      homeUrl: 'https://www.zhuanzhuan.com',
    },
    paipai: {
      name: '拍拍',
      baseUrl: 'https://www.paipai.com',
      searchUrl: (keyword) => `https://www.paipai.com/so/0_0_0_0_20_0_0_0?keyword=${encodeURIComponent(keyword)}`,
      itemUrl: (itemId) => `https://www.paipai.com/paipai/goods/${itemId}`,
      homeUrl: 'https://www.paipai.com',
    },
  },
  // 第三方服务链接
  services: {
    yanhuobao: {
      name: '验货宝',
      url: 'https://www.yanhuobao.com',
    },
    aihuishou: {
      name: '爱回收',
      url: 'https://www.aihuishou.com',
    },
    '12315': {
      name: '12315 投诉',
      url: 'https://www.12315.cn',
    },
  },
};

/**
 * 搜索参数配置
 */
class SearchConfig {
  constructor(options) {
    this.keyword = options.keyword || '';
    this.budget = options.budget || 0;
    this.budgetMax = options.budgetMax || this.budget + 200;
    this.condition = options.condition || '9 成新';
    this.batteryMin = options.batteryMin || 80;
    this.requireNoRepair = options.requireNoRepair !== false;
    this.requireGoodCredit = options.requireGoodCredit !== false;
    this.platform = options.platform || 'xianyu';
    this.location = options.location || '';
  }

  /**
   * 生成搜索关键词
   */
  getSearchKeywords() {
    const keywords = [this.keyword];
    
    // 添加成色关键词
    if (this.condition) {
      keywords.push(this.condition);
    }
    
    // 添加价格范围
    if (this.budget > 0) {
      keywords.push(`${this.budget}`);
    }
    
    return keywords.join(' ');
  }

  /**
   * 生成平台搜索 URL
   */
  getSearchUrl(platform = this.platform) {
    const platformConfig = CONFIG.platforms[platform];
    if (!platformConfig) {
      throw new Error(`不支持的平台：${platform}`);
    }
    return platformConfig.searchUrl(this.getSearchKeywords());
  }
}

/**
 * 商品信息解析
 */
class ProductItem {
  constructor(data) {
    this.title = data.title || '';
    this.price = data.price || 0;
    this.location = data.location || '';
    this.credit = data.credit || '';
    this.battery = data.battery || '';
    this.condition = data.condition || '';
    this.url = data.url || '';
    this.highlights = data.highlights || [];
    this.warnings = data.warnings || [];
  }

  /**
   * 是否符合预算要求
   */
  matchesBudget(budget, budgetMax) {
    return this.price >= budget * 0.8 && this.price <= budgetMax;
  }

  /**
   * 是否符合电池要求
   */
  matchesBattery(minBattery) {
    if (!this.battery || this.battery === '未说明') return true;
    const batteryNum = parseInt(this.battery);
    return isNaN(batteryNum) || batteryNum >= minBattery;
  }

  /**
   * 是否符合信用要求
   */
  matchesCredit(requireGood) {
    if (!requireGood) return true;
    const goodCredits = ['百分百好评', '卖家信用极好', '卖家信用优秀', '信用极好'];
    return goodCredits.some(c => this.credit.includes(c));
  }
}

/**
 * 生成推荐报告 - 增强版（含 Top3 推荐和避坑提醒）
 */
function generateReport(config, products) {
  const lines = [];
  const platformConfig = CONFIG.platforms[config.platform] || CONFIG.platforms.xianyu;
  
  // 标题 + 搜索链接
  lines.push(`## 🎯 闲鱼搜索结果：${config.keyword}`);
  lines.push('');
  lines.push(`**🔗 搜索页面**：[${config.getSearchUrl()}](${config.getSearchUrl()})`);
  lines.push('');
  
  // 按价格分组
  const underBudget = products.filter(p => p.price < config.budget);
  const nearBudget = products.filter(p => p.price >= config.budget && p.price <= config.budgetMax);
  
  // 预算内推荐
  if (underBudget.length > 0) {
    lines.push(`### 🏆 预算内推荐（¥${config.budget}以下）`);
    lines.push('');
    lines.push('| 价格 | 配置 | 地区 | 信用 | 亮点 | 商品链接 |');
    lines.push('|------|------|------|------|------|----------|');
    underBudget.slice(0, 5).forEach(p => {
      const configText = p.highlights[0] || p.condition || '详见商品页';
      lines.push(`| **¥${p.price}** | ${configText} | ${p.location} | ${p.credit || '-'} | ${p.highlights.slice(0, 2).join('，')} | [查看商品](${p.url}) |`);
    });
    lines.push('');
  }
  
  // 预算附近推荐
  if (nearBudget.length > 0) {
    lines.push(`### ✅ 预算附近（¥${config.budget}-${config.budgetMax}）`);
    lines.push('');
    lines.push('| 价格 | 配置 | 地区 | 信用 | 亮点 | 商品链接 |');
    lines.push('|------|------|------|------|------|----------|');
    nearBudget.slice(0, 5).forEach(p => {
      const configText = p.highlights[0] || p.condition || '详见商品页';
      lines.push(`| **¥${p.price}** | ${configText} | ${p.location} | ${p.credit || '-'} | ${p.highlights.slice(0, 2).join('，')} | [查看商品](${p.url}) |`);
    });
    lines.push('');
  }
  
  // 筛选符合条件的商品
  const matched = products.filter(p => 
    p.matchesBudget(config.budget, config.budgetMax) &&
    p.matchesBattery(config.batteryMin) &&
    p.matchesCredit(config.requireGoodCredit)
  );
  
  // 🏅 Top 3 最推荐（详细卡片格式）
  if (matched.length > 0) {
    lines.push('### 🏅 最推荐 Top 3');
    lines.push('');
    
    // 按不同维度排序选出 Top3
    const topByBattery = [...matched].sort((a, b) => {
      const batA = parseInt(a.battery) || 0;
      const batB = parseInt(b.battery) || 0;
      return batB - batA;
    })[0];
    
    const topByPrice = [...matched].sort((a, b) => a.price - b.price)[0];
    
    const topByCredit = matched.find(p => p.credit.includes('极好') || p.credit.includes('百分百')) || matched[0];
    
    // 🥇 首选推荐
    if (topByBattery) {
      lines.push(`#### 🥇 首选推荐：¥${topByBattery.price} - ${topByBattery.highlights[0] || '电池最新'}`);
      lines.push('');
      lines.push('| 项目 | 详情 |');
      lines.push('|------|------|');
      lines.push(`| **价格** | ¥${topByBattery.price}${topByBattery.price < config.budget ? `（预算内省${config.budget - topByBattery.price}）` : ''} |`);
      lines.push(`| **配置** | ${topByBattery.title.substring(0, 30)}... |`);
      lines.push(`| **电池** | ${topByBattery.battery || '未说明'} ${topByBattery.battery >= 90 ? '⭐' : ''} |`);
      lines.push(`| **成色** | ${topByBattery.condition || '详见商品页'} |`);
      lines.push(`| **信用** | ${topByBattery.credit || '-'} |`);
      lines.push(`| **地区** | ${topByBattery.location} |`);
      lines.push(`| **亮点** | ${topByBattery.highlights.slice(0, 2).join('，')} |`);
      lines.push(`| **链接** | [立即查看](${topByBattery.url}) |`);
      lines.push('');
      lines.push(`**推荐理由**：${topByBattery.highlights.join('，')}，性价比高，值得优先考虑。`);
      lines.push('');
    }
    
    // 🥈 性价比之选
    if (topByPrice && topByPrice !== topByBattery) {
      lines.push(`#### 🥈 性价比之选：¥${topByPrice.price} - 价格最优`);
      lines.push('');
      lines.push('| 项目 | 详情 |');
      lines.push('|------|------|');
      lines.push(`| **价格** | ¥${topByPrice.price}（预算内） |`);
      lines.push(`| **配置** | ${topByPrice.title.substring(0, 30)}... |`);
      lines.push(`| **成色** | ${topByPrice.condition || '详见商品页'} |`);
      lines.push(`| **亮点** | ${topByPrice.highlights.slice(0, 2).join('，')} |`);
      lines.push(`| **链接** | [立即查看](${topByPrice.url}) |`);
      lines.push('');
      lines.push(`**推荐理由**：同配置价格最低，适合追求性价比的买家。`);
      lines.push('');
    }
    
    // 🥉 售后好/信用好
    if (topByCredit && topByCredit !== topByBattery && topByCredit !== topByPrice) {
      lines.push(`#### 🥉 售后好：¥${topByCredit.price} - ${topByCredit.credit}`);
      lines.push('');
      lines.push('| 项目 | 详情 |');
      lines.push('|------|------|');
      lines.push(`| **价格** | ¥${topByCredit.price} |`);
      lines.push(`| **信用** | ${topByCredit.credit} |`);
      lines.push(`| **地区** | ${topByCredit.location} |`);
      lines.push(`| **亮点** | ${topByCredit.highlights.slice(0, 2).join('，')} |`);
      lines.push(`| **链接** | [立即查看](${topByCredit.url}) |`);
      lines.push('');
      lines.push(`**推荐理由**：卖家信用好，售后有保障，交易更安心。`);
      lines.push('');
    }
  }
  
  // ⚠️ 避坑提醒
  lines.push('### ⚠️ 避坑提醒');
  lines.push('');
  lines.push('| 价格 | 问题 | 原因 |');
  lines.push('|------|------|------|');
  
  // 检测问题商品
  const noScreen = products.find(p => p.title.includes('无头骑士') || p.title.includes('下半套') || p.title.includes('下半部'));
  if (noScreen) {
    lines.push(`| ¥${noScreen.price} | 无头骑士（下半套） | 没有屏幕，需自备显示器 |`);
  }
  
  const mdmLock = products.find(p => p.title.includes('企业') || p.title.includes('MDM') || p.title.includes('监管机'));
  if (mdmLock) {
    lines.push(`| ¥${mdmLock.price} | 企业 MDM 机 | 需要绕过，有风险 |`);
  }
  
  const broken = products.find(p => p.title.includes('指纹不可用') || p.title.includes('故障') || p.title.includes('损坏'));
  if (broken) {
    lines.push(`| ¥${broken.price} | ${broken.highlights[0] || '硬件故障'} | 影响使用体验 |`);
  }
  
  if (!noScreen && !mdmLock && !broken) {
    lines.push('| - | 暂无明显问题商品 | 仍需仔细验机 |');
  }
  lines.push('');
  
  // 购买建议
  lines.push('### 💡 购买建议');
  lines.push('');
  lines.push('**验机要点**：');
  lines.push('- [ ] 要求卖家提供电池健康度截图（系统报告→电源）');
  lines.push('- [ ] 视频验机（屏幕、键盘、所有接口）');
  lines.push('- [ ] 确认无 ID 锁（要求卖家当面退出 iCloud）');
  lines.push('- [ ] 检查序列号（官网查询保修状态）');
  lines.push('');
  lines.push('**砍价话术**：');
  lines.push('```');
  lines.push(`你好，诚心想买，看你信用特别好，`);
  lines.push(`机器描述也很实在。预算只有${config.budget}，`);
  lines.push(`可以的话我马上拍，不墨迹。`);
  lines.push(`电池健康度能截个图吗？`);
  lines.push(`有没有磕碰划痕？能发个详细视频吗？`);
  lines.push('```');
  lines.push('');
  lines.push('**注意事项**：');
  lines.push('⚠️ 走平台担保交易，不要直接转账');
  lines.push(`⚠️ 优先选择支持 [验货宝](${CONFIG.services.yanhuobao.url})/面交的商品`);
  lines.push('⚠️ 保留聊天记录和交易凭证');
  lines.push('⚠️ 收到货后尽快验机，有问题及时沟通');
  lines.push('');
  lines.push('### 🔗 快速链接');
  lines.push(`- [${platformConfig.name}首页](${platformConfig.homeUrl})`);
  lines.push(`- [${platformConfig.name}安全中心](${platformConfig.safetyUrl || platformConfig.homeUrl + '/safety'})`);
  lines.push(`- [${platformConfig.name}客服帮助](${platformConfig.helpUrl || platformConfig.homeUrl + '/help'})`);
  lines.push(`- [验货宝服务](${CONFIG.services.yanhuobao.url})`);
  lines.push(`- [12315 投诉](${CONFIG.services['12315'].url})`);
  
  return lines.join('\n');
}

/**
 * 主函数 - 执行搜索
 */
async function searchProducts(options) {
  const config = new SearchConfig(options);
  
  console.log(`🔍 开始搜索：${config.keyword}`);
  console.log(`💰 预算范围：¥${config.budget} - ¥${config.budgetMax}`);
  console.log(`📍 优先地区：${config.location || '不限'}`);
  console.log(`🔗 搜索链接：${config.getSearchUrl()}`);
  console.log('');
  
  // 注意：由于闲鱼有反爬虫机制，实际使用时需要：
  // 1. 用户手动点击搜索链接查看
  // 2. 或者使用浏览器自动化工具抓取
  // 这里返回搜索链接和配置，由用户自行查看
  
  return {
    config,
    searchUrl: config.getSearchUrl(),
    message: `由于闲鱼平台有反爬虫机制，请点击上方链接查看实时商品列表。`,
  };
}

// 导出模块
module.exports = {
  SearchConfig,
  ProductItem,
  generateReport,
  searchProducts,
  CONFIG,
};
