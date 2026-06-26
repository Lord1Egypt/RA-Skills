---
name: weibo-hot
description: "获取微博热搜榜单，按热度排序。无需 API Key。Use when: user asks about trending topics, hot news, social media trends in China."
homepage: https://v2.xxapi.cn
metadata: { "openclaw": { "emoji": "🔥", "requires": { "bins": ["curl", "jq"] } } }
---

# 微博热搜技能

获取实时微博热搜榜单，按热度排序。**无需 API Key**

## 使用方法

### 直接调用

```bash
./weibo_hot.sh
```

### 输出格式

每行一个热搜条目，格式为：`热度 | 标题`

```
1234567|某热门话题
987654|另一个热门话题
...
```

### 在脚本中使用

```bash
WEIBO_HOT=$(./weibo_hot.sh)

# 获取前 3 条
TOP3=$(echo "$WEIBO_HOT" | head -3)

# 获取第 4-10 条
NEXT7=$(echo "$WEIBO_HOT" | sed -n '4,10p')
```

## API 说明

- **接口**: https://v2.xxapi.cn/api/weibohot
- **认证**: 无需 API Key
- **返回**: JSON 格式，包含 data 数组
- **字段**: 
  - `title`: 热搜标题
  - `hot`: 热度值（数字）

## 注意事项

- 有 API 调用频率限制
- 建议缓存结果，避免频繁调用
- 需要安装 `curl` 和 `jq`
