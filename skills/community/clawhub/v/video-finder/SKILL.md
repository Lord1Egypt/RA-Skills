---                                 
name: video_finder
license: MIT
spdx: MIT
description: 帮助用户搜索、筛选并下载成人影片。支持 yt-dlp 下载、偏好记忆、代理配置、进度监控和反馈闭环。触发：找片、搜片、下片、下载视频、JAV、Pornhub 等

trigger_keywords:                   
  - 找片
  - 搜片
  - 来片
  - 来个片
  - 有没有片
  - 推荐片子
  - 涩片
  - 黄片
  - 毛片
  - AV
  - porn
  - xxx
  - amateur
  - homemade
  - sex tape
  - 🔞
  - NSFW

version: 2.0
author: Lingling && xiaoka520
---  

# video-finder — 找片下载技能

搜索、筛选并下载成人影片。

## 前置条件

- **称呼约定**：`{{{user}}}` 为占位符，实际对话时根据上下文自然称呼
- `yt-dlp` 安装在宿主机
- **工作目录**：skill 所在目录（相对路径，所有 JSON/MD 文件都在此目录下）
- **偏好配置**：`./preferences.json`（首次从 `preferences.example.json` 复制）
- **代理配置**：`./proxy.json`（首次从 `proxy.example.json` 复制）
- **下载跟踪**：`./tracking/downloads.json`（首次从 `tracking/downloads.example.json` 复制）
- **记忆文件**：`./history.md`（首次从 `history.example.md` 复制）
- **下载目录**：无默认值，由用户指定或自动探测
- **默认工作空间**：`./workspace`（最终回退目录）

## 子技能

| 技能 | 文件 | 职责 |
|------|------|------|
| 偏好管理 | `preferences.md` | 偏好初始化、修改、标签维护 |
| 代理探测 | `proxy.md` | 网络可达性探测、代理配置 |
| 搜索 | `search.md` | 多引擎搜索、自动筛选、结果展示 |
| 下载 | `download.md` | 目录确定、yt-dlp 下载、进度跟踪、清理 |
| 反馈闭环 | `feedback.md` | 观后反馈、正负面标签提炼 |

## 完整工作流程

### Phase 0: 代理探测

委托给 `video_finder_proxy`：每次访问站点前探测可达性。

### Phase 1: 接收任务

```
收到请求
├─ 检查 preferences.json（首次→委托 video_finder_preferences 初始化）
├─ 检查 proxy.json（首次→跳过，不通时委托 video_finder_proxy 初始化）
│
├─ 用户给关键词 → 走 Phase 2 搜索
├─ 用户给链接 → 走 Phase 3 下载
└─ 用户说"改偏好" → 委托 video_finder_preferences 覆盖配置
```

### Phase 2: 搜索

委托给 `video_finder_search`：
1. 探测目标站点可达性（→ video_finder_proxy）
2. 多搜索引擎查询
3. 获取页面内容（web_fetch / browser）
4. 基于 preferences.json 自动筛选
5. 展示结果供用户选择

→ 用户选定 → Phase 3  
→ 用户不满意 → 换关键词重新搜

### Phase 3: 下载

委托给 `video_finder_download`：
1. 确定下载目录（preferences → 自动沿用上次 → 首次询问 → 探测 → 回退）
2. 代理判断（→ video_finder_proxy）
3. 启动 yt-dlp（文件跟踪法，支持跨 session）
4. 定时进度检测（动态 cron + 心跳 cron）
5. 完成后清理

### Phase 4: 结果

```
成功 ✅
→ 告知{{{user}}}：文件名、路径、文件大小
→ 追加记录到 history.md

失败 ❌
→ 告知原因：链接失效 / 画质不足 / 代理 Timeout / 站点被墙
→ 询问是否换源继续
```

### Phase 5: 反馈闭环

委托给 `video_finder_feedback`：
- 轻量提醒一次（不追问）
- 根据反馈更新 `tag_weights` / `author_weights` 权重
- 追加反馈记录到 history.md

## 🚫 红线

| 规则 | 说明 |
|---|---|
| **用户确认后才下载** | 不能替用户决定下载哪个，只能推荐 |
| 不主动整站翻页搜刮 | 用户给了方向才搜 |
| 不关注剧情标签 | 默认忽略剧情关键词（可在 preferences.json 配置 `plot_tags: true` 开启） |
| 下载目录动态确定 | preferences → 自动沿用上次 → 首次询问 → 探测 → 回退到 workspace |
| proxy.json 保密 | 不在对话/日志中输出密码 |
| 反馈闭环 | 看完后提醒一次（不追问），维护 tag_weights 加权标签 |

## ♻️ 用户随时可干预

```
"改下偏好"       → 委托 video_finder_preferences 覆盖 preferences.json
"换个代理"       → 委托 video_finder_proxy 覆盖 proxy.json
"这次不用代理"   → 不加 --proxy，不写文件
"记得这个代理"   → 写入 proxy.json 持久化
```
