---
name: create-uk8s
description: 创建 UK8S Kubernetes 集群。通过 ucloud-cli 调用 API，自动获取 VPC/Subnet/版本/镜像，生成配置并创建集群。Use when user wants to create a UK8S cluster.
argument-hint: "[cluster-name]"
allowed-tools: Bash(ucloud *), Bash(${CLAUDE_SKILL_DIR}/*), Bash(openssl *), Bash(base64 *), Bash(cat *), Bash(echo *), Bash(python3 *), Bash(which *), Bash(brew *), Read, Write, Edit, AskUserQuestion
---

# 创建 UK8S Kubernetes 集群

你正在引导用户创建一个 UK8S 集群。集群名称从 `$ARGUMENTS` 获取，若未提供则默认为 `uk8s`。

## 默认配置

```
CLUSTER_NAME = $ARGUMENTS 或 "uk8s"

# Master 节点
MASTER_MACHINE_TYPE = "O"
MASTER_CPU = 2
MASTER_MEM = 4096
MASTER_COUNT = 3
MASTER_SERIES = "o1i"

# Node 节点
NODE_MACHINE_TYPE = "O"
NODE_CPU = 4
NODE_MEM = 4096
NODE_COUNT = 2
NODE_MAX_PODS = 110

# 存储
BOOT_DISK_TYPE = "CLOUD_RSSD"
BOOT_DISK_SIZE = 40
DATA_DISK_TYPE = "CLOUD_RSSD"
DATA_DISK_SIZE = 20

# 网络
CNI_MODE = "VPC"
SERVICE_CIDR = "192.168.0.0/16"

# 其他
CHARGE_TYPE = "Dynamic"
LB_CLASS = "nlb"
KUBE_PROXY = "iptables"
EXTERNAL_API_SERVER = "Yes"
DELETE_PROTECTION = "No"
IMAGE_OS = "Ubuntu 24.04"
```

## Step 1: 检查 ucloud-cli

检查 `ucloud` 命令是否可用：

```bash
which ucloud
```

如果不存在，执行以下脚本自动检测平台并下载：

```bash
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"
curl -L "https://github.com/ucloud/ucloud-cli/releases/download/v0.3.0/ucloud-${OS}_${ARCH}.zip" -o /tmp/ucloud.zip
unzip -o /tmp/ucloud.zip -d "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/ucloud"
export PATH="$INSTALL_DIR:$PATH"
```

安装后验证：

```bash
ucloud --help
```

若网络仍慢，告知用户手动下载对应平台包：
- macOS ARM: https://github.com/ucloud/ucloud-cli/releases/download/v0.3.0/ucloud-darwin_arm64.zip
- macOS Intel: https://github.com/ucloud/ucloud-cli/releases/download/v0.3.0/ucloud-darwin_amd64.zip
- Linux amd64: https://github.com/ucloud/ucloud-cli/releases/download/v0.3.0/ucloud-linux_amd64.zip
- Linux arm64: https://github.com/ucloud/ucloud-cli/releases/download/v0.3.0/ucloud-linux_arm64.zip
- Windows amd64: https://github.com/ucloud/ucloud-cli/releases/download/v0.3.0/ucloud-windows_amd64.zip

## Step 2: 检查 CLI 配置

检查当前配置：

```bash
ucloud config list
```

需要确认以下字段已配置：
- `public_key` — 不为空
- `private_key` — 不为空
- `region` — 不为空
- `zone` — 不为空
- `project_id` — 不为空

若有缺失，使用 `AskUserQuestion` 询问用户提供对应值，然后执行：

```bash
ucloud config set --region <Region> --zone <Zone> --project-id <ProjectId>
```

**记录下 Region、Zone、ProjectId 用于后续步骤。**

## Step 3: 获取 VPC 和 Subnet

### 3.1 获取 VPC

```bash
ucloud api --Action DescribeVPC --Region <Region> --ProjectId <ProjectId>
```

从返回结果中：
- 解析 `DataSet` 数组
- 优先选择 `Tag` 为 `Default` 的 VPC
- 若无默认 VPC，用 `AskUserQuestion` 列出所有 VPC 让用户选择
- 记录 `VPCId`

### 3.2 获取 Subnet

```bash
ucloud api --Action DescribeSubnet --Region <Region> --ProjectId <ProjectId> --VPCId <VPCId>
```

从返回结果中：
- 解析 `DataSet` 数组
- 优先选择 `Tag` 为 `Default` 的 Subnet
- 若无默认 Subnet，用 `AskUserQuestion` 列出所有 Subnet 让用户选择
- 记录 `SubnetId`

## Step 4: 获取 Kubernetes 版本

调用 `GetUK8SVersions` 接口获取可用版本列表：

```bash
ucloud api --Action GetUK8SVersions --Region <Region> --ProjectId <ProjectId> --Kind Dedicated
```

响应格式：

```json
{
  "RetCode": 0,
  "Data": [
    { "K8sVersion": "1.32.8", "ContainerdVersion": "1.6.33" },
    { "K8sVersion": "1.30.14", "ContainerdVersion": "1.6.33" },
    { "K8sVersion": "1.28.15", "ContainerdVersion": "1.6.10" }
  ]
}
```

解析出第一个版本（最新）作为默认值：

```bash
ucloud api --Action GetUK8SVersions --Region <Region> --ProjectId <ProjectId> --Kind Dedicated \
  | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['Data'][0]['K8sVersion'])"
```

- 默认使用列表中第一个版本（最新）
- 记录 `K8sVersion`（必须是完整三段式，如 `1.32.8`）

若接口报错，用 `AskUserQuestion` 让用户手动输入版本号。

## Step 5: 获取镜像 ID

```bash
ucloud api --Action DescribeUK8SImage --Region <Region> --ProjectId <ProjectId>
```

从返回结果中：
- 找到 `ImageName` 包含 `Ubuntu 24.04` 或 `Ubuntu 2404` 的镜像
- 若找不到，选择最新的 Ubuntu 镜像
- 记录 `ImageId`

若接口报错，用 `AskUserQuestion` 让用户提供镜像 ID。

## Step 6: 生成密码

生成随机密码（包含大小写字母和数字，12位）：

```bash
openssl rand -base64 12 | tr -dc 'A-Za-z0-9' | head -c 12
```

然后 Base64 编码：

```bash
echo -n "<password>" | base64
```

**务必记录明文密码，最后报告给用户。**

## Step 7: 组装请求 JSON 并创建集群

使用 Write 工具将以下 JSON 写入临时文件 `/tmp/create_uk8s.json`：

```json
{
  "Action": "CreateUK8SClusterV2",
  "Region": "<Region>",
  "Zone": "<Zone>",
  "ProjectId": "<ProjectId>",
  "ClusterName": "<CLUSTER_NAME>",
  "Tag": "Default",
  "LoginMode": "Password",
  "Password": "<Base64Password>",
  "K8sVersion": "<K8sVersion>",
  "VPCId": "<VPCId>",
  "SubnetId": "<SubnetId>",
  "ExternalApiServer": "Yes",
  "MasterMachineType": "O",
  "MasterCPU": 2,
  "MasterMem": 4096,
  "MasterMinmalCpuPlatform": "Intel/CascadelakeR",
  "MasterBootDiskType": "CLOUD_RSSD",
  "MasterDataDiskType": "CLOUD_RSSD",
  "MasterDataDiskSize": 20,
  "Nodes.0.Zone": "<Zone>",
  "Nodes.0.MachineType": "O",
  "Nodes.0.MinmalCpuPlatform": "Intel/CascadelakeR",
  "Nodes.0.CPU": 4,
  "Nodes.0.Mem": 4096,
  "Nodes.0.Count": 2,
  "Nodes.0.IsolationGroup": "",
  "Nodes.0.MaxPods": 110,
  "Nodes.0.Labels.0.Key": "",
  "Nodes.0.Labels.0.Value": "",
  "Nodes.0.BootDiskType": "CLOUD_RSSD",
  "Nodes.0.DataDiskType": "CLOUD_RSSD",
  "Nodes.0.DataDiskSize": 20,
  "ImageId": "<ImageId>",
  "CNIMode": "VPC",
  "ServiceCIDR": "192.168.0.0/16",
  "ChargeType": "Dynamic",
  "LbClass": "nlb",
  "KubeProxy.Mode": "iptables",
  "Master.0.Zone": "<Zone>",
  "Master.1.Zone": "<Zone>",
  "Master.2.Zone": "<Zone>"
}
```

**重要**：用实际获取到的值替换所有 `<placeholder>`。

## Step 8: 执行创建

```bash
ucloud api --local-file /tmp/create_uk8s.json
```

检查返回结果：
- 成功：解析 `ClusterId`
- 失败：显示错误信息，分析原因并提示用户

## Step 9: 报告结果

创建成功后，向用户报告：

```
UK8S 集群创建成功！

集群名称: <CLUSTER_NAME>
集群 ID:   <ClusterId>
Region:    <Region>
Zone:      <Zone>

Master: 3 x O型 (2C/4G)
Node:   2 x O型 (4C/4G)

K8s 版本: <K8sVersion>
CNI:      VPC 模式
Service CIDR: 192.168.0.0/16

登录密码: <明文密码>
（请妥善保管此密码）

集群创建中，预计 5-10 分钟完成。
可通过以下命令查看状态：
ucloud api --Action DescribeUK8SCluster --Region <Region> --ProjectId <ProjectId> --ClusterId <ClusterId>
```

## 错误处理

- 任何 API 调用失败时，显示完整错误信息
- 分析常见错误：余额不足、配额限制、参数错误
- 提供修复建议
- 不要静默忽略任何错误

## 参考文档

- UK8S API: https://docs.ucloud.cn/api/uk8s-api/
- VPC API: https://docs.ucloud.cn/api/vpc-api/README
- ucloud-cli: https://github.com/ucloud/ucloud-cli
