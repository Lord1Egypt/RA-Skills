/**
 * tax-monthly-selfcheck.js —— 税务月度自查包（free档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "增值税进销项与税负率核对": require('./parts/01.js'),
  "增值税附加税费核对": require('./parts/02.js'),
  "预缴企业所得税核对": require('./parts/03.js'),
};

const BUNDLE_CHECKS = ["增值税进销项与税负率核对", "增值税附加税费核对", "预缴企业所得税核对"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = ["企业所得税纳税调整核对", "税务风险指标自查核对"];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 增值税进销项与税负率核对 ===\n期间\t销售额\t销项税率\t销项税额\t进项税额\t上期留抵税额\t应纳增值税\t期末留抵税额\t税负率\n2026-01\t1000000.00\t13%\t130000.00\t90000.00\t0.00\t40000.00\t0.00\t4.00%\n2026-02\t800000.00\t13%\t104000.00\t150000.00\t0.00\t0.00\t46000.00\t0.00%\n2026-03\t1200000.00\t13%\t156000.00\t100000.00\t46000.00\t10000.00\t0.00\t0.83%\n合计\t3000000.00\t\t390000.00\t340000.00\t46000.00\t50000.00\t46000.00\n\n=== 增值税附加税费核对 ===\n期间\t增值税税额\t城建税率\t城建税\t教育费附加率\t教育费附加\t地方教育附加率\t地方教育附加\t附加合计\n2026-01\t40000.00\t7%\t2800.00\t3%\t1200.00\t2%\t800.00\t4800.00\n2026-02\t0.00\t7%\t0.00\t3%\t0.00\t2%\t0.00\t0.00\n合计\t40000.00\t\t2800.00\t\t1200.00\t\t800.00\t4800.00\n\n=== 预缴企业所得税核对 ===\n所属期\t利润总额\t税率\t应预缴所得税额\t已预缴所得税额\t本期应补(退)税额\t累计应预缴所得税额\t累计已预缴所得税额\n2026-Q1\t1000000.00\t25%\t250000.00\t200000.00\t50000.00\t250000.00\t200000.00\n2026-Q2\t800000.00\t25%\t200000.00\t250000.00\t-50000.00\t450000.00\t450000.00\n2026-Q3\t1200000.00\t25%\t300000.00\t280000.00\t20000.00\t750000.00\t730000.00\n合计\t3000000.00\t\t750000.00\t730000.00\t20000.00";

function splitSections(text) {
  const out = {};
  let cur = null;
  for (const raw of String(text).split(/\r?\n/)) {
    const m = /^===\s*(.+?)\s*===$/.exec(raw.trim());
    if (m) { cur = m[1].trim(); out[cur] = []; continue; }
    if (cur) out[cur].push(raw);
  }
  const res = {};
  for (const k of Object.keys(out)) res[k] = out[k].join('\n').trim();
  return res;
}

function run(payload) {
  const text = payload && typeof payload.text === 'string' ? payload.text : '';

  if (text.trim().length < 5) {
    return { status: 'insufficient_input',
      missing: ['分段正文（每段以 === 检查名 === 开头）'],
      advice: '把要做核对的表按 `=== 检查名 ===` 分段贴进来；材料不足时本工具不给任何结论。' };
  }
  const secs = splitSections(text);
  const findings = [];
  const perCheck = [];
  for (const name of BUNDLE_CHECKS) {
    const body = secs[name];
    const engine = ENGINES[name];
    if (body === undefined) {          // 整段没给 ⇒ 如实标"缺这一段"
      perCheck.push({ check: name, status: 'missing_section', findings: 0 });
      continue;
    }
    const r = engine.run({ text: body });
    if (r.status !== 'success') {
      perCheck.push({ check: name, status: 'insufficient_input', findings: 0,
        missing: (r.missing || []).slice(0, 3) });
      continue;
    }
    const fs = (r.result.findings || []).map((f) => Object.assign({}, f, { check: name }));
    perCheck.push({ check: name, status: 'ok', findings: fs.length,
      p0: r.result.summary.p0, p1: r.result.summary.p1, p2: r.result.summary.p2 });
    findings.push.apply(findings, fs);
  }
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const sectionsDone = perCheck.filter((c) => c.status === 'ok').length;
  const result = {
    status: 'success',
    service_type: 'FINANCE_MONTHLY_SELFCHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sections_done: sectionsDone,
      rows: findings.length,
      periods: sectionsDone,
      executed_locally: true,
      network_used: false,
    },
    findings,
    per_check: perCheck,
    summary: {
      rows: findings.length, periods: sectionsDone,
      total: findings.length, p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: '本版本只执行：' + CHECKS_GIVEN.join('、') + '；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核各段表内/表间的算术与勾稽，结论可由第三方用同一份输入复算；不替代鉴证与申报。',
  };

  return { status: 'success', result };
}

module.exports = { run, splitSections, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT };
