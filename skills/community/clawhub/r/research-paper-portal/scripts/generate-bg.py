#!/usr/bin/env python3
"""
使用 ComfyUI Flux2 为论文生成 AI 背景图

配置要求:
- COMFYUI_URL: ComfyUI 服务器地址
- 模型文件需提前部署到 ComfyUI

输出:
- preview-{id}.webp: 预览图 (640px)
- full-{id}.webp: 高清图 (1280px)
"""

import json
import requests
import time
import os
import random
from PIL import Image

# ============ 配置区域 ============
COMFYUI_URL = "http://YOUR_SERVER:8188"  # 修改为你的 ComfyUI 地址
PAPERS_FILE = "paper-index.json"
OUTPUT_DIR = "assets/images"
WIDTH = 1280
HEIGHT = 720
# ==================================

def get_prompt_for_paper(paper):
    """根据论文内容生成图像提示词"""
    tags = paper.get("tags", [])
    tags_str = ", ".join(tags)
    
    # 根据关键词选择主题
    if any(kw in tags_str.lower() for kw in ["geothermal", "earth", "geo"]):
        return "Deep underground geothermal energy, borehole drilling, earth layers cross-section, magma glow, warm orange red brown colors, scientific illustration, abstract background, 4k, detailed, no text"
    elif any(kw in tags_str.lower() for kw in ["heat", "thermal", "cooling"]):
        return "Heat pipe thermal management system, vapor condensation cycle, blue orange silver metallic colors, engineering diagram, abstract background, 4k, detailed, no text"
    elif any(kw in tags_str.lower() for kw in ["electric", "power", "energy"]):
        return "Thermoelectric generator module, P-N semiconductor junctions, blue red purple gradient, copper electrodes, scientific illustration, abstract background, 4k, detailed, no text"
    elif any(kw in tags_str.lower() for kw in ["nano", "material", "crystal"]):
        return "Nanoscale materials, molecular structure, crystal lattice, quantum dots, green blue silver colors, scientific illustration, abstract background, 4k, detailed, no text"
    else:
        return "Scientific research, abstract patterns, flowing lines, blue purple cyan colors, high quality, 4k, detailed, no text"

def create_flux2_workflow(prompt, filename, seed=None):
    """创建 Flux2 工作流"""
    if seed is None:
        seed = random.randint(1, 999999999)
    
    return {
        "1": {
            "inputs": {"unet_name": "flux2_dev_fp8mixed.safetensors", "weight_dtype": "default"},
            "class_type": "UNETLoader"
        },
        "2": {
            "inputs": {"clip_name": "mistral_3_small_flux2_bf16.safetensors", "type": "flux2"},
            "class_type": "CLIPLoader"
        },
        "3": {
            "inputs": {"vae_name": "flux2-vae.safetensors"},
            "class_type": "VAELoader"
        },
        "4": {
            "inputs": {"text": prompt, "clip": ["2", 0]},
            "class_type": "CLIPTextEncode"
        },
        "5": {
            "inputs": {"text": "", "clip": ["2", 0]},
            "class_type": "CLIPTextEncode"
        },
        "6": {
            "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1},
            "class_type": "EmptyFlux2LatentImage"
        },
        "7": {
            "inputs": {"noise_seed": seed},
            "class_type": "RandomNoise"
        },
        "8": {
            "inputs": {"model": ["1", 0], "positive": ["4", 0], "negative": ["5", 0], "cfg": 1.0},
            "class_type": "CFGGuider"
        },
        "9": {
            "inputs": {"sampler_name": "euler"},
            "class_type": "KSamplerSelect"
        },
        "10": {
            "inputs": {"steps": 20, "width": WIDTH, "height": HEIGHT},
            "class_type": "Flux2Scheduler"
        },
        "11": {
            "inputs": {
                "noise": ["7", 0],
                "guider": ["8", 0],
                "sampler": ["9", 0],
                "sigmas": ["10", 0],
                "latent_image": ["6", 0]
            },
            "class_type": "SamplerCustomAdvanced"
        },
        "12": {
            "inputs": {"samples": ["11", 0], "vae": ["3", 0]},
            "class_type": "VAEDecode"
        },
        "13": {
            "inputs": {"filename_prefix": filename, "images": ["12", 0]},
            "class_type": "SaveImage"
        }
    }

def submit_task(workflow):
    """提交工作流到 ComfyUI"""
    try:
        resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": workflow}, timeout=30)
        data = resp.json()
        return data.get("prompt_id")
    except Exception as e:
        print(f"  提交失败: {e}")
        return None

def wait_for_task(prompt_id, timeout=120):
    """等待任务完成"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
            data = resp.json()
            if prompt_id in data:
                if data[prompt_id].get("status", {}).get("completed"):
                    return data[prompt_id].get("outputs", {})
        except:
            pass
        time.sleep(2)
    return None

def download_image(filename, subfolder, output_path):
    """下载生成的图片"""
    url = f"{COMFYUI_URL}/view?filename={filename}&subfolder={subfolder}&type=output"
    try:
        resp = requests.get(url, timeout=60)
        with open(output_path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"  下载失败: {e}")
        return False

def convert_to_webp(png_path, output_dir, name):
    """转换为 WebP 格式"""
    img = Image.open(png_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # 生成预览图
    preview_img = img.copy()
    preview_img.thumbnail((640, 640 * 10), Image.LANCZOS)
    preview_path = os.path.join(output_dir, f"preview-{name}.webp")
    preview_img.save(preview_path, "WEBP", quality=85)
    
    # 生成高清图
    full_img = img.copy()
    full_img.thumbnail((1280, 1280 * 10), Image.LANCZOS)
    full_path = os.path.join(output_dir, f"full-{name}.webp")
    full_img.save(full_path, "WEBP", quality=85)
    
    # 删除原始 PNG
    os.remove(png_path)
    
    return preview_path, full_path

def main():
    print("=" * 50)
    print(" AI 背景图生成器 (Flux2)")
    print("=" * 50)
    print(f"ComfyUI: {COMFYUI_URL}")
    print()
    
    # 加载论文
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    papers = data.get("papers", [])
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    generated = 0
    for paper in papers:
        paper_id = paper.get("id", "unknown")
        bg_name = f"image_{paper_id}"
        
        preview_path = os.path.join(OUTPUT_DIR, f"preview-{bg_name}.webp")
        if os.path.exists(preview_path):
            print(f"[{bg_name}] 已存在，跳过")
            continue
        
        print(f"[{bg_name}] 生成中...")
        
        prompt = get_prompt_for_paper(paper)
        workflow = create_flux2_workflow(prompt, bg_name)
        prompt_id = submit_task(workflow)
        
        if not prompt_id:
            continue
        
        print(f"  任务: {prompt_id[:8]}... ", end="", flush=True)
        
        outputs = wait_for_task(prompt_id)
        if outputs:
            print("OK")
            for node_id, node_output in outputs.items():
                for img in node_output.get("images", []):
                    temp_path = os.path.join(OUTPUT_DIR, f"{bg_name}.png")
                    if download_image(img["filename"], img.get("subfolder", ""), temp_path):
                        convert_to_webp(temp_path, OUTPUT_DIR, bg_name)
                        paper["bgImage"] = bg_name
                        generated += 1
                        print(f"  已保存: {bg_name}.webp")
        else:
            print("超时")
        
        time.sleep(1)
    
    # 保存更新
    with open(PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n生成 {generated} 张背景图")
    print("=" * 50)

if __name__ == "__main__":
    main()
