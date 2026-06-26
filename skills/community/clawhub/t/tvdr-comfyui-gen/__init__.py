"""
ComfyUI Generator Skill
提供可靠的 ComfyUI 图像生成功能，内置错误预防机制
"""

import json
import urllib.request
import urllib.error
import os
import time
import shutil
from pathlib import Path

# 配置
COMFYUI_SERVER = os.environ.get("COMFYUI_SERVER", "http://192.168.18.15:8188")
DEFAULT_WORKFLOW = "/mnt/share2win/comfyui_work/comfyui_workflows/image_z_image_turbo（可用 写实）.json"
OUTPUT_DIR = "/mnt/share2win/comfyui_work/comfyui_output"


def test_connection():
    """测试 ComfyUI 连接"""
    try:
        response = urllib.request.urlopen(f"{COMFYUI_SERVER}/system_stats", timeout=5)
        data = json.loads(response.read().decode())
        return True, data
    except Exception as e:
        return False, str(e)


def validate_workflow(workflow_path):
    """验证工作流文件"""
    if not os.path.exists(workflow_path):
        return False, f"工作流文件不存在: {workflow_path}"

    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except Exception as e:
        return False, f"工作流文件格式错误: {e}"

    # 检查必需节点
    has_clip_node = False
    has_save_node = False

    for node_id, node in workflow.items():
        if node.get('class_type') == 'CLIPTextEncode':
            has_clip_node = True
        elif node.get('class_type') == 'SaveImage':
            has_save_node = True

    if not has_clip_node:
        return False, "工作流缺少 CLIPTextEncode 节点"

    if not has_save_node:
        return False, "工作流缺少 SaveImage 节点"

    return True, workflow


def modify_prompt(workflow, new_prompt, node_id=None, negative_prompt_node_id=None, filename_prefix=None):
    """
    修改工作流提示词

    Args:
        workflow: 工作流字典
        new_prompt: 新提示词
        node_id: 指定修改哪个节点（可选，默认自动查找）
        negative_prompt_node_id: 负面提示词节点ID，会被跳过
        filename_prefix: 输出文件名前缀

    Returns:
        (success, message)
    """
    modified = False
    modified_node_id = None

    if node_id and node_id in workflow:
        # 指定节点修改
        node = workflow[node_id]
        if node.get('class_type') == 'CLIPTextEncode':
            if 'text' in node.get('inputs', {}):
                node['inputs']['text'] = new_prompt
                modified = True
                modified_node_id = node_id
            else:
                return False, f"节点 {node_id} 没有 'text' 字段"
        else:
            return False, f"节点 {node_id} 不是 CLIPTextEncode 类型"
    else:
        # 自动查找并修改
        for node_id, node in workflow.items():
            if node.get('class_type') == 'CLIPTextEncode':
                # 跳过负面提示词节点
                if negative_prompt_node_id and node_id == negative_prompt_node_id:
                    continue

                if 'text' in node.get('inputs', {}):
                    # 检查是否是负面提示词/风格节点
                    current_text = node['inputs']['text']
                    if any(keyword in current_text for keyword in ['负面', 'negative', '风格', 'style', '插画风']):
                        continue

                    node['inputs']['text'] = new_prompt
                    modified = True
                    modified_node_id = node_id
                    break

    if not modified:
        return False, "未找到可修改的 CLIPTextEncode 节点"

    # 修改输出文件名前缀（不在这里 return，继续执行）
    if filename_prefix:
        for node_id, node in workflow.items():
            if node.get('class_type') == 'SaveImage':
                if 'filename_prefix' in node.get('inputs', {}):
                    node['inputs']['filename_prefix'] = filename_prefix
                    return True, f"已修改节点 {modified_node_id} 的提示词和文件前缀: {filename_prefix}"

    return True, f"已修改节点 {modified_node_id} 的提示词"


def submit_workflow(workflow, timeout=300):
    """
    提交工作流到 ComfyUI

    Args:
        workflow: 工作流字典
        timeout: 超时时间（秒）

    Returns:
        (success, prompt_id, error)
    """
    prompt = {"prompt": workflow}

    try:
        data = json.dumps(prompt).encode('utf-8')
        req = urllib.request.Request(
            f"{COMFYUI_SERVER}/prompt",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        prompt_id = result.get('prompt_id')
        return True, prompt_id, None

    except Exception as e:
        return False, None, str(e)


def wait_for_completion(prompt_id, timeout=300, check_interval=2):
    """
    等待生成完成

    Args:
        prompt_id: Prompt ID
        timeout: 超时时间（秒）
        check_interval: 检查间隔（秒）

    Returns:
        (success, duration_seconds, error)
    """
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            return False, elapsed, f"等待超时（{timeout}秒）"

        time.sleep(check_interval)

        try:
            req = urllib.request.Request(f"{COMFYUI_SERVER}/history/{prompt_id}")
            response = urllib.request.urlopen(req)
            history = json.loads(response.read().decode())

            if prompt_id in history:
                if 'outputs' in history[prompt_id]:
                    return True, elapsed, None

        except Exception as e:
            # 忽略临时网络错误，继续等待
            pass


def find_generated_file(filename_prefix):
    """
    查找生成的文件

    Args:
        filename_prefix: 文件名前缀

    Returns:
        (success, file_path, file_size_mb)
    """
    if not os.path.exists(OUTPUT_DIR):
        return False, None, 0

    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(filename_prefix)]

    if not files:
        return False, None, 0

    # 取第一个文件
    file_path = os.path.join(OUTPUT_DIR, files[0])
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    return True, file_path, file_size_mb


def generate(
    prompt,
    workflow_path=None,
    output_path=None,
    filename_prefix=None,
    node_id=None,
    negative_prompt_node_id=None,
    timeout=300,
    retry=2
):
    """
    生成图片

    Args:
        prompt: 提示词
        workflow_path: 工作流路径（默认使用 DEFAULT_WORKFLOW）
        output_path: 输出文件路径（可选，如果不指定则不复制）
        filename_prefix: 输出文件名前缀
        node_id: 指定修改哪个节点
        negative_prompt_node_id: 负面提示词节点ID
        timeout: 超时时间（秒）
        retry: 重试次数

    Returns:
        {
            'success': True/False,
            'file_path': '/path/to/file' (成功时),
            'file_size_mb': 2.47 (成功时),
            'prompt_id': 'uuid' (成功时),
            'duration_seconds': 45 (成功时),
            'error': 'error message' (失败时)
        }
    """
    # 使用默认工作流
    if workflow_path is None:
        workflow_path = DEFAULT_WORKFLOW

    # 验证工作流
    valid, result = validate_workflow(workflow_path)
    if not valid:
        return {'success': False, 'error': result}

    workflow = result

    # 修改提示词
    valid, message = modify_prompt(
        workflow,
        prompt,
        node_id=node_id,
        negative_prompt_node_id=negative_prompt_node_id,
        filename_prefix=filename_prefix
    )
    if not valid:
        return {'success': False, 'error': message}

    # 提交工作流（带重试）
    for attempt in range(retry + 1):
        success, prompt_id, error = submit_workflow(workflow, timeout)
        if success:
            break

        if attempt < retry:
            time.sleep(2)  # 重试前等待
        else:
            return {'success': False, 'error': f"提交失败（重试{retry}次）: {error}"}

    # 等待完成
    success, duration, error = wait_for_completion(prompt_id, timeout)
    if not success:
        return {'success': False, 'error': error}

    # 查找生成的文件
    if filename_prefix:
        success, file_path, file_size_mb = find_generated_file(filename_prefix)
    else:
        # 尝试从工作流中获取文件前缀
        prefix = None
        for node in workflow.values():
            if node.get('class_type') == 'SaveImage':
                prefix = node.get('inputs', {}).get('filename_prefix', 'output')
                break

        success, file_path, file_size_mb = find_generated_file(prefix)

    if not success:
        return {'success': False, 'error': '未找到生成的文件'}

    # 复制到目标路径
    if output_path:
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            shutil.copy2(file_path, output_path)
            file_path = output_path
        except Exception as e:
            return {'success': False, 'error': f"复制文件失败: {e}"}

    return {
        'success': True,
        'file_path': file_path,
        'file_size_mb': file_size_mb,
        'prompt_id': prompt_id,
        'duration_seconds': duration
    }


def batch_generate(prompts, output_dir, workflow_path=None, filename_prefix=None):
    """
    批量生成图片

    Args:
        prompts: 提示词列表
        output_dir: 输出目录
        workflow_path: 工作流路径
        filename_prefix: 文件名前缀

    Returns:
        {
            'success': True/False,
            'results': [生成结果列表],
            'failed_count': 失败数量
        }
    """
    results = []
    failed_count = 0

    for i, prompt in enumerate(prompts):
        output_path = os.path.join(output_dir, f"{filename_prefix}_{i:05d}.png")

        result = generate(
            prompt=prompt,
            workflow_path=workflow_path,
            output_path=output_path,
            filename_prefix=f"{filename_prefix}_{i:05d}"
        )

        results.append(result)

        if not result['success']:
            failed_count += 1

    return {
        'success': failed_count == 0,
        'results': results,
        'failed_count': failed_count
    }
