---
name: shopmind-price-compare
description: 全网比价助手，支持淘宝/天猫、京东、拼多多、抖音、快手、苏宁、唯品会、考拉、1688 十大平台实时比价。含优惠券筛选、热门爆品、省钱计算、购买链接。用户想购物、比价、找优惠券、看热销榜时使用。
homepage: https://clawhub.com/skills/shopmind-price-compare
metadata:
  {
    "openclaw":
      {
        "emoji": "🛒",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {"id": "uv-brew", "kind": "brew", "formula": "uv", "bins": ["uv"], "label": "Install uv (brew)"},
            {"id": "uv-pip", "kind": "pip", "formula": "uv", "bins": ["uv"], "label": "Install uv (pip)"},
          ],
      },
  }
---

# ShopMind 全网比价 v2.1.0

十大电��平台实时比价，开箱即用，无需部署后端。

## 支持平台

0:全部 1:淘宝/天猫 2:京东 3:拼多多 4:苏宁 5:唯品会 6:考拉 7:抖音 8:快手 10:1688

## 搜索比价

```shell
uv run scripts/main.py search --keyword='{keyword}'
uv run scripts/main.py search --keyword='{keyword}' --source=2
uv run scripts/main.py search --keyword='{keyword}' --sort=sales
uv run scripts/main.py search --keyword='{keyword}' --coupon=1
uv run scripts/main.py search --keyword='{keyword}' --min_price=50 --max_price=200
uv run scripts/main.py search --keyword='{keyword}' --page=2
```

排序选项 (--sort): price(价格↑) | price_desc(价格↓) | sales(销量) | discount(折扣) | commission(佣金)

## 商品详情+购买链接

```shell
uv run scripts/main.py detail --source={source} --id={goodsId}
```

返回：商品标题、价格、券后价、省钱金额、购买链接、淘口令

## 优惠券精选

```shell
uv run scripts/main.py coupons --keyword='{keyword}'
uv run scripts/main.py coupons --keyword='{keyword}' --source=1
```

## 热门爆品

```shell
uv run scripts/main.py hot
uv run scripts/main.py hot --source=2
```

## 关于脚本

本技能脚本不读写本地文件，仅请求第三方 maishou88.com 获取商品和价格数据。
