---
name: tc_migrate
description: 腾讯云跨账号资源迁移工具。将源账号（账号A）的 VPC、CLB、NAT、CVM、安全组等资源迁移到目标账号（账号B），通过 CCN 云联网实现跨账号网络互通。支持自动扫描、配置生成、Terraform 部署。
user-invocable: true
metadata: {"openclaw": {"os": ["linux"], "requires": {"bins": ["python3", "terraform"], "env": []}}}
---

# tc-migrate 跨账号迁移 Skill

腾讯云跨账号资源迁移工具，将源账号的云资源迁移到目标账号，通过 CCN 云联网实现网络互通。

**核心流程 — 4 步**：

```
① 配置 → ② 扫描 → ③ 生成 → ④ 部署
```

---

## 支持的资源类型

| 资源类型 | Key |
|----------|-----|
| VPC | `vpc` |
| Subnet | `subnet` |
| Security Group | `sg` |
| CLB | `clb` |
| NAT Gateway | `nat` |
| CVM | `cvm` |
| CCN（自动创建） | `ccn` |

---

## 前提条件

1. **安装依赖**：
   ```bash
   pip install -r {baseDir}/requirements.txt
   ```

2. **安装 Terraform**（>= 1.0）：
   ```bash
   # CentOS/RHEL
   sudo yum install -y yum-utils
   sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
   sudo yum -y install terraform
   
   # 验证
   terraform --version
   ```

3. **准备 `account.yaml`**（在工作目录下）：
   ```yaml
   account_a:  # 源账号
     secret_id: "AKID..."
     secret_key: "..."
   account_b:  # 目标账号
     secret_id: "AKID..."
     secret_key: "..."
   region_a: "ap-beijing"
   region_b: "ap-guangzhou"
   ```

> ⚠️ **安全提醒**：绝不要在对话中显示或记录密钥值！

---

## Step 1: 全自动配置

```bash
# 基本用法（推荐）
python3 {baseDir}/main.py config auto --skip-empty-vpc

# 生成密钥模板（如果没有 account.yaml）
python3 {baseDir}/main.py config account-init
```

**生成文件**：`tc-migrate.yaml`

---

## Step 2: 资源扫描

```bash
# 扫描并保存（推荐）
python3 {baseDir}/main.py scan --save --skip-empty-vpc

# 仅预览
python3 {baseDir}/main.py scan
```

**更新文件**：`tc-migrate.yaml`（追加 `resources` 配置）

> 💡 `config auto` 默认自动扫描，可跳过此步。

---

## Step 3: 生成 Terraform 变量文件

```bash
# 生成 tfvars（推荐）
python3 {baseDir}/main.py generate --force

# 仅预览
python3 {baseDir}/main.py generate --preview
```

**生成文件**：`{baseDir}/terraform/terraform.tfvars`

---

## Step 4: 执行迁移

```bash
# 执行迁移（会在 apply 前确认）
python3 {baseDir}/main.py run

# 跳过确认
python3 {baseDir}/main.py run -y
```

**内部流程**：generate → init → plan → apply

---

## 常见场景

### 场景 1：完整首次迁移

```bash
python3 {baseDir}/main.py config account-init     # 1. 生成密钥模板
# 编辑 account.yaml 填入密钥
python3 {baseDir}/main.py config auto --skip-empty-vpc  # 2. 配置 + 扫描
python3 {baseDir}/main.py generate                # 3. 生成 tfvars
python3 {baseDir}/main.py run                     # 4. 执行迁移
```

### 场景 2：增量变更

```bash
# 修改 tc-migrate.yaml 后
python3 {baseDir}/main.py generate
python3 {baseDir}/main.py plan
python3 {baseDir}/main.py apply
```

### 场景 3：销毁资源

```bash
python3 {baseDir}/main.py destroy
```

---

## 重要提醒

1. **绝不显示或记录密钥值**
2. **执行 apply 前务必确认 plan 输出**
3. **CCN 安全配置已通过 Terraform 自动实现**
4. **妥善保管 `terraform.tfstate`（包含敏感信息）**

---

## 参考文档

详细信息请查阅 `{baseDir}/reference/` 目录：

| 文档 | 内容 |
|------|------|
| `installation.md` | 安装指南 |
| `commands.md` | 完整命令参考 |
| `file-structure.md` | 文件结构和配置示例 |
| `ccn-security.md` | CCN 安全配置详解 |
| `troubleshooting.md` | 故障排查指南 |
