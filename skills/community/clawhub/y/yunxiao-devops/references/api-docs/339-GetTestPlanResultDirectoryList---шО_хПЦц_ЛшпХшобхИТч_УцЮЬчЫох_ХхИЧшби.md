# GetTestPlanResultDirectoryList - 获取测试计划结果目录列表

通过 OpenAPI 获取测试计划下的测试用例涉及的用例库的用例目录树，返回每个用例库下的目录列表及每个目录下的测试用例数量。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 测试管理 | 测试计划 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/testhub/organizations/{organizationId}/{testPlanIdentifier}/result/directory/list`

### **Region版**

```
GET https://{domain}/oapi/v1/testhub/{testPlanIdentifier}/result/directory/list
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | organizationId。 |  |
| testPlanIdentifier | string | path | 是 | 测试计划唯一标识。 |  |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/testhub/organizations/{organizationId}/{testPlanIdentifier}/result/directory/list' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/testhub/{testPlanIdentifier}/result/directory/list' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 用例库名称到目录列表的映射，key 是用例库名称，value 是该用例库下的目录列表（包含每个目录下的测试用例数量）。 | map\[用例库 A:\[map\[children:\[\] displayName:目录1 identifier:dir1 name:目录1 parentIdentifier: spaceIdentifier:space1 workitemCount:10\]\] 用例库 B:\[\]\] |

## **返回示例**

`map[用例库A:[map[children:[] displayName:目录1 identifier:dir1 name:目录1 parentIdentifier: spaceIdentifier:space1 workitemCount:10]] 用例库B:[]]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。