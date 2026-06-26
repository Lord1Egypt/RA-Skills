# -*- coding: utf-8 -*-
"""
简历与 JD 智能匹配 - OpenClaw Skill 处理器
专用于 OpenClaw 环境，通过 sessions_spawn 调用子 Agent 进行批量分析

使用方式：
在 OpenClaw 中发送消息：/skill resume-jd-matcher
或直接调用：python skill_handler.py（需要 OpenClaw 环境）
"""

import os
import json
import yaml
import glob
import time
from datetime import datetime
from pathlib import Path

# 读取配置文件
def load_config():
    config_path = Path(__file__).parent.parent / 'references' / 'config_resume_match.yaml'
    if not config_path.exists():
        # 回退到工作区配置
        config_path = Path(r"C:\Users\Administrator\.openclaw\workspace\config_resume_match.yaml")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()

# 路径配置
JD_FOLDER = config['paths']['jd_folder']
JL_FOLDER = config['paths']['jl_folder']
OUTPUT_FOLDER = config['paths']['output_folder']

# 日志配置
LOG_FILE = None

def init_log_file():
    """初始化日志文件"""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    log_file = os.path.join(OUTPUT_FOLDER, f"resume_match_skill_{timestamp}.log")
    return log_file

def log_message(message, log_file=None):
    """写入日志"""
    global LOG_FILE
    if log_file:
        LOG_FILE = log_file
    if not LOG_FILE:
        LOG_FILE = init_log_file()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
    except:
        pass

# ========== 文件读取工具 ==========
def read_docx(file_path):
    """读取 Word 文件"""
    try:
        import docx
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        log_message(f"读取 Word 失败 {file_path}: {e}")
        return ""

def read_pdf(file_path):
    """读取 PDF 文件"""
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text() or ''
                if extracted.strip():
                    text.append(extracted)
        return '\n'.join(text)
    except Exception as e:
        log_message(f"PDF 解析失败 {file_path}: {e}")
        return ""

def extract_text_from_file(file_path):
    """根据文件类型提取文本"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return read_docx(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    return ""

# ========== JD 处理 ==========
def get_jd_content(jd_folder):
    """读取所有 JD 文件"""
    jd_files = glob.glob(os.path.join(jd_folder, '*.docx'))
    jd_contents = {}
    for jd_file in jd_files:
        if not os.path.basename(jd_file).startswith('~$'):
            jd_name = os.path.basename(jd_file).replace('.docx', '')
            jd_contents[jd_name] = extract_text_from_file(jd_file)
            log_message(f"读取 JD: {jd_name}")
    return jd_contents

def extract_requirements(jd_content):
    """从 JD 中提取任职要求"""
    lines = jd_content.split('\n')
    in_req = False
    requirements = []
    
    for line in lines:
        line = line.strip()
        if any(kw in line for kw in ['任职要求', '岗位要求', 'Qualifications', 'Requirements']):
            in_req = True
            continue
        if in_req and line:
            # 检查是否到下一个章节
            if any(kw in line for kw in ['岗位职责', '工作职责', '福利待遇', '投递邮箱']):
                break
            requirements.append(line)
    
    # 如果没有提取到，返回前 2000 字符
    if not requirements:
        return [jd_content[:2000]]
    
    return requirements

def find_matching_jd(folder_name, jd_contents):
    """根据文件夹名称匹配 JD"""
    folder_lower = folder_name.lower()
    
    # 简单匹配：文件夹名称包含 JD 名称中的关键词
    for jd_name, jd_content in jd_contents.items():
        jd_name_lower = jd_name.lower()
        # 检查关键词匹配
        if any(kw in folder_lower for kw in jd_name_lower.split() if len(kw) > 2):
            return [(jd_name, extract_requirements(jd_content))]
    
    # 尝试模糊匹配
    for jd_name, jd_content in jd_contents.items():
        if 'investment' in folder_lower and '投资' in jd_content:
            return [(jd_name, extract_requirements(jd_content))]
        if '合规' in folder_name and '合规' in jd_content:
            return [(jd_name, extract_requirements(jd_content))]
    
    return None

# ========== AI 分析（Subagent 模式） ==========
def analyze_resume_subagent(resume_text, job_requirement, position_name, resume_name=""):
    """
    调用子 Agent 分析简历匹配度
    
    这是 OpenClaw Skill 专用版本，通过 sessions_spawn 工具调用
    """
    prompt = f"""请分析以下简历与该条任职要求的匹配程度：

## 简历内容：
{resume_text}

## 任职要求：
{job_requirement}

## 岗位名称：{position_name}

请针对这条任职要求进行分析，直接返回 JSON 格式：
{{"分析": "针对该条任职要求的匹配分析", "匹配等级": "完全匹配"}}

重要要求：
1. **请统一使用中文返回分析结果**
2. "分析"字段：只针对该条任职要求进行匹配分析，不要分析其他维度
3. "匹配等级"必须从以下选项中选择：完全匹配、高度匹配、匹配、部分匹配、不匹配、无相关信息
4. 即使简历或任职要求中有英文内容，分析内容也必须用中文
5. 如果简历中有英文内容（如英文公司名、英文职位等），请在分析中保留原文并附上中文说明
"""
    
    # 在 OpenClaw 环境中，这会通过工具调用执行
    # 返回格式：{"childSessionKey": "...", "runId": "..."}
    return {
        'task': prompt,
        'label': f"resume-{resume_name[:30] if resume_name else 'analysis'}"
    }

# ========== 批量处理 ==========
def process_resumes_batch(resume_folder, jd_requirements, max_concurrent=3):
    """
    批量处理简历文件夹
    
    Args:
        resume_folder: 简历文件夹路径
        jd_requirements: JD 要求列表 [(岗位名，要求列表), ...]
        max_concurrent: 最大并发子 Agent 数量
    """
    from sessions_spawn import sessions_spawn
    from subagents import subagents
    from sessions_history import sessions_history
    
    resume_files = glob.glob(os.path.join(resume_folder, '*.pdf')) + \
                   glob.glob(os.path.join(resume_folder, '*.docx'))
    resume_files = [f for f in resume_files if not os.path.basename(f).startswith('~$')]
    
    if not resume_files:
        log_message(f"  简历文件夹为空：{resume_folder}")
        return []
    
    log_message(f"  找到 {len(resume_files)} 份简历")
    
    # 存储所有子 Agent 调用
    pending_tasks = []
    results = []
    
    for resume_file in resume_files:
        resume_name = os.path.basename(resume_file)
        resume_key = resume_name.replace('.docx', '').replace('.pdf', '').strip()
        resume_content = extract_text_from_file(resume_file)
        
        if not resume_content.strip():
            log_message(f"  跳过空简历：{resume_name}")
            continue
        
        log_message(f"  处理简历：{resume_name}")
        
        # 为每份简历的每条任职要求创建子 Agent 任务
        for (position_name, req_list) in jd_requirements:
            for req_idx, requirement in enumerate(req_list):
                # 创建分析任务
                task_data = analyze_resume_subagent(
                    resume_content, 
                    requirement, 
                    position_name,
                    resume_key
                )
                
                # 调用子 Agent
                spawn_result = sessions_spawn(
                    task=task_data['task'],
                    runtime="subagent",
                    mode="run",
                    timeoutSeconds=60,
                    label=task_data['label']
                )
                
                pending_tasks.append({
                    'child_key': spawn_result.get('childSessionKey'),
                    'resume_name': resume_key,
                    'position': position_name,
                    'requirement': requirement,
                    'req_idx': req_idx + 1
                })
                
                log_message(f"    已提交任务：{position_name} - 要求{req_idx + 1}")
                
                # 控制并发数
                if len(pending_tasks) >= max_concurrent:
                    # 等待一批完成
                    batch_results = wait_for_batch(pending_tasks, max_concurrent)
                    results.extend(batch_results)
                    pending_tasks = [t for t in pending_tasks if t.get('status') != 'done']
    
    # 等待剩余任务完成
    if pending_tasks:
        log_message(f"等待剩余 {len(pending_tasks)} 个任务完成...")
        batch_results = wait_for_batch(pending_tasks, len(pending_tasks))
        results.extend(batch_results)
    
    return results

def wait_for_batch(tasks, max_wait_seconds=60):
    """
    等待一批子 Agent 任务完成
    
    Returns:
        list: 完成的任务结果
    """
    from subagents import subagents
    from sessions_history import sessions_history
    
    completed = []
    start_time = time.time()
    
    while time.time() - start_time < max_wait_seconds:
        # 检查所有任务状态
        agents = subagents(action="list")
        recent = {a['sessionKey']: a for a in agents.get('recent', [])}
        
        for task in tasks:
            if task.get('status') == 'done':
                continue
            
            child_key = task.get('child_key')
            if child_key in recent:
                agent_info = recent[child_key]
                if agent_info.get('status') == 'done':
                    # 获取结果
                    history = sessions_history(sessionKey=child_key, limit=10, includeTools=False)
                    if history.get('messages'):
                        last_msg = history['messages'][-1]
                        if last_msg.get('role') == 'assistant':
                            content = last_msg.get('content', [])
                            for item in content:
                                if item.get('type') == 'text':
                                    task['result'] = item.get('text', '')
                                    task['status'] = 'done'
                                    task['match_level'] = extract_match_level(item.get('text', ''))
                                    completed.append(task)
                                    log_message(f"    ✅ 完成：{task['resume_name']} - {task['position']} - {task['match_level']}")
                                    break
        
        # 检查是否全部完成
        all_done = all(t.get('status') == 'done' for t in tasks)
        if all_done:
            break
        
        time.sleep(2)
    
    return completed

def extract_match_level(ai_response):
    """从 AI 响应中提取匹配等级"""
    levels = ['完全匹配', '高度匹配', '匹配', '部分匹配', '不匹配', '无相关信息']
    for level in levels:
        if level in ai_response:
            return level
    return '无相关信息'

# ========== 主函数 ==========
def main():
    """Skill 主入口"""
    log_message("=" * 60)
    log_message("简历与 JD 智能匹配 - OpenClaw Skill 启动")
    log_message("=" * 60)
    
    # 读取 JD
    log_message("\n[1] 读取 JD 文件...")
    jd_contents = get_jd_content(JD_FOLDER)
    log_message(f"  找到 {len(jd_contents)} 个 JD 文件")
    
    # 扫描简历目录
    log_message("\n[2] 扫描简历目录...")
    jl_folders = [f for f in os.listdir(JL_FOLDER) if os.path.isdir(os.path.join(JL_FOLDER, f))]
    log_message(f"  找到 {len(jl_folders)} 个简历文件夹")
    
    all_results = []
    
    # 处理每个文件夹
    for folder_name in jl_folders:
        folder_path = os.path.join(JL_FOLDER, folder_name)
        log_message(f"\n[3] 处理文件夹：{folder_name}")
        
        # 匹配 JD
        jd_requirements = find_matching_jd(folder_name, jd_contents)
        if not jd_requirements:
            log_message(f"  ⚠️ 未找到匹配的 JD，跳过")
            continue
        
        log_message(f"  匹配岗位：{[item[0] for item in jd_requirements]}")
        
        # 批量处理简历
        results = process_resumes_batch(folder_path, jd_requirements, max_concurrent=3)
        all_results.extend(results)
    
    # 总结
    log_message("\n" + "=" * 60)
    log_message(f"处理完成！共分析 {len(all_results)} 条任职要求")
    log_message("=" * 60)
    
    return all_results

if __name__ == "__main__":
    main()
