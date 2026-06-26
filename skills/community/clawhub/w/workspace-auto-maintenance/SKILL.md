# Workspace Auto Maintenance
## 技能描述
OpenClaw工作空间自动化运维技能，支持健康检查、自动修复常见问题，提升工作空间稳定性和整洁度。

## 核心功能
1. **健康检查**：自动扫描工作空间，计算健康分数，识别问题
2. **自动修复**：支持`--fix`参数自动修复常见问题：
   - 根目录冗余文件自动归档
   - 记忆文件命名规范自动修复
   - 脚本自动添加执行权限
   - Git更改自动提交
3. **自定义规则**：支持扩展自定义检查规则
4. **跨平台支持**：兼容Windows/Linux/macOS平台

## 安装方法
```bash
clawhub install workspace-auto-maintenance
```

## 使用方法
```bash
# 仅执行健康检查
python src/workspace_check.py

# 执行健康检查并自动修复问题
python src/workspace_check.py --fix
```

## 参数说明
- `--fix`：开启自动修复模式，自动修复识别到的可修复问题
- `--threshold <分数>`：自定义健康分数阈值，低于阈值时告警
- `--output <路径>`：导出检查报告到指定路径

## 适配环境
- OpenClaw v0.9+
- Python 3.9+
- 无额外依赖

## 发布信息
- 作者：道一
- 版本：v1.0.0
- 发布日期：2026-04-21
- 许可证：MIT
