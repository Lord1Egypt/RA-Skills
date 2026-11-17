/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * waybill-pod-cod-check.js —— 运单回单与代收货款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月与网点 / 承运商结算运费之前**。物流与快递企业每个月都要
 * 把三件事逐票勾稽一遍：
 *   ① 回单（POD，客户签收单）有没有回来 —— 回单没回来，按合同就结不了运费，
 *      先结了也可能事后被扣回去；
 *   ② 代收货款（COD，替发货方代收的钱）有没有回款 —— 这是**替别人收的钱**，
 *      账上对不上就是挪用资金的风险敞口；
 *   ③ 异常件（破损 / 丢失 / 延误）的赔付有没有从应结运费里正确扣掉。
 * 这张表算错，方向只有两个 —— **多结运费**（公司先垫钱）或 **少收 / 漏收代收货款**
 * （对客户说不清，对账永远平不了）。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应结运费   = 运费 + 附加费 − 赔付金额
 *   COD 未回款 = 代收货款金额 − 已回款金额
 *   合计行各列 = 明细行相加（回单回收天数**不做合计**：天数不可加总）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某票异常件该不该赔、该赔多少，也不判断回单上的签收人是否合规
 *    （那属于合同与业务判断）：表里的运单号、运费、附加费、赔付金额、代收货款金额、
 *    已回款金额、回单回收天数一律**以你填的为准**，本工具只核表内勾稽与档位提示，
 *    并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应结运费复算（运费 + 附加费 − 赔付金额 = 应结运费）',
  'COD 未回款复算（代收货款金额 − 已回款金额 = COD 未回款）',
  '合计行逐列复核',
  '同一运单号同一期间重复行检测',
  '空白与占位符检测',
  '金额或天数为负检测',
];

const CHECKS_WITHHELD = [
  '已回款金额超过代收货款提示',
  '回单回收天数超过参考上限（30 天）提示',
  'COD 未回款超过参考金额（5000 元）提示',
  '同一运单重复结算提示（跨期间同号各结一次运费）',
  '赔付金额超过运费提示',
];

const OUT_OF_SCOPE = [
  '判断某票异常件该不该赔、该赔多少（破损 / 丢失 / 延误的定责与赔付标准属于承运合同与业务判断）',
  '判断回单上的签收人是否合规（是否本人签收、代签是否有授权、回单是否真实，属于业务与法务判断）',
  '核对承运合同 / 网点结算协议本身（计价重量、抛比、最低一票、返点、月结账期）对运费的影响',
  '处理代收货款的资金监管、手续费收入、增值税与「代收代付」的会计科目认定（请咨询税务与会计师）',
  '读取 TMS / WMS / 快递系统 / 银行流水导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t运单号\t发货客户\t运费\t附加费\t赔付金额\t应结运费\t代收货款金额\t已回款金额\tCOD未回款\t回单回收天数',
  '2026-01\tYD2026010001\t豫州商贸有限公司\t1200.00\t180.00\t0.00\t1380.00\t8000.00\t8000.00\t0.00\t12',
  '2026-01\tYD2026010002\t中岳设备租赁有限公司\t860.00\t120.00\t0.00\t980.00\t0.00\t0.00\t0.00\t18',
  '2026-01\tYD2026010003\t豫通物流有限公司\t2400.00\t300.00\t200.00\t2500.00\t12000.00\t9000.00\t3000.00\t26',
  '2026-02\tYD2026020001\t豫州商贸有限公司\t1500.00\t150.00\t0.00\t1650.00\t6000.00\t6000.00\t0.00\t9',
  '2026-02\tYD2026020002\t中岳设备租赁有限公司\t980.00\t60.00\t80.00\t960.00\t3000.00\t1500.00\t1500.00\t22',
  '合计\t\t\t6940.00\t810.00\t280.00\t7470.00\t29000.00\t24500.00\t4500.00\t',
].join('\n');

const TOL = 0.01;
/** 回单回收天数的参考上限：超过它说明回单压得太久，运费先结了也很难收回 */
const POD_DAYS_LIMIT = 30;
/** COD 未回款的参考金额：超过它就该单独盯人盯单，不要混在月结里 */
const COD_OUTSTANDING_LIMIT = 5000;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    「应结运费」不能被「运费」抢走（所以 settleFreight 排在 freight 之前）；
  //    「COD未回款」不能被「已回款」抢走（codOutstanding 排在 codPaid 之前）；
  //    「代收货款金额」排在更宽泛的「代收」类别名之前、「回单回收天数」排在「天数」之前。
  period: ['所属期间', '会计期间', '结算期间', '所属期', '账期', '期间', '月份', '月度'],
  waybill: ['运单编号', '运单号码', '快递单号', '物流单号', '托运单号', '运单号', '单据编号', '单号'],
  customer: ['发货客户', '客户名称', '发货单位', '发货方', '托运方', '客户'],
  settleFreight: ['应结运费金额', '本期应结运费', '应结运费', '运费结算金额', '结算运费', '应结金额'],
  freight: ['基本运费', '干线运费', '运输费用', '运费金额', '运费', '运输费'],
  surcharge: ['燃油附加费', '其他附加费', '附加费用', '增值服务费', '附加费'],
  compensation: ['赔付金额', '赔偿金额', '理赔金额', '破损赔付', '赔付'],
  codAmount: ['代收货款金额', '代收货款', 'COD金额', '代收金额', '代收款金额'],
  codOutstanding: ['COD未回款', '未回款金额', '待回款金额', '未收货款', '未回款', '待回款'],
  codPaid: ['已回款金额', '已收货款', '回款金额', '已代收金额', '已回款', '回款'],
  podDays: ['回单回收天数', '回单回传天数', '回单逾期天数', '回单天数', '回收天数', '签收天数', '天数'],
};

const LABELS = {
  period: '所属期间', waybill: '运单号', customer: '发货客户', freight: '运费', surcharge: '附加费',
  compensation: '赔付金额', settleFreight: '应结运费', codAmount: '代收货款金额',
  codPaid: '已回款金额', codOutstanding: 'COD未回款', podDays: '回单回收天数',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'waybill', 'freight', 'surcharge', 'compensation', 'settleFreight',
  'codAmount', 'codPaid', 'codOutstanding', 'podDays'];

/**
 * 行内必须填值的列（空了 / 是占位符就报）。
 * ⚠️ 刻意**不含** podDays —— 「回单还没回来」时这一格**本来就该是空的**，
 *    空值是**有意义的信息**，不是漏填；把它算成缺失等于对着正常业务喊狼来了。
 *    （回单未回的风险由完整档的「回单回收天数超过参考上限」从另一侧盯。）
 */
const BLANK_ROLES = ['period', 'waybill', 'freight', 'surcharge', 'compensation', 'settleFreight',
  'codAmount', 'codPaid', 'codOutstanding'];

/** 合计行逐列复核的列（**不含** podDays：天数不可加总，填了平均天数也不算错） */
const SUM_ROLES = ['freight', 'surcharge', 'compensation', 'settleFreight', 'codAmount',
  'codPaid', 'codOutstanding'];

/**
 * 免费档负值检测覆盖的列：运费 / 附加费 / 赔付 / 代收货款 / 已回款 / 回单回收天数。
 * ⚠️ 刻意**不含**应结运费与 COD 未回款这两个"轧差列"：
 *    · 赔付超过运费时，应结运费**本来就该是负的**（这票倒赔）—— 那是完整档
 *      「赔付金额超过运费」的检查项；
 *    · 已回款超过代收货款时，COD 未回款**本来就是负的** —— 那是完整档
 *      「已回款金额超过代收货款」的检查项。
 *    免费档提前把这两列报成"金额为负"，等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['freight', 'surcharge', 'compensation', 'codAmount', 'codPaid', 'podDays'];

const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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
  const n = [it && it.waybill, it && it.customer]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkSettleRecompute(it) {
  const out = [];
  const freight = normNumber(it.freight);
  const surcharge = normNumber(it.surcharge);
  const comp = normNumber(it.compensation);
  const stated = normNumber(it.settleFreight);
  if (freight === null || surcharge === null || comp === null || stated === null) return out;
  const expect = round2(freight + surcharge - comp);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应结运费复算不符', line: it.line,
    message: `${who(it)}：运费 ${freight.toFixed(2)} + 附加费 ${surcharge.toFixed(2)} − 赔付金额 ${comp.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「应结运费」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '应结运费就是这张表最终要付给网点 / 承运商的钱，"运费 + 附加费 − 赔付"三格对不上，'
      + '多结了是公司先垫钱、事后很难追回，少结了网点下一期会来补账。',
  });
  return out;
}

function checkCodRecompute(it) {
  const out = [];
  const amount = normNumber(it.codAmount);
  const codPaidAmt = normNumber(it.codPaid);
  const stated = normNumber(it.codOutstanding);
  if (amount === null || codPaidAmt === null || stated === null) return out;
  const expect = round2(amount - codPaidAmt);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: 'COD未回款复算不符', line: it.line,
    message: `${who(it)}：代收货款金额 ${amount.toFixed(2)} − 已回款金额 ${codPaidAmt.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「COD未回款」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '代收货款是**替发货方收的钱**，未回款额就是还没交到发货方手上的那部分：'
      + '这一格填小了，等于把"钱还没回来"说成"已经回来了"。',
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
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月结账单与客户对账的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const w = it.waybill !== undefined ? String(it.waybill).trim() : '';
    if (!p || !w) continue;
    const key = `${p}|${w}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一运单号重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一运单号再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一票被拆成两行（比如运费与附加费各建一行没合并），'
          + '多出来的那一行会把运费、代收货款与回单天数都重复计一遍。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of BLANK_ROLES) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，无代收货款 / 无赔付的运单在这些金额列填 0，不要留空，'
            + '别让空值静默跳过检查。',
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
    const shown = role === 'podDays' ? `${v} 天` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或天数为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 运费、附加费、赔付、代收货款、已回款与回单回收天数都不该为负，`
        + '冲回 / 红字应单独列示并在备注里说明；天数填成负数多半是把"逾期天数"或日期差算反了。',
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
    return insufficient('没有收到运单回单与代收货款核对表正文（text）—— 请把「所属期间 / 运单号 / 发货客户 / 运费 / 附加费 / 赔付金额 / 应结运费 / 代收货款金额 / 已回款金额 / COD未回款 / 回单回收天数」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `运单回单与代收货款核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何运单明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkSettleRecompute(it));
    findings.push(...checkCodRecompute(it));
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

  let freightTotal = 0;
  let settleTotal = 0;
  let codPaidTotal = 0;
  let codOutstandingTotal = 0;
  for (const it of t.items) {
    const f = normNumber(it.freight);
    if (f !== null) freightTotal += f;
    const s = normNumber(it.settleFreight);
    if (s !== null) settleTotal += s;
    const p = normNumber(it.codPaid);
    if (p !== null) codPaidTotal += p;
    const o = normNumber(it.codOutstanding);
    if (o !== null) codOutstandingTotal += o;
  }

  const result = {
    status: 'success',
    service_type: 'WAYBILL_POD_COD_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      freight_total: round2(freightTotal),
      settle_total: round2(settleTotal),
      paid_in_total: round2(codPaidTotal),
      outstanding_total: round2(codOutstandingTotal),
      pod_days_limit: POD_DAYS_LIMIT,
      cod_outstanding_limit: COD_OUTSTANDING_LIMIT,
      tolerance: TOL,
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
    disclaimer: '只核"运费 + 附加费 − 赔付金额 = 应结运费"与"代收货款金额 − 已回款金额 = COD未回款"这类**表内勾稽**'
      + '与档位提示，**不判断某票异常件该不该赔、回单签收人是否合规**（以承运合同与业务口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
