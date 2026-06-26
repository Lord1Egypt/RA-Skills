# 自媒体文案生成器

> 一键生成多平台爆款文案 - 小红书/抖音/公众号/知乎

**版本**: v0.1.0 (Sprint 1 MVP)  
**状态**: 🚧 开发中

---

## ✨ 功能特点

- 🎯 **4 平台支持** - 小红书、抖音、公众号、知乎
- 📝 **智能生成** - 根据主题自动生成文案 + 标题
- 🏷️ **标签推荐** - 热门/精准/长尾标签智能组合
- 🎨 **语气调节** - 自然/专业/幽默/温暖
- 📏 **长度控制** - short/medium/long

---

## 🚀 快速开始

### 安装

```bash
# 克隆或下载本技能
cd 自媒体文案生成器

# 无需额外依赖（Python 3.7+ 标准库）
```

### 基础用法

```bash
# 生成小红书文案
python generate.py "AI 写作技巧" -p xiaohongshu

# 生成公众号文章
python generate.py "职场沟通技巧" -p wechat -l long

# 生成抖音脚本
python generate.py "美妆教程" -p douyin -t 幽默

# 生成知乎回答
python generate.py "如何提升学习效率" -p zhihu
```

### 参数说明

```bash
python generate.py "主题" \
  -p [平台] \          # xiaohongshu/douyin/wechat/zhihu
  -t [语气] \          # 自然/专业/幽默/温暖
  -l [长度] \          # short/medium/long
  -k [关键词...] \     # 关键词列表
  -a [受众] \          # 目标受众
  -o [输出文件]        # 保存到文件
```

### 示例

```bash
# 完整示例
python generate.py "AI 工具提升工作效率" \
  -p xiaohongshu \
  -t 自然 \
  -l medium \
  -k AI 效率 工具 打工人 \
  -a "25-35 岁职场人" \
  -o "output/xiaohongshu-ai.md"

# 只生成标题选项
python generate.py "副业赚钱" --titles-only

# 不生成标签
python generate.py "旅行攻略" --no-tags
```

---

## 📋 输出示例

### 小红书文案

```markdown
# 🔥 5 个 AI 写作技巧，第 3 个绝了！

姐妹们！

今天想和大家聊聊 AI 写作这个话题～

## 为什么重要
很多人都不知道，用对 AI 工具真的能提升效率...

## 具体做法
1. 第一步...
2. 第二步...
3. 第三步...

## 注意事项
⚠️ 记得不要过度依赖 AI

希望这篇笔记对你们有帮助！
觉得有用记得点赞收藏哦～💕

#AI #写作技巧 #效率工具 #职场干货 #自我提升
```

### 标题选项

```bash
$ python generate.py "副业赚钱" --titles-only

📝 标题选项：

1. 💰 7 个副业赚钱技巧，第 3 个绝了！
2. 后悔没早知道！副业赚钱的 5 个真相
3. 副业赚钱怎么做？看这篇就够了
4. 亲测有效！副业赚钱的 7 种方法
5. 别再盲目尝试了！副业赚钱正确打开方式
...
```

---

## 🏗️ 架构设计

```
自媒体文案生成器/
├── generate.py           # 主入口
├── src/
│   ├── generator.py      # 核心生成器
│   └── tag_recommender.py # 标签推荐器
├── tests/                # 测试
├── examples/             # 示例
└── README.md             # 本文档
```

### 核心模块

| 模块 | 功能 | 状态 |
|:---|:---|:---|
| **generator.py** | 文案生成核心 | ✅ Sprint 1 |
| **tag_recommender.py** | 标签推荐 | ✅ Sprint 1 |
| **title_optimizer.py** | 标题优化 | 🚧 Sprint 2 |
| **batch_generator.py** | 批量生成 | 🚧 Sprint 2 |
| **hot_tracker.py** | 热点追踪 | 🚧 Sprint 3 |

---

## 📅 开发计划

### Sprint 1 (当前) - 核心功能 MVP
- ✅ 4 平台文案生成
- ✅ 标签推荐
- 🚧 标题优化
- 🚧 单元测试
- 🚧 文档完善

### Sprint 2 - 增强功能
- [ ] 批量生成
- [ ] Few-shot 示例库
- [ ] 历史记录
- [ ] 集成测试

### Sprint 3 - 高级功能
- [ ] 热点追踪
- [ ] 数据反馈
- [ ] 品牌词库
- [ ] 性能优化

---

## 🔧 开发

### 运行测试

```bash
# 运行单元测试
python -m pytest tests/

# 测试生成器
python -c "from src.generator import CopywriterGenerator; print('OK')"

# 测试标签推荐
python src/tag_recommender.py
```

### 添加新平台

1. 在 `PLATFORM_TEMPLATES` 添加新平台模板
2. 在 `Platform` 枚举添加新平台
3. 在 `TagRecommender` 添加热门标签

---

## 📊 性能指标

| 指标 | 目标 | 当前 |
|:---|:---|:---|
| 单次生成时间 | <5s | ~3s |
| 标题满意度 | >80% | 待测试 |
| 标签采纳率 | >60% | 待测试 |

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

### 待办事项

- [ ] 添加更多 Prompt 模板
- [ ] 收集高质量 few-shot 示例
- [ ] 接入真实 LLM API
- [ ] 添加 Web UI

---

## 📝 更新日志

### v0.1.0 (2026-03-03)
- 🎉 初始版本
- ✅ 4 平台基础生成
- ✅ 标签推荐
- 🚧 Sprint 1 开发中

---

## 📄 License

MIT License

---

**作者**: 小爱  
**联系方式**: 1416289917@qq.com
