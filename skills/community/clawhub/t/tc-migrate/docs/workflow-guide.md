# tc-migrate 工作流指南

本文档详细说明 tc-migrate 工具的标准执行流程，包括每个命令的作用、执行顺序以及生成的文件。

---

## 一、快速开始（标准四步流程）

```bash
# Step 1: 全自动配置（从 account.yaml 读取密钥，自动查询 API 生成配置）
tc-migrate config auto

# Step 2: 扫描源账号资源（CLB/NAT/CVM/SG）并保存到配置文件
tc-migrate scan --save --skip-empty-vpc

# Step 3: 生成 Terraform 变量文件
tc-migrate generate

# Step 4: 一键执行 Terraform 全流程
tc-migrate run
```

---

## 二、执行流程图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          tc-migrate 工作流程                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  前提: 准备好 account.yaml（包含源/目标账号的 SecretId/SecretKey/Region）

                    ┌─────────────────────────┐
                    │  tc-migrate config auto  │  ← Step 1: 全自动配置
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   生成 tc-migrate.yaml   │  ← 输出文件
                    │   (VPC/子网/账号信息)    │
                    └───────────┬─────────────┘
                                │
                                ▼
         ┌──────────────────────────────────────────────┐
         │  tc-migrate scan --save --skip-empty-vpc     │  ← Step 2: 资源扫描
         └───────────────────┬──────────────────────────┘
                             │
                             ▼
                    ┌─────────────────────────┐
                    │  更新 tc-migrate.yaml    │  ← 追加 resources 配置
                    │  (CLB/NAT/CVM/SG 信息)   │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   tc-migrate generate    │  ← Step 3: 生成 tfvars
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │ 生成 terraform.tfvars    │  ← 输出文件
                    │ (Terraform 变量文件)     │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │     tc-migrate run       │  ← Step 4: 执行迁移
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
              ▼                                   ▼
     ┌────────────────┐                 ┌─────────────────┐
     │ terraform init │                 │ terraform plan  │
     └────────────────┘                 └─────────┬───────┘
                                                  │
                                                  ▼
                                        ┌─────────────────┐
                                        │ terraform apply │
                                        └─────────┬───────┘
                                                  │
                                                  ▼
                                        ┌─────────────────────┐
                                        │   云资源创建完成     │
                                        │ (VPC/CCN/CLB/NAT/   │
                                        │  CVM/SG 等)         │
                                        └─────────────────────┘
```

---

## 三、各命令详解

### Step 1: `tc-migrate config auto`

**作用**：全自动配置，通过腾讯云 API 自动查询账号信息并生成迁移配置文件。

**前提条件**：
- 当前目录存在 `account.yaml` 文件，包含源/目标账号的密钥和地域

**执行过程**：
1. 从 `account.yaml` 读取密钥信息（SecretId、SecretKey、Region）
2. 调用腾讯云 API 查询源账号 UIN
3. 调用腾讯云 API 查询目标账号 UIN
4. 查询源账号指定地域下的所有 VPC
5. 查询每个 VPC 下的所有子网
6. 自动分配目标端 CIDR（如果配置了 `target_cidr`）
7. 自动扫描资源（默认开启，可用 `--no-scan` 关闭）

**生成文件**：

| 文件 | 路径 | 说明 |
|------|------|------|
| `tc-migrate.yaml` | 当前目录 | 迁移配置文件，包含 VPC/子网/账号信息 |

**配置文件结构**：
```yaml
# tc-migrate.yaml 结构
region_a: "ap-beijing"        # 源账号地域
region_b: "ap-guangzhou"      # 目标账号地域

account_a:                    # 源账号信息
  secret_id: "AKID..."
  secret_key: "..."
  uin: "100012345678"         # 自动查询填充

account_b:                    # 目标账号信息
  secret_id: "AKID..."
  secret_key: "..."
  uin: "100087654321"         # 自动查询填充

vpcs:                         # VPC 配置（自动发现）
  vpc-xxx:
    account_a_vpc_id: "vpc-xxx"
    account_b_vpc_name: "vpc-b-xxx"
    account_b_vpc_cidr: "172.16.0.0/16"
    account_b_subnets:
      - name: "subnet-xxx"
        cidr: "172.16.1.0/24"
        az: "ap-guangzhou-3"

tags:                         # 统一标签
  managed-by: "Terraform"
  business-id: "cross-account-migration"
  environment: "migration"
```

**常用选项**：
```bash
# 全自动配置（默认会自动扫描资源）
tc-migrate config auto

# 不自动扫描资源
tc-migrate config auto --no-scan

# 跳过空 VPC（无资源的 VPC 不纳入迁移）
tc-migrate config auto --skip-empty-vpc

# 指定目标网段自动分配
tc-migrate config auto --target-cidr 172.16.0.0/12

# 覆盖已有配置文件
tc-migrate config auto --force
```

---

### Step 2: `tc-migrate scan --save --skip-empty-vpc`

**作用**：扫描源账号中的云资源（CLB、NAT、CVM、SG），并将结果保存到配置文件。

**执行过程**：
1. 读取 `tc-migrate.yaml` 获取源账号密钥和 VPC 列表
2. 自动补全 UIN（如果之前未填写）
3. 按顺序扫描各类资源：
   - **SG（安全组）**：扫描 VPC 关联的安全组及规则
   - **CLB（负载均衡）**：扫描 VPC 下的 CLB 实例及监听器
   - **NAT（NAT 网关）**：扫描 VPC 下的 NAT 网关
   - **CVM（云服务器）**：扫描 VPC 下的 CVM 实例
4. 过滤掉空 VPC（如果使用 `--skip-empty-vpc`）
5. 将扫描结果写入 `tc-migrate.yaml` 的 `resources` 部分

**更新文件**：

| 文件 | 变化 |
|------|------|
| `tc-migrate.yaml` | 追加 `resources` 配置块（CLB/NAT/CVM/SG 信息） |

**追加的配置结构**：
```yaml
# tc-migrate.yaml 追加的 resources 部分
resources:
  sg:                           # 安全组配置
    enabled: true
    security_groups:
      sg-xxx:
        name: "migrated-sg-xxx"
        vpc_key: "vpc-xxx"
        ingress_rules: [...]
        egress_rules: [...]

  clb:                          # CLB 配置
    enabled: true
    instances:
      clb-xxx:
        name: "migrated-clb-xxx"
        load_balancer_type: "OPEN"
        vpc_key: "vpc-xxx"
        listeners: [...]

  nat:                          # NAT 网关配置
    enabled: true
    gateways:
      nat-xxx:
        name: "migrated-nat-xxx"
        vpc_key: "vpc-xxx"
        bandwidth: 100

  cvm:                          # CVM 配置
    enabled: true
    instances:
      cvm-xxx:
        name: "migrated-cvm-xxx"
        instance_type: "S5.MEDIUM4"
        vpc_key: "vpc-xxx"
        subnet_index: 0
```

**常用选项**：
```bash
# 扫描所有资源类型
tc-migrate scan --save

# 扫描所有资源并跳过空 VPC
tc-migrate scan --save --skip-empty-vpc

# 仅扫描指定类型
tc-migrate scan -r clb -r nat --save

# 仅预览扫描结果（不保存）
tc-migrate scan
```

---

### Step 3: `tc-migrate generate`

**作用**：根据 `tc-migrate.yaml` 配置文件生成 Terraform 变量文件 `terraform.tfvars`。

**执行过程**：
1. 读取并校验 `tc-migrate.yaml` 配置
2. 从 `account.yaml` 合并密钥信息
3. 渲染基础部分（账号认证、VPC、CCN 配置）
4. 渲染各资源插件的配置（CLB、NAT、CVM、SG）
5. 写入 `terraform.tfvars` 文件

**生成文件**：

| 文件 | 路径 | 说明 |
|------|------|------|
| `terraform.tfvars` | `terraform-cross-account/` 目录 | Terraform 变量文件 |

**生成的文件结构**：
```hcl
# terraform.tfvars 结构

# ── 账号认证 ──
secret_id_a  = "AKID..."
secret_key_a = "..."
uin_a        = "100012345678"
region_a     = "ap-beijing"

secret_id_b  = "AKID..."
secret_key_b = "..."
uin_b        = "100087654321"
region_b     = "ap-guangzhou"

# ── CCN 配置 ──
ccn_name                       = "ccn-cross-account-migration"
ccn_charge_type                = "PREPAID"
ccn_qos                        = "AU"
ccn_bandwidth_limit_type       = "INTER_REGION_LIMIT"
ccn_bandwidth                  = 1
configure_cross_region_bandwidth = false

# ── VPC 配置 ──
vpcs = {
  vpc-xxx = {
    account_a_vpc_id   = "vpc-xxx"
    account_b_vpc_name = "vpc-b-xxx"
    account_b_vpc_cidr = "172.16.0.0/16"
    account_b_subnets  = [...]
    account_b_sg_name  = "sg-b-xxx"
  }
}

# ── 标签 ──
tags = {
  managed-by  = "Terraform"
  business-id = "cross-account-migration"
  environment = "migration"
}

# ── 安全组 ──
security_groups = {
  sg-xxx = {
    name        = "migrated-sg-xxx"
    vpc_key     = "vpc-xxx"
    ingress_rules = [...]
    egress_rules  = [...]
  }
}

# ── CLB ──
clb_instances = {
  clb-xxx = {
    name               = "migrated-clb-xxx"
    load_balancer_type = "OPEN"
    vpc_key            = "vpc-xxx"
    listeners          = [...]
  }
}

# ── NAT 网关 ──
nat_gateways = {
  nat-xxx = {
    name      = "migrated-nat-xxx"
    vpc_key   = "vpc-xxx"
    bandwidth = 100
  }
}

# ── CVM ──
cvm_instances = {
  cvm-xxx = {
    name          = "migrated-cvm-xxx"
    instance_type = "S5.MEDIUM4"
    vpc_key       = "vpc-xxx"
    subnet_index  = 0
  }
}
```

**常用选项**：
```bash
# 生成 tfvars 文件
tc-migrate generate

# 仅预览生成内容（不写入文件）
tc-migrate generate --preview

# 强制覆盖已有文件
tc-migrate generate --force
```

---

### Step 4: `tc-migrate run`

**作用**：一键执行完整的 Terraform 流程，创建所有云资源。

**执行过程**：

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1/4 | `generate_tfvars()` | 生成/更新 `terraform.tfvars` |
| 2/4 | `terraform init` | 初始化 Terraform，下载 Provider |
| 3/4 | `terraform plan` | 生成执行计划，输出到 `tfplan` |
| 4/4 | `terraform apply` | 执行计划，创建云资源 |

**生成/更新文件**：

| 文件/目录 | 说明 |
|-----------|------|
| `terraform.tfvars` | Terraform 变量文件（每次 run 都会重新生成） |
| `tfplan` | Terraform 执行计划文件 |
| `.terraform/` | Terraform 工作目录（Provider 缓存等） |
| `.terraform.lock.hcl` | Provider 版本锁定文件 |
| `terraform.tfstate` | Terraform 状态文件（记录已创建的资源） |

**创建的云资源**：

```
账号B（目标账号）创建的资源：
├── VPC（虚拟私有网络）
│   ├── 子网（Subnet）
│   └── 路由表（Route Table）
├── 安全组（Security Group）
│   └── 安全组规则（Ingress/Egress Rules）
├── CCN（云联网）
│   ├── CCN 路由表（每对 VPC 独立）
│   ├── 路由接收策略（只接收 pair 内 VPC 的路由）
│   └── VPC 关联（跨账号关联）
├── CLB（负载均衡）
│   └── 监听器（Listener）
├── NAT 网关
│   └── EIP（弹性公网 IP）
└── CVM（云服务器）
    ├── 系统盘
    └── 数据盘

账号A（源账号）的操作：
├── CCN 跨账号关联申请（自动接受）
└── 原有资源保持不变
```

**🔒 CCN 安全配置（通过 Terraform 自动实现）**：

Terraform 会自动配置 CCN 路由表的安全隔离策略：

| 配置项 | 说明 |
|--------|------|
| 自定义路由表 | 每对 VPC 使用独立的自定义路由表 |
| 路由接收策略 | 只接收 pair 内两个 VPC 的路由 |
| 默认拒绝 | 自定义路由表默认拒绝其他所有路由 |
| 无绑定默认表 | 没有 VPC 绑定到 CCN 默认路由表 |

执行完成后，Terraform 会输出 `ccn_security_summary`：

```hcl
ccn_security_summary = {
  "custom_route_tables" = 1
  "isolation_method" = "每对 VPC 使用独立的自定义路由表，配置路由接收策略只接收 pair 内 VPC 的路由"
  "security_notes" = [
    "✓ 所有 VPC 均绑定到自定义路由表（非默认路由表）",
    "✓ 自定义路由表默认拒绝所有路由，只接收显式配置的 pair 内 VPC 路由",
    "✓ 不同 VPC pair 之间流量完全隔离",
    "⚠ 请勿手动将 VPC 绑定到 CCN 默认路由表，否则会破坏隔离性",
  ]
  "total_vpc_pairs" = 1
}
```

**常用选项**：
```bash
# 执行完整流程（会在 apply 前确认）
tc-migrate run

# 跳过所有确认（CI/CD 场景）
tc-migrate run -y
tc-migrate run --yes
```

---

## 四、文件清单汇总

### 输入文件

| 文件 | 必须 | 说明 |
|------|------|------|
| `account.yaml` | 推荐 | 密钥文件，包含 SecretId/SecretKey/Region |

### 生成/更新的文件

| 命令 | 生成的文件 | 说明 |
|------|------------|------|
| `config auto` | `tc-migrate.yaml` | 迁移配置文件 |
| `scan --save` | `tc-migrate.yaml`（更新） | 追加 resources 配置 |
| `generate` | `terraform.tfvars` | Terraform 变量文件 |
| `run` | `terraform.tfvars` | 重新生成 |
| `run` | `tfplan` | Terraform 执行计划 |
| `run` | `.terraform/` | Terraform 工作目录 |
| `run` | `.terraform.lock.hcl` | Provider 版本锁定 |
| `run` | `terraform.tfstate` | Terraform 状态文件 |

### 文件位置

```
项目目录/
├── account.yaml              # 密钥文件（手动创建或 account-init 生成）
├── tc-migrate.yaml           # 迁移配置文件（config auto 生成，scan 更新）
└── terraform-cross-account/  # Terraform 项目目录
    ├── terraform.tfvars      # 变量文件（generate 生成）
    ├── tfplan                 # 执行计划（run 生成）
    ├── terraform.tfstate      # 状态文件（apply 后生成）
    ├── .terraform/            # Terraform 工作目录
    └── .terraform.lock.hcl    # Provider 锁定文件
```

---

## 五、执行顺序依赖关系

```
account.yaml（前提）
      │
      ▼
┌─────────────────┐
│ config auto     │ ──生成──▶ tc-migrate.yaml
└────────┬────────┘
         │ 依赖
         ▼
┌─────────────────┐
│ scan --save     │ ──更新──▶ tc-migrate.yaml (resources)
└────────┬────────┘
         │ 依赖
         ▼
┌─────────────────┐
│ generate        │ ──生成──▶ terraform.tfvars
└────────┬────────┘
         │ 依赖
         ▼
┌─────────────────┐
│ run             │ ──生成──▶ tfplan, terraform.tfstate
└─────────────────┘
```

**注意**：
- `config auto` 默认会自动执行 `scan`，如果不需要可以加 `--no-scan`
- `run` 会自动执行 `generate`，所以如果不需要预览 tfvars，可以跳过手动 `generate`
- 如果只是想预览变更，可以单独执行 `tc-migrate plan`

---

## 六、常见场景

### 场景 1：完整首次迁移

```bash
# 1. 生成密钥文件模板
tc-migrate config account-init
# 编辑 account.yaml 填入密钥

# 2. 全自动配置 + 扫描
tc-migrate config auto --skip-empty-vpc

# 3. （可选）预览 tfvars
tc-migrate generate --preview

# 4. 执行迁移
tc-migrate run
```

### 场景 2：增量添加资源

```bash
# 修改 tc-migrate.yaml 添加新资源配置后
tc-migrate generate
tc-migrate plan     # 预览变更
tc-migrate apply    # 执行变更
```

### 场景 3：重新扫描资源

```bash
# 源账号资源变化后，重新扫描
tc-migrate scan --save --skip-empty-vpc
tc-migrate generate
tc-migrate plan
tc-migrate apply
```

### 场景 4：销毁所有资源

```bash
tc-migrate destroy
```

---

## 七、故障排查

### 问题：config auto 报错 "API 查询失败"

**原因**：密钥无效或权限不足

**解决**：
1. 检查 `account.yaml` 中的 SecretId/SecretKey 是否正确
2. 确认 API 密钥有 VPC、CLB、NAT、CVM、SG 的读取权限

### 问题：scan 报错 "未知的资源类型"

**原因**：指定了不存在的插件类型

**解决**：
```bash
# 查看已注册的插件
tc-migrate plugins
```

### 问题：generate 报错 "配置校验失败"

**原因**：tc-migrate.yaml 配置有误

**解决**：
```bash
# 校验配置文件
tc-migrate config validate
```

### 问题：terraform apply 失败

**原因**：可能是资源配额不足、CIDR 冲突、账号权限等

**解决**：
1. 查看详细错误信息
2. 检查腾讯云控制台的资源配额
3. 确认 API 密钥有创建资源的权限
