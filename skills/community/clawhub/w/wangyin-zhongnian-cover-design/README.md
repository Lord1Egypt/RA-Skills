# 网瘾中年公众号封面设计 Skill

把公众号文章扔给 agent，它读完内容、问你三轮问题，然后输出一段可以直接跑图的封面提示词。画幅固定 **2.35:1 横版**（公众号首图裁切安全区），完整适配「网瘾中年」品牌 VI 规范。

支持 Claude Code、Codex、WorkBuddy 以及任何支持自定义 skill 的 AI agent。

## 与原版 gbro-cover-design 的区别

基于 [pyang5166/gbro-cover-design](https://github.com/pyang5166/gbro-cover-design)（MIT）改造，主要差异：

| 维度 | 原版 gbro-cover-design | 本 Skill |
|------|------------------------|---------|
| 平台 | 公众号/小红书 3:4 竖版 | 公众号 2.35:1 横版 |
| 形象参考 | 真人正脸照（图1 人脸） | 品牌机器人 IP（图1 默认已内置） |
| 视觉风格 | 通用短视频/知识博主封面 | 工程图纸 + 深蓝科技 + FRF 波形 |
| 色彩 | 通用高饱和 | 深海蓝 Primary-900/700/500 + 橙色/青色点缀 |
| 字体 | 可选多种风格 | 思源黑体 Heavy / HarmonyOS Sans SC Heavy + Roboto Mono |
| 视觉符号 | 无固定符号 | NVH 频率响应曲线（FRF）作为品牌核心符号 |
| 禁用元素 | 基础限制 | 蓝紫渐变、粉彩、衬线体、卡通萌化、暖调摄影等 |

## 首次使用

第一次触发时 skill 会先带你完成配置（不需要 API key，本 skill 只产出提示词）：

1. **IP 参考图**：默认已内置 `assets/robot-ip-default.png`（圆润蓝色机器人，戴蓝色工程安全帽、耳机、胸口橙色仪表徽章）。如需替换，直接覆盖该文件；如不想 IP 出镜，选择「无 IP 出镜」。
2. **生图模型**：确认你用的模型支持多参考图输入（即梦/Seedream 4.0、Nano Banana、GPT-Image 等），否则无法保持 IP 形象一致性。

配置结果记在 `config.md`，之后不再重复问。

## 怎么用

把公众号文章内容发给 agent，skill 自动触发，分三轮问你：

1. **构图风格 + 封面标题**：根据文章内容推荐 1-2 种风格，同时给 1-3 个候选标题
2. **参考图**：图1 为机器人 IP 形象（默认已内置），图2 起为 UI 截图、产品图、数据图表等素材
3. **视觉细节**：表情/姿态、背景色调、字体风格、标题颜色效果

问完输出完整提示词，直接复制到生图模型跑图。不需要懂设计，不需要自己写提示词。

## 10 种构图风格

| # | 风格 | 适合什么 |
|---|------|---------|
| 1 | 深色工程图纸风 | 硬核技术解读、AI 工具方法论，品牌识别最强 |
| 2 | 极简深蓝留白风 | 观点类、深度长文，克制高级感 |
| 3 | 数据仪表盘风 | 有 UI 截图、软件界面、数据图表时首选 |
| 4 | 对比波形风 | 前后对比、案例复盘、正确 vs 错误 |
| 5 | 机器人侧置留白风 | 战略判断、行业观察，大气稳重 |
| 6 | 机器人背影构图风 | 启发、反思、趋势预判 |
| 7 | 局部道具风 | 工具测评、产品开箱、功能拆解 |
| 8 | 机器人正面指引风 | 教程、方法论、经验分享 |
| 9 | 信息拼贴风 | 多工具盘点、多案例、清单类 |
| 10 | 工业摄影风 | 硬核工程、现场检测、NVH 实操 |

每种风格的完整提示词模板在 `references/style-XX-*.md`，`references/examples.md` 还有 5 组示例做 few-shot 参照。

## 安装

本 skill 兼容任何 Agent Skills Standard 运行环境（Claude Code / Codex / Cursor / OpenClaw / Hermes / Gemini CLI / OpenCode / WorkBuddy 等）。核心只依赖 `SKILL.md` + `references/` + `assets/`，生图脚本 `gen_cover_volc.py` 为可选（纯 Python 标准库）。

### 一行命令（自动探测）
把 `wangyin-zhongnian-cover-design/` 整个目录复制到你的 skill 目录即可。例如在 WorkBuddy：

```bash
cp -r wangyin-zhongnian-cover-design \
  ~/.workbuddy/skills/wangyin-zhongnian-cover-design
```

### 各运行时路径表（手动复制用）
| 运行时 | skill 目录 |
|--------|-----------|
| WorkBuddy | `~/.workbuddy/skills/` |
| Claude Code | `~/.claude/skills/` |
| Codex / Cursor | 项目或用户级 `.skills/` 或对应 skills 目录 |
| OpenClaw / Hermes | 对应 agent 的 skills 目录（参考各自文档） |

> 只要目标环境能识别 `SKILL.md` frontmatter 即兼容，不限定某种 runtime。

注意：风格模板、示例库、VI 约束都在 `references/` 目录里，**不要只复制 SKILL.md**，必须完整复制整个目录；`gen_cover_volc.py` 仅在你想用脚本直出生图时需要。

## 文件结构

```
wangyin-zhongnian-cover-design/
├── SKILL.md              # 主 skill 入口
├── README.md             # 本文件
├── config.md             # 首次配置记录（已被 .gitignore 排除）
├── .gitignore            # 排除 config.md 和临时输出
├── gen_cover_volc.py     # 火山引擎 ARK 生图脚本（纯标准库，可选）
├── assets/               # 参考图
│   ├── robot-ip-default.png          # 默认机器人 IP 形象（图1）
│   ├── robot-expression-overwork.jpg # 疲惫加班表情参考
│   ├── robot-expression-shrug.jpg    # 摊手疑问表情参考
│   ├── robot-expression-thumbsup.jpg # 点赞推荐表情参考
│   └── robot-expression-thinking.jpg # 托腮思考表情参考
└── references/           # 模板与规范
    ├── vi-constraints.md             # 品牌视觉硬约束速查
    ├── examples.md                   # 5 组示例提示词
    ├── style-01-dark-engineering.md
    ├── style-02-minimal-dark-blue.md
    ├── style-03-dashboard-ui.md
    ├── style-04-waveform-comparison.md
    ├── style-05-robot-side-space.md
    ├── style-06-robot-back-view.md
    ├── style-07-prop-closeup.md
    ├── style-08-robot-front-guide.md
    ├── style-09-info-collage.md
    └── style-10-industrial-photo.md
```

## 生图模型建议

- **网页首选**：即梦 / Seedream 4.0（多参考图、中文文字表现较好）
- **脚本直出（已验证）**：火山引擎 ARK `doubao-seedream-5-0-260128` + 本仓库 `gen_cover_volc.py`，尺寸固定 `2976x1264`，`watermark:False`。用法见 SKILL.md「直接生图」一节。注意 pro/lite/4.5/4.0/3.0 等模型在多数账号未开通会 404
- **备选**：Nano Banana（Gemini 图像模型）、GPT-Image、Midjourney（需配合 --cref / --sref）
- **关键**：必须支持多参考图输入，否则 IP 形象一致性无法保证

## 提示词输出后

1. 复制到生图模型
2. 图1 传机器人 IP 参考图
3. 图2 起传其他素材
4. 生成后重点检查：标题文字是否错字、IP 形象是否变形、颜色是否出现蓝紫/粉彩等禁用色
5. 不满意就局部调整表情、背景、标题字重或 IP 位置后重新生成

## 品牌视觉核心

- **品牌定位**：懂工程的汽车 AI 实践者
- **主色**：深海蓝 `#001A33` / `#003A73` / `#005BAC`
- **强调色**：橙色 `#F56C2D`、青色 `#00C8FF`
- **核心符号**：NVH 频率响应曲线（FRF）
- **字体**：思源黑体 Heavy + Roboto Mono
- **IP 形象**：蓝色工程机器人（戴安全帽、耳机、胸口橙色仪表）

详细规范见 `references/vi-constraints.md`。

## License

MIT。基于 gbro-cover-design（MIT）改造，原始版权信息见原仓库 LICENSE。
