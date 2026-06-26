# Qiniu Upload Skill (tianshu-qiniu-upload)

将本地文件（图片、HTML、文档等）上传到七牛云存储，返回可公网访问的 CDN URL。AI 生成图片或页面后，只需说「上传到七牛」即可获得分享链接。

## 安装

```bash
# 1. 复制到 OpenClaw skills 目录
cp -r skills/tianshu-qiniu-upload ~/.openclaw/skills/

# 2. 安装依赖
cd ~/.openclaw/skills/tianshu-qiniu-upload && npm install

# 3. 配置环境变量（在 openclaw.json 或 .env）
```

## 配置

在 TsClaw 的 Skills 页面，找到 `tianshu-qiniu-upload`，配置以下环境变量：

| 变量 | 说明 |
|------|------|
| QINIU_ACCESS_KEY | 七牛 Access Key |
| QINIU_SECRET_KEY | 七牛 Secret Key |
| QINIU_BUCKET | 存储空间名 |
| QINIU_DOMAIN | 公开访问域名，如 https://xxx.qiniucdn.com |
| QINIU_PREFIX | 存储路径前缀，默认 uploads |

或直接编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "tianshu-qiniu-upload": {
        "enabled": true,
        "env": {
          "QINIU_ACCESS_KEY": "你的AK",
          "QINIU_SECRET_KEY": "你的SK",
          "QINIU_BUCKET": "你的bucket",
          "QINIU_DOMAIN": "https://你的域名",
          "QINIU_PREFIX": "uploads"
        }
      }
    }
  }
}
```

## 使用

对 OpenClaw 说：

- 「帮我生成一个 HTML 页面，上传到七牛」
- 「把这张图片上传到网上」
- 「用 tianshu-qiniu-upload 上传 /tmp/xxx.png」

AI 会生成/写入文件，然后调用上传脚本，返回可访问的 URL。

## 发布到 ClawHub

```bash
# 1. 安装 clawhub CLI
npm install -g clawhub

# 2. 登录（会打开浏览器用 GitHub 授权）
clawhub login

# 3. 在 Skill 目录下发布
cd skills/tianshu-qiniu-upload
clawhub publish . --slug tianshu-qiniu-upload --name "Qiniu Upload" --version 1.0.2 --changelog "Fix SKILL.md metadata format for TsClaw parsing"
```

或通过网页上传：访问 https://clawhub.ai/upload ，用 GitHub 登录后上传 Skill 压缩包。
