# ListFiles - 查询文件树

通过 OpenAPI 查询文件树。

| **适用版本** | **中心版、Region版** |
| --- | --- |

## **服务接入点与授权信息**

-   [获取服务接入点](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)：替换 API 请求语法中的 {domain} 。
-   [获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId：**仅中心版需要**。请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 代码管理 | 文件 | 只读 |

## **请求语法**

### **中心版**

`GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/files/tree`

### **Region版**

```
GET https://{domain}/oapi/v1/codeup/repositories/{repositoryId}/files/tree
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
| path | string | query | 否 | 指定查询的路径，例如需要查询 src/main 目录下的文件。 | src/main/test |
| ref | string | query | 否 | 指定引用名，一般为分支名，可为分支名、标签名和 CommitSHA，若不传值，则为当前代码库的默认分支，如 master。 | master |
| type | string | query | 否 | 文件树获取方式：DIRECT - 仅获取当前目录，默认方式；RECURSIVE - 递归查找当前路径下的所有文件；FLATTEN - 扁平化展示（如果是目录，递归查找，直到子目录包含文件或多个目录为止。 | DIRECT |

## **请求示例**

### **中心版**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/files/tree?path=src/main/test&ref=master&type=DIRECT' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

### **Region版**

```
curl -X 'GET' \
  'https://{domain}/oapi/v1/codeup/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/files/tree?path=src/main/test&ref=master&type=DIRECT' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object |  |  |
| id | string | 文件的 git object id，是文件的唯一标识。 | b573bb50d56e8c19282593cbf5b081e211923a83 |
| isLFS | boolean | 是否是 LFS 文件。 | false |
| mode | string | 类型、权限等信息，例如100644。 | 100644 |
| name | string | 文件名称。 | main.java |
| path | string | 文件路径。 | src/test/main.java |
| type | string | 文件类型：tree - 目录；blob - 文件；commit - 使用 submodule。 | tree |

## **返回示例**

`{ "id": "b573bb50d56e8c19282593cbf5b081e211923a83", "isLFS": false, "mode": "100644", "name": "main.java", "path": "src/test/main.java", "type": "tree" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。