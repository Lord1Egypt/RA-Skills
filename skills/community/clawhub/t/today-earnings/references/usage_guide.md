# 使用指南

这个文件只放操作层面的信息：安装、运行、输出和排障。

## 环境要求

- Google Chrome（或 Chromium，详见各平台说明）
- Node.js
- 可加载本地 Chrome Extension 的权限

**平台支持：**

| 平台 | 状态 | 说明 |
|------|------|------|
| macOS | ✅ 完整支持 | `install.sh` 自动安装 |
| Linux | ✅ 完整支持 | `install.sh` 自动安装（含 Ubuntu） |
| Windows | ⚠️ 需手动注册 | `install.sh` 生成文件，再运行 `install-windows.bat` |
| WSL | ⚠️ 有限支持 | 建议将仓库放在 Windows 文件系统，再手动注册 |

## 安装步骤

### 1. 加载 Chrome 扩展

1. 打开 `chrome://extensions`
2. 开启右上角"开发者模式"
3. 点击"加载已解压的扩展程序"
4. 选择仓库里的 `chrome-extension/` 目录
5. 记录扩展卡片中的扩展 ID

### 2. 安装 Native Host

在仓库根目录执行：

```bash
bash native-host/install.sh <扩展ID>
```

> **推荐用 `bash` 直接运行**，而不是 `./native-host/install.sh`。
> 解压或 clone 后脚本的执行位（`+x`）可能丢失，直接执行会报"权限不够"，
> 用 `bash` 运行则不依赖执行位，始终可用。

脚本会自动检测操作系统并安装到对应路径（见下方各平台说明）。

#### macOS

自动安装到：

- `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.today.earnings.host.json`
- 如果安装了 Chrome Canary 或 Chromium，也会同时安装到对应目录

#### Linux（含 Ubuntu）

自动安装到：

- `~/.config/google-chrome/NativeMessagingHosts/com.today.earnings.host.json`（Google Chrome）
- `~/.config/chromium/NativeMessagingHosts/com.today.earnings.host.json`（如检测到 Chromium）

**Ubuntu 注意：** Ubuntu 22.04+ 默认的 snap 版 Chromium 不支持 Native Messaging。建议安装 deb 版 Google Chrome：

```bash
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main > /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update && sudo apt-get install google-chrome-stable
```

#### Windows

`install.sh`（在 Git Bash / MINGW 下运行）会生成以下文件：

- `native-host/com.today.earnings.host.json`（manifest 文件）
- `native-host/run-host.bat`（Chrome 调用的包装脚本）
- `native-host/install-windows.bat`（注册表注册脚本）

生成后，**手动执行以下步骤**：

1. 确认 `com.today.earnings.host.json` 中 `"path"` 字段指向 `run-host.bat` 的 Windows 绝对路径，例如：
   ```
   C:\Users\你的用户名\repos\today-earnings-skill\native-host\run-host.bat
   ```
2. 双击运行 `native-host\install-windows.bat`（或在 CMD/PowerShell 中执行）
3. 脚本会将 manifest 路径写入 HKCU 注册表（Chrome 和 Chromium）
4. 重启 Chrome 并刷新扩展

注册表写入位置（仅用户级，无需管理员）：

```
HKCU\Software\Google\Chrome\NativeMessagingHosts\com.today.earnings.host
HKCU\Software\Chromium\NativeMessagingHosts\com.today.earnings.host
```

#### WSL（Windows Subsystem for Linux）

WSL 下 Chrome 运行在 Windows 侧，无法读取 WSL 内部文件系统（`/home/...`）的 manifest。

推荐做法：将仓库克隆到 Windows 文件系统，例如：

```bash
cd /mnt/c/Users/<用户名>/repos
git clone <仓库地址> today-earnings-skill
cd today-earnings-skill
bash native-host/install.sh <扩展ID>
```

然后在 Windows 侧运行生成的 `native-host\install-windows.bat`。

### 3. 刷新扩展

安装 Native Host 后，回到 `chrome://extensions`，对 Today Earnings 扩展点一次刷新。

### 4. 最小验证

```bash
./scripts/get-company-list.sh
```

返回 JSON 数组或空数组 `[]` 都表示调用链路已经通了。

## 运行方式

```bash
# 获取今天数据
./scripts/get-company-list.sh

# 获取指定日期数据
./scripts/get-company-list.sh 2026-03-14
```

## 输出格式

成功时输出 JSON 数组，每项固定字段：

```json
[
  {
    "code": "HPE",
    "earningType": "AMC",
    "marketCap": 28370000000
  }
]
```

字段含义：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | string | 股票代码 |
| `earningType` | string | 财报发布时间，可能为 `AMC`、`BMO`、`TNS` |
| `marketCap` | number | 市值，单位美元，纯数字 |

失败时 stderr 输出错误信息，进程返回非 0。

## 常见问题

### 无法连接 `/tmp/today-earnings.sock`

优先检查：
- Chrome 是否已启动
- 扩展是否已加载并启用
- Native Host 是否已安装
- 安装后是否刷新过扩展

### Native Host 立即退出

常见原因是 `node` 路径变化。重新执行：

```bash
bash native-host/install.sh <扩展ID>
```

### 扩展 ID 不匹配

**macOS：**

```bash
cat ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.today.earnings.host.json
```

**Linux：**

```bash
cat ~/.config/google-chrome/NativeMessagingHosts/com.today.earnings.host.json
```

**Windows：**

在 CMD 中查看注册表：

```cmd
REG QUERY "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.today.earnings.host"
```

确认其中 `allowed_origins` 的扩展 ID 与 `chrome://extensions` 页里显示的一致。

### 超时或页面没加载出来

先手动打开以下页面确认能正常访问：

```text
https://finance.yahoo.com/calendar/earnings?day=2026-03-14&offset=0&size=100
```

如果页面本身打不开，脚本链路也不会成功。

### Linux：snap 版 Chromium 不工作

Ubuntu 默认安装的 snap 版 Chromium 因沙箱限制不支持 Native Messaging。请改用 deb 版 Google Chrome（安装命令见上方"Linux 安装"章节）。
