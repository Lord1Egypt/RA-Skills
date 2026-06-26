# tc-migrate OpenClaw Skill

腾讯云跨账号资源迁移工具，将源账号的 VPC、CLB、NAT、CVM、安全组等资源迁移到目标账号，通过 CCN 云联网实现网络互通。

## 目录结构

```
tc-migrate/
├── SKILL.md                  # Skill 定义文件（OpenClaw 入口）
├── README.md                 # 本文件
├── requirements.txt          # Python 依赖说明
├── src/                      # Python 源代码
│   ├── pyproject.toml        # 包配置
│   └── tc_migrate/           # CLI 工具包
│       ├── cli.py            # CLI 入口
│       ├── config.py         # 配置加载
│       ├── terraform.py      # Terraform 执行器
│       ├── tfvars.py         # tfvars 生成
│       ├── commands/         # 子命令
│       └── plugins/          # 资源插件（CLB/NAT/CVM/SG）
├── terraform/                # Terraform 配置
│   ├── main.tf               # 主配置
│   ├── variables.tf          # 变量定义
│   ├── outputs.tf            # 输出定义
│   ├── providers.tf          # Provider 配置
│   └── modules/              # 子模块
│       ├── ccn/              # CCN 云联网
│       ├── ccn-vpc-pair/     # VPC 对路由表
│       ├── vpc/              # VPC 创建
│       └── ...
└── docs/                     # 文档
    └── workflow-guide.md     # 详细工作流指南
```

## 快速开始

### 1. 安装 CLI 工具

```bash
cd src && pip install -e .
```

### 2. 准备密钥文件

```bash
tc-migrate config account-init
# 编辑生成的 account.yaml，填入源/目标账号的密钥
```

### 3. 执行迁移

```bash
# 全自动配置
tc-migrate config auto --skip-empty-vpc

# 预览 Terraform 变量
tc-migrate generate --preview

# 执行迁移
tc-migrate run
```

## 支持的资源类型

| 资源类型 | 说明 |
|----------|------|
| VPC | 虚拟私有网络 |
| Subnet | 子网 |
| Security Group | 安全组 |
| CLB | 负载均衡 |
| NAT Gateway | NAT 网关 |
| CVM | 云服务器 |
| CCN | 云联网（自动创建） |

## 安全特性

- CCN 路由表安全隔离：每对 VPC 使用独立的自定义路由表
- 路由接收策略：只接收 pair 内 VPC 的路由
- 无 VPC 绑定到默认路由表

## 详细文档

- [SKILL.md](SKILL.md) - Skill 定义和使用说明
- [docs/workflow-guide.md](docs/workflow-guide.md) - 详细工作流指南

## 依赖

- Python >= 3.9
- Terraform >= 1.0
- 腾讯云 SDK（自动安装）
