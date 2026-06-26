# 故障排查指南

## config auto 报错 "API 查询失败"

**原因**：密钥无效或权限不足

**解决**：
1. 检查 `account.yaml` 中的 SecretId/SecretKey
2. 确认 API 密钥有 VPC、CLB、NAT、CVM、SG 的读取权限

---

## scan 报错 "未知的资源类型"

**原因**：指定了不存在的插件类型

**解决**：
```bash
tc-migrate plugins  # 查看已注册插件
```

---

## generate 报错 "配置校验失败"

**原因**：tc-migrate.yaml 配置有误

**解决**：
```bash
tc-migrate config validate  # 校验配置
```

---

## terraform apply 失败

**原因**：资源配额不足、CIDR 冲突、账号权限等

**解决**：
1. 查看详细错误信息
2. 检查腾讯云控制台的资源配额
3. 确认 API 密钥有创建资源的权限

---

## CCN 路由不通

**原因**：路由表配置问题或 VPC 关联未完成

**解决**：
1. 检查 CCN 路由表是否正确绑定 VPC
2. 确认路由接收策略包含 pair 内的 VPC
3. 检查 Terraform 输出的 `ccn_security_summary`

---

## 跨账号关联失败

**原因**：目标账号未授权或 API 密钥权限不足

**解决**：
1. 确认账号 A 的 API 密钥有 CCN 相关权限
2. 检查跨账号关联请求是否已自动接受

---

## Terraform 状态文件损坏

**原因**：并发操作或意外中断

**解决**：
```bash
# 备份当前状态
cp terraform/terraform.tfstate terraform/terraform.tfstate.backup

# 尝试刷新状态
cd terraform && terraform refresh
```

---

## 密钥权限要求

账号 A（源账号）需要的权限：
- `vpc:Describe*` - VPC 查询
- `clb:Describe*` - CLB 查询
- `cvm:Describe*` - CVM 查询
- `ccn:*` - CCN 操作（跨账号关联）

账号 B（目标账号）需要的权限：
- `vpc:*` - VPC 创建和管理
- `clb:*` - CLB 创建和管理
- `cvm:*` - CVM 创建和管理
- `ccn:*` - CCN 创建和管理
- `nat:*` - NAT 网关创建和管理
