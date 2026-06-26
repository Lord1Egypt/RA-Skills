# Tech News Daily Skill

**功能**: 每日科技资讯自动聚合、筛选、总结、推送至飞书

**触发**: 
- 每日 08:00 自动执行 (cron)
- 手动说 "生成日报"

## 信源配置

```json
{
  "rss": {
    "jiqizhixin": "https://www.jiqizhixin.com/feed",
    "geekpark": "https://www.geekpark.net/feed",
    "xin_zhiyuan": "https://www.leiphone.com/feed",
    "qclab": "https://qbit.ai/feed"
  },
  "api": {
    "github_trending": "https://api.github.com/search/repositories?q=created:>2026-03-28+language:Python",
    "baidu_hot": "https://top.baidu.com/board?tab=science"
  },
  "web": {
    "36kr": "https://www.36kr.com/hot-list-mot",
    "tmtp": "https://36kr.com/hot-list",
    "infoq": "https://www.infoq.cn/home"
  }
}
```

## 执行脚本

见 `scripts/fetch-daily.sh`

## 输出格式

飞书文本消息 + 图片摘要（可选）