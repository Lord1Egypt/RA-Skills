---
name: skill-assessment
description: "Agent skill quality checker. Input a skill directory or skill files; output trigger clarity, metadata issues, examples, safety boundaries, installability, portability risks, and prioritized fixes. Review-only by default: does not publish, delete, rename, or archive without explicit approval."
license: MIT
---
## 概述
**skill-assessment** 是一个轻量级静态分析工具，用于评估 OpenClaw 技能的质量。它不执行任何代码，仅通过文件分析和元数据检查，从**文档完整性**、**代码规范性**、**配置友好度**、**维护活跃度**四个维度对技能进行评分，帮助用户快速筛选技能，为开发者提供改进方向。

## 触发场景
- 当你想了解某个技能的可靠性和质量时
- 当你在多个相似技能间犹豫不决时  
- 当你开发完技能，想检查潜在问题和改进点时
- 当你需要批量评估所有本地技能，找出薄弱环节时

## 安装
```bash
# 方法1：从 ClawHub 安装（发布后）
clawhub install skill-assessment

# 方法2：本地安装（开发阶段）
cd /path/to/skill-assessment
ln -sf $(pwd) ~/.openclaw/skills/skill-assessment
```

## 使用方式

### 基本用法
```bash
# 评估单个技能
skill-assess ~/.openclaw/skills/skill-creator

# 评估当前目录下的技能
skill-assess .

# 批量评估所有本地技能
skill-assess --all

# 评估并生成JSON格式报告
skill-assess ~/.openclaw/skills/skill-creator --format json

# 仅显示问题清单
skill-assess ~/.openclaw/skills/skill-creator --problems-only

# 对比两个技能
skill-assess --compare skill-creator skill-audit
```

### 输出示例
```
🔍 技能评估报告：skill-creator
📊 综合评分：★★★★☆ (4.2/5)
⏱️ 评估用时：12秒
📁 技能路径：~/.openclaw/skills/skill-creator

维度得分：
  文档完整性：★★★★☆ (4.0/5)
  代码规范性：★★★★★ (4.5/5)
  配置友好度：★★★☆☆ (3.5/5)
  维护活跃度：★★★★☆ (4.0/5)

⚠️ 发现问题：3个
✅ 通过检查：21个
📋 详细报告：~/.openclaw/skills/skill-assessment/reports/skill-creator_2026-03-12.md
```

## 评估维度

### 1. 文档完整性 (权重30%)
- **SKILL.md 存在性**：强制检查，缺失则直接0分
- **必填章节**：name, description, triggers, usage, installation, configuration
- **示例质量**：示例是否可复制，是否有输入输出说明
- **配置说明**：默认配置示例，环境变量支持

### 2. 代码规范性 (权重40%)
- **文件结构**：清晰的目录组织（scripts/, templates/, examples/）
- **安全风险**：硬编码密钥、危险权限、注入漏洞
- **错误处理**：`set -e` 或 `try/catch`，友好的错误提示
- **工具使用**：权限申请合理性，安全边界

### 3. 配置友好度 (权重20%)
- **默认配置**：合理的默认值，不暴露敏感信息
- **配置方式**：支持环境变量、配置文件、命令行参数
- **错误提示**：配置缺失时的明确提示和修复建议

### 4. 维护活跃度 (权重10%)
- **版本管理**：语义化版本号（如 `1.0.0`）
- **更新记录**：CHANGELOG.md 或更新说明
- **最后更新**：3个月内+2分，6个月内+1分，1年内+0.5分

## 评分算法
```
总分 = 
  文档完整性得分 × 30% +
  代码规范性得分 × 40% + 
  配置友好度得分 × 20% +
  维护活跃度得分 × 10%
```

**星级转换**：
- 4.5-5.0: ★★★★★ (优秀)
- 4.0-4.4: ★★★★☆ (良好)  
- 3.5-3.9: ★★★☆☆ (中等)
- 3.0-3.4: ★★☆☆☆ (一般)
- 2.5-2.9: ★☆☆☆☆ (较差)
- <2.5: ☆☆☆☆☆ (不推荐)

## 配置选项
在技能根目录创建 `config.yaml` 或设置环境变量：

```yaml
# config.yaml
weights:
  documentation: 0.3    # 文档完整性权重
  code_quality: 0.4     # 代码规范性权重
  config_friendly: 0.2  # 配置友好度权重
  maintenance: 0.1      # 维护活跃度权重

checks:
  enable_security_scan: true     # 启用安全检查
  enable_performance_check: false # 不启用性能检查（静态分析不包含）
  min_score_to_warn: 3.0         # 低于此分数显示警告

output:
  format: "markdown"    # 输出格式：markdown, json, text
  save_report: true     # 保存详细报告
  report_dir: "./reports" # 报告保存目录
```

环境变量：
```bash
export SKILL_ASSESS_WEIGHTS='{"documentation":0.3,"code_quality":0.4}'
export SKILL_ASSESS_OUTPUT_FORMAT=json
```

## 文件结构
```
skill-assessment/
├── SKILL.md                    # 本文档
├── assess.sh                   # 主评估脚本
├── config.yaml                 # 默认配置
├── evaluators/                 # 评估模块
│   ├── doc_checker.sh          # 文档检查
│   ├── code_analyzer.sh        # 代码分析
│   ├── config_validator.sh     # 配置验证
│   └── maintenance_checker.sh  # 维护状态检查
├── templates/                  # 报告模板
│   ├── report.md.j2            # Markdown报告模板
│   └── summary.txt.j2          # 控制台摘要模板
├── examples/                   # 示例
│   ├── sample_report.md        # 示例报告
│   └── config.example.yaml     # 配置示例
└── reports/                    # 生成的报告存储
    └── skill-creator_2026-03-12.md
```

## 故障排除

### 常见问题
1. **评估时间过长**
   - 原因：技能文件过多或包含大文件
   - 解决：使用 `--exclude` 排除非必要文件，或设置文件大小限制

2. **误报安全问题**
   - 原因：检查规则过于严格
   - 解决：调整 `config.yaml` 中的安全检查敏感度，或添加例外规则

3. **缺少依赖工具**
   - 原因：未安装 jq、yq 等工具
   - 解决：`brew install jq yq` 或使用包管理器安装

4. **权限问题**
   - 原因：无法读取技能目录
   - 解决：检查目录权限，或使用 `sudo`（不推荐）

### 调试模式
```bash
# 启用详细日志
skill-assess ~/.openclaw/skills/skill-creator --verbose

# 查看检查过程
skill-assess ~/.openclaw/skills/skill-creator --debug
```

## 开发指南

### 添加新的检查规则
1. 在 `evaluators/` 目录下创建新的检查脚本
2. 脚本应输出 JSON 格式的结果：
   ```json
   {
     "score": 4.5,
     "max_score": 5,
     "issues": ["问题描述1", "问题描述2"],
     "suggestions": ["改进建议1", "改进建议2"]
   }
   ```
3. 在 `assess.sh` 中注册新的检查器
4. 更新 `config.yaml` 中的权重配置

### 扩展评估维度
如需添加新的评估维度（如“性能表现”），需要：
1. 动态测试支持（选项2或3）
2. 在沙箱中运行技能测试用例
3. 测量执行时间和资源消耗

## 版本历史
- **v1.0.0** (2026-03-12): 初始版本，静态分析四维度评估
- **v1.1.0** (规划中): 添加技能对比功能，集成到 ClawHub
- **v1.2.0** (规划中): 支持动态基础测试（选项2）

## 相关技能
- **skill-creator**: 技能创建辅助工具
- **skill-audit**: 技能安全审计工具  
- **find-skills**: 技能发现和搜索工具

## 贡献
欢迎提交 Issue 和 Pull Request：
1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License