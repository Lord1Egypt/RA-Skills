# 安装指南

> 所有平台和方法的完整安装说明。

## 📋 前置条件

安装前，请验证您拥有：

```bash
# 检查 Node.js 版本（必须 >= 18.0.0）
node --version

# 检查 npm 版本（必须 >= 9.0.0）
npm --version

# 检查 Git
git --version
```

**向量搜索的可选依赖：**
```bash
# 安装 Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# 启动 Ollama 并加载嵌入模型
ollama pull nomic-embed-text
ollama serve
```

## 📥 安装方法

### 方法 1：安装脚本（推荐）

安装脚本自动处理所有依赖和配置。

```bash
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

**脚本执行的操作：**
1. 检测您的操作系统和架构
2. 创建 `~/.unified-memory/` 目录
3. 全局安装 npm 包或克隆仓库
4. 设置配置文件
5. 初始化存储目录
6. 验证安装

### 方法 2：npm 全局安装

```bash
npm install -g unified-memory
```

**验证安装：**
```bash
unified-memory --version
# 应该输出：v5.2.0
```

### 方法 3：npm 本地安装（项目依赖）

```bash
# 创建新项目
mkdir my-project && cd my-project
npm init -y

# 作为依赖安装
npm install unified-memory
```

### 方法 4：手动克隆

```bash
# 克隆仓库
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory

# 安装依赖
npm install

# 构建生产版本
npm run deploy

# 全局链接（可选）
npm link
```

## 🐧 Linux 安装

### Ubuntu/Debian

```bash
# 安装依赖
sudo apt update
sudo apt install -y nodejs npm git

# 安装 Unified Memory
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

### Fedora/RHEL/CentOS

```bash
# 从 NodeSource 安装 Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs npm git

# 安装 Unified Memory
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

## 🍎 macOS 安装

### 使用 Homebrew

```bash
# 安装 Homebrew（如果还没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js
brew install node

# 安装 Unified Memory
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

### 使用 nvm

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc

# 安装并使用 Node.js 18
nvm install 18
nvm use 18

# 安装 Unified Memory
npm install -g unified-memory
```

## 🪟 Windows 安装

### 使用 Node.js 安装程序

1. 从 [nodejs.org](https://nodejs.org/) 下载 Node.js 18+
2. 运行安装程序
3. 打开 PowerShell 并安装：

```powershell
npm install -g unified-memory
```

### 使用 Windows 子系统 Linux (WSL)

```bash
# 打开 WSL 终端
wsl

# 按照 Linux 安装说明进行
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

## 🐳 Docker 安装

### 使用预构建镜像

```bash
# 拉取镜像
docker pull mouxangithub/unified-memory:latest

# 运行容器
docker run -d \
  --name unified-memory \
  -v ~/.unified-memory:/data \
  -p 3851:3851 \
  mouxangithub/unified-memory:latest
```

### 构建自己的镜像

```dockerfile
FROM node:18-alpine

WORKDIR /app
RUN npm install -g unified-memory

VOLUME ["/data"]
EXPOSE 3851

CMD ["unified-memory", "serve"]
```

构建并运行：
```bash
docker build -t my-unified-memory .
docker run -d -v ~/.unified-memory:/data -p 3851:3851 my-unified-memory
```

## ⚙️ 安装后设置

### 1. 验证安装

```bash
unified-memory --version
# 输出：v5.2.0

unified-memory --help
```

### 2. 初始化存储

```bash
unified-memory init
```

这会创建：
- `~/.unified-memory/memories.json` - 主记忆存储
- `~/.unified-memory/vector.lance` - 向量数据库
- `~/.unified-memory/config.json` - 配置文件

### 3. 配置（可选）

编辑 `~/.unified-memory/config.json`：

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance"
    }
  },
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log"
  },
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7
  }
}
```

### 4. 启动 MCP 服务器

```bash
# 后台启动
unified-memory serve &

# 或使用 Node.js API
node -e "require('unified-memory').serve()"
```

## 🔧 安装故障排除

### "权限被拒绝" 错误

```bash
# 修复 npm 权限
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 或使用 sudo（不推荐）
sudo npm install -g unified-memory
```

### "Node.js 版本太旧" 错误

```bash
# 使用 nvm 更新 Node.js
nvm install 18
nvm use 18
nvm alias default 18
```

### "找不到模块" 安装后

```bash
# 重新安装依赖
npm cache clean --force
npm install
```

### Ollama 连接错误（向量搜索）

```bash
# 确保 Ollama 正在运行
ollama serve

# 测试 Ollama
curl http://localhost:11434/api/generate -d '{"model":"llama2","prompt":"Hi"}'

# 拉取嵌入模型
ollama pull nomic-embed-text
```

## 📦 卸载

```bash
# 删除 npm 包
npm uninstall -g unified-memory

# 删除数据目录（可选）
rm -rf ~/.unified-memory

# 删除 CLI 工具
rm -f /usr/local/bin/unified-memory
```

## 🚀 下一步

- [快速入门教程](./quickstart.md) - 存储您的第一个记忆
- [配置指南](./configuration.md) - 自定义设置
- [基础使用指南](../guides/basic-usage.md) - 学习核心操作
