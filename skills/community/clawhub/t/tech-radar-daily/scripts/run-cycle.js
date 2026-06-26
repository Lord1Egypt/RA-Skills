#!/usr/bin/env node

/**
 * Tech Radar Daily - 核心运行逻辑
 * 每日扫描技术情报并推送到飞书
 */

const fs = require('fs');
const path = require('path');

// 导入各模块
const collectors = require('./collectors');
const filter = require('./filter');
const scorer = require('./scorer');
const summarizer = require('./summarizer');
const { sendToFeishu } = require('./feishu-sender');

// 超时设置 - 10 分钟
const TIMEOUT_MS = 600 * 1000;

// 主函数
async function main() {
  console.log(`[${new Date().toISOString()}] 🚀 Tech Radar Daily 开始运行`);
  
  const startTime = Date.now();
  const timeout = setTimeout(() => {
    console.error('❌ 运行超时，强制退出');
    process.exit(1);
  }, TIMEOUT_MS);

  try {
    // 1. 收集数据
    console.log('\n📡 第一步：收集情报源数据...');
    const rawData = await collectAllSources();
    console.log(`✅ 收集到 ${rawData.length} 条原始数据`);

    // 2. 过滤去重
    console.log('\n🔍 第二步：过滤和去重...');
    const filteredData = await filter.filterAndDedupe(rawData);
    console.log(`✅ 过滤后剩余 ${filteredData.length} 条`);

    // 3. 评分排序
    console.log('\n📊 第三步：价值评分...');
    const scoredData = await scorer.scoreProjects(filteredData);
    const topProjects = scoredData.slice(0, 9); // 取前 9 个
    console.log(`✅ 选出 ${topProjects.length} 条高价值情报`);

    // 4. 生成摘要
    console.log('\n✍️ 第四步：生成 AI 摘要...');
    const finalData = await summarizer.generateSummaries(topProjects);

    // 5. 格式化输出
    console.log('\n📝 第五步：格式化日报...');
    const report = formatDailyReport(finalData);
    const grouped = groupBySource(finalData);
    
    // 6. 保存本地存档
    const date = new Date().toISOString().split('T')[0];
    const archivePath = path.join(__dirname, '../logs/daily', `${date}.md`);
    fs.writeFileSync(archivePath, report, 'utf-8');
    console.log(`✅ 日报已存档：${archivePath}`);

    // 7. 推送到飞书
    if (process.env.FEISHU_WEBHOOK_URL && !process.argv.includes('--test')) {
      console.log('\n📤 第六步：推送到飞书...');
      await sendToFeishu(report);
      console.log('✅ 推送成功！');
    } else {
      console.log('\n⚠️ 测试模式或未配置飞书 Webhook，跳过推送');
      console.log('\n=== 日报内容 ===\n');
      console.log(report);
    }

    // 8. 更新去重数据库
    await updateSeenRepos(topProjects);
    
    // 9. 记录每日 stats 日志
    const stats = {
      date: new Date().toISOString().split('T')[0],
      collected: rawData.length,
      filtered: filteredData.length,
      sent: topProjects.length,
      sources: {
        github: grouped.github ? grouped.github.length : 0,
        tools: grouped.tools ? grouped.tools.length : 0,
        product: grouped.product ? grouped.product.length : 0,
        trend: grouped.trend ? grouped.trend.length : 0,
        awesome: grouped.awesome ? grouped.awesome.length : 0
      },
      duration: Math.round((Date.now() - startTime) / 1000),
      timestamp: new Date().toISOString()
    };
    
    const statsPath = path.join(__dirname, '../data/stats', `${stats.date}.json`);
    try {
      // 确保目录存在
      const statsDir = path.join(__dirname, '../data/stats');
      if (!fs.existsSync(statsDir)) {
        fs.mkdirSync(statsDir, { recursive: true });
      }
      fs.writeFileSync(statsPath, JSON.stringify(stats, null, 2), 'utf-8');
      console.log(`📊 Stats 已记录：${statsPath}`);
    } catch (e) {
      console.error('⚠️ 记录 stats 失败:', e.message);
    }

    const duration = Math.round((Date.now() - startTime) / 1000);
    console.log(`\n✅ Tech Radar Daily 运行完成！用时 ${duration} 秒`);
    
  } catch (error) {
    console.error('\n❌ 运行出错:', error);
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

// 收集所有情报源
async function collectAllSources() {
  const sources = [
    { name: 'GitHub Trending', fn: collectors.collectGitHubTrending },
    { name: 'GitHub Topics', fn: collectors.collectGitHubTopics },
    { name: 'Product Hunt', fn: collectors.collectProductHunt },
    { name: 'Hacker News', fn: collectors.collectHackerNews },
    { name: 'Awesome Lists', fn: collectors.collectAwesomeLists }
  ];

  const allData = [];
  
  for (const source of sources) {
    try {
      console.log(` 📡 正在扫描：${source.name}...`);
      const data = await source.fn();
      allData.push(...data);
      console.log(` ✅ ${source.name}: 获取 ${data.length} 条`);
    } catch (error) {
      console.error(` ❌ ${source.name} 失败:`, error.message);
    }
  }

  return allData;
}

// 格式化日报
function formatDailyReport(projects) {
  const date = new Date().toLocaleDateString('zh-CN');
  const grouped = groupBySource(projects);
  
  let report = `# 📡 Tech Radar Daily — ${date}\n\n`;
  report += `> 今日精选 ${projects.length} 条高价值技术情报\n\n`;
  report += `---\n\n`;

  // 1. GitHub Trending
  if (grouped.github && grouped.github.length > 0) {
    report += `## 1️⃣ GitHub Trending (${grouped.github.length} 个)\n\n`;
    grouped.github.forEach(item => {
      report += formatGitHubItem(item);
    });
  }

  // 2. 有趣小工具
  if (grouped.tools && grouped.tools.length > 0) {
    report += `## 2️⃣ 有趣小工具 (${grouped.tools.length} 个)\n\n`;
    grouped.tools.forEach(item => {
      report += formatToolItem(item);
    });
  }

  // 3. 赚钱项目
  if (grouped.product && grouped.product.length > 0) {
    report += `## 3️⃣ 赚钱项目 (${grouped.product.length} 个)\n\n`;
    grouped.product.forEach(item => {
      report += formatProductItem(item);
    });
  }

  // 4. 技术趋势
  if (grouped.trend && grouped.trend.length > 0) {
    report += `## 4️⃣ 技术趋势 (${grouped.trend.length} 个)\n\n`;
    grouped.trend.forEach(item => {
      report += formatTrendItem(item);
    });
  }

  // 5. Awesome Lists
  if (grouped.awesome && grouped.awesome.length > 0) {
    report += `## 5️⃣ Awesome Lists 挖宝 (${grouped.awesome.length} 个)\n\n`;
    grouped.awesome.forEach(item => {
      report += formatAwesomeItem(item);
    });
  }

  // 统计
  report += `---\n\n`;
  report += `## 📊 今日统计\n\n`;
  report += `- 总情报数：${projects.length} 条\n`;
  report += `- 新增工具：${grouped.tools ? grouped.tools.length : 0} 个\n`;
  report += `- GitHub 项目：${grouped.github ? grouped.github.length : 0} 个\n`;
  
  return report;
}

// 按来源分组
function groupBySource(projects) {
  const grouped = {};
  projects.forEach(item => {
    const type = item.sourceType || 'other';
    if (!grouped[type]) grouped[type] = [];
    grouped[type].push(item);
  });
  return grouped;
}

// 格式化各类项目
function formatGitHubItem(item) {
  const scoreText = item.score ? ` (Score: ${item.score})` : '';
  return `### ${item.trend || ''} ${item.name}${scoreText} ${item.confidence || ''}\n` +
    `- **Star**: +${item.starsToday || '?'}/${item.stars || '?'}\n` +
    `- **描述**: ${item.description || '无描述'}\n` +
    `- **价值点**: ${item.summary || '待分析'}\n` +
    `- **链接**: ${item.url}\n\n`;
}

function formatToolItem(item) {
  return `### ${item.name}\n` +
    `- **Star**: ${item.stars || '?'}\n` +
    `- **功能**: ${item.description || '无描述'}\n` +
    `- **可部署**: ${item.deployable ? '是' : '否'}\n` +
    `- **链接**: ${item.url}\n\n`;
}

function formatProductItem(item) {
  return `### ${item.name}\n` +
    `- **来源**: Product Hunt #${item.rank || '?'}\n` +
    `- **用户**: ${item.targetUser || '待分析'}\n` +
    `- **收费**: ${item.pricing || '待分析'}\n` +
    `- **可复制性**: ${item.replicability || '待分析'}\n` +
    `- **链接**: ${item.url}\n\n`;
}

function formatTrendItem(item) {
  return `### ${item.title}\n` +
    `- **来源**: Hacker News\n` +
    `- **讨论**: ${item.summary || '待分析'}\n` +
    `- **链接**: ${item.url}\n\n`;
}

function formatAwesomeItem(item) {
  return `### ${item.name}\n` +
    `- **来源**: ${item.awesomeList || 'awesome-list'}\n` +
    `- **功能**: ${item.description || '无描述'}\n` +
    `- **链接**: ${item.url}\n\n`;
}

// 更新去重数据库
async function updateSeenRepos(projects) {
  const seenReposPath = path.join(__dirname, '../data/seen_repos.json');
  let seenRepos = {};
  
  try {
    const data = fs.readFileSync(seenReposPath, 'utf-8');
    seenRepos = JSON.parse(data);
  } catch (e) {
    // 文件不存在或解析失败，使用空对象
  }

  const today = new Date().toISOString().split('T')[0];
  
  projects.forEach(item => {
    if (item.repoName) {
      seenRepos[item.repoName] = {
        first_seen: seenRepos[item.repoName]?.first_seen || today,
        last_recommended: today,
        source: item.source
      };
    }
  });

  fs.writeFileSync(seenReposPath, JSON.stringify(seenRepos, null, 2));
}

// 运行主函数
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { main };
