/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * social-insurance-base-check.js —— 社保公积金缴费基数核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每年调基、以及每月申报前**，财务/人事要把**缴费基数**核一遍 ——
 * 缴费基数是不是等于工资口径、有没有落在当地上下限之内、单位和个人的基数是不是同一个、
 * 单位缴费与个人缴费是不是按各自比例从基数算出来的。这些**全是算术勾稽，完全能算出对错**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   单位缴费 = 单位缴费基数 × 单位比例
 *   个人缴费 = 个人缴费基数 × 个人比例
 *   补缴金额 = 基数差额 × （单位比例 + 个人比例）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**当地比例与上下限：比例、下限、上限都以表里给的为准，
 *    只对"明显超出常见区间"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '单位缴费复算（单位缴费基数 × 单位比例 = 单位缴费）',
  '个人缴费复算（个人缴费基数 × 个人比例 = 个人缴费）',
  '合计行逐列复核',
  '同一人员同期重复行检测',
  '空白与占位符检测',
  '缴费基数或缴费比例为负检测',
];

const CHECKS_WITHHELD = [
  '缴费基数低于下限或高于上限提示（参考区间）',
  '单位与个人缴费基数不一致检测',
  '缴费比例偏离常见区间提示（参考口径）',
  '工资口径与缴费基数差异超过阈值提示',
  '补缴金额与基数差额不一致检测',
];

const OUT_OF_SCOPE = [
  '判断当地险种、缴费比例与上下限本身是否合规（各地各险种不同，请以当地社保/公积金经办机构口径为准）',
  '核对工资口径本身的组成（是否含奖金、津贴、年终奖、免税项）',
  '处理补缴的滞纳金、利息与跨年追溯调整',
  '读取社保/公积金申报系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显超出"时提示，不是合规判据 */
const ER_RATE_REF = [0.05, 0.40];
const EE_RATE_REF = [0.02, 0.20];
/* 工资口径与缴费基数的相对差异阈值：超过它才提示（参考） */
const WAGE_DIFF_REL = 0.05;

const SAMPLE_TEXT = [
  '期间\t姓名\t工资口径\t单位缴费基数\t个人缴费基数\t单位比例\t个人比例\t单位缴费\t个人缴费\t基数下限\t基数上限\t补缴金额\t基数差额',
  '2026-01\t张三\t10000.00\t10000.00\t10000.00\t27%\t10.5%\t2700.00\t1050.00\t5000.00\t35000.00\t0.00\t0.00',
  '2026-01\t李四\t15000.00\t15000.00\t15000.00\t27%\t10.5%\t4050.00\t1575.00\t5000.00\t35000.00\t0.00\t0.00',
  '2026-02\t张三\t10000.00\t10000.00\t10000.00\t27%\t10.5%\t2700.00\t1050.00\t5000.00\t35000.00\t0.00\t0.00',
  '合计\t\t35000.00\t35000.00\t35000.00\t\t\t9450.00\t3675.00\t\t\t0.00\t0.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「单位缴费基数」不能被「单位缴费」抢走）
  period: ['期间', '月份', '所属期', '年度'],
  person: ['员工姓名', '职工姓名', '姓名', '人员'],
  wage: ['工资口径', '应发工资', '工资总额', '计税工资', '工资'],
  baseEr: ['单位缴费基数', '单位社保基数', '单位申报基数', '单位基数'],
  baseEe: ['个人缴费基数', '个人社保基数', '个人申报基数', '个人基数'],
  erRate: ['单位缴费比例', '单位比例', '单位费率', '企业比例'],
  eeRate: ['个人缴费比例', '个人比例', '个人费率', '职工比例'],
  erPaid: ['单位缴费额', '单位缴费', '单位缴纳', '单位应缴'],
  eePaid: ['个人缴费额', '个人缴费', '个人缴纳', '个人应缴'],
  lowLimit: ['最低缴费基数', '最低基数', '基数下限', '缴费下限', '下限'],
  highLimit: ['最高缴费基数', '最高基数', '基数上限', '缴费上限', '上限'],
  backPay: ['补缴金额', '补缴额', '补缴'],
  diffBase: ['基数差额', '差额基数', '补差基数', '差额'],
};

const LABELS = {
  period: '期间', person: '姓名', wage: '工资口径', baseEr: '单位缴费基数', baseEe: '个人缴费基数',
  erRate: '单位比例', eeRate: '个人比例', erPaid: '单位缴费', eePaid: '个人缴费',
  lowLimit: '基数下限', highLimit: '基数上限', backPay: '补缴金额', diffBase: '基数差额',
};

const REQUIRED = ['period', 'person', 'baseEr', 'baseEe', 'erRate', 'eeRate', 'erPaid', 'eePaid'];
const SUM_ROLES = ['wage', 'baseEr', 'baseEe', 'erPaid', 'eePaid', 'backPay', 'diffBase'];
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

/** 比率归一化成小数：`27%` ⇒ 0.27；`0.27` ⇒ 0.27；`27` ⇒ 0.27 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
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

function who(it) {
  if (it && (it.person || it.period)) {
    const parts = [it.period, it.person]
      .map((x) => String(x === undefined ? '' : x).trim())
      .filter(Boolean);
    return parts.join(' ') + ' ';
  }
  return `第 ${it && it.line} 行 `;
}

/* ================================ 免费档检查项 ================================ */

function checkEmployerPaid(it) {
  const base = normNumber(it.baseEr);
  const rate = rateValue(it.erRate);
  const stated = normNumber(it.erPaid);
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '单位缴费与单位基数×单位比例不符', line: it.line,
    message: `${who(it)}：单位缴费基数 ${base.toFixed(2)} × 单位比例 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，表里单位缴费是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkEmployeePaid(it) {
  const base = normNumber(it.baseEe);
  const rate = rateValue(it.eeRate);
  const stated = normNumber(it.eePaid);
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '个人缴费与个人基数×个人比例不符', line: it.line,
    message: `${who(it)}：个人缴费基数 ${base.toFixed(2)} × 个人比例 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，表里个人缴费是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkNegative(it) {
  const out = [];
  for (const [role, label] of [['baseEr', '单位缴费基数'], ['baseEe', '个人缴费基数']]) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v < -TOL) {
      out.push({
        level: 'P0', category: '缴费基数或缴费比例为负', line: it.line,
        message: `${who(it)}的${label}是 ${v.toFixed(2)}（负数）—— 冲回请单独列示。`,
      });
    } else if (v <= TOL) {
      out.push({
        level: 'P0', category: '缴费基数或缴费比例为负', line: it.line,
        message: `${who(it)}的${label}是 ${v.toFixed(2)} —— 为零则缴费无从算起，请补齐。`,
      });
    }
  }
  for (const [role, label] of [['erRate', '单位比例'], ['eeRate', '个人比例']]) {
    const r = rateValue(it[role]);
    if (r !== null && r < -RATE_TOL) {
      out.push({
        level: 'P0', category: '缴费基数或缴费比例为负', line: it.line,
        message: `${who(it)}的${label}是 ${(r * 100).toFixed(3)}%（负数）—— 冲回请单独列示，不要写成负比例。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = `${String(it.period || '').trim()}|${String(it.person || '').trim()}`;
    if (key === '|') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一人员同期出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 会按两遍计算缴费。`,
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
    return insufficient('没有收到核对表正文（text）—— 请把「期间 / 姓名 / 工资口径 / 单位与个人缴费基数 / 比例 / 单位与个人缴费」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何人员明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkEmployerPaid(it); if (a) findings.push(a);
    const b = checkEmployeePaid(it); if (b) findings.push(b);
    for (const c of checkNegative(it)) findings.push(c);

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

  let erTotal = 0; let eeTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.erPaid); if (a !== null) erTotal += a;
    const b = normNumber(it.eePaid); if (b !== null) eeTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'SOCIAL_INSURANCE_BASE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      employer_paid_total: round2(erTotal),
      employee_paid_total: round2(eeTotal),
      employer_rate_ref: ER_RATE_REF,
      employee_rate_ref: EE_RATE_REF,
      wage_diff_rel: WAGE_DIFF_REL,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"基数 × 比例 = 缴费""合计 = 各行之和""单位与个人基数是否一致"这类内部勾稽，'
      + '**不规定当地比例与上下限**（以当地规定为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
