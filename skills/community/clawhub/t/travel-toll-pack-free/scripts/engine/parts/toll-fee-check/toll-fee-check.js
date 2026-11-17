/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * toll-fee-check.js —— 通行费与过路过桥核对（免费档子集）
 *
 * ## 为什么会有这个文件（根因，别删这段）
 *
 * 本技能包的第 ② 项一直写着"通行费与过路过桥核对"，但此前它被接到了 `toll-processing-manual-check`
 * —— 那是一个**只因为 slug 里同样含 "toll" 就被误选**、业务上完全不相干的工具（海关手册类核对：
 * 手册备案耗用、余料结转、内销补税）。于是买家装到的"通行费核对"实际在核海关手册的结余与耗用：
 * 表头不一样、业务不一样、结论指向的东西也不一样。ClawHub 的 LLM 安全审查逐包点名过这一类错配。
 * 所以本文件**不从任何别的包拷贝规则**，按通行费自己的单据重写：
 * 一张"通行明细表" + 一张随表附来的"车辆台账"。
 *
 * ## 谁在什么时候必须做这件事
 *
 * **有车队的公司每月报销通行费 / 过路过桥费时**，费用会计要把这张明细表逐行核一遍。
 * 每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *     折扣后金额 = 票面金额 − 折扣金额
 *     实付金额   = 折扣后金额                    （三者必须一致，差一分都要报）
 *     合计行各列 = 明细行逐列相加
 *     重复入账   = 同一车牌 + 同一通行时间 + 同一实付金额 出现两次
 *     非公司车辆 = 车牌**不在**随表附来的车辆台账里
 *
 * ## 契约
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD —— 那 5 项本文件**没有实现**，
 * 只是如实列在结果里）。材料不足时**绝不给结论**：缺列、缺车辆台账都不猜、不套默认值。
 *
 * ⚠️ 本工具**不判断**哪些通行费该不该报、能不能税前扣除，也不判断折扣幅度是否合理
 *    （那属于公司制度、税务与 ETC 协议口径）：表里的票面/折扣/实付一律**以你填的为准**。
 */

const CHECKS_GIVEN = [
  '通行费金额三方勾稽（票面金额 − 折扣金额 = 折扣后金额 = 实付金额）',
  '重复通行检测（同一车牌 + 同一通行时间 + 同一实付金额）',
  '跨期检测（通行时间不在本次报销所属期间内）',
  '车辆归属核对（车牌比对车辆台账，非公司车辆单独报出）',
  '合计行逐列复核（各金额列合计 = 明细行相加）',
  '空白与占位符检测（所属期间 / 通行时间 / 车牌号 / 实付金额为空白、占位符或认不出格式）',
];

const CHECKS_WITHHELD = [
  '金额为负检测（票面 / 折扣 / 折扣后 / 实付出现负数，冲回与退款没单独列示）',
  '同一票据号重复使用检测（同一票据号出现在多行）',
  '折扣列漏填检测（票面金额 ≠ 折扣后金额，但折扣金额为空或为 0）',
  '车牌号格式异常检测（不符合车牌号格式，疑似录入错位）',
  '车辆归属与车辆台账不一致检测（行内填的车辆归属 ≠ 台账登记口径）',
];

const OUT_OF_SCOPE = [
  '判断某笔通行费该不该报、能不能税前扣除（属于**公司制度与税务判断**，请按制度与主管口径执行）',
  '核对通行费电子票据 / ETC 流水的真伪（本工具只核你贴进来的这张表）',
  '判断折扣幅度、优惠比例本身是否合理（以发行方与 ETC 协议为准）',
  '判断非公司车辆的通行费该由谁承担（本工具只报出"车牌不在台账里"这个事实）',
  '读取 ETC 平台 / 报销系统的导出文件（需要你先导出成文本贴进来）',
];

/* 样例 = 干净稿（生成时逐项自证过 0 条发现）：4 笔通行 + 2 辆公司车的台账。
   ⚠️ 第二张表用 `--- 车辆台账 ---` 起头，**不要**写成 `=== 车辆台账 ===` ——
      本包的段路由按 `=== 标题 ===` 切材料，段里再出现标题会把后面的行错切给别的检查项。 */
const SAMPLE_TEXT = [
  '所属期间\t通行时间\t车牌号\t票据号\t票面金额\t折扣金额\t折扣后金额\t实付金额\t车辆归属',
  '2026-04\t2026-04-03 09:12\t京A12345\tTP20260403001\t120.00\t6.00\t114.00\t114.00\t公司自有',
  '2026-04\t2026-04-08 18:40\t京A12345\tTP20260408002\t85.00\t0.00\t85.00\t85.00\t公司自有',
  '2026-04\t2026-04-15 07:05\t京A67890\tTP20260415003\t240.00\t12.00\t228.00\t228.00\t公司自有',
  '2026-04\t2026-04-21 20:30\t京A67890\tTP20260421004\t60.00\t3.00\t57.00\t57.00\t公司自有',
  '合计\t\t\t\t505.00\t21.00\t484.00\t484.00\t',
  '--- 车辆台账（公司车辆）---',
  '车牌号\t车辆归属\t使用部门',
  '京A12345\t公司自有\t销售一部',
  '京A67890\t公司自有\t工程二部',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的别名必须排在更宽泛的别名前面**。
  //    这里有两个真坑（任一踩到都不会报错，只会**静默算错**）：
  //      · 「折扣后金额」里含「折扣」二字 —— 若 discount（折扣金额）排在 net（折扣后金额）前面，
  //        它会把「折扣后金额」整列抢走，net 读到的是票面值，三方勾稽**永远成立**（假通过）；
  //      · 「车辆归属」里含「车辆」二字 —— plate 的别名里**绝不能**放裸的「车辆」或裸的「号」。
  period: ['报销所属期间', '所属期间', '报销期间', '所属期', '期间', '月份'],
  date: ['通行日期时间', '通行时间', '通行日期', '过路时间', '交易时间'],
  plate: ['车牌号', '车牌', '车号', '号牌'],
  ticket: ['票据号', '发票号', '票号', '单据号', '通行流水号'],
  net: ['折扣后金额', '折后金额', '优惠后金额', '折扣后'],
  discount: ['折扣金额', '优惠金额', '折扣额', '折扣'],
  face: ['票面金额', '票面额', '票面'],
  paid: ['实付金额', '实际支付金额', '实付'],
  owner: ['车辆归属', '车辆性质', '车辆所属'],
};

const LABELS = {
  period: '所属期间', date: '通行时间', plate: '车牌号', ticket: '票据号',
  face: '票面金额', discount: '折扣金额', net: '折扣后金额', paid: '实付金额',
  owner: '车辆归属',
};

/* 必需列：缺任何一列都不出结论（认不出表头就不猜）。
   ⚠️ 车辆的归属**不能**由明细表的「车辆归属」列自证 —— 那一列是报销人手填的，
      真正判"是不是公司车"的依据只能是随表附来的车辆台账（见 ROSTER_MARK）。 */
const REQUIRED = ['period', 'date', 'plate', 'face', 'discount', 'net', 'paid'];
/* 可加总的列（金额列才是合计行的核对对象） */
const SUM_ROLES = ['face', 'discount', 'net', 'paid'];
/* 空白检测只看这几列：它们是其它每一项的前提 */
const KEY_ROLES = ['period', 'date', 'plate', 'paid'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计)$/;
/* 车辆台账的子表标题：允许 `--- 车辆台账 ---` / `车辆台账` / `--- 公司车辆台账（自有车）---` 等写法 */
const ROSTER_MARK = /^\s*(?:-{2,}\s*)?(?:公司|自有)?车辆(?:台账|清单|明细表|明细)\s*(?:[（(][^）)]*[）)])?\s*(?:-{2,})?\s*$/;
const DATE_RE = /^(\d{4})[-/.年](\d{1,2})(?:[-/.月](\d{1,2})日?)?(?:[ T](\d{1,2}):(\d{2}))?/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（认不出表头、缺车辆台账都不出结论）。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待核实)$/i.test(s);
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
  const s = String(raw).trim()
    .replace(/[,，\s¥￥$]/g, '')
    .replace(/(元|次|笔)$/, '')
    .replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;
const pad2 = (n) => (n < 10 ? `0${n}` : String(n));
const dayMs = (o) => Date.UTC(o.y, o.mo - 1, o.d);

/** 通行时间归一化：认 `2026-04-03 09:12` / `2026/4/3 9:12` / `2026.4.3` / `2026年4月3日 9:12`。
 *  返回 {y,mo,d,hh,mi,text,hasTime}；**认不出来返回 null**（认不出来就报"无法识别"，绝不猜）。 */
function parseStamp(raw) {
  if (isBlank(raw)) return null;
  const m = String(raw).trim().match(DATE_RE);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = m[3] === undefined ? 1 : Number(m[3]);
  if (!(mo >= 1 && mo <= 12) || !(d >= 1 && d <= 31)) return null;
  const hasTime = m[4] !== undefined && m[5] !== undefined;
  const hh = hasTime ? Number(m[4]) : null;
  const mi = hasTime ? Number(m[5]) : null;
  if (hasTime && (hh > 23 || mi > 59)) return null;
  const text = `${y}-${pad2(mo)}-${pad2(d)}` + (hasTime ? ` ${pad2(hh)}:${pad2(mi)}` : '');
  return { y, mo, d, hh, mi, hasTime, text };
}

/** 报销所属期间 → {startMs, endMs, label}：认 `2026-04`（整月）/ `2026-04-01 至 2026-04-30`（区间）/
 *  `2026年4月`（整月）/ `2026-04-15`（单日）；认不出来返回 null。
 *  为什么必须支持整月：报销单上最常见的写法就是"2026-04"，而通行时间是到分钟的。 */
function parsePeriod(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const label = s;
  const stamps = s.match(/\d{4}[-/.年]\d{1,2}(?:[-/.月]\d{1,2}日?)?/g);
  if (!stamps || !stamps.length) return null;
  const a = parseStamp(stamps[0]);
  if (!a) return null;
  if (stamps.length >= 2) {
    const b = parseStamp(stamps[1]);
    if (!b) return null;
    const end = Date.UTC(b.y, b.mo - 1, b.d) + 24 * 60 * 60 * 1000 - 1;
    return { startMs: dayMs(a), endMs: end, label };
  }
  const hasDay = /[-/.月]\d{1,2}日?/.test(stamps[0].replace(/^\d{4}[-/.年]\d{1,2}/, ''));
  if (hasDay) {
    return { startMs: dayMs(a), endMs: dayMs(a) + 24 * 60 * 60 * 1000 - 1, label };
  }
  /* 只到月份：整月（末日用「下月第 0 天」算，闰年由 Date 自己处理） */
  return {
    startMs: Date.UTC(a.y, a.mo - 1, 1),
    endMs: Date.UTC(a.y, a.mo, 0) + 24 * 60 * 60 * 1000 - 1,
    label,
  };
}

/** 把材料切成"通行明细表"与"车辆台账"两张表。
 *  为什么用一行子表标题而不是 `=== 车辆台账 ===`：包的段路由按 `=== 标题 ===` 切材料（见文件头）。 */
function parseTable(text) {
  const lines = String(text).split(/\r?\n/);
  const mark = lines.findIndex((l) => ROSTER_MARK.test(l));
  const mainRaw = (mark < 0 ? lines : lines.slice(0, mark)).filter((l) => l.trim() !== '');
  const rosterRaw = (mark < 0 ? [] : lines.slice(mark + 1)).filter((l) => l.trim() !== '');

  if (!mainRaw.length) {
    return { items: [], totals: {}, roster: new Map(), rosterError: null, missingColumns: null, headers: [] };
  }
  const headers = splitRow(mainRaw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);

  const items = [];
  const totals = {};
  for (let i = 1; i < mainRaw.length; i += 1) {
    const cells = splitRow(mainRaw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      /* 合计行的判据：身份列（所属期间 / 车牌号）被写成「合计」 */
      if ((role === 'period' || role === 'plate') && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (TOTAL_WORDS.test(String(cells[0] === undefined ? '' : cells[0]).trim())) isTotal = true;
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }

  /* 车辆台账：判"是不是公司车"的唯一依据。台账缺了**不猜**，直接报材料不足。 */
  let roster = new Map();
  let rosterError = null;
  if (!rosterRaw.length) {
    rosterError = '材料里没有随表附来的**车辆台账**（车牌号 / 车辆归属）—— '
      + '没有它就无法判断哪些通行费是非公司车辆产生的，本工具不猜';
  } else {
    const rHeaders = splitRow(rosterRaw[0]);
    const rRoles = rHeaders.map((h) => roleOf(h));
    const pIdx = rRoles.indexOf('plate');
    const oIdx = rRoles.indexOf('owner');
    if (pIdx < 0) {
      rosterError = `车辆台账（第 ${mark + 1} 行开始的子表）缺少「车牌号」列：`
        + `已识别的表头是 ${rHeaders.join(' / ') || '（空）'}`;
    } else {
      for (let i = 1; i < rosterRaw.length; i += 1) {
        const cells = splitRow(rosterRaw[i]);
        const plate = String(cells[pIdx] === undefined ? '' : cells[pIdx]).trim();
        if (!plate || TOTAL_WORDS.test(plate)) continue;
        roster.set(plate, {
          plate,
          owner: oIdx < 0 ? '' : String(cells[oIdx] === undefined ? '' : cells[oIdx]).trim(),
          line: mark + 1 + i + 1,
        });
      }
      if (!roster.size) rosterError = '车辆台账里一个车牌号都没有（只有表头）—— 无法判断车辆归属，本工具不猜';
    }
  }
  return { items, totals, roster, rosterError, missingColumns, headers };
}

const who = (it) => {
  const p = it && it.plate ? String(it.plate).trim() : '';
  const id = p ? `${p}（第 ${it.line} 行）` : `第 ${it && it.line} 行`;
  return id;
};
const money = (n) => Number(n).toFixed(2);

/* ================================ 免费档检查项 ================================ */

/** ① 三方勾稽：票面金额 − 折扣金额 = 折扣后金额，且 折扣后金额 = 实付金额。
 *  为什么三项都要：ETC 的折扣是"票面先减优惠再实收"，任何一环漏改（比如按票面报销、折扣没减）
 *  都会让实付与票面对不上 —— 这是通行费报销最常见的一类错。 */
function checkAmounts(it) {
  const face = normNumber(it.face);
  const disc = normNumber(it.discount);
  const net = normNumber(it.net);
  const paidAmt = normNumber(it.paid);
  if (paidAmt === null) return [];
  const out = [];
  if (face !== null && disc !== null && net !== null) {
    const expectNet = round2(face - disc);
    if (Math.abs(expectNet - net) > TOL) {
      out.push({
        level: 'P0', category: '折扣后金额与票面减折扣不符', line: it.line,
        message: `${who(it)}：票面金额 ${money(face)} − 折扣金额 ${money(disc)} = ${money(expectNet)}，`
          + `但折扣后金额填的是 ${money(net)}，相差 ${money(round2(net - expectNet))}。`,
      });
    }
  }
  if (net !== null && Math.abs(net - paidAmt) > TOL) {
    out.push({
      level: 'P0', category: '实付金额与折扣后金额不符', line: it.line,
      message: `${who(it)}：折扣后金额 ${money(net)}，但实付金额填的是 ${money(paid)}，`
        + `相差 ${money(round2(paidAmt - net))} —— 票面 / 折扣 / 折扣后 / 实付 四列必须自洽。`,
    });
  } else if (net === null && face !== null && disc !== null
    && Math.abs(round2(face - disc) - paidAmt) > TOL) {
    out.push({
      level: 'P0', category: '实付金额与票面减折扣不符', line: it.line,
      message: `${who(it)}：票面金额 ${money(face)} − 折扣金额 ${money(disc)} = ${money(round2(face - disc))}，`
        + `但实付金额填的是 ${money(paidAmt)}，相差 ${money(round2(paidAmt - round2(face - disc)))}。`,
    });
  }
  return out;
}

/** ② 重复通行：同一车牌 + 同一通行时间 + 同一实付金额 出现两次 = 同一笔被记了两遍（或重复报销）。
 *  ⚠️ 通行时间只到"日期"一级时，同车同日同额也会被报出 —— 这是**有意的**（宁可让人工确认一次），
 *     消息里会写清这一点，不让买家以为自己看错了。 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const plate = String(it.plate === undefined ? '' : it.plate).trim();
    const stamp = parseStamp(it.date);
    const paidAmt = normNumber(it.paid);
    if (!plate || !stamp || paidAmt === null) continue;
    const key = `${plate}|${stamp.text}|${paidAmt.toFixed(2)}`;
    if (seen.has(key)) {
      const first = seen.get(key);
      out.push({
        level: 'P1', category: '同一车牌同一通行时间重复入账', line: it.line,
        message: `${who(it)}：车牌 ${plate}、通行时间 ${stamp.text}、实付金额 ${money(paidAmt)} `
          + `在第 ${first} 行已经出现过 —— 同一笔通行费被记了两遍（或票被重复报销），请核对原始通行流水后冲掉其中一笔`
          + (stamp.hasTime ? '。' : '。（本行通行时间只到日期，同日同车同额也会被报出，请按流水确认）'),
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** ③ 跨期：通行时间必须落在**本次报销的所属期间**内。
 *  为什么必须核：通行费是"按期间入账"的，3 月的通行费混进 4 月的报销单会让两个月的费用都失真。
 *
 *  ⚠️ 「本次报销所属期间」**不能**只看某一行的期间列：那一列是逐行填的，跨期的那一笔往往
 *     自己写着 3 月（要么全单写 4 月、要么跨期行写 3 月，两种写法都要抓得住）。
 *     所以这里取**材料里出现次数最多的那个所属期间**作为整单口径（并列时取最早的那个），
 *     再拿每一行的通行时间去比 —— 口径会写进结果（scope.period）与结论里，第三方可复算。
 *  期间写法五花八门（2026-04 / 2026年4月 / 2026-04-01 至 2026-04-30），所以先归一化再比；
 *  认不出写法的期间**明确报出来**（不静默跳过），因为跳过等于这一行的跨期判断没做。 */
function batchPeriod(items) {
  const stat = new Map();
  for (const it of items) {
    const per = parsePeriod(it.period);
    if (!per) continue;
    const key = `${per.startMs}-${per.endMs}`;
    if (!stat.has(key)) stat.set(key, { per, n: 0 });
    stat.get(key).n += 1;
  }
  let best = null;
  for (const v of stat.values()) {
    if (!best || v.n > best.n || (v.n === best.n && v.per.startMs < best.per.startMs)) best = v;
  }
  return best ? best.per : null;
}

function checkPeriods(items, batch) {
  const out = [];
  /* 认不出的所属期间写法：按写法去重，一次说清有多少行受影响（逐行刷屏没人看） */
  const unreadable = new Map();
  for (const it of items) {
    const raw = String(it.period === undefined || it.period === null ? '' : it.period).trim();
    if (isBlank(raw) || parsePeriod(raw)) continue;
    if (!unreadable.has(raw)) unreadable.set(raw, { n: 0, line: it.line });
    unreadable.get(raw).n += 1;
  }
  for (const [raw, info] of unreadable) {
    out.push({
      level: 'P1', category: '所属期间无法识别', line: info.line,
      message: `材料里有 ${info.n} 行的所属期间写成「${raw}」，认不出是哪个期间（认 2026-04 / 2026年4月 / `
        + '2026-04-01 至 2026-04-30 这类写法）—— 这些行的跨期判断没有做。',
    });
  }
  if (!batch) return out;

  const start = new Date(batch.startMs).toISOString().slice(0, 10);
  const end = new Date(batch.endMs).toISOString().slice(0, 10);
  for (const it of items) {
    const per = parsePeriod(it.period);
    const stamp = parseStamp(it.date);
    if (!per || !stamp) continue;                       // 认不出的已在上面报过 / 空白由 ⑥ 报
    const ms = dayMs(stamp);
    const outOfBatch = ms < batch.startMs || ms > batch.endMs;
    const differs = per.startMs !== batch.startMs || per.endMs !== batch.endMs;
    if (!outOfBatch && !differs) continue;
    const place = `本次报销所属期间「${batch.label}」（${start} ~ ${end}）`;
    out.push({
      level: 'P1', category: '通行时间不在报销所属期间内', line: it.line,
      message: outOfBatch
        ? `${who(it)}：通行时间 ${stamp.text}（行内所属期间「${per.label}」）不在${place}内 —— `
          + '这笔通行费应当进它自己那个月的报销单（跨期入账）。'
        : `${who(it)}：行内所属期间「${per.label}」与${place}不一致（通行时间 ${stamp.text} 落在本次期间内）`
          + ' —— 请确认这一行的所属期间列是不是填错了。',
    });
  }
  return out;
}

/** ④ 车辆归属：车牌必须能在随表附来的车辆台账里找到，找不到就是**非公司车辆**的通行费。
 *  为什么不能只看明细表里的「车辆归属」列：那一列是报销人手填的，自己填"公司自有"就自己通过了
 *  —— 判归属的依据只能是台账（那是唯一一份外部依据）。 */
function checkOwnership(it, roster) {
  const plate = String(it.plate === undefined ? '' : it.plate).trim();
  if (!plate) return [];
  if (roster.has(plate)) return [];
  return [{
    level: 'P1', category: '非公司车辆通行费', line: it.line,
    message: `${who(it)}：车牌「${plate}」不在本次材料附来的车辆台账里`
      + `（台账共 ${roster.size} 个车牌）—— 非公司车辆产生的通行费不应进公司报销，请先确认这辆车的归属。`,
  }];
}

/** ⑤ 合计行逐列复核：每个金额列的合计 = 各明细行相加（票面 / 折扣 / 折扣后 / 实付）。 */
function checkTotalRow(totals, items, role) {
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
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${money(stated)}，各明细行相加是 ${money(sum)}，`
      + `相差 ${money(round2(stated - sum))}。`,
  });
  return out;
}

/** ⑥ 空白与占位符：所属期间 / 通行时间 / 车牌号 / 实付金额 是其它每一项的前提，空一格整行就核不了。
 *  ⚠️ 通行时间的值**认不出格式**时也必须报出来（不是只会不痛不痒地跳过去）：不报的话这一行会
 *     "静默地不参与"重复检测与跨期检测 —— 这个仓库为这种"不报错、只是永远不给结论"的形态踩过多次坑。 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of KEY_ROLES) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一行没法参与核对。`,
        });
        continue;
      }
      if (role === 'date' && !parseStamp(it.date)) {
        const s = String(it.date).trim();
        out.push({
          level: 'P0', category: '通行时间无法识别', line: it.line,
          message: `${who(it)}的「通行时间」是「${s}」，认不出是哪一天（认 2026-04-03 09:12 或 2026/4/3 这类写法）`
            + ' —— 这一行的重复检测与跨期检测都没有做。',
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */
/** ⑦ 金额为负检测 */
/** ⑧ 同一票据号重复使用检测 */
/** ⑨ 折扣列漏填检测 */
/** ⑩ 车牌号格式异常检测 */
/** ⑪ 车辆归属与车辆台账不一致检测 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到通行费与过路过桥明细表正文（text）—— 请把「所属期间 / 通行时间 / '
      + '车牌号 / 票据号 / 票面金额 / 折扣金额 / 折扣后金额 / 实付金额」这张表，'
      + '以及 `--- 车辆台账 ---` 那一段车牌清单贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `通行费明细表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${t.headers.join(' / ') || '（没有表头行）'}`,
    ]);
  }
  if (t.rosterError) {
    return insufficient([
      t.rosterError,
      '车辆台账请单独起一段：先一行 `--- 车辆台账 ---`，再一行 `车牌号 / 车辆归属` 表头，然后每个车牌一行',
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何一笔通行明细');
  }

  const findings = [];
  const batch = batchPeriod(t.items);
  for (const it of t.items) {
    for (const f of checkAmounts(it)) findings.push(f);
    for (const f of checkOwnership(it, t.roster)) findings.push(f);
  }
  for (const f of checkPeriods(t.items, batch)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkBlanks(t.items)) findings.push(f);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let total = 0;
  for (const it of t.items) {
    const v = normNumber(it.paid);
    if (v !== null) total += v;
  }

  const result = {
    status: 'success',
    service_type: 'TOLL_FEE_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      rows: t.items.length,
      total_paid: round2(total),
      vehicles_in_roster: t.roster.size,
      /* 本次报销所属期间 = 材料里出现次数最多的那个期间（跨期检测就是拿它当口径，见 ③） */
      period: batch ? batch.label : '',
      period_from: batch ? new Date(batch.startMs).toISOString().slice(0, 10) : '',
      period_to: batch ? new Date(batch.endMs).toISOString().slice(0, 10) : '',
      not_run_checks: CHECKS_WITHHELD.slice(),
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
      wrote_files: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"折扣后 = 票面 − 折扣""实付 = 折扣后""合计 = 明细相加""同车同时同额重复""通行时间是否在所属期间内"'
      + '与"车牌是否在车辆台账里"这类**表内/表间勾稽**，不规定折扣与报销口径；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, parseStamp, parsePeriod,
  CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
