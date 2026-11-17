"""并行下载 33 个分片。
策略：每个分片切成 N 段 Range 并发下载写入同一文件；同时并发处理 M 个分片。
带完整性校验（末尾补拉 / 自动重试 / 全零空洞探测 / .ok 完成标记）。

⚠️ 2026-09 修复（拼接混乱根因）：
  1. 失败分片曾把「预分配占位文件」（truncate 后部分全零）留在盘上，
     重跑时 getsize==size 会误判为"已下载完整"→ 残缺分片混入合并 → 黑屏段。
     现在：下载全部 range 成功且抽查非全零后才写 .ok 标记；失败立即删除占位文件；
     缓存跳过只认 .ok 标记，不认文件大小。
  2. 长度校验骗不过"恰好等长的垃圾响应"，新增首/中/尾 64KB 全零探测
     （truncate 预分配的空洞是 \x00，真实 MPEG 数据不可能 192KB 连续全零）。
"""
import json, os, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
import urllib.request

import sys
ROOT = (sys.argv[1] if len(sys.argv) > 1 else '.').rstrip('/') + '/'
SEG = ROOT + 'seg'
os.makedirs(SEG, exist_ok=True)

CHUNK_THREADS = 6      # 单个分片内的并发 Range 数
CHUNK_PARALLEL = 3     # 同时下载的分片数

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36')
HDR = {'Referer': 'https://v.youku.com/', 'User-Agent': UA}

info = {}  # main() 里从 chunks_full.json 加载（模块级读取会在文件缺失时炸掉导入）
lock = threading.Lock()
progress = {}


def fetch_range(url, start, end, retries=4):
    """下载 [start, end] 闭区间字节，返回 bytes"""
    req = urllib.request.Request(url, headers=dict(HDR, Range=f'bytes={start}-{end}'))
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                if len(data) == end - start + 1:
                    return data
        except Exception as e:
            if i == retries - 1:
                print(f'    [range fail] {start}-{end}: {str(e)[:60]}')
            time.sleep(1.2 * (i + 1))
    return None


def zero_probe(path, probe=65536):
    """抽查首/中/尾各 probe 字节是否全零（预分配空洞特征）。返回全零区块位置或 None"""
    size = os.path.getsize(path)
    if size == 0:
        return 'empty'
    with open(path, 'rb') as f:
        for name, off in (('head', 0), ('mid', max(0, size // 2 - probe // 2)), ('tail', max(0, size - probe))):
            f.seek(off)
            buf = f.read(min(probe, size - off))
            if buf and buf.count(0) == len(buf):
                return name
    return None


def download_chunk(item):
    k, meta = item
    url, size = meta['url'], meta['size']
    out = os.path.join(SEG, f'chunk_{k}.mp4')
    okf = out + '.ok'
    # 缓存判定只认 .ok 标记（曾经只看大小，残缺占位文件会被误判为完整 → 黑屏段）
    if os.path.exists(okf) and os.path.exists(out) and os.path.getsize(out) == size:
        with lock:
            print(f'[{k}] 已有 .ok 标记且大小一致，跳过')
        return k, True, 'cached'

    # 旧的无标记残留（大小恰好一致但没有 .ok）：删除重下，杜绝残缺混入
    if os.path.exists(out) and not os.path.exists(okf):
        with lock:
            print(f'[{k}] 存在无 .ok 标记的残留文件，删除重下')
        os.remove(out)

    # 预分配文件
    with open(out, 'wb') as f:
        f.truncate(size)

    part = size // CHUNK_THREADS
    ranges = []
    for i in range(CHUNK_THREADS):
        s = i * part
        e = (size - 1) if i == CHUNK_THREADS - 1 else (s + part - 1)
        ranges.append((s, e))

    def work(rg):
        s, e = rg
        data = fetch_range(url, s, e)
        if data is None:
            return False
        with lock:
            with open(out, 'r+b') as f:
                f.seek(s)
                f.write(data)
            progress[k] = progress.get(k, 0) + len(data)
        return True

    # 显式收集全部结果再判定（all(map) 短路会丢弃在飞结果，语义含糊）
    results = list(ThreadPoolExecutor(max_workers=CHUNK_THREADS).map(work, ranges))
    ok = all(results)

    actual = os.path.getsize(out)
    if ok and actual == size:
        zp = zero_probe(out)
        if zp:
            os.remove(out)
            return k, False, f'all-zero block at {zp} (bad CDN response?)'
        # 全部校验通过，写完成标记
        open(okf, 'w').write(f'{size}\n')
        return k, True, 'ok'
    # 失败：立即删除占位文件，防止残缺分片混入后续合并
    try:
        os.remove(out)
    except OSError:
        pass
    return k, False, f'size {actual}!={size}' if actual != size else 'range fail'


def main():
    global info
    info = json.load(open(ROOT + 'chunks_full.json'))
    items = sorted(info.items(), key=lambda kv: int(kv[0], 16))
    t0 = time.time()
    results = {}
    pending = list(items)
    # 最多 3 轮：首轮全量 + 2 轮失败分片自动补下
    # （2026-09 修复：此前失败分片要人工看 dl_result.json 手动重跑，漏看就会缺片合并）
    for rnd in range(1, 4):
        if not pending:
            break
        if rnd > 1:
            print(f'\n== 失败分片自动补下（第 {rnd - 1} 轮）: {[k for k, _ in pending]}')
        with ThreadPoolExecutor(max_workers=CHUNK_PARALLEL) as ex:
            for k, ok, note in ex.map(download_chunk, pending):
                results[k] = (ok, note)
                print(f'[{k}] {"OK" if ok else "FAIL"}  {note}  ({time.time()-t0:.0f}s)')
        pending = [(k, info[k]) for k, _ in sorted(results.items(), key=lambda kv: int(kv[0], 16))
                   if not results[k][0]]

    good = [k for k, (ok, _) in results.items() if ok]
    bad = [k for k, (ok, _) in results.items() if not ok]
    seg_files = [f for f in os.listdir(SEG) if f.endswith('.mp4')]
    total = sum(os.path.getsize(os.path.join(SEG, f)) for f in seg_files)
    print(f'\n完成 {len(good)}/{len(results)}，失败 {len(bad)}：{bad}')
    print(f'seg 目录现存 {len(seg_files)} 个 mp4（失败分片已自动删除，不残留占位文件）')
    print(f'已下载 {total/1073741824:.2f} GB，耗时 {time.time()-t0:.0f}s')
    json.dump({'bad': bad}, open(ROOT + 'dl_result.json', 'w'))


if __name__ == '__main__':
    main()
