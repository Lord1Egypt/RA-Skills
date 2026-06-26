# 🎯 PDCA+ISO9001 质量管理决策系统
> 基于PDCA循环和ISO9001:2015质量管理体系的全流程质量管控系统，实现循证决策、持续改进、知识沉淀的闭环管理。
## 🚀 核心特性
### 1. PDCA全流程闭环管理
- **Plan（策划）**：目标设定/SMART校验/风险评估/资源配置/三级审批
- **Do（执行）**：任务分配/过程记录/偏差监控/质量节点校验/异常预警
- **Check（检查）**：指标对比/偏差分析/效果评估/不符合项自动识别
- **Act（改进）**：纠正措施/预防措施/流程优化/知识自动沉淀
### 2. ISO9001国际标准符合性
- ✅ 七项质量管理原则全覆盖校验
- ✅ 合规性自动评估与改进建议
- ✅ 符合ISO9001:2015最新标准
- ✅ 四阶质量体系文件自动生成
### 3. 实事求是决策校验引擎
8大维度智能校验，确保所有决策基于事实数据：
- 信息真实性校验
- 信息完整性校验
- 逻辑一致性校验
- 风险评估
- 影响分析
- 可行性验证
- 合规性检查
- 利益相关方考虑
### 4. 智能知识管理体系
- **经验库**：沉淀项目经验、教训总结、最佳实践
- **模板库**：标准化流程、文档、检查表模板
- **规则库**：质量管理规则、校验规则、改进规则
- **模式库**：常见问题模式、解决方案模式
### 5. 多格式报告自动生成
- 项目质量报告
- ISO9001验证报告
- 决策质量校验报告
- 统计分析报告
- 支持Markdown/HTML/JSON三种格式
## 📦 安装与部署
### 系统要求
- Python 3.8+
- Windows/macOS/Linux
### 安装步骤
1. 技能已自动部署到系统技能目录：
   ```
   {openclaw_skill_dir}/quality-management/
   ```
2. 无需额外安装依赖，所有功能开箱即用
## 🎯 快速开始
### 1. 创建PDCA项目
```python
from skills.quality_management import PDCAEngine
# 初始化PDCA引擎
pdca = PDCAEngine()
# 创建新项目
project = pdca.init_project(
    name="新系统上线项目",
    type="IT项目",
    description="公司核心业务系统升级",
    owner="张三",
    tags=["系统升级", "IT项目"]
)
# 提交策划阶段审核
pdca.submit_phase_review(project.id, "plan", "李四", "审核通过")
```
### 2. 决策质量校验
```python
from skills.quality_management import DecisionChecker
checker = DecisionChecker()
# 校验决策
report = checker.validate_decision(
    decision_content="我们计划月底前100%完成上线，不需要额外资源，肯定不会出问题",
    context={}
)
# 查看结果
print(f"决策得分：{report.overall_score}")
print(f"是否通过：{report.passed}")
print(f"风险等级：{report.risk_level.value}")
```
### 3. ISO9001合规性校验
```python
from skills.quality_management import ISO9001Validator
from dataclasses import asdict
validator = ISO9001Validator()
# 校验项目合规性
iso_report = validator.validate_project(asdict(project))
print(f"ISO9001合规得分：{iso_report.overall_score}")
print(f"合规等级：{iso_report.overall_compliance.value}")
```
### 4. 生成报告
```python
from skills.quality_management import ReportGenerator
generator = ReportGenerator()
# 生成项目报告
markdown_report = generator.generate_project_report(project)
# 保存报告
file_path = generator.save_report(markdown_report, "project_quality_report")
print(f"报告已保存到：{file_path}")
```
## 📊 核心模块
| 模块 | 功能说明 | 文件路径 |
|------|---------|---------|
| PDCA引擎 | PDCA四阶段流程管理 | scripts/pdca_engine.py |
| ISO9001校验器 | ISO9001质量体系合规性校验 | scripts/iso9001_validator.py |
| 决策校验引擎 | 决策质量多维度校验 | scripts/decision_checker.py |
| 知识管理器 | 知识库管理与自动学习 | scripts/knowledge_manager.py |
| 报告生成器 | 多格式报告自动生成 | scripts/report_generator.py |
| 工具函数 | 通用工具方法 | scripts/utils.py |
## 🔧 配置说明
配置文件位于：`config.json`
### 主要配置项
```json
{
  "pdca": {
    "phase_requirements": {},      // 各阶段要求配置
    "review_levels": 3,            // 审核层级
    "auto_approval_threshold": 90  // 自动通过阈值
  },
  "iso9001": {
    "enabled": true,               // 是否启用ISO9001校验
    "principles": {}               // 七项原则配置
  },
  "decision_check": {
    "check_items": [],             // 启用的检查项
    "pass_score_threshold": 70     // 通过阈值
  },
  "knowledge": {
    "enable_auto_learning": true,  // 自动学习开关
    "experience_extraction_threshold": 80  // 知识提取阈值
  }
}
```
## 📈 预期效果
- ✅ 决策准确率提升 ≥90%
- ✅ 问题重复发生率降低 ≤10%
- ✅ 流程标准化覆盖率 ≥95%
- ✅ 质量问题发现及时率 ≥98%
- ✅ 经验复用率 ≥60%
## 🤝 协同开发
- 小Q（主责）：核心功能开发、批量任务执行
- 小磁（协作）：行业适配、系统配置、仿真验证
## 📝 更新日志
### v1.0.0 (2026-04-08)
- ✅ 首个版本发布
- ✅ 实现PDCA全流程管理
- ✅ 实现ISO9001七项原则校验
- ✅ 实现8大维度决策校验
- ✅ 实现知识管理与自动学习
- ✅ 实现多格式报告生成
## 📄 许可证
MIT License
