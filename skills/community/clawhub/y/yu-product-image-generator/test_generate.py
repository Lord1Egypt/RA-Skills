#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 使用 Nano Banana API 生成仿真绿植商品图（SSE 流式）
"""

import os
import json
import requests
import base64
import time
from datetime import datetime

# Nano Banana API 配置
API_KEY = "sk-6fe41fd597614d2686f6d0685b4bd232"
ENDPOINT = "https://grsai.dakka.com.cn/v1/draw/nano-banana"
RESULT_ENDPOINT = "https://grsai.dakka.com.cn/v1/draw/result"
TIMEOUT = 180  # 超时时间（秒）

# 产品图路径
PRODUCT_IMAGE = "/Users/master.yu/.openclaw/media/inbound/40bfe14f-0211-4950-8bd7-89f727c81b6a.png"

# 输出目录
OUTPUT_DIR = "/Users/master.yu/.openclaw/workspace/skills/product-image-generator/output/test_" + datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def encode_image(path):
    """将图片转为 base64"""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_image(prompt, output_name, reference_image=None):
    """调用 Nano Banana API 生成图片（SSE 流式）"""
    print(f"\n🎨 生成：{output_name}")
    print(f"   提示词：{prompt[:60]}...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    
    payload = {
        "model": "nano-banana-pro",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1
    }
    
    # 添加参考图
    if reference_image:
        try:
            img_base64 = encode_image(reference_image)
            payload["reference_images"] = [img_base64]
            print(f"   参考图：{reference_image.split('/')[-1]}")
        except Exception as e:
            print(f"   ⚠️ 参考图加载失败：{e}")
    
    try:
        print(f"   调用 API...")
        
        response = requests.post(
            ENDPOINT,
            headers=headers,
            json=payload,
            stream=True,
            timeout=TIMEOUT
        )
        
        if response.status_code != 200:
            print(f"   ❌ API 错误 {response.status_code}: {response.text[:200]}")
            return None
        
        # 解析 SSE 流
        task_id = None
        image_url = None
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                print(f"   SSE: {line_str[:100]}...")
                
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        
                        # 获取任务 ID
                        if 'id' in data:
                            task_id = data['id']
                            print(f"   任务 ID: {task_id}")
                        
                        # 检查状态
                        status = data.get('status', '')
                        if status == 'succeeded':
                            images = data.get('images', [])
                            if images:
                                image_url = images[0]
                                print(f"   ✅ 生成成功！")
                                break
                        elif status == 'failed':
                            error = data.get('failure_reason', data.get('error', '未知错误'))
                            print(f"   ❌ 生成失败：{error}")
                            return None
                        
                        # 进度更新
                        progress = data.get('progress', 0)
                        if progress and progress % 10 == 0:
                            print(f"   进度：{progress}%")
                    
                    except json.JSONDecodeError:
                        pass
        
        # 下载图片
        if image_url:
            print(f"   下载图片...")
            img_resp = requests.get(image_url, timeout=30)
            output_path = os.path.join(OUTPUT_DIR, output_name)
            with open(output_path, 'wb') as f:
                f.write(img_resp.content)
            print(f"   ✅ 保存：{output_path}")
            return output_path
        elif task_id:
            # 如果 SSE 没返回图片，轮询结果
            print(f"   轮询结果...")
            for i in range(60):
                time.sleep(2)
                result_resp = requests.get(
                    f"{RESULT_ENDPOINT}?id={task_id}",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    timeout=30
                )
                if result_resp.status_code == 200:
                    result_data = result_resp.json()
                    status = result_data.get('status')
                    
                    if status == 'succeeded':
                        images = result_data.get('images', [])
                        if images:
                            image_url = images[0]
                            img_resp = requests.get(image_url, timeout=30)
                            output_path = os.path.join(OUTPUT_DIR, output_name)
                            with open(output_path, 'wb') as f:
                                f.write(img_resp.content)
                            print(f"   ✅ 保存：{output_path}")
                            return output_path
                    elif status == 'failed':
                        print(f"   ❌ 生成失败")
                        return None
            
            print(f"   ⏱️ 轮询超时")
            return None
        else:
            print(f"   ❌ 无任务 ID")
            return None
            
    except Exception as e:
        print(f"   ❌ 异常：{e}")
        return None

def main():
    print("=" * 60)
    print("🎨 AI 商品图生成器 - 测试（Nano Banana API）")
    print("=" * 60)
    print(f"输出目录：{OUTPUT_DIR}\n")
    
    # 3 个分镜的提示词
    prompts = [
        {
            "name": "01_main.png",
            "prompt": "专业电商产品摄影，一盆仿真万年青绿植，白色陶瓷花盆，放在浅木色地板上，北欧简约风格，自然侧光，柔和光线，背景是干净的白墙，产品居中，高清，商业摄影，1200x1200"
        },
        {
            "name": "02_detail.png",
            "prompt": "产品细节特写，仿真万年青叶片特写，展示叶脉纹理和深绿与黄绿的色彩渐变，45 度角拍摄，浅景深，专业微距摄影，自然光线，高清质感，1200x1200"
        },
        {
            "name": "03_scene.png",
            "prompt": "家居场景图，仿真万年青绿植放在客厅角落，旁边有书籍和咖啡杯，温馨居家氛围，浅木色地板，白墙背景，生活气息，自然光，北欧风格室内摄影，1200x1200"
        }
    ]
    
    results = []
    for i, item in enumerate(prompts, 1):
        result = generate_image(item["prompt"], item["name"], PRODUCT_IMAGE)
        if result:
            results.append(result)
    
    print("\n" + "=" * 60)
    print(f"✅ 生成完成！共 {len(results)}/{len(prompts)} 张")
    print(f"输出目录：{OUTPUT_DIR}")
    
    if results:
        print(f"\n📦 生成的图片:")
        for img in results:
            print(f"   - {img}")
    else:
        print(f"\n⚠️ 未生成图片，请检查 API 状态")
    
    print("=" * 60)
    
    # 保存生成记录
    record = {
        "timestamp": datetime.now().isoformat(),
        "output_dir": OUTPUT_DIR,
        "images": results,
        "style": "北欧简约风",
        "language": "中文",
        "api": "nano-banana-pro"
    }
    with open(os.path.join(OUTPUT_DIR, "generation_record.json"), 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    
    return results

if __name__ == "__main__":
    main()
