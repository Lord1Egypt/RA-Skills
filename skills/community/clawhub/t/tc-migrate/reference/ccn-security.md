# CCN 安全配置说明

## 概述

CCN（云联网）用于实现跨账号 VPC 之间的网络互通。为确保网络安全隔离，本工具通过 Terraform 自动配置 CCN 路由表的安全策略。

---

## 安全配置要点

| 配置项 | 说明 |
|--------|------|
| **自定义路由表** | 每对 VPC 使用独立的自定义路由表，不使用 CCN 默认路由表 |
| **路由接收策略** | 只接收 pair 内两个 VPC 的路由，拒绝其他所有路由 |
| **默认拒绝** | 自定义路由表默认拒绝所有路由，只有显式配置的路由才会被接收 |
| **无绑定默认表** | 没有 VPC 绑定到 CCN 默认路由表，避免意外的路由泄露 |

---

## 安全隔离原理

```
CCN 云联网
├── 默认路由表（不绑定任何 VPC）
│
├── 自定义路由表 1（VPC Pair 1）
│   ├── 绑定：VPC-A1, VPC-B1
│   └── 路由接收策略：只接收 VPC-A1、VPC-B1 的路由
│
└── 自定义路由表 2（VPC Pair 2）
    ├── 绑定：VPC-A2, VPC-B2
    └── 路由接收策略：只接收 VPC-A2、VPC-B2 的路由

结果：
- VPC-A1 ↔ VPC-B1 互通 ✓
- VPC-A2 ↔ VPC-B2 互通 ✓
- VPC-A1 ↔ VPC-A2 隔离 ✗
- VPC-B1 ↔ VPC-B2 隔离 ✗
```

---

## Terraform 输出

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

---

## 安全检查清单

部署完成后，可通过以下方式验证安全配置：

### 1. 检查 Terraform 输出

```bash
cd terraform
terraform output ccn_security_summary
```

### 2. 控制台验证

1. 登录腾讯云控制台 → 云联网
2. 查看 CCN 实例 → 路由表
3. 确认：
   - 默认路由表无 VPC 绑定
   - 每个 VPC pair 有独立的自定义路由表
   - 自定义路由表的路由接收策略正确

### 3. 网络连通性测试

```bash
# 在 VPC-A 的 CVM 上测试
ping <VPC-B 内网 IP>  # 应该可通

# 在 VPC-A1 的 CVM 上测试（如果有多个 pair）
ping <VPC-A2 内网 IP>  # 应该不通（隔离）
```

---

## 安全注意事项

1. **不要手动修改 CCN 路由表**：所有配置通过 Terraform 管理，手动修改可能导致状态不一致

2. **不要将 VPC 绑定到默认路由表**：这会破坏隔离性，导致不同 pair 之间可以通信

3. **定期检查配置**：确保没有意外的路由表变更

4. **Terraform 状态文件安全**：`terraform.tfstate` 包含敏感信息，妥善保管

---

## 相关 Terraform 资源

- `tencentcloud_ccn` - CCN 实例
- `tencentcloud_ccn_route_table` - CCN 路由表
- `tencentcloud_ccn_route_table_input_policies` - 路由接收策略
- `tencentcloud_ccn_attachment` - VPC 关联
- `tencentcloud_ccn_route_table_associate_instance_config` - 路由表绑定
