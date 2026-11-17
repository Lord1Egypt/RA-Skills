# 架构设计

> 本文件描述 skill-standardization v2 的整体架构、模块关系和数据流。
> 适合需要深入理解内部实现或进行二次开发的读者。

---

## 系统概览

skill-standardization 是一个 **Skill 标准化规范引擎**，围绕「门禁 → 审计 → 二次筛 → 修复→ 一致性审查 → bump」的闭环构建。

6 种入口模式全部通过 `_semantic_precheck` 门禁校验：

```
用户请求 → ★ 自检闸门 → 【模式=xxx】 → --mode xxx + 子命令 → 门禁校验通过 → 执行
                                                                  ↓不匹配
                                                            exit(1) 拒绝
```

---

## 目录结构

```
skill-standardization/                 # Skill 根目录
│
├── SKILL.md                           # 主文件（≤230行渐进式入口）
├── _meta.json                         # 元数据（七字段）
│
├── references/                        # 渐进式 MD 辅助文档
│   ├── guide.md                       # 使用指南（详细教程）
│   ├── examples.md                    # 示例集合
│   ├── reference.md                   # 命令参考手册
│   ├── faq.md                         # 常见问题
│   ├── changelog.md                   # 版本更新日志
│   ├── antipatterns.md               # 反模式指南
│   ├── permissions.md                # 权限说明
│   ├── architecture.md                # 本文件 — 架构设计
│   ├── rules.md                       # R-01~R-26 规则定义
│   ├── blueprint_flow.md             # 蓝皮书 & 审计流程
│   ├── data_dir_map.md               # 数据目录路径对照
│   └── LICENSE.md                     # MIT 许可证
│
└── scripts/
    ├── __init__.py
    ├── permission_checker.py          # 权限扫描
    ├── safe_io.py                     # 原子写入
    ├── skill_inspector.py             # 蓝皮书扫描
    ├── skill_rollback.py              # 回滚工具
    ├── cleanup_manager.py             # 清理管理
    │
    └── skill_audit/                   # 审计引擎包
        ├── __init__.py                # 主入口 + cmd_xxx() + audit_skill()
        ├── consistency_checker.py     # 一致性审查
        ├── structure_checker.py       # R-06~R-26 检查函数
        ├── fix.py                     # 自动修复函数（35+ fix key，含新增的 code_block_markers/list_mixing/code_block_lang/section_completeness/error_handling_faq）
        ├── artifact_checker.py        # R-12 数据目录合规 + 产物物路径检查（v2.101.8: 支持 pathlib 推导式放行）
        ├── _path_detector.py          # 共享路径文件检测（v2.101.8: 优先改选 _paths.py）
        └── spec/
            └── body.json              # 正文章节结构规范（三层体系 + content_format）
```

---

## 模块关系

```
                    ┌─────────────────────────┐
                    │  _semantic_precheck()    │ ← 门禁
                    │  (模式-命令映射锁)        │
                    └──────────┬──────────────┘
                               │ 6 种入口模式
          ┌────────┬───────────┼───────────┬────────┬────────┐
          ▼        ▼           ▼           ▼        ▼        ▼
      readonly  audit      create      update   refactor   bump
          │        │           │           │        │        │
          ▼        ▼           ▼           ▼        ▼        ▼
      ┌──────────────────────────────────────────────────────┐
      │                  audit_skill()                       │
      │    R-01~R-26 全量/针对性审计                          │
      │    → _filter_false_positives() (读取 --classify)     │
      │    → _path_detector (共享路径文件检测)                 │
      └──────────────────────────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                     ▼
    _run_audit_loop()   一致性审查              cmd_bump()
    ┌──────────────┐    check_consistency()    版本号三端同步
    │① audit       │    → reclassify_consistency
    │② 二次筛阻断点 │      _false_positive()
    │③ auto-fix    │    → apply_consistency_fix()
    │  (35+ fix key)│
    │④ LLM manual  │
    │  (含BLOCKED   │
    │   指引输出)   │
    │⑤ re-audit    │
    └──────────────┘
```

---

## 核心流程

### refactor（10 步）
```
[1]  蓝皮书扫描
[2]  cleanup session + 备份
[3]  全量审计 → audit_skill()
[4]  _run_audit_loop()
       ├─ ★ 前置 LLM 二次筛阻断点（检查 --classify）
       ├─ auto-fix（按 fix key 粒度过滤 _llm_only_fix_keys 后修复）
       └─ LLM manual 指引（含 BLOCKED fix 的 3 步操作指引输出）
[5]  LLM 剩余项检查（读取 .remaining_llm.json）
[6]  全量审计确认（双0）
[7]  全量一致性审查（含自有二次筛）
[8]  --subtype 二次精筛（必须从枚举表匹配）
[9]  bump（feature → MINOR）
[10] cleanup 清理 + 展示报告
```

### update（9 步）
```
[1] 蓝皮书扫描
[2] cleanup session + 备份
[3] 变更声明（校验 changed-files）
[4] 针对性审计 → _run_audit_loop()
[5] LLM 剩余项检查
[6] 全量审计确认（双0）
[7] 针对性一致性审查
[8] bump（fix → PATCH）
[9] cleanup 清理
```

### create（3 步）
```
[1] 生成骨架（SKILL.md + _meta.json + 6 个 references/ 文件）
[2] 全量审计
[3] 创建总结
```

---

## 关键设计决策

### 1. 模式-命令映射锁（v2.90.0）
LLM 在自检闸门输出 `【模式=xxx】` 后，执行 CLI 时必须传 `--mode xxx`。
代码对比 `--mode` 值与当前子命令是否一致，不一致则 `exit(1)`。

### 2. 前置 LLM 二次筛阻断点（v2.90.0）
`_run_audit_loop()` 首次进入时检查 `--classify` 文件（`.verify_fp.json`），
无数据则阻断输出 3 步指引，`--continue` 跳过。

### 3. 误报分类与修复路径分离
- **误报（是否修）**：LLM 通过 `--classify` 标记，写入 `.verify_fp.json`
- **auto-fix / LLM manual（怎么修）**：三路判断 — fix key 不在 _llm_only_fix_keys 中的 auto-fix；fix key 在 _llm_only_fix_keys 中或无 fix key 的 LLM 手动

两条轴线独立运行，互不干扰。

### 4. 一致性审查自有二次筛（v2.91.0）
一致性审查使用与审计共享的 `.verify_fp.json` 文件，ID 格式 `C-{type}`。
所有硬编码误判规则已删除，统一走 LLM `--classify` 路径。

---

## 规范定义体系

R-01~R-26 规则定义在 `scripts/skill_audit/spec/rules.json`，由 `structure_checker.py` 逐条实现。

| 规则范围 | 规则ID | 说明 |
|----------|--------|------|
| Frontmatter | R-01~R-04 | 字段完整性、命名、版本、描述 |
| 正文结构 | R-06~R-09 | H1、触发条件、章节、工作流 |
| 版本 | R-10 | 版本三端一致性 |
| 路径安全 | R-11~R-12 | 产出物路径、数据目录规范 |
| 权限安全 | R-13~R-16 | 敏感访问、写入、permissions.md |
| 渐进加载 | R-17 | 文件行数 ≤ 230 + 非标章节迁移 |
| 内容质量 | R-18~R-19 | 反模式、FAQ |
| 写作规范 | R-20 | 术语一致/无模糊表述/中英文空格 |
| 渐进引用 | R-21 | 固定模板句 |
| 数据目录 | R-22 | 安装目录无越位数据文件 |
| 一致性 | R-23 | 文档-代码一致性 |
| 更新日志 | R-24 | 渐进式 changelog |
| 文档格式 | R-25 | C-01~C-19 写作格式规范（含 C-05/C-07/C-12/C-14/C-17/C-18/C-19） |
| 许可声明 | R-26 | LICENSE + README 规范 |

---

## 数据流

```
                    ┌──────────────┐
                    │  .verify_fp.json │ ← LLM 通过 --classify 写入
                    │  (共享误判标记)  │
                    └──────┬───────┘
                           │ 被 audit 和一致性审查同时读取
              ┌────────────┼────────────┐
              ▼            ▼            ▼
      audit_skill()   一致性审查      _run_audit_loop()
      _reclassify_    reclassify_    _filter_false_
      false_positive  consistency_   positives()
                      false_positive
```
