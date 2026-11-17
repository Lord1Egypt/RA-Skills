## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-standardization |
| 测试时间 | 2026-06-18 17:45 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 9 | 9 | 0 | 100% |
| D1-D6 功能测试 | 409 | 328 | 0 | 80% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景「audit 审计请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「refactor 改造请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「create 创建请求」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「全量审计执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「自动修复执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「版本号三端同步」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 2 个 CLI 命令 |
| S3 | INFO | 工作流「classify 误报标记后 continue」 | PASS | 由外部编排实现，无直接 CLI |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\cleanup_manager. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\permission_check | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\safe_io.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_inspector. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_rollback.p | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\__init__.py | FAIL | 0:文件内容为空 | scripts\__init__.py |
| D1 | INFO | 语法检查: scripts\skill_audit\arti | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\cons | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\data | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fix. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fron | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\perm | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\prog | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\stru | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\util | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\skill_audit\utils | FAIL | 0:文件内容为空 | scripts\skill_audit\utils_restored.py |
| D1 | INFO | 语法检查: scripts\skill_audit\_tre | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__in | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__ma | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\cr | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\mi | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\re | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\up | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ut | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ve | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\cleanup_manager.p | PASS | :0 | exit code 0, stdout 84 chars |
| D1 | INFO | 运行时: scripts\permission_checke | PASS | :0 | exit code 0, stdout 447 chars |
| D1 | INFO | 运行时: scripts\safe_io.py --help | PASS | :0 | exit code 0, stdout 343 chars |
| D1 | WARN | 启动失败: scripts\skill_inspector. | FAIL | scripts\skill_inspector.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\skill_rollback.py | PASS | :0 | exit code 0, stdout 0 chars |
| D1 | WARN | 启动失败: scripts\skill_audit\data | FAIL | scripts\skill_audit\data_dir_checker.py:0 | exit code 1: ddy\skills\skill-standardization\scri |
| D1 | WARN | 启动失败: scripts\skill_audit\__in | FAIL | scripts\skill_audit\__init__.py:0 | exit code 1: \Users\sm001\.workbuddy\skills\skill- |
| D1 | WARN | 启动失败: scripts\skill_audit\__ma | FAIL | scripts\skill_audit\__main__.py:0 | exit code 1: "C:\Users\sm001\.workbuddy\skills\ski |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__init__.py:0 | exit code 1: orkbuddy\skills\skill-standardization |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__main__.py:0 | exit code 1: :\Users\sm001\.workbuddy\skills\skill |
| D2 | WARN | 引用文件不存在 | FAIL | reference.md:0 | reference.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | INFO | 外部依赖: uuid | PASS | :0 | scripts\cleanup_manager.py → uuid |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\permission_checker.py → ast |
| D2 | INFO | 外部依赖: tokenize | PASS | :0 | scripts\permission_checker.py → tokenize |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\permission_checker.py → argparse |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\safe_io.py → io |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\safe_io.py → time |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\safe_io.py → argparse |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_inspector.py → ast |
| D2 | INFO | 外部依赖: logging | PASS | :0 | scripts\skill_rollback.py → logging |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\skill_rollback.py → glob |
| D2 | INFO | 外部依赖: difflib | PASS | :0 | scripts\skill_rollback.py → difflib |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._H |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._P |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._e |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._f |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils.pa |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\data_dir_checker.py → utils._i |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\fix.py → io |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\fix.py → traceback |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils._fmt_frontmatte |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils.parse_simple_ya |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.fix_ |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\fix.py → importlib |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\fix.py → permission_checker.Pe |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\fix.py → data_dir_checker.fix_ |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\fix.py → ast |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.chec |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\permission_checks.py → permiss |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\structure_checker.py → warning |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.T |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: py_compile | PASS | :0 | scripts\skill_audit\structure_checker.py → py_comp |
| D2 | INFO | 外部依赖: _tree_scanner | PASS | :0 | scripts\skill_audit\structure_checker.py → _tree_s |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\__init__.py → importlib.util |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_audit\__init__.py → argparse |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._fmt_front |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.RULES |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.TRIGGER_KE |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.CORE_KEYWO |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.WORKFLOW_K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.ARTIFACT_D |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._KNOWN_STA |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._HARDCODED |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._PATH_EXCL |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._is_hardco |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.parse_simp |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._find_skil |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.apply_fix |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.list_fixable |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\__init__.py → io |
| D2 | INFO | 外部依赖: skill_builder | PASS | :0 | scripts\skill_audit\__init__.py → skill_builder.ve |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_bu |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.fix_progress |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_audit\__main__.py → main |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.aud |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.for |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.pro |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\refactor.py → zipfile |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.fo |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\refactor.py → skill_inspecto |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._create_b |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ar |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ex |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._write_js |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\updater.py → skill_inspector |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\updater.py → version_manager |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\utils.py → zipfile |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_builder\__init__.py → argparse |
| D2 | INFO | 外部依赖: creator | PASS | :0 | scripts\skill_builder\__init__.py → creator.SkillC |
| D2 | INFO | 外部依赖: updater | PASS | :0 | scripts\skill_builder\__init__.py → updater.SkillU |
| D2 | INFO | 外部依赖: refactor | PASS | :0 | scripts\skill_builder\__init__.py → refactor.Refac |
| D2 | INFO | 外部依赖: migrator | PASS | :0 | scripts\skill_builder\__init__.py → migrator.Skill |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\__init__.py → version_manage |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\__init__.py → utils.* |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\__init__.py → skill_inspecto |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_builder\__main__.py → main |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\cleanup_manager.py:316 | 12 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\skill_audit\utils.py:331 | ".yml":     "data",   ".db":    "data",   ".sqlite |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\cleanup_manager.py:348 | print("用法: python cleanup_manager.py <skill_dir> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\permission_checker.py:952 | print(json.dumps(report, indent=2, ensure_ascii=Fa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:367 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:373 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:379 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:381 | print("Usage: python -m scripts.skill_inspector <s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:382 | print("只读操作，输出 skill 蓝皮书：结构、AST函数签名、引用链路") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:383 | print("用于 update/refactor 前的全貌扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:394 | print(result) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:126 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:191 | print("\n".join(diff)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:203 | print("用法: python skill_rollback.py rollback <roll |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:214 | print("用法: python skill_rollback.py show <rollback |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:789 | print("    [OK] 更新 _meta.json: data_dir = " + expe |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:824 | print("    [OK] 更新 " + fname + ": " + var_name + " |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:200 | print("用法: python data_dir_checker.py <skill_dir>  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:206 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:207 | print("  R-22 数据目录规范检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:208 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:213 | print(issue) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:216 | print("\n─── 自动修复 ──────────────────────────────── |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:931 | print("  skill-standardization 创建模板（供 LLM 参考）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:948 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:953 | print("用法：") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:954 | print("  python -m skill_audit create-template") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:955 | print("  python -m skill_audit create-template --j |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:956 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:964 | print("-" * 65) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1171 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1176 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1185 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1476 | print(json.dumps({ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1491 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1494 | print("  详细逐项结果:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1499 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1514 | print("可用修复 key（对应审计规则 R-01~R-26）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1517 | print("\n用法: python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1518 | print("      python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1753 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1881 | print("  步骤 2: 对确认为误报的一致性项执行 --classify（ID 格式 C-类型 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2470 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2518 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2894 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\creator.py:731 | print("[!] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:58 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:60 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:61 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:63 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:313 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:418 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:458 | print("[!] SKILL.md 不存在，无法升级版本号") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:465 | print("[!] SKILL.md frontmatter 中未找到 version 字段") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:217 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:226 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:238 | print("[!] permission_checker.py 不存在，跳过授权检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:281 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:346 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:348 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:349 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:351 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:438 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\__init__.py:130 | print(result) |
| D5 | INFO | 发现 48 个验证函数 | PASS | :0 | _check_sensitive_access, _check_critical_write, _c |
| D5 | INFO | 发现 3 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\cleanup_manager | PASS | :0 |  |
| D5 | INFO | 函数可运行: end_session() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 模块可加载: scripts\permission_chec | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\skill_rollback | PASS | :0 |  |
| D5 | INFO | 函数可运行: load_manifest() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: list_backups() | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 模块导入失败: scripts\skill_audit\fi | FAIL | scripts\skill_audit\fix.py:0 | 缺少依赖: attempted relative import with no known pare |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:46 | _resolve_manifest_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:120 | register() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:205 | finalize() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:323 | list_active_manifests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:205 | _get_ast_string_ranges() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:241 | _scan_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:273 | _check_sensitive_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:374 | _is_sensitive_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:441 | _is_regex_pattern() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:513 | _check_critical_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:569 | _check_network_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:594 | _check_file_delete() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:619 | _check_subprocess_call() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:723 | _determine_risk_level() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:744 | _generate_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:769 | _get_recommendation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:45 | safe_read() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:144 | _record_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:25 | inspect_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:257 | _format_text_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:94 | save_manifest() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:129 | rollback() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:166 | show_diff() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:21 | check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:93 | _check_root_artifact_files() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:151 | _check_artifact_directories() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:196 | _scan_dir_recursive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:215 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:249 | _scan_unknown_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:443 | _trace_cross_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:530 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:859 | _check_body_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:173 | _check_argparse_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:227 | _check_data_dir_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:294 | format_consistency_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:348 | apply_consistency_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:49 | _is_fix_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:56 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:186 | log_check_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:29 | _read_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:35 | _write_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:739 | fix_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:786 | fix_create_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1496 | fix_missing_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1728 | fix_section_constraint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2325 | _write_struct() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2336 | _struct_file_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2343 | _render_workflow_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2378 | _render_examples_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2409 | _render_capabilities_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:3254 | fix_license_compliance() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1696 | _norm_rel() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\frontmatter_checker.py:338 | _norm_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\permission_checks.py:157 | check_authorization_present() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:50 | create_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:94 | update_progress_from_audit() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:213 | finalize_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:283 | load_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:316 | format_progress_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:338 | body_has_antipattern_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:420 | body_has_faq_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:505 | _extract_qa_pairs() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:851 | check_doc_code_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:1251 | check_changelog_progressive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:412 | _is_hardcoded_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:493 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:523 | _classify_artifact_by_ext() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:532 | _extract_path_literal() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:541 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:442 | _reclassify_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:462 | _filter_false_positives() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:500 | format_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:626 | _save_html_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:643 | _save_remaining_llm() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:971 | _do_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1439 | cmd_audit_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1548 | _load_fp_ids() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:2234 | _run_audit_loop() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:114 | create() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:208 | _generate_guide_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:333 | _generate_permissions_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:385 | _generate_examples_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:696 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:720 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:814 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:827 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:831 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:20 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:23 | migrate() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:62 | _detect_current_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:124 | _compute_target_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:130 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:162 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:259 | _update_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:284 | _scan_hardcoded_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:543 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:24 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:27 | refactor() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:131 | _build_migration_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:196 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:302 | _write_permission_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:396 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:450 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:507 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:32 | _check_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:67 | _check_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:100 | _check_dir_structure() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:111 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:259 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:427 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:498 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:511 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:515 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:29 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:54 | _write_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:61 | _check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:86 | _check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:92 | request_changelog() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:124 | append_changelog() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\fix.py:0 | scripts\skill_audit\fix.py: 17 个 except / 3430 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\progress_manager.py:0 | scripts\skill_audit\progress_manager.py: 0 个 excep |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\utils.py:0 | scripts\skill_audit\utils.py: 2 个 except / 605 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\creator.py:0 | scripts\skill_builder\creator.py: 1 个 except / 839 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\__init__.py:0 | scripts\skill_builder\__init__.py: 0 个 except / 13 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-standardization |
| 测试时间 | 2026-06-18 17:47 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 关闭 |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 9 | 9 | 0 | 100% |
| D1-D6 功能测试 | 409 | 328 | 0 | 80% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景「audit 审计请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「refactor 改造请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「create 创建请求」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「全量审计执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「自动修复执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「版本号三端同步」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 2 个 CLI 命令 |
| S3 | INFO | 工作流「classify 误报标记后 continue」 | PASS | 由外部编排实现，无直接 CLI |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\cleanup_manager. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\permission_check | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\safe_io.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_inspector. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_rollback.p | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\__init__.py | FAIL | 0:文件内容为空 | scripts\__init__.py |
| D1 | INFO | 语法检查: scripts\skill_audit\arti | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\cons | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\data | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fix. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fron | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\perm | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\prog | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\stru | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\util | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\skill_audit\utils | FAIL | 0:文件内容为空 | scripts\skill_audit\utils_restored.py |
| D1 | INFO | 语法检查: scripts\skill_audit\_tre | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__in | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__ma | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\cr | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\mi | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\re | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\up | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ut | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ve | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\cleanup_manager.p | PASS | :0 | exit code 0, stdout 84 chars |
| D1 | INFO | 运行时: scripts\permission_checke | PASS | :0 | exit code 0, stdout 447 chars |
| D1 | INFO | 运行时: scripts\safe_io.py --help | PASS | :0 | exit code 0, stdout 343 chars |
| D1 | WARN | 启动失败: scripts\skill_inspector. | FAIL | scripts\skill_inspector.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\skill_rollback.py | PASS | :0 | exit code 0, stdout 0 chars |
| D1 | WARN | 启动失败: scripts\skill_audit\data | FAIL | scripts\skill_audit\data_dir_checker.py:0 | exit code 1: ddy\skills\skill-standardization\scri |
| D1 | WARN | 启动失败: scripts\skill_audit\__in | FAIL | scripts\skill_audit\__init__.py:0 | exit code 1: \Users\sm001\.workbuddy\skills\skill- |
| D1 | WARN | 启动失败: scripts\skill_audit\__ma | FAIL | scripts\skill_audit\__main__.py:0 | exit code 1: "C:\Users\sm001\.workbuddy\skills\ski |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__init__.py:0 | exit code 1: orkbuddy\skills\skill-standardization |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__main__.py:0 | exit code 1: :\Users\sm001\.workbuddy\skills\skill |
| D2 | WARN | 引用文件不存在 | FAIL | reference.md:0 | reference.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | INFO | 外部依赖: uuid | PASS | :0 | scripts\cleanup_manager.py → uuid |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\permission_checker.py → ast |
| D2 | INFO | 外部依赖: tokenize | PASS | :0 | scripts\permission_checker.py → tokenize |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\permission_checker.py → argparse |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\safe_io.py → io |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\safe_io.py → time |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\safe_io.py → argparse |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_inspector.py → ast |
| D2 | INFO | 外部依赖: logging | PASS | :0 | scripts\skill_rollback.py → logging |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\skill_rollback.py → glob |
| D2 | INFO | 外部依赖: difflib | PASS | :0 | scripts\skill_rollback.py → difflib |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._H |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._P |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._e |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._f |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils.pa |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\data_dir_checker.py → utils._i |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\fix.py → io |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\fix.py → traceback |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils._fmt_frontmatte |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils.parse_simple_ya |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.fix_ |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\fix.py → importlib |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\fix.py → permission_checker.Pe |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\fix.py → data_dir_checker.fix_ |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\fix.py → ast |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.chec |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\permission_checks.py → permiss |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\structure_checker.py → warning |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.T |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: py_compile | PASS | :0 | scripts\skill_audit\structure_checker.py → py_comp |
| D2 | INFO | 外部依赖: _tree_scanner | PASS | :0 | scripts\skill_audit\structure_checker.py → _tree_s |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\__init__.py → importlib.util |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_audit\__init__.py → argparse |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._fmt_front |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.RULES |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.TRIGGER_KE |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.CORE_KEYWO |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.WORKFLOW_K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.ARTIFACT_D |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._KNOWN_STA |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._HARDCODED |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._PATH_EXCL |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._is_hardco |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.parse_simp |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._find_skil |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.apply_fix |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.list_fixable |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\__init__.py → io |
| D2 | INFO | 外部依赖: skill_builder | PASS | :0 | scripts\skill_audit\__init__.py → skill_builder.ve |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_bu |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.fix_progress |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_audit\__main__.py → main |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.aud |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.for |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.pro |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\refactor.py → zipfile |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.fo |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\refactor.py → skill_inspecto |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._create_b |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ar |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ex |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._write_js |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\updater.py → skill_inspector |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\updater.py → version_manager |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\utils.py → zipfile |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_builder\__init__.py → argparse |
| D2 | INFO | 外部依赖: creator | PASS | :0 | scripts\skill_builder\__init__.py → creator.SkillC |
| D2 | INFO | 外部依赖: updater | PASS | :0 | scripts\skill_builder\__init__.py → updater.SkillU |
| D2 | INFO | 外部依赖: refactor | PASS | :0 | scripts\skill_builder\__init__.py → refactor.Refac |
| D2 | INFO | 外部依赖: migrator | PASS | :0 | scripts\skill_builder\__init__.py → migrator.Skill |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\__init__.py → version_manage |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\__init__.py → utils.* |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\__init__.py → skill_inspecto |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_builder\__main__.py → main |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\cleanup_manager.py:316 | 12 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\skill_audit\utils.py:331 | ".yml":     "data",   ".db":    "data",   ".sqlite |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\cleanup_manager.py:348 | print("用法: python cleanup_manager.py <skill_dir> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\permission_checker.py:952 | print(json.dumps(report, indent=2, ensure_ascii=Fa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:367 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:373 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:379 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:381 | print("Usage: python -m scripts.skill_inspector <s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:382 | print("只读操作，输出 skill 蓝皮书：结构、AST函数签名、引用链路") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:383 | print("用于 update/refactor 前的全貌扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:394 | print(result) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:126 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:191 | print("\n".join(diff)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:203 | print("用法: python skill_rollback.py rollback <roll |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:214 | print("用法: python skill_rollback.py show <rollback |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:789 | print("    [OK] 更新 _meta.json: data_dir = " + expe |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:824 | print("    [OK] 更新 " + fname + ": " + var_name + " |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:200 | print("用法: python data_dir_checker.py <skill_dir>  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:206 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:207 | print("  R-22 数据目录规范检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:208 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:213 | print(issue) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:216 | print("\n─── 自动修复 ──────────────────────────────── |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:931 | print("  skill-standardization 创建模板（供 LLM 参考）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:948 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:953 | print("用法：") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:954 | print("  python -m skill_audit create-template") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:955 | print("  python -m skill_audit create-template --j |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:956 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:964 | print("-" * 65) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1171 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1176 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1185 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1476 | print(json.dumps({ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1491 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1494 | print("  详细逐项结果:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1499 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1514 | print("可用修复 key（对应审计规则 R-01~R-26）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1517 | print("\n用法: python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1518 | print("      python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1753 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1881 | print("  步骤 2: 对确认为误报的一致性项执行 --classify（ID 格式 C-类型 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2470 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2518 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2894 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\creator.py:731 | print("[!] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:58 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:60 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:61 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:63 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:313 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:418 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:458 | print("[!] SKILL.md 不存在，无法升级版本号") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:465 | print("[!] SKILL.md frontmatter 中未找到 version 字段") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:217 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:226 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:238 | print("[!] permission_checker.py 不存在，跳过授权检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:281 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:346 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:348 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:349 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:351 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:438 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\__init__.py:130 | print(result) |
| D5 | INFO | 发现 48 个验证函数 | PASS | :0 | _check_sensitive_access, _check_critical_write, _c |
| D5 | INFO | 发现 3 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\cleanup_manager | PASS | :0 |  |
| D5 | INFO | 函数可运行: end_session() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 模块可加载: scripts\permission_chec | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\skill_rollback | PASS | :0 |  |
| D5 | INFO | 函数可运行: load_manifest() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: list_backups() | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 模块导入失败: scripts\skill_audit\fi | FAIL | scripts\skill_audit\fix.py:0 | 缺少依赖: attempted relative import with no known pare |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:46 | _resolve_manifest_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:120 | register() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:205 | finalize() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:323 | list_active_manifests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:205 | _get_ast_string_ranges() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:241 | _scan_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:273 | _check_sensitive_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:374 | _is_sensitive_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:441 | _is_regex_pattern() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:513 | _check_critical_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:569 | _check_network_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:594 | _check_file_delete() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:619 | _check_subprocess_call() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:723 | _determine_risk_level() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:744 | _generate_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:769 | _get_recommendation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:45 | safe_read() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:144 | _record_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:25 | inspect_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:257 | _format_text_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:94 | save_manifest() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:129 | rollback() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:166 | show_diff() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:21 | check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:93 | _check_root_artifact_files() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:151 | _check_artifact_directories() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:196 | _scan_dir_recursive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:215 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:249 | _scan_unknown_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:443 | _trace_cross_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:530 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:859 | _check_body_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:173 | _check_argparse_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:227 | _check_data_dir_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:294 | format_consistency_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:348 | apply_consistency_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:49 | _is_fix_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:56 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:186 | log_check_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:29 | _read_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:35 | _write_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:739 | fix_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:786 | fix_create_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1496 | fix_missing_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1728 | fix_section_constraint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2325 | _write_struct() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2336 | _struct_file_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2343 | _render_workflow_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2378 | _render_examples_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2409 | _render_capabilities_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:3254 | fix_license_compliance() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1696 | _norm_rel() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\frontmatter_checker.py:338 | _norm_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\permission_checks.py:157 | check_authorization_present() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:50 | create_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:94 | update_progress_from_audit() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:213 | finalize_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:283 | load_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:316 | format_progress_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:338 | body_has_antipattern_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:420 | body_has_faq_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:505 | _extract_qa_pairs() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:851 | check_doc_code_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:1251 | check_changelog_progressive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:412 | _is_hardcoded_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:493 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:523 | _classify_artifact_by_ext() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:532 | _extract_path_literal() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:541 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:442 | _reclassify_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:462 | _filter_false_positives() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:500 | format_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:626 | _save_html_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:643 | _save_remaining_llm() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:971 | _do_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1439 | cmd_audit_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1548 | _load_fp_ids() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:2234 | _run_audit_loop() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:114 | create() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:208 | _generate_guide_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:333 | _generate_permissions_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:385 | _generate_examples_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:696 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:720 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:814 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:827 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:831 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:20 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:23 | migrate() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:62 | _detect_current_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:124 | _compute_target_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:130 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:162 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:259 | _update_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:284 | _scan_hardcoded_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:543 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:24 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:27 | refactor() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:131 | _build_migration_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:196 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:302 | _write_permission_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:396 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:450 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:507 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:32 | _check_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:67 | _check_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:100 | _check_dir_structure() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:111 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:259 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:427 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:498 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:511 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:515 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:29 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:54 | _write_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:61 | _check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:86 | _check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:92 | request_changelog() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:124 | append_changelog() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\fix.py:0 | scripts\skill_audit\fix.py: 17 个 except / 3430 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\progress_manager.py:0 | scripts\skill_audit\progress_manager.py: 0 个 excep |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\utils.py:0 | scripts\skill_audit\utils.py: 2 个 except / 605 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\creator.py:0 | scripts\skill_builder\creator.py: 1 个 except / 839 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\__init__.py:0 | scripts\skill_builder\__init__.py: 0 个 except / 13 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-standardization |
| 测试时间 | 2026-06-18 17:48 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 9 | 9 | 0 | 100% |
| D1-D6 功能测试 | 409 | 328 | 0 | 80% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景「audit 审计请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「refactor 改造请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「create 创建请求」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「全量审计执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「自动修复执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「版本号三端同步」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 2 个 CLI 命令 |
| S3 | INFO | 工作流「classify 误报标记后 continue」 | PASS | 由外部编排实现，无直接 CLI |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\cleanup_manager. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\permission_check | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\safe_io.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_inspector. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_rollback.p | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\__init__.py | FAIL | 0:文件内容为空 | scripts\__init__.py |
| D1 | INFO | 语法检查: scripts\skill_audit\arti | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\cons | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\data | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fix. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fron | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\perm | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\prog | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\stru | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\util | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\skill_audit\utils | FAIL | 0:文件内容为空 | scripts\skill_audit\utils_restored.py |
| D1 | INFO | 语法检查: scripts\skill_audit\_tre | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__in | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__ma | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\cr | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\mi | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\re | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\up | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ut | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ve | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\cleanup_manager.p | PASS | :0 | exit code 0, stdout 84 chars |
| D1 | INFO | 运行时: scripts\permission_checke | PASS | :0 | exit code 0, stdout 447 chars |
| D1 | INFO | 运行时: scripts\safe_io.py --help | PASS | :0 | exit code 0, stdout 343 chars |
| D1 | WARN | 启动失败: scripts\skill_inspector. | FAIL | scripts\skill_inspector.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\skill_rollback.py | PASS | :0 | exit code 0, stdout 0 chars |
| D1 | WARN | 启动失败: scripts\skill_audit\data | FAIL | scripts\skill_audit\data_dir_checker.py:0 | exit code 1: ddy\skills\skill-standardization\scri |
| D1 | WARN | 启动失败: scripts\skill_audit\__in | FAIL | scripts\skill_audit\__init__.py:0 | exit code 1: \Users\sm001\.workbuddy\skills\skill- |
| D1 | WARN | 启动失败: scripts\skill_audit\__ma | FAIL | scripts\skill_audit\__main__.py:0 | exit code 1: "C:\Users\sm001\.workbuddy\skills\ski |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__init__.py:0 | exit code 1: orkbuddy\skills\skill-standardization |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__main__.py:0 | exit code 1: :\Users\sm001\.workbuddy\skills\skill |
| D2 | WARN | 引用文件不存在 | FAIL | reference.md:0 | reference.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | INFO | 外部依赖: uuid | PASS | :0 | scripts\cleanup_manager.py → uuid |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\permission_checker.py → ast |
| D2 | INFO | 外部依赖: tokenize | PASS | :0 | scripts\permission_checker.py → tokenize |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\permission_checker.py → argparse |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\safe_io.py → io |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\safe_io.py → time |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\safe_io.py → argparse |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_inspector.py → ast |
| D2 | INFO | 外部依赖: logging | PASS | :0 | scripts\skill_rollback.py → logging |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\skill_rollback.py → glob |
| D2 | INFO | 外部依赖: difflib | PASS | :0 | scripts\skill_rollback.py → difflib |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._H |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._P |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._e |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._f |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils.pa |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\data_dir_checker.py → utils._i |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\fix.py → io |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\fix.py → traceback |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils._fmt_frontmatte |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils.parse_simple_ya |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.fix_ |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\fix.py → importlib |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\fix.py → permission_checker.Pe |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\fix.py → data_dir_checker.fix_ |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\fix.py → ast |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.chec |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\permission_checks.py → permiss |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\structure_checker.py → warning |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.T |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: py_compile | PASS | :0 | scripts\skill_audit\structure_checker.py → py_comp |
| D2 | INFO | 外部依赖: _tree_scanner | PASS | :0 | scripts\skill_audit\structure_checker.py → _tree_s |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\__init__.py → importlib.util |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_audit\__init__.py → argparse |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._fmt_front |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.RULES |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.TRIGGER_KE |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.CORE_KEYWO |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.WORKFLOW_K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.ARTIFACT_D |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._KNOWN_STA |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._HARDCODED |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._PATH_EXCL |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._is_hardco |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.parse_simp |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._find_skil |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.apply_fix |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.list_fixable |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\__init__.py → io |
| D2 | INFO | 外部依赖: skill_builder | PASS | :0 | scripts\skill_audit\__init__.py → skill_builder.ve |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_bu |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.fix_progress |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_audit\__main__.py → main |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.aud |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.for |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.pro |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\refactor.py → zipfile |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.fo |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\refactor.py → skill_inspecto |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._create_b |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ar |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ex |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._write_js |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\updater.py → skill_inspector |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\updater.py → version_manager |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\utils.py → zipfile |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_builder\__init__.py → argparse |
| D2 | INFO | 外部依赖: creator | PASS | :0 | scripts\skill_builder\__init__.py → creator.SkillC |
| D2 | INFO | 外部依赖: updater | PASS | :0 | scripts\skill_builder\__init__.py → updater.SkillU |
| D2 | INFO | 外部依赖: refactor | PASS | :0 | scripts\skill_builder\__init__.py → refactor.Refac |
| D2 | INFO | 外部依赖: migrator | PASS | :0 | scripts\skill_builder\__init__.py → migrator.Skill |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\__init__.py → version_manage |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\__init__.py → utils.* |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\__init__.py → skill_inspecto |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_builder\__main__.py → main |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\cleanup_manager.py:316 | 12 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\skill_audit\utils.py:331 | ".yml":     "data",   ".db":    "data",   ".sqlite |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\cleanup_manager.py:348 | print("用法: python cleanup_manager.py <skill_dir> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\permission_checker.py:952 | print(json.dumps(report, indent=2, ensure_ascii=Fa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:367 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:373 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:379 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:381 | print("Usage: python -m scripts.skill_inspector <s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:382 | print("只读操作，输出 skill 蓝皮书：结构、AST函数签名、引用链路") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:383 | print("用于 update/refactor 前的全貌扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:394 | print(result) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:126 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:191 | print("\n".join(diff)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:203 | print("用法: python skill_rollback.py rollback <roll |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:214 | print("用法: python skill_rollback.py show <rollback |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:789 | print("    [OK] 更新 _meta.json: data_dir = " + expe |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:824 | print("    [OK] 更新 " + fname + ": " + var_name + " |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:200 | print("用法: python data_dir_checker.py <skill_dir>  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:206 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:207 | print("  R-22 数据目录规范检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:208 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:213 | print(issue) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:216 | print("\n─── 自动修复 ──────────────────────────────── |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:931 | print("  skill-standardization 创建模板（供 LLM 参考）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:948 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:953 | print("用法：") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:954 | print("  python -m skill_audit create-template") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:955 | print("  python -m skill_audit create-template --j |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:956 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:964 | print("-" * 65) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1171 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1176 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1185 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1476 | print(json.dumps({ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1491 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1494 | print("  详细逐项结果:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1499 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1514 | print("可用修复 key（对应审计规则 R-01~R-26）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1517 | print("\n用法: python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1518 | print("      python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1753 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1881 | print("  步骤 2: 对确认为误报的一致性项执行 --classify（ID 格式 C-类型 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2470 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2518 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2894 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\creator.py:731 | print("[!] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:58 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:60 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:61 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:63 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:313 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:418 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:458 | print("[!] SKILL.md 不存在，无法升级版本号") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:465 | print("[!] SKILL.md frontmatter 中未找到 version 字段") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:217 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:226 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:238 | print("[!] permission_checker.py 不存在，跳过授权检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:281 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:346 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:348 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:349 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:351 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:438 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\__init__.py:130 | print(result) |
| D5 | INFO | 发现 48 个验证函数 | PASS | :0 | _check_sensitive_access, _check_critical_write, _c |
| D5 | INFO | 发现 3 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\cleanup_manager | PASS | :0 |  |
| D5 | INFO | 函数可运行: end_session() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 模块可加载: scripts\permission_chec | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\skill_rollback | PASS | :0 |  |
| D5 | INFO | 函数可运行: load_manifest() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: list_backups() | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 模块导入失败: scripts\skill_audit\fi | FAIL | scripts\skill_audit\fix.py:0 | 缺少依赖: attempted relative import with no known pare |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:46 | _resolve_manifest_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:120 | register() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:205 | finalize() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:323 | list_active_manifests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:205 | _get_ast_string_ranges() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:241 | _scan_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:273 | _check_sensitive_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:374 | _is_sensitive_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:441 | _is_regex_pattern() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:513 | _check_critical_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:569 | _check_network_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:594 | _check_file_delete() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:619 | _check_subprocess_call() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:723 | _determine_risk_level() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:744 | _generate_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:769 | _get_recommendation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:45 | safe_read() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:144 | _record_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:25 | inspect_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:257 | _format_text_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:94 | save_manifest() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:129 | rollback() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:166 | show_diff() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:21 | check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:93 | _check_root_artifact_files() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:151 | _check_artifact_directories() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:196 | _scan_dir_recursive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:215 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:249 | _scan_unknown_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:443 | _trace_cross_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:530 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:859 | _check_body_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:173 | _check_argparse_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:227 | _check_data_dir_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:294 | format_consistency_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:348 | apply_consistency_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:49 | _is_fix_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:56 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:186 | log_check_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:29 | _read_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:35 | _write_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:739 | fix_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:786 | fix_create_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1496 | fix_missing_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1728 | fix_section_constraint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2325 | _write_struct() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2336 | _struct_file_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2343 | _render_workflow_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2378 | _render_examples_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2409 | _render_capabilities_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:3254 | fix_license_compliance() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1696 | _norm_rel() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\frontmatter_checker.py:338 | _norm_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\permission_checks.py:157 | check_authorization_present() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:50 | create_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:94 | update_progress_from_audit() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:213 | finalize_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:283 | load_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:316 | format_progress_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:338 | body_has_antipattern_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:420 | body_has_faq_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:505 | _extract_qa_pairs() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:851 | check_doc_code_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:1251 | check_changelog_progressive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:412 | _is_hardcoded_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:493 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:523 | _classify_artifact_by_ext() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:532 | _extract_path_literal() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:541 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:442 | _reclassify_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:462 | _filter_false_positives() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:500 | format_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:626 | _save_html_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:643 | _save_remaining_llm() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:971 | _do_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1439 | cmd_audit_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1548 | _load_fp_ids() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:2234 | _run_audit_loop() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:114 | create() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:208 | _generate_guide_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:333 | _generate_permissions_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:385 | _generate_examples_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:696 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:720 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:814 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:827 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:831 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:20 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:23 | migrate() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:62 | _detect_current_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:124 | _compute_target_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:130 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:162 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:259 | _update_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:284 | _scan_hardcoded_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:543 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:24 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:27 | refactor() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:131 | _build_migration_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:196 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:302 | _write_permission_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:396 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:450 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:507 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:32 | _check_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:67 | _check_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:100 | _check_dir_structure() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:111 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:259 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:427 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:498 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:511 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:515 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:29 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:54 | _write_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:61 | _check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:86 | _check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:92 | request_changelog() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:124 | append_changelog() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\fix.py:0 | scripts\skill_audit\fix.py: 17 个 except / 3430 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\progress_manager.py:0 | scripts\skill_audit\progress_manager.py: 0 个 excep |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\utils.py:0 | scripts\skill_audit\utils.py: 2 个 except / 605 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\creator.py:0 | scripts\skill_builder\creator.py: 1 个 except / 839 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\__init__.py:0 | scripts\skill_builder\__init__.py: 0 个 except / 13 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | skill-standardization |
| 测试时间 | 2026-06-18 17:49 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 9 | 9 | 0 | 100% |
| D1-D6 功能测试 | 409 | 328 | 0 | 80% |
| S4 执行忠实度 | 15 | 15 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 触发场景「audit 审计请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「refactor 改造请求」 | PASS | 由外部编排实现，无直接 CLI |
| S1 | INFO | 触发场景「create 创建请求」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「全量审计执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「自动修复执行」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力「版本号三端同步」 | PASS | 由外部编排实现，无直接 CLI |
| S2 | INFO | 核心能力执行汇总 | PASS | 执行了 2 个 CLI 命令 |
| S3 | INFO | 工作流「classify 误报标记后 continue」 | PASS | 由外部编排实现，无直接 CLI |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\cleanup_manager. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\permission_check | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\safe_io.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_inspector. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_rollback.p | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\__init__.py | FAIL | 0:文件内容为空 | scripts\__init__.py |
| D1 | INFO | 语法检查: scripts\skill_audit\arti | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\cons | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\data | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fix. | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\fron | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\perm | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\prog | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\stru | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\util | PASS | :0 |  |
| D1 | WARN | 空文件: scripts\skill_audit\utils | FAIL | 0:文件内容为空 | scripts\skill_audit\utils_restored.py |
| D1 | INFO | 语法检查: scripts\skill_audit\_tre | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__in | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_audit\__ma | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\cr | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\mi | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\re | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\up | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ut | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\ve | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\skill_builder\__ | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\cleanup_manager.p | PASS | :0 | exit code 0, stdout 84 chars |
| D1 | INFO | 运行时: scripts\permission_checke | PASS | :0 | exit code 0, stdout 447 chars |
| D1 | INFO | 运行时: scripts\safe_io.py --help | PASS | :0 | exit code 0, stdout 343 chars |
| D1 | WARN | 启动失败: scripts\skill_inspector. | FAIL | scripts\skill_inspector.py:0 | exit code 1:  |
| D1 | INFO | 运行时: scripts\skill_rollback.py | PASS | :0 | exit code 0, stdout 0 chars |
| D1 | WARN | 启动失败: scripts\skill_audit\data | FAIL | scripts\skill_audit\data_dir_checker.py:0 | exit code 1: ddy\skills\skill-standardization\scri |
| D1 | WARN | 启动失败: scripts\skill_audit\__in | FAIL | scripts\skill_audit\__init__.py:0 | exit code 1: \Users\sm001\.workbuddy\skills\skill- |
| D1 | WARN | 启动失败: scripts\skill_audit\__ma | FAIL | scripts\skill_audit\__main__.py:0 | exit code 1: "C:\Users\sm001\.workbuddy\skills\ski |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__init__.py:0 | exit code 1: orkbuddy\skills\skill-standardization |
| D1 | WARN | 启动失败: scripts\skill_builder\__ | FAIL | scripts\skill_builder\__main__.py:0 | exit code 1: :\Users\sm001\.workbuddy\skills\skill |
| D2 | WARN | 引用文件不存在 | FAIL | reference.md:0 | reference.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | WARN | 引用文件不存在 | FAIL | rules.md:0 | rules.md → references/xxx.md |
| D2 | INFO | 外部依赖: uuid | PASS | :0 | scripts\cleanup_manager.py → uuid |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\permission_checker.py → ast |
| D2 | INFO | 外部依赖: tokenize | PASS | :0 | scripts\permission_checker.py → tokenize |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\permission_checker.py → argparse |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\safe_io.py → io |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: time | PASS | :0 | scripts\safe_io.py → time |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\safe_io.py → argparse |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\safe_io.py → scripts.cleanup_manager.regis |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_inspector.py → ast |
| D2 | INFO | 外部依赖: logging | PASS | :0 | scripts\skill_rollback.py → logging |
| D2 | INFO | 外部依赖: glob | PASS | :0 | scripts\skill_rollback.py → glob |
| D2 | INFO | 外部依赖: difflib | PASS | :0 | scripts\skill_rollback.py → difflib |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._R |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._A |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._H |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._P |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._c |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._e |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._f |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils._i |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\artifact_checker.py → utils.pa |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\data_dir_checker.py → utils._i |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\fix.py → io |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\fix.py → traceback |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils._fmt_frontmatte |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\fix.py → utils.parse_simple_ya |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.fix_ |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\fix.py → importlib |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\fix.py → permission_checker.Pe |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\fix.py → data_dir_checker.fix_ |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\fix.py → ast |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\fix.py → artifact_checker.chec |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: safe_io | PASS | :0 | scripts\skill_audit\fix.py → safe_io.safe_write |
| D2 | INFO | 外部依赖: permission_checker | PASS | :0 | scripts\skill_audit\permission_checks.py → permiss |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\structure_checker.py → warning |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.T |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.C |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\structure_checker.py → utils.W |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: py_compile | PASS | :0 | scripts\skill_audit\structure_checker.py → py_comp |
| D2 | INFO | 外部依赖: _tree_scanner | PASS | :0 | scripts\skill_audit\structure_checker.py → _tree_s |
| D2 | INFO | 外部依赖: ast | PASS | :0 | scripts\skill_audit\structure_checker.py → ast |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: warnings | PASS | :0 | scripts\skill_audit\__init__.py → warnings |
| D2 | INFO | 外部依赖: importlib | PASS | :0 | scripts\skill_audit\__init__.py → importlib.util |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_audit\__init__.py → argparse |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._fmt_front |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.RULES |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.TRIGGER_KE |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.CORE_KEYWO |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.WORKFLOW_K |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.ARTIFACT_D |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._KNOWN_STA |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._ARTIFACT_ |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._HARDCODED |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._PATH_EXCL |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._is_hardco |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils.parse_simp |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_audit\__init__.py → utils._find_skil |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: frontmatter_checker | PASS | :0 | scripts\skill_audit\__init__.py → frontmatter_chec |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: structure_checker | PASS | :0 | scripts\skill_audit\__init__.py → structure_checke |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: artifact_checker | PASS | :0 | scripts\skill_audit\__init__.py → artifact_checker |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: permission_checks | PASS | :0 | scripts\skill_audit\__init__.py → permission_check |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: data_dir_checker | PASS | :0 | scripts\skill_audit\__init__.py → data_dir_checker |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.apply_fix |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.list_fixable |
| D2 | INFO | 外部依赖: io | PASS | :0 | scripts\skill_audit\__init__.py → io |
| D2 | INFO | 外部依赖: skill_builder | PASS | :0 | scripts\skill_audit\__init__.py → skill_builder.ve |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_bu |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_audit\__init__.py → skill_inspector. |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: consistency_checker | PASS | :0 | scripts\skill_audit\__init__.py → consistency_chec |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: progress_manager | PASS | :0 | scripts\skill_audit\__init__.py → progress_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.cleanup_ |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\skill_audit\__init__.py → traceback |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: fix | PASS | :0 | scripts\skill_audit\__init__.py → fix.fix_progress |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_audit\__init__.py → scripts.skill_in |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_audit\__main__.py → main |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.aud |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.for |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\creator.py → skill_audit.pro |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\refactor.py → scripts.cleanu |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\refactor.py → zipfile |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.pr |
| D2 | INFO | 外部依赖: skill_audit | PASS | :0 | scripts\skill_builder\refactor.py → skill_audit.fo |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\refactor.py → skill_inspecto |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._create_b |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ar |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._check_ex |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\updater.py → utils._write_js |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: cleanup_manager | PASS | :0 | scripts\skill_builder\updater.py → cleanup_manager |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: scripts | PASS | :0 | scripts\skill_builder\updater.py → scripts.cleanup |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\updater.py → skill_inspector |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\updater.py → version_manager |
| D2 | INFO | 外部依赖: zipfile | PASS | :0 | scripts\skill_builder\utils.py → zipfile |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\skill_builder\__init__.py → argparse |
| D2 | INFO | 外部依赖: creator | PASS | :0 | scripts\skill_builder\__init__.py → creator.SkillC |
| D2 | INFO | 外部依赖: updater | PASS | :0 | scripts\skill_builder\__init__.py → updater.SkillU |
| D2 | INFO | 外部依赖: refactor | PASS | :0 | scripts\skill_builder\__init__.py → refactor.Refac |
| D2 | INFO | 外部依赖: migrator | PASS | :0 | scripts\skill_builder\__init__.py → migrator.Skill |
| D2 | INFO | 外部依赖: version_manager | PASS | :0 | scripts\skill_builder\__init__.py → version_manage |
| D2 | INFO | 外部依赖: utils | PASS | :0 | scripts\skill_builder\__init__.py → utils.* |
| D2 | INFO | 外部依赖: skill_inspector | PASS | :0 | scripts\skill_builder\__init__.py → skill_inspecto |
| D2 | INFO | 外部依赖: main | PASS | :0 | scripts\skill_builder\__main__.py → main |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\cleanup_manager.py:316 | 12 个删除操作分布于不同文件 |
| D3 | WARN | DB 路径可能硬编码 | FAIL | scripts\skill_audit\utils.py:331 | ".yml":     "data",   ".db":    "data",   ".sqlite |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\cleanup_manager.py:348 | print("用法: python cleanup_manager.py <skill_dir> [ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\permission_checker.py:952 | print(json.dumps(report, indent=2, ensure_ascii=Fa |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:367 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:373 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\safe_io.py:379 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:381 | print("Usage: python -m scripts.skill_inspector <s |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:382 | print("只读操作，输出 skill 蓝皮书：结构、AST函数签名、引用链路") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:383 | print("用于 update/refactor 前的全貌扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_inspector.py:394 | print(result) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:126 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:191 | print("\n".join(diff)) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:203 | print("用法: python skill_rollback.py rollback <roll |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_rollback.py:214 | print("用法: python skill_rollback.py show <rollback |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:789 | print("    [OK] 更新 _meta.json: data_dir = " + expe |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\artifact_checker.py:824 | print("    [OK] 更新 " + fname + ": " + var_name + " |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:200 | print("用法: python data_dir_checker.py <skill_dir>  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:206 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:207 | print("  R-22 数据目录规范检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:208 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:213 | print(issue) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\data_dir_checker.py:216 | print("\n─── 自动修复 ──────────────────────────────── |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:931 | print("  skill-standardization 创建模板（供 LLM 参考）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:948 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:953 | print("用法：") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:954 | print("  python -m skill_audit create-template") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:955 | print("  python -m skill_audit create-template --j |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:956 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:964 | print("-" * 65) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1171 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1176 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1185 | print(json.dumps(result, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1476 | print(json.dumps({ |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1491 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1494 | print("  详细逐项结果:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1499 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1514 | print("可用修复 key（对应审计规则 R-01~R-26）:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1517 | print("\n用法: python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1518 | print("      python -m skill_audit fix <skill_dir> |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1753 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:1881 | print("  步骤 2: 对确认为误报的一致性项执行 --classify（ID 格式 C-类型 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2470 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2518 | print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_audit\__init__.py:2894 | print(json.dumps(output, ensure_ascii=False, inden |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\creator.py:731 | print("[!] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:58 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:60 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:61 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:63 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:313 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:418 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:458 | print("[!] SKILL.md 不存在，无法升级版本号") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\refactor.py:465 | print("[!] SKILL.md frontmatter 中未找到 version 字段") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:217 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:226 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:238 | print("[!] permission_checker.py 不存在，跳过授权检查") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:281 | print("[*] SKILL.md 已包含「授权要求」章节，跳过注入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:346 | print("  Skill 结构扫描 — 了解全貌后再改造") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:348 | print(inspect_skill(str(skill_dir))) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:349 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:351 | print("[!] skill_inspector 未找到，跳过结构扫描") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\updater.py:438 | print("[💡] 权限扫描无风险项，跳过 permissions.md 写入") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\skill_builder\__init__.py:130 | print(result) |
| D5 | INFO | 发现 48 个验证函数 | PASS | :0 | _check_sensitive_access, _check_critical_write, _c |
| D5 | INFO | 发现 3 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\cleanup_manager | PASS | :0 |  |
| D5 | INFO | 函数可运行: end_session() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 模块可加载: scripts\permission_chec | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\skill_rollback | PASS | :0 |  |
| D5 | INFO | 函数可运行: load_manifest() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: list_backups() | PASS | :0 | 返回值类型: NoneType |
| D5 | WARN | 模块导入失败: scripts\skill_audit\fi | FAIL | scripts\skill_audit\fix.py:0 | 缺少依赖: attempted relative import with no known pare |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:46 | _resolve_manifest_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:120 | register() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:205 | finalize() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\cleanup_manager.py:323 | list_active_manifests() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:205 | _get_ast_string_ranges() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:241 | _scan_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:273 | _check_sensitive_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:374 | _is_sensitive_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:441 | _is_regex_pattern() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:513 | _check_critical_write() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:569 | _check_network_access() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:594 | _check_file_delete() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:619 | _check_subprocess_call() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:723 | _determine_risk_level() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:744 | _generate_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\permission_checker.py:769 | _get_recommendation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:45 | safe_read() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\safe_io.py:144 | _record_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:25 | inspect_skill() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_inspector.py:257 | _format_text_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:94 | save_manifest() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:129 | rollback() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_rollback.py:166 | show_diff() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:21 | check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:93 | _check_root_artifact_files() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:151 | _check_artifact_directories() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:196 | _scan_dir_recursive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:215 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:249 | _scan_unknown_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:443 | _trace_cross_references() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:530 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\artifact_checker.py:859 | _check_body_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:173 | _check_argparse_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:227 | _check_data_dir_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:294 | format_consistency_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\consistency_checker.py:348 | apply_consistency_fix() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:49 | _is_fix_script() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:56 | check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\data_dir_checker.py:186 | log_check_result() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:29 | _read_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:35 | _write_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:739 | fix_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:786 | fix_create_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1496 | fix_missing_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1728 | fix_section_constraint() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2325 | _write_struct() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2336 | _struct_file_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2343 | _render_workflow_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2378 | _render_examples_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:2409 | _render_capabilities_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:3254 | fix_license_compliance() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\fix.py:1696 | _norm_rel() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\frontmatter_checker.py:338 | _norm_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\permission_checks.py:157 | check_authorization_present() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:50 | create_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:94 | update_progress_from_audit() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:213 | finalize_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:283 | load_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\progress_manager.py:316 | format_progress_markdown() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:338 | body_has_antipattern_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:420 | body_has_faq_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:505 | _extract_qa_pairs() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:851 | check_doc_code_consistency() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\structure_checker.py:1251 | check_changelog_progressive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:412 | _is_hardcoded_path() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:493 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:523 | _classify_artifact_by_ext() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:532 | _extract_path_literal() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\utils.py:541 | _is_asset_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:442 | _reclassify_false_positive() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:462 | _filter_false_positives() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:500 | format_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:626 | _save_html_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:643 | _save_remaining_llm() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:971 | _do_bump() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1439 | cmd_audit_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:1548 | _load_fp_ids() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_audit\__init__.py:2234 | _run_audit_loop() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:114 | create() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:208 | _generate_guide_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:333 | _generate_permissions_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:385 | _generate_examples_template() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:696 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:720 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:814 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:827 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\creator.py:831 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:20 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:23 | migrate() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:62 | _detect_current_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:124 | _compute_target_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:130 | _find_skills_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:162 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:259 | _update_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\migrator.py:284 | _scan_hardcoded_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:543 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:24 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:27 | refactor() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:131 | _build_migration_plan() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:196 | _execute_migration() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:302 | _write_permission_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:396 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:450 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\refactor.py:507 | _audit_and_update_progress() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:32 | _check_meta_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:67 | _check_skill_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:100 | _check_dir_structure() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:111 | _bump_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:259 | _inject_auth_section() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:427 | _write_permissions_md() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:498 | _get_category_description() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:511 | _get_item_explanation() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\updater.py:515 | _get_auth_method() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:29 | _create_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:54 | _write_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:61 | _check_artifact_paths() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\utils.py:86 | _check_external_data_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:92 | request_changelog() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\skill_builder\version_manager.py:124 | append_changelog() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\fix.py:0 | scripts\skill_audit\fix.py: 17 个 except / 3430 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\progress_manager.py:0 | scripts\skill_audit\progress_manager.py: 0 个 excep |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_audit\utils.py:0 | scripts\skill_audit\utils.py: 2 个 except / 605 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\creator.py:0 | scripts\skill_builder\creator.py: 1 个 except / 839 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\skill_builder\__init__.py:0 | scripts\skill_builder\__init__.py: 0 个 except / 13 |

### S4 执行忠实度
- 总噪声条目: 15
- 铁律坚守: 15 (100%)
