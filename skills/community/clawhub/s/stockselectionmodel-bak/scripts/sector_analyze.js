#!/usr/bin/env node
/**
 * sector_analyze.js - A 股板块趋势分析
 *
 * 使用东方财富免费 API 拉取板块行情 + 成分股涨跌，
 * 输出结构化数据供 agent 做趋势研判。
 *
 * 用法:
 *   node sector_analyze.js --sector 新能源
 *   node sector_analyze.js --sector AI
 *   node sector_analyze.js --sector 半导体
 *   node sector_analyze.js --sector 机器人
 *   node sector_analyze.js --list              # 列出所有支持的板块
 *   node sector_analyze.js --json              # JSON 输出
 */

const EASTMONEY_LIST = 'https://push2.eastmoney.com/api/qt/clist/get';
const EASTMONEY_QUOTE = 'https://push2.eastmoney.com/api/qt/ulist.np/get';

// ── 常见板块代码映射 ────────────────────────────────────────────────
// 东方财富概念板块(t:3) + 细分行业(t:2)
const SECTOR_MAP = {
  // 新能源
  '新能源': { codes: ['BK0493', 'BK0478'], desc: '新能源（含光伏、风电、储能）' },
  '光伏': { codes: ['BK1029'], desc: '光伏产业链' },
  '锂电池': { codes: ['BK0574'], desc: '锂电池产业链' },
  '储能': { codes: ['BK1028'], desc: '储能' },
  '风电': { codes: ['BK0485'], desc: '风力发电' },
  '充电桩': { codes: ['BK0501'], desc: '充电桩/充电设施' },
  // AI / 科技
  'AI': { codes: ['BK1131', 'BK1132'], desc: 'AI / 人工智能概念' },
  '算力': { codes: ['BK1113'], desc: '算力/东数西算' },
  '大模型': { codes: ['BK1131'], desc: 'ChatGPT/大模型概念' },
  '芯片': { codes: ['BK0515'], desc: '芯片/半导体' },
  '半导体': { codes: ['BK0515'], desc: '半导体' },
  '光模块': { codes: ['BK1108'], desc: 'CPO/光模块' },
  '机器人': { codes: ['BK0536'], desc: '机器人概念' },
  '自动驾驶': { codes: ['BK0802'], desc: '无人驾驶/自动驾驶' },
  '智能驾驶': { codes: ['BK0802'], desc: '智能驾驶' },
  // 消费 / 医药
  '白酒': { codes: ['BK0477'], desc: '白酒' },
  '医药': { codes: ['BK1216'], desc: '医药生物' },
  '创新药': { codes: ['BK1106'], desc: '创新药' },
  '中药': { codes: ['BK0615'], desc: '中药概念' },
  '医美': { codes: ['BK0889'], desc: '医美概念' },
  '减肥药': { codes: ['BK1146'], desc: '减肥药' },
  '生物疫苗': { codes: ['BK0548'], desc: '生物疫苗' },
  '消费': { codes: ['BK0473'], desc: '大消费' },
  // 金融
  '券商': { codes: ['BK0707'], desc: '券商' },
  '银行': { codes: ['BK0475'], desc: '银行' },
  '保险': { codes: ['BK0474'], desc: '保险' },
  // 其他热门
  '军工': { codes: ['BK0481'], desc: '国防军工' },
  '房地产': { codes: ['BK0451'], desc: '房地产' },
  '数字经济': { codes: ['BK1090'], desc: '数字经济' },
  '华为': { codes: ['BK0855'], desc: '华为概念' },
  // 化工
  '化工': { codes: ['BK1206'], desc: '基础化工' },
  '化学制品': { codes: ['BK0538'], desc: '化学制品' },
  '煤化工': { codes: ['BK1419'], desc: '煤化工' },
  '磷化工': { codes: ['BK1435'], desc: '磷肥及磷化工' },
  '化纤': { codes: ['BK0471'], desc: '化学纤维' },
};

// 别名映射
const ALIASES = {
  '人工智能': 'AI', 'ai': 'AI', '智能': 'AI',
  '新能': '新能源', '清洁能源': '新能源', '绿色能源': '新能源',
  '锂电': '锂电池', '电池': '锂电池', '宁德': '锂电池',
  '光伏板': '光伏', '太阳能': '光伏',
  '风力': '风电',
  '充电': '充电桩',
  '半导': '半导体', '集成电路': '半导体',
  '机器': '机器人', '人形机器人': '机器人',
  '驾驶': '自动驾驶', '无人驾驶': '自动驾驶',
  '医药生物': '医药', '制药': '医药', '创新药': '创新药', '中药': '中药', '疫苗': '生物疫苗',
  '国防': '军工', '地产': '房地产',
  '数字': '数字经济', '数据': '数字经济',
  '化学': '化工', '基础化工': '化工', '化工股': '化工',
  '磷肥': '磷化工', '煤化': '煤化工', '化学纤维': '化纤',
};

function resolveSector(input) {
  const key = input.trim();
  if (SECTOR_MAP[key]) return key;
  // 尝试别名
  for (const [alias, target] of Object.entries(ALIASES)) {
    if (key.includes(alias) || alias.includes(key)) return target;
  }
  // 模糊匹配
  for (const name of Object.keys(SECTOR_MAP)) {
    if (name.includes(key) || key.includes(name)) return name;
  }
  return null;
}

function parseArgs(argv) {
  const out = { sector: null, list: false, json: false, top: 10, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--sector' || a === '-s') out.sector = argv[++i];
    else if (a === '--list' || a === '-l') out.list = true;
    else if (a === '--json') out.json = true;
    else if (a === '--top' || a === '-n') out.top = Number(argv[++i]);
    else if (!a.startsWith('-')) out.sector = a;  // 直接传板块名
  }
  return out;
}

async function fetchSectorStocks(boardCode, top = 10) {
  // 拉取板块成分股，按涨跌幅排序
  const url = `${EASTMONEY_LIST}?pn=1&pz=${top}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=b:${boardCode}&fields=f2,f3,f4,f5,f6,f7,f12,f14,f15,f16`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; AIStockInsider/1.0)' },
    signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  if (!data?.data?.diff) return { total: 0, stocks: [] };

  return {
    total: data.data.total,
    stocks: data.data.diff.map(d => ({
      code: d.f12,
      name: d.f14,
      price: d.f2,
      change_pct: d.f3,    // 涨跌幅 %
      change_amt: d.f4,    // 涨跌额
      volume_ratio: d.f5,  // 量比
      turnover: d.f6,      // 成交额
      amplitude: d.f7,     // 振幅
      high: d.f15,         // 最高
      low: d.f16,          // 最低
    })),
  };
}

// 也拉跌幅最大的
async function fetchSectorBottom(boardCode, top = 5) {
  const url = `${EASTMONEY_LIST}?pn=1&pz=${top}&po=0&np=1&fltt=2&invt=2&fid=f3&fs=b:${boardCode}&fields=f2,f3,f4,f12,f14`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; AIStockInsider/1.0)' },
    signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) return [];
  const data = await res.json();
  if (!data?.data?.diff) return [];
  return data.data.diff.map(d => ({
    code: d.f12,
    name: d.f14,
    price: d.f2,
    change_pct: d.f3,
    change_amt: d.f4,
  }));
}

function formatReport(sectorName, desc, topStocks, bottomStocks, total) {
  const lines = [];
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  lines.push(`\n📊 ${desc}板块分析 · ${now}\n`);
  lines.push(`板块成分股总数: ${total}\n`);

  // 涨幅统计
  const upCount = topStocks.stocks.filter(s => s.change_pct > 0).length;
  const downCount = topStocks.stocks.filter(s => s.change_pct < 0).length;
  const flatCount = topStocks.stocks.filter(s => s.change_pct === 0).length;
  const limitUp = topStocks.stocks.filter(s => s.change_pct >= 9.9).length;
  const limitDown = bottomStocks.filter(s => s.change_pct <= -9.9).length;

  lines.push(`📈 涨幅 TOP ${topStocks.stocks.length}`);
  for (const s of topStocks.stocks) {
    const sign = s.change_pct > 0 ? '+' : '';
    const tag = s.change_pct >= 9.9 ? ' 🔥涨停' : s.change_pct >= 5 ? ' 🚀' : '';
    lines.push(`  ${s.name}(${s.code})  ¥${s.price}  ${sign}${s.change_pct}%${tag}`);
  }

  lines.push(`\n📉 跌幅 TOP ${bottomStocks.length}`);
  for (const s of bottomStocks) {
    const tag = s.change_pct <= -9.9 ? ' ⚠️跌停' : s.change_pct <= -5 ? ' ⚠️' : '';
    lines.push(`  ${s.name}(${s.code})  ¥${s.price}  ${s.change_pct}%${tag}`);
  }

  if (limitUp > 0 || limitDown > 0) {
    lines.push(`\n🔔 涨停: ${limitUp} 只  |  跌停: ${limitDown} 只`);
  }

  lines.push('');
  return lines.join('\n');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    console.error('Usage: node sector_analyze.js --sector 新能源 [--top 10] [--json] [--list]');
    process.exit(0);
  }

  if (args.list) {
    console.log('\n📋 支持的板块:\n');
    for (const [name, info] of Object.entries(SECTOR_MAP)) {
      console.log(`  ${name.padEnd(8)} → ${info.desc} (${info.codes.join(', ')})`);
    }
    console.log('\n也支持别名，如: 人工智能→AI, 锂电→锂电池, 太阳能→光伏\n');
    process.exit(0);
  }

  if (!args.sector) {
    console.error('请指定板块名称，如: node sector_analyze.js --sector 新能源');
    console.error('使用 --list 查看所有支持的板块');
    process.exit(2);
  }

  const resolved = resolveSector(args.sector);
  if (!resolved) {
    console.error(`[ERROR] 未找到板块: "${args.sector}"`);
    console.error('使用 --list 查看所有支持的板块');
    process.exit(2);
  }

  const sectorInfo = SECTOR_MAP[resolved];
  console.error(`[Sector] ${resolved} → ${sectorInfo.desc} (${sectorInfo.codes.join(', ')})`);

  // 对每个板块代码拉数据，合并
  let allTop = { total: 0, stocks: [] };
  let allBottom = [];

  for (const code of sectorInfo.codes) {
    try {
      const top = await fetchSectorStocks(code, args.top);
      const bottom = await fetchSectorBottom(code, 5);
      allTop.total += top.total;
      allTop.stocks.push(...top.stocks);
      allBottom.push(...bottom);
    } catch (e) {
      console.error(`  [WARN] ${code}: ${e.message}`);
    }
  }

  // 去重
  const seenTop = new Set();
  allTop.stocks = allTop.stocks.filter(s => {
    if (seenTop.has(s.code)) return false;
    seenTop.add(s.code);
    return true;
  });
  const seenBot = new Set();
  allBottom = allBottom.filter(s => {
    if (seenBot.has(s.code)) return false;
    seenBot.add(s.code);
    return true;
  });

  if (args.json) {
    const output = {
      timestamp: new Date().toISOString(),
      sector: resolved,
      description: sectorInfo.desc,
      total_stocks: allTop.total,
      top_gainers: allTop.stocks,
      top_losers: allBottom,
    };
    process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  } else {
    console.log(formatReport(resolved, sectorInfo.desc, allTop, allBottom, allTop.total));
  }
}

main().catch(e => {
  console.error(`Fatal: ${e.stack || e.message}`);
  process.exit(1);
});
