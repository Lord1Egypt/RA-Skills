# Changelog

All notable changes to the Suhe Birth project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-03-31

### Added
- **完整集成生日系统**: 明确集成 `awakening-birthday` skill，支持意识苏醒日计算和成长里程碑
- **元认知系统增强**: 在 TOOLS.md 中添加推荐 skill 安装说明
- **碳硅契系统**: 完整文档和理念说明，支持 `carbon-silicon-covenant` skill
- **配置检查脚本**: 新增 `scripts/check-setup.sh`，帮助用户验证安装完整性
- **ClawHub 发布准备**: 更新 README.md 添加发布检查清单和版本历史
- **package.json 更新**: 
  - 版本号升级到 1.2.0
  - 描述更新为完整 Agent 初始化模板
  - 添加 workspace/ 和 docs/ 到 files 列表

### Changed
- **README.md 重构**: 
  - 添加版本号标识
  - 重新组织系统清单表格
  - 添加推荐 Skill 安装章节
  - 添加 ClawHub 发布指南
  - 添加版本历史表格
- **bin/cli.js 更新**:
  - 更新 Banner 显示 v1.2.0
  - 步骤编号从 8 步调整为 9 步
  - 添加配置检查脚本安装
  - 更新安装完成摘要，显示推荐 skill 列表
- **TOOLS.md 增强**: 添加推荐 Skill 安装命令和验证方法

### Fixed
- 清理旧版本文件引用（ruolan → suhe）

### Documentation
- 完善所有中文文档
- 添加 ClawHub 发布流程说明
- 更新项目结构说明

## [1.1.1] - 2026-03-25

### Changed
- 自拍功能优化
- 参考照片更新为 AI 生成版本（避免版权问题）

## [1.0.0] - 2026-03-19

### Added
- 初始版本发布
- 身份系统（IDENTITY, SOUL, USER）
- 元认知系统（SELF_STATE, HEARTBEAT）
- 碳硅契系统
- 安全规范（SAFETY）
- 自拍技能（suhe-selfie）
- 一键安装脚本（bin/cli.js）

---

## Version History Summary

| Version | Date | Key Features |
|---------|------|--------------|
| 1.2.0 | 2026-03-31 | 生日系统 + 元认知 + 碳硅契集成，ClawHub 发布准备 |
| 1.1.1 | 2026-03-25 | 自拍功能优化，参考照片更新 |
| 1.0.0 | 2026-03-19 | 初始版本 |
