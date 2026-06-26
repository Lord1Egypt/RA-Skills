# 工具安装指南

本skill依赖两个外部工具：**opencli** 和 **flyai**。在使用前必须确保两者都已正确安装。

## 快速检查

```bash
# 检查 opencli
which opencli && opencli --version && echo "✅ opencli 已安装" || echo "❌ opencli 未安装"

# 检查 flyai
which flyai && flyai --help > /dev/null 2>&1 && echo "✅ flyai 已安装" || echo "❌ flyai 未安装"

# 检查 opencli 连接状态
opencli doctor
```

如果两个工具都已安装且 opencli doctor 显示连接正常，可直接使用。否则按以下步骤安装。

---

## flyai 安装

### 安装命令

```bash
npm i -g @fly-ai/flyai-cli
```

### 验证安装

```bash
# 查看帮助
flyai --help

# 测试搜索功能
flyai keyword-search --query "what to do in Sanya"
```

预期输出：单行JSON格式，包含搜索结果。

### 可选配置（增强结果）

```bash
flyai config set FLYAI_API_KEY "your-key"
```

配置API key可获得更丰富的搜索结果和更高的请求限额。

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| `npm` 命令不存在 | 先安装 Node.js：`brew install node`（macOS）或从官网下载 |
| 安装后命令找不到 | 检查 npm全局路径：`npm config get prefix`，确保在PATH中 |
| 搜索返回空结果 | 检查网络连接，或尝试更换关键词 |

---

## opencli 安装

opencli 通过复用本地 Chrome 的登录状态，让 AI 能够在终端直接操作网站。

### 前置要求

1. **Node.js**（版本需 ≥ 20.0.0）
2. **Chrome 浏览器**（需要已安装）

### 安装步骤

#### Step 1: 安装 opencli

```bash
# 全局安装
npm install -g @jackwener/opencli

# 验证安装
opencli --version
```

#### Step 2: 安装 Chrome 扩展

1. 访问 OpenCLI GitHub Releases 页面：https://github.com/jackwener/opencli/releases
2. 下载最新版本的 Chrome 扩展（.crx 文件或从 Chrome Web Store 安装）
3. 在 Chrome 中安装扩展：
   - 打开 Chrome → 扩展程序 → 开发者模式 → 加载已解压的扩展程序
   - 或直接从 Chrome Web Store 搜索 "OpenCLI" 安装

#### Step 3: 检查连接状态

```bash
# 检查扩展与后台服务的连接
opencli doctor
```

预期输出：
```
[OK] Daemon: running on port 19825
[OK] Extension: connected
[OK] Connectivity: connected
```

#### Step 4: 配置浏览器连接

```bash
# 自动检测并配置 Chrome 扩展 token
opencli setup
```

#### Step 5: 登录小红书

1. 在 Chrome 中打开 https://www.xiaohongshu.com
2. 登录账号（扫码登录或密码登录）
3. 确保登录状态保持（不要退出）

#### Step 6: 验证小红书搜索

```bash
# 测试小红书搜索
opencli xiaohongshu search "三亚酒店" --limit 5 -f json
```

预期输出：JSON格式，包含小红书搜索结果（标题、作者、点赞数、链接等）。

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| opencli 命令找不到 | 检查 npm 全局路径：`npm config get prefix`，确保在 PATH 中 |
| Node.js 版本过低 | 升级 Node.js：`brew upgrade node`（macOS）或从官网下载最新版 |
| Chrome 未安装 | macOS: `brew install --cask google-chrome`；Windows: 从官网下载 |
| opencli doctor 报错 | 确保 Chrome 扩展已安装并启用，尝试重启 Chrome 或重新运行 `opencli setup` |
| 小红书未登录 | 打开小红书页面，完成登录后再试 |
| 搜索返回空结果 | 检查 Chrome 是否打开，确保小红书登录状态有效 |

### 扩展未连接时的提示

如果 `opencli doctor` 显示 Extension 未连接：

> "需要在 Chrome 安装 **OpenCLI 扩展**。
> 安装步骤：
> 1. 访问 https://github.com/jackwener/opencli/releases 下载扩展
> 2. 打开 Chrome → 扩展程序 → 开启开发者模式 → 加载扩展
> 3. 运行 `opencli setup` 配置连接
> 4. 运行 `opencli doctor` 确认连接状态"

---

## 环境就绪确认清单

继续执行 skill 前，确认以下条件：

- ✅ `opencli` 命令可用（`opencli --version` 显示版本号）
- ✅ `flyai` 命令可用（`which flyai` 返回路径）
- ✅ `opencli doctor` 显示 Daemon、Extension、Connectivity 都正常
- ✅ Chrome 已登录小红书（可访问小红书页面且显示登录状态）

如果任一条件不满足，先完成安装再继续。

---

## 完整安装流程（从零开始）

适用于全新环境：

```bash
# 1. 检查 Node.js 版本
node --version  # 需要 >= 20.0.0

# 2. 安装 opencli
npm install -g @jackwener/opencli

# 3. 验证 opencli
opencli --version

# 4. 安装 Chrome 扩展（手动操作）
# 访问 https://github.com/jackwener/opencli/releases 下载并安装

# 5. 检查连接状态
opencli doctor

# 6. 配置浏览器连接
opencli setup

# 7. 安装 flyai
npm i -g @fly-ai/flyai-cli

# 8. 验证 flyai
flyai --help

# 9. 在 Chrome 中登录小红书（手动操作）
# 打开 https://www.xiaohongshu.com → 扫码/密码登录

# 10. 验证小红书搜索
opencli xiaohongshu search "三亚酒店" --limit 5 -f json

# 11. 全部验证通过
echo "✅ 环境就绪！可以开始使用 smart-hotel-search skill"
```

---

## 参考链接

- **OpenCLI GitHub**: https://github.com/jackwener/opencli
- **OpenCLI npm**: https://www.npmjs.com/package/@jackwener/opencli
- **OpenCLI Releases（Chrome 扩展）**: https://github.com/jackwener/opencli/releases
- **flyai 官网**: https://open.fly.ai/
- **flyai-cli npm**: https://www.npmjs.com/package/@fly-ai/flyai-cli
- **小红书**: https://www.xiaohongshu.com
- **安装教程参考**: https://www.cnblogs.com/dqtx33/p/19778018