---
name: qiniu-kodo
description: |
  七牛云 KODO 对象存储技能。支持文件上传、下载、列出、删除、获取 URL 等操作。
  三层架构：MCP 工具（优先）→ Node.js SDK → qshell CLI。
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["node", "python3", "pip3"], "packages": ["qiniu", "qiniu-mcp-server"] },
        "install":
          [
            { "id": "qiniu-sdk", "kind": "node", "package": "qiniu", "label": "Install qiniu Node.js SDK" },
            { "id": "qiniu-mcp", "kind": "python", "package": "qiniu-mcp-server", "label": "Install qiniu-mcp-server" },
          ],
      },
  }
---

# ☁️ 七牛云 KODO 技能

通过 **MCP 工具** / **Node.js SDK** / **qshell CLI** 管理七牛云对象存储。

---

## 🎯 执行策略（三层降级）

| 优先级 | 工具 | 使用场景 |
|--------|------|----------|
| **1** | `qiniu-mcp-server` | 功能最全，优先使用 |
| **2** | Node.js SDK | MCP 不可用时降级 |
| **3** | qshell CLI | 最后备选 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/qiniu-kodo

# 运行自动安装
bash scripts/setup.sh
```

### 2. 配置凭证

```bash
bash scripts/setup.sh \
  --access-key "YOUR_ACCESS_KEY" \
  --secret-key "YOUR_SECRET_KEY" \
  --region "z0" \
  --bucket "mybucket"
```

### 3. 测试连接

```bash
node scripts/qiniu_node.mjs test-connection
```

---

## 📋 使用示例

### 上传文件

```bash
node scripts/qiniu_node.mjs upload \
  --local "/path/to/file.txt" \
  --key "uploads/file.txt"
```

### 列出文件

```bash
node scripts/qiniu_node.mjs list --prefix "uploads/" --limit 100
```

### 下载文件

```bash
node scripts/qiniu_node.mjs download \
  --key "uploads/file.txt" \
  --local "/path/to/save.txt"
```

### 删除文件

```bash
node scripts/qiniu_node.mjs delete --key "uploads/file.txt" --force
```

### 获取文件 URL

```bash
# 公开空间
node scripts/qiniu_node.mjs url --key "uploads/file.txt"

# 私有空间（1小时有效）
node scripts/qiniu_node.mjs url --key "uploads/file.txt" --private --expires 3600
```

---

## 🔧 Node.js SDK API

| 命令 | 说明 |
|------|------|
| `upload --local <path> --key <key>` | 上传文件 |
| `download --key <key> --local <path>` | 下载文件 |
| `list [--prefix <p>] [--limit <n>]` | 列出文件 |
| `delete --key <key> [--force]` | 删除文件 |
| `url --key <key> [--private] [--expires <s>]` | 获取 URL |
| `stat --key <key>` | 文件信息 |
| `move --src-key <a> --dest-key <b>` | 移动文件 |
| `copy --src-key <a> --dest-key <b>` | 复制文件 |
| `test-connection` | 测试连接 |

---

## ⚙️ 配置文件

**config/qiniu-config.json**

```json
{
  "accessKey": "YOUR_ACCESS_KEY",
  "secretKey": "YOUR_SECRET_KEY",
  "bucket": "mybucket",
  "region": "z0",
  "domain": "https://cdn.example.com"
}
```

**区域代码**：
- `z0` - 华东（杭州）
- `z1` - 华北（河北）
- `z2` - 华南（广州）
- `na0` - 北美（洛杉矶）
- `as0` - 东南亚（新加坡）

---

## 🐛 故障排查

| 问题 | 解决 |
|------|------|
| `Cannot find module 'qiniu'` | `npm install qiniu` |
| `401 Unauthorized` | 检查 AccessKey/SecretKey |
| `连接超时` | 检查区域代码和网络 |

---

## 📚 相关链接

- [七牛云 MCP Server](https://github.com/qiniu/qiniu-mcp-server)
- [七牛云 Node.js SDK](https://developer.qiniu.com/kodo/sdk/1289/nodejs)
- [qshell 工具](https://developer.qiniu.com/kodo/tools/1302/qshell)

---

## 📄 许可证

MIT License
