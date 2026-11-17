# 配对条件与跨位置 OR 的执行示例

同一位置词组的嵌套逻辑先用 `preflight-complex` 尝试编译为一次查询。采购方类型与设备配对时，“查医院的设备 A 或学校的设备 B”须保留两组配对条件，建立两个完整操作：

```json
{"conditions":[{"id":"h","type":"organization_type","value":["医院"],"operation_ids":["hospital"]},{"id":"a","type":"keyword_group","value":{"keywords":["设备A"],"matchScopes":[2,9]},"operation_ids":["hospital"]},{"id":"s","type":"organization_type","value":["学校"],"operation_ids":["school"]},{"id":"b","type":"keyword_group","value":{"keywords":["设备B"],"matchScopes":[2,9]},"operation_ids":["school"]}],"logic_groups":[{"id":"hospital_branch","operator":"AND","condition_ids":["h","a"]},{"id":"school_branch","operator":"AND","condition_ids":["s","b"]},{"id":"root","operator":"OR","group_ids":["hospital_branch","school_branch"]}],"root_group_id":"root","operations":[{"id":"hospital","action":"search","data_source":"project"},{"id":"school","action":"search","data_source":"project"}]}
```

按预检返回的 `approved_operations` 原样执行。标题“物业”或附件“服务方案”也分别建一个搜索操作，各给词组位置 `[2]` 和 `[10]`，不把两词放进共同位置。共有地区、日期等条件在两个分支都保留；两个接口总数分别说明，不相加当作去重总数。原意明确时不再向用户追问。
