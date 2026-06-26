# 知乎技术博客生成器

AI 驱动的知乎风格技术博客自动生成工具。

## 功能特点

- **双模式话题选择**：支持指定主题或获取热门技术话题
- **多源信息收集**：GitHub、知乎、ArXiv、Hacker News 等
- **论文深度解析**：自动提取论文核心内容和原图
- **知乎风格写作**：标题吸引人、内容有深度、观点鲜明
- **反思优化机制**：去AI味、补深度、加观点
- **模块化设计**：每个步骤独立，便于管理和调试

## 使用方法

### 完整流程（一键生成）

```bash
# 指定主题模式
node scripts/run_all.js --topic "Claude 4" --mode "specific"

# 热门话题模式（会让你选择）
node scripts/run_all.js --mode "hot"
```

### 分步执行

```bash
# Step 1: 话题选择
node scripts/01_topic_selector.js --mode "hot"     # 热门话题
node scripts/01_topic_selector.js --topic "主题"    # 指定主题

# Step 2: 信息收集
node scripts/02_info_collector.js

# Step 3: 生成初稿
node scripts/03_blog_generator.js

# Step 4: 反思优化
node scripts/04_refine_blog.js

# Step 5: 输出文档
node scripts/05_output_md.js
```

## 输出示例

生成的技术博客示例：

```markdown
# Claude 4 深度解析：Agent 编程的「临界点」真的来了吗？

> 导语：当 AI 不仅能写代码，还能自己调试、自己查文档、自己提交 PR，这意味着什么？

## 一、背景：为什么我们需要能自主编程的 AI？
...

## 二、Claude 4 的核心突破：不只是更强的模型
...

## 三、源码级解读：Agent Loop 是如何实现的？
...

## 四、实战测试：我们让它重构了一个真实项目
...

## 五、我的判断：这会改变什么？
...
```

## 输出位置

所有生成的博客保存在：
```
D:\techinsight\reports\blog_{session_id}\05_output\
```

## 技术博客特点

| 特点 | 说明 |
|------|------|
| **标题新颖** | 使用数字、对比、悬念，吸引人点击 |
| **逻辑清晰** | 2-3级标题，层层递进 |
| **内容深度** | 源码分析、架构图、数据支撑 |
| **观点鲜明** | 不只是搬运，有个人判断 |
| **语言生动** | 去AI味，像技术博主在聊天 |
| **图文并茂** | 论文原图、架构图、代码片段 |
| **长度适中** | 1000-5000字，详略得当 |

## 配置说明

编辑 `lib/config.js` 可自定义：
- 输出路径
- 搜索渠道优先级
- 文章风格参数
- 质量检查规则

## 依赖

- Node.js >= 16
- Playwright（用于网页抓取）
- pdf-parse（用于论文解析）

## License

MIT
