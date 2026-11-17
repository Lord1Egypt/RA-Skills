#!/usr/bin/env node
'use strict';
/**
 * 睡眠优化计算器 - 生活阶段增强版（Node.js）
 * 基于循证睡眠医学的个性化睡眠计划生成器
 * 原 Python 版移植：逻辑与报告输出保持完全一致
 */

// ==================== 工具函数 ====================

/** 解析 "HH:MM" 为当天分钟数（0-1439） */
function parseTime(str) {
  if (str === null || str === undefined) {
    throw new Error(`无法解析时间: ${str}（需要 HH:MM 格式）`);
  }
  const m = /^(\d{1,2}):(\d{2})$/.exec(String(str).trim());
  if (!m) {
    throw new Error(`无法解析时间: ${str}（需要 HH:MM 格式）`);
  }
  const h = parseInt(m[1], 10);
  const min = parseInt(m[2], 10);
  if (h < 0 || h > 23 || min < 0 || min > 59) {
    throw new Error(`无法解析时间: ${str}（需要 HH:MM 格式）`);
  }
  return h * 60 + min;
}

/** 分钟数（可跨天取模）格式化为 "HH:MM" */
function formatTime(minutes) {
  const m = ((minutes % 1440) + 1440) % 1440;
  const hh = String(Math.floor(m / 60)).padStart(2, '0');
  const mm = String(m % 60).padStart(2, '0');
  return `${hh}:${mm}`;
}

/** 两个 "HH:MM" 之间的分钟差（自动处理跨夜） */
function timeDiffMinutes(start, end) {
  const diff = parseTime(end) - parseTime(start);
  return diff < 0 ? diff + 1440 : diff;
}

/** 复刻 Python str(浮点) 的展示形式：7.0 -> "7.0"，7.5 -> "7.5" */
function pyFloatStr(x) {
  return Number.isInteger(x) ? x.toFixed(1) : String(x);
}

/**
 * 复刻 Python 的 round-half-even 格式化（f"{x:.{digits}f}"）
 * 例如 pyRound(2.5, 0) === "2"，pyRound(-2.5, 0) === "-2"
 */
function pyRound(x, digits) {
  const factor = Math.pow(10, digits);
  const scaled = x * factor;
  const fl = Math.floor(scaled);
  const frac = scaled - fl;
  let r;
  if (Math.abs(frac - 0.5) < 1e-9) {
    r = fl % 2 === 0 ? fl : fl + 1;
  } else {
    r = Math.round(scaled);
  }
  return (r / factor).toFixed(digits);
}

// ==================== 可视化图表 ====================
// 科学依据：
// - 睡眠效率 ≥85%：CBT-I 睡眠限制疗法核心目标 (Spielman et al., 1987; Morin et al., 2006, Sleep)
// - 睡眠债：慢性睡眠不足的累积效应 (Van Dongen et al., 2003, Sleep)
// - 固定睡眠窗口/作息一致性：避免社交时差>2h (Wittmann et al., 2006, Chronobiology Int.)
// - 睡眠结构（N1 2-5% / N2 45-55% / N3 13-23% / REM 20-25%，周期约90分钟）：
//   NREM-REM 超日节律 (Carskadon & Dement, 2011, Principles and Practice of Sleep Medicine)

const BLOCK = '█';
const SHADE = '░';
const DOT = '·';

/** ① 睡眠效率条形图（CBT-I 目标 ≥85%） */
function renderEfficiencyChart(eff) {
  const target = 85;
  const width = 30;
  const filled = Math.max(0, Math.min(width, Math.round((eff / 100) * width)));
  const bar = BLOCK.repeat(filled) + SHADE.repeat(width - filled);
  const tPos = Math.round((target / 100) * width);
  const status = eff >= target ? '达标 ✓' : '未达标，需优化';
  return [
    '#### ① 睡眠效率（CBT-I 睡眠限制疗法目标 ≥85%）',
    `[${bar}] ${pyRound(eff, 1)}%  ${status}`,
    `${' '.repeat(tPos + 1)}↑85% 目标线`,
    ''
  ].join('\n');
}

/** ② 睡眠时长对比图（当前估算 vs 生活阶段推荐区间） */
function renderDurationChart(metrics, lifestyleConfig) {
  const est = metrics.estimated_sleep_time / 60;
  const lo = lifestyleConfig ? lifestyleConfig.sleep_range[0] : 7;
  const hi = lifestyleConfig ? lifestyleConfig.sleep_range[1] : 9;
  const scaleMax = Math.max(est, hi, 8);
  const width = 24;
  const bar = (v) => {
    const f = Math.max(0, Math.min(width, Math.round((v / scaleMax) * width)));
    return BLOCK.repeat(f) + SHADE.repeat(width - f);
  };
  const range = (a, b) => {
    const pa = Math.round((a / scaleMax) * width);
    const pb = Math.round((b / scaleMax) * width);
    const chars = [];
    for (let i = 0; i < width; i++) chars.push(i >= pa && i < pb ? BLOCK : DOT);
    return chars.join('');
  };
  const stageName = lifestyleConfig ? lifestyleConfig.name : '成人通用';
  const gap = Math.max(0, lo - est);
  const lines = [
    '#### ② 睡眠时长对比',
    `当前估算 [${bar(est)}] ${pyRound(est, 1)}h`,
    `推荐区间 [${range(lo, hi)}] ${pyFloatStr(lo)}–${pyFloatStr(hi)}h（${stageName}）`,
    `睡眠缺口 ${pyRound(gap, 1)}h`
  ];
  if (est > hi) {
    lines.push('注意：当前估算超过推荐上限 —— 过长的卧床时间会降低睡眠效率，建议按睡眠限制疗法缩减在床时间');
  }
  lines.push('');
  return lines.join('\n');
}

/** ③ 睡眠窗口甘特图（当前 vs 优化后，30分钟/格，固定起床时间原则） */
function renderWindowChart(data, plan) {
  const startH = 20;
  const width = 24; // 20:00–08:00，30分钟/格
  const pos = (t) => {
    let m = parseTime(t) - startH * 60;
    if (m < 0) m += 1440;
    return m / 30;
  };
  const row = (label, from, to) => {
    const a = Math.round(pos(from));
    const b = Math.round(pos(to));
    const chars = [];
    for (let i = 0; i < width; i++) chars.push(i >= a && i < b ? BLOCK : DOT);
    return `${label.padEnd(4)}[${chars.join('')}] ${from}→${to}`;
  };
  const labels = [];
  const ticks = [];
  for (let i = 0; i < width; i++) {
    if (i % 2 === 0) {
      const h = (startH + i / 2) % 24;
      labels.push(String(h).padStart(2, '0'));
      ticks.push('|');
    } else {
      labels.push('  ');
      ticks.push(' ');
    }
  }
  const napLine = plan.nap_start && plan.nap_end
    ? `午睡建议 ${plan.nap_start}–${plan.nap_end}（位于13:00–15:00最佳窗口内，避免超过30分钟防睡眠惯性）`
    : '午睡：无需午睡';
  return [
    '#### ③ 睡眠窗口（30分钟/格，固定起床时间为锚点）',
    `      ${labels.join('')}`,
    `      ${ticks.join('')}`,
    row('当前', data.night_bedtime, data.night_wakeup),
    row('优化', plan.night_bedtime, plan.night_wakeup),
    napLine,
    ''
  ].join('\n');
}

/** 8周渐进计划执行节奏图 */
function renderPlanVisual() {
  const phases = [
    ['第1-2周', 8, '稳定节律', '固定起床时间、睡前放松程序、睡眠日记'],
    ['第3-4周', 8, '优化效率', '睡眠限制、刺激控制（20分钟规则）'],
    ['第5-8周', 16, '巩固维持', '维持睡眠窗口、环境优化（18-22°C、黑暗、安静）'],
    ['长期', 16, '个性化优化', '应对生活变化、预防复发']
  ];
  const lines = ['### 执行节奏总览'];
  for (const [when, w, theme, desc] of phases) {
    const bar = BLOCK.repeat(w) + (when === '长期' ? '…' : '');
    lines.push(`${when.padEnd(7)}${bar} ${theme} · ${desc}`);
  }
  lines.push('');
  return lines.join('\n');
}

/** 健康成人睡眠结构参考图（典型值，随年龄/个体变化） */
function renderArchitectureChart() {
  const rows = [
    ['深睡N3', 18, '13–23%', '前半夜最集中，促进生长激素分泌与身体修复'],
    ['浅睡N2', 50, '45–55%', '整夜交替出现，占比最高'],
    ['快速眼动REM', 22, '20–25%', '后半夜更长，记忆巩固与情绪调节'],
    ['浅睡N1', 4, '2–5%', '入睡过渡期'],
    ['短暂清醒', 4, '<5%', '夜间短暂觉醒属正常现象']
  ];
  const width = 30;
  const lines = [
    '### 睡眠结构参考（健康成人典型值）',
    '整夜约4-5个睡眠周期，每周期约90分钟；深睡集中于前半夜，REM集中于后半夜。',
    '（比例随年龄与个体差异变化，仅供参考）'
  ];
  for (const [name, mid, pct, note] of rows) {
    const f = Math.max(1, Math.round((mid / 100) * width));
    const bar = BLOCK.repeat(f) + SHADE.repeat(width - f);
    lines.push(`[${bar}] ${name} ${pct} · ${note}`);
  }
  lines.push('');
  return lines.join('\n');
}

/** 生成 SVG 图表文件内容（--output 时伴随输出 .chart.svg） */
function renderSvgChart(data, metrics, plan, lifestyleConfig) {
  const W = 760;
  const H = 640;
  const pad = 40;
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const stageName = lifestyleConfig ? lifestyleConfig.name : '成人通用';
  const eff = metrics.sleep_efficiency;
  const est = metrics.estimated_sleep_time / 60;
  const lo = lifestyleConfig ? lifestyleConfig.sleep_range[0] : 7;
  const hi = lifestyleConfig ? lifestyleConfig.sleep_range[1] : 9;
  const scaleMax = Math.max(est, hi, 8);

  // 睡眠窗口：20:00 – 次日09:00
  const winMin = 780;
  const xOf = (t) => {
    let m = parseTime(t) - 20 * 60;
    if (m < 0) m += 1440;
    return pad + (m / winMin) * (W - 2 * pad);
  };
  const barW = W - 2 * pad;
  const hourTicks = [];
  for (let h = 20; h <= 33; h++) {
    const hh = h % 24;
    const x = pad + ((h - 20) / 13) * barW;
    hourTicks.push(`<text x="${x.toFixed(1)}" y="532" font-size="11" fill="#888" text-anchor="middle">${String(hh).padStart(2, '0')}</text>`);
    hourTicks.push(`<line x1="${x.toFixed(1)}" y1="452" x2="${x.toFixed(1)}" y2="458" stroke="#bbb"/>`);
  }

  const pct = (v, max) => Math.max(0, Math.min(100, (v / max) * 100));

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" font-family="Microsoft YaHei, PingFang SC, sans-serif">
  <rect width="${W}" height="${H}" fill="#ffffff"/>
  <text x="${pad}" y="30" font-size="18" font-weight="bold" fill="#222">个性化睡眠优化报告 · 可视化图表</text>
  <text x="${pad}" y="52" font-size="13" fill="#666">生活阶段：${esc(stageName)}　|　估算睡眠 ${pyRound(est, 1)}h　|　睡眠效率 ${pyRound(eff, 1)}%　|　睡眠债务 ${pyRound(metrics.sleep_debt, 0)}分钟</text>

  <!-- ① 睡眠效率 -->
  <text x="${pad}" y="95" font-size="14" font-weight="bold" fill="#333">① 睡眠效率（CBT-I 目标 ≥85%）</text>
  <rect x="${pad}" y="105" width="${barW}" height="22" rx="4" fill="#e8e8e8"/>
  <rect x="${pad}" y="105" width="${(pct(eff, 100) / 100 * barW).toFixed(1)}" height="22" rx="4" fill="${eff >= 85 ? '#3ba55d' : '#4a90d9'}"/>
  <line x1="${(pad + 0.85 * barW).toFixed(1)}" y1="100" x2="${(pad + 0.85 * barW).toFixed(1)}" y2="132" stroke="#e05656" stroke-dasharray="4,3"/>
  <text x="${(pad + 0.85 * barW).toFixed(1)}" y="147" font-size="12" fill="#e05656" text-anchor="middle">85% 目标</text>
  <text x="${(W - pad)}" y="120" font-size="13" font-weight="bold" fill="#333" text-anchor="end">${pyRound(eff, 1)}% ${eff >= 85 ? '✓ 达标' : '· 未达标'}</text>

  <!-- ② 睡眠时长对比 -->
  <text x="${pad}" y="190" font-size="14" font-weight="bold" fill="#333">② 睡眠时长对比（推荐 ${pyFloatStr(lo)}–${pyFloatStr(hi)}h）</text>
  <rect x="${pad}" y="205" width="${barW}" height="16" rx="3" fill="#f0f0f0"/>
  <rect x="${(pad + pct(lo, scaleMax) / 100 * barW).toFixed(1)}" y="205" width="${((pct(hi, scaleMax) - pct(lo, scaleMax)) / 100 * barW).toFixed(1)}" height="16" rx="3" fill="#ffd27f"/>
  <rect x="${pad}" y="230" width="${(pct(est, scaleMax) / 100 * barW).toFixed(1)}" height="16" rx="3" fill="#4a90d9"/>
  <text x="${pad}" y="218" font-size="11" fill="#8a6d1f">推荐区间</text>
  <text x="${(pad + 120)}" y="243" font-size="11" fill="#2a5d9f">当前估算 ${pyRound(est, 1)}h</text>
  <text x="${(pad + 260)}" y="243" font-size="11" fill="#666">睡眠缺口 ${pyRound(Math.max(0, lo - est), 1)}h</text>

  <!-- ③ 睡眠窗口 -->
  <text x="${pad}" y="285" font-size="14" font-weight="bold" fill="#333">③ 睡眠窗口（20:00 – 09:00，固定起床时间为锚点）</text>
  <text x="${pad}" y="305" font-size="12" fill="#888">当前　${esc(data.night_bedtime)} – ${esc(data.night_wakeup)}（${pyRound(metrics.night_time_in_bed / 60, 1)}h）</text>
  <rect x="${pad}" y="315" width="${barW}" height="20" rx="3" fill="#e8e8e8"/>
  <rect x="${xOf(data.night_bedtime).toFixed(1)}" y="315" width="${Math.max(0, xOf(data.night_wakeup) - xOf(data.night_bedtime)).toFixed(1)}" height="20" rx="3" fill="#b9b9b9"/>
  <text x="${pad}" y="355" font-size="12" fill="#2a5d9f">优化　${esc(plan.night_bedtime)} – ${esc(plan.night_wakeup)}（含15分钟睡前放松缓冲）</text>
  <rect x="${pad}" y="365" width="${barW}" height="20" rx="3" fill="#e8e8e8"/>
  <rect x="${xOf(plan.night_bedtime).toFixed(1)}" y="365" width="${Math.max(0, xOf(plan.night_wakeup) - xOf(plan.night_bedtime)).toFixed(1)}" height="20" rx="3" fill="#4a90d9"/>
  ${plan.nap_start && plan.nap_end ? `<text x="${pad}" y="410" font-size="12" fill="#666">午睡建议 ${esc(plan.nap_start)} – ${esc(plan.nap_end)}（13:00–15:00窗口，≤30分钟防睡眠惯性）</text>` : `<text x="${pad}" y="410" font-size="12" fill="#666">午睡：无需</text>`}
  <line x1="${pad}" y1="440" x2="${W - pad}" y2="440" stroke="#ccc"/>
  ${hourTicks.join('\n  ')}

  <text x="${pad}" y="575" font-size="12" fill="#555">科学依据：睡眠效率≥85%（Spielman 1987 睡眠限制疗法；Morin 2006）；</text>
  <text x="${pad}" y="595" font-size="12" fill="#555">固定作息避免社交时差（Wittmann 2006）；睡眠债（Van Dongen 2003）。</text>
  <text x="${pad}" y="625" font-size="11" fill="#999">本图表由 sleep-optimizer 技能生成，仅供参考，不能替代专业医疗建议。</text>
</svg>
`;
}

// ==================== 核心类 ====================

class SleepOptimizer {
  // 科学依据常量
  static RECOMMENDED_SLEEP_HOURS = [7, 9]; // 成人推荐睡眠时长
  static OPTIMAL_BEDTIME_RANGE = ["22:00", "23:30"]; // 理想上床时间
  static OPTIMAL_WAKEUP_RANGE = ["06:00", "07:30"]; // 理想起床时间
  static NAP_WINDOW = ["13:00", "15:00"]; // 午睡最佳窗口
  static MAX_NAP_MINUTES = 20; // 最大推荐午睡时长
  static TARGET_SLEEP_EFFICIENCY = 85; // 目标睡眠效率

  // 生活阶段配置（基于循证研究）
  static LIFESTYLE_CONFIGS = {
    freshman: { // 大一
      name: "大一生活",
      sleep_range: [7.5, 8.5],
      description: "适应新环境，建立独立作息",
      challenges: ["社交活动多", "作息不规律", "新环境适应"],
      recommendations: [
        "建立固定作息，避免熬夜社交",
        "利用学校作息规律建立生物钟",
        "周末保持与工作日相近作息"
      ],
      nap_recommended: true,
      nap_duration: 15,
      stress_level: "moderate",
      cognitive_load: "moderate"
    },
    sophomore: { // 大二
      name: "大二生活",
      sleep_range: [7.0, 8.0],
      description: "学业加重，社团活动平衡",
      challenges: ["课程压力增加", "多任务处理", "时间管理"],
      recommendations: [
        "优先保证核心课程学习前的睡眠",
        "学会说'不'，避免过度承诺",
        "建立学习-休息-睡眠的平衡"
      ],
      nap_recommended: true,
      nap_duration: 15,
      stress_level: "moderate",
      cognitive_load: "moderate"
    },
    postgraduate_prep: { // 考研备考
      name: "考研备考",
      sleep_range: [7.0, 7.5],
      description: "高强度学习，记忆巩固关键期",
      challenges: ["长期高压", "记忆负荷大", "焦虑情绪"],
      recommendations: [
        "睡眠是记忆巩固的关键，避免牺牲睡眠",
        "保持7小时以上睡眠以优化记忆提取",
        "睡前1小时复习，利用睡眠巩固记忆",
        "固定作息减少决策疲劳"
      ],
      nap_recommended: true,
      nap_duration: 20,
      stress_level: "high",
      cognitive_load: "very_high"
    },
    civil_service_prep: { // 考公备考
      name: "考公备考",
      sleep_range: [7.0, 7.5],
      description: "行测申论高强度训练，需要清晰思维",
      challenges: ["题量大", "时间压力", "竞争激烈"],
      recommendations: [
        "保证充足睡眠以维持逻辑思维敏捷",
        "模拟考试期间保持与考试日相同作息",
        "避免考前突击熬夜"
      ],
      nap_recommended: true,
      nap_duration: 15,
      stress_level: "high",
      cognitive_load: "high"
    },
    skill_training_physical: { // 技能培养-体力型
      name: "技能培养（体力型）",
      sleep_range: [8.0, 9.0],
      description: "运动/舞蹈/体育训练等体力消耗型技能",
      challenges: ["体力消耗大", "肌肉恢复需求", "受伤风险"],
      recommendations: [
        "增加睡眠至8-9小时促进肌肉修复",
        "训练后20-30分钟小睡加速恢复",
        "深度睡眠阶段对生长激素分泌至关重要",
        "避免训练后3小时内入睡（影响睡眠结构）"
      ],
      nap_recommended: true,
      nap_duration: 30,
      stress_level: "moderate",
      cognitive_load: "low"
    },
    skill_training_mental: { // 技能培养-脑力型
      name: "技能培养（脑力型）",
      sleep_range: [7.5, 8.5],
      description: "编程/语言/乐器等认知密集型技能",
      challenges: ["认知负荷高", "精细运动学习", "持续专注"],
      recommendations: [
        "REM睡眠对程序性记忆巩固至关重要",
        "练习后保证完整睡眠周期（90分钟倍数）",
        "避免睡前过度用脑导致入睡困难"
      ],
      nap_recommended: true,
      nap_duration: 20,
      stress_level: "moderate",
      cognitive_load: "high"
    },
    vacation: { // 假期
      name: "假期阶段",
      sleep_range: [7.5, 9.0],
      description: "放松恢复，但需保持节律",
      challenges: ["作息容易混乱", "社交时差", "开学适应"],
      recommendations: [
        "假期可适度补觉，但避免睡眠节律大幅偏移",
        "周末/假期与工作日作息差异<2小时",
        "利用假期建立更健康的长期作息",
        "开学前3-5天逐步调整回学习作息"
      ],
      nap_recommended: false,
      nap_duration: 0,
      stress_level: "low",
      cognitive_load: "low"
    },
    junior: { // 大三
      name: "大三生活",
      sleep_range: [7.0, 8.0],
      description: "专业课程深入，未来规划关键期",
      challenges: ["专业课难度大", "考研/就业抉择", "科研/项目压力"],
      recommendations: [
        "平衡专业课学习与未来准备",
        "避免过度焦虑影响睡眠",
        "建立稳定的晚间放松仪式"
      ],
      nap_recommended: true,
      nap_duration: 15,
      stress_level: "moderate",
      cognitive_load: "high"
    },
    senior: { // 大四
      name: "大四生活",
      sleep_range: [7.0, 8.0],
      description: "毕业设计/论文，求职/升学冲刺",
      challenges: ["毕业论文压力", "求职面试", "未来不确定性"],
      recommendations: [
        "论文写作期间保持规律作息",
        "面试前保证充足睡眠以提升表现",
        "将大任务分解，避免通宵赶工"
      ],
      nap_recommended: true,
      nap_duration: 20,
      stress_level: "high",
      cognitive_load: "high"
    },
    final_review: { // 期末复习周
      name: "期末复习周",
      sleep_range: [6.5, 7.5],
      description: "短期高强度复习，临时睡眠调整",
      challenges: ["多科目同时复习", "时间紧迫", "短期高压"],
      recommendations: [
        "短期可适当压缩睡眠，但避免连续<6小时",
        "利用午睡20分钟恢复认知功能",
        "睡前1小时复习重点，利用睡眠巩固",
        "考前一天恢复正常作息"
      ],
      nap_recommended: true,
      nap_duration: 20,
      stress_level: "very_high",
      cognitive_load: "very_high"
    },
    exam_week: { // 考试周
      name: "考试周",
      sleep_range: [7.0, 8.0],
      description: "考试期间，保持最佳状态",
      challenges: ["考试焦虑", "作息需配合考试时间", "脑力消耗大"],
      recommendations: [
        "考试日提前1小时起床，避免匆忙",
        "考前夜保证7小时以上睡眠",
        "午间小睡15-20分钟恢复警觉性",
        "避免考前一天突击熬夜"
      ],
      nap_recommended: true,
      nap_duration: 15,
      stress_level: "very_high",
      cognitive_load: "very_high"
    },
    internship_work: { // 实习/工作
      name: "实习/工作",
      sleep_range: [7.0, 8.0],
      description: "适应职场作息，通勤压力",
      challenges: ["早起通勤", "工作压力", "社交应酬"],
      recommendations: [
        "根据通勤时间倒推就寝时间",
        "午休20分钟提升下午工作效率",
        "工作日保持规律，周末补偿<1小时"
      ],
      nap_recommended: true,
      nap_duration: 15,
      stress_level: "moderate",
      cognitive_load: "moderate"
    }
  };

  constructor() {
    this.data = {};
    this.metrics = {};
    this.plan = {};
    this.lifestyle = null;
    this.lifestyle_config = null;
    // 便捷引用静态常量
    this.RECOMMENDED_SLEEP_HOURS = SleepOptimizer.RECOMMENDED_SLEEP_HOURS;
    this.TARGET_SLEEP_EFFICIENCY = SleepOptimizer.TARGET_SLEEP_EFFICIENCY;
    this.LIFESTYLE_CONFIGS = SleepOptimizer.LIFESTYLE_CONFIGS;
  }

  parse_time(str) {
    return parseTime(str);
  }

  time_diff_minutes(start, end) {
    return timeDiffMinutes(start, end);
  }

  format_time(minutes) {
    return formatTime(minutes);
  }

  /**
   * 输入睡眠数据和生活阶段
   * @param {string} night_bedtime 夜间上床时间 (HH:MM)
   * @param {string} night_wakeup 夜间起床时间 (HH:MM)
   * @param {string|null} nap_bedtime 午睡上床时间 (HH:MM, 可选)
   * @param {string|null} nap_wakeup 午睡起床时间 (HH:MM, 可选)
   * @param {Array|null} daytime_drowsiness 日间困倦记录列表 (可选)
   * @param {string|null} lifestyle 生活阶段代码 (可选)
   */
  input_sleep_data(night_bedtime, night_wakeup, nap_bedtime = null, nap_wakeup = null, daytime_drowsiness = null, lifestyle = null) {
    this.data = {
      night_bedtime,
      night_wakeup,
      nap_bedtime,
      nap_wakeup,
      daytime_drowsiness: daytime_drowsiness || [],
      lifestyle
    };

    if (lifestyle && this.LIFESTYLE_CONFIGS[lifestyle]) {
      this.lifestyle = lifestyle;
      this.lifestyle_config = this.LIFESTYLE_CONFIGS[lifestyle];
    }
  }

  /** 计算睡眠指标 */
  calculate_metrics() {
    // 夜间在床时长
    const night_time_in_bed = this.time_diff_minutes(
      this.data.night_bedtime,
      this.data.night_wakeup
    );

    // 估算实际睡眠时长（考虑入睡潜伏期和夜间觉醒）
    const sleep_onset_latency = 20; // 分钟
    const nighttime_awakenings_pct = 0.15;

    const estimated_sleep_time = (night_time_in_bed - sleep_onset_latency) * (1 - nighttime_awakenings_pct);

    // 睡眠效率
    const sleep_efficiency = (estimated_sleep_time / night_time_in_bed) * 100;

    // 睡眠债务（基于生活阶段调整推荐值）
    let recommended_mid;
    if (this.lifestyle_config) {
      recommended_mid = (this.lifestyle_config.sleep_range[0] + this.lifestyle_config.sleep_range[1]) / 2 * 60;
    } else {
      recommended_mid = (this.RECOMMENDED_SLEEP_HOURS[0] + this.RECOMMENDED_SLEEP_HOURS[1]) / 2 * 60;
    }
    const sleep_debt = recommended_mid - estimated_sleep_time;

    // 午睡时长
    let nap_duration = 0;
    if (this.data.nap_bedtime && this.data.nap_wakeup) {
      nap_duration = this.time_diff_minutes(
        this.data.nap_bedtime,
        this.data.nap_wakeup
      );
    }

    // 总睡眠时长
    const total_sleep = estimated_sleep_time + nap_duration;

    // 日间困倦评估
    const drowsiness_count = this.data.daytime_drowsiness.length;
    const drowsiness_details = this.data.daytime_drowsiness.map((d) => ({
      time: d.time,
      duration: d.duration !== undefined ? d.duration : 0,
      napped: d.napped !== undefined ? d.napped : false,
      nap_duration: d.nap_duration !== undefined ? d.nap_duration : 0
    }));

    this.metrics = {
      night_time_in_bed,
      estimated_sleep_time,
      sleep_efficiency,
      sleep_debt,
      nap_duration,
      total_sleep,
      drowsiness_count,
      drowsiness_details,
      recommended_sleep: recommended_mid / 60
    };

    return this.metrics;
  }

  /** 生成四个关键时间点（适配生活阶段） */
  generate_four_timepoints() {
    const metrics = this.metrics;

    // 1. 夜间起床时间 - 固定优先
    const current_wakeup = this.parse_time(this.data.night_wakeup);
    let wakeup_time = current_wakeup;

    // 根据生活阶段微调起床时间
    if (this.lifestyle_config) {
      if (this.lifestyle_config.stress_level === "high") {
        // 高压阶段建议稍晚起床，保证睡眠完整性
        if (current_wakeup < this.parse_time("06:30")) {
          wakeup_time = this.parse_time("06:30");
        }
      }
    }

    if (current_wakeup < this.parse_time("06:00")) {
      wakeup_time = this.parse_time("06:00");
    } else if (current_wakeup > this.parse_time("08:00")) {
      wakeup_time = this.parse_time("08:00");
    }

    // 2. 夜间上床时间 - 基于生活阶段推荐时长
    let target_sleep_hours;
    if (this.lifestyle_config) {
      target_sleep_hours = (this.lifestyle_config.sleep_range[0] + this.lifestyle_config.sleep_range[1]) / 2;
      // 体力型需要更多深度睡眠
      if (this.lifestyle === "skill_training_physical") {
        target_sleep_hours = this.lifestyle_config.sleep_range[1]; // 取上限
      }
    } else {
      target_sleep_hours = 7.5;
    }

    // 根据睡眠债务调整
    if (metrics.sleep_debt > 60) {
      target_sleep_hours += 0.5;
    } else if (metrics.sleep_debt < -30) {
      target_sleep_hours -= 0.5;
    }

    // 计算理想上床时间
    // 注意：Python 用 datetime 计算，跨过午夜的床上时间会落在"前一天"（日期更小），
    // 因此后续与 21:00/00:30 比较时永远小于 21:00 -> 被钳制为 21:00。
    // 这里用 day 偏移（0=当天, -1=前一天）完整复刻该语义。
    let raw = wakeup_time - target_sleep_hours * 60; // 可能为负
    let day = raw < 0 ? -1 : 0;
    let bedtime = ((raw % 1440) + 1440) % 1440;

    // 睡眠限制疗法（效率低时）
    if (metrics.sleep_efficiency < this.TARGET_SLEEP_EFFICIENCY) {
      const restriction = 30;
      bedtime += restriction;
      if (bedtime >= 1440) {
        bedtime -= 1440;
        day += 1;
      }
    }

    // 高压阶段提前上床（给予更多放松时间）
    if (this.lifestyle_config && this.lifestyle_config.stress_level === "high") {
      bedtime -= 15; // 提前15分钟上床放松
      if (bedtime < 0) {
        bedtime += 1440;
        day -= 1;
      }
    }

    // 确保在合理范围内（复刻 Python datetime 比较语义）
    const earliest_bedtime = this.parse_time("21:00");
    const latest_bedtime = this.parse_time("00:30");
    if (day < 0) {
      // 落在前一天：必然小于 21:00 -> 钳制为 21:00
      bedtime = earliest_bedtime;
    } else if (bedtime < earliest_bedtime) {
      bedtime = earliest_bedtime;
    } else if (bedtime > latest_bedtime) {
      bedtime = latest_bedtime;
    }

    // 3. 午睡时间（基于生活阶段）
    let nap_start = null;
    let nap_end = null;

    if (this.lifestyle_config && this.lifestyle_config.nap_recommended) {
      // 根据配置确定是否需要午睡
      if (metrics.sleep_debt > 30 || metrics.drowsiness_count >= 2) {
        nap_start = this.parse_time("13:30");

        // 根据生活阶段确定午睡时长
        let nap_duration;
        if (this.lifestyle === "skill_training_physical") {
          nap_duration = Math.min(30, this.lifestyle_config.nap_duration);
        } else {
          nap_duration = Math.min(20, this.lifestyle_config.nap_duration);
        }

        // 根据债务调整
        if (metrics.sleep_debt > 90) {
          nap_duration = Math.min(nap_duration + 5, 30);
        }

        nap_end = (nap_start + nap_duration) % 1440;
      }
    }

    this.plan = {
      night_bedtime: this.format_time(bedtime),
      night_wakeup: this.format_time(wakeup_time),
      nap_start: nap_start !== null ? this.format_time(nap_start) : null,
      nap_end: nap_end !== null ? this.format_time(nap_end) : null
    };

    return this.plan;
  }

  /** 生成8周渐进改善计划（适配生活阶段） */
  generate_progressive_plan() {
    // 基础计划
    const plan = {
      phase1: {
        weeks: "1-2",
        theme: "稳定节律",
        goals: [
          "固定每天起床时间（包括周末）",
          "建立睡前放松程序",
          "记录睡眠日记"
        ],
        actions: [
          `每天 ${this.plan.night_wakeup} 起床`,
          "睡前1小时：调暗灯光，避免蓝光",
          "睡前30分钟：温水澡或冥想",
          "晨间光照：起床后30分钟内接触自然光15-30分钟",
          "避免午后14:00后摄入咖啡因"
        ]
      },
      phase2: {
        weeks: "3-4",
        theme: "优化效率",
        goals: [
          "提高睡眠效率至85%以上",
          "缩短入睡潜伏期",
          "减少夜间觉醒"
        ],
        actions: [
          "如睡眠效率>85%，每3天提前上床15分钟",
          `目标上床时间：${this.plan.night_bedtime}`,
          "刺激控制：20分钟无法入睡即离开床",
          "睡眠限制：严格控制在床时间",
          "认知重构：建立'床=睡眠'的条件反射"
        ]
      },
      phase3: {
        weeks: "5-8",
        theme: "巩固维持",
        goals: [
          "达到目标睡眠时长和效率",
          "优化午睡策略",
          "建立长期睡眠卫生"
        ],
        actions: [
          `维持 ${this.plan.night_bedtime} - ${this.plan.night_wakeup} 睡眠窗口`,
          `午睡：${this.plan.nap_start || '无需午睡'} - ${this.plan.nap_end || 'N/A'}`,
          "环境优化：温度18-22°C，完全黑暗，安静",
          "周末保持相同作息，避免社交时差",
          "定期评估睡眠日记，微调计划"
        ]
      },
      phase4: {
        weeks: "持续",
        theme: "个性化优化",
        goals: [
          "根据生活变化调整",
          "预防失眠复发",
          "保持最佳日间功能"
        ],
        actions: [
          "旅行时：提前调整作息适应新时区",
          "压力大时：增加放松练习",
          "季节变化：调整光照暴露时间",
          "定期回顾：每月评估睡眠效率",
          "必要时：咨询睡眠专科医生"
        ]
      }
    };

    // 根据生活阶段添加特定建议
    if (this.lifestyle_config) {
      const lifestyle_actions = this.lifestyle_config.recommendations;
      plan.phase1.actions.push(...lifestyle_actions.slice(0, 2));
      plan.phase2.actions.push(...lifestyle_actions.slice(2));

      // 添加生活阶段特定目标
      if (this.lifestyle === "postgraduate_prep") {
        plan.phase1.goals.push("睡前1小时进行记忆巩固复习");
        plan.phase2.goals.push("优化睡眠结构以提升记忆提取");
      } else if (this.lifestyle === "skill_training_physical") {
        plan.phase1.goals.push("训练后充分冷却再入睡");
        plan.phase3.goals.push("监测肌肉恢复与睡眠质量关系");
      }
    }

    return plan;
  }

  /** 生成生活阶段分析 */
  generate_lifestyle_analysis() {
    if (!this.lifestyle_config) {
      return "";
    }

    const config = this.lifestyle_config;
    const metrics = this.metrics;

    const analysis = `
## 生活阶段分析：${config.name}

### 阶段特征
${config.description}

### 当前挑战
${config.challenges.map((c) => '- ' + c).join('\n')}

### 推荐睡眠参数
- **推荐睡眠时长**: ${pyFloatStr(config.sleep_range[0])}-${pyFloatStr(config.sleep_range[1])} 小时
- **当前估算睡眠**: ${pyRound(metrics.estimated_sleep_time / 60, 1)} 小时
- **睡眠缺口**: ${pyRound(Math.max(0, config.sleep_range[0] - metrics.estimated_sleep_time / 60), 1)} 小时
- **午睡建议**: ${config.nap_recommended ? '建议' : '可选'} (${config.nap_duration}分钟)

### 阶段特定建议
${config.recommendations.map((r) => '- ' + r).join('\n')}

### 认知负荷与压力管理
- **认知负荷**: ${config.cognitive_load}
- **压力水平**: ${config.stress_level}
- **建议**: ${config.stress_level === 'high' ? '睡前增加放松时间15-20分钟' : '保持规律放松练习'}
`;
    return analysis;
  }

  /** 生成完整报告（含生活阶段分析） */
  generate_report() {
    const metrics = this.calculate_metrics();
    const timepoints = this.generate_four_timepoints();
    const progressive_plan = this.generate_progressive_plan();
    const lifestyle_analysis = this.generate_lifestyle_analysis();

    const report = `
# 个性化睡眠优化报告

## 一、当前睡眠评估

### 基础指标
- **夜间在床时长**: ${pyRound(metrics.night_time_in_bed, 0)} 分钟 (${pyRound(metrics.night_time_in_bed / 60, 1)} 小时)
- **估算实际睡眠**: ${pyRound(metrics.estimated_sleep_time, 0)} 分钟 (${pyRound(metrics.estimated_sleep_time / 60, 1)} 小时)
- **睡眠效率**: ${pyRound(metrics.sleep_efficiency, 1)}%
- **睡眠债务**: ${pyRound(metrics.sleep_debt, 0)} 分钟 (${pyRound(metrics.sleep_debt / 60, 1)} 小时)
- **午睡时长**: ${pyRound(metrics.nap_duration, 0)} 分钟
- **日间困倦次数**: ${metrics.drowsiness_count} 次

### 评估结论
${metrics.sleep_efficiency >= 85 ? "[OK] 睡眠效率正常" : "[!] 睡眠效率偏低，建议优化"}
${metrics.sleep_debt <= 0 ? "[OK] 睡眠时长充足" : "[!] 存在睡眠债务，需要补偿"}
${metrics.drowsiness_count <= 1 ? "[OK] 日间功能良好" : "[!] 日间困倦较多，建议调整"}

### 睡眠可视化

${renderEfficiencyChart(metrics.sleep_efficiency)}
${renderDurationChart(metrics, this.lifestyle_config)}
${lifestyle_analysis}

## 二、优化后的四个关键时间点

| 时间点 | 当前 | 优化后 | 调整建议 |
|--------|------|--------|----------|
| 夜间上床 | ${this.data.night_bedtime} | ${timepoints.night_bedtime} | ${this.parse_time(timepoints.night_bedtime) < this.parse_time(this.data.night_bedtime) ? "提前" : this.parse_time(timepoints.night_bedtime) > this.parse_time(this.data.night_bedtime) ? "推迟" : "保持"} |
| 夜间起床 | ${this.data.night_wakeup} | ${timepoints.night_wakeup} | ${this.parse_time(timepoints.night_wakeup) < this.parse_time(this.data.night_wakeup) ? "提前" : this.parse_time(timepoints.night_wakeup) > this.parse_time(this.data.night_wakeup) ? "推迟" : "保持"} |
| 午睡开始 | ${this.data.nap_bedtime || 'N/A'} | ${timepoints.nap_start || '无需午睡'} | - |
| 午睡结束 | ${this.data.nap_wakeup || 'N/A'} | ${timepoints.nap_end || 'N/A'} | - |

${renderWindowChart(this.data, timepoints)}

## 三、8周渐进改善计划

${renderPlanVisual()}

### 第1-2周：稳定节律
**目标**: 建立固定作息，重置生物钟

关键行动：
${progressive_plan.phase1.actions.map((action) => '- ' + action).join('\n')}

### 第3-4周：优化效率
**目标**: 提高睡眠效率，缩短入睡时间

关键行动：
${progressive_plan.phase2.actions.map((action) => '- ' + action).join('\n')}

### 第5-8周：巩固维持
**目标**: 达到并维持理想睡眠模式

关键行动：
${progressive_plan.phase3.actions.map((action) => '- ' + action).join('\n')}

### 长期：个性化优化
**目标**: 适应生活变化，预防复发

关键行动：
${progressive_plan.phase4.actions.map((action) => '- ' + action).join('\n')}

## 四、每日执行清单

### 早晨
- [ ] ${timepoints.night_wakeup} 准时起床（无论多困）
- [ ] 起床后30分钟内接触自然光15-30分钟
- [ ] 简单伸展或轻度运动

### 白天
- [ ] 避免午后14:00后咖啡因
- [ ] 保持适度活动
- [ ] 如有午睡：${timepoints.nap_start || '无需午睡'} - ${timepoints.nap_end || 'N/A'}

### 晚间
- [ ] 睡前3小时：避免大量进食和酒精
- [ ] 睡前1小时：调暗灯光，停止使用电子设备
- [ ] 睡前30分钟：放松活动（阅读、冥想、温水澡）
- [ ] ${timepoints.night_bedtime} 上床准备入睡

## 五、重要提醒

${renderArchitectureChart()}
1. **固定起床时间是关键**：无论前一晚睡得多晚，都在同一时间起床
2. **床只用于睡眠**：避免在床上工作、玩手机或看电视
3. **20分钟规则**：如果躺下20分钟还未入睡，起床做些放松的事
4. **避免补偿性赖床**：周末也保持相同作息
5. **记录睡眠日记**：每天记录上床时间、入睡时间、觉醒次数、起床时间

## 六、何时就医

如出现以下情况，建议咨询睡眠专科医生：
- 失眠持续超过3个月
- 严重日间嗜睡影响工作/学习
- 睡眠中呼吸暂停或打鼾严重
- 不宁腿症状
- 抑郁或焦虑症状

---
*本报告基于循证睡眠医学研究生成，仅供参考，不能替代专业医疗建议。*
*生活阶段适配参考：Lund et al.(2010); Rasch & Born(2013); Kredlow et al.(2015)等研究*
*图表科学依据：睡眠效率≥85%（Spielman et al., 1987 睡眠限制疗法；Morin et al., 2006）；NREM-REM周期约90分钟、一夜4-5周期（Carskadon & Dement, 2011）；睡眠债（Van Dongen et al., 2003）；社交时差<2h（Wittmann et al., 2006）*
`;

    return report;
  }
}

// ==================== 命令行入口 ====================

function printError(msg) {
  console.error(`错误: ${msg}`);
}

function main() {
  // 解析 --key value / --key=value 参数
  const ALLOWED_KEYS = ["lifestyle", "bedtime", "wakeup", "nap-start", "nap-end", "drowsiness", "output"];
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith('--')) {
      let key = a.slice(2);
      let value;
      const eq = key.indexOf('=');
      if (eq !== -1) {
        value = key.slice(eq + 1);
        key = key.slice(0, eq);
      } else {
        value = args[++i];
        if (value === undefined) {
          printError(`参数 --${key} 缺少值`);
          process.exit(1);
        }
      }
      if (!ALLOWED_KEYS.includes(key)) {
        printError(`未知参数: --${key}`);
        process.exit(1);
      }
      opts[key] = value;
    } else {
      printError(`未知参数: ${a}`);
      process.exit(1);
    }
  }

  const optimizer = new SleepOptimizer();

  // 用户数据模式：有实际睡眠时间或生活阶段时，用传入数据生成报告
  if (opts.bedtime || opts.wakeup || opts.lifestyle) {
    if (!opts.bedtime || !opts.wakeup) {
      printError("--bedtime 和 --wakeup 必须同时提供（HH:MM 格式）");
      process.exit(1);
    }
    if (opts.lifestyle && !optimizer.LIFESTYLE_CONFIGS[opts.lifestyle]) {
      printError(`未知生活阶段: ${opts.lifestyle}。可选: ${Object.keys(optimizer.LIFESTYLE_CONFIGS).join(', ')}`);
      process.exit(1);
    }

    let drowsiness = [];
    if (opts.drowsiness) {
      let raw = opts.drowsiness;
      // 支持 @文件路径：避免 Windows 命令行转义 JSON 引号的问题
      if (raw.startsWith('@')) {
        try {
          raw = require('fs').readFileSync(raw.slice(1), 'utf8');
        } catch (e) {
          printError(`无法读取困倦记录文件: ${e.message}`);
          process.exit(1);
        }
      }
      try {
        drowsiness = JSON.parse(raw);
      } catch (e) {
        printError(`--drowsiness 不是合法 JSON: ${e.message}`);
        process.exit(1);
      }
    }

    try {
      optimizer.input_sleep_data(
        opts.bedtime,
        opts.wakeup,
        opts['nap-start'] || null,
        opts['nap-end'] || null,
        drowsiness,
        opts.lifestyle || null
      );
    } catch (e) {
      printError(e.message);
      process.exit(1);
    }

    const report = optimizer.generate_report();
    process.stdout.write(report + '\n');
    if (opts.output) {
      const fs = require('fs');
      fs.writeFileSync(opts.output, report, 'utf8');
      // 同时生成可视化 SVG 图表文件（同名 .chart.svg）
      const svg = renderSvgChart(optimizer.data, optimizer.metrics, optimizer.plan, optimizer.lifestyle_config);
      const svgPath = opts.output.replace(/\.md$/i, '') + '.chart.svg';
      fs.writeFileSync(svgPath, svg, 'utf8');
    }
    return;
  }

  // 示例模式：无参数时运行内置示例（考研备考学生）
  optimizer.input_sleep_data(
    "00:30",
    "07:30",
    "13:30",
    "14:00",
    [
      { time: "15:00", duration: 20, napped: false, nap_duration: 0 },
      { time: "21:00", duration: 15, napped: false, nap_duration: 0 }
    ],
    "postgraduate_prep" // 考研备考阶段
  );

  const report = optimizer.generate_report();
  process.stdout.write(report + '\n');

  // 保存报告
  require('fs').writeFileSync("sleep_report.md", report, 'utf8');
}

main();
