# question-bank-api · 题库 API 接口 Skill

把你的题库 API 封装成一个 WorkBuddy 技能。用户**购买 key → 安装 skill → 对话里取题**即可，
无需关心接口细节。

## 🔑 申请 API Key（用户第一步）

题库接口由「学库宝」提供，使用前需先申请 key：

1. 打开 https://api.xuekubao.com 注册账号；
2. 进入「API 管理」申请访问 key；
3. 购买 **¥9.9 测试套餐** 即可试用（有疑问联系微信客服：**569212182**）。

## 用户侧使用

1. 到 https://api.xuekubao.com 注册并申请 API key（见上方「申请 API Key」）。
2. 设置环境变量（或在每条命令后加 `--key` / `--base`）：
   - `QB_API_KEY`：你的 API key（X-API-Key 头）
   - `QB_API_BASE`：API 根地址（不含末尾 `/`），默认已是 `https://api.xuekubao.com`，
     一般无需修改（如需指向其他网关再覆盖）
3. 在 WorkBuddy 对话中直接说，例如：
   - "按知识点取五年级数学小数乘法的题"
   - "取出这套七年级数学期中试卷的所有题"
   - "把这几道题导出成 Word"

## 三条核心取题链路（对应你的接口）

| 意图 | 链路 |
|------|------|
| 按知识点取题 | `knowledge-tree` → 取第三级 `oldId` → `by-knowledge` |
| 按章节取题（语文/英语） | `chapter-tree` → 取章节 `id` → `by-chapter` |
| 按试卷取题 | `papers` / `paper-search` → 取试卷 `id` → `paper` |

取题后用题目里的 `md52` 调 `answer` 拿答案解析；用 `to-word` 把结构化题目渲染成 docx。

## 供应商发布步骤（让用户能搜到并安装）

技能已用 `skill-creator` 的 `package_skill.py` 打包为 `question-bank-api.zip`。两种上架方式：

1. **SkillHub（官方推荐市场，审核上架、安全可控）**
   - 网页端：访问 https://skillhub.cn 登录 → 发布 → 上传本 zip → 填名称/描述/分类/标签 →
     提交审核（通常 1–3 天）。可在发布页用 AI 辅助补全信息。
   - CLI：`skillhub login` → `skillhub init --name question-bank-api --category 教育` →
     `skillhub push` → `skillhub publish --visibility public`。
2. **ClawHub（社区市场，开放快速）**
   - 网页端：https://clawhub.ai 用 GitHub 登录 → 发布技能 → 上传本 zip → 提交审核。
   - CLI：`npm i -g clawhub` → `clawhub login` →
     `clawhub skill publish ./question-bank-api --slug question-bank-api --version 1.0.0`。

> 发布前务必把 `scripts/qb.py` 里的 `DEFAULT_BASE` 改成你的真实网关，并在 SKILL.md /
> 发布页说明用户如何购买 key。公开发布通常需实名/开发者注册。

## 目录结构

```
question-bank-api/
├── SKILL.md            # 触发描述 + 三个核心工作流
├── references/
│   └── api_docs.md     # 完整接口/字段参考（gradeId 速查、调用链路）
└── scripts/
    └── qb.py           # 标准库实现的客户端+CLI（无需 pip install）
```
