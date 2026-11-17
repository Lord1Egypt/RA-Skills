"""
用户验收通过后，安全删除中间分片。

⚠️ 调用时机：必须由用户明确确认「视频播放无误」之后才能执行。
   绝不要在合并完成但未验收时自动删除。

安全策略（默认不物理删除）：
  - macOS: 移到系统废纸篓（可恢复）
  - 其他:  重命名为 <分片目录>_pending_delete（可恢复）

用法:
    python cleanup.py <工作目录> [分片目录名(默认seg)] [--merged <成品路径>] [--purge]

选项:
    --merged <路径>  显式指定已验收的合并成品（推荐）。成品不一定在工作目录内，
                     用此参数可直接指定，跳过"在工作目录找最大视频"的脆弱启发。
    --purge  真·永久删除（rm -rf）。需用户二次确认，默认不使用。
"""
import os
import sys
import shutil
import subprocess


def parse_args(argv):
    merged_arg = None
    purge = '--purge' in argv
    positional = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--merged' and i + 1 < len(argv):
            merged_arg = argv[i + 1]
            i += 2
            continue
        if a == '--purge':
            i += 1
            continue
        positional.append(a)
        i += 1
    return positional, merged_arg, purge



def to_trash_macos(path):
    """macOS: 移到废纸篓。优先 Finder 删除；失败（如沙盒限制）则直接 mv 到 ~/.Trash。"""
    r = subprocess.run([
        'osascript', '-e',
        f'tell application "Finder" to delete POSIX file "{path}"'
    ], capture_output=True, text=True)
    if r.returncode == 0:
        return True
    # 回退：直接 mv 到 ~/.Trash（同样可恢复，且真正释放空间）
    try:
        trash = os.path.expanduser('~/.Trash')
        os.makedirs(trash, exist_ok=True)
        base = os.path.basename(path.rstrip('/'))
        dst = os.path.join(trash, base)
        n = 1
        while os.path.exists(dst):
            dst = os.path.join(trash, f'{base}_{n}')
            n += 1
        os.rename(path, dst)
        return True
    except OSError:
        return False


def dirsize(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def main():
    args, merged_arg, purge = parse_args(sys.argv[1:])
    if len(args) < 1:
        print(__doc__)
        sys.exit(1)
    root = args[0]
    segdir = args[1] if len(args) > 1 else 'seg'
    segpath = os.path.join(root, segdir)

    if not os.path.isdir(segpath):
        print(f'分片目录不存在: {segpath}（可能已清理）')
        return

    # 安全闸：确认存在比分片总量更大的成品文件
    size = dirsize(segpath)
    if merged_arg and os.path.isfile(merged_arg):
        # 优先用显式指定的成品（最稳，不依赖目录内启发）
        biggest = os.path.basename(merged_arg)
        bsize = os.path.getsize(merged_arg)
        print(f'[成品(显式)] {merged_arg}')
    else:
        merged = [f for f in os.listdir(root)
                  if f.lower().endswith(('.mp4', '.mkv', '.ts', '.flv'))
                  and os.path.isfile(os.path.join(root, f))]
        if merged_arg:
            print(f'⚠️ --merged 指定的文件不存在: {merged_arg}，退回目录内搜索')
        if not merged:
            print('⚠️ 工作目录里没找到成品视频文件，拒绝清理。')
            print('   请确认合并产物已放在工作目录下，或用 --merged 显式指定。')
            sys.exit(1)
        biggest = max(merged, key=lambda f: os.path.getsize(os.path.join(root, f)))
        bsize = os.path.getsize(os.path.join(root, biggest))
        print(f'[成品(目录内最大)] {biggest}')
    # 双重判断：绝对下限(防占位空文件) + 相对比例(防半成品)
    if bsize < 1024 * 1024:
        print(f'⚠️ 成品 {biggest} 只有 {bsize} 字节，小于 1 MB，不像是合并产物，拒绝清理。')
        sys.exit(1)
    if bsize < size * 0.9:
        print(f'⚠️ 成品 {biggest} ({bsize/1073741824:.2f} GB) 明显小于分片总量 '
              f'({size/1073741824:.2f} GB)，拒绝清理。')
        sys.exit(1)

    print(f'成品: {biggest}  {bsize/1073741824:.2f} GB')
    print(f'分片: {segpath}  {size/1073741824:.2f} GB（{len(os.listdir(segpath))} 个文件）')

    if purge:
        ans = input('⚠️ 即将【永久删除】分片，无法恢复。输入 DELETE 确认: ').strip()
        if ans != 'DELETE':
            print('已取消')
            return
        shutil.rmtree(segpath)
        print(f'已永久删除 {segpath}')
    else:
        if sys.platform == 'darwin' and to_trash_macos(segpath):
            print(f'已移到废纸篓: {segpath}（可恢复）')
        else:
            dst = segpath.rstrip('/') + '_pending_delete'
            n = 1
            while os.path.exists(dst):
                dst = segpath.rstrip('/') + f'_pending_delete_{n}'
                n += 1
            os.rename(segpath, dst)
            print(f'已重命名为: {dst}（确认无误后可自行删除）')

    print(f'释放空间约 {size/1073741824:.2f} GB')


if __name__ == '__main__':
    main()
