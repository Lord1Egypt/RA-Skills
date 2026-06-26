# 样例 03 · 今日好价

## 用户问

> "今天有什么数码好价？"

## AI 调用

```bash
curl -s "https://xiaxiayouhui.xyz/api/skill/v1/daily-deals?cat=digital&platform=all&limit=10"
```

## 服务端返回（mock）

```json
{
  "success": true,
  "cat": "digital",
  "platform": "all",
  "data": [
    {
      "platform": "jd",
      "goods_name": "小米 14 Ultra 16+512 雪山粉",
      "coupon_price": 6299.0,
      "coupon_amount": 800.0,
      "history_low": true,
      "discount_pct": 18,
      "promotion_url": "https://xiaxiayouhui.xyz/go/jd_xm14u",
      "third_party": false
    },
    {
      "platform": "pdd",
      "goods_name": "AirPods 4 主动降噪版",
      "coupon_price": 1099.0,
      "coupon_amount": 200.0,
      "history_low": false,
      "discount_pct": 15,
      "promotion_url": "https://xiaxiayouhui.xyz/go/pdd_ap4",
      "third_party": false
    },
    {
      "platform": "sn",
      "goods_name": "索尼 WH-1000XM5 无线降噪耳机",
      "coupon_price": 1999.0,
      "coupon_amount": 300.0,
      "history_low": false,
      "discount_pct": 32,
      "promotion_url": "https://xiaxiayouhui.xyz/go/sn_xm5",
      "third_party": false
    }
  ],
  "total": 3,
  "version": "1.1.0"
}
```

## AI 渲染输出

> 📅 **今日数码好价**（数据时效：30 分钟内 · 共 3 件 · 已按券后价由低到高排序）
>
> | # | 商品 | 平台 | 券后价 | 券 | 状态 | 操作 |
> |---|------|------|--------|------|------|------|
> | 1 | 小米 14 Ultra 16+512 雪山粉 | 京东 | **¥6299** | -¥800 | 🆕 新史低 | [领券购买](https://xiaxiayouhui.xyz/go/jd_xm14u) |
> | 2 | AirPods 4 主动降噪版 | 拼多多 | ¥1099 | -¥200 | 🟰 平史低 | [领券购买](https://xiaxiayouhui.xyz/go/pdd_ap4) |
> | 3 | 索尼 WH-1000XM5 无线降噪耳机 | 苏宁 | ¥1999 | -¥300 | 🔥 32% off | [领券购买](https://xiaxiayouhui.xyz/go/sn_xm5) |
>
> > 🆕 = 新史低 · 🟰 = 平史低 · 🔥 = 折扣力度大
> > 数据时效：30 分钟内（每 30 分钟刷新一次）

## 品类参数对照

| `cat` | 中文 | 典型商品 |
|---|---|---|
| `all` | 全部 | 所有品类混合排行 |
| `digital` | 数码 | 手机 / 电脑 / 耳机 / 相机 |
| `beauty` | 美妆 | 面膜 / 香水 / 彩妆 |
| `fashion` | 服饰 | 女装 / 男装 / 鞋包 |
| `home` | 家居 | 床品 / 厨具 / 收纳 |
| `food` | 食品 | 零食 / 生鲜 / 酒水 |
| `baby` | 母婴 | 奶粉 / 纸尿裤 / 玩具 |
| `sport` | 运动 | 跑鞋 / 健身器材 / 户外 |
| `book` | 图书 | 教辅 / 文学 / 童书 |
