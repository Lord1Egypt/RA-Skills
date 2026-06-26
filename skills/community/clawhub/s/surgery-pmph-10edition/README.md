# 外科学 Surgery-PMPH-10edition
<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> 基于人民卫生出版社《外科学》第10版的临床技能手册 — 240 项外科与急危重症临床技能
<br>
<br>
<img src="https://github.com/xllgreen/Surgery-PMPH-10edition-/blob/main/assets/Surgery.png" width="260px">
<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合临床外科学、急危重症医学、围手术期管理、创伤救治、肿瘤综合治疗、感染控制及多系统疾病诊疗等核心领域，涵盖 **240 项关键临床技能**，分为 17 大分类。

**适用人群**：外科医师、急诊医生、重症监护团队、医学生

**参考教材**：人民卫生出版社《外科学》第 10 版

## 项目结构

```
Surgery-PMPH-10edition/
├── SKILL.md              # 核心配置 — 240 项技能注册表
├── README.md             # 本文档 — 项目说明与使用指南
├── <skill-name>/         # 各项技能的详细定义
│   └── SKILL.md          #   技能详情（使用时机、执行步骤、参考文档）
├── scripts/              # 可执行工具脚本
│   ├── skill-search.sh   #   技能关键词搜索
│   └── skill-report.sh   #   技能清单报告生成
├── config/               # 配置文件
│   └── skill-config.yaml #   技能分类与元数据配置
└── tests/                # 验证与测试
    └── validate-all.sh   #   完整性校验脚本
```

## 技能分类一览

| 分类 | 技能数 | 说明 |
|------|--------|------|
| 🚑 急诊与复苏 | 14 | CPR、休克复苏、电解质紊乱急救 |
| 🦴 创伤与骨折 | 27 | 骨折分型、复位固定、神经损伤 |
| 🩺 普通外科与腹部急症 | 22 | 阑尾炎、肠梗阻、疝、腹膜炎 |
| 🫁 肝胆胰脾外科 | 19 | 胆道结石、胰腺炎、肝外伤 |
| 🩻 胃肠外科 | 10 | 胃癌、结直肠癌、GERD |
| 🫘 泌尿外科 | 24 | 结石、肿瘤、感染、尿道损伤 |
| 🩸 血管外科 | 7 | DVT、静脉曲张、血管修复 |
| 🔥 烧伤与整形 | 8 | 面积估算、深度分类、植皮 |
| 🧬 肿瘤外科与综合治疗 | 16 | TNM分期、放化疗、保肢手术 |
| 📋 围手术期管理 | 18 | 术前优化、抗生素、营养支持 |
| 💉 麻醉与疼痛 | 11 | 气道管理、腰麻、局麻 |
| ⚖️ 内分泌与代谢 | 6 | 甲旁亢、脱水、电解质 |
| 🦠 感染与免疫 | 7 | 结核、脓毒症、破伤风 |
| 📡 影像与介入 | 10 | 造影、内镜、介入放射 |
| 🏋️ 康复与功能评估 | 12 | 骨折康复、神经评估 |
| 🦿 风湿与脊柱疾病 | 5 | 强直性脊柱炎、椎管狭窄 |
| 🔧 其他专科技能 | 10 | ARDS、AKI、除颤等 |

## 快速开始

### 安装

CLI：
```bash
openclaw skills install surgery-pmph-10edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Surgery-PMPH-10edition" (xllgreen/surgery-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/surgery-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 安装后使用
需要对agent交代以下内容：
```bash
每次回答前请先去查一遍对应的医学skill来确认
```


### 查找技能

```bash
# 按关键词搜索
bash scripts/skill-search.sh 阑尾炎

# 生成技能清单
bash scripts/skill-report.sh
```

### 使用方式

每个技能包含四部分内容：
1. **使用时机** — 何时触发该技能
2. **执行步骤** — 标准化操作流程
3. **注意事项** — 禁忌与警示
4. **参考文档** — 详细补充资料

### 提问策略

#### 1.**概念** 
Question:
```bash
外科学中胰腺假性囊肿的概念是什么？
```
Answer：
```bash
## 胰腺假性囊肿（Pancreatic Pseudocyst, PPC）的概念
胰腺假性囊肿是**急性胰腺炎、胰腺外伤或慢性胰腺炎后**形成的并发症，本质上是**胰液经坏死或破裂的胰管溢出，在胰腺周围或小网膜囊内被纤维组织包裹形成的囊性结构**。
### 关键特征
| 特征 | 说明 |
|------|------|
| **"假性"的含义** | 囊壁**没有上皮细胞衬里**（区别于真性囊肿），由纤维结缔组织和肉芽组织构成 |
| **形成机制** | 胰管破裂 → 胰液向外渗漏 → 周围组织炎症反应包裹 → 囊壁逐渐成熟（约需 **≥6周**） |
| **囊液成分** | 富含胰酶（淀粉酶/脂肪酶）、蛋白性液体 |
| **好发部位** | 小网膜囊、胰腺周围间隙 |
### 自然转归
- **<4 cm** 的囊肿几乎均可自行吸收
- **<5 cm** 约 50% 可自行吸收
- **>6 cm 或多发** 自行吸收机会很小，需评估干预
- 囊壁成熟时间约 **6 周**，成熟后才适合做内引流
### 与真性囊肿/囊性肿瘤的鉴别
> 影像上易与胰腺囊性肿瘤（如浆液性囊腺瘤、黏液性囊腺瘤、IPMN）混淆。PPC 具有急性胰腺炎/外伤病史、囊壁无上皮、囊液淀粉酶显著升高三大特征，可资鉴别。
需要我展开讲治疗策略（观察 vs 内引流 vs 外引流 vs 切除）吗？
```

#### 2.**临床案例分析** 
Question:
```bash
女性，28岁。婚后3年不孕，闭经、溢乳6个月就诊。查体：外观容貌正常，有溢乳，眼底正常，视力视野正常。血催乳素 250ng/ml,MRI 检查发现鞍内4mmx4mm 大小的低信号区，距离视神经5mm。该病人的诊断与治疗措施是什么？
```
Answer：
```bash
## 病例分析
**关键线索梳理：**
| 项目 | 表现 |
|------|------|
| 患者 | 28岁女性 |
| 主诉 | **闭经 + 溢乳 + 不孕**（经典三联征） |
| 血 PRL | **250 ng/ml**（正常 < 25，显著升高） |
| MRI | 鞍内 **4mm × 4mm 低信号区**（微腺瘤 < 10mm） |
| 视野/视力 | **正常**，距视神经 5mm（无压迫） |
### 诊断：泌乳素型垂体微腺瘤（Prolactin-secreting Microadenoma）
**依据：**
- 高 PRL → 抑制 GnRH → **闭经-溢乳-不孕综合征**
- 4mm 肿瘤 = 微腺瘤
- 无视野缺损说明尚未压迫视交叉
### 治疗：首选药物治疗，不用手术
**一线：多巴胺受体激动剂**
| 药物 | 用法 | 优势 |
|------|------|------|
| **卡麦角林（Cabergoline）** | 0.25–0.5 mg，每周1–2次 | 首选，副作用小，服药方便 |
| 溴隐亭（Bromocriptine） | 1.25–5 mg，每日2–3次 | 备选，但恶心/头晕反应多见 |
**疗效预期：**
- **数周内** → PRL 降至正常 → 恢复排卵月经、溢乳消退
- **数月至一年** → 肿瘤显著缩小（约 80–90% 有效）
**为什么不做手术？**
- 微腺瘤首选药物治疗，有效率高、创伤小
- 经蝶手术适用于：药物耐药/不耐受、有视神经压迫症状、或怀疑非泌乳素瘤（如无功能瘤）时
- 此例距视神经 5mm、视野正常，**无手术指征**
### 随访
- 治疗后每 3–6 月复查 PRL
- 肿瘤缩小后 MRI 每年复查
- PRL 正常后即可备孕，孕期需产科+内分泌联合管理
```
#### 3.**考试题目**
Question:
```bash
下肢深静脉血栓形成最严重的并发症是
A下肢浅静脉曲张
B肺栓塞
C伴动脉痉挛、肢体缺血
D下肢溃疡
E腔静脉阻塞
```
Answer：
```bash
答案是 **B. 肺栓塞**
下肢深静脉血栓形成（DVT）最严重的并发症是**肺栓塞（Pulmonary Embolism, PE）**——血栓脱落经下腔静脉→右心房→右心室→肺动脉，可导致大面积肺梗死、猝死。
- **A** 下肢浅静脉曲张 → 属于 DVT 慢性期侧支循环代偿的表现，非严重并发症
- **C** 伴动脉痉挛、肢体缺血 → 见于"股青肿（Phlegmasia Cerulea Dolens）"型 DVT，严重但发生率远低于 PE
- **D** 下肢溃疡 → 慢性期后遗症，非最严重
- **E** 腔静脉阻塞 → 罕见，多为 DVT 向上延伸的结果
临床上 DVT 患者最致命的威胁就是 **血栓脱落致肺栓塞**，这也是为什么急性 DVT 需要立即抗凝和放置下腔静脉滤器（抗凝禁忌时）的根本原因。
```

## 关于作者

**小绿绿 xllgreen(https://xllgreen.github.io)** — 九江学院临床医学院学生·科技极客

## 技术支持
<br>
PDF2App项目：https://pdf2app.cn
<br>
Microsoft Visual Studio Code：https://code.visualstudio.com/
<br>
Claude Code for VS Code：https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API：https://platform.deepseek.com/
© 2026 杭州深度求索人工智能基础技术研究有限公司 版权所有
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API：https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## 许可证

本项目内容基于人民卫生出版社《外科学》第10版整理，仅供学习参考。

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FSurgery-PMPH-10edition-&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
 </picture>
</a>
