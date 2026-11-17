# 跨零点与当地时区（schema184 / 小程序0.3.36+）

dayId只控制展示归属日，不代表实际发生日期。凌晨接机可以留在出发当天，不自动移动或复制到第二天。

| 字段 | 含义 |
| --- | --- |
| place_time / end_time | 当地钟表HH:mm，不用25:00或“次日01:00”字符串 |
| start_day_offset | 相对所属行程日的开始日期：0当日，1次日；允许-1至7 |
| end_day_offset | 相对同一个所属行程日的结束日期，不是相对开始时刻 |
| start_timezone | IANA时区，如Asia/Hong_Kong；null恢复按地点坐标识别 |
| end_timezone | 结束/抵达当地时区，如Asia/Bangkok；默认沿用开始时区 |

创建默认偏移0；更新省略字段保留原值。只改开始偏移、未传结束偏移时，原本与开始同一天的结束日期跟随；已有独立结束偏移保留。已知完整时间建议明确传两者。

用create_and_assign_place、assign_place_to_day同次填写；修改用update_assignment_time。先读取真实ID，以下仅为格式示例：

```json
{"tripId":3,"dayId":12,"name":"抵达后接机","place_time":"01:00","end_time":"02:00","start_day_offset":1,"end_day_offset":1,"start_timezone":"Asia/Bangkok","transport_mode":"taxi","transport_source":"inferred","transport_reason":"落地后接驳建议，未预订"}
```

- 界面在原所属日显示次日01:00，排序在当晚23:15之后。跨时区飞行的两端分别按真实出发/抵达日期和当地时区填写，不能仅因结束钟点小于开始就判断无效。
- 写后核对day_id仍为原所属日、两项日偏移和actual_start/end_date；有坐标或指定时区时还核对effective_start/end_timezone及actual_start/end_at（UTC ISO）。不能只看数量。
- 首页与ICS使用实际时刻。无日期/时区时UTC返回null，补查地点或确认时区，不声称已精确转换。
- 夏令时不存在时刻拒绝或无法解析；重复钟点有歧义时核对票据，不承诺未经验证的精确时刻。
- 旧凌晨不能一律改次日；批量修复前按每次安排预览并确认。真的移动到另一行程日时另用移动操作，并重新核对偏移。
- 实时Schema缺字段时明确需升级，不能用25:00、改文案或移动日期绕过。
