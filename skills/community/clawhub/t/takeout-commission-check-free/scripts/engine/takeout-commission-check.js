#!/usr/bin/env node
/**
 * takeout-commission-check.js —— 外卖平台抽佣与配送费核对引擎（完整档 / 买断版）。
 *
 * 真实痛点：**每家做外卖的餐饮店每月都要和美团 / 饿了么 / 抖音外卖的账单对一遍账**。
 * 账单上的钱就是三条串行算式（本工具核的就是这三条）：
 *   ① 佣金（技术服务费）= 结算基数 × 佣金率
 *   ② 商家实收 = 结算基数 − 佣金 − 配送费商家承担 − 活动补贴商家承担
 *   ③ 账单合计 = 各门店 / 各平台明细行相加
 * 佣金率档位用错（8% 的店被按 12% 扣）、配送费在"配送服务费"和"履约服务费"里被扣两次、
 * 活动满减补贴扣了却没结算回来 —— 每一处都是**每月少收几百到几千块**；
 * 而几十上百行的账单靠人眼核不动，这三条却**纯算术、可复算**。
 *
 * 与已有能力的区别（同一个仓库里别买重）：
 *   · `ota-commission-check` 核的是**酒店 OTA 渠道**（房费收入 × 佣金率 → 净结算额）；
 *   · `platform-settlement-check` 核的是**电商平台结算单**（商品成交、退款、技术服务费）；
 *   · `promo-subsidy-check` 核的是**促销补贴的计提与核销**；
 *   · `driver-freight-settlement-check` 核的是**给司机结算运费**（这里是外卖配送费在商家侧的承担）；
 *   本能力核的是**餐饮外卖平台账单**：佣金 + 配送费商家承担 + 活动补贴商家承担 + 商家实收
 *   的逐行复算与合计勾稽；完整档再把这笔差额归因到"佣金档位错 / 配送费重复承担 / 活动补贴未结算"，
 *   给出带行号的申诉口径与补款金额，并按门店排出月度差额（追款清单）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查平台合同与费率档位库、不调用大模型；材料不足不给结论；不代你向平台申诉。
 *
 * ⚠️ 本文件是免费档与完整档的**共用源码**：完整档（买断版）在此基础上追加
 *    「差异归因 + 申诉口径 + 按门店差额排序」那一段；免费包由 tools/strip_free_engine.py
 *    把那段实现摘掉，只留免费检查项（免费包里没有任何付费实现，也没有付费开关）。
 */
'use strict';

const CHECKS_GIVEN = [
  '佣金勾稽（佣金 = 结算基数 × 佣金率）',
  '商家实收勾稽（实收 = 结算基数 − 佣金 − 配送费商家承担 − 活动补贴商家承担）',
  '账单合计行逐列复核（每一列的合计是否等于各明细行之和）',
  '重复行检测（同一门店 + 同一平台 + 同一期间出现多行）',
  '空白与占位符检测（关键字段缺失时不复算、不套默认值）',
];

const CHECKS_WITHHELD = [
  '差异归因（把每笔差额归到：佣金档位错 / 配送费重复承担 / 活动补贴未结算）',
  '补款金额与门店月度差额排序（追款清单，按门店合计差额从大到小）',
  '申诉话术生成（带账单行号、复算依据与应补 / 应退金额）',
  '佣金率超出 0~30% 合理区间检测',
  '商家实收为负检测',
  '商家实收大于结算基数检测',
  '费用项（佣金 / 配送费 / 活动补贴）为负检测',
  '订单数非正检测',
];

const OUT_OF_SCOPE = [
  '判断平台佣金率档位是否符合你与平台签的合同（那是商务条款的事；本工具只按账单自己列示的佣金率复算）',
  '把平台账单里的订单明细逐笔与汇总行勾稽（本表是账单汇总口径；逐笔核对请先把订单明细汇总成同结构）',
  '处理配送费按距离 / 时段 / 天气计价，以及平台补贴与商家自建活动分摊的规则差异',
  '处理退款、取消单、跨期结算与佣金返还等特殊口径',
  '读取 .xlsx 或平台后台账单文件、也不联网抓取平台账单（需要你先导出成文本贴进来）',
  '代你向平台申诉或与平台沟通（本工具只给出可复算的依据与话术文本）',
];

const SAMPLE_TEXT = [
  '门店\t平台\t期间\t结算基数\t佣金率\t佣金\t配送费商家承担\t活动补贴商家承担\t商家实收\t订单数',
  '望京店\t美团\t2026-03\t120000.00\t8%\t9600.00\t3200.00\t4500.00\t102700.00\t1200',
  '望京店\t饿了么\t2026-03\t80000.00\t10%\t8000.00\t2600.00\t3000.00\t66400.00\t800',
  '国贸店\t美团\t2026-03\t150000.00\t8%\t12000.00\t4000.00\t6000.00\t128000.00\t1500',
  '国贸店\t抖音外卖\t2026-03\t60000.00\t5%\t3000.00\t1500.00\t900.00\t54600.00\t500',
  '合计\t\t\t410000.00\t\t32600.00\t11300.00\t14400.00\t351700.00\t4000',
].join('\n');

const TOL = 0.01;          // 金额容差（分）

const ROLES = {
  // ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过三次的坑，见 tools/header_map_check.py）：
  //    「佣金率」必须排在「佣金」之前，否则佣金率那一列会被佣金抢走、整列算错却不会报缺列；
  //    门店别名里**不能**放「商家」（「商家实收」会同时命中门店与实收，导致实收整列被丢掉）。
  party: ['门店', '店铺', '门店名称', '商户'],
  platform: ['平台', '渠道', '平台名称'],
  period: ['期间', '账期', '结算周期', '月份'],
  base: ['结算基数', '抽佣基数', '计佣基数', '商品销售额', '结算金额'],
  rate: ['佣金率', '抽佣率', '技术服务费率', '佣金比例'],
  commission: ['佣金', '技术服务费', '平台服务费', '抽佣'],
  delivery: ['配送服务费商家承担', '配送费商家承担', '配送费', '履约服务费'],
  subsidy: ['活动补贴商家承担', '活动补贴', '补贴分摊', '满减分摊'],
  net: ['商家实收', '实收金额', '结算净额', '到账金额', '实收'],
  orders: ['订单数', '订单笔数', '订单量', '单量'],
};

const LABELS = {
  party: '门店', platform: '平台', period: '期间', base: '结算基数', rate: '佣金率',
  commission: '佣金', delivery: '配送费商家承担', subsidy: '活动补贴商家承担',
  net: '商家实收', orders: '订单数',
};

const REQUIRED = ['party', 'platform', 'period', 'base', 'rate', 'commission', 'delivery', 'subsidy', 'net'];
const SUM_ROLES = ['base', 'commission', 'delivery', 'subsidy', 'net', 'orders'];

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

const round2 = (n) => Math.round(n * 100) / 100;

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
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);

function distinct(items, role) {
  const s = new Set();
  for (const it of items) {
    const v = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
    if (v) s.add(v);
  }
  return [...s];
}

const who = (it) => {
  const parts = [];
  for (const role of ['party', 'platform', 'period']) {
    const v = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
    if (v) parts.push(`${LABELS[role]}「${v}」`);
  }
  return parts.length ? parts.join('·') : `第 ${it.line} 行`;
};

/* ===== 免费档（完整可用的核心产出）执行的检查 ===== */

function checkCommission(it) {
  const base = num(it, 'base');
  const rate = num(it, 'rate');
  const stated = num(it, 'commission');
  if (base === null || rate === null || stated === null) return null;
  const expect = round2(base * rate / 100);
  const diff = round2(stated - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P0', category: '佣金与复算不符', line: it.line,
    message: `${who(it)}的佣金（技术服务费）列的是 ${stated.toFixed(2)}，`
      + `按账单自己列示的 结算基数 ${base.toFixed(2)} × 佣金率 ${rate}% 应为 ${expect.toFixed(2)}，`
      + `${diff > 0 ? `多扣 ${diff.toFixed(2)}` : `少扣 ${Math.abs(diff).toFixed(2)}`}。`,
    advice: `先核佣金率档位：这张账单这一行写的佣金率是 ${rate}%；若实际适用档位不是它，`
      + '账单的「佣金率」列也要一起改 —— 只改佣金、不改佣金率，下个月还会错。',
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
}

function checkNet(it) {
  const base = num(it, 'base');
  const commission = num(it, 'commission');
  const delivery = num(it, 'delivery');
  const subsidy = num(it, 'subsidy');
  const stated = num(it, 'net');
  if (base === null || commission === null || delivery === null || subsidy === null || stated === null) return null;
  const expect = round2(base - commission - delivery - subsidy);
  const diff = round2(stated - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P0', category: '商家实收与复算不符', line: it.line,
    message: `${who(it)}的商家实收列的是 ${stated.toFixed(2)}，按 `
      + `结算基数 ${base.toFixed(2)} − 佣金 ${commission.toFixed(2)} − 配送费商家承担 ${delivery.toFixed(2)} `
      + `− 活动补贴商家承担 ${subsidy.toFixed(2)} = ${expect.toFixed(2)}，`
      + `${diff < 0 ? `账单少结 ${Math.abs(diff).toFixed(2)}` : `账单多结 ${diff.toFixed(2)}`}。`,
    advice: '把这条差额和同一行里的三个扣项比一比（佣金 / 配送费 / 活动补贴）：'
      + '差额等于哪一项，问题就在哪一项 —— 完整档会把差额直接归到这三类并给出申诉口径。',
    basis: `原文第 ${it.line} 行：${it.raw}`,
  };
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
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
          + `相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了某个门店 / 平台，要么合计行没跟着更新；'
          + '合计对不上时先别拿这张账单去核佣金率，先把行数对齐。',
        basis: `原文第 ${t.line} 行：${t.raw}`,
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = ['party', 'platform', 'period']
      .map((r) => String(it.byRole[r] === undefined ? '' : it.byRole[r]).trim()).join('|');
    if (key === '||') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一门店同一平台同一期间出现多行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行又出现一次。`,
        advice: '同一门店同一平台同一期间正常只有一行汇总；重复行会让佣金、配送费和实收一起翻倍，'
          + '先确认是不是"明细行 + 汇总行"混在一张表里了。',
        basis: `原文第 ${it.line} 行：${it.raw}`,
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
          advice: '缺这一格这笔钱就算不出来；补齐前本工具不会用 0 或默认值替你填，也不会替你下结论。',
          basis: `原文第 ${it.line} 行：${it.raw}`,
        });
      }
    }
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
      '含表头的外卖平台月度账单汇总（要能认出「门店」「平台」「期间」「结算基数」'
      + '「佣金率」「佣金」「配送费商家承担」「活动补贴商家承担」「商家实收」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从平台后台账单导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一个明细行（门店 / 平台 / 期间的汇总行）']);

  const findings = [];
  const notRun = [];
  let executed = CHECKS_GIVEN.slice();

  for (const it of t.items) {
    const a = checkCommission(it); if (a) findings.push(a);
    const b = checkNet(it); if (b) findings.push(b);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      stores: distinct(t.items, 'party').length,
      platforms: distinct(t.items, 'platform').length,
      periods: distinct(t.items, 'period').length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      base_total: sumOf('base'),
      commission_total: sumOf('commission'),
      delivery_total: sumOf('delivery'),
      subsidy_total: sumOf('subsidy'),
      net_total: sumOf('net'),
      basis: '佣金（技术服务费）= 结算基数 × 佣金率；商家实收 = 结算基数 − 佣金 − 配送费商家承担 '
        + '− 活动补贴商家承担；账单合计 = 各明细行之和（逐列复核）。',
    },
    scope: {
      executed,
      checks_not_run: notRun,
      out_of_scope: OUT_OF_SCOPE,
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: executed,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张账单按上面写明的口径算得对**：'
      + '佣金 = 结算基数 × 佣金率、商家实收 = 结算基数 − 佣金 − 配送费商家承担 − 活动补贴商家承担、'
      + '合计行逐列相符。它**不代表**平台的佣金率档位与你的合同一致，也不代表订单明细逐笔无差 —— '
      + '那些不在本工具范围内。';
  }



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, ROLES, REQUIRED, SUM_ROLES,
};
