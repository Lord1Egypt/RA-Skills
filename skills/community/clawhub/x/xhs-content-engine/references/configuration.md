# 小红书内容引擎配置说明

本文档用于配置 `xhs-content-engine` 的拆解、生成和视频生成能力，也说明如果要替换小红书爬虫，应该替换哪一层。

## 推荐结论

短期建议：继续把爬虫做成 HTTP 网关，默认使用 `https://agent.delu.cn`。

原因：
- skill 只负责内容工作流，不直接处理浏览器登录、Cookie、风控和反爬。
- agent.delu.cn、自建爬虫、内网爬虫都可以暴露同一套 HTTP 接口，skill 只改 `.env`。
- 直接在 skill 里用 Playwright/浏览器爬小红书，维护成本高，也更容易遇到登录态、验证码、IP、页面结构变化问题。

如果要换爬虫，优先做一个自建 crawler gateway，让它兼容本文档里的接口契约，再通过 `AGENT_DELU_*` 环境变量切过去。

## 配置文件位置

配置按以下优先级读取，前面的会覆盖后面的：

1. 当前 shell 环境变量
2. 当前运行目录的 `.env`
3. `~/.config/content-engine/.env`
4. skill 根目录的 `.env`

推荐长期配置写到：

```bash
mkdir -p ~/.config/content-engine
touch ~/.config/content-engine/.env
```

不要把真实 key 写入仓库、公开压缩包或聊天记录。

## 最小配置

只跑 v1 拆解：

```bash
AGENT_DELU_BASE_URL=https://agent.delu.cn
# 如接口需要认证再加：
AGENT_DELU_API_TOKEN=你的_agent_delu_token
```

跑 v2 生成文案/图片：

```bash
OFOX_API_KEY=ofox-你的_key
```

跑 v0.3.0+ Seedance 真视频：

```bash
ARK_API_KEY=你的_ark_key
```

完整示例：

```bash
cat >> ~/.config/content-engine/.env <<'EOF'
AGENT_DELU_BASE_URL=https://agent.delu.cn
AGENT_DELU_API_TOKEN=你的_agent_delu_token

OFOX_API_KEY=ofox-你的_key
OFOX_LLM_MODEL=claude-sonnet-4-6
OFOX_IMAGE_MODEL=nanobanana-pro

ARK_API_KEY=你的_ark_key
ARK_VIDEO_MODEL=doubao-seedance-2-0-260128
EOF
```

## agent.delu.cn / crawler gateway 配置

| 变量 | 默认值 | 说明 |
|---|---|---|
| `AGENT_DELU_BASE_URL` | `https://agent.delu.cn` | 爬虫网关域名 |
| `AGENT_DELU_API_TOKEN` / `AGENT_DELU_TOKEN` | 空 | 网关认证 token |
| `AGENT_DELU_AUTH_HEADER` | `Authorization` | 认证 header 名 |
| `AGENT_DELU_AUTH_SCHEME` | `Bearer` | token 前缀；设为 `raw` 时直接发送 token |
| `AGENT_DELU_USER_AGENT` | `curl/8.7.1` | 请求 User-Agent |
| `AGENT_DELU_METHOD` | `GET` | 全局请求方法，可设 `POST` |
| `AGENT_DELU_NOTE_METHOD` | 继承 `AGENT_DELU_METHOD`，默认 `GET` | 笔记详情接口方法 |
| `AGENT_DELU_COMMENT_METHOD` | 继承 `AGENT_DELU_METHOD`，默认 `GET` | 评论接口方法 |
| `AGENT_DELU_NOTE_PATH` | `/api/v1/xiaohongshu/app/get_note_info` | 笔记详情接口路径 |
| `AGENT_DELU_COMMENT_PATHS` | `/api/v1/xiaohongshu/app/get_note_comments,/api/v1/xiaohongshu/web/get_note_comments` | 评论接口候选，逗号分隔 |
| `AGENT_DELU_NOTE_ID_PARAM` | `note_id` | note id 参数名 |

GET 模式会把 note id 放到 query string：

```text
GET {AGENT_DELU_BASE_URL}{AGENT_DELU_NOTE_PATH}?{AGENT_DELU_NOTE_ID_PARAM}=<note_id>
GET {AGENT_DELU_BASE_URL}{comment_path}?{AGENT_DELU_NOTE_ID_PARAM}=<note_id>
```

POST 模式会发送 JSON body：

```json
{"note_id":"<note_id>"}
```

## 自建爬虫网关契约

如果不用 agent.delu.cn，建议自建一个 HTTP 服务，尽量保持以下行为：

- 输入：24 位小红书 note id
- 输出：JSON
- 鉴权：普通 header token
- 错误：401/403 表示认证失败，429 表示限流，5xx 表示网关或上游失败
- 不在响应里返回 token、cookie 或账号敏感信息

笔记详情响应可以是以下任一形状，parser 都能识别：

```json
{"note": {"type": "video", "title": "...", "desc": "..."}}
```

```json
{"data": {"note": {"type": "normal", "title": "...", "desc": "...", "images": []}}}
```

```json
{"data": {"data": [{"note_list": [{"type": "video", "title": "..."}]}]}}
```

笔记对象建议包含：

| 字段 | 说明 |
|---|---|
| `type` / `note_type` | `video` 或 `normal` |
| `title` / `display_title` | 标题 |
| `desc` / `description` / `content` | 发布正文 |
| `video.url` / `video_url` | 视频 URL，视频笔记需要 |
| `images` / `image_list` / `images_list` | 图片 URL 列表，图文笔记需要 |
| `interact_info` / `stats` | 点赞、收藏、评论、分享等 |
| `user` / `author` / `user_info` | 作者信息 |
| `hash_tag` / `tags` / `tag_list` | 话题标签 |
| `time` / `publish_time` / `create_time` | 发布时间 |

评论响应可以是：

```json
{"comments": [{"content": "怎么买", "like_count": 3}]}
```

也可以放在 `data.comments`、`data.comment_list`、`items`、`list` 等常见字段里。评论对象建议包含：

| 字段 | 说明 |
|---|---|
| `content` / `text` | 评论原文 |
| `like_count` / `likes` | 评论点赞数 |
| `user` / `author` | 评论用户信息 |
| `time` / `create_time` | 评论时间 |

## 常见配置场景

### 1. 默认 agent.delu.cn，无 token

适合内网 allowlist 或网关不要求鉴权：

```bash
AGENT_DELU_BASE_URL=https://agent.delu.cn
```

### 2. agent.delu.cn，Bearer token

```bash
AGENT_DELU_BASE_URL=https://agent.delu.cn
AGENT_DELU_API_TOKEN=你的_token
AGENT_DELU_AUTH_HEADER=Authorization
AGENT_DELU_AUTH_SCHEME=Bearer
```

### 3. 自建网关，POST JSON

```bash
AGENT_DELU_BASE_URL=https://crawler.example.com
AGENT_DELU_METHOD=POST
AGENT_DELU_NOTE_PATH=/xhs/note
AGENT_DELU_COMMENT_PATHS=/xhs/comments
AGENT_DELU_NOTE_ID_PARAM=note_id
AGENT_DELU_API_TOKEN=你的_internal_token
```

### 4. 自建网关，自定义 header

```bash
AGENT_DELU_BASE_URL=https://crawler.internal
AGENT_DELU_AUTH_HEADER=X-API-Key
AGENT_DELU_AUTH_SCHEME=raw
AGENT_DELU_API_TOKEN=你的_internal_token
```

### 5. 只生成脚本/文案，不真生成视频

```bash
OFOX_API_KEY=ofox-你的_key
```

运行时加 `--no-real-video`：

```bash
python3 scripts/generate_xhs.py "<XHS link>" --type video --count 1 --no-real-video
```

## 验证命令

只检查环境：

```bash
python3 scripts/extract_xhs.py --check
python3 scripts/generate_xhs.py --check
```

只解析链接，不调 API：

```bash
python3 scripts/extract_xhs.py --dry-run "<XHS link or note_id>"
```

跳过评论或媒体下载，方便排查：

```bash
python3 scripts/extract_xhs.py "<XHS link>" --no-comments
python3 scripts/extract_xhs.py "<XHS link>" --no-video
python3 scripts/extract_xhs.py "<XHS link>" --no-images
```

指定工作区：

```bash
python3 scripts/extract_xhs.py "<XHS link>" --out ~/xhs-workspace/demo
```

## 是否要改成其他爬虫方式

推荐优先级：

1. **保留 HTTP gateway 模式，换网关实现**：最推荐。让自建爬虫服务兼容上面的接口契约，skill 无需改代码或只改 `.env`。
2. **在 skill 中新增 provider 抽象**：适合未来同时维护多个 provider。可以加 `XHS_CRAWLER_PROVIDER=agent_delu|generic_http|mock`，但当前配置能力已经覆盖大多数替换场景。
3. **直接在 skill 里跑 Playwright/浏览器爬虫**：不推荐作为默认。它依赖登录态、浏览器环境和页面结构，出错面更大，也不适合公开分发。
4. **手工导入 JSON**：适合作为兜底。后续可以加 `--note-json` / `--comments-json` 参数，让没有爬虫权限的用户把已有数据导入工作区。

如果只是从 agent.delu.cn 切到你的自建接口，优先做第 1 种，不需要重写 crawler。

