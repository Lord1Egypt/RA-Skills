#!/usr/bin/env node

/**
 * tob-competitor-snip — 竞品狙击卡片生成器
 * 纯规则引擎，无外部依赖，无知识库调用
 */

const readline = require('readline');

// ── CLI 参数解析 ──

function parseArgs(argv) {
  const args = { competitor: null, industry: null, customerConcern: null, quick: false };
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--competitor': args.competitor = argv[++i]; break;
      case '--industry': args.industry = argv[++i]; break;
      case '--concern':
      case '--customer-concern': args.customerConcern = argv[++i]; break;
      case '--quick': args.quick = true; break;
      case '--help': case '-h': printHelp(); process.exit(0); break;
    }
  }
  return args;
}

function printHelp() {
  console.log(`
竞品狙击助手 — 输入竞品信息，输出狙击卡片

用法:
  node generator.js                          # 交互模式
  node generator.js --competitor "X公司" --concern "价格便宜30%"
  node generator.js --competitor "X公司" --industry "零售" --concern "功能更多"
  node generator.js --quick --competitor "X公司" --concern "品牌大"

参数:
  --competitor       竞品名称（必填）
  --industry         客户所在行业（可选）
  --concern          客户提到的竞品优势（可选，同 --customer-concern）
  --quick            快速模式：仅输出狙击话术
`);
}

// ── 规则引擎：经验规则集 ──

const RULE_DEFS = [
  {
    key: 'price',
    trigger: (c) => /便宜|低价|价格|报价|成本|预算|贵|低\d+%|省/.test(c || ''),
    data: {
      flip: (comp) => [
        `「${comp} 的首年报价确实可能更低，但 ToB 软件要看 3 年 TCO。很多客户第一年省了 20%，第二年因为定制和维护多花了 50%。」`,
        `「您比较的是首年授权费，实际落地后的接口对接、二次开发、培训成本，往往比授权费还高。」`,
        `「便宜的产品通常在前端功能上堆料，后端架构和数据安全上省钱。您关心的是上线效果还是上线价格？」`,
      ],
      comparison: [
        { dim: '首年授权/订阅', comp: '低', us: '中', note: '竞品常用低价获客' },
        { dim: '二次开发成本', comp: '高', us: '低', note: '标准化程度高' },
        { dim: '对接集成成本', comp: '中-高', us: '低', note: '预置行业模板' },
        { dim: '运维/培训', comp: '中', us: '低', note: '行业经验沉淀' },
        { dim: '3年TCO', comp: '高', us: '低', note: '总成本我们更低' },
      ],
    },
  },
  {
    key: 'features',
    trigger: (c) => /功能|多轮|工单|对话|自动化|AI|大模型|算法/.test(c || ''),
    data: {
      flip: (comp, ind) => [
        `「功能清单大家都能列，关键是实际落地率。很多客户对比时选了功能多的，上线后发现 60% 的功能用不起来。」`,
        `「${comp} 的功能可能更全，但您的核心需求是什么？先把 20% 的关键功能做到 90 分，比 100% 的功能做到 60 分更重要。」`,
        `「功能多不代表懂行业。我们深耕 ${ind || '该'} 场景，知道哪些功能真正产生业务价值。」`,
      ],
      comparison: [
        { dim: '功能数量', comp: '★★★★★', us: '★★★★', note: '竞品功能覆盖广' },
        { dim: '行业适配度', comp: '★★★', us: '★★★★★', note: '我们有行业模板' },
        { dim: '落地成功率', comp: '★★★', us: '★★★★★', note: '真实交付数据' },
        { dim: '交付速度', comp: '★★★', us: '★★★★', note: '标准化程度高' },
        { dim: '售后服务', comp: '★★★', us: '★★★★★', note: '专属客户成功' },
      ],
    },
  },
  {
    key: 'brand',
    trigger: (c) => /品牌|大公司|上市公司|知名度|规模|团队/.test(c || ''),
    data: {
      flip: () => [
        `「品牌大小和适不适合您是两回事。大厂商服务大客户，您的规模在他们那可能排不上优先级。」`,
        `「我们确实不是最大的，但我们的客户续约率是 90%+，这比品牌大小更能说明问题。」`,
      ],
      comparison: [
        { dim: '品牌知名度', comp: '高', us: '中', note: '我们专注细分领域' },
        { dim: '客户响应速度', comp: '低', us: '高', note: '扁平化服务' },
        { dim: '定制灵活性', comp: '低', us: '高', note: '敏捷交付' },
        { dim: '客户续约率', comp: '?', us: '90%+', note: '真实数据' },
      ],
    },
  },
  {
    key: 'general',
    trigger: () => true,
    data: {
      flip: [
        `「每个方案都有自己的强项，关键看哪家的强项正好是您的痛点。」`,
        `「建议您让两家都做个 POC，用真实数据说话，而不是听销售讲故事。」`,
        `「您现在最关心的是什么？我们可以围绕这个核心点做深度对比。」`,
      ],
      comparison: [
        { dim: '核心需求满足度', comp: '?', us: '待评估', note: '建议POC验证' },
        { dim: '行业适配度', comp: '?', us: '待评估', note: '需确认行业经验' },
        { dim: '交付保障', comp: '?', us: '待评估', note: '看交付团队能力' },
        { dim: '3年TCO', comp: '?', us: '待评估', note: '算总账不看首年' },
      ],
    },
  },
];

function detectScenario(concern) {
  for (const rule of RULE_DEFS) {
    if (rule.trigger(concern)) return rule;
  }
  return RULE_DEFS[RULE_DEFS.length - 1];
}

// ── 生成卡片 ──

function generateCard({ competitor, industry, customerConcern, quick }) {
  const rule = detectScenario(customerConcern);
  const data = rule.data;
  const flips = Array.isArray(data.flip) ? data.flip : (typeof data.flip === 'function' ? data.flip(competitor || '竞品', industry) : []);

  const lines = [
    '# 🔪 竞品狙击卡片', '',
    `> 竞品：${competitor || '未指定'}`,
  ];
  if (industry) lines.push(`> 行业：${industry}`);
  if (customerConcern) lines.push(`> 客户关注：${customerConcern}`);
  lines.push(`> 识别场景：${rule.key === 'general' ? '通用' : rule.key}`, '');

  if (quick) {
    lines.push('## 💬 狙击话术', '');
    flips.forEach((f, i) => lines.push(`${i + 1}. ${f}`, ''));
    lines.push('---', '', '**提示**：快速模式已精简。完整卡片请去掉 --quick 参数', '');
    return lines.join('\n');
  }

  // 模块 1
  lines.push('## 📋 竞品画像', '');
  if (competitor) {
    lines.push(`- **竞品名称**：${competitor}`);
    lines.push('- **行业经验**：知识库暂无交手记录');
    lines.push('- **已知强项**：待补充（使用后请反馈实际交手信息）');
    lines.push('- **已知弱项**：待补充（使用后请反馈实际交手信息）', '');
    lines.push('> 💡 知识库暂无该竞品交手记录，以下为规则引擎生成的通用框架。');
    lines.push('> 建议在实战后将实际交手信息沉淀回知识库。', '');
  } else {
    lines.push('> 请提供竞品名称以生成狙击卡片', '');
  }

  // 模块 2
  lines.push('## 📊 差异化对比', '');
  lines.push('| 维度 | 竞品 | 我们 | 说明 |');
  lines.push('|------|------|------|------|');
  data.comparison.forEach(r => {
    lines.push(`| ${r.dim} | ${r.comp} | ${r.us} | ${r.note} |`);
  });
  lines.push('');

  // 模块 3
  lines.push('## 💬 狙击话术', '');
  flips.forEach((f, i) => lines.push(`${i + 1}. ${f}`, ''));

  // 模块 4
  lines.push('## 🎯 实战建议', '',
    '1. **先承认，再翻转** — 不要否定竞品，先承认其优势，然后引导到 TCO',
    '2. **用问题反击** — "您关心的是首年价格还是 3 年总成本？"',
    '3. **给案例不给结论** — 当前使用通用框架，建议补充真实案例到知识库',
    '4. **引导 POC** — "让两家都做 POC，用真实数据说话"', '',
    '---', '',
    '**联用**：提案前用此卡片 → 再用 `tob-sales-proposal` 生成提案 → 丢单后用 `tob-win-loss-review` 复盘', ''
  );

  return lines.join('\n');
}

// ── 交互模式 ──

function interactiveMode() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q) => new Promise((resolve) => rl.question(q, resolve));

  (async () => {
    console.log('\n🔪 竞品狙击助手 — 输入竞品信息，输出狙击卡片\n');
    const competitor = await ask('竞品名称：');
    if (!competitor.trim()) { console.log('竞品名称不能为空'); rl.close(); return; }
    const industry = await ask('客户所在行业（回车跳过）：');
    const concern = await ask('客户提到的竞品优势/关注点（回车跳过）：');
    console.log('\n' + generateCard({ competitor: competitor.trim(), industry: industry.trim() || null, customerConcern: concern.trim() || null }));
    rl.close();
  })();
}

// ── 主入口 ──

if (require.main === module) {
  const args = parseArgs(process.argv);
  if (!args.competitor) { interactiveMode(); }
  else { console.log(generateCard(args)); }
}

module.exports = { detectScenario, generateCard, parseArgs };
