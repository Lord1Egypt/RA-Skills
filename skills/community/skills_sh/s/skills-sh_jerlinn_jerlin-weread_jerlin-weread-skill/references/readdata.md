# readdata

`weread.sh readdata -h`

## 语义陷阱

- `totalReadTime` 单位是秒，展示时转为「X 小时 Y 分钟」
- `dayAverageReadTime` 分母是周期已过去的自然日数，不是 readDays；阅读日均须 totalReadTime / readDays 另算
- `preferTime` 从 6 点开始到次日 5 点，不是 0 点
- `preferAuthor[].readTime` 是格式化字符串（如「5 小时 30 分钟」），不是秒数
- 统计总时长用 `totalReadTime`，不是 `readTimes` 分桶累加

## readTimes 分桶粒度

`readTimes` 是明细展示用（时间分布图），key 为分桶起始时间戳，value 为秒。粒度随 mode 变化：weekly/monthly 按天，annually 按月，overall 按年。

## 字段条件返回

部分字段仅在特定条件下出现，缺失时属正常行为：

| 字段 | 返回条件 |
|------|---------|
| compare | 当前周期且上一周期数据足够 |
| preferAuthor | 作者数据达到展示阈值 |
| preferPublisher | 至少 3 个出版社且最高本数达到阈值 |
| readRate / wrReadTime / wrListenTime | 总时长满 1 小时且文字阅读占比未过高 |
| rank | 仅当前周且未隐藏排行 |
| preferTimeWord | 总偏好时段数据满 10 小时 |
| dailyReadTimes | annually 模式可能返回 |

## mode 选择

mode 必须显式传，不传会报错（服务端不 fallback 默认值）。annually 只返回 baseTime 所在自然年。当前年份返回的是年初至今数据，不得标注为全年。

历史数据：目标周期内任一时间戳作为 baseTime。

## baseTime 归一化

weekly → 该周周一 00:00 | monthly → 1 日 00:00 | annually → 1 月 1 日 00:00 | overall → 0

## 任意日期区间组合

接口只支持固定自然周期，不支持任意起止日期。

规则：
1. 整年用 annually，整月用 monthly，减少调用次数
2. 跨年按自然年逐年查询累加，各年 baseTime 取该年内时间戳
3. 完整周期取 totalReadTime；不完整边界周期用 dailyReadTimes 日级扣减
4. 无日级明细时用月级近似，回答中标注口径
5. 回答标注：使用了哪些完整周期、是否日级扣减或月级近似

算法 trace —「2024-01-31 至今」：
- 查 2024 annually + 2025 annually + ... 至当前年，累加各年 totalReadTime
- 查 2024-01 monthly，从 2024 年总量中减去该月 totalReadTime → 得到 2024-02-01 至年底
- 若需精确保留 1 月 31 日：检查 2024 annually 是否返回 dailyReadTimes，有则只扣除 1 月 1-30 日的日级时长
- 无日级明细时，口径为「2024-02-01 至今」近似，需向用户说明
