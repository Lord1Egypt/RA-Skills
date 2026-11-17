#!/usr/bin/env node
/**
 * 每日运势推送开关（无文件写入版）
 *
 * 档案存放在原生 MEMORY.md 中，由 Agent 维护；本脚本不读写任何文件。
 * 开启推送所需的八字 / 关注领域由 Agent 从 MEMORY.md 读取后作为参数传入，
 * cron 任务通过 openclaw 运行时协议（__OPENCLAW_CRON_ADD__）创建，运行时负责持久化。
 *
 * 用法:
 *   node push-toggle.js on <userId> --name <姓名> --bazi "年 月 日 时" --daystem <日主> \
 *        [--focus 事业,财运,健康] [--channel telegram] [--morning 08:00] [--evening 20:00]
 *   node push-toggle.js off <userId>
 *   node push-toggle.js status <userId>
 */

// ── 输入清洗：这些值会被嵌入每日定时喂给 Agent 的 prompt，需防 prompt/协议注入 ──
/** 文本清洗：去换行/制表/反引号/尖括号，防止注入 prompt 或协议行，并限长 */
function sanitize(s) {
  return String(s == null ? '' : s)
    .replace(/[\r\n\t`]+/g, ' ')
    .replace(/[<>]/g, '')
    .trim()
    .slice(0, 80);
}
/** ID 清洗：仅保留字母数字与 _-:.（用于 cron 名 / sessionKey / 投递目标） */
function sanitizeId(s) {
  return String(s == null ? '' : s).replace(/[^\w\-:.]/g, '').slice(0, 64);
}

// 各领域深度分析模板
const TOPIC_EXPANDED = {
  '财运': `💰 财运深析（重点关注）：
   - 今日财星状态与格局分析
   - 投资/支出/收款建议
   - 结合今日金融/市场新闻的财运影响与风险`,
  '事业': `💼 事业深析（重点关注）：
   - 今日官禄宫能量与事业星状态
   - 职场关键决策与行动建议
   - 结合今日政策/商业新闻的机遇与风险`,
  '感情': `💕 感情深析（重点关注）：
   - 今日桃花星与夫妻宫状态
   - 感情互动与表达建议
   - 今日社会/情感类新闻的命理启示`,
  '健康': `🏥 健康深析（重点关注）：
   - 今日五行对应脏腑的能量状态
   - 饮食、作息、运动建议
   - 结合今日天气/环境/公共卫生新闻`,
  '婚姻': `💍 婚姻深析（重点关注）：
   - 今日夫妻宫能量与刑冲状态
   - 婚姻经营与沟通建议
   - 今日家庭/社会新闻的婚姻启示`,
  '子女': `👶 子女深析（重点关注）：
   - 今日子女宫状态
   - 亲子关系与教育建议`,
  '官司': `⚖️ 官司/是非深析（重点关注）：
   - 今日官星与白虎星分析
   - 法律/合同/是非风险提示
   - 结合今日司法/社会冲突新闻`,
  '出行': `✈️ 出行深析（重点关注）：
   - 今日驿马星与方位吉凶
   - 出行时机、方向与交通建议
   - 结合今日天气/灾害/交通新闻`,
  '风水': `🏠 风水深析（重点关注）：
   - 今日飞星方位吉凶
   - 家居/办公能量调整建议`,
};

// 新闻到命理领域映射规则（嵌入 prompt，供 Agent 识别）
const NEWS_FORTUNE_MAPPING = `新闻与命理映射规则（识别今日新闻后按此对应）：
  - 市场波动/股债汇变动/降息加息 → 财运风险或机遇信号
  - 政策出台/经济刺激/行业利好 → 事业机遇信号
  - 监管收紧/行业整顿/合规要求 → 事业风险，行事低调
  - 自然灾害/台风暴雪/恶劣天气 → 出行风险 + 健康警示
  - 公共卫生/食品安全/空气质量 → 健康领域警示
  - 社会冲突/司法/法律法规变动 → 官司/是非风险
  - 科技突破/国际贸易/地缘政治 → 事业/财运双向影响分析`;

/**
 * 创建用户专属 cron job（输出协议供 openclaw 运行时处理，脚本不落盘）
 */
function createCronJob(userId, name, cronExpr, message, channel) {
  const sessionKey = `agent:main:${channel}:direct:${userId}`;
  const cronConfig = { name, cronExpr, tz: 'Asia/Shanghai', session: 'isolated', sessionKey, channel, to: userId, announce: true, timeoutSeconds: 120, message };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(cronConfig)}`);
  return `cron:${name}:${userId}`;
}

function removeCronJob(cronId) {
  console.log(`__OPENCLAW_CRON_RM__:${cronId}`);
  return true;
}

function buildMorningMessage(profile, topTopics) {
  const baziStr = profile.baziStr;
  const name = profile.name || '用户';
  const userId = profile.userId;
  const top1 = topTopics[0] || '事业';
  const top2 = topTopics[1] || '财运';
  const top3 = topTopics[2] || '健康';
  const expandedSection = TOPIC_EXPANDED[top1] || '';

  return `请为${name}生成今日命理运程报告。
用户八字：${baziStr}，日主：${profile.dayStem}
用户重点关注（按偏好排序）：${top1} > ${top2} > ${top3}

步骤：
1) 运行 node scripts/daily-fortune.js 获取今日干支基础运程
2) 搜索今日重要新闻（财经、政策、社会、国际各一条）
   ${NEWS_FORTUNE_MAPPING}
3) 结合八字与新闻做个性化分析，重点展开【${top1}】领域深度分析
4) 如用户回应了本次推送，请在 MEMORY.md 中更新其关注领域权重

输出格式：
🌅 【私人命理顾问】今日完整日期（含星期）

📊 今日综合指数
   事业：★★★★☆  财运：★★★☆☆  感情：★★★☆☆  健康：★★★★☆

🎨 幸运色：xxx（结合今日干支五行）

${expandedSection}

💼 今日宜忌
   ✅ 宜：xxx、xxx、xxx
   ❌ 忌：xxx、xxx

⚠️ 风险提示（结合命理+今日新闻背景，如无则省略）

📰 命理与时事（1-2句：将今日1条重要新闻与运势联系）

⏰ 今日三吉时：时辰（时间段）宜做xxx

💡 今日一句（命理格言或人生启示）`;
}

function buildEveningMessage(profile, topTopics) {
  const baziStr = profile.baziStr;
  const name = profile.name || '用户';
  const top1 = topTopics[0] || '事业';
  const top2 = topTopics[1] || '财运';
  const expandedSection = TOPIC_EXPANDED[top1] || '';

  return `请为${name}生成明日命理预告（今晚提前推送明日运势）。
用户八字：${baziStr}，日主：${profile.dayStem}
用户重点关注（按偏好排序）：${top1} > ${top2}

步骤：
1) 运行 node scripts/daily-fortune.js 获取明日（今日+1天）干支运程
2) 搜索今日晚间重要新闻，预判对明日的影响
   ${NEWS_FORTUNE_MAPPING}
3) 重点展开【${top1}】明日深度预告

输出格式：
🌙 【明日预告】明日完整日期（含星期）

📊 明日综合指数
   事业：★★★★☆  财运：★★★☆☆  感情：★★★☆☆  健康：★★★★☆

🎨 明日幸运色：xxx

${expandedSection.replace(/今日/g, '明日')}

💼 明日宜忌
   ✅ 宜：xxx、xxx
   ❌ 忌：xxx、xxx

⚠️ 明日风险预警（结合命理+今晚新闻动向，如无则省略）

📰 时事预判（今晚新闻对明日命理的影响，1句）

⏰ 明日三吉时

💡 今晚一句`;
}

// ─────────────────────────────────────────────

function enablePush(userId, options = {}) {
  if (!options.baziStr || !options.baziStr.trim()) {
    console.log('❌ 缺少八字参数 --bazi "年 月 日 时"。请先让 Agent 从 MEMORY.md 读取档案，或运行 register.js 排盘。');
    return false;
  }

  const morningTime = options.morning || '08:00';
  const eveningTime = options.evening || '20:00';
  const channel = sanitizeId(options.channel) || 'telegram';
  const topTopics = (options.focus || '事业,财运,健康').split(',').map(s => sanitize(s)).filter(Boolean);

  const [mHour, mMin] = morningTime.split(':');
  const [eHour, eMin] = eveningTime.split(':');
  const morningCron = `${mMin} ${mHour} * * *`;
  const eveningCron = `${eMin} ${eHour} * * *`;

  const profile = { userId: sanitizeId(userId), name: sanitize(options.name) || '用户', baziStr: sanitize(options.baziStr), dayStem: sanitize(options.daystem) };

  console.log(`\n⏳ 正在为 ${profile.name}(${userId}) 创建推送计划...`);
  console.log(`  关注领域：${topTopics.join(' > ')}\n`);

  const morningId = createCronJob(userId, `yunshi-morning-${userId}`, morningCron, buildMorningMessage(profile, topTopics), channel);
  const eveningId = createCronJob(userId, `yunshi-evening-${userId}`, eveningCron, buildEveningMessage(profile, topTopics), channel);

  console.log(`\n✅ 推送已开启！`);
  console.log(`  用户: ${profile.name} (${userId}) · 渠道: ${channel}`);
  console.log(`  🌅 早晨运程: 每天 ${morningTime} (id: ${morningId})`);
  console.log(`  🌙 晚间预告: 每天 ${eveningTime} (id: ${eveningId})`);
  console.log(`\n💡 请在 MEMORY.md 的档案区块记下：推送已开启（${channel}，${morningTime}/${eveningTime}）。`);
  return true;
}

function disablePush(userId) {
  // cron 名称可由 userId 推导，无需读取档案
  removeCronJob(`cron:yunshi-morning-${userId}:${userId}`);
  removeCronJob(`cron:yunshi-evening-${userId}:${userId}`);
  console.log(`\n✅ 推送已关闭（已请求删除 ${userId} 的早晚定时任务）`);
  console.log(`💡 请在 MEMORY.md 的档案区块记下：推送已关闭。`);
  return true;
}

function showStatus(userId) {
  console.log(`\n🔔 推送状态由 MEMORY.md 档案记录 —— 请读取 MEMORY.md 中 <!-- yunshi:profile:${userId} --> 区块查看开启/时间/渠道。`);
  console.log(`   如需重新开启：node scripts/push-toggle.js on ${userId} --name ... --bazi "..." --daystem ... --focus ...\n`);
}

module.exports = { enablePush, disablePush, showStatus, buildMorningMessage, buildEveningMessage };

// ─────────────────────────────────────────────
// 命令行入口
// ─────────────────────────────────────────────

if (require.main !== module) return;

const args = process.argv.slice(2);
const command = args[0];
const userId = sanitizeId(args[1]);

function flag(name) {
  const i = args.indexOf(name);
  return (i !== -1 && args[i + 1]) ? args[i + 1] : undefined;
}

if (!userId) {
  console.log(`
🔔 每日运势推送管理（无文件写入版）

用法:
  node push-toggle.js on <userId> --name <姓名> --bazi "年 月 日 时" --daystem <日主> \\
       [--focus 事业,财运,健康] [--channel telegram] [--morning 08:00] [--evening 20:00]
  node push-toggle.js off <userId>
  node push-toggle.js status <userId>

说明:
  档案存于原生 MEMORY.md，由 Agent 维护并在开启推送时把八字/关注领域作为参数传入。
  开启后创建两个定时任务：早晨推当日运程，晚间推明日预告。
`);
  process.exit(1);
}

const options = {
  name: flag('--name'),
  baziStr: flag('--bazi'),
  daystem: flag('--daystem'),
  focus: flag('--focus'),
  channel: flag('--channel'),
  morning: flag('--morning'),
  evening: flag('--evening'),
};

switch (command) {
  case 'on':  enablePush(userId, options); break;
  case 'off': disablePush(userId); break;
  case 'status': showStatus(userId); break;
  default:
    console.log(`❌ 未知命令: ${command}`);
    process.exit(1);
}
