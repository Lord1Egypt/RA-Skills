# -*- coding: utf-8 -*-
"""口播段统一生成器（双引擎决策）——skill-promo-video v2

决策树（详见 references/digital-human.md）：
  音频 ≤5.1s（≤122 帧@24fps）→ H3-TALK（ref2va 音频驱动，口型天生同步，8 步 INT8，~13min/段）
  音频 >5.1s                 → S2V 720p（Wan2.2-S2V，16fps，4n+1 帧；Lightning 4 步）
  无音频/仅微动              → H3-I2V（严格首帧活体；⛔有文字对位的卡不用 r2v——构图漂移）

纪律：
  - ⛔所有生成段输出音轨一律 -an 剥掉（引擎会混入无意义自动音轨/源音轨，成片旁白统一由
    compose_3step.py adelay 注入）；本脚本自动完成 + ffprobe 复验单视频流零音轨
  - 提交前 object_info 节点名预检（防节点改名静默失败）；模型在盘预检
  - S2V 必须 720p 原生（480p 非原生=口型放大后"香肠嘴"根因）；cfg=1 时负向词无效，
    唇妆/质感约束全写正向 prompt
  - S2V 音频编码器必须 wav2vec2 large_english（chinese-base 13vs25 维度报错）

用法：
  python3 talking_segment.py --ref first_frame.png --audio narr.wav --prefix s03 \
      --out segs/s03.mp4 \
      --scene-prompt "现代诊室暖光背景，固定机位，中景构图" \
      --h3-url http://127.0.0.1:8189 --h3-root <ComfyUI-H3实例根目录>
输出：<prefix>.mp4（无声）+ <prefix>_qc/ 抽帧（口型三帧+首尾帧）。
"""
import argparse, json, math, os, shutil, subprocess, sys, time, uuid

sys.stdout.reconfigure(encoding="utf-8")

H3_NODES_BASE = ["VAELoader", "VAEDecodeAudio", "VAEDecode", "KSamplerSelect", "BasicScheduler",
                 "SamplerCustomAdvanced", "BasicGuider", "UNETLoader", "CLIPLoader", "RandomNoise",
                 "CreateVideo", "LoadImage", "PrimitiveStringMultiline", "SaveVideo",
                 "MiniMaxH3ImageToVideo", "MiniMaxH3ReferenceToVideo"]
H3_NODES_TALK = ["LoadAudio", "H3ReferenceAudio"]
H3_MODELS = ["minimax_h3_ref2va_pruned_int8_convrot.safetensors",
             "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
             "minimax_h3_video_vae_fp16.safetensors", "minimax_h3_audio_vae_fp32.safetensors"]
S2V_NODES = ["UnetLoaderGGUF", "LoraLoaderModelOnly", "CLIPLoader", "VAELoader", "AudioEncoderLoader",
             "LoadImage", "LoadAudio", "CLIPTextEncode", "AudioEncoderEncode", "ModelSamplingSD3",
             "WanSoundImageToVideo", "KSampler", "VAEDecode", "SaveVideo"]


def sh(cmd, timeout=30):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def audio_seconds(path):
    r = sh(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(r.stdout.strip())


def preflight(base_url, nodes, h3_models=None):
    """节点名+模型在位预检（以实例 object_info 清单为准，无文件系统假设）。"""
    obj = json.loads(sh(["curl", "-s", "--max-time", "8", base_url + "/object_info"]).stdout)
    missing = [c for c in nodes if c not in obj]
    assert not missing, "节点缺失: %s" % missing
    if h3_models:
        lists = {}
        for cls in ("UNETLoader", "CLIPLoader", "VAELoader"):
            r = json.loads(sh(["curl", "-s", base_url + "/object_info/" + cls]).stdout)
            key = {"UNETLoader": "unet_name", "CLIPLoader": "clip_name", "VAELoader": "vae_name"}[cls]
            lists[cls] = set(r[cls]["input"]["required"][key][0])
        dit, te, vae_v, vae_a = h3_models
        assert dit in lists["UNETLoader"], "DiT 不在实例清单: " + dit
        assert te in lists["CLIPLoader"], "TE 不在实例清单: " + te
        assert vae_v in lists["VAELoader"], "video VAE 不在实例清单: " + vae_v
        assert vae_a in lists["VAELoader"], "audio VAE 不在实例清单: " + vae_a
    print("preflight ok")


def strip_audio(src, dst):
    r = sh(["ffmpeg", "-y", "-i", src, "-an", "-c:v", "copy", dst])
    assert r.returncode == 0 and os.path.exists(dst), "strip audio 失败: " + r.stderr[-300:]
    probe = json.loads(sh(["ffprobe", "-v", "quiet", "-print_format", "json",
                           "-show_streams", dst]).stdout)
    kinds = [s["codec_type"] for s in probe.get("streams", [])]
    assert kinds == ["video"], "剥音轨后仍含非视频流: %s" % kinds


def qc_frames(mp4, outdir, prefix):
    os.makedirs(outdir, exist_ok=True)
    dur = audio_seconds(mp4)
    frames = []
    for tag, pct in [("first", 0.02), ("q25", 0.25), ("q50", 0.50), ("q75", 0.75), ("last", 0.98)]:
        t = max(0.0, min(dur - 0.05, dur * pct))
        f = os.path.join(outdir, "%s_%s.png" % (prefix, tag))
        r = sh(["ffmpeg", "-y", "-ss", "%.2f" % t, "-i", mp4, "-frames:v", "1", f])
        if r.returncode == 0:
            frames.append(f)
    return frames


def run_h3(a, mode, length):
    preflight(a.h3_url, H3_NODES_BASE + (H3_NODES_TALK if mode == "talking" else []), H3_MODELS)
    shutil.copyfile(a.ref, os.path.join(a.h3_input, os.path.basename(a.ref)))
    img = os.path.basename(a.ref)
    prompt = (a.scene_prompt.strip() + " " if a.scene_prompt else "")
    if mode == "talking":
        shutil.copyfile(a.audio, os.path.join(a.h3_input, os.path.basename(a.audio)))
        aud = os.path.basename(a.audio)
        prompt += ("Use <Picture 1> as the identity reference. The same woman speaks directly to the "
                   "camera; her lip movements match <Audio 1> exactly. Natural restrained talking to "
                   "camera, steady posture, small head/shoulder gestures, natural blinks and breathing, "
                   "fixed camera, medium shot")
        graph_talk = {
            "119": {"class_type": "VAELoader", "inputs": {"vae_name": H3_MODELS[2]}},
            "120": {"class_type": "VAELoader", "inputs": {"vae_name": H3_MODELS[3]}},
            "121": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["125", 0], "vae": ["120", 0]}},
            "122": {"class_type": "VAEDecode", "inputs": {"samples": ["125", 0], "vae": ["119", 0]}},
            "123": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
            "124": {"class_type": "BasicScheduler", "inputs": {"model": ["127", 0], "scheduler": "beta",
                    "steps": a.steps, "denoise": 1.0}},
            "125": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["129", 0], "guider": ["126", 0],
                    "sampler": ["123", 0], "sigmas": ["124", 0], "latent_image": ["136", 1]}},
            "126": {"class_type": "BasicGuider", "inputs": {"model": ["127", 0], "conditioning": ["136", 0]}},
            "127": {"class_type": "UNETLoader", "inputs": {"unet_name": H3_MODELS[0], "weight_dtype": "default"}},
            "128": {"class_type": "CLIPLoader", "inputs": {"clip_name": H3_MODELS[1], "type": "minimax"}},
            "129": {"class_type": "RandomNoise", "inputs": {"noise_seed": a.seed}},
            "130": {"class_type": "CreateVideo", "inputs": {"images": ["122", 0], "audio": ["121", 0], "fps": 24}},
            "137": {"class_type": "LoadImage", "inputs": {"image": img}},
            "138": {"class_type": "PrimitiveStringMultiline", "inputs": {"value": prompt}},
            "139": {"class_type": "LoadAudio", "inputs": {"audio": aud}},
            "140": {"class_type": "H3ReferenceAudio", "inputs": {"audio": ["139", 0], "max_seconds": 8.0}},
            "136": {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": {
                "clip": ["128", 0], "vae": ["119", 0], "audio_vae": ["120", 0],
                "prompt": ["138", 0], "width": a.width, "height": a.height, "length": length,
                "ref_image_size": "max", "ref_images.ref_image_0": ["137", 0],
                "ref_audios.ref_audio_0": ["140", 0]}},
            "92": {"class_type": "SaveVideo", "inputs": {"video": ["130", 0], "filename_prefix": a.prefix,
                   "format": "auto", "codec": "auto"}},
        }
    else:
        prompt += ("Use <Picture 1> as the identity reference. The same woman stays in place, alive and "
                   "natural: gentle breathing, subtle head and shoulder sway, soft blinks, lips gently "
                   "closed. Composition and camera completely fixed, only subtle natural micro-motion, "
                   "medium shot")
        graph_talk = {
            "119": {"class_type": "VAELoader", "inputs": {"vae_name": H3_MODELS[2]}},
            "122": {"class_type": "VAEDecode", "inputs": {"samples": ["125", 0], "vae": ["119", 0]}},
            "123": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
            "124": {"class_type": "BasicScheduler", "inputs": {"model": ["127", 0], "scheduler": "beta",
                    "steps": a.steps, "denoise": 1.0}},
            "125": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["129", 0], "guider": ["126", 0],
                    "sampler": ["123", 0], "sigmas": ["124", 0], "latent_image": ["136", 1]}},
            "126": {"class_type": "BasicGuider", "inputs": {"model": ["127", 0], "conditioning": ["136", 0]}},
            "127": {"class_type": "UNETLoader", "inputs": {"unet_name": H3_MODELS[0], "weight_dtype": "default"}},
            "128": {"class_type": "CLIPLoader", "inputs": {"clip_name": H3_MODELS[1], "type": "minimax"}},
            "129": {"class_type": "RandomNoise", "inputs": {"noise_seed": a.seed}},
            "130": {"class_type": "CreateVideo", "inputs": {"images": ["122", 0], "fps": 24}},
            "137": {"class_type": "LoadImage", "inputs": {"image": img}},
            "138": {"class_type": "PrimitiveStringMultiline", "inputs": {"value": prompt}},
            "136": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {
                "clip": ["128", 0], "vae": ["119", 0], "prompt": ["138", 0],
                "width": a.width, "height": a.height, "length": length, "first_frame": ["137", 0]}},
            "92": {"class_type": "SaveVideo", "inputs": {"video": ["130", 0], "filename_prefix": a.prefix,
                   "format": "auto", "codec": "auto"}},
        }
    return submit_and_wait(a.h3_url, graph_talk, os.path.join(a.h3_root, "output"))


def run_s2v(a):
    base = a.s2v_root
    rel = ["models/diffusion_models/Wan2.2-S2V-14B-Q5_K_M.gguf",
           "models/audio_encoders/wav2vec2_large_english_fp16.safetensors",
           "models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
           "models/vae/wan_2.1_vae.safetensors",
           "models/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors"]
    for m in rel:
        assert os.path.exists(os.path.join(base, m)), "模型缺失: " + m
    preflight(a.s2v_url, S2V_NODES)
    for f in (a.ref, a.audio):
        shutil.copyfile(f, os.path.join(base, "input", os.path.basename(f)))
    sec = audio_seconds(a.audio)
    length = int(math.ceil(sec * 16))
    length = length - (length % 4) + 1
    assert length >= 33, "音频过短"
    use_lora = a.s2v_steps <= 4
    pos = a.s2v_prompt.strip() or (
        "一位端庄优雅的年轻女性，正面面对镜头讲话，嘴唇随讲话内容自然张合，口型清晰同步，"
        "清透的浅色唇妆，口型开合幅度自然适中，头部随语气轻微自然晃动，手势轻柔配合讲解内容，"
        "表情亲切自信，眼神注视镜头，背景干净，柔和摄影灯光，皮肤质感真实，高清细节，"
        "画面稳定，固定机位，中景构图")
    neg = ("色调艳丽，过曝，静态，细节模糊不清，字幕，画作，整体发灰，最差质量，低质量，"
           "残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，形态畸形的肢体，"
           "手指融合，浓艳的深红色口红，嘴唇肥厚肿大，嘴巴过大，口型夸张，嘴唇变形")
    graph = {
        "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": "Wan2.2-S2V-14B-Q5_K_M.gguf"}},
        "10a": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0],
                "lora_name": "wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors",
                "strength_model": 1.0}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
               "type": "wan", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "wan_2.1_vae.safetensors"}},
        "4": {"class_type": "AudioEncoderLoader", "inputs": {"audio_encoder_name": "wav2vec2_large_english_fp16.safetensors"}},
        "5": {"class_type": "LoadImage", "inputs": {"image": os.path.basename(a.ref)}},
        "6": {"class_type": "LoadAudio", "inputs": {"audio": os.path.basename(a.audio)}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": pos}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": neg}},
        "9": {"class_type": "AudioEncoderEncode", "inputs": {"audio_encoder": ["4", 0], "audio": ["6", 0]}},
        "10": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["10a" if use_lora else "1", 0], "shift": 8.0}},
        "11": {"class_type": "WanSoundImageToVideo", "inputs": {
            "positive": ["7", 0], "negative": ["8", 0], "vae": ["3", 0],
            "width": a.width, "height": a.height, "length": length, "batch_size": 1,
            "audio_encoder_output": ["9", 0], "ref_image": ["5", 0]}},
        "12": {"class_type": "KSampler", "inputs": {
            "model": ["10", 0], "positive": ["11", 0], "negative": ["11", 1], "latent_image": ["11", 2],
            "seed": a.seed, "steps": a.s2v_steps, "cfg": a.cfg, "sampler_name": "euler", "scheduler": "simple",
            "denoise": 1.0}},
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["3", 0]}},
        "14": {"class_type": "SaveVideo", "inputs": {"images": ["13", 0], "filename_prefix": a.prefix,
               "format": "auto", "codec": "auto"}},
    }
    return submit_and_wait(a.s2v_url, graph, os.path.join(base, "output"))


def submit_and_wait(base_url, graph, out_root, timeout_min=60.0):
    cid = str(uuid.uuid4())
    r = sh(["curl", "-s", "-H", "Content-Type: application/json",
            "-d", json.dumps({"prompt": graph, "client_id": cid}), base_url + "/prompt"], timeout=60)
    resp = json.loads(r.stdout)
    if "prompt_id" not in resp:
        print("SUBMIT FAIL:", json.dumps(resp, ensure_ascii=False)[:1500], flush=True)
        sys.exit(1)
    pid = resp["prompt_id"]
    print("prompt_id:", pid, "t0:", time.strftime("%H:%M:%S"), flush=True)
    t0 = time.time()
    while True:
        time.sleep(20)
        h = json.loads(sh(["curl", "-s", base_url + "/history/" + pid], timeout=30).stdout or "{}")
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("completed"):
                if st.get("status_str") == "error":
                    msgs = [m for m in st.get("messages", []) if m[0] == "execution_error"]
                    print("EXEC ERROR:", json.dumps(msgs, ensure_ascii=False)[:2000], flush=True)
                    sys.exit(2)
                for _n, node in h[pid].get("outputs", {}).items():
                    for key in ("images", "gifs", "videos"):
                        for o in node.get(key, []):
                            full = os.path.join(out_root, o.get("subfolder", ""), o["filename"])
                            if os.path.exists(full):
                                print("OUT:", full, "DONE %.1f min" % ((time.time() - t0) / 60), flush=True)
                                return full
                print("completed but no output file found", flush=True)
                sys.exit(3)
        if (time.time() - t0) > timeout_min * 60:
            print("TIMEOUT waiting", pid, flush=True)
            sys.exit(4)
        print("[%4.1fm] waiting" % ((time.time() - t0) / 60), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True, help="首帧图（人物口播位）")
    ap.add_argument("--audio", default="", help="旁白 wav；空=微动模式(H3-I2V)")
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--out", required=True, help="最终无声 mp4 输出路径")
    ap.add_argument("--engine", choices=["auto", "h3", "s2v", "h3-i2v"], default="auto")
    ap.add_argument("--scene-prompt", default="", help="H3 口播场景提示（背景/构图；默认通用口播描述）")
    ap.add_argument("--s2v-prompt", default="", help="S2V 正向提示（人物+服饰+场景，负向无效全写正向）")
    ap.add_argument("--seed", type=int, default=61584)
    ap.add_argument("--steps", type=int, default=8, help="H3 步数（8）；S2V 下 ≤4 启用 Lightning LoRA")
    ap.add_argument("--cfg", type=float, default=1.0)
    ap.add_argument("--s2v-steps", type=int, default=4,
                    help="S2V 步数（默认 4=Lightning LoRA；20=全质量约 2h/段）")
    ap.add_argument("--width", type=int, default=1344)
    ap.add_argument("--height", type=int, default=768)
    ap.add_argument("--h3-url", default="http://127.0.0.1:8189")
    ap.add_argument("--h3-root", default=os.path.join(os.path.expanduser("~"), "ComfyUI-H3"))
    ap.add_argument("--s2v-url", default="http://127.0.0.1:8188")
    ap.add_argument("--s2v-root", default=os.path.join(os.path.expanduser("~"), "ComfyUI"))
    ap.add_argument("--s2v-width", type=int, default=1280)
    ap.add_argument("--s2v-height", type=int, default=720)
    ap.add_argument("--timeout-min", type=float, default=45.0)
    a = ap.parse_args()

    assert os.path.exists(a.ref), "首帧不存在: " + a.ref
    a.h3_input = os.path.join(a.h3_root, "input")
    if not os.path.isdir(a.h3_input):
        a.h3_input = os.path.join(a.s2v_root, "input")

    engine = a.engine
    if engine == "auto":
        if not a.audio:
            engine = "h3-i2v"
        else:
            sec = audio_seconds(a.audio)
            engine = "h3" if sec <= 5.1 else "s2v"
            print("auto engine:", engine, "(audio %.2fs)" % sec)
    engine = {"h3": "talking", "h3-i2v": "i2v"}.get(engine, engine)

    if engine in ("talking", "i2v"):
        length = 124 if engine == "i2v" else min(124, max(33, int(math.ceil(audio_seconds(a.audio) * 24)) + 4))
        assert length <= 124, "H3 单 clip 上限 124 帧；更长旁白用 s2v 引擎"
        src = run_h3(a, engine, length)
    else:
        assert a.audio, "s2v 必须给 --audio"
        src = run_s2v(a)

    strip_audio(src, a.out)
    frames = qc_frames(a.out, os.path.join(os.path.dirname(a.out) or ".", a.prefix + "_qc"), a.prefix)
    print("QC frames:", len(frames), "->", os.path.dirname(frames[0]) if frames else "-")
    print("SEGMENT OK:", a.out, "%.2fs" % audio_seconds(a.out))


if __name__ == "__main__":
    main()
