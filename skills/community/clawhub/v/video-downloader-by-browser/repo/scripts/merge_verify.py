"""
合并分片 + 完整性校验。

用法:
    python merge_verify.py <工作目录> <输出文件.mp4> [分片目录名(默认seg)]

流程:
    1. 只合并「通过 .ok 标记校验」的分片（youku_download.py 写入；
       无标记的残留/占位文件直接拒绝，杜绝残缺分片混入 —— 2026-09 修复）
    2. 分片号显式排序（hex int(k,16)/十进制自适应；旧 natural_sort 按数字捕获组拆分，
       对十六进制字母分片号 0a/1f… 会错序，已弃用 —— 2026-09 二次修复）
       + 连续性校验（缺号直接拒绝合并，防止采集漏片静默拼接导致成片跳段）
       → 生成 concat 列表
    3. ffmpeg -c copy 无损合并（不重编码，画质零损失）+faststart
    4. 解析合并后 MP4 的时长/分辨率/编码
    5. 用「分片真实时长累计表」逐个拼接点做解码体检
       （旧版按 dur/n 假设等长，末片更短时接缝位置算偏 —— 2026-09 修复）

依赖: imageio-ffmpeg（pip install imageio-ffmpeg，自带 ffmpeg 二进制）
"""
import os
import re
import sys
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor


def sort_chunks(names):
    """按分片号显式排序 + 连续性校验，返回有序文件名列表。

    ⚠️ 2026-09 二次修复：旧版 natural_sort 用 re.split(r'(\\d+)') 拆数字再转 int，
    对十六进制分片号会错序——'chunk_0a' 被拆成 [.., 0, 'a.mp', ..] 排到 'chunk_01' 之前，
    超过 10 个分片（≈23 分钟）的视频合并顺序必乱。改为：
      - 分片号含 a-f 字母 → int(id, 16) 十六进制排序（优酷）
      - 纯数字 → int(id) 十进制排序（其他平台）
      - 命名不合规 → 拒绝（绝不猜）
      - 分片号有缺口 → 拒绝（采集漏片静默合并 = 成片跳变一段，接缝体检发现不了）
    """
    def cid(n):
        m = re.match(r'chunk_([0-9a-fA-F]+)\.mp4$', n)
        if not m:
            raise SystemExit(f'分片命名不合规（期望 chunk_<编号>.mp4）: {n}')
        return m.group(1)
    ids = {n: cid(n) for n in names}
    hex_mode = any(re.search(r'[a-fA-F]', v) for v in ids.values())
    num = (lambda v: int(v, 16)) if hex_mode else int
    ordered = sorted(names, key=lambda n: num(ids[n]))
    nums = [num(ids[n]) for n in ordered]
    if len(nums) >= 2:
        gaps = [(a, b) for a, b in zip(nums, nums[1:]) if b - a > 1]
        if gaps:
            fmt = (lambda x: f'{x:02x}') if hex_mode else str
            missing = [fmt(x) for a, b in gaps for x in range(a + 1, b)]
            raise SystemExit(f'分片号不连续，缺失: {missing}（采集/probe 漏片，拒绝合并——'
                             f'请重跑 youku_collect.py / youku_download.py 补齐）')
    if nums and nums[0] != 0:
        print(f'⚠️ 分片号从 {nums[0]} 开始而非 0（1 起始平台？继续合并，请人工确认）')
    return ordered


def get_ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ff = os.popen('which ffmpeg').read().strip()
        if ff:
            return ff
        raise SystemExit('未找到 ffmpeg，请先 pip install imageio-ffmpeg')


def main():
    root = sys.argv[1]
    out = sys.argv[2]
    segdir = sys.argv[3] if len(sys.argv) > 3 else 'seg'
    segdir = os.path.join(root, segdir)
    ff = get_ffmpeg()
    print('ffmpeg:', ff)

    all_files = [f for f in os.listdir(segdir) if f.endswith('.mp4')]
    ok_files = [f for f in all_files if os.path.exists(os.path.join(segdir, f + '.ok'))]
    # 拒绝无 .ok 标记的分片（残缺占位/手工副本一律不进合并清单）
    rejected = sorted(set(all_files) - set(ok_files))
    if rejected:
        print(f'⚠️ 拒绝 {len(rejected)} 个无 .ok 标记的分片: {rejected}')
        raise SystemExit('存在未通过校验的分片，请先重跑 youku_download.py 补齐')
    if not ok_files:
        raise SystemExit(f'{segdir} 中没有带 .ok 标记的 mp4 分片')
    files = sort_chunks(ok_files)
    print(f'共 {len(files)} 个分片（全部通过 .ok 校验）')
    print('顺序:', ' '.join(files[:6]), '...', ' '.join(files[-3:]) if len(files) > 6 else '')

    # ── 源段号权威核对：chunks_full.json 里每个分片 URL 内嵌的段号必须 == 文件 key ──
    # URL 文件名 03000C2 X HH 64..，HH 是优酷 CDN 生成的源播放顺序段号（hex）。
    # 本地 key/排序万一记错，这里能在合并前拦住（比"看画面"可靠，见 SKILL.md 踩坑表）。
    full_path = os.path.join(root, 'chunks_full.json')
    if os.path.exists(full_path):
        try:
            full = json.load(open(full_path))
            seg_re = re.compile(r'03000C2[0-9a-fA-F]([0-9a-fA-F]{2})')
            bad = []
            checked = 0
            for name in files:
                m = re.match(r'chunk_([0-9a-fA-F]+)\.mp4$', name)
                if not m:
                    continue
                key = m.group(1).lower()
                meta = full.get(key) or full.get(m.group(1))
                if not meta:
                    continue
                fn = meta['url'].split('/')[-1]
                mm = seg_re.search(fn)
                if not mm:
                    continue  # 非优酷命名（其他平台），跳过
                checked += 1
                if mm.group(1).lower() != key:
                    bad.append((key, mm.group(1).lower()))
            if checked:
                if bad:
                    raise SystemExit(
                        f'⛔ 源段号核对失败：{len(bad)} 个分片 key 与 URL 内嵌段号不一致 {bad[:10]}，'
                        f'说明 key↔URL 映射错位，强行合并会顺序混乱。请重跑 collect/probe。')
                print(f'源段号核对通过：{checked} 个分片 key 与 URL 内嵌段号全部一致 ✓')
        except SystemExit:
            raise
        except Exception as e:
            print(f'⚠️ 源段号核对跳过（{str(e)[:60]}）')

    listf = os.path.join(root, 'concat.txt')
    with open(listf, 'w') as f:
        for name in files:
            p = os.path.join(segdir, name)
            f.write("file '%s'\n" % p.replace("'", "'\\''"))

    print('开始合并（-c copy，无损）...')
    r = subprocess.run(
        [ff, '-f', 'concat', '-safe', '0', '-i', listf,
         '-c', 'copy', '-movflags', '+faststart', '-y', out],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit('合并失败')
    print('合并完成:', out, '%.2f MB' % (os.path.getsize(out) / 1048576))

    # 校验：时长 / 分辨率
    here = os.path.dirname(os.path.abspath(__file__))
    info = subprocess.run([sys.executable, os.path.join(here, 'mp4info.py'), out],
                          capture_output=True, text=True)
    print('\n=== 合并结果 ===')
    print(info.stdout.strip())

    # ── 真实接缝时刻表：逐片解析真实时长并累计（不再假设等长） ──
    def seg_duration(name):
        """解析单个分片真实时长（秒）"""
        p = os.path.join(segdir, name)
        r = subprocess.run([ff, '-i', p], capture_output=True, text=True)
        m = re.search(r'Duration: (\d+):(\d+):(\d+\.?\d*)', r.stderr)
        if not m:
            return None
        h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
        return h * 3600 + mi * 60 + s

    durs = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for name, d in zip(files, ex.map(seg_duration, files)):
            durs[name] = d
    if any(d is None for d in durs.values()):
        print('⚠️ 有分片时长解析失败，回退等分假设')
        durs = {n: None for n in files}

    # 累计出每个分片的起始时刻 = 前面所有分片时长之和
    seams = []
    if durs[files[0]] is not None:
        t = 0.0
        for i, name in enumerate(files):
            t += durs[name]
            if i < len(files) - 1:
                seams.append((i + 1, t))  # (拼接点序号, 拼接点时刻)
        print(f'\n接缝体检：{len(seams)} 个拼接点（真实时长累计表，不等长也准确）')
    else:
        dur = None
        for line in info.stdout.splitlines():
            if line.startswith('时长:'):
                dur = float(line.split()[1])
        if not dur:
            print('无法解析时长，跳过接缝体检')
            return
        seg = dur / len(files)
        seams = [(i, i * seg) for i in range(1, len(files))]
        print(f'\n接缝体检：{len(seams)} 个拼接点（等分假设，回退模式）')

    def check(item):
        i, t = item
        tt = max(0, t - 3)
        rr = subprocess.run([ff, '-v', 'error', '-ss', str(tt), '-t', '10',
                             '-i', out, '-f', 'null', '-'],
                            capture_output=True, text=True)
        return i, rr.stderr.strip()

    errs = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, e in ex.map(check, seams):
            if e:
                errs.append((i, e))

    if errs:
        print(f'发现 {len(errs)} 个接缝有解码错误:')
        for i, e in errs[:10]:
            print(f'  seam {i}: {e[:300]}')
    else:
        print(f'全部 {len(seams)} 个拼接点解码无错误 ✓')


if __name__ == '__main__':
    main()
