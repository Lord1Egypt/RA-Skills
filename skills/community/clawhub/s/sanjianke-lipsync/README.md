# 数字人对口型 Skill

数字人对口型（Lipsync），任务由平台弹性部署调度。

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
python3 scripts/client.py schema lipsync

# 调用
python3 scripts/client.py call lipsync <接口编码> --json '{...}'

# 异步接口默认轮询到完成；只提交不等结果：
python3 scripts/client.py call lipsync <接口编码> --json '{...}' --no-wait
```

接口清单与参数表见 [`SKILL.md`](SKILL.md)，每个接口的完整文档在 `references/api-*.md`。

---

## 目录结构

```
lipsync/
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
