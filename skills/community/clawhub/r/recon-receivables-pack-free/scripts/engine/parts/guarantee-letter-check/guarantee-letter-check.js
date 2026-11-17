#!/usr/bin/env node
/**
 * guarantee-letter-check.js —— 保函台账与到期失效核对引擎（确定性、纯 Node 标准库；完整档与免费档共用同一份源码）。
 *
 * 真实痛点：**建筑/外贸/制造企业的资金与授信管理岗每月必做这一步**，而这一步全是可复算的勾稽：
 *   ① 保函金额 = 合同金额 × 保证金比例（开立金额与比例必须自洽）
 *   ② 到期日 = 开立日 + 保函期限月数（到期日算错 → 注销/续期的时点全错）
 *   ③ 同一保函号只能有一行；状态与注销日期必须自洽（已注销必然有注销日期）
 *   ④ 已过到期日却还没注销 → 银行担保额度还占着（白占授信、该释放没释放）
 * 保函到期忘了注销会白占授信额度、该续期没续期会违约、保证金比例算错会多占资金 ——
 * 这三件事都能用这张表算出来对错，所以它是"可被证明"的核对，不是主观判断。
 *
 * 与已有能力的区别：`contract-performance-bond-check` 核的是**保证金收退与保函余额**
 * （应退多少、退了没有、还欠多少）；`bid-deposit-refund-check` 核的是**投标保证金的收退**。
 * 本能力核的是**银行保函台账这一张表本身**：开立金额与比例勾稽、有效期复算、
 * 注销与状态自洽、到期失效与担保额度占用（含 30/60/90 天到期排期与额度释放清单）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查银行保函系统、不解析 .xlsx、不给法律意见；材料不足不给结论。
 *
 * 口径与确定性：
 *   · **基准日（as_of）取台账内最新的一行开立日**（= 这张台账最后更新的时候），**不取本机当天** ——
 *     同一份输入在任何一天复算，得到的清单完全一样。
 *   · 每条结论都带**原文行号**（按粘贴文本的真实行号）。
 *   · 全部分支只做加、减、乘、除与日历算术，第三方拿同一份输入可以逐条复算。
 *
 * ⚠️ 付费项用**形态 B**：先声明常量 paid（值为 Boolean(payload && 任一付费开关字段)），
 *    再把付费检查包进一个「该开关为真时」才执行的 if 块里（**不要**留「完整档才执行的检查」那类 MARKER ——
 *    两个形态同时存在时 strip_free_engine 会走形态 A 把免费检查也整块删掉）。
 *    （本段刻意不写出开关字段与开关语句的字面量：免费包里出现它们会被泄漏守卫判成"还留着付费开关"。）
 */
'use strict';

const CHECKS_GIVEN = [
  '保函金额与合同金额、保证金比例勾稽（保函金额 = 合同金额 × 保证金比例）',
  '有效期复算（到期日 = 开立日 + 保函期限月数，按自然月对齐、月末回退）',
  '同一保函号重复行检测',
  '关键字段空缺与占位符检测',
  '保函金额非正（≤0）检测',
  '保函期限月数非正（≤0）检测',
  '注销日期与状态一致性检测',
  '到期未注销仍占额度检测（已过到期日、未注销且状态仍显示有效）',
];

const CHECKS_WITHHELD = [
  '到期与额度风险判定 + 到期处理清单（30/60/90 天内到期排期：到期日、金额、受益人、行号，按到期日与金额排序）',
  '已过期未注销的应释放额度清单与合计（逐笔带行号，按到期日与金额排序）',
  '保函金额超过合同金额检测',
  '保证金比例低于合同约定比例检测（担保不足）',
  '同一合同同一保函类型出现多份重复保函检测',
  '担保额度占用与保函金额不一致检测',
  '担保额度占用合计与授信额度上限对比',
];

const OUT_OF_SCOPE = [
  '判断保函本身的真伪、银行是否已受理注销（那要向出具银行核验，本工具不联网）',
  '判断保证金比例、保函手续费率、授信额度是否公允（各业主、各地与各银行口径不同，请以合同与银行条款为准）',
  '处理保函展期、换开、索赔、授信调增等合同与银行流程',
  '给出法律意见或索赔/追偿意见；读取 .xlsx（请先把台账导出成文本贴进来）',
];

// 样例：一张**干净**的银行保函台账 —— 五笔保函，金额与比例勾得上、到期日算得对、
// 保函号不重复、状态与注销日期自洽、没有已过期未注销的、额度占用没超授信上限。
// 口径示范：
//   · 基准日 = 台账内最新的一行开立日（2026-04-05）；
//   · 已注销的那一笔不再占用担保额度（担保额度占用写 0.00，不是空着）；
//   · 未注销的保函「担保额度占用」= 保函金额；
//   · 「合同约定比例」是合同要求的最低开立比例（与合同金额一起判断担保是否足额）。
const SAMPLE_TEXT = [
  '保函号\t保函类型\t合同编号\t合同金额\t保证金比例\t合同约定比例\t保函金额\t开立日\t保函期限月数\t到期日\t注销日期\t状态\t受益人\t担保额度占用\t授信额度上限',
  'BH2026-0001\t投标\tHT-2026-018\t12000000.00\t2%\t2%\t240000.00\t2026-01-15\t12\t2027-01-15\t\t有效\t中环广场项目业主\t240000.00\t5000000.00',
  'BH2026-0002\t履约\tHT-2026-018\t12000000.00\t5%\t5%\t600000.00\t2026-02-01\t24\t2028-02-01\t\t有效\t中环广场项目业主\t600000.00\t5000000.00',
  'BH2026-0003\t预付款\tHT-2026-031\t8000000.00\t10%\t10%\t800000.00\t2026-03-10\t12\t2027-03-10\t\t有效\t临港物流园项目业主\t800000.00\t5000000.00',
  'BH2026-0004\t质量\tHT-2026-031\t8000000.00\t3%\t3%\t240000.00\t2026-04-05\t24\t2028-04-05\t\t有效\t临港物流园项目业主\t240000.00\t5000000.00',
  'BH2025-0007\t履约\tHT-2025-009\t5000000.00\t5%\t5%\t250000.00\t2025-03-01\t12\t2026-03-01\t2026-02-28\t已注销\t城西医院项目业主\t0.00\t5000000.00',
].join('\n');

const TOL = 0.01;          // 金额允差 1 分
const AMOUNT_TOL = 0.05;   // 汇总/额度允差 5 分
const RATIO_TOL = 0.02;    // 比例允差 0.02 个百分点
const HORIZONS = [30, 60, 90];

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面（本仓库踩过两次，见 tools/header_map_check.py）。
  //    「保函号」「保函类型」「保函金额」三列都要被各自的列认走；
  //    「合同约定比例」不能被「保证金比例」抢走；「担保额度占用」不能被「授信额度上限」抢走。
  guaranteeNo: ['保函号', '保函编号', '保函号码', '担保编号'],
  type: ['保函类型', '担保类型', '保函种类', '类型'],
  contractNo: ['合同编号', '合同号', '合同号码'],
  contractAmount: ['合同金额', '合同总额', '合同额', '合同总价'],
  agreedRatio: ['合同约定比例', '约定保证金比例', '约定比例', '合同最低比例'],
  depositRatio: ['保证金比例', '保证金率', '开立比例', '保证金百分比'],
  amount: ['保函金额', '保函开立金额', '开立金额', '担保金额', '保函额度'],
  issueDate: ['开立日', '开立日期', '签发日', '签发日期'],
  termMonths: ['保函期限月数', '期限月数', '保函期限', '期限'],
  dueDate: ['到期日', '到期日期', '有效期至', '失效日', '截止日'],
  cancelDate: ['注销日期', '注销日', '退回日期', '失效日期'],
  status: ['状态', '保函状态', '当前状态'],
  beneficiary: ['受益人', '受益单位', '受益人名称', '业主单位'],
  quotaUsed: ['担保额度占用', '占用担保额度', '额度占用', '占用额度'],
  creditLimit: ['授信额度上限', '担保额度上限', '授信上限', '授信额度', '额度上限'],
};

const LABELS = {
  guaranteeNo: '保函号', type: '保函类型', contractNo: '合同编号', contractAmount: '合同金额',
  agreedRatio: '合同约定比例', depositRatio: '保证金比例', amount: '保函金额',
  issueDate: '开立日', termMonths: '保函期限月数', dueDate: '到期日', cancelDate: '注销日期',
  status: '状态', beneficiary: '受益人', quotaUsed: '担保额度占用', creditLimit: '授信额度上限',
};

// 必须能认出来的列（免费档要用到的都在这里）
const REQUIRED = ['guaranteeNo', 'type', 'contractNo', 'contractAmount', 'depositRatio',
  'amount', 'issueDate', 'termMonths', 'dueDate', 'cancelDate', 'status', 'beneficiary'];
// 完整档的额度/约定比例检查还要这三列；缺了就**如实报"这项没跑"**，不给结论
const OPTIONAL = ['agreedRatio', 'quotaUsed', 'creditLimit'];
// 值不能空着的列：注销日期**不在此列** —— 没注销就是空的，空着是对的
const NONBLANK = REQUIRED.filter((r) => r !== 'cancelDate');

const PLACEHOLDER = /^(待填|待补|待定|待核|未知|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;
const STATUS_CANCELLED_RE = /(已注销|已退回|已失效|已撤销|已释放|已解除|已作废)/;
const STATUS_ACTIVE_RE = /(有效|在保|存续|未注销|未到期|正常)/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()：:]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '');
  if (/%$/.test(s)) return Number(s.replace(/%$/, ''));
  if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s);
  const m = s.match(/^(-?\d+(?:\.\d+)?)(万|亿)(元)?$/);
  if (m) return Number(m[1]) * (m[2] === '万' ? 10000 : 100000000);
  return null;
}

const round2 = (n) => Math.round(n * 100) / 100;
const fmt = (n) => (n === null || n === undefined ? '(未填)' : Number(n).toFixed(2));

/** 纯字符串上的天数（Date.UTC 只用来做日历算术，不依赖本机时区） */
function dayNumber(y, m, d) {
  return Math.round(Date.UTC(y, m - 1, d) / 86400000);
}

function daysInMonth(y, m) {
  return new Date(Date.UTC(y, m, 0)).getUTCDate();
}

function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '');
  const m = s.match(/^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$/);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  if (d > daysInMonth(y, mo)) return null;
  return { y, m: mo, d, text: `${y}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`, n: dayNumber(y, mo, d) };
}

/** 开立日 + N 个自然月；目标月没有该日则回退到该月最后一天（1/31 + 1 月 = 2/28） */
function addMonths(date, months) {
  const total = (date.y * 12 + (date.m - 1)) + months;
  const y = Math.floor(total / 12);
  const m = (total % 12 + 12) % 12 + 1;
  const d = Math.min(date.d, daysInMonth(y, m));
  return { y, m, d, text: `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`, n: dayNumber(y, m, d) };
}

function dayText(n) {
  const d = new Date(n * 86400000);
  return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}-${String(d.getUTCDate()).padStart(2, '0')}`;
}

/**
 * 基准日 = 台账内**最新的一行开立日**（不取系统当天，保证确定性）。
 * 返回 null 表示没有任何一行能解析出开立日 —— 此时到期类检查**一律不跑**（不猜）。
 */
function latestIssueDay(items) {
  const days = [];
  for (const it of items) {
    const d = normDate(it.byRole.issueDate);
    if (d) days.push(d.n);
  }
  return days.length ? Math.max.apply(null, days) : null;
}

/** 这笔保函是否已注销/已退回（不再占用担保额度） */
function isCancelled(it) {
  const raw = String(it.byRole.status === undefined ? '' : it.byRole.status).trim();
  if (STATUS_ACTIVE_RE.test(raw)) return false;      // 「未注销」「有效」优先，别被「注销」两字带偏
  if (STATUS_CANCELLED_RE.test(raw)) return true;
  return normDate(it.byRole.cancelDate) !== null;
}

function parseTable(text) {
  const all = String(text).split(/\r?\n/);
  const raw = [];
  const lineNos = [];
  for (let i = 0; i < all.length; i++) {
    if (all[i].trim() === '') continue;
    raw.push(all[i]);
    lineNos.push(i + 1);          // 行号按**粘贴文本的真实行号**记（空行不打乱它）
  }
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
    const row = { line: lineNos[i], raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => `保函号「${String(it.byRole.guaranteeNo || '').trim() || '(未填保函号)'}」`;

/* ===== 免费档（逐笔复算层）：每一笔都能手算复现 ===== */

// ⚠️ 形参刻意写成 `it`（这里 `it` 就是明细行数组）：工厂门禁的变异测试按
//    `function checkXxx(it) {` 找钉死点，找不到就**静默跳过**（守卫空转）。
//    本函数是引擎里第一个 check 函数，保留这个形状 —— 钉死它，这条结论必须消失。
function checkAmountRatio(it) {
  const out = [];
  for (const row of it) {
    const contract = num(row, 'contractAmount');
    const ratio = num(row, 'depositRatio');
    const stated = num(row, 'amount');
    if (contract === null || ratio === null || stated === null) continue;
    if (contract <= 0 || ratio <= 0) continue;      // 合同金额/比例本身不合法时先报那一条，不在这里硬算
    const expect = round2(contract * ratio / 100);
    if (Math.abs(expect - stated) <= TOL) continue;
    out.push({
      level: 'P0', category: '保函金额与比例复算不符',
      line: row.line, amount: stated,
      message: `${who(row)}的保函金额是 ${fmt(stated)}，`
        + `按 合同金额 ${fmt(contract)} × 保证金比例 ${ratio}% 应为 ${fmt(expect)}，`
        + `相差 ${fmt(round2(stated - expect))}。`,
      advice: '保函金额、合同金额、保证金比例三个数必须自洽：比例改过而保函没重开，'
        + '或按含税/不含税口径算错，都表现为这个差。',
    });
  }
  return out;
}

/** 逐笔复算：到期日 = 开立日 + 保函期限月数（自然月对齐、月末回退） */
function checkMaturity(it) {
  const out = [];
  for (const row of it) {
    const issue = normDate(row.byRole.issueDate);
    const term = num(row, 'termMonths');
    const stated = normDate(row.byRole.dueDate);
    if (!issue || term === null || !stated) continue;
    if (term <= 0) continue;                        // 期限非正另有检查
    const expect = addMonths(issue, Math.round(term));
    if (expect.n === stated.n) continue;
    out.push({
      level: 'P0', category: '到期日与开立日加期限不符',
      line: row.line, due_date: stated.text, amount: num(row, 'amount'),
      message: `${who(row)}的到期日是 ${stated.text}，`
        + `按 开立日 ${issue.text} + 保函期限 ${Math.round(term)} 个月 应为 ${expect.text}。`,
      advice: '到期日决定什么时候要办注销/续期；算错一天就可能"该注销没注销、该续期没续期"。'
        + '请以保函正本上记载的到期日为准更正。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.guaranteeNo || '').trim();
    if (!key || isBlank(key)) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P0', category: '同一保函号出现多行', line: it.line,
        amount: num(it, 'amount'),
        message: `保函号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '一笔保函只能记一次：重复行会让保函金额与担保额度占用一起虚增'
          + '（多为重复录入，或把展期换开的新保函沿用了旧保函号）。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(it) {
  const out = [];
  for (const row of it) {
    for (const role of NONBLANK) {
      const s = String(row.byRole[role] === undefined ? '' : row.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: row.line,
          message: `${who(row)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔保函就核不动；补齐前本工具不会用 0 或默认值替你填。'
            + '（「注销日期」没注销时留空是对的，不算缺失。）',
        });
      }
    }
  }
  return out;
}

function checkAmountNonPositive(it) {
  const out = [];
  for (const row of it) {
    const v = num(row, 'amount');
    if (v !== null && v <= 0) {
      out.push({
        level: 'P0', category: '保函金额非正', line: row.line, amount: v,
        message: `${who(row)}的保函金额是 ${v}。`,
        advice: '保函金额必然是正数；0 或负数说明这一格填错（常见：把保证金或手续费填进了保函金额列）。',
      });
    }
  }
  return out;
}

function checkTermNonPositive(it) {
  const out = [];
  for (const row of it) {
    const v = num(row, 'termMonths');
    if (v !== null && v <= 0) {
      out.push({
        level: 'P0', category: '保函期限月数非正', line: row.line,
        message: `${who(row)}的保函期限月数是 ${v}。`,
        advice: '保函期限是自然月数（常见 3/6/12/24 个月）；非正数说明这一格填错，到期日也就无从复算。',
      });
    }
  }
  return out;
}

/** 状态与注销日期必须自洽：已注销必然有注销日期；填了注销日期状态就不能还是"有效" */
function checkCancelConsistency(it) {
  const out = [];
  for (const row of it) {
    const raw = String(row.byRole.status === undefined ? '' : row.byRole.status).trim();
    if (isBlank(raw)) continue;                       // 状态空着由"关键字段缺失"报
    const cancel = normDate(row.byRole.cancelDate);
    const active = STATUS_ACTIVE_RE.test(raw);
    const cancelled = STATUS_CANCELLED_RE.test(raw) && !active;
    if (cancelled && !cancel) {
      out.push({
        level: 'P1', category: '注销日期与状态不一致', line: row.line,
        amount: num(row, 'amount'),
        message: `${who(row)}的状态是「${raw}」，但注销日期是空的。`,
        advice: '状态写已注销就必须有注销日期：没有注销日期，额度到底释放没释放就说不清。'
          + '请按银行退回/注销回执补上日期。',
      });
    }
    if (active && cancel) {
      out.push({
        level: 'P1', category: '注销日期与状态不一致', line: row.line,
        amount: num(row, 'amount'), due_date: cancel.text,
        message: `${who(row)}填了注销日期 ${cancel.text}，状态却还是「${raw}」。`,
        advice: '注销日期与状态两格必须同步改；只改一格会让额度占用、到期排期全都跟着错。',
      });
    }
  }
  return out;
}

/**
 * 到期未注销仍占额度（逐笔事实）：到期日已过基准日、未注销、状态仍显示有效。
 * 基准日 = 台账内最新开立日（不取系统当天）。
 */
function checkExpiredNotCancelled(it, asOf) {
  const out = [];
  for (const row of it) {
    if (isCancelled(row)) continue;
    const due = normDate(row.byRole.dueDate);
    if (!due || due.n >= asOf) continue;
    const overdue = asOf - due.n;
    out.push({
      level: 'P0', category: '到期未注销仍占额度', line: row.line,
      due_date: due.text, amount: num(row, 'amount'),
      message: `${who(row)}的到期日是 ${due.text}，已过基准日 ${dayText(asOf)}（逾期 ${overdue} 天），`
        + `注销日期为空、状态是「${String(row.byRole.status || '').trim() || '(空)'}」，`
        + `保函金额 ${fmt(num(row, 'amount'))} 仍被记为占用。`,
      advice: '到期后要么办注销/退回并释放额度，要么办续期并更新到期日；'
        + '既不注销也不续期，银行担保额度会一直白占着。',
    });
  }
  return out;
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的银行保函台账（要能认出「保函号」「保函类型」「合同编号」「合同金额」「保证金比例」'
      + '「保函金额」「开立日」「保函期限月数」「到期日」「注销日期」「状态」「受益人」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从保函台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行保函明细']);

  const findings = [];
  const notRun = [];

  // 基准日 = 台账内最新开立日（免费档也要用：判断"到期未注销"）
  const asOf = latestIssueDay(t.items);

  // —— 免费档：逐笔复算层 ——
  for (const f of checkAmountRatio(t.items)) findings.push(f);
  for (const f of checkMaturity(t.items)) findings.push(f);
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkAmountNonPositive(t.items)) findings.push(f);
  for (const f of checkTermNonPositive(t.items)) findings.push(f);
  for (const f of checkCancelConsistency(t.items)) findings.push(f);
  if (asOf === null) {
    notRun.push('到期未注销仍占额度检测（台账里没有一行能解析出开立日，基准日无法确定）');
  } else {
    for (const f of checkExpiredNotCancelled(t.items, asOf)) findings.push(f);
  }

  let schedule = [];
  let releaseList = [];
  let releaseTotal = 0;

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const sumOf = (role, filter) => round2(t.items.reduce((s, it) => {
    if (filter && !filter(it)) return s;
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const occupiedTotal = sumOf('quotaUsed', (it) => !isCancelled(it));
  const limits = t.items.map((it) => num(it, 'creditLimit')).filter((n) => n !== null);
  const creditLimit = limits.length ? round2(limits[0]) : null;

  const result = {
    findings,
    summary: {
      guarantees: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      contract_total: sumOf('contractAmount'),
      amount_total: sumOf('amount'),
      quota_occupied_total: occupiedTotal,
      credit_limit: creditLimit,
      as_of: asOf === null ? '' : dayText(asOf),
      basis: '保函金额 = 合同金额 × 保证金比例；到期日 = 开立日 + 保函期限月数（自然月对齐、月末回退）；'
        + '同一保函号唯一；状态与注销日期自洽；基准日 = 台账内最新开立日（不取系统当天）；'
        + '未注销保函的担保额度占用 = 保函金额，已注销的不再占用。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对**，'
      + '不代表保函本身真实、也不代表保证金比例与授信额度公允 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    guarantees: t.items.length,
    total_rows_ignored: t.totals.length,
    as_of: asOf === null ? '' : dayText(asOf),
    amount_total: sumOf('amount'),
    quota_occupied_total: occupiedTotal,
    credit_limit: creditLimit,
  };
  result.scope = scope;


  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, round2, addMonths, dayText, latestIssueDay, isCancelled, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, OPTIONAL, NONBLANK, HORIZONS,
};
