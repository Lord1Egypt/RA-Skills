# CreateHostGroup - 创建主机组

通过 OpenAPI 创建主机组。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 主机组 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/flow/organizations/{organizationId}/hostGroups`

### **Region版**

```
POST https://{domain}/oapi/v1/flow/hostGroups
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| type | string | query | 是 | 主机组类型，暂只支持 ECS。 | ECS |
| envId | string | query | 否 | 环境 id。 | 0 |
| name | string | query | 是 | 主机组名称。 | 主机组 |
| serviceConnectionId | integer | query | 是 | 服务连接 id。 | 123 |
| tagIds | string | query | 否 | 标签 id，多个逗号分割。 | 12,234 |
| ecsType | string | query | 否 | ECS 类型，暂支持 ECS\_ALIYUN。 | ECS\_ALIYUN |
| ecsLabelKey | string | query | 否 | ecs 标签 key。 | ecs |
| ecsLabelValue | string | query | 否 | ecs 标签 value。 | ecs |
| aliyunRegion | string | query | 否 | 阿里云 region。 | cn-beijing |
| machineInfos | string | query | 否 | aliyunRegionId 机器所在 aliyun region，machineSn 机器的 sn, instanceName,主机名，ip 主机 ip。 | \[{"aliyunRegionId":"cn-beijing","machineSn":"i-sssssss","instanceName":"ceshi","ip":"120.0.0.0"}\] |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/hostGroups?type=ECS&envId=0&name=主机组&serviceConnectionId=123&tagIds=12,234&ecsType=ECS_ALIYUN&ecsLabelKey=ecs&ecsLabelValue=ecs&aliyunRegion=cn-beijing&machineInfos=[{"aliyunRegionId":"cn-beijing","machineSn":"i-sssssss","instanceName":"ceshi","ip":"120.0.0.0"}]' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/flow/hostGroups?type=ECS&envId=0&name=主机组&serviceConnectionId=123&tagIds=12,234&ecsType=ECS_ALIYUN&ecsLabelKey=ecs&ecsLabelValue=ecs&aliyunRegion=cn-beijing&machineInfos=[{"aliyunRegionId":"cn-beijing","machineSn":"i-sssssss","instanceName":"ceshi","ip":"120.0.0.0"}]' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | integer | 主机组 id。 | 123 |

## **返回示例**

`123`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。