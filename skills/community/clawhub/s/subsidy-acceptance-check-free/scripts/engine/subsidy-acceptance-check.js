#!/usr/bin/env node
/**
 * subsidy-acceptance-check.js —— 政府补助与专项验收核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：拿到政府补助与专项资金的企业，**验收与拨付核对是必做的一步**，而这一步几乎全是跨列算术：
 *   ① 台账上的「补助金额」与银行到账的「到账金额」要对得上（分期拨款、代扣代缴、以拨代支都会造成差额）
 *   ② 「专项支出合计」要覆盖「补助金额」，又不能超过「支出预算」
 *   ③ 验收资料清单（立项批复 / 验收报告 / 专项审计报告 / 支出明细台账 / 发票清单）要一件不缺
 *   ④ 同一项目不能重复申报（同一补助年度内，项目编号唯一；项目名称 + 补助年度 也应唯一）
 * 补助资金对不上就结不了项，验收资料缺件就会被退件 —— 都是真金白银与工期。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现上面这六项**表内逐行算术与清单勾稽**；
 *    **完整档（付费）的实现不在这个包里** —— 跨项目/跨年度汇总台账、差异归因、
 *    按差额排序的处理清单、同一补助文号重复使用检测都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *    本版本**只做**台账金额与支出的逐行复算与勾稽，**不做**补助资格与政策适用性的判定。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定补助资格与政策适用性、不判定验收结论本身是否成立、不判断支出是否真实且与项目相关、
 *          不读 .xlsx/.pdf 原件、不联网核验补助文号真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '补助到账金额与台账一致（逐行复算 到账金额 − 补助金额，差额不为零即列出并给出差额）',
  '专项支出合计与补助金额配比（专项支出合计须不小于补助金额，不足即报出差额）',
  '验收资料清单完整性（按 立项批复/验收报告/专项审计报告/支出明细台账/发票清单 逐件点名缺件）',
  '同一项目重复申报（同一补助年度内 项目编号重复，或 项目名称+补助年度 重复）',
  '支出超预算与补助比例失衡（专项支出合计 > 支出预算；补助金额 > 支出预算）',
  '关键字段缺失与金额为负（项目编号/名称/补助金额/到账金额/支出合计缺失、金额为负或无法解析）',
];

const CHECKS_WITHHELD = [
  '跨项目/跨年度汇总台账（按补助年度、按验收结论分组汇总项目数、补助金额、到账金额、专项支出合计与差额）',
  '差异归因（把每条差额归到 补助口径 / 支出归集 / 预算科目 / 跨年归属 四类之一）',
  '按差额金额排序的处理清单（每条差额按 |差额| 从大到小排队，带处理建议）',
  '同一补助文号被多个项目重复使用检测',
];

const OUT_OF_SCOPE = [
  '判定补助资格与政策适用性（本项目是否符合申报条件、适用哪一档政策）—— 那是主管部门的认定权，本工具不做',
  '判定验收结论本身是否成立（专家对技术指标与建设内容是否达标的判断），本工具只核台账与资料清单的字面完整性',
  '判断支出是否「真实、合规、与项目相关」（那是专项审计的职责），本工具只做表内算术与清单勾稽',
  '读取 .xlsx / .pdf 原件、联网核验补助文号真伪、替代审计报告、法律意见或税务处理意见',
];

// 样例：一张**干净**的政府补助台账与验收资料对照表 —— 四个项目、两个补助年度，
// 补助金额 = 到账金额、专项支出合计既不小于补助金额也不超预算、验收资料五件齐全、项目编号不重复。
const SAMPLE_TEXT = [
  '项目编号\t项目名称\t补助年度\t补助文号\t补助金额\t到账金额\t支出预算\t专项支出合计\t验收资料清单\t验收结论\t备注',
  'ZL2024-018\t智能制造装备升级改造\t2024\t苏工信财〔2024〕37号\t1200000.00\t1200000.00\t3000000.00\t2980000.00\t立项批复;验收报告;专项审计报告;支出明细台账;发票清单\t已验收\t2024-11-20 全额到账',
  'ZL2024-026\t工业废水零排放技改\t2024\t苏环资财〔2024〕12号\t800000.00\t800000.00\t2000000.00\t1960000.00\t立项批复;验收报告;专项审计报告;支出明细台账;发票清单\t已验收\t2024-12-05 全额到账',
  'ZL2025-007\t中小企业数字化改造\t2025\t苏工信财〔2025〕09号\t500000.00\t500000.00\t1500000.00\t1470000.00\t立项批复;验收报告;专项审计报告;支出明细台账;发票清单\t已验收\t2025-06-18 全额到账',
  'ZL2025-021\t高技能人才培训基地建设\t2025\t苏人社财〔2025〕21号\t600000.00\t600000.00\t1800000.00\t1795000.00\t立项批复;验收报告;专项审计报告;支出明细台账;发票清单\t验收中\t2025-09-30 全额到账，验收资料已受理',
].join('\n');

const TOL = 0.01;

// 清单里固定要有的验收资料（缺哪件就点名哪件）
const REQUIRED_DOCS = ['立项批复', '验收报告', '专项审计报告', '支出明细台账', '发票清单'];

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = ['projectName', 'grantAmount', 'receivedAmount', 'budgetAmount', 'spendTotal', 'acceptanceDocs'];

// 单元格级必需字段（空白/占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['projectNo', '项目编号'],
  ['projectName', '项目名称'],
  ['grantAmount', '补助金额'],
  ['receivedAmount', '到账金额'],
  ['spendTotal', '专项支出合计'],
];

// 金额列（用于「为负 / 无法解析」判定）
const AMOUNT_FIELDS = [
  ['grantAmount', '补助金额'],
  ['receivedAmount', '到账金额'],
  ['budgetAmount', '支出预算'],
  ['spendTotal', '专项支出合计'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过两次，见 tools/header_map_check.py）。
const ROLES = {
  projectNo: ['项目编号', '项目代码', '项目编码', '申报编号', '编号'],
  projectName: ['项目名称', '专项名称', '项目', '申报项目'],
  year: ['补助年度', '资金年度', '所属年度', '预算年度', '年度'],
  docNo: ['补助文号', '批复文号', '资金文号', '下达文号', '文号'],
  grantAmount: ['补助金额', '补助资金', '补助总额', '批准金额', '补贴金额', '财政补助'],
  receivedAmount: ['到账金额', '实到金额', '已到账金额', '实际到账', '到账', '实收金额'],
  budgetAmount: ['支出预算', '项目预算', '预算金额', '预算总额', '预算'],
  spendTotal: ['专项支出合计', '支出合计', '专项支出', '已支出金额', '支出金额'],
  acceptanceDocs: ['验收资料清单', '验收材料清单', '验收资料', '资料清单', '验收材料'],
  acceptanceResult: ['验收结论', '验收结果', '验收状态', '验收情况', '结论'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  projectNo: '项目编号',
  projectName: '项目名称',
  year: '补助年度',
  docNo: '补助文号',
  grantAmount: '补助金额',
  receivedAmount: '到账金额',
  budgetAmount: '支出预算',
  spendTotal: '专项支出合计',
  acceptanceDocs: '验收资料清单',
  acceptanceResult: '验收结论',
  note: '备注',
};

const SUM_ROLES = ['grantAmount', 'receivedAmount', 'budgetAmount', 'spendTotal'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「一致」，也不说「不一致」。',
  };
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/** 解析成 {header, cols, items, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const num = (it, role) => {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
};

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function who(it) {
  const name = String(it.projectName == null ? '' : it.projectName).trim();
  const no = String(it.projectNo == null ? '' : it.projectNo).trim();
  return `第 ${it.line} 行「${name || no || '未命名项目'}」`;
}

function docList(v) {
  return String(v == null ? '' : v).split(/[;；,，、/|]+/).map((s) => s.trim()).filter((s) => s !== '');
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 补助到账金额与台账一致（逐行复算，差额不为零即列出） */
function checkReceivedVsGrant(items) {
  const out = [];
  for (const it of items) {
    const g = normNumber(it.grantAmount);
    const r = normNumber(it.receivedAmount);
    if (g === null || r === null) continue;          // 缺失/解析不了交给「关键字段」那一项
    const diff = round2(r - g);
    if (Math.abs(diff) < TOL) continue;
    out.push(finding(diff < 0 ? 'P0' : 'P2', '到账金额与补助金额不符', it, diff,
      `${who(it)}：台账补助金额 ${money(g)}，到账金额 ${money(r)}，差额 ${money(diff)}（${diff < 0 ? '少到账' : '多到账'}）。`,
      '拿银行回单对一遍：分期到账的请在台账里只记**本期实到**并另设累计列；若已全额到账则属登记错误。'
      + '本工具只列出差额，不认定是哪种原因。'));
  }
  return out;
}

/** 2. 专项支出合计与补助金额配比（支出合计须不小于补助金额） */
function checkSpendVsGrant(items) {
  const out = [];
  for (const it of items) {
    const g = normNumber(it.grantAmount);
    const s = normNumber(it.spendTotal);
    if (g === null || s === null) continue;
    if (s >= g - TOL) continue;
    out.push(finding('P0', '支出合计小于补助金额', it, round2(s - g),
      `${who(it)}：专项支出合计 ${money(s)} 小于补助金额 ${money(g)}，缺口 ${money(g - s)}。`
      + '补助资金要求全额用于本项目，支出归集不全时会出现这种缺口。',
      '先确认是否有支出还没归集到本项目（发票未到、跨年报销、走错科目），再确认是否形成结余需要按文件退回。'));
  }
  return out;
}

/** 3. 验收资料清单完整性（逐件点名缺件，不给"大概齐"的判断） */
function checkDocCompleteness(items) {
  const out = [];
  for (const it of items) {
    const have = docList(it.acceptanceDocs);
    if (!have.length) {
      out.push(finding('P1', '验收资料清单缺件', it, undefined,
        `${who(it)}：验收资料清单一栏是空的 —— 按口径应备齐 ${REQUIRED_DOCS.join('、')}`
        + `（共 ${REQUIRED_DOCS.length} 件），现在 ${REQUIRED_DOCS.length} 件都点不到。`,
        '验收资料按件列在「验收资料清单」里（分号分隔），缺件会被退件；先把清单补全再逐件归档。'));
      continue;
    }
    const missing = REQUIRED_DOCS.filter((d) => !have.some((h) => h.indexOf(d) >= 0));
    if (!missing.length) continue;
    out.push(finding('P1', '验收资料清单缺件', it, undefined,
      `${who(it)}：验收资料缺 ${missing.length} 件 —— ${missing.join('、')}（清单原文：${have.join(';')}）。`,
      '按验收办法逐件补齐；本工具只核**清单字面是否点到这些件**，不判断资料内容是否合格。'));
  }
  return out;
}

/** 4. 同一项目重复申报（同一补助年度内，项目编号唯一；项目名称 + 补助年度 也应唯一） */
function checkDuplicateProject(items) {
  const out = [];
  const reported = new Set();
  const byNoYear = new Map();
  const byNameYear = new Map();
  for (const it of items) {
    const no = String(it.projectNo == null ? '' : it.projectNo).trim();
    const name = String(it.projectName == null ? '' : it.projectName).trim();
    const year = String(it.year == null ? '' : it.year).trim();

    // ⚠️ 重复申报的口径是「同一补助年度内」：同一年度里同一项目出现两次才是重复申报；
    //    同一项目编号跨年度出现是**正常的跨年续建**，由完整档的「跨年归属」去核对，不算重复。
    const noKey = `${no}|${year}`;
    if (no && byNoYear.has(noKey) && !reported.has(it.line)) {
      reported.add(it.line);
      out.push(finding('P0', '同一项目重复申报', it, undefined,
        `${who(it)}：项目编号「${no}」在补助年度 ${year || '(未填)'} 里第 ${byNoYear.get(noKey)} 行已经出现过 —— 同一项目同一补助年度重复申报。`,
        '一个项目在一个补助年度里只应有一条台账记录；分次到账请用「到账金额/累计到账」列，不要新增行。'));
    }
    if (no && !byNoYear.has(noKey)) byNoYear.set(noKey, it.line);

    const key = `${name}|${year}`;
    if (name && byNameYear.has(key) && !reported.has(it.line)) {
      reported.add(it.line);
      out.push(finding('P0', '同一项目重复申报', it, undefined,
        `${who(it)}：「${name}」在补助年度 ${year || '(未填)'} 里第 ${byNameYear.get(key)} 行已经出现过 —— 同一项目同一补助年度重复申报。`,
        '一个项目在一个补助年度里只应有一条台账记录；分次到账请用「到账金额/累计到账」列，不要新增行。'));
    }
    if (name && !byNameYear.has(key)) byNameYear.set(key, it.line);
  }
  return out;
}

/** 5. 支出超预算与补助比例失衡 */
function checkBudgetRatio(items) {
  const out = [];
  for (const it of items) {
    const b = normNumber(it.budgetAmount);
    const s = normNumber(it.spendTotal);
    const g = normNumber(it.grantAmount);
    if (b !== null && s !== null && s > b + TOL) {
      out.push(finding('P1', '支出超预算', it, round2(s - b),
        `${who(it)}：专项支出合计 ${money(s)} 超过支出预算 ${money(b)}，超支 ${money(s - b)}。`,
        '核对是否有预算调整批复；没有批复的超预算支出会被审计问到，先把超支金额与批复文号对上。'));
    }
    if (b !== null && g !== null && g > b + TOL) {
      out.push(finding('P0', '补助金额超预算', it, round2(g - b),
        `${who(it)}：补助金额 ${money(g)} 超过该项目的支出预算 ${money(b)}，超出 ${money(g - b)} —— 补助比例在算术上不成立。`,
        '补助金额不可能大于项目自身预算；请核对预算列是否漏填了自筹部分，或补助金额是否串行登记。'));
    }
  }
  return out;
}

/** 6. 关键字段缺失与金额为负 / 无法解析 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const [role, label] of AMOUNT_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '金额无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的金额（只认数字、千分位、¥、括号负数）。`,
          '把金额改成纯数字形态（如 1200000.00）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '金额为负', it, n,
          `${who(it)}：「${label}」是负数（${money(n)}）—— 补助与支出类台账里出现负数通常是填反了方向或写成了红字冲销。`,
          '确认是红字冲销还是填错借贷方向；确属冲销的请写在「备注」里并保留原值，别直接改成正数。'));
      }
    }
  }
  return out;
}

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的政府补助台账与验收资料对照表']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的政府补助台账与验收资料对照表']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的政府补助台账与验收资料对照表（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行项目明细（现在只有表头，没有可核对的明细行）']);
  }

  const findings = [];
  const notRun = [];

  for (const f of checkReceivedVsGrant(t.items)) findings.push(f);
  for (const f of checkSpendVsGrant(t.items)) findings.push(f);
  for (const f of checkDocCompleteness(t.items)) findings.push(f);
  for (const f of checkDuplicateProject(t.items)) findings.push(f);
  for (const f of checkBudgetRatio(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：完整档那四类检查一项都不执行，这里如实记下来（只记「没做」，不会伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const grantTotal = t.totals.grantAmount;
  const receivedTotal = t.totals.receivedAmount;
  const spendTotal = t.totals.spendTotal;
  const budgetTotal = t.totals.budgetAmount;
  const receivedDiff = round2(receivedTotal - grantTotal);

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      grant_total: grantTotal,
      received_total: receivedTotal,
      spend_total: spendTotal,
      budget_total: budgetTotal,
      received_diff: receivedDiff,
      basis: '到账金额应等于台账补助金额（差额逐行列出）；专项支出合计须不小于补助金额、且不超过支出预算；'
        + '验收资料按固定五件清单（立项批复/验收报告/专项审计报告/支出明细台账/发票清单）点名缺件；'
        + '同一补助年度内 项目编号唯一，项目名称+补助年度 也应唯一。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张对照表按上面写明的口径算得对、清单点到的件都在**，'
      + '不代表补助资格、政策适用性、验收结论本身或支出的真实合规性已经过关 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    grant_total: grantTotal,
    received_total: receivedTotal,
    spend_total: spendTotal,
    budget_total: budgetTotal,
    received_diff: receivedDiff,
    paid_in_total: receivedTotal,
    outstanding_total: round2(grantTotal - receivedTotal),
  };
  result.scope = scope;



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
