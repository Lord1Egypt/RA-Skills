# AI 数字人 · 全驱动口播视频

**一张照片 + 一段录音 = 一条口播视频。**

不用架机位、不用出镜、不用背稿、不用后期剪辑。给了人物图片和驱动音频，
平台就能生成自然稳定的数字人视频——口型、表情、肢体一起动。

---

## 一条视频多少钱

**按驱动音频的时长计费**，四档清晰度单价不同（1 元 = 100 点）：

| `mode` | 档位 | 点/秒 | 折合 | **60 秒视频** |
|---|---|---|---|---|
| `fast` | 快速模式 | **1.5** | **0.015 元/秒** | **90 点 = 0.90 元** |
| `standard` | 标准模式（默认） | 2 | 0.02 元/秒 | 120 点 = 1.20 元 |
| `2k` | 高清模式 | 4 | 0.04 元/秒 | 240 点 = 2.40 元 |
| `4k` | 超清模式 | 8 | 0.08 元/秒 | 480 点 = 4.80 元 |

> `fast` 到 `4k` 单价差 **5.3 倍**。发布平台会二次压缩的，`fast` / `standard` 就够了；
> 只有要留后期余量才上 `2k` / `4k`。`query` 查询任务**免费**。

**怎么选档**：抖音/小红书/视频号竖版口播 → `fast` 或 `standard`；
批量铺矩阵号测脚本 → `fast`；正式投放 → `standard`；
大屏或要二次剪辑 → `2k`；交付母版 → `4k`。

---

## 前置条件

一把 **api.a7w.cn 的 API Key**。完整的注册、充值、取 Key 步骤见
[`references/getting-started.md`](references/getting-started.md)，
或直接去 [算力集市 · 注册领 API Key](https://api.a7w.cn/)。

```bash
python3 scripts/client.py login --key sk-你的key
python3 scripts/client.py whoami
```

---

## 使用

```bash
# 看这个插件有哪些接口、参数是什么
python3 scripts/client.py schema image_human

# 调用
python3 scripts/client.py call image_human <接口编码> --json '{...}'

# 异步接口默认轮询到完成；只提交不等结果：
python3 scripts/client.py call image_human <接口编码> --json '{...}' --no-wait
```

接口清单与参数表见 [`SKILL.md`](SKILL.md)，每个接口的完整文档在 `references/api-*.md`。

---

## 目录结构

```
image-human/
├── SKILL.md                   概览、接口索引与参数表
├── README.md                  本文件
├── LICENSE.md
├── references/
│   ├── getting-started.md     注册 / 充值 / 取 Key / 配置
│   └── api-*.md               各接口官方文档（2 个）
└── scripts/
    └── client.py                 通用客户端（零依赖）
```

---

## 客户端命令

| 命令 | 作用 |
|---|---|
| `login --key sk-xxx` | 验证并保存 Key 到 `~/.a7w/config.json` |
| `whoami` | 验证 Key，看可用插件数 |
| `apps` | 列出这个 Key 能用的所有插件 |
| `schema <app>` | 看某插件的接口与参数 |
| `call <app> <api> --json '{...}'` | 调用接口（异步自动轮询） |
| `task <task_id>` | 查异步任务状态 |
| `points` | 看最近任务的用量汇总 |

`--key` / `--host` 放在子命令前后都可以。

---

## 依赖

- Python 3.8+，**仅标准库**（urllib），无第三方包
- 需要能访问 `api.a7w.cn`

---

## 安全

- Key 存在本机 `~/.a7w/config.json`（权限 600）或环境变量 `A7W_API_KEY`
- 脚本只把 Key 发往 `api.a7w.cn`
- **不要**把 Key 提交到代码仓库

---

## 许可证

MIT，见 `LICENSE.md`。

---

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |
| [0人公司 · AI Agent 平台](https://a7w.cn/) | a7w.cn | 主站，了解整套 AI Agent 生态 |
