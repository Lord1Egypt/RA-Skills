# 📦 虾虾优惠 Skill 发布文件夹

> 此文件夹专门用于向各大 Skill 市场平台发布/上传。

## 📁 文件结构

```
publish/
├── SKILL.md          # Skill 主文档（包含完整 API 说明）
├── README.md         # 项目说明（用户安装指南）
└── examples/         # 使用示例
    ├── 01-compare.md
    ├── 02-parse-link.md
    ├── 03-daily-deals.md
    ├── 04-local.md
    └── README.md
```

## 🎯 用途

### 直接上传的平台
- **ClaWHub**（OpenClaw 官方）：直接选择此文件夹上传
- **Skillhub**（腾讯云）：选择此文件夹
- **其他支持文件夹上传的平台**

### 需要单独提交的平台
- **GitHub**：使用项目根目录（包含 LICENSE / .gitignore 等）
- **需要特定格式的平台**：从此文件夹复制文件后修改

## 🛡️ 安全保证

✅ **此文件夹已通过安全验证**：
- 不包含任何真实凭证（secret / password / token）
- 不包含内部 IP 地址
- 不包含敏感配置文件
- 只包含公开的 Skill 文档和示例

## 🔄 自动更新

每次 SKILL.md 更新后，运行：

```bash
bash generate_publish_folder.sh
```

会自动：
1. 清空旧文件
2. 复制最新的 SKILL.md / README.md / examples/
3. 安全验证（确保无凭证）
4. 生成文件清单

## 📝 注意事项

1. **此文件夹不提交到 Git**（已在 .gitignore 中排除）
2. **每次发布前建议重新生成**（保证最新）
3. **上传前再次确认文件内容**（避免误传）

---

🦐 虾虾优惠 Skill · 官方发布文件夹
