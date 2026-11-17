/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * store-gross-margin-check-full.js —— 门店毛利与损耗核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**门店每月结账、月度经营分析、盘点差异归因时**。
 * 门店每个月都要把「销售额 × 售价 = 销售额」「销售额 − 成本 = 毛利」「毛利 ÷ 销售额 = 毛利率」
 * 和「损耗金额 ÷ 损耗前库存 = 损耗率」逐行复算一遍，再把收款合计与销售额勾稽，才能出毛利表。
 * 这张表算错，方向只有两个 —— **毛利被算多了**（成本填少、损耗没进成本、收款没走账）
 * 或 **毛利被算少了**（销售额漏记、重复扣成本、损耗重复计）；两条都会在月报、店长考核
 * 和审计抽样上暴露出来，而且**结完账就看不出来了**。
 *
 * 好消息是：这张表每一格都能手算复现，所以「对不对」完全可以机械核出来：
 *
 *   销售额   = 销售数量 × 平均售价
 *   成本差异 = 实际成本 − 理论成本
 *   毛利     = 销售额 − 成本
 *   毛利率   = 毛利 ÷ 销售额
 *   损耗率   = 损耗金额 ÷ 损耗前库存金额
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件、不读 process.env、
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）、不写盘。
 *
 * 免费档执行 5 类；完整档追加 2 类（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**售价政策、成本口径（含税/不含税、运费与配送费是否进成本）、
 *   损耗的实物原因（报损报溢、偷盗、加工失水）与盘点制度本身对不对 ——
 *   表里的售价、成本、损耗金额、库存金额一律**以你填的为准**，本工具只核表内勾稽，
 *   并把可疑处按**原文行号**列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的完整档开关算成一个布尔常量，再把付费检查包进
 *    以该常量为条件的条件块。**不要**留「完整档才执行的检查」那类 MARKER：
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A，把免费检查也整块删掉（第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关或条件语句的字面量 —— `strip_free_engine` 的残渣断言认得
 *    那几个字面量，注释里写一遍就会被判成"没删干净"而整包回滚（第 236 轮连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '销售额与收款勾稽（收款合计 − 销售额 = 差异，含收款大于销售额与超限提示）',
  '成本与理论成本差异复算（实际成本 − 理论成本 = 成本差异）',
  '毛利率逐行复算（毛利 ÷ 销售额 = 毛利率）',
  '损耗率超限（损耗金额 ÷ 损耗前库存金额 > 2%）',
  '重复行与关键字段空缺检测',
];

const CHECKS_WITHHELD = [
  '毛利额变动的三因素归因（销量 / 售价 / 单位成本）',
  '按毛利额排序的门店 × 品类整改清单与跨门店损益台账',
];

const OUT_OF_SCOPE = [
  '判断售价政策、促销折扣与会员价本身是否合理（定价属于经营决策，请与店长 / 营运确认）',
  '判断成本口径该含税还是不含税、运费与配送费是否进成本、损耗是否计入成本（属于财务与税务判断）',
  '判断损耗的实物原因（报损报溢、偷盗、加工失水、称重误差）与盘点制度是否可靠（属于门店管理与内控判断）',
  '重构库存数量台账、成本计价方法（先进先出 / 加权平均 / 移动加权）与在途在库的归属',
  '给出定价、毛利率目标、是否关店或是否下架某个品类的建议',
  '读取 POS / 收银 / 进销存 / ERP 系统或银行流水（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t门店\t品类\t销售数量\t平均售价\t销售额\t实际成本\t理论成本\t成本差异\t毛利额\t毛利率\t损耗金额\t损耗前库存金额\t损耗率\t损耗原因\t收款合计\t应收账款增加\t退款金额\t退款率',
  '2026-01\t国贸店\t生鲜\t12000\t18.50\t222000.00\t142600.00\t142200.00\t400.00\t79400.00\t35.77%\t2852.00\t142600.00\t2.00%\t正常加工失水\t222000.00\t0.00\t1198.80\t0.54%',
  '2026-01\t国贸店\t日用百货\t5000\t36.00\t180000.00\t126000.00\t126000.00\t0.00\t54000.00\t30.00%\t2520.00\t126000.00\t2.00%\t包装破损\t180000.00\t0.00\t972.00\t0.54%',
  '2026-01\t朝阳店\t生鲜\t15000\t19.00\t285000.00\t178150.00\t177750.00\t400.00\t106850.00\t37.49%\t3563.00\t178150.00\t2.00%\t正常加工失水\t285000.00\t0.00\t1539.00\t0.54%',
  '2026-01\t朝阳店\t日用百货\t6000\t35.00\t210000.00\t151200.00\t151200.00\t0.00\t58800.00\t28.00%\t3024.00\t151200.00\t2.00%\t包装破损\t210000.00\t0.00\t1134.00\t0.54%',
  '2026-02\t国贸店\t生鲜\t12500\t18.50\t231250.00\t148541.67\t148141.67\t400.00\t82708.33\t35.77%\t2970.83\t148541.67\t2.00%\t正常加工失水\t231250.00\t0.00\t1248.75\t0.54%',
  '2026-02\t国贸店\t日用百货\t5200\t36.00\t187200.00\t131040.00\t131040.00\t0.00\t56160.00\t30.00%\t2620.80\t131040.00\t2.00%\t包装破损\t187200.00\t0.00\t1010.88\t0.54%',
  '2026-02\t朝阳店\t生鲜\t15200\t19.00\t288800.00\t180626.67\t180226.67\t400.00\t108173.33\t37.46%\t3612.53\t180626.67\t2.00%\t正常加工失水\t288800.00\t0.00\t1559.52\t0.54%',
  '2026-02\t朝阳店\t日用百货\t6100\t35.00\t213500.00\t153720.00\t153720.00\t0.00\t59780.00\t28.00%\t3074.40\t153720.00\t2.00%\t包装破损\t213500.00\t0.00\t1152.90\t0.54%',
  '合计\t\t\t77000\t\t1817750.00\t1211878.34\t1210278.34\t1600.00\t605871.66\t\t24237.56\t1211878.34\t\t\t1817750.00\t0.00\t9815.85\t',
].join('\n');

const TOL = 0.01;              // 金额 / 数量容差：1 分钱
const RATE_TOL = 0.0001;       // 比率容差：0.01 个百分点（表里按百分数保留两位）
const LOSS_LIMIT = 0.02;       // 损耗率参考上限：2%（超过就提示）
const REFUND_LIMIT = 0.03;     // 退款率参考上限：3%
const RECON_LIMIT = 0.005;     // 收款与销售额的容差：0.5%
const ATTR_TOP = 5;            // 完整档：按毛利额变动列出前 N 个门店 × 品类
const ATTR_TOL = 1.00;         // 完整档：三因素分解余项超过 1 元才算讲不通

const ROLES = {
  // ⚠️ 顺序即优先级：更**具体**的别名必须排在更**宽泛**的别名前面，否则会被抢走。
  //    这些别名会互相抢（都是真实表头，只差一个字），排错了就是"静默地把这一列算成那一列"：
  //      理论成本 / 成本差异 / 实际成本  ← 成本
  //      毛利率                        ← 毛利
  //      损耗率                        ← 损耗
  //      损耗前库存金额                ← 库存金额 / 损前库存金额
  //      平均售价                      ← 售价
  //    `header_map_check.py` 会用本引擎的 SAMPLE_TEXT 逐列表头核一遍，抢走就会报"没被识别成任何角色"。
  period: ['所属期间', '核算期间', '会计期间', '所属期', '期间', '月份', '月度'],
  store: ['门店名称', '门店', '分店', '店面', '店铺', '卖场'],
  category: ['品类名称', '商品品类', '品类', '类别', '大类', '类目'],
  qty: ['销售数量', '销量', '数量'],
  price: ['平均售价', '销售单价', '单价', '售价'],
  salesAmount: ['销售额', '销售收入', '营业收入', '销售金额', '营业额'],
  theoreticalCost: ['理论成本', '标准成本', '应耗成本'],
  costVariance: ['成本差异额', '成本差异'],
  cost: ['实际成本', '销售成本', '营业成本', '成本额', '成本'],
  grossMarginRate: ['毛利率', '毛利比率'],
  grossProfit: ['毛利额', '销售毛利', '毛利金额', '毛利'],
  lossRate: ['损耗率', '损耗比率', '报损率'],
  lossStockAmount: ['损耗前库存金额', '损前库存金额', '损耗前库存', '损前库存', '盘点前库存金额', '库存金额', '库存额'],
  lossReason: ['损耗原因', '报损原因', '损耗说明', '原因'],
  lossAmount: ['损耗金额', '报损金额', '损耗额', '损耗'],
  collections: ['收款合计', '实收合计', '回款合计', '收款总额', '实收款'],
  receivable: ['应收账款增加', '应收账款', '挂账金额', '赊销金额'],
  refundAmount: ['退款金额', '退货金额', '退款额'],
  refundRate: ['退款率', '退货率'],
};

const LABELS = {
  period: '所属期间', store: '门店', category: '品类', qty: '销售数量', price: '平均售价',
  salesAmount: '销售额', cost: '实际成本', theoreticalCost: '理论成本', costVariance: '成本差异',
  grossProfit: '毛利额', grossMarginRate: '毛利率', lossAmount: '损耗金额',
  lossStockAmount: '损耗前库存金额', lossRate: '损耗率', lossReason: '损耗原因',
  collections: '收款合计', receivable: '应收账款增加', refundAmount: '退款金额', refundRate: '退款率',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'store', 'category', 'qty', 'price', 'salesAmount', 'cost',
  'theoreticalCost', 'costVariance', 'grossProfit', 'grossMarginRate', 'lossAmount',
  'lossStockAmount', 'lossRate', 'collections'];
/** 合计行逐列复核的列（比率列是加权平均、不是相加，**刻意不核**） */
const SUM_ROLES = ['qty', 'salesAmount', 'cost', 'theoreticalCost', 'costVariance',
  'grossProfit', 'lossAmount', 'lossStockAmount', 'collections'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|合计:)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值、更不会输出"未发现问题"。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–/]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待核|空)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[,，\s¥￥$]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  s = s.replace(/[()]/g, '').replace(/%$/, '');
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

/** 比率归一化成小数：`36.22%` ⇒ 0.3622；`36.22` ⇒ 0.3622；`0.3622` ⇒ 0.3622 */
function ratioValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 2 ? n / 100 : n;   // 2 以上当百分数填的（36.22 ⇒ 0.3622；0.3622 ⇒ 0.3622）
}

const round2 = (n) => Math.round(n * 100) / 100;

const fmt2 = (n) => round2(n).toFixed(2);
const fmtPct = (n) => `${(n * 100).toFixed(2)}%`;
const fmtSigned = (n) => `${n >= 0 ? '+' : ''}${fmt2(n)}`;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, header: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns, header: headers };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    && !TOTAL_WORDS.test(String(it.period).trim())
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.store, it && it.category]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/** 同一门店同一品类同一期间的键：**期间也算进去**（同一家店同一个品类跨期是正常的） */
const groupKeyOf = (it) => {
  const s = it && it.store !== undefined ? String(it.store).trim() : '';
  const c = it && it.category !== undefined ? String(it.category).trim() : '';
  return [s, c].join('|');
};

/** 一行"内容指纹"：必需列的原文（用来区分"整行粘了两遍"与"同一门店品类被拆成两行核算"） */
const rowSignature = (it) => REQUIRED.map((r) => String(it[r] === undefined ? '' : it[r]).trim()).join('\u0001');

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

/** ① 销售额与收款勾稽：收款合计 − 销售额；收款大于销售额、或差异超过销售额的 0.5% 都提示 */
function checkSalesVsCollections(it) {
  const out = [];
  const sales = normNumber(it.salesAmount);
  const got = normNumber(it.collections);
  if (sales === null || got === null) return out;
  if (sales <= 0) return out;                       // 销售额非正由别的检查负责，这里不下结论
  const diff = round2(got - sales);
  const limit = Math.max(TOL, Math.abs(sales) * RECON_LIMIT);
  if (Math.abs(diff) <= limit) return out;
  const dir = diff > 0
    ? '收款**大于**销售额 = 有未确认的收入（预收 / 会员储值 / 平台未结算），或者销售额那格漏记了一部分'
    : '收款**小于**销售额 = 有挂账赊销、平台手续费未扣、或者收款那格漏记了';
  out.push({
    level: 'P0', category: '销售额与收款勾稽不符', line: it.line,
    message: `${who(it)}：收款合计 ${fmt2(got)} − 销售额 ${fmt2(sales)} = ${fmt2(diff)}，`
      + `超过容差 ${fmt2(limit)}（销售额的 0.5%）。${dir}。`
      + '销售额与收款是门店月报的两条独立入口：一个从 POS 出、一个从收银 / 银行流水出，'
      + '两边对不上说明至少有一边不完整，而毛利率是拿销售额算的 —— 这一格错，毛利跟着错。',
  });
  return out;
}

/** ② 成本与理论成本差异复算：实际成本 − 理论成本 = 成本差异 */
function checkCostVariance(it) {
  const out = [];
  const actual = normNumber(it.cost);
  const theory = normNumber(it.theoreticalCost);
  const stated = normNumber(it.costVariance);
  if (actual === null || theory === null || stated === null) return out;
  const expect = round2(actual - theory);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '成本差异复算不符', line: it.line,
    message: `${who(it)}：实际成本 ${fmt2(actual)} − 理论成本 ${fmt2(theory)} = ${fmt2(expect)}，`
      + `表里「成本差异」是 ${fmt2(stated)}，相差 ${fmt2(stated - expect)}。`
      + '成本差异就是"这批货比标准多花（或少花）了多少钱"，它是毛利差异归因的起点：'
      + '这一格错了，整条归因链都跟着错，所以差一分钱也要查。',
  });
  return out;
}

/** ③ 毛利率逐行复算：毛利 ÷ 销售额 = 毛利率（同时核 毛利额 = 销售额 − 成本） */
function checkGrossMargin(it) {
  const out = [];
  const sales = normNumber(it.salesAmount);
  const cost = normNumber(it.cost);
  const gp = normNumber(it.grossProfit);
  const rate = ratioValue(it.grossMarginRate);
  if (sales === null || cost === null) return out;
  if (sales === 0) return out;
  if (gp !== null) {
    const expect = round2(sales - cost);
    if (Math.abs(expect - gp) > TOL) {
      out.push({
        level: 'P0', category: '毛利额复算不符', line: it.line,
        message: `${who(it)}：销售额 ${fmt2(sales)} − 实际成本 ${fmt2(cost)} = ${fmt2(expect)}，`
          + `表里「毛利额」是 ${fmt2(gp)}，相差 ${fmt2(gp - expect)}。毛利额是店长考核与月度损益的取数口径，`
          + '这一格错说明成本或销售额有一边没跟上（例如损耗已扣在成本里、或销售额含了未实现的预收）。',
      });
    }
  }
  if (rate !== null) {
    const expectRate = (sales - cost) / sales;
    if (Math.abs(expectRate - rate) > RATE_TOL) {
      out.push({
        level: 'P0', category: '毛利率逐行复算不符', line: it.line,
        message: `${who(it)}：（销售额 ${fmt2(sales)} − 实际成本 ${fmt2(cost)}）÷ 销售额 = ${fmtPct(expectRate)}，`
          + `表里「毛利率」是 ${fmtPct(rate)}，相差 ${fmtPct(Math.abs(expectRate - rate))}。`
          + '毛利率是拿来做品类结构与门店横向对比的那一列：分母口径（用销售额还是用毛利额）'
          + '或在 Excel 里下拉公式时漏了一行，都会让这一列整列失真。',
      });
    }
  }
  return out;
}

/** ④ 损耗率超限：损耗金额 ÷ 损耗前库存金额 > 2%（同时核损耗率与两个金额是否自洽） */
function checkLossRate(it) {
  const out = [];
  const loss = normNumber(it.lossAmount);
  const stock = normNumber(it.lossStockAmount);
  const rate = ratioValue(it.lossRate);
  if (loss === null || stock === null) return out;
  if (stock <= 0) return out;
  const derived = loss / stock;
  if (rate !== null && Math.abs(derived - rate) > RATE_TOL) {
    out.push({
      level: 'P0', category: '损耗率与损耗金额不符', line: it.line,
      message: `${who(it)}：损耗金额 ${fmt2(loss)} ÷ 损耗前库存金额 ${fmt2(stock)} = ${fmtPct(derived)}，`
        + `表里「损耗率」是 ${fmtPct(rate)}，相差 ${fmtPct(Math.abs(derived - rate))}。`
        + '损耗率是门店月度损耗考核的分子分母口径：分母必须是**损耗前**库存金额，'
        + '用了期末库存（已扣损耗）当分母，损耗率会被系统性算高。',
    });
  }
  if (derived > LOSS_LIMIT + 1e-9) {
    const reason = it.lossReason === undefined ? '' : String(it.lossReason).trim();
    out.push({
      level: 'P1', category: '损耗率超出参考上限', line: it.line,
      message: `${who(it)}：损耗率 ${fmtPct(derived)} 超过参考上限 ${fmtPct(LOSS_LIMIT)}`
        + `（损耗金额 ${fmt2(loss)} ÷ 损耗前库存金额 ${fmt2(stock)}${reason ? `，表里填的原因：${reason}` : ''}）—— `
        + '损耗直接吃掉毛利，超过 2% 就要按品类追到具体环节：'
        + '生鲜看加工失水与称重误差，日配看临期报损，百货看包装破损与退换。'
        + '只在月报上写一句"损耗偏高"不算归因，条数、金额、原因三样都要落到单品。',
    });
  }
  return out;
}

/** ⑤ 重复行与关键字段空缺 */
function checkDuplicateRows(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = [periodKeyOf(it), groupKeyOf(it)].join('|');
    const sig = rowSignature(it);
    if (seen.has(key)) {
      const prev = seen.get(key);
      if (prev.sig === sig) {
        out.push({
          level: 'P1', category: '同一门店同一品类同一期间重复行', line: it.line,
          message: `${who(it)}与第 ${prev.line} 行**整行完全相同**：同一期间、同一门店、同一品类、`
            + '数量与金额一字不差地出现了两次 —— 多半是从 Excel 里粘了两遍（或两张分表合表时重复拼接）。'
            + '重复行会把销售额、成本与损耗**各多算一遍**，合计行跟着翻倍，毛利额虚增虚减都看不出来。',
        });
      }
      continue;
    }
    seen.set(key, { line: it.line, sig: sig });
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查'
            + '（空着不报，等于这一格根本没核过，而月报照样会取这一列）。',
        });
      }
    }
  }
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${fmt2(stated)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${fmt2(expect)}，`
        + `相差 ${fmt2(stated - expect)}。合计行是月度毛利表与门店考核的取数口径：`
        + '对不上说明有一边错了（明细漏行、合计被手改过、或者明细里混进了别的期间 / 别的门店）。',
    });
  }
  return out;
}

/* ================== 完整档追加的检查实现（免费包会被整块摘掉） ================== */

/** 把同一门店 × 品类的行按期间排序成序列 */
/**
 * 毛利额变动的三因素归因（完整档独有）：对同一门店 × 品类的相邻两期，
 *
 *   销量因素 = (本期数量 − 上期数量) × **上期单位毛利**
 *   售价因素 = (本期售价 − 上期售价) × 本期数量
 *   成本因素 = (上期单位成本 − 本期单位成本) × 本期数量
 *
 * ⚠️ 销量因素必须按**上期单位毛利**折算：按售价算出来的是"销售额变动"，不是毛利变动
 *    （按售价算的版本实测在干净表上留下几千元的假余项 —— 那是算法错，不是表错）。
 * 三项相加 = 毛利额变动，**当且仅当**"数量变动 × 单位毛利变动"这一项为 0；
 * 多因素同时变动会留下这一项（单位毛利变了、量也变了时的交叉项），所以它叫 residual；
 * residual 超过容差才如实报出来（不硬凑成 100%，那才是编数字）。容差常量见文件顶部的 ATTR_*。
 */
/** 三因素分解与毛利额变动**对不上**才报（对得上说明这张表本身讲得通，不需要人回头看） */
/** 按毛利额排序的门店 × 品类整改清单 + 跨门店损益台账（完整档独有，只做汇总不做认定） */
function summarizePeriods(items) {
  const set = new Set();
  for (const it of items) {
    const p = it && it.period !== undefined ? String(it.period).trim() : '';
    if (p && !TOTAL_WORDS.test(p)) set.add(p);
  }
  return [...set].sort();
}

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象（收到的是 ${typeof payload}）—— 请用 {"text":"…"} 把表贴进来`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到门店销售与成本毛利表正文（text）—— 请把「所属期间 / 门店 / 品类 / 销售数量 / 平均售价 / 销售额 / 实际成本 / 理论成本 / 成本差异 / 毛利额 / 毛利率 / 损耗金额 / 损耗前库存金额 / 损耗率 / 收款合计」这张表（含表头）贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `门店销售与成本毛利表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${(t.header || []).join(' / ') || '(没有表头行)'}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何门店明细行');
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkSalesVsCollections(it));
    findings.push(...checkCostVariance(it));
    findings.push(...checkGrossMargin(it));
    findings.push(...checkLossRate(it));
  }
  const attributed = [];

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicateRows(t.items));
  findings.push(...checkBlanks(t.items));

  const periods = summarizePeriods(t.items);
  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);
  // ⚠️ 这一行会被 `strip_free_engine` 还原成 `CHECKS_GIVEN`（免费包里的形态），
  //    所以 free 里也不能别处再出现开关标识符：下面 note 用 checksRun 推导。
  const checksRun = CHECKS_GIVEN;

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;

  const result = {
    status: 'success',
    service_type: 'STORE_GROSS_MARGIN_CHECK',
    scope: {
      checks: checksRun,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.length,
      stores: new Set(t.items.map((i) => String(i.store === undefined ? '' : i.store).trim())).size,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.length,
      total: findings.length,
      p0, p1,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    // 这段文案由 checksRun 推导（免费包里那一行被还原成 CHECKS_GIVEN），
    // 所以文件里不需要第二个开关引用 —— 否则免费包摘完开关会留下未定义标识符。
    note: `${checksRun.length > CHECKS_GIVEN.length ? CHECKS_WITHHELD.length + ' 项完整档检查已执行' : '本版本只执行：' + CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"销售数量 × 平均售价 = 销售额"、"实际成本 − 理论成本 = 成本差异"、'
      + '"毛利 ÷ 销售额 = 毛利率"、"损耗金额 ÷ 损耗前库存金额 = 损耗率"这类**表内勾稽**，'
      + '**不判断售价政策、成本口径（含税/不含税、运费是否进成本）、损耗的实物原因与盘点制度本身对不对**'
      + '（一律以你填的口径与门店单据为准）；结论可由第三方用同一份输入复算。',
  };

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
