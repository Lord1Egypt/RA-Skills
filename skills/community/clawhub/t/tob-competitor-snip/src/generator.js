#!/usr/bin/env node

/**
 * tob-competitor-snip — 竞品狙击助手
 *
 * 基于 ToB 项目经验萃取的规则（去敏）
 *
 * 输入：竞品名称 / 行业 / 客户关注点
 * 输出：竞品画像 + 差异化对比 + 狙击话术 + 实战建议
 *
 * 降级策略：
 *   1. 有该竞品交手记录 → 引用真实交手模式（去敏）
 *   2. 无记录但有同行业经验 → 引用行业通用打法
 *   3. 完全无匹配 → 通用狙击框架
 */

const readline = require('readline');

// ── CLI 参数解析 ──

function parseArgs(argv) {
  const args = {
    competitor: null,
    industry: null,
    concern: null,
    quick: false,
  };

  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--competitor': args.competitor = argv[++i]; break;
      case '--industry': args.industry = argv[++i]; break;
      case '--concern': args.concern = argv[++i]; break;
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
tob-competitor-snip — 竞品狙击助手

用法:
  tob-competitor-snip                                    # 交互模式
  tob-competitor-snip --competitor "某AI客服厂商" --industry "零售" \\
    --concern "他们说支持多轮对话和工单联动，价格比我们低30%"
  tob-competitor-snip --quick --competitor "X公司" --concern "价格便宜"

参数:
  --competitor  竞品名称（必填）
  --industry    客户所在行业（可选）
  --concern     客户说的竞品优势或关注点（可选）
  --quick       快速模式：输出精简狙击卡片
`);
}

// ── ToB 项目经验萃取规则（去敏） ──

// 零售行业竞品交手经验（萃取自某零售 IT 服务商项目）
const RETAIL_EXPERIENCE = {
  // 价格战场景
  priceWar: {
    pattern: '竞品打价格战，首年报价低 20-40%',
    insight: '零售客户对价格敏感，但更关注"上线后能否真正跑通"。低价竞品往往在实施环节缩水。',
    flip: '「您说的价格是首年报价。零售系统看 3 年 TCO — 实施质量决定上线后运维成本。低价 = 实施缩水 = 上线后天天改 = 隐性成本远超差价。」',
    case: '某鞋服客户对比 3 家后选了报价最高的，因为"上线跑通比省钱重要"。',
    question: '「您算过上线后第一年改 Bug 的成本吗？」',
  },
  // 功能对比场景
  featureCompare: {
    pattern: '竞品列功能清单，说"我们都有"',
    insight: '零售客户不缺功能清单，缺"功能在真实业务场景中的落地率"。',
    flip: '「功能清单大家都能列，关键是实际落地率。XX 功能你有，但日均 10 万单时能不能扛住？」',
    case: '某客户 POC 时竞品演示完美，上线后发现"多仓调拨"功能只支持 2 个仓，客户要管 50 个。',
    question: '「这个功能在您日均 XX 单、XX 个仓的场景下跑过吗？」',
  },
  // 品牌信任场景
  brandTrust: {
    pattern: '客户说"XX 品牌大，用着放心"',
    insight: '大品牌 ≠ 好服务。零售行业大品牌的服务响应往往慢，因为客户太多。',
    flip: '「品牌大确实放心，但您的项目在大客户里排第几优先级？出了问题等 3 天还是 3 小时？」',
    case: '某客户用大品牌，工单排队 3 天，后来换了小但专注的供应商，2 小时响应。',
    question: '「他们的 VIP 客户有多少？您的项目排第几？」',
  },
};

// 金融/银行行业竞品经验
const FINANCE_EXPERIENCE = {
  priceWar: {
    pattern: '金融客户预算充足但决策慢，竞品低价切入',
    insight: '金融客户真正担心的是安全合规，不是价格。低价 = 安全投入不足。',
    flip: '「金融项目看重的不是首年价格，是安全审计能不能过。低价竞品在安全上省的成本，审计时全补回来。」',
  },
  featureCompare: {
    pattern: '竞品强调 AI 能力',
    insight: '金融行业 AI 准确率要求极高，99% 和 99.9% 差一个量级的 bad case。',
    flip: '「AI 演示准确率 95% 不难，难的是 99.9%。金融场景一个 bad case 就是合规事故。」',
  },
  brandTrust: {
    pattern: '客户倾向选大厂',
    insight: '金融客户选大厂是避险行为，但要提醒"大厂的金融行业专注度"。',
    flip: '「大厂产品线广，但您的场景在他们营收里占多少？专注金融的供应商比通用大厂更懂合规。」',
  },
};

// 政务/央企行业竞品经验
const GOV_EXPERIENCE = {
  priceWar: {
    pattern: '政务项目低价中标常见',
    insight: '政务客户真正关心的是"安全合规 + 领导满意"，不是价格。',
    flip: '「政务项目低价中标看似省钱，但上线后领导不满意，谁承担政治风险？」',
  },
  featureCompare: {
    pattern: '竞品强调功能全面',
    insight: '政务客户需要的不是功能多，是"领导看得懂的成果"。',
    flip: '「功能 100 个不如 1 个领导能看懂的看板。政务项目最终是汇报给领导看的。」',
  },
  brandTrust: {
    pattern: '客户倾向选国企/央企',
    insight: '政务选国企是避险，但要提醒"响应速度 + 定制化能力"。',
    flip: '「国企确实放心，但您的需求他们排第几？定制化响应要多久？」',
  },
};

// 通用狙击框架（无行业匹配时）
const GENERIC_EXPERIENCE = {
  priceWar: {
    flip: '「您说的价格是首年报价。项目看 3 年 TCO，低价 = 实施缩水 = 隐性成本远超差价。」',
    question: '「您算过上线后第一年运维成本吗？」',
  },
  featureCompare: {
    flip: '「功能清单大家都能列，关键是实际落地率。您的场景他们跑过吗？」',
    question: '「这个功能在您的真实业务数据上验证过吗？」',
  },
  brandTrust: {
    flip: '「品牌大确实放心，但您的项目在他们客户里排第几优先级？」',
    question: '「出了问题，您能直接找到决策人吗？」',
  },
};

// ── 场景检测 ──

function detectScenario(concern) {
  if (!concern) return 'generic';
  const c = concern.toLowerCase();
  if (/便宜|低价|价格|省钱|cost/.test(c)) return 'priceWar';
  if (/功能|feature|支持|多轮|联动|智能/.test(c)) return 'featureCompare';
  if (/品牌|大厂|国企|放心|信任/.test(c)) return 'brandTrust';
  return 'generic';
}

// ── 获取行业经验 ──

function getExperience(industry) {
  const map = {
    '零售': RETAIL_EXPERIENCE,
    '鞋服': RETAIL_EXPERIENCE,
    '金融': FINANCE_EXPERIENCE,
    '银行': FINANCE_EXPERIENCE,
    '政务': GOV_EXPERIENCE,
    '央企': GOV_EXPERIENCE,
    '政府': GOV_EXPERIENCE,
  };
  return map[industry] || GENERIC_EXPERIENCE;
}

// ── 生成狙击卡片 ──

function generateCard(config) {
  const { competitor, industry, concern } = config;
  const scenario = detectScenario(concern);
  const exp = getExperience(industry);
  const rule = exp[scenario] || GENERIC_EXPERIENCE.generic || exp.priceWar;

  const lines = [];

  // 标题
  lines.push(`# 🎯 竞品狙击卡片`);
  lines.push('');
  lines.push(`> 竞品：${competitor || '未指定'}`);
  if (industry) lines.push(`> 行业：${industry}`);
  if (concern) lines.push(`> 客户关注点：${concern}`);
  lines.push(`> 场景：${scenario === 'priceWar' ? '价格战' : scenario === 'featureCompare' ? '功能对比' : scenario === 'brandTrust' ? '品牌信任' : '通用'}`);
  lines.push('');

  // 模块 1：竞品画像
  lines.push(`## 📋 竞品画像`);
  lines.push('');
  if (competitor) {
    lines.push(`- **竞品**：${competitor}`);
    lines.push(`- **行业经验**：${industry ? `基于 ${industry} 行业项目经验` : '无该竞品直接交手记录'}`);
    if (!industry) {
      lines.push(`- **建议**：补充交手记录，沉淀到共享知识库`);
    }
  } else {
    lines.push(`- **竞品**：未指定`);
    lines.push(`- **建议**：下次跟客户时记下竞品名称，用于精准狙击`);
  }
  lines.push('');

  // 模块 2：差异化对比
  lines.push(`## 📊 差异化对比`);
  lines.push('');
  lines.push(`| 维度 | 竞品典型做法 | 我们的优势 | 客户价值 |`);
  lines.push(`|------|-------------|-----------|---------|`);

  if (scenario === 'priceWar') {
    lines.push(`| 价格策略 | 首年低价，实施缩水 | 全生命周期 TCO 更优 | 上线后运维成本更低 |`);
    lines.push(`| 实施质量 | 标准化模板，快速交付 | 深度定制，确保跑通 | 真实业务场景可用 |`);
    lines.push(`| 服务响应 | 客户多，响应慢 | 专注服务，快速响应 | 问题 2 小时内解决 |`);
  } else if (scenario === 'featureCompare') {
    lines.push(`| 功能演示 | POC 环境完美 | 真实数据验证 | 日均 10 万单也能扛 |`);
    lines.push(`| 落地率 | 功能多但落地率低 | 核心功能 100% 可用 | 不追求数量追求质量 |`);
    lines.push(`| 行业适配 | 通用功能 | 行业 Know-how 深 | 懂您的业务 |`);
  } else if (scenario === 'brandTrust') {
    lines.push(`| 品牌规模 | 大，客户多 | 专注，服务深 | 您的项目是 VIP |`);
    lines.push(`| 响应速度 | 工单排队 3 天 | 2 小时响应 | 问题不积压 |`);
    lines.push(`| 定制能力 | 标准化为主 | 深度定制 | 按需调整 |`);
  } else {
    lines.push(`| 价格 | 首年低价 | 3 年 TCO 更优 | 长期省钱 |`);
    lines.push(`| 质量 | 演示完美 | 真实跑通 | 上线可用 |`);
    lines.push(`| 服务 | 客户多响应慢 | 专注快速响应 | 问题不积压 |`);
  }
  lines.push('');

  // 模块 3：狙击话术
  lines.push(`## 💬 狙击话术`);
  lines.push('');

  if (rule.flip) {
    lines.push(`**翻转话术**：${rule.flip}`);
    lines.push('');
  }
  if (rule.question) {
    lines.push(`**反问问题**：${rule.question}`);
    lines.push('');
  }
  if (rule.case) {
    lines.push(`**参考案例**：${rule.case}`);
    lines.push('');
  }

  lines.push(`**核心原则**：先承认竞品优势，再用问题翻转，给案例不给结论。`);
  lines.push('');

  // 模块 4：实战建议
  lines.push(`## 🚀 实战建议`);
  lines.push('');
  lines.push(`1. **先承认，再翻转** — 不要否定竞品，先说"他们确实在 XX 方面不错"，然后翻转`);
  lines.push(`2. **用问题反击** — 不要反驳，用问题让客户自己想清楚`);
  lines.push(`3. **给案例不给结论** — "XX 客户对比后选了我们"比"我们更好"有效 10 倍`);
  lines.push(`4. **引导 POC** — 如果客户还在犹豫，建议"不如做个 POC 验证一下"`);
  lines.push(`5. **记录交手** — 每次跟竞品交手后，记录结果沉淀回知识库`);
  lines.push('');

  // 联用提示
  lines.push(`---`);
  lines.push('');
  lines.push(`**联用**：狙击前用 \`tob-competitor-snip\` 出卡片 → 提案前用 \`tob-sales-proposal\` 生成提案 → 丢单后用 \`tob-win-loss-review\` 复盘`);
  lines.push('');

  // 经验来源声明
  lines.push(`> 💡 规则来源：ToB 项目经验萃取（去敏），不编造案例。`);
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
    console.log('\n🎯 竞品狙击助手 — 输入竞品信息，输出狙击卡片\n');

    const competitor = await ask('竞品名称：');
    if (!competitor.trim()) {
      console.log('竞品名称不能为空');
      rl.close();
      return;
    }

    const industry = await ask('客户所在行业（回车跳过）：');
    const concern = await ask('客户说的竞品优势或关注点（回车跳过）：');

    const card = generateCard({
      competitor: competitor.trim(),
      industry: industry.trim() || null,
      concern: concern.trim() || null,
    });

    console.log('\n' + card);
    rl.close();
  })();
}

// ── 主入口 ──

if (require.main === module) {
  const args = parseArgs(process.argv);

  if (!args.competitor) {
    interactiveMode();
  } else {
    const card = generateCard(args);
    console.log(card);
  }
}

module.exports = { generateCard, parseArgs };
