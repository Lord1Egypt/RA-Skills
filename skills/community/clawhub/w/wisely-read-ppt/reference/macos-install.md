# macOS LibreOffice 安装指南

> 当 `brew install --cask libreoffice` 不可用（无 Homebrew、sudo 被拒、沙盒环境）时，使用本指南的无 sudo 方案。

## 方案 A：Homebrew（推荐，需要已安装 brew）

```bash
brew install --cask libreoffice
brew install poppler  # 可选，缺失时 parse.py 自动 fallback 到 pymupdf
```

安装后 `soffice` 通常已在 PATH 中。如不在：

```bash
sudo ln -sf "/Applications/LibreOffice.app/Contents/MacOS/soffice" /usr/local/bin/soffice
```

## 方案 B：无 sudo 安装（无 Homebrew 或 sudo 被拒）

### 1. 下载 .dmg

根据 CPU 架构选择：

```bash
# Apple Silicon (M1/M2/M3/M4)
curl -L -o ~/Downloads/LibreOffice.dmg "https://download.documentfoundation.org/libreoffice/stable/26.2.5/mac/aarch64/LibreOffice_26.2.5_MacOS_aarch64.dmg"

# Intel (x86_64)
curl -L -o ~/Downloads/LibreOffice.dmg "https://download.documentfoundation.org/libreoffice/stable/26.2.5/mac/x86_64/LibreOffice_26.2.5_MacOS_x86-64.dmg"
```

> 版本号会更新，到 https://www.libreoffice.org/download/ 确认最新版本和 URL。

### 2. 挂载并拷贝到 ~/Applications

```bash
hdiutil attach ~/Downloads/LibreOffice.dmg -nobrowse
mkdir -p ~/Applications
cp -R "/Volumes/LibreOffice/LibreOffice.app" ~/Applications/
hdiutil detach "/Volumes/LibreOffice"
```

### 3. 创建软链接到 ~/.local/bin

```bash
mkdir -p ~/.local/bin
ln -sf ~/Applications/LibreOffice.app/Contents/MacOS/soffice ~/.local/bin/soffice
ln -sf ~/Applications/LibreOffice.app/Contents/MacOS/soffice ~/.local/bin/libreoffice
```

### 4. 配置 PATH

写 `~/.zshenv`（zsh 对交互/非交互/登录 shell 都生效，比 `.zshrc` 更可靠）：

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

> 如果 Bash 工具的非交互 shell 读不到 PATH，改写 `~/.zshenv`：
> ```bash
> echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshenv
> ```

### 5. 验证

```bash
soffice --version
```

### 6. poppler（可选）

parse.py 检测不到 `pdftoppm` 时自动 fallback 到 `pymupdf`，功能等价。如需安装：

```bash
brew install poppler  # 有 brew 时
```

无 brew 且无 sudo 时跳过，不影响正常使用。

## local-env.json macOS 示例

```json
{
  "platform": "darwin",
  "hasDisplay": true,
  "renderer": "libreoffice",
  "sofficePath": "/Users/<用户名>/Applications/LibreOffice.app/Contents/MacOS/soffice",
  "wpsAvailable": false,
  "notes": "无 sudo 安装到 ~/Applications，soffice 软链到 ~/.local/bin"
}
```

## 注意事项

- `parse.py` 用 `shutil.which("soffice")` 查 PATH，**不读 `local-env.json` 的 `sofficePath`**，所以 soffice 必须出现在 PATH 里
- pip 安装 Python 依赖时，`cryptography`/`pyzipper` 等包如遇编译失败（沙盒 SIGKILL），加 `--only-binary :all:` 参数
- 首次运行 LibreOffice 可能弹出 EULA/安全提示，需在 GUI 中确认
