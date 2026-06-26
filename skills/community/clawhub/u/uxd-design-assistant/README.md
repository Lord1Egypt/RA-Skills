# UXD 设计流程助手

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**UXD 设计流程助手**是由 UXPA 中国用户体验协会（AIGC 专委会）委托开发的公益开源项目，专为备战 **UXDA 全国高校用户体验设计大赛**的师生设计。本工具基于 OpenClaw 平台运行，旨在帮助参赛者学习并掌握正确的用户体验设计流程与方法，而非替代参赛者完成设计工作。

> 🎯 **核心理念**：以人为本、创新驱动、授人以渔，而非授人以鱼。

---

## 作者与授权

- **作者**：kingsunzhang
- **所属机构**：UXPA 中国用户体验协会 理事 / AIGC 专委会 技术推广负责人
- **授权方式**：MIT License
- **商业授权**：⚠️ 未经 **UXPA 中国用户体验协会** 与 **作者 kingsunzhang** 双方同时书面授权，**禁止**将本项目用于任何商业用途。违者将被追究法律责任与民事赔偿责任。

---

## 功能特性

### 📐 设计流程五阶段覆盖

```
调研阶段 → 分析阶段 → 设计阶段 → 测试阶段 → 输出阶段
```

### 🛠️ 核心工具

| 工具 | 说明 |
|------|------|
| 用户研究辅助 | 访谈法、问卷法、观察法、同理心地图等方法论指导 |
| 竞品分析辅助 | 功能拆解、体验对比、分析报告框架 |
| 低保真原型辅助 | 页面结构、信息架构、交互逻辑、线框图要点 |
| 测试辅助 | 可用性测试设计、SUS 评估指标、测试脚本 |
| 文档辅助 | 设计说明框架、报告格式、作品集展示 |

### 🤖 自动化脚本

| 脚本 | 用途 |
|------|------|
| `interview_generator.py` | 生成半结构化访谈大纲 |
| `competitor_analysis.py` | 生成竞品功能对比表格 |
| `video_script_generator.py` | 生成 UXD 作品展示视频分镜脚本 |

---

## 安装方法

### 方式一：通过 ClawHub 安装（推荐）

```bash
# 安装 OpenClaw CLI（如果尚未安装）
npm i -g openclaw

# 搜索并安装本技能
clawhub install uxd-design-assistant
```

### 方式二：手动安装

将本仓库克隆到本地 OpenClaw 的 skills 目录：

```bash
git clone https://github.com/kingsunzhang-openclaw/UXDA.git
# 将 uxd-design-assistant 目录移入 OpenClaw skills 目录
```

---

## 使用示例

### 示例一：获取设计流程指引

```
用户：我们要参加UXDA大赛，项目是校园活动推荐平台，接下来不知道从哪里开始。
助手（激活 uxd-design-assistant）：根据你的描述，你们目前处于「调研阶段」。
建议按以下步骤进行：...
```

### 示例二：生成访谈大纲

```bash
python3 scripts/interview_generator.py --goal "校园活动平台使用体验" --count 8
```

### 示例三：生成竞品分析表格

```bash
python3 scripts/competitor_analysis.py --products "活动行,Eventbrite,豆瓣活动" --format markdown
```

### 示例四：获取低保真原型建议

```
用户：如何设计新闻APP的首页低保真原型？
助手（激活 uxd-design-assistant）：参考 wireframe-guide.md，首页应包含...
```

---

## 适用对象

- 备战 UXDA 大赛的参赛师生
- 学习用户体验设计（UX）/ 服务设计（SD）的高校学生
- 需要系统化设计流程指导的入门学习者
- 希望借助 AI 工具提升备赛效率的指导老师

---

## 使用原则

1. **不代劳** — 仅提供方法论和框架，不替代用户完成设计
2. **循序渐进** — 根据当前阶段提供相应工具，不跳阶段
3. **鼓励思考** — 多提问少给答案，引导理解"为什么"
4. **证据驱动** — 设计决策需有调研或测试数据支撑

---

## 相关资源

- [UXPA 中国用户体验协会](https://www.uxpa.org.cn)
- [UXDA 大赛官网](http://www.uxda.cn)
- [OpenClaw 官网](https://www.openclaw.ai)
- [ClawHub 市场](https://clawhub.ai)

---

## 致谢

本项目为 UXPA 中国用户体验协会 AIGC 专委会的公益技术推广项目，感谢协会对 AIGC 辅助教学工具研发的持续投入。

---

*本项目仅供学习和公益使用，商业用途需经 UXPA 中国用户体验协会与作者 kingsunzhang 双方授权。*
