# 安装指南

## 前置要求

- Node.js 18+
- npm 或 yarn

## 安装步骤

### 1. 清理旧的依赖（如果存在）

```bash
# Windows
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item package-lock.json -ErrorAction SilentlyContinue

# Linux/macOS
rm -rf node_modules package-lock.json
```

### 2. 安装依赖

```bash
npm install
```

如果遇到问题，可以尝试：

```bash
npm install --legacy-peer-deps
```

### 3. 首次登录

```bash
npm run login
```

### 4. 启动服务

```bash
npm start
```

服务将在 http://localhost:18060/mcp 启动

## 常见问题

### Q: npm install 失败

尝试清理 npm 缓存：

```bash
npm cache clean --force
npm install
```

### Q: Puppeteer 下载失败

设置 Puppeteer 下载镜像：

```bash
# Windows (PowerShell)
$env:PUPPETEER_DOWNLOAD_HOST = "https://npmmirror.com/mirrors"
npm install

# Linux/macOS
PUPPETEER_DOWNLOAD_HOST=https://npmmirror.com/mirrors npm install
```

### Q: 端口被占用

修改环境变量：

```bash
# Windows (PowerShell)
$env:XHS_PORT = "18061"
npm start

# Linux/macOS
XHS_PORT=18061 npm start
```

## 验证安装

```bash
# 使用 MCP Inspector 验证
npx @modelcontextprotocol/inspector
```

然后连接到 `http://localhost:18060/mcp`
