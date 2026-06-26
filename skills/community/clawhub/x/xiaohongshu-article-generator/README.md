# 小红书图文生成技能

基于热点话题自动生成小红书风格的图文内容（文案 + HTML + 图片）

## 🚀 快速开始

### 方法 1：命令行调用

```bash
# 进入技能目录
cd C:\Users\Administrator\.openclaw\skills\xiaohongshu-article-generator

# 使用默认配置生成
node index.js --topic "美团年终奖"

# 完全自定义
node index.js \
  --topic "美团年终奖" \
  --template "gossip" \
  --output-dir "./xiaohongshu-output" \
  --pages 4
```

### 方法 2：代码调用

```javascript
import { generateXiaohongshuArticle } from './index.js';

const result = await generateXiaohongshuArticle({
  topic: '美团年终奖',
  template: 'gossip',  // gossip/knowledge/recommendation
  outputDir: './xiaohongshu-output',
  pages: 4
});

console.log(result);
```

## 📋 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `topic` | string | 必填 | 话题名称（用于命名输出文件） |
| `template` | string | `gossip` | 模板类型（gossip/knowledge/recommendation） |
| `outputDir` | string | `./xiaohongshu-output` | 输出目录 |
| `pages` | number | `3` | 内页数量（2-4） |

## 📁 输出结构

```
{xiaohongshu-output}/{topic}/
├── {topic}.html          # HTML 源文件
├── copywriting.md        # 文案（标题 + 正文 + 标签）
└── images/
    ├── page-01.png       # 封面图
    ├── page-1.png        # 内页 1
    ├── page-2.png        # 内页 2
    └── page-3.png        # 内页 3
```

## 🎨 模板类型

### 1. 吃瓜爆料型（gossip）
**适用**：大厂八卦、热点事件、娱乐新闻
**特点**：
- 橙色系配色（#FF6B35 + #FFD700）
- 网友评论为主
- 情绪强烈、互动性高

### 2. 干货科普型（knowledge）
**适用**：职场技巧、行业知识、教程指南
**特点**：
- 绿色系配色（#00C072 + #00E68A）
- 知识点 + 图表说明
- 专业性强、收藏价值高

### 3. 种草推荐型（recommendation）
**适用**：产品推荐、好物分享、使用体验
**特点**：
- 粉色系配色（#FF69B4 + #FFB6C1）
- 使用体验 + 对比测评
- 转化导向、购买建议

## 🔧 依赖技能

本技能依赖以下技能：

1. **html-pages-to-images**
   - 用途：将 HTML 页面转换为图片
   - 路径：`../html-pages-to-images`
   - 必需：✅

## 📝 使用示例

### 示例 1：生成大厂八卦图文

```javascript
const result = await generateXiaohongshuArticle({
  topic: '阿里 Qwen 人事震荡',
  template: 'gossip',
  outputDir: './xiaohongshu-output'
});

// 输出：
// xiaohongshu-output/ali-qwen-drama/
//   ├── ali-qwen-drama.html
//   ├── copywriting.md
//   └── images/
//       ├── page-01.png
//       ├── page-1.png
//       └── page-2.png
```

### 示例 2：生成职场干货图文

```javascript
const result = await generateXiaohongshuArticle({
  topic: '年终奖谈判技巧',
  template: 'knowledge',
  pages: 4
});
```

### 示例 3：生成产品种草图文

```javascript
const result = await generateXiaohongshuArticle({
  topic: '机械键盘推荐',
  template: 'recommendation',
  outputDir: './product-reviews'
});
```

## 🎯 发布建议

### 最佳发布时间
- **工作日**：中午 12:00-13:00，晚上 20:00-22:00
- **周五**：下午 16:00-18:00（摸鱼高峰）
- **周末**：上午 10:00-12:00，晚上 21:00-23:00

### 互动引导
- 评论区置顶：「满意扣 1，不满意扣 2」
- 回复前 10 条评论，提升互动率
- 使用投票式问题（A/B 选择）

### 标签策略
- 1-2 个大标签（#职场 #互联网）
- 2-3 个中标签（#年终奖 #大厂）
- 2-3 个小标签（#美团 #绩效）

## 📊 效果评估

| 指标 | 及格 | 良好 | 优秀 |
|------|------|------|------|
| 点赞数 | 500+ | 2000+ | 10000+ |
| 收藏数 | 200+ | 800+ | 5000+ |
| 评论数 | 100+ | 300+ | 2000+ |

## ⚠️ 注意事项

1. **内容合规**
   - 避免敏感话题
   - 不传播未经证实的消息
   - 标注"仅供参考"等免责声明

2. **版权问题**
   - 使用原创文案
   - 网友评论需匿名处理
   - 品牌名称合理使用

3. **图片质量**
   - 确保文字清晰可读
   - 检查颜色对比度
   - 避免截图模糊

## 🔗 相关技能

- `hot-trends-summary` - 热榜汇总技能（获取热点数据）
- `maimai-fetch` - 脉脉信息拉取（获取网友评论）
- `html-pages-to-images` - HTML 转图片（图片生成）
- `wechat-article-typeset` - 公众号排版（排版参考）

## 📚 更新日志

### v1.0.0 (2026-03-07)
- ✅ 初始版本发布
- ✅ 支持 3 种模板类型
- ✅ 自动生成文案 + HTML + 图片
- ✅ 集成 html-pages-to-images 技能

---

**作者**：OpenClaw  
**许可**：MIT  
**文档**：https://docs.openclaw.ai
