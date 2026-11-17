// 基于 extra_metric（10 个 0-100 行业百分位字段）计算一条线索的"优秀指标亮点"，
// 供日报（scripts/private-daily-report.js）和列表命令（bin/cli.js 的 list-private-leads/
// list-public-leads）共用。字段的原始数值只做中立格式化，不含"行业领先"这类定性措辞——
// 那部分由调用方（agent）按 tier 自己判断语气，因为同一份数据既会被 outstanding-only 的
// 日报场景使用，也会被可能是 outstanding 也可能是 fallback 的列表场景使用。

export function pickRepresentativeInsiteAccount(lead) {
  const accounts = lead.insite_accounts || [];
  if (accounts.length === 0) return null;
  return accounts.reduce((best, acc) => {
    const bestCount = typeof best?.follower_count === "number" ? best.follower_count : -1;
    const accCount = typeof acc?.follower_count === "number" ? acc.follower_count : -1;
    return accCount > bestCount ? acc : best;
  }, accounts[0]);
}

export function pickRepresentativeOuterShop(lead) {
  const shops = lead.outer_shops || [];
  if (shops.length === 0) return null;
  return shops.reduce((best, shop) => {
    const bestGmv = typeof best?.year_gmv === "number" ? best.year_gmv : -1;
    const gmv = typeof shop?.year_gmv === "number" ? shop.year_gmv : -1;
    return gmv > bestGmv ? shop : best;
  }, shops[0]);
}

// avg_item_price / trade_fan_avg_dgmv 在 leaddatacollector 的 LeadDtoAssembler 源码注释里
// 明确写着"DB 分"，需要 /100 换算成元；year_gmv/month_gmv/fans_dgmv 的注释是"不做单位转换"，
// 即已经是元，不转换。
export function fenToYuan(fen) {
  return fen / 100;
}

export function formatYuan(yuan) {
  if (yuan >= 10000) return `¥${(yuan / 10000).toFixed(2)}万`;
  return `¥${yuan.toFixed(2)}`;
}

export function formatCount(count) {
  if (count >= 10000) return `${(count / 10000).toFixed(2)}万`;
  return String(count);
}

// weight 只用来在一条线索命中多个字段时，挑"最值得写进一句话总结"的前几个，跟优质/达标
// 判定本身无关。后两个字段在当前 DTO 里没有对应的原始聚合数值，rawValue 返回 null，权重也最低。
export const QUALITY_METRIC_FIELDS = [
  {
    key: "fans_dgmv_pct",
    label: "站内粉丝DGMV",
    weight: 30,
    rawValue: (lead) => {
      const v = pickRepresentativeInsiteAccount(lead)?.fans_dgmv;
      return typeof v === "number" ? formatYuan(v) : null;
    },
  },
  {
    key: "trade_fan_avg_dgmv_pct",
    label: "交易粉丝人均DGMV",
    weight: 25,
    rawValue: (lead) => {
      const v = pickRepresentativeInsiteAccount(lead)?.trade_fan_avg_dgmv;
      return typeof v === "number" ? formatYuan(fenToYuan(v)) : null;
    },
  },
  {
    key: "outer_gmv1y_pct",
    label: "近1年站外GMV",
    weight: 25,
    rawValue: (lead) => {
      const v = pickRepresentativeOuterShop(lead)?.year_gmv;
      return typeof v === "number" ? formatYuan(v) : null;
    },
  },
  {
    key: "outer_gmv30d_pct",
    label: "近1个月站外GMV",
    weight: 20,
    rawValue: (lead) => {
      const v = pickRepresentativeOuterShop(lead)?.month_gmv;
      return typeof v === "number" ? formatYuan(v) : null;
    },
  },
  {
    key: "outer_avg_item_price_pct",
    label: "客单价",
    weight: 15,
    rawValue: (lead) => {
      const v = pickRepresentativeOuterShop(lead)?.avg_item_price;
      return typeof v === "number" ? formatYuan(fenToYuan(v)) : null;
    },
  },
  {
    key: "fans_pct",
    label: "站内粉丝数",
    weight: 15,
    rawValue: (lead) => {
      const v = pickRepresentativeInsiteAccount(lead)?.follower_count;
      return typeof v === "number" ? formatCount(v) : null;
    },
  },
  {
    key: "avg_note_ces_pct",
    label: "笔记CES",
    weight: 15,
    rawValue: (lead) => {
      const v = pickRepresentativeInsiteAccount(lead)?.avg_note_ces;
      return typeof v === "number" ? v.toFixed(1) : null;
    },
  },
  {
    key: "total_asset_pct",
    label: "用户资产分",
    weight: 10,
    rawValue: (lead) => {
      const v = pickRepresentativeInsiteAccount(lead)?.total_asset;
      return typeof v === "number" ? String(v) : null;
    },
  },
  { key: "outer_monthly_sales_pct", label: "月销量", weight: 5, rawValue: () => null },
  { key: "note_cnt30d_pct", label: "近30天有效笔记数", weight: 5, rawValue: () => null },
];

const OUTSTANDING_MIN_PCT = 80;
const FALLBACK_MIN_PCT = 40;
const MAX_FACTS = 3;

function collectHits(metric, minPct, maxPct) {
  const hits = [];
  for (const field of QUALITY_METRIC_FIELDS) {
    const pct = metric[field.key];
    if (typeof pct === "number" && pct >= minPct && pct < maxPct) hits.push({ field, pct });
  }
  return hits;
}

function toFacts(lead, hits) {
  return hits
    .sort((a, b) => b.field.weight - a.field.weight || b.pct - a.pct)
    .slice(0, MAX_FACTS)
    .map((h) => {
      const value = h.field.rawValue(lead);
      return value ? `${h.field.label} ${value}` : h.field.label;
    });
}

/**
 * 优先取 extra_metric 里 ≥80 分位的字段（outstanding）；一条都没有时 fallback 到
 * 40~80 分位的字段；两层都没有命中则 tier 为 "none"，facts 为空数组。
 */
export function computeQualityHighlight(lead) {
  const metric = lead?.extra_metric;
  if (!metric) return { tier: "none", facts: [], hitCount: 0, maxPct: 0 };

  const outstanding = collectHits(metric, OUTSTANDING_MIN_PCT, 100.01);
  const hits = outstanding.length > 0 ? outstanding : collectHits(metric, FALLBACK_MIN_PCT, OUTSTANDING_MIN_PCT);
  if (hits.length === 0) return { tier: "none", facts: [], hitCount: 0, maxPct: 0 };

  return {
    tier: outstanding.length > 0 ? "outstanding" : "fallback",
    facts: toFacts(lead, hits),
    hitCount: hits.length,
    maxPct: Math.max(...hits.map((h) => h.pct)),
  };
}
