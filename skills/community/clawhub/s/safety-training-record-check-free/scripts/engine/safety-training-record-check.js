#!/usr/bin/env node
/**
 * 安全教育培训记录与签到核对引擎 —— 制造业 / 建筑业 / 物业 / 危化企业的**每月必做**材料核对
 * （确定性、纯 Node 标准库）。
 *
 * 真实痛点：《安全生产法》要求新员工做**三级安全教育**（厂级 / 车间级 / 班组级），转岗与复工要再培训，
 * 特种作业人员必须持证上岗，每年**再教育学时**要达标，而且签到表、试卷 / 考核成绩、培训内容记录
 * 都要能查到。检查时「签到有、学时不够」「新人没做三级教育就上岗」「证过期还在排班」都是直接处罚项。
 * 安环部每个月都要把「应培训人员名单 - 培训计划 - 签到与学时 - 考核成绩 - 证书有效期」对上，
 * 这一步几乎全是跨列算术与名单勾稽：一张几十人的表人工核要小半天，还容易漏人、漏层级。
 *
 * 本引擎分两档（同一份源码）：免费档只做上面这些逐行核对；买断的完整档在此基础上**再多做**
 * 三级教育层级完整性、特种作业证有效期覆盖、培训内容与岗位风险匹配、
 * 培训记录与工资 / 考勤时间冲突、分部门×分培训类型汇总清单（按未达标人数排序，带可整改动作）。
 * 免费包里**没有**这五类的实现，只如实列出未执行项（见 CHECKS_WITHHELD）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定培训是否真实发生、不判定培训内容专业上是否充分、不代替法定合规结论、
 *          不读 .xlsx / .pdf 原件、不联网核验证书真伪；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '学时勾稽（逐行复算 结束时间 − 开始时间 得实际学时，再与「学时」「计划学时」两列比对）',
  '再教育学时达标（每人的 年度累计学时 与 规定下限 比对，不达标点名到人）',
  '应培训人员覆盖（应培训名单 vs 签到名单：应培训未签到 / 名单外多签到，逐行点名到人）',
  '同一人 + 同一培训主题 + 同一培训日期 重复登记检测',
  '考核成绩与合格线（成绩 < 合格线 即报出，并指出补考记录缺失）',
  '空白 / 占位符 / 时间与日期格式 / 负学时检测（关键字段缺失、格式不合法、数值无法解析或为负）',
];

const CHECKS_WITHHELD = [
  '三级教育层级完整性（新员工必须同时有 厂级 / 车间级 / 班组级 三条记录，缺哪一级点名到人）',
  '特种作业证有效期覆盖（培训 / 作业日期 不得晚于 证件到期日）',
  '培训内容与岗位风险匹配（按「岗位应训主题」清单逐项检查该人是否缺训）',
  '培训记录与工资 / 考勤时间冲突（培训时间段 与 出勤时间段 重叠即报出）',
  '分部门×分培训类型汇总清单（按未达标人数排序，给出可整改动作）+ 整改清单 consolidated_actions',
];

const OUT_OF_SCOPE = [
  '判定某次培训是否**真实发生**（签到表、试卷、现场照片的真伪）—— 那是现场检查与安全监管的认定权，本工具只核表内数字与字面记录',
  '判定培训内容是否**专业上充分**（课时安排是否合理、讲师是否有资格、课件是否覆盖岗位风险），本工具只核「岗位应训主题」有没有被点到',
  '代替《安全生产法》与地方规定给出合规结论（是否达到法定学时、这个人是否可以上岗）—— 本工具只按你表里给出的下限做算术比对',
  '读取 .xlsx / .pdf 原件、联网核验证书真伪、替代安全培训档案的纸质归档',
];

// 样例：一张**干净**的安全教育培训与签到台账 —— 新员工三级教育三级齐全、特种作业证在有效期内、
// 学时 = 起止时间复算值 = 计划学时、年度累计学时都不低于规定下限、签到与应培训名单一致、考核全部合格。
const SAMPLE_TEXT = [
  "姓名\t部门/班组\t岗位\t培训类型\t培训主题\t教育层级\t培训日期\t开始时间\t结束时间\t学时\t计划学时\t是否应培训\t是否签到\t考核成绩\t合格线\t补考成绩\t年度累计学时\t规定下限\t特种作业证号\t证件到期日\t岗位应训主题\t出勤时间段\t备注",
  "赵新宇\t生产二车间/A班\t操作工\t三级教育\t三级安全教育（厂级）\t厂级\t2026-03-02\t08:30\t12:00\t3.5\t3.5\t是\t是\t92\t80\t\t24\t20\t\t\t三级安全教育;危化品应急处置;岗位操作规程\t\t新员工入职首日，先做厂级教育",
  "赵新宇\t生产二车间/A班\t操作工\t三级教育\t三级安全教育（车间级）\t车间级\t2026-03-03\t08:30\t11:30\t3\t3\t是\t是\t88\t80\t\t24\t20\t\t\t\t13:00-17:00\t车间级教育，上午培训下午上岗",
  "赵新宇\t生产二车间/A班\t操作工\t三级教育\t三级安全教育（班组级）\t班组级\t2026-03-04\t13:30\t16:30\t3\t3\t是\t是\t90\t80\t\t24\t20\t\t\t\t07:30-11:00\t班组级教育，师傅带班",
  "赵新宇\t生产二车间/A班\t操作工\t三级教育\t危化品应急处置\t\t2026-03-05\t09:00\t11:00\t2\t2\t是\t是\t85\t80\t\t24\t20\t\t\t\t13:00-17:00\t应急处置演练",
  "赵新宇\t生产二车间/A班\t操作工\t三级教育\t岗位操作规程\t\t2026-03-06\t08:30\t11:30\t3\t3\t是\t是\t90\t80\t\t24\t20\t\t\t\t13:00-17:00\t岗位操作规程学习",
  "孙立群\t设备动力部/机修班\t电工\t特种作业\t低压电工作业复审\t\t2026-03-09\t08:30\t12:00\t3.5\t3.5\t是\t是\t86\t80\t\t22\t20\t320101********1234\t2027-05-31\t低压电工作业复审;电气安全操作\t13:00-17:00\t特种作业操作证在有效期内",
  "孙立群\t设备动力部/机修班\t电工\t再教育\t电气安全操作\t\t2026-03-10\t08:30\t10:30\t2\t2\t是\t是\t90\t80\t\t22\t20\t320101********1234\t2027-05-31\t\t13:00-17:00\t年度再教育学时",
  "周敏华\t生产一车间/B班\t班长\t转岗\t转岗安全培训（反应釜岗）\t\t2026-03-11\t14:00\t17:00\t3\t3\t是\t是\t84\t80\t\t21\t20\t\t\t转岗安全培训\t\t由包装岗转反应釜岗",
  "吴建国\t仓储部/危化品库\t保管员\t复工\t复工安全教育\t\t2026-03-12\t08:30\t11:30\t3\t3\t是\t是\t88\t80\t\t23\t20\t\t\t复工安全教育\t13:00-17:00\t停工三个月后复工",
  "郑雅琴\t安环部\t安全员\t再教育\t安全生产法律法规再教育\t\t2026-03-13\t09:00\t12:00\t3\t3\t是\t是\t95\t80\t\t26\t20\t\t\t\t13:00-17:00\t安环部内部培训",
].join('\n');

const TOL = 0.01;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'name', 'dept', 'post', 'trainType', 'topic', 'date', 'startTime', 'endTime',
  'hours', 'planHours', 'signed', 'score', 'passLine', 'yearHours', 'minHours',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['name', '姓名'],
  ['dept', '部门/班组'],
  ['post', '岗位'],
  ['trainType', '培训类型'],
  ['topic', '培训主题'],
  ['date', '培训日期'],
  ['startTime', '开始时间'],
  ['endTime', '结束时间'],
  ['hours', '学时'],
  ['planHours', '计划学时'],
  ['signed', '是否签到'],
  ['score', '考核成绩'],
  ['passLine', '合格线'],
  ['yearHours', '年度累计学时'],
  ['minHours', '规定下限'],
];

// 数值列（用于「为负 / 无法解析」判定）
const NUM_FIELDS = [
  ['hours', '学时'],
  ['planHours', '计划学时'],
  ['yearHours', '年度累计学时'],
  ['minHours', '规定下限'],
  ['score', '考核成绩'],
  ['passLine', '合格线'],
  ['retakeScore', '补考成绩'],
];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过六次，见 tools/header_map_check.py）。
//    特别注意：规定下限 → 计划学时 → 年度累计学时 → 学时 这个具体度顺序，
//    「学时」这个词能匹配后面三列中的任意一列，必须放到最后。
const ROLES = {
  minHours: ['规定学时下限', '年度学时下限', '学时下限', '规定下限', '最低学时', '下限'],
  planHours: ['计划学时', '应训学时', '规定学时', '学时计划'],
  yearHours: ['年度累计学时', '全年累计学时', '累计学时', '年度学时'],
  hours: ['实际学时', '学时合计', '培训学时', '本次学时', '学时'],
  startTime: ['开始时间', '起始时间', '开始时刻', '上课时间'],
  endTime: ['结束时间', '终止时间', '结束时刻', '下课时间'],
  date: ['培训日期', '培训日', '日期'],
  name: ['姓名', '员工姓名', '受训人', '培训人员', '人员'],
  dept: ['部门/班组', '部门班组', '部门', '班组', '车间', '科室'],
  // ⚠️「岗位应训主题」必须排在「岗位」前面：后者的关键词是前者的子串，顺序一反，
  //    「岗位」会把「岗位应训主题」这一列抢走（本仓库踩过六次的同一个坑）。
  postTopics: ['岗位应训主题', '岗位所需培训主题', '应训主题', '岗位培训要求', '所需培训主题'],
  post: ['岗位', '工种', '职位'],
  trainType: ['培训类型', '培训类别', '教育类型', '培训种类', '类型'],
  topic: ['培训主题', '培训内容', '培训科目', '主题', '内容'],
  level: ['教育层级', '培训层级', '三级层级', '教育级别', '层级'],
  shouldAttend: ['是否应培训', '应培训名单', '应培训', '名单内', '应参训'],
  signed: ['是否签到', '签到状态', '签到情况', '已签到', '签到'],
  retakeScore: ['补考成绩', '复考成绩', '补考分数', '复试成绩'],
  passLine: ['合格线', '合格分数', '合格标准', '合格分值', '及格线', '及格分'],
  score: ['考核成绩', '考试成绩', '考核得分', '成绩', '得分', '分数'],
  certExpiry: ['证件到期日', '证书到期日', '证件有效期', '证书有效期', '有效期至', '到期日'],
  certNo: ['特种作业证号', '特种作业证编号', '证书编号', '证件编号', '作业证号', '证号'],
  attendance: ['出勤时间段', '考勤时间段', '出勤时段', '考勤记录', '出勤情况'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  name: '姓名',
  dept: '部门/班组',
  post: '岗位',
  trainType: '培训类型',
  topic: '培训主题',
  level: '教育层级',
  date: '培训日期',
  startTime: '开始时间',
  endTime: '结束时间',
  hours: '学时',
  planHours: '计划学时',
  shouldAttend: '是否应培训',
  signed: '是否签到',
  score: '考核成绩',
  passLine: '合格线',
  retakeScore: '补考成绩',
  yearHours: '年度累计学时',
  minHours: '规定下限',
  certNo: '特种作业证号',
  certExpiry: '证件到期日',
  postTopics: '岗位应训主题',
  attendance: '出勤时间段',
  note: '备注',
};

const SUM_ROLES = ['hours', 'planHours', 'yearHours'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「学时够」，也不说「学时不够」。',
  };
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|（空）|\(空\))$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

/** 解析成 {header, cols, items, totals, missingRoles, missingColumns, error}；行是**扁平**对象：{line, raw, 角色:值…} */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }

  const header = splitRow(rows[0].raw);
  const cols = header.map((h, k) => ({ header: h, role: roleOf(h), index: k }));
  const items = [];
  for (let r = 1; r < rows.length; r++) {
    const cells = splitRow(rows[r].raw);
    const it = { line: rows[r].line, raw: rows[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const num = (it, role) => {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
};

function who(it) {
  const name = String(it.name == null ? '' : it.name).trim();
  const dept = String(it.dept == null ? '' : it.dept).trim();
  const topic = String(it.topic == null ? '' : it.topic).trim();
  return `第 ${it.line} 行「${name || '未填姓名'}」${dept ? `（${dept}）` : ''}${topic ? `·${topic}` : ''}`;
}

function hhmm(min) {
  return `${String(Math.floor(min / 60)).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;
}

/** 时钟时间 → 当天分钟数；只认 8:30 / 08:30 / 08:30:00（全角冒号也算） */
function normClock(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/：/g, ':');
  if (s === '') return null;
  const m = /^(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?$/.exec(s);
  if (!m) return null;
  const h = Number(m[1]);
  const mi = Number(m[2]);
  if (h > 23 || mi > 59) return null;
  return h * 60 + mi;
}

/** 日期 → YYYY-MM-DD；只认 2026-03-02 / 2026/3/2 / 2026.3.2 / 20260302 / 2026年3月2日 */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[年月]/g, '-').replace(/日/g, '').replace(/[./]/g, '-');
  if (s === '') return null;
  let m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) m = /^(\d{4})(\d{2})(\d{2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  return `${y}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

/** 是 / 否 三态：认不出来一律 null（不猜） */
function tri(raw) {
  const s = String(raw == null ? '' : raw).trim().toLowerCase().replace(/[\s（()）]/g, '');
  if (s === '') return null;
  if (/^(是|已签到|已培训|y|yes|true|1|√|✓)$/.test(s)) return true;
  if (/^(否|未签到|未培训|n|no|false|0|x|×)$/.test(s)) return false;
  return null;
}

function finding(level, category, it, diff, message, advice) {
  const f = { level, category, line: it.line, message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/* ============================ 免费档检查（六项） ============================ */

/** 1. 学时勾稽：结束时间 − 开始时间 = 实际学时，与「学时」「计划学时」两列比对 */
function checkHoursReconcile(items) {
  const out = [];
  for (const it of items) {
    const st = normClock(it.startTime);
    const et = normClock(it.endTime);
    const h = normNumber(it.hours);
    const p = normNumber(it.planHours);
    const hOk = h !== null && h >= 0;
    const pOk = p !== null && p >= 0;

    if (st !== null && et !== null && et > st && hOk) {
      const computed = round2((et - st) / 60);
      if (Math.abs(h - computed) >= TOL) {
        out.push(finding('P1', '学时与起止时间不符', it, round2(h - computed),
          `${who(it)}：起止时间 ${hhmm(st)}–${hhmm(et)} 复算为 ${computed} 学时，`
          + `但「学时」列写的是 ${h} 学时，差 ${round2(Math.abs(h - computed))} 学时。`,
          '按签到表上的实际起止时间重算一遍：迟到、中途离场、课间休息算不算学时，'
          + '要按本单位培训管理办法统一口径，别一个班次一个算法。'));
      }
    }

    if (hOk && pOk && Math.abs(h - p) >= TOL) {
      const short = h < p;
      out.push(finding(short ? 'P0' : 'P2', '学时与计划学时不符', it, round2(h - p),
        `${who(it)}：计划学时 ${p}，实际学时 ${h} —— ${short
          ? `少 ${round2(p - h)} 学时，未达到计划`
          : `多 ${round2(h - p)} 学时`}。`,
        short
          ? '学时不足的班次要么补训补齐（并留下补训签到与考核记录），要么在「备注」写明减免依据；'
            + '检查时「签到有、学时不够」是要现场解释的。'
          : '实际学时多于计划，一般是把签到等待、课间休息也算进去了，按管理办法口径修正。'));
    }
  }
  return out;
}

/** 2. 再教育学时达标：每人的 年度累计学时 ≥ 规定下限（不达标点名到人，一人只报一次） */
function checkYearHoursFloor(items) {
  const out = [];
  const seen = new Set();
  for (const it of items) {
    const y = normNumber(it.yearHours);
    const lo = normNumber(it.minHours);
    if (y === null || lo === null) continue;
    if (y < 0 || lo < 0) continue;                     // 交给「数值为负」那一项
    if (y >= lo - TOL) continue;
    const name = String(it.name == null ? '' : it.name).trim() || `第 ${it.line} 行的受训人`;
    if (seen.has(name)) continue;
    seen.add(name);
    out.push(finding('P0', '年度累计学时不达标', it, round2(y - lo),
      `${who(it)}：年度累计学时 ${y} 学时 < 规定下限 ${lo} 学时，差 ${round2(lo - y)} 学时`
      + `（培训类型：${String(it.trainType == null ? '' : it.trainType).trim() || '未填'}）。`,
      '把这个人本年度已完成的培训逐条累加核对：有没有只登了签到没登学时、有没有把半天当 8 学时；'
      + '缺的学时要在年度结束前安排补训并留下签到与考核记录。本工具按你表里的下限比对，不判定法定学时。'));
  }
  return out;
}

/** 3. 应培训人员覆盖：应培训名单 vs 签到名单（未签到 / 名单外多签到） */
function checkRosterSignIn(items) {
  const out = [];
  for (const it of items) {
    const should = tri(it.shouldAttend);
    const signed = tri(it.signed);
    if (signed === false && should !== false) {
      out.push(finding('P0', '应培训未签到', it, undefined,
        `${who(it)}：这条记录在应培训名单里（「是否应培训」=${String(it.shouldAttend == null ? '' : it.shouldAttend).trim() || '未填，按应培训处理'}），`
        + '但「是否签到」是"否" —— 未签到。',
        '未签到的培训不算完成：要么补签（并在备注说明原因），要么重新安排一次培训并留签到表；'
        + '检查时「名单上有人、签到表上没名字」是要现场解释的。'));
    }
    if (signed === true && should === false) {
      out.push(finding('P1', '名单外多签到', it, undefined,
        `${who(it)}：「是否应培训」是"否"，但「是否签到」是"是" —— 这条培训不在应培训名单里，却签到了。`,
        '核对是名单漏登记了这人，还是签到表上多写了名字（代签、串签）。两种都要更正，不能两头都留着。'));
    }
  }
  return out;
}

/** 4. 同一人 + 同一培训主题 + 同一培训日期 重复登记 */
function checkDuplicateRecords(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const name = String(it.name == null ? '' : it.name).trim();
    const topic = String(it.topic == null ? '' : it.topic).trim();
    const d = normDate(it.date) || String(it.date == null ? '' : it.date).trim();
    if (!name || !topic || !d) continue;
    const key = `${name}|${topic}|${d}`;
    if (seen.has(key)) {
      out.push(finding('P0', '同一人同主题同日期重复登记', it, undefined,
        `${who(it)}：「${name}」的「${topic}」在第 ${seen.get(key)} 行（同一天 ${d}）已经登记过一次 —— `
        + '同一人 + 同一培训主题 + 同一培训日期重复。',
        '一个人在同一天同一主题只应有一条记录：重复登记会让年度学时被重复累加（学时虚高），'
        + '现场检查时也解释不清。合并成一条，并在「备注」写清上下午班的实际时段。'));
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** 5. 考核成绩与合格线（含补考记录缺失） */
function checkScoreVsPassLine(items) {
  const out = [];
  for (const it of items) {
    const s = normNumber(it.score);
    const p = normNumber(it.passLine);
    if (s === null || p === null) continue;
    if (s < 0 || p < 0) continue;                      // 交给「数值为负」那一项
    if (s >= p - TOL) continue;
    // 「空着」与「写了但看不懂」要分开：空着才算缺补考记录，看不懂已经由「数值无法解析」点名
    const retakeRaw = it.retakeScore;
    const retake = normNumber(retakeRaw);
    const retakeBlank = isBlank(retakeRaw);
    out.push(finding('P0', '考核成绩低于合格线', it, round2(s - p),
      `${who(it)}：考核成绩 ${s} 分 < 合格线 ${p} 分，差 ${round2(p - s)} 分`
      + `（${retakeBlank ? '本行没有补考成绩'
        : retake === null ? `补考成绩「${String(retakeRaw).trim()}」不是可识别的分数`
          : `补考成绩已登记：${retake} 分`}）。`,
      '不合格的人要有补考安排与补考成绩；补考仍不合格的按制度重新培训。'
      + '本工具只做分数比对，不判定这个人能不能上岗。'));
    if (retakeBlank) {
      out.push(finding('P1', '补考记录缺失', it, undefined,
        `${who(it)}：考核不合格（${s} 分 < 合格线 ${p} 分），但补考成绩一栏是空的 —— 缺补考记录。`,
        '在「补考成绩」列登记补考分数与日期（或在「备注」写明补考安排）；'
        + '只有"不合格"没有"补考"，是安全培训档案里最常见的缺口。'));
    }
  }
  return out;
}

/** 6. 空白 / 占位符 / 时间与日期格式 / 负学时 / 数值无法解析 */
function checkFieldIntegrity(items) {
  const out = [];
  for (const it of items) {
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的格子会让对应的核对整项做不了；补全后再跑，本工具不会替你猜一个默认值（也不会把空格当 0）。'));
    }

    for (const [role, label] of NUM_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值无法解析', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字（只认数字、千分位、括号负数、百分号）。`,
          '把这一格改成纯数字形态（如 3.5、90）再跑；本工具不会把看不懂的值当成 0。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', (role === 'hours' || role === 'planHours') ? '学时为负' : '数值为负', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 培训台账里出现负学时，通常是把起止时间填反了，`
          + '或把红字冲销写进了学时列。',
          '核对签到表上的实际起止时间；确属冲销的请写在「备注」里并保留原值，不要直接改成正数把负数抹掉。'));
      }
    }

    if (!isBlank(it.startTime) && normClock(it.startTime) === null) {
      out.push(finding('P1', '时间格式不合法', it, undefined,
        `${who(it)}：「开始时间」的值「${String(it.startTime).trim()}」不是可识别的时间（只认 8:30 / 08:30 / 08:30:00）。`,
        '把开始时间改成 24 小时制的 HH:MM（Excel 里时间列常被写成 8.30 或"上午8点半"，都算不出来）。'));
    }
    if (!isBlank(it.endTime) && normClock(it.endTime) === null) {
      out.push(finding('P1', '时间格式不合法', it, undefined,
        `${who(it)}：「结束时间」的值「${String(it.endTime).trim()}」不是可识别的时间（只认 8:30 / 08:30 / 08:30:00）。`,
        '把结束时间改成 24 小时制的 HH:MM。'));
    }
    const st = normClock(it.startTime);
    const et = normClock(it.endTime);
    if (st !== null && et !== null && et <= st) {
      out.push(finding('P1', '时间区间不成立', it, undefined,
        `${who(it)}：结束时间 ${hhmm(et)} 不晚于开始时间 ${hhmm(st)} —— 起止时间填反了，或跨天夜班没写清。`,
        '先确认是不是填反了；确实是跨零点夜班的，请在「备注」注明"次日"，并按管理办法口径计算学时。'));
    }

    if (!isBlank(it.date) && normDate(it.date) === null) {
      out.push(finding('P1', '日期格式不合法', it, undefined,
        `${who(it)}：「培训日期」的值「${String(it.date).trim()}」不是可识别的日期`
        + '（只认 2026-03-02 / 2026/3/2 / 20260302 / 2026年3月2日）。',
        '把培训日期统一成 YYYY-MM-DD；日期写成"3月2日"这类文本，重复登记检测会失效（同一天被当成两天）。'));
    }
  }
  return out;
}

/* ============================ 完整档（付费）追加的检查 ============================ */
/* 说明：下面这些函数整体属于完整档能力；免费包由 tools/strip_free_engine.py 从本文件摘出时，
   它们会因为「入口里那个开关关掉之后没人再引用」被整块删掉，不会留在免费包里。 */

/** 三级安全教育的三个层级（新员工三条都要有） */
/** 三级安全教育的层级（先认「教育层级」列，列里没写就从培训主题里认） */
/** 完整档：三级教育层级完整性（新员工必须同时有 厂级 / 车间级 / 班组级） */
/** 完整档：特种作业证有效期覆盖（培训 / 作业日期 不得晚于 证件到期日） */
/** 完整档：培训内容与岗位风险匹配（按「岗位应训主题」清单逐项检查该人缺不缺） */
/** 完整档：培训记录与工资 / 考勤时间冲突（培训时间段 与 出勤时间段 重叠） */
/** 完整档：单人当行的未达标项（汇总清单与整改清单都用它，口径只有这一处） */
/** 完整档：分部门 × 分培训类型汇总清单（按未达标人数从多到少排序，每行带可整改动作） */
/** 完整档：整改清单（P0 在前，再按行号），带部门 / 类型 / 责任人定位 */
/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  const about = '一张含表头的安全教育培训与签到台账';
  const needCols = REQUIRED_ROLES.map((r) => LABELS[r]).join('」「');
  if (!String(text).trim()) {
    return insufficient([`原文（text）：${about}（至少要能认出「${needCols}」）`]);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient([`原文（text）：${about}（至少要能认出「${needCols}」）`]);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `${about}（至少要能认出「${needCols}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行培训明细（现在只有表头，没有可核对的记录行）']);
  }

  const findings = [];
  const notRun = [];
  const notes = [];

  for (const f of checkHoursReconcile(t.items)) findings.push(f);
  for (const f of checkYearHoursFloor(t.items)) findings.push(f);
  for (const f of checkRosterSignIn(t.items)) findings.push(f);
  for (const f of checkDuplicateRecords(t.items)) findings.push(f);
  for (const f of checkScoreVsPassLine(t.items)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  if (!t.cols.some((c) => c.role === 'shouldAttend')) {
    notes.push('本表没有「是否应培训」列：只能判「应培训未签到」，判不了「名单外多签到」；'
      + '没做的这一半如实记下来，不会用默认值补上。');
  }

  let extra = null;
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const names = new Set();
  for (const it of t.items) {
    const n = String(it.name == null ? '' : it.name).trim();
    if (n) names.add(n);
  }
  const hoursTotal = t.totals.hours;
  const planHoursTotal = t.totals.planHours;

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      people: names.size,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      hours_total: hoursTotal,
      plan_hours_total: planHoursTotal,
      hours_diff: round2(hoursTotal - planHoursTotal),
      basis: '实际学时 = 结束时间 − 开始时间，逐行复算，并与「学时」「计划学时」两列比对；'
        + '每人的 年度累计学时 不得低于「规定下限」；「是否应培训」为是而「是否签到」为否即未签到、'
        + '应培训为否却签到即名单外多签到；同一人 + 同一主题 + 同一日期只应有两条以内的记录（重复即报）；'
        + '考核成绩不得低于合格线，不合格必须能看到补考记录；关键字段空白 / 占位符、时间与日期格式不合法、'
        + '数值无法解析或为负一律逐行点名。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (notes.length) result.notes = notes;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对、名单与成绩对得上**，'
      + '不代表培训真实发生过、培训内容专业上充分，也不代表法定学时与上岗资格已经过关 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    people: names.size,
    columns_recognized: t.cols.filter((c) => c.role).length,
    hours_total: hoursTotal,
    plan_hours_total: planHoursTotal,
    hours_diff: round2(hoursTotal - planHoursTotal),
    roster_known: t.cols.some((c) => c.role === 'shouldAttend'),
  };
  result.scope = scope;



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
