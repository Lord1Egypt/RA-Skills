#!/usr/bin/env python3
"""
用 gpt-image-2(经 Ofox 中转，OpenAI 兼容)生成爆款封面图，远好于纯 ffmpeg 文字封面。
读取 covers.json（见 examples/covers.example.json）。

环境变量：OFOX_API_KEY（首选）或 OPENROUTER_API_KEY。
⚠️ 必须直连，别走本地代理：运行前 `unset http_proxy https_proxy all_proxy`，
   否则 Ofox 大图响应常 SSL EOF / Connection refused。脚本对每张做了重试。

用法: unset http_proxy https_proxy all_proxy; python3 gen_covers_ai.py --config covers.json
"""
import argparse, base64, json, os, time, urllib.request

OFOX_URL = "https://api.ofox.ai/v1/images/generations"
MODEL = "gpt-image-2"   # 注意：gpt-image-1 在 Ofox 上是 404

# 两种已验证有效的爆款风格模板（科技/AI 赛道）
STYLES = {
 # 酷炫赛博风：深色 + 电光绿 + 发光终端 + 光带分割（点击力强、辨识度高）
 "cyber": ("小红书竖版封面 3:4，极简而高级的未来科技感，强爆款点击力。做减法、大量深色留白、只聚焦一个主视觉。"
           "纯黑到深蓝干净渐变背景。主视觉只有一块发光的终端命令行窗口(青绿等宽字体、简洁真实的代码，大致内容：{terminal})，"
           "窗口外大片深色留白和极少细光线，不要发光大脑、不要堆砌粒子。标志性强调色：电光绿做点睛高亮。"
           "构图用一条利落的水平光带把画面干净分割。文字(粗体清晰准确简体中文极强层级不要乱码)："
           "顶部发光小胶囊标签『{eyebrow}』；中间超大主标题『{title}』(其中『{highlight}』用电光绿霓虹高亮、最大最亮)；"
           "底部一行小字『{subtitle}』。整体克制、高级、冷峻、信息差感强、忍不住点。"),
 # 柔和科技卡片风：奶油薄荷 + 圆角卡片 + 扁平图标（小红书原生、门槛低）
 "soft":  ("小红书竖版封面 3:4，柔和高级的科技卡片风，爆款点击力强、干净不廉价。"
           "奶油白到极淡薄荷渐变背景，大量留白，中间一张圆角白色卡片带极淡柔和阴影。"
           "卡片上一个可爱简洁的扁平3D小图标({icon})。标志性强调色：明亮珊瑚橙做高亮。"
           "文字(粗体清晰准确简体中文强层级不要乱码)：左上圆角小标签『{eyebrow}』；"
           "主标题大字『{title}』(其中『{highlight}』用珊瑚橙马克笔高亮)；利益副标小字『{subtitle}』。"
           "整体亲切、干净、高级、利益点直给、一眼想点。"),
}

def key():
    k = os.environ.get("OFOX_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not k: raise SystemExit("缺 OFOX_API_KEY / OPENROUTER_API_KEY")
    return k

def gen(prompt, out, tries=6):
    for t in range(1, tries+1):
        try:
            payload = json.dumps({"model": MODEL, "prompt": prompt, "size": "1024x1536", "n": 1}).encode()
            req = urllib.request.Request(OFOX_URL, data=payload,
                headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
            d = json.loads(urllib.request.urlopen(req, timeout=300).read())["data"][0]
            data = base64.b64decode(d["b64_json"]) if d.get("b64_json") else urllib.request.urlopen(d["url"]).read()
            open(out, "wb").write(data); return True
        except Exception as e:
            print(f"    重试{t}: {str(e)[:70]}", flush=True); time.sleep(4)
    return False

def to_3x4(src, dst):
    try:
        from PIL import Image
        im = Image.open(src).convert("RGB"); w, h = im.size; tw = int(round(h*3/4))
        c = Image.new("RGB", (tw, h), (0, 0, 0)); c.paste(im, ((tw-w)//2, 0)); c.save(dst, quality=92)
    except Exception:
        pass

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    style = STYLES[cfg.get("style", "cyber")]
    out_dir = os.path.expanduser(cfg["output_dir"]); os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "3x4"), exist_ok=True)
    for i, c in enumerate(cfg["covers"], 1):
        p = style.format(eyebrow=c.get("eyebrow", ""), title=c["title"], highlight=c.get("highlight", ""),
                         subtitle=c.get("subtitle", ""), terminal=c.get("terminal", ""), icon=c.get("icon", "一个相关的小图标"))
        out = os.path.join(out_dir, f"{c['name']}.png")
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print(f"[{i}] 跳过 {c['name']}"); continue
        ok = gen(p, out)
        if ok: to_3x4(out, os.path.join(out_dir, "3x4", f"{c['name']}.jpg"))
        print(f"[{i}] {'✅' if ok else '❌'} {c['name']}", flush=True)
    print("=== 封面完成 ===")

if __name__ == "__main__":
    main()
