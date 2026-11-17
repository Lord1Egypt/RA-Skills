# 到达方式：每次安排独立（server schema183 / 小程序0.3.35+）

## 含义与字段

`transport_mode` 表示“如何到达这次安排”，不是地点类别。同一家酒店多次到达可以不同，不要为修改一次到达而批量修改地点。

| 值 | 含义 |
| --- | --- |
| `none` | 无需交通，同一地点内活动 |
| `walking` | 步行 |
| `taxi` | 打车或包车、接送机 |
| `driving` | 自驾 |
| `transit` | 公共交通：地铁、公交、火车、渡船、接驳；具体方式写本次备注 |
| `cycling` | 骑行 |
| `flight` | 实际飞行段，不能因为地点是机场就使用 |

旧 `bicycling`、`metro` 可输入并规范成 `cycling`、`transit`。

- 新建日程：`create_and_assign_place`，已有地点排期：`assign_place_to_day`；直接同次传时间与到达方式。
- 修改一次到达：`update_assignment_time`，使用 `assignmentId` 而不是 `placeId`。
- `transport_source`：`confirmed` 仅限用户指定/有凭据事实；合理推断用 `inferred`。小程序手动选择保存为 `manual`。
- `transport_reason`：不超过500字，简短描述依据；建议不代表已预订、已付款或线路实时可用。
- 省略字段保持不变；`transport_mode:null` 清除该次覆盖，恢复旧地点值兼容。界面没有“未设置”选项。
- 自动修改默认拒绝覆盖 `manual`。只有用户明确要求替换其手动选择才传 `replace_manual_transport:true`，不能为消除错误而擅自打开。
- 返回和摘要中的 `days[].assignments[].transport_mode / transport_source / transport_reason` 是核对对象。不要只核对 `place.transport_mode`；`legacy` 表示旧地点兼容值。
- `create_place`、`create_place_accommodation` 的同名参数仅是可复用偏好，不会创建可见日程；日程仍需独立到达方式。

## 推断流程

1. 先读取该次安排的人工选择和用户指定/已订交通，不覆盖它们。
2. 根据上一站、实际路线、距离、同行者年龄/行动能力、行李、天气与时间余量推断。短距离不一定适合步行，长距离也不一定乘飞机。
3. 接送机设 `taxi`，实际航班设 `flight`，酒店内休息设 `none`。无法确定具体线路但动线可判断时给合理建议并标记 `inferred`，不要让用户逐条填空。
4. 第一站缺出发地或地图信息时尽量补查；若用保守接驳建议，要在依据中说明假设，不能假装已经订车。服务端未收到参数时只有有限文字/距离规则，不代替Agent的完整研究。
5. 复用地点按每次安排判断，写后逐次回读。重排或移动已有安排后交通值会保留，Agent应重新审视前后动线；人工值保持优先。
6. 历史默认 `walking` 无法可靠区分主动选择，禁止全量自动清空或改乘车。批量修复旧行程先按日期与assignment预览并取得确认。

## 同次创建示例

```json
{
  "tripId": 3,
  "dayId": 12,
  "name": "酒店入住",
  "place_time": "15:00",
  "transport_mode": "taxi",
  "transport_source": "inferred",
  "transport_reason": "机场至酒店携带行李，建议打车；未预订"
}
```

这些ID仅为格式示例，必须先从用户授权的行程中读取实际ID。若实时Schema缺少新字段，不要假装写入成功，也不要退回批量修改共用地点；先交付规划建议并明确服务端需升级。
