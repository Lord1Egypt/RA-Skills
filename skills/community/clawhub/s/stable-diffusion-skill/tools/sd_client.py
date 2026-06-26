#!/usr/bin/env python3
"""
Stable Diffusion WebUI API Client
Supports: txt2img, img2img, inpaint, ControlNet, upscale, model management
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

# Try to import requests, provide helpful error if missing
try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)

# ── Configuration ──────────────────────────────────────────────────────────────
SD_WEBUI_URL = os.environ.get("SD_WEBUI_URL", "http://127.0.0.1:7860")
SD_TIMEOUT = int(os.environ.get("SD_TIMEOUT", "300"))
SD_OUTPUT_DIR = os.environ.get("SD_OUTPUT_DIR", "./sd_output")


# ── Helpers ────────────────────────────────────────────────────────────────────
def api_get(endpoint: str) -> dict:
    url = f"{SD_WEBUI_URL.rstrip('/')}{endpoint}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


def api_post(endpoint: str, payload: dict) -> dict:
    url = f"{SD_WEBUI_URL.rstrip('/')}{endpoint}"
    resp = requests.post(url, json=payload, timeout=SD_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def img_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def b64_to_img(b64_str: str, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(b64_str))


def save_images(images_b64: list, output_dir: str, prefix: str = "output") -> list:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = int(time.time())
    saved = []
    for i, img_b64 in enumerate(images_b64):
        path = os.path.join(output_dir, f"{prefix}_{timestamp}_{i+1}.png")
        b64_to_img(img_b64, path)
        saved.append(path)
    return saved


def print_result(saved_paths: list, info: dict = None):
    print("\n✅ 生成成功！")
    for p in saved_paths:
        print(f"  📁 {os.path.abspath(p)}")
    if info:
        seed = info.get("seed", "unknown") if isinstance(info, dict) else "unknown"
        print(f"  🌱 Seed: {seed}")


# ── Actions ────────────────────────────────────────────────────────────────────

def action_status():
    """Check connection and WebUI version"""
    try:
        data = api_get("/internal/sysinfo")
        print("✅ SD WebUI 连接正常")
        print(f"  版本: {data.get('Version', 'unknown')}")
        print(f"  Python: {data.get('Python', 'unknown')}")
    except Exception:
        # fallback
        try:
            data = api_get("/sdapi/v1/options")
            print("✅ SD WebUI 连接正常")
            model = data.get("sd_model_checkpoint", "unknown")
            print(f"  当前模型: {model}")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            print(f"  请确认 SD WebUI 已启动（带 --api 参数），地址: {SD_WEBUI_URL}")
            sys.exit(1)


def action_list_models():
    models = api_get("/sdapi/v1/sd-models")
    print(f"\n📦 可用模型 ({len(models)} 个):")
    for m in models:
        active = " ✓" if m.get("is_active") else ""
        print(f"  {m['title']}{active}")


def action_list_samplers():
    samplers = api_get("/sdapi/v1/samplers")
    print(f"\n🎲 可用采样器 ({len(samplers)} 个):")
    for s in samplers:
        print(f"  {s['name']}")


def action_list_upscalers():
    upscalers = api_get("/sdapi/v1/upscalers")
    print(f"\n🔍 可用放大算法 ({len(upscalers)} 个):")
    for u in upscalers:
        print(f"  {u['name']}")


def action_list_loras():
    try:
        loras = api_get("/sdapi/v1/loras")
        print(f"\n🎭 可用 LoRA ({len(loras)} 个):")
        for l in loras:
            print(f"  {l['name']}  (用法: <lora:{l['name']}:0.8>)")
    except Exception as e:
        print(f"⚠️  无法获取 LoRA 列表: {e}")


def action_list_vaes():
    try:
        vaes = api_get("/sdapi/v1/sd-vae")
        print(f"\n🗜️  可用 VAE ({len(vaes)} 个):")
        for v in vaes:
            print(f"  {v['model_name']}")
    except Exception as e:
        print(f"⚠️  无法获取 VAE 列表: {e}")


def action_switch_model(model_name: str):
    print(f"🔄 正在切换模型: {model_name} ...")
    api_post("/sdapi/v1/options", {"sd_model_checkpoint": model_name})
    print(f"✅ 模型已切换为: {model_name}")


def action_txt2img(args):
    payload = {
        "prompt": args.prompt or "",
        "negative_prompt": args.negative_prompt or "(worst quality:2),(low quality:2),blurry,ugly,bad anatomy,bad hands,extra limbs,deformed,mutated,watermark,text",
        "steps": args.steps,
        "cfg_scale": args.cfg_scale,
        "width": args.width,
        "height": args.height,
        "seed": args.seed,
        "batch_size": args.batch_size,
        "n_iter": args.n_iter,
        "sampler_name": args.sampler,
        "restore_faces": args.restore_faces,
        "tiling": args.tiling,
    }

    # Hires fix
    if args.enable_hr:
        payload.update({
            "enable_hr": True,
            "hr_scale": args.hr_scale,
            "hr_upscaler": args.hr_upscaler,
            "hr_second_pass_steps": args.hr_steps,
            "denoising_strength": args.denoising_strength,
        })

    # Styles
    if args.styles:
        payload["styles"] = args.styles

    print(f"🎨 正在生成图像 ({args.width}x{args.height}, {args.steps} steps)...")
    print(f"   提示词: {args.prompt[:80]}{'...' if len(args.prompt or '') > 80 else ''}")

    result = api_post("/sdapi/v1/txt2img", payload)
    images = result.get("images", [])
    info = json.loads(result.get("info", "{}"))
    saved = save_images(images, args.output_dir, "txt2img")
    print_result(saved, info)


def action_img2img(args):
    if not args.init_image:
        print("❌ 需要提供 --init-image 参数")
        sys.exit(1)

    payload = {
        "init_images": [img_to_b64(args.init_image)],
        "prompt": args.prompt or "",
        "negative_prompt": args.negative_prompt or "(worst quality:2),(low quality:2),blurry,ugly",
        "steps": args.steps,
        "cfg_scale": args.cfg_scale,
        "width": args.width,
        "height": args.height,
        "seed": args.seed,
        "batch_size": args.batch_size,
        "denoising_strength": args.denoising_strength,
        "sampler_name": args.sampler,
        "resize_mode": args.resize_mode,
    }

    print(f"🔄 正在图生图 (强度: {args.denoising_strength})...")
    result = api_post("/sdapi/v1/img2img", payload)
    images = result.get("images", [])
    info = json.loads(result.get("info", "{}"))
    saved = save_images(images, args.output_dir, "img2img")
    print_result(saved, info)


def action_inpaint(args):
    if not args.init_image:
        print("❌ 需要提供 --init-image 参数")
        sys.exit(1)
    if not args.mask_image:
        print("❌ 需要提供 --mask-image 参数")
        sys.exit(1)

    payload = {
        "init_images": [img_to_b64(args.init_image)],
        "mask": img_to_b64(args.mask_image),
        "prompt": args.prompt or "",
        "negative_prompt": args.negative_prompt or "(worst quality:2),(low quality:2),blurry",
        "steps": args.steps,
        "cfg_scale": args.cfg_scale,
        "width": args.width,
        "height": args.height,
        "seed": args.seed,
        "denoising_strength": args.denoising_strength,
        "sampler_name": args.sampler,
        "inpainting_fill": args.inpainting_fill,
        "inpaint_full_res": args.inpaint_full_res,
        "inpaint_full_res_padding": 32,
        "mask_blur": 4,
    }

    print(f"🖌️  正在局部重绘...")
    result = api_post("/sdapi/v1/img2img", payload)
    images = result.get("images", [])
    info = json.loads(result.get("info", "{}"))
    saved = save_images(images, args.output_dir, "inpaint")
    print_result(saved, info)


def action_txt2img_controlnet(args):
    if not args.control_image:
        print("❌ 需要提供 --control-image 参数")
        sys.exit(1)

    controlnet_unit = {
        "input_image": img_to_b64(args.control_image),
        "module": args.control_module,
        "model": args.control_model,
        "weight": args.control_weight,
        "enabled": True,
        "lowvram": False,
        "pixel_perfect": True,
        "guidance_start": 0.0,
        "guidance_end": 1.0,
        "control_mode": 0,
        "resize_mode": 1,
    }

    payload = {
        "prompt": args.prompt or "",
        "negative_prompt": args.negative_prompt or "(worst quality:2),(low quality:2),blurry,ugly",
        "steps": args.steps,
        "cfg_scale": args.cfg_scale,
        "width": args.width,
        "height": args.height,
        "seed": args.seed,
        "batch_size": args.batch_size,
        "sampler_name": args.sampler,
        "alwayson_scripts": {
            "ControlNet": {
                "args": [controlnet_unit]
            }
        }
    }

    print(f"🎛️  正在使用 ControlNet ({args.control_module}) 生成...")
    result = api_post("/sdapi/v1/txt2img", payload)
    images = result.get("images", [])
    info = json.loads(result.get("info", "{}"))
    saved = save_images(images, args.output_dir, "controlnet")
    print_result(saved, info)


def action_upscale(args):
    if not args.image:
        print("❌ 需要提供 --image 参数")
        sys.exit(1)

    payload = {
        "resize_mode": 0,
        "show_extras_results": True,
        "gfpgan_visibility": 0,
        "codeformer_visibility": args.codeformer_visibility,
        "codeformer_weight": 0.5,
        "upscaling_resize": args.scale,
        "upscaler_1": args.upscaler,
        "upscaler_2": "None",
        "extras_upscaler_2_visibility": 0,
        "image": img_to_b64(args.image),
    }

    print(f"🔍 正在放大图像 ({args.scale}x, {args.upscaler})...")
    result = api_post("/sdapi/v1/extra-single-image", payload)
    image_b64 = result.get("image")
    if not image_b64:
        print("❌ 放大失败")
        sys.exit(1)
    saved = save_images([image_b64], args.output_dir, "upscale")
    print_result(saved)


def action_interrogate(args):
    """Use CLIP/DeepDanbooru to analyze image and get prompts"""
    if not args.image:
        print("❌ 需要提供 --image 参数")
        sys.exit(1)

    payload = {
        "image": img_to_b64(args.image),
        "model": args.interrogate_model,
    }

    print(f"🔎 正在分析图像提示词 ({args.interrogate_model})...")
    result = api_post("/sdapi/v1/interrogate", payload)
    caption = result.get("caption", "")
    print(f"\n✅ 图像提示词:\n{caption}")


def action_png_info(args):
    """Extract generation info from PNG"""
    if not args.image:
        print("❌ 需要提供 --image 参数")
        sys.exit(1)

    payload = {"image": img_to_b64(args.image)}
    result = api_post("/sdapi/v1/png-info", payload)
    info = result.get("info", "")
    print(f"\n📋 图像生成信息:\n{info}")


def action_progress():
    """Check current generation progress"""
    result = api_get("/sdapi/v1/progress")
    progress = result.get("progress", 0)
    state = result.get("state", {})
    eta = result.get("eta_relative", 0)

    print(f"⏳ 生成进度: {progress*100:.1f}%")
    if state.get("job"):
        print(f"   任务: {state['job']}")
    if eta > 0:
        print(f"   预计剩余: {eta:.1f}秒")


def action_skip():
    """Skip current generation"""
    api_post("/sdapi/v1/skip", {})
    print("⏭️  已跳过当前生成")


def action_interrupt():
    """Interrupt current generation"""
    api_post("/sdapi/v1/interrupt", {})
    print("⏹️  已中断生成")


# ── Argument Parser ────────────────────────────────────────────────────────────
def build_parser():
    parser = argparse.ArgumentParser(
        description="Stable Diffusion WebUI API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--action", required=True, choices=[
        "status", "list-models", "list-samplers", "list-upscalers",
        "list-loras", "list-vaes", "switch-model",
        "txt2img", "img2img", "inpaint", "txt2img-controlnet",
        "upscale", "interrogate", "png-info", "progress", "skip", "interrupt"
    ], help="执行的操作")

    # Common generation params
    gen = parser.add_argument_group("生成参数")
    gen.add_argument("--prompt", "-p", help="正向提示词")
    gen.add_argument("--negative-prompt", "-n", help="负向提示词")
    gen.add_argument("--steps", type=int, default=20, help="采样步数 (默认: 20)")
    gen.add_argument("--cfg-scale", type=float, default=7.0, help="提示词遵从度 (默认: 7.0)")
    gen.add_argument("--width", type=int, default=512, help="图像宽度 (默认: 512)")
    gen.add_argument("--height", type=int, default=512, help="图像高度 (默认: 512)")
    gen.add_argument("--seed", type=int, default=-1, help="随机种子 (-1=随机)")
    gen.add_argument("--sampler", default="DPM++ 2M Karras", help="采样器名称")
    gen.add_argument("--batch-size", type=int, default=1, help="每批生成数量")
    gen.add_argument("--n-iter", type=int, default=1, help="批次数量")
    gen.add_argument("--denoising-strength", type=float, default=0.75, help="去噪强度 (0-1)")
    gen.add_argument("--restore-faces", action="store_true", help="启用人脸修复")
    gen.add_argument("--tiling", action="store_true", help="启用无缝平铺")
    gen.add_argument("--styles", nargs="+", help="应用的样式名称")

    # Hires fix
    hr = parser.add_argument_group("高清修复 (Hires Fix)")
    hr.add_argument("--enable-hr", action="store_true", help="启用高清修复")
    hr.add_argument("--hr-scale", type=float, default=2.0, help="放大倍率")
    hr.add_argument("--hr-upscaler", default="R-ESRGAN 4x+", help="放大算法")
    hr.add_argument("--hr-steps", type=int, default=15, help="高清修复步数")

    # Image inputs
    img = parser.add_argument_group("图像输入")
    img.add_argument("--init-image", help="初始图像路径 (img2img/inpaint)")
    img.add_argument("--mask-image", help="蒙版图像路径 (inpaint)")
    img.add_argument("--image", help="输入图像路径 (upscale/interrogate)")
    img.add_argument("--resize-mode", type=int, default=0, help="调整大小模式 (0=缩放, 1=裁剪, 2=填充)")

    # Inpainting
    inpaint_grp = parser.add_argument_group("局部重绘参数")
    inpaint_grp.add_argument("--inpainting-fill", type=int, default=1,
                              help="蒙版填充模式 (0=填充,1=原始,2=潜空间噪声,3=潜空间无)")
    inpaint_grp.add_argument("--inpaint-full-res", action="store_true", help="全分辨率重绘")

    # ControlNet
    cn = parser.add_argument_group("ControlNet 参数")
    cn.add_argument("--control-image", help="ControlNet 参考图像路径")
    cn.add_argument("--control-module", default="openpose", help="ControlNet 模块 (预处理器)")
    cn.add_argument("--control-model", default="", help="ControlNet 模型名称")
    cn.add_argument("--control-weight", type=float, default=1.0, help="ControlNet 权重")

    # Upscaling
    up = parser.add_argument_group("放大参数")
    up.add_argument("--upscaler", default="R-ESRGAN 4x+", help="放大算法")
    up.add_argument("--scale", type=float, default=2.0, help="放大倍率")
    up.add_argument("--codeformer-visibility", type=float, default=0.0, help="CodeFormer 人脸修复强度")

    # Interrogate
    interr = parser.add_argument_group("图像分析参数")
    interr.add_argument("--interrogate-model", default="clip", choices=["clip", "deepdanbooru"],
                        help="图像分析模型")

    # Model
    model_grp = parser.add_argument_group("模型参数")
    model_grp.add_argument("--model-name", help="模型名称 (用于 switch-model)")

    # Output
    out = parser.add_argument_group("输出参数")
    out.add_argument("--output-dir", default=SD_OUTPUT_DIR, help="输出目录")

    return parser


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = build_parser()
    args = parser.parse_args()

    action_map = {
        "status": action_status,
        "list-models": action_list_models,
        "list-samplers": action_list_samplers,
        "list-upscalers": action_list_upscalers,
        "list-loras": action_list_loras,
        "list-vaes": action_list_vaes,
        "progress": action_progress,
        "skip": action_skip,
        "interrupt": action_interrupt,
    }

    # No-arg actions
    if args.action in action_map:
        if args.action == "switch-model":
            if not args.model_name:
                print("❌ 需要提供 --model-name 参数")
                sys.exit(1)
            action_switch_model(args.model_name)
        else:
            action_map[args.action]()
        return

    # Actions with args
    try:
        if args.action == "switch-model":
            if not args.model_name:
                print("❌ 需要提供 --model-name 参数")
                sys.exit(1)
            action_switch_model(args.model_name)
        elif args.action == "txt2img":
            action_txt2img(args)
        elif args.action == "img2img":
            action_img2img(args)
        elif args.action == "inpaint":
            action_inpaint(args)
        elif args.action == "txt2img-controlnet":
            action_txt2img_controlnet(args)
        elif args.action == "upscale":
            action_upscale(args)
        elif args.action == "interrogate":
            action_interrogate(args)
        elif args.action == "png-info":
            action_png_info(args)
    except requests.exceptions.ConnectionError:
        print(f"\n❌ 无法连接到 SD WebUI ({SD_WEBUI_URL})")
        print("   请确认:")
        print("   1. SD WebUI 已启动并添加 --api 参数")
        print("   2. SD_WEBUI_URL 环境变量设置正确")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"\n⏰ 请求超时 (>{SD_TIMEOUT}秒)")
        print("   可设置 SD_TIMEOUT 环境变量增加超时时间")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
