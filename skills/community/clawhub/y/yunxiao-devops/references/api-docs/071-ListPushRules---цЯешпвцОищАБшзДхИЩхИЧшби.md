# ListPushRules - 查询推送规则列表

通过 OpenAPI 查询推送规则列表，无分页。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 推送规则 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/pushRules`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/pushRules
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

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/pushRules' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/pushRules' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | array |  |  |
| \- | object |  |  |
| createdAt | string | 创建时间。 | 2024-10-05T15:30:45Z |
| id | integer | 推送规则主键 ID。 | 1 |
| ruleInfos | array | 规则信息列表。 |  |
| \- | object |  |  |
| checkerName | string | 规则名称，可为: CommitMessageChecker - 提交说明规则；CommitAuthorEmailChecker - 提交邮箱规则；CommitAuthorChecker - 提交作者检查；CommitCommitterChecker - 提交人检查；ForcePushChecker - 强制推送检查；CommitFilesChecker - 提交文件限制规则；ThirdPartyChecker - 三方校验规则。 | CommitMessageChecker |
| checkerType | string | 限制级别设置：warn - 仅警告，允许推送，block - 禁止推送。 | warn |
| extraMessage | string | 在提交说明、提交邮箱、检查作者、检查提交人以及禁止强制推送时有效：1.提交说明规则，extraMessage 传入检查的正则表达式; 2.提交邮箱规则，extraMessage 传入检查的邮箱正则表示; 3.禁止强制推送，extraMessage 传入 "disabled"; 4.检查作者规则，extraMessage 传入 "on"，若不需要则不传值; 5.检查提交人规则，extraMessage 传入 "on"，若不需要则不传值; 6. 三方校验规则，比如传入空字符串。 | username@example.com |
| fileRuleRegexes | array\[string\] | 该字段仅作用于提交文件限制，传入正则表达式，支持多条正则限制。 | \["\*.java"\] |
| thirdPartyTimeout | integer | 仅作用于三方校验规则，默认的超时时间为1000ms，三方校验服务的耗时尽可能不要超过1秒，也不建议将超时调大。 | 1000 |
| thirdPartyUrl | string | 仅作用于三方校验规则，表示三方校验地址；如果 codeup 后端服务到第三方服务网络不通，则会调用失败，这是常见问题。 | http://example.com/test |
| updatedAt | string | 更新时间。 | 2024-10-05T15:30:45Z |

## **返回示例**

`[ { "createdAt": "2024-10-05T15:30:45Z", "id": 1, "ruleInfos": [ { "checkerName": "CommitMessageChecker", "checkerType": "warn", "extraMessage": "username@example.com", "fileRuleRegexes": ["*.java"], "thirdPartyTimeout": 1000, "thirdPartyUrl": "http://example.com/test" } ], "updatedAt": "2024-10-05T15:30:45Z" } ]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。