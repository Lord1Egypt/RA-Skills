# GetAppOrchestrationExport - 导出应用编排

通过OpenAPI导出应用编排。

| **适用版本** | **企业标准版** |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/lingma/developer-reference/obtain-personal-access-token-1)。
-   获取organizationId，请前往组织管理后台的基本信息页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 应用编排 | 只读 |

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/orchestrations:export`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| organizationId | string | path | 是 | 组织 ID。 | bd9e3c6d-xxxxxxxc5e26f1ed0f0 |
| envName | string | query | 否 | 环境名称。 | dev |
| profileNames | string | query | 否 | 应用变量组名称，非必填，多个用逗号分隔。 | dev,test |
| renderType | string | query | 是 | 渲染类型，必填，值必须为：  -   `MANIFEST` :原生 YAML -   `CHARTS`: Helm Charts | MANIFEST |
| suitableResourceType | string | query | 是 | 适用资源类型，必填，值必须为:  -   `KUBERNETES`:Kubernetes 部署 -   `HOST`:主机部署 | KUBERNETES |
| sha | string | query | 是 | 编排版本信息 commit sha 值，必填，可参考 API `ListAppOrchestration` 获取。 | d23ccbd926c31e3cxxxxxxx3f22c4548b93b1426e |

## **请求示例**

`curl -X 'GET' \ 'https://{domain}/oapi/v1/appstack/organizations/bd9e3c6d-xxxxxxxc5e26f1ed0f0/apps/my-web-service/orchestrations:export?envName=dev&profileNames=dev,test&renderType=MANIFEST&suitableResourceType=KUBERNETES&sha=d23ccbd926c31e3cxxxxxxx3f22c4548b93b1426e' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 导出应用编排响应。 |  |

## **返回示例**

`map[demo-deployment.yaml:--- apiVersion: apps/v1 kind: Deployment metadata: name: k8s-111-dev labels: run: k8s-111-dev namespace: default spec: replicas: 1 selector: matchLabels: run: k8s-111-dev template: metadata: labels: run: k8s-111-dev spec: containers: - name: main image: NULL ports: - containerPort: 8080 resources: limits: cpu: 1 memory: 1024Mi requests: cpu: 0.01 memory: 32Mi demo-service.yaml:--- apiVersion: v1 kind: Service metadata: name: k8s-111-dev namespace: default spec: selector: run: k8s-111-dev ports: - protocol: TCP port: 80 targetPort: 8080]`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。