/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * vat-filing-reconcile.js —— 增值税申报与账载开票三方核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**财务每月申报前后**，必须把三个口径的销售额与销项税额对平 ——
 * **账面收入 / 增值税申报表 / 开票系统**。三者对不上就是"账税票不一致"：
 * 轻则申报表填错要更正申报，重则被系统比对出异常、进风险名单。
 * 这是每个月都要做一次、且**完全能算出来对错**的活。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   销项税额 = 销售额 × 适用税率
 *   账税差   = 账面不含税收入 − 申报销售额
 *   票税差   = 开票不含税金额 − 申报销售额
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断税法适用是否正确**：税率由表里给出，工具只做算术与一致性核对。
 */

const CHECKS_GIVEN = [
  '账载收入与申报销售额差额检测',
  '申报销项税额勾稽（申报销售额 × 适用税率）',
  '开票金额与申报销售额差额检测',
  '合计行逐列复核',
  '重复月份检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '差异率超阈值（1%）判定为重大差异',
  '账载销项税额与申报销项税额差额检测',
  '开票税额与申报销项税额差额检测',
  '适用税率超出常见档位（1%/3%/5%/6%/9%/13%）检测',
  '销售额或税额为负检测',
];

const OUT_OF_SCOPE = [
  '判断税率适用、进项抵扣、留抵退税是否正确（那属于税务判断，请咨询税务师）',
  '汇总未开票收入、简易计税与免税项目的分项申报逻辑',
  '生成或校验申报表本身（本工具只核三个口径的数字是否对得上）',
  '读取财务系统或开票系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '月份\t账面不含税收入\t申报销售额\t开票不含税金额\t适用税率\t账面销项税额\t申报销项税额\t开票税额',
  '2026-01\t1200000.00\t1200000.00\t1200000.00\t13%\t156000.00\t156000.00\t156000.00',
  '2026-02\t980000.00\t980000.00\t980000.00\t13%\t127400.00\t127400.00\t127400.00',
  '2026-03\t1350000.00\t1350000.00\t1350000.00\t13%\t175500.00\t175500.00\t175500.00',
  '合计\t3530000.00\t3530000.00\t3530000.00\t\t458900.00\t458900.00\t458900.00',
].join('\n');

const TOL = 0.01;
const RATE_CAP = 0.01;                       // 差异率 1%
const COMMON_RATES = [0.01, 0.03, 0.05, 0.06, 0.09, 0.13];

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  month: ['月份', '所属期', '期间', '月度'],
  bookSales: ['账面不含税收入', '账面收入', '账载收入', '账面销售额'],
  filedSales: ['申报销售额', '申报收入', '申报表销售额'],
  invoiceSales: ['开票不含税金额', '开票金额', '开票销售额', '发票金额'],
  rate: ['适用税率', '税率'],
  bookTax: ['账面销项税额', '账载销项税额', '账面销项'],
  filedTax: ['申报销项税额', '申报销项'],
  invoiceTax: ['开票税额', '发票税额', '开票销项'],
};

const LABELS = {
  month: '月份', bookSales: '账面不含税收入', filedSales: '申报销售额',
  invoiceSales: '开票不含税金额', rate: '适用税率', bookTax: '账面销项税额',
  filedTax: '申报销项税额', invoiceTax: '开票税额',
};

const REQUIRED = ['month', 'bookSales', 'filedSales', 'invoiceSales', 'rate'];
const SUM_ROLES = ['bookSales', 'filedSales', 'invoiceSales', 'bookTax', 'filedTax', 'invoiceTax'];
const TOTAL_WORDS = /^(合计|总计|小计|本年累计|累计)$/;

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

const round2 = (n) => Math.round(n * 100) / 100;

/** 税率归一化成小数：`13` / `13%` ⇒ 0.13；`0.13` ⇒ 0.13 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return n > 0.5 ? n / 100 : n;
}

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
      if (role === 'month' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.month ? `${String(it.month).trim()} 期` : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkBookVsFiled(it) {
  const a = normNumber(it.bookSales);
  const b = normNumber(it.filedSales);
  if (a === null || b === null || Math.abs(a - b) <= TOL) return null;
  return {
    level: 'P0', category: '账载收入与申报销售额不符', line: it.line,
    message: `${who(it)}：账面不含税收入 ${a.toFixed(2)}，申报销售额 ${b.toFixed(2)}，相差 ${round2(a - b).toFixed(2)}（正数=账面大于申报）。`,
  };
}

function checkFiledTax(it) {
  const sales = normNumber(it.filedSales);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.filedTax);
  if (sales === null || rate === null || stated === null) return null;
  const expect = round2(sales * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '申报销项税额与复算不符', line: it.line,
    message: `${who(it)}：申报销项税额 ${stated.toFixed(2)}，按 申报销售额 ${sales.toFixed(2)} × 税率 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkInvoiceVsFiled(it) {
  const a = normNumber(it.invoiceSales);
  const b = normNumber(it.filedSales);
  if (a === null || b === null || Math.abs(a - b) <= TOL) return null;
  return {
    level: 'P0', category: '开票金额与申报销售额不符', line: it.line,
    message: `${who(it)}：开票不含税金额 ${a.toFixed(2)}，申报销售额 ${b.toFixed(2)}，相差 ${round2(a - b).toFixed(2)}（正数=开票大于申报，通常意味着有未申报的已开票收入）。`,
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) sum += v;
  }
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各期相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.month || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一月份出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 至少有一行是多余的，差额结论会因此不确定。`,
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
    return insufficient('没有收到对照表正文（text）—— 请把「月份 / 账面 / 申报 / 开票」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `对照表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何期间明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkBookVsFiled(it); if (a) findings.push(a);
    const b = checkFiledTax(it); if (b) findings.push(b);
    const c = checkInvoiceVsFiled(it); if (c) findings.push(c);

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

  let bookTotal = 0; let filedTotal = 0; let invTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.bookSales); if (a !== null) bookTotal += a;
    const b = normNumber(it.filedSales); if (b !== null) filedTotal += b;
    const c = normNumber(it.invoiceSales); if (c !== null) invTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'VAT_FILING_RECONCILE',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      periods: t.items.length,
      book_sales_total: round2(bookTotal),
      filed_sales_total: round2(filedTotal),
      invoice_sales_total: round2(invTotal),
      book_minus_filed: round2(bookTotal - filedTotal),
      invoice_minus_filed: round2(invTotal - filedTotal),
      diff_rate_cap: RATE_CAP,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'MISMATCH_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'RECONCILED'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"账面 / 申报 / 开票"三个口径的数字是否对得上，**不判断税法适用是否正确**；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
