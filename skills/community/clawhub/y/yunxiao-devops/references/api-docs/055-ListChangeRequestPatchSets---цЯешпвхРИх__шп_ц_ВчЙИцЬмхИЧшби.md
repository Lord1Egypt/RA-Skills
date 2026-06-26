# ListChangeRequestPatchSets - 查询合并请求版本列表

通过 OpenAPI 查询合并请求版本列表。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 合并请求 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/patches`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/changeRequests/{localId}/diffs/patches
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 组织 ID。 | 60d54f3daccf2bbd6659f3ad |
| repositoryId | string | path | 是 | 代码库 ID 或者 URL-Encoder 编码的全路径。 | 2813489或者60de7a6852743a5162b5f957%2FDemoRepo |
| localId | integer | path | 是 | 局部 ID。 | 1 |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/diffs/patches' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/diffs/patches' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| commitId | string | 版本对应的提交 ID。 | 45ede4680536406d793e0e629bc771cb9fcaa153 |
| createTime | string | 版本创建时间。 | 2024-10-05T15:30:45Z |
| patchSetBizId | string | 版本 ID，具有唯一性。 | bf117304dfe44d5d9b1132f348edf92e |
| patchSetName | string | 版本名称。 | 版本1 |
| ref | string | 版本对应的 ref 信息。 | null |
| relatedMergeItemType | string | 关联的类型：MERGE\_SOURCE - 合并源；MERGE\_TARGET - 合并目标。 | MERGE\_SOURCE |
| shortId | string | 提交 ID 对应的短 ID，通常为8位。 | 45ede468 |
| versionNo | integer | 版本号。 | 1 |

## **返回示例**

`[ { "commitId": "45ede4680536406d793e0e629bc771cb9fcaa153", "createTime": "2024-10-05T15:30:45Z", "patchSetBizId": "bf117304dfe44d5d9b1132f348edf92e", "patchSetName": "版本1", "ref": "null", "relatedMergeItemType": "MERGE_SOURCE", "shortId": "45ede468", "versionNo": 1 } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。