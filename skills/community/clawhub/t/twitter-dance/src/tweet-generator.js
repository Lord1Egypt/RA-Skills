/**
 * Twitter Dance 推文生成器
 * 
 * 支持：
 * - Kimi API 生成高质量推文
 * - 本地模板快速生成
 * - 话题轮换
 */

const https = require('https');

class TweetGenerator {
  constructor(options = {}) {
    this.kimiApiKey = options.kimiApiKey || process.env.KIMI_API_KEY;
    this.verbose = options.verbose || false;

    this.topics = [
      {
        name: 'Crypto & Web3',
        keywords: ['Bitcoin', 'Ethereum', 'DeFi', 'NFT', 'Web3'],
        tone: '金融科技爱好者'
      },
      {
        name: 'AI & Technology',
        keywords: ['AI', 'LLM', 'ML', 'Open Source', 'Coding'],
        tone: '技术极客'
      },
      {
        name: 'Gaming & Metaverse',
        keywords: ['GameFi', 'P2E', 'Metaverse', 'Gaming', 'Play'],
        tone: '游戏玩家'
      },
      {
        name: 'Business & Startups',
        keywords: ['Startup', 'Business', 'Startup', 'Founder', 'Growth'],
        tone: '创业者'
      },
      {
        name: 'Life & Productivity',
        keywords: ['Life Hack', 'Productivity', 'Mindset', 'Growth', 'Success'],
        tone: '生活智慧'
      }
    ];
  }

  /**
   * 获取当日话题
   */
  getCurrentTopic() {
    const day = new Date().getDate();
    const topicIndex = (day - 1) % this.topics.length;
    return this.topics[topicIndex];
  }

  /**
   * 使用 Kimi API 生成推文
   */
  async generateWithKimi(topic) {
    if (!this.kimiApiKey) {
      return null;
    }

    console.log('[🤖] 使用 Kimi 生成推文...');

    const prompt = `生成一条 Twitter 推文（280 字以内）：
主题：${topic.name}
关键词：${topic.keywords.join(', ')}
语气：${topic.tone}

要求：
- 包含 2-3 个 emoji
- 吸引互动和转发
- 包含至少 1 个话题标签 (#)
- 专业但亲切

直接返回推文内容，无需额外说明。`;

    return new Promise((resolve) => {
      const payload = JSON.stringify({
        model: 'moonshot-v1-8k',
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 300
      });

      const options = {
        hostname: 'api.moonshot.cn',
        path: '/v1/chat/completions',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'Authorization': `Bearer ${this.kimiApiKey}`
        },
        timeout: 10000
      };

      const req = https.request(options, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            const text = parsed.choices?.[0]?.message?.content;

            if (!text) {
              resolve(null);
              return;
            }

            if (text.length > 280) {
              resolve(text.substring(0, 277) + '...');
            } else {
              console.log('[✅] Kimi 生成完成');
              resolve(text);
            }
          } catch {
            resolve(null);
          }
        });
      });

      req.on('timeout', () => {
        req.abort();
        console.log('[⏱️] Kimi 超时，使用本地模板');
        resolve(null);
      });

      req.on('error', () => {
        console.log('[⚠️] Kimi 连接失败，使用本地模板');
        resolve(null);
      });

      req.write(payload);
      req.end();
    });
  }

  /**
   * 本地模板生成
   */
  generateWithTemplate(topic) {
    const templates = [
      `🚀 ${topic.keywords[0]} 生态正在发展。

最近深入研究了几个热点项目，发现关键在于：
✨ ${topic.keywords[1]}
✨ 创新的商业模式
✨ 强大的社区支持

这就是为什么 #${topic.keywords[0]} 未来可期 🌟`,

      `💡 快速观点：

${topic.keywords[0]} 不仅仅是技术，更是对未来的想象。

在研究 ${topic.keywords[1]} 时发现：
• ${topic.keywords[2]} 的重要性
• 社区驱动的力量
• 开放生态的价值

你认为呢？#${topic.keywords[0]}`,

      `📊 数据说话：

${topic.keywords[0]} 领域的增长数据令人鼓舞。

关键驱动力：
🔸 ${topic.keywords[1]} 的突破
🔸 用户采用率上升
🔸 生态完善度提高

未来 3-6 个月非常值得关注 #${topic.keywords[0]}`,

      `🎯 深度思考：

为什么 ${topic.keywords[0]} 会改变游戏规则？

1️⃣ ${topic.keywords[1]} 的革新
2️⃣ 去中心化的力量
3️⃣ 用户真正需要的东西

现在是参与的好时候 #${topic.keywords[0]}`,

      `🌍 全局视角：

${topic.keywords[0]} 的发展阶段：
📈 从实验到应用
📈 从小众到主流
📈 从理想到现实

正在目睹历史 #${topic.keywords[0]} #${topic.keywords[1]}`
    ];

    const day = new Date().getDate();
    const templateIndex = (day - 1) % templates.length;
    return templates[templateIndex];
  }

  /**
   * 生成推文（Kimi 优先，回退本地）
   */
  async generate(options = {}) {
    const topic = options.topic || this.getCurrentTopic();

    console.log(`\n📝 生成推文（话题：${topic.name}）`);
    console.log(`关键词：${topic.keywords.join(', ')}`);

    let text = null;

    // 优先尝试 Kimi
    if (this.kimiApiKey) {
      text = await this.generateWithKimi(topic);
    }

    // 回退到本地模板
    if (!text) {
      console.log('[📝] 使用本地模板生成');
      text = this.generateWithTemplate(topic);
    }

    return {
      text,
      source: text ? (this.kimiApiKey ? 'kimi' : 'template') : 'template',
      topic: topic.name,
      length: text.length,
      keywords: topic.keywords
    };
  }

  /**
   * 批量生成
   */
  async generateBatch(count = 5, options = {}) {
    console.log(`\n📋 批量生成 ${count} 条推文`);

    const tweets = [];
    for (let i = 0; i < count; i++) {
      const tweet = await this.generate(options);
      tweets.push(tweet);
      console.log(`✅ 推文 ${i + 1}/${count} 完成（${tweet.length} 字）`);

      if (i < count - 1) {
        await new Promise(r => setTimeout(r, 500));
      }
    }

    return tweets;
  }
}

module.exports = TweetGenerator;
