/**
 * 招标情报 Skill 执行入口 (index.js)
 * 轻量化实现：读取本地已采集数据，支持搜索查询
 * 数据源优先级：千里马 > 中项网 > 甘肃政府采购网
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = 'C:\\Users\\Administrator\\.openclaw\\workspace';
const DATA_DIR = path.join(WORKSPACE, 'data');
const SKILL_DIR = __dirname;

const GANSU_CITIES = ['兰州','嘉峪关','金昌','白银','天水','武威','张掖','平凉','酒泉','庆阳','定西','陇南','临夏','甘南'];
const DEFAULT_KEYWORDS = ['安防','监控','智能化','弱电','门禁','报警','视频监控','智慧城市','网络安全','音视频','信息化'];

// 全国省份列表（用于搜索过滤）
const PROVINCES = ['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','新疆','台湾','香港','澳门'];

// 数据保留天数（超过则不加载）
const DATA_RETENTION_DAYS = 15;

const TENDER_TYPES  = ['招标公告','招标预告','招标变更','重新招标','答疑公告','意见征集'];
const BID_TYPES     = ['中标通知','中标公告','候选人公示','合同公告'];
const RESULT_TYPES   = ['结果公告','废标公告','流标公告','验收公告'];

// ─── 工作日基准（甘肃市场经验值）──────────────────────────────────────
// 甘肃安防市场工作日日均约 140-150 条招标/天
const WORKDAY_DAILY_BASELINE = 148;
const ALERT_THRESHOLD = 0.15;  // <15%基准 → 🔴 严重告警
const WARN_THRESHOLD  = 0.30;  // <30%基准 → 🟡 提醒

// ─── 数据加载 ───────────────────────────────────────────────

function loadQianlimaData() {
  const file = path.join(DATA_DIR, 'qianlima', 'gansu-tender.json');
  try {
    const raw = fs.readFileSync(file, 'utf8');
    const data = JSON.parse(raw);
    const items = Array.isArray(data) ? data : (data.items || []);

    const now = new Date();
    const cutoffMs = now.getTime() - DATA_RETENTION_DAYS * 86400000;

    return items.map(item => {
      const publishTimeRaw = item.publishTime || item.updateTime || '';
      const itemDate = new Date(publishTimeRaw);
      const itemDateMs = itemDate.getTime();

      // 数据时效管理：跳过超过 DATA_RETENTION_DAYS 的数据
      if (!publishTimeRaw || isNaN(itemDateMs) || itemDateMs < cutoffMs) {
        return null;
      }

      return {
        contentid: item.contentId || item.contentid,
        title: item.title || item.popTitle || '',
        city: item.city || item.areaName || normalizeCity(item.title || ''),
        province: extractProvince(item.areaName || ''),
        publishTime: publishTimeRaw,
        amountRaw: item.amountRaw || item.amount || null,
        amountUnit: item.amountUnit || '',
        tenderType: item.tenderType || item.noticeSegmentTypeName || '',
        bidEndTime: item.bidEndTime || '',
        url: item.url || (item.contentid ? `http://www.qianlima.com/zb/detail/${item.publishTime?.slice(0,4) || ''}${item.contentid}.html` : ''),
        matchedKeywords: item.matchedKeywords || [],
      };
    }).filter(Boolean);
  } catch(e) { return []; }
}

function loadBiddersData() {
  const file = path.join(DATA_DIR, 'qianlima', 'bidders-data.json');
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch(e) { return { bidders: [] }; }
}

/** 加载用户自定义关键词（优先读用户配置，不存在则用默认） */
function loadCustomKeywords() {
  const userKwFile = path.join(SKILL_DIR, 'user-keywords.txt');
  try {
    const raw = fs.readFileSync(userKwFile, 'utf8');
    const words = raw.split(/\n/).map(w => w.trim()).filter(w => w.length > 0 && !w.startsWith('#'));
    return words.length > 0 ? words : DEFAULT_KEYWORDS;
  } catch(e) {
    return DEFAULT_KEYWORDS;
  }
}

/** 获取用户自定义关键词文件路径（用于告知用户如何配置） */
function getCustomKeywordFile() {
  return path.join(SKILL_DIR, 'user-keywords.txt');
}

// ─── 工具函数 ──────────────────────────────────────────────

// ─── 工具函数 ──────────────────────────────────────────────

/** 从 areaName 提取省份（支持 "甘肃-天水" 格式） */
function extractProvince(areaName) {
  if (!areaName) return '';
  for (const p of PROVINCES) {
    if (areaName.startsWith(p)) return p;
  }
  // 兼容：天水/兰州 等城市名 → 甘肃
  for (const c of GANSU_CITIES) {
    if (areaName.includes(c)) return '甘肃';
  }
  return '';
}

function normalizeCity(text) {
  if (!text) return '未知';
  for (const c of GANSU_CITIES) {
    if (text.includes(c)) return c;
  }
  return '未知';
}

function parseAmount(title, href) {
  const patterns = [
    /([\d,]+\.?\d*)\s*亿/, /([\d,]+\.?\d*)\s*万/, /([\d,]+\.?\d*)\s*元/,
  ];
  for (const p of patterns) {
    const m = title.match(p);
    if (m) {
      const n = parseFloat(m[1].replace(/,/g, ''));
      if (p.toString().includes('亿')) return n * 1e8;
      if (p.toString().includes('万')) return n * 1e4;
      return n;
    }
  }
  return null;
}

function fmtMoney(n) {
  if (!n) return '未知';
  const num = parseFloat(n);
  if (isNaN(num)) return '未知';
  if (num >= 1e8) return (num/1e8).toFixed(2)+'亿';
  if (num >= 1e4) return (num/1e4).toFixed(2)+'万';
  return num.toFixed(0)+'元';
}

function isWeekend(date) {
  const d = date.getDay();
  return d === 0 || d === 6;
}

function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

function daysAgoMs(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.getTime();
}

function extractKeywords(query) {
  if (!query) return [];  // 无查询词 → 不做行业过滤，返回全部
  const stopWords = new Set(['招标','中标','甘肃','搜索','查看','帮我','今天','本周','最近','条数','近']);
  const words = query
    .replace(/[^\w\u4e00-\u9fff]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 1 && !stopWords.has(w));
  return words.length > 0 ? words : [];
}

function matchItem(item, keywords, provinces, query) {
  if (!query || (keywords.length === 0 && provinces.length === 0)) return true;  // 无查询词时返回全部
  const title = (item.title || '').toLowerCase();
  const city = (item.city || '').toLowerCase();
  const province = (item.province || '').toLowerCase();

  // 省份匹配
  if (provinces.length > 0) {
    const matchProvince = provinces.some(p => province.includes(p.toLowerCase()) || city.includes(p.toLowerCase()));
    if (!matchProvince) return false;
  }

  // 关键词匹配：标题或城市中包含任意一个关键词即匹配（无关键词时返回省份匹配的全部）
  if (keywords.length === 0) return true;
  return keywords.some(k => title.includes(k.toLowerCase()) || city.includes(k.toLowerCase()));
}

/** 从query中提取省份关键词（优先级高于行业关键词） */
function extractProvinces(query) {
  if (!query) return [];
  const provinces = [];
  const upper = query;
  for (const p of PROVINCES) {
    if (upper.includes(p)) provinces.push(p);
  }
  return provinces;
}

// ─── 核心搜索逻辑 ──────────────────────────────────────────

function search({ query = '', days = 7, limit = 20, type = 'all' } = {}) {
  const items = loadQianlimaData();
  const keywords = extractKeywords(query);
  const provinces = extractProvinces(query);
  const now = new Date();
  const cutoff = new Date(now); cutoff.setDate(cutoff.getDate() - days);

  const filtered = items.filter(item => {
    if (!item.publishTime) return false;
    const itemDate = new Date(item.publishTime);
    const diff = (now - itemDate) / 86400000;
    if (diff < 0 || diff > days) return false;
    if (!matchItem(item, keywords, provinces, query)) return false;
    if (type === 'tender' && !TENDER_TYPES.includes(item.tenderType)) return false;
    if (type === 'bid' && !BID_TYPES.includes(item.tenderType)) return false;
    return true;
  });

  filtered.sort((a, b) => (parseFloat(b.amountRaw||0)||0) - (parseFloat(a.amountRaw||0)||0));

  return filtered.slice(0, limit).map(item => {
    const amt = item.amountRaw ? fmtMoney(item.amountRaw) : fmtMoney(parseAmount(item.title || '', item.url || ''));
    return {
      title: item.title || '未知',
      party: item.tenderees || item.unit || '未知',
      amount: amt,
      date: item.publishTime ? item.publishTime.slice(0, 10) : '未知',
      source: '千里马',
      link: item.url || `https://www.qianlima.com/bid-${item.contentid}.html`,
      tenderType: item.tenderType || '未知',
      city: item.city || '未知',
    };
  });
}

// ─── 数据质量评估 ──────────────────────────────────────────

/**
 * 评估昨日数据质量
 * @returns {{ status: 'ok'|'warn'|'alert'|'weekend', message: string, yesterday: object }}
 */
function assessDataQuality() {
  const now = new Date();
  const yesterday = new Date(now); yesterday.setDate(yesterday.getDate() - 1);
  const yDateStr = `${yesterday.getFullYear()}-${String(yesterday.getMonth()+1).padStart(2,'0')}-${String(yesterday.getDate()).padStart(2,'0')}`;
  const dayOfWeek = yesterday.getDay();

  const items = loadQianlimaData();
  const yesterdayItems = items.filter(i => i.publishTime && i.publishTime.startsWith(yDateStr));
  const tenderCount = yesterdayItems.filter(i => TENDER_TYPES.includes(i.tenderType)).length;
  const bidCount = yesterdayItems.filter(i => BID_TYPES.includes(i.tenderType)).length;
  const totalCount = tenderCount + bidCount;

  // 获取最后数据更新时间（取最新一条的时间戳）
  let lastUpdateTime = null;
  if (items.length > 0) {
    const sorted = [...items].filter(i => i.publishTime).sort((a, b) => new Date(b.publishTime) - new Date(a.publishTime));
    if (sorted.length > 0) lastUpdateTime = sorted[0].publishTime;
  }

  // 判断质量状态
  let status, message, emoji;
  if (dayOfWeek === 0 || dayOfWeek === 6) {
    // 周末：标注低峰期，不报警
    status = 'weekend';
    emoji = '🟢';
    message = `周末低峰，属正常情况（节假日数据量通常大幅下降）`;
  } else {
    const ratio = totalCount / WORKDAY_DAILY_BASELINE;
    if (totalCount === 0) {
      status = 'alert';
      emoji = '🔴';
      message = `工作日数据为0，疑似采集异常`;
    } else if (ratio < ALERT_THRESHOLD) {
      status = 'alert';
      emoji = '🔴';
      message = `昨日仅 ${totalCount} 条，低于基准 ${WORKDAY_DAILY_BASELINE} 条的15%（${(ratio*100).toFixed(0)}%），可能存在采集问题`;
    } else if (ratio < WARN_THRESHOLD) {
      status = 'warn';
      emoji = '🟡';
      message = `昨日 ${totalCount} 条，低于基准 ${WORKDAY_DAILY_BASELINE} 条的30%（${(ratio*100).toFixed(0)}%），属轻微波动`;
    } else {
      status = 'ok';
      emoji = '🟢';
      message = `数据正常，工作日基准 ${WORKDAY_DAILY_BASELINE} 条/天`;
    }
  }

  return {
    status,
    emoji,
    message,
    yesterday: {
      date: yDateStr,
      tenderCount,
      bidCount,
      totalCount,
      dayName: ['周日','周一','周二','周三','周四','周五','周六'][dayOfWeek],
      lastUpdateTime,
    }
  };
}

// ─── 报告生成 ─────────────────────────────────────────────

function loadAllDataForReport(days = 1) {
  // 用于日报/周报：只过滤时间，不过滤关键词，得到最真实的数据概览
  // 使用日期字符串比较，避免UTC凌晨时区的边界问题
  const items = loadQianlimaData();
  const now = new Date();
  const todayStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  return items.filter(item => {
    if (!item.publishTime) return false;
    // publishTime 格式："2026-05-09"（日期字符串）或 "2026-05-09T10:30:00"（ISO时间戳）
    const itemDateStr = item.publishTime.slice(0, 10);  // 取前10字符即 YYYY-MM-DD
    const nowDateStr = todayStr;
    // 计算日期差：天数
    const itemDate = new Date(itemDateStr);
    const diff = Math.floor((now - itemDate) / 86400000);
    return diff >= 0 && diff <= days;
  });
}

function generateDailyBrief() {
  const quality = assessDataQuality();
  const now = new Date();
  const todayStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  // 日报：不按关键词过滤，只按类型展示（得到真实全量数据）
  const yesterdayRaw = loadAllDataForReport(1);
  const tenderItems = yesterdayRaw.filter(i => TENDER_TYPES.includes(i.tenderType));
  const bidItems = yesterdayRaw.filter(i => BID_TYPES.includes(i.tenderType));
  const totalItems = tenderItems.concat(bidItems);

  const qualityBlock = `${quality.emoji} 数据健康度：${quality.status === 'weekend' ? '正常' : quality.status === 'ok' ? '正常' : quality.status === 'warn' ? '轻微波动' : '⚠️ 需关注'}
  └ 昨日（${quality.yesterday.dayName}）新增 ${quality.yesterday.totalCount} 条（招标${quality.yesterday.tenderCount}条 / 中标${quality.yesterday.bidCount}条）${quality.status === 'weekend' ? '' : '— ' + quality.message}${quality.yesterday.lastUpdateTime ? '\n  └ 最后数据更新：' + quality.yesterday.lastUpdateTime.slice(0,16).replace('T',' ') : ''}`;

  let r = `📊 【X省安防市场日报】\n${todayStr}\n\n`;
  r += `【数据健康度】\n${qualityBlock}\n\n`;
  r += `【整体数据】\n`;
  r += `• 招标公告: ${tenderItems.length}条\n`;
  r += `• 中标公告: ${bidItems.length}条\n`;
  r += `• 合计: ${totalItems.length}条\n\n`;

  if (totalItems.length > 0) {
    r += `【招标项目 TOP5】\n`;
    tenderItems.slice(0, 5).forEach((item, i) => {
      const amt = item.amountRaw ? fmtMoney(item.amountRaw) : fmtMoney(parseAmount(item.title || '', item.url || ''));
      r += `${i+1}. ${item.title.slice(0, 40)}\n`;
      r += `   💰 ${amt} | ${item.city} | ${item.publishTime?.slice(0, 10)}\n`;
    });
    r += `\n【中标项目 TOP5】\n`;
    bidItems.slice(0, 5).forEach((item, i) => {
      const amt = item.amountRaw ? fmtMoney(item.amountRaw) : fmtMoney(parseAmount(item.title || '', item.url || ''));
      r += `${i+1}. ${item.title.slice(0, 40)}\n`;
      r += `   💰 ${amt} | ${item.city} | ${item.publishTime?.slice(0, 10)}\n`;
    });
  } else {
    r += `暂无数据（请检查采集是否正常运行）\n`;
  }
  r += `\n📁 数据来源：千里马招标网 | 总库${loadQianlimaData().length}条\n`;
  r += `💡 想看特定地区/关键词？试试：node index.js 兰州 监控\n`;
  return r;
}

// ─── 命令行 / Skill 入口 ──────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log(generateDailyBrief());
    return;
  }

  // 处理特殊命令
  if (args[0] === '--report') {
    const daysArg = parseInt(args[1]) || 1;
    const isWeekly = daysArg > 1;
    const scriptName = isWeekly ? 'generate-weekly-report.mjs' : 'generate-report-v8.mjs';
    const scriptDir = isWeekly
      ? path.join(SKILL_DIR, 'scripts')
      : path.join(WORKSPACE, 'scripts');
    const scriptPath = path.join(scriptDir, scriptName);
    const procArgs = isWeekly ? [String(daysArg)] : [];
    console.log(`📄 生成${isWeekly ? `周报（近${daysArg}天）` : '日报'}...`);
    const child = spawn('node', [scriptPath, ...procArgs], { shell: true });
    child.stdout.on('data', d => process.stdout.write(d));
    child.stderr.on('data', d => process.stderr.write(d));
    child.on('close', code => { process.exit(code || 0); });
    return;
  }

  if (args[0] === '--quality') {
    const q = assessDataQuality();
    console.log(`数据健康度评估：`);
    console.log(`  状态：${q.status}`);
    console.log(`  ${q.emoji} ${q.message}`);
    console.log(`  昨日（${q.yesterday.dayName}）：招标${q.yesterday.tenderCount}条 / 中标${q.yesterday.bidCount}条`);
    return;
  }

  if (args[0] === '--keywords') {
    const kw = loadCustomKeywords();
    const isDefault = !fs.existsSync(getCustomKeywordFile());
    if (isDefault) {
      console.log(`📋 当前使用默认关键词（${kw.length}个）：`);
    } else {
      console.log(`📋 当前使用自定义关键词（${kw.length}个，来自 user-keywords.txt）：`);
    }
    kw.forEach((k, i) => console.log(`  ${i+1}. ${k}`));
    if (isDefault) {
      console.log(`\n💡 如需自定义关键词，创建文件：`);
      console.log(`   ${getCustomKeywordFile()}`);
      console.log(`   每行一个关键词，#开头为注释`);
    }
    return;
  }

  if (args[0] === '--set-keyword') {
    const keyword = args.slice(1).join(' ');
    if (!keyword) { console.log('用法：node index.js --set-keyword <关键词>'); return; }
    const kwFile = getCustomKeywordFile();
    const existing = fs.existsSync(kwFile) ? fs.readFileSync(kwFile, 'utf8') : '# 自定义关键词\n';
    if (existing.includes(keyword)) {
      console.log(`关键词「${keyword}」已存在`);
    } else {
      fs.writeFileSync(kwFile, existing.trim() + '\n' + keyword + '\n', 'utf8');
      console.log(`✅ 已添加关键词「${keyword}」`);
    }
    return;
  }

  const query = args.join(' ');
  const typeMatch = query.match(/类型[=:](招标|中标|全部)/);
  const type = typeMatch ? (typeMatch[1] === '招标' ? 'tender' : typeMatch[1] === '中标' ? 'bid' : 'all') : 'all';
  const daysMatch = query.match(/近?(\d+)天/);
  const days = daysMatch ? parseInt(daysMatch[1]) : 7;
  const limitMatch = query.match(/条数[=:]?(\d+)/);
  const limit = limitMatch ? parseInt(limitMatch[1]) : 20;

  const keywords = loadCustomKeywords();
  const results = search({ query, days, limit, type });

  // 搜索时显示用了哪些关键词
  const usedKw = extractKeywords(query).filter(k => !['招标','中标','甘肃'].includes(k));

  if (results.length === 0) {
    console.log(`🔍 未找到匹配「${query}」的招标信息`);
    if (usedKw.length > 0) console.log(`   命中关键词：${usedKw.join(', ')}`);
    console.log(`   可尝试：扩大天数（近30天）或调整关键词`);
    return;
  }

  console.log(`🔍 搜索「${query}」，共找到 ${results.length} 条：`);
  if (usedKw.length > 0) console.log(`   命中关键词：${usedKw.join(', ')}`);
  console.log();
  results.forEach((item, i) => {
    console.log(`【${i+1}】${item.title}`);
    console.log(`   💰 ${item.amount} | ${item.city} | ${item.date} | ${item.source}`);
    console.log(`   🔗 ${item.link}`);
    console.log();
  });
}

main().catch(console.error);