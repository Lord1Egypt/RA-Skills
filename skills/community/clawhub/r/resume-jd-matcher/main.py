# -*- coding: utf-8 -*-
"""
Resume-JD-Matcher Skill - OpenClaw 入口处理器

当用户在 OpenClaw 中发送 /skill resume-jd-matcher 时触发
"""

import os
import sys

# 添加工作区路径
sys.path.insert(0, r"C:\Users\Administrator\.openclaw\workspace")

def handle_skill(context):
    """
    Skill 入口函数
    
    Args:
        context: OpenClaw 上下文（包含用户消息、配置等）
    
    Returns:
        str: 回复用户的消息
    """
    from sessions_spawn import sessions_spawn
    from subagents import subagents
    from sessions_history import sessions_history
    
    # 配置路径
    JD_FOLDER = r"C:\ResumeJD\JD"
    JL_FOLDER = r"C:\ResumeJD\JL"
    OUTPUT_FOLDER = r"C:\ResumeJD\JG"
    
    # 动态导入处理函数（避免直接 import 带版本号的模块）
    import importlib.util
    spec = importlib.util.spec_from_file_location("resume_match", r"C:\Users\Administrator\.openclaw\workspace\resume_match_v2.0.2.py")
    resume_match = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resume_match)
    
    get_jd_contents = resume_match.get_jd_contents
    find_matching_jd = resume_match.find_matching_jd
    extract_text = resume_match.extract_text
    call_subagent_batch = resume_match.call_subagent_batch
    create_excel = resume_match.create_excel
    
    # 1. 读取 JD
    print("[1] 读取 JD 文件...")
    jd_data = get_jd_contents(JD_FOLDER)
    
    # 2. 扫描简历
    print("[2] 扫描简历目录...")
    jl_folders = [f for f in os.listdir(JL_FOLDER) if os.path.isdir(os.path.join(JL_FOLDER, f))]
    
    # 3. 创建任务
    all_tasks = []
    
    for folder_name in jl_folders:
        folder_path = os.path.join(JL_FOLDER, folder_name)
        print(f"[3] 处理：{folder_name}")
        
        jd_requirements = find_matching_jd(folder_name, jd_data)
        if not jd_requirements:
            print(f"  未找到匹配 JD，跳过")
            continue
        
        resume_files = [
            f for f in os.listdir(folder_path)
            if f.endswith(('.pdf', '.docx')) and not f.startswith('~$')
        ]
        
        for resume_file in resume_files:
            resume_path = os.path.join(folder_path, resume_file)
            resume_key = resume_file.replace('.docx', '').replace('.pdf', '').strip()
            resume_content = extract_text(resume_path)
            
            if not resume_content.strip():
                continue
            
            for (position_name, req_list) in jd_requirements:
                for requirement in req_list:
                    all_tasks.append({
                        'resume_name': resume_key,
                        'resume_text': resume_content,
                        'position_name': position_name,
                        'job_requirement': requirement
                    })
    
    print(f"共 {len(all_tasks)} 个分析任务")
    
    # 4. 批量调用子 Agent
    results = call_subagent_batch(all_tasks, max_concurrent=3)
    
    # 5. 格式化结果
    from datetime import datetime
    formatted_results = []
    for r in results:
        formatted_results.append({
            'resume_name': r['task']['resume_name'],
            'position': r['task']['position_name'],
            'requirement': r['task']['job_requirement'],
            'match_level': r['match_level'],
            'ai_result': r['result'],
            'process_time': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
    
    # 6. 生成 Excel
    import os
    output_path = os.path.join(OUTPUT_FOLDER, f"AI_Resume_All_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    create_excel(formatted_results, output_path)
    
    # 7. 返回结果
    return f"""✅ 简历匹配完成！

**处理统计**：
- JD 文件：{len(jd_data)} 个
- 简历文件夹：{len(jl_folders)} 个
- 分析任务：{len(all_tasks)} 个
- 成功：{len(results)} 个

**输出文件**：
{output_path}

**Excel 包含**：
1. 简历匹配结果（明细表）- 每条任职要求一行
2. 应聘者总体评估表（汇总表）- 按人平均分排序
"""

# OpenClaw 会调用这个函数
if __name__ == "__main__":
    # 测试运行
    result = handle_skill({})
    print(result)
