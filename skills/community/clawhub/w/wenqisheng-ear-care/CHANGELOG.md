# Changelog

## v1.0.0 (2026-05-13)

### 架构升级
- **数据与逻辑分离**：SKILL.md 不再包含任何硬编码业务数据，所有价格、地址、时间等数据集中在 references/ 目录管理
- 新增 `version.json` 数据版本追踪
- 新增 GitHub Actions 自动打包发布
- 新增客户侧自动更新脚本 `scripts/auto_update.sh`

### 修复
- 修复所有脚本中的硬编码绝对路径，改为相对路径
- test_skill.py 移除对桌面 DOCX 文件的依赖
- deep_audit.py 移除 Unicode 转义序列，提高可读性
- 电话号码统一在 business-info.md 中管理
- .gitignore 排除 dist/*.skill 二进制文件

### 门店运营者更新指南
1. 编辑 `references/` 目录下的对应文件
2. 运行 `python scripts/test_skill.py` 验证
3. git commit & git push
4. 客户自动同步

### 初始数据
- 深度可视采耳 58元/25分钟
- 采耳+洗耳 98元/40分钟
- 炎症采耳+洗耳+养护 128元/60分钟
- 砭石草本眼护 58元/30分钟
- 充值优惠：充300送100 / 充500送200 / 充1000送500（截至2026年5月30日）
