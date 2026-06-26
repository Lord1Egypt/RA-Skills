# 巡检报告模板

已安装 skill 定期安全巡检使用以下格式：

```markdown
# Skills 安全巡检

时间: [YYYY-MM-DD HH:MM 时区]
主机: [主机名]
范围: ~/.agents/skills/

## 汇总
- 审查 skill 总数: X
- ✅ 正常: X
- ⚠️ 需关注: X
- ❌ 有问题: X

## 详细结果

### [skill 名称]
- 来源:
- 审查文件数:
- 红旗项:
- 权限:
- 风险等级:
- 结论:
- 备注:

## 建议
- [ ] 移除可疑 skill
- [ ] 复审有变更的 skill
- [ ] 继续监控
```

巡检文件使用时间戳命名：`security-audits/skills-audit-YYYY-MM-DD_HHMM.md`
