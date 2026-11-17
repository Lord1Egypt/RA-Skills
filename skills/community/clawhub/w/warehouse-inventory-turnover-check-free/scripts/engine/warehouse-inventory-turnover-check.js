/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * warehouse-inventory-turnover-check.js —— 仓库周转与呆滞库存核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月存货管理必做**。存货周转天数、呆滞金额、跌价准备三件事
 * 必须相互勾稽 —— 周转天数说明资金占用是否合理，呆滞金额说明有多少货已经转不动，
 * 跌价准备说明这部分呆滞有没有如实计提。**呆滞不清，就同时是跌价准备不足与资金长期占用**，
 * 这两件事都是月结会上要交代的。表里的数字全部能手算复现，所以完全能机械地核。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   周转天数 = 库存金额 ÷ 日均出库金额
 *   呆滞金额 = 超期库存数量 × 单位成本
 *   合计行   = 各明细行逐列相加（数量列、金额列）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**周转天数上限与呆滞比例的政策口径：180 天 / 10% 只是**参考**，
 *    超出只做提示，并明确标注是参考口径，不是准则要求。
 */

const CHECKS_GIVEN = [
  '周转天数复算（库存金额 ÷ 日均出库金额 = 周转天数）',
  '呆滞金额复算（超期库存数量 × 单位成本 = 呆滞金额）',
  '合计行逐列复核',
  '同一物料同一仓库重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '库存周转天数超过参考上限（180 天）提示（参考口径）',
  '呆滞比例超过参考上限（10%）提示（参考口径）',
  '跌价准备超过呆滞金额检测',
  '期末库存为负检测',
  '出库金额为零却有周转天数检测',
];

const OUT_OF_SCOPE = [
  '判断周转天数、呆滞比例与跌价准备的**企业口径与计提政策**（行业与会计政策不同，请以本单位存货政策与准则为准）',
  '复核库存金额的计价方法（先进先出 / 加权平均 / 个别计价）与成本还原过程',
  '重算期初 + 入库 − 出库 = 期末的收发存账（本工具只核表内自洽，不核明细账）',
  '替代存货跌价准备的可变现净值测试与审计程序',
  '读取 ERP / WMS 导出文件（需要你先导出成文本贴进来）',
];

/* 参考上限：仅供"明显超出"时提示，不是准则或税务要求 */
const TURNOVER_REF = 180;        // 天
const SLOW_RATE_REF = 0.10;      // 10%

const SAMPLE_TEXT = [
  '期间\t仓库\t物料编码\t物料名称\t库存数量\t单位成本\t库存金额\t日均出库金额\t周转天数\t超期库存数量\t呆滞比例\t呆滞金额\t期末库存数量\t跌价准备',
  '2026-01\t华东仓\tA1001\t螺纹钢\t1200\t100.00\t120000.00\t2000.00\t60.00\t50\t4.17%\t5000.00\t1150\t2000.00',
  '2026-01\t华南仓\tB2002\t铝板\t800\t250.00\t200000.00\t2500.00\t80.00\t20\t2.50%\t5000.00\t780\t1000.00',
  '2026-02\t华东仓\tA1001\t螺纹钢\t1000\t100.00\t100000.00\t2000.00\t50.00\t40\t4.00%\t4000.00\t960\t1500.00',
  '合计\t\t\t\t3000\t\t420000.00\t6500.00\t\t110\t\t14000.00\t2890\t4500.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  // （「超期库存数量」「期末库存数量」都含有「库存数量」，必须排在 stockQty 前面，否则会被抢走）
  period: ['会计期间', '所属期间', '期间', '月份'],
  warehouse: ['仓库名称', '仓库', '库房'],
  itemCode: ['物料编码', '物料编号', '存货编码', '物料代码', '物料号'],
  itemName: ['物料名称', '存货名称', '品名'],
  overdueQty: ['超期库存数量', '呆滞库存数量', '超期数量', '超期库存'],
  endQty: ['期末库存数量', '期末结存数量', '期末库存'],
  stockQty: ['库存数量', '结存数量', '库存数'],
  unitCost: ['单位成本', '单位成本价', '单价'],
  stockAmount: ['库存金额', '结存金额', '存货金额'],
  dailyOutAmount: ['日均出库金额', '平均日出库金额', '日均出库'],
  turnoverDays: ['库存周转天数', '周转天数'],
  slowRate: ['呆滞比例', '呆滞占比', '呆滞率'],
  slowAmount: ['呆滞金额', '呆滞存货金额'],
  provision: ['存货跌价准备', '跌价准备金额', '跌价准备'],
};

const LABELS = {
  period: '期间', warehouse: '仓库', itemCode: '物料编码', itemName: '物料名称',
  stockQty: '库存数量', unitCost: '单位成本', stockAmount: '库存金额',
  dailyOutAmount: '日均出库金额', turnoverDays: '周转天数', overdueQty: '超期库存数量',
  slowRate: '呆滞比例', slowAmount: '呆滞金额', endQty: '期末库存数量', provision: '跌价准备',
};

const REQUIRED = ['period', 'warehouse', 'itemCode', 'stockQty', 'unitCost', 'stockAmount',
  'dailyOutAmount', 'turnoverDays', 'overdueQty', 'slowAmount'];
const SUM_ROLES = ['stockQty', 'stockAmount', 'dailyOutAmount', 'overdueQty', 'slowAmount',
  'endQty', 'provision'];
const NEG_ROLES = ['stockQty', 'unitCost', 'stockAmount', 'dailyOutAmount', 'overdueQty', 'slowAmount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
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

/** 比率归一化成小数：`10%` ⇒ 0.1；`0.1` ⇒ 0.1；`10` ⇒ 0.1 */
const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

function who(it) {
  const p = it && it.period ? String(it.period).trim() : '';
  const w = it && it.warehouse ? String(it.warehouse).trim() : '';
  const c = it && it.itemCode ? String(it.itemCode).trim() : '';
  const tag = [p, w, c].filter(Boolean).join(' / ');
  return tag ? `${tag}（第 ${it.line} 行）` : `第 ${it && it.line} 行`;
}

/* ================================ 免费档检查项 ================================ */

function checkTurnoverRecalc(it) {
  const amount = normNumber(it.stockAmount);
  const daily = normNumber(it.dailyOutAmount);
  const stated = normNumber(it.turnoverDays);
  if (amount === null || daily === null || stated === null) return null;
  if (Math.abs(daily) <= TOL) return null;   // 分母为零：交给完整档的「出库金额为零却有周转天数」
  const expect = round2(amount / daily);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '周转天数与复算不符', line: it.line,
    message: `${who(it)}：库存金额 ${amount.toFixed(2)} ÷ 日均出库金额 ${daily.toFixed(2)} 应为 ${expect.toFixed(2)} 天，表里周转天数是 ${stated.toFixed(2)} 天，相差 ${round2(stated - expect).toFixed(2)} 天。`,
  };
}

function checkSlowAmountRecalc(it) {
  const qty = normNumber(it.overdueQty);
  const cost = normNumber(it.unitCost);
  const stated = normNumber(it.slowAmount);
  if (qty === null || cost === null || stated === null) return null;
  const expect = round2(qty * cost);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '呆滞金额与复算不符', line: it.line,
    message: `${who(it)}：超期库存数量 ${qty.toFixed(2)} × 单位成本 ${cost.toFixed(2)} 应为 ${expect.toFixed(2)}，表里呆滞金额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: role === 'stockQty' || role === 'stockAmount' ? 'P0' : 'P1',
      category: `${LABELS[role]}为负`, line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回或红字建议单独列示，混在正常行里会被当成正常库存一起汇总。`,
    });
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const code = String(it.itemCode || '').trim();
    if (!code) continue;
    const key = `${String(it.period || '').trim()}|${String(it.warehouse || '').trim()}|${code}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一物料同一仓库重复行', line: it.line,
        message: `${who(it)}：同一期间、同一仓库、同一物料编码「${code}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 库存金额与呆滞金额都会被重复汇总。`,
      });
    } else seen.set(key, it.line);
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到盘点表正文（text）—— 请把「期间 / 仓库 / 物料编码 / 库存数量 / 单位成本 / 库存金额 / 日均出库金额 / 周转天数 / 超期库存数量 / 呆滞金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `盘点表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何物料明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkTurnoverRecalc(it); if (a) findings.push(a);
    const b = checkSlowAmountRecalc(it); if (b) findings.push(b);
    for (const c of checkNegatives(it)) findings.push(c);

  }
  for (const role of SUM_ROLES) {
    for (const x of checkTotalRow(t.totals, t.items, role)) findings.push(x);
  }
  for (const x of checkDuplicates(t.items)) findings.push(x);
  for (const x of checkBlanks(t.items)) findings.push(x);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const periodSet = new Set();
  let stockTotal = 0;
  let slowTotal = 0;
  let provisionTotal = 0;
  for (const it of t.items) {
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periodSet.add(p);
    const s1 = normNumber(it.stockAmount); if (s1 !== null) stockTotal += s1;
    const s2 = normNumber(it.slowAmount); if (s2 !== null) slowTotal += s2;
    const s3 = normNumber(it.provision); if (s3 !== null) provisionTotal += s3;
  }

  const result = {
    status: 'success',
    service_type: 'WAREHOUSE_INVENTORY_TURNOVER_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periodSet.size,
      stock_amount_total: round2(stockTotal),
      slow_amount_total: round2(slowTotal),
      provision_total: round2(provisionTotal),
      turnover_ref_days: TURNOVER_REF,
      slow_rate_ref: SLOW_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periodSet.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"库存金额 ÷ 日均出库金额 = 周转天数""超期库存数量 × 单位成本 = 呆滞金额"这类内部勾稽，'
      + '**不规定周转天数上限与呆滞比例的政策口径**（180 天 / 10% 只是参考）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT,
};
