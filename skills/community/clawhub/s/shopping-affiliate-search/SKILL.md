---
name: shopping-affiliate-search
version: 1.0.0
description: 全球购物搜索联盟工具 - 搜索淘宝/京东/亚马逊等平台商品，自动添加你的推荐码获取佣金。当用户想买东西、搜索商品、比价时自动激活。
user-invocable: true
metadata:
  openclaw:
    emoji: "🛒"
    category: "赚钱工具"
    tags: ["购物", "搜索", "联盟", "佣金", "赚钱"]
---

# 🛒 全球购物搜索联盟工具

一键搜索全球主流电商平台商品，自动注入推荐码，赚取佣金收入！

## ✨ 核心功能

| 平台 | 状态 | 佣金模式 |
|------|------|---------|
| 淘宝 | ✅ | 淘宝客 |
| 京东 | ✅ | 京粉 |
| 拼多多 | ✅ | 多多进宝 |
| 亚马逊 | ✅ | Amazon Associates |
| 1688 | ✅ | 阿里妈妈 |

## 💰 赚钱方式

```
用户搜索商品 → 返回带推荐码链接 → 用户购买 → 你获得佣金
```

**佣金比例**：
- 淘宝：1-50%
- 京东：1-30%
- 拼多多：5-50%
- 亚马逊：1-10%

## 🚀 使用方法

### 1. 配置推荐码

```bash
# 设置淘宝客PID
python3 scripts/config.py --taobao "mm_xxxxx"

# 设置京东联盟ID
python3 scripts/config.py --jd "xxxxx"

# 设置亚马逊联盟ID
python3 scripts/config.py --amazon "xxxxx-20"
```

### 2. 搜索商品

```bash
# 搜索淘宝
python3 scripts/search.py "男士T恤" --platform taobao

# 搜索京东
python3 scripts/search.py "iPhone手机壳" --platform jd

# 搜索亚马逊
python3 scripts/search.py "wireless earbuds" --platform amazon

# 全平台搜索
python3 scripts/search.py "蓝牙耳机" --all
```

### 3. 获取带佣金的链接

```bash
python3 scripts/get_link.py --url "商品链接" --platform taobao
```

## 📝 示例

```
用户: 帮我搜索淘宝上的男士T恤
Agent: 正在搜索淘宝...

搜索结果（已注入推荐码）：

1. 纯棉男士T恤夏季薄款
   价格: ¥59.00
   销量: 5万+
   推荐链接: https://s.click.taobao.com/xxx
   
2. 复古港风男士短袖T恤
   价格: ¥89.00
   销量: 3万+
   推荐链接: https://s.click.taobao.com/yyy
   
...

💰 预计佣金: ¥5-15/件
```

## 🔧 配置文件

```json
{
  "taobao": {
    "pid": "mm_xxxxx_xxxxx_xxxxx",
    "enabled": true
  },
  "jd": {
    "union_id": "xxxxx",
    "enabled": true
  },
  "pdd": {
    "pid": "xxxxx",
    "enabled": true
  },
  "amazon": {
    "associate_id": "xxxxx-20",
    "enabled": true
  }
}
```

## 🎯 最佳实践

1. **选择高佣金商品** - 优先推荐佣金比例高的商品
2. **热门商品** - 选择销量高的爆款
3. **多平台对比** - 给用户提供价格对比
4. **优质内容** - 配合推荐理由增加转化

## ⚠️ 注意事项

- 需要先注册各平台联盟账号
- 推荐码需要定期更新
- 遵守平台推广规则
- 真实推荐，不夸大宣传

## 📊 预期收入

| 使用频率 | 月收入预估 |
|---------|-----------|
| 偶尔使用 | ¥100-500 |
| 每日使用 | ¥500-2000 |
| 高频使用 | ¥2000-10000+ |

---

**开始赚钱：配置你的推荐码，搜索商品，分享链接！** 💰