# 文件结构说明

## Skill 目录结构

`{baseDir}/` 表示 skill 根目录：

```
tc-migrate/                        # Skill 根目录
├── SKILL.md                       # Skill 定义文件（OpenClaw 入口）
├── main.py                        # CLI 入口脚本（python3 main.py ...）
├── README.md                      # 说明文档
├── requirements.txt               # Python 依赖
│
├── src/                           # Python 源代码
│   ├── pyproject.toml             # 包配置
│   ├── requirements.txt
│   └── tc_migrate/                # CLI 工具包
│       ├── __init__.py
│       ├── cli.py                 # CLI 入口
│       ├── config.py              # 配置加载
│       ├── terraform.py           # Terraform 执行器
│       ├── tfvars.py              # tfvars 生成
│       ├── models.py              # 数据模型
│       ├── commands/              # 子命令
│       │   ├── config_cmds.py     # config 命令
│       │   ├── scan_cmd.py        # scan 命令
│       │   ├── generate_cmd.py    # generate 命令
│       │   ├── run_cmd.py         # run 命令
│       │   └── tf_cmds.py         # terraform 命令
│       ├── plugins/               # 资源扫描插件
│       │   ├── base.py            # 插件基类
│       │   ├── clb_plugin.py      # CLB 扫描
│       │   ├── nat_plugin.py      # NAT 扫描
│       │   ├── cvm_plugin.py      # CVM 扫描
│       │   └── sg_plugin.py       # 安全组扫描
│       └── tools/                 # 工具脚本
│
├── terraform/                     # Terraform 配置
│   ├── main.tf                    # 主入口
│   ├── variables.tf               # 变量定义
│   ├── outputs.tf                 # 输出定义
│   ├── providers.tf               # Provider 配置
│   ├── ccn.tf                     # CCN 配置
│   ├── clb.tf                     # CLB 配置
│   ├── cvm.tf                     # CVM 配置
│   ├── nat.tf                     # NAT 配置
│   ├── sg.tf                      # 安全组配置
│   └── modules/                   # 子模块
│       ├── ccn/                   # CCN 云联网
│       ├── ccn-vpc-pair/          # VPC 对路由表
│       ├── vpc-network/           # VPC 创建
│       ├── security-group/        # 安全组
│       ├── clb/                   # 负载均衡
│       ├── nat-gateway/           # NAT 网关
│       └── cvm/                   # 云服务器
│
├── reference/                     # 参考文档
│   ├── troubleshooting.md         # 故障排查
│   ├── file-structure.md          # 文件结构（本文档）
│   ├── commands.md                # 命令参考
│   └── ccn-security.md            # CCN 安全配置
│
└── docs/                          # 详细文档
    └── workflow-guide.md          # 工作流指南
```

---

## 用户工作目录

执行迁移命令的目录：

```
工作目录/
├── account.yaml              # 密钥文件（必须）
│                             # - 手动创建
│                             # - 或 tc-migrate config account-init 生成模板
│
├── tc-migrate.yaml           # 迁移配置文件
│                             # - config auto 自动生成
│                             # - scan --save 追加资源配置
│
└── terraform/                # Terraform 工作目录
    │                         # - 可以是 skill 的 terraform/ 目录
    │                         # - 或复制到本地
    │
    ├── terraform.tfvars      # 变量文件（generate 生成）
    ├── tfplan                # 执行计划（plan 生成）
    ├── terraform.tfstate     # 状态文件（apply 后生成）
    ├── terraform.tfstate.backup  # 状态备份
    ├── .terraform/           # Terraform 工作目录（init 生成）
    └── .terraform.lock.hcl   # Provider 锁定文件
```

---

## 配置文件示例

### account.yaml

```yaml
account_a:  # 源账号
  secret_id: "AKID..."
  secret_key: "..."
account_b:  # 目标账号
  secret_id: "AKID..."
  secret_key: "..."
region_a: "ap-beijing"      # 源账号地域
region_b: "ap-guangzhou"    # 目标账号地域
```

### tc-migrate.yaml

```yaml
accounts:
  source:
    name: account_a
    region: ap-beijing
    uin: "100000000001"
  target:
    name: account_b
    region: ap-guangzhou
    uin: "100000000002"

vpcs:
  - source_vpc_id: vpc-xxxxxx
    source_cidr: 10.0.0.0/16
    target_cidr: 172.16.0.0/16
    subnets:
      - source_subnet_id: subnet-xxxxxx
        source_cidr: 10.0.1.0/24
        target_cidr: 172.16.1.0/24
        zone: ap-guangzhou-3

resources:
  clb:
    - source_id: lb-xxxxxx
      name: my-clb
      vpc_index: 0
      # ...
  nat:
    - source_id: nat-xxxxxx
      name: my-nat
      vpc_index: 0
      # ...
  cvm:
    - source_id: ins-xxxxxx
      name: my-cvm
      vpc_index: 0
      subnet_index: 0
      # ...
```
