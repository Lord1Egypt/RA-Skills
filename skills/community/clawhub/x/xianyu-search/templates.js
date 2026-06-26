/**
 * 输出模板 - 格式化商品推荐报告
 * 注意：本模块不依赖外部 CONFIG，所有平台配置内联定义
 */

// 平台配置（内联定义，避免依赖外部 CONFIG）
const PLATFORM_CONFIG = {
  xianyu: {
    name: '闲鱼',
    baseUrl: 'https://www.goofish.com',
    searchUrl: (keyword) => `https://www.goofish.com/search?q=${encodeURIComponent(keyword)}`,
    homeUrl: 'https://www.goofish.com',
    safetyUrl: 'https://www.goofish.com/safety',
    helpUrl: 'https://www.goofish.com/help',
  },
  zhuanzhuan: {
    name: '转转',
    baseUrl: 'https://www.zhuanzhuan.com',
    searchUrl: (keyword) => `https://www.zhuanzhuan.com/zz/pc/list?kw=${encodeURIComponent(keyword)}`,
    homeUrl: 'https://www.zhuanzhuan.com',
  },
  paipai: {
    name: '拍拍',
    baseUrl: 'https://www.paipai.com',
    searchUrl: (keyword) => `https://www.paipai.com/so/0_0_0_0_20_0_0_0?keyword=${encodeURIComponent(keyword)}`,
    homeUrl: 'https://www.paipai.com',
  },
};

// 第三方服务配置
const SERVICE_CONFIG = {
  yanhuobao: { name: '验货宝', url: 'https://www.yanhuobao.com' },
  aihuishou: { name: '爱回收', url: 'https://www.aihuishou.com' },
  '12315': { name: '12315 投诉', url: 'https://www.12315.cn' },
};

/**
 * 生成商品卡片表格
 */
function generateProductTable(products, options = {}) {
  const {
    showLink = true,
    showHighlights = true,
    maxItems = 10,
  } = options;

  const lines = [];
  
  lines.push('| 价格 | 地区 | 电池 | 信用 | 亮点 | 链接 |');
  lines.push('|------|------|------|------|------|------|');
  
  products.slice(0, maxItems).forEach(p => {
    const price = p.price ? `¥${p.price}` : '面议';
    const location = p.location || '不限';
    const battery = p.battery || '未说明';
    const credit = p.credit || '未标注';
    const highlights = showHighlights ? (p.highlights?.slice(0, 2).join('，') || '-') : '-';
    const link = showLink && p.url ? `[查看](${p.url})` : '-';
    
    lines.push(`| **${price}** | ${location} | ${battery} | ${credit} | ${highlights} | ${link} |`);
  });
  
  return lines.join('\n');
}

/**
 * 生成验机清单
 */
function generateChecklist(productType = 'general') {
  const checklists = {
    general: [
      '要求卖家提供实物视频',
      '确认商品功能正常',
      '检查外观成色',
      '确认配件齐全',
    ],
    laptop: [
      '要求卖家提供电池健康度截图（系统报告→电源）',
      '视频验机（屏幕、键盘、所有接口）',
      '确认无 ID 锁（要求卖家当面退出 iCloud）',
      '检查序列号（官网查询保修状态）',
      '运行测试软件（如 AIDA64、coconutBattery）',
      '检查屏幕坏点',
      '测试所有 USB 接口',
      '测试 WiFi/蓝牙',
    ],
    phone: [
      '检查 IMEI 码（拨号盘输入*#06#）',
      '确认无 ID 锁/账户锁',
      '测试 Face ID/Touch ID',
      '检查屏幕是否有划痕/坏点',
      '测试摄像头（前后）',
      '测试扬声器和麦克风',
      '检查电池健康度',
    ],
    camera: [
      '检查快门次数',
      '测试对焦功能',
      '检查 CMOS 是否有灰尘/划痕',
      '测试所有按键和拨轮',
      '检查镜头卡口',
    ],
  };
  
  const items = checklists[productType] || checklists.general;
  
  const lines = [];
  items.forEach(item => {
    lines.push(`- [ ] ${item}`);
  });
  
  return lines.join('\n');
}

/**
 * 生成砍价话术
 */
function generateBargainingScript(budget, productName = '') {
  return `你好，诚心想买${productName ? `这台${productName}` : ''}，
看你信用特别好，机器描述也很实在。
预算只有${budget}元，可以的话我马上拍，不墨迹。
${productName.includes('MacBook') || productName.includes('电脑') ? '电池健康度能截个图吗？' : ''}
有没有磕碰划痕？能发个详细视频吗？`;
}

/**
 * 生成注意事项
 */
function generateWarnings() {
  const lines = [
    '⚠️ 走平台担保交易，不要直接转账',
    '⚠️ 优先选择支持 [验货宝](https://www.yanhuobao.com)/面交的商品',
    '⚠️ 保留聊天记录和交易凭证',
    '⚠️ 收到货后尽快验机，有问题及时沟通',
    '⚠️ 价格过低需谨慎，谨防诈骗',
  ];
  
  return lines.join('\n');
}

/**
 * 生成快速链接部分
 */
function generateQuickLinks(platform = 'xianyu') {
  const links = {
    xianyu: {
      name: '闲鱼',
      home: 'https://www.goofish.com',
      safety: 'https://www.goofish.com/safety',
      help: 'https://www.goofish.com/help',
    },
    zhuanzhuan: {
      name: '转转',
      home: 'https://www.zhuanzhuan.com',
    },
    paipai: {
      name: '拍拍',
      home: 'https://www.paipai.com',
    },
  };
  
  const p = links[platform] || links.xianyu;
  
  const lines = [
    '### 🔗 快速链接',
    `- [${p.name}首页](${p.home})`,
  ];
  
  if (p.safety) {
    lines.push(`- [${p.name}安全中心](${p.safety})`);
  }
  if (p.help) {
    lines.push(`- [${p.name}客服帮助](${p.help})`);
  }
  lines.push('- [验货宝服务](https://www.yanhuobao.com)');
  lines.push('- [12315 投诉](https://www.12315.cn)');
  
  return lines.join('\n');
}

/**
 * 生成完整报告 - 增强版
 */
function generateFullReport(config, products, productType = 'general') {
  const lines = [];
  const platformConfig = PLATFORM_CONFIG[config.platform] || PLATFORM_CONFIG.xianyu;
  
  // 标题 + 搜索链接
  lines.push(`## 🎯 闲鱼搜索结果：${config.keyword}`);
  lines.push('');
  lines.push(`**🔗 搜索页面**：[${platformConfig.searchUrl(config.keyword)}](${platformConfig.searchUrl(config.keyword)})`);
  lines.push('');
  lines.push(`**搜索条件**：预算 ¥${config.budget}-${config.budgetMax} | 成色 ${config.condition} | 电池≥${config.batteryMin}%`);
  lines.push('');
  
  // 按价格分组
  const underBudget = products.filter(p => p.price < config.budget);
  const nearBudget = products.filter(p => p.price >= config.budget && p.price <= config.budgetMax);
  
  // 预算内推荐
  if (underBudget.length > 0) {
    lines.push(`### 🏆 预算内推荐（¥${config.budget}以下）`);
    lines.push('');
    lines.push(generateProductTable(underBudget.slice(0, 5)));
    lines.push('');
  }
  
  // 预算附近推荐
  if (nearBudget.length > 0) {
    lines.push(`### ✅ 预算附近（¥${config.budget}-${config.budgetMax}）`);
    lines.push('');
    lines.push(generateProductTable(nearBudget.slice(0, 5), { showHighlights: true }));
    lines.push('');
  }
  
  // 🏅 Top 3 推荐
  lines.push('### 🏅 最推荐 Top 3');
  lines.push('');
  lines.push(generateTop3Cards(products, config));
  lines.push('');
  
  // ⚠️ 避坑提醒
  lines.push('### ⚠️ 避坑提醒');
  lines.push('');
  lines.push(generateAvoidPitfalls(products));
  lines.push('');
  
  // 购买建议
  lines.push('### 💡 购买建议');
  lines.push('');
  lines.push('**验机要点**：');
  lines.push('');
  lines.push(generateChecklist(productType));
  lines.push('');
  lines.push('**砍价话术**：');
  lines.push('```');
  lines.push(generateBargainingScript(config.budget, config.keyword));
  lines.push('```');
  lines.push('');
  lines.push('**注意事项**：');
  lines.push('');
  lines.push(generateWarnings());
  lines.push('');
  lines.push(generateQuickLinks(config.platform));
  
  return lines.join('\n');
}

/**
 * 生成 Top 3 推荐卡片
 */
function generateTop3Cards(products, config) {
  const lines = [];
  
  // 筛选符合条件的
  const matched = products.filter(p => 
    p.price >= config.budget * 0.8 && 
    p.price <= config.budgetMax
  );
  
  if (matched.length === 0) return '暂无符合预算的商品';
  
  // 按不同维度排序
  const topByBattery = [...matched].sort((a, b) => {
    const batA = parseInt(a.battery) || 0;
    const batB = parseInt(b.battery) || 0;
    return batB - batA;
  })[0];
  
  const topByPrice = [...matched].sort((a, b) => a.price - b.price)[0];
  
  const topByCredit = matched.find(p => p.credit && (p.credit.includes('极好') || p.credit.includes('百分百'))) || matched[0];
  
  // 🥇
  if (topByBattery) {
    const savings = config.budget - topByBattery.price;
    lines.push(`#### 🥇 首选推荐：¥${topByBattery.price} - ${topByBattery.highlights[0] || '电池最新'}`);
    lines.push('');
    lines.push('| 项目 | 详情 |');
    lines.push('|------|------|');
    lines.push(`| **价格** | ¥${topByBattery.price}${savings > 0 ? `（预算内省¥${savings}）` : ''} |`);
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
  
  // 🥈
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
  
  // 🥉
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
  
  return lines.join('\n');
}

/**
 * 生成避坑提醒
 */
function generateAvoidPitfalls(products) {
  const lines = [];
  lines.push('| 价格 | 问题 | 原因 |');
  lines.push('|------|------|------|');
  
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
  
  return lines.join('\n');
}

module.exports = {
  generateProductTable,
  generateChecklist,
  generateBargainingScript,
  generateWarnings,
  generateQuickLinks,
  generateTop3Cards,
  generateAvoidPitfalls,
  generateFullReport,
};
