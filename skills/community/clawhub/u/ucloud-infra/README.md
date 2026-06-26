# UCloud Infrastructure Management Skill

UCloud 云资源管理工具，支持所有主要资源类型的完整操作。

## 特性

- ✅ 支持多种 UCloud 资源类型管理
- ✅ 自动记录创建和删除操作日志
- ✅ 统一的 JSON 输出格式
- ✅ 灵活的环境变量配置
- ✅ 完整的错误处理

## 先决条件

### 1. 安装 UCloud CLI

需要先安装 UCloud CLI 命令行工具。

**macOS (使用 Homebrew):**
```bash
brew install ucloud
```

**其他系统:**
请参考官方文档：https://github.com/UCloudDoc-Team/cli/blob/master/intro.md

安装完成后，确认 CLI 已正确安装：
```bash
ucloud --version
```

### 2. 配置环境变量

```bash
# 必需配置
export UCLOUD_PUBLIC_KEY="your_public_key_here"
export UCLOUD_PRIVATE_KEY="your_private_key_here"
export UCLOUD_PROJECT_ID="your_project_id"

# 可选配置
export UCLOUD_REGION="cn-wlcb"               # 默认地域
export UCLOUD_ZONE="cn-wlcb-01"             # 默认可用区
```

**注意**:
- API 密钥从 https://console.ucloud.cn/ 获取
- 项目 ID 可通过 `ucloud project list` 查看

## 使用方法

### 查看版本

```bash
node ucloud.mjs --version
```

### 基本语法

```bash
node ucloud.mjs --action <操作> --resource <资源类型> [其他参数]
```

### 示例

```bash
# 列出所有区域
node ucloud.mjs --action list --resource region

# 列出云主机
node ucloud.mjs --action list --resource uhost

# 列出 VPC
node ucloud.mjs --action list --resource vpc

# 创建云主机
node ucloud.mjs --action create --resource uhost \
  --cpu 2 --memory-gb 4 \
  --password "YourPassword123" \
  --image-id "uimage-xxxxx"

# 删除云主机
node ucloud.mjs --action delete --resource uhost --id "uhost-xxxxx"
```

## 支持的资源类型

- **uhost**: 云主机
- **mysql**: MySQL 数据库
- **redis**: Redis 缓存
- **memcache**: Memcached 缓存
- **eip**: 弹性IP
- **udisk**: 云硬盘
- **ulb**: 负载均衡
- **vpc**: 虚拟私有云
- **subnet**: 子网
- **firewall**: 防火墙
- **image**: 镜像
- **project**: 项目
- **region**: 区域

详细的操作说明请查看 [SKILL.md](./SKILL.md)

## 日志记录

所有创建（create）和删除（delete）资源的操作都会自动记录到 `logs` 目录中。

- 日志文件格式：`logs/ucloud-operations-YYYY-MM-DD.jsonl`
- 每条日志包含：时间戳、操作类型、资源类型、参数、操作结果

## 注意事项

1. 删除操作不可逆，请谨慎操作
2. 调整配置可能导致服务短暂中断
3. 重要操作前建议创建备份
4. 请妥善保管 API 密钥，不要提交到版本控制系统

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
