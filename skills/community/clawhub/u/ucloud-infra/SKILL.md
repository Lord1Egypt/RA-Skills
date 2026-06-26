---
name: ucloud
description: UCloud Cloud Management - Complete Version
user-invocable: true
metadata: {"clawdbot":{"emoji":"☁️","requires":{"env":["UCLOUD_PUBLIC_KEY","UCLOUD_PRIVATE_KEY"]},"primaryEnv":"UCLOUD_PUBLIC_KEY"}}
---

# UCloud Skill - 完整版本

UCloud云资源管理工具，支持所有主要资源类型的完整操作。

## 先决条件

在使用本工具之前，需要先安装 UCloud CLI 命令行工具。

安装方法请参考官方文档：https://github.com/UCloudDoc-Team/cli/blob/master/intro.md

安装完成后，确认 CLI 已正确安装：
```bash
ucloud --version
```

## 环境变量

```bash
# 必需配置
export UCLOUD_PUBLIC_KEY="your_public_key_here"
export UCLOUD_PRIVATE_KEY="your_private_key_here"

# 可选配置
export UCLOUD_PROJECT_ID="your_project_id"      # 默认项目ID
export UCLOUD_REGION="cn-wlcb"               # 默认地域
export UCLOUD_ZONE="cn-wlcb-01"             # 默认可用区
```

**注意**: API密钥从 https://console.ucloud.cn/ 获取

## 支持的资源类型和操作

### 云主机 (uhost)
**操作**: list, create, start, stop, restart, delete, reset-password, resize

### MySQL 数据库
**操作**:
- db: list, create, start, stop, restart, delete, reset-password, resize, restore, create-slave, promote-slave
- conf: list, describe, download, apply, clone, delete, update
- backup: list, create, delete, download
- logs: list, download, delete, archive

### Redis 缓存
**操作**: list, create, start, stop, restart, delete

### Memcached 缓存
**操作**: list, create, restart, delete

### 弹性IP (eip)
**操作**: list, allocate, bind, unbind, release, modify-bw, modify-traffic-mode

### 云硬盘 (udisk)
**操作**: list, create, delete, attach, detach, expand, snapshot, list-snapshot, delete-snapshot, restore

### 负载均衡 (ulb)
**操作**: list, create, delete, update
- vserver: list, create, delete, update
- backend: list, add, delete, update
- policy: list, add, delete, update
- ssl: list, add, delete, describe, bind, unbind

### 虚拟私有云 (vpc)
**操作**: list, create, delete, create-intercome, delete-intercome, list-intercome

### 子网 (subnet)
**操作**: list, create, delete, list-resource

### 防火墙 (firewall)
**操作**: list, create, delete, update, apply, add-rule, remove-rule, resource, copy

### 镜像 (image)
**操作**: list, create, delete, copy

### 项目 (project)
**操作**: list, create, update, delete

### GlobalSSH加速 (gssh)
**操作**: list, create, delete, update, location

### 全球加速 (pathx)
**操作**: uga (list, create, delete, describe, add-port, delete-port), upath

### 对等连接 (udpn)
**操作**: list, create, delete, modify-bw

### 物理主机 (uphost)
**操作**: list

### 带宽包 (bw)
**操作**: pkg (list, create, delete), shared (list, create, delete, resize)

### 区域查询 (region)
**操作**: list

### 配置管理 (config)
**操作**: list

## 使用方法

### 基本语法
```bash
# 资源类型和操作
node /root/.openclaw/skills/ucloud/ucloud.mjs --action <操作> --resource <资源类型>

# 列出所有主机
node /root/.openclaw/skills/ucloud/ucloud.mjs --action list --resource uhost

# 创建主机
node /root/.openclaw/skills/ucloud/ucloud.mjs --action create --resource uhost \
  --cpu 2 --memory-gb 4 \
  --password "YourPassword123" \
  --image-id "uimage-xxxxx"
```

# 列出所有MySQL
node /root/.openclaw/skills/ucloud/ucloud.mjs --action list --resource mysql
```

### MySQL高级操作示例
```bash
# MySQL配置管理
node /root/.openclaw/skills/ucloud/ucloud.mjs --action conf --resource mysql --conf-action list
node /root/.openclaw/skills/ucloud/ucloud.mjs --action conf --resource mysql --conf-action describe --conf-id "conf-xxx"

# MySQL备份
node /root/.openclaw/skills/ucloud/ucloud.mjs --action backup --resource mysql
node /root/.openclaw/skills/ucloud/ucloud.mjs --action backup-create --resource mysql --id "udb-xxx"
```

### 弹性IP示例
```bash
# 申请EIP
node /root/.openclaw/skills/ucloud/ucloud.mjs --action allocate --resource eip --bandwidth-mb 5 --line BGP

# 绑定EIP到主机
node /root/.openclaw/skills/ucloud/ucloud.mjs --action bind --resource eip --eip-id "eip-xxx" --resource-id "uhost-xxx"
```

### VPC示例
```bash
# 创建VPC
node /root/.openclaw/skills/ucloud/ucloud.mjs --action create --resource vpc --name "my-vpc" --segment "192.168.0.0/16"

# 创建子网
node /root/.openclaw/skills/ucloud/ucloud.mjs --action create --resource subnet --name "my-subnet" --vpc-id "vpc-xxx" --segment "192.168.1.0/24"
```

### 防火墙示例
```bash
# 创建防火墙
node /root/.openclaw/skills/ucloud/ucloud.mjs --action create --resource firewall --name "my-fw" \
  --rules "TCP|22|0.0.0.0/0|ACCEPT|HIGH,TCP|80|0.0.0.0/0|ACCEPT|MEDIUM"

# 添加规则
node /root/.openclaw/skills/ucloud/ucloud.mjs --action add-rule --resource firewall --id "fw-xxx" --rules "TCP|443|0.0.0.0/0|ACCEPT|LOW"
```

### 负载均衡示例
```bash
# 创建负载均衡
node /root/.openclaw/skills/ucloud/ucloud.mjs --action create --resource ulb --name "my-ulb" --mode outer

# 创建虚拟服务器
node /root/.openclaw/skills/ucloud/ucloud.mjs --action vserver --resource ulb --vserver-action create \
  --ulb-id "ulb-xxx" --name "web-server" --protocol http --frontend-port 80

# 添加后端
node /root/.openclaw/skills/ucloud/ucloud.mjs --action vserver --resource ulb --vserver-action backend --vserver-action add \
  --ulb-id "ulb-xxx" --vserver-id "vserver-xxx" --backend-ip "10.0.0.1" --backend-port 8080
```

## 常用参数

### 通用参数
- `--region` - 覆盖默认地域
- `--zone` - 覆盖默认可用区
- `--json` - 返回JSON格式输出

### ID参数
- `--id` / `--uhost-id` / `--udb-id` / `--cache-id` / `--udisk-id` / `--ulb-id` / `--vpc-id` / `--subnet-id` / `--eip-id` / `--firewall-id` / `--image-id` / `--snapshot-id` / `--backup-id` / `--conf-id` / `--rule-id` / `--vserver-id` / `--backend-id` / `--policy-id` / `--cert-id`

### 主机参数
- `--cpu` - CPU核心数 (required for create)
- `--memory-gb` - 内存大小GB (required for create)
- `--password` - 密码 (required for create, reset-password)
- `--image-id` - 镜像ID (required for create)
- `--name` - 主机名称
- `--count` - 创建数量 (default: 1)

### MySQL参数
- `--name` - 数据库名称 (required for create, min 6 chars)
- `--version` - MySQL版本 (required for create)
- `--password` - 数据库密码 (required for create, reset-password)
- `--conf-id` - 配置ID (required for create)
- `--memory-size-gb` - 内存大小GB (default: 1)
- `--disk-size-gb` - 磁盘大小GB (default: 20)
- `--port` - 端口 (default: 3306)
- `--mode` - 模式 Normal/HA (default: Normal)

### Redis参数
- `--name` - 实例名称 (required for create)
- `--size-gb` - 容量大小GB (required for create)
- `--version` - Redis版本 (optional)
- `--password` - 密码 (optional)

### EIP参数
- `--bandwidth-mb` - 带宽Mbps (required for allocate)
- `--line` - 线路类型 BGP/International
- `--resource-id` - 资源ID (for bind/unbind)
- `--traffic-mode` - 流量模式 Bandwidth/Traffic

### 防火墙参数
- `--name` - 防火墙名称 (required for create)
- `--rules` - 规则列表或--rules-file
- 规则格式: 协议|端口|IP|操作|级别

## 注意事项

1. 删除操作不可逆，请谨慎操作
2. 调整配置可能导致服务短暂中断
3. 重要操作前建议创建备份
4. 镜像ID可通过 `--action list --resource image` 查询
5. MySQL配置ID可通过 `--action conf --resource mysql` 查询

## 日志记录

所有创建（create）和删除（delete）资源的操作都会自动记录到当前工作目录的 `logs` 文件夹中。

- 日志文件格式：`ucloud-operations-YYYY-MM-DD.jsonl`
- 每条日志记录包含：
  - `timestamp`: 操作时间戳
  - `action`: 操作类型（create/delete）
  - `resource`: 资源类型
  - `params`: 操作参数
  - `success`: 操作是否成功
  - `data` 或 `error`: 操作结果或错误信息

示例日志记录：
```json
{"timestamp":"2026-03-14T10:30:00.000Z","action":"create","resource":"uhost","params":{"cpu":"2","memoryGb":"4","imageId":"uimage-xxx","name":"test-host","count":"1"},"success":true,"data":{...}}
```

## 输出格式

成功返回:
```json
{
  "success": true,
  "data": [...]
}
```

失败返回:
```json
{
  "success": false,
  "error": "错误信息"
}
```
