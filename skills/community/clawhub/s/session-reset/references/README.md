# 参考资料

## OpenClaw 相关文档

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw Skill 开发指南](https://docs.openclaw.ai/skills)
- [OpenClaw Session 管理](https://docs.openclaw.ai/sessions)

## 相关 Skill

- `skill-creator` - Skill 创建工具
- `skill-hub` - Skill 管理

## 技术参考

### Session 文件格式

```
~/.openclaw/sessions/
├── agent:main:discord:channel:xxx.jsonl
├── agent:hubu:discord:channel:xxx.jsonl
├── cron:xxx.jsonl
└── subagent:xxx.jsonl
```

### 备份文件结构

```
~/.openclaw/session-backups/
└── YYYYMMDD_HHMMSS/
    ├── manifest.json
    ├── agent:main:...jsonl
    └── ...
```

## 最佳实践

1. 修改配置前先预览 (`--dry-run`)
2. 定期清理旧备份 (`--cleanup`)
3. 重要操作前保留备份
4. 低峰期执行批量重置
