# GetLatestOrchestration - 查找匹配给定环境的最新一版编排实例

通过 OpenAPI 查找匹配给定环境的最新一版编排实例。

| 适用版本 | 标准版 |
| --- | --- |

## **服务接入点与授权信息**

-   获取服务接入点，替换 API 请求语法中的 <domain> ：[服务接入点（domain）](https://help.aliyun.com/zh/yunxiao/developer-reference/service-access-point-domain)。
-   获取个人访问令牌，具体操作，请参见[获取个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。
-   获取organizationId，请前往**组织管理后台**的**基本信息**页面获取组织 ID 。
    
    | **产品** | **资源** | **所需权限** |
    | --- | --- | --- |
    | 应用交付 | 应用编排 | 只读 |
    

## **请求语法**

`GET https://{domain}/oapi/v1/appstack/organizations/{organizationId}/apps/{appName}/envs/{envName}/orchestration:latestAvailable`

## **请求头**

| **参数** | **类型** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- |
| x-yunxiao-token | string | 是 | 个人访问令牌。 | pt-0fh3\*\*\*\*0fbG\_35af\*\*\*\*0484 |

## **请求参数**

| **参数** | **类型** | **位置** | **是否必填** | **描述** | **示例值** |
| --- | --- | --- | --- | --- | --- |
| appName | string | path | 是 | 应用名。 | my-web-service |
| envName | string | path | 是 | 环境名。 | dev |
| organizationId | string | path | 是 | 组织 ID。 | 99d1\*\*\*\*71d4 |

## **请求示例**

`curl -X 'GET' \ 'https://test.rdc.aliyuncs.com/oapi/v1/appstack/organizations/anyOrganizationId/apps/my-web-service/envs/dev/orchestration:latestAvailable' \ -H 'Content-Type: application/json' \ -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'`

## **返回参数**

| **参数** | **类型** | **描述** | **示例值** |
| --- | --- | --- | --- |
| \- | object | 应用内置编排。 |  |
| app | object | 应用。 |  |
| creatorId | string | 应用创建者。 | user-xxxx |
| description | string | 应用描述。 | app-description-xxx |
| favoured | boolean | 是否收藏。 | false |
| gmtCreate | string | 应用创建时间。 | 2024-09-01 00:00:00 |
| labelList | array | 应用标签列表。 |  |
| \- | object | AppStack 标签。 |  |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| name | string | 应用名称。 | app-name-xxx |
| type | string | 类型，可能的值：\[APP SYSTEM\]。 | APP |
| componentList | array | 组件列表。 |  |
| \- | object | 编排组件模型。 |  |
| content | string | 组件内容，以 go 标准库 text/template 的形式呈现。 | —\\napiVersion: v1\\nkind: Service\\nmetadata:\\n name: prod-sidecar-test-{{ .AppStack.envName }}\\n # 命名空间配置：\\n # 建议每个环境使用不同的 Kubernetes 集群命名空间，以便达到环境隔离效果\\n # 部署时云效会将占位符{{ .Values.namespace }}替换成右侧设置的实际值\\n namespace: {{ .Values.namespace }}\\nspec:\\n selector:\\n run: prod-sidecar-test-{{ .AppStack.envName }}\\n ports:\\n - protocol: TCP\\n port: 80\\n targetPort: 8080 |
| description | string | 组件描述。 | 示例描述 |
| kind | string | 组件类型（在 kubernetes 场景下，需要沿用 kubernetes 对象的 kind）。 | Service |
| name | string | 组件名。 | demo-service |
| priority | integer | 组件优先级，从 1 开始；环境部署时，会按优先级数值从低到高的顺序下发部署。 | 1 |
| type | string | 适用的部署架构类型（如 Kubernetes、主机等），可能的值：\[KUBERNETES HOST\]。 | KUBERNETES |
| creatorId | string | 创建人。 | app-builtin-creator-id |
| description | string | 描述。 | app-builtin-orchestration-description |
| format | string | 格式。 | MANIFEST |
| gmtCreate | string | 创建时间。 | 2024-09-01 00:00:00 |
| gmtModified | string | 修改时间。 | 2024-09-01 00:00:00 |
| groupNameMap | object |  |  |
| labelList | array | 标签列表。 |  |
| \- | object | AppStack 标签。 |  |
| displayName | string | 标签的展示名，用于描述性的场景，不参与标签匹配。 | 测试标签键 |
| displayValue | string | 标签的展示值，用于描述性的场景，不参与标签匹配。 | 测试标签值 |
| extraMap | object | 标签扩展属性 map，可在定义标签时用于存储自定义的扩展属性字段。 | map\[\] |
| name | string | 标签名，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label |
| namespace | string | 标签命名空间，决定了标签的作用域。 | default |
| value | string | 标签值，仅允许包含小写字母、中划线和数字，且开头、结尾均为小写字母或数字。 | demo-label-value |
| labelPolicy | string | 标签策略。 | NONE |
| modifierId | string | 修改人。 | app-builtin-modifier-id |
| name | string | 名称。 | app-builtin-orchestration-name |
| placeholderList | array | 占位符列表。 |  |
| \- | object | 占位符模型。 |  |
| description | string | 占位符描述。 | 内存限制 |
| name | string | 占位符名。 | memoryLimit |
| overridable | boolean | 占位符是否部署时可修改。 | true |
| predefined | boolean | 是否预置占位符。 | false |
| rsType | string | 适用的部署架构类型（如 Kubernetes、主机等），可能的值：\[KUBERNETES HOST\]。 | KUBERNETES |
| rule | string | 占位符取值的可选校验规则。 | "" |
| type | string | 占位符类型，可能的值：\[string number boolean float object\]。 | string |
| value | string | 占位符取值。 | 1024Mi |
| valueSource | string | 占位符取值的数据源类型（如常量、变量等），可能的值：\[CONSTANT VARIABLE NULL\]。 | CONSTANT |
| revision | object | 编排版本信息。 |  |
| author | string | 编排版本提交人。 | user-xxx |
| commitTime | string | 编排版本提交时间。 | 2024-09-01 00:00:00 |
| message | string | 编排版本信息 commit 信息。 | revision-message-xxx |
| sha | string | 编排版本信息 commit sha 值。 | revision-sha-xxx |
| sn | string | 唯一序列号。 | app-builtin-orchestration-1 |
| storageType | string | 存储类型。 | BUILTIN |
| suitableResourceTypes | array\[string\] | 使用资源类型。 |  |
| syncSourceTemplate | object | 编排同步源模板。 |  |
| appTemplateName | string | 应用模板名称。 | app-template-name |
| orchestrationSha | string | 应用模板版本 commit sha 值。 | app-template-version-sha |
| type | string | 类型。 | AppBuiltInOrchestration |

## **返回示例**

`{ "app": { "creatorId": "user-xxxx", "description": "app-description-xxx", "favoured": false, "gmtCreate": "2024-09-01 00:00:00", "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "name": "app-name-xxx", "type": "APP" }, "componentList": [ { "content": "---\napiVersion: v1\nkind: Service\nmetadata:\n name: prod-sidecar-test-{{ .AppStack.envName }}\n # 命名空间配置：\n # 建议每个环境使用不同的Kubernetes集群命名空间，以便达到环境隔离效果\n # 部署时云效会将占位符{{ .Values.namespace }}替换成右侧设置的实际值\n namespace: {{ .Values.namespace }}\nspec:\n selector:\n run: prod-sidecar-test-{{ .AppStack.envName }}\n ports:\n - protocol: TCP\n port: 80\n targetPort: 8080", "description": "示例描述", "kind": "Service", "name": "demo-service", "priority": 1, "type": "KUBERNETES" } ], "creatorId": "app-builtin-creator-id", "description": "app-builtin-orchestration-description", "format": "MANIFEST", "gmtCreate": "2024-09-01 00:00:00", "gmtModified": "2024-09-01 00:00:00", "groupNameMap": { }, "labelList": [ { "displayName": "测试标签键", "displayValue": "测试标签值", "extraMap": { }, "name": "demo-label", "namespace": "default", "value": "demo-label-value" } ], "labelPolicy": "NONE", "modifierId": "app-builtin-modifier-id", "name": "app-builtin-orchestration-name", "placeholderList": [ { "description": "内存限制", "name": "memoryLimit", "overridable": true, "predefined": false, "rsType": "KUBERNETES", "rule": "", "type": "string", "value": "1024Mi", "valueSource": "CONSTANT" } ], "revision": { "author": "user-xxx", "commitTime": "2024-09-01 00:00:00", "message": "revision-message-xxx", "sha": "revision-sha-xxx" }, "sn": "app-builtin-orchestration-1", "storageType": "BUILTIN", "suitableResourceTypes": [ ], "syncSourceTemplate": { "appTemplateName": "app-template-name", "orchestrationSha": "app-template-version-sha" }, "type": "AppBuiltInOrchestration" }`

## **错误码**

访问[错误码中心](https://help.aliyun.com/zh/yunxiao/developer-reference/error-code-center)查看 API 相关错误码。