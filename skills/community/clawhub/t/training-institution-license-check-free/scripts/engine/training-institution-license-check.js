#!/usr/bin/env node
/**
 * training-institution-license-check.js —— 校外培训机构资质与教师备案核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点："双减"之后，校外培训机构必须**证照齐全（办学许可证 / 营业执照）、教师持证并备案、
 *   收费进监管账户、培训时段合规**；缺一项就停业整改。校区**每月自查**＋**教育局年检**都要交这本台账：
 *   ① 证照有效期：办学许可证与营业执照的到期日必须覆盖本次核对基准日，超期就是无证办学；
 *   ② 教师持证与备案：教师资格证号要有、资格证要在有效期内、教师要在教育局备案（点人查，不查"平均"）；
 *   ③ 收费监管：学费必须进备案的监管账户，收款账户与备案监管账户不一致就是**账外收费**（年检直接扣分项）；
 *   ④ 台账唯一性：同一教师重复登记、同一个资格证号挂在两个主体名下，都会让"谁在教、教几节"算不清；
 *   ⑤ 合计行：教师数 / 班级数 / 课时数的合计必须等于明细行加总；
 *   ⑥ 字段合法性：日期格式、课时为负或为零、必需字段缺失、备案状态 / 科目类别 / 培训时段取值非法。
 *   核错一项，轻则整改停课，重则**停业整顿 + 退费** —— 所以每条结论都必须能拿原文复算。
 *
 * 本文件同时服务**完整档（买断版）**与**免费档**两个包：
 *   · 完整档执行全部检查项（免费六项 + 追加五项）；
 *   · 免费档只执行免费六项。追加项的实现在免费包里被 `tools/strip_free_engine.py` 整块摘除，
 *     免费包的 `CHECKS_WITHHELD` 里只剩**说明文本**，不是实现。
 *
 * ⚠️ 本文件是 **免费档子集**：只实现下面这六项**表内逐行算术与台账勾稽**：
 *     ① 证照有效期覆盖；② 教师持证与备案覆盖；③ 收费是否进监管账户；
 *     ④ 同一教师重复登记 / 同一教师资格证号出现在两个主体；⑤ 合计行逐列复核（教师数 / 班级数 / 课时数）；
 *     ⑥ 空白占位符与字段合法性（必需字段缺失、日期格式非法、课时为负或为零、备案状态 / 科目类别 /
 *        培训时段取值非法）。
 *    **完整档（付费）的实现不在这个包里** —— "双减"时段冲突、收费期与课时消耗不匹配、超班额、
 *    跨校区教师共用冲突、分校区 × 分学科汇总清单都不在这里。
 *    `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定机构该不该办学 / 该发什么许可、不判定证件真伪、不判定当地校历的寒暑假与调休、
 *          不读 .xlsx / .pdf 原件、不联网核验证照与监管账户；材料不足**一律不给结论**。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '证照有效期覆盖（办学许可证到期日与营业执照到期日都要 ≥ 核对基准日；超期逐条给出已超期天数）',
  '教师持证与备案覆盖（缺教师资格证号 / 资格证过期 / 未备案逐人点名）',
  '收费是否进监管账户（收款账户与备案监管账户不一致即报，逐条给出两个字面账户）',
  '同一教师重复登记 / 同一教师资格证号出现在两个主体（重复登记与跨主体同名证号都要点名）',
  '合计行逐列复核（数量类列：教师数、班级数、课时数）',
  '空白占位符与字段合法性（必需字段缺失、日期格式非法、课时为负或为零、备案状态 / 科目类别取值非法、培训时段格式非法）',
];

const CHECKS_WITHHELD = [
  '培训时段与"双减"时段限制冲突（学科类不得在法定节假日 / 休息日 / 寒暑假窗口开展，按排课表逐条判）',
  '收费期与课时消耗不匹配（一次收费超 3 个月或超 60 课时、消课数超过收费课时、收费课时与台账课时不符，跨表比对）',
  '班级备案人数与实际报名人数超限（超班额；同一班级的班额口径不一致也点名）',
  '跨校区教师共用冲突（同一教师同一时段在两个校区排课）',
  '分校区 × 分学科的汇总清单（按问题数降序 + 每组一条可整改动作，落在 result.rollup）',
];

const OUT_OF_SCOPE = [
  '判定这家机构到底该不该办学、该办哪类许可、办学许可证与营业执照该不该换发（那是教育行政部门与市场监管部门的认定权，本工具只核台账里的到期日有没有覆盖核对基准日）',
  '判定教师资格证本身的真伪、教师是否具备相应学科的任教资格（那是发证机关与教育局的认定权，本工具只核证号 / 到期日 / 备案状态的字面一致性）',
  '判定"双减"口径下某个具体日期在当地算不算寒暑假 / 节假日、要不要调休（本工具只按内置的一份 2026 年口径点名，最终以当地教育局公告与校历为准）',
  '判定收费金额本身是否合理、监管账户里的钱有没有被挪用（本工具只核台账与排课 / 收费记录的字面一致性）',
  '读取 .xlsx / .pdf 原件、联网核验办学许可证 / 营业执照 / 教师资格证 / 监管账户的真伪，替代教育局年检与资金监管部门的认定',
];

// 样例：一本**干净**的校外培训机构资质与教师备案台账（3 个校区 / 6 名教师 / 6 个班级，基准日 2026-03-31），
// 加上一段 `--- 排课与收费记录 ---`：证照与资格证都在有效期内、教师都已备案、收费都进了备案监管账户、
// 台账无重复、合计行与明细一致、学科类都排在周中（非学科类排在周末属允许情形）、
// 收费期都在 3 个月内且课时不超过 60、收费课时与台账课时一致、无跨校区同时段排课。**全表零命中**。
const SAMPLE_HEAD = '校区名称\t办学许可证号\t许可证到期日\t营业执照号\t营业执照到期日\t教师姓名\t教师资格证号\t教师资格证到期日\t备案状态\t任教科目\t科目类别\t班级名称\t报名人数\t班额上限\t收费标准(元/课时)\t收费金额(元)\t课时数\t培训时段\t收款账户\t监管账户\t核对基准日\t教师数\t班级数\t备注';
const SAMPLE_ROWS = [
  '城东校区\t教民1320506700001\t2028-06-30\t91320506XAMPLE01XA\t2030-06-30\t张淑芬\t320101********1234\t2029-08-31\t已备案\t语文\t学科类\t初一语文A班\t32\t40\t120\t5,760\t48\t2026-03-03 18:30-20:00\t苏州银行监管专户6201\t苏州银行监管专户6201\t2026-03-31\t1\t1\t证照齐全',
  '城东校区\t教民1320506700001\t2028-06-30\t91320506XAMPLE01XA\t2030-06-30\t李国强\t320102********5678\t2028-12-31\t已备案\t数学\t学科类\t初二数学B班\t28\t36\t130\t4,160\t32\t2026-03-04 18:30-20:00\t苏州银行监管专户6201\t苏州银行监管专户6201\t2026-03-31\t1\t1\t证照齐全',
  '城东校区\t教民1320506700001\t2028-06-30\t91320506XAMPLE01XA\t2030-06-30\t王海燕\t320103********9012\t2029-05-31\t已备案\t英语\t学科类\t初三英语C班\t24\t30\t140\t8,400\t60\t2026-03-05 19:00-20:30\t苏州银行监管专户6201\t苏州银行监管专户6201\t2026-03-31\t1\t1\t一次收费 60 课时为上限',
  '城西校区\t教民1320506800002\t2027-12-31\t91320508XAMPLE02XB\t2029-12-31\t陈晓东\t320104********3456\t2027-10-31\t已备案\t美术\t非学科类\t少儿美术D班\t18\t25\t90\t2,160\t24\t2026-03-07 09:00-10:30\t苏州银行监管专户6202\t苏州银行监管专户6202\t2026-03-31\t1\t1\t非学科类可排周末',
  '城西校区\t教民1320506800002\t2027-12-31\t91320508XAMPLE02XB\t2029-12-31\t赵敏\t320105********7890\t2028-03-31\t已备案\t书法\t非学科类\t硬笔书法E班\t16\t24\t80\t1,920\t24\t2026-03-08 14:00-15:30\t苏州银行监管专户6202\t苏州银行监管专户6202\t2026-03-31\t1\t1\t非学科类可排周末',
  '城南校区\t教民1320506900003\t2029-03-31\t91320509XAMPLE03XC\t2030-09-30\t周文涛\t320106********2345\t2029-06-30\t已备案\t物理\t学科类\t高一物理F班\t22\t30\t150\t4,500\t30\t2026-03-06 18:00-19:30\t苏州银行监管专户6203\t苏州银行监管专户6203\t2026-03-31\t1\t1\t证照齐全',
];
const SAMPLE_TOTAL = ['合计']
  .concat(new Array(15).fill('—'))
  .concat(['218'])
  .concat(new Array(4).fill('—'))
  .concat(['6', '6', '6 名教师、6 个班级、218 课时由明细行加总'])
  .join('\t');
const SECTION_NAME = '--- 排课与收费记录 ---';
const SECTION_HEAD = '校区名称\t班级名称\t教师姓名\t任教科目\t科目类别\t培训时段\t收费日期\t收费起始日\t收费截止日\t收费金额(元)\t收费课时\t已消课时';
const SECTION_ROWS = [
  '城东校区\t初一语文A班\t张淑芬\t语文\t学科类\t2026-03-03 18:30-20:00\t2026-03-01\t2026-03-01\t2026-03-31\t5,760\t48\t48',
  '城东校区\t初二数学B班\t李国强\t数学\t学科类\t2026-03-04 18:30-20:00\t2026-03-01\t2026-03-01\t2026-03-31\t4,160\t32\t32',
  '城东校区\t初三英语C班\t王海燕\t英语\t学科类\t2026-03-05 19:00-20:30\t2026-03-01\t2026-03-01\t2026-03-31\t8,400\t60\t60',
  '城西校区\t少儿美术D班\t陈晓东\t美术\t非学科类\t2026-03-07 09:00-10:30\t2026-03-01\t2026-03-01\t2026-04-30\t2,160\t24\t24',
  '城西校区\t硬笔书法E班\t赵敏\t书法\t非学科类\t2026-03-08 14:00-15:30\t2026-03-01\t2026-03-01\t2026-04-30\t1,920\t24\t24',
  '城南校区\t高一物理F班\t周文涛\t物理\t学科类\t2026-03-06 18:00-19:30\t2026-03-01\t2026-03-01\t2026-03-31\t4,500\t30\t30',
];
const SAMPLE_TEXT = [SAMPLE_HEAD]
  .concat(SAMPLE_ROWS)
  .concat([SAMPLE_TOTAL, SECTION_NAME, SECTION_HEAD])
  .concat(SECTION_ROWS)
  .join('\n');

const TOL = 0.01;

// 表头级必需列（缺任一列 ⇒ 材料不足，**绝不给结论**）
const REQUIRED_ROLES = [
  'campusName', 'licenseNo', 'licenseExpiry', 'bizLicenseNo', 'bizExpiry',
  'teacher', 'teacherCertNo', 'filingStatus', 'subject', 'className',
  'enrollCount', 'classCap', 'feeStandard', 'feeAmount', 'hours', 'timeSlot',
  'receiptAccount', 'superviseAccount', 'baseDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['campusName', '校区名称'],
  ['licenseNo', '办学许可证号'],
  ['licenseExpiry', '许可证到期日'],
  ['bizLicenseNo', '营业执照号'],
  ['bizExpiry', '营业执照到期日'],
  ['teacher', '教师姓名'],
  ['teacherCertNo', '教师资格证号'],
  ['teacherCertExpiry', '教师资格证到期日'],
  ['filingStatus', '备案状态'],
  ['subject', '任教科目'],
  ['className', '班级名称'],
  ['enrollCount', '报名人数'],
  ['classCap', '班额上限'],
  ['feeStandard', '收费标准'],
  ['feeAmount', '收费金额'],
  ['hours', '课时数'],
  ['timeSlot', '培训时段'],
  ['receiptAccount', '收款账户'],
  ['superviseAccount', '监管账户'],
  ['baseDate', '核对基准日'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['licenseExpiry', '许可证到期日'],
  ['bizExpiry', '营业执照到期日'],
  ['teacherCertExpiry', '教师资格证到期日'],
  ['baseDate', '核对基准日'],
];

// 数值列（为负 / 无法解析逐格点名）
const NUMBER_FIELDS = [
  ['enrollCount', '报名人数'],
  ['classCap', '班额上限'],
  ['feeStandard', '收费标准'],
  ['feeAmount', '收费金额'],
  ['hours', '课时数'],
  ['teacherCount', '教师数'],
  ['classCount', '班级数'],
];

// 等于 0 也非法的列（课时数为零 ⇒ 收了一笔没有课时的钱）
const ZERO_INVALID_ROLES = ['hours'];

// 备案状态只认这两个值（"双减"后的台账口径：要么已备案，要么未备案）
const FILING_STATUSES = ['已备案', '未备案'];
// 科目类别只认这两个值（决定"双减"时段限制是否适用）
const SUBJECT_CATEGORIES = ['学科类', '非学科类'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位：许可证到期日 / 营业执照到期日 / 教师资格证到期日 必须排在各自的"证件号"之前；
//    教师数 必须排在 教师姓名 之前；班级数 必须排在 班级名称 之前；
//    科目类别 必须排在 任教科目 之前；收费日期 / 收费起始日 / 收费截止日 / 收费课时 / 已消课时
//    必须排在"收费金额"与"课时数"这类宽泛词之前；兜底的 '科目' '班级' 只能放在最后。
const ROLES = {
  campusName: ['校区名称', '校区', '教学点', '办学点'],
  licenseExpiry: ['办学许可证到期日', '办学许可证有效期至', '许可证到期日', '许可证有效期至', '办学许可证有效期', '许可证有效期'],
  licenseNo: ['办学许可证号', '办学许可证编号', '许可证号', '许可证编号'],
  bizExpiry: ['营业执照到期日', '营业执照有效期至', '营业执照有效期'],
  bizLicenseNo: ['营业执照号', '营业执照编号', '营业执照注册号', '统一社会信用代码', '注册号'],
  teacherCertExpiry: ['教师资格证到期日', '教师资格证有效期至', '教师资格证有效期', '教师证到期日'],
  teacherCertNo: ['教师资格证号', '教师资格证编号', '教师证号', '资格证号'],
  teacherCount: ['教师数', '教师人数'],
  teacher: ['教师姓名', '授课教师', '任课教师', '任职教师'],
  filingStatus: ['备案状态', '备案情况', '备案结果'],
  classCount: ['班级数', '班级数量', '班数'],
  className: ['班级名称', '班次名称', '教学班名称', '班级'],
  enrollCount: ['报名人数', '实际报名人数', '在读人数', '招生人数'],
  classCap: ['班额上限', '班级备案人数', '备案人数', '班额'],
  subjectCategory: ['科目类别', '学科类别', '课程类别', '培训类别', '是否学科类'],
  subject: ['任教科目', '授课科目', '科目名称', '学科', '科目'],
  feeStandard: ['收费标准', '课时单价', '单价'],
  feeDate: ['收费日期', '缴费日期', '收款日期'],
  feeStart: ['收费起始日', '收费开始日期', '收费起日'],
  feeEnd: ['收费截止日', '收费结束日期', '收费止日'],
  paidHours: ['收费课时', '购买课时', '收费课次'],
  consumedHours: ['已消课时', '消耗课时', '已消耗课时', '消课课时'],
  feeAmount: ['收费金额', '实收金额', '收费总额', '金额'],
  hours: ['课时数', '课时', '课次'],
  timeSlot: ['培训时段', '上课时段', '授课时段', '培训时间', '排课时段', '时段'],
  receiptAccount: ['收款账户', '收款账号', '实际收款账户', '收款户名'],
  superviseAccount: ['监管账户', '监管账号', '备案监管账户', '资金监管账户'],
  baseDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  note: ['备注', '说明'],
};

const LABELS = {
  campusName: '校区名称',
  licenseNo: '办学许可证号',
  licenseExpiry: '许可证到期日',
  bizLicenseNo: '营业执照号',
  bizExpiry: '营业执照到期日',
  teacher: '教师姓名',
  teacherCertNo: '教师资格证号',
  teacherCertExpiry: '教师资格证到期日',
  filingStatus: '备案状态',
  subject: '任教科目',
  subjectCategory: '科目类别',
  className: '班级名称',
  enrollCount: '报名人数',
  classCap: '班额上限',
  feeStandard: '收费标准',
  feeAmount: '收费金额',
  hours: '课时数',
  timeSlot: '培训时段',
  receiptAccount: '收款账户',
  superviseAccount: '监管账户',
  baseDate: '核对基准日',
  teacherCount: '教师数',
  classCount: '班级数',
  note: '备注',
  feeDate: '收费日期',
  feeStart: '收费起始日',
  feeEnd: '收费截止日',
  paidHours: '收费课时',
  consumedHours: '已消课时',
};

const SUM_ROLES = ['teacherCount', 'classCount', 'hours'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「证照在有效期内」，也不说「超期」。',
  };
}

/** 全角数字 / 全角标点归一成半角（台账从 Excel / 微信里复制出来常常是全角） */
function toHalfWidth(raw) {
  if (raw === undefined || raw === null) return '';
  return String(raw)
    .replace(/[\uFF10-\uFF19]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/\uFF0E/g, '.').replace(/\uFF0D/g, '-').replace(/\uFF0B/g, '+')
    .replace(/\uFF0C/g, ',').replace(/\uFF05/g, '%').replace(/\uFF1A/g, ':')
    .replace(/\uFF08/g, '(').replace(/\uFF09/g, ')');
}

/** 数字：认千分位（1,200）、货币符号、全角数字、括号负数；认不出来返回 null */
function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalfWidth(raw).trim().replace(/[¥￥,\s]/g, '');
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核|未填)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = toHalfWidth(raw).trim();
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  s = s.replace(/[年月]/g, '-').replace(/日/g, '').replace(/[.／/]/g, '-').replace(/\s+/g, '');
  if (/^\d{8}$/.test(s)) s = s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8);
  const m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const dt = new Date(Date.UTC(y, mo - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
  return m[1] + '-' + String(mo).padStart(2, '0') + '-' + String(d).padStart(2, '0');
}

const DAY_MS = 86400000;
function dayNum(iso) {
  const p = iso.split('-').map(Number);
  return Date.UTC(p[0], p[1] - 1, p[2]) / DAY_MS;
}
/** b − a（整天数，正数表示 b 在 a 之后） */
function daysBetween(a, b) {
  return dayNum(b) - dayNum(a);
}
/** 日期 + 月数（按自然月加，目标月没有那一天就退到当月最后一天） */
const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = toHalfWidth(header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/** 合计行不是明细：逐行检查要跳过它，只有「合计行逐列复核」那一项会用到它 */
function isTotalRow(it) {
  const campus = String(it.campusName == null ? '' : it.campusName).trim();
  const cls = String(it.className == null ? '' : it.className).trim();
  return TOTAL_LABEL.test(campus) || TOTAL_LABEL.test(cls);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到 `--- 段名 ---` 就停（后面是另一张表）。
 */
function parseTable(text) {
  const rawLines = String(text == null ? '' : text).split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < rawLines.length; i++) {
    if (isSectionMarker(rawLines[i])) break;
    if (String(rawLines[i]).trim() === '') continue;
    rows.push({ line: i + 1, raw: String(rawLines[i]) });
  }
  if (!rows.length) {
    return {
      error: 'empty', header: [], cols: [], items: [], detail: [], totalRows: [], totals: {},
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
    it.isTotal = isTotalRow(it);
    items.push(it);
  }

  const missingRoles = REQUIRED_ROLES.filter((r) => !cols.some((c) => c.role === r));
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(detail.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return {
    error: missingRoles.length ? 'no_header' : null,
    header,
    cols,
    items,
    detail,
    totalRows,
    totals,
    missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  };
}

const cell = (it, role) => String(it[role] == null ? '' : it[role]).trim();

function who(it) {
  const campus = cell(it, 'campusName');
  const teacher = cell(it, 'teacher');
  const cls = cell(it, 'className');
  const head = [campus, teacher, cls].filter(Boolean).join(' / ');
  return `第 ${it.line} 行「${head || '未命名记录'}」`;
}

/** 每条结论都带原文依据：行号 + 校区 / 教师 / 班级 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    campus_name: cell(it, 'campusName'),
    teacher: cell(it, 'teacher'),
    class_name: cell(it, 'className'),
    subject: cell(it, 'subject'),
    evidence: String(it.raw == null ? '' : it.raw).slice(0, 200),
    message,
  };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

/** 台账里第一个能认出来的核对基准日（逐行没填时兜底；逐行填了就以逐行为准） */
function baseDateOf(items) {
  for (const it of items) {
    const d = normDate(it.baseDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.baseDate) || base;

/** 账户名归一化：去空白 / 全角标点与常见分隔符后再比字面 */
function normAccount(raw) {
  return toHalfWidth(raw).replace(/[\s\u3000]/g, '').replace(/[()（）【】\[\]·．.、,，:：;；]/g, '');
}

/** 培训时段：`YYYY-MM-DD HH:MM-HH:MM` 才算合法；认不出来返回 null（不参与任何时段推断） */
const SLOT_RE = /^(\d{4}-\d{1,2}-\d{1,2})\s+(\d{1,2}:\d{2})\s*[-~—～至]\s*(\d{1,2}:\d{2})$/;
function parseSlot(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalfWidth(raw).trim().replace(/\s+/g, ' ');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const m = SLOT_RE.exec(s);
  if (!m) return null;
  const date = normDate(m[1]);
  if (!date) return null;
  const mins = (t) => {
    const p = t.split(':');
    const h = Number(p[0]);
    const mi = Number(p[1]);
    if (!Number.isFinite(h) || !Number.isFinite(mi) || h > 23 || mi > 59) return null;
    return h * 60 + mi;
  };
  const a = mins(m[2]);
  const b = mins(m[3]);
  if (a === null || b === null || b <= a) return null;
  const hhmm = (n) => String(Math.floor(n / 60)).padStart(2, '0') + ':' + String(n % 60).padStart(2, '0');
  return { date, start: hhmm(a), end: hhmm(b), key: date + ' ' + hhmm(a) + '-' + hhmm(b) };
}

/** 周六 / 周日 */
/** 内置法定节假日窗口 */
/** 内置寒暑假窗口（按月日比） */
/* ============================ 免费档检查（六项） ============================ */

function checkLicenseValidity(items, base) {
  // ① 证照有效期覆盖：核对基准日 ≤ 办学许可证到期日、且 ≤ 营业执照到期日；超期逐条给天数
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const b = baseOf(it, base);
    if (!b) continue;                                  // 基准日缺失交给第 ⑥ 项点名
    const pairs = [
      ['licenseExpiry', '办学许可证', '办学许可证超期', '办学许可证'],
      ['bizExpiry', '营业执照', '营业执照超期', '营业执照'],
    ];
    for (const [role, doc, category, short] of pairs) {
      const raw = it[role];
      if (isBlank(raw)) continue;                      // 空着 ⇒ 判不了覆盖，交给第 ⑥ 项点名
      const d = normDate(raw);
      if (!d) continue;                                // 格式非法 ⇒ 交给第 ⑥ 项点名
      const over = daysBetween(d, b);
      if (over <= 0) continue;
      out.push(finding('P0', category, it, over,
        `${who(it)}：${doc}到期日 ${d}，早于核对基准日 ${b}，**已超期 ${over} 天**`
        + `（校区 ${cell(it, 'campusName') || '(未填)'}，${short}号 ${cell(it, role === 'licenseExpiry' ? 'licenseNo' : 'bizLicenseNo') || '(未填)'}）。`,
        `${short}到期未换发等于这段期间处于**无证办学**状态：先去审批机关换发（换发期间按当地要求停课），`
        + `换发后把新到期日填回台账再重跑。别只把台账日期往后改。`));
    }
  }
  return out;
}

function checkTeacherFiling(items, base) {
  // ② 教师持证与备案：教师资格证号要有、资格证到期日要覆盖核对基准日、备案状态必须"已备案"
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const b = baseOf(it, base);

    const no = cell(it, 'teacherCertNo');
    const exp = cell(it, 'teacherCertExpiry');
    if (!no || isBlank(exp)) {
      out.push(finding('P0', '教师资格证缺失或过期', it, undefined,
        `${who(it)}：${!no ? '教师资格证号是空的' : '教师资格证号 ' + no + ' 的到期日没填'}`
        + '—— 无证上岗是"双减"后校外培训的**直接处罚项**（任教科目 '
        + `${cell(it, 'subject') || '(未填)'}）。`,
        '把每位任课教师的姓名、教师资格证号与证件到期日逐行补进台账；'
        + '资格证在总校 / 别处的也必须能在这本台账里点到人。'));
    } else {
      const d = normDate(exp);
      if (d && b && daysBetween(d, b) > 0) {
        const over = daysBetween(d, b);
        out.push(finding('P0', '教师资格证缺失或过期', it, over,
          `${who(it)}：教师资格证 ${no} 到期日 ${d}，早于核对基准日 ${b}，**已过期 ${over} 天**。`,
          '资格证过期期间不得独立授课：先安排换证 / 复审或换人，'
          + '证件办好后把新到期日填回台账，再重跑这一项。'));
      }
    }

    const filing = cell(it, 'filingStatus');
    if (filing === '未备案') {
      out.push(finding('P0', '教师未备案', it, undefined,
        `${who(it)}：备案状态写的是「未备案」—— 教师未在教育局备案就排课，`
        + `属于年检直接扣分项（任教科目 ${cell(it, 'subject') || '(未填)'}，班级 ${cell(it, 'className') || '(未填)'}）。`,
        '先把任教教师的资质材料报到主管教育局完成备案，备案通过后再排课；'
        + '备案期间该教师的班级要么停课、要么换已备案教师。'));
    } else if (isBlank(filing)) {
      out.push(finding('P1', '教师未备案', it, undefined,
        `${who(it)}：备案状态是空的 —— 填不出来"是否已备案"，这一项就没法给结论。`,
        '备案状态填「已备案」或「未备案」两个字面值之一；拿不准的去教育局备案系统查实后再填。'));
    }
  }
  return out;
}

function checkSuperviseAccount(items) {
  // ③ 收费是否进监管账户：收款账户必须与备案的监管账户一致（字面归一化后比）
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const receipt = cell(it, 'receiptAccount');
    const sup = cell(it, 'superviseAccount');
    if (isBlank(receipt) || isBlank(sup)) continue;      // 空着 ⇒ 判不了，交给第 ⑥ 项点名
    if (normAccount(receipt) === normAccount(sup)) continue;
    out.push(finding('P0', '收费未进监管账户', it, undefined,
      `${who(it)}：收款账户写的是「${receipt}」，备案的监管账户是「${sup}」——`
      + '两个字面不一致，这笔培训费**没有进备案的资金监管账户**。',
      '监管账户是"双减"后资金监管的硬要求：先把收款账户改回备案的监管专户，'
      + '已收到的费用按规定划转进监管账户，并在台账备注里写明划转日期；'
      + '平台代收 / 个人二维码收款都算账外收费。'));
  }
  return out;
}

function checkDuplicateTeacher(items) {
  // ④ 同一教师重复登记 + 同一教师资格证号出现在两个主体
  const out = [];
  const seen = new Map();
  const certFirst = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const campus = cell(it, 'campusName');
    const teacher = cell(it, 'teacher');
    const cls = cell(it, 'className');
    const slot = cell(it, 'timeSlot');
    const key = [campus, teacher, cls, slot].join('|');
    if (teacher && campus && cls && slot) {
      if (seen.has(key)) {
        out.push(finding('P0', '教师重复登记', it, undefined,
          `${who(it)}：同一个（校区 ${campus} + 教师 ${teacher} + 班级 ${cls} + 培训时段 ${slot}）`
          + `在第 ${seen.get(key)} 行已经登记过一次 —— 同一节课重复登记。`,
          '同一节课在一本台账里只应有一行：重复登记会让课时数与收费金额被算两遍，'
          + '合计行也就跟着错。合并成一行，历史调整写进备注。'));
      } else {
        seen.set(key, it.line);
      }
    }

    const no = cell(it, 'teacherCertNo');
    if (!no) continue;
    if (certFirst.has(no)) {
      const prev = certFirst.get(no);
      if (prev.teacher !== teacher) {
        out.push(finding('P0', '证号跨主体重复', it, undefined,
          `${who(it)}：教师资格证号「${no}」在第 ${prev.line} 行挂在教师「${prev.teacher}」名下，`
          + `本行却挂在教师「${teacher}」名下 —— 同一个证号出现在两个主体。`,
          '一个教师资格证号只能对应一位教师：先核对是不是抄错了证号（掩码后四位最容易抄串），'
          + '确属两位教师共用一个号的要回教育局备案系统查实，不要靠改台账掩盖。'));
      }
    } else {
      certFirst.set(no, { line: it.line, teacher });
    }
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：教师数 / 班级数 / 课时数的合计行必须等于明细行加总
  const out = [];
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      if (!cols.some((c) => c.role === role)) continue;
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const declared = normNumber(raw);
      if (declared === null) {
        out.push(finding('P1', '合计行不符', tr, undefined,
          `第 ${tr.line} 行合计行的「${LABELS[role]}」值是「${String(raw).trim()}」，不是可识别的数字。`,
          '合计行只能写数字；请核对是否把单位（名 / 个 / 课时）写进了单元格里。'));
        continue;
      }
      const actual = round2(detail.reduce((acc, it) => {
        const n = normNumber(it[role]);
        return acc + (n === null ? 0 : n);
      }, 0));
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      out.push(finding('P1', '合计行不符', tr, diff,
        `第 ${tr.line} 行合计行的「${LABELS[role]}」写着 ${declared}，但上面 ${detail.length} 行明细逐行加总是 ${actual}，`
        + `差 ${diff}（合计 − 明细）。`,
        '合计行必须等于明细行逐列加总：先看有没有明细行被隐藏 / 筛选掉了，再看合计公式有没有漏行或重复计数。'
        + '（本工具只核这一个合计行，不替你去别的表里找补。）'));
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 必需字段缺失 / 日期格式非法 / 数值为负或课时为零 / 备案状态·科目类别·培训时段取值非法
  const out = [];
  for (const it of items) {
    if (it.isTotal) continue;
    const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
        '空着的字段会让对应的核对整项做不了（例如许可证到期日空着就判不了证照覆盖、'
        + '培训时段空着就判不了时段合规）；补全后重跑，本工具不会替你猜一个默认值。'));
    }

    for (const [role, label] of DATE_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      if (normDate(raw) === null) {
        out.push(finding('P1', '日期格式非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
          + '（只认 2026-03-31 / 2026/3/31 / 2026年3月31日 / 20260331 这几种形态）。',
          '把日期改成 2026-03-31 这种形态再跑；日期认不出来时本工具不会拿它去算超期天数。'));
      }
    }

    for (const [role, label] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        out.push(finding('P1', '数值为负或非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '金额、人数与课时都必须是纯数字（如 120 / 5,760 / 48）；'
          + '写成「一百二十」「壹佰」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 台账里的人数 / 金额 / 课时出现负数，通常是填反了或写成了红字。`,
          '确认是退费冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n === 0 && ZERO_INVALID_ROLES.indexOf(role) >= 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是 0 —— 课时为零却收了一笔培训费，台账口径上不成立（要么课还没开，要么填错了）。`,
          '按实际排课填真实课时数；预收费还没开课的，应当先按"未开课"登记并注明预计开课日期，而不是填 0。'));
      }
    }

    const filing = cell(it, 'filingStatus');
    if (filing && FILING_STATUSES.indexOf(filing) < 0) {
      out.push(finding('P1', '备案状态非法', it, undefined,
        `${who(it)}：备案状态写的是「${filing}」，不在允许的两个值里（${FILING_STATUSES.join(' / ')}）。`,
        '备案状态会直接决定"教师未备案"这类结论：按教育局备案系统的实际状态改成 已备案 / 未备案 之一。'));
    }

    const cat = cell(it, 'subjectCategory');
    if (cat && SUBJECT_CATEGORIES.indexOf(cat) < 0) {
      out.push(finding('P1', '科目类别非法', it, undefined,
        `${who(it)}：科目类别写的是「${cat}」，不在允许的两个值里（${SUBJECT_CATEGORIES.join(' / ')}）。`,
        '科目类别决定"双减"时段限制适不适用（学科类不得在法定节假日 / 休息日 / 寒暑假开展）：'
        + '按课程实际性质改成 学科类 / 非学科类 之一。'));
    }

    const slot = cell(it, 'timeSlot');
    if (slot && !isBlank(slot) && parseSlot(slot) === null) {
      out.push(finding('P1', '培训时段非法', it, undefined,
        `${who(it)}：培训时段「${slot}」不是可识别的时段`
        + '（只认 `2026-03-03 18:30-20:00` 这种"日期 + 起止时刻"的形态，且结束时刻必须晚于开始时刻）。',
        '把培训时段写成 `YYYY-MM-DD HH:MM-HH:MM`；写成「周六晚上」「每周三」这类描述时，'
        + '本工具不会去猜是哪一天 —— 时段合规与跨校区冲突两项都会因此做不了。'));
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的校外培训机构资质与教师备案台账'
      + '（完整档还可以在台账后面加一段 `--- 排课与收费记录 ---`）']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的校外培训机构资质与教师备案台账'
      + '（完整档还可以在台账后面加一段 `--- 排课与收费记录 ---`）']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的培训机构资质与教师备案台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行台账明细（现在只有表头或只有合计行，没有可核对的记录）']);
  }

  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];

  for (const f of checkLicenseValidity(t.items, base)) findings.push(f);
  for (const f of checkTeacherFiling(t.items, base)) findings.push(f);
  for (const f of checkSuperviseAccount(t.items)) findings.push(f);
  for (const f of checkDuplicateTeacher(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：完整档追加的那五项检查一项都不执行，这里如实记下来（只记「没做」，绝不伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const sumRole = (role) => round2(t.detail.reduce((acc, it) => {
    const n = normNumber(it[role]);
    return acc + (n === null ? 0 : n);
  }, 0));
  const overdueRows = findings.filter((f) => f.category === '办学许可证超期' || f.category === '营业执照超期');
  const overdueMax = overdueRows.reduce((m, f) => Math.max(m, f.diff || 0), 0);

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      teacher_count_total: t.totals.teacherCount,
      class_count_total: t.totals.classCount,
      hours_total: t.totals.hours,
      students_total: sumRole('enrollCount'),
      fee_total: sumRole('feeAmount'),
      certificate_overdue: overdueRows.length,
      certificate_overdue_days_max: overdueMax,
      unfiled_teachers: findings.filter((f) => f.category === '教师未备案').length,
      off_account_fees: findings.filter((f) => f.category === '收费未进监管账户').length,
      check_date: base,
      basis: '证照口径：核对基准日 ≤ 办学许可证到期日、且 ≤ 营业执照到期日，才算证照有效期被覆盖（超期按整天数计）；'
        + '教师口径：教师资格证号必须有、教师资格证到期日要覆盖核对基准日、备案状态必须是「已备案」；'
        + '收费口径：收款账户与备案监管账户归一化后逐字比较，不一致即报「收费未进监管账户」；'
        + '唯一性口径：同一（校区 + 教师 + 班级 + 培训时段）算同一条记录，重复登记即报，'
        + '同一个教师资格证号挂在两个教师姓名下即报「证号跨主体重复」；'
        + '合计口径：合计行的教师数 / 班级数 / 课时数必须等于明细行逐列加总；'
        + '时段口径：培训时段写成 `YYYY-MM-DD HH:MM-HH:MM` 才算合法，认不出来的只报格式非法、不参与任何时段推断；'
        + '双减口径（完整档）：学科类不得排在法定节假日 / 休息日 / 寒暑假窗口（内置 2026 年口径，最终以当地教育局校历为准）；'
        + '收费期口径（完整档）：收费起始日 + 3 个月 ≥ 收费截止日，且一次收费不得超过 60 课时。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这本台账按上面写明的口径算得对、'
      + '证照与教师资格证有效期都覆盖了核对基准日、收费账户与备案监管账户一致**，'
      + '不代表机构本身的办学资质已经获批、不代表证件与监管账户的真伪已经核验、'
      + '也不代表当地校历口径下的时段合规已经得到教育局认可 —— 那些不在本工具范围内。';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    teacher_count_total: t.totals.teacherCount,
    class_count_total: t.totals.classCount,
    hours_total: t.totals.hours,
    check_date: base,
  };
  result.scope = scope;

  return { status: 'success', result };
}

/* ============================ CLI（与 run.mjs 同一套参数口径） ============================ */

const CLI_USAGE = [
  '用法：node <engine>.js --sample | --input <入参.json|台账文本> [--json] [--no-stats]',
  '  --sample   用引擎内置样例（干净样例，0 命中）',
  '  --input    入参：{"text":"…"} 或直接粘贴的台账文本（含表头）',
  '  --json     以 JSON 输出',
  '  --no-stats 不做任何统计输出（离线）',
].join('\n');

function cliMain(argv) {
  const args = { input: '', sample: false, json: false, noStats: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--input' || a === '-i') args.input = argv[++i] || '';
    else if (a === '--sample') args.sample = true;
    else if (a === '--json') args.json = true;
    else if (a === '--no-stats') args.noStats = true;
    else if (a === '--help' || a === '-h') args.help = true;
  }
  if (args.help) {
    if (args.json) {
      console.log(JSON.stringify({ ok: true, usage: CLI_USAGE }, null, 2));
      return 0;
    }
    console.log(CLI_USAGE);
    return 0;
  }

  let payload = null;
  if (args.input) {
    let raw = '';
    try {
      raw = require('node:fs').readFileSync(args.input, 'utf8');
    } catch (e) {
      if (args.json) {
        console.log(JSON.stringify({ ok: false, error: '读不到入参文件：' + args.input }, null, 2));
        return 4;
      }
      console.error('读不到入参文件：' + args.input);
      return 4;
    }
    const trimmed = String(raw).replace(/^\uFEFF/, '').trim();
    try {
      payload = JSON.parse(trimmed);
    } catch (e) {
      payload = { text: String(raw) };
    }
  } else if (args.sample) {
    payload = { text: SAMPLE_TEXT };
  } else {
    if (args.json) {
      console.log(JSON.stringify({ ok: false, error: '缺少入参：用 --sample 或 --input' }, null, 2));
      return 1;
    }
    console.error('缺少入参：用 --sample 或 --input');
    return 1;
  }

  let out;
  try {
    out = run(payload);
  } catch (e) {
    if (args.json) {
      console.log(JSON.stringify({ ok: false, error: String((e && e.message) || e) }, null, 2));
      return 9;
    }
    console.error('引擎执行出错：' + ((e && e.message) || e));
    return 9;
  }

  // 免费档：无论入参里带什么开关，本包都只执行免费六项（付费实现不在这个包里）
  if (out.status !== 'success') {
    if (args.json) {
      console.log(JSON.stringify({
        ok: false, tier: 'free', status: out.status,
        missing: out.missing, advice: out.advice,
      }, null, 2));
      return 3;
    }
    console.log('材料不足，本次没有执行任何检查，因此不出结论。');
    for (const m of (out.missing || [])) console.log('  - ' + m);
    console.log('怎么补：' + out.advice);
    return 3;
  }

  if (args.json) {
    console.log(JSON.stringify({
      ok: true,
      tier: 'free',
      checks: CHECKS_GIVEN.length,
      checks_given: CHECKS_GIVEN,
      checks_withheld: CHECKS_WITHHELD,
      omitted_findings: 0,
      result: out.result,
    }, null, 2));
    return 0;
  }
  console.log('免费档核对完成');
  console.log(`本次执行的检查项：${CHECKS_GIVEN.join('、')}`);
  console.log(`本版本不包含（如实声明，未执行）：${CHECKS_WITHHELD.join('、')}`);
  console.log('');
  console.log(JSON.stringify(out.result, null, 2));
  return 0;
}

if (require.main === module) {
  process.exit(cliMain(process.argv.slice(2)));
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow, normAccount, parseSlot, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
