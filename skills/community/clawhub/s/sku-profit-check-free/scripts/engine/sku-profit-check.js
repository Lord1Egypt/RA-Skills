/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * sku-profit-check.js —— SKU 级利润核算（免费档）
 *
 * 谁在什么时候必须做这件事：**电商卖家 / 财务每月结账时，按 SKU 复算真实毛利**。
 * 平台后台的「毛利」通常只扣了成本和平台佣金，**漏掉头程运费、广告费与退货损失**，
 * 于是「看着赚钱、实际亏」。这张表把这六项都摆在同一行里，每一格都能手算复现：
 *
 *   折算后售价 = 售价 × 汇率                       （售价按原币填，换算成人民币）
 *   真实毛利   = 折算后售价 − 成本 − 头程运费
 *                − 折算后售价 × 平台佣金率
 *                − 广告费 ÷ 销量                     （广告费是本期总额，要摊到单件）
 *                − 折算后售价 × 退货率                （退货损失：退回的不只是货值）
 *   毛利率     = 真实毛利 ÷ 折算后售价               （分子分母同一口径，不能拿人民币毛利除原币售价）
 *
 * ⚠️ 口径（写死在结果里，第三方可用同一份输入复算）：
 *    · `售价` 按**原币**填（如美元），`汇率` = 1 原币兑多少人民币；`成本`/`头程运费`/`广告费` 按**人民币**填。
 *    · 净利润还会受税费、仓储、支付手续费、人工等影响 —— 本表**只核你填进来的六项**，
 *      不替你把没填的成本项补上（那属于会计口径，见 OUT_OF_SCOPE）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（源码里没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加的项见 CHECKS_WITHHELD（本包**不实现**）。
 * 材料不足时**绝不给结论**。
 */

const CHECKS_GIVEN = [
  '真实毛利复算（售价×汇率 − 成本 − 头程运费 − 折算后售价×平台佣金率 − 广告费÷销量 − 折算后售价×退货率）',
  '毛利率复算（真实毛利 ÷ 折算后售价）',
  '合计行逐列复核（广告费、销量）',
  '同一 SKU 编号重复行检测',
  '空白与占位符检测',
  '金额或比率为负检测',
];

const CHECKS_WITHHELD = [
  '亏损 SKU 按亏损金额排序的清单',
  '每条亏损 SKU 的调价建议/停售建议（含目标价）',
  '广告费占比（广告费 ÷ 折算后销售额）诊断',
  '整体月度亏损估算',
  '跨期对比（与上月/上季度的毛利、毛利率对比）',
];

const OUT_OF_SCOPE = [
  '选品建议（这个 SKU 该不该上、该进多少货、该不该砍）',
  '竞品比价与市场价判断（对手卖多少钱、该不该跟价）',
  '接入电商平台 / ERP / 广告后台 API 取数（佣金、广告、退货以你导出的表为准）',
  '替代会计口径（收入确认时点、存货计价、税费、汇兑损益与账务处理）',
];

/** 参考线：仅用于**逐行标注**"这条毛利率明显偏低，值得先看一眼"，不是行业标准，也不替代你的目标毛利率。 */
const LOW_MARGIN_REF = 0.1;

const SAMPLE_TEXT = [
  ['SKU编号', '商品名称', '售价', '成本', '头程运费', '平台佣金率', '广告费', '退货率', '汇率', '销量', '真实毛利', '毛利率'].join('\t'),
  ['SKU-1001', '无线耳机', '39.90', '62.00', '8.50', '15%', '2600.00', '3%', '7.20', '400', '158.57', '55.20%'].join('\t'),
  ['SKU-2001', '折叠收纳箱', '89.00', '42.00', '6.00', '5%', '1800.00', '2%', '1.00', '600', '31.77', '35.70%'].join('\t'),
  ['SKU-1002', '蓝牙音箱', '25.00', '55.00', '9.00', '12%', '1560.00', '2.5%', '7.20', '300', '84.70', '47.06%'].join('\t'),
  // 合计行：只对**可加列**（广告费、销量）复核；售价/成本/头程/比率是单件口径，逐行相加没有意义。
  ['合计', '', '', '', '', '', '5960.00', '', '', '1300', '', ''].join('\t'),
].join('\n');

const TOL = 0.01;                            // 金额容差（分）
const RATE_TOL = 0.0005;                     // 比率容差：0.05 个百分点
const ROUND_BAND = 1.0;                      // 合计差额 ≤ 1.00 元：疑似四舍五入（P2），> 1.00 判 P0
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合 计)$/;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的词前面，否则宽泛词会把整列抢走
  //    （现象是"算错但不报错"）。本表踩过 / 防过的四处：
  //    · 「毛利率」角色必须排在「毛利」之前 —— 否则毛利率那列被当成毛利金额；
  //    · 「头程运费」必须排在「运费」之前 —— 否则头程运费被当成普通运费拿走；
  //    · 「平台佣金率」必须排在「佣金率」之前 —— 否则平台佣金率被更宽泛的词匹配走；
  //    · 「成本单价」这类词不能被「单价」抢走 —— 所以「单价」不做任何角色的别名。
  sku: ['SKU编号', 'SKU号', 'SKU编码', '商品编号', '商品编码', '商品ID', '货号', 'SKU'],
  name: ['商品名称', '产品名称', '商品名', '品名', '商品'],
  price: ['售价', '销售单价', '销售价', '卖价', '前台价'],
  cost: ['成本', '采购成本', '商品成本', '成本单价', '进货成本'],
  headFreight: ['头程运费', '头程费', '头程', '跨境运费', '运费'],
  commissionRate: ['平台佣金率', '佣金率', '平台佣金比例', '佣金比例', '平台扣点率', '扣点率'],
  adCost: ['广告费', '广告费用', '推广费', '广告花费', '投放费用'],
  returnRate: ['退货率', '退款率', '退货比例'],
  fxRate: ['汇率', '结算汇率', '折合汇率', '兑人民币汇率'],
  qty: ['销量', '销售数量', '月销量', '出单量', '数量'],
  grossMargin: ['真实毛利率', '毛利率', '利润率'],
  grossProfit: ['真实毛利', '毛利额', '毛利'],
};

const LABELS = {
  sku: 'SKU编号', name: '商品名称', price: '售价', cost: '成本', headFreight: '头程运费',
  commissionRate: '平台佣金率', adCost: '广告费', returnRate: '退货率', fxRate: '汇率',
  qty: '销量', grossProfit: '真实毛利', grossMargin: '毛利率',
};

const REQUIRED = ['sku', 'name', 'price', 'cost', 'headFreight', 'commissionRate',
  'adCost', 'returnRate', 'fxRate', 'qty'];

/** 合计行逐列复核的列：这张表里**只有这两个是"可加列"**
 *  （售价/成本/头程运费是单件口径，佣金率/退货率/汇率是比率，逐行相加没有意义）。 */
const SUM_ROLES = ['adCost', 'qty'];

/** 负值检测覆盖的列（比率列另按比率解析） */
const NEGATIVE_ROLES = ['price', 'cost', 'headFreight', 'adCost', 'qty', 'grossProfit',
  'commissionRate', 'returnRate', 'fxRate', 'grossMargin'];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|-)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 比率归一化成小数：`15%` ⇒ 0.15；`0.15` ⇒ 0.15；`15` ⇒ 0.15（写成 `%` 最稳） */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const round4 = (n) => Math.round(n * 10000) / 10000;
const pct = (r) => `${(r * 100).toFixed(2)}%`;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    const keyCell = String(row.sku === undefined ? '' : row.sku).trim();
    const nameCell = String(row.name === undefined ? '' : row.name).trim();
    if (TOTAL_WORDS.test(keyCell) || TOTAL_WORDS.test(nameCell)) {
      totals.row = row;
      totals.line = i + 1;
    } else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const s = it && it.sku !== undefined && String(it.sku).trim() !== '' ? String(it.sku).trim() : '';
  const n = it && it.name !== undefined && String(it.name).trim() !== '' ? String(it.name).trim() : '';
  const head = s || `第 ${it && it.line} 行`;
  return n ? `${head}「${n}」` : head;
};

/** 逐行复算：算不出来（缺数 / 销量为 0）返回 null，绝不拿默认值凑一个数出来 */
function computeRow(it) {
  const price = normNumber(it.price);
  const cost = normNumber(it.cost);
  const head = normNumber(it.headFreight);
  const cr = rateValue(it.commissionRate);
  const ad = normNumber(it.adCost);
  const rr = rateValue(it.returnRate);
  const fx = normNumber(it.fxRate);
  const qty = normNumber(it.qty);
  if ([price, cost, head, cr, ad, rr, fx, qty].some((v) => v === null)) return null;
  const revenue = price * fx;                       // 折算后售价（单件，人民币）
  const commission = revenue * cr;
  if (Math.abs(qty) <= TOL) return null;            // 销量为 0：广告费无法摊到单件，复算无从算起
  const adPerUnit = ad / qty;
  const returnLoss = revenue * rr;
  const profit = revenue - cost - head - commission - adPerUnit - returnLoss;
  const margin = Math.abs(revenue) <= TOL ? null : profit / revenue;
  return {
    price, cost, head, cr, ad, rr, fx, qty,
    revenue, commission, adPerUnit, returnLoss, profit, margin,
  };
}

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkGrossProfit(it) {
  const out = [];
  const c = computeRow(it);
  if (!c) return out;
  const stated = normNumber(it.grossProfit);
  if (stated === null) return out;                  // 表里没给「真实毛利」列：只交付复算值，不做比对
  if (Math.abs(stated - c.profit) <= TOL) return out;
  out.push({
    level: 'P0', category: '真实毛利复算不符', line: it.line,
    message: `${who(it)}：按六项逐项复算 —— 售价 ${c.price.toFixed(2)} × 汇率 ${c.fx.toFixed(2)} = ${round2(c.revenue).toFixed(2)}（折算后售价）；`
      + `减成本 ${c.cost.toFixed(2)}、头程运费 ${c.head.toFixed(2)}、`
      + `平台佣金 ${round2(c.revenue).toFixed(2)}×${pct(c.cr)} = ${round2(c.commission).toFixed(2)}、`
      + `广告费 ${c.ad.toFixed(2)}÷销量 ${c.qty.toFixed(0)} = ${round2(c.adPerUnit).toFixed(2)}、`
      + `退货损失 ${round2(c.revenue).toFixed(2)}×${pct(c.rr)} = ${round2(c.returnLoss).toFixed(2)}`
      + ` ⇒ 真实毛利应为 ${round2(c.profit).toFixed(2)}，表里「真实毛利」写的是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - c.profit).toFixed(2)} —— 平台后台的「毛利」常常只扣成本和佣金，`
      + '漏掉头程运费、广告费与退货损失；这里是六项全扣后重算的。',
  });
  return out;
}

function checkGrossMargin(it) {
  const out = [];
  const c = computeRow(it);
  if (!c || c.margin === null) return out;
  const stated = rateValue(it.grossMargin);
  if (stated === null) return out;                  // 表里没给「毛利率」列：只交付复算值，不做比对
  if (Math.abs(stated - c.margin) <= RATE_TOL) return out;
  out.push({
    level: 'P1', category: '毛利率复算不符', line: it.line,
    message: `${who(it)}：真实毛利 ${round2(c.profit).toFixed(2)} ÷ 折算后售价 ${round2(c.revenue).toFixed(2)} `
      + `= ${pct(c.margin)}，表里「毛利率」写的是 ${pct(stated)}，相差 ${((stated - c.margin) * 100).toFixed(2)} 个百分点 —— `
      + '分子分母必须同一口径：毛利是人民币，售价也要先按汇率折算成人民币，'
      + '拿人民币毛利除以原币售价会得到一个偏大的假毛利率。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    sum = round2(sum);
    if (Math.abs(stated - sum) <= TOL) continue;
    const diff = round2(stated - sum);
    const rounding = Math.abs(diff) <= ROUND_BAND;
    out.push({
      level: rounding ? 'P2' : 'P0',
      category: rounding ? '合计行与明细之和不符（疑似舍入）' : '合计行与明细之和不符',
      line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 条明细行逐行相加是 ${sum.toFixed(2)}，`
        + `相差 ${diff.toFixed(2)} —— 合计行必须等于各明细行之和。`
        + (rounding ? '（差额在 1.00 元以内，像是四舍五入造成的，先对回原始台账再定）' : ''),
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const s = it.sku !== undefined ? String(it.sku).trim() : '';
    if (!s) continue;
    if (seen.has(s)) {
      out.push({
        level: 'P1', category: '同一 SKU 编号重复行', line: it.line,
        message: `${who(it)}与第 ${seen.get(s)} 行是同一个 SKU 编号，却列了两行 —— `
          + '广告费、销量与毛利会被重复汇总，等于把同一个 SKU 的亏损（或利润）算两遍；'
          + '如果要按渠道/月份拆开，请分行写清渠道或期间，或另给 SKU 编号。',
      });
    } else seen.set(s, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— `
            + '这一格会静默地不参与任何复算，真实毛利直接算不出来；先把原始数据补上再核。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = (role === 'commissionRate' || role === 'returnRate' || role === 'grossMargin')
      ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = (role === 'commissionRate' || role === 'returnRate' || role === 'grossMargin')
      ? pct(v) : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或比率为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 售价/成本/头程运费/广告费/销量/汇率与各比率都不该为负；`
        + '冲回、佣金返还或红字调整请单独列一行并注明依据，不要用负数混在正常行里。',
    });
  }
  return out;
}

/* ================================ 免费档核心产出 ================================ */
/**
 * 逐 SKU 交付：折算后售价 / 真实毛利 / 毛利率 / 是否低于参考线。
 * ⚠️ 这里**只逐行标注**，不做亏损排序、不给调价建议（那些是完整档的活，见 CHECKS_WITHHELD）。
 */
function buildSkuProfit(items) {
  return items.map((it) => {
    const c = computeRow(it);
    const base = {
      line: it.line,
      sku: it.sku === undefined ? '' : String(it.sku).trim(),
      name: it.name === undefined ? '' : String(it.name).trim(),
      stated_gross_profit: normNumber(it.grossProfit),
      stated_gross_margin: rateValue(it.grossMargin),
    };
    if (!c) {
      return Object.assign(base, {
        computable: false,
        not_computable_reason: Math.abs(normNumber(it.qty) || 0) <= TOL && normNumber(it.qty) !== null
          ? '销量为 0：广告费无法摊到单件'
          : '关键字段缺失或不是数字，复算无从算起',
        price: normNumber(it.price), cost: normNumber(it.cost), head_freight: normNumber(it.headFreight),
        commission_rate: rateValue(it.commissionRate), ad_cost: normNumber(it.adCost),
        return_rate: rateValue(it.returnRate), fx_rate: normNumber(it.fxRate), qty: normNumber(it.qty),
        unit_revenue_cny: null, gross_profit_cny: null, gross_margin: null, margin_band: null,
      });
    }
    const low = c.margin !== null && c.margin < LOW_MARGIN_REF;
    return Object.assign(base, {
      computable: true,
      price: c.price, cost: c.cost, head_freight: c.head,
      commission_rate: c.cr, ad_cost: c.ad, return_rate: c.rr, fx_rate: c.fx, qty: c.qty,
      unit_revenue_cny: round2(c.revenue),
      commission_cny: round2(c.commission),
      ad_per_unit_cny: round2(c.adPerUnit),
      return_loss_cny: round2(c.returnLoss),
      gross_profit_cny: round2(c.profit),
      gross_margin: c.margin === null ? null : round4(c.margin),
      margin_band: c.margin === null ? null : (low ? 'LOW' : 'OK'),
    });
  });
}

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload === null || typeof payload !== 'object' || Array.isArray(payload)) {
    return insufficient(`入参必须是对象（收到的是 ${Array.isArray(payload) ? 'array' : typeof payload}）—— `
      + '正确写法：{"text":"（含表头的 SKU 利润核算表，Tab 分隔最稳）"}');
  }
  const text = typeof payload.text === 'string' ? payload.text
    : (typeof payload.content === 'string' ? payload.content : '');
  if (text.trim().length < 5) {
    return insufficient('没有收到 SKU 利润核算表正文（text）—— 请把「SKU编号 / 商品名称 / 售价 / 成本 / '
      + '头程运费 / 平台佣金率 / 广告费 / 退货率 / 汇率 / 销量」这张表（**含表头**）贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `SKU 利润核算表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何 SKU 明细行');
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkGrossProfit(it));
    findings.push(...checkGrossMargin(it));
    findings.push(...checkNegative(it));
  }
  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const skuProfit = buildSkuProfit(t.items);
  const lowMarginRows = skuProfit.filter((r) => r.margin_band === 'LOW').length;

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'SKU_PROFIT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: CHECKS_WITHHELD,
      rows: t.items.length,
      totals_row: Boolean(t.totals && t.totals.row),
      computable_rows: skuProfit.filter((r) => r.computable).length,
      rows_margin_low: lowMarginRows,
      low_margin_ref: LOW_MARGIN_REF,
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      rounding_band: ROUND_BAND,
      fx_basis: '售价按原币填写，按「汇率」（1 原币 = X 人民币）折算成人民币；成本、头程运费、广告费按人民币填写',
      executed_locally: true,
      network_used: false,
    },
    sku_profit: skuProfit,
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: (p0 > 0 || p1 > 0) ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核**表内可算关系**：「真实毛利 = 售价×汇率 − 成本 − 头程运费 − 折算后售价×平台佣金率 '
      + '− 广告费÷销量 − 折算后售价×退货率」「毛利率 = 真实毛利 ÷ 折算后售价」「合计行 = 各明细行之和」，'
      + '以及重复、空缺、负值；只逐行复算并标注毛利率是否低于参考线，'
      + '**不做**亏损排序、调价/停售建议、广告占比诊断、月度亏损估算与跨期对比（那些是完整档）；'
      + '也不判断税费/仓储/支付手续费等没填进来的成本项（以你的会计口径为准）。'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
  LOW_MARGIN_REF, SAMPLE_TEXT,
};
