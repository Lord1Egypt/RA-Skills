# ListHostGroups - 获取主机组列表

通过 OpenAPI 获取主机组列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 主机组 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/hostGroups`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/hostGroups
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| ids | string | query | 否 | 主机组 id，多个逗号分割。 | 121,1212121232 |
| name | string | query | 否 | 主机组名称。 | 主机组 |
| createStartTime | integer | query | 否 | 主机组创建时间。 | 1586863220000 |
| createEndTime | integer | query | 否 | 主机组结束时间。 | 1586863220000 |
| creatorAccountIds | string | query | 否 | 创建阿里云账号 id，多个逗号分割。 | 1112122121,3223332 |
| perPage | integer | query | 否 | 每页数据条数，默认10，最大支持30。 | 10 |
| page | integer | query | 否 | 当前页，默认1。 | 1 |
| pageSort | string | query | 否 | 排序条件 ID。 | ID |
| pageOrder | string | query | 否 | 排序顺序 DESC 降序 ASC 升序。 | DESC |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/hostGroups?ids=121,1212121232&name=主机组&createStartTime=1586863220000&createEndTime=1586863220000&creatorAccountIds=1112122121,3223332&perPage=10&page=1&pageSort=ID&pageOrder=DESC' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/hostGroups?ids=121,1212121232&name=主机组&createStartTime=1586863220000&createEndTime=1586863220000&creatorAccountIds=1112122121,3223332&perPage=10&page=1&pageSort=ID&pageOrder=DESC' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| aliyunRegion | string | 阿里云区域。 | cn-hangzhou |
| createTime | integer | 创建时间。 | 1586863220000 |
| creatorAccountId | string | 创建人。 | 1111111111111 |
| description | string | 主机组描述。 | 主机组描述 |
| ecsLabelKey | string | ecs 标签 Key。 | ecs |
| ecsLabelValue | string | ecs 标签 Value。 | ecs |
| ecsType | string | ecs 类型，暂只支持 ECS\_ALIYUN。 | ECS\_ALIYUN |
| hostInfos | array |  |  |
| \- | object |  |  |
| aliyunRegion | string | 阿里云区域。 | cn-hangzhou |
| createTime | integer | 创建时间。 | 1586863220000 |
| creatorAccountId | string | 创建者阿里云账号。 | 1111111111111 |
| instanceName | string | 主机名。 | ceshi |
| ip | string | 机器 ip。 | 127.0.0.1 |
| machineSn | string | 机器 sn。 | 1ssasa |
| modifierAccountId | string | 修改者阿里云账号。 | 1111111111111 |
| objectType | string | MachineInfo 值固定为 MachineInfo。 | MachineInfo |
| updateTime | integer | 更新时间。 | 1586863220000 |
| hostNum | integer | 主机数。 | 1 |
| id | integer | 主机组 id。 | 1234 |
| modifierAccountId | string | 更新人。 | 1111111111111 |
| name | string | 主机组名称。 | 主机组名称 |
| serviceConnectionId | integer | 服务连接 id。 | 1234 |
| type | string | 主机组类型。 | ECS |
| updateTime | integer | 更新时间。 | 1586863220000 |
| uuid | string | 主机组 uuid。 | KxqtcgPp7y5ROZdd |

## **返回示例**

`[ { "aliyunRegion": "cn-hangzhou", "createTime": 1586863220000, "creatorAccountId": "1111111111111", "description": "主机组描述", "ecsLabelKey": "ecs", "ecsLabelValue": "ecs", "ecsType": "ECS_ALIYUN", "hostInfos": [ { "aliyunRegion": "cn-hangzhou", "createTime": 1586863220000, "creatorAccountId": "1111111111111", "instanceName": "ceshi", "ip": "127.0.0.1", "machineSn": "1ssasa", "modifierAccountId": "1111111111111", "objectType": "MachineInfo", "updateTime": 1586863220000 } ], "hostNum": 1, "id": 1234, "modifierAccountId": "1111111111111", "name": "主机组名称", "serviceConnectionId": 1234, "type": "ECS", "updateTime": 1586863220000, "uuid": "KxqtcgPp7y5ROZdd" } ]`

## **响应头**

| **参数** | **描述** | **示例值** |
| --- | --- | --- |
| x-next-page | 下一页。 | 3 |
| x-page | 当前页。 | 2 |
| x-per-page | 每页数据条数。 | 10 |
| x-prev-page | 上一页。 | 1 |
| x-total | 总数据量。 | 100 |
| x-total-pages | 总分页数。 | 10 |

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。