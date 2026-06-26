# -*- coding: utf-8 -*-
"""
简历与 JD 智能匹配 - 批量处理演示
展示如何在 OpenClaw 中使用 subagent 模式进行批量简历分析

使用方法：
在 OpenClaw 中运行此脚本，或通过消息触发 skill
"""

import os
import json
import yaml
import glob
import time
from datetime import datetime

# 配置路径
CONFIG_PATH = r"C:\Users\Administrator\.openclaw\workspace\config_resume_match.yaml"
JD_FOLDER = r"C:\ResumeJD\JD"
JL_FOLDER = r"C:\ResumeJD\JL"
OUTPUT_FOLDER = r"C:\ResumeJD\JG"

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def read_docx(file_path):
    try:
        import docx
        doc = docx.Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])
    except:
        return ""

def read_pdf(file_path):
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ''
                if t.strip():
                    text.append(t)
        return '\n'.join(text)
    except:
        return ""

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return read_docx(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    return ""

def get_jd_requirements(jd_file):
    """从 JD 文件中提取任职要求"""
    content = read_docx(jd_file)
    lines = content.split('\n')
    in_req = False
    requirements = []
    
    for line in lines:
        line = line.strip()
        if '任职要求' in line or '岗位要求' in line:
            in_req = True
            continue
        if in_req and line:
            if any(kw in line for kw in ['岗位职责', '福利', '邮箱']):
                break
            requirements.append(line)
    
    return requirements if requirements else [content[:1500]]

# ========== 批量处理核心 ==========
def process_resume_batch():
    """
    批量处理简历 - 演示 subagent 模式
    
    这个函数展示如何在 OpenClaw 中批量调用子 Agent
    """
    print("=" * 60)
    print("简历与 JD 智能匹配 - Subagent 批量处理演示")
    print("=" * 60)
    
    # 1. 读取 JD
    print("\n[1] 读取 JD 文件...")
    jd_files = glob.glob(os.path.join(JD_FOLDER, '*.docx'))
    
    if not jd_files:
        print(f"  ❌ 未找到 JD 文件：{JD_FOLDER}")
        return
    
    jd_data = {}
    for jd_file in jd_files:
        jd_name = os.path.basename(jd_file).replace('.docx', '')
        requirements = get_jd_requirements(jd_file)
        jd_data[jd_name] = requirements
        print(f"  ✅ {jd_name}: {len(requirements)} 条任职要求")
    
    # 2. 扫描简历
    print(f"\n[2] 扫描简历目录...")
    jl_folders = [f for f in os.listdir(JL_FOLDER) if os.path.isdir(os.path.join(JL_FOLDER, f))]
    print(f"  找到 {len(jl_folders)} 个简历文件夹")
    
    # 3. 批量分析（演示用，实际处理 1-2 份简历）
    print(f"\n[3] 开始批量分析（演示模式）...")
    
    tasks_submitted = []
    
    for folder_name in jl_folders[:2]:  # 演示：只处理前 2 个文件夹
        folder_path = os.path.join(JL_FOLDER, folder_name)
        print(f"\n  处理文件夹：{folder_name}")
        
        # 匹配 JD（简单匹配）
        matched_jd = None
        for jd_name, requirements in jd_data.items():
            if any(kw in folder_name.lower() for kw in jd_name.lower().split() if len(kw) > 2):
                matched_jd = (jd_name, requirements)
                break
        
        if not matched_jd:
            print(f"    ⚠️ 未找到匹配的 JD，跳过")
            continue
        
        jd_name, requirements = matched_jd
        print(f"    匹配 JD: {jd_name}")
        
        # 读取简历
        resume_files = glob.glob(os.path.join(folder_path, '*.pdf')) + \
                       glob.glob(os.path.join(folder_path, '*.docx'))
        resume_files = [f for f in resume_files if not os.path.basename(f).startswith('~$')][:2]  # 演示：每个文件夹只处理 2 份
        
        for resume_file in resume_files:
            resume_name = os.path.basename(resume_file)
            resume_content = extract_text(resume_file)
            
            if not resume_content.strip():
                print(f"    ⚠️ 简历为空：{resume_name}")
                continue
            
            print(f"\n    处理简历：{resume_name}")
            
            # 为每条任职要求调用子 Agent
            for req_idx, requirement in enumerate(requirements[:2], 1):  # 演示：每条 JD 只分析前 2 条要求
                print(f"      提交任务：要求{req_idx}...")
                
                # 这里应该调用 sessions_spawn，但为了演示，我们只显示任务信息
                # 实际使用时取消注释下面的代码
                
                """
                from sessions_spawn import sessions_spawn
                
                prompt = f\"\"\"请分析以下简历与任职要求的匹配度：

简历内容：
{resume_content[:1500]}

任职要求：
{requirement}

岗位名称：{jd_name}

请返回 JSON 格式：
{{\"分析\": \"...\", \"匹配等级\": \"完全匹配\"}}

匹配等级选项：完全匹配、高度匹配、匹配、部分匹配、不匹配、无相关信息
\"\"\"
                
                result = sessions_spawn(
                    task=prompt,
                    runtime="subagent",
                    mode="run",
                    timeoutSeconds=60,
                    label=f"resume-{resume_name[:20]}"
                )
                
                tasks_submitted.append({
                    'child_key': result.get('childSessionKey'),
                    'resume': resume_name,
                    'jd': jd_name,
                    'requirement_idx': req_idx
                })
                """
                
                print(f"        ✅ 任务已提交（演示模式，未实际调用）")
    
    # 4. 等待结果（演示）
    print(f"\n[4] 等待结果...")
    print(f"  已提交 {len(tasks_submitted)} 个子 Agent 任务")
    print(f"  （演示模式，实际会等待所有任务完成并收集结果）")
    
    # 5. 生成报告
    print(f"\n[5] 生成 Excel 报告...")
    print(f"  输出路径：{OUTPUT_FOLDER}\\AI_Resume_All_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx")
    
    print(f"\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print(f"\n提示：")
    print(f"  - 实际使用时，取消注释 sessions_spawn 调用代码")
    print(f"  - 批量处理时建议设置 max_concurrent=3 控制并发数")
    print(f"  - 每份简历 × N 条任职要求 = N 个子 Agent 任务")

if __name__ == "__main__":
    process_resume_batch()
