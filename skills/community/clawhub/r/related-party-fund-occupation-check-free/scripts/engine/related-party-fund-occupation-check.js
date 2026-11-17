/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * related-party-fund-occupation-check.js —— 关联方资金占用与往来清理核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有控股股东、实际控制人及其关联方（母公司、子公司、联营/合营企业、
 * 同一控制下的兄弟公司等）资金往来的公司**，在**月末/季末结账、编制财务报表附注「关联方往来」、
 * 年度审计与再融资/申报材料准备之前**。会计要把这张台账逐行核到能自证：
 * 每一行的余额滚动对不对、合计行能不能对上、有没有长期挂账、非经营性占用有没有余额、有没有清理计划。
 *
 * 核心可算关系（都能手算复现）：
 *   期末余额 = 期初余额 + 本期增加 − 本期减少
 *   合计行   = 各明细行逐列相加（期初 / 增加 / 减少 / 期末四列）
 *   期末余额 ≥ 0（往来台账的余额不应为负数）
 *   期末余额 ≤ 期初余额 + 本期增加（先加后减，期末不可能大于两者之和）
 *
 * 免费档执行 7 项；完整档再追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**：某笔往来该归「经营性」还是「非经营性」、占用是否构成违规、
 *    清理计划是否可执行（那属于会计、法律与监管判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**（本仓库踩过 6 次的坑）。
   `期初余额` / `期末余额` 都含 `余额`，`本期增加` / `本期减少` 都含 `增加` / `减少`，
   `关联方关系` 里含 `关联方`。若把裸词排前面，更具体的那一列会被**抢走**
   ⇒ 必需列永远认不出来（所有输入都变「材料不足」，`header_map_check` 会拦）。
   `关联方关系` 必须排在 `关联方名称` 前面，否则它会被 `关联方` 抢走。 */
const ROLES = {
  relation: ['关联关系', '关联方关系', '关系类型'],
  name: ['关联方名称', '关联方', '往来单位'],
  nature: ['往来性质', '资金占用性质', '款项性质', '性质'],
  opening: ['期初余额', '期初数', '期初'],
  increase: ['本期增加', '本期新增', '本年增加', '增加'],
  decrease: ['本期减少', '本期归还', '本期收回', '减少'],
  closing: ['期末余额', '期末数', '期末'],
  aging: ['账龄天数', '账龄', '天数'],
  interest: ['计息情况', '是否计息', '计息'],
  plan: ['清理计划', '清收计划', '还款计划', '计划'],
};

const LABELS = {
  relation: '关联关系', name: '关联方名称', nature: '往来性质',
  opening: '期初余额', increase: '本期增加', decrease: '本期减少', closing: '期末余额',
  aging: '账龄天数', interest: '计息情况', plan: '清理计划',
};

const REQUIRED = ['name', 'relation', 'nature', 'opening', 'increase', 'decrease', 'closing', 'aging', 'interest', 'plan'];
const SUM_ROLES = ['opening', 'increase', 'decrease', 'closing'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?|汇总)$/;
const TOL = 0.01;
const LONG_AGING_DAYS = 365;             // 超过一年的往来属长期挂账
const LARGE_OCCUPATION = 10000000;       // 1000 万以上视为大额占用
const NON_OPERATING = '非经营性';
const NO_INTEREST = '不计息';
/* 这两列各有专项检查（计息情况 / 清理计划），通用的空白检测要跳过它们，避免同一格报两条。 */
const DEDICATED_BLANK_ROLES = ['interest', 'plan'];

/* ⚠️ 付费开关**只声明一次**，且必须是「常量 paid 赋值为 Boolean(…)」这一种写法：
   `tools/strip_free_engine.py` 按这一行识别并摘掉所有付费语句；写成别的形式
   （例：数组的 `.some()` 判断）会**留下开关不删** ⇒ 泄漏守卫报「免费引擎里仍留着付费开关」。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成「没删干净」而整包跳过（本仓库实测踩到）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（期初余额 / 本期增加 / 本期减少 / 期末余额）',
  '同一关联方 + 往来性质重复行检测',
  '期末余额 = 期初余额 + 本期增加 − 本期减少（不符报 P0）',
  '期末余额为负检测（报 P0）',
  '期末余额与期初余额符号相反且金额差异较大提示（往来性质可能填错，报 P1）',
  '计息情况空白或占位符检测（资金占用必须说明是否计息，报 P1）',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '往来性质为「非经营性资金占用」且期末余额 > 0 检测（监管重点，应制定清理计划，报 P1）',
  '账龄天数 > 365 天检测（长期未清理，报 P1）',
  '期末余额 > 期初余额 + 本期增加 检测（逻辑不可能，报 P0）',
  '清理计划为空白或占位符检测（报 P2）',
  '计息情况为「不计息」且期末余额超过 1000 万提示（大额无偿占用，报 P2）',
];

const OUT_OF_SCOPE = [
  '判断某笔往来的**实质**是经营性还是非经营性资金占用（属于会计与监管判断，本工具只按你填的「往来性质」核对）',
  '认定资金占用是否构成违规占用、是否触发监管处罚或信息披露义务',
  '代替审计抽凭程序，也不出具审计意见或鉴证结论',
  '核对往来发生额的真伪，或与银行流水 / 明细账逐笔比对',
  '读取 ERP / 财务系统的导出文件（需要你先导出成文本贴进来）',
  '判断清理计划是否可执行、是否需要计提资金占用利息或坏账准备',
];

const SAMPLE_TEXT = [
  '关联方名称\t关联关系\t往来性质\t期初余额\t本期增加\t本期减少\t期末余额\t账龄天数\t计息情况\t清理计划',
  '豫州控股集团有限公司\t母公司\t经营性往来\t2000000.00\t500000.00\t800000.00\t1700000.00\t120\t不计息\t2026Q4 结清',
  '中岳联营企业\t联营企业\t非经营性资金占用\t0.00\t300000.00\t300000.00\t0.00\t0\t计息\t已结清',
  '合计\t\t\t2000000.00\t800000.00\t1100000.00\t1700000.00\t\t\t',
].join('\n');

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把关联方往来台账（**含表头**）贴进来：列名用「关联方名称 / 关联关系 / 往来性质 / 期初余额 / 本期增加 / 本期减少 / 期末余额 / 账龄天数 / 计息情况 / 清理计划」，Tab 分隔最稳；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|暂缺|不适用)$/i.test(s);
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

/** 结论里指代某一行的统一写法：有关联方名称就用名称（带上往来性质），否则退回行号。 */
const who = (it) => {
  const n = String(it.name || '').trim();
  if (!n) return `第 ${it.line} 行`;
  const t = String(it.nature || '').trim();
  return t ? `${n}（${t}）` : n;
};

const cellText = (v) => (v === undefined || String(v).trim() === '' ? '(空)' : String(v).trim());

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
        line: totals.line, level: 'P1', category: '合计行复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但 ${n} 行明细逐行相加是 ${sum}（差 ${round2(stated - sum)}）`,
        evidence: `合计行=${stated}；明细逐行相加=${sum}；明细行数=${n}；差额=${round2(stated - sum)}`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const name = String(it.name || '').trim();
    const nature = String(it.nature || '').trim();
    if (!name || !nature) continue;
    const key = `${name}|${nature}`;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${name}（${nature}）与第 ${seen.get(key)} 行是同一关联方、同一往来性质 —— 可能重复登记`,
        evidence: `关联方名称=${name}；往来性质=${nature}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBalanceEquation(it) {
  const opening = normNumber(it.opening);
  const increase = normNumber(it.increase);
  const decrease = normNumber(it.decrease);
  const closing = normNumber(it.closing);
  if (opening === null || increase === null || decrease === null || closing === null) return null;
  const expected = round2(opening + increase - decrease);
  if (Math.abs(closing - expected) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末余额勾稽不符',
      message: `${who(it)} 期末余额 ${closing} ≠ 期初 ${opening} + 本期增加 ${increase} − 本期减少 ${decrease} = ${expected}（差 ${round2(closing - expected)}）`,
      evidence: `期初余额=${opening}；本期增加=${increase}；本期减少=${decrease}；期末余额=${closing}；应为=${expected}；差额=${round2(closing - expected)}`,
    };
  }
  return null;
}

function checkNegativeClosing(it) {
  const closing = normNumber(it.closing);
  if (closing === null || closing >= -TOL) return null;
  return {
    line: it.line, level: 'P0', category: '期末余额为负',
    message: `${who(it)} 期末余额 ${closing} 为负数 —— 往来台账余额不应为负，先查余额方向或借贷登记`,
    evidence: `期末余额=${closing}`,
  };
}

function checkSignFlip(it) {
  const opening = normNumber(it.opening);
  const closing = normNumber(it.closing);
  if (opening === null || closing === null) return null;
  if (opening === 0 || closing === 0) return null;          // 归零不算方向相反
  if (opening * closing > 0) return null;                   // 同向：正常
  if (Math.abs(closing) < Math.abs(opening)) return null;   // 反向但金额明显缩小：属正常收回/归还
  return {
    line: it.line, level: 'P1', category: '期初期末方向相反',
    message: `${who(it)} 期初余额 ${opening} 与期末余额 ${closing} 符号相反且金额未缩小（|期末|=${Math.abs(closing)} ≥ |期初|=${Math.abs(opening)}）—— 往来性质可能填错`,
    evidence: `期初余额=${opening}；期末余额=${closing}；符号相反；|期末|-|期初|=${round2(Math.abs(closing) - Math.abs(opening))}`,
  };
}

function checkInterestMissing(it, missingColumns) {
  if ((missingColumns || []).indexOf('interest') >= 0) return null;   // 整列缺失已由「列缺失」报出
  if (!isBlank(it.interest)) return null;
  return {
    line: it.line, level: 'P1', category: '计息情况未说明',
    message: `${who(it)} 的「计息情况」是空白或占位符（${cellText(it.interest)}）—— 资金占用必须说明是否计息`,
    evidence: `计息情况=${cellText(it.interest)}`,
  };
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}（其余列照常核对）`,
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (DEDICATED_BLANK_ROLES.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符（${cellText(it[role])}）—— 这一行无法核对`,
          evidence: `${LABELS[role]}=${cellText(it[role])}`,
        });
      }
    }
  }
  return out;
}

/* ======================== 完整档（付费）追加的检查项 ======================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把关联方往来台账（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }
  if (!header.some((h) => roleOf(h))) {
    return insufficient(['认不出表头：第一行必须是列名（关联方名称 / 往来性质 / 期初余额 / 期末余额 等）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [
      checkBalanceEquation(it),
      checkNegativeClosing(it),
      checkSignFlip(it),
      checkInterestMissing(it, missingColumns),
    ];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;
  const colTotals = {};
  for (const role of SUM_ROLES) {
    colTotals[role] = round2(items.reduce((n, it) => n + (normNumber(it[role]) || 0), 0));
  }

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
        opening_total: colTotals.opening,
        increase_total: colTotals.increase,
        decrease_total: colTotals.decrease,
        closing_total: colTotals.closing,
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
