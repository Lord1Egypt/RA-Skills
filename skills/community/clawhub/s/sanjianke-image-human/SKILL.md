---
name: image-human
slug: image-human
displayName: AI数字人视频生成照片说话口播虚拟主播带货视频一键出片2K4K高清
description: "一张照片 + 一段录音，生成自然稳定的数字人口播视频——不用架机位、不用出镜、不用后期剪辑。四档清晰度可选，最低 0.015 元/秒，一条 60 秒口播视频最低 0.90 元。含完整参数表、分档计费口径与常见坑。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
version: 1.1.1
summary: "一张照片加一段录音，就能生成自然稳定的数字人口播视频——不用架机位、不用出镜、不用后期剪辑。支持 4 档清晰度（fast 快速 / standard 标准 / 2K 高清 / 4K 超清），按驱动音频时长计费，最低 1.5 点/秒（0.015 元/秒），一条 60 秒口播视频最低 0.90 元。适用于短视频口播矩阵号、电商带货讲解、知识科普、企业培训视频、课程讲师替身、虚拟主播、多语言版本批量生产、老照片复活与纪念视频等场景。含 submit / query 两个接口的完整参数表、mode 分档的真实计费口径（2K 是标准档的 2 倍、4K 是 4 倍）、图片与音频的入参要求、常见坑与排错，以及一个零依赖客户端。一个 Key 调用全部 AI 算力，不用自己部署 GPU，也不用同时管理几家的账单与配额。包内含完整操作文档与零依赖客户端（`SKILL.md` + `references/`）。需要自备 api.a7w.cn 的 API Key，注册领 Key 见 https://api.a7w.cn/ 。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - 设计多媒体
  - 数字人
  - 口播视频
  - 虚拟主播
  - 带货视频
---

# AI 数字人 · 全驱动口播视频

**一张照片 + 一段录音 = 一条口播视频。**

不用架机位、不用出镜、不用背稿、不用后期剪辑。给了人物图片和驱动音频，
平台就能生成自然稳定的数字人视频——口型、表情、肢体一起动。

| 你最关心 | 答案 |
|---|---|
| 多少钱 | **最低 1.5 点/秒 = 0.015 元/秒**（1 元 = 100 点） |
| 一条 60 秒口播 | **最低 90 点 = 0.90 元**（fast 档） |
| 要多清晰 | 四档：`fast` / `standard` / `2k` / `4k`，价格差 5.3 倍，**先算钱再选档** |
| 要多久 | 异步任务，提交后轮询；`query` 免费 |
| 要装什么 | **什么都不用装**。零依赖 Python 客户端只用标准库，或者直接用 `curl` |

**没有 Key 先去领**：[算力集市 api.a7w.cn](https://api.a7w.cn/) 注册（新用户有赠送点数，
可以先白跑几条试试）。完整步骤见 [`references/getting-started.md`](references/getting-started.md)。

---

## 一、一条视频多少钱（分档计费）

**按驱动音频的时长计费**，不同清晰度档位单价不同。四档的真实价格：

| `mode` | 档位 | 点/秒 | 折合 | **60 秒视频** | 120 秒视频 |
|---|---|---|---|---|---|
| `fast` | 快速模式 | **1.5** | **0.015 元/秒** | **90 点 = 0.90 元** | 180 点 = 1.80 元 |
| `standard` | 标准模式（默认） | 2 | 0.02 元/秒 | 120 点 = 1.20 元 | 240 点 = 2.40 元 |
| `2k` | 高清模式 | 4 | 0.04 元/秒 | 240 点 = 2.40 元 | 480 点 = 4.80 元 |
| `4k` | 超清模式 | 8 | 0.08 元/秒 | 480 点 = 4.80 元 | 960 点 = 9.60 元 |

> **`fast` 到 `4k`，单价差 5.3 倍。** 同一段 60 秒音频，`fast` 花 0.90 元、
> `4k` 花 4.80 元。**先想清楚这条片子发在哪**，再选档 —— 这是这个接口最容易花冤枉钱的地方。

**`query` 查询任务免费**，可以放心轮询。

> ⚠️ 价格来自接口的 `pricing_matrix`（`fast:1.5 / standard:2 / 2k:4 / 4k:8`）。
> 平台另有标准价与智能路由后的结算价，**以你账号里实际扣费为准**。

---

## 二、四档清晰度怎么选

| 你的用途 | 建议档位 | 理由 |
|---|---|---|
| 抖音 / 小红书 / 视频号竖版口播 | **`fast` 或 `standard`** | 平台本身会二次压缩，4K 上传后也看不出来 |
| 批量铺矩阵号、先测脚本 | **`fast`** | 成本压到最低，跑量首选 |
| 正式投放素材、品牌片 | **`standard`** | 性价比平衡点，多数场景够用 |
| 大屏播放、官网宣传片、二次剪辑素材 | **`2k`** | 留出裁剪与放大余量 |
| 影院 / 展馆 / 需要交付母版 | **`4k`** | 只有真需要母版时才值得 |

**一句话原则**：**发布平台会压缩的，就别买 4K。** 需要留后期余量的，才往上升档。

---

## 三、两个接口

| 接口 | 名称 | 模式 | 计费 |
|---|---|---|---|
| `submit` | 提交任务 | 异步 | 按输入音频时长 × 档位单价（1.5 / 2 / 4 / 8 点每秒） |
| `query` | 查询任务 | 同步 | **免费** |

---

## 四、⚠️ 用之前：先拿一个 Key，否则跑不起来

**本 Skill 不内嵌任何密钥，也不代付费用。** 必须有一个 `api.a7w.cn` 的 API Key。

### 第一步：注册并创建 Key

1. 打开 **[算力集市 api.a7w.cn](https://api.a7w.cn/)** 注册（新用户有赠送点数）
2. 在控制台创建一个 API Key，形如 `sk-xxxxxxxx...`
3. **完整复制保存** —— 多数平台只在创建时显示一次

### 第二步：把 Key 填进你正在用的地方

| 你在哪用 | 怎么填 |
|---|---|
| **AI 工具 / Agent 平台**（Kimi、扣子、SkillHub 客户端等） | 平台的**环境变量 / 凭证管理 / 插件配置**里加：`A7W_API_KEY` = `sk-你的key` |
| **本机命令行** | `export A7W_API_KEY=sk-你的key`（Windows 用 `$env:A7W_API_KEY="..."`） |
| **只想跑一次** | 命令里直接带 `--key sk-你的key` |
| **长期本机使用** | `python3 scripts/client.py login --key sk-你的key` |

**读取顺序**：`--key` 参数 → 环境变量 `A7W_API_KEY` → `~/.a7w/config.json`

> 详细步骤（注册、充值、兑换算力、常见错误）见
> [`references/getting-started.md`](references/getting-started.md)。

---

## 五、操作文档：怎么调用

### 零安装用法（推荐先看这个）

本 Skill 自带一个只用 Python 标准库的客户端，**不需要装任何第三方包**：

```bash
# 1. 配置你自己的 API Key（只需一次）
export A7W_API_KEY=sk-你的key

# 2. 看这个插件的接口与参数
python3 scripts/client.py schema image_human

# 3. 提交任务（异步，客户端会自动轮询到结束）
python3 scripts/client.py call image_human submit \
  --json '{
    "file_url": "https://你的存储/人物照片.png",
    "ref_file_url": "https://你的存储/口播录音.mp3",
    "mode": "standard"
  }'
```

### 直接 curl

```bash
# 提交任务
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/image_human/submit" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://你的存储/人物照片.png",
    "ref_file_url": "https://你的存储/口播录音.mp3",
    "mode": "standard"
  }'

# 拿返回的 task_id 查结果（免费）
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/image_human/query" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_id":"<上一步返回的 task_id>"}'
```

提交成功返回形如：

```json
{ "task_id": 123, "status": "pending" }
```

`client.py call` **默认自动轮询到结束**；加 `--no-wait` 只提交不等。

---

## 六、素材要求（决定成败）

这个接口只有两个必填参数，但**质量全压在这两份素材上**。

### `file_url` · 人物图片file_url### `ref_file_url` · 驱动音频ref_file_url### `prompt` · 可选提示词promptfile_url