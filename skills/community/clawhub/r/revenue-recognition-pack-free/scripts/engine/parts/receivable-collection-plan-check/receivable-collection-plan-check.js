/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * receivable-collection-plan-check.js —— 应收账款催收计划与回款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月编资金计划之前**，财务要按客户逐户过一遍应收 ——
 * 期初挂账、本期新增、承诺回款、实际回款、核销、期末余额、逾期情况。
 * 这张表是**下个月现金流预测的输入**：账龄错了、承诺回款写虚了、回款率算反了，
 * 资金计划就是错的。它内部全是可手算复现的勾稽关系，完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   期末应收 = 期初应收 + 本期新增 − 本期回款 − 本期核销
 *   回款率   = 实际回款 ÷ 承诺回款（按百分数）
 *   合计行   = 各客户明细逐列相加
 *   同一客户 + 同一期间 只能有一行
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**账龄口径、坏账政策与催收优先级（各企业不同）：只核表内勾稽与算术，
 *    对"明显越过常见界限"的做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '期末应收勾稽复算（期初 + 新增 − 回款 − 核销 = 期末）',
  '回款率复算（实际回款 ÷ 承诺回款）',
  '合计行逐列复核',
  '同一客户同一期间重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '逾期金额超过应收余额检测',
  '回款率低于参考下限（80%）提示（参考口径）',
  '承诺回款超过应收余额检测',
  '账龄天数与逾期天数不匹配（相差超过 30 天）提示（参考口径）',
  '核销金额超过应收余额检测',
];

const OUT_OF_SCOPE = [
  '判断账龄口径、坏账政策与催收优先级（各企业不同，请以本单位制度与合同账期为准）',
  '评价客户的真实偿付能力与信用风险（需要征信、银行流水等表外材料）',
  '计算逾期利息、违约金与诉讼时效',
  '读取 ERP / 财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '客户\t期间\t期初应收\t本期新增应收\t本期回款\t本期核销\t期末应收\t承诺回款\t回款率\t逾期金额\t逾期天数\t账龄天数',
  '甲客户\t2026-01\t100000.00\t50000.00\t40000.00\t0.00\t110000.00\t45000.00\t88.89%\t10000.00\t20\t30',
  '乙客户\t2026-01\t200000.00\t100000.00\t150000.00\t0.00\t150000.00\t150000.00\t100.00%\t30000.00\t45\t60',
  '甲客户\t2026-02\t80000.00\t20000.00\t50000.00\t0.00\t50000.00\t50000.00\t100.00%\t20000.00\t10\t25',
  '合计\t\t380000.00\t170000.00\t240000.00\t0.00\t310000.00\t245000.00\t\t60000.00\t\t',
].join('\n');

const TOL = 0.01;          // 金额容差
const RATE_TOL = 0.02;     // 回款率容差（百分点）

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「回款率」不能被「本期回款」抢走）
  period: ['期间', '月份', '所属期', '账期'],
  customer: ['客户名称', '客户', '往来单位', '商户'],
  closing: ['期末应收', '期末余额', '应收余额'],
  opening: ['期初应收', '期初余额', '上期结余'],
  newBilling: ['本期新增应收', '本期新增', '新增应收'],
  writeOff: ['本期核销', '核销金额', '核销'],
  promised: ['承诺回款', '计划回款', '承诺还款'],
  rate: ['回款率', '回款比例', '回款比率'],
  actual: ['本期回款', '实际回款', '已回款', '回款'],
  overdueAmount: ['逾期金额', '超期金额'],
  overdueDays: ['逾期天数', '超期天数'],
  agingDays: ['账龄天数', '账龄'],
};

const LABELS = {
  period: '期间', customer: '客户', opening: '期初应收', newBilling: '本期新增应收',
  actual: '本期回款', writeOff: '本期核销', closing: '期末应收', promised: '承诺回款',
  rate: '回款率', overdueAmount: '逾期金额', overdueDays: '逾期天数', agingDays: '账龄天数',
};

const REQUIRED = ['customer', 'period', 'opening', 'newBilling', 'actual', 'closing', 'promised'];
// 合计行逐列复核的列（回款率是比率、逾期/账龄是天数，都不逐列相加）
const SUM_ROLES = ['opening', 'newBilling', 'actual', 'writeOff', 'closing', 'promised', 'overdueAmount'];
// 「金额为负检测」覆盖的列
const AMOUNT_ROLES = ['opening', 'newBilling', 'actual', 'writeOff', 'closing', 'promised', 'overdueAmount'];
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

/** 比率归一化成**百分数**：`88.89%` ⇒ 88.89；`0.8889` ⇒ 88.89；`88.89` ⇒ 88.89 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n;
  return Math.abs(n) <= 1 ? n * 100 : n;
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
      if (TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const c = it && it.customer ? String(it.customer).trim() : '';
  const p = it && it.period ? String(it.period).trim() : '';
  const tag = [c, p].filter(Boolean).join(' / ');
  return tag ? `${tag}（第 ${it.line} 行）` : `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

/**
 * 形状约定：**单条**检查函数（`f(it)`）一律返回 `发现对象 | null`；
 * **多条**检查函数（`f(it)` / `f(items)` / `f(totals, items, role)`）一律返回**数组**。
 * 同一函数内不混用（第 236 轮记过的坑：一处返回 null、一处返回数组，调用方就会崩）。
 */
function checkBalance(it) {
  const open = normNumber(it.opening);
  const add = normNumber(it.newBilling);
  const got = normNumber(it.actual);
  const off = isBlank(it.writeOff) ? 0 : normNumber(it.writeOff);
  const end = normNumber(it.closing);
  if (open === null || add === null || got === null || off === null || end === null) return null;
  const expect = round2(open + add - got - off);
  if (Math.abs(expect - end) <= TOL) return null;
  return {
    level: 'P0', category: '期末应收与勾稽复算不符', line: it.line,
    message: `${who(it)}：期初 ${open.toFixed(2)} + 新增 ${add.toFixed(2)} − 回款 ${got.toFixed(2)} − 核销 ${off.toFixed(2)} = ${expect.toFixed(2)}，但表里期末应收是 ${end.toFixed(2)}，相差 ${round2(end - expect).toFixed(2)}。`,
  };
}

function checkCollectionRate(it) {
  const got = normNumber(it.actual);
  const promised = normNumber(it.promised);
  const stated = rateValue(it.rate);
  if (got === null || promised === null || stated === null) return null;
  if (promised <= TOL) return null;              // 承诺为 0 时不做除法（无意义）
  const expect = round2((got / promised) * 100);
  if (Math.abs(expect - stated) <= RATE_TOL) return null;
  return {
    level: 'P0', category: '回款率与复算不符', line: it.line,
    message: `${who(it)}：实际回款 ${got.toFixed(2)} ÷ 承诺回款 ${promised.toFixed(2)} = ${expect.toFixed(2)}%，但表里回款率是 ${stated.toFixed(2)}%，相差 ${round2(stated - expect).toFixed(2)} 个百分点。`,
  };
}

function checkNegativeAmount(it) {
  const out = [];
  for (const role of AMOUNT_ROLES) {
    const v = normNumber(it[role]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P1', category: '金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲销/红字建议单独列示，否则勾稽与回款率都会失真。`,
      });
    }
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
    const key = `${String(it.customer || '').trim()}||${String(it.period || '').trim()}`;
    if (key === '||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一客户同一期间出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 同一客户同一期间的挂账会被重复计算。`,
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
    return insufficient('没有收到回款表正文（text）—— 请把「客户 / 期间 / 期初应收 / 本期新增 / 本期回款 / 本期核销 / 期末应收 / 承诺回款」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `回款表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何客户明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkBalance(it); if (a) findings.push(a);
    const b = checkCollectionRate(it); if (b) findings.push(b);
    for (const x of checkNegativeAmount(it)) findings.push(x);

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

  const totalsOf = (role) => {
    let s = 0;
    for (const it of t.items) {
      const v = normNumber(it[role]);
      if (v !== null) s += v;
    }
    return round2(s);
  };
  const distinct = (role) => {
    const set = new Set();
    for (const it of t.items) {
      const v = String(it[role] === undefined ? '' : it[role]).trim();
      if (v) set.add(v);
    }
    return set.size;
  };

  const result = {
    status: 'success',
    service_type: 'RECEIVABLE_COLLECTION_PLAN_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: distinct('period'),
      customers: distinct('customer'),
      closing_total: totalsOf('closing'),
      actual_total: totalsOf('actual'),
      promised_total: totalsOf('promised'),
      overdue_total: totalsOf('overdueAmount'),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: distinct('period'),
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"期初 + 新增 − 回款 − 核销 = 期末""实际回款 ÷ 承诺回款 = 回款率"这类**表内勾稽**，'
      + '**不规定**账龄口径、坏账政策与催收优先级（以本单位制度与合同账期为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
