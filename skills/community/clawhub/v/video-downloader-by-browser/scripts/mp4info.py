"""
纯 Python 解析 MP4 元信息（无需 ffprobe）。

用法: python mp4info.py <文件.mp4>

输出: 文件大小 / 视频编码+分辨率 / 音频编码+声道+采样率 / 时长

说明:
  - 只读文件头部 8MB + 尾部 64MB，超大文件也很快
  - 同时兼容 moov 在文件头(faststart)和文件尾(常规)两种情况
"""
import struct
import sys
import os

CONTAINERS = ('moov', 'trak', 'mdia', 'minf', 'stbl', 'edts', 'udta', 'dinf')


def parse(data, start, end, out):
    pos = start
    while pos + 8 <= end:
        size = struct.unpack('>I', data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8].decode('latin1', 'ignore')
        hdr = 8
        if size == 1:
            if pos + 16 > end:
                break
            size = struct.unpack('>Q', data[pos + 8:pos + 16])[0]
            hdr = 16
        elif size == 0:
            size = end - pos
        if size < 8:
            break
        if not all(c.isalnum() or c == ' ' for c in typ):
            break
        payload = pos + hdr
        pend = min(pos + size, end)

        if typ == 'tkhd' and pend - payload >= 84:
            ver = data[payload]
            off = payload + 4 + (32 if ver == 1 else 20) + 8 + 8 + 36
            w = struct.unpack('>I', data[off:off + 4])[0] / 65536
            h = struct.unpack('>I', data[off + 4:off + 8])[0] / 65536
            if int(w) > 0 and int(h) > 0:
                out.setdefault('tkhd', [])
                if (int(w), int(h)) not in out['tkhd']:
                    out['tkhd'].append((int(w), int(h)))

        elif typ == 'mvhd' and pend - payload >= 32:
            ver = data[payload]
            if ver == 1:
                ts = struct.unpack('>I', data[payload + 20:payload + 24])[0]
                dur = struct.unpack('>Q', data[payload + 24:payload + 32])[0]
            else:
                ts = struct.unpack('>I', data[payload + 12:payload + 16])[0]
                dur = struct.unpack('>I', data[payload + 16:payload + 20])[0]
            if ts:
                out['duration'] = (dur, ts)

        elif typ == 'stsd' and pend - payload >= 8:
            ec = struct.unpack('>I', data[payload + 4:payload + 8])[0]
            e = payload + 8
            for _ in range(ec):
                if e + 8 > pend:
                    break
                esz = struct.unpack('>I', data[e:e + 4])[0]
                if esz < 8:
                    break
                fmt = data[e + 4:e + 8].decode('latin1', 'ignore')
                if esz >= 36 and fmt not in ('mp4a', 'sowt', 'ac-3', 'ec-3'):
                    w = struct.unpack('>H', data[e + 32:e + 34])[0]
                    h = struct.unpack('>H', data[e + 34:e + 36])[0]
                    out.setdefault('codec', [])
                    if (fmt, w, h) not in out['codec']:
                        out['codec'].append((fmt, w, h))
                elif fmt in ('mp4a', 'ac-3', 'ec-3') and esz >= 36:
                    # AudioSampleEntry: e+8 起 6 保留 + 2 data_ref_index = 16
                    # version(2) revision(2) vendor(4) -> e+24 channelcount(2)
                    # samplesize(2) pre_defined(2) reserved(2) -> e+32 samplerate(4, 16.16)
                    ch = struct.unpack('>H', data[e + 24:e + 26])[0]
                    sr = struct.unpack('>I', data[e + 32:e + 36])[0] >> 16
                    out['audio'] = (fmt, ch, sr)
                e += esz

        if typ in CONTAINERS:
            parse(data, payload, pend, out)
        pos += size


def read_head_tail(path, head_mb=8, tail_mb=64):
    """读头部 + 尾部，兼容 moov 在前(faststart)和在后两种情况"""
    size = os.path.getsize(path)
    head_n = min(head_mb * 1024 * 1024, size)
    tail_n = min(tail_mb * 1024 * 1024, size - head_n)
    with open(path, 'rb') as f:
        head = f.read(head_n)
        if tail_n > 0:
            f.seek(size - tail_n)
            return head + f.read(tail_n)
        return head


def probe(path):
    """返回 dict: {video, audio, duration, size}"""
    data = read_head_tail(path)
    out = {}
    # 先从头部的 moov 找，找不到再从尾部 buffer 里定位 moov 单独解析
    parse(data, 0, len(data), out)
    if 'duration' not in out:
        i = data.rfind(b'moov')
        if i > 4:
            sz = struct.unpack('>I', data[i - 4:i])[0]
            parse(data, i - 4, min(i - 4 + sz, len(data)), out)
    return out


def main():
    if len(sys.argv) < 2:
        print('用法: python mp4info.py <文件.mp4>')
        sys.exit(1)
    p = sys.argv[1]
    out = probe(p)
    print('文件:', os.path.basename(p), ' %.1f MB' % (os.path.getsize(p) / 1048576))
    for fmt, w, h in out.get('codec', []):
        print(f'视频编码: {fmt}  分辨率: {w}x{h}')
    if 'audio' in out:
        a = out['audio']
        print(f'音频编码: {a[0]}  声道: {a[1]}  采样率: {a[2]} Hz')
    if 'tkhd' in out:
        print('tkhd 显示尺寸:', out['tkhd'])
    if 'duration' in out:
        d, ts = out['duration']
        sec = d / ts
        print('时长: %.1f 秒 = %d 分 %d 秒' % (sec, int(sec) // 60, int(sec) % 60))
    else:
        print('时长: 解析失败（文件可能损坏或不是标准 MP4）')


if __name__ == '__main__':
    main()
