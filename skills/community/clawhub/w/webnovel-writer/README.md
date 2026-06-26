<div align="center">

# 📖 Novel Writer

**Enterprise-grade Long-form Web Novel Engine for AI Agents**

[![Tests](https://img.shields.io/badge/tests-284%20passed-success)]()
[![Scripts](https://img.shields.io/badge/scripts-18-orange)]()
[![References](https://img.shields.io/badge/references-20-blue)]()
[![Version](https://img.shields.io/badge/version-3.1.0-blue)]()

*Consistency-first novel writing with automated quality checks, character state machines, and plot tracking.*

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 为什么需要 Novel Writer？

写长篇小说（50万字+）最大的敌人是**前后矛盾**。AI 写作尤其容易犯：
- 角色名字写错
- 时间线对不上
- 角色突然知道不该知道的事
- 前面埋的伏笔忘了回收

Novel Writer 用**结构化追踪 + 自动化检测**解决这些问题。

### 核心能力

```
写作层：上下文包构建 → 正文写作 → 6步自检 → 状态更新
检测层：一致性 / 大纲偏差 / 节奏 / 对话质量 / 张力 / 伏笔 / 钩子 / 标题 / 开头 / 段落 / 重复（11维度）
追踪层：角色状态机 / 伏笔追踪 / 时间线 / 事件记录
参考层：20篇写作指南（大纲设计/钩子技巧/节奏模板/去AI味/弹幕管理...）
```

### 12个检测脚本

| 脚本 | CLI 别名 | 检测内容 |
|------|----------|----------|
| consistency_check | `check` | 角色称呼、设定冲突、时间线、AI高频词、跨章重复、角色消失 |
| outline_drift | `drift` | 标题匹配、关键词覆盖、角色出场偏差 |
| rhythm_check | `rhythm` | 紧张度、钩子密度、情感基调、节奏异常 |
| dialogue_tag_check | `dialogue` | 标签频率、单调性、副词过度、对话占比 |
| tension_forecast | `tension` | 张力分布预测、走势分析 |
| foreshadow_scan | `foreshadow` | 伏笔模式识别、未回收预警 |
| chapter_hook_check | `hook` | 钩子类型、强度评分、连续弱结尾 |
| chapter_title_check | `title` | 标题长度、平淡检测、标题党、信息过量 |
| opening_score | `opening` | 开头类型、吸引力评分、钩子检测 |
| paragraph_check | `paragraph` | 过长段落、墙文字、视觉节奏 |
| repetition_check | `repeat` | 跨章重复、连续句式 |
| run_all_checks | `all` | 一键全检 |
| config_manager | `config` | 小说注册/切换/配置管理 |
| changelog | `changelog` | 版本管理 |
| backup | `backup` | 结构化数据备份 |
| run_parallel | `parallel` | 并行检测+缓存+增量 |
| semantic_check | `semantic` | jieba语义重复+实体识别 |

### 深度审读（人工编辑级）

不只是跑脚本，而是像人类编辑一样逐字精读：
- 每批读 3-5 章，写精读笔记（证明理解了剧情）
- 每段带着 6 个问题分析（合理性/读者感受/衔接/AI味...）
- 跨章关联分析（角色弧线/情感曲线/伏笔回收）
- 输出精读报告 + 修改清单（P0/P1/P2 分级）

详细流程见 SKILL.md「三、深度审读」。

### 使用示例

```bash
# 一致性检查
python3 scripts/cli.py check 正文/ --tracking 追踪表.md --dict 设定词典.md

# 大纲偏差
python3 scripts/cli.py drift --outline 大纲.md --chapters 正文/

# 全部检测
python3 scripts/cli.py all 正文/

# 带建议输出
python3 scripts/cli.py hook --novel-dir 正文/ --suggest

# 注册小说并备份
python3 scripts/cli.py config register 我的小说 /path/to/novel
python3 scripts/cli.py backup /path/to/novel

# 并行全检（带缓存，快3-5倍）
python3 scripts/cli.py parallel 正文/ --workers 4

# 语义重复检测（需 pip install jieba）
python3 scripts/cli.py semantic 正文/ --threshold 0.7

# 缓存管理
python3 scripts/cli.py parallel --stats
python3 scripts/cli.py parallel --clear
```

### 20篇写作参考文档

| 文档 | 覆盖内容 |
|------|----------|
| checklist.md | 每章必查清单（A-E 五类） |
| hook_design.md | 钩子设计技巧与模板 |
| writing_tips.md | 新手避坑 TOP 20 |
| dialogue_quality.md | 对话去AI味指南 |
| foreshadowing.md | 伏笔管理完整流程 |
| character_state_machine.md | 角色状态机规范 |
| character_arc.md | 角色弧线四阶段模型 |
| outline_design.md | 大纲设计方法论 |
| continuity.md | 续写衔接机制 |
| emotion_arc_guide.md | 情感弧线设计 |
| reader_experience.md | 读者体验管理 |
| scene_transition.md | 场景转换技巧 |
| volume_transition.md | 多卷衔接实操 |
| writing_rhythm_guide.md | 5种节奏模板 + 10章周期 |
| style_consistency.md | 文风一致性检测 |
| smart_context.md | 智能上下文路由 |
| context_loader.md | 上下文加载器 |
| danmaku_management.md | 弹幕角色管理 |
| usage_examples.md | 完整使用示例 |
| iteration_report.md | 迭代报告 |

### 测试

```bash
cd novel-writer && python3 -m pytest scripts/tests/ -v  # 283 passed
```

## English

### Why Novel Writer?

Long-form novels (500K+ words) face one critical enemy: **inconsistency**. AI writing is especially prone to:
- Character name errors
- Timeline contradictions
- Information leaks (characters knowing what they shouldn't)
- Forgotten plot threads

Novel Writer solves this with **structured tracking + automated quality checks**.

### 12 Detection Scripts

| Script | Alias | What it Checks |
|--------|-------|---------------|
| consistency_check | `check` | Names, settings, timeline, AI words, cross-chapter repetition, missing characters |
| outline_drift | `drift` | Title match, keyword coverage, character appearance deviation |
| rhythm_check | `rhythm` | Tension, hook density, emotional tone, pacing anomalies |
| dialogue_tag_check | `dialogue` | Tag frequency, monotony, adverb overuse, dialogue ratio |
| tension_forecast | `tension` | Tension distribution prediction, trend analysis |
| foreshadow_scan | `foreshadow` | Foreshadowing pattern detection, unrecovered thread warnings |
| chapter_hook_check | `hook` | Hook types, strength scores, consecutive weak endings |
| chapter_title_check | `title` | Title length, bland detection, clickbait, info overload |
| opening_score | `opening` | Opening type, appeal score, hook detection |
| paragraph_check | `paragraph` | Long paragraphs, wall-of-text, visual pacing |
| repetition_check | `repeat` | Cross-chapter repetition, consecutive patterns |
| run_all_checks | `all` | Run everything |

### Test

```bash
cd novel-writer && python3 -m pytest scripts/tests/ -v  # 283 passed
```

### License

MIT License

### Credits

Built with ❤️ for the [OpenClaw](https://github.com/openclaw/openclaw) ecosystem.
