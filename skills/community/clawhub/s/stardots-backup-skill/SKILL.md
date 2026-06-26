# # StarDots Backup

将图像自动备份到 stardots.io 云存储平台，并提供访问链接。  

## 功能特点

- 📤 一键上传图像到 Stardots.io
- 📋 查看已上传文件列表
- 🔒 安全的API认证
- 📁 支持多空间管理
- 🌐 跨平台支持

## 安装方法

1. 在 OpenClaw 市场中搜索 "Stardots Backup"
2. 点击安装
3. 配置你的 Stardots.io API 凭证

## 配置说明

使用前需要在技能设置中配置以下参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| apiKey | 是 | Stardots.io API密钥 |
| apiSecret | 是 | Stardots.io API密钥 |
| space | 是 | 目标空间名称 |

## 使用方法

### 上传图像  
上传 /path/to/your/image.jpg  
备份 ~/Photos/vacation.png  


### 查看文件列表  
列出文件  
显示所有备份文件  


### 获取帮助  
帮助  
如何使用备份  

## 使用示例

**用户**: "上传 ~/Documents/photo.jpg"
**技能**: "✅ 图像上传成功！ 文件: photo.jpg 大小: 2.5 MB URL: https://stardots.io/..."

**用户**: "列出文件"
**技能**: "📁 文件列表 (第1页，共15个文件): - vacation.jpg (1.2 MB) [2024-01-15 14:30:22] - ..."

## 注意事项

- 支持的文件格式: JPG, JPEG, PNG, GIF, BMP, SVG, AVIF, WEBP
- 文件大小限制取决于你的 Stardots.io 套餐
- API凭证会加密存储，确保安全

## 故障排除

**上传失败: 文件不存在**
- 确保文件路径正确
- 使用绝对路径或相对于当前工作目录的路径

**认证失败**
- 检查API密钥是否正确
- 确认API密钥有足够权限

## 隐私说明

本技能仅在上传文件时访问指定路径的文件，不会收集任何个人信息。所有API凭证均加密存储。  

## 限制

- 速率限制：每分钟 300 次请求
- 文件大小：最大可升级到 30MB
- 文件名长度：最多 170 个字符

## 链接

- [Stardots.io](https://stardots.io)
- [API 文档](https://stardots.io/en/documentation/openapi)
- [ClawHub](https://clawhub.com)

## 许可证

MIT