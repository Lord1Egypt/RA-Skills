/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * tax-risk-indicator-check.js —— 税务风险指标自查核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月（或每季）纳税申报后、次月结账前**，
 * 财务要把税务风险自查表上的几个指标自己核一遍 —— **税负率**（应纳税额 ÷ 营业收入）、
 * **进销项比**（进项税额 ÷ 销项税额）、**收入与销项、成本与进项是否对得上**、**期末留抵是否合理**。
 * 这些指标异常**往往先于稽查预警出现**：税负率长期明显偏低、进销项比畸高畸低、
 * 收入有而销项对不上，都是"先自查还能补救、被约谈就只剩解释"的那类信号。
 * 表里的数都是自己填的，**完全能算出来对错**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   税负率   = 应纳税额 ÷ 营业收入
 *   进销项比 = 进项税额 ÷ 销项税额
 *   合计行   = 各金额列逐列相加（比率列不参与求和）
 *   收入 ↔ 销项、成本 ↔ 进项：按参考税率推算后比较偏离幅度
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**税负率、进销项比的合理水平：行业、地区、企业结构差异极大，
 *    只对"明显偏离常见参考口径"做**提示**并明确标注是参考，不作任何认定。
 */

const CHECKS_GIVEN = [
  '税负率复算（应纳税额 ÷ 营业收入 = 税负率）',
  '进销项比复算（进项税额 ÷ 销项税额 = 进销项比）',
  '合计行逐列复核',
  '同一期间重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '税负率低于参考下限（1%）提示（参考口径）',
  '进销项比偏离参考区间（0.5~1.5）提示（参考口径）',
  '收入与销项不匹配（按参考销项税率推算，差超 5%）提示',
  '成本与进项不匹配（按参考进项税率推算，差超 5%）提示',
  '留抵税额与进销项矛盾提示',
];

const OUT_OF_SCOPE = [
  '判断税负率、进销项比到底多少算"异常"（行业、地区、企业结构差异极大，请以当地主管机关口径与同行业对比为准）',
  '认定是否存在少计收入、虚抵进项等违法情形（那属于税务稽查判断，请咨询税务师）',
  '处理增值税留抵退税、加计抵减、即征即退等优惠政策的计算',
  '读取电子税务局或财务系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考口径：仅供"明显偏离"时提示，不构成任何认定 */
const BURDEN_FLOOR_REF = 0.01;      // 税负率参考下限 1%
const IO_RATIO_REF = [0.5, 1.5];    // 进销项比参考区间
const OUTPUT_RATE_REF = 0.13;       // 收入推算销项的参考税率 13%
const INPUT_RATE_REF = 0.13;        // 成本推算进项的参考税率 13%
const RATE_DRIFT_REF = 0.05;        // 推算偏差超过 5% 才算"对不上"

const SAMPLE_TEXT = [
  '期间\t营业收入\t应纳税额\t税负率\t进项税额\t销项税额\t进销项比\t营业成本\t期末留抵税额',
  '2026-01\t1000000.00\t39000.00\t3.90%\t91000.00\t130000.00\t0.7000\t700000.00\t0.00',
  '2026-02\t1200000.00\t46800.00\t3.90%\t109200.00\t156000.00\t0.7000\t840000.00\t0.00',
  '2026-03\t900000.00\t35100.00\t3.90%\t81900.00\t117000.00\t0.7000\t630000.00\t0.00',
  '合计\t3100000.00\t120900.00\t\t282100.00\t403000.00\t\t2170000.00\t0.00',
].join('\n');

const TOL = 0.01;          // 金额类容差
const RATE_TOL = 0.0055;   // 比率类容差：允许表里把比率写成百分比/两位小数的舍入

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「进销项比」不能被「进项税」抢走）
  period: ['会计期间', '所属期', '期间', '月份', '季度'],
  revenue: ['营业收入', '销售收入', '主营业务收入', '收入合计'],
  taxPayable: ['应纳税额', '应纳增值税额', '应纳税额合计', '应交税额'],
  burdenRate: ['税负率', '税收负担率', '税负比例'],
  inputVat: ['进项税额', '进项税额合计', '进项税'],
  outputVat: ['销项税额', '销项税额合计', '销项税'],
  ioRatio: ['进销项比', '进销比例', '进销比'],
  cost: ['营业成本', '主营业务成本', '销售成本'],
  creditCarry: ['期末留抵税额', '留抵税额', '期末留抵'],
};

const LABELS = {
  period: '期间', revenue: '营业收入', taxPayable: '应纳税额', burdenRate: '税负率',
  inputVat: '进项税额', outputVat: '销项税额', ioRatio: '进销项比',
  cost: '营业成本', creditCarry: '期末留抵税额',
};

const REQUIRED = ['period', 'revenue', 'taxPayable', 'burdenRate', 'inputVat', 'outputVat', 'ioRatio'];
/* 合计行只复核金额列：比率列（税负率、进销项比）不能相加 */
const SUM_ROLES = ['revenue', 'taxPayable', 'inputVat', 'outputVat', 'cost', 'creditCarry'];
const NEG_ROLES = ['revenue', 'taxPayable', 'inputVat', 'outputVat', 'cost', 'creditCarry'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|全年合计)$/;

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

/** 比率归一化成小数：`3.9%` ⇒ 0.039；`0.039` ⇒ 0.039；`3.9` ⇒ 0.039 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

/** 进销项比这类"可以是 1 以上"的比值：`0.7` ⇒ 0.7；`1.2` ⇒ 1.2；`70%` ⇒ 0.7 */
function ratioValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  return s.indexOf('%') >= 0 ? n / 100 : n;
}

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

const who = (it) => (it && it.period ? `${String(it.period).trim()} 期` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkBurdenRecalc(it) {
  const rev = normNumber(it.revenue);
  const tax = normNumber(it.taxPayable);
  const stated = rateValue(it.burdenRate);
  if (rev === null || tax === null || stated === null) return [];
  if (Math.abs(rev) <= TOL) return [];
  const expect = tax / rev;
  if (Math.abs(expect - stated) <= RATE_TOL) return [];
  return [{
    level: 'P0', category: '税负率与复算不符', line: it.line,
    message: `${who(it)}：应纳税额 ${tax.toFixed(2)} ÷ 营业收入 ${rev.toFixed(2)} = ${(expect * 100).toFixed(2)}%，`
      + `表里填的税负率是 ${(stated * 100).toFixed(2)}%，相差 ${((stated - expect) * 100).toFixed(2)} 个百分点 —— `
      + '税负率就是这两个数算出来的，必须相等。',
  }];
}

function checkIoRatioRecalc(it) {
  const inp = normNumber(it.inputVat);
  const out = normNumber(it.outputVat);
  const stated = ratioValue(it.ioRatio);
  if (inp === null || out === null || stated === null) return [];
  if (Math.abs(out) <= TOL) return [];
  const expect = inp / out;
  if (Math.abs(expect - stated) <= RATE_TOL) return [];
  return [{
    level: 'P0', category: '进销项比与复算不符', line: it.line,
    message: `${who(it)}：进项税额 ${inp.toFixed(2)} ÷ 销项税额 ${out.toFixed(2)} = ${expect.toFixed(4)}，`
      + `表里填的进销项比是 ${stated.toFixed(4)}，相差 ${(stated - expect).toFixed(4)} —— `
      + '进销项比就是这两个数算出来的，必须相等。',
  }];
}

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回、退税或红字建议单独列示，`
        + '负数混在正常期间里会让比率类指标失真。',
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各期相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.period || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一期间出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— `
          + '合计与指标会被重复计算，请确认是不是同一期间填了两遍。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— `
            + '指标算不出来，请不要用默认值替你填。',
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
    return insufficient('没有收到自查表正文（text）—— 请把「期间 / 营业收入 / 应纳税额 / 税负率 / 进项税额 / 销项税额 / 进销项比 / 营业成本」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `自查表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何期间明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkBurdenRecalc(it)) findings.push(f);
    for (const f of checkIoRatioRecalc(it)) findings.push(f);
    for (const f of checkNegatives(it)) findings.push(f);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let revenueTotal = 0; let taxTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.revenue); if (a !== null) revenueTotal += a;
    const b = normNumber(it.taxPayable); if (b !== null) taxTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'TAX_RISK_INDICATOR_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: t.items.length,
      executed_locally: true,
      network_used: false,
      revenue_total: round2(revenueTotal),
      tax_payable_total: round2(taxTotal),
      tolerance: TOL,
      refs: {
        burden_floor: BURDEN_FLOOR_REF,
        io_ratio: IO_RATIO_REF,
        output_rate_ref: OUTPUT_RATE_REF,
        input_rate_ref: INPUT_RATE_REF,
        rate_drift: RATE_DRIFT_REF,
      },
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"税负率 = 应纳税额 ÷ 营业收入""进销项比 = 进项税额 ÷ 销项税额""合计 = 各列之和"这类内部勾稽，'
      + '以及按参考税率推算的偏离提示，**不判断税负率与进销项比多少算异常**（以当地主管机关口径与同行业对比为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
