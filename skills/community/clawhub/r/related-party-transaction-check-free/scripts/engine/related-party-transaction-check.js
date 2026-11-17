/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * related-party-transaction-check.js —— 关联方交易与同期资料一致性核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有关联方交易、要填报关联业务往来报告表并准备同期资料的公司**，
 * 在**年度汇算清缴填报、编制报表附注「关联方交易」、以及年审提供底稿之前**。
 * 会计要把同一笔关联交易在**三处金额**上核成一致（账上的本期交易金额 / 关联交易台账 /
 * 报告表填报金额），再核期末往来余额、定价方法与同期资料准备情况 ——
 * 三处对不上，报告表就是错的，而它错不错**完全能用算术复算出来**。
 *
 * 核心可算关系（都能手算复现）：
 *   报告表填报金额 = 台账金额（表账一致）
 *   本期交易金额   = 台账金额（账账一致）
 *   期末往来余额   ≥ 0（往来余额不应为负）
 *   合计行各列     = 明细行逐列相加（交易金额 / 台账金额 / 报告表金额 / 往来余额）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**两个主体是否构成关联关系、定价是否公允、要不要做特别纳税调整（那属于法律与转让定价判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**。
   `报告表填报金额` 与 `台账金额` 都含 `金额`；`本期交易金额` 同理 ⇒ 宽泛的键排前面会互相抢列。 */
const ROLES = {
  party: ['关联方名称', '关联方', '交易对方'],
  relation: ['关联关系', '关联关系类型'],
  dealType: ['交易类型', '交易类别', '关联交易类型'],
  dealAmount: ['本期交易金额', '交易金额'],
  ledgerAmount: ['台账金额', '账面金额'],
  reportedAmount: ['报告表填报金额', '报告表金额', '申报表金额'],
  balance: ['期末往来余额', '往来余额', '期末余额'],
  share: ['占营业收入比例', '占比', '收入占比'],
  method: ['定价方法', '转让定价方法'],
  docs: ['同期资料', '同期资料准备情况'],
};

const LABELS = {
  party: '关联方名称', relation: '关联关系', dealType: '交易类型', dealAmount: '本期交易金额',
  ledgerAmount: '台账金额', reportedAmount: '报告表填报金额', balance: '期末往来余额',
  share: '占营业收入比例', method: '定价方法', docs: '同期资料',
};

const REQUIRED = ['dealAmount', 'ledgerAmount', 'reportedAmount', 'balance', 'method'];
const SUM_ROLES = ['dealAmount', 'ledgerAmount', 'reportedAmount', 'balance'];
const PRICING_METHODS = ['可比非受控价格法', '再销售价格法', '成本加成法', '交易净利润法', '利润分割法', '成本加利润法'];
const DOCS_THRESHOLD = 10000000;   // 1000 万：常见"本地文档"门槛量级（只作提示）
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**（形态 B，且必须是 `Boolean(...)` 这一种写法）：
   `strip_free_engine` 按「`const paid` + `Boolean(`」这一行识别并摘掉付费语句；
   写成别的形式（例：数组的 `.some()`）会**留下开关不删** ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成"没删干净"而整包跳过（本轮实测踩到）。
   两个形态（MARKER + 开关）同时出现会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（交易金额 / 台账金额 / 报告表金额 / 往来余额）',
  '同一关联方同一交易类型重复行检测',
  '报告表填报金额 = 台账金额（一致性）',
  '本期交易金额 = 台账金额（账表一致）',
  '期末往来余额为负检测',
  '定价方法空白或占位符检测（无法说明定价依据）',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '报告表金额与台账金额差异率超过 5% 提示（差异率要能解释）',
  '关联交易占营业收入比例超过 50% 提示（重大关联交易，关注特别纳税调整）',
  '期末往来余额超过本期交易金额（长期挂账）提示',
  '定价方法不在常见五法口径（可比非受控价格法/再销售价格法/成本加成法/交易净利润法/利润分割法）提示',
  '交易金额达到同期资料门槛却填「未准备/无」提示',
];

const OUT_OF_SCOPE = [
  '判断两个主体之间**是否构成关联关系**（属于法律与税务判断，请按公司法与税收口径认定）',
  '判断关联交易定价**是否公允**、要不要做特别纳税调整（属于转让定价专业判断）',
  '代填关联业务往来报告表，或出具鉴证意见与税务意见',
  '读取财务系统 / 关联交易台账系统 / 同期资料文档的原始文件（需要你先导出成文本贴进来）',
  '判断同期资料该准备哪几层（主体文档/本地文档/特殊事项文档）——本工具只核你填的字段与三处金额',
];

const SAMPLE_TEXT = [
  '关联方名称\t关联关系\t交易类型\t本期交易金额\t台账金额\t报告表填报金额\t期末往来余额\t占营业收入比例\t定价方法\t同期资料',
  '豫州控股集团有限公司\t母公司\t采购商品\t8000000.00\t8000000.00\t8000000.00\t1200000.00\t40%\t可比非受控价格法\t已准备（本地文档）',
  '中岳联营企业\t联营企业\t提供劳务\t3000000.00\t3000000.00\t3000000.00\t500000.00\t15%\t成本加成法\t已准备（本地文档）',
  '合计\t\t\t11000000.00\t11000000.00\t11000000.00\t1700000.00\t\t\t',
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
const who = (it) => { const p = String(it.party || '').trim(); return p ? `${p}（${String(it.dealType || '').trim() || '未注明类型'}）` : `第 ${it.line} 行`; };

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
    const key = [String(it.party || '').trim(), String(it.dealType || '').trim()].join('|');
    if (!key.replace(/\|/g, '')) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「关联方 + 交易类型」完全相同 —— 可能重复计入`,
        evidence: `关联方=${it.party}；交易类型=${it.dealType}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkReportedVsLedger(it) {
  const rep = normNumber(it.reportedAmount);
  const led = normNumber(it.ledgerAmount);
  if (rep === null || led === null) return null;
  if (Math.abs(rep - led) > TOL) {
    return {
      line: it.line, level: 'P0', category: '报告表金额与台账金额不一致',
      message: `${who(it)} 报告表填报金额 ${rep} ≠ 台账金额 ${led}`,
      evidence: `报告表填报金额=${rep}；台账金额=${led}；差异=${round2(rep - led)}`,
    };
  }
  return null;
}

function checkDealVsLedger(it) {
  const deal = normNumber(it.dealAmount);
  const led = normNumber(it.ledgerAmount);
  if (deal === null || led === null) return null;
  if (Math.abs(deal - led) > TOL) {
    return {
      line: it.line, level: 'P0', category: '交易金额与台账金额不一致',
      message: `${who(it)} 本期交易金额 ${deal} ≠ 台账金额 ${led}`,
      evidence: `本期交易金额=${deal}；台账金额=${led}；差异=${round2(deal - led)}`,
    };
  }
  return null;
}

function checkNegativeBalance(it) {
  const bal = normNumber(it.balance);
  if (bal === null || bal >= 0) return null;
  return {
    line: it.line, level: 'P0', category: '期末往来余额为负',
    message: `${who(it)} 期末往来余额为 ${bal}（负数）—— 往来余额不应为负`,
    evidence: `期末往来余额=${bal}`,
  };
}

function checkMethodBlank(it) {
  if (!isBlank(it.method)) return null;
  return {
    line: it.line, level: 'P1', category: '定价方法缺失',
    message: `${who(it)} 的「定价方法」是空白或占位符 —— 关联交易必须说明定价依据`,
    evidence: `定价方法=${it.method === undefined ? '(空)' : it.method}`,
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
  if (text.trim() === '') return insufficient(['材料文本为空：请把关联交易台账（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkReportedVsLedger(it), checkDealVsLedger(it), checkNegativeBalance(it), checkMethodBlank(it)];
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
        deal_total: round2(items.reduce((n, it) => n + (normNumber(it.dealAmount) || 0), 0)),
        balance_total: round2(items.reduce((n, it) => n + (normNumber(it.balance) || 0), 0)),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, PRICING_METHODS,
};
