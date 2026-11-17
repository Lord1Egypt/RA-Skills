/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * cit-prepay-check.js —— 预缴企业所得税核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每个季度申报（预缴）之前**，财务要按**利润总额 × 适用税率**
 * 算出**本期应预缴**企业所得税，再和**已经预缴的税额**勾稽，得出**本期应补(退)** 税额。
 * 这张「季度预缴所得税计算表」是申报表的底稿：算错就直接错到申报里去，而且
 * **每一格都能用手算复现** —— 所以对错完全能机械判定。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应预缴所得税额   = 利润总额 × 适用税率
 *   本期应补(退)税额 = 应预缴所得税额 − 已预缴所得税额（正数=应补，负数=应退）
 *   合计行           = 各所属期逐列相加
 *   累计已预缴       ≤ 累计应预缴（超过说明累计多缴，要核）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断税率是否合法、是否该享受优惠**（那要税法与主管税务机关口径）：
 *    只对"明显偏离常见预缴口径"的税率做**提示**，并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '应预缴所得税额复算（利润总额 × 适用税率 = 应预缴）',
  '本期应补(退)税额复算（应预缴 − 已预缴 = 本期应补退）',
  '合计行逐列复核',
  '重复所属期检测',
  '空白与占位符检测',
  '利润总额或税率为负检测',
];

const CHECKS_WITHHELD = [
  '适用税率偏离参考口径（法定 25%、小微 20%/5%、高新 15%）提示',
  '已预缴所得税额为负检测',
  '本期应补(退)与应预缴方向矛盾检测',
  '利润总额为零却有应预缴检测',
  '累计已预缴超过累计应预缴提示',
];

const OUT_OF_SCOPE = [
  '判断适用税率是否合法、是否享受小微企业/高新技术企业优惠及优惠适用条件（请以税法与主管税务机关口径为准）',
  '处理弥补以前年度亏损、纳税调整、境外所得抵免等对计税依据的影响',
  '代企业填写申报表或与电子税务局对接（本工具只核底稿表内的算术与勾稽）',
  '读取财务/报税系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考口径：仅供"明显偏离"时提示，**不是**税率合法性判断 */
const STATUTORY_RATE = 0.25;
const RATE_REFS = [0.25, 0.20, 0.15, 0.05];

const SAMPLE_TEXT = [
  '所属期\t利润总额\t税率\t应预缴所得税额\t已预缴所得税额\t本期应补(退)税额\t累计应预缴所得税额\t累计已预缴所得税额',
  '2026-Q1\t1000000.00\t25%\t250000.00\t200000.00\t50000.00\t250000.00\t200000.00',
  '2026-Q2\t800000.00\t25%\t200000.00\t250000.00\t-50000.00\t450000.00\t450000.00',
  '2026-Q3\t1200000.00\t25%\t300000.00\t280000.00\t20000.00\t750000.00\t730000.00',
  '合计\t3000000.00\t\t750000.00\t730000.00\t20000.00\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**。
  //    「累计应预缴所得税额」里含「应预缴所得税额」、「累计已预缴所得税额」里含「已预缴所得税额」，
  //    所以两个「累计」角色必须排在 prepayDue / prepaid 之前，否则后写的列会被前面的角色抢走
  //    （表头角色映射守卫的实测坑：不报缺列，只是算错）。
  period: ['所属期', '纳税所属期', '税款所属期', '期间', '季度', '月份'],
  cumulativeDue: ['累计应预缴所得税额', '累计应预缴税额', '累计应纳所得税额', '累计应纳税额', '累计应预缴'],
  cumulativePrepaid: ['累计已预缴所得税额', '累计已预缴税额', '累计已缴所得税额', '累计已缴税额', '累计已预缴'],
  profitTotal: ['利润总额', '本期利润总额', '应纳税所得额', '计税利润'],
  taxRate: ['适用税率', '预缴税率', '所得税税率', '税率'],
  prepayDue: ['应预缴所得税额', '应预缴税额', '本期应预缴所得税额', '应预缴'],
  prepaid: ['已预缴所得税额', '已预缴税额', '本期已预缴所得税额', '已预缴', '已缴所得税额'],
  adjust: ['本期应补退税额', '应补退税额', '本期应补', '应补退', '应补税额', '应退税额'],
};

const LABELS = {
  period: '所属期', profitTotal: '利润总额', taxRate: '税率', prepayDue: '应预缴所得税额',
  prepaid: '已预缴所得税额', adjust: '本期应补(退)税额',
  cumulativeDue: '累计应预缴所得税额', cumulativePrepaid: '累计已预缴所得税额',
};

const REQUIRED = ['period', 'profitTotal', 'taxRate', 'prepayDue', 'prepaid', 'adjust'];
const SUM_ROLES = ['profitTotal', 'prepayDue', 'prepaid', 'adjust', 'cumulativeDue', 'cumulativePrepaid'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计|本季合计)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（税率、已预缴额都不猜）。',
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

/** 比率归一化成小数：`25%` ⇒ 0.25；`0.25` ⇒ 0.25；`25` ⇒ 0.25 */
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

const who = (it) => (it && it.period ? `${String(it.period).trim()} 期` : `第 ${it && it.line} 行`);
const pct = (r) => `${(r * 100).toFixed(3)}%`;

/* ================================ 免费档检查项 ================================ */

function checkPrepayDue(it) {
  const profit = normNumber(it.profitTotal);
  const rate = rateValue(it.taxRate);
  const stated = normNumber(it.prepayDue);
  if (profit === null || rate === null || stated === null) return null;
  const expect = round2(profit * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应预缴所得税额复算不符', line: it.line,
    message: `${who(it)}：利润总额 ${profit.toFixed(2)} × 税率 ${pct(rate)} 应为应预缴 ${expect.toFixed(2)}，`
      + `表里应预缴是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkAdjust(it) {
  const due = normNumber(it.prepayDue);
  const prepaid = normNumber(it.prepaid);
  const stated = normNumber(it.adjust);
  if (due === null || prepaid === null || stated === null) return null;
  const expect = round2(due - prepaid);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应补退税额复算不符', line: it.line,
    message: `${who(it)}：应预缴 ${due.toFixed(2)} − 已预缴 ${prepaid.toFixed(2)} = ${expect.toFixed(2)}，`
      + `但表里本期应补(退)是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  };
}

function checkBaseSign(it) {
  const out = [];
  const profit = normNumber(it.profitTotal);
  const rate = rateValue(it.taxRate);
  if (profit !== null && profit < -TOL) {
    out.push({
      level: 'P0', category: '利润总额或税率为负', line: it.line,
      message: `${who(it)}的利润总额是 ${profit.toFixed(2)}（负数）—— 亏损期一般预缴为 0，`
        + '负数请确认是否应填在「利润总额」列（冲回建议单独列示）。',
    });
  }
  if (rate !== null && rate < -RATE_TOL) {
    out.push({
      level: 'P0', category: '利润总额或税率为负', line: it.line,
      message: `${who(it)}的适用税率是 ${pct(rate)}（负数）—— 税率不可能为负，请核对取值。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各所属期相加是 ${sum.toFixed(2)}，`
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
        level: 'P1', category: '同一所属期出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现 —— `
          + '同一所属期会被重复预缴/重复勾稽。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 缺这一格就算不出勾稽，请补齐。`,
        });
      }
    }
  }
  return out;
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到计算表正文（text）—— 请把「所属期 / 利润总额 / 税率 / 应预缴 / 已预缴 / 本期应补退」这张表贴进来（含表头，Tab 分隔最稳）');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `计算表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何所属期明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkPrepayDue(it); if (a) findings.push(a);
    const b = checkAdjust(it); if (b) findings.push(b);
    for (const c of checkBaseSign(it)) findings.push(c);

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

  let dueTotal = 0; let prepaidTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.prepayDue); if (a !== null) dueTotal += a;
    const b = normNumber(it.prepaid); if (b !== null) prepaidTotal += b;
  }

  const result = {
    status: 'success',
    service_type: 'CIT_PREPAY_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      periods: t.items.length,
      prepay_due_total: round2(dueTotal),
      prepaid_total: round2(prepaidTotal),
      statutory_rate: STATUTORY_RATE,
      rate_refs: RATE_REFS,
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
    disclaimer: '只核「利润总额 × 税率 = 应预缴」「应预缴 − 已预缴 = 本期应补(退)」这类表内勾稽，'
      + '**不判断税率合法性、不判断是否该享受小微/高新优惠、不处理纳税调整与亏损弥补**'
      + '（以税法与主管税务机关口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
