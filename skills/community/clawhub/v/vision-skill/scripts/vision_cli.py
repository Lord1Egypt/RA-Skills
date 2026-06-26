#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vision Skill CLI
主入口脚本，用于接收命令并启动后台任务
"""

import sys
import os
import argparse
import subprocess
import json
import time
import requests
from task_utils import create_task, get_task, repair_json

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKER_SCRIPT = os.path.join(SCRIPT_DIR, 'worker.py')

# 预置生成风格 (Generation Presets)
STYLE_PRESETS = {
    "ppt": "Flat vector illustration, minimalist style, suitable for business presentation, white background, high quality",
    "business_flat": "Business flat illustration, clean geometric shapes, corporate palette, 16:9 composition, slide-friendly",
    "id_photo": "Professional ID photo, frontal portrait, ensuring the face is centered and fully visible, neutral expression, soft and even studio lighting, high sharpness, skin texture details, plain background (white or blue), formal attire",
    "cartoon": "Disney/Pixar style 3D cartoon, vibrant colors, expressive characters, cute, high detail",
    "tech_isometric": "Isometric tech illustration, modern SaaS style, soft gradients, clean layout, presentation-ready",
    "hand_drawn": "Hand-drawn sketch style, simple lines, warm tone, suitable for conceptual explanation",
    "icon": "3D icon, clay morphism, soft lighting, rounded corners, high resolution, suitable for app icon",
    "photo": "Photorealistic, 8k resolution, cinematic lighting, highly detailed, realistic texture",
    "anime": "Japanese anime style, cel shading, clean lines, vibrant colors, detailed background",
    "sketch": "Pencil sketch, black and white, artistic, rough lines, hand-drawn style"
}

# 预置识别格式 (Recognition Formats)
FORMAT_PRESETS = {
    "business_card": "请识别名片内容，并输出 JSON，字段至少包含：姓名、职位、公司、手机、电话、邮箱、地址、网站、其他信息。若某字段不存在请返回空字符串。",
    "table": "请识别图片中的表格内容，并严格以 Markdown 表格格式输出，不要包含其他解释性文字。",
    "json": "请提取图片中的关键实体信息（如姓名、日期、金额、地址等），并以 JSON 格式结构化输出。",
    "key_value": "请提取图片中的关键信息，并以“字段: 值”的键值对格式输出。",
    "markdown_note": "请将图片内容整理为 Markdown 笔记，使用清晰的标题与要点列表。",
    "qa_pairs": "请基于图片内容生成问答对，格式为 Q: ... A: ...，不少于5组。",
    "invoice": "请识别发票内容，输出 JSON，字段至少包含：发票号码、日期、购方、销方、金额、税额、价税合计。",
    "contract": "请识别合同关键信息，输出 JSON，字段至少包含：合同名称、甲方、乙方、签署日期、生效日期、终止日期、金额、关键条款。",
    "form": "请识别表单内容，输出 JSON，按字段名映射到字段值。",
    "slide": "请识别幻灯片内容，输出 Markdown，包含标题、要点、图示说明。",
    "whiteboard": "请识别白板内容，输出结构化会议纪要：议题、讨论点、结论、行动项。",
    "code": "请识别图片中的代码内容，直接输出代码块，不要包含其他解释性文字。",
    "ocr": "请提取图片中所有可见的文字，保持原有排版格式，不要遗漏。",
    "analysis": "请详细分析图片内容，包括场景、人物、物体、颜色、构图以及可能的情感色彩。"
}

def run_worker(task_id):
    """启动后台工作进程（带简单的最大并发限制）"""
    # 检查当前正在运行的 worker 数量
    # 通过 ps 命令检查 worker.py 的进程数
    try:
        # grep -v grep 排除自身，wc -l 统计行数
        # 注意：这只是一个简易的软限制，不够精确但能防止瞬间炸机
        cmd = "ps -ef | grep worker.py | grep -v grep | wc -l"
        result = subprocess.check_output(cmd, shell=True)
        count = int(result.strip())
        
        MAX_CONCURRENT_WORKERS = 5
        if count >= MAX_CONCURRENT_WORKERS:
            # 如果并发满了，稍微等一下再试（简易排队）
            # 但由于 CLI 是短连接，这里只能直接启动并祈祷 OS 调度，或者简单的 sleep
            # 更好的做法是引入真正的队列（如 Redis/SQLite），但为了保持无依赖，
            # 我们这里做一个简单的退避策略：如果太忙，就 warn 一下用户
            print(f"Warning: 当前并发任务较多 ({count}), 任务启动可能会有延迟...")
    except:
        pass

    env = os.environ.copy()
    env['PYTHONPATH'] = SCRIPT_DIR + os.pathsep + env.get('PYTHONPATH', '')
    
    subprocess.Popen(
        [sys.executable, WORKER_SCRIPT, task_id],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True
    )

def wait_for_task(task_id, timeout=300):
    """同步等待任务完成"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        task = get_task(task_id)
        if not task:
            return {"status": "error", "error": "任务不存在"}
            
        status = task.get("status")
        if status in ["completed", "failed"]:
            return task
            
        time.sleep(2)
    return {"status": "timeout", "error": "任务执行超时"}

def extract_recognition_text(rec_res):
    if isinstance(rec_res, dict) and "choices" in rec_res and rec_res["choices"]:
        return rec_res["choices"][0]["message"]["content"]
    return str(rec_res)

def save_result(result, output_path):
    """保存结果到文件"""
    try:
        if "generation_result" in result:
            gen_res = result.get("generation_result", {})
            if isinstance(gen_res, dict) and "data" in gen_res:
                urls = [item["url"] for item in gen_res["data"]]
            elif isinstance(gen_res, dict) and "url" in gen_res:
                 urls = [gen_res["url"]]
            elif isinstance(gen_res, list):
                urls = [item.get("url") for item in gen_res if isinstance(item, dict)]
            else:
                 urls = []
            if not urls and isinstance(gen_res, dict) and "data" in gen_res:
                 urls = [item.get("url") for item in gen_res["data"]]
            if urls:
                if len(urls) == 1:
                    download_file(urls[0], output_path)
                    print(f"图片已保存至: {output_path}")
                else:
                    base, ext = os.path.splitext(output_path)
                    for i, url in enumerate(urls):
                        path = f"{base}_{i+1}{ext}"
                        download_file(url, path)
                        print(f"图片已保存至: {path}")
            else:
                print("未找到可下载的图片 URL")
        elif "recognition_result" in result:
            rec_res = result.get("recognition_result", {})
            content = extract_recognition_text(rec_res)
            
            # 尝试修复 JSON
            if content.strip().startswith('{') or "json" in output_path.lower():
                 repaired_json = repair_json(content)
                 if repaired_json and "error" not in repaired_json:
                     content = json.dumps(repaired_json, ensure_ascii=False, indent=2)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"识别结果已保存至: {output_path}")
        elif "items" in result:
            items = result.get("items", [])
            payload = []
            for item in items:
                if item.get("status") == "completed":
                    raw_content = extract_recognition_text(item.get("recognition_result", {}))
                    # 尝试修复 JSON
                    repaired_content = repair_json(raw_content)
                    final_content = repaired_content if "error" not in repaired_content else raw_content
                    
                    payload.append({
                        "input": item.get("input"),
                        "image_url": item.get("image_url"),
                        "content": final_content
                    })
                else:
                    payload.append({
                        "input": item.get("input"),
                        "status": "failed",
                        "error": item.get("error")
                    })
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            print(f"批量识别结果已保存至: {output_path}")

    except Exception as e:
        print(f"保存结果失败: {e}")

def download_file(url, path):
    """下载文件"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

def handle_recognize(args):
    """处理识别命令"""
    for image_path in args.image_path:
        if not os.path.exists(image_path) and not image_path.startswith(('http://', 'https://')):
            print(json.dumps({"error": f"图片文件不存在或无效URL: {image_path}"}))
            return

    prompt = args.prompt
    if args.format and args.format in FORMAT_PRESETS:
        preset_prompt = FORMAT_PRESETS[args.format]
        prompt = f"{preset_prompt}\n\n补充要求: {prompt}" if prompt != "你看见了什么？" else preset_prompt

    params = {
        "prompt": prompt,
        "quality": args.quality,
        "retry_count": args.retry
    }
    if len(args.image_path) == 1:
        params["image"] = args.image_path[0]
    else:
        params["images"] = args.image_path
    
    task_id = create_task("vision_recognition", params)
    run_worker(task_id)
    
    if args.wait:
        print(f"任务已提交 (ID: {task_id})，正在等待结果...")
        task = wait_for_task(task_id, timeout=args.timeout)
        if task["status"] == "completed":
            print(json.dumps(task["result"], ensure_ascii=False, indent=2))
            if args.output:
                save_result(task["result"], args.output)
        else:
            print(json.dumps(task, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            "task_id": task_id,
            "status": "pending",
            "message": "视觉识别任务已提交",
            "input_count": len(args.image_path)
        }, ensure_ascii=False))

def handle_generate(args):
    """处理生成命令"""
    prompt = args.prompt
    if args.style and args.style in STYLE_PRESETS:
        style_prompt = STYLE_PRESETS[args.style]
        prompt = f"{style_prompt}. Content: {prompt}"

    params = {
        "prompt": prompt,
        "ref_images": args.ref_images,
        "sequential_options": None,
        "quality": args.quality,
        "retry_count": args.retry
    }
    
    if args.seq_count:
        params["sequential_options"] = {"max_images": args.seq_count}
        
    task_id = create_task("image_generation", params)
    run_worker(task_id)
    
    if args.wait:
        print(f"任务已提交 (ID: {task_id})，正在等待结果...")
        task = wait_for_task(task_id, timeout=args.timeout)
        if task["status"] == "completed":
            print(json.dumps(task["result"], ensure_ascii=False, indent=2))
            if args.output:
                save_result(task["result"], args.output)
        else:
            print(json.dumps(task, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            "task_id": task_id,
            "status": "pending",
            "message": "图像生成任务已提交"
        }, ensure_ascii=False))

def handle_status(args):
    """处理状态查询命令"""
    task = get_task(args.task_id)
    if not task:
        print(json.dumps({"error": "任务不存在"}, ensure_ascii=False))
        return
    print(json.dumps(task, ensure_ascii=False, indent=2))
    
    if args.output and task.get("status") == "completed":
        save_result(task["result"], args.output)

def main():
    parser = argparse.ArgumentParser(description="Vision Skill CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Recognize command
    recognize_parser = subparsers.add_parser("recognize", help="Perform vision recognition")
    recognize_parser.add_argument("image_path", nargs="+", help="Path or URL to the image, supports multi-image batch input")
    recognize_parser.add_argument("--prompt", default="你看见了什么？", help="Prompt for recognition")
    recognize_parser.add_argument("--format", choices=FORMAT_PRESETS.keys(), help="Preset output format")
    recognize_parser.add_argument("--quality", choices=["fast", "balanced", "high"], default="balanced", help="Quality mode")
    recognize_parser.add_argument("--retry", type=int, default=2, help="Retry count on API failures")
    recognize_parser.add_argument("--wait", action="store_true", help="Wait for task completion")
    recognize_parser.add_argument("--timeout", type=int, default=300, help="Wait timeout in seconds")
    recognize_parser.add_argument("--output", help="Save result to file")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate images")
    generate_parser.add_argument("prompt", help="Prompt for generation")
    generate_parser.add_argument("--ref", dest="ref_images", nargs="+", help="Reference image paths or URLs")
    generate_parser.add_argument("--seq", dest="seq_count", type=int, help="Number of sequential images to generate")
    generate_parser.add_argument("--style", choices=STYLE_PRESETS.keys(), help="Preset generation style")
    generate_parser.add_argument("--quality", choices=["fast", "balanced", "high"], default="balanced", help="Quality mode")
    generate_parser.add_argument("--retry", type=int, default=2, help="Retry count on API failures")
    generate_parser.add_argument("--wait", action="store_true", help="Wait for task completion")
    generate_parser.add_argument("--timeout", type=int, default=300, help="Wait timeout in seconds")
    generate_parser.add_argument("--output", help="Save generated image to file")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check task status")
    status_parser.add_argument("task_id", help="Task ID")
    status_parser.add_argument("--output", help="Save result if completed")
    
    args = parser.parse_args()
    
    if args.command == "recognize":
        handle_recognize(args)
    elif args.command == "generate":
        handle_generate(args)
    elif args.command == "status":
        handle_status(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
