def split_video_by_size(filepath, max_size_mb=MAX_FILE_SIZE_MB):
    """分割视频：一次 ffmpeg 调用生成所有分段"""
    size_mb = os.path.getsize(filepath) / (1024*1024)
    if size_mb <= max_size_mb:
        return [filepath]
    print(f'视频 {size_mb:.1f}MB 超过 {max_size_mb}MB，开始分割...')
    duration = get_duration(filepath) / 1000.0
    num_parts = math.ceil(size_mb / max_size_mb)
    segment_duration = int(duration / num_parts) + 1  # 秒
    output_dir = os.path.dirname(filepath)
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    # 输出模板：包含 %03d，ffmpeg 会自动填充
    output_template = os.path.join(output_dir, f'{base_name}_part%03d.mp4')
    cmd = [
        'ffmpeg', '-i', filepath,
        '-c', 'copy',
        '-map', '0',
        '-segment_time', str(segment_duration),
        '-f', 'segment',
        '-reset_timestamps', '1',
        output_template
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=600)
    except subprocess.CalledProcessError as e:
        print(f'分割失败: {e.stderr.decode(errors="ignore") if e.stderr else e}')
        # 尝试 fallback: 不分割直接返回原文件（但会超限）
        return [filepath]
    # 收集生成的文件（按顺序）
    part_files = []
    for i in range(num_parts):
        candidate = os.path.join(output_dir, f'{base_name}_part{i:03d}.mp4')
        if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
            part_files.append(candidate)
        else:
            break  # 没有足够的段
    print(f'分割完成: {len(part_files)} 段')
    return part_files if part_files else [filepath]