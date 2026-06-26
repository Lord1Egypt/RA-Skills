# Search and Audit Guide | 搜索与审计指南

## Search workflow | 搜索流程

1. Check local formal skills first.  
   先检查本地正式技能。
2. Check built-in skills if relevant.  
   如有需要，再检查内置技能。
3. Search ClawHub only when local options are insufficient.  
   只有在本地选项不足时才搜索 ClawHub。
4. Let the user choose before install or replacement.  
   在安装或替换前，让用户做选择。

## Search commands | 搜索相关命令

```bash
clawhub search <query>
clawhub inspect <slug>
clawhub list
clawhub uninstall <slug>
clawhub star <slug>
clawhub unstar <slug>
```

## Audit mindset | 审计思路

Before recommending install or update, check:  
在推荐安装或更新前，检查：
- overlap with existing local skills  
  是否与现有本地技能功能重叠
- whether the skill is actively maintained  
  技能是否还在持续维护
- whether the skill description matches the user's real need  
  技能描述是否真的匹配用户需求
- whether sensitive or risky behavior needs review  
  是否存在需要额外审查的敏感或高风险行为

## Output style | 输出风格

Give the user a short comparison:  
给用户一个简短对比：
- recommended  
  推荐
- possible alternative  
  可选替代
- not recommended  
  不推荐

Keep recommendations concrete.  
建议必须具体，不要空泛。
