# MCP Client 测试文档

**版本**: 0.1.0  
**更新日期**: 2026-03-17

---

## 📋 测试清单

### ✅ 单元测试
- [x] MCP 客户端连接
- [x] 工具列表获取
- [x] 资源列表获取
- [x] 提示词列表获取
- [ ] 工具调用
- [ ] 资源读取
- [ ] 提示词获取

### ⏳ 集成测试
- [ ] Filesystem Server 连接
- [ ] Filesystem Server 读写文件
- [ ] Filesystem Server 列出目录
- [ ] GitHub Server 连接
- [ ] GitHub Server 读取仓库
- [ ] GitHub Server 创建 Issue

---

## 🚀 快速开始

### 1. 安装依赖
```bash
cd skills/mcp-client
npm install
```

### 2. 配置服务器

编辑 `src/mcp-config.json`:

```json
{
  "filesystem": {
    "id": "filesystem",
    "name": "Filesystem Server",
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "C:\\Users\\99236\\.openclaw\\workspace"
    ],
    "description": "本地文件系统访问"
  },
  "github": {
    "id": "github",
    "name": "GitHub Server",
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-github"
    ],
    "env": {
      "GITHUB_TOKEN": "your_github_token_here"
    },
    "description": "GitHub API 集成"
  }
}
```

**获取 GitHub Token**:
1. 访问 https://github.com/settings/tokens
2. 创建新 token (classic)
3. 选择 scopes: `repo`, `read:user`, `user:email`
4. 复制 token 到配置文件

### 3. 运行测试

#### 运行所有测试
```bash
npm run test:all
```

#### 单独测试 Filesystem Server
```bash
npm run test:filesystem
```

#### 单独测试 GitHub Server
```bash
npm run test:github
```

#### 安全测试
```bash
npm run test:security
```

---

## 🧪 测试用例详情

### Filesystem Server 测试

**测试目标**: 验证本地文件系统访问功能

**测试内容**:
1. 连接到 filesystem server
2. 列出可用工具
3. 读取文件 (`read_file`)
4. 列出目录 (`list_directory`)
5. 创建文件 (`write_file`) - 需用户确认
6. 删除文件 (`delete_file`) - 需用户确认 + 确认码

**预期结果**:
- ✅ 成功连接
- ✅ 列出 5+ 个工具
- ✅ 读取文件内容正确
- ✅ 列出目录内容正确
- ⚠️ 写/删操作需用户确认

---

### GitHub Server 测试

**测试目标**: 验证 GitHub API 集成功能

**测试内容**:
1. 连接到 github server
2. 列出可用工具
3. 读取仓库信息 (`get_repository`)
4. 列出 Issues (`list_issues`)
5. 创建 Issue (`create_issue`) - 需用户确认
6. 读取用户信息 (`get_user`)

**预期结果**:
- ✅ 成功连接
- ✅ 列出 10+ 个工具
- ✅ 读取仓库信息正确
- ✅ 列出 Issues 正确
- ⚠️ 创建/修改操作需用户确认

---

## 🔒 安全测试

### 权限验证
- [ ] 未批准的工具调用被阻止
- [ ] 未批准的资源访问被阻止
- [ ] 敏感操作需要二次确认
- [ ] 确认码验证 (`Qazwsx12@` 或 `确认`)

### 数据泄露防护
- [ ] 文件路径限制在工作目录内
- [ ] GitHub token 不泄露到日志
- [ ] 外部服务器无法访问本地敏感文件

---

## 📊 测试报告模板

```markdown
### 测试日期：YYYY-MM-DD

**测试人员**: [姓名]
**环境**: Windows/macOS/Linux, Node.js 版本

#### 通过测试
- ✅ 测试用例 1
- ✅ 测试用例 2

#### 失败测试
- ❌ 测试用例 3
  - **错误**: [错误信息]
  - **原因**: [根本原因]
  - **解决方案**: [修复方法]

#### 待改进
- ⚠️ 性能问题：[描述]
- 💡 建议：[改进建议]
```

---

## 🐛 已知问题

1. **Windows 路径问题**
   - 问题：反斜杠 `\` 可能需要转义
   - 解决：使用正斜杠 `/` 或双反斜杠 `\\`

2. **npx 首次运行慢**
   - 问题：首次运行需要下载 server
   - 解决：耐心等待，后续会缓存

3. **GitHub Token 权限不足**
   - 问题：token scopes 不够
   - 解决：检查并添加所需 scopes

---

## 📚 参考资料

- [MCP 官方规范](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Server 注册表](https://registry.mcp.run)
- [Filesystem Server 源码](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [GitHub Server 源码](https://github.com/modelcontextprotocol/servers/tree/main/src/github)

---

*最后更新：2026-03-17*
