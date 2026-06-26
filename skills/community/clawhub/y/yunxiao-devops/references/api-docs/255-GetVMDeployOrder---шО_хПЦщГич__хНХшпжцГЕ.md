# GetVMDeployOrder - 获取部署单详情

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 主机部署 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/{pipelineId}/deploy/{deployOrderId}`

### **Region版**

```
GET https://{domain}/oapi/v1/flow/pipelines/{pipelineId}/deploy/{deployOrderId}
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| pipelineId | string | path | 是 | 流水线 id。 | 123 |
| deployOrderId | string | path | 是 | 部署 Id。 | 1111 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/123/deploy/1111' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/flow/pipelines/123/deploy/1111' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| actions | array |  |  |
| \- | object |  |  |
| disable | boolean | 当前用户是否有权限进行后续 action。 | true |
| params | object | 参数。 | map\[\] |
| type | string | 类型 StopVMDeployOrder 取消部署单 ResumeVMDeployOrder 继续部署单运行。 | StopVMDeployOrder |
| createTime | integer | 创建时间。 | 1729178040000 |
| creator | string | 创建人。 | ssaassa |
| currentBatch | integer | 当前发布批次。 | 2 |
| deployMachineInfo | object |  |  |
| batchNum | integer | 发布批次。 | 2 |
| deployMachines | array |  |  |
| \- | object |  |  |
| actions | array |  |  |
| \- | object |  |  |
| disable | boolean | 当前用户是否有权限进行后续 action。 | true |
| params | object | 参数。 | map\[\] |
| type | string | 类型 RetryVMDeployMachine 重试机器部署 SkipVMDeployMachine 跳过机器部署 LogVMDeployMachine 查看机器部署日志。 | RetryVMDeployMachine |
| batchNum | integer | 部署批次。 | 2 |
| clientStatus | string | 机器状态 ok(正常) error(连接失败)。 | ok |
| createTime | integer | 创建时间。 | 1729178040000 |
| ip | string | 机器 ip。 | 127.0.0.1 |
| machineSn | string | 机器 sn。 | asssssssxsx |
| status | string | 状态 Success 成功 Pending 待部署 Running 部署中 Cancelled 取消 Queued 部署等待中 Failed 失败 Skipped 已跳过。 | Success |
| updateTime | integer | 更新时间。 | 1729178040000 |
| hostGroupId | integer | 主机组 Id。 | 123 |
| deployOrderId | integer | 部署单 id。 | 1111 |
| exceptionCode | string | 错误码。 | 500 |
| status | string | 发布状态 Waiting 暂停 Running 部署中 Cancelled 已取消 Success 成功。 | Success |
| totalBatch | integer | 总发布批次。 | 3 |
| updateTime | integer | 更新时间。 | 1729178040000 |

## **返回示例**

`{ "actions": [ { "disable": true, "params": { }, "type": "StopVMDeployOrder" } ], "createTime": 1729178040000, "creator": "ssaassa", "currentBatch": 2, "deployMachineInfo": { "batchNum": 2, "deployMachines": [ { "actions": [ { "disable": true, "params": { }, "type": "RetryVMDeployMachine" } ], "batchNum": 2, "clientStatus": "ok", "createTime": 1729178040000, "ip": "127.0.0.1", "machineSn": "asssssssxsx", "status": "Success", "updateTime": 1729178040000 } ], "hostGroupId": 123 }, "deployOrderId": 1111, "exceptionCode": "500", "status": "Success", "totalBatch": 3, "updateTime": 1729178040000 }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。