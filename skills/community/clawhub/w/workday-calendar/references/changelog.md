## 2.2.0 (2026-06-22)

### Added
- B 层排班时段规则系统（WorkSlot 15 分钟粒度）
- 岗位（position）+ 多人多岗多赋值（WorkSlot.assignments）
- 排班时段条（tl-bar，工作日蓝灰交替/周末全灰/假日隐藏）
- 弹出框排班时段表 + 个人日程按 B 层时段染色
- 排班表导出（export_schedule_table，周/月/日期范围，按周或月分组）
- 日程自动状态流转（pending → missed/completed，配置开关）
- 平台无关的自动化定时配置（auto add/check CLI）
- 补班日弹出框按工作日时段展示

### Changed
- 周末色统一为绿色（法定假休），不再与轮休双色区分
- 日类型简化为：绿=休息（法定/双休/轮休/公休/临修）、红=补班、白=工作
- get_day_type() 逻辑重构：排班规则只定义上班，不上班=休息
- config.json 缺字段自动补默认值（不再因旧文件无 key 而失效）

### Fixed
- load_config() 新增字段自动合并默认值
- auto_update_event_statuses() 支持 missed→completed 重评
- get_slot_color_for_time() 按 weekday+time 正确映射时段颜色
- weekend_config 映射 bug（config 0=周日→Python 6=周日）
- 弹出框日程染色正确（午休灰、上午班蓝、下午班蓝）

## 2.1.0 (2026-06-22)

### Added
- 基础周 HTML 导出与配置中心（settings.py）
- 岗位+人员多赋值支持（WorkSlot.assignments）
- 排班表导出（周/月/日期范围）
- 定时任务自动化配置（auto CLI）
- 过期日程自动打标（missed/completed 配置切换）
- 排班时段条（tl-bar 可视化）
- 配置中心 Web 界面

### Fixed
- `update_schedule_event()` 增加冲突检测
- `export_rules_table()` 修复硬编码 52 周
- 节假日落在周末重复扣除 Bug
- 周末规则转换 Bug（config_weekends_to_python）
- `scheduling_rules.json` 清空后默认回退

### Changed
- WorkSlot 重构：assignments 列表替代单 position/persons
- 加载配置使用默认值合并（兼容旧 config.json）

## 1.6.5 (2026-05-31)

### 修复
- **data_dir 格式修正**: frontmatter 的 data_dir 恢复为 ../ 相对路径格式（此前错误同步为 skills/ 格式）

---
## 1.6.4 (2026-05-31)

### 修复
- audit --fix 自动修正: meta_field_sync

---

## 1.6.3 (2026-05-31)

### 修复
- **H1 位置修复**: 将 H1 从第 38 行移至 frontmatter 后首行（原距 frontmatter 闭合后有 22 行空白）

---
## 1.6.2 (2026-05-31)

### 修复
- **R-04**: description 删除版本号
- **R-10**: changelog 版本号去 v 前缀

---

## 1.6.1 (2026-05-30)

### 修复
- audit --fix 自动修正

---


## 1.6.0（2026-05-30）

### 修复
- R-12 数据目录路径合规修复（`scripts/workday_calendar.py` 新增 `DEFAULT_DATA_DIR_RAW` 审计锚点 + `_data_dir_abs` 运行时路径）
- `_meta.json` 补充 `data_dir` 字段（与 SKILL.md frontmatter 保持一致）
- `get_skill_data_dir()` 改用 `_data_dir_abs` 静态路径替代动态目录遍历

### 更新
- SKILL.md frontmatter 版本号升至 v1.6.0，描述更新
- `_meta.json` 版本号和描述同步更新
- `references/changelog.md` 补写 v1.6.0 改动记录

---

## 1.5.0（2026-05-27）

### 修复
- 经 skill-standardization 改造，文件结构规范化（scripts/、references/ 归位）
- R-11 产出物路径合规性修复（删除根目录违规文件）
- R-12 数据目录路径统一（data_dir: ../.standardization/workday-calendar/data/）
- SKILL.md frontmatter 补充 trigger/trigger_negative 字段

### 更新
- SKILL.md frontmatter 版本号升至 v1.5.0
- _meta.json 版本号和描述更新
- references/changelog.md 补写 v1.4.0 遗漏的实际改动

---

## 1.4.0（2026-05-27）

### 修复
- 经 skill-standardization 改造，文件结构规范化（scripts/、references/ 归位）
- R-11 产出物路径合规性修复（删除根目录违规文件）
- R-12 数据目录路径统一（data_dir: ../.standardization/workday-calendar/data/）

### 更新
- SKILL.md frontmatter 版本号升至 v1.4.0
- _meta.json 版本号和描述更新

---

## 1.3.0（2026-05-27）

### 新增
- 国家法定假日区间管理
- 年度工作日计算
- 周历生成
- 日程管理

---
