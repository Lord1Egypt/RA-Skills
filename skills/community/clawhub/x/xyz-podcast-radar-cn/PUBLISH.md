# Podcast Radar CN - Clawhub 发布包

## 包信息

- **名称**: podcast-radar-cn
- **版本**: 1.0.0
- **描述**: 中文播客数据工具包——发现 · 分析 · 追踪 · 报告
- **大小**: 140KB
- **文件数**: 15 个文件

## 包内容

```
podcast-radar-cn/
├── SKILL.md                    # 技能主文档（YAML frontmatter + Markdown）
├── README.md                   # 用户README
├── agents/
│   └── openai.yaml            # Agent配置
├── references/                # 参考文档
│   ├── api.md                # API字段说明
│   ├── output-modes.md       # 输出格式指南
│   └── title-signals.md      # 标题信号解读
└── scripts/                   # 核心脚本（9个）
    ├── fetch_xyz_rank.py     # 榜单获取
    ├── analyze_genre.py      # 竞争分析
    ├── generate_report.py    # 报告生成
    ├── batch_track.py        # 订阅追踪
    ├── track_episodes.py     # 爆款追踪
    ├── topic_trends.py       # 话题趋势
    ├── enrich_xiaoyuzhou.py  # 详情补充
    ├── track_podcast.py      # 单播客追踪
    └── track_subscription.py # 订阅追踪核心
```

## 核心亮点

1. **双数据源**: xyzrank.com 榜单 + api.xyzrank.top 趋势
2. **完整工作流**: 发现 → 分析 → 追踪 → 报告
3. **9个脚本**: 覆盖播客创作全场景
4. **零依赖**: 纯标准库，无需 pip 安装
5. **API文档**: 完整的速查卡和示例

## 发布步骤

### 方式 1: 通过 Claw CLI 发布

```bash
# 1. 确保已安装 claw CLI
claw --version

# 2. 登录 clawhub
claw login

# 3. 进入包目录
cd ~/.qclaw/workspace/skills/podcast-radar-cn-publish

# 4. 发布
claw skill publish .

# 或指定命名空间
claw skill publish . --namespace your-namespace
```

### 方式 2: 手动打包上传

```bash
# 1. 打包
cd ~/.qclaw/workspace
tar czvf podcast-radar-cn-v1.0.0.tar.gz podcast-radar-cn-publish/

# 2. 登录 clawhub.ai
# 3. 进入 "Publish Skill" 页面
# 4. 上传 tar.gz 包
# 5. 填写元数据（名称、描述、标签等）
# 6. 提交审核
```

### 方式 3: GitHub 集成（推荐）

```bash
# 1. 创建 GitHub 仓库
# 2. 推送代码
cd ~/.qclaw/workspace/skills/podcast-radar-cn-publish
git init
git add .
git commit -m "Initial release: podcast-radar-cn v1.0.0"
git remote add origin https://github.com/yourname/podcast-radar-cn.git
git push -u origin main

# 3. 在 clawhub.ai 关联 GitHub 仓库
# 4. 开启自动同步
```

## 发布前检查清单

- [x] SKILL.md 包含 YAML frontmatter（name, description）
- [x] 所有 Python 脚本语法正确
- [x] 无敏感数据（已排除 JSON 数据文件）
- [x] README.md 完整
- [x] 文件结构清晰

## 建议的标签

- 播客
- podcast
- 数据分析
- 内容创作
- xyzrank
- 小宇宙
- 中文

## 建议的发布说明

```markdown
## Podcast Radar CN v1.0.0

中文播客数据工具包，整合 xyzrank 榜单 + 官方趋势 API + 小宇宙详情，提供完整的播客发现、分析、追踪、报告工作流。

### 核心功能
- 🔍 榜单发现：热门/新锐播客和单集
- 📈 趋势分析：官方历史订阅增长数据
- 📊 订阅追踪：本地订阅量变化监控
- ⚔️ 竞争分析：分类竞争格局评估
- 📋 机会报告：完整创作机会分析
- 🔥 爆款追踪：特定话题/嘉宾单集追踪

### 快速开始
```bash
python scripts/analyze_genre.py --genre 科技
python scripts/generate_report.py --custom-query "AI"
```

### 依赖
Python 3.8+，纯标准库，无需额外安装。
```

## 安装后的使用

用户安装后可通过以下方式使用：

```bash
# 直接运行脚本
claw skill run podcast-radar-cn -- python scripts/analyze_genre.py --genre 商业

# 或在对话中触发
# "分析一下科技类播客的竞争格局"
# "帮我生成一份关于纵横四海的报告"
```

## 更新维护

建议的后续版本规划：

- v1.1.0: 添加更多可视化输出（图表）
- v1.2.0: 支持导出 Excel/PDF 报告
- v1.3.0: 添加更多数据源（荔枝、喜马拉雅）
- v2.0.0: Web 界面支持

---

**发布包位置**: `~/.qclaw/workspace/skills/podcast-radar-cn-publish/`
