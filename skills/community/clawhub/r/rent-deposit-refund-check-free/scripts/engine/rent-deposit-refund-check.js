/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * rent-deposit-refund-check.js —— 押金保证金收取与退还核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**出纳 / 财务 / 物业与招商运营在押金收取、退租退押、
 * 月底核对押金台账时**。押金是"别人的钱趴在账上"：收的时候容易，退的时候每一分都要有据可依。
 * 每月都在吵的就是这几处：
 *   · 应退金额没把扣除项减掉（违约金 / 损坏赔偿 / 欠费），或者扣除额比押金还大；
 *   · 扣了钱，扣除依据栏却是空的 —— 对方不认这笔扣款；
 *   · 约定期限到了钱还没退出去，台账余额一直挂着，没人催；
 *   · 同一份合同同一笔押金退了两遍（重复付款）；
 *   · 台账余额与「收取 − 退还 − 已结转」对不上，账实不符。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   应退金额   = 收取金额 − 扣除金额
 *   台账余额   = 收取金额 − 退还金额 − 已结转金额
 *   应退截止日 = 收取日期 + 约定退还期限（自然日）
 *   已结转金额 = 本行押金在本期已处置的金额（含按依据扣除核销的部分 + 转入下期 / 其他合同的部分）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），不写盘、不读环境变量。
 *
 * 免费档执行 6 项；完整档追加 3 项（见 CHECKS_WITHHELD），其中最后一项是免费档**结构上做不到**的：
 * 「按超期未退金额排序的处理清单」。
 *
 * ⚠️ 本工具**不判断**押金该收多少、扣除依据的文本是否合法有效、押金是否真的收到或退还
 *    （那属于租赁合同、招标文件与银行流水的核定）：表里的金额、日期、期限一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号与合同编号列出来。
 *
 * ⚠️ 付费项用**形态 A**：付费实现集中在 `/* ===== … ===== *​/` 标记与入口函数之间，
 *    由 tools/strip_free_engine.py 整块摘掉；开关**只声明一次**（见入口函数第一行），
 *    注释里不要写出那一行的字面量 —— 残渣断言是纯字符串包含判断。
 */

const CHECKS_GIVEN = [
  '应退金额复算（应退金额 = 收取金额 − 扣除金额）',
  '扣除金额带依据（违约金 / 损坏赔偿 / 欠费）与上限（扣除金额 ≤ 收取金额）',
  '退还时间超过约定期限提示（应退截止日 = 收取日期 + 约定退还期限；含已过截止日仍未退清）',
  '同一合同同一押金类型重复退还检测',
  '台账余额勾稽（台账余额 = 收取金额 − 退还金额 − 已结转金额）',
  '关键字段缺失 / 金额为负检测',
];

const CHECKS_WITHHELD = [
  '差异归因（扣除依据口径 / 期限口径 / 重复退口径 / 结转口径）',
  '跨项目 / 跨期押金汇总台账（按项目与按收取月份归集收取 / 扣除 / 应退 / 退还 / 结转 / 未退余额）',
  '按超期未退金额排序的处理清单（带原文行号、超期天数与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断押金 / 保证金该收多少、比例是否合规（以租赁合同、招标文件与内部制度为准）',
  '判断扣除依据的文本是否合法有效、违约金到底该不该收（本工具只看依据栏是否为空、有没有写明扣除事由）',
  '判断押金是否真的收到 / 退还（要拿银行流水、收据与退款凭证核，本工具不去查外部系统）',
  '计算押金的利息 / 资金占用费，或处理增值税、代扣代缴与发票',
  '读取 Excel / 财务系统 / 银行流水导出文件（需要你先导出成文本贴进来）',
  '按汇率折算多币种后合并（本表按同一币种口径核对）',
  '判断「约定退还期限」是否符合当地租赁与招投标法规（本工具只按你填的天数复算截止日）',
];

const SAMPLE_TEXT = [
  '合同编号\t承租方\t项目\t押金类型\t收取日期\t收取金额\t扣除金额\t扣除依据\t应退金额\t退还日期\t退还金额\t已结转金额\t台账余额\t约定退还期限\t备注',
  'HT-2026-001\t星海科技\t科创园A座\t租赁押金\t2025-03-01\t30000.00\t0.00\t\t30000.00\t2025-05-20\t30000.00\t0.00\t0.00\t90\t正常退租 无扣款',
  'HT-2026-002\t蓝湾餐饮\t蓝湾广场B1\t租赁押金\t2025-04-01\t50000.00\t3200.00\t欠费3200元已发催缴单\t46800.00\t2025-06-25\t46800.00\t3200.00\t0.00\t90\t欠租3个月已发催缴单',
  'HT-2026-003\t云图设计\t科创园B座\t履约保证金\t2025-05-06\t80000.00\t0.00\t\t80000.00\t2025-07-20\t80000.00\t0.00\t0.00\t180\t项目验收合格后退还',
  'HT-2026-004\t恒芯半导体\t蓝湾广场B2\t装修押金\t2025-06-01\t20000.00\t1500.00\t损坏赔偿1500元有维修单\t18500.00\t2025-08-10\t18500.00\t1500.00\t0.00\t90\t退租时墙面损坏已修复',
  'HT-2026-005\t星海科技\t科创园A座\t水电押金\t2025-06-15\t5000.00\t0.00\t\t5000.00\t\t0.00\t5000.00\t0.00\t60\t押金结转至新合同 HT-2026-009',
  'HT-2026-006\t恒芯半导体\t科创新城C区\t投标保证金\t2026-01-05\t20000.00\t0.00\t\t20000.00\t\t0.00\t0.00\t20000.00\t90\t招标项目尚未定标',
].join('\n');

const TOL = 0.01;
const DAY_MS = 86400000;

/** 免费档口径的说明文本（付费档会在入口里换成完整档口径）——必须留在摘除标记**之前**，
 *  否则整块摘掉后免费引擎会引用到不存在的常量（第 286 轮实测）。 */
const NOTE_FREE = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 checks_not_run。`;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前，兜底的宽泛别名在后。
  //    「扣除依据」必须排在「扣除金额」前面（否则被扣款列抢走，依据永远核不了）；
  //    「退还日期」必须排在「退还金额」前面；「约定退还期限」必须排在「退还金额」前面；
  //    「已结转金额」必须排在「台账余额」前面 —— 这类顺序错**不会报缺列，只会算错**。
  contract: ['合同编号', '合同号', '协议编号', '合同代码'],
  tenant: ['承租方', '租户名称', '租户', '客户名称', '客户'],
  project: ['项目名称', '所属项目', '项目'],
  depositType: ['押金类型', '保证金类型', '款项类型', '押金种类', '押金项目'],
  collectDate: ['收取日期', '收款日期', '缴纳日期', '入账日期', '收取时间'],
  collectAmt: ['收取金额', '实收金额', '已收金额', '收取本金', '押金金额'],
  dueDays: ['约定退还期限', '退还期限', '约定期限', '押金期限', '期限天数'],
  deductBasis: ['扣除依据', '扣款依据', '扣除原因', '扣除事由', '扣款原因', '扣款说明'],
  deductAmt: ['扣除金额', '扣款金额', '扣减金额', '扣除款'],
  expectRefund: ['应退金额', '应退押金', '应退款项', '应退'],
  refundDate: ['退还日期', '退款日期', '退回日期', '退还时间', '实退日期'],
  asOfDate: ['台账截止日', '数据截止日', '对账截止日', '台账基准日', '统计日期'],
  refundAmt: ['退还金额', '已退金额', '实退金额', '退款金额', '退还本金'],
  carryAmt: ['已结转金额', '结转金额', '结转到下期', '结转下期', '结转数', '结转'],
  balance: ['台账余额', '押金余额', '期末余额', '账面余额', '余额'],
  remark: ['备注', '说明', '摘要'],
};

const LABELS = {
  contract: '合同编号', tenant: '承租方', project: '项目', depositType: '押金类型',
  collectDate: '收取日期', collectAmt: '收取金额', dueDays: '约定退还期限',
  deductBasis: '扣除依据', deductAmt: '扣除金额',
  expectRefund: '应退金额', refundDate: '退还日期', asOfDate: '台账截止日', refundAmt: '退还金额',
  carryAmt: '已结转金额',
  balance: '台账余额', remark: '备注',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 去替你假设"没有这项扣除"） */
const REQUIRED = ['contract', 'tenant', 'project', 'depositType', 'collectDate', 'dueDays', 'deductBasis',
  'deductAmt', 'expectRefund', 'refundDate', 'refundAmt', 'carryAmt', 'balance'];
/** 参与金额归集的列（用于 scope.column_totals 与完整档汇总台账逐列合计） */
const SUM_ROLES = ['collectAmt', 'deductAmt', 'expectRefund', 'refundAmt', 'carryAmt', 'balance'];
/** 逐行必须填的单元格：**扣除依据 / 退还日期 / 备注**允许留空（没扣款、还没退、不用写说明） */
const CELL_REQUIRED = ['contract', 'tenant', 'project', 'depositType', 'collectDate', 'dueDays',
  'deductAmt', 'expectRefund', 'refundAmt', 'carryAmt', 'balance'];
/** 负数检查的列 */
const NEGATIVE_ROLES = [['collectAmt', '收取金额'], ['deductAmt', '扣除金额'], ['expectRefund', '应退金额'],
  ['refundAmt', '退还金额'], ['carryAmt', '已结转金额'], ['balance', '台账余额']];
/** 扣除事由关键词：依据栏必须落到这些事由上，否则等于"没写清为什么扣" */
const BASIS_WORDS = /违约金|赔偿|损坏|欠费|欠租|滞纳|逾期|罚款|维修|复原|清洁|拆改|水电|燃气|物业费|其他扣款/;
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a|-+|—+|–+)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（缺一列就报缺列，不会替你按 0 算）。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function cell(v) {
  return v === undefined || v === null ? '' : String(v).trim();
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = cell(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥$,\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) {
    return { error: 'empty', items: [], totals: { row: null, line: 0, rows: 0 }, cols: [], missingColumns: [] };
  }
  const headers = splitRow(raw[0]);
  const cols = headers.map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingColumns = REQUIRED.filter((r) => !have.has(r)).map((r) => LABELS[r]);
  if (missingColumns.length) {
    return { items: [], totals: { row: null, line: 0, rows: 0 }, cols, missingColumns };
  }
  const items = [];
  let totalRow = null;
  let totalRows = 0;
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    cols.forEach((c, idx) => {
      if (!c.role) return;
      if (row[c.role] === undefined) row[c.role] = cells[idx] === undefined ? '' : cells[idx];
    });
    if (TOTAL_WORDS.test(cell(cells[0]))) {
      // 一份材料里拼了多期 / 多个项目时会出现多行「合计 / 小计」：只把**最后一行**当汇总行；
      // 行数记进 scope.totals_rows 让人看得见，不静默丢数据。
      totalRow = row;
      totalRows += 1;
    } else {
      items.push(row);
    }
  }
  return {
    items,
    totals: { row: totalRow, line: totalRow ? totalRow.line : 0, rows: totalRows },
    cols,
    missingColumns: [],
  };
}

const num = (row, role) => normNumber(row[role]);

function sumRole(rows, role) {
  let s = 0;
  for (const it of rows) {
    const v = num(it, role);
    if (v !== null) s += v;
  }
  return round2(s);
}

function who(it) {
  return `合同「${cell(it.contract) || '(未填合同编号)'}」${cell(it.depositType) || '(未填押金类型)'}`;
}

/* —— 日期：只认 YYYY-MM-DD（也接受 / 与 . 分隔），全部按 UTC 零点算，避免时区漂移 —— */
function parseDateMs(v) {
  const s = cell(v);
  const m = s.match(/^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$/);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const t = Date.UTC(y, mo - 1, d);
  const dt = new Date(t);
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return t;
}

function fmtDate(ms) {
  const d = new Date(ms);
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())}`;
}

function monthOf(ms) {
  return fmtDate(ms).slice(0, 7);
}

/** 收取日 + 约定退还期限 = 应退截止日；退还日期晚于截止日即超期 */
function dueInfoOf(it) {
  const collectMs = parseDateMs(it.collectDate);
  const days = num(it, 'dueDays');
  const refundMs = parseDateMs(it.refundDate);
  const dueMs = (collectMs !== null && days !== null) ? collectMs + Math.round(days) * DAY_MS : null;
  const overDays = (dueMs !== null && refundMs !== null && refundMs > dueMs)
    ? Math.round((refundMs - dueMs) / DAY_MS) : 0;
  return { collectMs, days, refundMs, dueMs, overDays, dueIso: dueMs === null ? '' : fmtDate(dueMs) };
}

/** 材料自身的口径日：全表最晚的那一天（用来判断"已过应退截止日仍未退清"） */
function latestDateMs(rows) {
  let max = null;
  for (const it of rows) {
    for (const role of ['collectDate', 'refundDate']) {
      const ms = parseDateMs(it[role]);
      if (ms !== null && (max === null || ms > max)) max = ms;
    }
  }
  return max;
}

/** 台账截止日（可选列）：填了就用它当口径日；没填就退回"表内最晚日期" */
function cutoffDateMs(rows) {
  let max = null;
  for (const it of rows) {
    const ms = parseDateMs(it.asOfDate);
    if (ms !== null && (max === null || ms > max)) max = ms;
  }
  return max;
}

/** 同一合同同一押金类型、且退还金额大于 0 的行：第 2 行及以后都算重复退还 */
function duplicateRefundInfo(rows) {
  const first = new Map();
  const dups = new Map();
  for (const it of rows) {
    const refund = num(it, 'refundAmt');
    const contract = cell(it.contract);
    const type = cell(it.depositType);
    if (!contract || !type || refund === null || refund <= TOL) continue;
    const key = `${contract}|${type}`;
    if (first.has(key)) dups.set(it.line, first.get(key));
    else first.set(key, it.line);
  }
  return { first, dups };
}

/* ============================ 免费档执行的检查项 ============================ */

function expectRefundIssue(it) {
  const collect = num(it, 'collectAmt');
  const deduct = num(it, 'deductAmt');
  const stated = num(it, 'expectRefund');
  if (collect === null || deduct === null || stated === null) return null;
  const expect = round2(collect - deduct);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '应退金额复算不符', line: it.line,
    message: `${who(it)}的应退金额是 ${stated.toFixed(2)}，按 收取金额 ${collect.toFixed(2)} − 扣除金额 ${deduct.toFixed(2)} = `
      + `${expect.toFixed(2)}，应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '应退金额是打给对方的钱。先看是不是「扣除金额没从应退里减掉」（差额正好等于扣除金额），'
      + '再看是不是收取金额改过而应退金额没跟着重算 —— 两个方向都按合同与扣除依据逐笔对。',
    stated, expect, diff: round2(stated - expect),
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

function deductBasisIssue(it) {
  const deduct = num(it, 'deductAmt');
  if (deduct === null || deduct <= TOL) return null;
  const basis = cell(it.deductBasis);
  const empty = basis === '' || isBlank(basis) || PLACEHOLDER.test(basis);
  if (!empty && BASIS_WORDS.test(basis)) return null;
  const why = empty
    ? `「${LABELS.deductBasis}」是空的或占位符（${basis || '空'}）`
    : `「${LABELS.deductBasis}」只写了「${basis}」，没有写明扣除事由（违约金 / 损坏赔偿 / 欠费 等）`;
  return {
    level: 'P0', category: '扣除金额缺少有效依据', line: it.line,
    message: `${who(it)}扣了 ${deduct.toFixed(2)}，但${why} —— 凭这一栏对不上任何凭证，对方不会认这笔扣款。`,
    advice: '把凭证形式写进「扣除依据」：违约金要有合同条款号、损坏赔偿要有维修单 / 报价单编号、'
      + '欠费要有催缴单或对账确认；拿不出依据的扣除先冲回，不要直接从应退金额里扣掉。',
    deduct, basis_text: basis,
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

function deductLimitIssue(it) {
  const deduct = num(it, 'deductAmt');
  const collect = num(it, 'collectAmt');
  if (deduct === null || collect === null) return null;
  if (collect <= TOL) return null;               // 本金本身非正数：交给"金额为负"那条说，别在这里算上限
  if (deduct <= collect + TOL) return null;
  return {
    level: 'P0', category: '扣除金额超过收取金额', line: it.line,
    message: `${who(it)}的扣除金额 ${deduct.toFixed(2)} 超过了收取金额 ${collect.toFixed(2)}，`
      + `超出 ${round2(deduct - collect).toFixed(2)} —— 押金本身只有这么多，扣不到这个数。`,
    advice: '超出部分不是押金能覆盖的：要么把超出金额另开应收（欠费 / 违约金单独挂账），'
      + '要么这一格的金额抄错了（常见的是一行写成了两行的合计）。先确认押金本金到底是多少。',
    deduct, collect, diff: round2(deduct - collect),
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

function refundOverdueIssue(it) {
  const info = dueInfoOf(it);
  if (info.dueMs === null) return null;
  if (info.overDays > 0 && info.refundMs !== null) {
    return {
      level: 'P1', category: '退还日期超过约定期限', line: it.line,
      message: `${who(it)}的应退截止日是 ${info.dueIso}（收取日期 ${cell(it.collectDate)} + 约定退还期限 `
        + `${info.days} 天），实际退还日期是 ${cell(it.refundDate)}，超期 ${info.overDays} 天。`,
      advice: '超期退还会引发资金占用争议，也可能触发合同里的逾期责任。先确认是不是流程卡在审批，'
        + '再把起算日与期限天数按合同原文核一遍（本工具只按你填的天数复算）。',
      due_date: info.dueIso, refund_date: cell(it.refundDate), over_days: info.overDays,
      basis: `原文第 ${it.line} 行：${it.raw}`,
    };
  }
  return null;
}

function refundUnsettledIssue(it, baseMs) {
  const balance = num(it, 'balance');
  const info = dueInfoOf(it);
  if (balance === null || balance <= TOL) return null;
  if (info.dueMs === null || baseMs === null) return null;
  if (info.refundMs !== null) return null;          // 已退过但没退完：交给上一条按超期天数说
  if (baseMs <= info.dueMs) return null;            // 还没到应退截止日：不算超期
  const overDays = Math.round((baseMs - info.dueMs) / DAY_MS);
  return {
    level: 'P1', category: '已过约定退还期限仍未退清', line: it.line,
    message: `${who(it)}的应退截止日是 ${info.dueIso}，台账余额仍有 ${balance.toFixed(2)} 且没有退还日期`
      + `（按材料内最晚日期 ${fmtDate(baseMs)} 算，已过截止日 ${overDays} 天）。`,
    advice: '这笔钱还趴在你的账上。先按合同确认该不该退、退给谁，再排进付款计划；'
      + '若确实要留作质保金或抵扣，请把「已结转金额」与依据写清，不要让余额长期无说明地挂着。',
    due_date: info.dueIso, balance, over_days: overDays,
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

function duplicateRefundIssue(rows) {
  const out = [];
  const { dups } = duplicateRefundInfo(rows);
  for (const it of rows) {
    if (!dups.has(it.line)) continue;
    const refund = num(it, 'refundAmt');
    out.push({
      level: 'P0', category: '同一合同同一押金类型重复退还', line: it.line,
      message: `${who(it)}在第 ${dups.get(it.line)} 行已经退过一次押金，第 ${it.line} 行又退了一次`
        + `${refund !== null ? `（本行退还金额 ${refund.toFixed(2)}）` : ''} —— 同一笔押金退了两次就是重复付款。`,
      advice: '先看是不是重复粘贴（台账里最常见），或把同一笔押金按两个合同号 / 两次退款登记了。'
        + '确属分次退还的，请把每次退还拆成同一行内的多次记录或另附退款明细，不要用两行都挂同一份合同。',
      refund: refund === null ? null : refund,
      basis: `原文第 ${it.line} 行：${it.raw}`,
    });
  }
  return out;
}

function balanceIssue(it) {
  const collect = num(it, 'collectAmt');
  const refund = num(it, 'refundAmt');
  const carry = num(it, 'carryAmt');
  const stated = num(it, 'balance');
  if (collect === null || refund === null || carry === null || stated === null) return null;
  const expect = round2(collect - refund - carry);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '台账余额与收取-退还-结转不符', line: it.line,
    message: `${who(it)}的台账余额是 ${stated.toFixed(2)}，按 收取金额 ${collect.toFixed(2)} − 退还金额 `
      + `${refund.toFixed(2)} − 已结转金额 ${carry.toFixed(2)} = ${expect.toFixed(2)}，`
      + `应为 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '台账余额是"这笔押金还挂在账上多少"。差额常见于三处：扣掉的钱没记进「已结转金额」、'
      + '退还金额没从余额里减、或余额是上期数没跟着本期变动重算。改完请与押金台账科目余额核对。',
    stated, expect, diff: round2(stated - expect),
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

function negativeIssue(it) {
  const out = [];
  for (const [role, label2] of NEGATIVE_ROLES) {
    const v = num(it, role);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '金额为负', line: it.line,
        message: `${who(it)}的「${label2}」是 ${v.toFixed(2)}（负数）。`,
        advice: '这几列按口径都是"正数金额"。负号多半是粘贴时符号掉了、或公式取反了；'
          + '负数会顺着三个算式把应退金额与台账余额一起算错。',
        basis: `原文第 ${it.line} 行：${it.raw}`,
      });
    }
  }
  return out;
}

function blankIssue(rows) {
  const out = [];
  for (const it of rows) {
    for (const role of CELL_REQUIRED) {
      const s = cell(it[role]);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这一行就核不动。本工具不会用 0 或默认值替你填：金额列填 0.00 表示"确实没有"，'
            + '留空表示"不知道" —— 这两者不能混（扣除依据 / 退还日期 / 备注确实没有时可以留空）。',
          basis: `原文第 ${it.line} 行：${it.raw}`,
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const p = payload && typeof payload === 'object' ? payload : null;
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient([`入参不是对象或数组（收到的是 ${typeof payload}）`]);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient(['没有收到押金保证金台账与退还明细表正文（text）—— 请把「合同编号 / 承租方 / 项目 / '
      + '押金类型 / 收取日期 / 收取金额 / 扣除金额 / 扣除依据 / 应退金额 / 退还日期 / 退还金额 / 已结转金额 / '
      + '台账余额 / 约定退还期限」这张表（含表头）贴进来']);
  }
  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['表里没有任何内容（空白行不算材料）']);
  }
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `押金保证金台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient(['表里只有表头，没有任何押金明细行']);
  }
  // 一行能核的最低要求：收取金额与应退金额读得出数字（台账余额读不出时由"关键字段缺失"那条报，
  // 不把整行静默丢掉）
  const workable = t.items.filter((it) => num(it, 'collectAmt') !== null
    && num(it, 'expectRefund') !== null);
  if (!workable.length) {
    return insufficient(['每一行的「收取金额 / 应退金额」都读不出数字（空或占位符），一行都核不动']);
  }

  const rows = workable;
  const asOfMs = cutoffDateMs(rows);
  const baseMs = asOfMs === null ? latestDateMs(rows) : asOfMs;
  const dupInfo = duplicateRefundInfo(rows);


  const projects = new Set();
  const contracts = new Set();
  const periods = new Set();
  for (const it of rows) {
    projects.add(cell(it.project));
    contracts.add(cell(it.contract));
    const ms = parseDateMs(it.collectDate);
    periods.add(ms === null ? '(未填收取日期)' : monthOf(ms));
  }

  const findings = [];
  for (const it of rows) {
    const a = expectRefundIssue(it); if (a) findings.push(a);
    const b = deductBasisIssue(it); if (b) findings.push(b);
    const c = deductLimitIssue(it); if (c) findings.push(c);
    const d = refundOverdueIssue(it); if (d) findings.push(d);
    const e = refundUnsettledIssue(it, baseMs); if (e) findings.push(e);
    const f = balanceIssue(it); if (f) findings.push(f);
    findings.push(...negativeIssue(it));

  }
  findings.push(...blankIssue(rows));
  findings.push(...duplicateRefundIssue(rows));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const columnTotals = {};
  for (const role of SUM_ROLES) columnTotals[role] = sumRole(rows, role);

  let outstandingTotal = 0;
  for (const it of rows) {
    const v = num(it, 'balance');
    if (v !== null && v > 0) outstandingTotal += v;
  }

  const result = {
    status: 'success',
    service_type: 'RENT_DEPOSIT_REFUND_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: rows.length,
      contracts: contracts.size,
      projects: projects.size,
      periods: periods.size,
      base_date: baseMs === null ? '' : fmtDate(baseMs),
      cutoff_source: asOfMs === null
        ? '表内最晚日期（未提供「台账截止日」列；表内只有收取日期时，本工具不会凭空断定已超期）'
        : '台账截止日列',
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      column_totals: columnTotals,
      collect_total: columnTotals.collectAmt,
      deduct_total: columnTotals.deductAmt,
      expect_refund_total: columnTotals.expectRefund,
      refund_total: columnTotals.refundAmt,
      carry_total: columnTotals.carryAmt,
      balance_total: columnTotals.balance,
      outstanding_total: round2(outstandingTotal),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: rows.length,
      contracts: contracts.size,
      projects: projects.size,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: NOTE_FREE,
    disclaimer: '只核"应退金额 = 收取金额 − 扣除金额"、"台账余额 = 收取金额 − 退还金额 − 已结转金额"与'
      + '"应退截止日 = 收取日期 + 约定退还期限"这类**表内勾稽**，不判断押金该收多少、扣除依据是否合法有效、'
      + '押金是否真的收到或退还（以租赁合同、招标文件与银行流水为准）；'
      + '每条结论都带原文行号与合同编号，可由第三方用同一份输入复算。',
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, REQUIRED, CELL_REQUIRED, TOL,
};
