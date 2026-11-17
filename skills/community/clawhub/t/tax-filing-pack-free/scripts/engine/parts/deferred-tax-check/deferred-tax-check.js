#!/usr/bin/env node
'use strict';
/**
 * deferred-tax-check.js —— 递延所得税与暂时性差异核对（免费档 / 完整档共用源码）
 *
 * 真实痛点：**每季度与年度汇算时都要核一遍递延所得税台账**。
 * 这张表把会计口径与税法口径的差额落在纸面上：
 *   ① 暂时性差异 = 账面价值 − 计税基础（正数＝应纳税暂时性差异，负数＝可抵扣暂时性差异）
 *   ② 递延所得税资产/负债 = 暂时性差异 × 适用税率（方向：可抵扣 → 资产；应纳税 → 负债）
 *   ③ 本期变动 = 期末余额 − 期初余额（应与利润表「递延所得税费用」勾稽）
 *   ④ 可抵扣亏损：结转期用尽或确认条件不满足时**不得**确认递延所得税资产
 * 税率用错、差异方向搞反、亏损条件不够却确认了资产 —— 是审计调整与税企争议的高发点。
 * 纯算术 + 口径一致性，但行一多、税率多档、方向一转就极易错。
 *
 * 与已有能力的区别：`cit-adjustment-check` 核的是**纳税调整明细**（调增调减、应纳税所得额）；
 * 本能力核的是**递延所得税台账**（账面价值/计税基础 → 暂时性差异 → 递延余额与本期变动），
 * 是资产负债表口径的另一张表。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 *      可选入参：rate（给定税率）、period（本表所属期，用于比对亏损结转期）；都不给也能跑。
 * 刻意不做：不联网、不查税率文库、不调用大模型；材料不足不给结论；不给税务/审计意见，
 * 只核**表内可算关系与口径一致性**。
 *
 * ⚠️ 分层写法用**形态 B**：本文件里另有一个由订阅标记打开的付费执行开关（读入参里的
 *    开启标记），五条付费检查全部包在它的分支里（**不要**再加「完整档才执行的检查」那类
 *    MARKER——两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，
 *    第 236 轮踩过）。免费包那份引擎由 `python3 tools/strip_free_engine.py --apply` 自动摘掉
 *    付费实现；`CHECKS_WITHHELD` 只是"未执行的检查项"的说明文本，不是实现。
 */

const CHECKS_GIVEN = [
  '暂时性差异逐项复算（账面价值 − 计税基础）',
  '递延所得税资产/负债余额复算（暂时性差异 × 适用税率）',
  '本期变动勾稽（期末余额 − 期初余额）',
  '方向标记与差异正负号的一致性核对',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复项目检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '差异方向与确认科目（资产/负债）是否相符的判定',
  '适用税率与表内多数口径或给定税率不一致的判定',
  '可抵扣亏损在结转期外或确认条件不满足仍确认资产的判定',
  '本期变动与利润表所得税费用的勾稽判定',
  '超额确认导致递延所得税资产虚增的判定（按金额排序的处理清单）',
];

const OUT_OF_SCOPE = [
  '判断未来期间是否有足够应纳税所得额（那是管理层判断与审计评估，本工具只做表内一致性）',
  '给出税务/审计意见，或判断某项差异是否真的属于暂时性差异（如永久性差异的识别）',
  '处理企业合并、权益法核算、境外子公司税率差异等特殊口径',
  '读取 .xlsx（需要你先导出成文本贴进来）',
];

// 干净样例（**带符号口径**：递延所得税资产为正、递延所得税负债为负）：
// 两种方向各两行、统一税率 5%、合计行逐列勾稽、无亏损行与利润表行
const SAMPLE_TEXT = [
  '项目\t方向\t账面价值\t计税基础\t暂时性差异\t适用税率\t期初余额\t期末余额\t本期变动',
  '固定资产（折旧年限差）递延所得税负债\t应纳税\t500000.00\t400000.00\t100000.00\t5%\t3500.00\t5000.00\t1500.00',
  '存货跌价准备递延所得税资产\t可抵扣\t200000.00\t240000.00\t-40000.00\t5%\t-3500.00\t-2000.00\t1500.00',
  '交易性金融资产（公允价值变动）递延所得税负债\t应纳税\t360000.00\t300000.00\t60000.00\t5%\t-2500.00\t-3000.00\t-500.00',
  '预计负债（产品质量保证）递延所得税资产\t可抵扣\t0.00\t20000.00\t-20000.00\t5%\t-500.00\t-1000.00\t-500.00',
  '合计\t\t1060000.00\t960000.00\t100000.00\t\t-3000.00\t-1000.00\t2000.00',
].join('\n');

const TOL = 0.02;              // 金额容差（表中金额保留两位小数，允许半分位舍入）
const RATE_TOL = 0.01;         // 税率容差（百分点）
const EXCESS_MIN = 0.05;       // 超额确认的最小金额门槛：低于此视为半分位舍入，不报
const DEFAULT_RATE = 25;       // 仅用于"表内给不出税率时"的说明文字，不用于任何复算

// ⚠️ 更具体的关键词必须排在更宽泛的前面（这是本仓库踩过两次的坑，见 tools/header_map_check.py）：
//    「期初余额」必须排在「余额」之前；「亏损可结转期末」必须排在「亏损」之前；
//    「本期变动」必须排在「变动」之前。
const ROLES = [
  ['roleDir', ['项目', '科目', '类别', '明细', '名称', '项目名称']],
  ['direction', ['方向', '差异性质', '差异方向', '性质']],
  ['book', ['账面价值', '账面金额', '会计口径金额']],
  ['taxBasis', ['计税基础', '税法口径金额']],
  ['diff', ['暂时性差异', '应纳税暂时性差异', '可抵扣暂时性差异', '差异额']],
  ['rate', ['适用税率', '所得税税率', '税率']],
  ['opening', ['期初余额', '期初递延', '年初余额']],
  ['closing', ['期末余额', '期末递延']],
  ['change', ['本期变动', '本期发生额', '本期增减']],
  ['lossExpiryPeriod', ['亏损可结转期末', '亏损结转期末', '结转到期期间', '可结转期末']],
  ['lossAmount', ['未弥补亏损', '可抵扣亏损', '亏损金额', '弥补亏损']],
];

const LABELS = {
  roleDir: '项目', direction: '方向', book: '账面价值', taxBasis: '计税基础', diff: '暂时性差异',
  rate: '适用税率', opening: '期初余额', closing: '期末余额', change: '本期变动',
  lossExpiryPeriod: '亏损可结转期末', lossAmount: '未弥补亏损',
};

// 逐行复算至少要有：项目、方向、账面价值、计税基础、暂时性差异、期初/期末/本期变动
const REQUIRED = ['roleDir', 'direction', 'book', 'taxBasis', 'diff', 'opening', 'closing', 'change'];
const FILL_ROLES = ['opening', 'closing', 'change'];
const SUM_ROLES = ['book', 'taxBasis', 'diff', 'opening', 'closing', 'change'];

// ⚠️ 只用完整科目名做判定：单写「资产」「负债」会把「交易性金融资产」这类
//    **承载差异的项目名**误判成递延所得税科目（实测踩过：`资产` 命中「负债」字样之外的行）。
const ASSET_WORDS = ['递延所得税资产', '递延资产'];
const LIABILITY_WORDS = ['递延所得税负债', '递延负债'];
const LOSS_WORDS = ['亏损', '结转'];
const EXPENSE_WORDS = ['所得税费用', '递延所得税费用', '费用'];
const TOTAL_RE = /^(合计|总计|小计|total)/i;

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
  const h = String(header).replace(/[\s（）()%％]/g, '');
  for (const [role, keys] of ROLES) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/[%％]$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;
const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `项目「${it.byRole.roleDir || '(未命名)'}」`;
// 内部排序用金额：每条结论都带（口径统一），排序完摘掉，不落到输出里
const gapOf = (x, y) => Math.abs(round2((x === null || x === undefined ? 0 : x) - (y === null || y === undefined ? 0 : y)));
const fmt = (n) => Number(n).toFixed(2);

function hasAny(it, words) {
  const s = String(it.byRole.roleDir || '');
  return words.some((w) => s.indexOf(w) >= 0);
}

const isLossItem = (it) => hasAny(it, LOSS_WORDS) || num(it, 'lossAmount') !== null
  || !isBlank(it.byRole.lossExpiryPeriod);
const isExpenseItem = (it) => !isLossItem(it) && hasAny(it, EXPENSE_WORDS);
const isBalanceItem = (it) => !isLossItem(it) && !isExpenseItem(it);

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (TOTAL_RE.test(first) || isBlank(row.byRole.roleDir)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

/* ===== 免费档：逐项复算与勾稽（免费包与完整档都执行） ===== */

function checkDiff(it) {
  const book = num(it, 'book');
  const base = num(it, 'taxBasis');
  const stated = num(it, 'diff');
  if (book === null || base === null || stated === null) return null;
  const expect = round2(book - base);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '暂时性差异与复算不符', line: it.line,
    message: `${who(it)}的暂时性差异是 ${fmt(stated)}，按 账面价值 ${fmt(book)} − 计税基础 ${fmt(base)} 应为 ${fmt(expect)}`
      + '（正数＝应纳税暂时性差异，负数＝可抵扣暂时性差异）。',
    advice: '差异方向由 账面价值 − 计税基础 的正负决定：资产账面高于计税基础＝应纳税，低于＝可抵扣。',
  };
}

function checkDeferredBalance(it) {
  const diff = num(it, 'diff');
  const rate = num(it, 'rate');
  const stated = num(it, 'closing');
  if (diff === null || rate === null || stated === null) return null;
  // 只核**金额大小**：余额用正数（按科目分区）或带符号（资产为正/负债为负）两种写法都放行，
  // 方向由「方向」列与科目名决定，不靠正负号 —— 否则同一张表两种排版会被误报。
  const expect = round2(Math.abs(diff) * rate / 100);
  if (Math.abs(expect - Math.abs(stated)) <= TOL) return null;
  return {
    level: 'P0', category: '递延所得税余额与复算不符', line: it.line,
    message: `${who(it)}的期末余额是 ${fmt(stated)}，按 暂时性差异 ${fmt(diff)} × 适用税率 ${rate}% 的金额应为 ${fmt(expect)}。`,
    advice: '递延所得税资产/负债余额＝暂时性差异×适用税率（只核金额，正负号按你表内的写法）；税率用错档会整行算错。',
  };
}

function checkChange(it) {
  const opening = num(it, 'opening');
  const closing = num(it, 'closing');
  const stated = num(it, 'change');
  if (opening === null || closing === null || stated === null) return null;
  const expect = round2(closing - opening);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期变动与复算不符', line: it.line,
    message: `${who(it)}的本期变动是 ${fmt(stated)}，按 期末余额 ${fmt(closing)} − 期初余额 ${fmt(opening)} 应为 ${fmt(expect)}。`,
    advice: '本期变动＝期末−期初；这一列是利润表「递延所得税费用」勾稽的入口。',
  };
}

function checkDirectionConsistency(it) {
  const raw = String(it.byRole.direction === undefined ? '' : it.byRole.direction).trim();
  const diff = num(it, 'diff');
  if (diff === null) return null;
  const statedDeductible = /可抵扣|可抵减/.test(raw);
  const statedTaxable = /应纳税|应税/.test(raw);
  if (!statedDeductible && !statedTaxable) return null;
  const expectDeductible = diff < 0;
  if (statedDeductible !== expectDeductible && Math.abs(diff) > TOL) {
    return {
      level: 'P0', category: '方向标记与差异正负号不一致', line: it.line,
      message: `${who(it)}标的"${raw}"，但 账面价值 − 计税基础 = ${fmt(diff)}，`
        + `按口径应属「${expectDeductible ? '可抵扣' : '应纳税'}暂时性差异」。`,
      advice: '方向搞反是最常见的一类错：可抵扣＝账面低于计税基础（负数），应纳税＝账面高于计税基础（正数）。',
    };
  }
  if (Math.abs(diff) <= TOL) {
    return {
      level: 'P2', category: '零差异行仍标了方向', line: it.line,
      message: `${who(it)}的暂时性差异是 ${fmt(diff)}（零差异），但仍标了"${raw}"。`,
      advice: '零差异不留方向标记，否则下游按方向汇总时会多算一笔。',
    };
  }
  return null;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${fmt(stated)}，各明细行相加是 ${fmt(sum)}，相差 ${fmt(stated - sum)}。`,
        advice: '要么明细行漏了项目，要么合计行没跟着更新。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.roleDir || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一项目按不同税率分行列示是正常的；若本表按项目列示，重复行会让递延余额一起翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这项差异就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
    // 有差异却没有税率：余额那一步就算不出来（本工具绝不用默认税率顶替，只报缺失）
    if (num(it, 'diff') !== null && num(it, 'rate') === null) {
      out.push({
        level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
        message: `${who(it)}有暂时性差异 ${fmt(num(it, 'diff'))}，但「适用税率」是空的或占位符`
          + `（${String(it.byRole.rate === undefined ? '' : it.byRole.rate).trim() || '空'}）。`,
        advice: '没有税率就算不出递延所得税余额；本工具不会套用默认税率替你算。',
        amount: Math.abs(num(it, 'diff')),
      });
    }
    // 亏损行的专属两列：要么整行给全，要么一个都不给 —— 半拉子数据算不出确认条件
    const hasExpiry = !isBlank(it.byRole.lossExpiryPeriod);
    const hasAmount = !isBlank(it.byRole.lossAmount);
    if (hasExpiry !== hasAmount) {
      out.push({
        level: 'P2', category: '亏损行信息不完整', line: it.line,
        message: `${who(it)}只填了「${hasAmount ? '未弥补亏损' : '亏损可结转期末'}」，另一列没填。`,
        advice: '亏损能否确认资产，要同时看可结转期末与未弥补亏损金额；只有一个算不出来。',
      });
    }
  }
  return out;
}

/* ===== 完整档（付费）追加：方向与确认判定 + 按金额排序的处理清单 ===== */

/** 表内所属期：优先取"当前期间/所属期"列，其次取最大的可结转期末（保守，宁可不报也不误报） */
function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的递延所得税台账（要能认出「项目」「方向」「账面价值」「计税基础」'
      + '「暂时性差异」「期初余额」「期末余额」「本期变动」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从台账或底稿导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个项目的明细行']);

  const givenRate = normNumber(payload && payload.rate);
  const givenPeriod = normNumber(payload && payload.period);
  t.items.forEach((it) => { it.__givenRate = givenRate; });

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkDiff(it); if (a) findings.push(a);
    const b = checkDeferredBalance(it); if (b) findings.push(b);
    const c = checkChange(it); if (c) findings.push(c);
    const d = checkDirectionConsistency(it); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  // 排序键：金额（涉及金额的取绝对值，缺的按 0）—— 同一口径，逐条补，避免各检查各算一套
  const magOf = (f) => {
    const it = t.items.concat(t.totals).find((x) => x.line === f.line) || null;
    const closing = it ? num(it, 'closing') : null;
    const diff = it ? num(it, 'diff') : null;
    if (/复算不符|与明细之和不符|不一致|超额确认|不勾稽|仍确认资产|科目不符/.test(f.category)) {
      if (closing !== null) return Math.abs(closing);
      if (diff !== null) return Math.abs(diff);
    }
    return typeof f.amount === 'number' ? Math.abs(f.amount) : 0;
  };
  // 处理清单排序：按金额从大到小，同金额再按行号
  findings.sort((x, y) => (magOf(y) - magOf(x)) || (x.line - y.line)
    || String(x.category).localeCompare(String(y.category)));
  for (const f of findings) delete f.amount;

  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const lossTotal = round2(t.items.filter(isLossItem).reduce((s, it) => {
    const n = num(it, 'lossAmount');
    return s + (n === null ? 0 : n);
  }, 0));
  const balanceChanges = round2(t.items.filter(isBalanceItem).reduce((s, it) => {
    const n = num(it, 'change');
    return s + (n === null ? 0 : n);
  }, 0));
  const rates = t.items.map((it) => num(it, 'rate')).filter((n) => n !== null);
  const ratesUsed = Array.from(new Set(rates.map(round2))).sort((a, b) => a - b);
  const missingFill = [];
  for (const it of t.items) {
    for (const role of FILL_ROLES) {
      if (!isBlank(it.byRole[role])) { missingFill.push({ line: it.line, role: LABELS[role] }); break; }
    }
  }

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      diff_total: sumOf('diff'),
      opening_total: sumOf('opening'),
      closing_total: sumOf('closing'),
      change_total: sumOf('change'),
      balance_change_total: balanceChanges,
      loss_total: lossTotal,
      rates_used: ratesUsed,
      basis: '暂时性差异 = 账面价值 − 计税基础（正数＝应纳税，负数＝可抵扣）；'
        + '递延所得税余额 = 暂时性差异 × 适用税率；本期变动 = 期末余额 − 期初余额；'
        + '合计行逐列复核；本期变动合计与利润表递延所得税费用勾稽。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    // ⚠️ checks_withheld 只在**真的没执行**时才出现：买断档全部跑了，
    //    留着它会让人以为还有 5 项没查（守卫实测踩过）。
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    scope: {
      rows: t.items.length,
      total_rows: t.totals.length,
      balance_rows: t.items.filter(isBalanceItem).length,
      loss_rows: t.items.filter(isLossItem).length,
      expense_rows: t.items.filter(isExpenseItem).length,
      checks_run: CHECKS_GIVEN.length,
      checks_not_run: CHECKS_WITHHELD.slice(),
      balance_change_total: balanceChanges,
      loss_total: lossTotal,
      closing_total: sumOf('closing'),
      default_rate_note: `表内未给出税率时不会套用 ${DEFAULT_RATE}% —— 缺税率就报"关键字段缺失"，绝不替填。`,
      sign_note: '余额只核金额大小，正负号按你表内的写法（资产为正/负债为负，或按科目分区都行）。',
      period_note: '亏损结转期比对的所属期 = 入参 period（给了就用）> 表内当前期间列 > 表内最大的可结转期末；'
        + '三者都取不到时，不作「已过结转期」的判定（宁可不报，也不误报）。',
    },
    missing_fill: missingFill,
  };
  result.checks_withheld = CHECKS_WITHHELD;
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、口径内部一致**，'
      + '不代表未来期间一定有足够应纳税所得额，也不代表差异分类（暂时性/永久性）一定正确 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
