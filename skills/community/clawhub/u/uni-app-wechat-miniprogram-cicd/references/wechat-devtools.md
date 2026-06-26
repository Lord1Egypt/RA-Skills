# 微信开发者工具 CLI 参考

## 开启服务端口

微信开发者工具必须开启 CLI 功能：

1. 打开微信开发者工具
2. 点击右上角 **设置 → 安全设置**
3. 勾选 **开启服务端口**

## CLI 路径

```
Windows: C:\Program Files (x86)\Tencent\微信web开发者工具\WechatDevTools\1.02.xxx\cli.bat
Windows (新版): %LOCALAPPDATA%\微信开发者工具\cli.bat
macOS: /Applications/wechat devtools/Contents/MacOS/cli
Linux: ~/WeChatWebDevTools/cli.sh
```

## 常用 CLI 命令

### 登录

```bash
# 打开登录界面（需手动扫码）
cli.bat open --project "C:\project\my-miniprogram"
```

### 预览

```bash
# 指定项目路径预览（生成二维码）
cli.bat preview --project "C:\project\dist\build\mp-weixin" --compile-type miniprogram
```

### 上传（已废弃，推荐使用 miniprogram-ci）

微信开发者工具 CLI `upload` 命令已弃用，请使用 `miniprogram-ci`。

## project.config.json 关键配置

```json
{
  "miniprogramRoot": "./dist/build/mp-weixin/",
  "projectname": "my-uniapp-project",
  "compileType": "miniprogram",
  "appid": "wx0123456789abcdef",
  "setting": {
    "urlCheck": false,
    "es6": true,
    "postcss": true,
    "minified": true,
    "newFeature": true,
    "bigPackageSizeSupport": true
  },
  "libVersion": "3.3.5"
}
```

## 常见问题

| 问题 | 解决方案 |
|---|---|
| `CLI 启动失败` | 确认已开启服务端口，重启开发者工具 |
| `登录态失效` | CI 环境中需预先登录；推荐使用 `miniprogram-ci` 无需 GUI 登录 |
| `preview 生成二维码失败` | 检查项目路径是否包含中文或特殊字符 |
| 端口被占用 | `netstat -ano | findstr 54231`，kill 对应 PID |
