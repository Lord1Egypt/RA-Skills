# CreateServiceCredential - 创建服务证书

通过 OpenAPI 创建服务证书。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 流水线 | 服务连接 | 读写 |

## **请求语法**

### **中心版**

`POST https://{domain}/oapi/v1/flow/organizations/{organizationId}/serviceCredentials`

### **Region版**

```
POST https://{domain}/oapi/v1/flow/serviceCredentials
```

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| organizationId | string | path | -   是：中心版 -   否：Region版 | 企业 Id。 | 5ebbc0228123212b59xxxxx |
| \- | object | body | 否 |  |  |
| name | string | body | 是 | 服务证书名称。 | 张三的 Git 证书 |
| password | string | body | 是 | 密码。 | zhangsan |
| scope | string | body | 否 | 可见范围：如 PERSON。 | PERSON （私有） |
| type | string | body | 是 | 服务证书类型，默认 USERNAME\_PASSWORD。 | USERNAME\_PASSWORD （用户密码类型） |
| username | string | body | 是 | 用户名。 | zhangsan |

## **请求示例**

### **中心版**

`curl -X 'POST' \ 'https://{domain}/oapi/v1/flow/organizations/5ebbc0228123212b59xxxxx/serviceCredentials' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \ --data ' { "name": "张三的Git证书", "password": "zhangsan", "scope": "PERSON （私有）", "type": "USERNAME_PASSWORD （用户密码类型）", "username": "zhangsan" }'`

### **Region版**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/flow/serviceCredentials' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "name": "张三的Git证书",
        "password": "zhangsan",
        "scope": "PERSON  （私有）",
        "type": "USERNAME_PASSWORD  （用户密码类型）",
        "username": "zhangsan"
    }'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | integer | 服务证书 id。 | 11222 |

## **返回示例**

`11222`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。