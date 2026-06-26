# WeChat Draft Deleter

微信公众号草稿删除工具 - 快速清理草稿箱，保持工作区整洁。

## 简介

`wechat-draft-deleter` 是一个专门用于删除微信公众号草稿箱中草稿的工具。它基于微信公众号官方API开发，支持批量删除、文件操作和安全确认机制。

## 快速开始

### 安装
```bash
clawhub install wechat-draft-deleter
```

### 配置
```bash
export WECHAT_APP_ID="你的AppID"
export WECHAT_APP_SECRET="你的AppSecret"
```

### 使用
```bash
# 删除单个草稿
wechat-draft-delete --media-id "草稿MediaID"

# 批量删除
wechat-draft-delete --file media_ids.txt
```

## 功能特点

- 🚀 **高效批量删除**：一次操作删除多个草稿
- 🔒 **安全确认**：删除前需要确认，避免误操作
- 📁 **文件支持**：支持从文件读取Media ID列表
- 📊 **结果统计**：显示成功/失败统计信息
- 🛡️ **错误处理**：完善的错误提示和日志
- 🔧 **简单集成**：易于集成到自动化工作流

## 使用场景

### 1. 清理测试草稿
```bash
# 删除所有测试草稿
wechat-draft-delete --file test_drafts.txt
```

### 2. 版本管理
```bash
# 只保留最新版本，删除旧版本
wechat-draft-delete --media-ids "old_version1,old_version2"
```

### 3. 自动化清理
```bash
# 集成到CI/CD流程
wechat-draft-delete --file drafts_to_clean.txt --force
```

## API文档

### 微信公众号API
- **接口**: `POST https://api.weixin.qq.com/cgi-bin/draft/delete`
- **参数**: `{"media_id": "草稿Media ID"}`
- **响应**: `{"errcode": 0, "errmsg": "ok"}`

### 获取Media ID
1. **wenyan工具**: 发布时返回Media ID
2. **微信公众号后台**: 草稿详情中查看
3. **API获取**: 通过草稿列表API获取

## 配置要求

### 微信公众号
- ✅ 已认证的微信公众号
- ✅ 开通草稿箱功能  
- ✅ API调用权限

### 系统要求
- ✅ Python 3.6+
- ✅ requests库
- ✅ 有效的AppID和AppSecret

## 安全警告

⚠️ **重要提示**：
- 删除操作**不可逆**
- 建议先备份重要草稿
- 确认Media ID正确性
- 在生产环境前先测试

## 示例

### 示例1：清理所有测试草稿
```bash
# 创建Media ID列表文件
cat > drafts.txt << EOF
DgrVBScHsvTZOSzU4WcnaTobRFBFXoaG0AIrFKAU_E6MKLBPNkZ9s6XVMv2GVFDl
DgrVBScHsvTZOSzU4WcnadL0xBHHy-8b232944xVRg-PjZ3aq81X98J6M35oA6vC
EOF

# 执行删除
wechat-draft-delete --file drafts.txt
```

### 示例2：集成到工作流
```bash
#!/bin/bash
# 自动化清理脚本

# 设置凭证
export WECHAT_APP_ID="wx6c51352c4c382e6e"
export WECHAT_APP_SECRET="0b65da00f3050128765a524b5c88dc1e"

# 生成需要删除的Media ID列表
python3 generate_draft_list.py > to_delete.txt

# 执行删除
wechat-draft-delete --file to_delete.txt --force

# 记录日志
echo "$(date): 删除了 $(wc -l < to_delete.txt) 个草稿" >> cleanup.log
```

## 故障排除

### 常见问题

**Q: 获取access_token失败**
A: 检查AppID和AppSecret是否正确，确保微信公众号已认证。

**Q: 删除返回成功但草稿还在**
A: 微信公众号API可能返回成功但实际未删除，建议在后台确认。

**Q: 批量删除部分失败**
A: 检查失败的Media ID是否正确，是否有删除权限。

### 错误代码
- `40001`: 无效的access_token
- `42001`: access_token过期
- `45009`: API调用频率限制
- `48001`: API功能未授权

## 开发

### 项目结构
```
wechat-draft-deleter/
├── SKILL.md          # 技能元数据
├── README.md         # 项目说明
├── package.json      # 包配置
├── install.sh        # 安装脚本
└── scripts/
    └── delete_drafts.py  # 主程序
```

### 本地开发
```bash
# 克隆项目
git clone https://github.com/yourusername/wechat-draft-deleter.git

# 安装依赖
pip install -r requirements.txt

# 测试
python scripts/delete_drafts.py --help
```

## 许可证

MIT License © 2026 wechat-公众号运营

## 支持

- 提交Issue: [GitHub Issues](https://github.com/yourusername/wechat-draft-deleter/issues)
- 文档: [完整文档](https://github.com/yourusername/wechat-draft-deleter/wiki)
- 示例: [使用示例](https://github.com/yourusername/wechat-draft-deleter/examples)