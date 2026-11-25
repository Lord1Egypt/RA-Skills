# -*- coding: utf-8 -*-
"""构图卡口播兜底合成（确定性）——skill-promo-video v2

用途：当 H3-TALK 对「人物+卡面文字」同框的首帧发生文字融化/构图漂移时
（pitfalls #34），改走两路合成：
  1. 人物帧：PE 生成「人物左置、右侧干净墙面、无任何文字」的口播首帧 → H3-TALK（无文字可融化）
  2. 文字面板：源构图卡（已逐字验收）右半裁片 = 静态 PNG，零生成零漂移
本脚本把静态面板羽化叠加到人物视频右部，输出最终卡段。

⛔ 面板必须来自逐字验收过的源卡；人物首帧必须无文字（否则融化风险照旧）。
⛔ 这不是面部窗口：不裁人脸不贴脸，人物视频整帧保真，面板只覆盖无人物的右侧区域。

用法：
  python3 card_composite.py --person-video seg_left.mp4 --panel source_card.png \
      --panel-left 0.38 --feather 48 --out card_final.mp4
"""
import argparse, os, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--person-video", required=True)
    ap.add_argument("--panel", required=True, help="源构图卡 PNG（逐字验收过）")
    ap.add_argument("--panel-left", type=float, default=0.38,
                    help="面板覆盖起点（画面宽度比例；人物须在此线左侧）")
    ap.add_argument("--feather", type=int, default=48, help="面板左缘羽化像素")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert os.path.exists(a.person_video) and os.path.exists(a.panel)

    from PIL import Image
    W, H, FL = a.width, a.height, a.feather
    x0 = int(W * a.panel_left)
    # 面板：源卡裁掉左侧 (1-panel_left) 区域 → 缩放到覆盖区 → 左缘羽化 alpha
    src = Image.open(a.panel).convert("RGB")
    crop = src.crop((int(src.width * a.panel_left), 0, src.width, src.height))
    panel = crop.resize((W - x0, H), Image.LANCZOS).convert("RGBA")
    import numpy as np
    mask_arr = np.full((H, W - x0), 255, dtype=np.uint8)
    ramp = (np.linspace(0, 1, max(2, FL)) ** 1.5 * 255).astype(np.uint8)
    mask_arr[:, :FL] = ramp[None, :]
    panel.putalpha(Image.fromarray(mask_arr))
    tmpd = tempfile.mkdtemp(prefix="spv_comp_")
    panel_path = os.path.join(tmpd, "panel.png")
    panel.save(panel_path)

    # 视频：人物帧归一 → overlay 面板
    cmd = ["ffmpeg", "-y", "-i", a.person_video, "-loop", "1", "-framerate", "30",
           "-t", "%.2f" % probe(a.person_video), "-i", panel_path,
           "-filter_complex",
           ("[0:v]scale=%d:%d:force_original_aspect_ratio=decrease,pad=%d:%d:(ow-iw)/2:(oh-ih)/2,"
            "setsar=1,fps=30[base];[base][1:v]overlay=%d:0:format=auto" % (W, H, W, H, x0)),
           "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
           "-movflags", "+faststart", a.out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-400:]
    print("COMPOSITE OK:", a.out, "%.2fs" % probe(a.out))


if __name__ == "__main__":
    main()
