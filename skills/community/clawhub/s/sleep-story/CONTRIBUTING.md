# 贡献指南 - Sleep Story Skill

感谢你对本项目的关注！欢迎各种形式的贡献。🎉

## 📋 目录

- [贡献类型](#贡献类型)
- [开发环境设置](#开发环境设置)
- [提交流程](#提交流程)
- [代码规范](#代码规范)
- [故事创作规范](#故事创作规范)

---

## 🎯 贡献类型

### 1. 内容贡献

#### 新增故事模板
- 位置：`references/story-templates.md`
- 要求：遵循催眠递进结构（5 段式）
- 字数：1500-2500 字
- 检查：禁忌内容清单

#### 新增元素
- 位置：`references/element-database.md`
- 类型：场景/角色/旅程/发现/感官焦点
- 要求：提供核心意象、感官焦点、适用情绪

#### 新增温暖词汇
- 位置：`references/warm-words.md`
- 要求：符合助眠主题，避免刺激词汇

#### 季节性故事
- 位置：`references/seasonal-stories.md`
- 要求：符合当季意象和色彩基调

### 2. 研究贡献

#### 新增研究依据
- 位置：`references/research-evidence.md`
- 要求：
  - 同行评议期刊
  - 提供完整引用
  - 包含效果量数据
  - 说明应用场景

### 3. 系统优化

#### 个性化系统
- 位置：`references/personalization-system.md`
- 内容：推荐算法、偏好计算、学习逻辑

#### 反馈系统
- 位置：`references/feedback-loop-system.md`
- 内容：反馈收集、数据分析、优化流程

### 4. 文档贡献

#### 文档完善
- 修复拼写错误
- 补充说明
- 添加示例
- 翻译（多语言支持）

### 5. Bug 报告

#### 提交 Issue
- 位置：https://github.com/yourusername/sleep-story-skill/issues
- 模板：[ISSUE_TEMPLATE.md](ISSUE_TEMPLATE.md)
- 要求：
  - 清晰描述问题
  - 提供复现步骤
  - 附上相关日志
  - 标注优先级

---

## 🛠️ 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/sleep-story-skill.git
cd sleep-story-skill
```

### 2. 创建分支

```bash
# 功能开发
git checkout -b feature/your-feature-name

# Bug 修复
git checkout -b fix/issue-number

# 文档更新
git checkout -b docs/update-description
```

### 3. 目录结构

```
sleep-story/
├── SKILL.md                          # 主技能文件
├── README.md                         # 项目说明
├── LICENSE                           # 许可证
├── .gitignore                        # Git 忽略文件
├── INTEGRATION.md                    # 系统整合说明
├── COMPLETE-SUMMARY.md               # 优化总结
├── references/                       # 参考文档
│   ├── research-evidence.md         # 研究依据
│   ├── element-database.md          # 元素数据库
│   ├── seasonal-stories.md          # 季节故事
│   ├── personalization-system.md    # 个性化系统
│   ├── series-story-framework.md    # 系列故事
│   ├── feedback-loop-system.md      # 反馈系统
│   ├── psychology-techniques.md     # 心理学技术
│   ├── story-templates.md           # 故事模板
│   └── warm-words.md                # 温暖词汇
├── examples/                         # 示例故事
│   ├── three-nights.md              # 前三晚故事
│   └── stories.md                   # 优化示例
└── memory/                           # 用户数据（不提交）
    ├── user-preferences.json.template
    └── sleep-story-history.json.template
```

---

## 📤 提交流程

### 1. 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### 2. Type 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(series): 添加治愈旅程系列` |
| `fix` | Bug 修复 | `fix(recommend): 修复推荐算法权重` |
| `docs` | 文档更新 | `docs(readme): 更新快速开始指南` |
| `style` | 格式调整 | `style(format): 统一 Markdown 格式` |
| `refactor` | 重构 | `refactor(system): 优化个性化系统` |
| `test` | 测试 | `test(story): 添加故事效果测试` |
| `chore` | 构建/工具 | `chore(deps): 更新依赖` |

### 3. 提交示例

```bash
# 新功能
git commit -m "feat(story): 添加冬季专属故事模板"

# Bug 修复
git commit -m "fix(recommend): 修复元素冷却期计算错误"

# 文档更新
git commit -m "docs(readme): 补充安装步骤说明"

# 多行提交
git commit -m "feat(series): 添加《星星旅馆》系列

- 完成 7 集完整大纲
- 添加连续性设计说明
- 补充独立性保证机制

Closes #12"
```

### 4. 推送代码

```bash
# 推送到远程
git push origin feature/your-feature-name

# 设置上游分支（首次）
git push -u origin feature/your-feature-name
```

### 5. 创建 Pull Request

1. 访问 GitHub 项目
2. 点击 "New Pull Request"
3. 选择分支
4. 填写 PR 描述
5. 等待审核

### 6. PR 模板

```markdown
## 描述
简要说明本次 PR 的目的

## 类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 重构
- [ ] 其他

## 相关 Issue
Closes #issue-number

## 测试
- [ ] 已测试新功能
- [ ] 已验证修复
- [ ] 已更新文档

## 截图（如适用）
[截图]

## 其他说明
[任何额外信息]
```

---

## 📝 代码规范

### Markdown 规范

1. **标题**
   - 使用 ATX 风格（# 标题）
   - 标题后空一行

2. **列表**
   - 统一使用 `-` 或 `*`
   - 列表项之间不空行

3. **代码块**
   - 指定语言类型
   - 保持缩进一致

4. **链接**
   - 使用相对路径
   - 提供清晰的链接文本

### 文件命名

- 小写字母
- 连字符分隔
- 英文命名
- 示例：`story-templates.md`

### 注释规范

```markdown
<!-- 注释内容 -->

<!-- 
多行注释
用于复杂说明
-->
```

---

## 📖 故事创作规范

### 1. 结构要求

遵循**催眠递进结构**（5 段式）：

```
【第一阶段】注意力聚焦 (150-200 字)
【第二阶段】身心放松 (400-500 字)
【第三阶段】情绪安抚 (200-250 字)
【第四阶段】意识模糊 (150-200 字)
【第五阶段】睡眠诱导 (250-300 字)
```

### 2. 禁忌内容

❌ **绝对禁止**：
- 紧张刺激情节（追逐、冲突、危险）
- 负面情绪词汇（恐惧、愤怒、绝望）
- 突然转折或惊吓
- 需要思考的复杂逻辑
- 明亮色彩（红色、橙色）
- 电子设备、工作学习相关内容

✅ **推荐使用**：
- 重复、可预测的节奏
- 温暖、柔和的意象
- 安全、被保护的感觉
- 逐渐淡出的结尾
- 自然过渡到睡眠的暗示

### 3. 字数要求

- 短篇：1000-1500 字
- 中篇：1500-2000 字（推荐）
- 长篇：2000-2500 字

### 4. 质量检查清单

提交前检查：

- [ ] 催眠元素完整（5 段结构）
- [ ] 禁忌内容避免
- [ ] 去重检查通过
- [ ] 字数符合要求
- [ ] 温暖词汇使用
- [ ] 心理学技术融入
- [ ] 语法和拼写正确
- [ ] 格式统一

---

## 🔍 审核流程

### 1. 自动检查

- GitHub Actions 运行
- Markdown 格式检查
- 链接有效性验证

### 2. 人工审核

- 内容质量审核
- 科学性验证
- 一致性检查

### 3. 反馈时间

- 初次审核：3-5 个工作日
- 修改后审核：1-2 个工作日

---

## 🎓 学习资源

### 内部文档

- [SKILL.md](SKILL.md) - 技能核心文档
- [research-evidence.md](references/research-evidence.md) - 研究依据
- [story-templates.md](references/story-templates.md) - 模板示例

### 外部资源

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Markdown Guide](https://www.markdownguide.org/)

---

## ❓ 常见问题

### Q: 我可以贡献什么？
A: 任何内容！故事、研究、代码、文档、翻译、建议都可以。

### Q: 我没有心理学背景可以贡献吗？
A: 可以！内容贡献不需要专业背景，但研究贡献需要提供可靠来源。

### Q: 如何测试我的故事？
A: 先自己朗读测试，然后邀请朋友试用，收集反馈。

### Q: 提交后多久能合并？
A: 通常 3-5 个工作日，复杂功能可能需要更长时间。

### Q: 我可以认领 Issue 吗？
A: 当然！在 Issue 下评论表示愿意认领即可。

---

## 🙏 致谢

感谢所有贡献者！你们的付出让这个项目变得更好。

[贡献者列表](https://github.com/yourusername/sleep-story-skill/graphs/contributors)

---

**最后更新**：2026-04-05
**版本**：1.0
