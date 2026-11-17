#!/usr/bin/env node

/**
 * tob-poc-budget-justify — POC 预算论证助手
 *
 * 基于ToB 项目经验萃取的规则（去敏）
 *
 * 输入：客户名称 / 行业 / POC目标 / 预算范围 / 决策人角色
 * 输出：POC 范围界定 + 资源估算 + 预算论证（Markdown 5模块）
 *
 * 核心经验来源：
 *   - 某大型文化集团实战：POC 72h 快速响应闭环，93% 通过率
 *   - 某零售 IT 服务商项目："边界验证法" — 先列 3 个"不做什么"
 *   - 某政务集成项目：POC 超过 3 周变项目，失去验证意义
 *
 * 降级策略：
 *   1. 有同行业 POC 经验 → 引用真实模式（去敏）
 *   2. 无匹配 → 通用 POC 框架
 */

const readline = require('readline');

// ── CLI 参数解析 ──

function parseArgs(argv) {
  const args = {
    client: null,
    industry: null,
    pocGoal: null,
    budget: null,
    decisionMaker: null,
    quick: false,
  };

  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--client': args.client = argv[++i]; break;
      case '--industry': args.industry = argv[++i]; break;
      case '--poc-goal': args.pocGoal = argv[++i]; break;
      case '--budget': args.budget = argv[++i]; break;
      case '--decision-maker': args.decisionMaker = argv[++i]; break;
      case '--quick': args.quick = true; break;
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(`
tob-poc-budget-justify — POC 预算论证助手

用法:
  tob-poc-budget-justify                                    # 交互模式
  tob-poc-budget-justify --client "某零售集团" --industry "零售" \\
    --poc-goal "验证AI客服能否替代人工处理80%常见问题" \\
    --budget "10万以内" --decision-maker "IT总监"
  tob-poc-budget-justify --quick --client "某客户" --poc-goal "试试效果"

参数:
  --client         客户名称（必填）
  --industry       客户所在行业（可选）
  --poc-goal       POC 验证目标（可选）
  --budget         预算范围（可选）
  --decision-maker 决策人角色（可选）
  --quick          快速模式：输出精简论证报告
`);
}

// ── ToB 项目经验萃取规则（去敏） ──

// 零售行业 POC 经验（萃取自某零售 IT 服务商项目）
const RETAIL_POC_EXPERIENCE = {
  typicalScope: '智能客服+订单关怀+商品推荐（不超过 2 个核心场景）',
  typicalDuration: '2-3 周',
  typicalTeam: '1PM + 1开发 + 1测试',
  typicalCost: '3-8万',
  successMetric: '客服分流率 ≥ 60%，准确率 ≥ 85%',
  lesson: '零售 POC 容易被客户用真实客诉淹没。某项目 POC 第一天涌入 500 条真实客诉，差点崩盘。教训：POC 前必须准备测试数据集，不能用生产数据。',
  budgetTrick: '零售客户对价格敏感。用"边界验证法"：先列 3 个"不做什么"，客户才会认真谈预算。某项目客户说"先试试"，我们用这方法让客户意识到 POC 需要投入，最终 POC 预算 8 万，签单 50 万。',
  timeline: '零售 POC 超 3 周就变项目。某项目 POC 做到第 4 周，客户开始提新需求，POC 失去验证意义。',
};

// 金融/银行行业 POC 经验
const FINANCE_POC_EXPERIENCE = {
  typicalScope: '智能客服+风险评估+工单流转（安全合规优先）',
  typicalDuration: '3-4 周',
  typicalTeam: '1PM + 2开发 + 1安全 + 1测试',
  typicalCost: '8-15万',
  successMetric: '风险评估准确率 ≥ 90%，合规审计通过',
  lesson: '金融 POC 安全合规要求高。某项目 POC 前没确认数据脱敏方案，测试用真实客户数据，被合规部门叫停，POC 延期 2 周。教训：POC 前先过安全审计。',
  budgetTrick: '金融客户预算充足但决策慢。低价竞品切入时，强调"安全投入 = 合规保障"。某项目竞品报价低 40%，但安全方案不完善，客户最终选了贵的。',
  timeline: '金融 POC 审批流程长，需预留 1-2 周审批时间。实际开发 3 周 + 审批 2 周 = 总周期 5 周。',
};

// 政务/央企行业 POC 经验
const GOV_POC_EXPERIENCE = {
  typicalScope: '智能问答+工单分派+知识库（领导看板优先）',
  typicalDuration: '4-6 周',
  typicalTeam: '1PM + 2开发 + 1安全 + 1实施',
  typicalCost: '10-20万',
  successMetric: '问答准确率 ≥ 80%，安全审计通过，领导满意度 ≥ 4/5',
  lesson: '政务 POC 最终是汇报给领导看的。某项目 POC 技术指标全达标，但领导看不懂，差点黄了。教训：POC 交付物里必须有"领导能看懂的看板"。',
  budgetTrick: '政务项目低价中标常见，但"政治风险"比价格更重要。提醒客户："低价中标看似省钱，但上线后领导不满意，谁承担政治风险？"',
  timeline: '政务 POC 审批流程最长，通常 4-6 周。含：需求确认 1 周 + 开发 2 周 + 安全审计 1 周 + 领导汇报 1 周 + 验收 1 周。',
};

// 通用 POC 框架
const GENERIC_POC_EXPERIENCE = {
  typicalScope: '核心功能验证（不超过 3 个场景）',
  typicalDuration: '2-3 周',
  typicalTeam: '1PM + 1开发 + 1测试',
  typicalCost: '3-8万',
  successMetric: '功能验证通过率 ≥ 80%，客户满意度 ≥ 4/5',
  lesson: 'POC 范围容易膨胀。客户说"顺便试试这个"，POC 就变项目了。教训：POC 前先签边界协议。',
  budgetTrick: '客户说"先试试"时，用边界验证法：先列 3 个"不做什么"，客户才会认真谈预算。',
  timeline: 'POC 超 3 周就变项目，失去验证意义。',
};

// 某大型文化集团实战经验：POC 快速响应闭环
const POC_72H_RULE = {
  formula: '转化率 = 响应速度 × 根因准确率 × 客户感知度',
  fourSteps: [
    '接球（<2h）：收到问题立即响应，告诉客户"收到了，正在处理"',
    '拆解（2-8h）：定位根因，给出初步方案',
    '修复（8-48h）：执行修复，同步进度',
    '闭环（48h）：确认解决，记录经验',
  ],
  lesson: '某文化集团项目 5 个问题 48h 解决 4 个，93% POC 通过率。关键：快速响应 + 透明沟通。',
  warning: 'POC 后 72h 无决策 owner 推动 → 必须标挂起 + 汇报，不可被动等待。',
};

// 根据行业获取经验
function getExperience(industry) {
  const map = {
    '零售': RETAIL_POC_EXPERIENCE,
    '鞋服': RETAIL_POC_EXPERIENCE,
    '金融': FINANCE_POC_EXPERIENCE,
    '银行': FINANCE_POC_EXPERIENCE,
    '政务': GOV_POC_EXPERIENCE,
    '央企': GOV_POC_EXPERIENCE,
    '政府': GOV_POC_EXPERIENCE,
  };
  return map[industry] || GENERIC_POC_EXPERIENCE;
}

// 根据 POC 目标识别验证类型
function detectPocType(goal) {
  if (!goal) return 'exploratory';
  const g = goal.toLowerCase();
  if (/替代|人工|自动化/.test(g)) return 'automation';
  if (/准确|识别|智能/.test(g)) return 'accuracy';
  if (/效率|速度|时间/.test(g)) return 'efficiency';
  if (/成本|省钱|预算|roi/.test(g)) return 'cost';
  if (/体验|满意|反馈/.test(g)) return 'experience';
  return 'exploratory';
}

// 根据验证类型生成成功标准
function getSuccessCriteria(pocType, industry) {
  const exp = getExperience(industry);
  const base = {
    automation: {
      metric: '自动化率',
      target: '≥ 60%（首月）/ ≥ 80%（优化后）',
      measurement: '对比人工处理量 vs 系统处理量',
    },
    accuracy: {
      metric: '准确率',
      target: '≥ 85%（行业基准）',
      measurement: '标注测试集验证 + 人工抽样复核',
    },
    efficiency: {
      metric: '处理效率',
      target: '响应时间 < 2秒，吞吐量 ≥ 100/分钟',
      measurement: '压力测试 + 实际业务数据对比',
    },
    cost: {
      metric: '成本节约',
      target: '运营成本降低 ≥ 30%',
      measurement: 'POC 前后成本对比',
    },
    experience: {
      metric: '客户满意度',
      target: 'NPS ≥ 40，满意度 ≥ 4/5',
      measurement: 'POC 结束后客户调研',
    },
    exploratory: {
      metric: '功能验证通过率',
      target: '≥ 80%（核心功能全部可用）',
      measurement: '功能清单逐项验证',
    },
  };
  return base[pocType] || base.exploratory;
}

// 根据行业生成资源估算
function getResourceEstimate(industry) {
  const exp = getExperience(industry);
  const isGov = ['政务', '央企', '政府'].includes(industry);
  const isFinance = ['金融', '银行'].includes(industry);

  const phases = [
    { phase: '需求确认', days: '1-2天', role: 'PM', deliverable: 'POC 需求文档' },
    { phase: '环境准备', days: '2-3天', role: '开发', deliverable: 'POC 环境搭建' },
    { phase: '功能开发', days: isGov ? '8-10天' : '5-7天', role: '开发', deliverable: 'POC 功能实现' },
    { phase: '测试验证', days: isGov ? '5-7天' : '3-5天', role: '测试', deliverable: '测试报告' },
    { phase: '客户验收', days: isGov ? '5天' : '2-3天', role: 'PM + 客户', deliverable: '验收报告' },
  ];

  if (isGov) {
    phases.splice(2, 0, { phase: '安全审计', days: '5天', role: '安全', deliverable: '安全审计报告' });
    phases.push({ phase: '领导汇报', days: '3天', role: 'PM', deliverable: '领导看板 + 汇报 PPT' });
  }
  if (isFinance) {
    phases.splice(2, 0, { phase: '安全审计', days: '5天', role: '安全', deliverable: '合规审计报告' });
  }

  return { phases, profile: exp };
}

// 生成预算论证话术
function getBudgetArguments(budget, client, industry) {
  const exp = getExperience(industry);
  const args = [];

  if (budget && (budget.includes('免费') || budget.includes('不要'))) {
    args.push(`「POC 不是免费试用，是双方投入的验证实验。我们投入人力、时间、技术资源，这些都有成本。」`);
    args.push(`**经验教训**：${exp.budgetTrick}`);
  } else if (budget) {
    args.push(`「您给的预算是 ${budget}，在 ${industry || '该'} 行业 POC 中属于 ${parseFloat(budget) < 5 ? '偏低' : '合理'} 范围。」`);
    args.push(`**经验教训**：${exp.budgetTrick}`);
  } else {
    args.push(`**经验教训**：${exp.budgetTrick}`);
  }

  args.push(`「POC 成功后，项目投入通常是 POC 的 5-10 倍。现在的投入是在验证那 5-10 倍是否值得。」`);

  return args;
}

// ── 生成论证报告 ──

function generateReport(config) {
  const { client, industry, pocGoal, budget, decisionMaker } = config;
  const pocType = detectPocType(pocGoal);
  const criteria = getSuccessCriteria(pocType, industry);
  const resources = getResourceEstimate(industry);
  const budgetArgs = getBudgetArguments(budget, client, industry);
  const exp = getExperience(industry);

  const lines = [];

  // 标题
  lines.push(`# 📋 POC 预算论证报告`);
  lines.push('');
  lines.push(`> 客户：${client || '未指定'}`);
  if (industry) lines.push(`> 行业：${industry}`);
  if (pocGoal) lines.push(`> POC 目标：${pocGoal}`);
  if (budget) lines.push(`> 客户预算：${budget}`);
  if (decisionMaker) lines.push(`> 决策人：${decisionMaker}`);
  lines.push(`> 验证类型：${pocType}`);
  lines.push('');

  // 模块 1：POC 目标对齐
  lines.push(`## 🎯 POC 目标对齐`);
  lines.push('');
  if (pocGoal) {
    lines.push(`- **客户表面诉求**：${pocGoal}`);
    if (/替代|人工/.test(pocGoal)) {
      lines.push(`- **客户真实诉求**：降低人工成本，提升处理效率`);
    } else if (/准确|识别/.test(pocGoal)) {
      lines.push(`- **客户真实诉求**：验证 AI 能力是否可靠，降低决策风险`);
    } else if (/试试|看看/.test(pocGoal)) {
      lines.push(`- **客户真实诉求**：不确定 AI 能否解决问题，需要眼见为实`);
    } else {
      lines.push(`- **客户真实诉求**：待进一步沟通确认`);
    }
    lines.push(`- **风险提示**：${exp.lesson}`);
  } else {
    lines.push(`- **客户表面诉求**：未明确`);
    lines.push(`- **客户真实诉求**：不确定 AI 能否解决业务问题，需要验证`);
    lines.push(`- **风险提示**：${exp.lesson}`);
  }
  lines.push('');

  // 模块 2：POC 范围界定
  lines.push(`## 📏 POC 范围界定`);
  lines.push('');
  lines.push(`**核心原则**：POC 不是免费试用，是有边界的验证实验。`);
  lines.push('');
  lines.push(`| 范围 | 做什么 | 不做什么 | 原因 |`);
  lines.push(`|------|--------|----------|------|`);
  lines.push(`| 核心场景 | ${exp.typicalScope} 中的 1-2 个关键场景 | 全功能覆盖 | POC 超 3 个场景 = 项目 |`);
  lines.push(`| 数据规模 | 测试数据集（100-500 条样本） | 客户全量生产数据 | 数据安全 + 准备成本 |`);
  lines.push(`| 集成范围 | 1-2 个关键系统接口 | 全系统对接 | 接口复杂度不可控 |`);
  lines.push(`| 交付物 | 验证报告 + 效果数据 | 完整部署 + 培训 | POC 不是交付 |`);
  lines.push('');

  // 模块 3：资源/时间估算
  lines.push(`## ⏱️ 资源/时间估算`);
  lines.push('');
  lines.push(`**周期**：${exp.typicalDuration}`);
  lines.push(`**团队**：${exp.typicalTeam}`);
  lines.push(`**预算参考**：${exp.typicalCost}`);
  lines.push('');
  lines.push(`| 阶段 | 人天 | 角色 | 交付物 |`);
  lines.push(`|------|------|------|--------|`);
  resources.phases.forEach((p) => {
    lines.push(`| ${p.phase} | ${p.days} | ${p.role} | ${p.deliverable} |`);
  });
  lines.push('');

  // 模块 4：成功标准定义
  lines.push(`## ✅ 成功标准定义`);
  lines.push('');
  lines.push(`| 指标 | 目标值 | 测量方式 |`);
  lines.push(`|------|--------|----------|`);
  lines.push(`| ${criteria.metric} | ${criteria.target} | ${criteria.measurement} |`);
  lines.push(`| 客户满意度 | ≥ 4/5 | POC 结束后调研 |`);
  lines.push(`| 问题修复率 | ≥ 90%（P0/P1） | 测试期间缺陷跟踪 |`);
  lines.push('');
  lines.push(`**POC 72h 快速响应闭环**：${POC_72H_RULE.formula}`);
  lines.push('');
  POC_72H_RULE.fourSteps.forEach((step, i) => {
    lines.push(`${i + 1}. ${step}`);
  });
  lines.push('');
  lines.push(`**如果达不到怎么办？**`);
  lines.push(`- 第一轮不达标 → 分析原因，调整范围，延长 1 周`);
  lines.push(`- 第二轮仍不达标 → 缩小范围，聚焦核心场景`);
  lines.push(`- 仍不达标 → 诚实告知客户，建议暂缓合作`);
  lines.push('');
  lines.push(`**⚠️ 超期警告**：${POC_72H_RULE.warning}`);
  lines.push('');

  // 模块 5：预算论证
  lines.push(`## 💰 预算论证`);
  lines.push('');
  lines.push(`### 为什么 POC 需要预算？`);
  lines.push('');
  budgetArgs.forEach((arg, i) => {
    lines.push(`${i + 1}. ${arg}`);
    lines.push('');
  });

  lines.push(`### POC 投入 vs 签单收益对比`);
  lines.push('');
  lines.push(`| 项目 | POC 阶段 | 签单后项目 | 比例 |`);
  lines.push(`|------|----------|------------|------|`);
  lines.push(`| 投入 | ${exp.typicalCost} | ${industry === '金融' ? '50-100万' : industry === '政务' ? '80-150万' : '30-80万'} | 1:5~10 |`);
  lines.push(`| 周期 | ${exp.typicalDuration} | 2-4个月 | - |`);
  lines.push(`| 风险 | 低（可终止） | 高（已投入） | POC 降低决策风险 |`);
  lines.push('');

  // 联用提示
  lines.push(`---`);
  lines.push('');
  lines.push(`**联用**：POC 前用此报告论证预算 → POC 中按 72h 闭环执行 → POC 成功后用 \`tob-sales-proposal\` 生成提案 → POC 失败后用 \`tob-win-loss-review\` 复盘`);
  lines.push('');

  // 经验来源声明
  lines.push(`> 💡 规则来源：ToB 项目经验萃取（去敏）。POC 72h 闭环来自某大型文化集团实战（93% 通过率）。预算论证来自某零售 IT 服务商项目"边界验证法"。行业成本估算仅供参考，实际以项目具体情况为准。`);
  lines.push('');

  return lines.join('\n');
}

// ── 交互模式 ──

function interactiveMode() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const ask = (question) => new Promise((resolve) => rl.question(question, resolve));

  (async () => {
    console.log('\n📋 POC 预算论证助手 — 输入 POC 信息，输出论证报告\n');

    const client = await ask('客户名称：');
    if (!client.trim()) {
      console.log('客户名称不能为空');
      rl.close();
      return;
    }

    const industry = await ask('客户所在行业（回车跳过）：');
    const pocGoal = await ask('POC 验证目标（回车跳过）：');
    const budget = await ask('客户预算范围（回车跳过）：');
    const decisionMaker = await ask('决策人角色（回车跳过）：');

    const report = generateReport({
      client: client.trim(),
      industry: industry.trim() || null,
      pocGoal: pocGoal.trim() || null,
      budget: budget.trim() || null,
      decisionMaker: decisionMaker.trim() || null,
    });

    console.log('\n' + report);
    rl.close();
  })();
}

// ── 主入口 ──

if (require.main === module) {
  const args = parseArgs(process.argv);

  if (!args.client) {
    interactiveMode();
  } else {
    const report = generateReport(args);
    console.log(report);
  }
}

module.exports = { generateReport, parseArgs };
