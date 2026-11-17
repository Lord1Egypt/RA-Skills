/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * retail-member-points-check.js —— 会员积分与储值卡核销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**零售 / 连锁门店每月结账前**。会员积分与储值卡这张表，
 * 每个月都要把「积分发放 / 兑换 / 过期」与「储值卡充值 / 消费 / 退卡」逐笔勾稽一遍。
 * 这两样在账上都是**预收款（合同负债）**：
 *   · 储值卡余额多记 ⇒ 预收款虚增、收入少确认；少记 ⇒ 收入多确认、负债漏记；
 *   · 会员积分是"未来要兑出去的义务"，兑换时要按比例把预收款结转为收入。
 * 两边任何一个算错，都是**收入确认与负债双错**，而且门店小票、会员系统与总账三方永远对不平。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   储值卡期末余额 = 储值卡期初余额 + 本期充值 − 本期消费 − 本期退卡
 *   积分期末余额   = 积分期初余额 + 本期发放积分 − 本期兑换积分 − 本期过期积分
 *   合计行各列     = 明细行相加（比例列不加总）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**积分与储值余额该按什么口径确认收入、赠送额是否计入卡内余额、
 *    预付卡的税务与监管事项（那属于会计、税务与合规判断）：表里给的期初余额、充值、
 *    消费、退卡、发放、兑换、过期一律**以你填的为准**，本工具只核表内勾稽，
 *    并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，再把付费检查
 *    包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 strip_free_engine 会走形态 A，把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：strip_free_engine 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '储值卡期末余额滚动复算（期初 + 本期充值 − 本期消费 − 本期退卡 = 期末）',
  '积分期末余额滚动复算（期初 + 本期发放 − 本期兑换 − 本期过期 = 期末）',
  '合计行逐列复核',
  '同一会员同一期间重复行检测',
  '空白与占位符检测',
  '金额或积分为负检测',
];

const CHECKS_WITHHELD = [
  '消费金额超过储值卡余额提示',
  '兑换积分超过可用积分提示',
  '退卡金额超过剩余余额提示',
  '充值赠送比例与活动口径不一致提示',
  '积分兑换率偏离参考区间提示',
];

const OUT_OF_SCOPE = [
  '判断积分与储值卡余额该按什么口径确认收入（合同负债 / 预收账款、积分的单独售价分摊、充值赠送额是否计入卡内余额，属于会计判断，请咨询会计师）',
  '核对会员系统 / 收银系统 / ERP 导出的原始流水本身（本工具只核你贴进来的这张表，不回溯原始凭证）',
  '判断某项积分活动、充值赠送活动本身是否合规（广告、标价、单用途预付卡监管口径）',
  '处理预付卡 / 储值卡的增值税、开票、资金存管与备案等税务与监管事项',
  '跨期连续性核对（本期期初是否等于上期期末）：本工具只核**同一行内**的滚动公式与同一张表的合计勾稽',
  '读取会员系统 / 收银系统 / POS 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t门店\t会员卡号\t储值卡期初余额\t本期充值\t本期消费\t本期退卡\t储值卡期末余额\t积分期初余额\t本期发放积分\t本期兑换积分\t本期过期积分\t积分期末余额\t活动赠送比例\t本期赠送金额\t积分兑换金额',
  '2026-01\t中山路店\tM0001\t1000.00\t500.00\t300.00\t0.00\t1200.00\t2000\t500\t300\t0\t2200\t10.00%\t50.00\t3.00',
  '2026-01\t中山路店\tM0002\t0.00\t0.00\t0.00\t0.00\t0.00\t8000\t0\t4000\t0\t4000\t0.00%\t0.00\t40.00',
  '2026-02\t中山路店\tM0001\t1200.00\t0.00\t200.00\t0.00\t1000.00\t2200\t0\t100\t50\t2050\t10.00%\t0.00\t1.00',
  '2026-02\t中山路店\tM0002\t0.00\t0.00\t0.00\t0.00\t0.00\t4000\t1000\t0\t0\t5000\t0.00%\t0.00\t0.00',
  '2026-03\t人民路店\tM0003\t500.00\t2000.00\t300.00\t100.00\t2100.00\t0\t0\t0\t0\t0\t10.00%\t200.00\t0.00',
  '2026-03\t人民路店\tM0004\t300.00\t0.00\t100.00\t0.00\t200.00\t1000\t200\t500\t100\t600\t0.00%\t0.00\t5.00',
  '合计\t\t\t3000.00\t2500.00\t900.00\t100.00\t4500.00\t17200\t1700\t4900\t150\t13850\t\t250.00\t49.00',
].join('\n');

const TOL = 0.01;              // 金额容差 1 分、积分容差 1 分
const RATE_TOL = 0.005;        // 赠送比例容差：0.5 个百分点
const REDEEM_RATE_MIN = 0.005; // 积分兑换率参考区间下限：0.005 元/积分（100 积分 ≈ 0.5 元）
const REDEEM_RATE_MAX = 0.05;  // 上限：0.05 元/积分（100 积分 ≈ 5 元）

const ROLES = {
  // ⚠️ 顺序即优先级：① 更具体的别名在同组里排在前面（「储值卡期末余额」不能被同组的「期末余额」抢走）；
  //    ② **跨组**更要小心 —— 带裸「余额」兜底的储值两列必须排在积分两列**之后**，
  //    否则「积分期末余额」会被「期末余额」抢走。列被抢走不会报缺列，只会**静默算错**
  //    （第 232 轮 header_map_check 记过的坑），所以顺序是判据的一部分。
  period: ['所属期间', '会计期间', '所属期', '结算期间', '期间', '月份', '月度'],
  store: ['门店名称', '门店', '分店', '店铺', '网点', '柜组'],
  card: ['会员卡号', '储值卡号', '会员编号', '会员号', '会员ID', '卡号'],
  pointsBegin: ['积分期初余额', '期初积分余额', '上期积分期末余额', '积分期初', '积分期初结余'],
  pointsEnd: ['积分期末余额', '期末积分余额', '下期积分期初余额', '积分期末', '积分结余'],
  valueBegin: ['储值卡期初余额', '期初储值余额', '上期储值卡期末余额', '储值卡期初', '期初余额'],
  valueEnd: ['储值卡期末余额', '期末储值余额', '下期储值卡期初余额', '储值卡余额', '期末余额'],
  // ⚠️ 两个「赠送」列必须排在「充值」之前：否则「充值赠送金额」会被「充值」抢走
  bonusRate: ['活动赠送比例', '活动赠送率', '赠送比例', '赠送率'],
  bonusAmount: ['本期赠送金额', '充值赠送金额', '赠送金额', '赠送额'],
  recharge: ['本期充值金额', '本期充值', '储值卡充值', '充值金额', '充值'],
  consume: ['本期消费金额', '储值卡消费', '本期消费', '消费金额', '刷卡金额', '消费'],
  refund: ['本期退卡金额', '退卡金额', '本期退卡', '销卡退款', '退卡'],
  pointsIssued: ['本期发放积分', '本期积分发放', '发放积分', '新增积分'],
  pointsRedeemed: ['本期兑换积分', '本期核销积分', '兑换积分', '已兑积分', '核销积分'],
  pointsExpired: ['本期过期积分', '过期积分', '失效积分'],
  redeemAmount: ['积分兑换金额', '积分抵现金额', '兑换金额', '抵扣金额'],
};

const LABELS = {
  period: '所属期间', store: '门店', card: '会员卡号', valueBegin: '储值卡期初余额',
  recharge: '本期充值', consume: '本期消费', refund: '本期退卡', valueEnd: '储值卡期末余额',
  pointsBegin: '积分期初余额', pointsIssued: '本期发放积分', pointsRedeemed: '本期兑换积分',
  pointsExpired: '本期过期积分', pointsEnd: '积分期末余额', bonusRate: '活动赠送比例',
  bonusAmount: '本期赠送金额', redeemAmount: '积分兑换金额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'card', 'valueBegin', 'recharge', 'consume', 'refund', 'valueEnd',
  'pointsBegin', 'pointsIssued', 'pointsRedeemed', 'pointsExpired', 'pointsEnd'];
/** 合计行逐列复核的列（⚠️ 不含「活动赠送比例」—— 比例相加没有意义） */
const SUM_ROLES = ['valueBegin', 'recharge', 'consume', 'refund', 'valueEnd',
  'pointsBegin', 'pointsIssued', 'pointsRedeemed', 'pointsExpired', 'pointsEnd',
  'bonusAmount', 'redeemAmount'];
/**
 * 免费档负值检测覆盖的列：**收付两侧的金额与积分**。
 * ⚠️ 刻意**不含**「储值卡期末余额」「积分期末余额」—— "消费/兑换/退卡把余额冲成负数"
 *    是完整档的独立检查项（见 CHECKS_WITHHELD），免费档提前报出期末余额为负
 *    就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['valueBegin', 'recharge', 'consume', 'refund',
  'pointsBegin', 'pointsIssued', 'pointsRedeemed', 'pointsExpired',
  'bonusAmount', 'redeemAmount', 'bonusRate'];
/** 以「比例」形式填写的列（负值检测与不一致检测都要先归一化成小数） */
const RATE_ROLES = ['bonusRate'];
/** 以「积分」为单位的列（打印时按整数，不补两位小数） */
const POINTS_ROLES = ['pointsBegin', 'pointsIssued', 'pointsRedeemed', 'pointsExpired'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：|总计：)$/;

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

/** 比例归一化成小数：`10%` ⇒ 0.10；`0.1` ⇒ 0.10；`10` ⇒ 0.10 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
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
  const n = [it && it.store, it && it.card]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const cardKeyOf = (it) => {
  const c = it && it.card !== undefined ? String(it.card).trim() : '';
  return c || `第 ${it && it.line} 行`;
};

/** 按「金额 / 积分 / 比例」三种单位打印同一个数（message 里不能把比例印成 0.10） */
function shown(role, v) {
  if (RATE_ROLES.indexOf(role) >= 0) return `${(v * 100).toFixed(2)}%`;
  if (POINTS_ROLES.indexOf(role) >= 0) return Number.isInteger(v) ? String(v) : v.toFixed(2);
  return v.toFixed(2);
}

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkValueRolling(it) {
  const out = [];
  const begin = normNumber(it.valueBegin);
  const recharge = normNumber(it.recharge);
  const consume = normNumber(it.consume);
  const refund = normNumber(it.refund);
  const stated = normNumber(it.valueEnd);
  if (begin === null || recharge === null || consume === null || refund === null || stated === null) return out;
  const expect = round2(begin + recharge - consume - refund);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '储值卡期末余额滚动复算不符', line: it.line,
    message: `${who(it)}：储值卡期初余额 ${begin.toFixed(2)} + 本期充值 ${recharge.toFixed(2)} `
      + `− 本期消费 ${consume.toFixed(2)} − 本期退卡 ${refund.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「储值卡期末余额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '储值卡余额是**预收款**：滚动公式差一分，本期的收入确认与负债余额就同时错一分。',
  });
  return out;
}

function checkPointsRolling(it) {
  const out = [];
  const begin = normNumber(it.pointsBegin);
  const issued = normNumber(it.pointsIssued);
  const redeemed = normNumber(it.pointsRedeemed);
  const expired = normNumber(it.pointsExpired);
  const stated = normNumber(it.pointsEnd);
  if (begin === null || issued === null || redeemed === null || expired === null || stated === null) return out;
  const expect = round2(begin + issued - redeemed - expired);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '积分期末余额滚动复算不符', line: it.line,
    message: `${who(it)}：积分期初余额 ${begin} + 本期发放 ${issued} `
      + `− 本期兑换 ${redeemed} − 本期过期 ${expired} = ${expect}，`
      + `表里「积分期末余额」是 ${stated}，相差 ${round2(stated - expect)} 分。`
      + '积分是"未来要兑出去的义务"，发放多计会虚增费用与负债、兑换漏记会少结转收入，'
      + '过期没冲回则余额永远挂在那里对不平。',
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
      message: `合计行的「${LABELS[role]}」是 ${shown(role, stated)}，`
        + `本表 ${n} 行明细的「${LABELS[role]}」相加是 ${shown(role, expect)}，`
        + `相差 ${shown(role, round2(stated - expect))}。`
        + '合计行就是月报与门店对账的取数口径：这里对不上，说明明细漏了一行，或者合计行是手改过的。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const c = it.card !== undefined ? String(it.card).trim() : '';
    if (!p || !c) continue;
    const key = `${p}|${c}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一会员重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一会员卡号再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一张卡的储值流水与积分流水各建了一行却没合并。'
          + '多出来的那一行会把充值、消费、发放、兑换全部重复计一遍。',
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
            + '这一列缺失时对应的滚动复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const isRate = RATE_ROLES.indexOf(role) >= 0;
    const v = isRate ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额或积分为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown(role, v)}（负数）—— `
        + '充值、消费、退卡、发放、兑换、过期都不该为负；'
        + '红字冲回 / 退货应当单独列示并在备注里说明，直接填负数会让滚动公式两边一起跑偏。',
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
    return insufficient('没有收到会员积分与储值卡核销核对表正文（text）—— 请把「所属期间 / 门店 / 会员卡号 / 储值卡期初余额 / 本期充值 / 本期消费 / 本期退卡 / 储值卡期末余额 / 积分期初余额 / 本期发放积分 / 本期兑换积分 / 本期过期积分 / 积分期末余额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `会员积分与储值卡核销核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何会员明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkValueRolling(it));
    findings.push(...checkPointsRolling(it));
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

  let valueEndTotal = 0;
  let pointsRedeemedTotal = 0;
  let valueConsumedTotal = 0;
  for (const it of t.items) {
    const e = normNumber(it.valueEnd);
    if (e !== null) valueEndTotal += e;
    const r = normNumber(it.pointsRedeemed);
    if (r !== null) pointsRedeemedTotal += r;
    const c = normNumber(it.consume);
    if (c !== null) valueConsumedTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'RETAIL_MEMBER_POINTS_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      value_end_total: round2(valueEndTotal),
      value_consumed_total: round2(valueConsumedTotal),
      points_redeemed_total: round2(pointsRedeemedTotal),
      tolerance: TOL,
      redeem_rate_reference: [REDEEM_RATE_MIN, REDEEM_RATE_MAX],
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
    disclaimer: '只核"储值卡期初 + 充值 − 消费 − 退卡 = 期末"、"积分期初 + 发放 − 兑换 − 过期 = 期末"'
      + '与"合计行 = 明细之和"这类**表内勾稽**与档位提示，'
      + '**不判断积分与储值余额该按什么口径确认收入、赠送额是否计入卡内余额**（以你的会计口径与门店活动规则为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
