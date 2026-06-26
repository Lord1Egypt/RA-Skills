# ClawHub 技能更新速查

## 首次登录（仅需一次）

```bash
clawhub login --device --no-browser
# 然后在手机/浏览器上打开提示的URL，输入设备码
```

## 日常更新流程

### 1. 修改代码
编辑 `~/.workbuddy/skills/rus-chn05-analyzer/` 下的文件

### 2. 更新版本号
编辑 `SKILL.md` 的 frontmatter：
```yaml
version: 1.0.0  →  version: 1.0.1  (修bug)
                  →  version: 1.1.0  (加功能)
                  →  version: 2.0.0  (大改版)
```

### 3. 发布新版本
```bash
clawhub skill publish ~/.workbuddy/skills/rus-chn05-analyzer --version 1.0.1
```

### 4. 同步到 Gitee + GitHub
```bash
cd ~/.workbuddy/skills/rus-chn05-analyzer
git add -A && git commit -m "v1.0.1: 描述改动内容"
git push gitee main
# GitHub 需要通过 API 上传（如果 github.com 不可访问）
```

## 注意事项

- ClawHub **不支持增量更新**，每次更新 = 发布新版本
- 旧版本不可修改，但用户仍可通过指定版本号访问
- `latest` 标签自动指向最新版本
- 发布会触发安全扫描，通过后对用户可见
- 技能文件名不能以 `.` 开头（.env.example、.gitignore 会被拒绝）
- `.git` 目录不要包含在上传中

## 三平台同步状态

| 平台 | 仓库地址 | 认证方式 |
|------|---------|---------|
| Gitee | https://gitee.com/povoss/rus-chn05-analyzer | PAT: d7dd...52d |
| GitHub | https://github.com/povoss/rus-chn05-analyzer | PAT: ghp_e6...PA (API上传) |
| ClawHub | https://clawhub.ai/skills/rus-chn05-analyzer | GitHub OAuth |
