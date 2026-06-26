# SocialPost-Auto 技能包

社交媒体自动化运营助手 - OpenClaw 技能

## 文件结构

```
socialpost-auto/
├── SKILL.md              # 技能定义文件（必需）
├── package.json          # 包配置
├── crontab-example.txt   # 定时任务示例
├── README.md             # 本文件
├── scripts/
│   └── post.py           # 核心发布脚本
└── data/
    └── tasks.json        # 任务数据（运行时生成）
```

## 安装步骤

1. 将 `socialpost-auto` 文件夹复制到 `~/.openclaw/workspace/skills/`

2. 配置 `~/.openclaw/openclaw.json`，添加平台凭据

3. （可选）添加 cron 定时任务：
   ```bash
   crontab -e
   # 添加 crontab-example.txt 中的内容
   ```

## 使用方法

### 手动发布
```bash
python3 scripts/post.py add twitter "今天 AI 又有了新突破..." "2026-04-10T09:00:00"
```

### 执行定时任务
```bash
python3 scripts/post.py run
```

### 查看任务列表
```bash
python3 scripts/post.py list
```

## 支持平台

- ✅ Twitter (X)
- ✅ 小红书
- ✅ 微博
- 🔄 更多平台开发中...

## 定价

- **免费版**: $0/月 - 1 个账号，1 条/日，仅 Twitter
- **专业版**: $19/月 - 3 个账号，5 条/日，全平台
- **企业版**: $49/月 - 10 个账号，无限发布，自动回复

## 联系

📧 ai.agent.anson@qq.com  
🏠 https://asmartglobal.com

## 作者

Anson @ Jiufang Intelligent (Shenzhen)

## 许可证

MIT-0
