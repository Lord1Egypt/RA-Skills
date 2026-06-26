# -*- coding: utf-8 -*-
"""
拼接器核心 - V3.0

把对话里出现的 Skill/Tool/Function 按顺序拼接成可执行代码
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from chain_extractor import extract_execution_chain
from param_recognizer import recognize_params
from output_handler import get_output_function_code


class WorkflowJoiner:
    """工作流拼接器"""
    
    def __init__(self, task_name: str = "固化任务"):
        self.task_name = task_name
        self.output_dir = "./fixed_tasks"
        self.log_dir = "./task_logs"
        
        # 确保目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
    
    def join(self, conversation: List[Dict[str, str]], 
             output_type: str = "screen",
             output_path: str = None,
             api_url: str = None) -> Dict[str, Any]:
        """
        拼接工作流
        
        Args:
            conversation: 对话历史
            output_type: 输出方式 (screen/file/api/web)
            output_path: 输出文件路径
            api_url: API URL
            
        Returns:
            拼接结果 {code, params, program_path}
        """
        # 1. 提取执行链
        execution_chain = extract_execution_chain(conversation)
        
        if not execution_chain:
            return {
                "status": "error",
                "message": "未从对话中提取到 Skill/Tool/Function 调用"
            }
        
        # 2. 识别参数
        params = recognize_params(conversation, execution_chain)
        
        # 3. 拼接代码
        code = self._generate_code(execution_chain, params, 
                                    output_type, output_path, api_url)
        
        # 4. 保存程序
        safe_name = self._sanitize_name(self.task_name)
        program_path = os.path.join(self.output_dir, f"{safe_name}.py")
        
        with open(program_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        return {
            "status": "success",
            "code": code,
            "params": params,
            "execution_chain": execution_chain,
            "program_path": program_path
        }
    
    def _generate_code(self, chain: List[Dict], params: Dict,
                       output_type: str, output_path: str, 
                       api_url: str) -> str:
        """生成 Python 代码"""
        
        # 代码头部
        code = f'''# -*- coding: utf-8 -*-
"""
OpenClaw 固化程序：{self.task_name}
生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
输出方式：{output_type}
"""

import logging
from datetime import datetime
from exception_wrapper import level3_wrapper, raise_level1, raise_level2, raise_level3
from output_handler import output_screen, output_file, output_api, output_web

# ==================== 配置区域 ====================
TASK_NAME = "{self.task_name}"
LOG_DIR = "{self.log_dir}"

# 自动识别的参数
params = {self._format_params(params)}

# ==================== 业务函数占位 ====================
# 以下是从对话中提取的 Skill/Tool 调用
# 实际使用时需要实现这些函数或导入对应模块

'''
        
        # 收集需要声明的函数
        declared_funcs = set()
        
        for step in chain:
            func_name = step["name"]
            if func_name not in declared_funcs:
                code += f'''def {func_name}(**kwargs):
    """{step['type']} 函数：{func_name}"""
    # TODO: 实现具体逻辑或导入对应模块
    # 示例：return skill_module.{func_name}(**kwargs)
    pass

'''
                declared_funcs.add(func_name)
        
        # 生成 run 函数
        code += '''# ==================== 主执行逻辑 ====================
@level3_wrapper(task_name=TASK_NAME, log_dir=LOG_DIR)
def run():
    """拼接的执行流程"""
'''
        
        # 拼接执行步骤
        for i, step in enumerate(chain):
            func_name = step["name"]
            params_str = self._format_call_params(step["params"])
            
            if i < len(chain) - 1:
                # 中间步骤
                code += f'''    result_{i+1} = {func_name}({params_str})
'''
            else:
                # 最后一步，添加输出
                code += f'''    result = {func_name}({params_str})
    {get_output_function_code(output_type, output_path, api_url)}
    return result

'''
        
        # 添加入口
        code += '''
# ==================== 入口 ====================
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    result = run()
    print(f"程序执行完成：{result}")
'''
        
        return code
    
    def _format_params(self, params: Dict) -> str:
        """格式化参数字典"""
        # 过滤内部参数
        display_params = {k: v for k, v in params.items() 
                         if not k.startswith("_")}
        return self._python_repr(display_params)
    
    def _python_repr(self, obj: Any) -> str:
        """生成 Python 字面量表示"""
        if isinstance(obj, dict):
            items = [f'"{k}": {self._python_repr(v)}' for k, v in obj.items()]
            return "{\n        " + ",\n        ".join(items) + "\n    }"
        elif isinstance(obj, str):
            return f'"{obj}"'
        elif isinstance(obj, bool):
            return "True" if obj else "False"
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, list):
            items = [self._python_repr(item) for item in obj]
            return "[" + ", ".join(items) + "]"
        else:
            return f'"{str(obj)}"'
    
    def _format_call_params(self, params: Dict) -> str:
        """格式化函数调用参数"""
        if not params:
            return ""
        
        items = []
        for key, value in params.items():
            if isinstance(value, str):
                items.append(f'{key}=params.get("{key}", "{value}")')
            else:
                items.append(f'{key}=params.get("{key}", {self._python_repr(value)})')
        
        return ", ".join(items)
    
    def _sanitize_name(self, name: str) -> str:
        """清理文件名"""
        import re
        sanitized = re.sub(r'[^\w\u4e00-\u9fff]', '_', name)
        return sanitized.strip()


def join_workflow(conversation: List[Dict[str, str]], 
                  task_name: str = "固化任务",
                  output_type: str = "screen",
                  output_path: str = None,
                  api_url: str = None) -> Dict[str, Any]:
    """便捷函数：拼接工作流"""
    joiner = WorkflowJoiner(task_name)
    return joiner.join(conversation, output_type, output_path, api_url)


# 测试
if __name__ == "__main__":
    test_conversation = [
        {"role": "user", "content": "帮我搜索 AI 相关新闻，keyword=AI, limit=10"},
        {"role": "assistant", "content": "已调用 skill_search(keyword='AI', limit=10)"},
        {"role": "user", "content": "保存到 result.csv"},
        {"role": "assistant", "content": "已调用 tool_file_save(data, path='result.csv')"}
    ]
    
    result = join_workflow(test_conversation, task_name="新闻监控", 
                          output_type="file", output_path="./result.csv")
    
    print(f"状态：{result['status']}")
    print(f"程序路径：{result.get('program_path')}")
    print(f"\n生成的代码:\n{result.get('code', '')}")
