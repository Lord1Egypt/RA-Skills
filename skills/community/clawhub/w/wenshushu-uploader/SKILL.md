---
name: wenshushu-file-uploader
description: 文叔叔文件上传技能，自动上传文件到文叔叔并生成分享链接和取件码
---

# 文叔叔文件分享技能

自动将文件上传到文叔叔（wenshushu.cn），生成分享链接和取件码，方便快速分享文件。

## 🎯 触发场景

- 用户说"发文件给我"、"上传文件"、"分享文件"
- 用户要求"把文件发到文叔叔"
- 用户说"生成下载链接"
- 用户指定文件路径要求分享

## 📦 功能说明

### 核心能力

1. **文件上传**：支持任意类型文件上传到文叔叔
2. **取件码生成**：自动生成4位数字取件码
3. **链接生成**：生成公共下载链接和管理链接
4. **自动发送**：上传后自动将链接和取件码发送给用户
5. **多文件支持**：可上传单个文件或多个文件

### 输出格式

上传成功后返回：
- 📎 文件名和大小
- 🔗 公共下载链接（无需登录即可下载）
- 🔢 取件码（4位数字）
- ⚙️ 个人管理链接（可查看上传记录）

## ⚙️ 配置说明

### 系统要求

- ✅ wssf 工具已安装（文叔叔命令行工具）
- ✅ Python 3.8+ 环境
- ✅ 网络可访问 wenshushu.cn

### 自动安装

首次使用时，技能会自动：
1. 检查 wssf 是否已安装
2. 如未安装，自动下载并安装 wssf 5.0.6
3. 配置 uv 虚拟环境（如需）

### 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `wenshushu.use_login` | `false` | 是否使用登录账户上传（更大空间）|
| `wenshushu.random_key` | `true` | 是否随机生成取件码 |
| `wenshushu.custom_key` | `null` | 自定义取件码（4位数字）|
| `wenshushu.proxy` | `null` | 代理服务器地址 |

## 🔄 工作流程

```
1. 用户请求上传文件
2. AI 检查文件是否存在
3. 调用 wssf 工具上传
4. wssf 返回链接和取件码
5. AI 格式化消息发送给用户
6. （可选）保存上传记录到 MEMORY.md
```

## 📝 使用示例

### 示例1：基本上传
**用户**: "发文件给我"
**AI**: `请提供要上传的文件路径，例如：/path/to/file.zip`

**用户**: "上传 /root/.openclaw/workspace/report.pdf"
**AI**: 自动上传并返回：
```
📄 文件上传成功！

文件名：report.pdf
大小：2.3 MB

🔗 下载链接：https://c.wss.ink/f/xxxxx
🔢 取件码：1234

📊 管理链接：https://www.wenshushu.cn/t/xxxxx
```

### 示例2：自定义取件码
**用户**: "上传文件，取件码设置为 8888"
**AI**: 使用自定义取件码上传并返回链接

### 示例3：批量上传
**用户**: "把这三个文件发到文叔叔：file1.txt file2.pdf file3.zip"
**AI**: 分别上传每个文件，返回各自的链接和取件码

## ⚠️ 注意事项

1. **文件大小限制**：
   - 匿名用户：单文件 ≤ 5GB
   - 登录用户：单文件 ≤ 40GB（需配置登录）

2. **网络要求**：
   - 需要可访问 wenshushu.cn
   - 如遇滑块验证需手动完成
   - 大文件建议使用代理

3. **隐私安全**：
   - 上传链接 anyone with link can download
   - 敏感文件请加密后上传
   - 取件码建议随机生成

4. **文件保留**：
   - 文叔叔默认保留时间较长（官方未明确说明）
   - 建议定期清理不需要的文件

## 🔧 高级用法

### 配置登录（可选）

如需更大空间和更长保留时间，可配置登录：

```bash
# 1. 访问 https://www.wenshushu.cn 并登录
# 2. 打开开发者工具（F12）
# 3. 切换到 Network 标签
# 4. 刷新页面，找到 X-TOKEN 请求头
# 5. 复制 token（以 30 或 31 开头）

# 然后在 OpenClaw 中配置：
wenshushu.login("30Bxxxxxxxxxxxxxxxxx")
```

### 使用代理

如果网络受限，可配置代理：
```bash
wenshushu.upload("file.zip", proxy="http://127.0.0.1:7890")
```

### 批量上传目录

```bash
wenshushu.upload_folder("/path/to/folder")
```

## 🛠️ 技术实现

### 依赖工具

- **wssf**: 文叔叔官方命令行工具（Python）
- **uv**: 现代 Python 包管理器（推荐）
- **browser**: OpenClaw 浏览器自动化（可选，用于滑块验证）

### 核心脚本

- `scripts/upload.py`: 文件上传主逻辑
- `scripts/download.py`: 文件下载功能（预留）
- `scripts/utils.py`: 工具函数

### 配置存储

- 登录 token: `~/.config/wenshushu/token.txt`
- 多用户管理: `~/.config/wenshushu/user_tokens.json`

## 📊 上传记录

每次上传会记录到：
```
~/.openclaw/memory/wenshushu-uploads.jsonl
```

格式：
```json
{
  "timestamp": "2026-03-16T15:10:00Z",
  "filename": "report.pdf",
  "size": 2345678,
  "public_url": "https://c.wss.ink/f/xxxxx",
  "pickup_code": "1234",
  "management_url": "https://www.wenshushu.cn/t/xxxxx"
}
```

## 🔐 安全建议

1. **不要上传敏感信息**：如密码、密钥、身份证等
2. **使用强取件码**：避免使用简单序列（如1234）
3. **定期清理**：登录后可在管理页面删除旧文件
4. **检查链接**：上传后确认链接可正常访问

---

## 🚀 快速开始

### 方法一：自动安装（推荐）
当用户第一次请求上传时，AI 会自动：
1. 检查并安装 uv（如果未安装）
2. 创建虚拟环境
3. 安装 wssf 依赖
4. 开始上传

### 方法二：手动安装
```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装 wssf
uv venv
uv pip install wssf==5.0.6

# 3. 验证安装
uv run wss.py --help
```

---

## 📝 示例对话

**User**: "把 HertzBeat 架构分析文档发给我"

**AI**:
```
正在上传文件：/root/.openclaw/workspace/hertzbeat-architecture-analysis.md

📤 使用 wenshushu 工具上传...
✅ 上传成功！

📄 文件名: hertzbeat-architecture-analysis.md
📏 大小: 11 KB

🔗 下载链接: https://c.wss.ink/f/jfgeidlyzdf
🔢 取件码: 7010

📋 管理链接: https://www.wenshushu.cn/t/jfgeiDlYwit3IuLs

请在浏览器中打开下载链接，输入取件码即可下载。
```

---

## 🐛 故障排除

### 问题：wssf 安装失败
**解决**：手动安装 pip 或 uv，然后 `pip install wssf`

### 问题：上传时遇到滑块验证
**解决**：在浏览器中手动完成验证（已登录状态通常不需要）

### 问题：文件太大上传失败
**解决**：
- 使用登录账户（更大空间）
- 使用代理加速
- 分卷压缩后分批上传

### 问题：下载链接无法访问
**解决**：
- 检查链接是否完整
- 确认取件码正确
- 联系上传者确认文件未过期

---

**版本**: 1.0.0
**创建日期**: 2026-03-16
**依赖**: wssf 5.0.6+, uv (推荐)
**协议**: MIT