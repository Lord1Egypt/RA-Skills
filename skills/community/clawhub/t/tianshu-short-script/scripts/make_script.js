#!/usr/bin/env node
/**
 * 短视频口播分镜表
 * node make_script.js --topic "..." --seconds 60 --shots 6 --platform douyin
 */

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {
    topic: '',
    seconds: 60,
    shots: null,
    platform: 'douyin',
  };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if ((a === '--topic' || a === '-t') && args[i + 1]) out.topic = args[++i];
    else if ((a === '--seconds' || a === '-s') && args[i + 1])
      out.seconds = Math.max(15, parseInt(args[++i], 10) || 60);
    else if ((a === '--shots' || a === '-n') && args[i + 1])
      out.shots = Math.min(12, Math.max(3, parseInt(args[++i], 10) || 0));
    else if ((a === '--platform' || a === '-p') && args[i + 1]) out.platform = args[++i];
  }
  return out;
}

const PLATFORM_HINTS = {
  douyin: {
    hook: '前 3 秒：悬念/反差/痛点，避免免责声明式开场',
    cta: '结尾：关注 + 评论关键词/点击主页（按你的账号定位改写）',
  },
  wechat: {
    hook: '前 5 秒：身份 + 价值承诺，适合视频号竖屏',
    cta: '结尾：引导私信/企微/收藏本视频（注意平台引流规则）',
  },
  bilibili: {
    hook: '前 10 秒：梗或三连提示适度出现，忌冗长',
    cta: '结尾：点赞投币 + 下期预告',
  },
};

function distributeSeconds(total, n) {
  const base = Math.floor(total / n);
  const rest = total % n;
  const arr = Array(n).fill(base);
  for (let i = 0; i < rest; i++) arr[i] += 1;
  return arr;
}

function main() {
  const opts = parseArgs();
  if (!opts.topic.trim()) {
    console.error('用法: node make_script.js --topic "主题" [--seconds 60] [--shots 6] [--platform douyin|wechat|bilibili]');
    process.exit(1);
  }

  const n =
    opts.shots || Math.min(12, Math.max(3, Math.round(opts.seconds / 10)));
  const durations = distributeSeconds(opts.seconds, n);
  const hints = PLATFORM_HINTS[opts.platform] || PLATFORM_HINTS.douyin;

  const shotTemplates = [
    ['片头/钩子', '人物中近景或大字封面', '点题 + 抛出问题或结果 preview'],
    ['痛点展开', '素材混剪或侧拍', '类比/场景，让用户对号入座'],
    ['核心信息 1', '特写关键道具/界面', '第一条干货，短句密集'],
    ['核心信息 2', '切换场景防疲劳', '第二条干货，可举例'],
    ['核心信息 3', '对比前后', '小结/强化记忆点'],
    ['信任背书', '数据/案例截图（注意授权）', '轻量背书，忌夸大'],
    ['互动', '对镜头提问', '引导评论关键词'],
    ['结尾 CTA', '固定结尾版式', '关注/下载/私信（按合规改写）'],
  ];

  const lines = [];
  lines.push(`## 短视频分镜稿（${opts.platform}｜约 ${opts.seconds}s）\n`);
  lines.push(`**主题：** ${opts.topic.trim()}\n`);
  lines.push('### 片头与结尾原则\n');
  lines.push(`- **片头：** ${hints.hook}`);
  lines.push(`- **结尾：** ${hints.cta}`);
  lines.push('');
  lines.push('| 镜号 | 时长(s) | 画面/景别 | 口播要点 | 花字/字幕 |');
  lines.push('| --- | --- | --- | --- | --- |');

  for (let i = 0; i < n; i++) {
    const tpl = shotTemplates[Math.min(i, shotTemplates.length - 1)];
    const rowShot = tpl[0];
    const rowVisual = tpl[1];
    const rowTalk = tpl[2];
    lines.push(
      `| ${i + 1} | ${durations[i]} | ${rowShot}：${rowVisual} | 结合主题：${rowTalk} | 关键词大字报 |`
    );
  }

  lines.push('');
  lines.push('### 给剪辑/拍摄的备注');
  lines.push('- 口播要点列需替换为你的具体 product/案例细节；可用天树模型扩写每格台词。');
  lines.push('- 单条时长已为整数拆分，实拍可按现场 ±1～2 秒微调。');
  lines.push('- BGM 节奏点建议落在「核心信息」切换处。');

  process.stdout.write(lines.join('\n') + '\n');
}

main();
