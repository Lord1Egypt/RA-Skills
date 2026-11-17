#!/usr/bin/env node
/**
 * social-insurance-check.js —— 社保公积金核对引擎（确定性、纯 Node 标准库）。
 *
 * 为什么做这个（真实痛点：要写得出「谁、在什么时候、因为什么必须做这件事」）：
 *   **每家有人交社保的公司，每个月都要**拿社保/公积金系统的申报明细核一遍：
 *   逐人的个人合计是不是各项之和、单位合计对不对、应缴合计等不等于两者相加、
 *   公积金合计对不对、有没有同一个人出现两行、有没有人漏填或占位符没替换；
 *   再深一层还要看个人扣款比例（养老 8% / 医疗 2% / 失业 0.5%）、
 *   公积金比例在不在 5%~12%。这些**全是算术** ——
 *   能被算出来证明是错的地方，就不该靠人眼逐字找。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（与其它引擎一致）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *
 * 刻意不做的事：
 *   · 不联网、不调用任何大模型；
 *   · 材料不足时**不给结论**（认不出必需列就返回 insufficient_input，绝不输出「未发现问题」）；
 *   · 不判断"这个人该不该参保""基数该定多少"（那是当地政策与公司制度的事）。
 */
'use strict';

const CHECKS_GIVEN = [
  '逐人个人合计算术（个人养老 + 个人医疗 + 个人失业 = 个人合计）',
  '逐人单位合计算术（单位养老 + 医疗 + 失业 + 工伤 + 生育 = 单位合计）',
  '应缴合计勾稽（个人合计 + 单位合计 = 应缴合计）',
  '公积金合计勾稽（个人公积金 + 单位公积金 = 公积金合计）',
  '重复人员检测（同一人出现两行）',
  '空白与占位符检测（该填没填、模板没替换）',
];

const CHECKS_WITHHELD = [
  '个人扣款比例校验（养老 8% / 医疗 2% / 失业 0.5%，按缴费基数复算）',
  '公积金缴存比例区间校验（个人与单位都应在 5%~12%）',
  '缴费基数上下限校验（需你在入参里给出 baseMin / baseMax，否则本项不执行）',
  '个人与单位缴费基数不一致检测',
];

const OUT_OF_SCOPE = [
  '判断某个人该不该参保、该按什么基数参保（那是当地社保政策与劳动合同的事）',
  '判断当地当期的法定比例、基数上下限是多少（政策会变，本工具只按你给或默认的口径算）',
  '核对社保/公积金系统的申报是否已被受理（那要登录官方系统看）',
  '给出税务、劳动法或审计意见',
  '读取 .xlsx / PDF（需要你先从系统导出、复制成文本贴进来）',
];

/* 标准个人扣款比例（可被入参 rates 覆盖）。医疗各地有小额差异，
   所以比例校验只在「偏离标准且超过容差」时才报，并把差额算出来给人看。 */
const DEFAULT_RATES = { pension: 0.08, medical: 0.02, unemploy: 0.005 };
const FUND_MIN = 0.05;
const FUND_MAX = 0.12;
const AMOUNT_TOLERANCE = 0.01;   // 金额容差（元）—— 分位取整造成的几分钱不报

const SAMPLE_TEXT = [
  '姓名\t缴费基数\t个人养老\t个人医疗\t个人失业\t个人合计\t单位养老\t单位医疗\t单位失业\t单位工伤\t单位生育\t单位合计\t应缴合计\t公积金基数\t个人公积金\t单位公积金\t公积金合计',
  '张三\t10000.00\t800.00\t200.00\t50.00\t1050.00\t1600.00\t950.00\t50.00\t20.00\t80.00\t2700.00\t3750.00\t10000.00\t1200.00\t1200.00\t2400.00',
  '李四\t12000.00\t960.00\t240.00\t60.00\t1260.00\t1920.00\t1140.00\t60.00\t24.00\t96.00\t3240.00\t4500.00\t12000.00\t1440.00\t1440.00\t2880.00',
  '王五\t8000.00\t640.00\t160.00\t40.00\t840.00\t1280.00\t760.00\t40.00\t16.00\t64.00\t2160.00\t3000.00\t8000.00\t960.00\t960.00\t1920.00',
  '赵六\t15000.00\t1200.00\t300.00\t75.00\t1575.00\t2400.00\t1425.00\t75.00\t30.00\t120.00\t4050.00\t5625.00\t15000.00\t1800.00\t1800.00\t3600.00',
  '合计\t45000.00\t3600.00\t900.00\t225.00\t4725.00\t7200.00\t4275.00\t225.00\t90.00\t360.00\t12150.00\t16875.00\t45000.00\t5400.00\t5400.00\t10800.00',
].join('\n');

/* ---------------------------------------------------------------- 解析 */

/** 表头列名 -> 角色。**按下标顺序**匹配，越具体的越靠前
    （否则「个人合计」会被「个人养老」抢走，这是这类表最常见的解析错）。 */
const COLUMN_ROLES = [
  [/姓名|员工姓名|人员姓名|职工/, 'name'],
  [/公积金基数|缴存基数/, 'fundBase'],
  [/缴费基数|社保基数|参保基数|月缴费基数/, 'base'],
  [/个人.*养老|养老.*个人/, 'pPension'],
  [/个人.*医疗|医疗.*个人/, 'pMedical'],
  [/个人.*失业|失业.*个人/, 'pUnemploy'],
  [/个人.*工伤|工伤.*个人/, 'pInjury'],
  [/个人.*生育|生育.*个人/, 'pMaternity'],
  [/个人.*公积金|公积金.*个人/, 'pFund'],
  [/个人.*合计|个人.*小计|个人.*总额/, 'pTotal'],
  [/单位.*养老|养老.*单位/, 'cPension'],
  [/单位.*医疗|医疗.*单位/, 'cMedical'],
  [/单位.*失业|失业.*单位/, 'cUnemploy'],
  [/单位.*工伤|工伤.*单位/, 'cInjury'],
  [/单位.*生育|生育.*单位/, 'cMaternity'],
  [/单位.*公积金|公积金.*单位/, 'cFund'],
  [/单位.*合计|单位.*小计|单位.*总额/, 'cTotal'],
  [/公积金.*合计|合计.*公积金/, 'fundTotal'],
  [/应缴合计|合计应缴|缴费合计|缴费总额|总计|合计总额/, 'grandTotal'],
];

/** 角色 -> 给人看的列名。**结论里绝不能露出内部字段名**（第一版露出了 `pUnemploy`，
    用户根本不知道那是什么列 —— 报告要能直接念给人听）。 */
const ROLE_LABELS = {
  name: '姓名', base: '缴费基数', fundBase: '公积金基数',
  pPension: '个人养老', pMedical: '个人医疗', pUnemploy: '个人失业',
  pInjury: '个人工伤', pMaternity: '个人生育', pFund: '个人公积金', pTotal: '个人合计',
  cPension: '单位养老', cMedical: '单位医疗', cUnemploy: '单位失业',
  cInjury: '单位工伤', cMaternity: '单位生育', cFund: '单位公积金', cTotal: '单位合计',
  fundTotal: '公积金合计', grandTotal: '应缴合计',
};
const labelOf = (role) => ROLE_LABELS[role] || role;

/** 这些表头看着像金额，但不该参与「合计 = 各项之和」的勾稽。 */
const NON_AMOUNT_KWS = /身份证|证件|编号|序号|备注|状态|日期|月份|单位名称|公司|社保号|公积金账号/;

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t');
  if (line.indexOf(',') >= 0) return line.split(',');
  return line.trim().split(/\s{2,}|\s+/);
}

function roleOf(header) {
  const h = String(header || '').replace(/\s/g, '');
  if (!h) return 'skip';
  if (NON_AMOUNT_KWS.test(h)) return 'skip';
  for (const [re, role] of COLUMN_ROLES) if (re.test(h)) return role;
  return 'extra';
}

function normAmount(v) {
  if (v === null || v === undefined) return null;
  let s = String(v).trim();
  if (!s) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  s = s.replace(/[¥￥,\s]/g, '').replace(/元$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  return neg ? -n : n;
}

function isBlank(v) {
  const s = String(v === null || v === undefined ? '' : v).trim();
  if (!s) return true;
  return /^(--+|\?\?+|N\/?A|na|待填|TODO|xxx|\*\*\*?)$/i.test(s);
}

function findHeader(lines) {
  for (let i = 0; i < Math.min(lines.length, 10); i += 1) {
    const cells = splitRow(lines[i]).map((c) => c.trim());
    const roles = cells.map(roleOf);
    const known = roles.filter((r) => r !== 'skip' && r !== 'extra');
    // 至少要认出「姓名」+「个人合计」+「单位合计/应缴合计」，才敢认这是申报明细表头
    const hasName = known.includes('name');
    const hasTotals = ['pTotal', 'cTotal', 'grandTotal'].filter((r) => known.includes(r)).length >= 2;
    if (hasName && hasTotals) return { index: i, cells, roles };
  }
  return null;
}

function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const header = findHeader(lines);
  if (!header) return { error: 'no_header' };

  const people = [];
  const totals = [];
  for (let i = header.index + 1; i < lines.length; i += 1) {
    const raw = lines[i];
    if (!raw || !raw.trim()) continue;
    const cells = splitRow(raw).map((c) => c.trim());
    const rec = { line: i + 1, raw: raw.trim(), cells, byRole: {} };
    header.roles.forEach((role, ci) => {
      if (role === 'skip' || role === 'extra') return;
      rec.byRole[role] = cells[ci] === undefined ? '' : cells[ci];
    });
    const name = String(rec.byRole.name || '').trim();
    if (/^(合计|总计|小计|total)/i.test(name)) totals.push(rec); else people.push(rec);
  }
  return { header, people, totals, cols: header.cells };
}

/* ---------------------------------------------------------------- 检查 */

function finding(level, category, line, message, evidence, advice) {
  return { level, category, line, message, evidence, advice };
}

function sumOf(rec, roles) {
  let sum = 0;
  const parts = [];
  for (const r of roles) {
    const n = normAmount(rec.byRole[r]);
    if (n === null) return null;
    sum += n;
    parts.push(r + '=' + n.toFixed(2));
  }
  return { sum: Math.round(sum * 100) / 100, parts };
}

function checkGroupSum(rec, addends, totalRole, label) {
  const t = normAmount(rec.byRole[totalRole]);
  if (t === null) return null;                     // 没有这一列 / 没填 -> 不认定
  const s = sumOf(rec, addends);
  if (!s) return null;                             // 有项认不出 -> 不认定
  if (Math.abs(s.sum - t) <= AMOUNT_TOLERANCE) return null;
  return finding('P0', label + '不等于各项之和', rec.line,
    rec.byRole.name + ' 的' + label + '是 ' + t.toFixed(2)
      + '，但各项相加是 ' + s.sum.toFixed(2) + '（差 ' + (t - s.sum).toFixed(2) + '）',
    rec.raw, '先确认口径：如果有减免、补缴或滞纳金，请把它们也列成一项再核。');
}

function checkDuplicates(people) {
  const seen = new Map();
  const out = [];
  for (const p of people) {
    const name = String(p.byRole.name || '').trim();
    if (!name) continue;
    if (seen.has(name)) {
      out.push(finding('P0', '同一人出现两行', p.line,
        name + ' 出现了两次（上一次在第 ' + seen.get(name) + ' 行）',
        p.raw, '同一人多行可能是一人多岗或跨月数据混在一起，请先确认是不是重复申报。'));
    } else seen.set(name, p.line);
  }
  return out;
}

function checkBlanks(people) {
  const out = [];
  const roles = Object.keys(people[0] ? people[0].byRole : {})
    .filter((r) => r !== 'name');
  for (const p of people) {
    const name = String(p.byRole.name || '').trim();
    if (!name) {
      out.push(finding('P0', '姓名缺失', p.line, '这一行没有姓名', p.raw,
        '请确认这一行是否有效。'));
      continue;
    }
    for (const r of roles) {
      const v = p.byRole[r];
      if (isBlank(v)) {
        out.push(finding('P1', '该填没填', p.line,
          name + ' 的「' + labelOf(r) + '」是空的或还是占位符（' + (String(v).trim() || '空') + '）',
          p.raw, '社保明细里出现空列，通常是从系统导出时漏选，或模板没替换。'));
      } else if (normAmount(v) === null) {
        out.push(finding('P1', '金额无法解析', p.line,
          name + ' 的「' + labelOf(r) + '」写作「' + String(v).trim() + '」，不是能计算的金额',
          p.raw, '请确认列是否串位，或该列本来就是文字列。'));
      }
    }
  }
  return out;
}

/** 比例校验：某人某项个人扣款 / 缴费基数 应为标准比例。只在**偏离且超容差**时报。 */
/* ---------------------------------------------------------------- 入口 */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['社保/公积金申报明细原文（text）']);

  const t = parseTable(text);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的申报明细（需要认出「姓名」+ 至少两个合计列，例如「个人合计」「单位合计」「应缴合计」）',
      '从社保系统导出后，请连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.people.length) return insufficient(['至少一名参保人的明细行']);

  const rates = Object.assign({}, DEFAULT_RATES, (payload && payload.rates) || {});
  const min = payload ? payload.baseMin : undefined;
  const max = payload ? payload.baseMax : undefined;

  const findings = [];
  const notRun = [];

  for (const p of t.people) {
    const a = checkGroupSum(p, ['pPension', 'pMedical', 'pUnemploy'], 'pTotal', '个人合计');
    if (a) findings.push(a);
    const b = checkGroupSum(p, ['cPension', 'cMedical', 'cUnemploy', 'cInjury', 'cMaternity'], 'cTotal', '单位合计');
    if (b) findings.push(b);
    const c = checkGroupSum(p, ['pTotal', 'cTotal'], 'grandTotal', '应缴合计');
    if (c) findings.push(c);
    const d = checkGroupSum(p, ['pFund', 'cFund'], 'fundTotal', '公积金合计');
    if (d) findings.push(d);


  }
  for (const f of checkDuplicates(t.people)) findings.push(f);
  for (const f of checkBlanks(t.people)) findings.push(f);

  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => x.line - y.line);

  const result = {
    findings,
    summary: {
      people: t.people.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      basis: '逐人把各项相加与合计列比对；比例按缴费基数复算',
    },
    columns: t.cols,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明「算得对」，'
      + '不代表参保资格、基数政策或申报受理状态没问题 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normAmount, checkGroupSum, isBlank, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, DEFAULT_RATES, FUND_MIN, FUND_MAX, ROLE_LABELS, labelOf,
};
