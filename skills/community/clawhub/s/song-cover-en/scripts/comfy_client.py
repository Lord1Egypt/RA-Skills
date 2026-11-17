"""ComfyUI API 客户端：向本地 ComfyUI 提交 Z-Image-Turbo 文生图任务并取回图片。"""
import json, sys, time, urllib.request, urllib.error, urllib.parse, os, uuid

HOST = os.environ.get("COMFY_HOST", "http://127.0.0.1:8188")
# 本机回环不走系统代理/VPN
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def api(path, data=None, method=None):
    url = HOST + path
    body = None
    headers = {"User-Agent": "dsh-comfy-client"}
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with _OPENER.open(req, timeout=60) as r:
        raw = r.read()
        ct = r.headers.get("Content-Type", "")
        return json.loads(raw) if "json" in ct else raw


def build_workflow(prompt, negative="", width=1024, height=1024, steps=8, seed=None, prefix="dsh"):
    seed = seed if seed is not None else int(time.time() * 1000) % (2**48)
    neg = negative or ""
    wf = {
        "30": {"class_type": "CLIPLoader",
               "inputs": {"clip_name": "qwen_3_4b_fp8_mixed.safetensors", "type": "lumina2", "device": "default"}},
        "29": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "28": {"class_type": "UNETLoader",
               "inputs": {"unet_name": "z_image_turbo_int8_convrot.safetensors", "weight_dtype": "default"}},
        "27": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["30", 0]}},
        "13": {"class_type": "EmptySD3LatentImage",
               "inputs": {"width": width, "height": height, "batch_size": 1}},
        "11": {"class_type": "ModelSamplingAuraFlow", "inputs": {"shift": 3, "model": ["28", 0]}},
        "3": {"class_type": "KSampler",
              "inputs": {"model": ["11", 0], "positive": ["27", 0], "negative": ["33", 0],
                         "latent_image": ["13", 0], "seed": seed, "steps": steps, "cfg": 1,
                         "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["29", 0]}},
        "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": prefix}},
    }
    if neg:
        wf["34"] = {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["30", 0]}}
        wf["3"]["inputs"]["negative"] = ["34", 0]
    else:
        wf["33"] = {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["27", 0]}}
    return wf


def generate(prompt, negative="", width=1024, height=1024, steps=8, seed=None,
             out_dir=r"D:\DSH\workspace\comfyui_out", timeout=900):
    wf = build_workflow(prompt, negative, width, height, steps, seed)
    client_id = str(uuid.uuid4())
    res = api("/prompt", {"prompt": wf, "client_id": client_id})
    pid = res["prompt_id"]
    print(f"[queued] prompt_id={pid} number={res.get('number')}", flush=True)
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = api(f"/history/{pid}")
        if pid in h:
            entry = h[pid]
            status = entry.get("status", {})
            if status.get("status_str") == "error" or status.get("completed") is False and status.get("status_str") == "error":
                print("EXECUTION ERROR:", json.dumps(status, ensure_ascii=False)[:2000], flush=True)
                return None, status
            imgs = []
            for node_id, out in entry.get("outputs", {}).items():
                for im in out.get("images", []):
                    imgs.append(im)
            if imgs:
                os.makedirs(out_dir, exist_ok=True)
                paths = []
                for im in imgs:
                    q = f"/view?filename={urllib.parse.quote(im['filename'])}&subfolder={urllib.parse.quote(im.get('subfolder',''))}&type={im.get('type','output')}"
                    data = api(q)
                    p = os.path.join(out_dir, im["filename"])
                    with open(p, "wb") as f:
                        f.write(data)
                    paths.append(p)
                    print(f"[image] {p} ({len(data)/1024:.0f} KB)", flush=True)
                print(f"[elapsed] {time.time()-t0:.1f}s", flush=True)
                return paths, entry
        time.sleep(1.5)
    print("[timeout]", flush=True)
    return None, None


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "a photo of a red apple on a wooden table, studio lighting"
    paths, _ = generate(prompt)
    print(json.dumps(paths, ensure_ascii=False) if paths else "FAILED")
