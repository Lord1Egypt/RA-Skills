#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能编程助手 CLI - 多模型协作编程工具
"""

import json
import sys
import os
from pathlib import Path
from typing import Optional
import subprocess

# 导入模型路由器
from model_router import route_task, MODEL_PROFILES, TaskType


def load_config() -> dict:
    """加载配置文件"""
    config_path = Path.home() / ".smart_coding_config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "default_model": "qwen-coder-plus",
        "review_model": "claude-sonnet",
        "enable_caching": True,
        "max_collab_models": 3,
        "cost_limit_per_task": 5.0
    }


def call_model(model: str, prompt: str, system_prompt: str = "") -> str:
    """
    调用模型 API
    
    实际使用时需要根据你的 API 配置实现
    这里提供 Bailian/DeepSeek/GLM 的示例
    """
    config = load_config()
    
    # 示例：使用 Bailian API
    if model.startswith("qwen"):
        return call_bailian(model, prompt, system_prompt)
    elif model.startswith("deepseek"):
        return call_deepseek(model, prompt, system_prompt)
    elif model.startswith("glm"):
        return call_glm(model, prompt, system_prompt)
    else:
        raise ValueError(f"不支持的模型：{model}")


def call_bailian(model: str, prompt: str, system_prompt: str = "") -> str:
    """调用 Bailian API"""
    api_key = os.environ.get("QWEN_API_KEY")
    if not api_key:
        raise EnvironmentError("未设置 QWEN_API_KEY 环境变量")
    
    # 这里应该调用实际的 API
    # 示例代码结构：
    """
    from http import HTTPStatus
    import dashscope
    
    dashscope.api_key = api_key
    
    response = dashscope.Generation.call(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    
    if response.status_code == HTTPStatus.OK:
        return response.output.text
    else:
        raise Exception(f"API 调用失败：{response.code} - {response.message}")
    """
    
    # Mock 响应（实际使用时删除）
    return f"[{model}] 收到任务：{prompt[:50]}..."


def call_deepseek(model: str, prompt: str, system_prompt: str = "") -> str:
    """调用 DeepSeek API"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise EnvironmentError("未设置 DEEPSEEK_API_KEY 环境变量")
    
    # 类似实现...
    return f"[{model}] 收到任务：{prompt[:50]}..."


def call_glm(model: str, prompt: str, system_prompt: str = "") -> str:
    """调用 GLM API"""
    api_key = os.environ.get("GLM_API_KEY")
    if not api_key:
        raise EnvironmentError("未设置 GLM_API_KEY 环境变量")
    
    # 类似实现...
    return f"[{model}] 收到任务：{prompt[:50]}..."


def execute_single_task(
    task: str,
    model: Optional[str] = None,
    verbose: bool = False
) -> str:
    """
    执行单个编程任务
    
    Args:
        task: 任务描述
        model: 指定模型（None 则自动选择）
        verbose: 是否输出详细信息
        
    Returns:
        模型响应
    """
    # 路由任务
    route_result = route_task(task, verbose=verbose)
    
    if model is None:
        model = route_result["recommended_model"]
    
    if verbose:
        print(f"\n🎯 使用模型：{model}")
        print(f"📋 任务类型：{route_result['task_type']}")
    
    # 构建系统提示
    system_prompt = build_system_prompt(route_result["task_type"])
    
    # 调用模型
    response = call_model(model, task, system_prompt)
    
    return response


def execute_collab_task(
    task: str,
    verbose: bool = False
) -> str:
    """
    执行多模型协作任务
    
    Args:
        task: 任务描述
        verbose: 是否输出详细信息
        
    Returns:
        最终结果
    """
    # 路由任务
    route_result = route_task(task, verbose=verbose)
    
    if not route_result["collaboration_mode"]:
        return execute_single_task(task, verbose=verbose)
    
    collab_plan = route_result["collaboration_plan"]
    
    if verbose:
        print(f"\n🔄 启用协作模式：{' → '.join(collab_plan)}")
    
    # 执行协作流程
    context = task
    results = []
    
    for i, model in enumerate(collab_plan):
        if verbose:
            print(f"\n[{i+1}/{len(collab_plan)}] 使用 {model}...")
        
        # 根据角色构建提示
        if i == 0:
            prompt = context
            system_prompt = build_system_prompt(route_result["task_type"])
        else:
            # 后续模型进行审查/优化
            prompt = f"""
前序工作成果：
{results[-1]}

请审查并提出改进建议，然后给出优化后的版本。
"""
            system_prompt = "你是一位代码审查专家，请仔细审查代码质量、安全性、性能等方面。"
        
        response = call_model(model, prompt, system_prompt)
        results.append(response)
        
        if verbose:
            print(f"✅ {model} 完成")
    
    # 返回最终结果
    return results[-1]


def build_system_prompt(task_type: str) -> str:
    """根据任务类型构建系统提示"""
    
    prompts = {
        "code_generation": """你是一位资深软件工程师，擅长编写高质量、可维护的代码。
请遵循以下原则：
1. 代码清晰易懂，命名规范
2. 添加必要的注释和文档
3. 考虑边界情况和错误处理
4. 遵循最佳实践和设计模式
5. 提供使用示例""",
        
        "code_review": """你是一位代码审查专家，擅长发现代码中的问题和改进空间。
请从以下维度审查：
1. 代码质量和可读性
2. 潜在的安全隐患
3. 性能瓶颈
4. 设计模式和架构
5. 测试覆盖
6. 改进建议""",
        
        "bug_debug": """你是一位调试专家，擅长快速定位和修复 Bug。
请按以下步骤：
1. 分析错误现象和日志
2. 定位问题根源
3. 提供修复方案
4. 解释问题原因
5. 给出预防建议""",
        
        "performance_opt": """你是一位性能优化专家，擅长提升代码执行效率。
请从以下方面优化：
1. 算法复杂度
2. 内存使用
3. 并发处理
4. 缓存策略
5. 资源利用""",
        
        "refactoring": """你是一位重构专家，擅长改进代码结构。
请遵循以下原则：
1. 保持外部行为不变
2. 提高代码可读性
3. 减少代码重复
4. 应用设计模式
5. 改进模块化""",
        
        "unit_test": """你是一位测试专家，擅长编写全面的单元测试。
请确保：
1. 覆盖正常路径
2. 覆盖边界情况
3. 覆盖异常情况
4. 使用合适的 Mock
5. 测试用例清晰独立""",
        
        "technical_qa": """你是一位技术专家，擅长解答技术问题。
请确保回答：
1. 准确清晰
2. 有深度但不晦涩
3. 提供示例代码
4. 指出常见误区
5. 给出进一步学习建议""",
        
        "documentation": """你是一位文档专家，擅长编写清晰的技术文档。
请确保文档：
1. 结构清晰
2. 语言简洁
3. 示例充分
4. 覆盖常见场景
5. 易于理解和查阅""",
        
        "architecture": """你是一位架构师，擅长设计可扩展的系统架构。
请考虑：
1. 业务需求
2. 可扩展性
3. 可维护性
4. 性能要求
5. 安全考虑
6. 技术选型""",
        
        "code_explanation": """你是一位技术导师，擅长解释代码。
请确保解释：
1. 清晰易懂
2. 逐行分析关键逻辑
3. 说明设计意图
4. 指出潜在问题
5. 提供改进建议"""
    }
    
    return prompts.get(task_type, "你是一位专业的编程助手，请帮助用户完成编程任务。")


def interactive_mode():
    """交互模式"""
    print("🤖 智能编程助手 - 交互模式")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'help' 查看帮助\n")
    
    while True:
        try:
            task = input(">>> ").strip()
            
            if task.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            
            if task.lower() == 'help':
                print("""
帮助：
- 直接输入编程任务，如："写一个快速排序"
- 添加 --collab 启用协作模式："重构这个模块 --collab"
- 添加 --model 指定模型："生成代码 --model qwen-max"
- 添加 --verbose 显示详细信息："任务 --verbose"
                """)
                continue
            
            # 解析参数
            verbose = "--verbose" in task or "-v" in task
            collab = "--collab" in task
            model = None
            
            # 提取 --model 参数
            if "--model" in task:
                parts = task.split("--model")
                task = parts[0].strip()
                model = parts[1].strip().split()[0] if len(parts) > 1 else None
            
            # 清理任务字符串
            task = task.replace("--verbose", "").replace("-v", "").replace("--collab", "").strip()
            
            if not task:
                continue
            
            # 执行任务
            if collab:
                result = execute_collab_task(task, verbose=verbose)
            else:
                result = execute_single_task(task, model=model, verbose=verbose)
            
            print("\n" + "="*60)
            print(result)
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"❌ 错误：{e}\n")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='智能编程助手 - 多模型协作编程工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "写一个快速排序"
  %(prog)s "审查这段代码" --collab
  %(prog)s "优化性能" --model qwen-coder-plus
  %(prog)s --interactive
        """
    )
    
    parser.add_argument('task', nargs='?', help='编程任务描述')
    parser.add_argument('--model', '-m', type=str, help='指定模型')
    parser.add_argument('--collab', '-c', action='store_true', help='启用多模型协作')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    parser.add_argument('--json', '-j', action='store_true', help='JSON 格式输出')
    
    args = parser.parse_args()
    
    if args.interactive or not args.task:
        interactive_mode()
        return
    
    if args.collab:
        result = execute_collab_task(args.task, verbose=args.verbose)
    else:
        result = execute_single_task(args.task, model=args.model, verbose=args.verbose)
    
    if args.json:
        print(json.dumps({"result": result}, ensure_ascii=False, indent=2))
    else:
        print(result)


if __name__ == "__main__":
    main()
