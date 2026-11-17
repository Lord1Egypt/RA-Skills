#!/usr/bin/env node
/**
 * installment-rate-check.js —— 分期「名义费率 vs 实际年化」核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**"月费率 0.6%"听起来很便宜，实际年化接近 14%** —— 因为手续费按**初始本金**收，
 * 但本金是**逐月在还**的，真实占用的资金只有一半左右。企业做分期促销、或采购设备分期时，
 * 若只比"名义费率"，很容易把年化 14% 的资金当成 7.2% 用。
 *
 * 本引擎算两套口径，并**逐笔复算**：
 *   ① 名义：总手续费 = 本金 × 名义月费率 × 期数；每期还款 = (本金 + 总手续费) ÷ 期数；名义年化 = 名义月费率 × 12
 *   ② 实际：**用 IRR** —— 求月利率 r 使「−本金 + Σ_{i=1..n} 每期还款 ÷ (1+r)^i = 0」，
 *      再换算年化 = (1+r)^12 − 1
 * IRR 用**二分法固定迭代 200 次**（确定性；同输入永远同结果，第三方可用同一口径复算）。
 *
 * 与已有能力的区别：`overdue-interest-check` 算**逾期利息**、`discount-interest-check` 算**票据贴现**；
 * 本能力算的是**等额本息分期的真实资金成本**（名义 vs 实际年化），口径与用途都不同。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查市场利率、不调用大模型；材料不足不给结论；不给金融建议。
 */
'use strict';

const CHECKS_GIVEN = [
  '名义总手续费勾稽（本金 × 名义月费率 × 期数）',
  '每期还款勾稽（(本金 + 总手续费) ÷ 期数）',
  '名义年化勾稽（名义月费率 × 12）',
  '实际年化（IRR）勾稽 —— 二分法固定迭代 200 次，同输入同结果、可第三方复算',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复方案检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '名义月费率超出 0~3% 检测',
  '期数超出 1~60 检测',
  '实际年化低于名义年化检测（数学上不可能，说明算错）',
  '每期还款为负检测',
  'IRR 不收敛（现金流异常）检测',
];

const OUT_OF_SCOPE = [
  '判断该不该做这笔分期、或哪家资金更划算（那是财务决策）',
  '处理先息后本、气球贷、随借随还等非等额本息结构',
  '处理提前还款违约金与手续费退还',
  '考虑货币时间价值之外的税费、保证金与贴息',
  '给出金融建议；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '方案\t本金\t期数\t名义月费率\t名义总手续费\t每期还款\t名义年化\t实际年化',
  'A方案\t12000.00\t12\t0.6%\t864.00\t1072.00\t7.20%\t13.84%',
  '合计\t12000.00\t12\t\t864.00\t\t\t',
].join('\n');

const TOL = 0.01;
const PCT_TOL = 0.02;          // 年化保留两位小数，容差 0.02 个百分点
const BISECT_ITER = 200;

const ROLES = {
  party: ['方案', '名称', '产品', '渠道'],
  principal: ['本金', '分期本金', '贷款金额'],
  periods: ['期数', '分期数', '月数'],
  rateNominal: ['名义月费率', '月费率', '名义费率'],
  feeTotal: ['名义总手续费', '总手续费', '手续费合计'],
  perPeriod: ['每期还款', '月供', '每期金额'],
  rateAnnualNominal: ['名义年化', '名义年利率'],
  rateAnnualReal: ['实际年化', '实际年利率', 'IRR年化'],
};

const LABELS = {
  party: '方案', principal: '本金', periods: '期数', rateNominal: '名义月费率',
  feeTotal: '名义总手续费', perPeriod: '每期还款',
  rateAnnualNominal: '名义年化', rateAnnualReal: '实际年化',
};

const REQUIRED = ['party', 'principal', 'periods', 'rateNominal', 'feeTotal', 'perPeriod',
  'rateAnnualNominal', 'rateAnnualReal'];
const SUM_ROLES = ['principal', 'periods', 'feeTotal', 'perPeriod'];

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
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库五次踩过的坑）：
  //    「名义月费率」要排在「月费率」之前；「实际年化」要排在「名义年化」之前；
  //    「名义总手续费」要排在「手续费合计」之前。
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 数字：带 % 的按百分数原样返回（0.6% -> 0.6）。 */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 等额本息的净现值：NPV(r) = −本金 + 每期还款 × (1 − (1+r)^−n) / r（r=0 时取极限 = n）。 */
function npv(principal, perPeriod, periods, r) {
  if (r === 0) return -principal + perPeriod * periods;
  const annuity = (1 - Math.pow(1 + r, -periods)) / r;
  return -principal + perPeriod * annuity;
}

/**
 * 用**二分法固定迭代**求月利率（确定性：同输入永远同结果）。
 * 返回 {monthly, annualPct, converged}。
 */
function solveIrr(principal, perPeriod, periods) {
  let lo = 0;
  let hi = 1;                                   // 月利率 100% 的上界足够覆盖极端情况
  let fLo = npv(principal, perPeriod, periods, lo);
  let fHi = npv(principal, perPeriod, periods, hi);
  let guard = 0;
  while (fLo * fHi > 0 && guard < 40) {         // 需要时把上界继续放大
    hi *= 2;
    fHi = npv(principal, perPeriod, periods, hi);
    guard += 1;
  }
  if (fLo * fHi > 0) return { monthly: null, annualPct: null, converged: false };
  for (let i = 0; i < BISECT_ITER; i += 1) {
    const mid = (lo + hi) / 2;
    const fMid = npv(principal, perPeriod, periods, mid);
    if (fLo * fMid <= 0) { hi = mid; fHi = fMid; } else { lo = mid; fLo = fMid; }
  }
  const monthly = (lo + hi) / 2;
  return { monthly, annualPct: round2((Math.pow(1 + monthly, 12) - 1) * 100), converged: true };
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `方案「${it.byRole.party || '(未命名)'}」`;

function checkFeeTotal(it) {
  const p = num(it, 'principal'); const r = num(it, 'rateNominal'); const n = num(it, 'periods');
  const stated = num(it, 'feeTotal');
  if (p === null || r === null || n === null || stated === null) return null;
  const expect = round2(p * r / 100 * n);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '名义总手续费与复算不符', line: it.line,
    message: `${who(it)}的名义总手续费是 ${stated.toFixed(2)}，按 本金 ${p.toFixed(2)} × 月费率 ${r}% × ${n} 期 应为 ${expect.toFixed(2)}。`,
    advice: '手续费按**初始本金**乘期数收，这一点正是"名义便宜、实际贵"的根源。',
  };
}

function checkPerPeriod(it) {
  const p = num(it, 'principal'); const fee = num(it, 'feeTotal'); const n = num(it, 'periods');
  const stated = num(it, 'perPeriod');
  if (p === null || fee === null || n === null || stated === null || n === 0) return null;
  const expect = round2((p + fee) / n);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '每期还款与复算不符', line: it.line,
    message: `${who(it)}的每期还款是 ${stated.toFixed(2)}，按 (本金 ${p.toFixed(2)} + 总手续费 ${fee.toFixed(2)}) ÷ ${n} 期 应为 ${expect.toFixed(2)}。`,
    advice: '等额本息（手续费摊入月供）的口径：每期还款 = (本金 + 总手续费) ÷ 期数。',
  };
}

function checkNominalAnnual(it) {
  const r = num(it, 'rateNominal'); const stated = num(it, 'rateAnnualNominal');
  if (r === null || stated === null) return null;
  const expect = round2(r * 12);
  if (Math.abs(expect - stated) <= PCT_TOL) return null;
  return {
    level: 'P1', category: '名义年化与复算不符', line: it.line,
    message: `${who(it)}的名义年化是 ${stated}%，按 月费率 ${r}% × 12 应为 ${expect}%。`,
    advice: '名义年化 = 月费率 × 12（单利）。',
  };
}

function checkRealAnnual(it) {
  const p = num(it, 'principal'); const a = num(it, 'perPeriod'); const n = num(it, 'periods');
  const stated = num(it, 'rateAnnualReal');
  if (p === null || a === null || n === null || stated === null || p <= 0 || n <= 0) return null;
  const { annualPct, converged } = solveIrr(p, a, n);
  if (!converged) return null;
  if (Math.abs(annualPct - stated) <= PCT_TOL) return null;
  return {
    level: 'P0', category: '实际年化（IRR）与复算不符', line: it.line,
    message: `${who(it)}的实际年化是 ${stated}%，`
      + `按「−${p.toFixed(2)} + 每期 ${a.toFixed(2)} × ${n} 期的年金现值」求月利率并换算年化应为 **${annualPct}%**。`,
    advice: '名义月费率 × 12 只是"看着便宜"的数；**资金是逐月归还的**，真实成本要看 IRR 年化。'
      + '本工具用二分法固定 200 次迭代，同输入结果唯一、可用同口径复算。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '注意：月费率、名义年化、实际年化都是**比率，不能按行相加**（合计行里应为空）。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.party || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一方案出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一方案分不同期数分行是正常的；但若本表按方案汇总，重复行会让本金与手续费一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这条方案就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的分期方案核对表（要能认出「本金」「期数」「名义月费率」「名义总手续费」'
      + '「每期还款」「名义年化」「实际年化」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从分期方案或对账表导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个方案的明细行']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkFeeTotal(it); if (a) findings.push(a);
    const b = checkPerPeriod(it); if (b) findings.push(b);
    const c = checkNominalAnnual(it); if (c) findings.push(c);
    const d = checkRealAnnual(it); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      schemes: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      principal_total: sumOf('principal'),
      fee_total: sumOf('feeTotal'),
      basis: '名义总手续费 = 本金 × 名义月费率 × 期数；每期还款 = (本金 + 总手续费) ÷ 期数；'
        + '名义年化 = 名义月费率 × 12；**实际年化 = IRR 年化**（求月利率 r 使 −本金 + Σ 每期还款÷(1+r)^i = 0，'
        + `再换算 (1+r)^12 − 1；二分法固定迭代 ${BISECT_ITER} 次，结果唯一可复算）。`,
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表这笔分期划算、也不代表方案结构是标准等额本息 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, solveIrr, npv, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, BISECT_ITER,
};
