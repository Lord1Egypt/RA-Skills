---
name: xiaohongshu
description: >
  小红书自动化运营工具-支持：搜索笔记、查看笔记详情及评论、浏览推荐流、发布图文笔记。
  当用户提及 xiaohongshu、小红书、RedNote，或需要在该平台进行内容调研/发布时使用。
---

# 小红书 MCP

本 Skill 是一个薄的 Python 客户端，通过 HTTP 调用用户**自行独立安装、启动并保管**的第三方本地组件 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)。本 Skill 不分发、不捆绑、不自动拉取任何第三方二进制。首次安装请参阅 [SETUP.md](SETUP.md)。

## 客户端侧自动护栏（客户端拒绝执行的条件）

以下检查由 `scripts/xhs_client.py` **自动执行**，任何一项不满足都会直接拒绝发起调用：

| 检查 | 触发条件 | 客户端行为 |
| ---- | -------- | ---------- |
| Loopback 端点 | 目标地址不解析到 127.0.0.1/localhost/::1 | 进程启动即拒绝（退出码 1） |
| 非交互发布 | stdin 非 TTY 且未传 `--yes` | 拒绝 `publish`，返回 error |
| 交互发布确认 | TTY 下用户未输入 `PUBLISH` 字面量 | 取消 `publish` |
| 专用账号声明 | `XHS_DEDICATED_ACCOUNT` 未显式置 `yes` | 拒绝 `publish` |
| 上游版本可见性 | `XHS_UPSTREAM_PINNED_VERSION` 未设置 | `status` 输出中性提醒 |

这些不是建议，是**运行时机械拒绝**。用户或代理无需依赖额外自律。

## 快速参考

```bash
python scripts/xhs_client.py status
python scripts/xhs_client.py search "美食推荐"
python scripts/xhs_client.py search "美食" --sort "最多点赞" --type "图文" --time "一周内"
python scripts/xhs_client.py detail <feed_id> <xsec_token> --comments
python scripts/xhs_client.py feeds
python scripts/xhs_client.py publish "标题" "正文" "图1,图2" --tags "标签1,标签2"
```

所有命令支持 `--json` 输出原始 JSON。

## 工作流：市场调研（只读）

```
进度：
- [ ] 第 1 步：验证连接
- [ ] 第 2 步：搜索关键词
- [ ] 第 3 步：获取笔记详情
- [ ] 第 4 步：分析结果
```

**第 1 步**

```bash
python scripts/xhs_client.py status
```

**第 2 步**

```bash
python scripts/xhs_client.py search "户外电源" --sort "最多点赞" --json
```

筛选：`--sort`（综合/最新/最多点赞/最多评论/最多收藏）、`--type`（不限/视频/图文）、`--time`（不限/一天内/一周内/半年内）。

**第 3 步**

```bash
python scripts/xhs_client.py detail "<feed_id>" "<xsec_token>" --comments --json
```

**第 4 步**

查看笔记内容、互动数据（点赞、收藏、评论）与评论情感倾向。

## 工作流：发布内容

```
进度：
- [ ] 第 1 步：验证连接
- [ ] 第 2 步：准备素材
- [ ] 第 3 步：向用户展示预览并获取逐次授权
- [ ] 第 4 步：发起发布（受客户端护栏保护）
- [ ] 第 5 步：验证上线
```

**第 1 步**

```bash
python scripts/xhs_client.py status
```

**第 2 步**

准备标题（建议 ≤ 20 字）、正文、可公开访问的图片 URL、可选标签。

**第 3 步 — 代理必须执行的强制预览**

调用 `publish` 前，代理必须向用户打印结构化预览并等待用户在对话中回复明确授权词：

```
📋 发布预览
────────────
账号：<status 返回的账号>
标题：<title>
正文：<content 全文>
图片：<逐行 URL>
标签：<tags>
────────────
请回复“确认发布”以继续；任何其他回复视为取消。
```

模糊回复、沉默、或"以后都可以发"等概括授权**一律视为未授权**。

**第 4 步 — 发起发布**

仅在收到用户授权后执行：

```bash
python scripts/xhs_client.py publish "标题" "正文" "https://img1.jpg,https://img2.jpg" --tags "标签1,标签2"
```

客户端会再对第 3 步的授权做机械验证（TTY 二次确认或 `--yes` + 专用账号声明）。

**第 5 步**

```bash
python scripts/xhs_client.py search "标题" --sort "最新"
```

## 注意事项

- **频率控制**：请适当控制请求间隔。
- **维护脚本**：`scripts/publish.sh` 仅用于把本 Skill 包发布到 ClawHub 市场，与"在小红书发布笔记"无关，终端用户无需运行。
