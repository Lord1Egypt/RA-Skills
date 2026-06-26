# Skill Dependency Resolver

**自动检测并解决技能间的 Python 依赖冲突**

## 描述

当安装多个 OpenClaw 技能时，不同技能可能依赖不同版本的 Python 包（如 pandas、numpy），导致冲突和安装失败。本技能自动扫描所有技能的 `requirements.txt`，检测版本冲突，并提供自动解决策略，生成统一的 `requirements-merged.txt` 供一键安装。

## 使用场景

- 用户安装多个技能后出现 `pip install` 版本冲突错误
- 技能开发者希望确保自己的技能与其他技能兼容
- 系统管理员需要批量部署技能到多台机器
- 希望自动化依赖管理，减少手动调试时间

## 功能清单

- ✅ 扫描指定技能目录下的所有 `requirements.txt`
- ✅ 解析包名和版本规范（>=, <=, ~=, ==, !=）
- ✅ 检测同一包的不同版本要求
- ✅ 提供自动解决策略（选择最高版本或最低版本）
- ✅ 支持手动模式，列出冲突供用户选择
- ✅ 生成合并后的 `requirements.txt`
- ✅ 输出简洁的分析报告（JSON 格式）
- ✅ 零外部依赖，纯 Python 标准库实现

## 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skills_dir` | string | 否 | `~/.openclaw/workspace/skills` | 技能目录路径，递归搜索所有子目录的 requirements.txt |
| `output_file` | string | 否 | `./requirements-merged.txt` | 输出的合并后 requirements 文件路径 |
| `strategy` | string | 否 | `auto` | 冲突解决策略：`auto`（自动选最高版本），`manual`（列出冲突等待用户选择） |

## 输出

- `report` (object): 依赖分析报告
  - `total_skills` (int): 扫描的技能数量
  - `conflicts_count` (int): 检测到的冲突数量
  - `solutions` (array): 每个冲突的解决方案（包名、冲突版本、选定版本、策略）
  - `output_path` (string): 生成的 merged requirements 文件路径
  - `summary` (string): 简要总结

## 示例

### 基本扫描（自动解决）
```bash
skill-dependency-resolver skills_dir="./skills" output_file="requirements.txt"
```

### 手动模式（列出冲突供选择）
```bash
skill-dependency-resolver strategy="manual"
```

### 扫描并生成报告
```bash
skill-dependency-resolver output_file="/tmp/merged.txt" | jq '.conflicts_count'
```

## 技术细节

- **扫描机制**：使用 `os.walk` 递归查找 `requirements.txt`，跳过 `tests/` 和 `node_modules/`
- **解析器**：使用正则表达式解析包名和版本规范，支持 `pkg>=1.0,<=2.0` 格式
- **冲突检测**：收集每个包的所有版本范围，检查是否存在不可交集的区间
- **解决算法**：
  - `auto`：取所有版本上限中的最小值（保守）或下限中的最大值（激进，当前使用：选最高版本）
  - `manual`：输出冲突详情供用户决策
- **输出生成**：将选定版本写入新 requirements 文件，保留原始注释（如有）

## 限制

- 仅支持 Python `requirements.txt` 格式，不支持 `Pipfile` 或 `pyproject.toml`
- 版本规范解析基于正则，可能无法覆盖所有复杂情况（如环境标记 `; python_version < "3.8"`）
- 不执行实际的 `pip install`，仅生成合并后的文件

## 未来增强

- 支持 `pyproject.toml` 和 `Pipfile`
- 检测并建议虚拟环境（避免全局冲突）
- 集成到 `clawhub install` 流程，自动预处理依赖
- 提供冲突解决的历史记录和回滚

## 相关技能

- `skill-composer`：工作流编排，可调用本技能预处理依赖
- `skill-secure-checker`：安全扫描，确保合并后的 requirements 无恶意包
- `workspace-heartbeat-integration`：定期扫描依赖，保持系统健康

---

**作者**：小叮当  
**标签**：devops, dependency, installation, quality  
**许可证**：MIT
