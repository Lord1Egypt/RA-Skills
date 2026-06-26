---
name: xiaoka-food-log
description: "记录饮食、记录早餐、记录午餐、记录晚餐、记录加餐、今天吃了什么、今日饮食。当用户说这些关键词或描述吃了什么食物时，必须使用此skill调用API记录，禁止自行回复。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🥗",
        "requires": { "bins": ["curl", "jq"] },
      },
  }
---

# 小卡健康饮食记录

通过小卡健康API记录饮食并计算卡路里。**必须调用API，禁止自行估算或编造数据。**

## 凭证管理

API Key 存储在本地文件，**无需配置任何环境变量，无需重启**。

每次调用前先读取凭证：

```bash
XIAOKA_API="https://cal-cn.ishuohua.cn"
CRED="$HOME/.openclaw/workspace/skills/xiaoka-food-log/.credentials"
XIAOKA_API_KEY=$(cat "$CRED" 2>/dev/null || echo "")
```

如果 `XIAOKA_API_KEY` 为空，走绑定流程。

## 绑定流程（首次使用或凭证失效时）

**第一步**：获取配对码

```bash
XIAOKA_API="https://cal-cn.ishuohua.cn"
curl -s "$XIAOKA_API/openclaw/api/pair-code" | jq -r '.data.message'
```

**第二步**：告诉用户去**小卡健康 App → AI搭子**，发送：

```
绑定openclaw XXXXXX
```

（XXXXXX 替换为实际配对码）

**第三步**：用户把 App 的回复粘贴回来后，提取 `oc_` 开头的 API Key 并保存：

```bash
CRED="$HOME/.openclaw/workspace/skills/xiaoka-food-log/.credentials"
echo "oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > "$CRED"
chmod 600 "$CRED"
echo "绑定成功，已保存凭证。"
```

保存后立即生效，**无需重启**。

## 触发条件

以下任一情况必须使用此skill：
- 消息包含：记录饮食、记录早餐、记录午餐、记录晚餐、记录加餐
- 用户描述吃了什么（如"我吃了一碗面"、"刚喝了咖啡"）
- 用户问今天吃了什么 / 今日饮食

## 记录饮食

### 餐次判断

| 用户输入 | meal_type |
|---------|-----------|
| 记录早餐... | breakfast |
| 记录午餐... | lunch |
| 记录晚餐... | dinner |
| 记录加餐... | snack |
| 其他 | 不传，自动判断 |

### 调用

text 字段去掉"记录饮食/记录早餐"等前缀，只传食物描述。

```bash
XIAOKA_API="https://cal-cn.ishuohua.cn"
CRED="$HOME/.openclaw/workspace/skills/xiaoka-food-log/.credentials"
XIAOKA_API_KEY=$(cat "$CRED")
curl -s -X POST "$XIAOKA_API/openclaw/api/food/log" \
  -H "Authorization: Bearer $XIAOKA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "一碗米饭和红烧肉", "meal_type": "lunch"}' | jq .
```

### 展示结果

```
已记录午餐，共650卡 🥗

📋 食物明细：
  - 米饭 200g 232卡
  - 红烧肉 150g 418卡

💡 建议：蛋白质偏低，建议搭配豆制品
```

字段：`data.message`（主消息）、`data.ingredients[]`（明细）、`data.suggestion`（建议）

## 查看今日饮食

```bash
XIAOKA_API="https://cal-cn.ishuohua.cn"
CRED="$HOME/.openclaw/workspace/skills/xiaoka-food-log/.credentials"
XIAOKA_API_KEY=$(cat "$CRED")
curl -s "$XIAOKA_API/openclaw/api/food/today" \
  -H "Authorization: Bearer $XIAOKA_API_KEY" | jq .
```

## 错误处理

- **401**：凭证失效，删除凭证文件重新绑定：
  ```bash
  rm "$HOME/.openclaw/workspace/skills/xiaoka-food-log/.credentials"
  ```
- **403**：免费次数已用完，提示用户开通小卡健康会员
- **429**：超出每日上限（50次）
- **500**：稍后重试
