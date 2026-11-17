# 链私有蓝皮书

每条链创建时自动保存步骤接口快照到 `chains/{name}/blueprints.json`，同时记录所有涉及 skill 的 SKILL.md md5。

**执行前自动校验：**
chain_executor plan 自动比对 blueprints.json 中的 _skill_md5s vs 当前 SKILL.md，偏移则阻断。

```bash
chain_manager.py check-health --name "链名"
```
