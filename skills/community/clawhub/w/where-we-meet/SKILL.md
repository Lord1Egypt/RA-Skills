---
name: where-we-meet
description: WhereWeMeet / 约哪儿：多人聚会、约饭、聚餐、约会选址 skill。Use when the user asks “Where should we meet”“约哪儿”“找一个谁都不远的地方”“大家住得分散去哪吃/玩”“聚餐去哪”“约饭去哪”“第一个人在...第二个人在...第三个人住...”“A 在...B 在...C 在...”，并给出多人出发地、城市、餐饮/娱乐类型，如日料、重庆火锅、湘菜或者川菜。默认输出 5 个候选地点、各自通勤时间、附近同类店数量、移动端高德地图二维码/schemaUrl 和 PC HTML 对比页。
---

# WhereWeMeet（约哪儿）

## 执行

把用户请求整理成 JSON，运行：

```bash
node scripts/where-we-meet.js request.json
```

最小输入：

```json
{
  "city": "北京",
  "people": [
    { "name": "A", "address": "管庄地铁站" },
    { "name": "B", "address": "北苑路北地铁站" },
    { "name": "C", "address": "望京" }
  ],
  "poiKeywords": ["湘菜", "川菜"],
  "mode": "transit"
}
```

`poiKeyword` 仍兼容旧输入；多个品类必须用 `poiKeywords`。用户说“湘菜或者川菜”“川菜和湘菜都行”时，使用 OR 语义合并候选池，不要只跑第一个。

交通方式默认 `transit`。用户说“开车/打车/驾车/自驾/出租车”用 `driving`；说“步行/走路”用 `walking`。某个人交通方式不同，写到 `people[].mode`。

环境变量：

- `AMAP_KEY`：高德 Web 服务 Key，必需。
- `AMAP_JSAPI_KEY`：高德 JSAPI Web Key，可选；配置后 HTML 自动加载地图。
- `AMAP_SECURITY_JS_CODE`：高德 JSAPI 安全密钥，可选。

## 回复

运行后直接转发 stdout，默认输出已经是最终回复文本，不需要再解析、改写或重排。不要改用 `--json` 或 `--full`，除非用户明确要调试结构化结果。

默认 stdout 可能以一行 `MEDIA:<二维码PNG绝对路径>` 开头。OpenClaw/支持 `MEDIA:` 的平台会把这一行作为附件展示；不支持时，可以忽略这一行，正文里的 schemaUrl 仍可点击跳转高德地图。不要再额外用 message tool 或附件字段发送同一张二维码，否则会重复出现。

正文必须原样保留，不要自行重写候选结果。PC HTML 地址已经包含在正文中。

输出里必须保留：

- 本次交通方式口径。
- 每个候选地到每个人的时间。
- 代表店。
- “附近还有 N 家同类店”。
- 手机二维码或明确失败原因。
- PC HTML 文件地址或明确失败原因。

调试时可用：

```bash
node scripts/where-we-meet.js request.json --json
node scripts/where-we-meet.js request.json --full
```

## 规则

默认给 5 个候选地。不要主动设置 `regionLimit: 3`；只有用户明确说“只给 3 个/三个候选”时才减少数量。默认不设置店铺数硬门槛；只有用户明确说“多几家候选店”“成熟商圈”“不要单店”时，才设置 `minRegionShopCount`。

排序口径：

```text
1. 最大通勤时间更短
2. 通勤时间标准差更小
3. 平均通勤时间更短
4. 区域内同类店更多
5. 区域内评分更高
```

高德个人地图 marker 样式不可配置，所以移动端二维码地图只放候选地/代表店，不放 A/B/C/D 出发地。出发地距离放在文字摘要和 PC HTML 中。
