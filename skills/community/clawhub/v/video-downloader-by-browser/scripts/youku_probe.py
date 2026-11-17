"""
优酷专用：把采集到的带窗口参数的 URL，转换成「整分片」URL 并探测真实大小。

这是 youku_collect.py 与 youku_download.py 之间**必须**的一环：
collect 产出 chunks.json（带 ts_start/ts_end/ts_seg_no 的 10 秒窗口 URL），
download 需要的是 chunks_full.json（去掉窗口参数的整分片 URL + 总字节数）。

原理：去掉 ts_start / ts_end / ts_seg_no 三个参数后，CDN 返回整个 140 秒分片的完整 MP4。

用法:
    python youku_probe.py <工作目录>

输出:
    <工作目录>/chunks_full.json   {分片号: {"url": 整分片URL, "size": 字节数}}
"""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = (sys.argv[1] if len(sys.argv) > 1 else '.').rstrip('/') + '/'

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36')


def strip_window(u):
    """去掉 10 秒窗口参数，得到整分片 URL"""
    u = re.sub(r'&?ts_start=[0-9.]+', '', u)
    u = re.sub(r'&?ts_end=[0-9.]+', '', u)
    u = re.sub(r'&?ts_seg_no=\d+', '', u)
    return u.replace('?&', '?').replace('&&', '&')


def probe(item):
    k, u = item
    full = strip_window(u)
    # -r 0-0 只取 1 字节，从 Content-Range: bytes 0-0/TOTAL 读出总长度
    r = subprocess.run(
        ['curl', '-sS', '-D', '-', '-o', '/dev/null', '--max-time', '30',
         '-H', 'Referer: https://v.youku.com/', '-H', 'User-Agent: ' + UA,
         '-r', '0-0', full],
        capture_output=True, text=True)
    codes = [l for l in r.stdout.splitlines() if l.startswith('HTTP/')]
    code = codes[-1].strip() if codes else 'NO-RESP'
    cr = [l.split('/')[-1].strip() for l in r.stdout.splitlines()
          if 'Content-Range' in l]
    size = int(cr[0]) if cr and cr[0].isdigit() else -1
    return k, code, size, full


def main():
    path = ROOT + 'chunks.json'
    if not os.path.exists(path):
        raise SystemExit(f'找不到 {path}，请先运行 youku_collect.py')
    chunks = json.load(open(path))
    print(f'待探测 {len(chunks)} 个分片...')

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(probe, sorted(chunks.items(), key=lambda kv: int(kv[0], 16))))

    total, ok = 0, 0
    out = {}
    for k, code, size, full in res:
        good = ('200' in code or '206' in code) and size > 0
        if good:
            out[k] = {'url': full, 'size': size}
            total += size
            ok += 1
        print(f'{k}  {"OK " if good else "BAD"}  {code[:22]:22s} '
              f'{size / 1048576 if size > 0 else 0:8.1f} MB')

    print(f'\n有效 {ok}/{len(chunks)}   总计 {total / 1073741824:.2f} GB')
    if not out:
        raise SystemExit('全部探测失败：令牌可能已过期，请重新运行 youku_collect.py')
    with open(ROOT + 'chunks_full.json', 'w') as f:
        json.dump(out, f, indent=1)
    print('已写入 chunks_full.json')


if __name__ == '__main__':
    main()
