#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后台任务执行器
"""

import sys
import os
import json
import logging
import time
from datetime import datetime
from task_utils import get_task, update_task
from cos_client import COSClient
from doubao_client import DoubaoClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tasks/worker.log')
)
logger = logging.getLogger(__name__)

def apply_quality_prompt(task_name, prompt, quality_mode):
    if quality_mode == "fast":
        suffix = "请优先快速返回结果，保持关键信息准确。"
    elif quality_mode == "high":
        suffix = "请进行高细节分析，输出完整、严谨、结构清晰的结果。"
    else:
        suffix = "请平衡速度与质量，输出清晰且可直接使用的结果。"
    if task_name == "image_generation":
        return f"{prompt}\n\n质量要求: {suffix}"
    return f"{prompt}\n\n回答要求: {suffix}"

def resolve_image_input(image_input, cos_client, metrics):
    if os.path.exists(image_input):
        logger.info(f"上传图片到COS: {image_input}")
        upload_result = cos_client.upload_file(image_input)
        if not upload_result['success']:
            raise Exception(f"图片上传失败: {upload_result.get('error')}")
        metrics["uploads"] = metrics.get("uploads", 0) + 1
        image_url = upload_result['url']
        logger.info(f"图片上传成功: {image_url}")
        return image_url
    return image_input

def run_with_retry(func, retry_count, stage_name, model_name, metrics):
    last_error = None
    total_attempts = retry_count + 1
    for attempt in range(1, total_attempts + 1):
        started = time.time()
        try:
            result = func()
            if isinstance(result, dict) and result.get("error"):
                raise RuntimeError(result.get("error"))
            metrics["api_attempts"].append({
                "stage": stage_name,
                "model": model_name,
                "attempt": attempt,
                "status": "success",
                "duration_ms": int((time.time() - started) * 1000)
            })
            return result
        except Exception as e:
            last_error = e
            metrics["api_attempts"].append({
                "stage": stage_name,
                "model": model_name,
                "attempt": attempt,
                "status": "failed",
                "duration_ms": int((time.time() - started) * 1000),
                "error": str(e)
            })
            if attempt < total_attempts:
                time.sleep(min(2 * attempt, 5))
    raise RuntimeError(str(last_error))

def handle_vision_task(params, metrics):
    prompt = params.get('prompt', '你看见了什么？')
    quality_mode = params.get("quality", "balanced")
    retry_count = int(params.get("retry_count", 2))
    images = params.get("images")
    if not images:
        one_image = params.get("image")
        images = [one_image] if one_image else []
    images = [img for img in images if img]
    if not images:
        raise ValueError("缺少 image 或 images 参数")

    client = DoubaoClient()
    fallback_model = os.getenv("DOUBAO_VISION_FALLBACK_MODEL")
    cos_client = COSClient()
    enhanced_prompt = apply_quality_prompt("vision_recognition", prompt, quality_mode)
    items = []
    success_count = 0

    for image_input in images:
        image_url = resolve_image_input(image_input, cos_client, metrics)
        model_used = client.vision_model
        try:
            result = run_with_retry(
                lambda: client.vision_recognition(image_url, enhanced_prompt, model_override=None),
                retry_count,
                "vision_primary",
                client.vision_model,
                metrics
            )
        except Exception as primary_error:
            if fallback_model and fallback_model != client.vision_model:
                try:
                    result = run_with_retry(
                        lambda: client.vision_recognition(image_url, enhanced_prompt, model_override=fallback_model),
                        retry_count,
                        "vision_fallback",
                        fallback_model,
                        metrics
                    )
                    model_used = fallback_model
                except Exception as fallback_error:
                    items.append({
                        "input": image_input,
                        "image_url": image_url,
                        "status": "failed",
                        "error": str(fallback_error)
                    })
                    continue
            else:
                items.append({
                    "input": image_input,
                    "image_url": image_url,
                    "status": "failed",
                    "error": str(primary_error)
                })
                continue

        success_count += 1
        items.append({
            "input": image_input,
            "image_url": image_url,
            "status": "completed",
            "model": model_used,
            "recognition_result": result
        })

    if success_count == 0:
        first_error = items[0]["error"] if items else "识别失败"
        raise RuntimeError(first_error)

    if len(items) == 1 and success_count == 1 and items[0]["status"] == "completed":
        return {
            "image_url": items[0]["image_url"],
            "model": items[0]["model"],
            "recognition_result": items[0]["recognition_result"]
        }

    return {
        "prompt": prompt,
        "quality": quality_mode,
        "items": items,
        "summary": {
            "total": len(items),
            "success": success_count,
            "failed": len(items) - success_count
        }
    }

def handle_generation_task(params, metrics):
    prompt = params.get('prompt')
    ref_images = params.get('ref_images') # 列表或单个路径/URL
    sequential_options = params.get('sequential_options')
    quality_mode = params.get("quality", "balanced")
    retry_count = int(params.get("retry_count", 2))

    if not prompt:
        raise ValueError("缺少 prompt 参数")

    processed_ref_images = []
    if ref_images:
        if isinstance(ref_images, str):
            ref_images = [ref_images]

        cos_client = COSClient()
        for img in ref_images:
            processed_ref_images.append(resolve_image_input(img, cos_client, metrics))

    logger.info("调用豆包图像生成API")
    client = DoubaoClient()
    fallback_model = os.getenv("DOUBAO_IMAGE_FALLBACK_MODEL")

    ref_input = processed_ref_images if processed_ref_images else None
    if ref_input and len(ref_input) == 1:
        ref_input = ref_input[0]

    enhanced_prompt = apply_quality_prompt("image_generation", prompt, quality_mode)
    model_used = client.image_model
    try:
        result = run_with_retry(
            lambda: client.generate_image(enhanced_prompt, image_urls=ref_input, sequential_options=sequential_options, model_override=None),
            retry_count,
            "image_primary",
            client.image_model,
            metrics
        )
    except Exception:
        if fallback_model and fallback_model != client.image_model:
            result = run_with_retry(
                lambda: client.generate_image(enhanced_prompt, image_urls=ref_input, sequential_options=sequential_options, model_override=fallback_model),
                retry_count,
                "image_fallback",
                fallback_model,
                metrics
            )
            model_used = fallback_model
        else:
            raise

    return {
        "prompt": prompt,
        "quality": quality_mode,
        "model": model_used,
        "ref_images": processed_ref_images,
        "generation_result": result
    }

def main():
    if len(sys.argv) < 2:
        logger.error("缺少任务ID参数")
        return
        
    task_id = sys.argv[1]
    logger.info(f"开始处理任务: {task_id}")
    started_at = datetime.now().isoformat()
    started_ts = time.time()
    metrics = {
        "started_at": started_at,
        "uploads": 0,
        "api_attempts": []
    }

    try:
        update_task(task_id, {"status": "processing", "started_at": started_at, "metrics": metrics})
        task = get_task(task_id)
        if not task:
            logger.error(f"找不到任务: {task_id}")
            return

        task_type = task.get('type')
        params = task.get('params', {})

        result = None
        if task_type == 'vision_recognition':
            result = handle_vision_task(params, metrics)
        elif task_type == 'image_generation':
            result = handle_generation_task(params, metrics)
        else:
            raise ValueError(f"未知任务类型: {task_type}")

        ended_at = datetime.now().isoformat()
        metrics["ended_at"] = ended_at
        metrics["duration_ms"] = int((time.time() - started_ts) * 1000)
        metrics["api_attempt_count"] = len(metrics["api_attempts"])
        update_task(task_id, {
            "status": "completed",
            "ended_at": ended_at,
            "metrics": metrics,
            "result": result
        })
        logger.info(f"任务完成: {task_id}")

    except Exception as e:
        logger.error(f"任务失败: {task_id}, 错误: {str(e)}", exc_info=True)
        ended_at = datetime.now().isoformat()
        metrics["ended_at"] = ended_at
        metrics["duration_ms"] = int((time.time() - started_ts) * 1000)
        metrics["api_attempt_count"] = len(metrics["api_attempts"])
        update_task(task_id, {
            "status": "failed",
            "ended_at": ended_at,
            "metrics": metrics,
            "error": str(e)
        })

if __name__ == "__main__":
    main()
