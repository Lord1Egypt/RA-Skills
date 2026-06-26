/**
 * 暖男话术库 - 结合女孩心理学的得体搭讪/聊天话术
 * 不油腻、不土味、展现情商与真诚
 */

const opening = {
  dating: [
    { text: "你拍照一定不需要美颜吧？", type: "夸奖" },
    { text: "你这么会聊天，朋友圈肯定很热闹", type: "幽默夸" },
    { text: "看你发的动态，感觉你是个很有趣的人", type: "真诚好奇" },
    { text: "我发现你说话的方式很特别诶", type: "细节夸" },
  ],
  wechat: [
    { text: "今天发现一家很棒的小店，想分享给你", type: "价值展示+分享" },
    { text: "刚在路上看到一只狗，突然想到你说你喜欢", type: "关联感" },
    { text: "这篇内容我觉得你会喜欢", type: "懂她" },
  ],
  first: [
    { text: "你好，打扰了。我是看到你……觉得你很特别，所以想认识你", type: "直接真诚" },
    { text: " Hi，我注意到你……想和你聊几句，没打扰吧？", type: "礼貌开场" },
  ]
};

const continue_ = {
  curious: [
    "你平时空闲的时候喜欢做什么？",
    "你最喜欢的电影是哪部呀？",
    "听起来很有趣，你是怎么开始接触这个的？",
    "你这人说话很有意思，跟你聊天感觉很轻松",
  ],
  lightFlirt: [
    "跟你聊天有点上头",
    "我发现我打字变快了",
    "你这样说，我都不知道怎么接了",
    "你让我有点词穷",
  ]
};

const response = {
  sheReplied: [
    { text: "看到你消息的时候，正在做的事情突然就不香了", type: "表达在意" },
    { text: "你回的比我预期的早，我很高兴", type: "坦诚" },
    { text: "这个表情，我存下来了", type: "俏皮记录" },
  ],
  sheJokes: [
    { text: "你是故意的吧？", type: "轻推" },
    { text: "说不过你，但你笑的样子很好看", type: "夸她+认输" },
    { text: "这波我认输", type: "大方认输" },
  ],
  sheTeases: [
    { text: "被你发现了", type: "坦诚承认" },
    { text: "那你要不要教教我？", type: "顺水推舟" },
    { text: "行行行，你赢了，开心了吧", type: "宠溺让步" },
  ]
};

const night = [
  { text: "晚安，做个好梦，希望梦里也有我", type: "暧昧收尾" },
  { text: "今晚聊得很开心，早点休息哦", type: "温暖关心" },
  { text: "快睡吧，别熬夜，明天有事我叫你", type: "照顾感" },
  { text: "晚安～记得喝水", type: "细节关心" },
];

const escalate = [
  { text: "跟你聊天真的很舒服，想多了解你一点", type: "坦诚表达意愿" },
  { text: "你有没有想过，我们见面会聊什么？", type: "试探见面" },
  { text: "你这人挺有意思的，什么时候有空出来坐坐？", type: "邀约试探" },
  { text: "说实话，我想认识你真人", type: "直接但真诚" },
];

function pick(lines) {
  return lines[Math.floor(Math.random() * lines.length)];
}

// 安全白名单：只允许访问预定义的数据对象
const ALLOWED_CATEGORIES = {
  opening,
  continue_,
  response,
  night,
  escalate
};

// 白名单子属性
const ALLOWED_SUBS = {
  opening: ['dating', 'wechat', 'first'],
  continue_: ['curious', 'lightFlirt'],
  response: ['sheReplied', 'sheJokes', 'sheTeases'],
};

function safeGet(obj, key) {
  if (typeof key !== 'string') return null;
  // 只允许字母数字下划线，防止注入
  if (!/^\w+$/.test(key)) return null;
  return obj[key] || null;
}

function show(category, sub) {
  const cat = ALLOWED_CATEGORIES[category];
  if (!cat) return '未知分类: ' + category;
  let items;
  if (sub) {
    const allowedSubs = ALLOWED_SUBS[category] || [];
    if (!allowedSubs.includes(sub)) return '未知子分类: ' + sub;
    const subData = safeGet(cat, sub);
    if (!subData) return '未找到: ' + sub;
    items = subData;
  } else {
    items = Array.isArray(cat) ? cat : Object.values(cat).flat();
  }
  return items.map((item, i) => `${i + 1}. [${item.type}] ${item.text}`).join('\n');
}

const args = process.argv.slice(2);
const cmd = args[0];

if (cmd === '开场') {
  const sub = args[1] || 'dating';
  console.log('\n🎯 开场白（' + sub + '场景）:\n');
  console.log(show('opening', sub));
} else if (cmd === '延续') {
  const sub = args[1] || 'curious';
  console.log('\n💬 延续话题（' + sub + '）:\n');
  console.log(show('continue_', sub));
} else if (cmd === '回复') {
  const sub = args[1] || 'sheReplied';
  console.log('\n💡 她的回复后，这样回（' + sub + '）:\n');
  console.log(show('response', sub));
} else if (cmd === '晚安') {
  console.log('\n🌙 晚安话术:\n');
  console.log(show('night'));
} else if (cmd === '进阶') {
  console.log('\n🚀 关系进阶话术:\n');
  console.log(show('escalate'));
} else if (cmd === '随机') {
  const all = [...opening.dating, ...response.sheReplied, ...night, ...escalate];
  const item = pick(all);
  console.log('\n✨ 随机推荐:\n[' + item.type + '] ' + item.text + '\n');
} else {
  console.log(`
🌿 暖男话术库 - 使用指南

使用方法: node chats.js <分类>

分类命令:
  开场 [dating|wechat|first]  - 不同场景的开场白
  延续 [curious|lightFlirt]   - 延续对话的话题/调情
  回复 [sheReplied|sheJokes|sheTeases] - 她的回复后怎么接
  晚安                        - 结束对话的温暖收尾
  进阶                        - 关系升温的表达
  随机                        - 随机推荐一句

示例:
  node chats.js 开场 dating
  node chats.js 延续 lightFlirt
  node chats.js 回复 sheReplied
  node chats.js 晚安
  node chats.js 进阶
  `);
}
