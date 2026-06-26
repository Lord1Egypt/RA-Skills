---
name: wechat-publisher
description: 微信公众号发文自动化 skill。覆盖 Markdown 排版渲染（12 种内置主题 + 自定义主题）、正文图片上传、封面上传、草稿创建/更新/预览、人工确认发布、发布状态查询、素材/草稿/已发布文章查询。Use when agent needs to help write or publish 公众号文章, or for requests like "发公众号", "创建草稿", "更新草稿", "确认发布", "查询发布结果", "查素材", "查草稿列表", "查已发布文章", "添加主题", "切换主题", or "主题列表".
---

# WeChat Publisher

## 能力概览

覆盖公众号发文全链路：

**发文工作流**（主路径）：
1. 收集输入 → 询问用户选择排版主题
2. WeMD 渲染：Markdown / 纯文本 → 带主题样式的微信 HTML
3. 正文内本地图片自动上传并替换为微信 CDN URL
4. 封面素材自动上传
5. 创建或更新草稿 → 返回预览链接
6. 等待人工确认（不可跳过）
7. 提交发布 → 查询发布状态

**资产查询**（只读）：素材 / 草稿 / 已发布文章的列表与详情

**主题管理**：12 个内置主题 + 用户自定义主题（发送 CSS 即可添加）

**仅 client 封装**（高风险）：删除素材 / 草稿 / 已发布文章

**首次使用**：自动安装 Node.js 依赖（需要 Node.js v18+），后续跳过

---

## 核心规则

- 发布前必须有明确人工确认，拒绝任何隐含或沉默批准
- 不暴露凭据到用户侧输出
- 删除类操作默认不触发，需用户明确要求
- 只做发文相关链路，不扩展到菜单、群发、客服、统计等域
- 用户未指定主题时必须询问，不擅自选择

---

## 工作流

### 1. 收集输入

必填：
- `title`
- `author`
- `digest`（摘要）
- 正文：`content_markdown` / `content_markdown_path` / `content_text` / `content`
- 封面：`thumb_image_path`（本地图片）或 `thumb_media_id`（已上传素材）
- `theme`：排版主题（用户未指定时**必须询问**）

可选：
- `content_base_dir`：正文中相对路径图片的基准目录
- `draft_media_id` / `media_id`：更新已有草稿时必填
- `content_source_url` / `need_open_comment` / `only_fans_can_comment`

**主题选择规则：**
- 用户未指定主题时，向用户展示主题列表请用户选择
- 中文名或英文名都可以，脚本自动识别
- 用户说"默认"或不想选 → 使用默认主题

**内置主题（12 个）：**

| 中文名 | 英文 ID | 适合场景 |
|--------|---------|----------|
| 默认 | Default | 通用，微信绿现代风 |
| 学术论文 | Academic-Paper | 技术论文、研究报告 |
| 极光玻璃 | Aurora-Glass | 产品介绍、创意内容 |
| 包豪斯 | Bauhaus | 设计、艺术、创意 |
| 赛博朋克 | Cyberpunk-Neon | 科技、数码、AI |
| 知识库 | Knowledge-Base | 教程、说明文档 |
| 黑金奢华 | Luxury-Gold | 品牌文、深度文章 |
| 莫兰迪森林 | Morandi-Forest | 生活方式、慢阅读 |
| 新粗野主义 | Neo-Brutalism | 潮流、先锋、态度文 |
| 购物小票 | Receipt | 趣味内容、清单、复古 |
| 落日胶片 | Sunset-Film | 故事、散文、影评 |
| 主题模板 | Template | 基础排版参考 |

### 2. 归一化正文

由 `upsert_draft.py` 自动调用，无需手动执行。首次使用时自动安装 Node.js 依赖。

渲染引擎：[WeMD](https://github.com/tenngoxars/WeMD)

处理流程：
1. Markdown / 纯文本 → 经 WeMD 渲染为带内联样式的微信兼容 HTML
2. 本地图片自动上传到微信图文图片接口，替换为 CDN URL
3. 锚点链接自动转为脚注引用

### 3. 创建或更新草稿

```bash
python scripts/upsert_draft.py --input article.json
python scripts/upsert_draft.py --input article.json --update
```

草稿创建完成后向用户呈现：标题、摘要、主题、预览链接。

### 4. 等待人工确认

接受：确认发布 / 可以发布 / 批准发布

### 5. 提交发布

```bash
python scripts/submit_publish.py --draft-id <media_id> --confirmed
```

### 6. 查询发布状态

```bash
python scripts/query_publish_status.py --publish-id <publish_id>
```

### 7. 查询资产

```bash
python scripts/query_assets.py materials-count
python scripts/query_assets.py drafts-list [--no-content]
python scripts/query_assets.py published-list [--no-content]
```

### 8. 管理自定义主题

```bash
python scripts/manage_themes.py add --cn "清新蓝" --en "Fresh-Blue" --css-file /path/to/theme.css
python scripts/manage_themes.py list
python scripts/manage_themes.py delete --name "清新蓝"
```

**Agent 交互规则：**
1. 用户指定了中英文名 → 直接使用
2. 用户只给了中文名 → agent 生成英文 ID
3. 用户什么名字都没指定 → agent 根据 CSS 风格取名，**先问用户同意再保存**
4. CSS 必须以 `#wemd` 为根选择器

---

## 输入 JSON 样例

```json
{
  "title": "2026 AI 工具盘点",
  "author": "Bingo",
  "digest": "深度盘点。",
  "content_markdown_path": "/root/articles/ai-tools.md",
  "thumb_image_path": "/root/articles/cover.jpg",
  "theme": "黑金奢华"
}
```

---

## 输出格式规范

```
- 动作：创建草稿
- 主题：黑金奢华
- media_id：TnhkZ9HGMxOYETms_33Ct...
- 预览：http://mp.weixin.qq.com/s?...
- 下一步：请点击预览确认内容，确认后说"确认发布"
```

---

## 脚本索引

| 脚本 | 用途 |
|------|------|
| `setup.py` | 首次使用时自动安装 Node.js 依赖 |
| `normalize_article.py` | 正文归一化（WeMD 渲染 + 图片上传替换） |
| `upload_material.py` | 上传封面等永久素材 |
| `upsert_draft.py` | 创建/更新草稿 |
| `submit_publish.py` | 提交发布（需 `--confirmed`） |
| `query_publish_status.py` | 查询发布进度与结果 |
| `query_assets.py` | 只读查询：素材 / 草稿 / 已发布文章 |
| `manage_themes.py` | 主题管理：添加 / 列出 / 删除 |
| `wechat_client.py` | 底层接口封装 |

---

## 参考文档

- `references/api-mapping.md`：接口映射、渲染引擎详情
- `references/safety-rules.md`：确认门槛、凭据规范、能力边界
