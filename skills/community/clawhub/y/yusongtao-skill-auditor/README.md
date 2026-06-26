# Skill Auditor - 技能安全审计工具

## 功能说明
此技能用于审计OpenClaw技能的安全性，检测可能存在的恶意代码或高风险操作。

## 审计项目
- 检测动态代码执行（exec, eval等）
- 检测系统命令执行（subprocess, os.system等）
- 检测网络操作（socket, requests等）
- 检测文件写入操作
- 检测敏感信息（密码、token等）
- 检测危险导入模块

## 使用方法
```python
from auditor import SkillAuditor

auditor = SkillAuditor('audit_config.json')
result = auditor.scan_skill_directory('/path/to/skill')
report = auditor.generate_report(result)
```

## 安全规则
配置文件 `audit_config.json` 包含可自定义的安全规则，可以根据需要调整检测模式。