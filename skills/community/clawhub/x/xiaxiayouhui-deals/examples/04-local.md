# 样例 04 · 本地生活神券

## 用户问

> "深圳有什么外卖券？"

## AI 调用

```bash
curl -s "https://xiaxiayouhui.xyz/api/skill/v1/local?cat=waimai&city=shenzhen&limit=10"
```

## 服务端返回（mock）

```json
{
  "success": true,
  "cat": "waimai",
  "city": "shenzhen",
  "data": [
    {
      "platform": "meituan",
      "act_id": "MT_WM_3012",
      "title": "美团外卖大额神券",
      "discount_desc": "满 30 减 12",
      "valid_until": "2026-05-25 23:59",
      "promotion_url": "https://xiaxiayouhui.xyz/go/local_mt3012",
      "third_party": false
    },
    {
      "platform": "eleme",
      "act_id": "ELE_RED_258",
      "title": "饿了么红包雨",
      "discount_desc": "满 25 减 8",
      "valid_until": "2026-05-26 23:59",
      "promotion_url": "https://xiaxiayouhui.xyz/go/local_ele258",
      "third_party": false
    },
    {
      "platform": "meituan",
      "act_id": "MT_MCD_99",
      "title": "麦当劳 1+1 随心配",
      "discount_desc": "9.9 元",
      "valid_until": "2026-05-30 23:59",
      "promotion_url": "https://xiaxiayouhui.xyz/go/local_mcd99",
      "third_party": false
    }
  ],
  "version": "1.1.0"
}
```

## AI 渲染输出

> 🍜 **深圳 · 外卖神券**（数据时效：30 分钟内）
>
> | 优惠 | 平台 | 力度 | 有效期 | 操作 |
> |------|------|------|--------|------|
> | 美团外卖大额神券 | 美团 | **满 30 减 12** | 至 5/25 23:59 | [领券购买](https://xiaxiayouhui.xyz/go/local_mt3012) |
> | 饿了么红包雨 | 饿了么 | 满 25 减 8 | 至 5/26 23:59 | [领券购买](https://xiaxiayouhui.xyz/go/local_ele258) |
> | 麦当劳 1+1 随心配 | 美团 | 9.9 元 | 至 5/30 | [领券购买](https://xiaxiayouhui.xyz/go/local_mcd99) |
>
> > 数据时效：30 分钟内 · 神券每天上午 10 点 / 下午 4 点更新
> > 点击"领券购买"会自动唤起 App，券会到你的账号里

## 品类参数对照

| `cat` | 中文 | 触发关键词 |
|---|---|---|
| `all` | 全部本地生活 | "本地生活"、"团购优惠" |
| `waimai` | 外卖 | "外卖券"、"美团券"、"饿了么"、"点外卖" |
| `movie` | 电影 | "电影票"、"看电影" |
| `hotel` | 酒店 | "酒店"、"旅游住宿" |
| `chuxing` | 打车 | "打车券"、"滴滴优惠" |
| `chadrink` | 茶饮 | "奶茶券"、"喜茶"、"瑞幸"、"咖啡券" |
| `meishi` | 美食团购 | "团购"、"火锅"、"美食优惠" |
