#!/usr/bin/env node
/**
 * strategy-output.js
 * 根据客户分层评分结果生成策略建议 JSON
 * 
 * 核心功能:
 *   1. 按层级生成差异化策略建议
 *   2. upgrade_opportunities: 距升级 gap≤20 的客户 Top10 + 瓶颈维度 + nudge 建议
 *   3. 输出 strategy-recommendations.json 供下游 skill 消费
 *   4. --format summary 输出 Discord 友好文字
 * 
 * 用法:
 *   node strategy-output.js                    # 生成策略 JSON
 *   node strategy-output.js --format summary   # 输出 Discord 文字摘要
 *   node strategy-output.js --sample           # 用示例评分数据
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const DATA_DIR = path.join(ROOT, 'data');
const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, 'config/segmentation-rules.json'), 'utf8'));

// ==================== 策略模板 ====================
const STRATEGY_TEMPLATES = {
  VIP: {
    priority: 'highest',
    actions: [
      '优先跟进: 48h 内必须响应询盘',
      '专属折扣: pricing-engine 自动应用 VIP 折扣',
      '季度回访: 每季度主动联系确认需求',
      '新品优先: 新产品发布第一时间通知',
      '专属客服: 指定专人跟进'
    ],
    email_cadence: '每周至少 1 次主动触达',
    discount_tier: 'VIP'
  },
  active: {
    priority: 'high',
    actions: [
      '定期跟进: 每两周确认订单进度和需求',
      '新品推荐: 根据历史订单推荐相关产品',
      '交叉销售: 分析采购品类缺口，推荐互补产品',
      '促销通知: 季节性促销优先通知'
    ],
    email_cadence: '每两周 1 次主动触达',
    discount_tier: 'A'
  },
  normal: {
    priority: 'medium',
    actions: [
      '常规维护: 每月确认合作状态',
      '促销通知: 大型促销活动通知',
      '需求挖掘: 了解新项目计划'
    ],
    email_cadence: '每月 1 次主动触达',
    discount_tier: 'B'
  },
  dormant: {
    priority: 'high',
    actions: [
      '唤醒邮件: 发送定制唤醒邮件（含专属优惠）',
      '特别优惠: 提供限时折扣刺激复购',
      '原因调查: 了解停止采购的原因',
      '竞品分析: 检查是否转向竞品'
    ],
    email_cadence: '每两周 1 次唤醒触达',
    discount_tier: 'C',
    urgency: '休眠超 90 天需立即启动唤醒流程'
  },
  lost: {
    priority: 'low',
    actions: [
      '最后挽回: 发送最终挽回邮件（1 次机会）',
      '流失归档: 记录流失原因',
      '竞品情报: 了解客户转向哪家供应商',
      '长期跟踪: 加入年度回访名单'
    ],
    email_cadence: '季度 1 次低频触达',
    discount_tier: 'D',
    urgency: '超 180 天无互动，标记为长期流失'
  }
};

// ==================== 升级机会分析 ====================
function findUpgradeOpportunities(results, segmentLevels, topN = 10) {
  const opportunities = [];
  const dimensionLabels = {
    order_amount: '订单金额',
    order_frequency: '交易频次',
    recency: '最近活跃',
    interaction: '跟进互动'
  };

  const dimensionWeights = {};
  for (const [key, dim] of Object.entries(CONFIG.kpis.dimensions)) {
    dimensionWeights[key] = dim.weight;
  }

  // 按 min_score 降序排列 segments，确保正确匹配
  const sortedSegments = [...segmentLevels].sort((a, b) => b.min_score - a.min_score);

  for (const r of results) {
    if (r.manual_override) continue;

    // 找到当前层级和上一层级
    const currentIdx = sortedSegments.findIndex(s => s.name === r.segment);
    if (currentIdx <= 0) continue; // VIP 无法再升级

    const nextLevel = sortedSegments[currentIdx - 1];
    const gap = nextLevel.min_score - r.total_score;

    if (gap > 20) continue; // 差距太大，不列为机会

    // 找到瓶颈维度（归一化得分最低且权重最高的）
    const dims = Object.entries(r.scores).map(([key, val]) => ({
      key,
      label: dimensionLabels[key] || key,
      normalized: val.normalized,
      raw: val.raw,
      weight: dimensionWeights[key] || 0,
      potential: (100 - val.normalized) * (dimensionWeights[key] || 0)
    }));

    // 按提升潜力排序（potential = 可提升空间 × 权重）
    dims.sort((a, b) => b.potential - a.potential);
    const bottleneck = dims[0];

    // 生成 nudge 建议
    const nudge = generateNudge(bottleneck, r);

    opportunities.push({
      company_id: r.company_id,
      company_name: r.company_name,
      current_segment: r.segment,
      current_score: r.total_score,
      target_segment: nextLevel.name,
      target_score: nextLevel.min_score,
      gap: Math.round(gap * 100) / 100,
      bottleneck: {
        dimension: bottleneck.key,
        label: bottleneck.label,
        current_score: bottleneck.normalized,
        raw_value: bottleneck.raw,
        potential_gain: Math.round(bottleneck.potential * 100) / 100
      },
      nudge
    });
  }

  // 按 gap 升序排列（最接近升级的排前面）
  opportunities.sort((a, b) => a.gap - b.gap);
  return opportunities.slice(0, topN);
}

function generateNudge(bottleneck, customer) {
  const key = bottleneck.key;

  switch (key) {
    case 'order_amount':
      return `增加订单金额是关键。当前 12 个月累计 $${bottleneck.raw.toLocaleString()}。建议推荐高价值产品或大批量优惠方案。`;
    case 'order_frequency':
      return `提升下单频次。当前 12 个月仅 ${bottleneck.raw} 单。建议定期发送新品通知和补货提醒。`;
    case 'recency':
      return `客户已 ${bottleneck.raw} 天未活跃。建议立即发送跟进邮件或新品推荐，重新激活互动。`;
    case 'interaction':
      return `跟进互动偏少（${bottleneck.raw} 次/年）。建议增加主动沟通频率，定期分享行业资讯和产品更新。`;
    default:
      return `建议关注 ${bottleneck.label} 维度的提升。`;
  }
}

// ==================== 层级汇总 ====================
function buildSegmentSummary(results, segmentLevels) {
  const summary = {};

  for (const level of segmentLevels) {
    const customers = results.filter(r => r.segment === level.name);
    const template = STRATEGY_TEMPLATES[level.name] || {};

    summary[level.name] = {
      label: level.label,
      count: customers.length,
      avg_score: customers.length > 0
        ? Math.round(customers.reduce((sum, c) => sum + c.total_score, 0) / customers.length * 100) / 100
        : 0,
      strategy: template,
      customers: customers.map(c => ({
        company_id: c.company_id,
        company_name: c.company_name,
        score: c.total_score,
        manual_override: c.manual_override || false
      }))
    };
  }

  return summary;
}

// ==================== 格式化输出 ====================
function formatDiscordSummary(output) {
  const lines = [];
  lines.push('**客户分层策略报告**');
  lines.push(`生成时间: ${output.generated_at}`);
  lines.push(`客户总数: ${output.total_customers}`);
  lines.push('');

  // 层级概览
  lines.push('**分层概览**');
  for (const [seg, data] of Object.entries(output.segments)) {
    const emoji = seg === 'VIP' ? '🏆' : seg === 'active' ? '🟢' : seg === 'normal' ? '🔵' : seg === 'dormant' ? '🟠' : '⚪';
    lines.push(`${emoji} ${data.label}: ${data.count} 客户 (平均分 ${data.avg_score})`);
    if (data.customers.length > 0) {
      for (const c of data.customers.slice(0, 5)) {
        const badge = c.manual_override ? ' [手动]' : '';
        lines.push(`   ${c.company_name} (${c.score})${badge}`);
      }
      if (data.customers.length > 5) {
        lines.push(`   ...及 ${data.customers.length - 5} 位`);
      }
    }
  }

  // 升级机会
  if (output.upgrade_opportunities && output.upgrade_opportunities.length > 0) {
    lines.push('');
    lines.push('**升级机会 (距升级 ≤20 分)**');
    for (const opp of output.upgrade_opportunities.slice(0, 5)) {
      lines.push(`📈 ${opp.company_name}: ${opp.current_segment} → ${opp.target_segment} (差 ${opp.gap} 分)`);
      lines.push(`   瓶颈: ${opp.bottleneck.label} (${opp.bottleneck.current_score}/100)`);
      lines.push(`   建议: ${opp.nudge}`);
    }
  }

  return lines.join('\n');
}

// ==================== 主流程 ====================
async function generateStrategy(options = {}) {
  const { useSample = false, format = 'json' } = options;
  const startTime = Date.now();

  console.log(`[strategy] 生成策略建议... (sample: ${useSample})`);

  // 1. 加载评分数据
  let scoresData;
  if (useSample) {
    // 先尝试读取已有文件，没有则自动运行 scoring-engine --sample 生成
    const samplePath = path.join(DATA_DIR, 'scores-current.json');
    if (!fs.existsSync(samplePath)) {
      console.log('[strategy] scores-current.json 不存在，自动运行 scoring-engine 生成示例数据...');
      const { execSync } = await import('child_process');
      // scoring-engine --sample 不写文件，用无 --sample 模式 + 临时 customers-raw.json
      // 更简单: 直接 fork scoring-engine 让它写数据
      execSync(`node ${path.join(__dirname, 'scoring-engine.js')}`, {
        cwd: ROOT,
        stdio: 'pipe',
        env: { ...process.env, SCORING_FORCE_SAMPLE_WRITE: '1' }
      });
    }
    if (!fs.existsSync(samplePath)) {
      // 如果还不存在，手动生成最小样本
      console.log('[strategy] 使用内联示例评分数据');
      scoresData = generateInlineSampleScores();
    } else {
      scoresData = JSON.parse(fs.readFileSync(samplePath, 'utf8'));
      console.log('[strategy] 加载 scores-current.json');
    }
  } else {
    const scoresPath = path.join(DATA_DIR, 'scores-current.json');
    if (!fs.existsSync(scoresPath)) {
      console.error('[strategy] scores-current.json 不存在。请先运行评分流程。');
      process.exit(1);
    }
    scoresData = JSON.parse(fs.readFileSync(scoresPath, 'utf8'));
    console.log(`[strategy] 加载评分数据 (${scoresData.results.length} 客户)`);
  }

  const results = scoresData.results;
  const segmentLevels = CONFIG.segments.levels;

  // 2. 层级汇总
  const segments = buildSegmentSummary(results, segmentLevels);

  // 3. 升级机会分析
  const upgradeOpportunities = findUpgradeOpportunities(results, segmentLevels);

  // 4. 组装输出
  const output = {
    generated_at: new Date().toISOString(),
    scored_at: scoresData.scored_at,
    total_customers: results.length,
    segments,
    upgrade_opportunities: upgradeOpportunities,
    metadata: {
      config_version: CONFIG.settings ? 'segmentation-rules.json' : 'unknown',
      generation_ms: Date.now() - startTime
    }
  };

  // 5. 输出
  if (format === 'summary') {
    const text = formatDiscordSummary(output);
    console.log(text);
    return output;
  }

  // 写文件
  fs.mkdirSync(DATA_DIR, { recursive: true });
  const outputPath = path.join(DATA_DIR, 'strategy-recommendations.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(`[strategy] 策略建议已写入: ${outputPath}`);

  // 打印摘要
  console.log('\n========== 策略建议摘要 ==========');
  console.log(`客户总数: ${output.total_customers}`);
  for (const [seg, data] of Object.entries(output.segments)) {
    console.log(`  ${data.label}: ${data.count} 客户 (平均分 ${data.avg_score})`);
  }

  if (upgradeOpportunities.length > 0) {
    console.log(`\n升级机会: ${upgradeOpportunities.length} 位客户`);
    for (const opp of upgradeOpportunities) {
      console.log(`  📈 ${opp.company_name}: ${opp.current_segment} → ${opp.target_segment} (差 ${opp.gap} 分, 瓶颈: ${opp.bottleneck.label})`);
    }
  } else {
    console.log('\n无升级机会（所有客户距下一层级 >20 分）');
  }

  console.log(`\n[strategy] 完成。耗时: ${Date.now() - startTime}ms`);
  return output;
}

// ==================== CLI ====================
const args = process.argv.slice(2);
const useSample = args.includes('--sample');
const formatIdx = args.indexOf('--format');
const format = formatIdx >= 0 && args[formatIdx + 1] ? args[formatIdx + 1] : 'json';

generateStrategy({ useSample, format }).catch(err => {
  console.error(`[strategy] 错误: ${err.message}`);
  process.exit(1);
});
