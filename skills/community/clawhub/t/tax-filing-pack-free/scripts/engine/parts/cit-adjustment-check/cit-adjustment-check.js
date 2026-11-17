/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * cit-adjustment-check.js —— 企业所得税纳税调整核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每年汇算清缴（年度申报）之前**，财务要把会计利润
 * 逐项调成**应纳税所得额**：利润总额 + 纳税调增 − 纳税调减 = 应纳税所得额。
 * 而**限额类项目**（业务招待费、广告费和业务宣传费、公益性捐赠支出）都有**法定上限**，
 * 超限部分必须调增；漏调 = 少缴（要补税、加滞纳金），多调 = 多缴（白掏钱）。
 * 这张「企业所得税纳税调整表」是年度申报表的底稿，**每一格都能用手算复现** ——
 * 所以对错完全能机械判定。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应纳税所得额 = 利润总额 + 调增合计 − 调减合计
 *   调增合计     = 各明细项「调增金额」之和
 *   调减合计     = 各明细项「调减金额」之和
 *   合计行       = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 下面 3 条限额公式**只属于完整档（付费）**，本免费档**不执行**：既不参与任何计算，
 *    也不写进返回值（它们只作为"未执行的检查项"列在 CHECKS_WITHHELD / scope.checks_not_run）。
 *    把它们留在返回值里会被当成"限额已核对" ⇒ 虚假保证，是本仓库最不能接受的错。
 *      业务招待费扣除上限     = min(发生额 × 60%, 营业收入 × 5‰)
 *      广告费和业务宣传费上限 = 营业收入 × 15%
 *      公益性捐赠支出上限     = 利润总额 × 12%
 * ⚠️ 本工具**不判断**调整事项的税法依据是否成立、也**不判断**企业是否真的适用某项优惠税率：
 *    税法口径以税法与主管税务机关为准。
 */

const CHECKS_GIVEN = [
  '应纳税所得额复算（利润总额 + 调增合计 − 调减合计 = 应纳税所得额）',
  '调增/调减合计 = 各明细项之和复算',
  '合计行逐列复核',
  '同一调整项目重复行检测',
  '空白与占位符检测',
  '调增/调减金额为负（口径异常）检测',
];

const CHECKS_WITHHELD = [
  '业务招待费超限额（发生额 60% 与营业收入 5‰ 孰低）未足额调增提示',
  '广告费和业务宣传费超过营业收入 15% 未足额调增提示',
  '公益性捐赠支出超过利润总额 12% 未足额调增提示',
  '应纳税所得额为负却算出应纳税额检测',
  '适用税率偏离法定 25%（小微 20%/5%、高新 15%）提示',
];

const OUT_OF_SCOPE = [
  '判断各项纳税调整的税法依据是否成立（如扣除凭证、资产损失清单申报、不征税收入条件），请以税法与主管税务机关口径为准',
  '处理以前年度亏损弥补、境外所得抵免、税收优惠备案与季度预缴衔接',
  '代企业填写企业所得税年度纳税申报表或与电子税务局对接（本工具只核底稿表内的算术与勾稽）',
  '读取财务/报税系统导出文件（需要你先导出成文本贴进来）',
];

/* 法定与常见优惠口径：仅供"明显偏离"时提示，**不是**税率适用性判断
   （税率偏离提示属完整档；免费档只把 RATE_REFS 作为参考值随 scope 返回，不对税率做任何判定） */
const STATUTORY_RATE = 0.25;
const RATE_REFS = [0.25, 0.20, 0.15, 0.05];
/* ⚠️ 这里**刻意不再定义**限额比例常量（招待费 60%/5‰、广告费 15%、捐赠 12%）：
   免费档不执行限额类判断，留着常量就会被写进返回值（旧的 limit_rates），
   调用方/买家会以为限额已经核对过 —— 那是虚假保证。限额公式只在完整档里实现。 */

const SAMPLE_TEXT = [
  '行次\t项目\t金额\t调增金额\t调减金额',
  '1\t利润总额\t1000000.00\t\t',
  '2\t营业收入\t8000000.00\t\t',
  '3\t适用税率\t25%\t\t',
  '4\t业务招待费\t100000.00\t60000.00\t',
  '5\t广告费和业务宣传费\t900000.00\t0.00\t',
  '6\t公益性捐赠支出\t110000.00\t0.00\t',
  '7\t税收滞纳金\t30000.00\t30000.00\t',
  '8\t国债利息收入\t50000.00\t\t50000.00',
  '9\t研发费用加计扣除\t200000.00\t\t200000.00',
  '10\t调增合计\t90000.00\t\t',
  '11\t调减合计\t250000.00\t\t',
  '12\t应纳税所得额\t840000.00\t\t',
  '13\t应纳税额\t210000.00\t\t',
  '14\t合计\t1390000.00\t90000.00\t250000.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**。
  //    「调增金额」「调减金额」里都含「金额」，「账载金额」也含「金额」——
  //    所以 amount 必须排在 addAmt / subAmt **之后**，否则「调增金额」整列会被
  //    「金额」这个宽泛角色抢走（表现为：不报缺列，只是把调增金额当成"金额"算，静默算错）。
  seq: ['行次', '序号'],
  period: ['所属期', '纳税所属期', '税款所属期', '纳税年度', '期间', '年度'],
  addAmt: ['调增金额', '纳税调增金额', '调增额', '调增'],
  subAmt: ['调减金额', '纳税调减金额', '调减额', '调减'],
  amount: ['账载金额', '本期金额', '金额'],
  item: ['调整项目', '项目名称', '项目'],
};

const LABELS = {
  seq: '行次', period: '所属期', item: '项目', amount: '金额',
  addAmt: '调增金额', subAmt: '调减金额',
};

const REQUIRED = ['item', 'amount', 'addAmt', 'subAmt'];
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

/* 表内"要素行"：不是调整明细，而是这张表的其他已知格 */
const ELEMENTS = [
  ['taxableIncome', ['应纳税所得额', '纳税调整后所得']],
  ['taxPayable', ['应纳税额', '应纳所得税额', '应纳企业所得税额']],
  ['profitTotal', ['利润总额', '会计利润总额']],
  ['revenue', ['营业收入', '营业总收入', '收入总额']],
  ['rate', ['适用税率', '所得税税率', '税率']],
];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（不会给"未发现问题"的结论）。',
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
  if (isBlank(raw)) return null;
  let s = String(raw).trim().replace(/[,，\s¥￥$]/g, '');
  const wrapped = /^\(.*\)$/.test(s);              // (1234.00) 是会计上的负数写法
  if (wrapped) s = s.slice(1, -1);
  s = s.replace(/%$/, '');
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return wrapped ? -n : n;
}

/** 比率归一化成小数：`25%` ⇒ 0.25；`0.25` ⇒ 0.25；`25` ⇒ 0.25 */
const round2 = (n) => Math.round(n * 100) / 100;

/** 去掉空白与全角括号后的项目名，用于分类 */
function nameOf(v) {
  return String(v === undefined || v === null ? '' : v).replace(/[\s（）()：:]/g, '');
}

/** 要素行归类：利润总额 / 营业收入 / 适用税率 / 应纳税所得额 / 应纳税额 */
function elementOf(item) {
  const s = nameOf(item);
  if (!s) return null;
  for (const [role, keys] of ELEMENTS) {
    if (keys.some((k) => s.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 段合计行归类：调增合计 / 调减合计 */
function sectionTotalOf(item) {
  const s = nameOf(item);
  if (!s) return null;
  if (s.indexOf('调增合计') >= 0 || s.indexOf('纳税调整增加额') >= 0 || s.indexOf('调增项目合计') >= 0) return 'add';
  if (s.indexOf('调减合计') >= 0 || s.indexOf('纳税调整减少额') >= 0 || s.indexOf('调减项目合计') >= 0) return 'sub';
  return null;
}

/** 调整明细行：既不是要素行，也不是段合计行 */
function isDetail(row) {
  const n = nameOf(row && row.item);
  if (!n) return true;                     // 项目为空的行仍按明细行处理，交给空白检测报出来
  return !elementOf(n) && !sectionTotalOf(n);
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  const empty = {
    items: [], totals: {}, elementRows: {},
    addTotalRow: null, subTotalRow: null, missingColumns: null,
  };
  if (!raw.length) return empty;
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  const elementRows = {};
  let addTotalRow = null;
  let subTotalRow = null;
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'item' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    const iName = String(row.item === undefined ? '' : row.item).trim();
    if (isTotal) { totals.row = row; totals.line = i + 1; continue; }
    const sec = sectionTotalOf(iName);
    if (sec === 'add') { if (!addTotalRow) addTotalRow = row; continue; }
    if (sec === 'sub') { if (!subTotalRow) subTotalRow = row; continue; }
    const el = elementOf(iName);
    if (el && !elementRows[el]) elementRows[el] = row;
    items.push(row);
  }
  return { items, totals, elementRows, addTotalRow, subTotalRow, missingColumns };
}

const who = (it) => {
  const n = it && it.item ? String(it.item).trim() : '';
  return n ? `${n}（第 ${it.line} 行）` : `第 ${it && it.line} 行`;
};

function sumOf(rows, role) {
  let sum = 0;
  let n = 0;
  for (const r of rows) {
    const v = normNumber(r[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  return { sum: round2(sum), n };
}

/* =============================== 免费档检查项 =============================== */

/** 【免费·6-1】调增/调减栏不能填负数（负数=两栏填反或口径混在一列） */
function checkNegative(it) {
  const out = [];
  if (elementOf(it.item)) return out;
  for (const pair of [['addAmt', '调增金额'], ['subAmt', '调减金额']]) {
    const v = normNumber(it[pair[0]]);
    if (v !== null && v < -TOL) {
      out.push({
        level: 'P0', category: '调增/调减金额为负（口径异常）', line: it.line,
        message: `${who(it)}的「${pair[1]}」是 ${v.toFixed(2)}（负数）—— 调增/调减只填正数，`
          + '负数说明调增调减两栏填反了，或把两个口径挤进了一列。',
      });
    }
  }
  return out;
}

/** 【免费·6-2】空白与占位符 */
function checkBlankRow(it) {
  const out = [];
  if (isBlank(it.item)) {
    const s = String(it.item === undefined ? '' : it.item).trim();
    out.push({
      level: 'P0', category: '空白与占位符', line: it.line,
      message: `第 ${it.line} 行的「项目」是空的或占位符（${s || '空'}）—— 认不出这是哪一项调整，`
        + '这一行既不参与任何勾稽，也无法追到具体事项。',
    });
    return out;
  }
  if (elementOf(it.item)) {
    if (isBlank(it.amount)) {
      out.push({
        level: 'P0', category: '空白与占位符', line: it.line,
        message: `${who(it)}的「金额」是空的或占位符 —— 这一格是整张表勾稽的起点，缺了就核不动。`,
      });
    }
    return out;
  }
  if (isBlank(it.amount) && isBlank(it.addAmt) && isBlank(it.subAmt)) {
    out.push({
      level: 'P0', category: '空白与占位符', line: it.line,
      message: `${who(it)}的金额、调增金额、调减金额全是空的或占位符 —— 这一行没有任何可核对的数据。`,
    });
  }
  return out;
}

/** 【免费·6-3】应纳税所得额 = 利润总额 + 调增合计 − 调减合计 */
function checkTaxableIncome(t) {
  const out = [];
  const profitRow = t.elementRows.profitTotal;
  const taxableRow = t.elementRows.taxableIncome;
  const profit = profitRow ? normNumber(profitRow.amount) : null;
  const addT = t.addTotalRow ? normNumber(t.addTotalRow.amount) : null;
  const subT = t.subTotalRow ? normNumber(t.subTotalRow.amount) : null;
  const stated = taxableRow ? normNumber(taxableRow.amount) : null;
  if (!taxableRow || profit === null || addT === null || subT === null || stated === null) return out;
  const expect = round2(profit + addT - subT);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应纳税所得额与勾稽不符', line: taxableRow.line,
    message: `利润总额 ${profit.toFixed(2)} + 调增合计 ${addT.toFixed(2)} − 调减合计 ${subT.toFixed(2)}`
      + ` = ${expect.toFixed(2)}，但表里「应纳税所得额」填的是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)} —— 这一格错了，全年应纳税额就跟着错。`,
  });
  return out;
}

/** 【免费·6-4】调增合计 / 调减合计 = 各明细项之和 */
function checkAdjustTotals(t) {
  const out = [];
  const details = t.items.filter(isDetail);
  const pairs = [
    { row: t.addTotalRow, role: 'addAmt', label: '调增' },
    { row: t.subTotalRow, role: 'subAmt', label: '调减' },
  ];
  for (const p of pairs) {
    if (!p.row) continue;
    const stated = normNumber(p.row.amount);
    if (stated === null) continue;
    const agg = sumOf(details, p.role);
    if (!agg.n) continue;
    if (Math.abs(stated - agg.sum) <= TOL) continue;
    out.push({
      level: 'P0', category: `${p.label}合计与各明细项之和不符`, line: p.row.line,
      message: `${p.label}合计填的是 ${stated.toFixed(2)}，各明细项「${LABELS[p.role]}」相加是 ${agg.sum.toFixed(2)}，`
        + `相差 ${round2(stated - agg.sum).toFixed(2)} —— 合计行不是独立的数，它只能是明细之和。`,
    });
  }
  return out;
}

/** 【免费·6-5】合计行逐列复核（每一列都要等于明细行之和） */
function checkTotalRow(t) {
  const out = [];
  if (!t.totals || !t.totals.row) return out;
  const details = t.items.filter(isDetail);
  for (const role of ['amount', 'addAmt', 'subAmt']) {
    const stated = normNumber(t.totals.row[role]);
    if (stated === null) continue;
    const agg = sumOf(details, role);
    if (!agg.n) continue;
    if (Math.abs(stated - agg.sum) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: t.totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${agg.sum.toFixed(2)}，`
        + `相差 ${round2(stated - agg.sum).toFixed(2)}。`,
    });
  }
  return out;
}

/** 【免费·6-6】同一调整项目出现多行 */
function checkDuplicates(t) {
  const out = [];
  const seen = new Map();
  for (const it of t.items) {
    const key = nameOf(it.item);
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一调整项目重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现过，第 ${it.line} 行又列了一次 —— `
          + '同一事项被拆成两行，很容易只调增一次或者重复调增。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 【完整·1】业务招待费：扣除上限 = min(发生额 × 60%, 营业收入 × 5‰) */
/** 【完整·2】广告费和业务宣传费：超过营业收入 15% 的部分本年必须调增 */
/** 【完整·3】公益性捐赠支出：超过利润总额 12% 的部分应调增（且不得结转） */
/** 【完整·4】应纳税所得额为负（亏损）却算出正的应纳税额 */
/** 【完整·5】适用税率偏离法定 25% 与常见优惠口径 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到纳税调整表正文（text）—— 请把「行次 / 项目 / 金额 / 调增金额 / 调减金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `纳税调整表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何调整项目明细行 —— 请把明细行一起贴进来');
  }

  const findings = [];
  for (const f of checkTaxableIncome(t)) findings.push(f);
  for (const f of checkAdjustTotals(t)) findings.push(f);
  for (const f of checkTotalRow(t)) findings.push(f);
  for (const f of checkDuplicates(t)) findings.push(f);
  for (const it of t.items) {
    for (const f of checkBlankRow(it)) findings.push(f);
    for (const f of checkNegative(it)) findings.push(f);
  }
  if (t.addTotalRow) for (const f of checkNegative(t.addTotalRow)) findings.push(f);
  if (t.subTotalRow) for (const f of checkNegative(t.subTotalRow)) findings.push(f);


  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let periods = 0;
  const seenPeriod = new Set();
  for (const it of t.items) {
    const v = it.period === undefined ? '' : String(it.period).trim();
    if (v && !isBlank(v)) seenPeriod.add(v);
  }
  periods = seenPeriod.size || 1;
  const rows = t.items.length + (t.totals && t.totals.row ? 1 : 0)
    + (t.addTotalRow ? 1 : 0) + (t.subTotalRow ? 1 : 0);

  const result = {
    status: 'success',
    service_type: 'CIT_TAX_ADJUSTMENT_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows,
      periods,
      adjustment_rows: t.items.filter(isDetail).length,
      tolerance: TOL,
      rate_refs: RATE_REFS,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows,
      periods,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`
      + '**限额类判断本版本未执行**（业务招待费、广告费和业务宣传费、公益性捐赠支出的扣除上限均未核对），'
      + '不要据本结果认为限额已经查过。',
    disclaimer: '只核「利润总额 + 调增 − 调减 = 应纳税所得额」「合计 = 明细之和」这类表内勾稽；'
      + '本版本**不核对**限额类扣除上限（业务招待费 min(发生额 60%, 营业收入 5‰)、广告费和业务宣传费 15% 营业收入、'
      + '公益性捐赠 12% 利润总额）—— 这些只是未执行的检查项，见 scope.checks_not_run，'
      + '本结果**不能**被理解为"限额已核对"；'
      + '**不判断**调整事项的税法依据是否成立、也不判断优惠税率是否真的适用（以税法与主管税务机关口径为准）；'
      + `法定税率参考值 ${STATUTORY_RATE * 100}%。结论可由第三方用同一份输入复算。`,
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
