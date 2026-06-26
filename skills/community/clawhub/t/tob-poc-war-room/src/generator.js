#!/usr/bin/env node

/**
 * tob-poc-war-room — POC 战情室 v1.0.0
 *
 * 基于多行业 ToB POC 交付实战经验萃取（去敏）
 * 不是 POC 项目管理模板，是"只有真干过 POC 的人才知道"的节奏控制和排兵布阵
 *
 * 输入：行业 / POC 目标 / 当前天数 / 问题清单
 * 输出：POC 健康度评估 + 48h 排兵布阵 + 签约路径预判
 */

const readline = require('readline');

// ═══════════════════════════════════════════════════════════
// 行业 POC 特征库
// ═══════════════════════════════════════════════════════════

const INDUSTRY_POC = {
  政务: {
    typicalDuration: '4-8 周',
    keyMetrics: ['政策问答准确率', '响应时间', '用户满意度'],
    decisionChain: '业务处室 → IT 部门 → 分管领导 → 一把手',
    typicalStakeholders: ['业务使用人', '技术评估人', '预算决策人'],
    riskFactors: [
      '政策合规审查拖延（新增法规突然要求审查）',
      '领导更换/调岗导致决策链断裂',
      '预算周期错过（财政年度结束前必须走完流程）',
    ],
    demoTips: '领导只看结果，不看过程。演示必须 15 分钟内展示核心价值',
    dataPrep: '政策文件相对标准，但旧政策清理和版本管理是难点',
    competitorAware: '政务项目常有"关系户"，纯技术 POC 不保证签单',
    caseStudy: {
      summary: '某市政务智能客服 POC，6 周周期',
      problem: '第 2 周客户说数据下周给，实际等了 3 周；竞品同期跑 POC',
      fix: '① 自带脱敏样例数据先行演示 ② 锁定 3 个验收指标 ③ 第 3 天主动汇报进度给业务处室 ④ 提前触达分管领导',
      result: '以"政策准确率 89%"胜出，竞品 72%',
    },
  },
  金融: {
    typicalDuration: '8-12 周',
    keyMetrics: ['bad case 率', '合规通过率', '准确率'],
    decisionChain: '业务部门 → 风控合规 → IT → 分管副总',
    typicalStakeholders: ['业务使用人', '合规审查人', '技术评估人', '预算决策人'],
    riskFactors: [
      '合规审查周期极长（2-4 周起步）',
      '数据安全要求极高，POC 数据获取困难',
      'bad case 零容忍，一个错误可能终止整个 POC',
    ],
    demoTips: '先展示 bad case 防控能力，再展示准确率。金融客户最怕出错',
    dataPrep: '金融数据极度敏感，POC 通常需要脱敏或合成数据',
    competitorAware: '金融客户倾向已有合作关系的供应商，新进入者需要更亮眼的指标',
    caseStudy: {
      summary: '某券商智能投顾 POC，10 周周期',
      problem: '合规审查卡了 4 周，POC 进度严重滞后；同时竞品也在跑',
      fix: '① POC 前 2 周先跑合规预审 ② 自带脱敏数据+合成数据 ③ 每周向合规部门汇报进展 ④ 第 6 周安排高层演示',
      result: 'bad case 率 0.08%，合规一次通过，签单',
    },
  },
  教育: {
    typicalDuration: '4-6 周',
    keyMetrics: ['答案与教材一致率', '响应时间', '教师满意度'],
    decisionChain: '教研室 → 信息中心 → 分管校长 → 校长',
    typicalStakeholders: ['教师/教研员', '技术管理员', '校长/副校长'],
    riskFactors: [
      '教材版本混乱（新旧版并存）',
      '学期周期影响（寒暑假前决策加速/减速）',
      '教育预算审批流程长',
    ],
    demoTips: '让教师亲自试用，比演示给领导看更有说服力',
    dataPrep: '教材内容标准化程度高，但版本管理和知识点标注是难点',
    competitorAware: '教育行业竞品多，差异化在内容理解深度而非技术本身',
    caseStudy: {
      summary: '某教育出版社智能答疑 POC，5 周周期',
      problem: '教材版本不一致导致答案与教材不符，教师反馈差',
      fix: '① POC 前确认教材版本 ② 建立"答案来源标注"机制 ③ 邀请 3 位教师参与测试 ④ 第 4 周安排校长汇报',
      result: '答案一致率从 62% 提升至 94%，签单',
    },
  },
  零售: {
    typicalDuration: '2-4 周',
    keyMetrics: ['商品推荐准确率', '客服解决率', '响应时间'],
    decisionChain: '运营 → 技术 → VP → CEO',
    typicalStakeholders: ['运营人员', '技术对接人', '业务决策人'],
    riskFactors: [
      '商品知识库碎片化（SKU 信息散落在 Excel/PDF/系统）',
      '促销活动时效性强，POC 期间活动可能已过期',
      '零售客户决策快但要求也高，POC 周期短',
    ],
    demoTips: '用客户自己的商品数据演示，效果最直观',
    dataPrep: '商品数据量大但结构简单，快速整理 Top 100 SKU 即可启动 POC',
    competitorAware: '零售客户看重速度和效果，谁先跑出结果谁领先',
    caseStudy: {
      summary: '某鞋服品牌客服 RAG POC，3 周周期',
      problem: '客户商品数据散落在 3 个系统，POC 第 1 周还在整理数据',
      fix: '① 先拿 Top 100 SKU 跑通核心场景 ② 第 2 周展示推荐准确率 ③ 第 3 周安排运营团队试用 ④ 对比竞品方案差异',
      result: '商品推荐准确率 83%，3 周完成 POC 并签单',
    },
  },
};

const DEFAULT_POC = {
  typicalDuration: '4-8 周',
  keyMetrics: ['准确率', '响应时间', '用户满意度'],
  decisionChain: '业务 → IT → 决策层',
  typicalStakeholders: ['业务使用人', '技术评估人', '预算决策人'],
  riskFactors: [
    'POC 目标不清晰，验收标准模糊',
    '客户数据准备延迟',
    '竞品并行 POC',
  ],
  demoTips: '前 15 分钟展示核心价值',
  dataPrep: '确认数据格式和可用性',
  competitorAware: '关注竞品动态',
  caseStudy: null,
};

// ═══════════════════════════════════════════════════════════
// POC 阶段判定
// ═══════════════════════════════════════════════════════════

function determinePhase(day, industry) {
  const poc = INDUSTRY_POC[industry] || DEFAULT_POC;
  const durationWeeks = parseInt(poc.typicalDuration);
  const totalDays = durationWeeks * 7;

  if (day <= 3) return { name: '启动期', color: '🟢', phase: 'startup', criticalWindow: true };
  if (day <= totalDays * 0.3) return { name: '执行早期', color: '🟡', phase: 'early', criticalWindow: false };
  if (day <= totalDays * 0.7) return { name: '执行中期', color: '🟡', phase: 'mid', criticalWindow: false };
  if (day <= totalDays) return { name: '收尾期', color: '🟠', phase: 'closing', criticalWindow: true };
  return { name: '跟进期', color: '🔴', phase: 'followup', criticalWindow: true };
}

// ═══════════════════════════════════════════════════════════
// 风险等级评估
// ═══════════════════════════════════════════════════════════

function assessRisk(day, problems, industry, passRate, silenceDays, procurementPath) {
  const poc = INDUSTRY_POC[industry] || DEFAULT_POC;
  const riskItems = [];
  let riskScore = 0;

  const p = (problems || '').toLowerCase();
  const rate = Number.isFinite(passRate) ? passRate : null;
  const silentDays = Number.isFinite(silenceDays) ? silenceDays : null;
  const procurement = (procurementPath || '').trim();

  if (rate !== null) {
    if (rate >= 90) {
      riskItems.push({ level: '✅', factor: '通过率达到收口线', impact: '技术侧已具备进入签约推进的基础，前提是 P0 问题清零或有客户接受的 workaround', action: '准备 POC 一页纸复盘，并把剩余问题转为收口清单' });
    } else if (rate >= 70) {
      riskItems.push({ level: '🟡', factor: '通过率处于黄区', impact: '客户可能认可方向，但还不足以支撑签约动作', action: '未来 48 小时集中处理影响验收的 Top 2 问题' });
      riskScore += 2;
    } else {
      riskItems.push({ level: '🔴', factor: '通过率低于可收口线', impact: '此时谈合同会放大客户不信任，容易把 POC 变成失败样板', action: '暂停签约推进，重设验收指标并补齐核心场景' });
      riskScore += 4;
    }
  }

  if (silentDays !== null) {
    if (silentDays >= 7) {
      riskItems.push({ level: '🔴', factor: '客户沉默达到 7 天', impact: 'POC 成功后沉默不是中性信号，通常意味着内部 buying process 无 owner 或竞品介入', action: '当天触达 champion，要求安排决策人/采购路径确认；同步触发 poc-to-contract-closer' });
      riskScore += 3;
    } else if (silentDays >= 3) {
      riskItems.push({ level: '🟡', factor: '客户沉默达到 3 天', impact: '需要主动维持势能，不能等客户自然回复', action: '发送 POC 进展/结果摘要，明确约下一步会议或确认阻塞' });
      riskScore += 1;
    }
  }

  if (rate !== null && rate >= 90 && !procurement) {
    riskItems.push({ level: '🟡', factor: '采购路径未知', impact: 'POC 结果好但 buying process 没 owner，报价和合同节点容易空转', action: '触发 poc-to-contract-closer，先确认招投标/比价/单一来源/框架协议/续约路径' });
    riskScore += 2;
  }

  if (/数据.*未.*到|数据.*没.*有|数据.*延迟|数据.*不到位|数据.*明天|客户说.*数据|数据.*下周|数据.*再给/.test(p)) {
    riskItems.push({ level: '🔴', factor: '数据未到位', impact: 'POC 最大瓶颈，80% 延期源于此', action: '自带脱敏样例数据先行推进；同时明确客户数据交付 deadline' });
    riskScore += 3;
  }
  if (/竞品|对手|也在跑|同时/.test(p)) {
    riskItems.push({ level: '🟡', factor: '竞品并行 POC', impact: '胜负手不是功能多少，是最痛痛点谁解决得最好', action: '锁定客户最痛的 1-2 个点，集中资源打出优势' });
    riskScore += 2;
  }
  if (/目标.*不清|指标.*多|验收.*模糊|需求.*变更/.test(p)) {
    riskItems.push({ level: '🔴', factor: 'POC 目标不清', impact: '超过 3 个指标说明没搞清楚客户真正关心什么', action: '立即与客户对齐，锁定 ≤3 个可量化验收指标' });
    riskScore += 3;
  }
  if (/合规|审查|审批/.test(p)) {
    riskItems.push({ level: '🟡', factor: '合规/审批流程', impact: '合规审查通常 2-4 周，是最大时间不确定因素', action: 'POC 启动前先跑合规预审；每周向合规部门汇报进展' });
    riskScore += 2;
  }
  if (/领导|决策人|一把手|校长|VP|CEO/.test(p)) {
    riskItems.push({ level: '🟡', factor: '决策人未触达', impact: 'POC 结果好不等于签单，必须搞定决策链', action: '安排高层演示，直接触达最终决策人' });
    riskScore += 2;
  }
  if (/沉默|没回复|不响应|没消息/.test(p)) {
    if (day > 7) {
      riskItems.push({ level: '🔴', factor: 'POC 后沉默 >7 天', impact: '7 天沉默 = 死单预警，客户可能已选竞品或放弃', action: '第 3 天就应主动触达；现在立即联系业务对接人' });
      riskScore += 3;
    } else {
      riskItems.push({ level: '🟡', factor: '客户响应变慢', impact: '可能内部在讨论或竞品在介入', action: '主动发送 POC 进展简报，保持存在感' });
      riskScore += 1;
    }
  }
  if (/演示.*失败|演示.*不好|demo.*差/.test(p)) {
    riskItems.push({ level: '🔴', factor: '演示效果不佳', impact: '客户记住的是演示时的体验，不是 PPT', action: '重新准备演示脚本，聚焦前 15 分钟核心价值' });
    riskScore += 3;
  }

  // 阶段风险加成
  const phase = determinePhase(day, industry);
  if (phase.phase === 'followup' && day > 14) {
    riskItems.push({ level: '🔴', factor: 'POC 完成但长时间未推进', impact: 'POC 后 7 天沉默 = 危险信号', action: '立即启动签约推进 6 步法（见 poc-to-contract-closer）' });
    riskScore += 2;
  }

  let riskLevel;
  if (riskScore >= 6) riskLevel = { label: '高', color: '🔴' };
  else if (riskScore >= 3) riskLevel = { label: '中', color: '🟡' };
  else if (riskScore >= 1) riskLevel = { label: '低', color: '🟢' };
  else riskLevel = { label: '无', color: '✅' };

  return { riskItems, riskScore, riskLevel, phase };
}

// ═══════════════════════════════════════════════════════════
// 48h 排兵布阵
// ═══════════════════════════════════════════════════════════

function generate48hPlan(phase, riskItems, industry, problems) {
  const poc = INDUSTRY_POC[industry] || DEFAULT_POC;
  const actions = [];

  if (phase.phase === 'startup') {
    actions.push({
      time: 'Day 1',
      priority: 'P0',
      action: '锁定 POC 目标',
      detail: `与客户对齐并书面确认 ≤3 个可量化验收指标。示例：${poc.keyMetrics.join('、')}`,
      owner: '业务对接人 + 项目经理',
    });
    actions.push({
      time: 'Day 1-2',
      priority: 'P0',
      action: '数据到位确认',
      detail: '确认客户数据格式、内容、可用性。如数据未就绪，准备脱敏样例先行',
      owner: '技术团队',
    });
    actions.push({
      time: 'Day 2',
      priority: 'P1',
      action: '决策链映射',
      detail: `绘制决策链：${poc.decisionChain}，确认当前已触达的角色和待触达的角色`,
      owner: '销售/商务',
    });
    actions.push({
      time: 'Day 2-3',
      priority: 'P1',
      action: '演示脚本准备',
      detail: poc.demoTips,
      owner: '技术+演示负责人',
    });
  } else if (phase.phase === 'early' || phase.phase === 'mid') {
    actions.push({
      time: 'Today',
      priority: 'P0',
      action: '进度汇报',
      detail: '向客户业务对接人发送 POC 进展简报（本周做了什么、下周计划、风险/阻塞）',
      owner: '项目经理',
    });
    actions.push({
      time: 'Today',
      priority: 'P0',
      action: '问题清零',
      detail: '梳理当前未解决的问题清单，按影响程度排序，集中资源解决 Top 2',
      owner: '技术团队',
    });
    actions.push({
      time: 'Within 48h',
      priority: 'P1',
      action: '高层演示安排',
      detail: `安排一次面向决策层的演示，触达：${poc.typicalStakeholders[poc.typicalStakeholders.length - 1]}`,
      owner: '销售/商务',
    });
    if (problems && /竞品/.test(problems)) {
      actions.push({
        time: 'Within 48h',
        priority: 'P1',
        action: '竞品差异化分析',
        detail: '梳理我们与竞品在客户最痛痛点上的差异，准备对比话术',
        owner: '售前+销售',
      });
    }
  } else if (phase.phase === 'closing') {
    actions.push({
      time: 'Today',
      priority: 'P0',
      action: '验收指标核对',
      detail: `逐项核对 POC 验收指标：${poc.keyMetrics.join('、')}，准备验收报告`,
      owner: '技术团队+项目经理',
    });
    actions.push({
      time: 'Today',
      priority: 'P0',
      action: '启动签约推进',
      detail: 'POC 验收通过后立即启动 poc-to-contract-closer 六步法，不要等客户主动',
      owner: '销售',
    });
    actions.push({
      time: 'Within 48h',
      priority: 'P1',
      action: '决策人汇报',
      detail: '安排面向最终决策人的 POC 结果汇报，准备一页纸汇报材料',
      owner: '销售+项目经理',
    });
  } else {
    actions.push({
      time: 'Immediately',
      priority: 'P0',
      action: '紧急触达',
      detail: 'POC 后长时间未推进，立即联系业务对接人了解最新状态',
      owner: '销售',
    });
    actions.push({
      time: 'Within 24h',
      priority: 'P0',
      action: '激活沉默客户',
      detail: '发送 POC 结果回顾+下一步建议，附带一个"限时"价值点（如免费上线支持）',
      owner: '销售',
    });
  }

  return actions;
}

// ═══════════════════════════════════════════════════════════
// 生成报告
// ═══════════════════════════════════════════════════════════

function generateReport(config) {
  const { industry, objective, day, problems, passRate, silenceDays, procurementPath } = config;
  const poc = INDUSTRY_POC[industry] || DEFAULT_POC;
  const { phase, riskLevel, riskItems, riskScore } = assessRisk(day || 0, problems, industry, passRate, silenceDays, procurementPath);
  const plan48h = generate48hPlan(phase, riskItems, industry, problems);

  const lines = [];

  // 标题
  lines.push('# 🔥 POC 战情室报告');
  lines.push('');
  lines.push(`> 行业：${industry || '未指定'}`);
  if (objective) lines.push(`> POC 目标：${objective}`);
  lines.push(`> 当前进度：第 ${day || 0} 天（${phase.name}）`);
  if (Number.isFinite(passRate)) lines.push(`> 当前通过率：${passRate}%`);
  if (Number.isFinite(silenceDays)) lines.push(`> 客户沉默：${silenceDays} 天`);
  lines.push(`> 采购路径：${procurementPath || '未知'}`);
  lines.push(`> 典型周期：${poc.typicalDuration}`);
  lines.push('');

  // 模块 1：健康度评估
  lines.push('## 一、POC 健康度评估');
  lines.push('');
  lines.push(`| 维度 | 状态 | 详情 |`);
  lines.push(`|------|------|------|`);
  lines.push(`| 当前阶段 | ${phase.color} ${phase.name} | ${phase.criticalWindow ? '⚠️ 关键窗口期' : ''} |`);
  lines.push(`| 风险等级 | ${riskLevel.color} ${riskLevel.label} | 风险分 ${riskScore} |`);
  lines.push(`| 决策链 | ${poc.decisionChain} | ${poc.typicalStakeholders.join(' → ')} |`);
  lines.push(`| 关键指标 | - | ${poc.keyMetrics.join('、')} |`);
  lines.push('');

  if (riskItems.length > 0) {
    lines.push('### ⚠️ 风险项');
    lines.push('');
    riskItems.forEach((item) => {
      lines.push(`- ${item.level} **${item.factor}**`);
      lines.push(`  - 影响：${item.impact}`);
      lines.push(`  - 建议：${item.action}`);
      lines.push('');
    });
  }

  // 模块 2：48h 排兵布阵
  lines.push('## 二、48h 排兵布阵');
  lines.push('');
  lines.push('| 时间 | 优先级 | 行动 | 负责人 |');
  lines.push('|------|--------|------|--------|');
  plan48h.forEach((a) => {
    lines.push(`| ${a.time} | ${a.priority} | **${a.action}**<br/>${a.detail} | ${a.owner} |`);
  });
  lines.push('');

  // 模块 3：POC 节奏控制
  lines.push('## 三、POC 节奏控制');
  lines.push('');
  lines.push('### 关键里程碑');
  lines.push('');
  lines.push('- [ ] **Kickoff**：POC 目标书面确认（≤3 个指标）');
  lines.push('- [ ] **Day 3**：数据到位 + 首次进展汇报');
  lines.push('- [ ] **Day 7**：中期进展汇报（含风险/阻塞）');
  lines.push('- [ ] **演示日**：面向决策层的正式演示');
  lines.push('- [ ] **验收日**：验收指标逐项核对签字');
  lines.push('- [ ] **POC 后第 3 天**：主动触达客户，启动签约推进');
  lines.push('- [ ] **POC 后第 7 天**：如未推进，启动死单预警');
  lines.push('');

  lines.push('### 客户沟通节奏');
  lines.push('');
  lines.push(`- **启动期**：每天简短同步进展，建立信任`);
  lines.push(`- **执行期**：每周正式汇报一次（进展+风险+下周计划）`);
  lines.push(`- **收尾期**：每 2 天同步一次验收进度`);
  lines.push(`- **跟进期**：POC 后第 3 天必须主动触达，不要等客户找你`);
  lines.push('');

  if (problems && /竞品/.test(problems)) {
    lines.push('### 🏁 竞品应对');
    lines.push('');
    lines.push('- **不是比功能多** — 比的是客户最痛的那个点谁解决得最好');
    lines.push('- **锁定 1-2 个差异化优势** — 集中资源打出亮点');
    lines.push('- **提前触达决策人** — 不要只跟技术对接人沟通，决策人可能不看 POC 报告');
    lines.push(`- ${poc.competitorAware}`);
    lines.push('');
  }

  // 模块 4：签约路径预判
  lines.push('## 四、签约路径预判');
  lines.push('');

  if ((Number.isFinite(passRate) && passRate >= 90) || (Number.isFinite(silenceDays) && silenceDays >= 7) || (phase.phase === 'followup' && day > 7)) {
    lines.push('⚠️ **当前状态：POC 后长时间未推进，签单风险高**');
    lines.push('');
    lines.push('建议立即启动 poc-to-contract-closer 六步法：');
    lines.push('1. 数据达标确认 → 2. 问题清零 → 3. 决策人触达 → 4. 采购路径确认 → 5. 一页纸汇报/报价 → 6. 上线窗口');
    lines.push('');
    if (!procurementPath) {
      lines.push('采购路径当前未知：先确认招投标/比价/单一来源/框架协议/续约路径，不要直接丢报价。');
    }
    lines.push('');
  } else if (phase.phase === 'closing') {
    lines.push('✅ **当前状态：POC 收尾阶段，准备启动签约推进**');
    lines.push('');
    lines.push('验收通过后 48h 内启动签约推进，不要等客户主动。');
    lines.push('');
  } else if (phase.phase === 'startup') {
    lines.push('🟢 **当前状态：POC 启动阶段**');
    lines.push('');
    lines.push('前 48 小时是关键。锁定目标、数据到位、演示准备三件事并行推进。');
    lines.push('');
  } else {
    lines.push(`🟡 **当前状态：POC 执行中，第 ${day} 天**`);
    lines.push('');
    lines.push('保持节奏，每周汇报，问题清零。关注客户决策链触达情况。');
    lines.push('');
  }

  // 模块 5：立即可执行的 3 步
  lines.push('## 五、立即可执行的 3 步行动');
  lines.push('');

  const topActions = plan48h.filter(a => a.priority === 'P0').slice(0, 3);
  if (topActions.length < 3) {
    const p1Actions = plan48h.filter(a => a.priority === 'P1').slice(0, 3 - topActions.length);
    topActions.push(...p1Actions);
  }

  topActions.forEach((a, i) => {
    lines.push(`${i + 1}. **${a.action}**（${a.time}，${a.owner}）`);
    lines.push(`   ${a.detail}`);
    lines.push('');
  });

  lines.push('## 六、回退路径');
  lines.push('');
  lines.push('- 如果 `poc-to-contract-closer` 判定 P0 未清、通过率不足或验收证据缺失，立即回到本 war-room。');
  lines.push('- 回退后只做 48h 问题清零、验收证据补齐、客户沟通节奏恢复，不推进报价。');
  lines.push('');

  // 实战案例
  if (poc.caseStudy) {
    lines.push('---');
    lines.push('');
    lines.push(`## 📌 ${industry}行业 POC 实战案例`);
    lines.push('');
    lines.push(`**案例**：${poc.caseStudy.summary}`);
    lines.push('');
    lines.push(`**问题**：${poc.caseStudy.problem}`);
    lines.push('');
    lines.push(`**解决方案**：${poc.caseStudy.fix}`);
    lines.push('');
    lines.push(`**结果**：${poc.caseStudy.result}`);
    lines.push('');
  }

  // 数据来源
  lines.push('---');
  lines.push('');
  lines.push('> 💡 规则来源：多行业 ToB POC 交付实战经验（去敏）。每条规则来自真实踩坑，不是教科书理论。');
  lines.push('> ⚠️ 本报告为诊断和排兵布阵参考，实际执行需结合项目具体情况。');
  lines.push('');

  return lines.join('\n');
}

// ═══════════════════════════════════════════════════════════
// 交互模式
// ═══════════════════════════════════════════════════════════

function interactiveMode() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (question) => new Promise((resolve) => rl.question(question, resolve));

  (async () => {
    console.log('\n🔥 POC 战情室 — 输入 POC 信息，输出排兵布阵方案\n');

    const industry = await ask('行业（政务/金融/教育/零售，回车跳过）：');
    const objective = await ask('POC 目标（如"政策问答准确率 >80%"）：');
    const dayStr = await ask('当前第几天（如 3 表示第 3 天）：');
    const problems = await ask('当前问题（多个用逗号分隔，如"数据未到位,竞品也在跑"）：');
    const procurementPath = await ask('采购路径（招投标/比价/单一来源/框架协议/未知，回车跳过）：');

    const report = generateReport({
      industry: industry.trim() || null,
      objective: objective.trim() || null,
      day: parseInt(dayStr) || 0,
      problems: problems.trim() || null,
      procurementPath: procurementPath.trim() || null,
    });
    console.log('\n' + report);
    rl.close();
  })();
}

// ═══════════════════════════════════════════════════════════
// 主入口
// ═══════════════════════════════════════════════════════════

function parseArgs(argv) {
  const args = { industry: null, objective: null, day: 0, problems: null, passRate: null, silenceDays: null, procurementPath: null };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--industry': args.industry = argv[++i]; break;
      case '--objective': args.objective = argv[++i]; break;
      case '--day': args.day = parseInt(argv[++i]) || 0; break;
      case '--problems': args.problems = argv[++i]; break;
      case '--pass-rate': args.passRate = Number.parseFloat(argv[++i]); break;
      case '--silence-days': args.silenceDays = Number.parseFloat(argv[++i]); break;
      case '--procurement-path': args.procurementPath = argv[++i]; break;
      case '--help': case '-h': printHelp(); process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(`
tob-poc-war-room — POC 战情室 v1.0.0

用法:
  tob-poc-war-room                                          # 交互模式
  tob-poc-war-room --industry "政务" --objective "政策问答准确率>80%" \\
    --day 3 --problems "数据未到位,竞品也在跑"

参数:
  --industry   行业（政务/金融/教育/零售）
  --objective  POC 目标
  --day        当前第几天
  --problems   当前问题（逗号分隔）
  --pass-rate  当前通过率百分比，例如 93
  --silence-days 客户最近沉默天数，例如 7
  --procurement-path 采购路径，例如 招投标/比价/单一来源/框架协议/续约

行业支持：政务、金融、教育、零售
`);
}

if (require.main === module) {
  const args = parseArgs(process.argv);
  if (!args.industry && !args.objective && !args.problems && !Number.isFinite(args.passRate) && !Number.isFinite(args.silenceDays) && !args.procurementPath) {
    interactiveMode();
  } else {
    console.log(generateReport(args));
  }
}

module.exports = {
  assessRisk,
  determinePhase,
  generate48hPlan,
  generateReport,
  parseArgs,
};
