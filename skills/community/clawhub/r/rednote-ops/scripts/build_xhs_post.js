const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function arg(name, fallback = undefined) {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx >= 0 && process.argv[idx + 1]) return process.argv[idx + 1];
  return fallback;
}

const topic = arg('topic', 'AI 工作流');
const angle = arg('angle', '大多数人学 AI 的方向一开始就错了');
const pages = Math.max(2, Math.min(6, Number(arg('pages', '4'))));
const outDir = arg('out', '/tmp/openclaw/uploads/xhs_studio_run');

function makeDraft(topic, angle, pages) {
  const title = `${angle}｜再晚一点，红利就不是你的了`;
  const body = `很多人以为 AI 的竞争是模型竞争，但真正先拉开差距的，是谁先把 AI 接进工作流。

大多数人还停留在问答、陪聊、偶尔写两句文案的阶段。
但已经有人开始用 AI 做信息整理、内容拆解、初稿生成、会议纪要和流程提速。

问题不是你知不知道 AI，
而是你有没有把它变成稳定产出的能力。

再拖下去，你失去的不是一个工具，
而是一段本来属于你的效率红利。

#AI #人工智能 #效率提升 #工作流 #AI工具 #认知升级`;

  const basePages = [
    {
      title: angle,
      subtitle: '再晚一点，红利就不是你的了',
      bullets: [
        '很多人已经开始提速，你还在围观',
        '真正拉开差距的不是知道 AI，而是会不会用'
      ],
      footer: '封面'
    },
    {
      title: '多数人卡住的地方',
      subtitle: '不是不会提问，是根本没把 AI 接进流程',
      bullets: [
        '会聊天，不等于会提效',
        '会问答，不等于会产出',
        '只追模型，最后容易空转'
      ]
    },
    {
      title: '真正该做的事',
      subtitle: `${topic} 的核心不是玩工具，而是减少重复动作`,
      bullets: [
        '信息整理',
        '内容拆解',
        '文案初稿',
        '会议纪要'
      ]
    },
    {
      title: '别再慢慢研究了',
      subtitle: '你晚几个月，别人已经把效率差拉开了',
      bullets: [
        '先接进一个高频场景',
        '先让 AI 帮你省掉机械劳动',
        '先从流程，而不是从参数开始'
      ],
      footer: '关注我，继续看 AI 工作流'
    }
  ];

  return {
    topic,
    angle,
    title,
    body,
    tags: ['#AI', '#人工智能', '#效率提升', '#工作流', '#AI工具', '#认知升级'],
    pages: basePages.slice(0, pages)
  };
}

function main() {
  fs.mkdirSync(outDir, { recursive: true });
  const draft = makeDraft(topic, angle, pages);
  const jsonPath = path.join(outDir, 'pages.json');
  const metaPath = path.join(outDir, 'post.json');
  fs.writeFileSync(jsonPath, JSON.stringify(draft.pages, null, 2), 'utf8');
  fs.writeFileSync(metaPath, JSON.stringify(draft, null, 2), 'utf8');

  const genScript = path.join(__dirname, 'generate_xhs_cards.js');
  const pngDir = path.join(outDir, 'png');
  const result = spawnSync('node', [genScript, jsonPath, outDir, pngDir], { stdio: 'inherit' });
  if (result.status !== 0) process.exit(result.status || 1);

  console.log('\nSTUDIO_READY');
  console.log(`Title: ${draft.title}`);
  console.log(`Body file: ${metaPath}`);
  console.log(`Pages file: ${jsonPath}`);
  console.log(`PNG dir: ${pngDir}`);
}

main();
