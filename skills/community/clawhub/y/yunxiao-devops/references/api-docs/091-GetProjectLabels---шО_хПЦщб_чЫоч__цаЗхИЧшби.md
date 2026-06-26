# GetProjectLabels - 获取项目类标列表

通过 OpenAPI 获取项目类标列表。

| **适用版本** | **中心版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 项目类标 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/labels`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | 是 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| repositoryId | string | path | 是 | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| search | string | query | 否 | 类标名称搜索。 | bug |
| page | integer | query | 否 | 页码。 | 1 |
| with\_counts | boolean | query | 否 | 是否包含关联的打开的 MR 数量，默认为 false。 | true |
| per\_page | integer | query | 否 | 每页数量。 | 10 |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/labels?search=bug&page=1&with_counts=true&per_page=10' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| color | string | 类标颜色（十六进制格式），可填值：#006AD4, #2FA6A4, #6190AC, #4B81D0, #4D5DBB, #A16AD7, #3BA630, #95B44F, #AA945F, #B36A53, #FD842F, #EF433B。 | #006AD4 |
| description | string | 类标描述。 | 表示代码中的错误 |
| id | string | 类标 ID。 | 68c1bd9b8515477fa86fac5exxxxx941 |
| name | string | 类标名称。 | Bug |
| open\_merge\_requests\_count | integer | 类标关联打开的 MR 的数量。 | 10 |

## **返回示例**

`[ { "color": "#006AD4", "description": "表示代码中的错误", "id": "68c1bd9b8515477fa86fac5exxxxx941", "name": "Bug", "open_merge_requests_count": 10 } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。