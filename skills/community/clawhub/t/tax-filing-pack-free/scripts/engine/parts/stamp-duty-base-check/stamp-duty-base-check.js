/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * stamp-duty-base-check.js —— 印花税计税依据核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每季度申报印花税之前**，财务要把合同台账与申报数对一遍 ——
 * 印花税是**按合同金额（计税依据）× 税目税率**逐份合同算出来的：
 * 漏了合同、用错税目税率、计税依据少填，都是申报期最常见的错，
 * 而且**税务局能从合同台账、发票、资金流三头比对**。这是每季度都要做、且完全能算出来对错的活。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应纳税额 = 计税依据 × 适用税率
 *   计税依据应当 = 合同（应税凭证）所列金额
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某份合同该不该交、该按什么税目：税率以表里给的为准；
 *    内置税目税率表只用于**档位提示**（并明确标注是参考）。
 */

const CHECKS_GIVEN = [
  '税额勾稽（计税依据 × 适用税率 = 已缴税额）',
  '计税依据与合同金额一致性核对',
  '已缴税额为负检测',
  '合计行逐列复核',
  '重复合同编号检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '税目与税率档位是否匹配（参考口径提示）',
  '合同金额为负或为零检测',
  '已缴税额超过按合同金额计算的应纳税额（多缴）检测',
  '签订日期缺失或不可解析检测',
  '未申报检测（合同金额 > 0 而已申报计税依据为 0）',
];

const OUT_OF_SCOPE = [
  '判断某份合同是否属于应税凭证、适用哪个税目（那属于税务判断，请咨询税务师）',
  '处理减免优惠、按季不足 1 元免纳、境外书立应税凭证等特殊情形',
  '核对实收资本与资本公积的营业账簿印花税（需要另给账簿数据）',
  '读取合同管理系统或税务申报系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考税目税率表（印花税法 2022-07-01 起施行；**仅供档位提示，以税法与主管税务机关口径为准**） */
const DUTY_RATES = [
  [/借款|融资租赁/, 0.00005],
  [/买卖|承揽|建设工程|运输|技术/, 0.0003],
  [/租赁|保管|仓储|财产保险/, 0.001],
  [/产权转移|股权转让|不动产/, 0.0005],
  [/营业账簿|实收资本|资本公积/, 0.00025],
  [/证券交易/, 0.001],
];

const SAMPLE_TEXT = [
  '合同编号\t合同类型\t合同金额\t适用税率\t已申报计税依据\t已缴税额\t签订日期',
  'HT-2026-001\t建设工程合同\t3200000.00\t0.03%\t3200000.00\t960.00\t2026-01-15',
  'HT-2026-002\t买卖合同\t1450000.00\t0.03%\t1450000.00\t435.00\t2026-02-08',
  'HT-2026-003\t租赁合同\t600000.00\t0.1%\t600000.00\t600.00\t2026-03-01',
  '合计\t\t5250000.00\t\t5250000.00\t1995.00\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 2e-6;          // 税率比较容忍（万分之一量级）

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  contractNo: ['合同编号', '合同号', '凭证编号', '协议编号'],
  contractType: ['合同类型', '税目', '凭证类型', '合同类别'],
  amount: ['合同金额', '合同金额（元）', '计税金额', '合同总金额'],
  rate: ['适用税率', '税率'],
  declaredBase: ['已申报计税依据', '申报计税依据', '计税依据'],
  paidTax: ['已缴税额', '已缴印花税', '实缴税额', '印花税额'],
  signDate: ['签订日期', '签署日期', '合同日期'],
};

const LABELS = {
  contractNo: '合同编号', contractType: '合同类型', amount: '合同金额', rate: '适用税率',
  declaredBase: '已申报计税依据', paidTax: '已缴税额', signDate: '签订日期',
};

const REQUIRED = ['contractNo', 'contractType', 'amount', 'rate', 'declaredBase', 'paidTax'];
const SUM_ROLES = ['amount', 'declaredBase', 'paidTax'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

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
const round8 = (n) => Math.round(n * 1e8) / 1e8;

/** 税率归一化成小数：`0.03%` ⇒ 0.0003；`0.0003` ⇒ 0.0003；`0.03` ⇒ 0.0003（按百分数看） */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return n >= 0.005 ? n / 100 : n;              // 印花税税率都很小：≥0.005 视为百分数
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
      if (role === 'contractNo' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.contractNo ? String(it.contractNo) : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkTaxIdentity(it) {
  const base = normNumber(it.declaredBase);
  const rate = rateValue(it.rate);
  const stated = normNumber(it.paidTax);
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '税额与复算不符', line: it.line,
    message: `${who(it)}：计税依据 ${base.toFixed(2)} × 税率 ${(rate * 100).toFixed(4)}% 应为 ${expect.toFixed(2)}，表里已缴税额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkBaseVsAmount(it) {
  const amt = normNumber(it.amount);
  const base = normNumber(it.declaredBase);
  if (amt === null || base === null || Math.abs(amt - base) <= TOL) return null;
  return {
    level: 'P0', category: '计税依据与合同金额不符', line: it.line,
    message: `${who(it)}：合同金额 ${amt.toFixed(2)}，申报的计税依据 ${base.toFixed(2)}，相差 ${round2(base - amt).toFixed(2)} —— 除非有明确的不计入依据（如增值税税额单列），否则应当一致。`,
  };
}

function checkNegativeTax(it) {
  const v = normNumber(it.paidTax);
  if (v === null || v >= -TOL) return null;
  return {
    level: 'P0', category: '已缴税额为负', line: it.line,
    message: `${who(it)}的已缴税额是 ${v.toFixed(2)}（负数）—— 退税或更正请单独列示。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.contractNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一合同编号出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— 印花税按份计征，重复会多缴或少缴。`,
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
    return insufficient('没有收到台账正文（text）—— 请把「合同编号 / 合同类型 / 合同金额 / 税率 / 已申报计税依据 / 已缴税额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何合同明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkTaxIdentity(it); if (a) findings.push(a);
    const b = checkBaseVsAmount(it); if (b) findings.push(b);
    const c = checkNegativeTax(it); if (c) findings.push(c);

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

  let amountTotal = 0; let baseTotal = 0; let taxTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.amount); if (a !== null) amountTotal += a;
    const b = normNumber(it.declaredBase); if (b !== null) baseTotal += b;
    const c = normNumber(it.paidTax); if (c !== null) taxTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'STAMP_DUTY_BASE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      contracts: t.items.length,
      amount_total: round2(amountTotal),
      declared_base_total: round2(baseTotal),
      paid_tax_total: round2(taxTotal),
      base_minus_amount: round2(baseTotal - amountTotal),
      reference_rate_table: '印花税法（2022-07-01 起）常见税目税率，仅供档位提示',
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      contracts: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'MISMATCH_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'RECONCILED'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"计税依据 × 税率 = 已缴税额"与依据/金额的一致性，**不判断合同是否应税、适用哪个税目**；'
      + '税额可由第三方用同一份台账复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
