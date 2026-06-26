# 安装与配置

## 环境要求

- **Windows 10/11 (x64)**
- **Node.js 18+** — https://nodejs.org（LTS 版本）
- 无需 Python、WSL、Linux 二进制，无需任何外部服务

## 安装步骤

### 第一步：安装依赖

```powershell
cd "E:\qclaw文件\resources\openclaw\config\skills\xiaohongshu-win\scripts"
.\Setup-Xhs.ps1
```

脚本会自动：
1. 检查 Node.js 是否安装
2. `npm install playwright`（约 5MB）
3. `npx playwright install chromium`（约 150MB，下载 Chromium 浏览器）

### 第二步：登录小红书

```powershell
node xhs.js login
```

会弹出 Chromium 浏览器窗口，在里面完成登录（支持扫码/账号密码）。  
登录成功后 Cookie 自动保存到 `%USERPROFILE%\.xiaohongshu-win\cookies.json`，**浏览器持久化 Profile** 保存在 `%USERPROFILE%\.xiaohongshu-win\browser-profile\`。

### 第三步：验证

```powershell
node xhs.js status
```

## Cookie 有效期

Cookie 有效期约 30 天。过期后重新运行 `node xhs.js login`。

## 常见问题

### 执行策略报错
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Chromium 下载慢
设置镜像：
```powershell
$env:PLAYWRIGHT_DOWNLOAD_HOST = "https://npmmirror.com/mirrors/playwright"
npx playwright install chromium
```

### 登录后仍提示未登录
删除旧数据重新登录：
```powershell
Remove-Item -Recurse "$env:USERPROFILE\.xiaohongshu-win" -Force
node xhs.js login
```
