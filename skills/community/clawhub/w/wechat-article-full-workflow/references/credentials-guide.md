# 微信公众号凭证获取指南

## 凭证查找顺序

按以下优先级查找 WECHAT_APP_ID 和 WECHAT_APP_SECRET：

1. **Bash session 环境变量**：`$WECHAT_APP_ID` / `$WECHAT_APP_SECRET`
2. **配置文件**：`wechat_config.json`（格式：`{"appid":"...", "secret":"..."}`）
3. **Windows 用户环境变量（PowerShell 只读）**：
   ```powershell
   [Environment]::GetEnvironmentVariable("WECHAT_APP_SECRET", "User")
   [Environment]::GetEnvironmentVariable("WECHAT_APP_ID", "User")
   ```

## 已知配置

- **AppID**: `wxca0592af7747824d`
- **AppSecret 来源**: Windows 用户环境变量 `WECHAT_APP_SECRET`
- **注意**: Bash/Git Bash 默认读取不到 Windows 层级的环境变量，需要用 PowerShell 桥接

## 跨环境传递凭证

在 Bash 中使用时：
```bash
export WECHAT_APP_ID="wxca0592af7747824d"
export WECHAT_APP_SECRET=$(powershell -Command '[Environment]::GetEnvironmentVariable("WECHAT_APP_SECRET","User")')
```

## 公众号信息

- AppID: `wxca0592af7747824d`
- 微信号昵称: `<示例昵称>`（后台预览用）
- 类型: 普通订阅号
- 公众号预览 API 不可用（权限不足 48001），只能后台手动预览
- 推送流程：写文章 → 推草稿箱 → 给预览方式（不群发）
