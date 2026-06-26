# semantic-compress - OpenClaw 语义压缩技能

在**不降低准确度**的前提下，大幅减少 LLM token 消耗。保留完整关键信息和语义骨架，只去除冗余废话。

## 🎯 解决什么问题

- 长对话上下文 token 消耗太快，很快占满上下文窗口
- 想节省 token 成本，但又不想丢失信息降低准确度
- 传统摘要会丢失细节，关键词提取会破坏逻辑

## ✨ 核心优势

| 方法 | Token 减少 | 准确度保留 | 推荐 |
|------|-----------|------------|------|
| 全文保留 | 0% | ✅ 100% | 浪费 token |
| 摘要总结 | 70%-90% | ❌ 丢失细节 | 不适合需要准确度的场景 |
| 关键词提取 | 80% | ❌ 丢失逻辑关联 | 不推荐 |
| **语义压缩** | **50%-70%** | ✅ 完整保留关键信息 | ✅ **推荐** |

## 📋 压缩原则

1. ✅ **必须保留**：所有核心论点、结论、决策、数据、关键事实、逻辑关系
2. ❌ **必须删除**：客套话、重复说明、过程性废话、修饰性铺垫，只删不增
3. 📐 **分层策略**：最近 3-5 轮对话完整保留保证连贯，更早对话只保留结论
4. ⚠️ **禁忌**：不准做摘要、不准丢失信息、不准添加新内容

## 🚀 使用方式

### 命令行调用

```bash
node scripts/compress.js 输入文件.txt [输出文件.txt]
```

### 在对话中使用

只需要说：`请用 semantic-compress 压缩上文，保留全部关键信息`

### Node.js API

```javascript
const { semanticCompress } = require('./index.js');
const result = semanticCompress(yourLongText, {
  targetCompression: 0.5,
  preserveAccuracy: true
});
// result.prompt 就是可以直接发给 LLM 的压缩 prompt
```

## 📊 效果示例

| 原文长度 (字符) | 估算原 token | 压缩后 token | 压缩率 |
|-----------------|--------------|--------------|--------|
| 8000 | 2000 | ~600 | 30% |
| 4000 | 1000 | ~300 | 30% |
| 2000 | 500 | ~200 | 40% |

## 🔧 安装

```bash
# 在 OpenClaw 技能目录
clawhub install semantic-compress
# 或者
git clone <repo-url> semantic-compress
npm install # 无额外依赖，直接使用
```

## 📝 适用场景

- ✅ 长对话历史上下文压缩
- ✅ 多轮对话后清理上下文节省 token
- ✅ 保存历史对话到长期记忆
- ✅ 长文章/文档精简但保留全部要点

## ❌ 不适用场景

- 原文已经很精简 (<500 token)
- 需要保留原始完整文本
- 诗歌、文学作品等需要保留修辞

## 📄 License

MIT License
