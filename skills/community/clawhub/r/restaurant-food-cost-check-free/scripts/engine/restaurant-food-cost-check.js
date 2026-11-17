/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * restaurant-food-cost-check-full.js —— 餐饮菜品成本与出品率核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**餐饮门店每月结账 / 月度成本分析时**。门店每个月都要把
 * 「标准成本卡 vs 实际领用」和「投料量 vs 出餐份数（出品率）」**逐菜**核一遍，才能出毛利表。
 * 这张表算错，方向只有两个 —— **成本被吃掉**（实际领用远高于理论成本、出品率掉下来）或
 * **领用被记少**（漏记 / 未入仓直接领用，账面成本偏低、出品率超过 100%）。两条都会在
 * 月度毛利表、盘点差异和审计抽样上暴露出来，而且**月底盘点前根本发现不了**。
 *
 * 好消息是：这张表每一格都能手算复现，所以「对不对」完全可以机械核出来：
 *
 *   理论耗用 = 出餐份数 × 单份标准用量
 *   成本差异 = 实际领用金额 − 理论成本
 *   出品率   = 理论耗用 ÷ 实际领用数量 × 100%
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**菜品的标准成本卡本身对不对、也不判断领用与出餐的原始单据是否真实
 *    （配方与损耗口径属于厨政、盘点与报损属于门店管理、含税不含税属于财务税务判断）：
 *    表里的标准用量、单份标准成本、成本卡成本、领用数量与金额一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的完整档开关算成一个布尔常量，再把付费检查包进
 *    以该常量为条件的条件块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关或条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍就会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '理论耗用复算（出餐份数 × 单份标准用量 = 理论耗用）',
  '成本差异复算（实际领用金额 − 理论成本 = 成本差异）',
  '合计行逐列复核',
  '同一菜品同一期间重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '出品率超出参考区间提示（默认 85%~105%）',
  '成本差异率超出参考区间提示（默认 ±5%）',
  '实际领用低于理论耗用提示（疑似漏记）',
  '单份标准成本与成本卡不一致提示',
  '同一菜品重复核算同一期间提示',
];

const OUT_OF_SCOPE = [
  '判断菜品标准成本卡本身是否正确（配方、单份投料量、加工损耗与净料率口径属于厨政与成本会计判断，请与厨师长 / 成本会计确认）',
  '判断实际领用与出餐份数的原始单据是否真实完整（月末盘点、报损报废、赠送、试菜、员工餐的真实性属于门店管理判断）',
  '判断领用金额该含税还是不含税、是否包含运费与配送费（进项税与食材成本口径属于财务与税务判断）',
  '处理存货计价方法（先进先出 / 加权平均 / 月末一次加权）以及在制品、半成品、调料的成本分摊',
  '给出菜品定价、毛利率目标或是否下架的建议',
  '读取 POS / 收银系统 / 进销存 / ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t门店\t菜品名称\t出餐份数\t单份标准用量\t计量单位\t理论耗用\t单份标准成本\t成本卡单份成本\t理论成本\t实际领用数量\t实际领用金额\t成本差异\t成本差异率\t出品率',
  '2026-01\t国贸店\t宫保鸡丁\t800\t0.30\t千克\t240.00\t12.00\t12.00\t9600.00\t242.00\t9720.00\t120.00\t1.25%\t99.17%',
  '2026-01\t国贸店\t麻婆豆腐\t1200\t0.25\t千克\t300.00\t4.50\t4.50\t5400.00\t303.00\t5460.00\t60.00\t1.11%\t99.01%',
  '2026-01\t朝阳店\t宫保鸡丁\t650\t0.30\t千克\t195.00\t12.00\t12.00\t7800.00\t196.00\t7860.00\t60.00\t0.77%\t99.49%',
  '2026-01\t朝阳店\t麻婆豆腐\t900\t0.25\t千克\t225.00\t4.50\t4.50\t4050.00\t227.00\t4110.00\t60.00\t1.48%\t99.12%',
  '2026-02\t国贸店\t宫保鸡丁\t820\t0.30\t千克\t246.00\t12.00\t12.00\t9840.00\t248.00\t9900.00\t60.00\t0.61%\t99.19%',
  '2026-02\t国贸店\t麻婆豆腐\t1150\t0.25\t千克\t287.50\t4.50\t4.50\t5175.00\t289.00\t5220.00\t45.00\t0.87%\t99.48%',
  '合计\t\t\t5520\t\t\t1493.50\t\t\t41865.00\t1505.00\t42270.00\t405.00\t\t',
].join('\n');

const TOL = 0.01;             // 金额 / 数量容差：1 分钱、0.01 个计量单位
const YIELD_LOW = 0.85;       // 出品率参考区间下限（低于它 = 投料多、出餐少）
const YIELD_HIGH = 1.05;      // 出品率参考区间上限（高于它 = 领用记少了）
const VAR_LIMIT = 0.05;       // 成本差异率参考区间：±5%

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的别名前面。
  //    「单份标准用量」不能被「用量」抢走、「成本卡单份成本」不能被「单份成本」抢走、
  //    「单份标准成本」不能被「成本」抢走、「成本差异率」不能被「成本差异」抢走、
  //    「出餐份数」不能被「份数」抢走 —— 被抢走的表现是**算错但不报缺列**。
  period: ['所属期间', '核算期间', '会计期间', '所属期', '期间', '月份', '月度'],
  store: ['门店名称', '门店', '分店', '餐厅', '店面', '店铺'],
  dish: ['菜品名称', '菜品', '菜名', '品名', '商品名称', '单品'],
  portions: ['出餐份数', '出品份数', '销售份数', '售卖份数', '实际份数', '出餐数', '份数'],
  theoreticalQty: ['理论耗用量', '理论耗用', '理论用量', '标准耗用', '应耗用量'],
  stdQty: ['单份标准用量', '每份标准用量', '单份用量', '每份用量', '标准用量', '标准投料量', '投料量', '用量'],
  costCardCost: ['成本卡单份标准成本', '成本卡单份成本', '成本卡标准成本', '成本卡单位成本', '成本卡成本'],
  stdCost: ['单份标准成本', '每份标准成本', '单份成本', '标准成本'],
  varianceRate: ['成本差异率', '差异率'],
  costVariance: ['成本差异额', '成本差异'],
  theoreticalCost: ['理论总成本', '理论成本', '应耗成本', '标准成本额', '成本'],
  actualQty: ['实际领用数量', '实际领用量', '领用数量', '实际耗用量', '实际用量'],
  actualAmount: ['实际领用金额', '实际领用额', '领用金额', '实际耗用金额', '实际成本'],
  yieldRate: ['出品率', '出成率', '净料率', '出餐率', '成品率'],
  unit: ['计量单位', '规格单位', '单位'],
};

const LABELS = {
  period: '所属期间', store: '门店', dish: '菜品名称', portions: '出餐份数', stdQty: '单份标准用量',
  unit: '计量单位', theoreticalQty: '理论耗用', stdCost: '单份标准成本', costCardCost: '成本卡单份成本',
  theoreticalCost: '理论成本', actualQty: '实际领用数量', actualAmount: '实际领用金额',
  costVariance: '成本差异', varianceRate: '成本差异率', yieldRate: '出品率',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'dish', 'portions', 'stdQty', 'theoreticalQty', 'stdCost',
  'costCardCost', 'theoreticalCost', 'actualQty', 'actualAmount', 'costVariance',
  'varianceRate', 'yieldRate'];
/** 合计行逐列复核的列（比率列是加权平均、不是相加，**刻意不核**） */
const SUM_ROLES = ['portions', 'theoreticalQty', 'theoreticalCost', 'actualQty', 'actualAmount', 'costVariance'];
/**
 * 免费档负值检测覆盖的列：数量与金额。
 * ⚠️ 刻意**不含**成本差异与成本差异率 —— 实际领用低于理论成本时它们本来就是负数（节约），
 *    那是正常结果，不是填错。
 */
const NEGATIVE_ROLES = ['portions', 'stdQty', 'theoreticalQty', 'stdCost', 'costCardCost',
  'theoreticalCost', 'actualQty', 'actualAmount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|合计:)$/;

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
  return s === '' || /^[-—–/]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待核|空)$/i.test(s);
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
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 比率归一化成小数：`1.25%` ⇒ 0.0125；`1.25` ⇒ 0.0125；`0.0125` ⇒ 0.0125；`99.17%` ⇒ 0.9917 */
const round2 = (n) => Math.round(n * 100) / 100;

const fmt2 = (n) => round2(n).toFixed(2);
const fmtPct = (n) => `${(n * 100).toFixed(2)}%`;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
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
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.store, it && it.dish]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/** 同一菜品同一期间的键：**门店也算进去**（两家店同一个菜同期是正常的，不算重复） */
const dishKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  const s = it && it.store !== undefined ? String(it.store).trim() : '';
  const d = it && it.dish !== undefined ? String(it.dish).trim() : '';
  return [p, s, d].join('|') || `第 ${it && it.line} 行`;
};

/** 一行"内容指纹"：必需列的原文（用来区分"整行粘了两遍"与"同一菜品被拆成两行核算"） */
const rowSignature = (it) => REQUIRED.map((r) => String(it[r] === undefined ? '' : it[r]).trim()).join('\u0001');

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkTheoreticalQty(it) {
  const out = [];
  const portions = normNumber(it.portions);
  const stdQty = normNumber(it.stdQty);
  const stated = normNumber(it.theoreticalQty);
  if (portions === null || stdQty === null || stated === null) return out;
  const expect = round2(portions * stdQty);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '理论耗用复算不符', line: it.line,
    message: `${who(it)}：出餐份数 ${portions} × 单份标准用量 ${stdQty} = ${fmt2(expect)}，`
      + `表里「理论耗用」是 ${fmt2(stated)}，相差 ${fmt2(stated - expect)}。`
      + '理论耗用是"这份菜按标准配方应该用掉多少料"，它是出品率与成本差异的基数：'
      + '这一格错了，出品率与成本差异都会跟着错，而且看不出是哪一格先错的。',
  });
  return out;
}

function checkCostVariance(it) {
  const out = [];
  const actual = normNumber(it.actualAmount);
  const theory = normNumber(it.theoreticalCost);
  const stated = normNumber(it.costVariance);
  if (actual === null || theory === null || stated === null) return out;
  const expect = round2(actual - theory);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '成本差异复算不符', line: it.line,
    message: `${who(it)}：实际领用金额 ${fmt2(actual)} − 理论成本 ${fmt2(theory)} = ${fmt2(expect)}，`
      + `表里「成本差异」是 ${fmt2(stated)}，相差 ${fmt2(stated - expect)}。`
      + '成本差异就是"多领了多少钱"，它是毛利表上的成本超支数：正数是超支（吃掉毛利），'
      + '负数是节约。差一分钱都要查，因为月报直接取这一列。',
  });
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
        + `相差 ${fmt2(stated - expect)}。合计行是月度毛利表与成本考核的取数口径：`
        + '对不上说明有一边错了（明细漏行、合计被手改过、或者明细里混进了别的期间的菜）。',
    });
  }
  return out;
}

function checkDuplicateRows(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = dishKeyOf(it);
    const sig = rowSignature(it);
    if (seen.has(key)) {
      const prev = seen.get(key);
      if (prev.sig === sig) {
        out.push({
          level: 'P1', category: '同一菜品同一期间重复行', line: it.line,
          message: `${who(it)}与第 ${prev.line} 行**整行完全相同**：同一门店、同一菜品、同一期间、`
            + '数量与金额一字不差地出现了两次 —— 多半是从 Excel 里粘了两遍（或两张分表合表时重复拼接）。'
            + '重复行会把出餐份数、领用数量与成本差异**各多算一遍**，合计行跟着翻倍。',
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
            + '（空着不报，等于这一格根本没核过）。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${fmt2(v)}（负数）—— 出餐份数、标准用量、`
        + '单份成本、理论成本与领用金额都不该为负，多半是录数时符号掉了或公式写反了。'
        + '红字冲回 / 退货要单独列示并在备注里说明，不能直接填负数。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到餐饮菜品成本与出品率核对表正文（text）—— 请把「所属期间 / 门店 / 菜品名称 / 出餐份数 / 单份标准用量 / 理论耗用 / 单份标准成本 / 成本卡单份成本 / 理论成本 / 实际领用数量 / 实际领用金额 / 成本差异 / 成本差异率 / 出品率」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `餐饮菜品成本与出品率核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何菜品明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkTheoreticalQty(it));
    findings.push(...checkCostVariance(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicateRows(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const result = {
    status: 'success',
    service_type: 'RESTAURANT_FOOD_COST_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"出餐份数 × 单份标准用量 = 理论耗用"、"实际领用金额 − 理论成本 = 成本差异"'
      + '这类**表内勾稽**与档位提示，**不判断标准成本卡本身对不对、也不判断领用与出餐的原始单据是否真实**'
      + '（以你填的口径与厨政单据为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
