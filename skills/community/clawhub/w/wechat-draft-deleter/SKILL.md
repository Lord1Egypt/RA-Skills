---
name: wechat-draft-deleter
description: 删除微信公众号草稿箱中的草稿。支持批量删除指定Media ID的草稿。
version: 1.0.0
author: wechat-公众号运营
tags: [wechat, draft, delete, 公众号, 草稿, 微信]
---

# WeChat Draft Deleter

删除微信公众号草稿箱中的草稿。基于微信公众号官方API开发。

## 功能特性

- ✅ **删除单个草稿**：通过Media ID删除指定草稿
- ✅ **批量删除草稿**：一次删除多个草稿
- ✅ **文件批量操作**：从文件读取Media ID列表
- ✅ **安全确认**：删除前需要确认（可强制模式）
- ✅ **结果汇总**：显示成功/失败统计
- ✅ **错误处理**：完善的错误提示和日志

## 使用场景

1. **清理测试草稿**：删除测试发布的多余草稿
2. **版本管理**：删除旧版本文章草稿
3. **批量清理**：一次性清理多个草稿
4. **自动化运维**：集成到自动化工作流中

## 安装方法

### 方法一：使用clawhub安装
```bash
clawhub install wechat-draft-deleter
```

### 方法二：手动安装
```bash
# 克隆或下载技能目录
cd skills/wechat-draft-deleter
chmod +x install.sh
./install.sh
```

## 使用方法

### 设置环境变量
```bash
export WECHAT_APP_ID="你的微信公众号AppID"
export WECHAT_APP_SECRET="你的微信公众号AppSecret"
```

### 删除单个草稿
```bash
wechat-draft-delete --media-id "DgrVBScHsvTZOSzU4WcnaTobRFBFXoaG0AIrFKAU_E6MKLBPNkZ9s6XVMv2GVFDl"
```

### 批量删除草稿
```bash
wechat-draft-delete --media-ids "id1,id2,id3"
```

### 从文件删除草稿
```bash
# 创建media_ids.txt文件
echo "DgrVBScHsvTZOSzU4WcnaTobRFBFXoaG0AIrFKAU_E6MKLBPNkZ9s6XVMv2GVFDl" > media_ids.txt
echo "DgrVBScHsvTZOSzU4WcnadL0xBHHy-8b232944xVRg-PjZ3aq81X98J6M35oA6vC" >> media_ids.txt

# 执行删除
wechat-draft-delete --file media_ids.txt
```

### 强制删除（不确认）
```bash
wechat-draft-delete --file media_ids.txt --force
```

## API说明

### 微信公众号API
- **接口地址**: `https://api.weixin.qq.com/cgi-bin/draft/delete`
- **请求方法**: POST
- **请求参数**: `{"media_id": "草稿Media ID"}`
- **返回结果**: `{"errcode": 0, "errmsg": "ok"}`

### 获取Media ID
Media ID可以通过以下方式获取：
1. **wenyan工具发布时返回**
2. **微信公众号后台查看草稿详情**
3. **通过微信公众号API获取草稿列表**

## 配置要求

### 微信公众号权限
- 需要已认证的微信公众号
- 需要开通草稿箱功能
- 需要API调用权限

### 系统要求
- Python 3.6+
- requests库
- 微信公众号AppID和AppSecret

## 安全注意事项

⚠️ **重要警告**：
1. **删除不可逆**：草稿删除后无法恢复
2. **权限验证**：确保有删除权限
3. **备份建议**：重要草稿建议先备份
4. **测试建议**：先在测试环境验证

## 错误代码

| 错误代码 | 说明 | 解决方案 |
|---------|------|---------|
| 40001 | 无效的access_token | 检查AppID和AppSecret |
| 40066 | 无效的URL | 检查API接口地址 |
| 42001 | access_token过期 | 重新获取access_token |
| 45009 | API调用频率限制 | 降低调用频率 |
| 48001 | API功能未授权 | 检查微信公众号权限 |

## 开发记录

### 版本历史
- **v1.0.0** (2026-03-19): 初始版本发布
  - 支持单个草稿删除
  - 支持批量删除
  - 支持文件操作
  - 添加安全确认机制

### 测试验证
本技能已在真实微信公众号环境中测试：
- ✅ 成功删除8个测试草稿
- ✅ API返回正常
- ✅ 错误处理完善

## 贡献指南

欢迎提交Issue和Pull Request：
1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License