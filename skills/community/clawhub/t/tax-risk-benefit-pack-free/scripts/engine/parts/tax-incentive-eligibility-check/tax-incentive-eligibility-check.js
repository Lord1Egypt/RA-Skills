/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * tax-incentive-eligibility-check.js —— 税收优惠适用条件自查核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每年汇算清缴前（以及每个预缴期享受优惠时）**，
 * 财务 / 税务岗都要把「税收优惠适用条件自查表」核一遍 —— 高新技术企业收入占比、
 * 研发费用占比、小型微利企业三项指标、安置残疾人就业比例、各类扣除限额……
 * **条件不满足却享受了优惠 ⇒ 汇算清缴要补税 + 滞纳金**（严重的还会被认定偷税）。
 * 这张表完全能算出来对错：占比 = 分子 ÷ 分母、限额 = 基数 × 比例上限、
 * 合计行必须等于各明细之和，缺项 / 负值 / 重复行都是硬伤。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**优惠政策口径与阈值：政策口径以**最新规定与主管税务机关口径**为准；
 *    这里只对"明显低于 / 超出常见参考口径"做**提示**，并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '指标占比复算（指标分子 ÷ 指标分母 = 指标占比）',
  '限额复算（限额基数 × 比例上限 = 准予扣除限额）',
  '合计行逐列复核',
  '同一优惠项目重复行检测',
  '空白与占位符检测',
  '金额或数量为负检测',
];

const CHECKS_WITHHELD = [
  '高新收入占比低于 60% 提示（参考口径）',
  '研发费用占比低于参考下限提示（参考口径，按销售收入分档）',
  '小微三项指标（应纳税所得额 / 从业人数 / 资产总额）超限提示（参考口径）',
  '安置比例不足却享受优惠提示（参考口径）',
  '分子大于分母（比例 >100%）异常提示',
];

const OUT_OF_SCOPE = [
  '判断你是否真的符合某项税收优惠的**实体条件**（政策适用以最新规定与主管税务机关口径为准）',
  '代为填报申报表、出具鉴证报告或给出"能不能享受"的法律结论',
  '计算应补税款、滞纳金与罚款金额',
  '读取财务系统 / 电子税务局导出文件（需要你先导出成文本贴进来）',
];

/* ============================ 参考口径（**仅供参考**） ============================
 * 这些常量只用来做"明显不合常理"的**提示**，不是政策判定依据。
 * 政策口径会随年度与地区变化，请以最新规定与主管税务机关口径为准。
 */
const HIGHTECH_RATIO_FLOOR = 0.60;      // 高新技术企业：高新技术产品(服务)收入占同期总收入比例 ≥ 60%
const RD_RATE_REF = [                   // 研发费用占销售收入比例下限（按收入分档的常见口径）
  { maxRevenue: 50000000, floor: 0.05, label: '销售收入 ≤ 5,000 万' },
  { maxRevenue: 200000000, floor: 0.04, label: '5,000 万 < 销售收入 ≤ 2 亿' },
  { maxRevenue: Infinity, floor: 0.03, label: '销售收入 > 2 亿' },
];
const MINI_REF = { taxableIncome: 3000000, employees: 300, assets: 50000000 };  // 小型微利企业三项参考上限
const PLACEMENT_RATE_REF = 0.015;       // 安置残疾人就业比例参考下限（各地口径不同）

const SAMPLE_TEXT = [
  '所属期\t优惠项目\t指标分子\t指标分母\t指标占比\t限额基数\t比例上限\t准予扣除限额\t应纳税所得额\t从业人数\t资产总额\t已享受优惠金额',
  '2026 年度\t高新技术企业收入占比\t68000000.00\t100000000.00\t68%\t\t\t\t\t\t\t',
  '2026 年度\t研发费用占比\t5200000.00\t100000000.00\t5.2%\t\t\t\t\t\t\t',
  '2026 年度\t小型微利企业条件\t\t\t\t\t\t\t2400000.00\t180\t42000000.00\t',
  '2026 年度\t安置残疾人就业优惠\t12\t500\t2.4%\t\t\t\t\t\t\t360000.00',
  '2026 年度\t职工教育经费扣除限额\t\t\t\t8000000.00\t8%\t640000.00\t\t\t\t',
  // 合计行 = 各明细行之和（分子 / 分母是混合口径，不合计；占比与比例上限也不合计）
  '合计\t\t\t\t\t8000000.00\t\t640000.00\t2400000.00\t180\t42000000.00\t360000.00',
].join('\n');

const TOL = 0.01;          // 金额 / 数量容差
const RATE_TOL = 0.0005;   // 比率容差（0.05 个百分点）

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    「比例上限」必须比「指标占比」先判，否则会被「比例」抢走；
  //    「限额基数」必须比「准予扣除限额」先判，否则「基数」会被「限额」抢走。
  period: ['所属期', '期间', '月份', '年度', '纳税期间'],
  item: ['优惠项目', '减免项目', '优惠事项', '优惠名称', '项目名称'],
  numerator: ['指标分子', '分子'],
  denominator: ['指标分母', '分母'],
  capRate: ['比例上限', '上限比例', '扣除比例上限'],
  ratio: ['指标占比', '占比', '比例'],
  base: ['限额基数', '扣除基数', '基数'],
  limit: ['准予扣除限额', '扣除限额', '限额'],
  taxableIncome: ['应纳税所得额', '应纳税所得', '所得额'],
  employees: ['从业人数', '在职职工人数', '职工人数', '人数'],
  assets: ['资产总额', '资产合计', '资产'],
  benefitAmt: ['已享受优惠金额', '享受优惠金额', '已享受金额', '减免金额', '优惠金额'],
};

const LABELS = {
  period: '所属期', item: '优惠项目', numerator: '指标分子', denominator: '指标分母',
  ratio: '指标占比', base: '限额基数', capRate: '比例上限', limit: '准予扣除限额',
  taxableIncome: '应纳税所得额', employees: '从业人数', assets: '资产总额', benefitAmt: '已享受优惠金额',
};

/* 表头级别必需列（缺了就没法核对） */
const REQUIRED_BASE = ['period', 'item'];
const RATIO_COLS = ['numerator', 'denominator', 'ratio'];
const LIMIT_COLS = ['base', 'capRate', 'limit'];
/* 合计行逐列复核的列（占比与比例上限不合计） */
const SUM_ROLES = ['numerator', 'denominator', 'base', 'limit', 'taxableIncome', 'employees', 'assets', 'benefitAmt'];
/* 不允许为负的金额 / 数量列 */
const NEG_ROLES = ['numerator', 'denominator', 'base', 'limit', 'taxableIncome', 'employees', 'assets', 'benefitAmt'];
/* 每一行的必填列；同组"只填了一半"也算缺 */
const ROW_REQUIRED = ['period', 'item'];
const BLANK_GROUPS = [RATIO_COLS, LIMIT_COLS];
const TOTAL_WORDS = /^(合计|总计|小计|共计|全年合计)$/;

/* 优惠项目的关键词识别（完整档 5 项用） */
const RE_HIGHTECH = /高新/;
const RE_RD = /研发/;
const RE_MINI = /小微|小型微利/;
const RE_PLACEMENT = /安置|残疾/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|\?+|\*+)$/i.test(s);
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

/** 比率归一化成小数：`60%` ⇒ 0.6；`0.6` ⇒ 0.6；`60` ⇒ 0.6 */
const rateValue = (raw) => {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
};

const round2 = (n) => Math.round(n * 100) / 100;

const who = (it) => {
  const name = it && !isBlank(it.item) ? String(it.item).trim() : `第 ${it && it.line} 行`;
  return it && !isBlank(it.period) ? `${name}（${String(it.period).trim()}）` : name;
};

/** 行的比例取值：优先用表里写的占比，没有就用 分子 ÷ 分母 复算（完整档 5 项用） */
/** 把比率格式化成百分数文案 */
const pct = (r) => `${(r * 100).toFixed(2)}%`;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  const missingColumns = [];
  if (!raw.length) return { items: [], totals: {}, missingColumns: ['整张表（一行都没有）'] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  for (const r of REQUIRED_BASE) {
    if (roles.indexOf(r) < 0) missingColumns.push(LABELS[r]);
  }
  const hasRatio = RATIO_COLS.every((r) => roles.indexOf(r) >= 0);
  const hasLimit = LIMIT_COLS.every((r) => roles.indexOf(r) >= 0);
  if (!hasRatio && !hasLimit) {
    missingColumns.push('至少一组可复算列（指标分子 / 指标分母 / 指标占比，或 限额基数 / 比例上限 / 准予扣除限额）');
  }
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
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns };
}

/* ================================ 免费档检查项 ================================ */

/** 1) 指标占比复算：指标分子 ÷ 指标分母 = 指标占比 */
function checkRatioRecalc(it) {
  const num = normNumber(it.numerator);
  const den = normNumber(it.denominator);
  const stated = rateValue(it.ratio);
  if (num === null || den === null || stated === null) return null;
  if (Math.abs(den) <= TOL) return null;            // 分母为 0 时比例无定义，不硬算
  const expect = num / den;
  if (Math.abs(expect - stated) <= RATE_TOL) return null;
  return {
    level: 'P0', category: '指标占比复算不符', line: it.line,
    message: `${who(it)}：表里「${LABELS.ratio}」写的是 ${pct(stated)}，但 ${LABELS.numerator} ${num} ÷ ${LABELS.denominator} ${den} = ${pct(expect)}，`
      + `相差 ${round2((stated - expect) * 10000) / 100} 个百分点 —— 占比是算出来的，必须能被复算。`,
  };
}

/** 2) 限额复算：限额基数 × 比例上限 = 准予扣除限额 */
function checkLimitRecalc(it) {
  const base = normNumber(it.base);
  const cap = rateValue(it.capRate);
  const limit = normNumber(it.limit);
  if (base === null || cap === null || limit === null) return null;
  const expect = round2(base * cap);
  if (Math.abs(expect - limit) <= TOL) return null;
  return {
    level: 'P0', category: '准予扣除限额复算不符', line: it.line,
    message: `${who(it)}：${LABELS.base} ${base.toFixed(2)} × ${LABELS.capRate} ${pct(cap)} 应为 ${expect.toFixed(2)}，`
      + `表里「${LABELS.limit}」是 ${limit.toFixed(2)}，相差 ${round2(limit - expect).toFixed(2)}。`,
  };
}

/** 3) 合计行逐列复核 */
function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;                   // 合计行该列留空 ⇒ 不硬套 0
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

/** 4) 同一优惠项目重复行检测（同一所属期 + 同一优惠项目） */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = isBlank(it.period) ? '' : String(it.period).trim();
    const name = isBlank(it.item) ? '' : String(it.item).trim();
    const key = `${p}｜${name}`;
    if (p === '' && name === '') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一优惠项目重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行再次出现 —— 同一优惠项目同一所属期重复列示，汇总时会被重复计算。`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 5) 空白与占位符检测（必填列 + "只填了一半"的组） */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of ROW_REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一行定位不到优惠项目，无法核对。`,
        });
      }
    }
    for (const group of BLANK_GROUPS) {
      const filled = group.filter((r) => !isBlank(it[r]));
      if (filled.length === 0 || filled.length === group.length) continue;
      for (const role of group) {
        if (!isBlank(it[role])) continue;
        const others = group.filter((r) => r !== role).map((r) => LABELS[r]).join(' / ');
        out.push({
          level: 'P0', category: '关键字段缺失或占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符，但同组的「${others}」已经填了 —— 残缺的一组不会被复算，请补齐或整组留空。`,
        });
      }
    }
  }
  return out;
}

/** 6) 金额或数量为负检测 */
function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额或数量为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 这个口径不可能是负数：`
        + '要么录错了，要么把冲回 / 调整数混进了本行，请拆开单列。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 追加 1) 高新收入占比低于 60% 提示 */
/** 追加 2) 研发费用占比低于参考下限提示（按销售收入分档） */
/** 追加 3) 小微三项指标（应纳税所得额 / 从业人数 / 资产总额）超限提示 */
/** 追加 4) 安置比例不足却享受优惠提示 */
/** 追加 5) 分子大于分母（比例 >100%）异常提示 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到自查表正文（text）—— 请把「所属期 / 优惠项目 / 指标分子 / 指标分母 / 指标占比」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `自查表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何优惠项目明细行');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkRatioRecalc(it); if (a) findings.push(a);
    const b = checkLimitRecalc(it); if (b) findings.push(b);
    for (const x of checkNegatives(it)) findings.push(x);

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

  const periodSet = new Set();
  let benefitTotal = 0;
  for (const it of t.items) {
    const p = isBlank(it.period) ? '' : String(it.period).trim();
    if (p) periodSet.add(p);
    const v = normNumber(it.benefitAmt);
    if (v !== null) benefitTotal += v;
  }
  const periods = periodSet.size || t.items.length;

  const result = {
    status: 'success',
    service_type: 'TAX_INCENTIVE_ELIGIBILITY_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"分子 ÷ 分母 = 占比""基数 × 比例上限 = 限额""合计 = 各明细之和"这类**表内可复算关系**，'
      + '以及明显不合常理的取值；**不规定政策口径与阈值**（参考口径已在结论里标注，以最新规定与主管税务机关口径为准）；'
      + `本表「${LABELS.benefitAmt}」合计 ${round2(benefitTotal).toFixed(2)}，不构成应补税款的计算。`,
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, rateValue, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
