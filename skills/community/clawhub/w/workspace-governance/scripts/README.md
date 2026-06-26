# scripts

存放治理辅助脚本，例如：

- 目录结构检查
- 批量审计导出
- 日志归档

建议脚本命名：`check_*.sh`、`check_*.py`。

## 现有脚本

- `check_skill_contract.sh`：检查 `SKILL.md` 是否包含关键治理契约段落
- `check_docs_sync.sh`：检查 `SKILL.md` 与中英文手册是否保持同步结构
- `check_adapt_contract.sh`：检查 `SKILL_ADAPT.yaml` 是否包含关键策略字段
- `check_openclaw_profile.sh`：检查 OpenClaw profile 关键安全字段与合并策略
- `check_hermes_profile.sh`：检查 Hermes profile 关键安全字段与平台策略
- `check_cursor_profile.sh`：检查 Cursor profile 关键安全字段与合并策略
- `check_claude_profile.sh`：检查 Claude Code profile 关键安全字段与合并策略

## 使用示例

```bash
# 在仓库根目录执行
bash scripts/check_skill_contract.sh

# 检查指定文件
bash scripts/check_skill_contract.sh ./SKILL.md

# 检查手册同步
bash scripts/check_docs_sync.sh

# 检查 SKILL_ADAPT 配置契约
bash scripts/check_adapt_contract.sh

# 检查 OpenClaw profile 契约
bash scripts/check_openclaw_profile.sh

# 检查 Hermes profile 契约
bash scripts/check_hermes_profile.sh

# 检查 Cursor profile 契约
bash scripts/check_cursor_profile.sh

# 检查 Claude Code profile 契约
bash scripts/check_claude_profile.sh
```
