/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * saas-revenue-recognition-check.js —— SaaS订阅收入确认核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结账前**。SaaS / 软件服务业的订阅合同在签约收款时
 * 还不能确认收入 —— 钱先挂**合同负债（递延收益）**，再按**履约进度**逐期确认：
 *
 *   本期应确认收入 = 合同金额 ÷ 分摊期数（直线法，按服务期分摊）
 *   期末递延余额   = 期初递延余额 + 本期收款 − 本期确认收入
 *
 * 这两条是**滚动勾稽**：确认多了，收入虚增、合同负债虚减；确认少了则相反，
 * 月报与审计抽样都会被打回。而这张表的每一格都能手算复现，所以"对不对"完全可以机械核出来。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   本期确认收入 = 合同金额 ÷ 分摊期数
 *   期末递延余额 = 期初递延余额 + 本期收款 − 本期确认收入
 *   合计行各列   = 明细行相加（合同金额按合同去重，同一合同的多期明细只算一次）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某笔订阅到底该在哪个时点确认、按什么口径分摊（那属于会计判断）：
 *    表里给的合同金额、分摊期数、服务起止日期一律**以你填的为准**，本工具只核表内勾稽。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（本次实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应确认收入复算（合同金额 ÷ 分摊期数 = 本期确认收入）',
  '期末递延余额滚动复算（期初递延 + 本期收款 − 本期确认 = 期末递延）',
  '合计行逐列复核',
  '同一客户同一期间重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '确认金额超过合同期内可确认总额提示',
  '递延余额为负检测',
  '分摊期数与服务起止日期不一致提示（跨期错配）',
  '确认比例与履约进度偏离参考区间（0~100%）提示',
  '同一合同重复建行（合同号重复但客户不同）提示',
];

const OUT_OF_SCOPE = [
  '判断某笔订阅收入到底该在哪个时点、按什么口径确认（履约进度法还是完工百分比等，属于会计判断，请咨询会计师）',
  '核对合同条款本身（自动续费、阶梯价、赠送期、不可退款条款）对分摊口径的影响',
  '处理含税/不含税、外币折算、重大融资成分与合同变更（改期、加购、退订）的重新分摊',
  '读取 ERP / CRM 或财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t客户名称\t合同号\t合同金额\t服务开始\t服务结束\t分摊期数\t期初递延余额\t本期收款\t本期确认收入\t期末递延余额\t确认比例\t履约进度',
  '2026-01\t云启科技\tHT-2026-001\t120000.00\t2026-01-01\t2026-12-31\t12\t0.00\t120000.00\t10000.00\t110000.00\t8.33%\t8.33%',
  '2026-02\t云启科技\tHT-2026-001\t120000.00\t2026-01-01\t2026-12-31\t12\t110000.00\t0.00\t10000.00\t100000.00\t16.67%\t16.67%',
  '2026-01\t星野数据\tHT-2026-002\t60000.00\t2026-01-01\t2026-06-30\t6\t0.00\t60000.00\t10000.00\t50000.00\t16.67%\t16.67%',
  '2026-02\t星野数据\tHT-2026-002\t60000.00\t2026-01-01\t2026-06-30\t6\t50000.00\t0.00\t10000.00\t40000.00\t33.33%\t33.33%',
  '合计\t\t\t180000.00\t\t\t\t160000.00\t180000.00\t40000.00\t300000.00\t\t',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;                    // 比例容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「合同金额」不能被「合同」抢走、「本期确认收入」不能被「本期收款」抢走）
  period: ['会计期间', '所属期间', '所属期', '期间', '月份', '月度'],
  client: ['客户名称', '客户简称', '订阅客户', '客户'],
  contract: ['合同编号', '合同号', '合同编码', '合同ID', '合同id', '订购单号', '订单号'],
  contractAmount: ['合同金额', '合同总额', '合同含税金额', '订阅金额', '合同价款', '合同价'],
  startDate: ['服务开始日期', '服务开始时间', '服务开始', '开始日期', '服务起始日', '服务起始'],
  endDate: ['服务结束日期', '服务结束时间', '服务结束', '结束日期', '服务到期日', '服务止'],
  months: ['分摊期数', '摊销期数', '服务期数', '分摊月数', '月数', '期数'],
  deferredBegin: ['期初递延余额', '期初递延', '期初未确认', '期初余额'],
  cashIn: ['本期收款', '本期回款', '本期收款额', '收款金额', '回款金额', '收款额'],
  revenue: ['本期确认收入', '当期确认收入', '本期确认', '确认收入', '收入确认额', '确认金额'],
  deferredEnd: ['期末递延余额', '期末递延', '期末未确认', '期末余额'],
  ratio: ['确认比例', '收入确认比例', '确认率', '比例'],
  progress: ['履约进度', '完工进度', '履约百分比', '进度'],
};

const LABELS = {
  period: '期间', client: '客户名称', contract: '合同号', contractAmount: '合同金额',
  startDate: '服务开始', endDate: '服务结束', months: '分摊期数',
  deferredBegin: '期初递延余额', cashIn: '本期收款', revenue: '本期确认收入',
  deferredEnd: '期末递延余额', ratio: '确认比例', progress: '履约进度',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'client', 'contract', 'contractAmount', 'startDate', 'endDate',
  'months', 'deferredBegin', 'cashIn', 'revenue', 'deferredEnd'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['contractAmount', 'deferredBegin', 'cashIn', 'revenue', 'deferredEnd'];
/** 这几列是**按合同**的口径（同一合同的多期明细里，合同金额只算一次，否则会被重复加总） */
const PER_CONTRACT_ROLES = ['contractAmount'];
/**
 * 免费档负值检测覆盖的列：**收入侧**的金额与比例。
 * ⚠️ 刻意**不含**期初/期末递延余额 —— "递延余额为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出来就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['contractAmount', 'cashIn', 'revenue', 'ratio', 'progress'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

/** 比率归一化成小数：`8.33%` ⇒ 0.0833；`0.0833` ⇒ 0.0833；`8.33` ⇒ 0.0833 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

/** 日期归一化：支持 `2026-01-01` / `2026/1/1` / `2026年1月1日` / `20260101` */
/** 含头含尾的月份跨度：2026-01-01 ~ 2026-12-31 ⇒ 12 期 */
const round2 = (n) => Math.round(n * 100) / 100;

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
  const n = [it && it.client, it && it.contract]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const contractKeyOf = (it) => {
  const c = it && it.contract !== undefined ? String(it.contract).trim() : '';
  return c || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkRevenueRecompute(it) {
  const out = [];
  const amount = normNumber(it.contractAmount);
  const months = normNumber(it.months);
  const stated = normNumber(it.revenue);
  if (amount === null || months === null || stated === null) return out;
  if (months <= 0) return out;                 // 分摊期数填 0 或负：算不出每期分摊额（负值由负值检测报）
  const expect = round2(amount / months);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '本期确认收入与分摊复算不符', line: it.line,
    message: `${who(it)}：合同金额 ${amount.toFixed(2)} ÷ 分摊期数 ${months} = ${expect.toFixed(2)}，`
      + `表里「本期确认收入」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '订阅收入按服务期直线分摊，每期确认额就是合同金额 ÷ 分摊期数。',
  });
  return out;
}

function checkDeferredRolling(it) {
  const out = [];
  const begin = normNumber(it.deferredBegin);
  const cash = normNumber(it.cashIn);
  const revenue = normNumber(it.revenue);
  const stated = normNumber(it.deferredEnd);
  if (begin === null || cash === null || revenue === null || stated === null) return out;
  const expect = round2(begin + cash - revenue);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末递延余额滚动不符', line: it.line,
    message: `${who(it)}：期初递延余额 ${begin.toFixed(2)} + 本期收款 ${cash.toFixed(2)} − 本期确认收入 ${revenue.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末递延余额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '递延余额就是合同负债的滚动结果，滚不动后面每一期都会连锁错。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let expect = null;
    let how = '';
    if (PER_CONTRACT_ROLES.indexOf(role) >= 0) {
      const first = new Map();
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null && !first.has(contractKeyOf(it))) first.set(contractKeyOf(it), v);
      }
      if (!first.size) continue;
      expect = round2(Array.from(first.values()).reduce((a, b) => a + b, 0));
      how = `按合同去重后 ${first.size} 份合同的「${LABELS[role]}」相加`;
    } else {
      let sum = 0;
      let n = 0;
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null) { sum += v; n += 1; }
      }
      if (!n) continue;
      expect = round2(sum);
      how = `本表 ${n} 行明细的「${LABELS[role]}」相加`;
    }
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${how}是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const c = it.client !== undefined ? String(it.client).trim() : '';
    if (!p || !c) continue;
    const key = `${p}|${c}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一客户同一期间出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一合同被拆成两行，多出来的那一行会把收入与递延都重复计一遍。',
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
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'ratio' || role === 'progress' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'ratio' || role === 'progress' ? `${(v * 100).toFixed(3)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 合同金额、收款与本期确认收入都不该为负，`
        + '退款/冲回应单独列示并在备注里说明。',
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
    return insufficient('没有收到SaaS订阅收入确认表正文（text）—— 请把「期间 / 客户名称 / 合同号 / 合同金额 / 服务开始 / 服务结束 / 分摊期数 / 期初递延余额 / 本期收款 / 本期确认收入 / 期末递延余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `SaaS订阅收入确认表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何客户明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkRevenueRecompute(it));
    findings.push(...checkDeferredRolling(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let revenueTotal = 0;
  for (const it of t.items) {
    const v = normNumber(it.revenue);
    if (v !== null) revenueTotal += v;
  }

  const result = {
    status: 'success',
    service_type: 'SAAS_REVENUE_RECOGNITION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      revenue_recognized_total: round2(revenueTotal),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
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
    disclaimer: '只核"合同金额 ÷ 分摊期数 = 本期确认收入"与"期初递延 + 本期收款 − 本期确认 = 期末递延"这类**表内勾稽**与档位提示，'
      + '**不判断某笔订阅该在哪个时点确认**（以会计准则与会计师口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
