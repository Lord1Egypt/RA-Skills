#!/usr/bin/env node
/**
 * SkillPick API CLI v6.5.0 — 挑选Skill · 13维质量融合版
 *
 * 用法：
 *   node api.js top3 [赛道名]           赛道TOP3推荐
 *   node api.js search <关键词>         搜索推荐
 *   node api.js similar <skill名>       相似替代推荐
 *   node api.js workflow [场景名]        工作流推荐
 *   node api.js detail <skill名>        Skill详情（含13维质量雷达）
 *   node api.js quality                 质量报告总览
 *   node api.js search <关键词> --show-all    强制显示全量（含D/F级）
 *
 * 核心特性：
 *   - QUALITY_BOOST_TABLE 全局配置表（驾驶舱）
 *   - qualityGate() 三层门控函数（pass/warn/block）
 *   - 搜索推荐：乘法模型(×multiplier) + D/F一票否决
 *   - 相似替代：质量第三维度排序 + 替代标签融入等级差
 *   - 工作流推荐：门控拦截 + hits×boost 加权 + 自动fallback
 *   - TOP3：同分按质量重排序 + 等级徽章 + C/D级警告标注
 *   - 13维Z-score标准化质量评分 + GitHub/SkillHub/市场验证三增强
 */

const fs = require('fs');
const path = require('path');

// 加载主数据
const dataPath = path.join(__dirname, 'skills_data.js');

let skillsData;
try {
  const raw = fs.readFileSync(dataPath, 'utf8');
  // 方式1: 标准 JS 对象导出格式
  let match = raw.match(/const\s+SKILLS_DATA\s*=\s*(\{[\s\S]*\})\s*;?\s*$/);
  if (match) {
    skillsData = JSON.parse(match[1]);
  } else {
    // 方式2: 尝试更宽松的匹配（兼容换行+注释+空格等）
    match = raw.match(/const\s+SKILLS_DATA\s*=\s*(\{[\s\S]*\})\s*;?\s*(?:\/\/.*)?$/);
    if (!match) throw new Error('invalid skills_data.js: SKILLS_DATA object not found');
    skillsData = JSON.parse(match[1]);
  }
} catch (e) {
  console.error('加载 skills_data.js 失败:', e.message);
  process.exit(1);
}

// 兼容处理：skills_data.js 可能没有 all_skills（只有 categories）
let allSkills = skillsData.all_skills || [];
if (allSkills.length === 0 && skillsData.categories) {
  // 从 categories 展开构建 allSkills
  allSkills = [];
  Object.values(skillsData.categories).forEach(cat => {
    if (cat.top3) {
      allSkills.push(...cat.top3);
    }
    if (cat.list) {
      allSkills.push(...cat.list);
    }
  });
  // 去重
  const seen = new Set();
  allSkills = allSkills.filter(s => {
    if (seen.has(s.name)) return false;
    seen.add(s.name);
    return true;
  });
  console.log(`⚠️ all_skills 为空，已从 categories 展开 ${allSkills.length} 条`);
}

const categories = skillsData.categories || {};
const workflows = skillsData.workflows || {};

// ★ 13维质量数据加载（优先内嵌数据，兼容外部文件）
let qualityV2 = [];
let qualityMap = {}; // 快速查找表
try {
  // 1. 优先从 SKILLS_DATA.quality_map 读取（内嵌版，发布包用）
  if (skillsData.quality_map && Object.keys(skillsData.quality_map).length > 0) {
    qualityMap = skillsData.quality_map;
    console.log('✅ 已加载 ' + Object.keys(qualityMap).length + ' 条质量映射（内嵌）');
  } else {
    // 2. 回退到外部文件（本地开发用）
    const slimPath = path.join(__dirname, 'data', 'quality_map_slim.json');
    const fullMapPath = path.join(__dirname, 'data', 'quality_map.json');
    const fullPath = path.join(__dirname, 'data', 'quality_v2_scores.json');

    if (fs.existsSync(slimPath)) {
      qualityMap = JSON.parse(fs.readFileSync(slimPath, 'utf8'));
      console.log('✅ 已加载 ' + Object.keys(qualityMap).length + ' 条质量映射');
    } else if (fs.existsSync(fullMapPath)) {
      qualityMap = JSON.parse(fs.readFileSync(fullMapPath, 'utf8'));
      console.log('✅ 已加载 ' + Object.keys(qualityMap).length + ' 条质量映射（全量）');
    } else if (fs.existsSync(fullPath)) {
      qualityV2 = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
      qualityV2.forEach(q => {
        qualityMap[q.name] = {
          q: q.quality_score || 0, g: q.quality_grade || '?',
          dims: q.dimensions || {}, label: q.quality_label || '',
        };
      });
      console.log('✅ 已加载 ' + qualityV2.length + ' 条质量评分');
    }
  }
} catch (e) {
  console.log('⚠️ 质量数据加载失败:', e.message);
}

// ====== 工具函数 ======
function isCN(s) { return s.region === 'CN' || s.is_cn === true; }
function confLabel(c) { return { high: '🔴高', medium: '🟡中', low: '🟢低' }[c] || '🟢低'; }

// ★ 获取13维质量分（Z-score标准化区间[20,98]）
function getQuality(name) {
  const q = qualityMap[name];
  if (!q) return 50;
  return q.q || 50;
}

// ★ 获取质量等级（A/B+/B/C/D）
function getQualityGrade(name) {
  const q = qualityMap[name];
  if (!q) return '?';
  return q.g || '?';
}

// ★ 获取质量维度数据
function getQualityDims(name) {
  const q = qualityMap[name];
  if (!q || !q.dims) return null;
  return q.dims;
}

// ★ 质量等级标签
function gradeLabel(g) {
  return { A: '🏆A级', 'B+': '⭐B+', B: '📗B级', C: '📙C级', D: '📕D级', F: '❌F级' }[g] || g;
}

// ★ 质量等级比较工具
const GRADE_ORDER = ['F', 'D', 'C', 'B', 'B+', 'A', 'A+'];
function isHigherGrade(g1, g2) { // g1是否比g2高
  return (GRADE_ORDER.indexOf(g1) || 0) > (GRADE_ORDER.indexOf(g2) || 0);
}
function isLowerGrade(g1, g2) { // g1是否比g2低
  return (GRADE_ORDER.indexOf(g1) || 0) < (GRADE_ORDER.indexOf(g2) || 0);
}

// ====== ★ 三层漏斗质量融合核心 ======

/**
 * QUALITY_BOOST_TABLE — 全局质量策略配置表（驾驶舱）
 * 调此表即改所有算法的质量行为，无需动内部逻辑
 *
 * multiplier: 质量乘法系数（Layer 3 排序用）
 * gate: 门控类型 — pass(正常通过) / warn(警告+降权) / block(拦截隐藏)
 */
const QUALITY_BOOST_TABLE = {
  'A+': { multiplier: 1.20, display: '🟢 卓越', gate: 'pass' },
  'A':  { multiplier: 1.15, display: '🟢 优秀', gate: 'pass' },
  'B+': { multiplier: 1.08, display: '🔵 良好+', gate: 'pass' },
  'B':  { multiplier: 1.00, display: '🔵 良好',  gate: 'pass' },
  'C':  { multiplier: 0.50, display: '🟡 及格',  gate: 'warn', penalty: '降权50%' },
  'D':  { multiplier: 0.0,  display: '🔴 较差',  gate: 'block', reason: '质量不达标' },
  'F':  { multiplier: 0.0,  display: '⛔ 不推荐', gate: 'block', reason: '存在严重缺陷' },
  null: { multiplier: 0.90, display: '❓ 未扫描', gate: 'warn', penalty: '无质量数据' }, // 保守处理
};

/**
 * qualityGate() — Layer 1: 质量门控
 * 根据13维质量等级返回门控结果，供四大算法统一调用
 *
 * @param {string} skillName - skill名称
 * @returns {{ allowed: boolean, boost: number, label: string, grade: string, reason?: string }}
 */
function qualityGate(skillName) {
  const grade = getQualityGrade(skillName);
  const config = QUALITY_BOOST_TABLE[grade] || QUALITY_BOOST_TABLE[null];
  return {
    allowed: config.gate !== 'block',
    boost: config.multiplier,
    label: config.display,
    grade: grade || '?',
    reason: config.reason || null,
    isWarn: config.gate === 'warn',
    isBlock: config.gate === 'block',
    penalty: config.penalty || null,
  };
}

/**
 * getBoostConfig() — 快速取质量配置
 */
function getBoostConfig(skillName) {
  const grade = getQualityGrade(skillName);
  return QUALITY_BOOST_TABLE[grade] || QUALITY_BOOST_TABLE[null];
}

// 搜索意图映射表（v7.0 扩展版：18→35 个意图）
const INTENT_MAP = {
  // === 文档处理（原版保留）===
  'pdf':    { expand: ['pdf', 'document', 'doc', 'paper', 'file', 'reader', 'writer'], avoid_cats: [] },
  'excel':  { expand: ['excel', 'xlsx', 'spreadsheet', 'table', 'data', 'csv'], avoid_cats: [] },
  'ppt':    { expand: ['ppt', 'powerpoint', 'slide', 'presentation', 'deck'], avoid_cats: [] },
  'word':   { expand: ['word', 'docx', 'document', 'report', 'write'], avoid_cats: [] },

  // === 媒体创作（原版保留+扩展）===
  '图片':   { expand: ['image', 'img', 'picture', 'photo', 'visual', 'screenshot', 'draw', 'paint', 'design', 'graphic', 'dall-e', 'midjourney'], avoid_cats: [] },
  '视频':   { expand: ['video', 'movie', 'clip', 'record', 'stream', 'ffmpeg', 'edit', 'render'], avoid_cats: [] },

  // === 电商/零售（新增）===
  '电商':   { expand: ['ecommerce', 'shopping', 'retail', 'shopify', '商品', 'product', 'goods', '商城', '购物', '店铺', '订单', 'order', 'cart', 'checkout', 'sku'], avoid_cats: ['开发测试', 'DevOps'] },
  '商品':   { expand: ['product', 'goods', 'commodity', 'item', 'sku', '商品', '货品', '选品'], avoid_cats: ['开发测试', 'DevOps'] },

  // === 客服/服务（新增）===
  '客服':   { expand: ['customer', 'service', 'support', 'ticket', 'helpdesk', '客服', '工单', '售后', '咨询', 'zendesk'], avoid_cats: ['开发测试', 'DevOps', '安全质量', '后端开发'] },

  // === 广告/营销/设计（新增）===
  '广告':   { expand: ['ad', 'advert', 'ads', 'marketing', 'campaign', '投放', '广告', '推广', 'creative', 'banner'], avoid_cats: [] },
  '设计':   { expand: ['design', 'ui', 'ux', 'graphic', 'visual', 'canva', 'figma', 'ps', 'photoshop', '设计', '海报', '创意'], avoid_cats: ['开发测试'] },
  '营销':   { expand: ['marketing', 'promotion', 'branding', 'content', 'campaign', 'social', '营销', '推广', '品牌', '运营'], avoid_cats: [] },

  // === 本地生活（新增）===
  '本地生活': { expand: ['local', 'life', 'o2o', 'lifestyle', 'poi', 'nearby', '本地', '生活', '到店', '团购', '优惠券'], avoid_cats: [] },
  '短视频':  { expand: ['short', 'video', 'douyin', 'tiktok', 'reels', '短视频', '抖音', '直播', 'livestream', '带货'], avoid_cats: [] },

  // === 开发/运维（原版保留+扩展）===
  '代码':   { expand: ['code', 'coding', 'dev', 'programming', 'developer', 'script', 'git', 'repo'], avoid_cats: [] },
  '数据':   { expand: ['data', 'analytics', 'chart', 'database', 'sql', 'bi', '仪表盘', 'dashboard'], avoid_cats: [] },
  '邮件':   { expand: ['email', 'mail', 'smtp', 'imap', 'send', 'outlook'], avoid_cats: [] },
  '翻译':   { expand: ['translate', 'i18n', 'language', 'localize', '多语言', 'gpt', 'deepL'], avoid_cats: [] },
  '测试':   { expand: ['test', 'testing', 'qa', 'e2e', 'unit', 'spec', 'pytest', 'jest'], avoid_cats: [] },
  '部署':   { expand: ['deploy', 'ci', 'cd', 'release', 'publish', 'hosting', 'docker', 'k8s'], avoid_cats: [] },
  '监控':   { expand: ['monitor', 'alert', 'log', 'observe', 'metrics', '告警', '日志'], avoid_cats: [] },
  '搜索':   { expand: ['search', 'find', 'query', 'index', 'retrieval', 'rag'], avoid_cats: [] },
  '写作':   { expand: ['write', 'writing', 'content', 'copy', 'article', 'blog', '文案', '稿件'], avoid_cats: [] },
  '分析':   { expand: ['analyze', 'analysis', 'insight', 'report', 'statistics', '统计', '复盘'], avoid_cats: [] },
  '自动化':  { expand: ['automation', 'automate', 'workflow', 'pipeline', 'cron', 'schedule', 'zapier', 'ifttt'], avoid_cats: [] },

  // === 效率工具（新增）===
  '浏览器':  { expand: ['browser', 'web', 'scrape', 'crawl', 'selenium', 'playwright', 'puppeteer', '浏览器', '爬虫', '自动化测试'], avoid_cats: [] },
  '金融':   { expand: ['finance', 'stock', 'trading', 'crypto', 'financial', '股票', '基金', '行情', '投资', '金融'], avoid_cats: [] },
  '知识管理': { expand: ['knowledge', 'wiki', 'note', 'notion', 'obsidian', '知识', '笔记', '文档管理'], avoid_cats: [] },
};

// ====== 搜索日志（仅本地开发模式记录，发布版静默跳过）======

/**
 * 记录搜索/推荐日志（追加写入 JSONL，写失败静默忽略）
 */
function logSearch(cmd, query, results) {
  try {
    const logPath = path.join(__dirname, 'data', 'search_log.jsonl');
    // 仅当 data 目录存在时写入（发布版无 data 目录则跳过）
    if (fs.existsSync(path.join(__dirname, 'data'))) {
      const entry = JSON.stringify({ cmd, q: query, r: results.slice(0, 3), ts: new Date().toISOString() });
      fs.appendFileSync(logPath, entry + '\n');
    }
  } catch (e) { /* 静默 */ }
}

function pickIntent(query) {
  const q = (query || '').toLowerCase();

  let direct = null;
  for (const [kw, intent] of Object.entries(INTENT_MAP)) {
    const kl = kw.toLowerCase();
    if (q.includes(kl)) {
      if (!direct || kl.length > direct.kw.length) direct = { kw: kl, intent };
    }
  }
  if (direct) return direct;

  let fallback = null;
  for (const [kw, intent] of Object.entries(INTENT_MAP)) {
    const kl = kw.toLowerCase();
    if (kl.includes(q)) {
      if (!fallback || kl.length < fallback.kw.length) fallback = { kw: kl, intent };
    }
  }
  return fallback;
}

function searchScore(skill, query, expandedWords, avoidCats) {
  let sc = 0;
  let textScore = 0;
  const q = query.toLowerCase();
  const name = skill.name.toLowerCase();
  const desc = (skill.desc || '').toLowerCase();
  const tagsEnh = (skill.tags_enhanced || skill.tags || []).join(' ').toLowerCase();
  const cat = (skill.cat || '').toLowerCase();
  const all = name + ' ' + desc + ' ' + tagsEnh + ' ' + cat;

  // 精确名称匹配（最高权重）
  if (name === q) { sc += 220; textScore += 220; }
  else if (name.includes(q)) { sc += 180; textScore += 180; }
  else if (q.includes(name)) { sc += 100; textScore += 100; }

  // 标签/描述/赛道匹配
  if (tagsEnh.includes(q)) { sc += 120; textScore += 120; }
  if (desc.includes(q)) { sc += 70; textScore += 70; }
  if (cat.includes(q)) { sc += 30; textScore += 30; }

  // 扩展词匹配
  if (expandedWords && expandedWords.length > 0) {
    let expandHits = 0;
    for (const w of expandedWords) {
      const wl = w.toLowerCase();
      if (name.includes(wl)) { sc += 35; textScore += 35; expandHits++; }
      if (desc.includes(wl)) { sc += 18; textScore += 18; expandHits++; }
      if (tagsEnh.includes(wl)) { sc += 38; textScore += 38; expandHits++; }
      if (cat.includes(wl)) { sc += 8; textScore += 8; expandHits++; }
    }
    sc += Math.min(expandHits * 5, 25);
  }

  // 分词匹配
  const tokenized = q.split(/[\s,，.。;；!！?？/\\|_-]+/).filter(t => t.length >= 2);
  if (tokenized.length > 1) {
    let tokenHits = 0;
    for (const t of tokenized) {
      if (name.includes(t) || desc.includes(t) || tagsEnh.includes(t) || cat.includes(t)) tokenHits++;
    }
    sc += tokenHits * 28;
    textScore += tokenHits * 28;
  }

  // bigram 匹配
  const qBigrams = [];
  const clean = q.replace(/[\s\d\p{P}]/gu, '');
  for (let i = 0; i < clean.length - 1; i++) qBigrams.push(clean[i] + clean[i + 1]);
  if (qBigrams.length > 0) {
    let hits = 0;
    for (const bg of qBigrams) if (all.includes(bg)) hits++;
    sc += Math.min(hits * 5, 20);
    textScore += Math.min(hits * 5, 20);
  }

  // 赛道排除
  if (avoidCats && avoidCats.length > 0) {
    for (const ac of avoidCats) {
      const acl = ac.toLowerCase();
      if (cat.includes(acl) || acl.includes(cat)) { sc -= 150; break; }
    }
  }

  // PDF 意图特殊加权
  const hasPdfIntent = q.includes('pdf') || (expandedWords || []).some(w => w.toLowerCase() === 'pdf');
  if (hasPdfIntent) {
    if (name.includes('pdf')) { sc += 120; textScore += 120; }
    if (tagsEnh.includes('pdf')) { sc += 45; textScore += 45; }
    if (cat.includes('文档')) { sc += 25; textScore += 25; }
  }

  if (textScore <= 0) return 0;

  // ★ Layer 1 门控 + Layer 3 质量乘法
  const gate = qualityGate(skill.name);

  // D/F 级一票否决（--show-all 可绕过）
  if (gate.isBlock && !global._SHOW_ALL) return -999;

  // 质量乘法模型：textScore × boost（比加法更公平，相对比例一致）
  sc = Math.round(textScore * gate.boost);

  // C 级额外标记（不在此处降权，由boost=0.70统一处理）
  
  // 质量已通过 qualityMultiplier 体现，不再混入 final_score（双轨分离）

  return sc;
}
// 相似度计算（同前端逻辑）
function calcSimilar(a, b) {
  let sim = 0;
  if (a.cat === b.cat) sim += 40;
  else {
    const ac = a.cat.toLowerCase(), bc = b.cat.toLowerCase();
    if (ac.includes(bc) || bc.includes(ac)) sim += 25;
  }
  const aTags = new Set((a.tags_enhanced || a.tags || []).map(t => t.toLowerCase()));
  const bTags = new Set((b.tags_enhanced || b.tags || []).map(t => t.toLowerCase()));
  let overlap = 0;
  for (const t of aTags) if (bTags.has(t)) overlap++;
  sim += (overlap / Math.max(aTags.size, bTags.size, 1)) * 30;
  const aWords = new Set((a.desc || '').toLowerCase().split(/[\s,，.。;；!！?？/\\|]+/).filter(w => w.length > 2));
  const bWords = new Set((b.desc || '').toLowerCase().split(/[\s,，.。;；!！?？/\\|]+/).filter(w => w.length > 2));
  let descOverlap = 0;
  for (const w of aWords) if (bWords.has(w)) descOverlap++;
  sim += Math.min(descOverlap * 3, 15);
  const aName = a.name.toLowerCase(), bName = b.name.toLowerCase();
  if (aName === bName) sim += 30;
  else if (aName.includes(bName) || bName.includes(aName)) sim += 15;
  else {
    const aParts = new Set(aName.split(/[-_\s]/));
    const bParts = new Set(bName.split(/[-_\s]/));
    let partHit = 0;
    for (const p of aParts) if (p.length >= 2 && bParts.has(p)) partHit++;
    sim += Math.min(partHit * 5, 15);
  }
  if (isCN(a) === isCN(b)) sim += 5;
  return Math.round(sim);
}

// ====== 命令实现 ======

function cmdTop3(catName) {
  const entries = Object.entries(categories);
  // ★ 排序加入质量门控
  const sorted = entries.sort((a, b) => {
    const aChartSum = a[1].top3.reduce((sum, s) => sum + (s.chart_count || 0), 0);
    const bChartSum = b[1].top3.reduce((sum, s) => sum + (s.chart_count || 0), 0);
    if (bChartSum !== aChartSum) return bChartSum - aChartSum;
    const aChartCount = a[1].top3.filter(s => (s.chart_count || 0) > 0).length;
    const bChartCount = b[1].top3.filter(s => (s.chart_count || 0) > 0).length;
    if (bChartCount !== aChartCount) return bChartCount - aChartCount;
    return b[1].count - a[1].count;
  });

  if (catName) {
    const cat = catName.toLowerCase();
    const match = sorted.find(([name]) => name.toLowerCase().includes(cat));
    if (!match) {
      console.log('❌ 未找到赛道: ' + catName);
      console.log('可用赛道: ' + sorted.map(([n]) => n).slice(0, 20).join('、') + '...');
      return;
    }
    const [name, info] = match;
    
    // ★ 同 final_score 时按质量分重排序
    const top3Sorted = [...info.top3].sort((a, b) => {
      if ((b.final_score || 0) !== (a.final_score || 0)) 
        return (b.final_score || 0) - (a.final_score || 0);
      // 分数相同时，质量高的排前
      return getQuality(b.name) - getQuality(a.name);
    });
    
    const chartSum = top3Sorted.reduce((sum, s) => sum + (s.chart_count || 0), 0);
    const tier = chartSum >= 3 ? '🏅🔥强推' : (top3Sorted.filter(s => (s.chart_count || 0) > 0).length >= 2 || chartSum >= 2) ? '🏅热门' : (top3Sorted.filter(s => (s.chart_count || 0) > 0).length >= 1) ? '🏅上榜' : '';
    console.log(`\n🏆 ${name}（${info.count}个skill）${tier}`);
    console.log('─'.repeat(50));
    top3Sorted.forEach((s, i) => {
      const hasChart = (s.chart_count || 0) > 0;
      const mark = i === 0 ? '🥇' : i === 1 ? '🥈' : '🥉';
      const gate = qualityGate(s.name);
      const qg = getQuality(s.name);
      
      console.log(`${mark} ${s.name} (${s.final_score}分) ${confLabel(s.confidence)}${hasChart ? ' 🏅' + s.chart_count + '榜' : ''}${isCN(s) ? ' 🇨🇳' : ''} ${gradeLabel(gate.grade)}${gate.isWarn ? ' ⚠️' + gate.penalty : ''}${gate.isBlock ? ' 🔴' + gate.reason : ''}`);
      if (s.recommend_reason) console.log(`   💡 ${s.recommend_reason}`);
    });
    return;
  }

  // 全量输出 — 每个赛道的TOP3也做同分质量重排
  console.log('\n🏆 SkillPick 赛道 TOP3 推荐（质量融合版）\n');
  sorted.slice(0, 20).forEach(([name, info]) => {
    const chartSum = info.top3.reduce((sum, s) => sum + (s.chart_count || 0), 0);
    const tier = chartSum >= 3 ? '🔥强推' : (info.top3.filter(s => (s.chart_count || 0) > 0).length >= 2 || chartSum >= 2) ? '热门' : (info.top3.filter(s => (s.chart_count || 0) > 0).length >= 1) ? '上榜' : '';
    const best = info.top3[0];
    console.log(`📋 ${name}（${info.count}个）${tier ? '· ' + tier : ''}`);
    
    // ★ 同分质量重排
    const top3Sorted = [...info.top3].sort((a, b) => {
      if ((b.final_score || 0) !== (a.final_score || 0)) 
        return (b.final_score || 0) - (a.final_score || 0);
      return getQuality(b.name) - getQuality(a.name);
    });
    
    top3Sorted.forEach((s, i) => {
      const mark = i === 0 ? '  🥇' : i === 1 ? '  🥈' : '  🥉';
      const gate = qualityGate(s.name);
      console.log(`${mark} ${s.name} (${s.final_score})${(s.chart_count || 0) > 0 ? ' 🏅' + s.chart_count : ''}${isCN(s) ? ' 🇨🇳' : ''} ${gate.isWarn ? '⚠️' + gradeLabel(gate.grade) : ''}${gate.isBlock ? '🚫' + gate.grade : ''}`);
    });
  });
  if (sorted.length > 20) console.log(`\n... 共 ${sorted.length} 个赛道，使用 "node api.js top3 <赛道名>" 查看指定赛道`);
}

function cmdSearch(query) {
  if (!query) { console.log('❌ 请输入搜索关键词'); return; }

  // ★ 解析 --show-all 参数
  const showAllIdx = query.indexOf('--show-all');
  global._SHOW_ALL = showAllIdx !== -1;
  if (global._SHOW_ALL) {
    query = query.replace('--show-all', '').trim();
  }
  if (!query) { console.log('❌ 请输入搜索关键词'); return; }

  let expandedWords = [], avoidCats = [];
  const picked = pickIntent(query);
  if (picked) {
    expandedWords = picked.intent.expand;
    avoidCats = picked.intent.avoid_cats;
  }

  const results = allSkills
    .map(s => ({ ...s, _search_score: searchScore(s, query, expandedWords, avoidCats), _gate: qualityGate(s.name) }))
    .filter(s => s._search_score > 0)
    .sort((a, b) => {
      // ★ 主排序=搜索分(已含质量乘法)，副排序=原始质量分
      if (b._search_score !== a._search_score) return b._search_score - a._search_score;
      return getQuality(b.name) - getQuality(a.name);
    })
    .slice(0, 3);

  // 📝 记录搜索日志
  logSearch('search', query, results.map(r => r.name));

  if (results.length === 0) {
    console.log('❌ 未找到匹配的 Skill，试试其他关键词');
    return;
  }

  console.log(`\n🔍 搜索：${query}${expandedWords.length > 0 ? '（扩展：' + expandedWords.slice(0, 5).join('、') + '）' : ''}\n`);

  const bestSearchScore = results[0]._search_score;
  const second = results[1] || null;
  const leadRatio = second ? (bestSearchScore / Math.max(second._search_score, 1)) : Infinity;

  results.forEach((s, i) => {
    let tag;
    if (i === 0) {
      // ★ 结合搜索领先度 + 质量门控等级决定推荐标签
      const gate = s._gate;
      const isStrongLead = leadRatio >= 1.2 && getQuality(s.name) >= 50;
      const isWeakLead = leadRatio >= 1.1 || getQuality(s.name) >= 55;
      
      if (gate.isBlock) tag = '🚫 已拦截';
      else if (gate.isWarn) tag = isStrongLead ? '✅ 推荐(⚠️)' : (isWeakLead ? '✅ 推荐(⚠️)' : '⚠️ 备选(⚠️)');
      else if (isStrongLead) tag = '✅ 推荐';
      else if (i === 0 && isWeakLead) tag = '✅ 推荐';
      else tag = '⚠️ 备选';
    } else {
      const gate = s._gate;
      if (gate.isBlock) tag = '🚫 已拦截';
      else if (gate.isWarn) tag = s._search_score >= bestSearchScore * 0.75 ? '⚠️ 备选(⚠️)' : '⏭️ 不推荐';
      else tag = s._search_score >= bestSearchScore * 0.75 ? '⚠️ 备选' : '⏭️ 不推荐';
    }

    const hasChart = (s.chart_count || 0) > 0;
    const install = s.install_hint ? s.install_hint.hint : '无安装信息';
    const qg = getQuality(s.name);
    const qGrade = getQualityGrade(s.name);
    const qm = qualityMap[s.name];
    const safetyFatal = qm && qm.dims && qm.dims.safety <= 20;
    const gateInfo = s._gate; // ★

    console.log(`${tag} ${s.name} (${s.final_score}分·${gradeLabel(qGrade)} 质量${qg}) ${confLabel(s.confidence)}${hasChart ? ' 🏅' + s.chart_count + '榜' : ''}${isCN(s) ? ' 🇨🇳' : ''}${safetyFatal ? ' ☠️' : ''}${gateInfo.isWarn ? ' ⚠️' + gateInfo.penalty : ''}${gateInfo.isBlock ? ' 🔴' + gateInfo.reason : ''}`);
    
    // ★ 质量驱动推荐理由
    let reasons = [];
    if (s.recommend_reason) reasons.push(s.recommend_reason);
    
    if (!gateInfo.isBlock) {
      if (qg >= 65) reasons.push('13维A级·GitHub+SkillHub+市场验证');
      else if (qg >= 55) reasons.push('13维B+级·结构完整');
      else if (qg >= 45) reasons.push('13维B级·可用');
      else if (qg < 38) reasons.push('⚠️ 质量偏低(13维C/D)，谨慎使用');
      
      // 显示维度短板
      const dims = getQualityDims(s.name);
      if (dims && dims.safety < 40) reasons.push(`🔴 安全维度低(${dims.safety})`);
      if (dims && dims.market >= 80) reasons.push(`💰 市场热度高(${dims.market})`);
      if (safetyFatal) reasons.push('存在安全隐患');
      
      if (gateInfo.isWarn) reasons.push(`⚠️ ${gateInfo.label}（${gateInfo.penalty}）`);
    } else {
      reasons.push(`🔴 ${gateInfo.reason} — 使用 --show-all 查看`);
    }
    
    console.log(`   赛道: ${s.cat}${reasons.length > 0 ? ' · ' + reasons.join(' | ') : ''}`);
    console.log(`   📦 ${install}`);
    console.log();
  });

  // ★ 结论区
  if (second) {
    const topQ = getQuality(results[0].name);
    const secQ = getQuality(second.name);
    const qDiff = topQ - secQ;
    const topGrade = getQualityGrade(results[0].name);
    
    if (leadRatio >= 1.3 && topQ >= 50) {
      console.log(`🏆 结论：装 ${results[0].name}，不用纠结（${gradeLabel(topGrade)} 质量${topQ} vs ${secQ}，差距明显）`);
    } else if (leadRatio >= 1.15 && topQ >= secQ + 8) {
      console.log(`🏆 结论：优先装 ${results[0].name}（质量更高+搜索匹配更好）`);
    } else if (topGrade === 'A' || (topQ >= 65 && qDiff >= 10)) {
      console.log(`🏆 结论：装 ${results[0].name}（A级${topQ}，13维验证通过）`);
    } else if (topQ <= 36) {
      console.log(`⏸️ 结论：该领域暂无高质量 skill，建议降低预期或手动评估`);
    } else {
      console.log(`🏆 结论：可先试用 ${results[0].name}（与 ${second.name} 接近，但质量略优）`);
    }
  } else {
    console.log(`🏆 结论：唯一匹配，直接装 ${results[0].name}`);
  }
}

function pickSimilarTarget(ql) {
  const normalizedQuery = ql.replace(/[\s_-]+/g, '');
  const queryTokens = ql.split(/[-_\s]+/).filter(t => t.length >= 2);

  const scored = allSkills
    .map(s => {
      const name = s.name.toLowerCase();
      const nameCompact = name.replace(/[\s_-]+/g, '');
      const tagsArr = (s.tags_enhanced || s.tags || []).map(t => t.toLowerCase());
      const tagsText = tagsArr.join(' ');
      const desc = (s.desc || '').toLowerCase();
      const cat = (s.cat || '').toLowerCase();

      let score = 0;
      if (name === ql) score += 420;
      else if (normalizedQuery && nameCompact === normalizedQuery) score += 360;
      else if (name.startsWith(ql)) score += 300;
      else if (name.includes(ql)) score += 260;

      if (normalizedQuery && nameCompact.includes(normalizedQuery)) score += 90;
      if (tagsArr.some(t => t === ql || t.includes(ql))) score += 170;
      if (desc.includes(ql)) score += 120;
      if (cat.includes(ql)) score += 80;

      if (queryTokens.length > 0) {
        let tokenHits = 0;
        for (const t of queryTokens) {
          if (name.includes(t) || tagsText.includes(t) || desc.includes(t) || cat.includes(t)) tokenHits++;
        }
        score += tokenHits * 35;
      }

      return { skill: s, score };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return b.skill.final_score - a.skill.final_score;
    });

  return scored.length > 0 ? scored[0].skill : null;
}

function cmdSimilar(query) {
  if (!query) { console.log('❌ 请输入 Skill 名称'); return; }
  const ql = query.toLowerCase();

  const target = pickSimilarTarget(ql);
  if (!target) {
    console.log('❌ 未找到该 Skill，试试更精确的名称');
    return;
  }

  const results = allSkills
    .filter(s => s.name !== target.name)
    .map(s => ({ ...s, _sim: calcSimilar(target, s), _gate: qualityGate(s.name) }))
    // ★ 排序 = 相似度↓(差距>10) → 质量分↓(差距>10) → final_score↓
    .sort((a, b) => {
      if (b._sim !== a._sim && Math.abs(b._sim - a._sim) > 10) return b._sim - a._sim;
      // ★ 新增第二维度: 质量分
      const qA = getQuality(a.name), qB = getQuality(b.name);
      if (Math.abs(qB - qA) > 10) return qB - qA;
      return b.final_score - a.final_score;
    })
    .slice(0, 3);

  // 📝 记录搜索日志
  logSearch('similar', query, results.map(r => r.name));

  const hasChart = (target.chart_count || 0) > 0;
  console.log(`\n🔄 基于 ${target.name}（${target.cat}·${target.final_score}分·${confLabel(target.confidence)}${hasChart ? '·🏅' + target.chart_count + '榜' : ''}${isCN(target) ? '·🇨🇳' : ''}）查找相似替代\n`);

  results.forEach(s => {
    const scoreDiff = s.final_score - target.final_score;
    const gate = s._gate; // ★
    const qGradeTarget = getQualityGrade(target.name);
    const qGradeAlt = getQualityGrade(s.name);
    
    // ★ 替代类型标签融入质量等级差
    let tag;
    if (gate.isBlock) {
      tag = '🚫 不推荐';
    } else if (scoreDiff > 5 && s._sim >= 30 && isHigherGrade(qGradeAlt, qGradeTarget)) {
      tag = '👍 更优替代';  // 分更高 + 质量更好 + 相似度够
    } else if (scoreDiff > 5 && s._sim >= 30) {
      tag = '👍 更优替代';
    } else if (scoreDiff >= -5 && scoreDiff <= 5 && s._sim >= 40) {
      // ★ 新增: 质量更好时也标"更优"
      if (isHigherGrade(qGradeAlt, qGradeTarget)) tag = '⚖️ 可比(质更优)';
      else if (isLowerGrade(qGradeAlt, qGradeTarget)) tag = '⚖️ 可比(质较低)';
      else tag = '⚖️ 可比替代';
    } else if (isLowerGrade(qGradeAlt, qGradeTarget)) {
      tag = '📉 较弱替代';
    } else {
      tag = '📉 较弱替代';
    }

    const diffs = [];
    if (s.cat !== target.cat) diffs.push('不同赛道：' + s.cat);
    if (scoreDiff > 0) diffs.push('评分高' + scoreDiff + '分');
    else if (scoreDiff < 0) diffs.push('评分低' + Math.abs(scoreDiff) + '分');
    if (isCN(s) && !isCN(target)) diffs.push('有国内镜像');
    if (s.best_in_track) diffs.push('赛道最优');
    
    // ★ 质量差异信息
    if (qGradeAlt !== qGradeTarget) {
      const cmp = isHigherGrade(qGradeAlt, qGradeTarget) ? '↑' : '↓';
      diffs.push(`质量${cmp}${gradeLabel(qGradeAlt)} vs ${gradeLabel(qGradeTarget)}`);
    }

    const sChart = s.chart_count || 0;
    const tChart = target.chart_count || 0;
    if (sChart > tChart) diffs.push('榜单更多(' + sChart + 'vs' + tChart + ')');

    const install = s.install_hint ? s.install_hint.hint : '';
    console.log(`${tag} ${s.name} (${s.final_score}分·相似度${s._sim}%${gate.isWarn ? ' ⚠️' + gradeLabel(qGradeAlt) : ''}·${gradeLabel(qGradeAlt)}) ${confLabel(s.confidence)}${isCN(s) ? ' 🇨🇳' : ''}`);
    console.log(`   ${diffs.length > 0 ? diffs.join(' · ') : '核心能力接近，差异不明显'}`);
    if (install) console.log(`   📦 ${install}`);
    console.log();
  });
}
function cmdWorkflow(sceneName) {
  const entries = Object.entries(workflows);
  if (entries.length === 0) {
    console.log('❌ 无工作流数据');
    return;
  }

  if (sceneName) {
    const scene = workflows[sceneName];
    if (!scene) {
      const match = entries.find(([n]) => n.toLowerCase().includes(sceneName.toLowerCase()));
      if (match) {
        cmdWorkflow(match[0]);
        return;
      }
      console.log('❌ 未找到场景: ' + sceneName);
      console.log('可用场景: ' + entries.map(([n]) => n).join('、'));
      return;
    }

    console.log(`\n🧩 ${sceneName}\n${scene.description}\n`);

    const wfResults = []; // 收集工作流推荐结果用于日志
    for (const step of scene.steps) {
      const keywords = step.keywords || [];
      const candidates = allSkills
        .map(s => {
          const searchable = (s.name + ' ' + (s.tags_enhanced || s.tags || []).join(' ') + ' ' + (s.desc || '') + ' ' + s.cat).toLowerCase();
          let hits = 0;
          for (const kw of keywords) {
            const kwLower = kw.toLowerCase();
            if (s.name.toLowerCase().includes(kwLower)) hits += 3;
            else if (searchable.includes(kwLower)) hits += 1;
          }
          // ★ 加入质量门控信息
          const gate = qualityGate(s.name);
          return { skill: s, hits, boosted: Math.round(hits * gate.boost), gate };
        })
        .filter(item => item.hits > 0)
        // ★ 排序 = hits×boost ↓ → 原始hits↓ → final_score↓
        .sort((a, b) => {
          if (b.boosted !== a.boosted) return b.boosted - a.boosted;
          if (b.hits !== a.hits) return b.hits - a.hits;
          return b.skill.final_score - a.skill.final_score;
        })
        .map(item => item.skill);

      let best = candidates.length > 0 ? candidates[0] : null;
      
      // ★ D/F级自动fallback
      let fallbackReason = '';
      if (best) {
        const bestGate = qualityGate(best.name);
        if (bestGate.isBlock && candidates.length > 1) {
          const altBest = candidates[1];
          fallbackReason = `（首选${best.name}被质量拦截:${bestGate.reason}，自动降级）`;
          best = altBest;
        }
      }

      const hasChart = best && (best.chart_count || 0) > 0;
      const bestGrade = best ? getQualityGrade(best.name) : '?';
      const bestGateInfo = best ? qualityGate(best.name) : null;

      console.log(`${step.role}${best ? ' → ' + best.name + ' (' + best.final_score + '分' + ')' + confLabel(best.confidence) + (hasChart ? ' 🏅' + best.chart_count + '榜' : '') + (isCN(best) ? ' 🇨🇳' : '') + (bestGateInfo && !bestGateInfo.isBlock ? ' ·' + gradeLabel(bestGrade) : '') + (bestGateInfo?.isWarn ? ' ⚠️' + bestGateInfo.penalty : '') : ' → ❌ 未找到匹配skill'}${fallbackReason}`);
      if (best && best.recommend_reason) console.log(`   💡 ${best.recommend_reason}`);
      if (best && best.install_hint) console.log(`   📦 ${best.install_hint.hint}`);
      if (best) wfResults.push(best.name);
    }
    // 📝 记录工作流搜索日志
    logSearch('workflow', sceneName, wfResults);
    return;
  }

  console.log('\n🧩 可用工作流场景\n');
  entries.forEach(([name, wf]) => {
    console.log(`📦 ${name} — ${wf.description}`);
    console.log(`   角色：${wf.steps.map(s => s.role).join(' → ')}`);
    console.log();
  });
  console.log('使用 "node api.js workflow <场景名>" 查看详细推荐');
}

function cmdDetail(query) {
  if (!query) { console.log('❌ 请输入 Skill 名称'); return; }
  const ql = query.toLowerCase();
  const skill = allSkills.find(s => s.name.toLowerCase() === ql) || allSkills.find(s => s.name.toLowerCase().includes(ql));
  if (!skill) { console.log('❌ 未找到 Skill: ' + query); return; }

  const hasChart = (skill.chart_count || 0) > 0;
  const install = skill.install_hint ? skill.install_hint.hint : '无安装信息';
  
  // ★ 13维质量数据
  const qg = getQuality(skill.name);
  const qGrade = getQualityGrade(skill.name);
  const dims = getQualityDims(skill.name);
  const qm = qualityMap[skill.name];
  
  console.log(`\n📋 ${skill.name}`);
  console.log(`   ┌─────────────────────────────────────┐`);
  console.log(`   │ 评分：${skill.final_score}（原始${skill.score}）· ${confLabel(skill.confidence)}${hasChart ? ' · 🏅' + skill.chart_count + '榜' : ''}${isCN(skill) ? ' · 🇨🇳' : ''} │`);
  console.log(`   │ 赛道：${skill.cat}${skill.best_in_track ? '（赛道最优）' : ''}          │`);
  console.log(`   │ ★ 13维质量：${gradeLabel(qGrade)} (${qg}/100)            │`);
  if (dims) {
    // 显示13维雷达
    const dimNames = ['description','tags','install','safety','dependency','doc_structure','error_handling','maintenance','tests','market','market_validation'];
    const dimLabels = ['描述质量','标签完整','安装便捷','安全评分','依赖复杂度','文档结构','错误处理','维护活跃度','测试覆盖','市场热度','市场验证'];
    let dimStr = dimNames.map((k, i) => {
      const v = dims[k] !== undefined ? dims[k] : '?';
      const bar = '█'.repeat(Math.round(v/5)) + '░'.repeat(20-Math.round(v/5));
      return `      ${dimLabels[i].padEnd(6)} ${String(v).padStart(3)} ${bar}`;
    }).join('\n');
    console.log(`   │                                     │`);
    console.log(`   │  维度雷达:                           │`);
    console.log(dimStr);
  }
  if (qm && qm.details && qm.details.github_data) {
    const gh = qm.details.github_data;
    if (gh.stars) console.log(`   │ GitHub: ⭐${(gh.stars/1000).toFixed(1)}K stars · 🍴${gh.forks || '?'} forks  │`);
  }
  if (qm && qm.details && qm.details.market_data) {
    const mk = qm.details.market_data;
    if (mk.downloads) console.log(`   │ SkillHub: 📥${(mk.downloads/1000).toFixed(1)}K downloads        │`);
  }
  console.log(`   └─────────────────────────────────────┘`);
  console.log(`   描述：${skill.desc || '无'}`);
  if (skill.recommend_reason) console.log(`   💡 ${skill.recommend_reason}`);
  if (skill.vs_note) console.log(`   📊 ${skill.vs_note}`);
  console.log(`   📦 ${install}`);
}

// ★ 全局质量报告
function cmdQualityReport() {
  if (qualityV2.length === 0) { console.log('❌ 无质量数据'); return; }
  
  // 等级分布
  const dist = {};
  qualityV2.forEach(q => {
    const g = q.quality_grade || '?';
    dist[g] = (dist[g] || 0) + 1;
  });
  
  // 分数分布
  const buckets = {'70+':0, '60-69':0, '50-59':0, '40-49':0, '30-39':0, '<30':0};
  qualityV2.forEach(q => {
    const s = q.quality_score || 0;
    if (s >= 70) buckets['70+']++;
    else if (s >= 60) buckets['60-69']++;
    else if (s >= 50) buckets['50-59']++;
    else if (s >= 40) buckets['40-49']++;
    else if (s >= 30) buckets['30-39']++;
    else buckets['<30']++;
  });
  
  // Top 10
  const top10 = [...qualityV2].sort((a,b) => b.quality_score - a.quality_score).slice(0,10);

  console.log('\n📊 SkillPick 13维质量报告\n');
  console.log('─'.repeat(50));
  console.log(`总技能数: ${qualityV2.length} | 数据源: 元数据推断 + GitHub API + SkillHub全量25000`);
  console.log('\n等级分布:');
  Object.entries({A:'🏆', 'B+':'⭐', B:'📗', C:'📙', D:'📕', F:'❌'}).forEach(([g, icon]) => {
    if (dist[g]) console.log(`  ${icon} ${g}: ${dist[g]} (${(dist[g]/qualityV2.length*100).toFixed(1)}%)`);
  });

  console.log('\n分数分布:');
  Object.entries(buckets).forEach(([range, count]) => {
    const bar = '█'.repeat(Math.round(count/qualityV2.length*50));
    console.log(`  ${range.padStart(5)}: ${count.toString().padStart(4)} ${bar}`);
  });

  console.log('\n🏆 TOP 10（13维质量分）:');
  top10.forEach((q, i) => {
    const mark = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `  `;
    const dims = q.dimensions || {};
    console.log(`${mark} ${q.name} (${q.quality_score}) ${gradeLabel(q.quality_grade)} 维护:${dims.maintenance||'?'} 市场:${dims.market||'?'}`);
  });

  // 各维度均值
  const dimNames = ['description','tags','install','safety','dependency','doc_structure','error_handling','maintenance','tests','market','market_validation'];
  const dimLabels = ['描述质量','标签完整','安装便捷','安全评分','依赖复杂度','文档结构','错误处理','维护活跃度','测试覆盖','市场热度','市场验证'];
  console.log('\n📈 维度均值:');
  dimNames.forEach((k, i) => {
    let sum = 0, cnt = 0;
    qualityV2.forEach(q => { if (q.dimensions && q.dimensions[k] !== undefined) { sum += q.dimensions[k]; cnt++; } });
    const avg = cnt > 0 ? (sum/cnt).toFixed(1) : 'N/A';
    const bar = '█'.repeat(Math.round(Number(avg)/5));
    console.log(`  ${dimLabels[i].padEnd(6)}: ${avg.padStart(5)} ${bar}`);
  });
}

// ====== 主入口 ======
const args = process.argv.slice(2);
const cmd = args[0] || 'help';
const param = args.slice(1).join(' ');

switch (cmd) {
  case 'top3':
  case 'categories':
  case 'tracks':
    cmdTop3(param);
    break;
  case 'search':
  case 'find':
  case 's':
    cmdSearch(param);
    break;
  case 'similar':
  case 'alt':
    cmdSimilar(param);
    break;
  case 'workflow':
  case 'combo':
  case 'wf':
    cmdWorkflow(param);
    break;
  case 'detail':
  case 'info':
  case 'd':
    cmdDetail(param);
    break;
  case 'quality':
  case 'report':
  case 'q':
    cmdQualityReport();
    break;
  case 'help':
  default:
    console.log(`
🏆 SkillPick API v6.3.2 — 13维质量融合版

用法：
  node api.js top3 [赛道名]       赛道TOP3推荐（同分按质量重排）
  node api.js search <关键词>     搜索推荐（乘法质量模型）
  node api.js similar <skill名>   相似替代推荐（质量排序）
  node api.js workflow [场景名]   工作流推荐（门控+加权+自动fallback）
  node api.js detail <skill名>    Skill详情（含13维质量雷达）
  node api.js quality             全局质量分布报告
  node api.js search <关键词> --show-all  强制显示全量（含D/F级）

核心特性：
  - QUALITY_BOOST_TABLE 全局配置表（调表即改策略）
  - qualityGate() 三层门控：pass(正常) / warn(C级降权30%) / block(D/F隐藏)
  - 搜索：乘法模型(×multiplier)，更公平
  - 相似：质量第三维度排序 + 替代标签融入等级差
  - 工作流：D/F级拦截+hits×boost排序+自动fallback到次优
  - TOP3：同final_score时质量高的排前 + 等级徽章 + C/D警告标注
  - 13维Z-score标准化：GitHub/SkillHub/市场验证三增强

示例：
  node api.js top3 文档处理           查看文档处理赛道
  node api.js search PDF处理          搜索推荐
  node api.js similar pdf             pdf替代选项
  node api.js detail coding-agent     详情（含13维雷达）
  node api.js quality                 全局质量报告

数据：954 skills / 45+ tracks / 7 sources + 13维质量评分(Z-score)
`);
}
