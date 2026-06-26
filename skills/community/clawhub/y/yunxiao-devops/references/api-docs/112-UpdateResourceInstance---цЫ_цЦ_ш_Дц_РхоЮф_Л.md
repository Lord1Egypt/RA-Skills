# UpdateResourceInstance - 更新资源实例

通过OpenAPI更新资源实例。

## **前提条件**

-   获取服务接入点，替换 API **请求语法**中的 `<domain>` 。关于如何获取`domain`，请参见[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取**组织 ID** 。

## **授权信息**

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 企业设置 | 读写 |

## **请求语法**

`PUT https://{domain}/oapi/v1/appstack/organizations/{organizationId}/pools/instances/{name}`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| name | string | path | 是 | 资源实例的唯一名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | my-k8s |
| kubeconfig | string | query | 是 | kubeconfig 配置。 | apiVersion: v1... |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exe671 |

## **请求示例**

`curl -X 'PUT' \ 'https://openapi-rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exe671/pools/instances/my-k8s' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ -d 'kubeconfig=apiVersion: v1..'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| data | object | 资源实例。 |  |
| category | string | 资源类别（如计算、存储、网络等），可能的值：\[COMPUTE\]。 | COMPUTE |
| cloudMetadata | string | 云产品元数据。 |  |
| cloudProvider | string | 云产品提供方。 |  |
| contextMap | object | 资源详情数据。 |  |
| description | string | 资源描述。 | 测试用集群 |
| displayName | string | 资源展示名。 | 示例 kubernetes 集群 |
| host | boolean |  | false |
| instanceId | string | 资源实例 ID。 | 1745402511111 |
| k8s | boolean | 是否 k8s。 | true |
| name | string | 资源实例的唯一名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | my-k8s |
| poolName | string | 资源池唯一名。 | default |
| region | string | 资源所处区域。 | cn-hangzhou |
| resourceItemList | array\[string\] | 资源项列表。 | \[\] |
| errorAdvice | string |  |  |
| errorCode | string | 可能的值：  -   ResourceInstanceNotFound -   ResourceInstanceKubeConfigInvalid -   ClusterCaNotAllowedInKubeConfig -   UserExecNotAllowedInKubeConfig UserClientCertificateNotAllowedInKubeConfig -   UserClientKeyNotAllowedInKubeConfig -   UserTokenFileNotAllowedInKubeConfig -   UserAuthProviderNotAllowedInKubeConfig -   SystemInternalError | ResourceInstanceNotFound |
| errorMap | object |  |  |
| errorMessage | string |  |  |
| showType | integer |  |  |
| success | boolean |  |  |
| traceId | string |  |  |

## **返回示例**

`{ "data": { "category": "COMPUTE", "cloudMetadata": "", "cloudProvider": "", "contextMap": { }, "description": "测试用集群", "displayName": "示例 kubernetes 集群", "host": false, "instanceId": "1745402511111", "k8s": true, "name": "my-k8s", "poolName": "default", "region": "cn-hangzhou", "resourceItemList": [], "type": "SELF_KUBERNETES" }, "errorAdvice": "", "errorCode": "ResourceInstanceNotFound", "errorMap": { }, "errorMessage": "", "showType": 0, "success": false, "traceId": "" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。