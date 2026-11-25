# -*- coding: utf-8 -*-
"""构图卡/首帧批量生成（PE 直出文字，身份锚+服饰参数化）——skill-promo-video v2

两种版式（scene.layout）：
  card    人物左+卷轴文字右（知识解说卡；卡面文字 PE 直出，禁 PIL 贴补）
  talker  口播首帧：人物中景面向镜头（H3-TALK/S2V 的 first frame；预留下方字幕净区）

纪律：
  - prompt 末尾必须附逐行核对清单；成图后逐字 OCR 复验（--wait 自动回捞+空白图护栏）
  - 参考图 API 键名必须带点嵌套 images.image_1（裸 image_1 / "images" 列表均静默失败）
  - GPU 串行：与 TTS/H3 严禁并发
  - cfg=1.0 负向提示无效：一切"避免X"必须写成正向描述

用法：
  python3 gen_scene_cards.py --config config.json --out-dir cards/ --wait \
      --ref /path/to/character_ref.png --output-dir <ComfyUI实例output目录>
config 里 character.costume / character.scene_bg 驱动服饰与场景；scene.layout 驱动版式。
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, time, zlib

sys.stdout.reconfigure(encoding="utf-8")


def person_desc(ch):
    """人物描述 = 身份锚（与参考图一致）+ 服饰/发型（config 换装即换人设）。"""
    return ("same woman from image1，五官与脸型与参考图完全一致："
            + ch["identity"].strip().rstrip("。") + "。"
            + ch["costume"].strip().rstrip("。") + "。")


def build_prompt_card(sc, ch, bg):
    lines = sc["prompt_lines"]
    pl = "、".join(f"「{x}」" for x in lines)
    return (
        "一张16:9横版知识解说画面，左人物右内容分栏构图，背景干净不繁杂。"
        "左半边是解说区：" + person_desc(ch) +
        "她侧身站立面向右方，右手指向右侧卷面，左手轻持一卷收起的卷轴于腰前，"
        "目光落在右侧卷面上，神情认真温和带笑，正在讲解。"
        "右半边是内容区：一轴素雅的宣纸长卷自上而下展开，卷面干净只有少量淡墨点缀："
        f"卷面顶端深红色漆渍笔刷横幅配白色粗体标题「{sc['title']}」；"
        "标题横幅正下方一行金色小字「—— 对智能体说 ——」，居中；"
        f"其下用毛笔行书分行书写提示词原文，共 {len(lines)} 行，依次为：{pl}；"
        "提示词下方直至卷轴下缘为大片空白宣纸区域，不绘制任何图形或纹样。"
        + bg +
        "\n文字必须逐字准确、笔画完整清晰，严格按上述拼写，"
        "不得出现除此之外的任何其他文字或乱码。空白区域必须完全空白。\n"
        "最终逐行核对（不得缺字、错字、并字、重复）：「" + sc["title"] + "」／"
        + "／".join(f"「{x}」" for x in lines) + "。空白区不得有任何图形。人物区不得出现文字。")


def build_prompt_talker(sc, ch, bg):
    """口播首帧：中景面向镜头，唇自然轻闭（开口由音频驱动），下 1/4 留字幕净区。"""
    extra = (sc.get("talker_props") or "").strip()
    return (
        "一张16:9横版人物口播画面，中景构图，背景干净不繁杂。"
        + person_desc(ch) +
        "她正面站立面向镜头，目光注视镜头，双唇自然轻闭，神情亲切自信带温和微笑，"
        "双手在身前自然交代（十指完整、每只手五指），肩颈放松，头顶留出适当空间。"
        "画面底部四分之一为干净的纯色渐变地面区域，无任何文字、图形与杂物（留给字幕）。"
        + (extra + "。" if extra else "") + bg +
        "\n画面中不得出现任何文字、水印、标志或乱码。人物结构准确，手部无畸形。")


def build_graph(prompt, ref_name, seed, prefix):
    return {
        "PE": {"class_type": "QwenPERewriteT8", "inputs": {
            "user_prompt": prompt, "task": "t2i", "aspect_ratio": "16:9",
            "output_language": "auto", "transparent_rgba": False,
            "t2i_model": "Qwen-Image-2.1-PE-T2I.Q4_K_M.gguf",
            "edit_model": "Qwen-Image-2.1-PE-T2I.Q4_K_M.gguf",
            "vision_model": "Auto", "model_lifetime": "after_run", "seed": seed}},
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "qwen_image_2.1_bf16.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_8b_int8_convrot.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "10": {"class_type": "LoadImage", "inputs": {"image": ref_name}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1536, "height": 864, "batch_size": 1}},
        # ⛔ 参考图键名带点嵌套 images.image_1，且 TE 节点必须接 vae
        "5": {"class_type": "TextEncodeQwenImage21", "inputs": {"clip": ["2", 0], "vae": ["3", 0],
               "prompt": ["PE", 0], "negative_prompt": "", "resolution": 1024,
               "images.image_1": ["10", 0]}},
        "6": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["5", 0], "negative": ["5", 1],
               "latent_image": ["4", 0], "seed": seed, "steps": 25, "cfg": 1.0,
               "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["3", 0]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": prefix}},
    }


def http_json(url, payload=None, timeout=20):
    if payload is None:
        r = subprocess.run(["curl", "-s", "-m", str(timeout), url], capture_output=True, text=True)
    else:
        pf = os.path.join(tempfile.mkdtemp(prefix="spv_pl_"), "payload.json")
        json.dump(payload, open(pf, "w"), ensure_ascii=False)
        r = subprocess.run(["curl", "-s", "-m", str(timeout), "-X", "POST", "-H",
                            "Content-Type: application/json", "-d", "@" + pf, url],
                           capture_output=True, text=True)
        os.remove(pf)
    return json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ref", required=True, help="人物身份参考图（角色卡/定妆照，用户自备）")
    ap.add_argument("--t2i-url", default="http://127.0.0.1:8190")
    ap.add_argument("--input-dir", default="", help="ComfyUI 实例的 input 目录（参考图拷入；空=假定参考图已在位）")
    ap.add_argument("--output-dir", default="", help="ComfyUI 实例的 output 目录（--wait 回捞用）")
    ap.add_argument("--wait", action="store_true", help="提交并轮询回捞到 out-dir")
    ap.add_argument("--seed", type=int, default=20261018)
    ap.add_argument("--timeout-min", type=float, default=25.0)
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding="utf-8"))
    ch = cfg["character"]
    bg = ch.get("scene_bg", "背景为干净不繁杂的纯色渐变。").strip()
    os.makedirs(a.out_dir, exist_ok=True)
    assert os.path.exists(a.ref), "身份参考图不存在: " + a.ref

    ref_name = os.path.basename(a.ref)
    if a.input_dir:
        os.makedirs(a.input_dir, exist_ok=True)
        dst = os.path.join(a.input_dir, ref_name)
        if os.path.abspath(a.ref) != os.path.abspath(dst):
            shutil.copyfile(a.ref, dst)
    if a.output_dir:
        os.makedirs(a.output_dir, exist_ok=True)

    jobs = []
    for sc in cfg["scenes"]:
        layout = sc.get("layout", "card")
        if layout == "card":
            prompt = build_prompt_card(sc, ch, bg)
        elif layout == "talker_left":
            # 人物严格左置 1/3，右 2/3 干净墙面（配合 card_composite.py 静态面板；
            # H3-TALK 对同框文字有融化风险时用此降级，见 pitfalls #34）
            prompt = build_prompt_talker(sc, ch, bg).replace(
                "一张16:9横版人物口播画面，中景构图，背景干净不繁杂。",
                "一张16:9横版人物口播画面，人物位于画面左侧三分之一（身体的右缘不超过画面宽度百分之四十），"
                "右侧三分之二为干净的暖灰色纯色渐变墙面，无任何文字、图形与杂物。中景构图。")
        elif layout == "talker":
            prompt = build_prompt_talker(sc, ch, bg)
        else:  # raw：整段自定义文案，{person}=人物描述占位
            prompt = sc["prompt"].replace("{person}", person_desc(ch) + "她")
            if sc.get("check"):
                prompt += "\n最终逐行核对（不得缺字、错字、并字、重复）：" + "／".join(
                    "「%s」" % x for x in sc["check"]) + "。"
        graph = build_graph(prompt, ref_name, a.seed + zlib.crc32(sc["id"].encode()) % 10000, "promo_" + sc["id"])
        try:
            resp = http_json(a.t2i_url + "/prompt", {"prompt": graph})
        except Exception as e:
            resp = {"err": str(e)}
        if "prompt_id" not in resp:
            print(sc["id"], "SUBMIT FAIL:", json.dumps(resp, ensure_ascii=False)[:200], flush=True)
            jobs.append((sc["id"], None))
        else:
            print(sc["id"], "submitted", resp["prompt_id"], flush=True)
            jobs.append((sc["id"], resp["prompt_id"]))

    if not a.wait:
        print("ALL SUBMITTED（未带 --wait，不回捞）")
        return

    t0 = time.time()
    pending = {pid: sid for sid, pid in jobs if pid}
    fails = [sid for sid, pid in jobs if not pid]
    while pending and (time.time() - t0) < a.timeout_min * 60:
        time.sleep(15)
        for pid in list(pending):
            try:
                h = http_json("%s/history/%s" % (a.t2i_url, pid), timeout=10)
            except Exception:
                continue
            node = h.get(pid) if isinstance(h, dict) else None
            if not node:
                continue
            st = node.get("status", {})
            if st.get("status_str") == "error":
                print(pending[pid], "EXEC ERROR", flush=True)
                fails.append(pending[pid]); pending.pop(pid); continue
            if not st.get("completed"):
                continue
            got = False
            for _n, out in node.get("outputs", {}).items():
                for im in out.get("images", []):
                    src = os.path.join(a.output_dir or ".", im.get("subfolder", ""), im["filename"])
                    if os.path.exists(src) and os.path.getsize(src) > 100_000:  # 空白图护栏
                        shutil.copyfile(src, os.path.join(a.out_dir, pending[pid] + ".png"))
                        print(pending[pid], "OK", os.path.getsize(src), "B", flush=True)
                        got = True
                    elif os.path.exists(src):
                        print(pending[pid], "SUSPECT blank/small:", src, os.path.getsize(src), "B", flush=True)
            if not got and pending[pid] not in fails:
                fails.append(pending[pid])
            pending.pop(pid)
    for pid in pending:
        print(pid, "TIMEOUT", flush=True)
        fails.append(pending[pid])
    print("BATCH", "ALL OK" if not fails else "FAILED: %s" % fails, flush=True)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
