/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * recruitment-agency-fee-check.js —— 猎头服务费与保证期退款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**企业 HR / 财务在收到猎头供应商的服务费账单、准备付款或月末对账时**。
 * 猎头费的每一格都能手算复现，而每次都会吵的就是这几处：
 *   · 服务费不是按「候选人年薪 × 合同约定的服务费率」算的（年薪口径换了、费率抄错档位）；
 *   · 候选人在**保证期内离职**，按合同应当按未满天数比例退款，账单里却没退或少退；
 *   · 账单合计行是手打的，明细改了合计没跟着改；
 *   · 同一个候选人在同一供应商同一月份被计了两遍费（同一人重复建行）；
 *   · 实际收的服务费率高于合同费率上限；
 *   · 关键格留着空 / 「待填」，金额是负数。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   服务费     = 候选人年薪 × 服务费率（费率按百分数填：20% 与 20 都表示 20%）
 *   应退比例   = (保证期天数 − 已服务天数) ÷ 保证期天数      —— 仅当「保证期内离职」
 *   应退金额   = 服务费 × 应退比例
 *   非保证期内离职 ⇒ 应退比例与应退金额都应为 0
 *   账单合计行 = 各明细行逐列相加（服务费 / 应退金额 / 实退金额）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），不读环境变量、不写文件。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD），其中最后一项是免费档**结构上做不到**的：
 * 「跨供应商跨月汇总台账 + 按差异金额排序的处理清单 + 差异归因（年薪口径 / 费率档位 / 保证期天数 / 退款比例）」。
 *
 * ⚠️ 本工具**不判断**年薪口径本身对不对（税前/税后、含不含奖金、12 薪还是 13 薪），
 *    也不判断合同里的费率档位与保证期长度是否合法 —— 表里的年薪、费率、保证期天数、离职标记
 *    一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号与候选人列出来。
 *
 * ⚠️ 付费项用**形态 B**：付费实现集中在文件里那段「完整档（付费）检查区」注释之后的区域，
 *    并由 run() 里**只声明一次**的档位开关控制。注释里不要写出开关那一行的字面量：
 *    `strip_free_engine` 的残渣断言是**纯字符串包含**判断，写了就会被判『没删干净』而整包跳过。
 */

const CHECKS_GIVEN = [
  '服务费复算（候选人年薪 × 服务费率 = 服务费，逐行用同一口径复算）',
  '保证期退款复算（保证期内离职按未满天数折算应退比例与应退金额；非保证期内离职时两者都应为 0）',
  '账单合计勾稽（合计行的服务费 / 应退金额 / 实退金额 = 各明细行逐列相加）',
  '同一候选人重复计费检测（同一供应商 + 同一候选人 + 同一月份出现多行）',
  '服务费率超合同上限检测（服务费率 > 合同费率上限）',
  '关键字段缺失 / 占位符 / 负数检测（空白、「待填」这类占位符、负金额）',
];

const CHECKS_WITHHELD = [
  '跨供应商跨月汇总台账（按供应商 × 月份汇总服务费 / 应退 / 实退 / 待退，用于月末合并对账）',
  '按差异金额排序的处理清单（每条带原文行号、候选人与供应商，可直接当待办清单用）',
  '实退与应退差额判定（应退未退 / 实退多于应退，逐行报出差额）',
  '保证期天数档位判定（不在常见约定档位 30/45/60/90/120/180/365 内即提示）',
  '退款口径矛盾与归因（保证期内离职却已服务满保证期天数、未按全额退款；并把差异归因到年薪口径 / 费率档位 / 保证期天数 / 退款比例）',
];

const OUT_OF_SCOPE = [
  '判断年薪口径本身是否正确（税前还是税后、含不含奖金与股权、按 12 薪还是 13 薪折算）—— 以你填的年薪与服务费率为准',
  '判断猎头服务合同里的费率档位、保证期长度、退款比例公式是否合法或是否与合同一致（本工具按行业常见口径复算，不替合同做解释）',
  '判断候选人是否真的在保证期内离职、入职日期与离职日期是否真实（要拿离职证明与社保记录核，本工具不去查外部系统）',
  '计算个税 / 社保 / 增值税与发票税额，或处理外籍候选人、境外供应商等特殊结算口径',
  '读取 Excel / HR 系统 / 供应商 PDF 账单（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  ['所属月份', '猎头供应商', '候选人', '职位', '入职日期', '年薪', '服务费率', '服务费', '合同费率上限',
    '保证期天数', '保证期内离职', '已服务天数', '应退比例', '应退金额', '实退金额'].join('\t'),
  ['2026-01', '智联猎头', '张伟', '技术总监', '2025-11-01', '600000.00', '22%', '132000.00', '25%',
    '90', '否', '120', '0%', '0.00', '0.00'].join('\t'),
  ['2026-01', '智联猎头', '李娜', '财务经理', '2025-12-01', '360000.00', '20%', '72000.00', '20%',
    '90', '是', '45', '50%', '36000.00', '36000.00'].join('\t'),
  ['2026-01', '伯乐猎头', '王强', '销售总监', '2025-10-15', '480000.00', '25%', '120000.00', '25%',
    '180', '否', '200', '0%', '0.00', '0.00'].join('\t'),
  ['2026-02', '智联猎头', '赵敏', '产品经理', '2026-01-05', '300000.00', '20%', '60000.00', '25%',
    '120', '是', '30', '75%', '45000.00', '45000.00'].join('\t'),
  ['2026-02', '伯乐猎头', '陈磊', '运营总监', '2025-12-20', '420000.00', '22%', '92400.00', '22%',
    '90', '是', '0', '100%', '92400.00', '92400.00'].join('\t'),
  ['2026-02', '智联猎头', '孙悦', '人力资源总监', '2026-01-20', '360000.00', '20%', '72000.00', '25%',
    '90', '否', '100', '0%', '0.00', '0.00'].join('\t'),
  ['合计', '', '', '', '', '', '', '548400.00', '', '', '', '', '', '173400.00', '173400.00'].join('\t'),
].join('\n');

/** 金额公差：1 分。超过就报差异，不超过就当作四舍五入。 */
const TOL = 0.01;
/** 比例公差：0.01 个百分点（表里比例常写成 2 位小数）。 */
const RATE_TOL = 0.01;
/** 常见约定保证期档位（自然日） */
const GUARANTEE_TIERS = [30, 45, 60, 90, 120, 180, 365];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)/;

const ADVICE = '把猎头服务费账单与保证期明细表（含表头）整段贴进来，Tab 分隔最稳：'
  + '可用 {"text": "…"}，或先跑 --sample 看需要哪些列。';

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的别名前面，
  //    否则宽泛别名会把具体那一列抢走（抢走不会报错，只会静默算错）。
  //    · rateCap 必须排在 rate 前面（否则「合同费率上限」被「费率」抢走）；
  //    · rate 必须排在 fee 前面（否则「服务费率」被「服务费」抢走）；
  //    · leftInGuarantee 必须排在 guaranteeDays 前面（否则「保证期内离职」被「保证期」抢走）；
  //    · refundRate 必须排在 refundAmount 前面（否则「应退比例」被兜底的「应退」抢走）。
  period: ['所属月份', '结算月份', '服务月份', '账单月份', '所属期间', '月份', '期间'],
  vendor: ['猎头供应商', '供应商名称', '猎头公司', '服务商', '供应商'],
  candidate: ['候选人姓名', '候选人', '人选', '被推荐人', '姓名'],
  position: ['职位名称', '招聘职位', '岗位名称', '职位', '岗位'],
  onboardDate: ['入职日期', '到岗日期', '入职时间', '到岗日', '入职'],
  annualSalary: ['候选人年薪', '年度薪酬', '税前年薪', '年度薪资', '年薪'],
  rateCap: ['合同费率上限', '合同费率', '费率上限', '合同上限', '约定上限'],
  rate: ['服务费率', '猎头费率', '收费比例', '佣金比例', '费率'],
  fee: ['服务费金额', '猎头服务费', '服务费', '猎头费'],
  leftInGuarantee: ['保证期内离职', '是否保证期内离职', '保证期内是否离职', '保内离职'],
  guaranteeDays: ['保证期天数', '质保期天数', '保证期', '质保期'],
  servedDays: ['已服务天数', '在职天数', '服务天数', '已工作天数'],
  refundRate: ['应退比例', '退款比例', '应退比率', '退款率'],
  refundAmount: ['应退金额', '应退服务费', '退款金额', '应退'],
  refundedAmount: ['实退金额', '已退金额', '实际退款', '已退'],
};

const LABELS = {
  period: '所属月份', vendor: '猎头供应商', candidate: '候选人', position: '职位',
  onboardDate: '入职日期', annualSalary: '年薪', rateCap: '合同费率上限', rate: '服务费率',
  fee: '服务费', leftInGuarantee: '保证期内离职', guaranteeDays: '保证期天数',
  servedDays: '已服务天数', refundRate: '应退比例', refundAmount: '应退金额',
  refundedAmount: '实退金额',
};

/** 列级必需：缺一列就**不给结论**（宁可说"材料不足"，也不拿 0 替你假设"这列没有"） */
const REQUIRED = ['period', 'vendor', 'candidate', 'annualSalary', 'rate', 'fee', 'rateCap',
  'guaranteeDays', 'leftInGuarantee', 'servedDays', 'refundRate', 'refundAmount'];
/** 行级必需：某一行的这些格空着（或写着"待填"这类占位符）就逐行报出来 */
const ROW_REQUIRED = ['period', 'vendor', 'candidate', 'annualSalary', 'rate', 'fee', 'rateCap',
  'guaranteeDays', 'leftInGuarantee', 'refundRate', 'refundAmount'];
/** 这些格子为负一定是错的（负数会把合计与退款比例一起带偏） */
const NEG_ROLES = ['annualSalary', 'fee', 'refundAmount', 'refundedAmount', 'servedDays',
  'guaranteeDays', 'refundRate', 'rate'];
/** 合计行逐列复核的列。**不含单价类（费率）与人数**：比率加总没有意义。 */
const SUM_ROLES = ['fee', 'refundAmount', 'refundedAmount'];

const fmt = (n) => (n === null || n === undefined ? '' : Number(n).toFixed(2));

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing || []),
    advice: advice || ADVICE,
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

const cell = (v) => (v === undefined || v === null ? '' : String(v).trim());

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header === undefined || header === null ? '' : header).replace(/[\s\u3000]/g, '');
  if (h === '') return null;
  for (const role of Object.keys(ROLES)) {
    for (const alias of ROLES[role]) {
      if (h.indexOf(alias) >= 0) return role;
    }
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim()
    .replace(/[¥￥$,\s\u3000，]/g, '')
    .replace(/％/g, '%')
    .replace(/[—–－]/g, '-');
  if (s === '' || s === '-') return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const num = (row, role) => normNumber(row ? row[role] : null);

/** 是否「保证期内离职」：认 是/Y/YES/TRUE/1/保证期内/保内；否/NO/0/FALSE 一律为否 */
function isInGuarantee(v) {
  const s = cell(v);
  if (s === '') return false;
  if (/否|no$|^n$|^0$|false/i.test(s)) return false;
  return /是|yes|true|^1$|保证期|保内|离职/i.test(s);
}

function isTotalRow(cells) {
  const n = Math.min(cells.length, 3);
  for (let i = 0; i < n; i++) {
    const c = String(cells[i] === undefined || cells[i] === null ? '' : cells[i]).replace(/[\s\u3000]/g, '');
    if (c !== '' && TOTAL_WORDS.test(c)) return true;
  }
  return false;
}

function parseTable(text) {
  const src = String(text === undefined || text === null ? '' : text);
  const lines = src.split(/\r?\n/);
  const out = { items: [], totals: {}, missingColumns: [], header: [], cols: {}, unmappedHeaders: [] };
  let headerAt = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].replace(/^\uFEFF/, '').trim() !== '') { headerAt = i; break; }
  }
  if (headerAt < 0) { out.missingColumns = REQUIRED.slice(); return out; }
  out.header = splitRow(lines[headerAt].replace(/^\uFEFF/, ''));
  out.header.forEach((h, i) => {
    const role = roleOf(h);
    if (!role) { if (h !== '') out.unmappedHeaders.push(h); return; }
    if (out.cols[role] === undefined) out.cols[role] = i;   // 先到先得，后一列不许覆盖前一列
  });
  out.missingColumns = REQUIRED.filter((r) => out.cols[r] === undefined);
  const roleNames = Object.keys(out.cols);
  for (let i = headerAt + 1; i < lines.length; i++) {
    const raw = lines[i].replace(/^\uFEFF/, '');
    if (raw.trim() === '') continue;
    const cells = splitRow(raw);
    const row = { line: i + 1, raw: raw.trim() };
    for (const role of roleNames) {
      const idx = out.cols[role];
      row[role] = cells[idx] === undefined ? '' : cells[idx];
    }
    if (isTotalRow(cells)) {
      out.totals.row = row;
      out.totals.line = row.line;
      out.totals.rows = (out.totals.rows || 0) + 1;
      continue;
    }
    out.items.push(row);
  }
  out.rows = out.items.length;
  return out;
}

function who(it) {
  const parts = [cell(it.period), cell(it.vendor), cell(it.candidate)].filter((x) => x !== '');
  return parts.join(' ') || '(未填候选人)';
}

/* ---------------- 免费档的 6 项检查 ---------------- */

/** 服务费 = 年薪 × 服务费率（费率按百分数填） */
function checkFeeRecompute(it) {
  const salary = num(it, 'annualSalary');
  const rate = num(it, 'rate');
  const fee = num(it, 'fee');
  if (salary === null || rate === null || fee === null) return null;   // 交给缺失检测，不猜默认值
  const expected = round2(salary * rate / 100);
  const diff = round2(fee - expected);
  if (Math.abs(diff) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '服务费复算不符', who: who(it),
    expected, actual: fee, diff, amount: diff,
    message: `第 ${it.line} 行 ${who(it)}：服务费 ${fmt(fee)} ≠ 年薪 ${fmt(salary)} × 服务费率 ${rate}% = ${fmt(expected)}（差 ${fmt(diff)}）`,
  };
}

/** 保证期退款：保内按未满天数折算；保外两者都应为 0 */
function checkRefundRecompute(it) {
  const out = [];
  const inG = isInGuarantee(it.leftInGuarantee);
  const fee = num(it, 'fee');
  const gDays = num(it, 'guaranteeDays');
  const sDays = num(it, 'servedDays');
  const rRate = num(it, 'refundRate');
  const rAmt = num(it, 'refundAmount');
  if (inG) {
    if (gDays === null || gDays <= 0 || sDays === null || fee === null) return out;
    const frac = Math.min(1, Math.max(0, (gDays - sDays) / gDays));
    const expPts = round2(frac * 100);
    const expAmt = round2(fee * frac);
    if (rRate !== null && Math.abs(rRate - frac * 100) > RATE_TOL) {
      out.push({
        line: it.line, level: 'P1', category: '退款比例不符', who: who(it),
        expected: expPts, actual: rRate, amount: round2(rRate - expPts),
        message: `第 ${it.line} 行 ${who(it)}：应退比例 ${rRate}% ≠ (保证期 ${gDays} 天 − 已服务 ${sDays} 天) ÷ ${gDays} 天 = ${expPts}%（差 ${round2(rRate - expPts)} 个百分点）`,
      });
    }
    if (rAmt !== null && Math.abs(rAmt - expAmt) > TOL) {
      out.push({
        line: it.line, level: 'P0', category: '应退金额复算不符', who: who(it),
        expected: expAmt, actual: rAmt, diff: round2(rAmt - expAmt), amount: round2(rAmt - expAmt),
        message: `第 ${it.line} 行 ${who(it)}：应退金额 ${fmt(rAmt)} ≠ 服务费 ${fmt(fee)} × 应退比例 ${expPts}% = ${fmt(expAmt)}（差 ${fmt(round2(rAmt - expAmt))}）`,
      });
    }
    return out;
  }
  // 非保证期内离职：按约定不该退钱，表里却填了金额
  if (rRate !== null && rRate > RATE_TOL) {
    out.push({
      line: it.line, level: 'P1', category: '非保证期内离职却填了应退比例', who: who(it), amount: rRate,
      message: `第 ${it.line} 行 ${who(it)}：标记为「非保证期内离职」，应退比例却填了 ${rRate}%（按约定应为 0）—— 要么是离职标记填错，要么是多退`,
    });
  }
  if (rAmt !== null && rAmt > TOL) {
    out.push({
      line: it.line, level: 'P1', category: '非保证期内离职却填了应退金额', who: who(it), amount: rAmt,
      message: `第 ${it.line} 行 ${who(it)}：标记为「非保证期内离职」，应退金额却填了 ${fmt(rAmt)}（按约定应为 0.00）`,
    });
  }
  return out;
}

/** 服务费率不得超过合同费率上限 */
function checkRateCap(it) {
  const rate = num(it, 'rate');
  const cap = num(it, 'rateCap');
  if (rate === null || cap === null) return null;
  const over = round2(rate - cap);
  if (over <= RATE_TOL) return null;
  return {
    line: it.line, level: 'P1', category: '服务费率超合同上限', who: who(it), amount: over,
    message: `第 ${it.line} 行 ${who(it)}：服务费率 ${rate}% 高于合同费率上限 ${cap}%（超 ${over} 个百分点）`,
  };
}

/** 关键字段缺失 / 占位符 / 负数（逐行） */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    const missing = [];
    for (const role of ROW_REQUIRED) {
      if (role === 'servedDays') continue;
      if (isBlank(it[role])) missing.push(LABELS[role] || role);
    }
    if (isInGuarantee(it.leftInGuarantee) && isBlank(it.servedDays)) missing.push(LABELS.servedDays);
    if (missing.length) {
      out.push({
        line: it.line, level: 'P1', category: '关键字段缺失', who: who(it), amount: 0,
        message: `第 ${it.line} 行 ${who(it)}：这些格是空的或写着占位符（本行因此不参与相应复算）：${missing.join('、')}`,
      });
    }
    const negs = [];
    for (const role of NEG_ROLES) {
      const v = num(it, role);
      if (v !== null && v < 0) negs.push(`${LABELS[role] || role}=${v}`);
    }
    if (negs.length) {
      out.push({
        line: it.line, level: 'P0', category: '负数金额', who: who(it), amount: 1,
        message: `第 ${it.line} 行 ${who(it)}：出现负数（${negs.join('、')}）—— 负数会把合计与退款比例一起带偏`,
      });
    }
  }
  return out;
}

/** 同一供应商 + 同一候选人 + 同一月份出现多行 ⇒ 可能重复计费 */
function checkDuplicates(items) {
  const out = [];
  const groups = {};
  const order = [];
  for (const it of items) {
    const name = cell(it.candidate);
    if (name === '') continue;
    const key = [cell(it.vendor), name, cell(it.period)].join('|');
    if (!groups[key]) { groups[key] = []; order.push(key); }
    groups[key].push(it);
  }
  for (const key of order) {
    const g = groups[key];
    if (g.length < 2) continue;
    const lines = g.map((x) => x.line).join('、');
    for (const it of g) {
      out.push({
        line: it.line, level: 'P0', category: '同一候选人重复计费', who: who(it), amount: 1,
        message: `第 ${it.line} 行 ${who(it)}：同一供应商 + 同一候选人 + 同一月份共出现 ${g.length} 行（原文第 ${lines} 行），服务费可能被重复计了一遍`,
      });
    }
  }
  return out;
}

/** 合计行勾稽：合计行各列 = 明细行逐列相加 */
function checkTotalRows(totals, items) {
  const out = [];
  const row = totals && totals.row;
  if (!row) return out;
  for (const role of SUM_ROLES) {
    const tv = num(row, role);
    if (tv === null) continue;
    let sum = 0;
    let any = false;
    for (const it of items) {
      const v = num(it, role);
      if (v !== null) { sum += v; any = true; }
    }
    if (!any) continue;
    sum = round2(sum);
    const diff = round2(tv - sum);
    if (Math.abs(diff) <= TOL) continue;
    out.push({
      line: row.line, level: 'P0', category: '账单合计不符', who: '合计行',
      expected: sum, actual: tv, diff, amount: Math.abs(diff),
      message: `第 ${row.line} 行（合计行）：${LABELS[role]} ${fmt(tv)} ≠ 各明细行相加 ${fmt(sum)}（差 ${fmt(diff)}）`,
    });
  }
  return out;
}

function run(payload) {
  const p = (payload && typeof payload === 'object' && !Array.isArray(payload)) ? payload : {};
  if (payload !== undefined && payload !== null
      && (typeof payload !== 'object' || Array.isArray(payload))) {
    return insufficient([`入参不是对象（收到的是 ${Array.isArray(payload) ? 'array' : typeof payload}）`]);
  }
  const text = (payload && typeof payload.text === 'string') ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient([
      '没有收到猎头服务费账单与保证期明细表正文（text）',
      '需要一张含表头的明细表：所属月份 / 猎头供应商 / 候选人 / 职位 / 入职日期 / 年薪 / 服务费率 / 服务费 / 合同费率上限 / 保证期天数 / 保证期内离职 / 已服务天数 / 应退比例 / 应退金额 / 实退金额',
    ]);
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `账单缺少必需列：${t.missingColumns.map((r) => LABELS[r] || r).join('、')}`,
      `已识别的表头：${t.header.join(' / ') || '(没认出表头)'}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient(['表里只有表头，没有任何候选人明细行']);
  }

  const findings = [];
  for (const it of t.items) {
    const fFee = checkFeeRecompute(it);
    if (fFee) findings.push(fFee);
    findings.push.apply(findings, checkRefundRecompute(it));
    const fCap = checkRateCap(it);
    if (fCap) findings.push(fCap);



  }
  findings.push.apply(findings, checkBlanks(t.items));
  findings.push.apply(findings, checkDuplicates(t.items));
  findings.push.apply(findings, checkTotalRows(t.totals, t.items));

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  let p0 = 0;
  let p1 = 0;
  let p2 = 0;
  for (const f of findings) {
    if (f.level === 'P0') p0 += 1;
    else if (f.level === 'P1') p1 += 1;
    else p2 += 1;
  }

  const months = new Set();
  const vendors = new Set();
  let feeTotal = 0;
  let refundTotal = 0;
  let refundedTotal = 0;
  for (const it of t.items) {
    months.add(cell(it.period));
    vendors.add(cell(it.vendor));
    const fee = num(it, 'fee');
    if (fee !== null) feeTotal += fee;
    const due = num(it, 'refundAmount');
    if (due !== null) refundTotal += due;
    const got = num(it, 'refundedAmount');
    if (got !== null) refundedTotal += got;
  }
  feeTotal = round2(feeTotal);
  refundTotal = round2(refundTotal);
  refundedTotal = round2(refundedTotal);

  const scopeChecks = CHECKS_GIVEN.slice();
  let note = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.withheld。`;

  const result = {
    status: 'success',
    service_type: 'RECRUITMENT_AGENCY_FEE_CHECK',
    scope: {
      checks: scopeChecks,
      rows: t.items.length,
      months: months.size,
      vendors: vendors.size,
      totals_row: Boolean(t.totals.row),
      totals_rows: t.totals.rows || 0,
      fee_total: feeTotal,
      refund_total: refundTotal,
      refunded_total: refundedTotal,
      outstanding_total: round2(refundTotal - refundedTotal),
      paid_in_total: feeTotal,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      months: months.size,
      vendors: vendors.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_out_of_scope: OUT_OF_SCOPE,
    note,
    disclaimer: '只核"年薪 × 服务费率 = 服务费"与"保证期内离职按未满天数折算退款"这类**表内勾稽**，'
      + '不判断年薪口径（税前/税后、含不含奖金、12 薪还是 13 薪）、合同费率档位与保证期长度是否合法；'
      + '每条结论都带原文行号与候选人，可由第三方用同一份输入复算。',
  };

  result.scope.withheld = CHECKS_WITHHELD;


  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
