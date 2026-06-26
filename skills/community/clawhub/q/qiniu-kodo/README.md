# ☁️ 七牛云 KODO 技能

OpenClaw 技能，用于管理七牛云对象存储（KODO）。

## ✨ 功能

- 📤 上传文件
- 📥 下载文件
- 📋 列出文件
- 🗑️ 删除文件
- 🔗 获取文件 URL（支持私有空间签名）
- 📊 查看文件信息
- 📁 移动/复制文件

## 🚀 快速开始

```bash
# 安装依赖
npm install

# 配置凭证
bash scripts/setup.sh --access-key "xxx" --secret-key "xxx" --region "z0" --bucket "mybucket"

# 测试连接
node scripts/qiniu_node.mjs test-connection
```

## 📖 使用示例

```bash
# 上传
node scripts/qiniu_node.mjs upload --local file.txt --key uploads/file.txt

# 列出
node scripts/qiniu_node.mjs list --prefix uploads/

# 下载
node scripts/qiniu_node.mjs download --key uploads/file.txt --local file.txt

# 删除
node scripts/qiniu_node.mjs delete --key uploads/file.txt --force

# 获取 URL
node scripts/qiniu_node.mjs url --key uploads/file.txt
```

## 🔧 架构

三层降级策略：
1. **MCP 工具** (`qiniu-mcp-server`) - 功能最全
2. **Node.js SDK** (`qiniu`) - 稳定可靠
3. **qshell CLI** - 官方命令行

## 📄 许可证

MIT
