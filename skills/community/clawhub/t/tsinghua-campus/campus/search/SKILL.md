---
name: campus-search
description: 校园信息多源搜索。在清华校园站点（info 信息门户 / its 信息化服务 / learn 网络学堂）搜索通知、服务说明、课件等，结果带来源。当用户需要"搜索校园信息、找通知、查服务指南、检索课件"时使用。
metadata:
  openclaw:
    os:
      - windows
      - macos
      - linux
---

# 校园信息多源搜索

在多个清华校园站点搜索，返回统一结果（每条带 source 来源），供用户判断优先级。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：结果必须带 source**。AI 汇报时说明每条来自哪个站点。
- **铁律 4：不硬编码**。关键词由用户提供，不写死。

### 使用

```
search.py --query <关键词> --source all --limit 5
```

- `--source`: `info` / `its` / `learn` / `all`（默认 all）
- `--limit`: 每源返回条数（默认 5）

### 各源说明

| source | 站点 | 内容 | 登录要求 |
|--------|------|------|---------|
| info | info.tsinghua.edu.cn | 信息门户通知/公告/应用 | 校园网直连；站内全文搜索需登录 |
| its | its.tsinghua.edu.cn | 信息化服务指南（网络/邮箱/VPN/账号） | 搜索接口需登录态（复用 base-cas CDP） |
| learn | learn.tsinghua.edu.cn | 网络学堂课件/公告 | 需 base-cas learn 会话 |

### 工作流

```
用户: 帮我搜一下"奖学金"相关通知
AI:
  1. 若 base-cas 浏览器未运行 → login.py --system learn --ensure（建立登录态）
  2. search.py --query 奖学金 --source all
  3. 读 JSON results，按 source 分组汇报（标题 + 来源 + 链接）
```

### 边界

- 搜索结果可能为空（该站无匹配 / 本机环境被 webvpn 拦截）→ 如实说明，不编造
- info 站内全文搜索接口在 webvpn 代理下会失效（JS 被替换）→ 校园网直连正常，AI 需区分环境

---

## 如果你是用户，请阅读以下内容

对 AI 说："帮我搜一下 XX 相关的内容"（通知/服务/课件均可）。

AI 会在清华各站点搜索，告诉你找到什么、来自哪个网站。
