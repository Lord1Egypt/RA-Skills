/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * training-hour-consumption-check.js —— 教培课消与预收学费核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**教培 / 培训机构每月结账前**。学员这个月消耗了多少课时
 * （课消），就要把预收学费按相同的口径**结转**成收入；同时剩余课时要跟教务系统对得上，
 * 退费要逐笔算得清。这张表算错，方向只有两个 —— **收入确认错**（课消结转多了或少了，
 * 当月利润跟着错）或 **剩余课时 / 退费算不清**（家长一投诉就说不清还剩多少、该退多少）。
 * 预收学费还是监管重点：预收的钱不是收入，只有课消掉的那部分才能结转。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   课消金额     = 本期课消课时 × 课时单价
 *   剩余课时     = 期初课时 + 本期购买课时 − 本期课消课时 − 本期退费课时
 *   合计行各列   = 明细行相加
 *   已收学费     = 课消金额 + 退费金额 + 预收学费结转（收进来的钱只有这三个去处）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该按什么口径确认收入、赠送课时怎么折算、退费该按什么价退
 *    （那属于合同与会计判断）：表里给的课时单价、合同课时单价一律**以你填的为准**，
 *    本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '课消金额复算（本期课消课时 × 课时单价 = 课消金额）',
  '剩余课时滚动复算（期初课时 + 本期购买课时 − 本期课消课时 − 本期退费课时 = 剩余课时）',
  '合计行逐列复核',
  '同一学员同一期间重复行检测',
  '空白与占位符检测',
  '金额或课时为负检测',
];

const CHECKS_WITHHELD = [
  '课消课时超过可用课时提示',
  '剩余课时为负提示',
  '退费金额超过已收学费提示',
  '课时单价与合同不一致提示（同一学员同一课程跨期间单价突变，多为调价 / 优惠 / 含赠品折算）',
  '同一学员同一期间重复课消提示',
];

const OUT_OF_SCOPE = [
  '判断该按什么口径确认课消收入（一次性确认还是按期分摊、赠送课时怎么折算、跨期报名怎么切分，属于合同与会计判断，请咨询会计师）',
  '核对培训合同条款本身（赠送课时、请假与停课、转班转课、退费规则）对课消与结转的影响',
  '判断退费该按原价还是折后价计算（那是合同与机构制度的判断）',
  '处理预收学费的资金监管、发票、增值税与退费手续费等财税处理',
  '读取教务系统 / 收银系统 / Excel 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t学员编号\t学员姓名\t课程名称\t期初课时\t本期购买课时\t本期课消课时\t本期退费课时\t剩余课时\t课时单价\t课消金额\t已收学费\t退费金额\t预收学费结转',
  '2026-01\tS001\t甲同学\t数学一对一提分\t20\t10\t8\t0\t22\t200.00\t1600.00\t4000.00\t0.00\t2400.00',
  '2026-01\tS002\t乙同学\t英语精品小班\t40\t0\t30\t0\t10\t150.00\t4500.00\t6000.00\t0.00\t1500.00',
  '2026-01\tS003\t丙同学\t数学一对一提分\t10\t0\t4\t0\t6\t200.00\t800.00\t1800.00\t0.00\t1000.00',
  '2026-02\tS002\t乙同学\t英语精品小班\t10\t20\t20\t0\t10\t150.00\t3000.00\t6000.00\t0.00\t3000.00',
  '2026-02\tS004\t丁同学\t物理实验班\t0\t5\t1\t3\t1\t100.00\t100.00\t500.00\t0.00\t400.00',
  '合计\t\t\t\t80\t35\t63\t3\t49\t\t10000.00\t18300.00\t0.00\t8300.00',
].join('\n');
const TOL = 0.01;
const PRICE_TOL = 0.005;      // 课时单价容差：差半分钱以内不算不一致

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（「剩余课时」不能被「课时单价」抢走、
  //    「课消金额」「退费金额」不能被泛化的「金额」抢走、「已收学费」不能被「学费」抢走）
  period: ['所属期间', '所属月份', '会计期间', '所属期', '月份', '期间'],
  code: ['学员编号', '学员号', '学号', '会员号', '学员ID'],
  name: ['学员姓名', '学员', '学生', '会员', '姓名'],
  course: ['课程名称', '课程', '班级', '班型', '科目'],
  hourBegin: ['期初课时', '上期期末课时', '期初剩余课时', '起初课时', '期初课次', '上期结余课时'],
  hourBuy: ['本期购买课时', '本期购课课时', '本期新增课时', '购买课时', '新增课时', '本期购买课次', '续费课时'],
  hourUse: ['本期课消课时', '课消课时', '已消课时', '本期消课课时', '消课课时', '已耗课时', '课消课次'],
  hourRefund: ['本期退费课时', '退费课时', '退课课时', '冲回课时'],
  hourLeft: ['剩余课时', '期末剩余课时', '结余课时', '剩余课次', '课时余额'],
  price: ['课时单价', '课次单价', '课时收费标准', '课时费', '单价'],
  amount: ['课消金额', '消课金额', '课消费', '耗课金额', '已耗课费', '确认课消收入', '课时消耗金额'],
  paid: ['已收学费', '实收学费', '已缴学费', '预收合计', '收费金额', '学费收入'],
  refundAmount: ['退费金额', '退费额', '已退金额', '退款金额', '退费合计'],
  deferredRevenue: ['预收学费结转', '预收结转', '预收学费余额', '待结转学费', '未确认收入'],
};

const LABELS = {
  period: '所属期间', code: '学员编号', name: '学员姓名', course: '课程名称',
  hourBegin: '期初课时', hourBuy: '本期购买课时', hourUse: '本期课消课时',
  hourRefund: '本期退费课时', hourLeft: '剩余课时', price: '课时单价',
  amount: '课消金额', paid: '已收学费',
  refundAmount: '退费金额', deferredRevenue: '预收学费结转',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'code', 'name', 'hourBegin', 'hourBuy', 'hourUse', 'hourRefund',
  'hourLeft', 'price', 'amount', 'paid', 'refundAmount', 'deferredRevenue'];
/** 合计行逐列复核的列（单价列本来就不该有合计，课消金额与已收学费是钱、课时是量） */
const SUM_ROLES = ['hourBegin', 'hourBuy', 'hourUse', 'hourRefund', 'hourLeft',
  'amount', 'paid', 'refundAmount', 'deferredRevenue'];
/** 这几列是**课时**（量），用于负值与合计的口径区分 */
const HOUR_ROLES = ['hourBegin', 'hourBuy', 'hourUse', 'hourRefund', 'hourLeft'];
/**
 * 免费档负值检测覆盖的列：课时与金额。
 * ⚠️ 刻意**不含**剩余课时 —— "剩余课时为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出它就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['hourBegin', 'hourBuy', 'hourUse', 'hourRefund',
  'amount', 'paid', 'refundAmount', 'deferredRevenue', 'price'];
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

/** 行内"是谁"：期间 + 学员（编号 / 姓名）+ 课程，用于每条结论的定位 */
const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const s = [it && it.code, it && it.name]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' ');
  const c = it && it.course !== undefined ? String(it.course).trim() : '';
  const tail = [s, c].filter(Boolean).join(' / ');
  return tail ? `${p}「${tail}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/** 同一学员的定位键：优先学员编号，其次编号+姓名，最后退化成行号 */
const studentKeyOf = (it) => {
  const c = it && it.code !== undefined ? String(it.code).trim() : '';
  const n = it && it.name !== undefined ? String(it.name).trim() : '';
  const k = [c, n].filter(Boolean).join('|');
  return k || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkConsumptionRecompute(it) {
  const out = [];
  const hours = normNumber(it.hourUse);
  const price = normNumber(it.price);
  const stated = normNumber(it.amount);
  if (hours === null || price === null || stated === null) return out;
  const expect = round2(hours * price);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '课消金额复算不符', line: it.line,
    message: `${who(it)}：本期课消课时 ${hours} × 课时单价 ${price.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「课消金额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '课消金额就是当期要结转确认的收入：算少了收入少确认，算多了当月利润虚高，'
      + '而且预收学费结转会跟着一起错。',
  });
  return out;
}

function checkHourRolling(it) {
  const out = [];
  const begin = normNumber(it.hourBegin);
  const buy = normNumber(it.hourBuy);
  const use = normNumber(it.hourUse);
  const refund = normNumber(it.hourRefund);
  const stated = normNumber(it.hourLeft);
  if (begin === null || buy === null || use === null || refund === null || stated === null) return out;
  const expect = round2(begin + buy - use - refund);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '剩余课时滚动复算不符', line: it.line,
    message: `${who(it)}：期初课时 ${begin} + 本期购买课时 ${buy} − 本期课消课时 ${use} `
      + `− 本期退费课时 ${refund} = ${expect}，表里「剩余课时」是 ${stated}，相差 ${round2(stated - expect)} 课时。`
      + '剩余课时是家长随时会问的那个数：滚不动就是有课时不翼而飞或多出来，'
      + '后面每一次续费报价与退费计算都会跟着错。',
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
    const unit = HOUR_ROLES.indexOf(role) >= 0 ? ' 课时' : '';
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}${unit}，`
        + `本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}${unit}，`
        + `相差 ${round2(stated - expect).toFixed(2)}${unit}。`
        + '合计行就是月报与教务系统对账、以及预收学费结转的取数口径，对不上说明有一边错。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const c = it.code !== undefined ? String(it.code).trim() : '';
    const n = it.name !== undefined ? String(it.name).trim() : '';
    if (!p || (!c && !n)) continue;
    // ⚠️ 判据必须与完整档的「重复课消」**严格分开**，否则同一行会同时报两条：
    //    这里只认**整行逐格相同**（含课程与金额）—— 典型的"整行粘了两遍"；
    //    同一学员同一期间、同一课程、但课时或金额不同的重复，归完整档的「重复课消」。
    const vals = REQUIRED.map((r2) => String(it[r2] === undefined ? '' : it[r2]).trim()).join('\u0001');
    const key = `${p}|${studentKeyOf(it)}|${vals}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一学员重复行', line: it.line,
        message: `${who(it)}与第 ${seen.get(key)} 行**逐格完全相同** —— `
          + '这通常是从教务系统导出后整行粘了两遍：多出来的那一行会把课时与课消金额都重复计一遍，'
          + '收入被重复确认、剩余课时被多扣一次。先确认是不是同一笔课消，是就删掉一行。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
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
      level: 'P0', category: '金额或课时为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— `
        + '课时与金额都不该为负，冲回 / 红字应单独列示并在备注里说明；'
        + '负的课消金额会让当期收入被倒冲，负的购买课时会让剩余课时凭空少掉。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 同一学员同一课程跨期间分组：单价一致性的比对范围 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到教培课消与预收学费核对表正文（text）—— 请把「所属期间 / 学员编号 / 学员姓名 / 课程名称 / 期初课时 / 本期购买课时 / 本期课消课时 / 本期退费课时 / 剩余课时 / 课时单价 / 合同课时单价 / 课消金额 / 已收学费 / 退费金额 / 预收学费结转」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `教培课消与预收学费核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何学员课消明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkConsumptionRecompute(it));
    findings.push(...checkHourRolling(it));
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

  let amountTotal = 0;
  let hourUseTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.amount);
    if (a !== null) amountTotal += a;
    const u = normNumber(it.hourUse);
    if (u !== null) hourUseTotal += u;
  }

  const result = {
    status: 'success',
    service_type: 'TRAINING_HOUR_CONSUMPTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      amount_total: round2(amountTotal),
      hour_used_total: round2(hourUseTotal),
      tolerance: TOL,
      price_tolerance: PRICE_TOL,
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
    disclaimer: '只核"课消课时 × 课时单价 = 课消金额"与"期初课时 + 本期购买课时 − 本期课消课时 − 本期退费课时 = 剩余课时"'
      + '这类**表内勾稽**与档位提示，**不判断该按什么口径确认课消收入、赠送课时怎么折算、退费该按什么价退**'
      + '（以培训合同与会计师口径为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
