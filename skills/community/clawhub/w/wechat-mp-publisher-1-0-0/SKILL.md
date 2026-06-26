# 微信公众号发布技能 (wechat-mp-publisher)

通过微信公众平台 API 发布文章到微信公众号。

## 前置条件

1. 已注册微信公众号（订阅号或服务号）
2. 已获取 AppID 和 AppSecret
3. 公众号已认证（服务号需要认证）

## 环境变量

在 `.env` 文件中配置：

```
WECHAT_APPID=你的 appid
WECHAT_APPSECRET=你的 appsecret
```

## 使用方法

### 发布文章

```bash
node index.js publish --title "标题" --content "内容" --author "作者"
```

### 获取 access_token

```bash
node index.js token
```

## API 限制

- access_token 有效期 2 小时
- 每天发布次数有限制（订阅号 1 次/天，服务号 4 次/月）
- 需要服务器 IP 白名单

## 注意事项

- 首次使用需要在微信公众平台配置 IP 白名单
- 建议将技能部署在固定 IP 的服务器上
- AppSecret 需要保密，不要提交到代码库

## 安装步骤

1. 安装依赖：`npm install`
2. 复制配置：`touch .env`
3. 编辑 `.env` 填入你的 WECHAT_APPID 和 WECHAT_APPSECRET
4. 微信公众平台配置 IP 白名单
