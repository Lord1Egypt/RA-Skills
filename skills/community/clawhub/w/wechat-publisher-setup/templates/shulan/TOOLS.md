# 可用工具与环境配置

## 通用工具
- 文件读写：Read / Write / Edit（读取和编辑 workspace 内的文件）
- 网络搜索：Web Search（搜索行业数据、运营方法论）

## 微信公众平台 API 工具（核心）

通过 `wechat_publish.cjs` 脚本调用微信官方 API，配置文件位于 `~/.openclaw/workspace-wechat-publisher/.env`。
仅依赖 Node.js 内置模块，跨平台可用（Windows/macOS/Linux）。

### 可用命令
| 命令 | 用途 | 示例 |
|------|------|------|
| `node wechat_publish.cjs token` | 获取/刷新 access_token | 验证 API 连通性 |
| `node wechat_publish.cjs upload-thumb <图片>` | 上传封面图 → media_id | 发布前上传封面 |
| `node wechat_publish.cjs upload-image <图片>` | 上传正文图片 → URL | 正文配图上传 |
| `node wechat_publish.cjs create-draft <JSON>` | 创建草稿 → media_id | 提交文章到草稿箱 |
| `node wechat_publish.cjs publish <media_id>` | 发布草稿 | 用户确认后执行 |
| `node wechat_publish.cjs get-status <publish_id>` | 查询发布状态 | 确认是否发布成功 |
| `node wechat_publish.cjs get-stats <开始> <结束>` | 图文数据统计 | 拉取阅读/分享数据 |

### API 权限说明
- **认证服务号**：所有接口可用
- **认证订阅号**：草稿/发布接口可用，部分数据接口受限
- **未认证账号**：大部分接口不可用，建议先完成微信认证

### API 限频
- access_token 有效期 7200 秒，脚本自动缓存
- 素材上传：每日限 5000 次
- 草稿创建：无明确限频
- 数据接口：每日限 500 次

## 角色专用工具
- 新榜（Newrank）数据：行业对标数据、竞品分析、内容评分
- 数据可视化工具：图表生成，将数据转化为直观的可视化呈现

## 外部服务（可选配置）
- 西瓜数据：公众号数据分析和排名
- 清博大数据：新媒体传播分析
- 表格工具：Excel / Google Sheets（数据整理和计算）

## 安全约束
- **发布操作必须获得用户明确确认**，不可自动发布
- API 凭证存储在 `.env` 文件中，权限 600，不可泄露
- 不将 AppID/AppSecret 写入任何 Agent 的 workspace .md 文件
- 不访问未授权的外部服务
- 数据报告中不包含用户隐私数据（如具体用户 ID、地理位置等）
