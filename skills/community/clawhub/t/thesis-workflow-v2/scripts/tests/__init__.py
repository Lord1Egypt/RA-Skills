# scripts/tests package marker
#
# 原 __init__.py 包含 25 个 unittest.TestCase 测试类
# （TestStateManager 8 + TestLoopSelfCheck 12 + TestMd2DocxStrict 5）
# 但 pytest 默认不收集 __init__.py 里的测试。
#
# 修复 P2-2：已拆分到独立文件
# - test_state_manager.py
# - test_loop_self_check.py
# - test_md2docx_strict.py
# 现在 pytest 能正常收集这 25 个测试。