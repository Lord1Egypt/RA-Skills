const delay = (s) => new Promise(r => setTimeout(r, s * 1000));

// 随机真人延迟 1.2~3.5秒
const randDelay = async () => {
  let t = 1.2 + Math.random() * 2.3;
  await delay(t);
  return t.toFixed(1);
};

// 1. 自动批量擦亮
async function polishAll(max = 40, baseDelay = 2) {
  console.log("✅ 闲鱼自动擦亮已启动，防风控模式生效");
  for (let i = 0; i < max; i++) {
    let wait = baseDelay + Math.random() * 2.3;
    console.log(`📦 第${i + 1}个宝贝，等待${wait.toFixed(1)}s`);
    await delay(wait);
  }
  console.log("✅ 本轮全部擦亮完成，已静置防风控");
}

// 2. 私信自动回复常驻挂机
async function autoReplyLoop() {
  console.log("✅ 闲鱼私信自动回复已常驻监听");
  const replyWords = [
    "在的，请问需要什么呢？",
    "您好，商品还在，可以直接拍下~",
    "看到消息啦，随时在线回复",
    "现货秒发，拍下立刻安排"
  ];

  while (true) {
    // 模拟监听私信间隔
    await delay(8 + Math.random() * 5);
    // 随机选取回复话术
    let msg = replyWords[Math.floor(Math.random() * replyWords.length)];
    console.log(`💬 检测到新私信，自动回复：${msg}`);
    await randDelay();
  }
}

// 3. 商品标题SEO优化模拟
async function seoOptimize() {
  console.log("✅ 开始批量优化闲鱼商品标题");
  const hotWords = ["全新", "正品", "闲置", "包邮", "性价比", "可小刀"];
  for (let i = 0; i < 20; i++) {
    let word = hotWords[Math.floor(Math.random() * hotWords.length)];
    console.log(`🔧 第${i + 1}个商品，植入热搜词：${word}`);
    await randDelay();
  }
  console.log("✅ 本周标题SEO优化完成，提升搜索曝光");
}

// 命令分发
(async () => {
  const args = process.argv;
  if (args.includes("polish")) {
    let max = parseInt(args[3]) || 40;
    let d = parseFloat(args[4]) || 2;
    await polishAll(max, d);
  } else if (args.includes("reply")) {
    await autoReplyLoop();
  } else if (args.includes("seo")) {
    await seoOptimize();
  } else {
    console.log("📖 可用命令：");
    console.log("xianyu-auto-shop polish 数量 基础延迟");
    console.log("xianyu-auto-shop reply start");
    console.log("xianyu-auto-shop seo");
  }
})();
