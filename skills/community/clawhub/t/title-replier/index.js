/**
 * Title Replier - 称号回复技能
 * 为 OpenClaw 助手的回复添加随机不重复的称号
 * 
 * @version 1.0.0
 * @author OpenClaw Community
 */

const fs = require('fs');
const path = require('path');

// 称号库
const titles = {
  professional: [
    '资深顾问',
    '技术专家',
    '数据分析师',
    '解决方案架构师',
    '项目顾问',
    '首席顾问',
    '高级分析师',
    '专业助手'
  ],
  humorous: [
    '代码搬运工',
    'Bug 终结者',
    '键盘侠',
    '熬夜冠军',
    '咖啡消耗机',
    '需求粉碎机',
    '逻辑鬼才',
    '摸鱼达人'
  ],
  classical: [
    '谋士',
    '军师',
    '智者',
    '先生',
    '阁下',
    '夫子',
    '真人',
    '居士'
  ],
  modern: [
    '小助手',
    '好帮手',
    '私人助理',
    '智能管家',
    '贴心伙伴',
    '专属顾问',
    '得力助手',
    '贴心小棉袄'
  ]
};

// 历史文件路径
const historyPath = path.join(__dirname, 'history.json');

/**
 * 加载使用历史
 */
function loadHistory() {
  try {
    if (fs.existsSync(historyPath)) {
      const data = fs.readFileSync(historyPath, 'utf-8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('加载历史失败:', error.message);
  }
  return { used: [], style: 'mixed' };
}

/**
 * 保存使用历史
 */
function saveHistory(history) {
  try {
    fs.writeFileSync(historyPath, JSON.stringify(history, null, 2), 'utf-8');
  } catch (error) {
    console.error('保存历史失败:', error.message);
  }
}

/**
 * 获取可用称号
 */
function getAvailableTitles(style = 'mixed', used = []) {
  let titlePool = [];
  
  if (style === 'mixed') {
    // 混合所有风格
    Object.values(titles).forEach(arr => {
      titlePool = titlePool.concat(arr);
    });
  } else if (titles[style]) {
    // 指定风格
    titlePool = titles[style];
  } else {
    // 默认混合
    Object.values(titles).forEach(arr => {
      titlePool = titlePool.concat(arr);
    });
  }
  
  // 过滤已使用的称号
  return titlePool.filter(title => !used.includes(title));
}

/**
 * 随机选择称号
 */
function selectTitle(style = 'mixed', maxHistory = 100) {
  const history = loadHistory();
  let availableTitles = getAvailableTitles(style, history.used);
  
  // 如果所有称号都用过了，清空历史
  if (availableTitles.length === 0) {
    history.used = [];
    availableTitles = getAvailableTitles(style, []);
  }
  
  // 随机选择一个称号
  const randomIndex = Math.floor(Math.random() * availableTitles.length);
  const selectedTitle = availableTitles[randomIndex];
  
  // 记录使用历史
  history.used.push(selectedTitle);
  
  // 限制历史记录大小
  if (history.used.length > maxHistory) {
    history.used = history.used.slice(-maxHistory);
  }
  
  // 保存历史
  saveHistory(history);
  
  return selectedTitle;
}

/**
 * 格式化回复
 */
function formatReply(title, content, showEmoji = true) {
  const emoji = showEmoji ? '🏷️ ' : '';
  return `${emoji}【${title}】\n\n${content}`;
}

/**
 * 主函数 - 生成带称号的回复
 */
function reply(content, options = {}) {
  const {
    style = 'mixed',
    showEmoji = true,
    maxHistory = 100
  } = options;
  
  const title = selectTitle(style, maxHistory);
  return formatReply(title, content, showEmoji);
}

/**
 * CLI 命令处理
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args[0] === 'test') {
    // 测试模式
    const style = args[1] || 'mixed';
    const title = selectTitle(style);
    console.log(`🏷️【${title}】`);
    console.log('\n测试内容：这是一个测试回复');
  } else if (args[0] === 'list') {
    // 列出所有称号
    console.log('称号库：\n');
    Object.entries(titles).forEach(([style, titleList]) => {
      console.log(`${style}:`);
      titleList.forEach(title => console.log(`  - ${title}`));
      console.log();
    });
  } else if (args[0] === 'history') {
    // 显示使用历史
    const history = loadHistory();
    console.log('已使用的称号：');
    history.used.forEach((title, index) => {
      console.log(`  ${index + 1}. ${title}`);
    });
  } else if (args[0] === 'reset') {
    // 重置历史
    saveHistory({ used: [], style: 'mixed' });
    console.log('✅ 历史已重置');
  } else {
    // 显示帮助
    console.log('Title Replier - 称号回复技能 v1.0.0');
    console.log('\n用法:');
    console.log('  node index.js test [style]  - 测试生成称号');
    console.log('  node index.js list          - 列出所有称号');
    console.log('  node index.js history       - 显示使用历史');
    console.log('  node index.js reset         - 重置使用历史');
    console.log('\n可用风格:');
    console.log('  professional - 专业风格');
    console.log('  humorous     - 幽默风格');
    console.log('  classical    - 古风风格');
    console.log('  modern       - 现代风格');
    console.log('  mixed        - 混合风格 (默认)');
  }
}

// 导出模块
module.exports = {
  reply,
  selectTitle,
  formatReply,
  titles,
  loadHistory,
  saveHistory
};

// 如果是直接运行，执行 CLI
if (require.main === module) {
  main();
}
