/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * share-based-payment-check.js —— 股份支付费用分摊核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有股权激励（限制性股票 / 股票期权 / 员工持股平台份额）的公司**，
 * 在**每月（或每季）确认股份支付费用、以及年度审计提供底稿之前**。
 * 会计要把"授予日公允价值 × 授予数量"在**等待期内分期确认**为费用，并逐期维护
 * "累计已分摊 / 未分摊余额"这几列；审计与券商盯的就是它们能不能**滚动对上**。
 *
 * 核心可算关系（都能手算复现）：
 *   授予总额   = 授予数量 × 授予日公允价值
 *   直线法每期 = 授予总额 ÷ 等待期月数
 *   期末未分摊 = 期初未分摊 − 本期实摊金额
 *   期末未分摊 = 授予总额 − 累计已分摊金额
 *   累计已分摊 ≤ 授予总额（不能超额分摊）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该用哪档公允价值、等待期怎么定、能不能一次确认（那属于会计与评估判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**（本仓库踩过 6 次的坑）。
   `授予日公允价值` 里含 `授予日` —— 若 `grantDate` 排在前面，公允价值那一列会被
   「授予日」抢走，`fairValue` 永远认不出来 ⇒ 所有输入都缺必需列（`header_map_check` 会拦）。 */
const ROLES = {
  plan: ['计划名称', '激励计划', '计划'],
  fairValue: ['授予日公允价值', '每股公允价值', '授予日每股公允价值', '公允价值'],
  grantDate: ['授予日期', '授予日'],
  qty: ['授予数量', '授予份数', '授予股数'],
  vestMonths: ['等待期月数', '归属期月数', '等待期'],
  elapsedMonths: ['已过月数', '已过期间', '累计月数'],
  openBalance: ['期初未分摊余额', '期初未摊销余额', '期初余额'],
  currentShould: ['本期应分摊金额', '本期应摊销金额', '本期应分摊'],
  currentActual: ['本期实摊金额', '本期实摊销金额', '本期摊销金额', '本期实摊'],
  cumAmort: ['累计已分摊金额', '累计已摊销金额', '累计已分摊'],
  closeBalance: ['期末未分摊余额', '期末未摊销余额', '期末余额'],
};

const LABELS = {
  plan: '计划名称', grantDate: '授予日', qty: '授予数量', fairValue: '授予日公允价值',
  vestMonths: '等待期月数', elapsedMonths: '已过月数', openBalance: '期初未分摊余额',
  currentShould: '本期应分摊金额', currentActual: '本期实摊金额', cumAmort: '累计已分摊金额',
  closeBalance: '期末未分摊余额',
};

const REQUIRED = ['qty', 'fairValue', 'vestMonths', 'openBalance', 'currentActual', 'closeBalance'];
const SUM_ROLES = ['qty', 'openBalance', 'currentShould', 'currentActual', 'cumAmort', 'closeBalance'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**（形态 B，且必须是 `Boolean(...)` 这一种写法）：
   `strip_free_engine` 按「`const paid` + `Boolean(`」这一行识别并摘掉付费语句；
   写成别的形式（例：数组的 `.some()`）会**留下开关不删** ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成"没删干净"而整包跳过（本轮实测踩到）。
   两个形态（MARKER + 开关）同时出现会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（明细逐行相加 = 合计）',
  '期末未分摊 = 期初未分摊 − 本期实摊金额',
  '期末未分摊 = 授予数量 × 授予日公允价值 − 累计已分摊金额',
  '本期实摊金额为负检测',
  '同一计划同一期间重复行检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '本期实摊与直线法口径（授予总额 ÷ 等待期月数）偏离超过 5% 提示',
  '累计已分摊超过授予总额（超额分摊）检测',
  '已过月数超过等待期月数却仍在分摊（等待期已满）检测',
  '等待期已满但期末未分摊余额未归零提示',
  '累计已分摊 + 期末未分摊 ≠ 授予总额 检测',
];

const OUT_OF_SCOPE = [
  '判断授予日公允价值该用市价、评估价还是期权定价模型的结果（属于会计与评估判断）',
  '判断等待期、业绩条件、可行权数量如何估计与后续调整',
  '出具有关股份支付的审计或鉴证意见，或判断要不要确认递延所得税',
  '读取股权激励管理系统 / 券商底稿 / 评估报告的原始文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '计划名称\t授予日\t授予数量\t授予日公允价值\t等待期月数\t已过月数\t期初未分摊余额\t本期应分摊金额\t本期实摊金额\t累计已分摊金额\t期末未分摊余额',
  '2026年限制性股票计划\t2026-01-01\t100.00\t12.00\t24\t1\t1200.00\t50.00\t50.00\t50.00\t1150.00',
  '2026年员工持股平台份额\t2026-01-01\t60.00\t15.00\t36\t1\t900.00\t25.00\t25.00\t25.00\t875.00',
  '合计\t\t160.00\t\t\t\t2100.00\t75.00\t75.00\t75.00\t2025.00',
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
const who = (it) => String(it.plan || '').trim() || `第 ${it.line} 行`;

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

function checkCloseVsOpen(it) {
  const open = normNumber(it.openBalance);
  const act = normNumber(it.currentActual);
  const close = normNumber(it.closeBalance);
  if (open === null || act === null || close === null) return null;
  const want = round2(open - act);
  if (Math.abs(want - close) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末余额与滚动关系不符',
      message: `${who(it)} 期末未分摊 ${close} ≠ 期初未分摊 ${open} − 本期实摊 ${act} = ${want}`,
      evidence: `期初未分摊=${open}；本期实摊=${act}；期末未分摊=${close}；应为 ${want}`,
    };
  }
  return null;
}

function checkCloseVsGrantMinusCum(it) {
  const qty = normNumber(it.qty);
  const fv = normNumber(it.fairValue);
  const cum = normNumber(it.cumAmort);
  const close = normNumber(it.closeBalance);
  if (qty === null || fv === null || cum === null || close === null) return null;
  const grant = round2(qty * fv);
  const want = round2(grant - cum);
  if (Math.abs(want - close) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末余额与授予总额不符',
      message: `${who(it)} 期末未分摊 ${close} ≠ 授予总额 ${grant}（${qty} × ${fv}）− 累计已分摊 ${cum} = ${want}`,
      evidence: `授予数量=${qty}；授予日公允价值=${fv}；授予总额=${grant}；累计已分摊=${cum}；期末未分摊=${close}；应为 ${want}`,
    };
  }
  return null;
}

function checkNegativeActual(it) {
  const act = normNumber(it.currentActual);
  if (act === null || act >= 0) return null;
  return {
    line: it.line, level: 'P0', category: '本期实摊为负',
    message: `${who(it)} 本期实摊金额为 ${act}（负数）—— 股份支付费用不应为负`,
    evidence: `本期实摊金额=${act}`,
  };
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = [String(it.plan || '').trim(), String(it.grantDate || '').trim(),
      String(it.elapsedMonths || '').trim()].join('|');
    if (!key.replace(/\|/g, '')) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「计划 + 授予日 + 已过月数」完全相同 —— 可能重复计入`,
        evidence: `计划=${it.plan}；授予日=${it.grantDate}；已过月数=${it.elapsedMonths}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
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
  if (text.trim() === '') return insufficient(['材料文本为空：请把股份支付费用分摊表（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkCloseVsOpen(it), checkCloseVsGrantMinusCum(it), checkNegativeActual(it)];
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
        grant_total: round2(items.reduce((n, it) => {
          const q = normNumber(it.qty); const v = normNumber(it.fairValue);
          return n + ((q === null || v === null) ? 0 : q * v);
        }, 0)),
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
