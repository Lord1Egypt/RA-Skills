# DeleteAppStackWebhook - 删除 AppStack Webhook

删除指定的 AppStack Webhook 配置。

| **适用版本** | **企业标准版** |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/lingma/developer-reference/obtain-personal-access-token-1)。
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | Webhook | 读写 |

## **请求语法**

`DELETE https://{domain}/oapi/v1/appstack/organizations/{organizationId}/hook/{sn}/api`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | ec766e6xxxxxxxxxx34d6exe671 |
| sn | string | path | 是 | Webhook 唯一标识。 | c263a67497xxxxxxx42f45f2f80e |

## **请求示例**

`curl -X 'DELETE' \ 'https://{domain}/oapi/v1/appstack/organizations/ec766e6xxxxxxxxxx34d6exe671/hook/c263a67497xxxxxxx42f45f2f80e/api' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | boolean |  | true |

## **返回示例**

`true`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。