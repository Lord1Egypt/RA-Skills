'use strict';
/**
 * teacher-hour-pay-check.js —— 课时消耗与教师课时费核对（免费档 / 完整档共用源码）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），不写盘、不读环境变量。
 *
 * 真实痛点：教培机构每月要给老师结课时费，源头是两套数：
 *   ① **学员课时消耗**（学员课时包里扣掉多少课时，来自教务系统「课耗」）；
 *   ② **教师课时费**（老师上了几节课 × 课时单价，再加代课补贴）。
 * 两条线各记一套，财务就是要把它们核到一起。可这张表里全是纯算术，几十上百行没人愿意手核：
 *   · 课时费 = 课时数 × 课时单价（逐行复算；单价录错一位、课时数漏乘都是钱）
 *   · 正课 / 试听 / 补课 的**口径不一样**：试听与补课**不消耗学员课时**（补课是服务补救，
 *     原课次已经扣过），但老师照拿课时费 —— 把两套口径混着填，两边都对不平
 *   · 学员消课课时 与 系统课耗课时 必须逐笔相等（差一笔就是学员课时包或老师课时费算错）
 *   · 合计行的课时消耗合计必须等于明细之和
 *   · 课时单价不得低于合同保底单价（低价排课会直接亏）
 *   · 同一教师同一天同一课型同样课时数的重复记录、关键字段空缺
 * 每一步都带原文行号，第三方可按同一口径复算。
 *
 * 与已有能力的区别：`training-hour-consumption-check` 核的是培训课时消耗台账本身；
 * 本能力核的是**教师课时费与学员课时消耗两条线的对账口径**：逐行复算、课型口径、双线勾稽、
 * 合计复核、保底单价、重复与空缺。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不判排课/考勤是否真实、不给劳动法或合同意见；材料不足不给结论。
 *
 * ⚠️ 完整档（付费）的实现集中在下方 MARKER 与 `function run(payload) {` 之间，
 *    免费包会**整块**摘掉它；免费包只保留免费检查项。
 */

const CHECKS_GIVEN = [
  '课时费 = 课时数 × 课时单价 逐行复算',
  '正课 / 试听 / 补课 口径区分（试听与补课不消耗学员课时）',
  '课时消耗与系统课耗逐笔勾稽（学员消课课时 vs 系统课耗课时）',
  '合计行逐列复核（课时消耗合计必须等于明细之和）',
  '课时单价低于合同保底单价',
  '重复课时记录与关键字段空缺检测（教师 + 日期 + 课型 + 课时数）',
];

const CHECKS_WITHHELD = [
  '跨教师 / 跨校区汇总台账（逐组汇总课时、课耗、实发课时费与差额，按差额从大到小排序）',
  '按差额排序的处理清单（先核哪几笔，带原文行号与金额）',
  '课时费差额归因：课时数差异 / 单价差异 / 代课补贴 / 录入口径残差（四项之和恒等于总差额）',
  '同一教师同一课程类型的课时单价一致性检测（同一课型不该出现两个价）',
  '同一教师同一日课时数超过单日上限检测（默认 8 课时）',
];

const OUT_OF_SCOPE = [
  '判断排课、考勤与上课是否真实发生（那是教务排课系统、签到与监控的事）',
  '判断课时包售卖价格、退费与赠课规则是否合规（那是销售合同与退费政策的事）',
  '判断课时单价、保底单价与代课补贴标准本身是否合理或合法（那是劳动合同/课酬制度的事）',
  '处理跨月结转、跨校区调课、教师离职结算与个税社保代扣（口径按制度，需逐项确认）',
  '区分同一教师同一天给不同学员上同样长度的课（本表没有学员列，请加一列学员再核）',
  '读取 .xlsx / .pdf 原文件（需要你先导出成文本贴进来）',
];

/** 干净样例：一张算得对的课时消耗与教师课时费明细表（两档都必须 0 条问题） */
const SAMPLE_TEXT = [
  '教师\t校区\t课程类型\t上课日期\t课时数\t课时单价\t课时费\t代课补贴\t学员消课课时\t系统课耗课时\t合同保底单价',
  '张老师\t中关村校区\t正课\t2025-03-03\t2\t120.00\t240.00\t0.00\t2\t2\t100.00',
  '张老师\t中关村校区\t正课\t2025-03-04\t3\t120.00\t360.00\t0.00\t3\t3\t100.00',
  '张老师\t中关村校区\t试听\t2025-03-05\t1\t120.00\t120.00\t0.00\t0\t0\t100.00',
  '李老师\t望京校区\t补课\t2025-03-06\t1.5\t130.00\t195.00\t50.00\t0\t0\t110.00',
  '合计\t\t\t\t7.5\t\t915.00\t50.00\t5\t5\t',
].join('\n');

/** 金额容差：0.01 元（表里都是两位小数，四舍五入到分以后要能对齐） */
const TOL = 0.01;

/** 单日课时上限（完整档的排课超限检测用；正课 1 课时通常 40~60 分钟） */
const DAILY_HOUR_CAP = 8;

/**
 * 表头 → 角色的关键词表。
 * ⚠️ **顺序即优先级**：更具体的角色必须排在更宽泛的角色前面，否则宽泛词会把具体列抢走
 *    （例如「合同保底单价」会被「单价」抢走、「课时费」会被「课时」抢走 ⇒ 列被覆盖、静默算错）。
 */
const ROLES = {
  teacher: ['教师姓名', '授课教师', '教师', '老师'],
  campus: ['校区', '教学点', '分校区', '分校'],
  courseType: ['课程类型', '课次类型', '课时类型', '课型', '课别'],
  date: ['上课日期', '授课日期', '课次日期', '日期'],
  floor: ['合同保底单价', '保底课时单价', '保底单价', '合同单价'],
  pay: ['课时费', '应发课时费', '课时金额', '课酬'],
  rate: ['课时单价', '课时标准', '标准课时费', '单价'],
  subsidy: ['代课补贴', '代课费', '补贴'],
  consumed: ['学员消课课时', '消课课时', '课时消耗', '课消课时'],
  sysConsumed: ['系统课耗课时', '系统课耗', '系统消课', '课耗课时'],
  hours: ['课时数', '授课课时', '课次课时', '课时'],
};

const LABELS = {
  teacher: '教师', campus: '校区', courseType: '课程类型', date: '上课日期',
  hours: '课时数', rate: '课时单价', pay: '课时费', subsidy: '代课补贴',
  consumed: '学员消课课时', sysConsumed: '系统课耗课时', floor: '合同保底单价',
};

/** 必需列：缺一个就**不给结论**（宁可说"材料不足"，也不套默认值） */
const REQUIRED = ['teacher', 'campus', 'courseType', 'date', 'hours', 'rate', 'pay',
  'subsidy', 'consumed', 'sysConsumed', 'floor'];

/** 可以逐列复核合计的列（课时单价、合同保底单价是"价"，求和无意义） */
const SUM_ROLES = ['hours', 'pay', 'subsidy', 'consumed', 'sysConsumed'];

const BASIS = '课时费 = 课时数 × 课时单价；学员消课课时 = 系统课耗课时；'
  + '试听与补课不消耗学员课时（消课课时应为 0），正课必须有课时消耗；'
  + '课时单价 ≥ 合同保底单价；合计行逐列复核。';

/** 课程类型别名：只认三种口径，认不出就报「口径异常」而不是猜 */
const KIND_ALIASES = [
  ['正课', ['正课', '常规课', '正式课', '正常课', '标准课']],
  ['试听', ['试听课', '试听', '体验课']],
  ['补课', ['补课时', '补课', '补习']],
];

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice || '请补上这些再跑；材料不足时本工具不做任何认定，也不会套用 0 或默认值替你填。',
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

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥$,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

const money = (n) => Number(n).toFixed(2);

function roleOf(header) {
  const h = String(header === undefined || header === null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const role of Object.keys(ROLES)) {
    if (ROLES[role].some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/**
 * 解析：把整段文本当成"第一张非空行是表头、其余是数据行"的表。
 * 返回 { header, cols, items, totals, missingColumns, missingRoles } 或 { error }。
 * `line` 是**原文行号**（1 起，跳过空行时也保留真实行号），结论据此可回查原文。
 */
function parseTable(text) {
  const all = String(text === undefined || text === null ? '' : text).split(/\r?\n/);
  const idx = [];
  for (let i = 0; i < all.length; i++) if (all[i].trim() !== '') idx.push(i);
  if (!idx.length) {
    return { error: 'empty', header: [], cols: [], items: [], totals: [], missingColumns: [], missingRoles: [] };
  }
  const header = splitRow(all[idx[0]]);
  const cols = header.map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return {
      error: 'no_header', header, cols, items: [], totals: [],
      missingColumns: missingRoles.map((r) => LABELS[r]), missingRoles,
    };
  }
  const items = [];
  const totals = [];
  for (let k = 1; k < idx.length; k++) {
    const i = idx[k];
    const cells = splitRow(all[i]);
    const byRole = {};
    cols.forEach((c, ci) => {
      if (c.role && byRole[c.role] === undefined) {
        byRole[c.role] = cells[ci] === undefined ? '' : cells[ci];
      }
    });
    const row = { line: i + 1, raw: all[i], byRole };
    const first = String(cells[0] === undefined ? '' : cells[0]).trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { header, cols, items, totals, missingColumns: [], missingRoles: [] };
}

const num = (it, role) => normNumber(it.byRole[role]);
const text = (it, role) => String(it.byRole[role] === undefined || it.byRole[role] === null ? '' : it.byRole[role]).trim();
const teacherOf = (it) => text(it, 'teacher');
const campusOf = (it) => text(it, 'campus');
const dayOf = (it) => text(it, 'date');

function kindOf(raw) {
  const s = String(raw === undefined || raw === null ? '' : raw).replace(/[\s（）()\-—_]/g, '');
  if (!s) return null;
  for (const pair of KIND_ALIASES) {
    if (pair[1].some((a) => s.indexOf(a) >= 0)) return pair[0];
  }
  return null;
}

const who = (it) => {
  const t = teacherOf(it) || '(未填教师)';
  const c = campusOf(it);
  return c ? `教师「${t}」(${c})` : `教师「${t}」`;
};

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

/* =========================== 免费档：逐行与合计检查 =========================== */

/** ① 课时费 = 课时数 × 课时单价（最常错的一格） */
function checkPayFormula(it, ev) {
  const hours = num(it, 'hours');
  const rate = num(it, 'rate');
  const stated = num(it, 'pay');
  if (hours === null || rate === null || stated === null) return null;
  const expect = round2(hours * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '课时费与复算不符', line: it.line, amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}课时费填 ${money(stated)}，按 课时数 ${hours} × 课时单价 ${money(rate)} 复算应为 ${money(expect)}，`
      + `相差 ${money(round2(stated - expect))}。`,
    evidence: ev(it.line),
    advice: '课时费这一格必须能由「课时数 × 课时单价」复算出来；单价调过、课时数录错，都会直接变成钱。',
  };
}

/** ② 正课 / 试听 / 补课 的口径区分 */
function checkCourseKind(it, ev) {
  const raw = text(it, 'courseType');
  if (!raw) return null;                        // 空缺交给空缺检查，不在这里重复报
  const kind = kindOf(raw);
  const consumed = num(it, 'consumed');
  if (!kind) {
    return {
      level: 'P1', category: '课程类型口径异常', line: it.line, amount: 0,
      message: `${who(it)}（原文第 ${it.line} 行）的课程类型是「${raw}」，认不出属于 正课 / 试听 / 补课 哪一类，`
        + '无法判断该不该消耗学员课时。',
      evidence: ev(it.line),
      advice: '课程类型只写「正课」「试听」「补课」三种口径（可带前后缀，如"正课-数学"）；新口径先说清楚口径再核。',
    };
  }
  if (consumed === null) return null;
  if (kind !== '正课' && consumed !== 0) {
    return {
      level: 'P1', category: '课程类型口径异常', line: it.line, amount: Math.abs(consumed),
      message: `${who(it)}这一行是${kind}，按口径不该消耗学员课时，但「学员消课课时」填了 ${consumed}。`,
      evidence: ev(it.line),
      advice: '试听与补课都不重复扣学员课时（补课是服务补救，原课次已经扣过），这一格应为 0；确实要扣请在备注里写依据。',
    };
  }
  if (kind === '正课' && consumed === 0) {
    return {
      level: 'P1', category: '课程类型口径异常', line: it.line, amount: 0,
      message: `${who(it)}这一行是正课，却没有学员课时消耗（「学员消课课时」是 0）—— 要么这一格漏填，要么课型填错了。`,
      evidence: ev(it.line),
      advice: '正课必须对应学员课时消耗；先确认这一格是不是漏填，或者把课型改成试听 / 补课。',
    };
  }
  return null;
}

/** ③ 学员消课课时 = 系统课耗课时（两条线逐笔勾稽） */
function checkConsumedTie(it, ev) {
  const a = num(it, 'consumed');
  const b = num(it, 'sysConsumed');
  if (a === null || b === null) return null;
  const diff = round2(a - b);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P0', category: '课时消耗与系统课耗不符', line: it.line, amount: Math.abs(diff),
    message: `${who(it)}学员消课课时 ${a}，系统课耗课时 ${b}，相差 ${diff}。`,
    evidence: ev(it.line),
    advice: '这两列必须逐笔对上：差一笔就意味着学员课时包与教师课时费至少有一边算错了。',
  };
}

/** ④ 课时单价不得低于合同保底单价 */
function checkRateFloor(it, ev) {
  const rate = num(it, 'rate');
  const floor = num(it, 'floor');
  if (rate === null || floor === null) return null;
  if (rate >= floor - TOL) return null;
  const gap = round2(floor - rate);
  const hours = num(it, 'hours');
  return {
    level: 'P0', category: '课时单价低于合同保底单价', line: it.line,
    amount: round2(gap * (hours === null ? 1 : hours)),
    message: `${who(it)}课时单价填 ${money(rate)}，低于合同保底单价 ${money(floor)}，每课时少 ${money(gap)}`
      + `${hours === null ? '' : `，这一行共少 ${money(round2(gap * hours))}`}。`,
    evidence: ev(it.line),
    advice: '低于保底单价的排课会直接亏；确认是单价录错、还是走了特批（特批要有依据并单独列示）。',
  };
}

/** ⑤ 合计行逐列复核（课时消耗合计必须等于明细之和） */
function checkTotalRow(totals, items, role, ev) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: t.line, amount: Math.abs(round2(stated - sum)),
      message: `合计行「${LABELS[role]}」填 ${money(stated)}，${items.length} 个明细行相加是 ${money(sum)}，`
        + `相差 ${money(round2(stated - sum))}。`,
      evidence: ev(t.line),
      advice: '要么明细行漏了一行，要么合计行没跟着更新；课时消耗合计对不上，两边就都结不了账。',
    });
  }
  return out;
}

/** ⑥a 同一教师 + 同一日期 + 同一课型 + 同一课时数出现多行 */
function checkDuplicateSessions(items, ev) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const t = teacherOf(it);
    const d = dayOf(it);
    const k = text(it, 'courseType');
    const h = num(it, 'hours');
    if (!t || !d || !k || h === null) continue;
    const key = `${t}|${d}|${k}|${h}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一教师同一日期同一课型同样课时数出现多行', line: it.line, amount: 0,
        message: `「${t}」在 ${d} 的${k} ${h} 课时，第 ${seen.get(key)} 行已经记过一次，第 ${it.line} 行又出现一次。`,
        evidence: ev(it.line),
        advice: '同一教师同一天给不同学员上同样长度的课是正常的，但本表没有学员列 —— 请加一列学员（或课次编号）区分；'
          + '若确实是同一节课重复录入，课时费会翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** ⑥b 关键字段空缺或占位符 */
function checkBlanks(items, ev) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const raw = it.byRole[role];
      const s = String(raw === undefined || raw === null ? '' : raw).trim();
      if (isBlank(raw) || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line, amount: 0,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          evidence: ev(it.line),
          advice: '缺这一格这一行就算不出来；补齐前本工具不会用 0 或默认值替你填，也不会给结论。',
        });
      }
    }
  }
  return out;
}

function countLevels(findings) {
  const lv = { p0: 0, p1: 0, p2: 0 };
  for (const f of findings) {
    if (f.level === 'P0') lv.p0 += 1;
    else if (f.level === 'P1') lv.p1 += 1;
    else lv.p2 += 1;
  }
  return lv;
}

const byPosition = (a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category));

function buildSummary(t, findings, ledger, attr) {
  const lv = countLevels(findings);
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const payTotal = sumOf('pay');
  const subsidyTotal = sumOf('subsidy');
  const dueTotal = round2(t.items.reduce((s, it) => {
    const c = num(it, 'consumed');
    const f = num(it, 'floor');
    return s + (c === null || f === null ? 0 : c * f);
  }, 0));
  const s = {
    rows: t.items.length,
    total: findings.length,
    p0: lv.p0,
    p1: lv.p1,
    p2: lv.p2,
    omitted: 0,
    hours_total: sumOf('hours'),
    pay_total: payTotal,
    subsidy_total: subsidyTotal,
    consumed_total: sumOf('consumed'),
    sys_consumed_total: sumOf('sysConsumed'),
    due_total: dueTotal,
    variance_total: round2(payTotal + subsidyTotal - dueTotal),
    verdict: lv.p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
    basis: BASIS,
  };
  if (ledger) {
    s.ledger_groups = ledger.rows.length;
    s.action_items = ledger.action_items.length;
  }
  if (attr) {
    s.attribution_total = attr.total_variance;
    s.attribution_residual = attr.entry_residual;
  }
  return s;
}

function run(payload) {
  const p = payload;
  if (p !== undefined && p !== null && typeof p !== 'object') {
    return insufficient([`入参不是对象（收到的是 ${typeof p}）`], '用法：{"text":"（把表头和数据行一起复制进来，Tab 分隔最稳）"}');
  }
  if (!p) {
    return insufficient(['原文（text）', '课时消耗与教师课时费明细表的表头与数据行'],
      '用 {"text":"…"} 传材料；或先用 --sample 看看需要什么格式。');
  }
  const raw = p.text !== undefined ? p.text : p.content;
  const body = Array.isArray(raw) ? raw.join('\n') : raw;
  if (!String(body === undefined || body === null ? '' : body).trim()) {
    return insufficient(['原文（text）', '课时消耗与教师课时费明细表的表头与数据行（Tab 分隔最稳）'],
      '把表头和你关心的数据行一起复制成文本贴进来，别只贴合计行。');
  }
  const srcName = String(p.file || p.name || p.filename || '课时消耗与教师课时费明细表').trim() || '课时消耗与教师课时费明细表';
  const ev = (line) => `${srcName}:${line}`;

  const t = parseTable(body);
  if (t.error === 'empty') {
    return insufficient(['原文（text）', '至少一行表头'], '贴进来的内容全是空白。');
  }
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的课时消耗与教师课时费明细表（要能认出「教师」「校区」「课程类型」「上课日期」「课时数」'
      + '「课时单价」「课时费」「代课补贴」「学员消课课时」「系统课耗课时」「合同保底单价」）',
      `本次没认出来的列：${t.missingColumns.join('、')}`,
      '从教务/课时费台账导出后**连同表头**一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行明细（表头下面至少一行数据）'],
      '只给了表头（或只有合计行）无法核对；把明细行一起贴进来。');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkPayFormula(it, ev); if (a) findings.push(a);
    const b = checkCourseKind(it, ev); if (b) findings.push(b);
    const c = checkConsumedTie(it, ev); if (c) findings.push(c);
    const d = checkRateFloor(it, ev); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role, ev)) findings.push(f);
  }
  for (const f of checkDuplicateSessions(t.items, ev)) findings.push(f);
  for (const f of checkBlanks(t.items, ev)) findings.push(f);
  findings.sort(byPosition);

  const result = {
    status: 'success',
    service_type: 'TEACHER_HOUR_PAY_CHECK',
    source: srcName,
    columns: t.cols.map((c) => c.header),
    findings,
    summary: buildSummary(t, findings),
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      rows: t.items.length,
      total_rows: t.totals.length,
      executed_locally: true,
      network_used: false,
    },
    checks_given: CHECKS_GIVEN.slice(),
    checks_withheld: CHECKS_WITHHELD.slice(),
    checks_executed: CHECKS_GIVEN.slice(),
    checks_not_run: CHECKS_WITHHELD.slice(),
    checks_out_of_scope: OUT_OF_SCOPE,
    basis: BASIS,
    disclaimer: '只核这张表内部的算术与口径勾稽：结论都带**原文行号**、可由第三方用同一口径复算；'
      + '不代替排课/考勤记录与教师合同，不做劳动法或薪酬制度意见，也不判断单价与补贴标准本身。',
  };

  if (findings.length === 0) {
    result.note = '本次执行的检查项都没有报出问题 —— 这只说明**这张表按上面写明的口径算得对**，'
      + '不代表排课与课时消耗真实、也不代表课酬制度本身合理，那些不在本工具范围内。';
  } else {
    result.note = `本次共报出 ${findings.length} 条需要复核的问题（P0 ${result.summary.p0} 条 / P1 ${result.summary.p1} 条），`
      + '每条都带原文行号与出处，可以按同一口径复算。';
  }

  // 完整档开关：只在这一行判断档位（免费包里这一行会被整行摘掉）
    result.scope.tier = 'free';
  

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
