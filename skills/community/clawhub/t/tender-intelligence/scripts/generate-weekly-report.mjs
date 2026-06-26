/**
 * 招标周报生成脚本
 * 输入：最近7天招标数据
 * 输出：Markdown格式周报
 * 用法：node generate-weekly-report.mjs [近N天] [输出路径]
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = 'C:\\Users\\Administrator\\.openclaw\\workspace';
const DATA_DIR = path.join(WORKSPACE, 'data');
const OUTPUT_DIR = path.join(WORKSPACE, 'memory');

const GANSU_CITIES = ['兰州','嘉峪关','金昌','白银','天水','武威','张掖','平凉','酒泉','庆阳','定西','陇南','临夏','甘南'];
const TENDER_TYPES  = ['招标公告','招标预告','招标变更','重新招标','答疑公告','意见征集'];
const BID_TYPES     = ['中标通知','中标公告','候选人公示','合同公告'];

// 核心安防关键词（必须有）+ 排除词
const SECURITY_KEYWORDS = ['安防', '监控', '门禁', '报警', '智能化', '智慧', '弱电', '视频', '网络', '布线', '楼宇', '道闸', '停车场', '人脸', '识别', '考勤', '对讲', '巡更', '广播', '大屏', '拼接屏', '会议', '音响', '周界', '电子围栏', '红外', '闸机', '升降柱', '防撞', '防护'];
const EXCLUDE_KEYWORDS  = ['高铁', '铁路', '架梁', '通车', '地铁', '轨道', '列车', '车厢', '农田', '高标准农田', '供热', '供暖', '管网', '水利', '饮水', '蓄水池', '高速公', '高速公', '架设'];

function isRelevantTender(item) {
  const title = (item.title || item.popTitle || '');
  const tenderees = (item.tenderees || '');
  const combined = title + ' ' + tenderees;
  if (EXCLUDE_KEYWORDS.some(k => combined.includes(k))) return false;
  return SECURITY_KEYWORDS.some(k => combined.includes(k));
}

function loadQianlimaData() {
  const file = path.join(DATA_DIR, 'qianlima', 'gansu-tender.json');
  try {
    const raw = fs.readFileSync(file, 'utf8');
    const data = JSON.parse(raw);
    const items = Array.isArray(data) ? data : (data.items || []);
    return items.map(item => ({
      contentid: item.contentId || item.contentid,
      title: item.title || item.popTitle || '',
      city: item.city || item.areaName || '',
      publishTime: item.publishTime || item.updateTime || '',
      amountRaw: item.amountRaw || item.amount || null,
      amountUnit: item.amountUnit || '',
      tenderType: item.tenderType || item.noticeSegmentTypeName || '',
      tenderees: item.tenderees || item.purchasingUnit || item.unit || '',
      url: item.url || '',
      bidEndTime: item.bidEndTime || item.tenderEndTime || '',
    }));
  } catch(e) { return []; }
}

function fmtMoney(n) {
  if (!n) return '未知';
  const num = parseFloat(n);
  if (isNaN(num)) return '未知';
  if (num >= 1e8) return (num/1e8).toFixed(2)+'亿';
  if (num >= 1e4) return (num/1e4).toFixed(2)+'万';
  return num.toFixed(0)+'元';
}

function daysAgo(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d;
}

function formatDate(d) {
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

function generateWeeklyReport(days = 7, outputFile = null) {
  const items = loadQianlimaData();
  const now = new Date();
  const startDate = daysAgo(days);

  // 筛选近N天数据
  const filtered = items.filter(item => {
    if (!item.publishTime) return false;
    const itemDate = new Date(item.publishTime);
    const diff = (now - itemDate) / 86400000;
    return diff >= 0 && diff <= days;
  });

  const tenderItems = filtered.filter(i => TENDER_TYPES.includes(i.tenderType));
  const bidItems = filtered.filter(i => BID_TYPES.includes(i.tenderType));
  const totalAmount = filtered.reduce((s, i) => s + (parseFloat(i.amountRaw)||0), 0);

  // 城市分布（基于全部数据，不限于安防关键词）
  const cityStats = {};
  GANSU_CITIES.forEach(c => cityStats[c] = {tender: 0, bid: 0, amount: 0});
  filtered.forEach(i => {
    const city = i.city && GANSU_CITIES.includes(i.city) ? i.city : '其他';
    if (!cityStats[city]) cityStats[city] = {tender:0, bid:0, amount:0};
    if (TENDER_TYPES.includes(i.tenderType)) {
      cityStats[city].tender++;
      cityStats[city].amount += parseFloat(i.amountRaw)||0;
    }
    if (BID_TYPES.includes(i.tenderType)) cityStats[city].bid++;
  });

  const topCities = GANSU_CITIES
    .map(c => ({ city: c, ...cityStats[c] }))
    .filter(c => c.tender > 0 || c.bid > 0)
    .sort((a, b) => (b.tender + b.bid) - (a.tender + a.bid));

  // TOP 10 招标（按金额，安防相关项目，按金额降序）
  const topTenders = tenderItems
    .filter(i => i.amountRaw && isRelevantTender(i))
    .sort((a, b) => parseFloat(b.amountRaw||0) - parseFloat(a.amountRaw||0))
    .slice(0, 10);

  // 海康威视中标
  const haikangBids = bidItems.filter(i => {
    const t = (i.title||'') + (i.tenderees||'');
    return t.includes('海康') || t.includes('hikvision');
  });

  // 近7天趋势
  const trend = [];
  for (let d = days - 1; d >= 0; d--) {
    const dt = daysAgo(d);
    const dtStr = formatDate(dt);
    const dayItems = filtered.filter(i => i.publishTime && i.publishTime.startsWith(dtStr));
    const tNum = dayItems.filter(i => TENDER_TYPES.includes(i.tenderType)).length;
    const bNum = dayItems.filter(i => BID_TYPES.includes(i.tenderType)).length;
    const dayNm = ['日','一','二','三','四','五','六'][dt.getDay()];
    trend.push({ date: dtStr, day: dayNm, tender: tNum, bid: bNum });
  }

  const endDate = formatDate(now);
  const startStr = formatDate(startDate);
  const weekStr = `${startStr} ~ ${endDate}`;

  let md = '';
  md += `# 📈 甘肃安防市场周报\n`;
  md += `**${weekStr}** (共${days}天)\n\n`;

  md += `## 📊 本周概览\n\n`;
  md += `| 指标 | 数值 |\n|------|------|\n`;
  md += `| 新增招标公告 | ${tenderItems.length}条 |\n`;
  md += `| 新增中标公告 | ${bidItems.length}条 |\n`;
  md += `| 合计 | ${filtered.length}条 |\n`;
  md += `| 总金额 | ${fmtMoney(totalAmount)} |\n\n`;

  md += `## 📅 近${days}天趋势\n\n`;
  md += `| 日期 | 星期 | 招标 | 中标 |\n`;
  md += `|------|------|------|------|\n`;
  trend.forEach(t => {
    md += `| ${t.date} | ${t.day} | ${t.tender} | ${t.bid} |\n`;
  });
  md += `\n`;

  md += `## 🗺️ 地区分布\n\n`;
  if (topCities.length === 0) {
    md += `暂无数据\n`;
  } else {
    topCities.forEach(({ city, tender, bid, amount }) => {
      md += `- **${city}**: 招标${tender}条 | 中标${bid}条${amount > 0 ? ' | 金额' + fmtMoney(amount) : ''}\n`;
    });
  }
  md += `\n`;

  // 海康威视中标项目
  if (haikangBids.length > 0) {
    md += `## 🔥 海康威视中标项目\n\n`;
    haikangBids.slice(0, 10).forEach(item => {
      md += `- 【${item.city}】【${item.publishTime}】${(item.title||'').substring(0,50)}\n`;
      if (item.amountRaw) md += `  - 金额：${fmtMoney(item.amountRaw)}\n`;
    });
    md += `\n`;
  } else {
    md += `## 🔥 海康威视中标项目\n\n暂无中标数据\n\n`;
  }

  // 重点项目 TOP10（安防相关，按金额降序）
  md += `## ⭐ 重点项目 TOP10（招标，按金额降序）\n\n`;
  if (topTenders.length === 0) {
    md += `暂无数据\n`;
  } else {
    topTenders.forEach((item, i) => {
      md += `${i+1}. **${item.title.slice(0, 55)}**\n`;
      md += `   - 💰 ${fmtMoney(item.amountRaw)} | ${item.city} | ${item.publishTime}`;
      if (item.bidEndTime) md += ` | 截止：${item.bidEndTime}`;
      md += `\n`;
    });
  }
  md += `\n`;

  md += `## 📁 数据来源\n\n`;
  md += `- 千里马招标网 (总库${items.length}条)\n`;
  md += `- 本周采集数据${filtered.length}条\n\n`;
  md += `---\n`;
  md += `*由 9527 自动生成 | ${new Date().toLocaleString('zh-CN')}*\n`;

  if (outputFile) {
    fs.writeFileSync(outputFile, md, 'utf8');
    console.log(`✅ 周报已保存: ${outputFile}`);
  }

  return md;
}

// CLI
const args = process.argv.slice(2);
const daysArg = parseInt(args.find(a => /^\d+$/.test(a)) || '7');
const outputPath = args.find(a => a.endsWith('.md') || a.endsWith('.txt')) || null;
const report = generateWeeklyReport(daysArg, outputPath);
if (!outputPath) console.log(report);