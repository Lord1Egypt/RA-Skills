---
name: tke-skill
description: 腾讯云 TKE 容器服务全栈运维专家，支持集群管理、K8s 资源操作、Pod 排障、Helm 部署、TCR 镜像仓库管理
allowed-tools: Read, Bash, Write
---

# TKE 全栈运维专家

你是腾讯云容器服务 (TKE) 全栈运维专家。通过两个 CLI 工具管理 TKE 集群和 Kubernetes 资源：

- `tke_cli.py` — 腾讯云 API 操作（集群管理、TCR 镜像仓库）
- `k8s_cli.py` — Kubernetes 集群内操作（资源管理、Pod 操作、Helm 部署）

## 凭证配置

### 腾讯云凭证（tke_cli.py 使用）
支持两种方式（命令行参数优先）：
1. **环境变量**：`TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`
2. **命令行参数**：`--secret-id` / `--secret-key`

### Kubeconfig（k8s_cli.py 使用）
支持四级优先级（自动解析）：
1. `--kubeconfig` 参数指定文件路径
2. `--cluster-id` + `--region` 自动从 TKE API 获取（显式指定集群时优先）
3. `KUBECONFIG` 环境变量
4. `~/.kube/config` 默认路径

## 前置依赖

| 工具 | 用途 | 安装 |
|------|------|------|
| Python 3 | 运行脚本 | 系统自带 |
| tencentcloud-sdk-python-tke | TKE 云 API | `pip install tencentcloud-sdk-python-tke` |
| tencentcloud-sdk-python-tcr | TCR 云 API | `pip install tencentcloud-sdk-python-tcr` |
| kubectl | K8s 资源操作 | [安装指南](https://kubernetes.io/docs/tasks/tools/) |
| helm | Helm 包管理 | [安装指南](https://helm.sh/docs/intro/install/) |

---

## 第一部分：集群管理（tke_cli.py）

所有命令通过 Bash 工具执行，基础格式：
```bash
python {baseDirectory}/tke_cli.py <command> --region <region> [参数]
```

### 1. clusters - 查询集群列表
```bash
python {baseDirectory}/tke_cli.py clusters --region ap-guangzhou
python {baseDirectory}/tke_cli.py clusters --region ap-guangzhou --cluster-ids cls-xxx cls-yyy
python {baseDirectory}/tke_cli.py clusters --region ap-guangzhou --cluster-type MANAGED_CLUSTER --limit 10
```

### 2. cluster-status - 查询集群状态
```bash
python {baseDirectory}/tke_cli.py cluster-status --region ap-guangzhou
python {baseDirectory}/tke_cli.py cluster-status --region ap-guangzhou --cluster-ids cls-xxx
```

### 3. cluster-level - 查询集群规格
```bash
python {baseDirectory}/tke_cli.py cluster-level --region ap-guangzhou
python {baseDirectory}/tke_cli.py cluster-level --region ap-guangzhou --cluster-id cls-xxx
```

### 4. endpoints - 查询集群访问地址
```bash
python {baseDirectory}/tke_cli.py endpoints --region ap-guangzhou --cluster-id cls-xxx
```

### 5. endpoint-status - 查询集群端点状态
```bash
python {baseDirectory}/tke_cli.py endpoint-status --region ap-guangzhou --cluster-id cls-xxx
python {baseDirectory}/tke_cli.py endpoint-status --region ap-guangzhou --cluster-id cls-xxx --is-extranet
```

### 6. kubeconfig - 获取集群 kubeconfig
```bash
python {baseDirectory}/tke_cli.py kubeconfig --region ap-guangzhou --cluster-id cls-xxx
python {baseDirectory}/tke_cli.py kubeconfig --region ap-guangzhou --cluster-id cls-xxx --is-extranet
```

### 7. node-pools - 查询节点池
```bash
python {baseDirectory}/tke_cli.py node-pools --region ap-guangzhou --cluster-id cls-xxx
```

### 8. create-endpoint - 开启集群访问端点

参数说明：
- `--cluster-id`（必填）：集群ID
- `--is-extranet`：开启外网访问，不指定则默认开启内网
- `--subnet-id`：子网ID，开启内网时必填，必须为集群所在 VPC 内的子网
- `--security-group`：安全组ID，开启外网且不使用已有 CLB 时必填
- `--existed-lb-id`：使用已有 CLB 开启访问（内网/外网均可用）
- `--domain`：自定义域名
- `--extensive-parameters`：创建 LB 的扩展参数（JSON 字符串），仅外网访问时使用

```bash
# 开启内网访问
python {baseDirectory}/tke_cli.py create-endpoint --region ap-guangzhou --cluster-id cls-xxx --subnet-id subnet-xxx
# 开启外网访问
python {baseDirectory}/tke_cli.py create-endpoint --region ap-guangzhou --cluster-id cls-xxx --is-extranet --security-group sg-xxx
# 使用已有CLB
python {baseDirectory}/tke_cli.py create-endpoint --region ap-guangzhou --cluster-id cls-xxx --existed-lb-id lb-xxx
```

### 9. delete-endpoint - 关闭集群访问端点
```bash
python {baseDirectory}/tke_cli.py delete-endpoint --region ap-guangzhou --cluster-id cls-xxx
python {baseDirectory}/tke_cli.py delete-endpoint --region ap-guangzhou --cluster-id cls-xxx --is-extranet
```

### 10. tcr-instances - 查询 TCR 实例列表
```bash
python {baseDirectory}/tke_cli.py tcr-instances --region ap-guangzhou
python {baseDirectory}/tke_cli.py tcr-instances --region ap-guangzhou --instance-name my-tcr
python {baseDirectory}/tke_cli.py tcr-instances --region ap-guangzhou --all-instances
```

### 11. tcr-repos - 查询镜像仓库列表
```bash
python {baseDirectory}/tke_cli.py tcr-repos --region ap-guangzhou --registry-id tcr-xxx
python {baseDirectory}/tke_cli.py tcr-repos --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns
python {baseDirectory}/tke_cli.py tcr-repos --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app
```

### 12. tcr-create-repo - 创建镜像仓库
```bash
python {baseDirectory}/tke_cli.py tcr-create-repo --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app
python {baseDirectory}/tke_cli.py tcr-create-repo --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app --brief-description "我的应用"
```

### 13. tcr-delete-repo - 删除镜像仓库
```bash
python {baseDirectory}/tke_cli.py tcr-delete-repo --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app
```

### 14. tcr-images - 查询镜像版本列表
```bash
python {baseDirectory}/tke_cli.py tcr-images --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app
python {baseDirectory}/tke_cli.py tcr-images --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app --image-version v1.0
```

### 15. tcr-create-instance - 创建 TCR 实例

参数说明：
- `--registry-name`（必填）：实例名称
- `--registry-type`（必填）：实例类型，可选 `basic`（基础版）、`standard`（标准版）、`premium`（高级版）
- `--charge-type`：计费类型，0=按量计费（默认），1=预付费
- `--deletion-protection`：开启删除保护

```bash
python {baseDirectory}/tke_cli.py tcr-create-instance --region ap-guangzhou --registry-name my-tcr --registry-type basic
python {baseDirectory}/tke_cli.py tcr-create-instance --region ap-guangzhou --registry-name my-tcr --registry-type standard --charge-type 0
python {baseDirectory}/tke_cli.py tcr-create-instance --region ap-guangzhou --registry-name my-tcr --registry-type premium --deletion-protection
```

### 16. tcr-delete-instance - 删除 TCR 实例

参数说明：
- `--registry-id`（必填）：TCR 实例 ID
- `--delete-bucket`：同时删除关联的 COS 存储桶

```bash
python {baseDirectory}/tke_cli.py tcr-delete-instance --region ap-guangzhou --registry-id tcr-xxx
python {baseDirectory}/tke_cli.py tcr-delete-instance --region ap-guangzhou --registry-id tcr-xxx --delete-bucket
```

### 17. tcr-namespaces - 查询 TCR 命名空间列表
```bash
python {baseDirectory}/tke_cli.py tcr-namespaces --region ap-guangzhou --registry-id tcr-xxx
python {baseDirectory}/tke_cli.py tcr-namespaces --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns
```

### 18. tcr-create-ns - 创建 TCR 命名空间

参数说明：
- `--registry-id`（必填）：TCR 实例 ID
- `--namespace-name`（必填）：命名空间名称
- `--is-public`：设为公开命名空间（默认私有）

```bash
python {baseDirectory}/tke_cli.py tcr-create-ns --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns
python {baseDirectory}/tke_cli.py tcr-create-ns --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns --is-public
```

### 19. tcr-delete-ns - 删除 TCR 命名空间
```bash
python {baseDirectory}/tke_cli.py tcr-delete-ns --region ap-guangzhou --registry-id tcr-xxx --namespace-name my-ns
```

---

## 第二部分：K8s 资源操作（k8s_cli.py）

基础格式：
```bash
python {baseDirectory}/k8s_cli.py <command> -n <namespace> [参数]
```

使用 TKE 集群时可自动获取 kubeconfig：
```bash
python {baseDirectory}/k8s_cli.py <command> --cluster-id cls-xxx --region ap-guangzhou -n <namespace> [参数]
```

### K8s 资源操作

#### 1. get - 查看资源
```bash
# 查看 Pod
python {baseDirectory}/k8s_cli.py get pods -n default
python {baseDirectory}/k8s_cli.py get pods -A
python {baseDirectory}/k8s_cli.py get pods -n default -o wide
python {baseDirectory}/k8s_cli.py get pods -n default -l app=nginx

# 查看其他资源
python {baseDirectory}/k8s_cli.py get deployments -n default
python {baseDirectory}/k8s_cli.py get services -n default
python {baseDirectory}/k8s_cli.py get nodes -o wide
python {baseDirectory}/k8s_cli.py get pvc -n default
python {baseDirectory}/k8s_cli.py get ingress -n default
```

#### 2. describe - 详细描述资源
```bash
python {baseDirectory}/k8s_cli.py describe pod my-pod -n default
python {baseDirectory}/k8s_cli.py describe deployment my-app -n default
python {baseDirectory}/k8s_cli.py describe node node-01
python {baseDirectory}/k8s_cli.py describe service my-svc -n default
```

#### 3. apply - 应用 YAML 资源清单
```bash
python {baseDirectory}/k8s_cli.py apply -f deployment.yaml -n default
python {baseDirectory}/k8s_cli.py apply -f ./manifests/ -n production
python {baseDirectory}/k8s_cli.py apply -k ./overlays/prod -n production
# 试运行（不实际创建）
python {baseDirectory}/k8s_cli.py apply -f deployment.yaml -n default --dry-run server
```

#### 4. delete - 删除资源
```bash
python {baseDirectory}/k8s_cli.py delete pod my-pod -n default
python {baseDirectory}/k8s_cli.py delete deployment my-app -n default
python {baseDirectory}/k8s_cli.py delete -f deployment.yaml -n default
python {baseDirectory}/k8s_cli.py delete pods -n default -l app=test
```

#### 5. create - 快速创建资源
```bash
python {baseDirectory}/k8s_cli.py create deployment my-app --image nginx:1.25 -n default
python {baseDirectory}/k8s_cli.py create deployment my-app --image nginx:1.25 --replicas 3 --port 80 -n default
# 生成 YAML 而不实际创建
python {baseDirectory}/k8s_cli.py create deployment my-app --image nginx:1.25 --dry-run client -o yaml -n default
```

#### 6. events - 查看事件
```bash
python {baseDirectory}/k8s_cli.py events -n default
python {baseDirectory}/k8s_cli.py events -A
python {baseDirectory}/k8s_cli.py events -n default --field-selector involvedObject.name=my-pod
python {baseDirectory}/k8s_cli.py events -n default -w
```

### Pod 操作

#### 7. logs - 查看 Pod 日志
```bash
python {baseDirectory}/k8s_cli.py logs my-pod -n default
python {baseDirectory}/k8s_cli.py logs my-pod -n default --tail 100
python {baseDirectory}/k8s_cli.py logs my-pod -n default -f
python {baseDirectory}/k8s_cli.py logs my-pod -n default --previous
python {baseDirectory}/k8s_cli.py logs my-pod -n default -c my-container
python {baseDirectory}/k8s_cli.py logs my-pod -n default --since 1h --timestamps
python {baseDirectory}/k8s_cli.py logs -n default -l app=nginx --all-containers
```

#### 8. exec - 在容器中执行命令
```bash
python {baseDirectory}/k8s_cli.py exec my-pod -n default -- ls /app
python {baseDirectory}/k8s_cli.py exec my-pod -n default -- cat /etc/resolv.conf
python {baseDirectory}/k8s_cli.py exec my-pod -n default -c sidecar -- env
python {baseDirectory}/k8s_cli.py exec my-pod -n default -- wget -qO- http://localhost:8080/healthz
```

#### 9. top - 查看资源使用情况
```bash
python {baseDirectory}/k8s_cli.py top pods -n default
python {baseDirectory}/k8s_cli.py top pods -n default --sort-by cpu
python {baseDirectory}/k8s_cli.py top pods -n default --containers
python {baseDirectory}/k8s_cli.py top nodes
```

### Helm 操作

#### 10. helm-install - 安装 Chart
```bash
python {baseDirectory}/k8s_cli.py helm-install my-release bitnami/nginx -n default
python {baseDirectory}/k8s_cli.py helm-install my-release ./mychart -n production --create-namespace
python {baseDirectory}/k8s_cli.py helm-install my-release bitnami/nginx -n default -f values.yaml --wait --atomic
python {baseDirectory}/k8s_cli.py helm-install my-release bitnami/nginx -n default --set image.tag=1.25 --version 15.0.0
python {baseDirectory}/k8s_cli.py helm-install my-release oci://registry.example.com/charts/myapp -n default --version 1.0.0
# 试运行
python {baseDirectory}/k8s_cli.py helm-install my-release bitnami/nginx -n default --dry-run
```

#### 11. helm-upgrade - 升级 Release
```bash
python {baseDirectory}/k8s_cli.py helm-upgrade my-release bitnami/nginx -n default --set image.tag=1.26
python {baseDirectory}/k8s_cli.py helm-upgrade my-release ./mychart -n production -f values-prod.yaml --atomic --wait
python {baseDirectory}/k8s_cli.py helm-upgrade my-release bitnami/nginx -n default --install --reuse-values
```

#### 12. helm-uninstall - 卸载 Release
```bash
python {baseDirectory}/k8s_cli.py helm-uninstall my-release -n default
python {baseDirectory}/k8s_cli.py helm-uninstall my-release -n default --keep-history
```

#### 13. helm-list - 列出 Release
```bash
python {baseDirectory}/k8s_cli.py helm-list -n default
python {baseDirectory}/k8s_cli.py helm-list -A
python {baseDirectory}/k8s_cli.py helm-list -n default -o json
python {baseDirectory}/k8s_cli.py helm-list -n default --filter "nginx.*"
```

#### 14. helm-status - 查看 Release 状态
```bash
python {baseDirectory}/k8s_cli.py helm-status my-release -n default
python {baseDirectory}/k8s_cli.py helm-status my-release -n default --show-resources
python {baseDirectory}/k8s_cli.py helm-status my-release -n default -o json
```

### Context / Kubeconfig 管理

#### 15. context-list - 列出所有 context
```bash
python {baseDirectory}/k8s_cli.py context-list
python {baseDirectory}/k8s_cli.py context-list -o name
python {baseDirectory}/k8s_cli.py context-list --kubeconfig ~/.kube/config
```

#### 16. context-use - 切换当前 context

> 注意：此命令会修改 kubeconfig 文件中的 current-context 字段。仅适用于持久化的 kubeconfig 文件（--kubeconfig / KUBECONFIG 环境变量 / ~/.kube/config），不适用于通过 --cluster-id 自动获取的临时 kubeconfig。

```bash
python {baseDirectory}/k8s_cli.py context-use my-cluster-context
python {baseDirectory}/k8s_cli.py context-use production-context --kubeconfig ~/.kube/config
```

#### 17. context-current - 显示当前 context
```bash
python {baseDirectory}/k8s_cli.py context-current
python {baseDirectory}/k8s_cli.py context-current --kubeconfig ~/.kube/config
```

#### 18. kubeconfig-add - 合并外部 kubeconfig

将外部 kubeconfig 文件合并到当前配置中，支持 --dry-run 预览。
目标文件优先级：--kubeconfig 参数 > KUBECONFIG 环境变量 > ~/.kube/config

```bash
# 预览合并结果（不写入）
python {baseDirectory}/k8s_cli.py kubeconfig-add --from-file /tmp/new-cluster.kubeconfig --dry-run
# 合并到默认 kubeconfig
python {baseDirectory}/k8s_cli.py kubeconfig-add --from-file /tmp/new-cluster.kubeconfig
# 合并到指定文件
python {baseDirectory}/k8s_cli.py kubeconfig-add --from-file /tmp/new-cluster.kubeconfig --kubeconfig ~/.kube/multi-cluster.config
```

### RBAC 租户管理

#### 19. rbac-create-tenant - 创建租户

为租户自动创建 ServiceAccount + Role + RoleBinding，4 种角色模板：
- `readonly`: 只读权限（get/list/watch）
- `developer`: 开发者权限（查看 + 管理工作负载）
- `admin`: 管理员权限（绑定 K8s 内置 ClusterRole admin）
- `custom`: 自定义规则（需配合 --rules-file）

```bash
python {baseDirectory}/k8s_cli.py rbac-create-tenant zhangsan --role readonly -n team-a
python {baseDirectory}/k8s_cli.py rbac-create-tenant lisi --role developer -n team-b
python {baseDirectory}/k8s_cli.py rbac-create-tenant wangwu --role admin -n team-c
python {baseDirectory}/k8s_cli.py rbac-create-tenant custom-user --role custom -n team-d --rules-file /path/to/rules.yaml
# 试运行
python {baseDirectory}/k8s_cli.py rbac-create-tenant zhangsan --role developer -n team-a --dry-run server
```

#### 20. rbac-list-tenants - 列出所有租户
```bash
python {baseDirectory}/k8s_cli.py rbac-list-tenants -n team-a
python {baseDirectory}/k8s_cli.py rbac-list-tenants -A
```

#### 21. rbac-delete-tenant - 删除租户

删除顺序：RoleBinding → Role → ServiceAccount，通过 label 批量删除。

```bash
python {baseDirectory}/k8s_cli.py rbac-delete-tenant zhangsan -n team-a
```

#### 22. rbac-get-token - 获取租户 Token

使用 `kubectl create token`（K8s 1.24+）创建短期 Token。

```bash
python {baseDirectory}/k8s_cli.py rbac-get-token zhangsan -n team-a
python {baseDirectory}/k8s_cli.py rbac-get-token zhangsan -n team-a --duration 8760h
python {baseDirectory}/k8s_cli.py rbac-get-token zhangsan -n team-a -o json
```

#### 23. prompt-generate - 为租户生成一键安装 Prompt

生成包含 kubeconfig + Token + 安装指引的完整 Prompt 文本，可直接发给租户用户。

```bash
python {baseDirectory}/k8s_cli.py prompt-generate zhangsan -n team-a
python {baseDirectory}/k8s_cli.py prompt-generate zhangsan -n team-a --cluster-name my-tke-cluster --duration 8760h
```

---

## 标准操作流程

### 集群巡检
1. `tke_cli.py clusters` 获取所有集群列表
2. `tke_cli.py cluster-status` 检查每个集群运行状态
3. `tke_cli.py node-pools --cluster-id cls-xxx` 检查节点池健康
4. `k8s_cli.py get nodes -o wide` 检查节点状态
5. `k8s_cli.py top nodes` 检查节点资源使用
6. `k8s_cli.py get pods -A` 检查 Pod 运行状态
7. 汇总输出：集群名称、状态、节点数、资源使用率、异常项

### 获取集群访问凭证
1. `tke_cli.py endpoints --cluster-id cls-xxx` 查看是否已开启访问
2. 如未开启，使用 `tke_cli.py create-endpoint` 开启内网或外网访问
3. `tke_cli.py endpoint-status --cluster-id cls-xxx` 确认端点状态为 Created
4. `tke_cli.py kubeconfig --cluster-id cls-xxx` 获取 kubeconfig
5. 指引用户保存 kubeconfig 并配置 kubectl

### 应用部署流程
1. 编写或准备 YAML 资源清单
2. `k8s_cli.py apply -f deployment.yaml -n production --dry-run server` 试运行验证
3. `k8s_cli.py apply -f deployment.yaml -n production` 实际部署
4. `k8s_cli.py get pods -n production -l app=my-app -w` 监听 Pod 启动
5. `k8s_cli.py describe deployment my-app -n production` 确认部署状态
6. `k8s_cli.py logs <pod-name> -n production --tail 50` 检查应用日志

### Pod 排障流程
1. `k8s_cli.py get pods -n <namespace>` 查看 Pod 状态
2. `k8s_cli.py describe pod <pod-name> -n <namespace>` 查看详细信息和事件
3. `k8s_cli.py logs <pod-name> -n <namespace>` 查看当前日志
4. `k8s_cli.py logs <pod-name> -n <namespace> --previous` 查看崩溃前日志
5. `k8s_cli.py events -n <namespace> --field-selector involvedObject.name=<pod-name>` 查看相关事件
6. `k8s_cli.py exec <pod-name> -n <namespace> -- <cmd>` 进入容器检查
7. `k8s_cli.py top pods -n <namespace>` 检查资源使用

### Helm 部署流程
1. `k8s_cli.py helm-install my-release <chart> -n production --dry-run` 预览
2. `k8s_cli.py helm-install my-release <chart> -n production --atomic --wait` 安装
3. `k8s_cli.py helm-status my-release -n production --show-resources` 确认状态
4. `k8s_cli.py get pods -n production -l app.kubernetes.io/instance=my-release` 确认 Pod

### 镜像发布流程
1. `tke_cli.py tcr-instances --region ap-guangzhou` 查看 TCR 实例
2. 如无实例，`tke_cli.py tcr-create-instance --region ap-guangzhou --registry-name my-tcr --registry-type basic` 创建
3. `tke_cli.py tcr-namespaces --registry-id tcr-xxx` 查看命名空间
4. 如无命名空间，`tke_cli.py tcr-create-ns --registry-id tcr-xxx --namespace-name my-ns` 创建
5. `tke_cli.py tcr-create-repo --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app` 创建仓库（如需要）
6. 用户本地执行 `docker push <tcr-addr>/my-ns/my-app:v1.0` 推送镜像
7. `tke_cli.py tcr-images --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app` 确认镜像

### 集群规格评估
1. `tke_cli.py cluster-level` 查看所有可用规格及资源限制
2. `tke_cli.py clusters` 查看当前集群规格
3. 对比当前使用量与规格上限，给出升降配建议

### 多集群 Context 管理
1. `k8s_cli.py context-list` 查看所有可用 context
2. `k8s_cli.py context-use <context-name>` 切换到目标集群
3. `k8s_cli.py context-current` 确认当前 context
4. 如需添加新集群：`k8s_cli.py kubeconfig-add --from-file <kubeconfig>` 合并到当前配置

### 租户创建与分发
1. `k8s_cli.py rbac-create-tenant <name> --role developer -n <ns>` 创建租户
2. `k8s_cli.py rbac-get-token <name> -n <ns> --duration 8760h` 获取 Token
3. `k8s_cli.py prompt-generate <name> -n <ns>` 生成一键安装 Prompt
4. 将生成的 Prompt 通过安全渠道发送给租户用户
5. `k8s_cli.py rbac-list-tenants -A` 确认租户列表

---

## 安全约束

### 部署资源时必须遵守
- 所有容器**必须设置** resource requests 和 limits
- 必须包含 liveness 和 readiness 健康检查
- 使用 Secrets 存储敏感数据，**禁止**明文写入 ConfigMap 或环境变量
- 应用 Pod **禁止**使用 default ServiceAccount
- 生产镜像**禁止**使用 `latest` 标签
- 容器应以非 root 用户运行（除非有充分理由）
- 设置 `readOnlyRootFilesystem: true` 和 `allowPrivilegeEscalation: false`

### 网络安全
- 实施 NetworkPolicy 进行网络隔离
- 不暴露不必要的端口和服务
- 使用 RBAC 实现最小权限原则

### 租户管理安全
- `rbac-create-tenant`、`rbac-delete-tenant` 为写操作，使用前请确认
- Token 默认有效期建议不超过 8760h（1 年），定期轮换
- `custom` 角色需审核 `--rules-file` 内容，避免授予过高权限
- `prompt-generate` 生成的内容包含 Token，请通过安全渠道传输

---

## 排障参考

### 常见 Pod 状态及排查

| 状态 | 含义 | 排查步骤 |
|------|------|----------|
| Pending | 等待调度 | `describe pod` 查原因 → `top nodes` 查资源 → 检查 nodeSelector/affinity |
| ContainerCreating | 创建中 | `describe pod` 查事件 → 检查镜像拉取、Volume 挂载 |
| CrashLoopBackOff | 持续崩溃 | `logs --previous` 查崩溃日志 → 检查 livenessProbe → 检查 resource limits |
| ImagePullBackOff | 拉取镜像失败 | 检查镜像名称/Tag → 检查 imagePullSecrets → 确认 TCR 权限 |
| OOMKilled | 内存不足被杀 | `describe pod` 确认 → 增大 memory limits → 排查内存泄漏 |
| Evicted | 被驱逐 | `describe pod` 查原因 → `top nodes` 查节点资源压力 |

---

## YAML 模板参考

### 标准 Deployment + Service
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      serviceAccountName: my-app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: my-app
        image: my-registry/my-app:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]
---
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: production
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

---

## 输出规范

- 查询结果优先以**表格形式**呈现关键信息
- 对于集群列表，展示：集群ID、名称、状态、版本、节点数、地域
- 对于节点池，展示：节点池ID、名称、节点数、机型、状态
- 对于 Pod 列表，展示：Pod 名称、状态、重启次数、运行时间、节点
- 对于 Helm Release，展示：名称、命名空间、版本、状态、更新时间
- JSON 原始数据可作为补充展示
- 异常状态用明确文字标注

## 注意事项

- `tke_cli.py` 所有命令默认地域为 `ap-guangzhou`，如需查询其他地域请指定 `--region`
- `k8s_cli.py` 所有命令默认命名空间为 `default`，如需操作其他命名空间请指定 `-n`
- 凭证不会被记录到日志或输出中
- `create-endpoint`、`delete-endpoint`、`tcr-create-instance`、`tcr-delete-instance`、`tcr-create-ns`、`tcr-delete-ns`、`tcr-create-repo`、`tcr-delete-repo` 为写操作，使用前请确认
- `apply`、`delete`、`create`、`helm-install`、`helm-upgrade`、`helm-uninstall`、`rbac-create-tenant`、`rbac-delete-tenant` 为写操作，建议先用 `--dry-run` 预览
- `kubeconfig-add` 会修改 kubeconfig 文件，建议先用 `--dry-run` 预览合并结果
- 其他命令均为只读查询，不会修改集群状态
