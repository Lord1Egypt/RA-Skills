/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * rd-capitalization-check.js —— 研发支出资本化与费用化划分核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有研发投入、要区分研究阶段与开发阶段的公司**，
 * 在**每月结账、年度研发费用加计扣除归集与年审提供底稿之前**。
 * 会计要把每个研发项目当期的「本期发生额」拆成「资本化 / 费用化」两列，
 * 再沿无形资产那条线逐期维护「累计资本化 / 累计摊销 / 期末余额」这几列；
 * 审计与税务盯的就是它们能不能**对上、能不能自证**。
 *
 * 核心可算关系（都能手算复现）：
 *   本期发生额       = 资本化金额 + 费用化金额
 *   期末无形资产余额 = 累计资本化金额 − 累计摊销额
 *   直线法每期摊销   = 累计资本化金额 ÷ 摊销月数（完整档按 5% 容差比）
 *   合计行各列       = 明细行逐列相加
 *   资本化 / 费用化 / 本期摊销额均不应为负
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某笔支出该不该资本化、研发阶段怎么划分、摊销年限是否合理（那属于会计判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**带前缀的列必须排在裸词前面**（`累计资本化金额` 必须先于 `资本化金额`，
   `期末无形资产余额` 含 `余额`，别让宽泛的键抢走）。 */
const ROLES = {
  project: ['项目名称', '研发项目', '项目'],
  stage: ['研发阶段', '项目阶段', '阶段'],
  expenseType: ['支出类型', '费用类型', '支出类别'],
  occurred: ['本期发生额', '本期支出额', '发生额'],
  cumCapitalized: ['累计资本化金额', '累计资本化'],
  capitalized: ['本期资本化金额', '资本化金额'],
  expensed: ['本期费用化金额', '费用化金额'],
  amortMonths: ['摊销月数', '摊销期限月数'],
  cumAmort: ['累计摊销额', '累计摊销'],
  currentAmort: ['本期摊销额', '本期摊销金额'],
  netBook: ['期末无形资产余额', '期末账面余额', '无形资产余额'],
};

const LABELS = {
  project: '项目名称', stage: '研发阶段', expenseType: '支出类型', occurred: '本期发生额',
  capitalized: '资本化金额', expensed: '费用化金额', cumCapitalized: '累计资本化金额',
  amortMonths: '摊销月数', cumAmort: '累计摊销额', currentAmort: '本期摊销额',
  netBook: '期末无形资产余额',
};

const REQUIRED = ['occurred', 'capitalized', 'expensed', 'cumCapitalized', 'netBook'];
const SUM_ROLES = ['occurred', 'capitalized', 'expensed', 'cumCapitalized', 'cumAmort', 'currentAmort', 'netBook'];
const RESEARCH_WORDS = ['研究阶段', '研究'];
const DEV_WORDS = ['开发阶段', '开发'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**（形态 B，且必须是 `Boolean(...)` 这一种写法）：
   `strip_free_engine` 按「`const paid` + `Boolean(`」这一行识别并摘掉付费语句；
   写成别的形式（例：数组的 `.some()`）会**留下开关不删** ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成"没删干净"而整包跳过（本轮实测踩到）。
   两个形态（MARKER + 开关）同时出现会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（发生额 / 资本化 / 费用化 / 累计资本化 / 累计摊销 / 本期摊销 / 期末余额）',
  '同一项目同一阶段重复行检测',
  '本期发生额 = 资本化金额 + 费用化金额',
  '期末无形资产余额 = 累计资本化金额 − 累计摊销额',
  '资本化金额或费用化金额为负检测',
  '本期摊销额为负检测',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '研究阶段却有资本化金额检测（研究阶段支出应费用化）',
  '开发阶段但资本化金额为 0 提示（可能该资本化而未资本化）',
  '本期摊销额与直线法（累计资本化 ÷ 摊销月数）偏离超过 5% 提示',
  '资本化金额超过本期发生额检测',
  '期末无形资产余额为负检测',
];

const OUT_OF_SCOPE = [
  '判断研发阶段怎么划分、某笔支出**该不该资本化**（属于会计判断与专业论证，须与审计/技术部门确认）',
  '判断研发费用加计扣除的归集口径与优惠资格（属于税务判断，见同系列「研发费用加计扣除归集核对」）',
  '代替审计程序或出具鉴证意见，也不判断资本化时点是否恰当',
  '读取研发项目管理系统 / 工时系统 / 财务系统的导出文件（需要你先导出成文本贴进来）',
  '判断无形资产的摊销年限是否合理（本工具只核你给的摊销月数与摊销额之间的算术关系）',
];

const SAMPLE_TEXT = [
  '项目名称\t研发阶段\t支出类型\t本期发生额\t资本化金额\t费用化金额\t累计资本化金额\t摊销月数\t累计摊销额\t本期摊销额\t期末无形资产余额',
  '智能检测算法研发\t开发阶段\t人工\t500000.00\t400000.00\t100000.00\t400000.00\t60\t6666.67\t6666.67\t393333.33',
  '新材料配方预研\t研究阶段\t材料\t200000.00\t0.00\t200000.00\t0.00\t0\t0.00\t0.00\t0.00',
  '合计\t\t\t700000.00\t400000.00\t300000.00\t400000.00\t\t6666.67\t6666.67\t393333.33',
].join('\n');

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
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const who = (it) => { const p = String(it.project || '').trim(); return p ? `${p}（${String(it.stage || '').trim() || '未注明阶段'}）` : `第 ${it.line} 行`; };

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
}

/* ================================ 免费档检查项 ================================ */

function checkTotalRow(items, totals) {
  if (!totals.row) return [];
  const out = [];
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      sum += v;
      n += 1;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}`,
        evidence: `合计=${stated}；明细合计=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = [String(it.project || '').trim(), String(it.stage || '').trim()].join('|');
    if (!key.replace(/\|/g, '')) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「项目 + 研发阶段」完全相同 —— 可能重复计入`,
        evidence: `项目=${it.project}；研发阶段=${it.stage}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkOccurredSplit(it) {
  const occ = normNumber(it.occurred);
  const cap = normNumber(it.capitalized);
  const exp = normNumber(it.expensed);
  if (occ === null || cap === null || exp === null) return null;
  const want = round2(cap + exp);
  if (Math.abs(want - occ) > TOL) {
    return {
      line: it.line, level: 'P0', category: '发生额与资本化加费用化不符',
      message: `${who(it)} 本期发生额 ${occ} ≠ 资本化 ${cap} + 费用化 ${exp} = ${want}`,
      evidence: `本期发生额=${occ}；资本化金额=${cap}；费用化金额=${exp}；应为 ${want}`,
    };
  }
  return null;
}

function checkNetBook(it) {
  const cumCap = normNumber(it.cumCapitalized);
  const cumAmort = normNumber(it.cumAmort);
  const net = normNumber(it.netBook);
  if (cumCap === null || net === null) return null;
  const amort = cumAmort === null ? 0 : cumAmort;
  const want = round2(cumCap - amort);
  if (Math.abs(want - net) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末余额与累计资本化/摊销不符',
      message: `${who(it)} 期末无形资产余额 ${net} ≠ 累计资本化 ${cumCap} − 累计摊销 ${amort} = ${want}`,
      evidence: `累计资本化金额=${cumCap}；累计摊销额=${amort}；期末无形资产余额=${net}；应为 ${want}`,
    };
  }
  return null;
}

function checkNegativeSplit(it) {
  const cap = normNumber(it.capitalized);
  const exp = normNumber(it.expensed);
  const capNeg = cap !== null && cap < 0;
  const expNeg = exp !== null && exp < 0;
  if (!capNeg && !expNeg) return null;
  return {
    line: it.line, level: 'P0', category: '资本化或费用化金额为负',
    message: `${who(it)} 资本化金额=${cap === null ? '-' : cap}，费用化金额=${exp === null ? '-' : exp}（不应为负）`,
    evidence: `资本化金额=${cap}；费用化金额=${exp}`,
  };
}

function checkNegativeAmort(it) {
  const cur = normNumber(it.currentAmort);
  if (cur === null || cur >= 0) return null;
  return {
    line: it.line, level: 'P0', category: '本期摊销额为负',
    message: `${who(it)} 本期摊销额为 ${cur}（负数）—— 摊销额不应为负`,
    evidence: `本期摊销额=${cur}`,
  };
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}`,
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把研发支出明细表（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkOccurredSplit(it), checkNetBook(it), checkNegativeSplit(it), checkNegativeAmort(it)];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        occurred_total: round2(items.reduce((n, it) => n + (normNumber(it.occurred) || 0), 0)),
        capitalized_total: round2(items.reduce((n, it) => n + (normNumber(it.capitalized) || 0), 0)),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
