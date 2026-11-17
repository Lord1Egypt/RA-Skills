'use strict';

// 西安地区装修参考价目表（摘自本地装修公司真实工程预算样本）
// 单位：万元。半包=基础施工+间接费+管理费(10%)；主材=砖/门/洁具/美缝等；
// 全屋定制单列（经验区间）；合计=半包+主材+全屋定制（不含家具电器）。
const BUDGET_TABLE = [
  { area: 80,  half: [3.4, 4.2], main: [2.6, 3.2], cabinet: [1.5, 2.5], total: [7.5, 9.9] },
  { area: 90,  half: [3.8, 4.8], main: [2.9, 3.6], cabinet: [2.0, 3.0], total: [8.7, 11.4] },
  { area: 100, half: [4.2, 5.2], main: [3.2, 4.0], cabinet: [2.5, 3.5], total: [9.9, 12.7] },
  { area: 120, half: [5.2, 6.4], main: [3.8, 4.8], cabinet: [3.0, 4.0], total: [12.0, 15.2] },
  { area: 150, half: [6.8, 8.4], main: [5.0, 6.5], cabinet: [4.0, 6.0], total: [15.8, 20.9] },
];

// 旧房额外：拆除/铲素灰/拆保温/防水铲除/常需换窗（万元）
const OLD_EXTRA = [0.8, 1.5];

function round1(n) { return Math.round(n * 10) / 10; }

function pickTier(area) {
  if (area <= 0) throw new Error('面积必须大于 0');
  const first = BUDGET_TABLE[0];
  const last = BUDGET_TABLE[BUDGET_TABLE.length - 1];
  if (area <= first.area) return { tier: first, overflow: area < first.area ? 'low' : null };
  if (area >= last.area) return { tier: last, overflow: area > last.area ? 'high' : null };
  let best = first;
  let bestDiff = Math.abs(area - first.area);
  for (const t of BUDGET_TABLE) {
    const d = Math.abs(area - t.area);
    if (d < bestDiff) { best = t; bestDiff = d; }
  }
  return { tier: best, overflow: null };
}

// 按装修档次在档位区间内取子区间
function adjustTier([lo, hi], level) {
  const span = hi - lo;
  if (level === 'economy') return [round1(lo), round1(lo + span * 0.55)];
  if (level === 'quality') return [round1(hi - span * 0.55), round1(hi)];
  return [lo, hi]; // standard
}

function labelLevel(l) {
  return l === 'economy' ? '经济' : l === 'quality' ? '品质' : '标准';
}

function formatWan([lo, hi]) { return lo + '~' + hi + ' 万'; }

function parseQuery(query) {
  const text = String(query || '');
  const areaMatch = text.match(/(\d+(?:\.\d+)?)\s*(?:平米|平方米|平方|㎡|平)/);
  const area = areaMatch ? parseFloat(areaMatch[1]) : null;
  const houseType = /(旧房|老房|二手房|翻新|改造)/.test(text) ? 'old' : 'new';
  let packageType = 'full';
  if (/(半包|自购主材|自己买主材|清包)/.test(text)) packageType = 'half';
  else if (/(全包|整装|大包|包主材)/.test(text)) packageType = 'full';
  let level = 'standard';
  if (/(经济|简装|低端|刚需|省钱)/.test(text)) level = 'economy';
  else if (/(品质|高端|轻奢|豪华|中高端)/.test(text)) level = 'quality';
  return { area, houseType, packageType, level };
}

function calculateDecorationBudget(input) {
  const { area, houseType = 'new', packageType = 'full', level = 'standard' } = input || {};
  if (!area || area <= 0) {
    return { ok: false, error: '请提供建筑面积（例如"100平装修多少钱"）' };
  }
  const { tier, overflow } = pickTier(area);
  const half = adjustTier(tier.half, level);
  const main = adjustTier(tier.main, level);
  const cabinet = adjustTier(tier.cabinet, level);
  const total = adjustTier(tier.total, level);

  const result = {
    ok: true,
    area,
    houseType,
    packageType,
    level,
    halfPackage: { range: half },
    mainMaterial: { range: main },
    customCabinet: { range: cabinet },
    fullPackageTotal: { range: total },
    oldHouseExtra: houseType === 'old' ? { range: OLD_EXTRA } : null,
    note: overflow === 'low'
      ? '面积小于 80㎡，按 80㎡ 档估算，实际可能更低'
      : overflow === 'high'
        ? '面积大于 150㎡，按 150㎡ 档估算，大户型通常需上浮'
        : null,
  };
  return result;
}

function handleQuery(query, context) {
  const parsed = parseQuery(query);
  if (!parsed.area) {
    return '没太看懂面积～请告诉我建筑面积（比如"100平装修多少钱""120平旧房半包"），我帮你估算西安参考价的装修预算区间。';
  }
  const r = calculateDecorationBudget(parsed);
  if (!r.ok) return r.error;

  const lines = [];
  lines.push('【' + r.area + '㎡' + (r.houseType === 'old' ? '旧房' : '新房') + ' · ' + labelLevel(r.level) + '装修 估算】');
  lines.push('');
  lines.push('全包总价区间（含主材+全屋定制，不含家具电器）：约 ' + formatWan(r.fullPackageTotal.range));
  lines.push('半包总价（施工+辅料，主材自购）：约 ' + formatWan(r.halfPackage.range));
  lines.push('');
  lines.push('【钱花在哪 · 分项】');
  lines.push('· 半包（基础施工+间接费+管理费10%）：' + formatWan(r.halfPackage.range));
  lines.push('· 主材（砖/门/洁具/美缝等）：' + formatWan(r.mainMaterial.range));
  lines.push('· 全屋定制（衣柜/鞋柜/橱柜等，变量最大）：' + formatWan(r.customCabinet.range));
  if (r.oldHouseExtra) {
    lines.push('· 旧房额外（拆除/铲素灰/拆保温/换窗等）：约 ' + formatWan(r.oldHouseExtra.range));
  }
  if (r.note) lines.push('⚠️ ' + r.note);
  lines.push('');
  lines.push('【诚实边界】');
  lines.push('· 以上为西安地区参考价，基于本地装修公司真实工程预算提炼，非承诺报价。');
  lines.push('· 其他城市人工/材料差异大，请按当地行情上下浮动 ±15%~30%。');
  lines.push('· 最终以你与施工方签字确认的正式预算单为准。');
  lines.push('');
  lines.push('【避坑提醒】');
  lines.push('· 水电按实决算：前期估价低，完工量上来超 30% 很常见。');
  lines.push('· 主材明细口径：先确认"含不含全屋定制"，避免重复算或漏算。');
  lines.push('· 定制柜漏项：见光板、五金、特殊拉篮常不写进预算，后期全是增项。');
  lines.push('· 旧房拆除费：新房没有，旧房拆改轻松多花大几千。');
  lines.push('· 管理费比例：西安常见 10%，超过要问为什么。');
  lines.push('');
  lines.push('想让我帮你逐项核对自家的报价单合不合理？把预算表发我，我按「装修报价审核」的思路给你过一遍。');
  return lines.join('\n');
}

module.exports = { calculateDecorationBudget, parseQuery, handleQuery, BUDGET_TABLE };
