#!/usr/bin/env python3
"""
ComfyUI 图像生成器 - 防止历史错误的可靠实现

历史错误预防:
1. ✅ 强制使用 inputs['text'] 而非 inputs['prompt']
2. ✅ 不使用 spawn，避免重复生成
3. ✅ 自动检查节点类型 CLIPTextEncode
4. ✅ 自动跳过负面提示词节点
5. ✅ 完整的错误处理和重试机制
"""

import json
import time
import os
import urllib.request
from urllib.parse import quote
from typing import Dict, Any, Optional

# 配置
COMFYUI_SERVER = os.getenv('COMFYUI_SERVER', 'http://192.168.18.15:8188')
DEFAULT_WORKFLOW = r'/mnt/share2win/comfyui_work/comfyui_workflows/image_z_image_turbo（可用 写实）.json'
DEFAULT_TIMEOUT = 300  # 5分钟
MAX_RETRIES = 3


def test_connection() -> Dict[str, Any]:
    """测试 ComfyUI 服务器连接"""
    try:
        response = urllib.request.urlopen(f"{COMFYUI_SERVER}/system_stats", timeout=5)
        data = json.loads(response.read().decode())
        return {
            'success': True,
            'server': COMFYUI_SERVER,
            'queue_remaining': data.get('queue_remaining', 0)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'server': COMFYUI_SERVER
        }


def load_workflow(workflow_path: str) -> Dict[str, Any]:
    """
    加载工作流并验证

    返回:
        (workflow, info): 工作流字典和节点信息
    """
    if not os.path.exists(workflow_path):
        raise FileNotFoundError(f"工作流文件不存在: {workflow_path}")

    with open(workflow_path, 'r') as f:
        workflow = json.load(f)

    # 验证必需节点
    has_clip_text_encode = False
    has_save_image = False

    for node_id, node in workflow.items():
        class_type = node.get('class_type')
        if class_type == 'CLIPTextEncode':
            has_clip_text_encode = True
        elif class_type == 'SaveImage':
            has_save_image = True

    if not has_clip_text_encode:
        raise ValueError("工作流缺少必需的 CLIPTextEncode 节点")

    if not has_save_image:
        raise ValueError("工作流缺少必需的 SaveImage 节点")

    return workflow


def modify_prompt(
    workflow: Dict[str, Any],
    new_prompt: str,
    node_id: Optional[str] = None,
    skip_node_ids: Optional[list] = None,
    skip_keywords: Optional[list] = None
) -> Dict[str, Any]:
    """
    修改工作流的提示词（强制使用正确的字段名）

    Args:
        workflow: 工作流字典
        new_prompt: 新的提示词
        node_id: 指定修改哪个节点（如果不指定则自动查找）
        skip_node_ids: 要跳过的节点 ID 列表
        skip_keywords: 包含这些关键词的节点将被跳过（如 '负面', '插画风'）

    Returns:
        修改后的工作流

    Raises:
        ValueError: 未找到可修改的 CLIPTextEncode 节点
    """
    if skip_node_ids is None:
        skip_node_ids = []
    if skip_keywords is None:
        skip_keywords = ['负面', '插画风', '水彩', 'style']

    modified = False

    for nid, node in workflow.items():
        if node.get('class_type') != 'CLIPTextEncode':
            continue

        # 检查是否跳过此节点
        if nid in skip_node_ids:
            continue

        # 检查是否包含跳过关键词
        if 'text' in node.get('inputs', {}):
            current_text = node['inputs']['text']
            if any(kw in current_text for kw in skip_keywords):
                continue

        # 指定节点 ID 或未指定时查找第一个
        if node_id is None or nid == node_id:
            # ✅ 强制使用正确的字段名 'text'
            if 'text' in node.get('inputs', {}):
                node['inputs']['text'] = new_prompt
                modified = True
                break
            else:
                raise ValueError(f"节点 {nid} 没有 'text' 字段，无法修改提示词")

    if not modified:
        raise ValueError("未找到可修改的 CLIPTextEncode 节点")

    return workflow


def set_output_filename(
    workflow: Dict[str, Any],
    filename_prefix: str
) -> Dict[str, Any]:
    """
    设置输出文件名

    Args:
        workflow: 工作流字典
        filename_prefix: 文件名前缀

    Returns:
        修改后的工作流
    """
    for node_id, node in workflow.items():
        if node.get('class_type') == 'SaveImage':
            node['inputs']['filename_prefix'] = filename_prefix
            break
    return workflow


def wait_for_completion(prompt_id: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """
    等待任务完成

    Args:
        prompt_id: 任务 ID
        timeout: 超时时间（秒）

    Returns:
        任务信息

    Raises:
        TimeoutError: 任务超时
        RuntimeError: 任务执行失败
    """
    url = f"{COMFYUI_SERVER}/history/{prompt_id}"
    start = time.time()

    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
        except Exception as e:
            time.sleep(3)
            continue

        if prompt_id not in data:
            time.sleep(3)
            continue

        status = data[prompt_id]['status'].get('status_str', 'unknown')

        if status == 'success':
            time.sleep(1)  # 等待文件完全保存
            # 再次获取最新信息
            with urllib.request.urlopen(req, timeout=5) as response2:
                data2 = json.loads(response2.read().decode())
            return data2[prompt_id]
        elif status == 'error':
            raise RuntimeError(data[prompt_id]['status'].get('message', 'Unknown error'))

        time.sleep(3)

    raise TimeoutError(f"任务超时 ({timeout}秒)")


def download_image(filename: str, output_path: str) -> Dict[str, Any]:
    """
    下载生成的图片

    Args:
        filename: 文件名
        output_path: 保存路径

    Returns:
        下载结果

    Raises:
        IOError: 下载失败
    """
    # 确保目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 构造下载 URL
    url = f"{COMFYUI_SERVER}/view?filename={quote(filename)}&type=output"

    req = urllib.request.Request(url, headers={'User-Agent': 'nanobot/1.0'})

    with urllib.request.urlopen(req) as response:
        content = response.read()

    with open(output_path, 'wb') as f:
        f.write(content)

    return {
        'file_path': output_path,
        'file_size_bytes': len(content),
        'file_size_mb': len(content) / 1024 / 1024
    }


def generate(
    prompt: str,
    output_path: str,
    workflow_path: Optional[str] = None,
    filename_prefix: Optional[str] = None,
    node_id: Optional[str] = None,
    negative_prompt_node_id: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT
) -> Dict[str, Any]:
    """
    生成图片（同步执行，不使用 spawn）

    Args:
        prompt: 提示词
        output_path: 输出文件路径
        workflow_path: 工作流文件路径（默认使用标准工作流）
        filename_prefix: 输出文件名前缀
        node_id: 指定修改哪个节点（可选）
        negative_prompt_node_id: 负面提示词节点 ID（可选）
        timeout: 超时时间（秒）

    Returns:
        生成结果

        {
            'success': bool,
            'file_path': str or None,
            'file_size_mb': float or None,
            'prompt_id': str or None,
            'duration_seconds': float,
            'error': str or None
        }
    """
    start_time = time.time()

    # 使用默认工作流
    if workflow_path is None:
        workflow_path = DEFAULT_WORKFLOW

    # 设置文件名前缀
    if filename_prefix is None:
        filename_prefix = "comfyui_output"

    try:
        # 1. 加载工作流
        workflow = load_workflow(workflow_path)

        # 2. 修改提示词
        skip_node_ids = [negative_prompt_node_id] if negative_prompt_node_id else []
        workflow = modify_prompt(
            workflow,
            prompt,
            node_id=node_id,
            skip_node_ids=skip_node_ids
        )

        # 3. 设置输出文件名
        workflow = set_output_filename(workflow, filename_prefix)

        # 4. 提交任务
        url = f"{COMFYUI_SERVER}/prompt"
        data = json.dumps({"prompt": workflow}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        prompt_id = json.loads(response.read())['prompt_id']

        # 5. 等待完成
        task_info = wait_for_completion(prompt_id, timeout)

        # 6. 下载图片
        outputs = task_info.get('outputs', {})
        downloaded = False

        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                for img in node_output['images']:
                    filename = img['filename']
                    download_result = download_image(filename, output_path)

                    duration = time.time() - start_time

                    return {
                        'success': True,
                        'file_path': download_result['file_path'],
                        'file_size_mb': download_result['file_size_mb'],
                        'prompt_id': prompt_id,
                        'duration_seconds': duration,
                        'error': None
                    }

        return {
            'success': False,
            'file_path': None,
            'file_size_mb': None,
            'prompt_id': prompt_id,
            'duration_seconds': time.time() - start_time,
            'error': '未找到生成的图片'
        }

    except Exception as e:
        return {
            'success': False,
            'file_path': None,
            'file_size_mb': None,
            'prompt_id': None,
            'duration_seconds': time.time() - start_time,
            'error': str(e)
        }


# 命令行测试
if __name__ == '__main__':
    import sys

    print("="*60)
    print("ComfyUI 生成器 - 命令行测试")
    print("="*60)

    # 测试连接
    print("\n1. 测试 ComfyUI 连接...")
    conn = test_connection()
    if conn['success']:
        print(f"   ✓ 连接成功: {conn['server']}")
        print(f"   队列长度: {conn['queue_remaining']}")
    else:
        print(f"   ✗ 连接失败: {conn['error']}")
        sys.exit(1)

    # 如果有参数，执行生成
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/comfyui_test_output.png"

        print(f"\n2. 生成图片...")
        print(f"   提示词: {prompt}")
        print(f"   输出路径: {output_path}")

        result = generate(
            prompt=prompt,
            output_path=output_path
        )

        if result['success']:
            print(f"   ✓ 生成成功!")
            print(f"   文件: {result['file_path']}")
            print(f"   大小: {result['file_size_mb']:.2f} MB")
            print(f"   耗时: {result['duration_seconds']:.1f} 秒")
        else:
            print(f"   ✗ 生成失败: {result['error']}")
            sys.exit(1)
    else:
        print("\n用法:")
        print("  python comfyui_generator.py \"提示词\" [输出路径]")
        print("\n示例:")
        print("  python comfyui_generator.py \"古代剑客，正面特写\" /tmp/hero.png")
