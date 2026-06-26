# 命令参考

> 所有命令使用 `python3 {baseDir}/main.py` 调用。

## 核心命令

### config - 配置管理

```bash
# 全自动配置（推荐）
python3 {baseDir}/main.py config auto [OPTIONS]

# 选项：
#   --skip-empty-vpc    跳过空 VPC（无资源的 VPC）
#   --target-cidr TEXT  目标网段（如 172.16.0.0/12）
#   --no-scan           不自动扫描资源
#   --force             覆盖已有配置

# 生成密钥文件模板
python3 {baseDir}/main.py config account-init

# 校验配置文件
python3 {baseDir}/main.py config validate
```

---

### scan - 资源扫描

```bash
# 扫描所有资源
python3 {baseDir}/main.py scan [OPTIONS]

# 选项：
#   --save              保存到配置文件
#   --skip-empty-vpc    跳过空 VPC
#   -r, --resource TYPE 指定资源类型（可多次使用）

# 示例：
python3 {baseDir}/main.py scan --save --skip-empty-vpc
python3 {baseDir}/main.py scan -r clb -r nat --save
python3 {baseDir}/main.py scan  # 仅预览
```

---

### generate - 生成 Terraform 变量文件

```bash
python3 {baseDir}/main.py generate [OPTIONS]

# 选项：
#   --preview    仅预览（不写入文件）
#   --force      强制覆盖

# 示例：
python3 {baseDir}/main.py generate --force
python3 {baseDir}/main.py generate --preview
```

---

### run - 一键执行迁移

```bash
python3 {baseDir}/main.py run [OPTIONS]

# 选项：
#   -y, --yes    跳过确认

# 内部流程：
# 1. 生成 terraform.tfvars
# 2. terraform init
# 3. terraform plan
# 4. terraform apply（需确认）
```

---

## 辅助命令

### plan - 仅执行 Terraform plan

```bash
python3 {baseDir}/main.py plan
```

---

### apply - 仅执行 Terraform apply

```bash
python3 {baseDir}/main.py apply [OPTIONS]

# 选项：
#   -y, --yes    跳过确认
```

---

### destroy - 销毁资源

```bash
python3 {baseDir}/main.py destroy [OPTIONS]

# 选项：
#   -y, --yes    跳过确认

# ⚠️ 危险操作，会删除所有 Terraform 管理的资源
```

---

### plugins - 查看资源扫描插件

```bash
python3 {baseDir}/main.py plugins

# 输出示例：
# 已注册的资源扫描插件：
# - clb: 负载均衡 (CLB)
# - nat: NAT 网关
# - cvm: 云服务器 (CVM)
# - sg: 安全组
```

---

## 全局选项

所有命令都支持的选项：

```bash
# 指定 Terraform 目录
--tf-dir PATH

# 指定配置文件
--config PATH

# 详细输出
--verbose / -v
```

---

## 命令执行顺序

### 首次迁移

```bash
python3 {baseDir}/main.py config account-init     # 1. 生成密钥模板
# 编辑 account.yaml
python3 {baseDir}/main.py config auto --skip-empty-vpc  # 2. 自动配置 + 扫描
python3 {baseDir}/main.py generate                # 3. 生成 tfvars
python3 {baseDir}/main.py run                     # 4. 执行迁移
```

### 增量变更

```bash
# 修改 tc-migrate.yaml
python3 {baseDir}/main.py generate
python3 {baseDir}/main.py plan
python3 {baseDir}/main.py apply
```

### 重新扫描

```bash
python3 {baseDir}/main.py scan --save --skip-empty-vpc
python3 {baseDir}/main.py generate
python3 {baseDir}/main.py plan
python3 {baseDir}/main.py apply
```
