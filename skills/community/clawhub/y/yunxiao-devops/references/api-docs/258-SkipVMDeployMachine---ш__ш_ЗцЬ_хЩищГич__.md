# SkipVMDeployMachine - 跳过机器部署

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 主机部署 | 读写 |

## **请求语法**

### **中心版**

`PUT https://{domain}/oapi/v1/flow/organizations/{organizationId}/pipelines/{pipelineId}/deploy/{deployOrderId}/machine/{machineSn}/skip`

### **Region版**

```
PUT https://{domain}/oapi/v1/flow/pipelines/{pipelineId}/deploy/{deployOrderId}/machine/{machineSn}/skip
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| pipelineId | string | path | 是 | 流水线 Id。 | 123 |
| deployOrderId | string | path | 是 | 部署单 Id。 | 1111 |
| machineSn | string | path | 是 | 机器 sn。 | asssssssxsx |

## **请求示例**

### **中心版**

`curl -X 'PUT' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/pipelines/123/deploy/1111/machine/asssssssxsx/skip' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'PUT' \
  'https://{domain}/oapi/v1/flow/pipelines/123/deploy/1111/machine/asssssssxsx/skip' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | boolean | 是否成功。 | true |

## **返回示例**

`true`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。