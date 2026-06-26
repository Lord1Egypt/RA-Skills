#!/usr/bin/env node
/**
 * skill-everyday runner - 抓取 Clawhub 热门技能并生成分析报告
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const SCRIPT_DIR = path.dirname(__filename);
const SKILL_DIR = path.dirname(SCRIPT_DIR);
const DATA_DIR = path.join(SKILL_DIR, 'data');
const REPORTS_DIR = path.join(DATA_DIR, 'reports');
const ANALYZED_FILE = path.join(DATA_DIR, 'analyzed.json');

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
if (!fs.existsSync(REPORTS_DIR)) fs.mkdirSync(REPORTS_DIR, { recursive: true });

if (!fs.existsSync(ANALYZED_FILE)) {
  fs.writeFileSync(ANALYZED_FILE, JSON.stringify({ analyzed: [], lastRun: null }, null, 2));
}

/**
 * 深度模板：与「一、核心工作原理 / 二、为什么受欢迎」结构一致
 */
const SKILL_KNOWLEDGE = {
  'self-improving-agent': {
    structured: true,
    titleLine: 'Self-Improve-Agent Skill（自我进化代理技能）',
    corePrinciple: '闭环式自主学习+本地记忆沉淀+实时反馈修正，让AI越用越聪明',
    section1: `### 1. 触发机制（自动捕获）

- **错误检测**：监听工具执行结果，识别失败/报错/用户纠正
- **三类触发场景**：
  - 命令/工具执行失败 → 写入 \`ERRORS.md\`
  - 用户明确纠正 → 写入 \`LEARNINGS.md\`
  - 新功能/能力缺失 → 写入 \`FEATURE_REQUESTS.md\`
- **每条记录含**：ID、时间、优先级、状态、标签、摘要、上下文、修复方案`,
    section2: `### 2. 记忆系统（本地Markdown驱动）

- **短期记忆**：对话上下文、当前任务状态
- **长期记忆库（\`.learnings/\`）**：
  - \`ERRORS.md\`：错误场景+复现+修复
  - \`LEARNINGS.md\`：用户纠正、知识缺口、最佳实践
  - \`FEATURE_REQUESTS.md\`：能力需求+复杂度评估
- **核心记忆文件（提炼后写入）**：
  - \`claude.md\`：项目事实/约定
  - \`agents.md\`：工作流/分工
  - \`tools.md\`：工具使用心得
  - \`soul.md\`：行为准则/偏好`,
    section3: `### 3. 自我进化闭环（核心）

\`\`\`
交互执行 → 错误/反馈捕获 → 结构化记录 → AI/人工Review → 提炼升级 → 记忆更新 → 下次调用优化
\`\`\`

- **自动反思**：定期复盘日志，识别重复问题、模式、改进点
- **知识复用**：同类场景直接调用记忆，避免重复犯错
- **偏好适配**：学习你的输出格式、技术栈、标准，自动适配
- **能力拓展**：记录需求，自主探索/安装新技能`,
    section4: `### 4. 底层技术栈

- **监控脚本**：\`error-detector.sh\` 实时监听执行结果
- **本地存储**：纯 Markdown，零依赖、可版本控制
- **元认知**：自我评估、自我修正、自我优化（「思考自己的思考」）
- **反馈循环**：强化学习+持续迭代，性能随使用提升`,
    sectionWhy: `## 二、为什么受欢迎

- **零配置、轻量**：本地运行、无外部依赖、易集成
- **越用越准**：自动避坑、适配习惯、沉淀最佳实践
- **透明可控**：记忆可查看/编辑/版本化，不黑盒
- **开发者友好**：适配 OpenClaw 等 Agent 框架，提升研发效率`,
  },
  default: {
    structured: false,
    corePrinciple: '基于 OpenClaw 技能框架实现，通过标准化接口提供服务',
    triggerMechanism: `### 触发机制

- 用户明确请求该功能时激活，或作为工作流步骤被其他技能调用
- 支持配置化触发条件`,
    memorySystem: `### 数据与状态

- 使用本地文件系统存储配置和状态
- 支持配置持久化`,
    evolutionLoop: `### 扩展与迭代

- 通过用户反馈持续改进
- 支持配置扩展`,
    techStack: `### 技术特点

- 标准化技能接口
- 模块化设计
- 易于集成和扩展`,
    whyPopular: `## 为什么受欢迎

- 解决实际需求
- 集成简单
- 社区认可度高`,
  },
};

function buildStructuredReport(skillInfo, knowledge, introText) {
  const meta = [
    `| 项目 | 内容 |`,
    `| --- | --- |`,
    `| 排名 | ${skillInfo.rank} |`,
    `| 技能标识 | \`${skillInfo.slug}\` |`,
    `| 分类 | ${skillInfo.category || '通用'} |`,
    `| 下载 / 点赞 | ${skillInfo.downloads?.toLocaleString() ?? 'N/A'} / ${skillInfo.stars?.toLocaleString() ?? 'N/A'} |`,
  ].join('\n');

  return `## ${knowledge.titleLine}

**核心原理**：${knowledge.corePrinciple}

### Clawhub 简介

${introText || '（暂无官方摘要）'}

${meta}

## 一、核心工作原理（OpenClaw 主流实现）

${knowledge.section1}

${knowledge.section2}

${knowledge.section3}

${knowledge.section4}

${knowledge.sectionWhy}
`;
}

function buildDefaultReport(skillInfo, knowledge, introText) {
  return `**核心原理**：${knowledge.corePrinciple}

### 功能介绍（Clawhub）

${introText || '暂无描述'}

### 核心流程与特点

${knowledge.triggerMechanism}

${knowledge.memorySystem}

${knowledge.evolutionLoop}

${knowledge.techStack}

${knowledge.whyPopular}
`;
}

async function fetchSkillDetail(browser, slug) {
  const page = await browser.newPage();
  try {
    await page.goto(`https://clawhub.ai/skill/${slug}`, {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
    await page.waitForTimeout(3000);

    const title = await page.title();
    const description = await page.$eval('meta[name="description"]', (el) => el.content).catch(() => '');
    const mainDesc = await page.$eval('main', (el) => el.innerText).catch(() => '');

    return { title, description, content: mainDesc.slice(0, 5000) };
  } catch (e) {
    return { error: e.message };
  } finally {
    await page.close();
  }
}

async function run() {
  console.log('📊 skill-everyday 启动...\n');

  let analyzedData = JSON.parse(fs.readFileSync(ANALYZED_FILE, 'utf-8'));

  let apiData = null;
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.route('https://wry-manatee-359.convex.cloud/api/query', async (route) => {
    const response = await route.fetch();
    const data = await response.json();
    apiData = data;
    route.continue();
  });

  const gotoOpts = { waitUntil: 'domcontentloaded', timeout: 120000 };
  console.log('📡 正在获取 Clawhub 技能列表...');
  await page.goto('https://clawhub.ai/skills', gotoOpts);
  await page.waitForTimeout(5000);

  const result = apiData?.status === 'success' ? apiData.value : apiData;
  let skills = result?.page || [];

  skills.sort((a, b) => (b.skill?.stats?.downloads || 0) - (a.skill?.stats?.downloads || 0));

  console.log(`✅ 获取到 ${skills.length} 个技能\n`);

  let targetSkill = null;
  let rank = 0;
  for (let i = 0; i < skills.length; i++) {
    const slug = skills[i].skill?.slug;
    if (!analyzedData.analyzed.includes(slug)) {
      targetSkill = skills[i];
      rank = i + 1;
      break;
    }
  }

  if (!targetSkill) {
    console.log('🎉 所有热门技能都已分析完成！');
    await browser.close();
    return;
  }

  const skillInfo = {
    rank,
    name: targetSkill.skill?.displayName,
    slug: targetSkill.skill?.slug,
    owner: targetSkill.ownerHandle,
    category: targetSkill.skill?.category || '通用',
    downloads: targetSkill.skill?.stats?.downloads,
    stars: targetSkill.skill?.stats?.stars,
    installs: targetSkill.skill?.stats?.installsCurrent,
    summary: targetSkill.skill?.summary,
    version: targetSkill.latestVersion?.version,
  };

  console.log(`📊 将分析排名第 ${rank} 的技能: ${skillInfo.name}`);
  console.log(`   作者: ${skillInfo.owner}`);
  console.log(`   下载: ${skillInfo.downloads?.toLocaleString()}\n`);

  console.log('📄 正在获取技能详情...');
  const skillDetail = await fetchSkillDetail(browser, skillInfo.slug);
  console.log('✅ 详情获取完成\n');

  const introRaw =
    (skillInfo.summary && String(skillInfo.summary).trim()) ||
    (!skillDetail.error &&
      (skillDetail.description || (skillDetail.content && String(skillDetail.content).trim()))) ||
    '';
  const introText =
    introRaw.length > 3500 ? `${introRaw.slice(0, 3500)}…` : introRaw || '';

  const skillsRoot = path.join(SKILL_DIR, '..');
  const targetSkillDir = path.join(skillsRoot, skillInfo.slug);
  let localFilesNote = '';
  if (fs.existsSync(targetSkillDir)) {
    console.log(`📂 找到本地技能: ${targetSkillDir}`);
    localFilesNote = `\n### 本地技能目录\n\n\`${targetSkillDir}\`\n\n文件：\n\n\`\`\`\n${fs.readdirSync(targetSkillDir).join('\n')}\n\`\`\`\n`;
  }

  const knowledge = SKILL_KNOWLEDGE[skillInfo.slug] || SKILL_KNOWLEDGE.default;

  const today = new Date().toISOString().split('T')[0];

  let body;
  if (knowledge.structured) {
    body = buildStructuredReport(skillInfo, knowledge, introText);
  } else {
    body = `### 排名\n${rank}\n\n### 技能名称\n${skillInfo.name}\n\n### 技能标识\n\`${skillInfo.slug}\`\n\n### 分类\n${skillInfo.category}\n\n### 下载量 / 点赞数\n下载量：${skillInfo.downloads?.toLocaleString() || 'N/A'} | 点赞数：${skillInfo.stars?.toLocaleString() || 'N/A'}\n\n${buildDefaultReport(skillInfo, knowledge, introText)}`;
  }

  const report = `---
date: ${today}
rank: ${rank}
skill: ${skillInfo.slug}
---

${body}${localFilesNote}
---
*分析时间：${new Date().toLocaleString('zh-CN')} · 数据来源：Clawhub 榜单 + 技能详情页*
`;

  const reportPath = path.join(REPORTS_DIR, `${today}-${skillInfo.slug}.md`);
  const latestPath = path.join(REPORTS_DIR, 'LATEST.md');
  fs.writeFileSync(reportPath, report);
  // 固定文件名，方便在 IDE / 资源管理器中始终打开「最近一次」完整报告（不依赖终端是否显示全文）
  fs.writeFileSync(latestPath, report);

  analyzedData.analyzed.push(skillInfo.slug);
  analyzedData.lastRun = today;
  fs.writeFileSync(ANALYZED_FILE, JSON.stringify(analyzedData, null, 2));

  const fileUrl =
    process.platform === 'win32'
      ? 'file:///' + reportPath.replace(/\\/g, '/')
      : 'file://' + reportPath;

  // 短输出：多数环境会完整显示；完整正文以文件为准（见 LATEST.md）
  console.log('');
  console.log('========== skill-everyday 本次结果 ==========');
  console.log(`排名: ${rank}  |  技能: ${skillInfo.name}  (${skillInfo.slug})`);
  console.log(`主报告文件: ${reportPath}`);
  console.log(`最近一次（固定入口，内容同本次）: ${latestPath}`);
  console.log(`可尝试在浏览器打开: ${fileUrl}`);
  console.log('==========================================');
  console.log('提示: 若在 Cursor/终端里看不到下方长文，请直接打开上述 .md 文件查看完整报告。');
  console.log('');

  // UTF-8 直写 stdout；部分 IDE 仍可能截断，以 LATEST.md 为准
  try {
    const banner = '\n========== 报告全文（与 LATEST.md 一致）==========\n';
    fs.writeSync(1, Buffer.from(banner, 'utf8'));
    fs.writeSync(1, Buffer.from(report, 'utf8'));
    fs.writeSync(1, Buffer.from('\n', 'utf8'));
  } catch (e) {
    console.error('stdout 输出失败，请打开报告文件:', e.message);
    console.log(report);
  }

  await browser.close();
}

run().catch(console.error);
