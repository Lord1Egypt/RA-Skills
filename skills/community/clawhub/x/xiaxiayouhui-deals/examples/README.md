# 调用样例集

本目录提供 4 大场景的真实调用样例，含 curl 命令、JSON 返回、AI 渲染输出三段式对照。

> BaseURL = `https://xiaxiayouhui.xyz`

## 文件清单

| 文件 | 场景 | 适用问题 |
|---|---|---|
| `01-compare.md` | 跨平台比价 | "iPhone 17 哪里便宜" |
| `02-parse-link.md` | 链接 / 口令解析 | 用户粘贴拼多多/京东商品链接 |
| `03-daily-deals.md` | 今日好价 | "今天有什么数码好价" |
| `04-local.md` | 本地生活神券 | "美团有什么外卖券" |

## 联调测试脚本

```bash
# 一键 smoke test 所有 endpoint
BASE=https://xiaxiayouhui.xyz
echo "==== compare ===="     && curl -s "$BASE/api/skill/v1/compare?q=iPhone+17&limit=3"     | head -c 500
echo "==== coupon ===="      && curl -s "$BASE/api/skill/v1/coupon?q=扫地机器人&platform=pdd&limit=3" | head -c 500
echo "==== parse-link ===="  && curl -s "$BASE/api/skill/v1/parse-link?url=https%3A%2F%2Fmobile.yangkeduo.com%2Fgoods.html%3Fgoods_id%3D123" | head -c 500
echo "==== daily-deals ====" && curl -s "$BASE/api/skill/v1/daily-deals?cat=digital&limit=3" | head -c 500
echo "==== local ===="       && curl -s "$BASE/api/skill/v1/local?cat=waimai&city=shenzhen&limit=3" | head -c 500
echo "==== health ===="      && curl -s "$BASE/api/skill/v1/health"
```
