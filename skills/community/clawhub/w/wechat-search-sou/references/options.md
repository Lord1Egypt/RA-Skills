# 微信搜一搜实时搜索 (Wechat Search & Analysis) 完整选项参数说明

## 微信文章搜索

| 参数            | 缩写 | 作用       | 可选值                                      | 必填 | 默认值 |
| --------------- | ---- | ---------- | ------------------------------------------- | ---- | ------ |
| `--keyword`     | `-K` | 搜索关键词 | 2-50 位长度的汉字或单词                     | 是   | 无     |
| `--sort`        | `-S` | 排序       | 0=综合 / 1=最新 / 2=最热                    | 否   | 0      |
| `--publishTime` | `-P` | 发布时间   | 0=不限 / 1=最近1天 / 2=最近7天 / 3=最近半年 | 否   | 0      |
| `--limit`       | `-L` | 返回数量   | 1-10000                                     | 否   | 10     |

```bash
# **基础语法**
node scripts/wechat/article-cli.js --keyword <关键词> --sort <排序>  --publishTime <发布时间> --limit <返回数量>

# **使用示例**

# 搜索"AI"的微信文章
node scripts/wechat/article-cli.js --keyword AI

# 搜索"AI"的热门微信文章
node scripts/wechat/article-cli.js --keyword AI --sort 2

# 搜索"AI"的最近1天发布的微信文章
node scripts/wechat/article-cli.js --keyword AI --publishTime 1
```

## 微信视频搜索

| 参数         | 缩写 | 作用       | 可选值                                           | 必填 | 默认值 |
| ------------ | ---- | ---------- | ------------------------------------------------ | ---- | ------ |
| `--keyword`  | `-K` | 搜索关键词 | 2-50 位长度的汉字或单词                          | 是   | 无     |
| `--sort`     | `-S` | 排序       | 0=综合 / 1=最新 / 2=最热                         | 否   | 0      |
| `--duration` | `-D` | 视频时长   | 0=不限 / 1=5分钟以下 / 2=5-20分钟 / 3=20分钟以上 | 否   | 0      |
| `--limit`    | `-L` | 返回数量   | 1-10000                                          | 否   | 10     |

```bash
# **基础语法**
node scripts/wechat/article-cli.js --keyword <关键词> --sort <排序>  --duration <视频时长> --limit <返回数量>

# **使用示例**

# 搜索"AI"的微信视频
node scripts/wechat/video-cli.js --keyword AI

#搜索"AI"的最新微信视频
node scripts/wechat/video-cli.js --keyword AI --sort 1

#搜索长度在5-20分钟的"AI"的微信视频
node scripts/wechat/video-cli.js --keyword AI --sort 2 --duration 2
```
