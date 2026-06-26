#!/usr/bin/env python3
"""
Doubao Seedream Skill - 主生成脚本
支持火山方舟 Ark API 的 Seedream 系列模型

API 文档: https://www.volcengine.com/docs/82379/1541523
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import base64
import time
import io
import re
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 脚本所在目录
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_FILE = SKILL_DIR / "config.json"

# 火山方舟 API 端点
API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 支持的模型列表
MODELS = [
    {
        "id": "doubao-seedream-5-0-260128",
        "name": "Doubao-Seedream-5.0",
        "type": "文生图",
        "description": "最新版本，效果最好",
        "default_size": "1920x1928",
        "supported_sizes": ["1920x1928"]
    },
    {
        "id": "doubao-seedream-4-5-251128",
        "name": "Doubao-Seedream-4.5",
        "type": "文生图",
        "description": "4.5版本，效果优秀",
        "default_size": "1920x1928",
        "supported_sizes": ["1920x1928"]
    },
    {
        "id": "doubao-seedream-4-0-250828",
        "name": "Doubao-Seedream-4.0",
        "type": "文生图",
        "description": "4.0版本，稳定可靠",
        "default_size": "1024x1024",
        "supported_sizes": ["512x512", "768x768", "1024x1024", "1024x2048", "2048x1024"]
    },
    {
        "id": "doubao-seededit-3-0-i2i-250628",
        "name": "Doubao-SeedEdit-3.0-i2i",
        "type": "图生图",
        "description": "图片编辑模型",
        "default_size": "1024x1024",
        "supported_sizes": ["512x512", "768x768", "1024x1024", "1024x2048", "2048x1024"]
    },
    {
        "id": "doubao-seedream-3-0-t2i-250415",
        "name": "Doubao-Seedream-3.0-t2i",
        "type": "文生图",
        "description": "3.0版本，经典版",
        "default_size": "1024x1024",
        "supported_sizes": ["512x512", "768x768", "1024x1024", "1024x2048", "2048x1024"]
    },
]

def load_config():
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"api_key": "", "default_model": "doubao-seedream-4-0-250828", "output_dir": "./generated-images"}

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"配置已保存到: {CONFIG_FILE}")

def get_api_key(config):
    """获取 API Key，优先检查环境变量"""
    api_key = os.environ.get('VOLCENGINE_API_KEY', '')
    if not api_key:
        api_key = config.get('api_key', '')
    return api_key

def check_api_key(config):
    """检查 API Key 是否已设置"""
    api_key = get_api_key(config)
    if api_key:
        return True
    return False

def setup_api_key(config):
    """引导用户设置 API Key"""
    print("\n" + "="*60)
    print(" 火山方舟 API Key 设置")
    print("="*60)
    print("\n请选择设置方式:")
    print("  1. 输入 API Key（仅本次会话有效）")
    print("  2. 输入 API Key（保存到配置文件）")
    print("  3. 从环境变量读取")
    print("  4. 退出")
    
    choice = input("\n请选择 [1-4]: ").strip()
    
    if choice == '1':
        api_key = input("请输入 API Key: ").strip()
        if api_key:
            return api_key, config
    elif choice == '2':
        api_key = input("请输入 API Key: ").strip()
        if api_key:
            config['api_key'] = api_key
            save_config(config)
            return api_key, config
    elif choice == '3':
        env_key = os.environ.get('VOLCENGINE_API_KEY', '')
        if env_key:
            print(f"检测到环境变量中的 API Key")
            return env_key, config
        else:
            print("未找到 VOLCENGINE_API_KEY 环境变量")
    elif choice == '4':
        print("已退出")
        sys.exit(0)
    
    return None, config

def list_models():
    """列出所有可用模型"""
    print("\n" + "="*60)
    print(" Doubao Seedream 可用模型")
    print("="*60)
    print()
    
    t2i_models = [m for m in MODELS if m['type'] == '文生图']
    i2i_models = [m for m in MODELS if m['type'] == '图生图']
    
    print("📝 文生图模型:")
    print("-"*50)
    for i, m in enumerate(t2i_models, 1):
        print(f"  {i}. {m['name']}")
        print(f"     ID: {m['id']}")
        print(f"     {m['description']}")
        print()
    
    if i2i_models:
        print("🖼️ 图生图模型:")
        print("-"*50)
        for i, m in enumerate(i2i_models, len(t2i_models)+1):
            print(f"  {i}. {m['name']}")
            print(f"     ID: {m['id']}")
            print(f"     {m['description']}")
            print()

def select_model():
    """交互式选择模型"""
    print("\n请选择模型:")
    print("-"*50)
    
    for i, m in enumerate(MODELS, 1):
        emoji = "📝" if m['type'] == '文生图' else "🖼️"
        print(f"  {i}. {emoji} {m['name']} - {m['type']}")
    
    while True:
        try:
            choice = int(input("\n请输入序号 [1-5]: ").strip())
            if 1 <= choice <= len(MODELS):
                return MODELS[choice - 1]
        except ValueError:
            pass
        print("无效选择，请重新输入")

def download_image(url, output_path):
    """下载图片到本地"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=60) as response:
            img_data = response.read()
            with open(output_path, 'wb') as f:
                f.write(img_data)
            return img_data
    except Exception as e:
        return None

def generate_image(prompt, model_id, api_key, input_image=None, output_path=None, size="1024x1024"):
    """调用火山方舟 API 生成图片
    
    使用 /api/v3/images/generations 端点
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    if input_image:
        # 图生图模式 - 使用 Vision API (chat completions)
        with open(input_image, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        ext = Path(input_image).suffix.lower()
        mime_type = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp'
        }.get(ext, 'image/png')
        
        image_url = f"data:{mime_type};base64,{image_data}"
        
        payload = {
            "model": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "max_tokens": 1024
        }
        endpoint = "/chat/completions"
    else:
        # 文生图模式 - 使用 Images API
        payload = {
            "model": model_id,
            "prompt": prompt,
            "size": size,
            "n": 1
        }
        endpoint = "/images/generations"
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        print(f"正在调用 API...")
        
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # 处理 Images API 响应
            if endpoint == "/images/generations":
                if 'data' in result and len(result['data']) > 0:
                    # 优先下载 URL 图片
                    img_url = result['data'][0].get('url', '')
                    if img_url:
                        img_data = download_image(img_url, output_path)
                        if img_data:
                            return output_path
                    
                    # 如果没有 URL，尝试 base64
                    image_b64 = result['data'][0].get('b64_json', '')
                    if image_b64:
                        img_data = base64.b64decode(image_b64)
                        if output_path:
                            with open(output_path, 'wb') as f:
                                f.write(img_data)
                        return output_path
                
                return result
            
            # 处理 Chat API 响应（图生图）
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                if 'data:image' in content:
                    match = re.search(r'data:image/\w+;base64,([A-Za-z0-9+/=]+)', content)
                    if match:
                        img_data = base64.b64decode(match.group(1))
                        if output_path:
                            with open(output_path, 'wb') as f:
                                f.write(img_data)
                        return output_path
                
                return content
            
            return result
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"error": str(e)}

def interactive_mode():
    """交互式生成模式"""
    config = load_config()
    
    # 检查 API Key
    if not check_api_key(config):
        print("\n⚠️  未检测到 API Key，需要先设置")
        api_key, config = setup_api_key(config)
        if not api_key:
            return
    else:
        api_key = get_api_key(config)
    
    # 选择模型
    print("\n" + "="*60)
    print(" Doubao Seedream 图片生成器")
    print("="*60)
    
    model = select_model()
    
    # 选择模式
    print("\n选择生成模式:")
    print("  1. 📝 文生图（根据文字描述生成图片）")
    print("  2. 🖼️ 图生图（上传图片进行编辑）")
    
    mode_choice = input("\n请选择 [1-2]: ").strip()
    
    input_image = None
    if mode_choice == '2' and model['type'] == '图生图':
        input_image = input("请输入图片路径: ").strip()
        if not os.path.exists(input_image):
            print(f"✗ 文件不存在: {input_image}")
            return
    
    # 输入提示词
    if model['type'] == '图生图':
        prompt = input("\n请输入编辑指令: ").strip()
    else:
        prompt = input("\n请输入图片描述: ").strip()
    
    if not prompt:
        print("✗ 提示词不能为空")
        return
    
    # 设置输出路径
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    model_name_short = model['id'].replace('-', '_')
    default_output = f"seedream_{model_name_short}_{timestamp}.png"
    output_path = input(f"\n输出文件名 [默认: {default_output}]: ").strip() or default_output
    
    # 确保输出目录存在
    output_dir = Path(output_path).parent
    if str(output_dir) != '.':
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成图片
    print("\n⏳ 正在生成图片，请稍候...")
    print(f"  模型: {model['name']}")
    print(f"  提示词: {prompt}")
    
    result = generate_image(prompt, model['id'], api_key, input_image, output_path)
    
    if isinstance(result, dict) and 'error' in result:
        print(f"\n✗ 生成失败: {result['error']}")
    elif isinstance(result, str) and os.path.exists(result):
        print(f"\n✅ 生成成功！")
        print(f"   文件: {os.path.abspath(result)}")

def main():
    parser = argparse.ArgumentParser(
        description="Doubao Seedream 图片生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # list 命令
    subparsers.add_parser('list', help='列出所有可用模型')
    
    # generate 命令
    gen_parser = subparsers.add_parser('generate', help='生成图片')
    gen_parser.add_argument('-p', '--prompt', required=True, help='图片描述')
    gen_parser.add_argument('-m', '--model', default='doubao-seedream-4-0-250828', help='模型 ID')
    gen_parser.add_argument('-o', '--output', help='输出文件路径')
    gen_parser.add_argument('-i', '--input-image', help='输入图片（图生图模式）')
    gen_parser.add_argument('-s', '--size', default='1024x1024', help='图片尺寸')
    
    # edit 命令
    edit_parser = subparsers.add_parser('edit', help='图生图编辑')
    edit_parser.add_argument('-p', '--prompt', required=True, help='编辑指令')
    edit_parser.add_argument('-i', '--input-image', required=True, help='输入图片路径')
    edit_parser.add_argument('-m', '--model', default='doubao-seededit-3-0-i2i-250628', help='模型 ID')
    edit_parser.add_argument('-o', '--output', help='输出文件路径')
    
    # config 命令
    subparsers.add_parser('config', help='配置管理')
    
    args = parser.parse_args()
    
    # 无参数时进入交互模式
    if args.command is None:
        interactive_mode()
        return
    
    # 处理各命令
    if args.command == 'list':
        list_models()
        
    elif args.command == 'generate':
        config = load_config()
        
        # 检查 API Key
        if not check_api_key(config):
            print("⚠️  未检测到 API Key")
            api_key, config = setup_api_key(config)
            if not api_key:
                return
        else:
            api_key = get_api_key(config)
        
        # 设置输出路径
        if not args.output:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            args.output = f"seedream_output_{timestamp}.png"
        
        print("⏳ 正在生成图片...")
        result = generate_image(args.prompt, args.model, api_key, args.input_image, args.output, args.size)
        
        if isinstance(result, dict) and 'error' in result:
            print(f"✗ 生成失败: {result['error']}")
        elif isinstance(result, str) and os.path.exists(result):
            print(f"✅ 生成成功: {os.path.abspath(result)}")
    
    elif args.command == 'edit':
        config = load_config()
        
        # 检查 API Key
        if not check_api_key(config):
            print("⚠️  未检测到 API Key")
            api_key, config = setup_api_key(config)
            if not api_key:
                return
        else:
            api_key = get_api_key(config)
        
        # 检查输入文件
        if not os.path.exists(args.input_image):
            print(f"✗ 输入文件不存在: {args.input_image}")
            return
        
        # 设置输出路径
        if not args.output:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            args.output = f"seedream_edited_{timestamp}.png"
        
        print("⏳ 正在编辑图片...")
        result = generate_image(args.prompt, args.model, api_key, args.input_image, args.output)
        
        if isinstance(result, dict) and 'error' in result:
            print(f"✗ 生成失败: {result['error']}")
        elif isinstance(result, str) and os.path.exists(result):
            print(f"✅ 生成成功: {os.path.abspath(result)}")
    
    elif args.command == 'config':
        config = load_config()
        setup_api_key(config)

if __name__ == '__main__':
    main()
