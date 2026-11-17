---
name: tingdong-skill
description: |
  文章转 AI 播客。将公众号/知乎/任意网页链接转换为语音播客，AI 分析 + Edge-TTS 合成。
  触发词：转成播客、生成播客、文章转语音、朗读文章、听这篇文章、tingdong、听懂了。
  仅在用户明确请求音频/播客/语音版本时调用。
---

# 听懂了 (TingDong) - 文章转 AI 播客

把任意文章变成"为你量身定制"的知识音频。粘贴链接，AI 深度分析 + 语音合成，通勤/碎片时间"听懂"内容。

## 触发条件

**仅在用户明确请求以下场景时调用：**
- "把这篇文章转成播客" / "生成播客"
- "帮我读一下这篇文章" / "朗读文章"
- "听这篇文章" / "语音版" / "音频版"
- 用户发送链接并说 "tingdong" / "听懂了"

**不要**在普通聊天、搜索、总结等场景下自动触发。

## 核心能力

| 能力 | 说明 |
|------|------|
| 链接转播客 | 支持微信公众号、知乎、任意网页链接 |
| 三档风格 | 摘要版(3-5min) / 对话版(8-12min) / 深度版(15-20min) |
| 异步处理 | 提交后立即返回，后台生成完成后推送结果 |
| 缓存加速 | 同一链接+同风格二次提交秒回 |
| 多文章批量 | 同时处理多篇，生成播放列表 |

## 前置依赖

本 Skill 调用外部 REST API。默认使用公共服务，**也支持连接用户自部署的后端**。

### 使用默认服务（无需配置）
直接调用即可，无需本地安装。

**注意**：默认服务需要 API Token 认证。设置环境变量：
```bash
export TINGDONG_API_TOKEN="你的Token"
```

### 使用自定义后端（可选）
如需连接自己的服务器，设置环境变量：
```bash
export TINGDONG_API_URL="http://你的服务器:端口/api/v1"
export TINGDONG_API_TOKEN="你的Token"
```

自定义后端部署指南见 `references/api_docs.md`。

**后端服务**：`http://111.229.22.145:8092`（默认公共服务）

## 使用方式

### 1. 单篇文章转播客

**用户输入**：
> 把这篇文章转成播客：https://mp.weixin.qq.com/s/xxxxx

**Skill 处理**：
```bash
# 提交任务（异步）
curl -s -X POST http://111.229.22.145:8092/api/v1/podcast/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TINGDONG_API_TOKEN" \
  -d '{"content":"https://mp.weixin.qq.com/s/xxxxx","content_type":"url","style":"conversational","user_id":"user_001"}'

# 返回
{"task_id":"td_20260820_103528_d9ea7fd1","status":"pending","estimated_time":60}
```

**即时回复用户**：
> 👌 已收到《文章标题》
> 正在制作播客，预计 1-2 分钟...

**轮询结果**（每 5 秒，最多 5 分钟）：
```bash
curl -s -H "Authorization: Bearer $TINGDONG_API_TOKEN" \
  http://111.229.22.145:8092/api/v1/podcast/td_20260820_103528_d9ea7fd1
```

**完成后推送**：
> 🎵 播客已生成！《文章标题》
>
> 🔊 [点击收听](http://111.229.22.145:8092/tingdongle/audio/xxx.mp3)
> ⏱️ 约 8 分钟 | 📎 富兰克林读书俱乐部

### 2. 指定风格

| 用户说法 | style 参数 | 时长 |
|---------|-----------|------|
| "摘要版" / "精简版" / "短版" | `summary` | 3-5 分钟 |
| "深度解读" / "详细版" / "长版" | `deep_dive` | 15-20 分钟 |
| 默认 / 未指定 | `conversational` | 8-12 分钟 |

```bash
curl -s -X POST http://111.229.22.145:8092/api/v1/podcast/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TINGDONG_API_TOKEN" \
  -d '{"content":"https://...","style":"deep_dive","user_id":"user_001"}'
```

### 3. 批量处理

用户发送多个链接时，分别提交，用 batch API 批量查询进度：
```bash
# 批量查询（最多 20 个）
curl -s -X POST http://111.229.22.145:8092/api/v1/podcast/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TINGDONG_API_TOKEN" \
  -d '{"task_ids":["td_xxx","td_yyy"]}'
```

### 4. 本地脚本调用

```bash
# 基础用法（需先设置 TINGDONG_API_TOKEN）
python3 scripts/generate_podcast.py "https://mp.weixin.qq.com/s/xxxxx"

# 指定风格
python3 scripts/generate_podcast.py "https://zhuanlan.zhihu.com/p/xxxxx" --style deep_dive

# 只提交不等待
python3 scripts/generate_podcast.py "https://..." --no-wait
```

## 内容源支持

| 来源 | 识别特征 | 支持度 |
|------|---------|--------|
| 微信公众号 | `mp.weixin.qq.com` | ✅ 最佳（Playwright 反爬） |
| 知乎 | `zhihu.com` / `zhuanlan.zhihu.com` | ✅ 支持 |
| 普通网页 | `http://` / `https://` | ✅ 尝试抓取 |
| 纯文本输入 | 无 URL | ⚠️ 暂不支持，引导发链接 |

## 任务状态

| 状态 | 含义 |
|------|------|
| `pending` | 已提交，等待处理 |
| `fetching` | 正在抓取文章内容 |
| `analyzing` | AI 分析中 |
| `synthesizing` | 语音合成中 |
| `completed` | 完成，可获取音频 |
| `failed` | 失败，查看 error 字段 |

## 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| API 返回 500 / 超时 | 后端服务繁忙或磁盘满 | 稍后重试，或联系服务维护者 |
| "无法访问该链接" | 网站反爬或链接失效 | 让用户复制粘贴文章正文 |
| TTS 失败 "No audio was received" | Edge-TTS 服务端限流 | 重试，或稍后再次提交 |
| 处理超时（>5分钟） | 文章过长或网络慢 | 缩短文章或稍后重试 |
| 两次提交同一链接内容不同 | 同链接不同 style 会重新生成 | 正常行为，缓存按 `url+style` 隔离 |

## 隐私说明

- 文章内容发送至后端服务器进行 AI 分析和语音合成
- 音频文件暂存于服务器（`http://111.229.22.145:8092/tingdongle/audio/`）
- 不收集用户身份信息，仅通过 `user_id` 区分额度

## 资源

- **API 完整文档**: `references/api_docs.md`
- **内容源策略**: `references/content_sources.md`
- **后端部署指南**: 联系服务提供者或参考 API 文档自行部署
