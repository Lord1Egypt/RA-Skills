# 公众号内容发布自动化 - 用户工具配置

## 已配置的工具

### API Keys (需设置环境变量)

```bash
# MiniMax API - 主要图片生成
export MINIMAX_API_KEY="sk-cp-xxx"

# 腾讯云 - 腾讯文档/混元
export TENCENT_SECRET_ID="xxx"
export TENCENT_SECRET_KEY="xxx"
```

### 技能列表

| 技能名 | 版本 | 用途 |
|--------|------|------|
| illustrated-ppt | - | 图文并茂生成 |
| course-ppt-generator | 1.0.2 | 课程PPT |
| ai-ppt-generator | 1.1.5 | AI PPT助手 |
| hunyuan-image | 1.0.3 | 混元生图 |
| free-image-skill | 1.0.0 | 免费图片 |
| yaniw-wechat-publisher | 1.1.0 | 公众号发布 |
| wechat-article-crayon | 1.0.1 | 排版美化 |
| tavily-search | 1.0.0 | 网络搜索 |
| multi-search-engine | 2.1.3 | 多引擎搜索 |
| news-aggregator-skill | 0.1.0 | 资讯聚合 |

## 工作流配置

### 定时任务 (每日08:00)

```bash
# 编辑 crontab
crontab -e

# 添加
0 8 * * * cd /root/.openclaw/workspace/skills/wechat-content-pipeline && python3 scripts/run_pipeline.py --topic 深度学习 --count 8
```

### 腾讯文档配置

1. 获取 Folder Token
2. 配置权限
3. 设置中转路径

### 公众号配置

1. AppID: wx90d7cc689e706a15
2. 配置IP白名单
3. 设置草稿箱权限