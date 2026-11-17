'use strict';
/**
 * invoice-consistency.js —— 票据一致性AI核对（免费档）本地引擎
 *
 * 设计原则（与本仓库「宁可失败也不猜错」的教训一致）：
 *   · 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件
 *     （技能包是从注册表单独下载安装的，跨包引用一定会断）；
 *   · **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）；
 *   · 每条结论都必须能由第三方用同一份输入复算：消息里直接引用出问题的原文、数字、行号；
 *   · 材料不足时绝不输出"未发现问题"，而是返回 insufficient_input 并说明缺什么。
 *
 * 免费档只做九项检查，别无其他：
 *   1. 行内算术        2. 分项加总        3. 税额计算
 *   4. 价税合计        5. 大小写金额一致  6. 抬头/主体一致
 *   7. 日期逻辑        8. 重复票检测      9. 占位符/空白残留
 *
 * 中英文票据都支持。刻意不实现本版本范围之外的检查项（见 CHECKS_WITHHELD），
 * 它们只会以"未执行"的名义出现，绝不会被伪造出来。
 */

/* ------------------------------------------------------------------ 常量 */

const CHECKS_GIVEN = [
  '行内算术',
  '分项加总',
  '税额计算',
  '价税合计',
  '大小写金额一致',
  '抬头/主体一致',
  '日期逻辑',
  '重复票检测',
  '占位符/空白残留',
];

const CHECKS_WITHHELD = [
  '发票真伪查验与代码号码规则校验',
  '税收分类编码与税率目录核对',
  '三单匹配（采购订单、入库单与发票）',
  '预算科目与费用归属核对',
  '供应商主体资格与失信名单核对',
  '差旅与费用标准超标判定',
  '红冲作废与发票联次状态一致性核对',
  '报销审批链与权限核对',
  '异常模式与关联方识别',
];

/** 金额容差：与票据两位小数口径一致 */
const TOLERANCE = 0.01;
/** 税额容差：金额 × 税率 常因分位舍入差一两分，给到 0.02 */
const TAX_TOLERANCE = 0.02;
/** 一段材料至少要有这么长，才谈得上"核对" */
const MIN_MATERIAL_CHARS = 8;
/** 结论条数上限（超出计入 omitted，绝不静默丢弃） */
const MAX_FINDINGS = 200;

/* ------------------------------------------------------------ 通用小工具 */

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice: advice };
}

/** 每行的起始偏移，用于"字符位置 → 行号" */
function lineStarts(text) {
  const starts = [0];
  for (let i = 0; i < text.length; i++) {
    if (text.charCodeAt(i) === 10) starts.push(i + 1);
  }
  return starts;
}

function lineOf(starts, idx) {
  let lo = 0;
  let hi = starts.length - 1;
  while (lo < hi) {
    const mid = (lo + hi + 1) >> 1;
    if (starts[mid] <= idx) lo = mid; else hi = mid - 1;
  }
  return lo + 1;
}

function round2(n) {
  return Math.round(n * 100) / 100;
}

function fmtMoney(n) {
  if (n === null || n === undefined || !Number.isFinite(Number(n))) return '—';
  return Number(n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function clip(s, n) {
  const t = String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
  return t.length > n ? t.slice(0, n) + '…' : t;
}

function uniq(arr) {
  return Array.from(new Set(arr));
}

function finding(level, category, line, message, advice, evidence) {
  return { level: level, category: category, line: line, message: message, advice: advice, evidence: evidence };
}

/** 名称归一：只去空白与标点、统一大小写，**不动词干**
 *（"有限公司"与"有限责任公司"必须判为不同，否则会把真问题放过） */
function normName(s) {
  return String(s == null ? '' : s)
    .replace(/[\s\u00A0]/g, '')
    .replace(/[“”"'‘’《》〈〉（）()【】\[\]、,，.。;；:：·&｜|\-—_]/g, '')
    .toLowerCase();
}

/** 数字解析：接受数字、带千分位/全角逗号、带 万/亿 后缀、带币种符号的金额串 */
function numOf(v) {
  if (typeof v === 'number') return Number.isFinite(v) ? round2(v) : null;
  if (v === null || v === undefined) return null;
  let s = String(v).replace(/[\s\u00A0]/g, '').split(/[，,]/).join('');
  if (!s) return null;
  let mult = 1;
  if (s.indexOf('亿元') >= 0) { mult = 1e8; s = s.replace(/亿元/g, ''); }
  else if (s.indexOf('亿') >= 0) { mult = 1e8; s = s.replace(/亿/g, ''); }
  else if (s.indexOf('万元') >= 0) { mult = 1e4; s = s.replace(/万元/g, ''); }
  else if (s.indexOf('万') >= 0) { mult = 1e4; s = s.replace(/万/g, ''); }
  s = s.replace(/[\u00A5\uFFE5$\u20AC\u00A3]/g, '');
  s = s.replace(/^(USD|RMB|CNY)/i, '').replace(/(USD|RMB|CNY)$/i, '');
  const m = /-?\d+(?:\.\d+)?/.exec(s);
  if (!m) return null;
  const n = parseFloat(m[0]) * mult;
  return Number.isFinite(n) ? round2(n) : null;
}

/** 税率解析：13% / 13％ / 0.13 / 6 都归一到小数口径 */
function rateOf(v) {
  if (v === null || v === undefined) return null;
  const s = String(v).replace(/[\s\u00A0]/g, '');
  const m = /(-?\d+(?:\.\d+)?)\s*(%|％)?/.exec(s);
  if (!m) return null;
  const n = parseFloat(m[1]);
  if (!Number.isFinite(n)) return null;
  if (m[2]) return n / 100;   // 带 % 一定是百分比
  if (n === 0) return 0;
  // 裸数字口径：>=1 当百分比（「1」= 1% 征收率、「13」= 13%），<1 当小数（「0.13」= 13%）。
  // ⚠️ 原实现把「1」当成 100%、「1.2」当成 120%。增值税税率只有 0/1/3/5/6/9/13%，
  // 100% 不是税率 —— 后果是误报：发票写 1% 征收率时按 100% 推税额，把对的判成错的。
  if (n < 1) return n;
  return n / 100;
}

/* ------------------------------------------------------------- 中文数字 */

const CN_DIGITS = {
  '〇': 0, '零': 0, '○': 0,
  '一': 1, '壹': 1, '二': 2, '贰': 2, '两': 2, '三': 3, '叁': 3,
  '四': 4, '肆': 4, '五': 5, '伍': 5, '六': 6, '陆': 6, '七': 7, '柒': 7,
  '八': 8, '捌': 8, '九': 9, '玖': 9,
};

const CN_UNITS = {
  '十': 10, '拾': 10, '百': 100, '佰': 100, '千': 1000, '仟': 1000,
};

/** 纯中文数字串 → 数值（支持 万 / 亿 分段）；出现非数字字符返回 null */
function cnToNumber(s) {
  const str = String(s == null ? '' : s);
  if (!str) return null;
  let total = 0;
  let section = 0;
  let current = 0;
  let seen = false;
  for (const ch of str) {
    if (CN_DIGITS[ch] !== undefined) {
      current = CN_DIGITS[ch];
      seen = true;
    } else if (CN_UNITS[ch] !== undefined) {
      const u = CN_UNITS[ch];
      section += (current || 1) * u;
      current = 0;
      seen = true;
    } else if (ch === '万' || ch === '亿' || ch === '兆') {
      const mult = ch === '万' ? 1e4 : (ch === '亿' ? 1e8 : 1e12);
      section = (section + current) * mult;
      total += section;
      section = 0;
      current = 0;
      seen = true;
    } else {
      return null;
    }
  }
  if (!seen) return null;
  return total + section + current;
}

/** 中文大写金额（壹佰万元整 / 叁仟贰佰元伍角）→ 数值 */
function parseCnCapital(token) {
  let t = String(token == null ? '' : token);
  if (!t) return null;
  t = t.replace(/^人民币/, '').replace(/[整正]$/, '');
  let intPart = t;
  let fracPart = '';
  const m = /^(.*?)[元圆](.*)$/.exec(t);
  if (m) {
    intPart = m[1];
    fracPart = m[2];
  } else if (!/[拾佰仟万亿兆]/.test(t)) {
    return null;
  }
  intPart = intPart.replace(/[整正]/g, '') || '零';
  const base = cnToNumber(intPart);
  if (base === null) return null;
  let val = base;
  const jiao = /([零〇壹贰叁肆伍陆柒捌玖])角/.exec(fracPart);
  const fen = /([零〇壹贰叁肆伍陆柒捌玖])分/.exec(fracPart);
  if (jiao) val += CN_DIGITS[jiao[1]] / 10;
  if (fen) val += CN_DIGITS[fen[1]] / 100;
  return Number.isFinite(val) ? round2(val) : null;
}

/* ------------------------------------------------------------ 英文数字词 */

const EN_ONES = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9,
  ten: 10, eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15,
  sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19,
};
const EN_TENS = {
  twenty: 20, thirty: 30, forty: 40, fifty: 50, sixty: 60, seventy: 70, eighty: 80, ninety: 90,
};
const EN_SCALES = { hundred: 100, thousand: 1e3, million: 1e6, billion: 1e9, trillion: 1e12 };
const EN_WORD_ALT = Object.keys(EN_ONES).concat(Object.keys(EN_TENS)).concat(Object.keys(EN_SCALES)).join('|');

/** 英文数字词短语 → 数值；含非数字词返回 null */
function parseEnWords(phrase) {
  const words = String(phrase == null ? '' : phrase)
    .toLowerCase()
    .replace(/[-,]/g, ' ')
    .split(/\s+/)
    .filter((w) => w && w !== 'and');
  if (!words.length) return null;
  let total = 0;
  let current = 0;
  let seen = false;
  for (const w of words) {
    if (EN_ONES[w] !== undefined) { current += EN_ONES[w]; seen = true; }
    else if (EN_TENS[w] !== undefined) { current += EN_TENS[w]; seen = true; }
    else if (EN_SCALES[w] !== undefined) {
      const sc = EN_SCALES[w];
      if (sc === 100) current = (current || 1) * 100;
      else { total += (current || 1) * sc; current = 0; }
      seen = true;
    } else {
      return null;
    }
  }
  return seen ? total + current : null;
}

const EN_WORDS_RE = new RegExp('\\b(?:' + EN_WORD_ALT + ')(?:[\\s-]+(?:and[\\s-]+)?(?:' + EN_WORD_ALT + '))*\\b', 'gi');
const CN_CAP_RE = /[零〇壹贰叁肆伍陆柒捌玖拾佰仟万亿兆圆元角分整正]{2,}/g;

/** 大写金额字段 → {cap, figure, rawCap, rawFigure}（cap 为大写解析值，figure 为同字段里的阿拉伯数字） */
function parseCapitalField(value) {
  const text = String(value == null ? '' : value);
  const out = { cap: null, figure: null, rawCap: '', rawFigure: '' };

  CN_CAP_RE.lastIndex = 0;
  const cn = CN_CAP_RE.exec(text);
  if (cn && /[零〇壹贰叁肆伍陆柒捌玖]/.test(cn[0]) && (/[元圆]/.test(cn[0]) || /[拾佰仟万亿兆]/.test(cn[0]))) {
    const v = parseCnCapital(cn[0]);
    if (v !== null && v > 0) { out.cap = v; out.rawCap = cn[0]; }
  }
  if (out.cap === null) {
    EN_WORDS_RE.lastIndex = 0;
    const en = EN_WORDS_RE.exec(text);
    if (en) {
      const v = parseEnWords(en[0]);
      if (v !== null && v > 0) { out.cap = v; out.rawCap = en[0]; }
    }
  }
  // 同一字段里若同时写了大写与小写（如「价税合计（大写）… （小写）14,100.00」），取出阿拉伯数字单独比
  const cleaned = text.replace(CN_CAP_RE, ' ');
  const nm = /-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?/.exec(cleaned);
  if (nm) {
    const v = numOf(nm[0]);
    if (v !== null) { out.figure = v; out.rawFigure = nm[0]; }
  }
  return out;
}

/* ------------------------------------------------------------ 字段标签表 */

const FIELD_SPECS = [
  { key: 'invoice_code', labels: ['发票代码', '票据代码', 'Invoice Code'] },
  { key: 'invoice_no', labels: ['发票号码', '发票号', '票据号码', '发票编号', 'Invoice No', 'Invoice Number', 'Invoice #', 'Inv No'] },
  { key: 'invoice_date', labels: ['开票日期', '开具日期', '开票时间', '发票日期', 'Invoice Date', 'Date of Issue', 'Issue Date'] },
  { key: 'reimburse_date', labels: ['报销单日期', '报销日期', '提交日期', '申请日期', '受理日期', '收单日期', 'Reimbursement Date', 'Expense Date', 'Claim Date', 'Submitted Date', 'Submission Date'] },
  { key: 'business_date', labels: ['业务发生日期', '服务日期', '消费日期', '交易日期', '业务日期', '发生日期', 'Service Date', 'Transaction Date', 'Business Date', 'Date of Service'] },
  { key: 'buyer', labels: ['买方名称', '抬头单位', '发票抬头', '付款方名称', '付款单位', '买方', '抬头', 'Buyer', 'Bill To', 'Purchaser', 'Customer', 'Client', 'Account Name'],
    raw: [{ label: '购方名称', pattern: '购\\s*买?\\s*方\\s*(?:名\\s*称)?' }] },
  { key: 'seller', labels: ['销售方名称', '销方名称', '卖方名称', '供应商名称', '开票方', '收款方', '销方', '卖方', 'Seller', 'Vendor', 'Supplier', 'Issued By', 'From'] },
  { key: 'entity', labels: ['报销单位', '报销主体', '报销公司', '报销部门单位', '费用承担单位', '申请单位', '报销人单位', '单位名称', '报销抬头', 'Reimbursement Entity', 'Expense Entity', 'Claim Entity', 'Company', 'Employer', 'Reimbursed To'] },
  { key: 'item_name', labels: ['货物或应税劳务名称', '货物名称', '劳务名称', '服务名称', '项目名称', '品名', 'Description', 'Particulars', 'Item', 'Service', 'Goods'] },
  { key: 'qty', labels: ['数量', 'Qty', 'Quantity'] },
  { key: 'unit_price', labels: ['单价', 'Unit Price', 'Price'] },
  { key: 'amount', labels: ['不含税金额', '金额', 'Amount', 'Net Amount'] },
  { key: 'rate', labels: ['税率', '征收率', 'Tax Rate', 'VAT Rate', 'Rate'] },
  { key: 'tax', labels: ['税额', '税金', '增值税额', 'Tax Amount', 'VAT', 'Tax'] },
  { key: 'net_total', labels: ['不含税金额合计', '不含税合计', '金额合计', '合计金额', '净额', '小计', 'Subtotal', 'Net Total', 'Total excl. tax', 'Amount excl. tax'] },
  { key: 'gross_total', labels: ['价税合计', '价税总计', '含税合计', '含税金额', '应付金额', '实付金额', '支付金额', '报销金额', '总金额', '总额', 'Total incl. tax', 'Total incl. VAT', 'Total including tax', 'Grand Total', 'Total Amount', 'Amount Due', 'Total Payable', 'Payable', 'Total'] },
  { key: 'capital', labels: ['价税合计（大写）', '价税合计(大写)', '价税合计大写', '合计大写', '金额大写', '大写金额', '大写', 'Amount in Words', 'Total in Words', 'In Words', 'Say'] },
];

const DATE_KEYS = ['invoice_date', 'reimburse_date', 'business_date'];
const AMOUNT_KEYS = ['net_total', 'gross_total', 'amount', 'tax'];
/** 这些字段写成空的（或只留占位符）要报"必填字段空白" */
const REQUIRED_KEYS = ['invoice_no', 'invoice_date', 'net_total', 'gross_total', 'amount', 'tax'];

const ALL_LABELS = (function () {
  const out = [];
  for (const spec of FIELD_SPECS) {
    for (const label of spec.labels) out.push({ key: spec.key, label: label, pattern: '' });
    for (const r of (spec.raw || [])) out.push({ key: spec.key, label: r.label, pattern: r.pattern });
  }
  out.sort((a, b) => b.label.length - a.label.length || (a.label < b.label ? -1 : 1));
  return out;
})();

function escapeRe(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** 标签 → 正则片段：ASCII 标签加词边界（用 lookaround，兼容以 # 结尾的标签）；
 *  中文标签允许字间出现空格（官方发票版式里常写成「购 方 名 称」）。
 *  带 pattern 的标签直接用写好的正则（官方版式还有「购 买 方 名 称」这一种写法）。 */
function labelBody(entry) {
  const item = (typeof entry === 'string') ? { label: entry, pattern: '' } : entry;
  if (item && item.pattern) return '(?:' + item.pattern + ')';
  const label = (item && item.label) || '';
  if (/^[\x20-\x7E]+$/.test(label)) {
    return '(?<![A-Za-z0-9])' + escapeRe(label) + '(?![A-Za-z0-9])';
  }
  return Array.from(label).map(function (ch) {
    const e = escapeRe(ch);
    return /[\u4e00-\u9fff]/.test(ch) ? e + '\\s*' : e;
  }).join('');
}

const LABEL_ALT = ALL_LABELS.map(function (x) { return '(' + labelBody(x) + ')'; }).join('|');
const COLON_SRC = '(?:' + LABEL_ALT + ')\\.?[ \\t]*[：:]';
const ANY_LABEL_RE = new RegExp('(?:' + LABEL_ALT + ')\\.?', 'g');

function hasAnyLabel(s) {
  ANY_LABEL_RE.lastIndex = 0;
  return ANY_LABEL_RE.test(String(s == null ? '' : s));
}

/* ------------------------------------------------------------ 字段抽取 */

/** 逐行抽取"标签 + 冒号 + 值"；同一行有多个标签时，值止于下一个标签。
 *  无冒号的"行首标签 + 空格 + 值"作为兜底（值里含其它标签则判为表头，不收）。 */
function collectFields(lines, starts) {
  const out = [];
  const re = new RegExp(COLON_SRC, 'g');
  const lineStart = new RegExp('^[ \\t]*(?:' + LABEL_ALT + ')\\.?[ \\t]+(.*)$');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const base = starts[i];
    re.lastIndex = 0;
    const hits = [];
    let m;
    while ((m = re.exec(line)) !== null) {
      let key = null;
      let label = '';
      for (let g = 1; g <= ALL_LABELS.length; g++) {
        if (m[g] !== undefined) { key = ALL_LABELS[g - 1].key; label = ALL_LABELS[g - 1].label; break; }
      }
      if (!key) continue;
      hits.push({ key: key, label: label, start: m.index, end: m.index + m[0].length });
      if (re.lastIndex <= m.index) re.lastIndex = m.index + 1;
    }
    if (hits.length) {
      for (let k = 0; k < hits.length; k++) {
        const valueEnd = (k + 1 < hits.length) ? hits[k + 1].start : line.length;
        const rawValue = line.slice(hits[k].end, valueEnd);
        out.push({
          key: hits[k].key,
          label: hits[k].label,
          value: rawValue.trim(),
          raw: line.slice(hits[k].start, valueEnd).trim(),
          line: i + 1,
          index: base + hits[k].start,
          valueStart: base + hits[k].end,
          valueEnd: base + valueEnd,
          lineText: line,
        });
      }
      continue;
    }
    const ls = lineStart.exec(line);
    if (ls) {
      const value = String(ls[ALL_LABELS.length + 1] || '').trim();
      if (!value) continue;
      if (hasAnyLabel(value)) continue;                 // 表头行：值里还是标签，不是字段值
      if (!/\d/.test(value) && !/[A-Za-z\u4e00-\u9fff]/.test(value)) continue;
      let key2 = null;
      let label2 = '';
      for (let g = 1; g <= ALL_LABELS.length; g++) {
        if (ls[g] !== undefined) { key2 = ALL_LABELS[g - 1].key; label2 = ALL_LABELS[g - 1].label; break; }
      }
      if (!key2) continue;
      const off = line.indexOf(value);
      out.push({
        key: key2,
        label: label2,
        value: value,
        raw: line.trim(),
        line: i + 1,
        index: base,
        valueStart: base + (off >= 0 ? off : 0),
        valueEnd: base + line.length,
        lineText: line,
      });
    }
  }
  out.sort((a, b) => a.index - b.index);
  return out;
}

/* ------------------------------------------------------------ 明细行 */

const NUM_TOKEN_RE = /(?<![0-9,.])(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![0-9,.])/g;

function numbersInLine(line) {
  const out = [];
  NUM_TOKEN_RE.lastIndex = 0;
  let m;
  while ((m = NUM_TOKEN_RE.exec(line)) !== null) {
    const after = line[m.index + m[0].length] || '';
    if (after === '%' || after === '％') continue;
    const v = numOf(m[0]);
    if (v === null) continue;
    out.push({ value: v, raw: m[0], index: m.index });
  }
  return out;
}

function lineHasKey(line, key) {
  const labels = [];
  for (const spec of FIELD_SPECS) {
    if (spec.key === key) for (const l of spec.labels) labels.push(l);
  }
  for (const l of labels) {
    const re = new RegExp(labelBody(l));
    if (re.test(line)) return true;
  }
  return false;
}

/** 表格明细：表头行同时含 数量 / 单价 / 金额 三个标签，且表头行本身没有冒号字段；
 *  其后的行只要一整行恰好能取出 ≥3 个数，就按 倒数第3/第2/第1 个数当作 数量/单价/金额。 */
function collectTableItems(lines, starts, fieldsByLine) {
  const items = [];
  const headerLines = new Set();
  const rowLines = new Set();
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    if (fieldsByLine.has(i + 1)) continue;
    if (!lineHasKey(line, 'qty') || !lineHasKey(line, 'unit_price') || !lineHasKey(line, 'amount')) continue;
    headerLines.add(i + 1);
    for (let j = i + 1; j < lines.length; j++) {
      const row = lines[j];
      if (!row.trim()) break;
      if (fieldsByLine.has(j + 1)) break;
      if (headerLines.has(j + 1)) break;
      const nums = numbersInLine(row);
      if (nums.length < 3) break;
      const q = nums[nums.length - 3];
      const p = nums[nums.length - 2];
      const a = nums[nums.length - 1];
      const name = row.slice(0, q.index).trim() || row.trim();
      items.push({
        name: clip(name, 40),
        qty: q.value, qtyRaw: q.raw,
        unit_price: p.value, priceRaw: p.raw,
        amount: a.value, amountRaw: a.raw,
        line: j + 1,
        where: '第' + (j + 1) + '行',
      });
      rowLines.add(j + 1);
    }
  }
  return { items: items, headerLines: headerLines, rowLines: rowLines };
}

/** 同一行上写了两个以上「标签：值」的明细行（数量：2 单价：5,000.00 金额：10,000.00） */
function collectInlineItems(fields) {
  const byLine = new Map();
  for (const f of fields) {
    if (f.key !== 'qty' && f.key !== 'unit_price' && f.key !== 'amount') continue;
    if (!byLine.has(f.line)) byLine.set(f.line, []);
    byLine.get(f.line).push(f);
  }
  const items = [];
  for (const entry of byLine) {
    const list = entry[1];
    const keys = uniq(list.map((x) => x.key));
    if (keys.length < 2) continue;
    const pick = (k) => {
      const hit = list.filter((x) => x.key === k)[0];
      if (!hit) return null;
      const v = numOf(hit.value);
      return v === null ? null : { value: v, field: hit };
    };
    const q = pick('qty');
    const p = pick('unit_price');
    const a = pick('amount');
    items.push({
      name: clip(entry[1][0].lineText, 40),
      qty: q ? q.value : null, qtyRaw: q ? q.field.value : null,
      unit_price: p ? p.value : null, priceRaw: p ? p.field.value : null,
      amount: a ? a.value : null, amountRaw: a ? a.field.value : null,
      line: entry[0],
      where: '第' + entry[0] + '行',
    });
  }
  return items;
}

/** 单张票只有一个明细：数量 / 单价 / 金额 各写一行（没写成表格）。
 *  只在三者在同一张单据里各出现且仅出现一次、且行号彼此接近时才认，避免把不相干的数字凑成一行。 */
function docItemsFallback(fields) {
  const one = (key) => {
    const list = fields.filter((f) => f.key === key);
    return list.length === 1 ? list[0] : null;
  };
  const q = one('qty');
  const p = one('unit_price');
  const a = one('amount');
  if (!q || !p || !a) return [];
  const lines = [q.line, p.line, a.line];
  if (Math.max.apply(null, lines) - Math.min.apply(null, lines) > 4) return [];
  const qv = numOf(q.value);
  const pv = numOf(p.value);
  const av = numOf(a.value);
  if (qv === null || pv === null || av === null) return [];
  return [{
    name: clip(a.lineText, 40),
    qty: qv, qtyRaw: q.value,
    unit_price: pv, priceRaw: p.value,
    amount: av, amountRaw: a.value,
    line: a.line,
    where: '第' + a.line + '行',
  }];
}

/* ------------------------------------------------------------ 日期 */

const MONTHS = {
  january: 1, february: 2, march: 3, april: 4, may: 5, june: 6, july: 7, august: 8,
  september: 9, october: 10, november: 11, december: 12,
  jan: 1, feb: 2, mar: 3, apr: 4, jun: 6, jul: 7, aug: 8, sep: 9, sept: 9, oct: 10, nov: 11, dec: 12,
};
const MONTH_ALT = Object.keys(MONTHS).join('|');

function daysInMonth(y, m) {
  if (!(y >= 1 && y <= 9999)) return 0;
  if (m === 2) {
    const leap = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
    return leap ? 29 : 28;
  }
  return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1] || 0;
}

function validYmd(y, m, d) {
  if (!Number.isFinite(y) || !Number.isFinite(m) || !Number.isFinite(d)) return false;
  if (y < 1900 || y > 9999) return false;
  if (m < 1 || m > 12) return false;
  return d >= 1 && d <= daysInMonth(y, m);
}

function ymdValue(y, m, d) {
  return y * 10000 + m * 100 + d;
}

function ymdText(y, m, d) {
  const pad = (n) => (n < 10 ? '0' + n : String(n));
  return y + '-' + pad(m) + '-' + pad(d);
}

/** 在一段文本里找日期；返回 {raw, y, m, d, valid, ambiguous, offset} */
function findDatesIn(text) {
  const out = [];
  const taken = [];
  const push = (raw, y, m, d, offset, ambiguous) => {
    out.push({
      raw: raw, y: y, m: m, d: d, offset: offset,
      valid: validYmd(y, m, d), ambiguous: !!ambiguous,
    });
  };
  const overlaps = (a, b) => out.some((t) => {
    const s = t.offset; const e = t.offset + t.raw.length;
    return a < e && b > s;
  });
  let m;
  // YYYY-MM-DD / YYYY/M/D / YYYY.M.D / YYYY年M月D日
  const reA = /(\d{4})\s*(?:[-/.]|年)\s*(\d{1,2})\s*(?:[-/.]|月)\s*(\d{1,2})\s*日?/g;
  while ((m = reA.exec(text)) !== null) {
    push(m[0], parseInt(m[1], 10), parseInt(m[2], 10), parseInt(m[3], 10), m.index, false);
    taken.push([m.index, m.index + m[0].length]);
  }
  // Month D, YYYY
  const reB = new RegExp('\\b(' + MONTH_ALT + ')\\.?\\s+(\\d{1,2})(?:st|nd|rd|th)?\\s*,?\\s*(\\d{4})', 'gi');
  while ((m = reB.exec(text)) !== null) {
    if (overlaps(m.index, m.index + m[0].length)) continue;
    push(m[0], parseInt(m[3], 10), MONTHS[m[1].toLowerCase()], parseInt(m[2], 10), m.index, false);
    taken.push([m.index, m.index + m[0].length]);
  }
  // D Month YYYY
  const reC = new RegExp('\\b(\\d{1,2})(?:st|nd|rd|th)?\\s+(' + MONTH_ALT + ')\\.?\\s*,?\\s*(\\d{4})', 'gi');
  while ((m = reC.exec(text)) !== null) {
    if (overlaps(m.index, m.index + m[0].length)) continue;
    push(m[0], parseInt(m[3], 10), MONTHS[m[2].toLowerCase()], parseInt(m[1], 10), m.index, false);
    taken.push([m.index, m.index + m[0].length]);
  }
  // D/M/YYYY 或 M/D/YYYY：两边都 <=12 时口径不明，标记为 ambiguous 且不参与逻辑比较
  const reD = /(?<![0-9])(\d{1,2})\s*\/\s*(\d{1,2})\s*\/\s*(\d{4})(?![0-9])/g;
  while ((m = reD.exec(text)) !== null) {
    if (overlaps(m.index, m.index + m[0].length)) continue;
    const a = parseInt(m[1], 10);
    const b = parseInt(m[2], 10);
    const y = parseInt(m[3], 10);
    if (a > 12 && b > 12) continue;
    if (a > 12) push(m[0], y, b, a, m.index, false);
    else if (b > 12) push(m[0], y, a, b, m.index, false);
    else push(m[0], y, a, b, m.index, true);
    taken.push([m.index, m.index + m[0].length]);
  }
  out.sort((x, y) => x.offset - y.offset);
  return out;
}

/* ------------------------------------------------------------ 占位符规则 */

const PLACEHOLDER_RULES = [
  { re: /\bX{2,}\b/g, label: 'XXX 占位', level: 'P1' },
  { re: /\bTBD\b/gi, label: 'TBD 占位', level: 'P1' },
  { re: /\bTBC\b/gi, label: 'TBC 占位', level: 'P1' },
  { re: /\bTBF\b/gi, label: 'TBF 占位', level: 'P1' },
  { re: /【[^】\n]{0,40}】/g, label: '【…】方括号占位', level: 'P1' },
  { re: /＿{2,}/g, label: '＿＿ 下划线占位', level: 'P1' },
  { re: /_{3,}/g, label: '____ 下划线占位', level: 'P1' },
  { re: /\{\{[^}\n]{1,40}\}\}/g, label: '{{var}} 模板变量占位', level: 'P1' },
  { re: /待填|此处填写|请填写|待补充|待补|待定|待上传|待提供/g, label: '中文待填占位', level: 'P1' },
  { re: /to\s+be\s+(?:filled|advised|provided|confirmed)/gi, label: 'to be filled 占位', level: 'P1' },
  { re: /\[\s*\]/g, label: '[ ] 空方括号占位', level: 'P2' },
  { re: /\bN\/A\b/g, label: 'N/A 占位', level: 'P2' },
];

function collectPlaceholders(text, starts) {
  const out = [];
  const taken = [];
  for (const rule of PLACEHOLDER_RULES) {
    rule.re.lastIndex = 0;
    let m;
    while ((m = rule.re.exec(text)) !== null) {
      if (taken.some((t) => m.index >= t[0] && m.index < t[1])) continue;
      taken.push([m.index, m.index + m[0].length]);
      out.push({ raw: m[0], label: rule.label, level: rule.level, index: m.index, line: lineOf(starts, m.index) });
    }
  }
  out.sort((a, b) => a.index - b.index);
  return out;
}

/* ------------------------------------------------------------ 材料收集 */

/**
 * 从入参里取出"可核对的材料"。
 * 空 / 只有空白 / 只有一个字符 / 类型不对 / null / 裸数组 —— 一律 insufficient，绝不出结论。
 */
function collectMaterial(payload) {
  let text = null;

  if (payload === null || payload === undefined) {
    return { missing: ['没有收到任何材料：入参是 null（或 undefined）。'] };
  }
  if (Array.isArray(payload)) {
    return {
      missing: ['入参是数组（' + payload.length + ' 个元素），不是一份票据材料。'],
      advice: '请给 {"text": "发票 / 报销单文本"}，或直接把票据文本当作纯文本传入。',
    };
  }
  if (typeof payload === 'string') {
    text = payload;
  } else if (typeof payload === 'number' || typeof payload === 'boolean') {
    return {
      missing: ['入参是 ' + typeof payload + '（' + JSON.stringify(payload) + '），不是票据文本。'],
      advice: '请给 {"text": "发票 / 报销单文本"}，或直接把票据文本当作纯文本传入。',
    };
  } else if (typeof payload === 'object') {
    if (typeof payload.text === 'string') text = payload.text;
    else if (typeof payload.content === 'string') text = payload.content;
    else if (payload.text !== undefined && payload.text !== null) {
      return {
        missing: ['text 不是字符串（收到的是 ' + (Array.isArray(payload.text) ? 'array' : typeof payload.text)
          + '：' + clip(JSON.stringify(payload.text), 40) + '）。'],
        advice: '把票据文本放进 text 字符串字段，例如 {"text": "发票号码：12345678"}。',
      };
    } else {
      return {
        missing: ['入参对象里没有可用的 text（或 content）字符串字段。'],
        advice: '把票据文本放进 text 字符串字段，例如 {"text": "发票号码：12345678"}。',
      };
    }
  } else {
    return { missing: ['入参类型是 ' + typeof payload + '，无法当作票据文本。'] };
  }

  const raw = String(text);
  const trimmed = raw.trim();
  if (!trimmed) {
    return {
      missing: ['材料是空的（只有空白字符），没有任何可以核对的内容。'],
      advice: '把发票 / 报销单文本粘贴进 text 字段，至少要有金额、日期、号码、抬头或占位符中的一类。',
    };
  }
  if (trimmed.length < MIN_MATERIAL_CHARS) {
    return {
      missing: ['材料只有 ' + trimmed.length + ' 个字符（「' + clip(trimmed, 20) + '」），不构成一份可以核对的票据文本。'],
      advice: '请提供完整票据文本（或至少包含一个可核对要素的片段）。',
    };
  }
  return { text: raw };
}

/* ------------------------------------------------------------ 文档切分 */

const SEP_LINE_RE = /^[ \t]*(?:-{3,}|={3,})[ \t]*$/;
const DOC_START_RE = /^[ \t]*(?:发票号码|发票号|票据号码|发票编号|Invoice\s+No\.?|Invoice\s+Number|Invoice\s*#|Inv\.?\s*No\.?)[ \t]*[：:\s]/i;

function buildBlocks(lines) {
  const blocks = [];
  let cur = { from: 0, hard: true };
  for (let i = 0; i < lines.length; i++) {
    if (SEP_LINE_RE.test(lines[i])) {
      blocks.push({ from: cur.from, to: i - 1, hard: cur.hard });
      cur = { from: i + 1, hard: true };
    } else if (i > cur.from && DOC_START_RE.test(lines[i])) {
      blocks.push({ from: cur.from, to: i - 1, hard: false });
      cur = { from: i, hard: false };
    }
  }
  blocks.push({ from: cur.from, to: lines.length - 1, hard: cur.hard });
  return blocks.filter((b) => b.to >= b.from);
}

/* ------------------------------------------------------------ 单项检查 */

function checkLineArithmetic(doc) {
  const out = [];
  for (const item of doc.items) {
    if (item.qty === null || item.unit_price === null || item.amount === null) continue;
    const expected = round2(item.qty * item.unit_price);
    if (!Number.isFinite(expected)) continue;
    const diff = round2(item.amount - expected);
    if (Math.abs(diff) <= TOLERANCE) continue;
    out.push(finding(
      'P0', '行内算术', item.line,
      doc.where + item.where + '「' + item.name + '」金额 ' + fmtMoney(item.amount)
        + ' 与 数量 ' + item.qtyRaw + ' × 单价 ' + fmtMoney(item.unit_price) + ' = ' + fmtMoney(expected)
        + ' 不符（差 ' + fmtMoney(diff) + '）',
      '核对这一行的数量 / 单价 / 金额，按原票面重算或要求对方更正。',
      { document: doc.index, line_text: item.name, qty: item.qtyRaw, unit_price: item.priceRaw, amount_stated: item.amountRaw, amount_expected: fmtMoney(expected), diff: fmtMoney(diff) }
    ));
  }
  return out;
}

function itemSum(doc) {
  let sum = 0;
  let n = 0;
  for (const item of doc.items) {
    if (item.amount === null) continue;
    sum += item.amount;
    n++;
  }
  return n ? round2(sum) : null;
}

function firstField(doc, key) {
  for (const f of doc.fields) if (f.key === key) return f;
  return null;
}

function checkSubtotal(doc) {
  const out = [];
  const sum = itemSum(doc);
  if (sum === null) return out;
  const amounts = doc.items.filter((x) => x.amount !== null);
  if (amounts.length < 2) return out;
  let stated = firstField(doc, 'net_total');
  let statedLabel = stated ? stated.label : '';
  if (!stated && !firstField(doc, 'tax') && !firstField(doc, 'rate')) {
    stated = firstField(doc, 'gross_total');
    statedLabel = stated ? stated.label : '';
  }
  if (!stated) return out;
  const v = numOf(stated.value);
  if (v === null) return out;
  const diff = round2(v - sum);
  if (Math.abs(diff) <= TOLERANCE) return out;
  out.push(finding(
    'P0', '分项加总', stated.line,
    doc.where + '第' + stated.line + '行「' + statedLabel + '」' + fmtMoney(v)
      + ' 与各明细行金额之和 ' + fmtMoney(sum) + '（共 ' + amounts.length + ' 行）不符（差 ' + fmtMoney(diff) + '）',
    '核对分项金额与合计栏，两者必须能相互加出来。',
    { document: doc.index, stated: stated.raw, stated_value: fmtMoney(v), items_sum: fmtMoney(sum), item_lines: amounts.map((x) => x.line), diff: fmtMoney(diff) }
  ));
  return out;
}

/** 不含税金额：单据写明的不含税合计优先，其次明细行之和，再次裸「金额」字段 */
function resolveNet(doc) {
  const f = firstField(doc, 'net_total');
  if (f) {
    const v = numOf(f.value);
    if (v !== null) return { value: v, line: f.line, label: f.label, raw: f.value };
  }
  const sum = itemSum(doc);
  if (sum !== null) return { value: sum, line: doc.startLine, label: '明细行金额之和', raw: String(sum) };
  const a = firstField(doc, 'amount');
  if (a) {
    const v = numOf(a.value);
    if (v !== null) return { value: v, line: a.line, label: a.label, raw: a.value };
  }
  return null;
}

function checkTax(doc) {
  const out = [];
  const rateField = firstField(doc, 'rate');
  const taxField = firstField(doc, 'tax');
  if (!rateField || !taxField) return out;
  const rate = rateOf(rateField.value);
  const tax = numOf(taxField.value);
  if (rate === null || tax === null) return out;
  const net = resolveNet(doc);
  if (!net) return out;
  const expected = round2(net.value * rate);
  if (!Number.isFinite(expected)) return out;
  const diff = round2(tax - expected);
  if (Math.abs(diff) <= TAX_TOLERANCE) return out;
  out.push(finding(
    'P0', '税额计算', taxField.line,
    doc.where + '第' + taxField.line + '行「' + taxField.label + '」' + fmtMoney(tax)
      + ' 与 ' + (net.label === '明细行金额之和' ? net.label : '第' + net.line + '行「' + net.label + '」')
      + ' ' + fmtMoney(net.value) + ' × 税率 ' + rateField.value.trim() + ' = ' + fmtMoney(expected)
      + ' 不符（差 ' + fmtMoney(diff) + '）',
    '核对税率与税额；税率要按票面口径（13% / 9% / 6% / 3% 等）重新计算。',
    { document: doc.index, net: fmtMoney(net.value), rate: rateField.value.trim(), tax_stated: fmtMoney(tax), tax_expected: fmtMoney(expected), diff: fmtMoney(diff) }
  ));
  return out;
}

function checkGross(doc) {
  const out = [];
  const taxField = firstField(doc, 'tax');
  if (!taxField) return out;
  // 价税合计：优先用「价税合计 / Total incl. tax」字段；
  // 官方票面把价税合计只写成「价税合计（大写）…（小写）14,100.00」时，取同一行的小写数字当价税合计。
  let gross = null;
  let grossLine = 0;
  let grossLabel = '';
  let grossRaw = '';
  const grossField = firstField(doc, 'gross_total');
  if (grossField) {
    gross = numOf(grossField.value);
    grossLine = grossField.line;
    grossLabel = grossField.label;
    grossRaw = grossField.value;
  }
  if (gross === null) {
    const capField = firstField(doc, 'capital');
    if (capField) {
      const parsed = parseCapitalField(capField.value);
      if (parsed.figure !== null) {
        gross = parsed.figure;
        grossLine = capField.line;
        grossLabel = capField.label + '（小写）';
        grossRaw = parsed.rawFigure;
      }
    }
  }
  if (gross === null) return out;
  const tax = numOf(taxField.value);
  const net = resolveNet(doc);
  if (tax === null || !net) return out;
  const expected = round2(net.value + tax);
  if (!Number.isFinite(expected)) return out;
  const diff = round2(gross - expected);
  if (Math.abs(diff) <= TOLERANCE) return out;
  out.push(finding(
    'P0', '价税合计', grossLine,
    doc.where + '第' + grossLine + '行「' + grossLabel + '」' + fmtMoney(gross)
      + ' 与 不含税金额 ' + fmtMoney(net.value) + ' + 税额 ' + fmtMoney(tax) + ' = ' + fmtMoney(expected)
      + ' 不符（差 ' + fmtMoney(diff) + '）',
    '核对价税合计栏；不含税金额与税额相加必须等于价税合计。',
    { document: doc.index, gross_stated: fmtMoney(gross), gross_raw: grossRaw, net: fmtMoney(net.value), tax: fmtMoney(tax), gross_expected: fmtMoney(expected), diff: fmtMoney(diff) }
  ));
  return out;
}

function checkCapital(doc) {
  const out = [];
  const capField = firstField(doc, 'capital');
  if (!capField) return out;
  const parsed = parseCapitalField(capField.value);
  if (parsed.cap === null) return out;
  if (parsed.figure !== null) {
    const diff = round2(parsed.figure - parsed.cap);
    if (Math.abs(diff) > TOLERANCE) {
      out.push(finding(
        'P0', '大小写金额一致', capField.line,
        doc.where + '第' + capField.line + '行大写「' + parsed.rawCap + '」= ' + fmtMoney(parsed.cap)
          + ' 与小写 ' + parsed.rawFigure + ' = ' + fmtMoney(parsed.figure) + ' 不符（差 ' + fmtMoney(diff) + '）',
        '以大写为准重新出具票据，或核对小写金额。',
        { document: doc.index, capital: parsed.rawCap, capital_value: fmtMoney(parsed.cap), figure: parsed.rawFigure, figure_value: fmtMoney(parsed.figure), diff: fmtMoney(diff) }
      ));
    }
    return out;
  }
  let target = firstField(doc, 'gross_total');
  if (!target) target = firstField(doc, 'net_total');
  if (!target) return out;
  const tv = numOf(target.value);
  if (tv === null) return out;
  const diff = round2(tv - parsed.cap);
  if (Math.abs(diff) <= TOLERANCE) return out;
  out.push(finding(
    'P0', '大小写金额一致', capField.line,
    doc.where + '第' + capField.line + '行大写「' + parsed.rawCap + '」= ' + fmtMoney(parsed.cap)
      + ' 与第' + target.line + '行「' + target.label + '」' + fmtMoney(tv) + ' 不符（差 ' + fmtMoney(diff) + '）',
    '核对大写与小写金额，两者必须一致。',
    { document: doc.index, capital: parsed.rawCap, capital_value: fmtMoney(parsed.cap), target_label: target.label, target_value: fmtMoney(tv), diff: fmtMoney(diff) }
  ));
  return out;
}

function checkEntity(docs) {
  const out = [];
  const seen = new Set();
  const pairs = [];
  for (const doc of docs) {
    const buyers = doc.fields.filter((f) => f.key === 'buyer');
    const entities = doc.fields.filter((f) => f.key === 'entity');
    for (const b of buyers) for (const e of entities) pairs.push([b, e]);
    if (buyers.length > 1) {
      const norm = uniq(buyers.map((b) => normName(b.value)));
      if (norm.length > 1) pairs.push([buyers[0], buyers[1]]);
    }
  }
  for (const [b, e] of pairs) {
    const nb = normName(b.value);
    const ne = normName(e.value);
    if (!nb || !ne || nb === ne) continue;
    const sig = nb + '\u0000' + ne;
    if (seen.has(sig)) continue;
    seen.add(sig);
    const sameField = b.key === e.key;
    out.push(finding(
      'P1', '抬头/主体一致', e.line,
      sameField
        ? '同一主体先后写成两个名字：第' + b.line + '行「' + clip(b.value, 40) + '」与第' + e.line + '行「' + clip(e.value, 40) + '」'
        : '第' + b.line + '行「' + b.label + '」' + clip(b.value, 40) + ' 与第' + e.line + '行「' + e.label + '」' + clip(e.value, 40) + ' 不是同一个主体',
      '确认抬头主体到底是谁；发票抬头与报销单主体不一致会导致无法入账或退单。',
      { document: b.document, first: b.raw, first_line: b.line, second: e.raw, second_line: e.line }
    ));
  }
  return out;
}

function checkDates(docs) {
  const out = [];
  // 1) 非法日历日期（有标签的与无标签的都报）
  for (const doc of docs) {
    for (const d of doc.dateTokens) {
      if (d.valid) continue;
      out.push(finding(
        'P0', '日期逻辑', d.line,
        doc.where + '第' + d.line + '行出现了不存在的日历日期「' + d.raw + '」'
          + (d.m > 12 ? '（月份 ' + d.m + ' 超出 1-12）'
            : (d.d > daysInMonth(d.y, d.m) ? '（' + d.y + ' 年 ' + d.m + ' 月只有 ' + daysInMonth(d.y, d.m) + ' 天）' : '')),
        '改成真实存在的日期；非法日期在税务与财务系统里都会被拒。',
        { document: doc.index, raw: d.raw, line_text: d.lineText, field: d.key || null }
      ));
    }
    // 2) 同一字段出现两个不同日期
    const byKey = new Map();
    for (const d of doc.dateTokens) {
      if (!d.key || !d.valid) continue;
      if (!byKey.has(d.key)) byKey.set(d.key, []);
      byKey.get(d.key).push(d);
    }
    for (const entry of byKey) {
      const list = entry[1];
      const values = uniq(list.map((x) => ymdValue(x.y, x.m, x.d)));
      if (values.length <= 1) continue;
      out.push(finding(
        'P1', '日期逻辑', list[0].line,
        doc.where + '同一个「' + list[0].label + '」写成了两个不同的日期：'
          + list.map((x) => '第' + x.line + '行 ' + x.raw + '（' + ymdText(x.y, x.m, x.d) + '）').join('、'),
        '同一语义的日期只能有一个值，请确认以哪个为准。',
        { document: doc.index, key: list[0].key, values: list.map((x) => ymdText(x.y, x.m, x.d)), lines: list.map((x) => x.line) }
      ));
    }
  }
  // 3) 开票日期 vs 报销日期 / 业务发生日期
  const all = [];
  for (const doc of docs) {
    for (const d of doc.dateTokens) {
      if (d.valid && !d.ambiguous && d.key) all.push(Object.assign({ doc: doc.index }, d));
    }
  }
  const pick = (key) => all.filter((x) => x.key === key);
  const seen = new Set();
  for (const inv of pick('invoice_date')) {
    for (const re of pick('reimburse_date')) {
      if (ymdValue(inv.y, inv.m, inv.d) > ymdValue(re.y, re.m, re.d)) {
        const sig = 'R' + inv.line + '-' + re.line;
        if (seen.has(sig)) continue;
        seen.add(sig);
        out.push(finding(
          'P0', '日期逻辑', inv.line,
          '开票日期 ' + ymdText(inv.y, inv.m, inv.d) + '（第' + inv.line + '行）晚于报销日期 '
            + ymdText(re.y, re.m, re.d) + '（第' + re.line + '行）：先报销、后开票',
          '确认报销单日期是否填错；开票日期晚于报销日期属于典型的事后补票。',
          { documents: [inv.doc, re.doc], invoice_date: ymdText(inv.y, inv.m, inv.d), invoice_line: inv.line, reimburse_date: ymdText(re.y, re.m, re.d), reimburse_line: re.line }
        ));
      }
    }
    for (const biz of pick('business_date')) {
      if (ymdValue(inv.y, inv.m, inv.d) < ymdValue(biz.y, biz.m, biz.d)) {
        const sig = 'B' + inv.line + '-' + biz.line;
        if (seen.has(sig)) continue;
        seen.add(sig);
        out.push(finding(
          'P1', '日期逻辑', inv.line,
          '开票日期 ' + ymdText(inv.y, inv.m, inv.d) + '（第' + inv.line + '行）早于业务发生日期 '
            + ymdText(biz.y, biz.m, biz.d) + '（第' + biz.line + '行）：业务还没发生就先开了票',
          '确认业务发生日期与开票日期；两者顺序颠倒通常意味着日期填错。',
          { documents: [inv.doc, biz.doc], invoice_date: ymdText(inv.y, inv.m, inv.d), invoice_line: inv.line, business_date: ymdText(biz.y, biz.m, biz.d), business_line: biz.line }
        ));
      }
    }
  }
  return out;
}

function checkDuplicates(docs) {
  const out = [];
  const byNo = new Map();
  for (const doc of docs) {
    const f = firstField(doc, 'invoice_no');
    if (!f || !String(f.value).trim()) continue;
    const key = String(f.value).replace(/[\s\u00A0]/g, '').toUpperCase();
    if (!byNo.has(key)) byNo.set(key, []);
    byNo.get(key).push({ doc: doc, field: f });
  }
  for (const entry of byNo) {
    const list = entry[1];
    if (list.length < 2) continue;
    out.push(finding(
      'P0', '重复票检测', list[1].field.line,
      '发票号码「' + list[0].field.value.trim() + '」在同一批材料里出现了 ' + list.length + ' 次：'
        + list.map((x) => '第' + x.field.line + '行').join('、'),
      '同一张发票不应重复报销；确认是否重复提交或号码填错。',
      { invoice_no: list[0].field.value.trim(), lines: list.map((x) => x.field.line), occurrences: list.length }
    ));
  }
  const bySig = new Map();
  for (const doc of docs) {
    const g = firstField(doc, 'gross_total') || firstField(doc, 'net_total');
    const d = firstField(doc, 'invoice_date');
    const s = firstField(doc, 'seller');
    if (!g || !d || !s) continue;
    const amount = numOf(g.value);
    const dt = doc.dateTokens.filter((x) => x.key === 'invoice_date' && x.valid && !x.ambiguous)[0];
    if (amount === null || !dt) continue;
    const key = String(amount) + '|' + ymdText(dt.y, dt.m, dt.d) + '|' + normName(s.value);
    if (!bySig.has(key)) bySig.set(key, []);
    bySig.get(key).push({ doc: doc, field: d, amount: amount, date: ymdText(dt.y, dt.m, dt.d), seller: s.value });
  }
  for (const entry of bySig) {
    const list = entry[1];
    if (list.length < 2) continue;
    out.push(finding(
      'P0', '重复票检测', list[1].field.line,
      '金额 ' + fmtMoney(list[0].amount) + ' + 开票日期 ' + list[0].date + ' + 销方「' + clip(list[0].seller, 30)
        + '」完全相同的票据出现了 ' + list.length + ' 张：' + list.map((x) => '第' + x.field.line + '行').join('、'),
      '三项同时相同基本可以判定为重复票；请核对是否重复报销。',
      { amount: fmtMoney(list[0].amount), date: list[0].date, seller: list[0].seller, lines: list.map((x) => x.field.line), occurrences: list.length }
    ));
  }
  return out;
}

function checkPlaceholders(docs) {
  const out = [];
  for (const doc of docs) {
    for (const p of doc.placeholders) {
      out.push(finding(
        p.level, '占位符/空白残留', p.line,
        doc.where + '第' + p.line + '行残留占位内容「' + p.raw + '」（' + p.label + '）',
        '把占位内容替换成真实信息后再提交。',
        { document: doc.index, raw: p.raw, kind: p.label }
      ));
    }
    for (const f of doc.fields) {
      if (REQUIRED_KEYS.indexOf(f.key) < 0) continue;
      if (String(f.value).trim() !== '') continue;
      out.push(finding(
        'P1', '占位符/空白残留', f.line,
        doc.where + '第' + f.line + '行「' + f.label + '」是空的：必填字段没有填写内容',
        '补上该字段的值；空白必填字段在入账与查验环节都会被退回。',
        { document: doc.index, field: f.label, line_text: f.lineText }
      ));
    }
  }
  return out;
}

/* ------------------------------------------------------------ 主入口 */

function analyze(text) {
  const starts = lineStarts(text);
  const lines = text.split(/\r\n|\r|\n/);
  const fields = collectFields(lines, starts);
  const fieldsByLine = new Set(fields.map((f) => f.line));
  const table = collectTableItems(lines, starts, fieldsByLine);
  const inlineItems = collectInlineItems(fields);
  const globalDates = findDatesIn(text);
  const fieldsWithDoc = fields.map((f) => {
    f.document = 0;
    return f;
  });

  // 归属到文档
  const blocks = buildBlocks(lines);
  const labeledDateKeys = [];
  const dateTokensAll = [];
  for (const f of fields) {
    if (DATE_KEYS.indexOf(f.key) < 0) continue;
    const local = findDatesIn(f.value);
    for (const d of local) {
      const start = f.valueStart + d.offset;
      const end = start + d.raw.length;
      dateTokensAll.push({
        raw: d.raw, y: d.y, m: d.m, d: d.d, valid: d.valid, ambiguous: d.ambiguous,
        line: lineOf(starts, start), index: start, key: f.key, label: f.label,
        lineText: f.lineText, labeled: true,
      });
      labeledDateKeys.push([start, end]);
    }
  }
  for (const d of globalDates) {
    const start = d.offset;
    const end = start + d.raw.length;
    if (labeledDateKeys.some((r) => start >= r[0] && start < r[1])) continue;
    dateTokensAll.push({
      raw: d.raw, y: d.y, m: d.m, d: d.d, valid: d.valid, ambiguous: d.ambiguous,
      line: lineOf(starts, start), index: start, key: null, label: '（无字段名）',
      lineText: lines[lineOf(starts, start) - 1] || '', labeled: false,
    });
  }
  dateTokensAll.sort((a, b) => a.index - b.index);

  const placeholdersAll = collectPlaceholders(text, starts);

  const docs = [];
  const rawBlocks = [];
  for (const b of blocks) {
    const blockText = lines.slice(b.from, b.to + 1).join('\n');
    if (!blockText.trim()) continue;
    const inRange = (ln) => ln >= b.from + 1 && ln <= b.to + 1;
    const docFields = fields.filter((f) => inRange(f.line));
    const docItems = [];
    for (const it of table.items) if (inRange(it.line)) docItems.push(it);
    for (const it of inlineItems) if (inRange(it.line)) docItems.push(it);
    const docDates = dateTokensAll.filter((d) => inRange(d.line));
    const docPlaceholders = placeholdersAll.filter((p) => inRange(p.line));
    rawBlocks.push({
      block: b, text: blockText, fields: docFields, items: docItems,
      dates: docDates, placeholders: docPlaceholders,
      hasDate: docDates.length > 0,
      hasTotal: docFields.some((f) => f.key === 'net_total' || f.key === 'gross_total'),
    });
  }
  // 抬头片段（例如票头两行）并入下一块，除非它自己有日期或合计
  const merged = [];
  for (let i = 0; i < rawBlocks.length; i++) {
    const cur = rawBlocks[i];
    if (merged.length && !rawBlocks[i - 1].hard) {
      const prev = merged[merged.length - 1];
      if (!prev.hasDate && !prev.hasTotal) {
        merged.pop();
        cur.fields = prev.fields.concat(cur.fields);
        cur.items = prev.items.concat(cur.items);
        cur.dates = prev.dates.concat(cur.dates);
        cur.placeholders = prev.placeholders.concat(cur.placeholders);
        cur.block = { from: prev.block.from, to: cur.block.to, hard: cur.block.hard };
        cur.text = prev.text + '\n' + cur.text;
        cur.hasDate = cur.hasDate || prev.hasDate;
        cur.hasTotal = cur.hasTotal || prev.hasTotal;
      }
    }
    merged.push(cur);
  }

  let index = 0;
  for (const b of merged) {
    if (!b.fields.length && !b.items.length) continue;
    index++;
    const items = b.items.length ? b.items : docItemsFallback(b.fields);
    const doc = {
      index: index,
      where: merged.length > 1 ? '单据' + index + '：' : '',
      startLine: b.block.from + 1,
      endLine: b.block.to + 1,
      text: b.text,
      fields: b.fields.map((f) => { f.document = index; return f; }),
      items: items,
      dateTokens: b.dates,
      placeholders: b.placeholders,
    };
    docs.push(doc);
  }
  return {
    text: text,
    starts: starts,
    lines: lines,
    fields: fieldsWithDoc,
    items: table.items,
    tableHeaders: table.headerLines,
    docs: docs,
    dates: dateTokensAll,
    placeholders: placeholdersAll,
  };
}

/**
 * 执行免费档的九项AI核对。
 * @param {Object|String} payload {text} | {content} | 纯文本
 * @returns {{status:'success', result:Object}|{status:'insufficient_input', missing:string[], advice:string}}
 */
function run(payload) {
  const mat = collectMaterial(payload);
  if (!mat.text) return insufficient(mat.missing, mat.advice || '请提供票据文本后再核对。');

  const a = analyze(mat.text);
  const docs = a.docs;

  const fieldCount = docs.reduce((n, d) => n + d.fields.length, 0);
  const itemCount = docs.reduce((n, d) => n + d.items.length, 0);

  if (!docs.length || (!fieldCount && !itemCount)) {
    return insufficient(
      ['这段材料（' + a.text.trim().length + ' 个字符）里没有识别出任何可核对的票据要素：'
        + '既没有「发票号码 / 开票日期 / 购方名称 / 销方名称 / 金额 / 税额 / 价税合计 / 报销日期」这类字段标记，'
        + '也没有识别出带表头的明细行。'],
      '请粘贴发票或报销单文本（中英文均可），字段写成「开票日期：2026-03-15」这样的"标签 + 冒号 + 值"格式。'
    );
  }

  let findings = [].concat(
    checkLineArithmeticDocuments(docs),
    checkSubtotalDocuments(docs),
    checkTaxDocuments(docs),
    checkGrossDocuments(docs),
    checkCapitalDocuments(docs),
    checkEntity(docs),
    checkDates(docs),
    checkDuplicates(docs),
    checkPlaceholders(docs)
  );
  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const omitted = Math.max(0, findings.length - MAX_FINDINGS);
  if (omitted) findings = findings.slice(0, MAX_FINDINGS);

  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const byCategory = {};
  for (const c of CHECKS_GIVEN) byCategory[c] = 0;
  for (const f of findings) byCategory[f.category] = (byCategory[f.category] || 0) + 1;

  const dates = a.dates;
  const result = {
    status: 'success',
    service_type: 'INVOICE_CONSISTENCY_FREE',
    scope: {
      checks: CHECKS_GIVEN,
      chars: a.text.trim().length,
      lines: a.lines.length,
      documents: docs.length,
      counts: {
        fields: fieldCount,
        items: itemCount,
        dates: dates.length,
        invoice_nos: docs.filter((d) => firstField(d, 'invoice_no')).length,
        tax_fields: docs.filter((d) => firstField(d, 'tax')).length,
        gross_fields: docs.filter((d) => firstField(d, 'gross_total')).length,
        capital_fields: docs.filter((d) => firstField(d, 'capital')).length,
        placeholders: a.placeholders.length,
        ambiguous_dates: dates.filter((d) => d.ambiguous).length,
        unlabeled_dates: dates.filter((d) => !d.key).length,
      },
      findings_by_category: byCategory,
      tolerance: TOLERANCE,
      tax_tolerance: TAX_TOLERANCE,
      executed_locally: true,
      network_used: false,
    },
    documents_summary: docs.map((d) => {
      const g = firstField(d, 'gross_total');
      const n = firstField(d, 'net_total');
      const i = firstField(d, 'invoice_no');
      const dt = d.dateTokens.filter((x) => x.key === 'invoice_date')[0];
      const b = firstField(d, 'buyer');
      const s = firstField(d, 'seller');
      const e = firstField(d, 'entity');
      return {
        document: d.index,
        lines: d.startLine + '-' + d.endLine,
        invoice_no: i ? i.value.trim() : null,
        invoice_date: dt ? ymdText(dt.y, dt.m, dt.d) : null,
        buyer: b ? b.value.trim() : null,
        seller: s ? s.value.trim() : null,
        entity: e ? e.value.trim() : null,
        net_total: n ? numOf(n.value) : null,
        gross_total: g ? numOf(g.value) : null,
        items: d.items.length,
      };
    }),
    findings: findings,
    summary: {
      p0: p0,
      p1: p1,
      p2: p2,
      total: findings.length,
      by_category: byCategory,
      verdict: p0 ? 'CONTRADICTION_FOUND' : (findings.length ? 'ISSUES_FOUND' : 'CLEAN'),
      omitted: omitted,
    },
    note: '本结果只覆盖上面九项AI核对，每一条都引用了出问题的原文、数字或行号，可由第三方用同一份输入复算；'
      + '其余检查项见 checks_withheld，本次未执行，也不会用默认值编造结论。',
    disclaimer: '只做AI一致性核对，不做发票真伪查验、不构成税务或审计意见；'
      + '本工具不联网、不外发材料，也不调用任何模型。',
  };

  return { status: 'success', result: result };
}

/* 把逐文档的检查套在文档列表上 */
function checkLineArithmeticDocuments(docs) {
  const out = [];
  for (const d of docs) out.push.apply(out, checkLineArithmetic(d));
  return out;
}
function checkSubtotalDocuments(docs) {
  const out = [];
  for (const d of docs) out.push.apply(out, checkSubtotal(d));
  return out;
}
function checkTaxDocuments(docs) {
  const out = [];
  for (const d of docs) out.push.apply(out, checkTax(d));
  return out;
}
function checkGrossDocuments(docs) {
  const out = [];
  for (const d of docs) out.push.apply(out, checkGross(d));
  return out;
}
function checkCapitalDocuments(docs) {
  const out = [];
  for (const d of docs) out.push.apply(out, checkCapital(d));
  return out;
}

/* ---------------------------------------------------------------- 样例 */

const SAMPLE_TEXT = [
  '增值税电子普通发票',
  '发票代码：011002000411',
  '发票号码：12345678',
  '开票日期：2026-03-15',
  '购方名称：北京星河科技有限公司',
  '销方名称：上海云帆信息技术有限公司',
  '',
  '项目名称          数量      单价        金额',
  '服务器运维服务     2        5,000.00    10,000.00',
  '应急响应服务       3        1,000.00    3,500.00',
  '',
  '合计金额：13,000.00',
  '税率：6%',
  '税额：710.00',
  '价税合计：14,100.00',
  '价税合计（大写）：壹万肆仟叁佰元整',
  '',
  '报销单',
  '报销单位：北京星河科技有限责任公司',
  '报销日期：2026-03-10',
  '业务发生日期：2026-04-01',
  '备注：发票编号待补充，经办人 XXX',
  '---',
  '增值税电子普通发票',
  '发票号码：12345678',
  '开票日期：2026-03-15',
  '购方名称：北京星河科技有限公司',
  '销方名称：上海云帆信息技术有限公司',
  '合计金额：13,000.00',
  '税额：710.00',
  '价税合计：14,100.00',
].join('\n');

module.exports = {
  run,
  analyze,
  collectMaterial,
  collectFields,
  collectTableItems,
  collectPlaceholders,
  findDatesIn,
  parseCnCapital,
  parseEnWords,
  parseCapitalField,
  cnToNumber,
  numOf,
  rateOf,
  normName,
  SAMPLE_TEXT,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
};
