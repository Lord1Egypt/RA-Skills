#!/usr/bin/env node
/**
 * secondary-water-supply-check.js —— 二次供水清洗消毒与水质检测核对引擎（**免费档**；确定性、纯 Node 标准库）。
 *
 * 真实痛点：物业 / 供水管理单位对**二次供水**的水箱（水池）必须**每半年（180 天口径）清洗消毒一次**
 * 并做水质检测，台账每月 / 每季要向业主与卫生监督报一次。这本台账一旦出错，直接是**卫生监督处罚 + 水质事故**：
 *   ① 清洗周期超期：距上次清洗已过 180 天还没洗 —— 监管直接下整改 / 处罚；
 *   ② 检测项目缺失：常规指标子集没做全（缺菌落总数、缺总大肠菌群…），"其他项都合格"不能顶；
 *   ③ 检测结果超限值 / 低于限值：超标水样不得作为合格报告归档，必须复采复检并闭环；
 *   ④ 清洗单位资质与作业人员健康证：缺证 / 过期作业是直接处罚项；
 *   ⑤ 同一水箱同一天被登记成两次清洗（两套单位 / 人员打架）：追溯时说不清到底洗过没有。
 * 所以每条结论都必须能拿原文行号 + 原文行内容复算。
 *
 * ⚠️ 本文件是**免费档子集**：只实现下面这六项**表内逐行算术与台账勾稽**：
 *   ① 清洗周期覆盖（基准日 − 上次清洗日期 ≤ 180 天，超期给天数）+ 下次清洗日期复算；
 *   ② 检测项目齐全（常规指标子集）与限值判定（超上限 / 低于下限，给倍数）；
 *   ③ 清洗单位与作业人员健康证覆盖；④ 同一水箱同日重复清洗记录；
 *   ⑤ 合计行逐列复核（水箱数 / 检测项数）；⑥ 字段合法性（缺失、日期格式、数值为负或为零、供水状态非法）。
 *   **完整档（付费）的实现不在这个包里** —— 超期未清洗或未检测仍在供水、停用废弃水箱仍在巡检记录、
 *   检测结果超标未闭环、消毒剂残留检测断档、分小区 × 分水箱汇总清单都不在这里。
 *   `CHECKS_WITHHELD` 只是「未执行的检查项」的**说明文本**，不是实现；
 *   本次**没有执行**的检查项会原样出现在结果的 `checks_not_run` 里，并明确写「这不等于没问题」——
 *   未执行就是未执行，绝不用默认值编造结论。
 *
 * 与同仓库另外三个跟"水 / 物业"有关的产品**不是一回事**（别混用）：
 *   · `utility-meter-reading-check` 核的是水电抄表与账单（表底、单价、用量、账单金额）；
 *   · `property-utility-apportionment-check` 核的是公共能耗在业主之间的分摊；
 *   · `wastewater-fee-check` 核的是污水处理费结算（水量勾稽、水质档位、超标扣款）；
 *   本产品核的是**二次供水水箱的清洗消毒周期 + 水质检测项目与限值**，既不抄表、也不分摊、也不算污水费。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定水箱容积 / 材质 / 消毒方式是否符合卫生规范、不判定水样采集与实验室检测过程是否规范、
 *          不判定现场是否真的洗过、不读 .xlsx / .pdf 原件、不联网核验清洗单位资质证书 / 健康证 / 检测报告真伪；
 *          材料不足**一律不给结论**（连「未发现问题」也不输出）。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '清洗周期覆盖（核对基准日 − 上次清洗日期 ≤ 180 天，超期逐水箱给出已超期天数；「下次清洗日期」与「上次清洗日期 + 180 天」逐水箱复算）',
  '检测项目齐全与限值判定（按水箱核对常规指标子集是否齐全；逐项判定检测结果是否超出上限 / 低于下限并给出倍数）',
  '清洗单位与作业人员健康证覆盖（清洗单位 / 清洗人员不得空缺；健康证有效期要覆盖本次清洗作业日，缺证或过期逐水箱点名）',
  '同一水箱同日重复清洗记录（同一水箱编号 + 同一上次清洗日期下出现互相矛盾的清洗单位或清洗人员）',
  '合计行逐列复核（水箱数 = 明细里不重复的水箱编号个数；检测项数 = 明细行数）',
  '字段合法性（关键字段缺失、日期格式非法、数值为负或为零、供水状态非法）',
];

const CHECKS_WITHHELD = [
  '超期未清洗或未检测仍在供水（供水状态=在供水，且清洗已超 180 天 / 检测已超 180 天 / 查不到有效检测日期；P0 并附超期天数）',
  '停用或已废弃水箱仍出现在巡检记录（跨表交叉：台账供水状态为停用 / 废弃，却在「巡检记录」段里出现，点巡检记录原文行号）',
  '检测结果超标未闭环（跨表交叉：台账里越过限值的项，到「复检记录」段核对复检日期与复检结果；缺复检或复检仍不合格逐条点名）',
  '消毒剂残留检测断档（跨表交叉：按「水箱 × 检测日期」逐次比对消毒剂残留记录，哪一次没有余氯 / 二氧化氯记录就点哪一次）',
  '分小区 × 分水箱（设施）汇总清单（按超期天数降序，每组给出可整改动作）与逐水箱整改清单（result.rollup / result.consolidated_actions）',
];

const OUT_OF_SCOPE = [
  '判定二次供水水箱的容积、材质、内壁处理与消毒方式是否符合卫生规范（那是设计审查与卫生许可的口径，本工具只核台账日期与检测算术）',
  '判定水样采集 / 保存 / 运输 / 实验室检测过程是否规范、判定检测报告本身是否有效（那是 CMA / CNAS 检测机构与卫生监督部门的判定权）',
  '判定超期未清洗到底是物业没做还是做了没记、判定现场是否真的已经清洗或已经停水（本工具只核台账与巡检 / 复检记录的字面一致性）',
  '读取 .xlsx / .pdf 原件、联网核验清洗单位资质证书 / 作业人员健康证 / 水质检测报告的真伪，替代卫生监督部门或供水管理单位的认定',
];

// 样例：一本**干净**的二次供水清洗消毒与水质检测台账 —— 2 个小区、3 个水箱、18 条检测记录：
// 清洗周期都在 180 天内、下次清洗日期复算一致、常规指标子集齐全且结果全在限值内、健康证都在有效期内、
// 水箱编号不重复、合计行与明细一致；三段跨表记录（消毒剂残留 / 巡检 / 复检）也都对得上。**全表零命中**。
const SAMPLE_TEXT = [
  '小区/项目名称\t水箱编号\t水箱名称\t上次清洗日期\t下次清洗日期\t清洗单位\t清洗人员\t健康证有效期\t检测日期\t检测项目\t检测结果\t限值\t单位\t供水状态\t水箱数\t检测项数\t核对基准日\t备注',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t色度\t5\t15\t度\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t浑浊度\t0.3\t1\tNTU\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\tpH\t7.2\t6.5~8.5\t无量纲\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t游离余氯\t0.35\t0.05~0.8\tmg/L\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t菌落总数\t20\t100\tCFU/mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-01\t1号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t王丽娟\t2027-03-31\t2026-03-18\t总大肠菌群\t未检出\t不得检出\tMPN/100mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t色度\t6\t15\t度\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t浑浊度\t0.35\t1\tNTU\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\tpH\t7.1\t6.5~8.5\t无量纲\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t游离余氯\t0.32\t0.05~0.8\tmg/L\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t菌落总数\t25\t100\tCFU/mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '阳光花园小区\tSX-2026-02\t2号生活水箱\t2025-11-20\t2026-05-19\t江南清洗消毒服务有限公司\t陈志强\t2026-12-31\t2026-03-18\t总大肠菌群\t未检出\t不得检出\tMPN/100mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t色度\t5\t15\t度\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t浑浊度\t0.4\t1\tNTU\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\tpH\t7.0\t6.5~8.5\t无量纲\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t游离余氯\t0.30\t0.05~0.8\tmg/L\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t菌落总数\t30\t100\tCFU/mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '桂花苑小区\tSX-2026-03\t高区生活水箱\t2025-12-05\t2026-06-03\t江城水务清洗有限公司\t刘海燕\t2028-01-31\t2026-04-08\t总大肠菌群\t未检出\t不得检出\tMPN/100mL\t在供水\t—\t—\t2026-04-30\t常规指标全项合格',
  '合计\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t—\t3\t18\t2026-04-30\t2 个小区 3 个水箱 18 条检测记录由明细行汇总',
  '--- 消毒剂残留检测记录 ---',
  '水箱编号\t检测日期\t余氯(mg/L)\t二氧化氯(mg/L)',
  'SX-2026-01\t2026-03-18\t0.35\t—',
  'SX-2026-02\t2026-03-18\t0.32\t—',
  'SX-2026-03\t2026-04-08\t0.30\t—',
  '--- 巡检记录 ---',
  '水箱编号\t巡检日期\t巡检人\t巡检结果',
  'SX-2026-01\t2026-04-10\t赵国庆\t正常',
  'SX-2026-02\t2026-04-10\t赵国庆\t正常',
  'SX-2026-03\t2026-04-12\t孙明远\t正常',
  '--- 复检记录 ---',
  '水箱编号\t检测项目\t复检日期\t复检结果',
].join('\n');

const TOL = 0.01;

/** 二次供水水箱的法定清洗消毒周期：每半年（按 180 天口径核） */
const CLEAN_CYCLE_DAYS = 180;

// 表头级必需列（缺列 ⇒ 材料不足，不给结论）
const REQUIRED_ROLES = [
  'community', 'tankNo', 'lastCleanDate', 'cleanCompany', 'cleanStaff', 'healthCertExpiry',
  'testDate', 'testItem', 'testResult', 'limitValue', 'unit', 'nextCleanDate', 'checkDate',
];

// 单元格级必需字段（空白 / 占位符 ⇒ 逐行点名）
const REQUIRED_FIELDS = [
  ['community', '小区/项目名称'],
  ['tankNo', '水箱编号'],
  ['lastCleanDate', '上次清洗日期'],
  ['cleanCompany', '清洗单位'],
  ['cleanStaff', '清洗人员'],
  ['healthCertExpiry', '健康证有效期'],
  ['testDate', '检测日期'],
  ['testItem', '检测项目'],
  ['testResult', '检测结果'],
  ['limitValue', '限值'],
  ['unit', '单位'],
  ['nextCleanDate', '下次清洗日期'],
  ['checkDate', '核对基准日'],
];

// 日期列（格式非法逐格点名）
const DATE_FIELDS = [
  ['lastCleanDate', '上次清洗日期'],
  ['nextCleanDate', '下次清洗日期'],
  ['healthCertExpiry', '健康证有效期'],
  ['testDate', '检测日期'],
  ['checkDate', '核对基准日'],
];

// 数值列：[角色, 标签, 允许定性文字]
//   水箱数 / 检测项数 是纯数量（负数或 0 都不成立）；检测结果允许「未检出 / 阴性」这类定性描述。
const NUMBER_FIELDS = [
  ['tankCount', '水箱数', false],
  ['itemCount', '检测项数', false],
  ['testResult', '检测结果', true],
];

// 二次供水水质检测的**常规指标子集**：这 6 项少任何一项，这份检测报告在卫生监督眼里都不算做全
const REQUIRED_TEST_ITEMS = ['色度', '浑浊度', 'pH', '游离余氯', '菌落总数', '总大肠菌群'];

// 供水状态只认这三个值（二次供水水箱台账口径）
const SUPPLY_STATUSES = ['在供水', '停用', '废弃'];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词就会把更具体的列抢走（本仓库踩过多次，见 tools/header_map_check.py）。
//    本表的坑位：
//      · 「清洗单位」必须排在「单位」之前（否则被 unit 抢走）；
//      · 「下次清洗日期」必须排在「上次清洗日期」之前（后者的「清洗日期」会抢先命中）；
//      · 「水箱数」「检测项数」必须排在「水箱编号」「检测项目」之前；
//      · 「复检结果」「巡检结果」必须排在「检测结果」之前；
//      · 「检测日期」必须排在兜底的「日期」（recordDate）之前；
//      · 兜底的「日期」只能放在所有日期角色之后。
const ROLES = {
  tankCount: ['水箱数量', '水箱数', '设施数量'],
  itemCount: ['检测项目数', '检测项数', '检测项目合计'],
  community: ['小区/项目名称', '小区名称', '项目名称', '小区', '管理处'],
  tankNo: ['水箱编号', '水池编号', '水箱号', '设施编号'],
  tankName: ['水箱名称', '设施名称', '水箱位置'],
  nextCleanDate: ['下次清洗消毒日期', '下次清洗日期', '计划清洗日期', '下次清洗'],
  lastCleanDate: ['上次清洗消毒日期', '上次清洗日期', '最近一次清洗日期', '清洗日期', '上次清洗'],
  cleanCompany: ['清洗消毒单位', '清洗单位', '施工单位', '服务单位'],
  cleanStaff: ['清洗消毒人员', '清洗人员', '作业人员', '施工人员'],
  healthCertExpiry: ['健康证有效期至', '健康证有效期止', '健康证有效期', '健康证明有效期', '健康证到期日'],
  recheckDate: ['复检日期', '复查日期', '复检时间'],
  recheckResult: ['复检结果', '复查结果', '复检值'],
  recordResult: ['巡检结果', '巡检情况', '巡查结果'],
  testItem: ['检测项目', '检验项目', '水质检测项目'],
  testResult: ['检测结果', '检验结果', '检测值'],
  limitValue: ['限值', '标准限值', '限值要求', '标准值', '卫生标准'],
  testDate: ['检测日期', '检验日期', '采样日期', '检测时间'],
  unit: ['单位', '计量单位'],
  supplyStatus: ['供水状态', '水箱状态', '使用状态', '运行状态'],
  inspector: ['巡检人员', '巡检人', '巡检员'],
  recordDate: ['巡检日期', '巡查日期', '记录日期', '日期'],
  chlorineDioxide: ['二氧化氯'],
  chlorine: ['游离性余氯', '余氯'],
  checkDate: ['核对基准日', '核对日期', '核查日期', '基准日期', '基准日'],
  note: ['备注', '说明'],
};

const LABELS = {
  community: '小区/项目名称',
  tankNo: '水箱编号',
  tankName: '水箱名称',
  lastCleanDate: '上次清洗日期',
  nextCleanDate: '下次清洗日期',
  cleanCompany: '清洗单位',
  cleanStaff: '清洗人员',
  healthCertExpiry: '健康证有效期',
  testDate: '检测日期',
  testItem: '检测项目',
  testResult: '检测结果',
  limitValue: '限值',
  unit: '单位',
  supplyStatus: '供水状态',
  tankCount: '水箱数',
  itemCount: '检测项数',
  checkDate: '核对基准日',
  recheckDate: '复检日期',
  recheckResult: '复检结果',
  recordDate: '巡检日期',
  inspector: '巡检人',
  recordResult: '巡检结果',
  chlorine: '余氯',
  chlorineDioxide: '二氧化氯',
  note: '备注',
};

// 合计行要复核的数量类列：水箱数（不重复水箱个数）与检测项数（明细行数）
const SUM_ROLES = ['tankCount', 'itemCount'];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张台账补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「周期覆盖」，也不说「超期」。',
  };
}

/** 全角数字 / 全角符号 → 半角（物业与检测台账里很常见；认不出来就绝不猜） */
function toHalf(raw) {
  return String(raw)
    .replace(/[\uFF10-\uFF19]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
    .replace(/\uFF0E/g, '.').replace(/\uFF0C/g, ',').replace(/\uFF0B/g, '+')
    .replace(/\uFF0D/g, '-').replace(/\uFF05/g, '%')
    .replace(/\uFF08/g, '(').replace(/\uFF09/g, ')')
    .replace(/\uFF1C/g, '<').replace(/\uFF1E/g, '>')
    .replace(/\u3000/g, ' ');
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = toHalf(String(raw)).trim().replace(/[¥￥,，\s]/g, '');
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
  const s = toHalf(String(v)).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|不适用|待填|待补|待定|待核)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 日期归一化成 YYYY-MM-DD；认不出来返回 null（认不出来绝不当成今天） */
function normDate(raw) {
  if (raw === undefined || raw === null) return null;
  let s = toHalf(String(raw)).trim();
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
function isoOfDayNum(n) {
  return new Date(n * DAY_MS).toISOString().slice(0, 10);
}
/** b − a（整天数，正数表示 b 在 a 之后） */
function daysBetween(a, b) {
  return dayNum(b) - dayNum(a);
}
/** 日期 + 天数（清洗周期用**天**口径，避免 30 / 31 天换月带来的 1 天争议） */
function addDays(iso, n) {
  return isoOfDayNum(dayNum(iso) + n);
}

const SECTION_RE = /^\s*-{2,}\s*(.+?)\s*-{2,}\s*$/;
function isSectionMarker(line) {
  return SECTION_RE.test(String(line == null ? '' : line));
}

function roleOf(header) {
  const h = toHalf(String(header == null ? '' : header)).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    for (const k of keys) {
      if (h.indexOf(k) >= 0) return role;
    }
  }
  return null;
}

const TOTAL_LABEL = /^(合计|小计|总计|总合计|合\s*计)$/;
/**
 * 合计行不是水箱明细：逐水箱检查要跳过它，只有「合计行逐列复核」那一项会用到它。
 * 合计行可能把「合计」写在小区 / 项目名称列（本台账的写法），也可能写在水箱编号 / 水箱名称列 —— 都要认出来。
 */
function isTotalRow(it) {
  const no = String(it.tankNo == null ? '' : it.tankNo).trim();
  const name = String(it.tankName == null ? '' : it.tankName).trim();
  const cm = String(it.community == null ? '' : it.community).trim();
  return TOTAL_LABEL.test(no) || TOTAL_LABEL.test(name) || TOTAL_LABEL.test(cm);
}

/**
 * 解析成 {header, cols, items, detail, totalRows, totals, missingRoles, missingColumns, error}。
 * items 是**扁平**对象：{line, raw, isTotal, 角色:值…}；遇到一行 `--- 段名 ---` 就停（后面是另一张表）。
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
  // 合计口径：水箱数 = 明细里不重复的水箱编号个数；检测项数 = 明细行数（不是逐行求和）
  const tanks = new Set(detail.map((it) => cell(it, 'tankNo')).filter(Boolean));
  const totals = { tankCount: tanks.size, itemCount: detail.length };
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
  const name = cell(it, 'tankName');
  const no = cell(it, 'tankNo');
  const cm = cell(it, 'community');
  const label = name || no || '未命名水箱';
  const tail = name && no ? ' / ' + no : '';
  return `第 ${it.line} 行「${label}${tail}」${cm ? '（' + cm + '）' : ''}`;
}

function listShow(arr, max) {
  const n = max || 8;
  const a = arr.slice(0, n);
  return a.join('、') + (arr.length > n ? ' 等' : '');
}

/** 每条结论都带原文依据：行号 + 水箱编号 + 该行原文（截断），可被第三方用同一口径复算 */
function finding(level, category, it, diff, message, advice) {
  const f = {
    level,
    category,
    line: it.line,
    tank_no: cell(it, 'tankNo'),
    community: cell(it, 'community'),
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
    const d = normDate(it.checkDate);
    if (d) return d;
  }
  return null;
}
const baseOf = (it, base) => normDate(it.checkDate) || base;

/** 把明细行按水箱编号分组（同一水箱的多条检测记录合成一组，逐水箱检查只报一次） */
function tankGroups(items) {
  const map = new Map();
  let seq = 0;
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'tankNo');
    let key = no;
    if (!key) { seq += 1; key = '(未填水箱编号)#' + seq; }
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(it);
  }
  return [...map.values()];
}

/** 一组行里第一个能认出来的日期 */
function firstDateOf(rows, role) {
  for (const r of rows) {
    const d = normDate(r[role]);
    if (d) return d;
  }
  return null;
}

/* ============================ 限值判定（免费档第 ② 项用） ============================ */

/**
 * 解析「限值」单元格，支持四种真实形态：
 *   · 单个数字   15 / 100       ⇒ 上限（结果 ≤ 限值）
 *   · 区间       6.5~8.5        ⇒ 上下限都要满足（分隔符认 ~ ～ - — 至）
 *   · 带比较符   ≥0.05 / ≤15    ⇒ 只判下限 / 只判上限
 *   · 定性       不得检出        ⇒ 结果必须是 未检出 / 阴性 / 0
 */
function parseLimit(raw) {
  const s = toHalf(String(raw == null ? '' : raw)).replace(/\s/g, '');
  if (!s || /^[-—–]+$/.test(s)) return { kind: 'blank' };
  if (/不得检出|不应检出|不得验出|不得测出/.test(s)) return { kind: 'nodetect', raw: s };
  const cmp = /^([≥≤<>=]+)/.exec(s);
  const body = s.replace(/^[≥≤<>=]+/, '');
  const m = /^(-?\d+(?:\.\d+)?)\s*[~～\-—至]\s*(-?\d+(?:\.\d+)?)$/.exec(body);
  if (m) return { kind: 'range', lo: Number(m[1]), hi: Number(m[2]), raw: s };
  const n = normNumber(body);
  if (n === null) return { kind: 'unknown', raw: s };
  if (cmp) {
    if (/[≥>]/.test(cmp[1])) return { kind: 'min', v: n, raw: s };
    if (/[≤<]/.test(cmp[1])) return { kind: 'max', v: n, raw: s };
  }
  return { kind: 'max', v: n, raw: s };
}

const NEG_WORDS = /未检出|未测出|未验出|阴性|不检出|无检出/;
const POS_WORDS = /检出|阳性/;

/**
 * 判定「检测结果」是否在「限值」之内。返回 {verdict, ratio, why, value}：
 *   verdict: ok / over（越过上限，或"不得检出"却检出） / under（低于下限） / unknown（认不出来）
 *   ratio  : 越限倍数（结果 ÷ 上限）；低于下限时给「下限 ÷ 结果」的倍数
 */
function judgeResult(resultRaw, limitRaw) {
  const rRaw = String(resultRaw == null ? '' : resultRaw).trim();
  const lim = parseLimit(limitRaw);
  if (lim.kind === 'blank') return { verdict: 'unknown', why: '限值没填' };
  if (lim.kind === 'unknown') return { verdict: 'unknown', why: `限值「${lim.raw}」认不出是数字、区间还是比较符` };
  if (rRaw === '') return { verdict: 'unknown', why: '检测结果没填' };

  const rNum = normNumber(rRaw);
  const rNeg = NEG_WORDS.test(rRaw);
  const rPos = !rNeg && POS_WORDS.test(rRaw);

  if (lim.kind === 'nodetect') {
    if (rNeg) return { verdict: 'ok', value: 0 };
    if (rNum !== null) {
      return rNum > TOL
        ? { verdict: 'over', value: rNum, why: `限值是「不得检出」，但结果填了 ${rNum}` }
        : { verdict: 'ok', value: rNum };
    }
    if (rPos) return { verdict: 'over', value: rRaw, why: `限值是「不得检出」，但结果是「${rRaw}」` };
    return { verdict: 'unknown', why: `限值是「不得检出」，但结果「${rRaw}」看不出是检出还是未检出` };
  }

  const value = rNum !== null ? rNum : (rNeg ? 0 : null);
  if (value === null) return { verdict: 'unknown', why: `结果「${rRaw}」既不是数字，也不是未检出 / 阴性这类定性描述` };

  if (lim.kind === 'range') {
    if (value > lim.hi + TOL) return { verdict: 'over', ratio: round2(value / lim.hi), value, why: `超过区间上限 ${lim.hi}` };
    if (value < lim.lo - TOL) return { verdict: 'under', ratio: value > 0 ? round2(lim.lo / value) : undefined, value, why: `低于区间下限 ${lim.lo}` };
    return { verdict: 'ok', value };
  }
  if (lim.kind === 'min') {
    if (value < lim.v - TOL) return { verdict: 'under', ratio: value > 0 ? round2(lim.v / value) : undefined, value, why: `低于下限 ${lim.v}` };
    return { verdict: 'ok', value };
  }
  if (value > lim.v + TOL) return { verdict: 'over', ratio: lim.v > 0 ? round2(value / lim.v) : undefined, value, why: `超过限值 ${lim.v}` };
  return { verdict: 'ok', value };
}

/* ============================ 免费档检查（六项） ============================ */

function checkCleanCycle(items, base) {
  // ① 清洗周期覆盖：核对基准日 − 上次清洗日期 ≤ 180 天，超期给天数；下次清洗日期按 +180 天逐水箱复算
  const out = [];
  for (const rows of tankGroups(items)) {
    const first = rows[0];
    const last = firstDateOf(rows, 'lastCleanDate');
    const b = baseOf(first, base);
    if (last && b) {
      const elapsed = daysBetween(last, b);
      if (elapsed > CLEAN_CYCLE_DAYS) {
        const over = elapsed - CLEAN_CYCLE_DAYS;
        out.push(finding('P1', '清洗超期', first, over,
          `${who(first)}：上次清洗日期 ${last}，距核对基准日 ${b} 已经 ${elapsed} 天，`
          + `超过 ${CLEAN_CYCLE_DAYS} 天的半年清洗周期，**已超期 ${over} 天**`
          + `（该水箱在台账里有 ${rows.length} 条检测记录）。`,
          '二次供水水箱每半年必须清洗消毒一次：先按上面的天数排进本月清洗计划，'
          + '清洗完成后补做一次水质检测，并把新的「上次清洗日期 / 下次清洗日期」填回台账；别只改日期。'));
      }
    }
    const next = firstDateOf(rows, 'nextCleanDate');
    if (last && next) {
      const expect = addDays(last, CLEAN_CYCLE_DAYS);
      if (next !== expect) {
        const drift = daysBetween(expect, next);
        out.push(finding('P2', '清洗周期与下次清洗日期不符', first, drift,
          `${who(first)}：上次清洗日期 ${last} + ${CLEAN_CYCLE_DAYS} 天 = ${expect}，`
          + `但台账写的下次清洗日期是 ${next}，差 ${Math.abs(drift)} 天（复算值 − 台账值）。`,
          '两个字段只能有一个是对的：要么上次清洗日期抄错，要么下次清洗日期是照抄上一年 / 手工估的。'
          + '先拿清洗消毒记录单上的日期改正，再重跑。'));
      }
    }
  }
  return out;
}

function checkTestItemsAndLimits(items) {
  // ②-a 检测项目齐全：按水箱核对常规指标子集（缺哪一项就点哪一项）
  const out = [];
  for (const rows of tankGroups(items)) {
    const first = rows[0];
    const have = [];
    for (const r of rows) {
      const t = cell(r, 'testItem');
      if (t && have.indexOf(t) < 0) have.push(t);
    }
    if (!have.length) continue;                     // 检测项目整列空 ⇒ 交给第 ⑥ 项逐行点名
    const miss = REQUIRED_TEST_ITEMS.filter((req) => !have.some((t) => t.indexOf(req) >= 0));
    if (miss.length) {
      out.push(finding('P1', '检测项目缺失', first, miss.length,
        `${who(first)}：这个水箱的定期水质检测一共只登记了 ${have.length} 项（${listShow(have, 6)}），`
        + `常规指标子集里缺这几项 —— ${miss.join('、')}。`,
        '二次供水的水质检测项目要覆盖卫生规范要求的常规指标子集：缺哪一项就先补采水样做哪一项；'
        + '缺项的检测报告在卫生监督眼里等于没做全，别用其他项都合格顶过去。'));
    }
  }

  // ②-b 逐项限值判定（越限就报，并给倍数）
  for (const it of items) {
    if (it.isTotal) continue;
    const raw = cell(it, 'testResult');
    const limRaw = cell(it, 'limitValue');
    if (isBlank(raw) || isBlank(limRaw)) continue;  // 缺谁交给第 ⑥ 项点名
    const j = judgeResult(raw, limRaw);
    const item = cell(it, 'testItem') || '(未填检测项目)';
    const unit = cell(it, 'unit');
    if (j.verdict === 'over') {
      out.push(finding('P0', '检测结果超限值', it, j.ratio,
        `${who(it)}：检测项目「${item}」的结果 ${raw}${unit ? ' ' + unit : ''} 越过了限值 ${limRaw}`
        + `（${j.why}${j.ratio !== undefined ? '，为限值的 ' + j.ratio + ' 倍' : ''}）。`,
        '超标水样不得作为合格报告归档：先同一样点、同一项目复采复检；'
        + '同时按超标项目倒查消毒与清洗环节，整改后重新检测并留痕，复检结果填进「复检记录」段。'));
    } else if (j.verdict === 'under') {
      out.push(finding('P1', '检测结果低于限值', it, j.ratio,
        `${who(it)}：检测项目「${item}」的结果 ${raw}${unit ? ' ' + unit : ''} 低于限值 ${limRaw}`
        + `（${j.why}${j.ratio !== undefined ? '，只有下限的 1/' + j.ratio : ''}）。`,
        '低于下限同样不合格：消毒剂残留不足会让管网末梢的余氯掉到保护线以下，'
        + '先查投加设备与投加量，再补做一次检测确认。'));
    }
  }
  return out;
}

function checkCleaningQualification(items, base) {
  // ③ 清洗单位 / 清洗人员 / 健康证：人员与单位不得空缺；健康证有效期必须覆盖本次清洗作业日
  const out = [];
  for (const rows of tankGroups(items)) {
    const first = rows[0];
    const staff = cell(first, 'cleanStaff');
    const miss = [];
    if (isBlank(first.cleanCompany)) miss.push('清洗单位');
    if (isBlank(first.cleanStaff)) miss.push('清洗人员');
    if (miss.length) {
      out.push(finding('P1', '清洗单位或人员缺失', first, miss.length,
        `${who(first)}：${miss.join('、')}是空的 —— 清洗记录连是谁来洗的都点不出来。`,
        '二次供水清洗消毒必须由具备资质的清洗单位派人作业：把清洗单位全称与作业人员姓名补进台账，'
        + '并保留清洗消毒记录单（含单位盖章、作业日期、人员签到）。'));
    }

    const certRaw = first.healthCertExpiry;
    const work = firstDateOf(rows, 'lastCleanDate') || baseOf(first, base);
    if (isBlank(certRaw)) {
      out.push(finding('P1', '健康证过期或缺失', first, undefined,
        `${who(first)}：清洗人员 ${staff || '(未填)'} 的健康证有效期是空的 —— `
        + '台账里连到期日都点不出来，等于无法证明作业时持有效健康证。',
        '从事二次供水清洗消毒的人员必须持有效健康证：把姓名与健康证有效期逐水箱补进台账，'
        + '证件在别处的也要能在这本台账里点到。'));
    } else {
      const d = normDate(certRaw);
      if (d && work && daysBetween(d, work) > 0) {
        const over = daysBetween(d, work);
        out.push(finding('P0', '健康证过期或缺失', first, over,
          `${who(first)}：清洗人员 ${staff || '(未填)'} 的健康证有效期 ${d}，`
          + `早于本次清洗作业日 ${work}，**作业时已过期 ${over} 天**。`,
          '健康证过期期间不得从事二次供水清洗消毒作业：先安排体检换证或换持证人，'
          + '并把换证后的有效期填回台账。'));
      }
    }
  }
  return out;
}

function checkDuplicateCleaning(items) {
  // ④ 同一水箱 + 同一上次清洗日期下出现互相矛盾的清洗单位 / 清洗人员 ⇒ 同一天被登记成两次清洗
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (it.isTotal) continue;
    const no = cell(it, 'tankNo');
    const last = normDate(it.lastCleanDate);
    if (!no || !last) continue;
    const key = no + '|' + last;
    const company = cell(it, 'cleanCompany');
    const staff = cell(it, 'cleanStaff');
    if (!seen.has(key)) {
      seen.set(key, { line: it.line, company, staff });
      continue;
    }
    const p = seen.get(key);
    const conf = [];
    if (p.company && company && p.company !== company) {
      conf.push(`清洗单位「${p.company}」（第 ${p.line} 行）与「${company}」`);
    }
    if (p.staff && staff && p.staff !== staff) {
      conf.push(`清洗人员「${p.staff}」（第 ${p.line} 行）与「${staff}」`);
    }
    if (!conf.length) continue;
    out.push(finding('P0', '同一水箱同日重复清洗记录', it, conf.length,
      `${who(it)}：水箱编号 ${no} 的「上次清洗日期」都写着 ${last}，但清洗记录出现了互相矛盾的两套 —— `
      + `${conf.join('；')}。同一天被登记成两次清洗（或至少两套记录打架），追溯时说不清到底洗过没有。`,
      '一个水箱一次清洗只能有一条清洗记录：先找清洗消毒记录单核对当天的实际作业单位与人员，'
      + '删掉错的那一行，并把两套记录的来源写进备注（别只改一行了事）。'));
  }
  return out;
}

function checkTotals(items, cols) {
  // ⑤ 合计行逐列复核：水箱数 = 不重复水箱编号个数；检测项数 = 明细行数
  const out = [];
  const detail = items.filter((it) => !it.isTotal);
  const totalRows = items.filter((it) => it.isTotal);
  const expected = {
    tankCount: new Set(detail.map((it) => cell(it, 'tankNo')).filter(Boolean)).size,
    itemCount: detail.length,
  };
  for (const tr of totalRows) {
    for (const role of SUM_ROLES) {
      if (!cols.some((c) => c.role === role)) continue;
      const raw = tr[role];
      if (isBlank(raw)) continue;
      const declared = normNumber(raw);
      if (declared === null) {
        out.push(finding('P1', '合计行不符', tr, undefined,
          `第 ${tr.line} 行合计行的「${LABELS[role]}」值是「${String(raw).trim()}」，不是可识别的数字。`,
          '合计行只能写数字；请核对是否把单位（个 / 项）写进了单元格里。'));
        continue;
      }
      const actual = expected[role];
      const diff = round2(declared - actual);
      if (Math.abs(diff) < TOL) continue;
      const how = role === 'tankCount'
        ? `明细里不重复的水箱编号只有 ${actual} 个`
        : `明细一共 ${actual} 行`;
      out.push(finding('P1', '合计行不符', tr, diff,
        `第 ${tr.line} 行合计行的「${LABELS[role]}」写着 ${declared}，但${how}，`
        + `差 ${diff}（合计 − 明细）。`,
        '合计行必须与明细对得上：先看有没有明细行被隐藏 / 筛选掉了，再看合计公式有没有把同一水箱的多条检测记录重复计数'
        + '（水箱数要按**不重复的水箱编号**数，不是按行数）。'));
    }
  }
  return out;
}

function checkFieldIntegrity(items) {
  // ⑥ 关键字段缺失 / 日期格式非法 / 数值为负或为零 / 供水状态非法
  const out = [];
  for (const it of items) {
    if (!it.isTotal) {
      const miss = REQUIRED_FIELDS.filter(([role]) => isBlank(it[role])).map(([, label]) => label);
      if (miss.length) {
        out.push(finding('P1', '关键字段缺失', it, miss.length,
          `${who(it)}：这些关键字段是空的或占位符 —— ${miss.join('、')}。`,
          '空着的字段会让对应的核对整项做不了（例如限值空着就判不了超标、健康证空着就判不了覆盖）；'
          + '补全后重跑，本工具不会替你猜一个默认值。'));
      }
      for (const [role, label] of DATE_FIELDS) {
        const raw = it[role];
        if (isBlank(raw)) continue;
        if (normDate(raw) === null) {
          out.push(finding('P1', '日期格式非法', it, undefined,
            `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的日期`
            + '（只认 2026-04-30 / 2026/4/30 / 2026年4月30日 / 20260430 这几种形态）。',
            '把日期改成 2026-04-30 这种形态再跑；日期认不出来时本工具不会拿它去算清洗周期或超期天数。'));
        }
      }
      const st = cell(it, 'supplyStatus');
      if (st && SUPPLY_STATUSES.indexOf(st) < 0) {
        out.push(finding('P1', '供水状态非法', it, undefined,
          `${who(it)}：供水状态写的是「${st}」，不在允许的三个值里（${SUPPLY_STATUSES.join(' / ')}）。`,
          '供水状态会直接决定「超期未清洗仍在供水」这类结论：按实际状态改成 在供水 / 停用 / 废弃 之一。'));
      }
    }

    for (const [role, label, soft] of NUMBER_FIELDS) {
      const raw = it[role];
      if (isBlank(raw)) continue;
      const n = normNumber(raw);
      if (n === null) {
        if (soft) continue;                         // 检测结果允许「未检出 / 阴性」这类定性描述
        out.push(finding('P1', '数值为负或非法', it, undefined,
          `${who(it)}：「${label}」的值「${String(raw).trim()}」不是可识别的数字。`,
          '数量必须是纯数字（如 3 / 18）；写成「三」「壹拾捌」这类形态本工具一律不给结论。'));
        continue;
      }
      if (n < 0) {
        out.push(finding('P0', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是负数（${n}）—— 台账里的数量出现负数，通常是填反了或写成了红字。`,
          '确认是红字冲销还是填错方向；确属冲销的请写在备注里并保留原值，别直接改成正数。'));
      } else if (n === 0 && !soft) {
        out.push(finding('P1', '数值为负或非法', it, n,
          `${who(it)}：「${label}」是 0 —— 数量为零说明这本台账根本没覆盖到任何水箱 / 检测记录，口径上不成立。`,
          '按实际覆盖范围填真实的个数；确实还没有水箱的要先确认这本台账是不是空表，别用 0 顶过去。'));
      }
    }
  }
  return out;
}

/* ============================ 入口 ============================ */

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  if (!String(text).trim()) {
    return insufficient(['原文（text）：一张含表头的二次供水清洗消毒与水质检测台账']);
  }

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）：一张含表头的二次供水清洗消毒与水质检测台账']);
  }
  if (t.error === 'no_header') {
    return insufficient([
      `含表头的二次供水清洗消毒与水质检测台账（至少要能认出「${REQUIRED_ROLES.map((r) => LABELS[r]).join('」「')}」）`,
      t.missingRoles.length
        ? `本次没认出来的必需列：${t.missingColumns.join('、')}`
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.detail.length) {
    return insufficient(['至少一行水箱检测明细（现在只有表头或只有合计行，没有可核对的水箱）']);
  }

  const base = baseDateOf(t.items);
  const findings = [];
  const notRun = [];

  for (const f of checkCleanCycle(t.items, base)) findings.push(f);
  for (const f of checkTestItemsAndLimits(t.items)) findings.push(f);
  for (const f of checkCleaningQualification(t.items, base)) findings.push(f);
  for (const f of checkDuplicateCleaning(t.items)) findings.push(f);
  for (const f of checkTotals(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  // 免费档：完整档追加的那五项检查一项都不执行，这里**如实记下来**（只记「没做」，绝不伪造结论）
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const overdueRows = findings.filter((f) => f.category === '清洗超期');
  const cleanOverdueMax = overdueRows.reduce((m, f) => Math.max(m, f.diff || 0), 0);
  const communities = new Set(t.detail.map((it) => cell(it, 'community')).filter(Boolean));

  const result = {
    findings,
    summary: {
      rows: t.detail.length,
      total_rows: t.totalRows.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      communities: communities.size,
      water_tanks: t.totals.tankCount,
      test_records: t.totals.itemCount,
      clean_overdue_tanks: overdueRows.length,
      clean_overdue_days_max: cleanOverdueMax,
      check_date: base,
      basis: '核对基准日（表内「核对基准日」，逐行为准、缺行用表内第一个）− 上次清洗日期 ≤ 180 天，才算清洗周期被覆盖；'
        + '「下次清洗日期」必须等于「上次清洗日期 + 180 天」；'
        + '按水箱核对常规指标子集（色度 / 浑浊度 / pH / 游离余氯 / 菌落总数 / 总大肠菌群）是否齐全，'
        + '并逐项判定检测结果是否越过限值（单值按上限、区间按上下限、带比较符按对应边界、「不得检出」按定性）；'
        + '清洗单位 / 清洗人员不得空缺，健康证有效期要覆盖本次清洗作业日；'
        + '同一水箱编号 + 同一上次清洗日期下不得出现矛盾的清洗单位 / 清洗人员；'
        + '合计行的水箱数 = 不重复水箱编号个数、检测项数 = 明细行数；'
        + '供水状态只认 在供水 / 停用 / 废弃 三个值。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次**实际执行**的全部检查项都通过了。这只说明**这本台账按上面写明的口径算得对、'
      + '清洗周期与检测项目 / 限值都对得上**，不代表水箱现场真的已经清洗过、'
      + '不代表水样采集与实验室检测过程规范、也不代表清洗单位资质与健康证的真伪已经核验 —— 那些不在本工具范围内。'
      + '（本次没有执行的检查项见 checks_not_run：未执行 ≠ 没问题。）';
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.detail.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    water_tanks: t.totals.tankCount,
    test_records: t.totals.itemCount,
    check_date: base,
  };
  result.scope = scope;

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, normDate, round2, isBlank, splitRow, addDays, judgeResult, parseLimit, tankGroups, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, REQUIRED_TEST_ITEMS, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
