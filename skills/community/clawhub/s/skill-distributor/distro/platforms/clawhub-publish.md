# ClawHub 发布命令

## 发布命令
```bash
cd /path/to/skill-distributor
clawhub skill publish . \
  --name "skill-distributor" \
  --version "1.0.0" \
  --changelog "Initial release"
```

## 前置条件
1. 安装 clawhub CLI：`npm install -g clawhub`
2. 登录：`clawhub login`
3. 需要 GitHub OAuth 授权

## 依赖
- Node.js 18+
- GitHub 账号

## 发布后链接
https://clawhub.ai/skills/skill-distributor

## 注意
- `--workdir .` 必须添加，否则找不到 SKILL.md
- `--version` 必须为字符串格式：`"1.0.0"`
