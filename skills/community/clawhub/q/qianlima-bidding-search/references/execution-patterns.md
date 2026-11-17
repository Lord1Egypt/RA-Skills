# 命令与复杂预检样板

根目录运行 `python3 scripts/qianlima_skill.py`；用户文本不拼入 shell。

search 见 [普通项目](capabilities/project-search.md#最短调用入口)。

## 可直接表达的多条件

“标题有空调或新风，正文有安装或改造，财政资金且无附件”是平铺 AND，直接 `search --query-json`，无须预检：

```json
{"keywordGroups":[{"keywords":["空调","新风"],"matchScopes":[2]},{"keywords":["安装","改造"],"matchScopes":[8]}],"fundsSources":[1],"hasAnnex":0}
```

## 需要编译的嵌套逻辑

“空调，或者新风且安装”，各词均搜标题＋标的物：

```json
{"conditions":[{"id":"a","type":"keyword_group","value":{"keywords":["空调"],"matchScopes":[2,9]}},{"id":"b","type":"keyword_group","value":{"keywords":["新风"],"matchScopes":[2,9]}},{"id":"c","type":"keyword_group","value":{"keywords":["安装"],"matchScopes":[2,9]}}],"logic_groups":[{"id":"root","operator":"OR","condition_ids":["a"],"group_ids":["both"]},{"id":"both","operator":"AND","condition_ids":["b","c"]}],"root_group_id":"root","operations":[{"id":"op1","action":"search","data_source":"project"}]}
```

运行 `preflight-complex --plan-json '<上述JSON>' --user-text '<原话>'` 一次，按 `approved_operations`（含 `access_mode`）原样调用；无批准操作不调业务。不填 normalized/applies_to、condition_ids/query；组引用合法。

同位置词组预检为一次查询；医院设备 A 或学校设备 B，以及标题“物业”或附件“服务方案”，都按配对/位置分支执行，见 [分支示例](branch-query-examples.md)。

## 指定机构与精确时间

普通项目采购单位角色条件示例：

```json
{"id":"c1","type":"organization_role","value":{"role":"purchasing_unit","keywords":["北京大学"]}}
```

普通 `publish_time` value 可用 `{"start":"2026-09-01 09:30:00","end":"2026-09-02 18:00:00"}`；仅普通项目支持单端。相对范围 `{"relative":"past_months","count":3}` 或 future_months；current_date 用当天，不复用样例日期。

## 多源与细化

“北京近一个月 500 万以上物业招标，和未来半年到期物业服务合同”：area 共同；“物业”、公告时间、金额和阶段只给 project 操作；“物业服务”、到期时间只给 expiring_project 操作，用各自 condition.operation_ids 绑定。预检一次，各批准分支一次，分区展示，不合并总数或把结果冒充交集。

临期追问“地区不变，加 500 万以上并排除保洁”：原结果直接 refine，patch `{"beginContractAmount":5000000,"excludeWords":["保洁"]}`；按追加保留原排除词、地区、到期时间。缓存不可用按下节恢复，不改为普通项目。

## 恢复完整查询

原 session_id/result_set_id 仍可用；明确 `--result-set-id RESULT` 可省会话。缓存不可用按 [完整上下文](api.md#完整查询上下文) 恢复原全条件与精确页码。

## 公司和单条资源

公司候选、翻页和企业统计命令见 [企业情报](capabilities/enterprise-intelligence.md)。指定单位的公告列表仍用 search。

已知公告正文/附件/时间线用对应命令 `--id ID`，不先取详情。序号/标题定位与独立节点读取见 [项目资源](api-project-resources.md)。

## 同时取消普通项目两项筛选

“附件和采购方式都不限”：带原 `session_id/result_set_id` 直接 refine，patch 如下，无须因改两项而预检：

```json
{"hasAnnex":null,"procurementMethods":null}
```

未改条件继承；0 不取消。分支重组需预检。
