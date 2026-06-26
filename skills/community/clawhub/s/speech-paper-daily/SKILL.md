---
name: speech-paper-daily
description: 语音领域每日论文速递。搜索最新语音大模型（Speech LLM、TTS、ASR、codec、speech generation）和语音前端（speech enhancement、noise suppression、beamforming、source separation、dereverberation）预印本论文，以领域专家视角精读每篇论文，输出技术方案、实验结果、简介摘要和10分制评分，并将结果写入腾讯文档「每日论文速递」文件夹。触发场景：用户说"帮我找最新语音论文"、"搜语音预印本"、"语音论文速递"、"今天有什么语音论文"、"看看最新的 TTS/ASR/语音增强论文"等。
---

# 语音论文速递 Skill

## 目标

搜索近 30 天语音领域 arXiv 预印本（20-30 篇），以领域专家视角精读，写入腾讯文档。

---

## 第一步：获取论文列表

**主要来源（优先使用）**：用 `web_fetch` 抓取 arXiv 官方每日列表页面，获取当天最新论文 ID：

1. `https://arxiv.org/list/cs.SD/new` — Sound 分类（仅今日新提交）
2. `https://arxiv.org/list/eess.AS/new` — Audio and Speech Processing 分类（仅今日新提交）

从页面中提取**当天所有 arXiv ID**，合并去重。`/new` 页面只列出今日新提交论文，无需按日期筛选。

> ⚠️ 页面只显示 ID，不含 abstract。提取 ID 后，用 `read_arxiv_paper` 逐篇读取全文（含 abstract + 正文）。

**补充来源（当天论文 < 5 篇时启用）**：使用 `search_arxiv`，`date_from` 往前推 7 天，关键词：
- `speech synthesis TTS neural`
- `automatic speech recognition ASR`
- `speech enhancement noise suppression`
- `speech separation audio`

### ⚠️ 过滤规则（必须执行）

从官方列表获取的论文已属于 `cs.SD` 或 `eess.AS`，无需额外过滤分类。但需人工判断是否与**语音/音频处理**直接相关，丢弃以下类型：
- 纯音乐生成（与语音无关）
- 纯图像/视频处理（误入 cross-list）
- 纯理论数学/物理声学（非 ML/DL 方法）

保留所有 TTS、ASR、语音增强、语音分离、说话人识别/验证、音频语言模型、声码器、语音编解码等方向的论文。

合并两个页面结果，按提交日期降序，去重后**全部保留**（不设数量上限）。

---

## 第二步：精读论文

对所有通过过滤的论文，**无论评分高低，一律读取全文**，策略如下：

1. **优先用 HTML 版本**：用 `web_fetch` 抓取 `https://arxiv.org/html/<ID>v1`，文字质量更好、公式不乱码
2. **回退 PDF**：若 HTML 页面返回 404 或内容为空，改用 `read_arxiv_paper` 读 PDF

读取全文时，注意提取论文中出现的 **demo 页面链接**（通常在 abstract 或 introduction 中，形如 `demo page`、`audio samples`、`https://xxx.github.io` 等）和**代码仓库链接**（形如 `github.com/xxx`）。

从**语音领域专家**视角输出：

```
## [序号] 论文标题

**arXiv ID**: 2501.xxxxx
**方向**: 语音大模型 / 语音前端
**作者**: 作者1, 作者2, 作者3 等
**机构**: xxx（作者所属单位，多机构用 / 分隔）
**发布日期**: YYYY-MM-DD
**论文链接**: https://arxiv.org/abs/2501.xxxxx
**PDF 链接**: https://arxiv.org/pdf/2501.xxxxx.pdf
**代码链接**: https://github.com/xxx/xxx（若论文未提供则填"暂无"）
**Demo 链接**: https://xxx.github.io/xxx（若论文未提供则填"暂无"）

### 📌 简介
2-3句话：解决什么问题，核心贡献是什么。

### 🔧 技术方案

**模型架构**：
- 整体框架（encoder/decoder结构、主干网络类型）
- 关键模块设计（注意力机制、特征提取方式、信号处理流程）
- 与 Transformer/Conformer/Mamba 等基础架构的关系

**核心创新**：
- 本文提出的新方法/新机制（与现有方法的本质区别）
- 解决了什么已有方法解决不了的问题

**训练策略**：
- 损失函数设计（感知损失、对抗损失、重建损失等）
- 数据预处理/增强方式
- 预训练 / 微调 / 多阶段训练策略（如有）

### 📊 实验结果
- 数据集 + 主要指标数值（与 baseline 对比）
- 是否开源

### ⭐ 评分：X/10
理由：创新性 / 实验充分性 / 实用价值
```

### 评分标准

| 分数 | 标准 |
|------|------|
| 9-10 | 突破性，顶会水准（Interspeech/ICASSP/NeurIPS） |
| 7-8  | 有实质贡献，实验较充分 |
| 5-6  | 增量工作，有参考价值 |
| 3-4  | 实验不足或方法普通 |
| 1-2  | 质量较低，建议跳过 |

---

## 第三步：写入腾讯文档

### 固定参数（勿改）

- **文件夹 ID**：`YUsookchBhki`（「每日论文速递」文件夹，已确认）
- **文档标题格式**：`YYYY-MM-DD 语音`
- **文档类型**：`smartcanvas`（MDX 格式）

### ⚠️ 写入方式（必须按此操作，禁止其他方式）

**步骤 1**：用 `write` 工具将完整 MDX 内容写入临时文件（如 `/tmp/speech_paper_YYYYMMDD.md`）

**步骤 2**：用 `write` 工具创建 Python 脚本（如 `/tmp/create_tdoc_YYYYMMDD.py`），脚本内容固定为：

```python
import subprocess, json

# 从文件读取内容（禁止用 f-string 拼接内容！）
with open("/tmp/speech_paper_YYYYMMDD.md", "r") as f:
    content = f.read()

args = json.dumps({
    "mdx": content,          # 参数名必须是 mdx，不是 content
    "parent_id": "YUsookchBhki",  # 文件夹 ID，必须传
    "title": "YYYY-MM-DD 语音"    # 文档标题
})

result = subprocess.run(
    ["mcporter", "call", "tencent-docs", "create_smartcanvas_by_mdx", "--args", args],
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr)
```

**步骤 3**：用 `exec` 工具执行 `python3 /tmp/create_tdoc_YYYYMMDD.py`

**步骤 4**：检查返回的 `file_id` 和 `url`，确认写入成功后告知用户。

### ⚠️ 关键注意事项（血泪教训）

1. **内容必须先写文件，再读文件传参**——禁止在脚本里 f-string 或字符串拼接 MDX 内容，否则特殊字符（引号、反引号、换行）会导致 JSON 解析失败或内容截断
2. **参数名是 `mdx`，不是 `content`**——传错参数名腾讯文档返回 400001（content is empty）
3. **`parent_id` 必须传**——不传则文档创建在根目录而非目标文件夹
4. **禁止 shell 直接拼接大段中文内容**——必须通过 Python `json.dumps` 序列化

### 文档结构模板

```markdown
# YYYY-MM-DD 语音论文速递

**共收录**: XX 篇 | **语音大模型**: XX 篇 | **语音前端**: XX 篇

> 今日 arXiv 语音相关论文（eess.AS / cs.SD / cs.CL）共命中 XX 篇。

---

## 🤖 语音大模型

[各篇论文内容]

---

## 🎙️ 语音前端

[各篇论文内容]

---

*由开心果 🍀 自动生成 · 数据来源：arXiv*
```

---

## 注意事项

- 过滤严格执行，宁少勿滥，不混入非语音论文
- 全程中文输出，论文标题保留英文原文
- 腾讯文档写入失败时直接在对话输出结果并告知原因
- 若文档内容过长（> 8000 字），拆为两个文档分别写入，标题加 `(上)` / `(下)` 后缀
