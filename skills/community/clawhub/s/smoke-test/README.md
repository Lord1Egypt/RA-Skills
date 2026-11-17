# 冒烟测试（Smoke Test）— 技能发布说明

> 作者：**大雪块** ｜ 版本：**1.0.0** ｜ 许可证：**Apache-2.0**
> 技能类型：用户级（通用 Web 应用 QA 工作流）

---

## 一、这是什么

「冒烟测试」是一个**多模态大模型辅助的 Web 应用「测试—修复」迭代工作流**技能。它把一次真实项目中沉淀出的经验，抽象成一套不绑定技术栈、可跨项目复用的质量保障流程：

**测试 → 审核 → 修复 → 回归 → 报告**（收敛式闭环）

适用对象：任何需要系统化 QA 的 Web 应用（前端 + 后端 API）。已验证可覆盖纯前端、FastAPI/Node 后端、多 JS 补丁层竞争等典型场景。

---

## 二、核心能力

| 能力 | 说明 |
|------|------|
| 全视图遍历 | 自动枚举并遍历所有视图，逐页抓取指标卡文本、截图、监控错误 |
| 多模态校验 | DOM 文本断言 + 截屏证据 + API 真值比对，比纯 OCR 更精准 |
| 根因定位 | 用 `window.fn.toString()` 运行时读源码，识别多 loader 竞争、端点错接 |
| 代码级修复 | 前端改盘即生效式修复 + 后端重启式修复，带时间戳备份 |
| 回归闭环 | 每轮修复后重跑全套测试，禁止串扫描防旧 bug 复现 |
| 证据链报告 | 自动产出自包含 HTML 报告（内嵌截图与断言表） |

内置 **11 项校验方案 V1–V11**（DOM 断言、禁止串扫描、截屏、API 真值、函数探针、控制台监控、并发压测、协议审计、DB 快照、降级横幅、前后态断言）。

---

## 三、安装

### WorkBuddy / CodeBuddy

将 `webapp-qa-workflow/` 目录解压到用户技能目录（系统自动发现）：

```bash
unzip webapp-qa-workflow.zip -d ~/.workbuddy/skills/
```

### OpenClaw

OpenClaw 技能目录为 `~/.openclaw/skills/`，同样解压即可：

```bash
unzip webapp-qa-workflow.zip -d ~/.openclaw/skills/
```

解压后目录结构应为：`~/.openclaw/skills/webapp-qa-workflow/SKILL.md`。

---

## 四、触发方式

在对话中提到以下任一短语，AI 即加载本技能：

- 中文：`测试` / `回归` / `修复验证` / `功能测试` / `冒烟测试` / `全面测试` / `审计`
- 英文：`test` / `regression test` / `functional test` / `quality assurance` / `smoke test` / `audit`

---

## 五、五阶段工作流

```
测试 → 审核 → 修复 → 回归 → 报告
  ↑                        │
  └── 发现问题 → 进入下一轮 ┘
```

1. **全面测试**：A/B/C 三级矩阵（只读→可逆写→破坏性），Playwright 遍历全视图，DOM 断言 + 禁止串扫描。
2. **审核定位**：截屏 vs API 真值比对；区分「真缺陷 / 误报 / 设计占位」；`window.fn.toString()` 查多 loader 竞争。
3. **代码修复**：前端下载→编辑→`node --check`→上传→带时间戳备份；后端改源→重启→health 200。关键约定：**禁止任何层无归一化函数直接 `*100`**。
4. **回归验证**：重跑全套，0 控制台错误 / 0 禁止串 / 关键断言通过为达标。
5. **工作报告**：产出自包含 HTML 报告，上传 `docs/` 并沉淀到长期记忆。

---

## 六、目录结构

```
webapp-qa-workflow/
├── SKILL.md                         # 五阶段工作流 + 工具链模式 + 关键约定
├── _skillhub_meta.json              # 发布元数据（中文名/作者/示例/图标）
├── LICENSE.txt                      # Apache-2.0
├── README.md                        # 本发布说明
├── references/
│   └── verification-schemes.md      # V1–V11 校验方案详解 + 工具选择指南
└── scripts/
    ├── probe_functions.js           # 全局 onclick 函数探针模板
    └── smoke_views.js               # 多视图回归冒烟模板
```

---

## 七、换项目复用

两个脚本模板只需替换顶部 CONFIG 即可适配新项目：

| 变量 | 位置 | 含义 |
|------|------|------|
| `VIEWS[]` | `scripts/smoke_views.js` | 当前项目的视图 ID 列表 |
| `FORBIDDEN[]` | `scripts/smoke_views.js` | 旧 bug 特征串（如 `'NaN%'`、`'12300%'`） |
| `SPECIFIC_ASSERTS[]` | `scripts/smoke_views.js` | 必须满足的特定指标断言 |
| `BASE_URL` | `scripts/*.js` | 目标地址 |

---

## 八、打包与发布

本技能已随附可发布 zip（`webapp-qa-workflow.zip`）。如需自行重新打包：

```bash
# 方式 A：使用 skill-creator 的打包脚本（自动校验后打包）
python ~/.workbuddy/skills/skill-creator/scripts/package_skill.py \
    ~/.workbuddy/skills/webapp-qa-workflow ./dist

# 方式 B：直接 zip（保持目录结构）
cd ~/.workbuddy/skills && zip -r webapp-qa-workflow.zip webapp-qa-workflow/
```

打包物应包含：`SKILL.md`、`_skillhub_meta.json`、`LICENSE.txt`、`README.md`、`references/`、`scripts/`。

---

## 九、许可证

Apache License 2.0。详见 `LICENSE.txt`。保留版权声明与许可证副本即可自由分发、修改、二次发布。

---

## 十、版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-08-08 | 首次发布：五阶段闭环 + V1–V11 校验方案 + 两个脚本模板，中文名「冒烟测试」，作者大雪块 |
