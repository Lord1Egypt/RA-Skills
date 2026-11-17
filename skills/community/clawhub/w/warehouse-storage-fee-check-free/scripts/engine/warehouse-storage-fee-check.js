/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * warehouse-storage-fee-check-full.js —— 仓储费与库龄结算核对（完整档 / 买断版）
 *
 * 谁在什么时候必须做这件事：**仓储/物流的财务与对账岗，每月收到第三方仓库（3PL）或自有仓的
 * 仓储费结算单 + 库龄明细表时**，必须在付款前把这张表核一遍。仓储费是**乘出来的**
 * （体积或托盘数 × 单价 × 计费天数，计费天数 = 库龄天数 − 免租期），
 * 最容易在这里被多收：免租期没扣、天数按自然月算、单价悄悄上调、库龄超期附加费重复计。
 * 这些全都**能算出来对错**，不需要任何行业外部标准。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），
 * 不读 `process.env`，不写盘。
 *
 * 核心可算关系（都能手算复现）：
 *   计费天数       = 库龄天数 − 免租期                       （免费项 2）
 *   仓储费         = （库存体积 或 托盘数）× 单价 × 计费天数   （免费项 1）
 *   超期附加费     = 超期占用天数 × 超期日费率                 （免费项 3）
 *   应付合计       = 仓储费 + 库龄超期附加费                   （免费项 4）
 *   合计行         = 各明细行逐列相加                          （免费项 5）
 *
 * 免费档执行 8 项（见 CHECKS_GIVEN）；完整档另追加 8 项（见 CHECKS_WITHHELD）。
 * 材料不足时**绝不给结论**：返回 status='insufficient_input' 并列出缺什么。
 * 每条结论都带原文行号（line）。
 * ⚠️ 本工具**不规定**仓库收费标准、免租期政策与超期附加费率：单价、免租期天数、每日费率
 *    一律**以表里给出的数字为准**，只做表内复算与表内互相印证；结论可由第三方用同一份输入复算。
 */

const CHECKS_GIVEN = [
  '逐行复算仓储费：库存体积（或托盘数）× 结算单价 × 计费天数 = 仓储费（并按出入库日期复核库龄天数）',
  '计费天数复核：库龄天数 − 免租期 = 计费天数（表里第 G−H=I 列的关系）',
  '库龄超期附加费复算：超期占用天数 × 超期日费率 = 库龄超期附加费',
  '应付合计勾稽：仓储费 + 库龄超期附加费 = 应付合计；合计行 = 各明细行逐列相加',
  '重复行与空缺列检测（同一仓库+客户+物料多行；仓库/客户/物料/库龄天数/计费天数/仓储费/应付合计为空或占位符）',
  '数量、单价或金额为负检测；计费天数出现小数检测',
];

const CHECKS_WITHHELD = [
  '跨仓库 / 跨客户汇总台账：按仓库、按客户双向汇总计费天数、体积、仓储费、超期附加费与应付合计',
  '仓库小计行勾稽：本仓库明细逐列相加 = 表里那一行「仓库小计」',
  '超收金额处理清单：按超收金额从大到小排序，逐条给出「同款物料基准单价 → 应收 → 实收 → 超收」证据链',
  '费用差异归因：同仓库同客户同物料的两行，把差额拆成单价效应 / 天数效应 / 体积效应三块并各自配平',
  '库龄超期附加费超标清单：按超期加成率（附加费 ÷ 仓储费）从高到低排序，给出按金额加权的超期费用占比',
  '同款物料计费口径不一致提示：表内出现两种以上结算单价，或两种以上超期日费率',
  '合计行数量列勾稽：合计行的体积 / 托盘数 = 各明细行逐列相加',
  '空体积却有仓储费检测（计价数量与单价全空时，这一行的仓储费无从复算）',
  '库龄天数与出入库日期不符提示（表里的库龄天数 ≠ 出库日期 − 入库日期）',
];

const OUT_OF_SCOPE = [
  '判断仓库收费标准、免租期政策与超期附加费率是否合理（以双方合同与报价单为准，本工具只按表里的数字复算）',
  '核对出入库单、托盘流转记录、库存台账本身是否准确（需要你先导出成文本贴进来）',
  '处理税率、发票、付款账期与预付款抵扣',
  '读取 WMS / ERP / 结算系统导出的二进制文件（请先导出成文本或 JSON）',
  '跨期比较（上月 vs 本月单价与天数）——需要你自己把两期贴成同一张表',
];

/**
 * 干净样例：**逐列对齐由代码保证**（下列 18 个表头与每一行的 18 个格子一一对应），
 * 每条关系都算平：逐行复算、库龄−免租期=计费天数、超期天数×日费率=附加费、
 * 仓储费+附加费=应付合计、仓库小计行、合计行；同款物料在整个表内只有一个单价，
 * 计价基础（体积/托盘）逐行注明 ⇒ 两档跑它都必须 0 命中。
 */
const SAMPLE_HEAD = [
  '仓库', '客户', '物料', '入库日期', '出库日期', '库存体积', '托盘数', '库龄天数', '免租期',
  '计费天数', '计价基础', '体积费率', '结算单价', '仓储费', '超期占用天数', '超期日费率',
  '库龄超期附加费', '应付合计',
];
const SAMPLE_ROWS = [
  ['上海仓', 'C001', '镀锌板卷', '2026-01-01', '2026-02-01', '100.00', '5', '31', '0', '31', '体积', '1.20', '1.20', '3720.00', '0', '0', '0.00', '3720.00'],
  ['上海仓', 'C002', '聚丙烯颗粒', '2026-01-01', '2026-02-01', '80.00', '4', '31', '0', '31', '体积', '1.20', '1.20', '2976.00', '0', '0', '0.00', '2976.00'],
  ['上海仓', 'C003', '纸箱', '2026-01-01', '2026-02-01', '50.00', '3', '31', '0', '31', '体积', '1.20', '1.20', '1860.00', '0', '0', '0.00', '1860.00'],
  ['仓库小计', '', '', '', '', '230.00', '12', '', '', '', '', '', '', '8556.00', '0', '', '0.00', '8556.00'],
  ['广州仓', 'C001', '镀锌板卷', '2026-01-01', '2026-02-01', '120.00', '6', '31', '0', '31', '体积', '1.20', '1.20', '4464.00', '0', '0', '0.00', '4464.00'],
  ['广州仓', 'C002', '聚丙烯颗粒', '2026-01-01', '2026-02-01', '90.00', '4', '31', '0', '31', '体积', '1.20', '1.20', '3348.00', '0', '0', '0.00', '3348.00'],
  ['广州仓', 'C003', '纸箱', '2026-01-01', '2026-02-01', '40.00', '2', '31', '0', '31', '体积', '1.20', '1.20', '1488.00', '0', '0', '0.00', '1488.00'],
  ['合计', '', '', '', '', '480.00', '24', '', '', '', '', '', '', '17856.00', '0', '', '0.00', '17856.00'],
];
const SAMPLE_TEXT = [SAMPLE_HEAD, ...SAMPLE_ROWS].map((r) => r.join('\t')).join('\n');

const TOL = 0.01;
const MATERIALITY = 0.005;

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的表头必须排在更宽泛的前面**，否则更宽泛的关键词会把那一列整个抢走，
  //    而且不会报缺列（只会静默算错）——表头角色映射守卫 `tools/header_map_check.py` 就是钉这个的：
  //    · 「体积费率」含「体积」 ⇒ 必须排在 volume（库存体积）之前；
  //    · 「库龄超期附加费」含「库龄」和「超期」 ⇒ 必须排在 ageDays / overDays / overRate 之前；
  //    · 「超期日费率」含「超期」 ⇒ 必须排在 overDays（超期占用天数）之前；
  //    · 「超期占用天数」含「超期天数」的反向不成立，但仍让长别名优先，读起来更安全。
  overFee: ['库龄超期附加费', '超期附加费', '库龄超期费'],
  basis: ['计价基础', '计价单位', '计费基础'],
  // 「体积费率」这一列也要有**自己的**角色，否则会落到更宽泛的 volume（库存体积）上，
  // 把库存体积整列覆盖掉（表头角色映射守卫会因此报「列被覆盖/丢掉」）。它是说明列，
  // 只用来展示，不参与复算（单价就是元/计价单位·天）。
  volumeRateLabel: ['体积费率', '立方费率'],
  overRate: ['超期日费率', '超期费率', '逾期费率'],
  overDays: ['超期占用天数', '超期天数', '逾期天数'],
  ageDays: ['库龄天数', '在库天数', '库龄'],
  freeDays: ['免租期', '免租天数', '免仓期'],
  billDays: ['计费天数', '结算天数', '计费日数'],
  unitPrice: ['结算单价', '单价'],
  storageFee: ['仓储费', '仓租费', '存储费'],
  volume: ['库存体积', '体积', '立方数'],
  pallets: ['托盘数', '托盘', '板数'],
  inbound: ['入库日期', '入库日', '进仓日期'],
  outbound: ['出库日期', '出库日', '出仓日期'],
  warehouse: ['仓库名称', '仓库', '库房', '仓别'],
  customer: ['客户名称', '客户', '货主', '委托方'],
  material: ['物料名称', '物料', '品名', '货品', '商品'],
  payable: ['应付合计', '应付金额', '结算合计'],
};

const LABELS = {
  warehouse: '仓库', customer: '客户', material: '物料', inbound: '入库日期', outbound: '出库日期',
  volume: '库存体积', pallets: '托盘数', ageDays: '库龄天数', freeDays: '免租期', billDays: '计费天数',
  basis: '计价基础', volumeRateLabel: '体积费率', unitPrice: '结算单价', storageFee: '仓储费',
  overDays: '超期占用天数', overRate: '超期日费率', overFee: '库龄超期附加费', payable: '应付合计',
};

const SUM_BASES = ['volume', 'pallets'];

const REQUIRED = ['warehouse', 'customer', 'material', 'ageDays', 'billDays', 'storageFee', 'payable'];
const SUM_ROLES = ['volume', 'pallets', 'storageFee', 'overFee', 'payable'];
const AMOUNT_ROLES = ['storageFee', 'overFee', 'payable'];
const MAX_ROLES = ['volume', 'pallets', 'unitPrice', 'storageFee', 'overFee', 'payable'];
const INT_ROLES = ['ageDays', 'freeDays', 'billDays', 'overDays'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总|仓库小计|客户小计|合计金额)$/;

/** 材料不足：说清楚缺什么，并且明确不给结论 */
function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把仓储费结算单与库龄明细表（**含表头**）整块贴进来：'
      + '{"text": "仓库\\t客户\\t物料\\t入库日期\\t出库日期\\t库龄天数\\t免租期\\t计费天数\\t单价\\t仓储费\\t超期占用天数\\t超期日费率\\t库龄超期附加费\\t应付合计\\n上海仓\\tC001\\t镀锌板卷\\t…"}，'
      + '或先用 --sample 看看需要哪些列。材料不足时本工具不做任何认定，也不套用默认值。',
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
  // 会计写法：括号 = 负数。**必须先剥括号再判是不是数字**，否则 '(100.00)' 整串过不了数字正则。
  const s0 = String(raw).trim().replace(/[¥￥$,，\s]/g, '').replace(/%$/, '');
  const negParen = /^\(.*\)$/.test(s0);
  const s = negParen ? s0.slice(1, -1).trim() : s0;
  if (!/^[-+]?\d*\.?\d+$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return negParen ? -Math.abs(n) : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

/* 日期工具（只在计费天数缺失时用来兜底重算，绝不覆盖表里填好的数字） */
const DAY_MS = 86400000;

function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '').replace(/[/.]/g, '-');
  const m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if (!m) return null;
  const y = Number(m[1]); const mo = Number(m[2]); const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const t = Date.UTC(y, mo - 1, d);
  return Number.isFinite(t) ? t : null;
}

function dateDiff(a, b) {
  if (a === null || b === null) return null;
  return Math.round((b - a) / DAY_MS);
}

function derivedDays(it) {
  if (!isBlank(it.billDays)) return normNumber(it.billDays);
  return dateDiff(normDate(it.inbound), normDate(it.outbound));
}

/** 计费基数候选：表里给出且非零的体积 / 托盘数 */
function basesOf(it) {
  const out = [];
  for (const role of SUM_BASES) {
    const v = normNumber(it[role]);
    if (v !== null && v !== 0) out.push({ role, label: LABELS[role], qty: v });
  }
  return out;
}

/**
 * 本行实际用哪种计价基础 —— **必须先确定这个，否则单价根本不可比**：
 * 元/m³·天 与 元/托·天 差一个量级，拿体积口径的单价去乘托盘数会得出荒唐的"超收"。
 *   ① 表里有「计价基础」列 ⇒ 以它为准（体积/m³/立方 → volume；托盘/板/托 → pallets）；
 *   ② 没有这一列时：只有一种候选数量就给那一种；两种都有 ⇒ 用仓储费反推，取更接近的口径。
 */
/** 本行的单价在哪个计价基础上才有意义（跨计价基础的单价不可比） */
function parseTable(text) {
  const raw = String(text === undefined || text === null ? '' : text)
    .split(/\r?\n/)
    .filter((l) => l.trim() !== '');
  const headerLine = raw.length ? raw[0] : '';
  const headers = splitRow(headerLine);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const unmappedColumns = headers.filter((h, i) => h !== '' && !roles[i]);
  const items = [];
  // ⚠️ 三类「非明细行」必须都从 items 里摘出去，否则会被当成明细重复计入加总：
  //    · 全表合计行（仓库/客户/物料任一处写「合计」）→ totals.row
  //    · 仓库小计行（写「仓库小计」）              → totals.warehouseRows
  //    · 客户小计行（写「客户小计」）              → totals.customerRows
  const totals = { row: null, line: null, warehouseRows: [], customerRows: [] };
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    let isTotal = false;
    let isWarehouseSub = false;
    let isCustomerSub = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role !== 'warehouse' && role !== 'customer' && role !== 'material') return;
      const s = String(v).trim();
      if (!TOTAL_WORDS.test(s)) return;
      if (/仓库小计/.test(s) || (role === 'warehouse' && /^(小计|汇总)$/.test(s))) isWarehouseSub = true;
      else if (/客户小计/.test(s) || (role === 'customer' && /^(小计|汇总)$/.test(s))) isCustomerSub = true;
      else isTotal = true;
    });
    if (isTotal) {
      if (totals.row === null) { totals.row = row; totals.line = i + 1; }
    } else if (isWarehouseSub) {
      totals.warehouseRows.push(row);
    } else if (isCustomerSub) {
      totals.customerRows.push(row);
    } else items.push(row);
  }
  return { items, totals, missingColumns, unmappedColumns, header: headers };
}

const cell = (it, role) => String((it && it[role]) === undefined ? '' : it[role]).trim();

const who = (it) => {
  const w = cell(it, 'warehouse');
  const m = cell(it, 'material');
  const c = cell(it, 'customer');
  if (w && m) return `${w} ${c ? c + ' ' : ''}${m}`;
  if (w) return w;
  if (m) return m;
  return `第 ${it && it.line} 行`;
};

const dupKey = (it) => {
  const w = cell(it, 'warehouse');
  const c = cell(it, 'customer');
  const m = cell(it, 'material');
  if (!w || !c || !m) return '';
  return `${w}|${c}|${m}`;
};

/** 多层分组：按 groupRoles 指定的角色值组合成 key */
/** 在合计/小计行里找「某一列等于给定值」的那一行 */
/* ================================ 免费档检查项 ================================ */

function checkStorageRecompute(it) {
  const stated = normNumber(it.storageFee);
  const days = derivedDays(it);
  const price = normNumber(it.unitPrice);
  if (stated === null || days === null || price === null) return null;
  const bases = basesOf(it);
  if (!bases.length) return null;
  const exp = bases.map((b) => ({ label: b.label, qty: b.qty, expect: round2(b.qty * price * days) }));
  if (exp.some((e) => Math.abs(e.expect - stated) <= TOL)) return null;
  const detail = exp
    .map((e) => `按${e.label} ${e.qty.toFixed(2)} × 单价 ${price.toFixed(2)} × ${days} 天 = ${e.expect.toFixed(2)}`)
    .join('；');
  return {
    level: 'P0', category: '仓储费复算不符', line: it.line,
    message: `${who(it)}：${detail}，但表里的仓储费是 ${stated.toFixed(2)}，`
      + `与最接近的口径也相差 ${round2(stated - exp[0].expect).toFixed(2)} —— `
      + '仓储费就是「计价数量 × 单价 × 计费天数」乘出来的：先看计费天数有没有被按自然月多算、再看单价有没有被调过。',
  };
}

function checkBilledDays(it) {
  // 这里刻意**只认表里的「计费天数」列**，不走 derivedDays 的日期兜底：
  // 「库龄天数 − 免租期 = 计费天数」是表内声明的关系，用兜底值会把这一层关系测没了。
  const age = normNumber(it.ageDays);
  const free = isBlank(it.freeDays) ? 0 : normNumber(it.freeDays);
  const bill = normNumber(it.billDays);
  if (age === null || free === null || bill === null) return null;
  const expect = round2(age - free);
  if (Math.abs(bill - expect) <= TOL) return null;
  return {
    level: 'P0', category: '免租期与实际计费天数不符', line: it.line,
    message: `${who(it)}：库龄天数 ${age} − 免租期 ${free} = ${expect} 天，但表里的计费天数是 ${bill}，`
      + `相差 ${round2(bill - expect)} 天 —— 免租期没扣干净（或扣多了）都会被直接乘进仓储费，`
      + '而计费天数是仓储费与超期天数的共同基础，先把它钉死。',
  };
}

function checkOverFee(it) {
  const stated = normNumber(it.overFee);
  const overDays = isBlank(it.overDays) ? 0 : normNumber(it.overDays);
  const rate = normNumber(it.overRate);
  if (stated === null || overDays === null || rate === null) return null;
  const expect = round2(overDays * rate);
  if (Math.abs(stated - expect) <= TOL) return null;
  return {
    level: 'P0', category: '库龄超期附加费复算不符', line: it.line,
    message: `${who(it)}：超期占用天数 ${overDays} × 超期日费率 ${rate.toFixed(2)} = ${expect.toFixed(2)}，`
      + `但表里的库龄超期附加费是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— `
      + '超期占用天数是从库龄天数里减出来的（库龄 − 免租期 − 合同允许占用天数），'
      + '天数多写一天就按日费率放大一次。',
  };
}

function checkPayableSum(it) {
  const payable = normNumber(it.payable);
  const storage = normNumber(it.storageFee);
  if (payable === null || storage === null) return null;
  const over = normNumber(it.overFee) || 0;
  const sum = round2(storage + over);
  if (Math.abs(payable - sum) <= TOL) return null;
  return {
    level: 'P0', category: '应付合计与明细不符', line: it.line,
    message: `${who(it)}：仓储费 ${storage.toFixed(2)} + 库龄超期附加费 ${over.toFixed(2)} = ${sum.toFixed(2)}，`
      + `但应付合计写的是 ${payable.toFixed(2)}，相差 ${round2(payable - sum).toFixed(2)} —— `
      + '付款金额就是这一列，它和明细对不上说明有一边被改过。',
  };
}

function checkAmountRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行金额列与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 合计行被改过，或者有明细行没贴进来`
      + '（中间的仓库小计行要贴成「仓库小计」，它们不会被算进明细加总）。',
  });
  return out;
}

/* ——— 以下为买断档：合计行的数量列（体积/托盘数）逐列勾稽 ——— */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = dupKey(it);
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一仓库同一客户同一物料出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次 —— `
          + '同一仓库 + 同一客户 + 同一物料正常只该有一行；从 Excel 复制整月数据时贴了两遍，费用会凭空翻倍。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        out.push({
          level: 'P0', category: '关键列空缺或占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${cell(it, role) || '空'}）—— `
            + '缺了它这条明细就无法复算，请回到结算单补上再核。',
        });
      }
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of MAX_ROLES) {
      const v = normNumber(it[role]);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0', category: '数量、单价或金额为负', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— `
            + '红字冲回应当单独列一行并注明原因，否则会与正常费用混在一起，合计看着正常但明细多扣了钱。',
        });
      }
    }
  }
  return out;
}

/** 数量、单价或金额为负（红字冲回要单独列行） */
function checkNegativesAll(items) {
  return checkNegatives(items);
}

/** 计费天数的完整性：出现小数说明用了半个计费周期，会直接把误差乘进金额 */
function checkIntFields(items) {
  const out = [];
  for (const it of items) {
    for (const role of INT_ROLES) {
      const v = normNumber(it[role]);
      if (v === null || Math.abs(v - Math.round(v)) <= TOL) continue;
      out.push({
        level: 'P1', category: '天数出现小数', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v} 天（不是整数）—— `
          + '天数按自然日计，出现小数通常是把半个计费周期四舍五入进了天数，会直接把误差乘进金额。',
      });
    }
  }
  return out;
}

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到结算单正文（text）—— 请把「仓库 / 客户 / 物料 / 入库日期 / 出库日期 / 库龄天数 / 免租期 / 计费天数 / 单价 / 仓储费 / 超期占用天数 / 超期日费率 / 库龄超期附加费 / 应付合计」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns.length) {
    const rawHeader = String(text).split(/\r?\n/).filter((l) => l.trim() !== '')[0] || '';
    return insufficient([
      `结算单缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(rawHeader).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何仓储费明细行');
  }

  const findings = [];

  for (const it of t.items) {
    const a = checkStorageRecompute(it); if (a) findings.push(a);
    const b = checkBilledDays(it); if (b) findings.push(b);
    const c = checkOverFee(it); if (c) findings.push(c);
    const d = checkPayableSum(it); if (d) findings.push(d);
  }
  for (const x of checkNegativesAll(t.items)) findings.push(x);
  for (const x of checkIntFields(t.items)) findings.push(x);
  for (const role of AMOUNT_ROLES) {
    for (const f of checkAmountRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  // ⚠️ 付费检查一律用 `?.` 取值：万一某条付费检查被摘掉/被改成返回空（工厂变异门禁会这么干），
  //    这里**静默少一条结论**而不是整包崩掉 —— 崩溃会把"变异生效"这件事藏起来，
  //    而少一条付费结论会让对照测试当场红，这才是门禁想要的效果。
  const ledger = {};


  // ⚠️ 免费档摘除工具 `tools/strip_free_engine.py` 只会删掉「开关声明 + if(paid)/三元 paid?…:…」这几类形态：
  //    它**不会**删掉别处裸露的 `paid` 标识符。所以 `paid` 只允许出现在下面这两行里，
  //    别处一律用它们算好的结果（否则免费包里会留下 `paid is not defined`）。
  const checksRun = CHECKS_GIVEN;
  const checksNotRun = CHECKS_WITHHELD.slice();

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let payableTotal = 0; let storageTotal = 0; let overTotal = 0; let daysTotal = 0;
  const warehouseSet = new Set(); const customerSet = new Set();
  for (const it of t.items) {
    const a = normNumber(it.payable); if (a !== null) payableTotal += a;
    const b = normNumber(it.storageFee); if (b !== null) storageTotal += b;
    const c = normNumber(it.overFee); if (c !== null) overTotal += c;
    const d = normNumber(it.billDays); if (d !== null) daysTotal += d;
    const w = cell(it, 'warehouse'); if (w) warehouseSet.add(w);
    const cu = cell(it, 'customer'); if (cu) customerSet.add(cu);
  }

  const rows = t.items.length;
  const result = {
    status: 'success',
    service_type: 'WAREHOUSE_STORAGE_FEE_CHECK',
    scope: {
      checks: checksRun,
      checks_not_run: checksNotRun,
      rows,
      warehouses: warehouseSet.size,
      customers: customerSet.size,
      bill_days_total: round2(daysTotal),
      storage_fee_total: round2(storageTotal),
      over_fee_total: round2(overTotal),
      payable_total: round2(payableTotal),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows,
      warehouses: warehouseSet.size,
      customers: customerSet.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本次执行 ${checksRun.length} 项检查；未执行的检查项见 scope.checks_not_run：`
      + (checksNotRun.length ? checksNotRun.join('、') : '（无）'),
    disclaimer: '只核「计价数量 × 单价 × 计费天数 = 仓储费」「库龄天数 − 免租期 = 计费天数」'
      + '「超期占用天数 × 超期日费率 = 超期附加费」「仓储费 + 超期附加费 = 应付合计」这类**表内可复算**的关系；'
      + '**不规定仓库收费标准、免租期政策与超期附加费率**（以合同/报价单为准），'
      + '超收基准取的是**本表同款物料的单价均值**；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, AMOUNT_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
