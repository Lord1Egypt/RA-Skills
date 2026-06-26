#!/usr/bin/env node
/**
 * fetch_us_related.js - 抓取板块对应的美股关联信息
 *
 * 数据源：东方财富全球指数 + 搜索接口
 * 输出：JSON { us_stocks, events }
 *
 * 用法:
 *   node fetch_us_related.js --sector 化工
 *   node fetch_us_related.js --sector 医药
 */

// ── A股板块 → 美股关联映射 ──
const US_MAPPING = {
  '化工': { keywords: ['化工 涨价 供应', '化工品 期货 能源'], filter: /化工|化学|能源|原油|天然气|甲醇|烧碱|聚氨酯|磷|钾肥/, stocks: [
    { name: '陶氏化学', ticker: 'DOW', desc: '全球化工龙头' },
    { name: '巴斯夫', ticker: 'BASFY', desc: '欧洲化工巨头' },
    { name: '利安德巴塞尔', ticker: 'LYB', desc: '聚烯烃/炼化' },
  ]},
  '基础化工': { keywords: ['化工 涨价 供应', '化工品 期货 能源'], filter: /化工|化学|能源|原油|天然气|甲醇|烧碱|聚氨酯|磷|钾肥/, stocks: [
    { name: '陶氏化学', ticker: 'DOW', desc: '全球化工龙头' },
    { name: '巴斯夫', ticker: 'BASFY', desc: '欧洲化工巨头' },
    { name: '利安德巴塞尔', ticker: 'LYB', desc: '聚烯烃/炼化' },
  ]},
  '医药': { keywords: ['医药 FDA 新药 审批', '创新药 集采 医保'], filter: /医药|药|FDA|集采|医保|临床|审批|生物|疫苗/, stocks: [
    { name: '辉瑞', ticker: 'PFE', desc: '全球制药龙头' },
    { name: '礼来', ticker: 'LLY', desc: '减肥药/糖尿病' },
    { name: '安进', ticker: 'AMGN', desc: '生物制药' },
  ]},
  '医药生物': { keywords: ['医药 FDA 新药 审批', '创新药 集采 医保'], filter: /医药|药|FDA|集采|医保|临床|审批|生物|疫苗/, stocks: [
    { name: '辉瑞', ticker: 'PFE', desc: '全球制药龙头' },
    { name: '礼来', ticker: 'LLY', desc: '减肥药/糖尿病' },
    { name: '安进', ticker: 'AMGN', desc: '生物制药' },
  ]},
  'AI': { keywords: ['英伟达 AI 芯片', 'OpenAI 大模型 算力'], filter: /AI|人工智能|芯片|算力|英伟达|NVIDIA|大模型|GPU|数据中心/, stocks: [
    { name: '英伟达', ticker: 'NVDA', desc: 'AI芯片/GPU' },
    { name: '微软', ticker: 'MSFT', desc: 'AI云/OpenAI' },
    { name: '谷歌', ticker: 'GOOGL', desc: 'Gemini/AI搜索' },
    { name: '博通', ticker: 'AVGO', desc: 'AI网络芯片' },
  ]},
  '半导体': { keywords: ['半导体 芯片 出口管制', '台积电 晶圆 先进制程'], filter: /半导体|芯片|晶圆|制程|光刻|封装|存储|GPU|CPU/, stocks: [
    { name: '英伟达', ticker: 'NVDA', desc: 'GPU/AI芯片' },
    { name: '台积电', ticker: 'TSM', desc: '晶圆代工' },
    { name: 'AMD', ticker: 'AMD', desc: 'CPU/GPU' },
    { name: '高通', ticker: 'QCOM', desc: '移动芯片' },
  ]},
  '新能源': { keywords: ['新能源 特斯拉 光伏 储能', '锂电 碳酸锂 电池'], filter: /新能源|光伏|锂|电池|储能|风电|特斯拉|充电|碳酸锂/, stocks: [
    { name: '特斯拉', ticker: 'TSLA', desc: '新能源车/储能' },
    { name: 'First Solar', ticker: 'FSLR', desc: '光伏组件' },
    { name: 'Enphase', ticker: 'ENPH', desc: '微型逆变器' },
  ]},
  '机器人': { keywords: ['机器人 人形 特斯拉 Optimus', '机器人 减速器 伺服'], filter: /机器人|人形|Optimus|减速器|伺服|手术/, stocks: [
    { name: '特斯拉', ticker: 'TSLA', desc: 'Optimus机器人' },
    { name: '直觉外科', ticker: 'ISRG', desc: '手术机器人' },
  ]},
  '自动驾驶': { keywords: ['自动驾驶 FSD 智驾', '无人驾驶 Robotaxi'], filter: /驾驶|FSD|智驾|Robotaxi|激光雷达|域控/, stocks: [
    { name: '特斯拉', ticker: 'TSLA', desc: 'FSD自动驾驶' },
    { name: 'Mobileye', ticker: 'MBLY', desc: '智驾芯片' },
  ]},
  '白酒': { keywords: ['白酒 消费 茅台', '高端白酒 消费升级'], filter: /白酒|茅台|消费|酒/, stocks: [
    { name: '帝亚吉欧', ticker: 'DEO', desc: '全球烈酒龙头' },
  ]},
  '券商': { keywords: ['券商 资本市场 改革', 'A股 成交量 两融'], filter: /券商|投行|资本市场|两融|成交|IPO|注册制/, stocks: [
    { name: '高盛', ticker: 'GS', desc: '全球投行龙头' },
    { name: '摩根士丹利', ticker: 'MS', desc: '投行/财富管理' },
    { name: '嘉信理财', ticker: 'SCHW', desc: '零售券商' },
  ]},
  '银行': { keywords: ['银行 利率 LPR', '银行 净息差 信贷'], filter: /银行|利率|LPR|净息差|信贷|存款/, stocks: [
    { name: '摩根大通', ticker: 'JPM', desc: '全球最大银行' },
    { name: '美国银行', ticker: 'BAC', desc: '美国零售银行' },
  ]},
  '军工': { keywords: ['军工 国防 订单', '军工 地缘 冲突'], filter: /军工|国防|导弹|战斗机|航空发动机|地缘|冲突/, stocks: [
    { name: '洛克希德马丁', ticker: 'LMT', desc: '全球军工龙头' },
    { name: '雷神', ticker: 'RTX', desc: '导弹/防务' },
  ]},
  '光模块': { keywords: ['光模块 CPO 800G', '光通信 AI 数据中心'], filter: /光模块|CPO|光通信|800G|1.6T|数据中心/, stocks: [
    { name: 'Coherent', ticker: 'COHR', desc: '光模块/激光' },
    { name: 'Lumentum', ticker: 'LITE', desc: '光通信' },
  ]},
  '房地产': { keywords: ['房地产 政策 放松', '楼市 房贷 利率'], filter: /房地产|楼市|房贷|地产|土地|住房/, stocks: [
    { name: 'Prologis', ticker: 'PLD', desc: '物流地产REITs' },
  ]},
};

// 默认映射
const DEFAULT_US = { keywords: [], stocks: [] };

function parseArgs(argv) {
  const out = { sector: null, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--sector' || a === '-s') out.sector = argv[++i];
    else if (!a.startsWith('-') && !out.sector) out.sector = a;
  }
  return out;
}

function stripHtml(s = '') {
  return s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function truncate(s = '', n = 50) {
  return s.length > n ? s.slice(0, n) + '...' : s;
}

async function fetchEvents(keywords) {
  if (!keywords.length) return [];
  const allEvents = [];
  for (const kw of keywords.slice(0, 2)) {
    try {
      const param = { uid: '', keyword: kw, type: ['cmsArticleWebOld'], pageIndex: 1, pageSize: 5 };
      const url = 'https://search-api-web.eastmoney.com/search/jsonp?cb=&param=' + encodeURIComponent(JSON.stringify(param));
      const res = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; AIStockInsider/1.0)' },
        signal: AbortSignal.timeout(8000),
      });
      if (!res.ok) continue;
      const text = await res.text();
      const m = text.match(/^\((.*)\)$/s);
      const data = JSON.parse(m ? m[1] : text);
      const list = data?.result?.cmsArticleWebOld || [];
      for (const x of list) {
        allEvents.push({
          title: stripHtml(x.title),
          summary: truncate(stripHtml(x.content), 80),
          source: x.mediaName || '',
          time: x.date || '',
          url: x.url || '',
        });
      }
    } catch {}
  }
  // 去重
  const seen = new Set();
  return allEvents.filter(x => {
    const key = x.title.slice(0, 20);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, 5);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.sector) {
    console.error('Usage: node fetch_us_related.js --sector 化工');
    process.exit(args.help ? 0 : 2);
  }

  let mapping = US_MAPPING[args.sector] || DEFAULT_US;
  if (!mapping.stocks.length) {
    for (const [k, v] of Object.entries(US_MAPPING)) {
      if (args.sector.includes(k) || k.includes(args.sector)) {
        mapping = v;
        break;
      }
    }
  }
  const events = await fetchEvents(mapping.keywords);

  // 用 filter 正则过滤掉弱相关事件
  const filterRe = mapping.filter || null;
  const filtered = filterRe
    ? events.filter(e => filterRe.test(e.title + ' ' + (e.summary || '')))
    : events;

  process.stdout.write(JSON.stringify({
    timestamp: new Date().toISOString(),
    sector: args.sector,
    us_stocks: mapping.stocks,
    events: filtered.slice(0, 3),
  }, null, 2) + '\n');
}

main().catch(e => {
  console.error(`Fatal: ${e.stack || e.message}`);
  process.exit(1);
});
