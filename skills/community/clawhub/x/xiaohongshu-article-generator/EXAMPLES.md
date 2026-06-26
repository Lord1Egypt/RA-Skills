# 小红书图文生成技能 - 使用示例

## 🚀 快速开始

### 示例 1：生成美团年终奖图文（吃瓜爆料型）

```bash
cd C:\Users\Administrator\.openclaw\skills\xiaohongshu-article-generator

node index.js \
  --topic "美团年终奖" \
  --template "gossip" \
  --output-dir "C:\Users\Administrator\.openclaw\workspace\xiaohongshu-output"
```

**输出**：
```
C:\Users\Administrator\.openclaw\workspace\xiaohongshu-output\美团年终奖\
├── 美团年终奖.html
├── copywriting.md
└── images/
    ├── page-01.png (封面)
    ├── page-1.png (评论区)
    ├── page-2.png (系数科普)
    └── page-3.png (互动)
```

---

### 示例 2：生成阿里 Qwen 人事图文（吃瓜爆料型）

```bash
node index.js \
  --topic "阿里 Qwen 人事震荡" \
  --template "gossip" \
  --pages 4
```

**文案预览**：
```markdown
# 阿里 Qwen 人事震荡❗️网友破防了😭

家人们谁懂啊！！阿里 Qwen 人事震荡终于来了🎉
来看看大家都怎么说👇

---

🔥 热搜第一：阿里 Qwen 人事震荡

💬 评论区炸锅了：
- 「这也太真实了」
- 「破防了家人们」
- 「你怎么看？」

---

❓ 互动话题：
你对这件事怎么看？
评论区聊聊👇

#阿里 Qwen 人事震荡 #热点 #吃瓜 #网友热议 #话题讨论
```

---

### 示例 3：生成职场干货图文（知识科普型）

```bash
node index.js \
  --topic "年终奖谈判技巧" \
  --template "knowledge" \
  --pages 4
```

**特点**：
- 绿色系配色（#00C072）
- 知识点 + 图表说明
- 专业性强、收藏价值高

---

### 示例 4：生成产品种草图文（种草推荐型）

```bash
node index.js \
  --topic "机械键盘推荐" \
  --template "recommendation" \
  --output-dir "C:\Users\Administrator\.openclaw\workspace\xiaohongshu-output\product-reviews"
```

**特点**：
- 粉色系配色（#FF69B4）
- 使用体验 + 对比测评
- 转化导向、购买建议

---

## 📋 完整工作流

### Step 1: 获取热点数据

```javascript
// 调用 hot-trends-summary 技能获取热点
import { generateXiaohongshuArticle } from './index.js';

const hotTopics = [
  '美团年终奖',
  '阿里 Qwen 人事',
  '得物双瓜',
  '西贝换帅'
];
```

### Step 2: 批量生成图文

```javascript
for (const topic of hotTopics) {
  await generateXiaohongshuArticle({
    topic,
    template: 'gossip',
    pages: 4
  });
}
```

### Step 3: 发布到小红书

```bash
# 输出目录中的图片可直接用于发布
C:\Users\Administrator\.openclaw\workspace\xiaohongshu-output\{topic}\images\
```

---

## 🎨 自定义模板

### 添加新模板

在 `templates/` 目录下创建新模板文件：

```javascript
// templates/custom.js
export async function generateCustomCopywriting({ topic, hotData }) {
  const title = `${topic}🌟自定义标题`;
  
  const content = `# ${title}

## 正文

自定义内容...

#${topic.replace(/\s/g, '')} #自定义 #标签
`;

  return { title, content, template: 'custom' };
}
```

然后在 `index.js` 中注册：

```javascript
const templates = {
  gossip: generateGossipCopywriting,
  knowledge: generateKnowledgeCopywriting,
  recommendation: generateRecommendationCopywriting,
  custom: generateCustomCopywriting  // 新增
};
```

---

## 📊 效果优化

### 标题优化

```javascript
// 好标题示例
"美团年终奖❗️L7 系数 0.7 破防了😭"
"阿里 Qwen 人事震荡🔥内部员工爆料"
"得物双瓜连续剧🍉前小红书负责人空降"

// 标题公式
情绪词 + 核心话题 + 数字/对比 + emoji
```

### 互动优化

```javascript
// 好的互动引导
"满意扣 1，不满意扣 2"
"你遇到过吗？评论区聊聊"
"A/B 选择，你站哪边？"
```

### 发布时间优化

| 时间段 | 适合内容 | 预期流量 |
|--------|----------|----------|
| 12:00-13:00 | 轻松八卦 | ⭐⭐⭐⭐ |
| 16:00-18:00 | 职场干货 | ⭐⭐⭐⭐⭐ |
| 20:00-22:00 | 吃瓜爆料 | ⭐⭐⭐⭐⭐ |
| 22:00-24:00 | 情感共鸣 | ⭐⭐⭐ |

---

## 🔗 相关技能组合

### 组合 1：热点追踪 + 图文生成

```javascript
// 1. 获取热点
const hotData = await hotTrendsSummary();

// 2. 生成图文
for (const topic of hotData.topics) {
  await generateXiaohongshuArticle({
    topic: topic.title,
    hotData: topic.details,
    template: 'gossip'
  });
}
```

### 组合 2：脉脉爆料 + 图文生成

```javascript
// 1. 获取脉脉爆料
const maimaiData = await maimaiFetch({
  type: 'hot-rank'
});

// 2. 生成图文
await generateXiaohongshuArticle({
  topic: maimaiData.topTopic,
  hotData: maimaiData.comments,
  template: 'gossip'
});
```

---

## 📝 注意事项

### 内容合规
- ✅ 使用原创文案
- ✅ 网友评论匿名处理
- ✅ 标注"仅供参考"
- ❌ 避免敏感话题
- ❌ 不传播未经证实消息

### 图片质量
- ✅ 确保文字清晰
- ✅ 检查颜色对比度
- ✅ 375x667px 标准尺寸
- ❌ 避免截图模糊

### 发布节奏
- ✅ 每日≤3 篇
- ✅ 错开时间段
- ✅ 内容多样化
- ❌ 避免刷屏

---

## 📚 更新日志

### v1.0.0 (2026-03-07)
- ✅ 初始版本发布
- ✅ 支持 3 种模板类型
- ✅ 自动生成文案 + HTML + 图片
- ✅ 集成 html-pages-to-images 技能

---

**最后更新**：2026-03-07 09:40  
**作者**：OpenClaw  
**许可**：MIT
