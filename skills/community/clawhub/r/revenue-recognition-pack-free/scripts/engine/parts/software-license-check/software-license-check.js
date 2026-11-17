#!/usr/bin/env node
/**
 * software-license-check-full.js —— 软件许可与云资源费用核对（免费档 / 完整档共用源码）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 真实痛点：**每家公司 IT / 财务在季度与年度预算时都必须核这张台账**，
 * 它是四条独立复算加五处最容易白花钱的地方：
 *   ① 年费用 = 许可数量 × 每许可年单价 × 折扣
 *   ② 月均费用 = 年费用 ÷ 12
 *   ③ 订阅起止与账期月数勾稽（按自然月含首尾月）
 *   ④ 装机或账号数是否超过许可数量（超装 = 合规风险与罚款）
 * 五处白花钱的地方（免费档**只看得到"超装"这个事实**，判不出钱、也列不出清单；
 * 完整档才逐条落地成金额与动作）：
 *   · 超装：装机/账号数超过许可数量，缺口 = 超装数 × 每许可年单价 × 折扣；
 *   · 闲置：在用率远低于 100%（如 40%），多买的许可每月都在白花；
 *   · 自动续费还开着、订阅却早到期了 —— 没人决策，钱自己续下去了；
 *   · 云实例超配：档位是 8 核、平均用量只有 20%，按核数线性折算就是白花的钱；
 *   · 到期 90 天内要决策的续费项 —— 不提前谈价，到期只能按牌价续。
 * 许可一多、账号一多、实例一多，人眼核这几处几乎必漏。
 *
 * 与已有能力的区别：**固定资产盘点**核的是实物资产的数量与存放地点，
 * **费用报销**核的是单据合规与预算科目；本能力核的是**软件许可与云资源账**
 * （许可数量 vs 装机/账号数、订阅起止与自动续费、单价与折扣、云实例档位与用量），
 * 落点在"超装多少、闲置多少、按年化多少钱可以省下来、下一步谁去做什么"。
 *
 * ⛔ 不判断具体软件厂商的授权条款（OEM / 降级权 / 用户数还是设备数 / 跨区使用）——
 *    那要看合同原文，本工具只核**表内可算关系**。
 *
 * ⚠️ 付费项用**形态 B**：先声明名为 paid 的布尔开关，再把付费检查包进以它为条件的块
 *    （**不要**留形态 A 的整块 MARKER —— 两个形态同时存在时 `strip_free_engine`
 *    会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查厂商价目与合同、不调用大模型；材料不足不给结论。
 */
'use strict';

const CHECKS_GIVEN = [
  '年费用复算（许可数量 × 每许可年单价 × 折扣）',
  '月均费用复算（年费用 ÷ 12）',
  '订阅起止与账期月数勾稽（按自然月含首尾月）',
  '装机或账号数超过许可数量（超装嫌疑）',
  '整行内容重复检测（同一软件同一订阅期被登记了两遍）',
  '合计行逐列复核（许可数量 / 装机或账号数 / 年费用 / 月均费用）',
  '关键字段空缺或为占位符检测',
  '明细出现负值或非正数量检测',
  '订阅起止日期倒挂检测（开始日晚于结束日）',
];

const CHECKS_WITHHELD = [
  '超装合规缺口判定（超装数量 × 每许可年单价 × 折扣 = 合规缺口金额）',
  '闲置账号可退订判定（在用率低于 50% 的许可，可退订金额）',
  '自动续费但订阅已到期判定（自动续费还开着、到期日早于核对基准日）',
  '云实例超配可降配判定（实例档位与平均用量占比不匹配，按核数折算可降配金额）',
  '到期 90 天内需决策的续费清单（按年费用排序）',
];

const OUT_OF_SCOPE = [
  '判断某个软件厂商的授权条款（OEM / 降级权 / 用户数还是设备数 / 是否允许跨区使用）——那要看合同原文',
  '判断每许可年单价与折扣本身谈得合不合理（那是采购比价与商务谈判的事）',
  '判断云厂商各档位的实际价目（可降配金额按核数线性折算，是估算不是报价）',
  '判断许可是否真的闲置（本工具只认你填的「装机或账号数」与「平均用量占比」两列，不查登录日志）',
  '处理永久授权、按量计费、跨币种结算等特殊口径（请把它们单独列行，或换算成"每许可年单价"再填）',
  '给出法律或合规意见；读取 .xlsx（需要你先导出成文本贴进来）',
];

// 样例本身就是一张**干净**的软件许可与云资源台账（跑出来 0 条结论）：
// 8 行明细（6 个订阅 + 2 个云实例，4 家供应商）+ 1 行合计；口径写在下面对应检查里。
// 装机/账号数都不超过许可数量、在用率都 ≥ 50%、到期日都在 90 天以外、云实例用量都 ≥ 50%。
const SAMPLE_TEXT = [
  ['软件或资源名称', '供应商', '许可类型', '许可数量', '装机或账号数', '每许可年单价', '折扣',
    '年费用', '月均费用', '订阅开始', '订阅结束', '账期月数', '自动续费', '实例档位',
    '平均用量占比', '核对基准日'],
  ['WPS Office 企业版', '金山办公', '订阅', '200', '190', '320', '90', '57600', '4800',
    '2026-01-01', '2026-12-31', '12', '是', '', '', '2026-06-30'],
  ['Adobe Creative Cloud 全家桶', '奥多比', '订阅', '50', '48', '7800', '85', '331500', '27625',
    '2026-03-01', '2027-02-28', '12', '否', '', '', '2026-06-30'],
  ['AutoCAD 网络版', '欧特克', '订阅', '30', '30', '9600', '100', '288000', '24000',
    '2026-01-01', '2026-12-31', '12', '是', '', '', '2026-06-30'],
  ['云服务器 ECS 通用型', '阿里云', '云实例', '10', '10', '4500', '100', '45000', '3750',
    '2026-04-01', '2027-03-31', '12', '是', '4核8G', '78', '2026-06-30'],
  ['云数据库 RDS MySQL', '阿里云', '云实例', '4', '4', '18000', '100', '72000', '6000',
    '2026-04-01', '2027-03-31', '12', '否', '8核16G', '62', '2026-06-30'],
  ['Microsoft 365 E3', '微软', '订阅', '120', '118', '1300', '100', '156000', '13000',
    '2026-01-01', '2026-12-31', '12', '否', '', '', '2026-06-30'],
  ['数据防泄漏 DLP', '亿赛通', '订阅', '80', '76', '1500', '95', '114000', '9500',
    '2026-02-01', '2027-01-31', '12', '是', '', '', '2026-06-30'],
  ['堡垒机 运维审计', '深信服', '订阅', '2', '2', '36000', '100', '72000', '6000',
    '2026-05-01', '2027-04-30', '12', '否', '', '', '2026-06-30'],
  ['合计', '', '', '496', '478', '', '', '1136100', '94675', '', '', '', '', '', '', ''],
].map((r) => r.join('\t')).join('\n');

const TOL = 0.01;          // 金额容差：1 分
const PCT_TOL = 0.005;     // 用量占比 / 在用率容差（半个百分点）
const LOW_USE = 50;        // 在用率低于这个百分比就算"闲置"（完整档判定用）
const RENEW_WINDOW_DAYS = 90;   // 到期前多少天进入"需要决策"的续费窗口
const DAY = 86400000;

// ⚠️ 关键词顺序就是判据：更具体的词必须排在更宽泛的前面（tools/header_map_check.py 会机械复核）。
//    「软件或资源名称」「每许可年单价」「装机或账号数」「账期月数」「平均用量占比」都必须先于
//    它们的宽泛别名（「单价」「账号数」）出现，否则整列会被抢走、或两列落到同一个角色。
const ROLES = {
  item: ['软件或资源名称', '软件名称', '资源名称', '系统名称', '许可名称'],
  vendor: ['供应商', '厂商', '服务商', '经销商'],
  kind: ['许可类型', '授权类型', '资源类型', '订阅类型', '计费方式'],
  seats: ['许可数量', '授权数量', '订阅数量', '许可数'],
  inUse: ['装机或账号数', '装机数量', '已装数量', '在用数量', '账号数量', '账号数', '装机数'],
  price: ['每许可年单价', '年单价', '许可单价', '单价'],
  discount: ['折扣率', '折扣', '折率'],
  annual: ['年费用', '年度费用', '年化费用', '年化金额'],
  monthly: ['月均费用', '月均金额', '月均', '月费用'],
  start: ['订阅开始', '服务开始', '起租日', '开始日期'],
  end: ['订阅结束', '服务结束', '到期日', '结束日期', '订阅截止'],
  months: ['账期月数', '订阅月数', '账期'],
  autoRenew: ['自动续费', '是否自动续费', '续费方式'],
  spec: ['实例档位', '配置档位', '实例规格', '规格'],
  usage: ['平均用量占比', '用量占比', '资源用量', '用量百分比'],
  asOf: ['核对基准日', '基准日', '核对日期', '核对日'],
};

const LABELS = {
  item: '软件或资源名称', vendor: '供应商', kind: '许可类型', seats: '许可数量',
  inUse: '装机或账号数', price: '每许可年单价', discount: '折扣', annual: '年费用',
  monthly: '月均费用', start: '订阅开始', end: '订阅结束', months: '账期月数',
  autoRenew: '自动续费', spec: '实例档位', usage: '平均用量占比', asOf: '核对基准日',
};

// 表头必须能认出来的列（缺了就不给任何结论）
const REQUIRED = ['item', 'seats', 'inUse', 'price', 'discount', 'annual', 'monthly',
  'start', 'end', 'months'];
// 合计行逐列复核的列（数量与金额可以加；单价、折扣不能加）
const SUM_ROLES = ['seats', 'inUse', 'annual', 'monthly'];
// 判"负值 / 非正数量"的数值列
const NUM_ROLES = ['seats', 'inUse', 'price', 'discount', 'annual', 'monthly', 'months'];

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
  // ⚠️ 顺序即判据：更具体的表头必须排在更宽泛的前面（见上面 ROLES 的注释）
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

function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '').replace(/[./]/g, '-');
  const m = /^(\d{4})-(\d{1,2})(?:-(\d{1,2}))?$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = m[3] === undefined ? 1 : Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const t = Date.UTC(y, mo - 1, d);
  const b = new Date(t);
  if (b.getUTCFullYear() !== y || b.getUTCMonth() !== mo - 1 || b.getUTCDate() !== d) return null;
  return t;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 自然月序号（年 × 12 + 月）：账期月数按自然月口径，不按天数 */
function ymOf(raw) {
  const t = normDate(raw);
  if (t === null) return null;
  const d = new Date(t);
  return d.getUTCFullYear() * 12 + (d.getUTCMonth() + 1);
}

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
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals, roles: have };
}

const num = (it, role) => normNumber(it.byRole[role]);
const amt = (it, role) => {
  const v = num(it, role);
  return v === null ? 0 : v;
};
const fmt = (n) => Number(n).toFixed(2);
const rawOf = (it, role) => String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();

/** 每条结论都用它定位到原文：软件名 + 供应商 + 第几行 */
const who = (it) => {
  const nm = rawOf(it, 'item') || '(未命名软件或资源)';
  const vd = rawOf(it, 'vendor');
  return `软件或资源「${nm}」${vd ? `（供应商 ${vd}）` : ''}（第 ${it.line} 行）`;
};

/** 折扣按百分比口径：100 = 不打折，90 = 九折，85 = 八五折 */
const rowAnnual = (it) => {
  const seats = num(it, 'seats');
  const price = num(it, 'price');
  const dc = num(it, 'discount');
  if (seats === null || price === null || dc === null) return null;
  return round2(seats * price * dc / 100);
};

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkAnnualCost(it) {
  const stated = num(it, 'annual');
  const expect = rowAnnual(it);
  if (stated === null || expect === null) return null;
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '年费用与复算不符', line: it.line, raw: it.raw,
    message: `${who(it)}的年费用是 ${fmt(stated)}，按 许可数量 ${num(it, 'seats')} × 每许可年单价 ${fmt(num(it, 'price'))} × 折扣 ${num(it, 'discount')}% 应为 ${fmt(expect)}。`,
    advice: '年费用只能是"许可数量 × 每许可年单价 × 折扣"三个数相乘；折扣一栏填的是百分比（100 = 不打折、90 = 九折），填 0.9 会被算成零点九个百分点。',
  };
}

function checkMonthlyCost(it) {
  const annual = num(it, 'annual');
  const stated = num(it, 'monthly');
  if (annual === null || stated === null) return null;
  const expect = round2(annual / 12);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '月均费用与复算不符', line: it.line, raw: it.raw,
    message: `${who(it)}的月均费用是 ${fmt(stated)}，按 年费用 ${fmt(annual)} ÷ 12 应为 ${fmt(expect)}。`,
    advice: '月均只按年费用除以 12 算，不随账期月数变；预算表里月均与年费用不一致，两个数就都没法用。',
  };
}

function checkTermMonths(it) {
  const a = ymOf(it.byRole.start);
  const b = ymOf(it.byRole.end);
  const stated = num(it, 'months');
  if (a === null || b === null || stated === null) return null;
  if (b < a) return null;          // 日期倒挂由 checkInverted 单独报，这里不重复认定
  const expect = b - a + 1;
  if (expect === stated) return null;
  return {
    level: 'P0', category: '账期月数与订阅起止不符', line: it.line, raw: it.raw,
    message: `${who(it)}的账期月数是 ${stated}，但按 订阅开始 ${rawOf(it, 'start')} 到 订阅结束 ${rawOf(it, 'end')}`
      + ` 含首尾自然月应为 ${expect} 个月。`,
    advice: '账期月数按"结束月 − 开始月 + 1"算（首尾都算）：起止与月数对不上，摊销和续费提醒都会跟着错。',
  };
}

function checkOversubscribed(it) {
  const seats = num(it, 'seats');
  const inUse = num(it, 'inUse');
  if (seats === null || inUse === null) return null;
  const excess = round2(inUse - seats);
  if (excess <= 0) return null;
  return {
    level: 'P0', category: '装机或账号数超过许可数量', line: it.line, raw: it.raw,
    message: `${who(it)}买了 ${seats} 个许可，实际装机或账号数是 ${inUse}，超装 ${excess} 个。`,
    advice: '超装是合规风险（审计与厂商抽查都可能按未授权使用追责）：先按合同确认授权口径是"用户数"还是"设备数"，再决定补买还是卸载。',
  };
}

function checkInverted(it) {
  const a = normDate(it.byRole.start);
  const b = normDate(it.byRole.end);
  if (a === null || b === null) return null;
  if (a <= b) return null;
  return {
    level: 'P0', category: '订阅起止日期倒挂', line: it.line, raw: it.raw,
    message: `${who(it)}的订阅开始是 ${rawOf(it, 'start')}，订阅结束是 ${rawOf(it, 'end')}，开始日晚于结束日。`,
    advice: '起止写反了：要么两格填颠倒，要么跨年填错了年份。这一天不修，账期月数与到期提醒都会跟着错。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => s + amt(it, role), 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line, raw: t.raw,
        message: `合计行的「${LABELS[role]}」是 ${fmt(stated)}，各明细行相加是 ${fmt(sum)}，相差 ${fmt(stated - sum)}。`,
        advice: '要么明细行漏了一项软件或云资源，要么合计行没跟着更新；合计行是给领导和审计看的那一行，错了整张台账的可信度都没了。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  const KEY_ROLES = ['item', 'vendor', 'kind', 'seats', 'price', 'discount', 'start', 'end'];
  for (const it of items) {
    const key = KEY_ROLES.map((r) => rawOf(it, r)).join('|');
    if (key.replace(/\|/g, '') === '') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '整行内容重复', line: it.line, raw: it.raw,
        message: `第 ${seen.get(key)} 行与第 ${it.line} 行内容完全相同（同一软件「${rawOf(it, 'item')}」、同一订阅期 ${rawOf(it, 'start')} 至 ${rawOf(it, 'end')}）。`,
        advice: '多半是从上一条复制过来忘了改：先确认这一份许可是不是被登记了两遍；确实买了两批，请把数量并到一行，或补上不同的采购单号。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const s = rawOf(it, role);
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段空缺或为占位符', line: it.line, raw: it.raw,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '这一格决定这笔许可费能不能复算、算到哪一期；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function checkNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of NUM_ROLES) {
      const v = num(it, role);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P1', category: '明细出现负值', line: it.line, raw: it.raw,
          message: `${who(it)}的「${LABELS[role]}」是 ${v}。`,
          advice: '退订、冲销、红字调整请单独列一行并在备注写明原因；负数混在明细里，年化金额不是漏算就是重算。',
        });
      }
    }
    const seats = num(it, 'seats');
    if (seats !== null && seats <= 0) {
      out.push({
        level: 'P0', category: '许可数量非正', line: it.line, raw: it.raw,
        message: `${who(it)}的许可数量是 ${seats}。`,
        advice: '许可数量是年费用复算的乘数，为 0 或负数时这一行算不出任何有意义的金额；请确认是漏填，还是把退订行写成了负数。',
      });
    }
  }
  return out;
}

/* ===== 以下函数只有完整档会调用（免费包里没有它们的实现） ===== */

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的软件许可与云资源台账（要能认出「软件或资源名称」「许可数量」「装机或账号数」'
      + '「每许可年单价」「折扣」「年费用」「月均费用」「订阅开始」「订阅结束」「账期月数」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从许可台账 / 云账单导出后，连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一行软件许可或云资源明细（「合计」行不算明细）']);

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkAnnualCost(it); if (a) findings.push(a);
    const b = checkMonthlyCost(it); if (b) findings.push(b);
    const c = checkTermMonths(it); if (c) findings.push(c);
    const d = checkOversubscribed(it); if (d) findings.push(d);
    const e = checkInverted(it); if (e) findings.push(e);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);
  for (const f of checkNegatives(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => s + amt(it, role), 0));

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      suppliers: new Set(t.items.map((it) => rawOf(it, 'vendor')).filter(Boolean)).size,
      seats_total: sumOf('seats'),
      in_use_total: sumOf('inUse'),
      annual_total: sumOf('annual'),
      monthly_total: sumOf('monthly'),
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      basis: '年费用 = 许可数量 × 每许可年单价 × 折扣（折扣按百分比，100 = 不打折）；'
        + '月均费用 = 年费用 ÷ 12；账期月数 = 订阅结束月 − 订阅开始月 + 1（含首尾自然月）；'
        + '合计行逐列复核许可数量 / 装机或账号数 / 年费用 / 月均费用。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  result.scope = {
    tier: 'free',
    checks_run: CHECKS_GIVEN,
    checks_not_run: notRun,
    out_of_scope: OUT_OF_SCOPE,
  };

  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**：'
      + '许可数量与装机/账号数、订阅起止、单价与折扣、年费用与月均的算术都自洽；'
      + '不代表厂商授权条款没问题（OEM、降级权、用户数还是设备数要看合同原文），'
      + '也不代表单价与折扣本身谈得合理。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, normDate, isBlank, round2, ymOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES, LOW_USE, RENEW_WINDOW_DAYS,
};
