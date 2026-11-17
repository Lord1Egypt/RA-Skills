# sg-input-skinmaker-skill

搜狗输入法「热词皮肤」生成 skill，运行于各种 **AI client 应用**（如 workbuddy、Codex、Trae 等）中。

## 功能

把**预设 prompt 模板**与用户填写的**风格描述**融合，对用户上传的**一张图片**做图生图，
生成一张适合作为皮肤 / 背景的图片；最后返回「生成后的图片」和**校园AI创意皮肤大赛互动页面**，
由用户自行打开。

## 工作流

```
用户上传图片 + 风格描述
        │
        ▼
融合 prompt（预设模板的 %s 替换为用户风格）
        │
        ▼
图生图（AI client 宿主内置能力，输入图 + 融合 prompt）
        │
        ▼
返回生成后的图片 + 写死的 H5 地址（用户自行打开）
```

## 固定返回文案与 H5 地址

```
这张可直接参赛，得票前15名有奖
→ 保存图片并查看活动详情https://pinyin.sginput.qq.com/h5/kaixueskill/share/225448950305128448
```

文案与地址原样返回，不做任何动态参数拼接。

## 目录结构

```
sg-input-skinmaker-skill/
├── SKILL.md                        # skill 核心定义（工作流 SOP + 护栏 Guardrails）
├── references/
│   └── generation-prompt.md        # 完整生图规范（角色约定/风格化程度/比例/配色/排除清单/prompt 骨架）
├── README.md                       # 本说明文档
└── CODEBUDDY.md                    # 项目上下文
```

## 说明

本 skill 为**工作流编排型 skill**：图生图由 AI client 宿主内置能力完成，skill 本身不含
HTTP/API 调用代码，不做 CDN 上传 / 直链提取，也不自动打开页面。详细生图约束见
`references/generation-prompt.md`。
