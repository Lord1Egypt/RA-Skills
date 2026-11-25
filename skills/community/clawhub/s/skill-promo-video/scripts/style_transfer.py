# -*- coding: utf-8 -*-
"""风格化重绘（Qwen-Image-Edit-2511 Plus）——skill-promo-video v2

用途：Blender 素模/白模渲染图 → 按参考图风格重绘（结构保持，风格替换）。
可选模块：若 Blender 直渲观感已达标则跳过（少一次 AI 漂移面）。

配方（已验证）：
  UNETLoader(qwen_image_edit_2511_fp8mixed) + CLIPLoader(qwen_2.5_vl_7b_fp8_scaled, qwen_image)
  + TextEncodeQwenImageEditPlus 双节点(正/负) + ModelSamplingAuraFlow(shift 3.1)
  + CFGNorm(1.0) + KSampler(euler/simple/20步/cfg4.0/denoise1.0)
  + latent=VAEEncode(原图)；具名输入 image1/image2（指令按 <Picture N> 引用）

用法：
  python3 style_transfer.py --image raw.png --ref style_ref.png \
      --instruction "按图2风格渲染图1场景，保持构图与结构完全不变" \
      --out styled.png --input-dir <ComfyUI实例input目录> --output-dir <同实例output目录>
"""
import argparse, json, os, shutil, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8")


def build_graph(image_name, ref_name, instruction, seed, prefix):
    pos = ("<Picture 1>: the scene to restyle. <Picture 2>: the style reference. " + instruction)
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "qwen_image_edit_2511_fp8mixed.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "10": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "11": {"class_type": "LoadImage", "inputs": {"image": ref_name}},
        "5p": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["2", 0], "vae": ["3", 0],
               "prompt": pos, "image1": ["10", 0], "image2": ["11", 0]}},
        "5n": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["2", 0], "vae": ["3", 0],
               "prompt": "", "image1": ["10", 0], "image2": ["11", 0]}},
        "6a": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.1}},
        "6b": {"class_type": "CFGNorm", "inputs": {"model": ["6a", 0], "strength": 1.0}},
        "6": {"class_type": "KSampler", "inputs": {"model": ["6b", 0], "positive": ["5p", 0], "negative": ["5n", 0],
               "latent_image": ["5p", 2], "seed": seed, "steps": 20, "cfg": 4.0,
               "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["3", 0]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": prefix}},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--ref", required=True, help="风格参考图")
    ap.add_argument("--instruction", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--edit-url", default="http://127.0.0.1:8190")
    ap.add_argument("--input-dir", required=True, help="ComfyUI 实例 input 目录（LoadImage 从这里读）")
    ap.add_argument("--output-dir", required=True, help="ComfyUI 实例 output 目录（回捞）")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--timeout-min", type=float, default=15.0)
    a = ap.parse_args()
    assert os.path.exists(a.image) and os.path.exists(a.ref)

    for f in (a.image, a.ref):
        dst = os.path.join(a.input_dir, os.path.basename(f))
        if os.path.abspath(f) != os.path.abspath(dst):
            shutil.copyfile(f, dst)

    prefix = "spv_style_%d" % int(time.time())
    graph = build_graph(os.path.basename(a.image), os.path.basename(a.ref), a.instruction, a.seed, prefix)
    import tempfile
    pf = os.path.join(tempfile.mkdtemp(prefix="spv_style_"), "payload.json")
    json.dump({"prompt": graph}, open(pf, "w"), ensure_ascii=False)
    r = subprocess.run(["curl", "-s", "-m", "30", "-X", "POST", "-H", "Content-Type: application/json",
                        "-d", "@" + pf, a.edit_url + "/prompt"], capture_output=True, text=True)
    resp = json.loads(r.stdout)
    assert "prompt_id" in resp, "SUBMIT FAIL: " + r.stdout[:300]
    pid = resp["prompt_id"]
    t0 = time.time()
    while (time.time() - t0) < a.timeout_min * 60:
        time.sleep(10)
        h = json.loads(subprocess.run(["curl", "-s", a.edit_url + "/history/" + pid],
                                      capture_output=True, text=True).stdout or "{}")
        node = h.get(pid)
        if not node:
            continue
        st = node.get("status", {})
        if st.get("status_str") == "error":
            print("EXEC ERROR"); sys.exit(2)
        if not st.get("completed"):
            continue
        for _n, out in node.get("outputs", {}).items():
            for im in out.get("images", []):
                src = os.path.join(a.output_dir, im.get("subfolder", ""), im["filename"])
                if os.path.exists(src) and os.path.getsize(src) > 100_000:
                    shutil.copyfile(src, a.out)
                    print("STYLE OK:", a.out, os.path.getsize(src), "B")
                    return
        print("completed, no output"); sys.exit(3)
    print("TIMEOUT"); sys.exit(4)


if __name__ == "__main__":
    main()
