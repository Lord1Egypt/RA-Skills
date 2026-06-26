#!/usr/bin/env node
/**
 * 聊天助理 - 幽默风趣回复生成器
 * 输入她说的话 → 输出多个回复选项 + 分析
 */

const SHE_PHRASES = {
  // 敷衍型
  '嗯': { type: '敷衍', level: 'danger', replies: [
    { text: '就一个字，你是在考验我肺活量吗', emoji: '🤨' },
    { text: '嗯——这也太惜字如金了，不过我喜欢', emoji: '😏' },
    { text: '好的收到，那我继续说，你继续嗯', emoji: '😂' },
  ], tip: '她在敷衍/忙/情绪一般。不要追问，给她空间，换个轻松话题再试' },

  '哦': { type: '敷衍', level: 'danger', replies: [
    { text: "哦？那你发现什么有趣的事了吗", emoji: '👀' },
    { text: '你这语气让我有点慌，正常回复是这样吗：「哦～好的！」', emoji: '😅' },
    { text: '收到，那我先存着，回头一起说', emoji: '📝' },
  ], tip: '冷淡信号。不要连发消息，隔1-2小时换个有趣话题重启' },

  '在忙': { type: '忙', level: 'warning', replies: [
    { text: '好，你先忙，忙完来找我，我等你', emoji: '👍' },
    { text: '去吧！我的消息随时都在，不急', emoji: '🫡' },
    { text: '收到，等你忙完了说一声', emoji: '📌' },
  ], tip: '她是真的忙，不是拒绝。表示理解+表达愿意等，比一直问好得多' },

  '哈哈': { type: '开心', level: 'good', replies: [
    { text: '你笑起来一定很好看', emoji: '😊' },
    { text: '哈！看来我说话还行，继续保持', emoji: '😎' },
    { text: '笑成这样，今天心情不错啊', emoji: '🤭' },
  ], tip: '积极信号！她笑了=情绪好，可以继续当前话题或轻微推进' },

  '哈哈哈': { type: '真开心', level: 'great', replies: [
    { text: '笑了就值了，再说一个', emoji: '😄' },
    { text: '三个哈，看来我是有点东西的', emoji: '🤓' },
    { text: '你这笑法，我要收藏了', emoji: '❤️' },
  ], tip: '非常好的信号！情绪到位，可以适度调情或约出来' },

  '？？': { type: '疑惑', level: 'neutral', replies: [
    { text: '翻译过来就是：你认真的吗？——是的我很认真', emoji: '😂' },
    { text: '问号太多，我开始怀疑人生了', emoji: '🤔' },
    { text: '别问了，再问我也要打问号了', emoji: '⁉️' },
  ], tip: '她没理解你的意思或觉得你有点奇怪，用幽默化解尴尬' },

  '什么意思': { type: '追问', level: 'neutral', replies: [
    { text: '字面意思，你品，你细品', emoji: '😏' },
    { text: '没别的意思，就是觉得你有趣', emoji: '😊' },
    { text: '意思是……我想多了解你一点？', emoji: '🤭' },
  ], tip: '追问说明她在认真对待。给正面回答，不要绕弯子' },

  '你怎么知道': { type: '惊讶', level: 'good', replies: [
    { text: '我会算啊，专攻你这卦', emoji: '🔮' },
    { text: '猜的，厉害吧', emoji: '😎' },
    { text: '秘密，先不告诉你', emoji: '🤫' },
  ], tip: '她对你的洞察力有好感。可以继续展示你懂她的面' },

  '你真烦': { type: '假生气', level: 'great', replies: [
    { text: '烦着烦着你就习惯了', emoji: '😏' },
    { text: '嘴上说烦，身体很诚实嘛', emoji: '🤭' },
    { text: '我知道，你嫌我烦是因为说少了，多说点就习惯了', emoji: '😂' },
  ], tip: '假生气真撒娇！她在给你机会继续聊，别停' },

  '滚': { type: '假生气', level: 'warning', replies: [
    { text: '好滚，但你得告诉我去哪', emoji: '😂' },
    { text: '滚远了记得把我捡回来', emoji: '🥺' },
  ], tip: '假生气可以接得住。但如果连续3次都是这种语气就真的烦了，收一收' },

  '随便': { type: '无感', level: 'danger', replies: [
    { text: '随便选，你这话说的，我选你', emoji: '😏' },
    { text: '那我来定，你负责开心就行', emoji: '👍' },
    { text: '这两个随便都不是给你的吗？那我随便选了啊', emoji: '🤔' },
  ], tip: '她说随便=不想动脑子/对你还在观望。你要主动做决定+展示主导力' },

  '没干嘛': { type: '无聊', level: 'neutral', replies: [
    { text: '没干嘛的时候最适合和我聊天了', emoji: '😏' },
    { text: '那正好，我给你讲讲我今天遇到的事', emoji: '📖' },
    { text: '无聊的时候就来找我，这个理由够不够', emoji: '🤭' },
  ], tip: '她无聊=有窗口。主动开启话题，约出来的好时机' },

  '吃了吗': { type: '问候', level: 'good', replies: [
    { text: '吃了，想你想得吃不下', emoji: '😏' },
    { text: '正在吃，跟我说说你吃的啥，让我也馋一下', emoji: '🤤' },
    { text: '还没，等你呢', emoji: '😎' },
  ], tip: '主动问候说明她在想着你。可以借机延续话题或约饭' },

  '晚安': { type: '结束', level: 'good', replies: [
    { text: '晚安，梦里见，不见不散', emoji: '🌙' },
    { text: '晚安～记得喝水，明天不许变丑', emoji: '😴' },
    { text: '晚安，我的聊天搭子明天见', emoji: '👋' },
  ], tip: '她说晚安=今天聊天愉快。温暖收尾，不要再追发了' },

  '你叫什么': { type: '初识', level: 'good', replies: [
    { text: '我叫XXX（停顿）——骗你的，你猜', emoji: '😏' },
    { text: '名字不重要，重要的是我们聊得来', emoji: '😎' },
    { text: 'XXX，你呢', emoji: '😊' },
  ], tip: '她在主动了解你。直接给名字+反问，不要绕弯子' },
};

// 通用回复生成（用于没匹配上的情况）
function genReply(text) {
  const t = text.toLowerCase();
  if (t.includes('吗') || t.includes('么') || t.includes('?') || t.includes('？')) {
    return [
      { text: '你猜', emoji: '😏' },
      { text: '不告诉你，猜中有奖', emoji: '🤭' },
      { text: '与其问我，不如你先说说自己', emoji: '😎' },
    ];
  }
  if (t.includes('我') || t.includes('你')) {
    return [
      { text: '说下去，我听着呢', emoji: '👂' },
      { text: '你继续，这个话题我喜欢', emoji: '😊' },
    ];
  }
  return [
    { text: '有点意思，继续说', emoji: '👀' },
    { text: '你这人说话很有意思', emoji: '🤔' },
    { text: '等等，我消化一下', emoji: '🤓' },
  ];
}

function analyze(text) {
  // 先精确匹配
  for (const [keyword, data] of Object.entries(SHE_PHRASES)) {
    if (text.includes(keyword)) {
      return data;
    }
  }
  // 模糊匹配
  const t = text.toLowerCase();
  for (const [keyword, data] of Object.entries(SHE_PHRASES)) {
    if (t.includes(keyword.toLowerCase())) return data;
  }
  return null;
}

function format(replies) {
  return replies.map((r, i) => `  ${i + 1}. ${r.emoji} ${r.text}`).join('\n');
}

const args = process.argv.slice(2);
const herMsg = args.join(' ');

if (!herMsg) {
  console.log(`
💬 聊天助理 - 使用方法

输入她说的话，给出幽默风趣的回复参考

示例:
  node chat.js 哈哈哈
  node chat.js 你怎么知道的
  node chat.js 你叫什么名字
  node chat.js 随便吧
  `);
  console.log('\n支持匹配的类型:', Object.keys(SHE_PHRASES).join(' | '));
  process.exit(0);
}

const result = analyze(herMsg);
const replies = result ? result.replies : genReply(herMsg);

console.log('\n👧 她说:', herMsg);
console.log('─────────────────────────────────');
console.log('\n🎯 推荐回复:\n');
console.log(format(replies));
if (result) {
  console.log('\n💡 分析:', result.tip);
  const levelMap = { great: '🟢', good: '🟢', warning: '🟡', danger: '🔴', neutral: '⚪' };
  console.log('📊 情绪判断:', levelMap[result.level] || '⚪', result.type);
} else {
  console.log('\n💡 分析: 没匹配到精准类型，用通用回复+真诚接话');
}
console.log();
