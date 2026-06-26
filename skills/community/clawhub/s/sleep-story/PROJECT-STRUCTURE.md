# Sleep Story Skill - 项目结构

## 📁 完整目录结构

```
sleep-story/
│
├── 📄 核心文件
│   ├── SKILL.md                          # 主技能文件（必读）
│   ├── README.md                         # 项目说明（GitHub 首页）
│   ├── INTEGRATION.md                    # 四大系统整合说明
│   ├── COMPLETE-SUMMARY.md               # 完整优化总结
│   ├── OPTIMIZATION.md                   # 第一轮优化说明
│   ├── CONTRIBUTING.md                   # 贡献指南
│   ├── CODE_OF_CONDUCT.md                # 行为准则
│   ├── ISSUE_TEMPLATE.md                 # Issue 模板
│   ├── LICENSE                           # MIT 许可证
│   └── .gitignore                        # Git 忽略文件
│
├── 📚 references/                        # 参考文档目录
│   ├── research-evidence.md              # 科学研究依据（8 大类技术）
│   ├── element-database.md               # 元素数据库（50+ 场景×40+ 角色）
│   ├── seasonal-stories.md               # 季节性故事库（春夏秋冬）
│   ├── personalization-system.md         # 个性化适配和学习系统
│   ├── series-story-framework.md         # 系列故事框架（5 大类型）
│   ├── feedback-loop-system.md           # 反馈循环系统（效果追踪）
│   ├── psychology-techniques.md          # 心理学技术详解（8 大技术）
│   ├── story-templates.md                # 故事模板库（8+ 模板）
│   └── warm-words.md                     # 温暖词汇库（多感官）
│
├── 📖 examples/                          # 示例故事目录
│   ├── three-nights.md                   # 前三晚完整故事（可直接使用）
│   └── stories.md                        # 优化后示例故事
│
└── 💾 memory/                            # 用户数据目录（不提交到 Git）
    ├── user-preferences.json.template    # 用户偏好档案模板
    └── sleep-story-history.json.template # 历史记录模板
```

---

## 📊 文件大小统计

| 类别 | 文件数 | 总大小 | 最大文件 |
|------|--------|--------|----------|
| 核心文件 | 10 | ~20KB | README.md (6.8KB) |
| 参考文档 | 9 | ~55KB | personalization-system.md (7.5KB) |
| 示例故事 | 2 | ~8.5KB | three-nights.md (5.3KB) |
| 数据模板 | 2 | ~3KB | user-preferences.json (2.3KB) |
| **总计** | **23** | **~86.5KB** | - |

---

## 🎯 文件用途说明

### 核心文件

| 文件 | 用途 | 目标读者 |
|------|------|----------|
| `SKILL.md` | 技能核心逻辑和创作指南 | AI 技能执行者 |
| `README.md` | 项目介绍和使用说明 | GitHub 访问者 |
| `INTEGRATION.md` | 四大系统整合说明 | 开发者/高级用户 |
| `COMPLETE-SUMMARY.md` | 完整优化总结 | 开发者/研究者 |
| `CONTRIBUTING.md` | 贡献指南 | 贡献者 |
| `CODE_OF_CONDUCT.md` | 行为准则 | 社区成员 |

### 参考文档

| 文件 | 用途 | 核心内容 |
|------|------|----------|
| `research-evidence.md` | 科学依据 | 8 大类技术，20+ 研究 |
| `element-database.md` | 元素库 | 50+ 场景，40+ 角色 |
| `seasonal-stories.md` | 季节适配 | 春夏秋冬专属 |
| `personalization-system.md` | 个性化 | 偏好追踪和适配 |
| `series-story-framework.md` | 系列故事 | 5 大类型，8 个系列 |
| `feedback-loop-system.md` | 反馈优化 | 效果追踪和迭代 |
| `psychology-techniques.md` | 技术详解 | 8 大心理学技术 |
| `story-templates.md` | 模板库 | 8+ 故事模板 |
| `warm-words.md` | 词汇库 | 多感官温暖词汇 |

### 示例故事

| 文件 | 用途 | 内容 |
|------|------|------|
| `three-nights.md` | 直接使用 | 前三晚完整故事 |
| `stories.md` | 参考示例 | 优化后示例故事 |

### 数据模板

| 文件 | 用途 | 说明 |
|------|------|------|
| `user-preferences.json.template` | 用户档案 | 偏好数据结构 |
| `sleep-story-history.json.template` | 历史记录 | 去重追踪数据 |

---

## 🔧 使用流程

### 新用户

```
1. 阅读 README.md → 了解项目
2. 阅读 SKILL.md → 学习使用
3. 使用 examples/three-nights.md → 开始体验
4. 复制 memory/*.template → 建立档案
```

### 贡献者

```
1. 阅读 CONTRIBUTING.md → 了解规范
2. 选择贡献类型 → 内容/研究/系统/文档
3. 参考对应 reference 文件 → 学习格式
4. 创建分支 → 提交 PR
```

### 开发者

```
1. 阅读 INTEGRATION.md → 理解系统
2. 阅读 COMPLETE-SUMMARY.md → 了解全貌
3. 参考 research-evidence.md → 科学依据
4. 开发新功能 → 测试 → 部署
```

---

## 📈 项目指标

### 内容规模

| 指标 | 数量 |
|------|------|
| 故事场景 | 50+ |
| 角色类型 | 40+ |
| 旅程类型 | 30+ |
| 温暖发现 | 40+ |
| 感官焦点 | 20+ |
| 故事模板 | 8+ |
| 系列规划 | 8 个 |
| 研究依据 | 20+ 篇 |

### 理论组合

| 组合类型 | 数量 |
|----------|------|
| 场景×角色×旅程×发现×感官 | 480 万+ |
| 可用年限（不重复） | 13000+ 年 |

### 文档覆盖

| 维度 | 覆盖率 |
|------|--------|
| 科学依据 | ✅ 完整 |
| 创作指南 | ✅ 完整 |
| 个性化系统 | ✅ 完整 |
| 系列故事 | ✅ 完整 |
| 反馈优化 | ✅ 完整 |
| 示例故事 | ✅ 完整 |

---

## 🚀 扩展方向

### 短期（1-3 月）

- [ ] 补充更多系列故事大纲
- [ ] 增加季节性场景（每季 10+）
- [ ] 完善个性化算法
- [ ] 添加更多语言版本

### 中期（3-6 月）

- [ ] 开发语音版本（TTS 优化）
- [ ] 整合背景音乐
- [ ] 创建移动应用
- [ ] 建立用户社区

### 长期（6-12 月）

- [ ] 机器学习模型训练
- [ ] 生理数据接入
- [ ] 多平台同步
- [ ] 开放 API

---

## 📞 维护指南

### 日常维护

- 每周检查 Issue
- 每月更新文档
- 每季度大优化
- 年度版本发布

### 内容更新

- 每月新增故事模板
- 每季更新季节故事
- 半年更新研究依据
- 年度元素库扩展

### 质量控制

- 提交前检查清单
- 同行评审流程
- 用户反馈收集
- 效果数据追踪

---

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

**项目创建**：2026-04-05  
**当前版本**：v2.0  
**许可证**：MIT

---

**最后更新**：2026-04-05
