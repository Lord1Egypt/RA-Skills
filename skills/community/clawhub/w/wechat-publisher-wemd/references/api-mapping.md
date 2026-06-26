# WeChat Publisher: API mapping

## 能力域

| 能力域 | 作用 |
|--------|------|
| 素材管理 | 封面上传、图文内图片上传、永久素材查询/删除 |
| 草稿管理 | 创建/更新/获取/列出/删除草稿 |
| 发布能力 | 提交发布、查询状态、列出/获取/删除已发布文章 |

## 渲染引擎

使用 [WeMD](https://github.com/tenngoxars/WeMD)，通过 `vendor/wemd/render.js` 调用。

首次使用时 `setup.py` 自动执行 `npm install` 安装依赖。

每个主题完整 CSS = `_base.css` + 主题覆盖层 + `_code-github.css`

## 接口映射

### 素材管理

| 操作 | client 函数 | 接口路径 |
|------|-------------|---------|
| 上传永久素材 | `upload_permanent_material()` | `POST /cgi-bin/material/add_material` |
| 上传图文消息内图片 | `upload_article_image()` | `POST /cgi-bin/media/uploadimg` |
| 获取/删除/列出/统计永久素材 | `get/delete/list_materials/get_material_count()` | 对应接口 |

### 草稿管理

| 操作 | client 函数 | 接口路径 |
|------|-------------|---------|
| 新增/更新/获取/列出/统计/删除草稿 | `add/update/get/list/count/delete_draft()` | 对应 `/cgi-bin/draft/*` |

### 发布能力

| 操作 | client 函数 | 接口路径 |
|------|-------------|---------|
| 提交/查询/列出/获取/删除 | `submit_publish/query_publish_status/list_published/get_published_article/delete_published_article()` | 对应 `/cgi-bin/freepublish/*` |

## 常见错误码

| 错误码 | 含义 |
|--------|------|
| `40137` | 图片格式不合规 |
| `40164` | IP 不在白名单 |
| `45166` | 正文内容违规 |
| `48001` | 接口未授权 |
