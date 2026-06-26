# 微信公众号配置模板

## 使用说明

1. 复制本文件为 `config.sh`
2. 填入你的真实凭证
3. 确保 `config.sh` 不被提交到版本控制（加入 .gitignore）

```bash
# 微信公众号凭证配置
# 获取方式：微信公众平台 → 设置与开发 → 基本配置

# ⚠️ 请替换为你的真实 AppID
APPID="wxYOUR_APPID_HERE"

# ⚠️ 请替换为你的真实 AppSecret
APPSECRET="YOUR_SECRET_HERE"

# ⚠️ 可选：配置 IP 白名单
# 登录微信公众平台 → 设置与开发 → 基本配置 → IP 白名单
# 添加你的服务器 IP 地址
```

## 获取凭证步骤

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入 **设置与开发** → **基本配置**
3. 复制 **AppID(应用 ID)**
4. 生成并复制 **AppSecret(应用密钥)**
5. 配置 **IP 白名单**（添加你的服务器公网 IP）

## 安全提醒

- ❌ 不要将真实凭证提交到公开仓库
- ✅ 使用 `.gitignore` 忽略 `config.sh`
- ✅ 定期更换 AppSecret
- ✅ 限制 IP 白名单范围
