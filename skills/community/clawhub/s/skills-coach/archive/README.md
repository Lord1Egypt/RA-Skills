# Archive Directory

This directory contains historical files that are no longer actively used but kept for reference.

## Contents

### backups/
Backup files created during development:
- `smart_task_generator.py.backup` - Sample-agent backup before v2.0 enhancements
- `evaluator.py.backup` - Evaluate-agent backup before v2.0 enhancements
- `training_free_grpo_optimizer.py.backup` - Optimizer backup
- `training_free_grpo_optimizer_clean.py` - Alternative optimizer implementation
- `training_free_grpo_simple.py` - Simplified optimizer version
- `run_training_free_grpo.py` - Standalone runner script

### docs/
Historical documentation files:
- `AGENT_OPTIMIZATION_SUMMARY.md` - Agent optimization process documentation
- `CHANGELOG_v2.2.0.md` - Version 2.2.0 changelog
- `COMPLETION_SUMMARY.md` - Project completion summary
- `IMPLEMENTATION_REPORT.md` - Detailed implementation report
- `README_TRAINING_FREE_GRPO.md` - Training-Free GRPO explanation

## Note

All information from these files has been consolidated into the main README.md.
These files are kept for historical reference only.

## Restoration

If you need to restore any of these files:

```bash
# Restore a backup
cp archive/backups/[filename] subskills/[agent-name]/

# View historical documentation
cat archive/docs/[filename]
```
