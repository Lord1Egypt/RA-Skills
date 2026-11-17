# SuperMom 育儿指南（0-12岁）

**SuperMom Parenting Guide (0-12)**

育儿号全平台内容产出引擎：一个选题，一次产出小红书、抖音、快手、B站四平台文案 + 一套图片生成提示词。

A multi-platform parenting content engine: one topic in, four sets of platform-native copy plus a matching image-prompt set out.

---

## ⚠️ 免责声明 / Disclaimer

本技能产出为 **育儿科普与内容创作参考**，不构成医疗、诊断或治疗建议。涉及疾病、用药、营养与发育问题时，请以执业儿科医生的面诊意见为准。

Output from this skill is **parenting education and content-creation reference only**. It is not medical advice. For illness, medication, nutrition, or developmental concerns, consult a licensed pediatrician.

---

## 它做什么 / What it does

| 阶段 | 产出 |
|------|------|
| 账号定位 | 按选题关键词自动判定人格（较真妈妈 / 摆烂妈妈 / 懒人妈妈 / 学霸妈妈 / 做饭妈妈 / 运动妈妈 / 规律妈妈 / 懂心妈妈），并映射到四个平台的子角色 |
| 时令检测 | 按当前日期匹配节日 / 二十四节气 / 换季 / 学校周期，推荐 3-5 个时效性选题 |
| 选题分析 | 5 维评分、年龄段锁定、爆点设计、知识挖掘（必存级 / 讨论级 / 传播级，必存级须标注来源） |
| 图片提示词 | 5-12 张 Gemini 提示词，蜡笔画风格，封面 + 内容页 + 金句收尾 |
| 平台文案 | 小红书 / 抖音 / 快手 / B站 各一套：标题候选 + 正文 + 标签 + 首评 |

产出默认落在 `output/{YYYYMMDD}_{选题简称}/`，一平台一文件夹，图片提示词单独文件夹。

---

## 快速开始 / Quick start

**安装（ClawHub）**

```bash
clawhub install supermom-parenting-guide
```

**安装（手动）**

把整个文件夹复制到你的 skills 目录（如 `~/.claude/skills/`），确保 `SKILL.md` 位于文件夹根目录。

**使用**

直接用触发词说话即可，例如：

```
做一个「1岁宝宝发烧护理」的育儿科普长图
来个「秋季腹泻预防」的全平台育儿文案
出个育儿科普图，主题是 6 个月添加辅食
```

只说平台名可收窄范围：`小红书` / `抖音` / `快手` / `B站`。不指定则四平台全出。

---

## 触发词 / Triggers

`育儿科普长图` · `做个育儿图` · `来个育儿长图` · `出个育儿科普图` · `育儿长图出图` · `四平台育儿文案`

一般育儿知识问答**不会**触发本技能，只在需要出图文 / 长图 / 多平台文案时启用。

---

## 产出结构 / Output layout

```
output/{YYYYMMDD}_{选题简称}/
├── 00_账号状态卡.md
├── 01_选题分析与爆点设计.md
├── 图片prompt/
│   ├── 图1_封面图.txt
│   ├── 图2_XXX.txt
│   ├── ...
│   └── 图N_金句收尾图.txt
├── 小红书/发布文案.md
├── 抖音/发布文案.md
├── 快手/发布文案.md
└── B站/发布文案.md
```

---

## 内容原则 / Editorial principles

- **不造数据**：数字、剂量、时间必须有可验证来源（国家卫健委、WHO、中华医学会、AAP、中国营养学会等）。
- **不冒充权威**：不虚构机构名与研究结论。
- **不贩卖焦虑**：禁用「90% 家长都不知道」「再不做就晚了」一类话术。
- **不诱导营销**：禁止送东西、抽奖、免费领取、薅羊毛等。
- **不做绝对化医疗建议**：一律「建议」「可考虑」，并提示咨询医生。

---

## 隐私与安全 / Privacy & security

- 本技能**不联网**：无外部请求、无遥测、无 API Key。
- **不采集、不上传**任何用户数据；不读取环境变量、密钥或系统目录。
- 所有产出**仅写入本地** `output/`；该目录已在 `.clawhubignore` / `.gitignore` 中排除，不会随包分发。
- 技能包内不含作者真实姓名、邮箱、电话、本机路径或任何内部标识。

---

## 目录结构 / Repository layout

```
supermom-parenting-guide/
├── SKILL.md                      # 主编：定位、选题、调度、审核
├── README.md
├── LICENSE
├── references/
│   ├── persona-library.md        # 人格库与平台子角色映射
│   ├── seasonal-topics.md        # 节日 / 节气 / 换季 / 学校周期选题
│   ├── copywriting-guide.md      # 四平台文案规范
│   ├── layout-style-guide.md     # 图片布局、风格、配色
│   ├── gemini-prompt-guide.md    # Gemini 提示词结构
│   ├── growth-strategy-guide.md  # 发布与评论区运营
│   ├── data-tracking-guide.md    # 数据追踪与复盘
│   ├── 05-copywriter/role.md     # 子角色：文案写手
│   └── 06-designer/role.md       # 子角色：视觉设计师
└── output/                       # 本地生成物（不随包分发）
```

---

## 许可 / License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — 可自由转载、改编、商用，需署名。

Released under CC BY 4.0: free to share and adapt, including commercially, with attribution.
