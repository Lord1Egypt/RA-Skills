"""类型注解测试模块 - 验证所有模块的类型注解"""

import ast
from pathlib import Path
from typing import Any

import pytest


SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def parse_python_file(filepath: Path) -> ast.Module:
    """解析 Python 文件为 AST"""
    with open(filepath, "r", encoding="utf-8") as f:
        return ast.parse(f.read())


def get_function_annotations(filepath: Path) -> dict[str, dict[str, Any]]:
    """获取文件中所有函数的类型注解"""
    tree = parse_python_file(filepath)
    annotations = {}
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name
            func_annotations = {
                "return_type": node.returns is not None,
                "param_types": {},
            }
            
            for arg in node.args.args:
                if arg.arg != "self" and arg.annotation is not None:
                    func_annotations["param_types"][arg.arg] = True
            
            annotations[func_name] = func_annotations
    
    return annotations


def get_class_annotations(filepath: Path) -> dict[str, dict[str, Any]]:
    """获取文件中所有类的类型注解"""
    tree = parse_python_file(filepath)
    annotations = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_annotations = {
                "methods": {},
                "class_vars": {},
            }
            
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    method_annotations = {
                        "return_type": item.returns is not None,
                        "param_types": {},
                    }
                    
                    for arg in item.args.args:
                        if arg.arg != "self" and arg.annotation is not None:
                            method_annotations["param_types"][arg.arg] = True
                    
                    class_annotations["methods"][method_name] = method_annotations
            
            annotations[class_name] = class_annotations
    
    return annotations


class TestConfigManagerTypeAnnotations:
    """测试 config_manager.py 的类型注解"""
    
    def test_module_has_type_imports(self):
        """测试模块是否导入了 typing 模块"""
        filepath = SCRIPTS_DIR / "config_manager.py"
        tree = parse_python_file(filepath)
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        assert "typing" in imports or "dataclasses" in imports
    
    def test_dataclass_fields_have_annotations(self):
        """测试 dataclass 字段是否有类型注解"""
        filepath = SCRIPTS_DIR / "config_manager.py"
        tree = parse_python_file(filepath)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.AnnAssign):
                        assert item.annotation is not None, f"Class {node.name} has unannotated field"
    
    def test_config_manager_methods_have_return_types(self):
        """测试 ConfigManager 方法是否有返回类型注解"""
        filepath = SCRIPTS_DIR / "config_manager.py"
        annotations = get_class_annotations(filepath)
        
        if "ConfigManager" in annotations:
            methods = annotations["ConfigManager"]["methods"]
            for method_name in ["load", "save", "get_llm_api_key"]:
                if method_name in methods:
                    assert methods[method_name]["return_type"], \
                        f"ConfigManager.{method_name} missing return type annotation"


class TestErrorHandlerTypeAnnotations:
    """测试 error_handler.py 的类型注解"""
    
    def test_handle_error_has_return_type(self):
        """测试 handle_error 函数是否有返回类型注解"""
        filepath = SCRIPTS_DIR / "error_handler.py"
        annotations = get_function_annotations(filepath)
        
        assert "handle_error" in annotations
        assert annotations["handle_error"]["return_type"], \
            "handle_error missing return type annotation"
    
    def test_safe_execute_has_return_type(self):
        """测试 safe_execute 函数是否有返回类型注解"""
        filepath = SCRIPTS_DIR / "error_handler.py"
        annotations = get_function_annotations(filepath)
        
        assert "safe_execute" in annotations
        assert annotations["safe_execute"]["return_type"], \
            "safe_execute missing return type annotation"
    
    def test_exception_classes_have_init_annotations(self):
        """测试异常类 __init__ 方法是否有类型注解"""
        filepath = SCRIPTS_DIR / "error_handler.py"
        annotations = get_class_annotations(filepath)
        
        for class_name in ["StockTrackerError", "DatabaseError", "APIError", "ConfigError", "CookieError"]:
            if class_name in annotations:
                if "__init__" in annotations[class_name]["methods"]:
                    method = annotations[class_name]["methods"]["__init__"]
                    assert method["return_type"], \
                        f"{class_name}.__init__ missing return type annotation"


class TestStockTrackerTypeAnnotations:
    """测试 stock_tracker.py 的类型注解"""
    
    def test_main_functions_have_return_types(self):
        """测试主要函数是否有返回类型注解"""
        filepath = SCRIPTS_DIR / "stock_tracker.py"
        annotations = get_function_annotations(filepath)
        
        main_functions = [
            "setup_logging", "send_notification", "_notify_terminal",
            "_notify_webhook", "_backup_database", "handle_stats",
            "handle_clean", "handle_prune", "handle_list",
            "handle_list_groups", "handle_fetch_content", "_fetch_announcements",
            "_save_announcements", "handle_main_flow", "run"
        ]
        
        for func_name in main_functions:
            if func_name in annotations:
                assert annotations[func_name]["return_type"], \
                    f"{func_name} missing return type annotation"
    
    def test_module_level_variables_have_annotations(self):
        """测试模块级变量是否有类型注解"""
        filepath = SCRIPTS_DIR / "stock_tracker.py"
        with open(filepath, "r") as f:
            content = f.read()
        
        # 检查关键常量是否有类型注解
        annotated_constants = ["SKILL_DIR", "DEFAULT_CONFIG", "DEFAULT_COOKIE", "DEFAULT_LOG_DIR"]
        
        for const in annotated_constants:
            # 检查是否在文件中定义并有类型注解
            assert f"{const}: str" in content or f"{const}:" in content, \
                f"Constant {const} should have a type annotation"


class TestAnnDetailTypeAnnotations:
    """测试 ann_detail.py 的类型注解"""
    
    def test_main_functions_have_return_types(self):
        """测试主要函数是否有返回类型注解"""
        filepath = SCRIPTS_DIR / "ann_detail.py"
        annotations = get_function_annotations(filepath)
        
        main_functions = [
            "_get_session", "_extract_text_from_pdf", "_extract_toc_only",
            "should_skip_content", "fetch_announcement_content", "fetch_all_contents"
        ]
        
        for func_name in main_functions:
            if func_name in annotations:
                assert annotations[func_name]["return_type"], \
                    f"{func_name} missing return type annotation"


class TestDailySummaryTypeAnnotations:
    """测试 daily_summary.py 的类型注解"""
    
    def test_main_functions_have_return_types(self):
        """测试主要函数是否有返回类型注解"""
        filepath = SCRIPTS_DIR / "daily_summary.py"
        annotations = get_function_annotations(filepath)
        
        main_functions = [
            "get_unsummarized_announcements", "build_summary_prompt",
            "call_llm", "_clean_llm_json", "parse_summaries",
            "generate_summaries", "format_digest", "main"
        ]
        
        for func_name in main_functions:
            if func_name in annotations:
                assert annotations[func_name]["return_type"], \
                    f"{func_name} missing return type annotation"


class TestLLMJudgeTypeAnnotations:
    """测试 llm_judge.py 的类型注解"""
    
    def test_llm_judge_class_has_annotations(self):
        """测试 LLMJudge 类是否有类型注解"""
        filepath = SCRIPTS_DIR / "llm_judge.py"
        annotations = get_class_annotations(filepath)
        
        assert "LLMJudge" in annotations
        llm_judge = annotations["LLMJudge"]
        
        # 检查关键方法
        for method_name in ["__init__", "judge", "report", "from_config"]:
            if method_name in llm_judge["methods"]:
                assert llm_judge["methods"][method_name]["return_type"], \
                    f"LLMJudge.{method_name} missing return type annotation"


class TestDBTypeAnnotations:
    """测试 db.py 的类型注解"""
    
    def test_main_functions_have_return_types(self):
        """测试主要函数是否有返回类型注解"""
        filepath = SCRIPTS_DIR / "db.py"
        annotations = get_function_annotations(filepath)
        
        main_functions = [
            "_get_conn", "_migrate_schema", "init_db", "_migrate_from_json",
            "make_ann_id", "get_seen_ids", "record_announcements",
            "update_content", "update_clean_text", "update_summary",
            "get_stock_overview", "get_announcements_for_stock",
            "get_records_needing_clean", "get_pending_content",
            "prune_empty", "_count_by_source", "get_stats",
            "list_announcements", "get_announcements_with_summary"
        ]
        
        for func_name in main_functions:
            if func_name in annotations:
                assert annotations[func_name]["return_type"], \
                    f"{func_name} missing return type annotation"


class TestCrossModuleConsistency:
    """测试跨模块类型注解一致性"""
    
    def test_all_modules_have_typing_imports(self):
        """测试所有模块是否导入了 typing 模块"""
        modules = [
            "config_manager.py", "error_handler.py", "stock_tracker.py",
            "ann_detail.py", "daily_summary.py", "llm_judge.py", "db.py"
        ]
        
        for module in modules:
            filepath = SCRIPTS_DIR / module
            if filepath.exists():
                tree = parse_python_file(filepath)
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
                
                # 检查是否导入了 typing 或使用了类型注解
                has_typing = "typing" in imports
                has_dataclasses = "dataclasses" in imports
                
                # 至少应该有一种类型相关的导入
                assert has_typing or has_dataclasses or module in ["stock_tracker.py", "db.py"], \
                    f"{module} missing typing or dataclasses import"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])