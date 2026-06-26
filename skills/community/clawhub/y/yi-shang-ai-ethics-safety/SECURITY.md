# 🔒 安全与隐私声明

## 安全原则

本技能（yi-shang-ai-ethics-safety）严格遵守以下安全与隐私原则：

### ✅ 已实现的安全措施

| 安全项 | 状态 | 说明 |
|--------|------|------|
| **不读取系统历史记录** | ✅ 已实现 | 移除了 `subprocess.run(['sh', '-c', 'history 10'])` 代码 |
| **无硬编码个人路径** | ✅ 已实现 | 使用 `Path(__file__).parent` 动态获取相对路径 |
| **参数化配置** | ✅ 已实现 | 支持 `--text` 和 `--output-dir` 参数自定义 |
| **最小权限原则** | ✅ 已实现 | 仅需要标准文件读写权限 |
| **透明输入输出** | ✅ 已实现 | 所有操作均可通过命令行参数控制 |

### ❌ 已移除的风险代码

**修复前 (v1.2.0):**
```python
# ❌ 风险 1: 读取 Shell 历史记录
import subprocess
result = subprocess.run(['sh', '-c', 'history 10'], capture_output=True, text=True)

# ❌ 风险 2: 硬编码个人路径
sys.path.append('/path/to/user/specific/location/scripts')
reports_dir = '/path/to/user/specific/location/reports'
```

**修复后 (v1.2.1):**
```python
# ✅ 使用参数化输入
parser.add_argument("--text", "-t", type=str, help="待审计的 AI 响应文本")

# ✅ 使用相对路径
SCRIPT_DIR = Path(__file__).parent.parent
reports_dir = Path(output_dir)  # 可配置
```

## 使用说明

### 安全运行方式

```bash
# 方式 1: 命令行参数（推荐）
python scripts/run_audit.py \
  --text "待检测的 AI 文本" \
  --output-dir ./reports

# 方式 2: 默认配置（使用示例文本）
python scripts/run_audit.py

# 方式 3: 在代码中调用
from scripts.run_audit import run_audit_and_save_report
run_audit_and_save_report("待检测文本", "./custom-output-dir")
```

### 权限需求

- **文件系统**: 仅需要在指定输出目录的写权限
- **系统权限**: 不需要任何特殊权限（如 root、sudo）
- **网络访问**: 不需要网络访问
- **其他**: 不访问系统配置、环境变量或个人文件

## 审计日志

### v1.2.1 安全更新 (2026-03-30)

**更新内容:**
- ✅ 移除 `subprocess` 模块调用
- ✅ 移除 Shell 历史记录读取功能
- ✅ 移除所有硬编码的绝对路径
- ✅ 添加参数化配置支持
- ✅ 更新文档说明安全原则

**影响范围:**
- `scripts/run_audit.py` - 完全重构
- `scripts/reports/generate_audit_report.py` - 路径处理改进
- `SKILL.md` - 添加安全声明章节
- `_meta.json` - 版本更新为 1.2.1

## 验证方法

```bash
# 1. 检查是否包含敏感代码
grep -r "subprocess\|history\|figocheung" scripts/ || echo "✅ 无敏感代码"

# 2. 测试参数化功能
python scripts/run_audit.py --help

# 3. 运行完整测试
python scripts/run_audit.py --text "测试文本" --output-dir ./reports
```

## 联系方式

如发现任何安全问题，请通过以下渠道联系：

- **项目维护者**: Figo Cheung
- **技能名称**: yi-shang-ai-ethics-safety
- **平台**: ClawHub

---

*本技能承诺：以义为体，以情智为用 - 不仅守护 AI 伦理，也守护用户隐私。* 🌿
