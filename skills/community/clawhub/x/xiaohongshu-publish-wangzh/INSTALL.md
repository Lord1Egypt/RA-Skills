# 安装指南

## 本地开发安装
```bash
# 复制技能到OpenClaw技能目录
cp -r xiaohongshu-publisher ~/.openclaw/skills/

# 或者创建符号链接（推荐用于开发）
ln -s $(pwd)/xiaohongshu-publisher ~/.openclaw/skills/xiaohongshu-publisher
```

## 通过ClawHub发布（可选）
如果要将此技能发布到ClawHub供其他人使用：

1. 确保已安装clawhub CLI
2. 在技能目录下运行：
```bash
clawhub publish
```

## 依赖验证
确保以下依赖已正确配置：
- OpenClaw 浏览器自动化支持
- 已登录的小红书创作者账号

## 测试安装
```bash
# 验证技能是否被正确识别
openclaw skill list | grep xiaohongshu-publisher

# 运行测试（提供测试标题和内容）
openclaw skill run xiaohongshu-publisher --title "测试标题" --content "测试内容"
```