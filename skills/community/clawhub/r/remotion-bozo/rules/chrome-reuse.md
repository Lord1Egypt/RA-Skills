# Chrome 复用配置

避免每次渲染都重复下载 chrome-headless-shell，复用已安装的浏览器。

## 问题说明

默认情况下，每次创建新的 Remotion 项目时，渲染视频都会从 Google 下载 chrome-headless-shell（约 90MB）。

## 解决方案

### 方案一：复用 Playwright 的 Chrome（推荐）

Playwright 已经下载了 chrome-headless-shell，可以直接复用。

#### 查找 Playwright Chrome

```bash
# macOS
ls ~/Library/Caches/ms-playwright/chromium_headless_shell-*/

# Linux
ls ~/.cache/ms-playwright/chromium_headless_shell-*/

# Windows
dir %USERPROFILE%\AppData\Local\ms-playwright\chromium_headless_shell-*\
```

#### 设置环境变量

在 `~/.zshrc` 中添加：

```bash
# macOS
export REMOTION_BROWSER_EXECUTABLE="$HOME/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell"

# 如果你的路径不同，请根据实际路径调整
```

然后重新加载：

```bash
source ~/.zshrc
```

### 方案二：使用全局安装的 Chrome

如果你已经全局安装了 Chrome，也可以使用它。

```bash
# 在 ~/.zshrc 中添加
export REMOTION_BROWSER_EXECUTABLE="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

### 方案三：缓存到固定位置

首次下载后，将 chrome-headless-shell 复制到固定位置。

#### 步骤

```bash
# 1. 创建缓存目录
mkdir -p ~/Library/Caches/remotion

# 2. 从任意 Remotion 项目中复制 chrome-headless-shell
cp -r node_modules/.remotion/chrome-headless-shell ~/Library/Caches/remotion/

# 3. 在 ~/.zshrc 中添加
export REMOTION_BROWSER_EXECUTABLE="$HOME/Library/Caches/remotion/chrome-headless-shell/macos-arm64/chrome-headless-shell"
```

### 方案四：使用 Puppeteer 的 Chrome

如果你也使用了 Puppeteer，可以复用它的 Chrome。

```bash
# 在 ~/.zshrc 中添加
export REMOTION_BROWSER_EXECUTABLE="$HOME/.cache/puppeteer/chrome/*/chrome-mac-arm64/chrome"
```

## 验证配置

### 检查是否生效

```bash
# 查看当前使用的浏览器
echo $REMOTION_BROWSER_EXECUTABLE

# 预览时测试
remotion studio src/index.tsx

# 如果没有重新下载，说明配置成功
```

### 测试渲染

```bash
# 创建测试项目
mkdir test-remotion && cd test-remotion
npm init -y
npm install remotion react react-dom

# 创建简单视频组件
# （创建 src/index.tsx 和 src/Video.tsx）

# 渲染测试
remotion render src/index.tsx Video test.mp4
```

如果没有出现 "Getting Headless Shell" 的下载提示，说明配置成功！

## 当前系统 Chrome 位置

根据你的系统，chrome-headless-shell 的位置可能是：

### macOS (M1/M2 ARM)

```bash
# Playwright 版本
~/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell

# Puppeteer 版本
~/.cache/puppeteer/chrome/mac-arm64-xxx/chrome-mac-arm64/chrome
```

### macOS (Intel)

```bash
# Playwright 版本
~/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-x64/chrome-headless-shell

# Puppeteer 版本
~/.cache/puppeteer/chrome/mac-x64-xxx/chrome-mac-x64/chrome
```

### Linux

```bash
# Playwright 版本
~/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell
```

### Windows

```bash
# Playwright 版本
%USERPROFILE%\AppData\Local\ms-playwright\chromium_headless_shell-1208\chrome-headless-shell-win64\chrome-headless-shell.exe
```

## 推荐配置

### ~/.zshrc 添加内容

```bash
# Remotion Chrome 复用配置
# 检测并使用 Playwright 的 Chrome
if [ -f "$HOME/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell" ]; then
  export REMOTION_BROWSER_EXECUTABLE="$HOME/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell"
  echo "✓ Remotion using Playwright Chrome"
elif [ -f "$HOME/.cache/puppeteer/chrome/mac/arm-*/chrome-mac-arm64/chrome" ]; then
  export REMOTION_BROWSER_EXECUTABLE=$(find ~/.cache/puppeteer/chrome -name "chrome-mac-arm64/chrome" | head -1)
  echo "✓ Remotion using Puppeteer Chrome"
else
  echo "⚠ Remotion will download Chrome on first render"
fi
```

## 性能对比

| 方式 | 首次渲染 | 后续渲染 | 磁盘占用 |
|------|----------|----------|----------|
| 默认下载 | ~3分钟 | ~3分钟 | 每个 ~90MB |
| 复用 Chrome | ~1分钟 | ~1分钟 | 共享 ~90MB |
| 系统 Chrome | 即时 | 即时 | 0MB (已安装) |

## 故障排除

### Chrome 版本不兼容

如果遇到版本不兼容错误：

```bash
# 更新 Playwright
cd ~/.claude/skills/playwright-skill
npx playwright install chromium
```

### 权限问题

```bash
# 添加执行权限
chmod +x $REMOTION_BROWSER_EXECUTABLE
```

### 环境变量未生效

```bash
# 确认配置已加载
echo $REMOTION_BROWSER_EXECUTABLE

# 如果为空，手动加载
source ~/.zshrc
```
