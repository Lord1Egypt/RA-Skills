"""采集优酷全部分片的窗口 URL。
优酷分片规律：
  文件名 03000C2{X}{HEX}649EAA...  其中：
    前 7 位 03000C2 固定；第 8 位 {X} 随视频/流变化（实测见过 0/1/7，
      例如同一批两个视频分别是 03000C20 和 03000C27），**不要写死**；
    {HEX} = 分片号(00~.. 十六进制 2 位)，这才是播放顺序的权威编号。
  每个分片约 140 秒，seek 到 i*140+2 即可引出第 i 个分片的 URL
  请求带 ts_start/ts_end/ts_seg_no(10秒窗口)，去掉后可取回整个分片
"""
import json, os, math, time, urllib.parse as up

import sys
ROOT = (sys.argv[1] if len(sys.argv) > 1 else '.').rstrip('/') + '/'
NET2 = ROOT + 'netlog2.jsonl'
CMD = ROOT + 'cmd.txt'
WIN = 140.0
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 4599.0  # 正片总时长
# N = ceil(总时长/140)，自动适配不同长度视频（优酷每分片约140秒）
CHUNKS = max(1, math.ceil(DUR / WIN))
print(f'[collect] 按时长 {DUR:.0f}s 推算分片数 N={CHUNKS}')


import re as _re
_SEG_RE = _re.compile(r'^03000C2[0-9a-fA-F]([0-9a-fA-F]{2})')


def chunk_index(url):
    """从 URL 文件名提取分片号(十六进制2位)。
    文件名 03000C2 X HH 64..：前 7 位 03000C2 固定，第 8 位 X 随流变化(0/1/7..)，
    第 9-10 位 HH 才是分片号。早期写死 startswith('03000C21') 会漏掉 X≠1 的视频
    （实测 03000C20 / 03000C27 整片采不到），故第 8 位通配。"""
    fn = up.urlparse(url).path.split('/')[-1]
    m = _SEG_RE.match(fn)
    if not m:
        return None
    try:
        return int(m.group(1), 16)
    except ValueError:
        return None


def discovered(since_ts=0):
    """返回 {分片号: (时间戳, url)}"""
    got = {}
    if not os.path.exists(NET2):
        return got
    for line in open(NET2):
        try:
            r = json.loads(line)
        except Exception:
            continue
        u = r.get('url', '')
        if 'cibntv' not in u:
            continue
        if r.get('ts', 0) < since_ts:
            continue
        idx = chunk_index(u)
        if idx is None or not (0 <= idx < CHUNKS):
            continue
        got.setdefault(idx, (r['ts'], u))
    return got


def main():
    # 只用本次运行之后抓到的记录，避免混入过期令牌
    t0 = int(time.time() * 1000)
    print(f'基准时间戳 {t0}，开始遍历 {CHUNKS} 个分片...')

    for rnd in range(3):
        got = discovered(t0)
        missing = [k for k in range(CHUNKS) if k not in got]
        print(f'\n== 第{rnd+1}轮: 已发现 {len(got)}/{CHUNKS}, 缺 {[f"{k:02x}" for k in missing]}')
        if not missing:
            break
        for k in missing:
            # 在分片内取多个探测点，任一点命中即可
            # ⚠️ offset 首选 2 而非 5：实测优酷播放器 seek 到 ≤5s（chunk 0 内）时
            #    经常不重新发 chunk 0 请求（判定为"已在开头附近"），导致 chunk 0 采集
            #    盲区——3 轮全 MISS（2026-09 实战踩坑）。seek 2s 可稳定触发。
            for offset in (2, 5, 60, 120, 30, 95):
                got = discovered(t0)
                if k in got:
                    break
                t = min(WIN * k + offset, DUR - 9)
                with open(CMD, 'w') as f:
                    f.write(f'seek {t:.1f}\n')
                time.sleep(3.2)
            got = discovered(t0)
            print(f'  chunk {k:02x} (t={WIN*k+5:.0f}s) -> {"OK" if k in got else "MISS"}   共 {len(got)}/{CHUNKS}')
        time.sleep(1)

    got = discovered(t0)
    print(f'\n最终发现 {len(got)}/{CHUNKS} 个分片')
    out = {}
    mismatch = 0
    for k in sorted(got):
        url = got[k][1]
        # 权威顺序校验：URL 文件名内嵌的段号必须 == 字典 key（chunk_index 本就从
        # URL 提取段号，这里二次核验，防止任何 key 记错/错位——内嵌段号是优酷 CDN
        # 生成的源播放顺序，比任何本地排序都可信）。
        emb = chunk_index(url)
        if emb != k:
            print(f'  ⚠️ 段号不一致: key={k:02x} 但 URL 内嵌段号={emb if emb is None else f"{emb:02x}"}')
            mismatch += 1
        out[f'{k:02x}'] = url
        fn = up.urlparse(url).path.split('/')[-1][:12]
        print(f'  {k:02x}  {fn}')
    missing = [f'{k:02x}' for k in range(CHUNKS) if k not in got]
    # N=ceil(dur/140) 可能比实际多 1（末片按 140s 切，但整片可能刚好不产生最后一片，
    # 此前实测 dur=4524 → N=33 而实际只有 00..1f 共 32 片且 00..1f 连续无洞）。
    # 区分两种情况：只缺"最后一个号"且其余 0..N-2 连续 → 可能是 N 多算，放行并提示；
    # 中间有洞 → 真漏片，必须重采。
    have = sorted(got)
    hole_idx = [k for i, k in enumerate(have) if i > 0 and k != have[i - 1] + 1]
    if hole_idx:
        print(f'\n⛔ 分片号中间有断档（真漏片）: 断在 {[f"{k:02x}" for k in hole_idx]}，'
              f'请重跑本脚本补齐；缺 {missing}')
    elif missing:
        print(f'\n⚠️ 仅缺末尾 {missing}（0..{have[-1]:02x} 连续无洞）：'
              f'多为 N=ceil(dur/140) 多算 1，末片本就不存在。合并后用时长核对页面 dur 即可确认。')
    if mismatch:
        print(f'⛔ {mismatch} 个分片 key 与 URL 内嵌段号不一致，勿直接合并！')
    with open(ROOT + 'chunks.json', 'w') as f:
        json.dump(out, f, indent=1)
    print(f'\n已写入 chunks.json ({len(out)} 条)')
    return len(out)


if __name__ == '__main__':
    main()
