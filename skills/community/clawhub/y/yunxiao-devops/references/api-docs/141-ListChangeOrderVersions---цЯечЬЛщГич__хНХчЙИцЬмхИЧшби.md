# ListChangeOrderVersions - 查看部署单版本列表

通过 OpenAPI 查看部署单版本列表。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。

| **产品** | **资源** | **所需权限** |
| --- | --- | --- |
| 应用交付 | 部署单 | 只读 |

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/changeOrders/versions`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| envNames | array | query | 否 | 环境标识列表，如不需按环境过滤，请置空。 | \[‘dev’,‘test’\] |
| states | array | query | 否 | 状态筛选列表，如不需按状态过滤，请置空。部署单状态，可能的值：\[INIT PREPARING RUNNING STOPPING SUSPENDING SUSPENDED SUCCESS FAILED CANCELED\]。主要状态含义：RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功。 | \['SUCCESS','FAILED','CANCELED'\] |
| creators | array\[integer\] | query | 否 | 创建人云效账号 ID 列表，如不需按创建人过滤，请置空。 | \[‘bd9e3c6d-624f-4580-af7d-c5e26f1xxxxx’\] |
| pageSize | integer | query | 是 | 分页记录数（默认 10 条）。 | 10 |
| current | integer | query | 否 | 当前页号（从 1 开始，默认取 1） | 1 |
| organizationId | string | path | 是 | 组织 ID。 | ec766e63aee3437d9a51f334d6exxxxx |

## **请求示例**

`curl -X 'GET' \ 'https://openapi-rdc.aliyuncs.com/oapi/v1/appstack/organizations/ec766e63aee3437d9a51f334d6exxxxx/apps/my-web-service/changeOrders/versions?envNames=dev,test&creators=bd9e3c6d-624f-4580-af7d-c5e26fxxxxx&current=1&pageSize=10' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| total | number | 总数。 | 10 |
| current | number | 当前页数。 | 1 |
| pageSize | number | 每页大小。 | 10 |
| pages | number | 总页数。 | 10 |
| records | array | 数据列表，详见[records参数说明](#b201a76fd24le)。 |  |

### **records参数说明**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| version | string | 版本号。 | 20250717115350-021 |
| appOrchestration | object | 应用内置编排，详见[appOrchestration参数说明](#173c11be16onf)。 |  |
| artifacts | string | 产物信息。 | {‘test’:{‘image’:‘nginx’}} |
| changeOrderSummarys | array | 部署单概要信息列表，详见[changeOrderSummarys参数说明](#ca407315e53n2)。 |  |
| creator | string | 创建人。 | 5e706d5503283833284f41c1 |
| gmtCreate | string | 应用创建时间。 | 2025-07-17T03:53:55.000+00:00 |
| envs | array | 环境列表，详见[envs参数说明](#0d2e3fd59auvi)。 |  |

### **appOrchestration参数说明**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| storageType | string | 存储类型。 | BUILTIN |
| app | object | 应用。 |  |
| -   creatorId | string | 应用创建者。 | 10df6011-2837-4fdb-ad92-356a679xxxxx |
| -   description | string | 应用描述。 | for java |
| -   labelList | array | 标签列表，详见[labelList参数说明](#16c62c32a6nal)。 |  |
| -   favoured | boolean | 是否收藏。 | false |
| -   gmtCreate | string | 应用创建时间。 | 2024-09-01 00:00:00 |
| -   type | string | app类型。 | APP |
| format | string | 格式。 | MANIFEST |
| suitableResourceTypes | array\[string\] | 使用资源类型。 |  |
| sn | string | 唯一序列号。 | app-builtin-orchestration-1 |
| revision | object | 编排版本信息。 |  |
| -   sha | string | 编排版本信息 commit sha 值。 | c229f22024535638af41838daa43af1e6d4xxxxx |
| -   message | string | 编排版本信息 commit 信息。 | 3t7cb880d20614038740e00e819dcdb13a3xxxxx |
| -   author | string | 编排版本提交人。 | 10df6011-2837-4fdb-ad92-356a679xxxxx |
| -   commitTime | string | 编排版本提交时间。 | 2024-09-01 00:00:00 |
| name | string | 应用名称。 | my-web-app |
| creatorId | string | 应用创建者。 | 10df6011-2837-4fdb-ad92-356a679xxxxx |
| gmtCreate | string | 应用创建时间。 | 2024-09-01 00:00:00 |
| modifierId | string | 修改人。 | app-builtin-modifier-id |
| gmtModified | string | 修改时间。 | 2024-09-01 00:00:00 |
| description | string | 应用描述。 | for java |
| type | string | 类型。 | AppBuiltInOrchestration |
| labelPolicy | string | 标签策略。 | NONE |
| labelList | array | 标签列表，详见[labelList参数说明](#16c62c32a6nal)。 |  |
| syncSourceTemplate | object | 编排同步源模板。 |  |
| placeholderList | array | 占位符列表。 |  |
| -   description | string | 占位符描述。 | 内存限制 |
| -   name | string | 占位符名。 | memoryLimit |
| -   overridable | boolean | 占位符是否部署时可修改。 | true |
| -   predefined | boolean | 是否预置占位符。 | false |
| -   rsType | string | 适用的部署架构类型（如 Kubernetes、主机等），可能的值：\[KUBERNETES HOST\]。 | KUBERNETES |
| -   rule | string | 占位符取值的可选校验规则。 |  |
| -   type | string | 占位符类型，可能的值：\[string number boolean float object\]。 | string |
| -   value | string | 占位符取值。 | 1024Mi |
| -   valueSource | string | 占位符取值的数据源类型（如常量、变量等），可能的值：\[CONSTANT VARIABLE NULL\]。 | CONSTANT |
| componentList | array | 组件列表。 |  |
| -   content | string | 组件内容，以 go 标准库 text/template 的形式呈现。 | —\\napiVersion: v1\\nkind: Service\\nmetadata:\\n name: prod-sidecar-test-{{ .AppStack.envName }}\\n # 命名空间配置：\\n # 建议每个环境使用不同的 Kubernetes 集群命名空间，以便达到环境隔离效果\\n # 部署时云效会将占位符{{ .Values.namespace }}替换成右侧设置的实际值\\n namespace: {{ .Values.namespace }}\\nspec:\\n selector:\\n run: prod-sidecar-test-{{ .AppStack.envName }}\\n ports:\\n - protocol: TCP\\n port: 80\\n targetPort: 8080 |
| -   description | string | 组件描述。 | 示例描述 |
| -   kind | string | 组件类型（在 Kubernetes 场景下，需要沿用 Kubernetes 对象的 kind）。 | Service |
| -   name | string | 组件名。 | demo-service |
| -   priority | integer | 组件优先级，从 1 开始；环境部署时，会按优先级数值从低到高的顺序下发部署。 | 1 |
| -   type | string | 适用的部署架构类型（如 Kubernetes、主机等），可能的值：\[KUBERNETES HOST\]。 | KUBERNETES |
| groupNameMap | object |  |  |

### **changeOrderSummarys参数说明**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| sn | string | 部署单唯一标识。 | bc62b3e953714aa8be431f47b9cxxxxx |
| name | string | 部署单名称。 | 20241008171130-部署 |
| state | string | 部署单状态，可能的值：\[INIT PREPARING RUNNING SUSPENDED CANCELED SUCCESS FAILED\]。 | 操作类型：RUNNING-运行中，SUSPENDED-暂停中，CANCELED-已取消，FAILED-已失败，SUCCESS-成功 |
| type | string | 部署单类型，可能的值：\[Deploy Scale Rollback Destroy\]。 | 操作类型：Deploy-部署，Scale-扩缩，Rollback-回滚，Destroy-销毁 |

### **envs参数说明**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| deployGroupName | string | 部署组名称。 | deploy-group-name |
| displayName | string | 环境展示名称。 | test-display-name |
| labelList | array | 标签列表，详见[labelList参数说明](#16c62c32a6nal)。 |  |

### **labelList参数说明**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |

## **返回示例**

`{ "total": 88, "current": 1, "pageSize": 1, "pages": 88, "records": [ { "version": "20250717115350-021", "appOrchestration": { "storageType": "BUILTIN", "app": { "name": "huaihu-k8s-test", "description": "这是建立于2025-04-29的应用", "labelList": [], "favoured": false, "creatorId": "5e706d5503283833284f41c1", "gmtCreate": "2025-04-29T08:37:44.000+00:00", "type": "APP" }, "format": "MANIFEST", "suitableResourceTypes": [ "KUBERNETES" ], "sn": "huaihu-k8s-test@KUBERNETES", "revision": { "sha": "ecff6bebc255b6506cd75a3c3689539ec5463155", "message": "修改 k8s 编排", "author": "5e706d5503283833284f41c1", "commitTime": "2025-06-27T10:08:23.932+00:00" }, "name": "huaihu-k8s-test", "creatorId": "5e706d5503283833284f41c1", "gmtCreate": "2025-06-27T10:08:24.000+00:00", "modifierId": "5e706d5503283833284f41c1", "gmtModified": "2025-06-27T10:08:24.000+00:00", "description": null, "type": "AppBuiltInOrchestration", "labelPolicy": "FROM_LABEL_BINDING", "labelList": [ { "namespace": "default", "name": "envType", "value": "dev", "displayName": "环境级别", "displayValue": "开发环境", "extraMap": {} }, { "namespace": "default", "name": "envType", "value": "test", "displayName": "环境级别", "displayValue": "测试环境", "extraMap": {} }, { "namespace": "default", "name": "envType", "value": "prepub", "displayName": "环境级别", "displayValue": "预发环境", "extraMap": {} }, { "namespace": "default", "name": "envType", "value": "production", "displayName": "环境级别", "displayValue": "生产环境", "extraMap": {} } ], "syncSourceTemplate": null, "placeholderList": [ { "name": "image.backend", "description": "后端服务镜像", "type": "string", "value": "NULL", "overridable": true, "rule": null, "valueSource": "CONSTANT", "predefined": true, "rsType": "KUBERNETES" }, { "name": "envName", "description": "环境名", "type": "string", "value": "APPSTACK_ENV_NAME", "overridable": false, "rule": null, "valueSource": "VARIABLE", "predefined": true, "rsType": "KUBERNETES" }, { "name": "namespace", "description": "命名空间", "type": "string", "value": "default", "overridable": true, "rule": null, "valueSource": "CONSTANT", "predefined": false, "rsType": "KUBERNETES" }, { "name": "cpuLimit", "description": "CPU限制", "type": "string", "value": "1", "overridable": true, "rule": null, "valueSource": "CONSTANT", "predefined": false, "rsType": "KUBERNETES" }, { "name": "memoryLimit", "description": "内存限制", "type": "string", "value": "1024Mi", "overridable": true, "rule": null, "valueSource": "CONSTANT", "predefined": false, "rsType": "KUBERNETES" }, { "name": "cpuRequest", "description": "CPU请求", "type": "string", "value": "0.01", "overridable": true, "rule": null, "valueSource": "CONSTANT", "predefined": false, "rsType": "KUBERNETES" }, { "name": "memoryRequest", "description": "内存请求", "type": "string", "value": "32Mi", "overridable": true, "rule": null, "valueSource": "CONSTANT", "predefined": false, "rsType": "KUBERNETES" } ], "componentList": [ { "name": "demo-deployment", "kind": "Deployment", "description": "无状态应用", "content": "---\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n name: huaihu-k8s-test-{{ .AppStack.envName }}\n labels:\n run: huaihu-k8s-test-{{ .AppStack.envName }}\n # 命名空间配置：\n # 建议每个环境使用不同的Kubernetes集群命名空间，以便达到环境隔离效果\n # 部署时云效会将占位符{{ .Values.namespace }}替换成右侧设置的实际值\n namespace: {{ .Values.namespace }}\nspec:\n strategy:\n rollingUpdate:\n maxSurge: 20%\n maxUnavailable: 0%\n type: RollingUpdate\n replicas: 2\n selector:\n matchLabels:\n run: huaihu-k8s-test-{{ .AppStack.envName }}\n template:\n metadata:\n labels:\n run: huaihu-k8s-test-{{ .AppStack.envName }}\n spec:\n containers:\n - name: main\n readinessProbe:\n exec:\n command:\n - echo\n - hello\n failureThreshold: 3\n initialDelaySeconds: 30\n periodSeconds: 10\n successThreshold: 1\n timeoutSeconds: 1\n # 镜像配置：\n # 部署时云效会将预置占位符{{ .AppStack.image.backend }}替换成实际部署时的镜像\n # 支持在新建部署单时手动输入镜像地址，也支持接收流水线的上游构建产物\n # 另外，在右侧镜像占位符处添加多个镜像，可以支持SideCar或InitContainer等多容器场景\n image: {{ .AppStack.image.backend }}\n # 端口配置：\n ports:\n - containerPort: 8080\n # 资源规格配置：\n # 当不同环境有不同的CPU或内存资源规格要求时，可以定义占位符搭配变量组使用\n # 如，设置{{ .Values.cpuLimit }}占位符，部署时云效会将占位符{{ .Values.cpuLimit }}替换成右侧设置的实际值\n resources:\n limits:\n cpu: {{ .Values.cpuLimit }}\n memory: {{ .Values.memoryLimit }}\n requests:\n cpu: {{ .Values.cpuRequest }}\n memory: {{ .Values.memoryRequest }}\n # 生命周期配置：\n #lifecycle:\n # preStop:\n # exec:\n # command: [ \"/bin/bash\", \"-c\", \"sleep 10\" ]\n # 探活配置：\n #livenessProbe:\n # initialDelaySeconds: 10\n # failureThreshold: 3\n # periodSeconds: 5\n # successThreshold: 1\n # timeoutSeconds: 2\n # httpGet:\n # scheme: HTTP\n # path: /health\n # port: 7002\n # 就绪探测配置：\n #readinessProbe:\n # initialDelaySeconds: 60\n # failureThreshold: 4\n # periodSeconds: 10\n # successThreshold: 1\n # timeoutSeconds: 3\n # httpGet:\n # scheme: HTTP\n # port: 7002\n # path: /health", "priority": 1, "type": "KUBERNETES" } ], "groupNameMap": {} }, "artifacts": { "k8s-test": { "image.backend": "anolis-registry.cn-zhangjiakou.cr.aliyuncs.com/openanolis/nginx:1.14.1-8.6" } }, "changeOrderSummarys": [ { "sn": "25d37df408584f13a85ba03a4caf7f5b", "name": "20250717115349-部署", "state": "SUCCESS", "type": "Deploy" } ], "creator": "5e706d5503283833284f41c1", "gmtCreate": "2025-07-17T03:53:55.000+00:00", "envs": [ { "name": "k8s-test", "displayName": "k8s-test", "deployGroupName": "yufa-ceshi", "labelList": [ { "namespace": "default", "name": "envType", "value": "dev", "displayName": "环境级别", "displayValue": "开发环境", "extraMap": {} } ] } ] } ] }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。