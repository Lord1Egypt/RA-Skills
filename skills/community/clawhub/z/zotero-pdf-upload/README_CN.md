# 📎 zotero-pdf-upload

[English](README.md) | [GitHub](https://github.com/chenhaox/zotero-pdf-upload)

> 🤖 AI Skill — 让你的 LLM 直接操作 [Zotero Web Library](https://www.zotero.org)：上传 PDF、创建条目、匹配合集。

## ⚙️ 配置

使用前需要准备两样东西：**Zotero API Key** 和你的 **Zotero 文献库 URL**。

### 第一步 — 创建 Zotero API Key

1. 登录 [zotero.org](https://www.zotero.org)，点击右上角的 **"Settings"**。

2. 在设置页面，点击左侧 **"Security"** 标签，然后滚动到 **Applications** 区域，点击 **"Create new private key"**。

3. 配置密钥权限：
   - **Personal Library**：✅ Allow library access、✅ Allow notes access、✅ Allow write access
   - **Default Group Permissions**：选择 **Read/Write**（如果使用 group 库）
   - 点击 **"Save Key"** 生成 `Zotero_API_Key`

4. **复制生成的密钥** — 下一步会用到。

### 第二步 — 获取 Zotero 文献库 URL

在浏览器中打开你的 Zotero 文献库，从地址栏复制 URL：

- **个人库**：`https://www.zotero.org/<你的用户名>/library`
- **群组库**：`https://www.zotero.org/groups/<群组ID>/<群组名>/library`

例如：
```
# 个人库
https://www.zotero.org/chenhaox/library

# 群组库
https://www.zotero.org/groups/6320165/fafu_robot/library
```

### 第三步 — 运行配置

```bash
python scripts/setup.py "<YOUR_LIBRARY_URL>" "<YOUR_API_KEY>"
```

✅ **搞定！** 重启对话，LLM 会自动识别并使用该 skill。

> 💡 直接告诉 AI：_"帮我把这篇 PDF 上传到 Zotero 的 XX 合集"_，它就会自动调用。

---

## 🔧 功能一览

| 功能 | 说明 |
|------|------|
| 🔗 解析 URL | 支持 group / personal 两种 Zotero 库 |
| 📂 合集管理 | 列出、匹配、创建合集 |
| 📝 创建条目 | 自动填充论文元数据 |
| 📤 上传 PDF | 附件自动关联到条目 |
| 🔐 安全认证 | API Key 从环境变量 / 文件安全加载 |
| ✋ 写保护 | 所有写操作需明确确认 |
---

## 🛠 进阶用法

### 📁 主要脚本

| 脚本 | 说明 |
|------|------|
| `scripts/setup.py` | ⚡ 一行命令生成配置 |
| `scripts/zotero_workflow.py` | 🚀 CLI 入口 |
| `scripts/zotero_client.py` | 🔌 Zotero API 客户端 |
| `tests/smoke_test_zotero_pdf_upload.py` | 🧪 离线冒烟测试 |

### 📖 详细用法

#### 1️⃣ 解析 URL

```bash
python scripts/zotero_workflow.py parse-url --url "https://www.zotero.org/groups/123456/my-group/library"
```

#### 2️⃣ 列出合集（只读）

```bash
python scripts/zotero_workflow.py list-collections --config config.json
```

#### 3️⃣ 选择合集（只读）

```bash
python scripts/zotero_workflow.py choose-collection --config config.json --item-json references/item.example.json
```

#### 4️⃣ 创建合集（显式写入）

```bash
python scripts/zotero_workflow.py create-collection --config config.json --name "LLM Safety" --approve-create
```

#### 5️⃣ 创建条目 + 上传 PDF（显式写入）

```bash
python scripts/zotero_workflow.py create-item \
  --config config.json \
  --item-json references/item.example.json \
  --auto-match-collection \
  --attach-pdf /path/to/paper.pdf \
  --approve-write
```

### 🧪 测试

```bash
python tests/smoke_test_zotero_pdf_upload.py
```

## 📄 License

MIT
