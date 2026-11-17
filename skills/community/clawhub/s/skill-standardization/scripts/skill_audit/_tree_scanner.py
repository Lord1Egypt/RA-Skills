def _check_directory_tree(filepath, body, skill_dir, issues):
    """检查文档中的目录树是否与磁盘一致（v2.56.0）"""
    import re, os
    # 要检查的 .md 文件
    md_files = [('SKILL.md', body.split('\n'))]
    refs_dir = os.path.join(skill_dir, 'references')
    if os.path.isdir(refs_dir):
        for fname in sorted(os.listdir(refs_dir)):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(refs_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                md_files.append((f'references/{fname}', content.split('\n')))
            except Exception:
                continue

    tree_lines = []  # (filepath, source_name, line_num, indent_level, entry_type, entry_name)
    # Box-drawing characters: ├ ─ └ │
    tree_pattern = re.compile(
        r'^(?P<indent>[ │]+)?(?P<branch>[├└])──\s+(?P<name>.+)$'
    )

    for src_name, lines in md_files:
        dir_stack = []  # stack of (indent_level, dir_name)
        for ln, line in enumerate(lines, 1):
            m = tree_pattern.search(line)
            if not m:
                continue
            indent = len(m.group('indent') or '')
            indent_level = indent // 4  # each indent level is ~4 chars
            entry_name = m.group('name').strip().rstrip()
            branch = m.group('branch')

            # Clean up: remove trailing # comments
            entry_name = entry_name.split('  #')[0].strip()

            # ★ 筛除非文件系统路径的条目：
            # 如果 entry_name 包含中文字符、中文括号、或明显不是文件/目录名的内容，跳过
            # 避免将文档中的概念图（如 "├── 联网搜索（参见 search-integration.md）"）误判为文件路径
            if re.search(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef（）]', entry_name):
                continue
            # 跳过含空格或特殊标记的条目（典型文档标记而非文件路径）
            if '（' in entry_name or '）' in entry_name:
                continue
            # 跳过无文件扩展名且不以 / 结尾的条目（非目录也非文件）
            if not entry_name.endswith('/') and '.' not in entry_name:
                continue

            if entry_name.endswith('/'):
                # Directory entry
                dir_name = entry_name.rstrip('/')
                # Adjust stack
                while dir_stack and dir_stack[-1][0] >= indent_level:
                    dir_stack.pop()
                dir_stack.append((indent_level, dir_name))
            else:
                # File entry
                # Build full path from stack + entry_name
                path_parts = [d[1] for d in dir_stack if d[0] < indent_level]
                path_parts.append(entry_name)
                full_path = '/'.join(path_parts)
                tree_lines.append((full_path, src_name, ln, entry_name))

    if not tree_lines:
        return

    for full_path, src_name, ln, entry_name in tree_lines:
        if not full_path:
            continue
        disk_path = os.path.join(skill_dir, full_path)
        if os.path.isfile(disk_path):
            continue
        # Also check with scripts/ prefix
        alt_path = os.path.join(skill_dir, 'scripts', full_path)
        if os.path.isfile(alt_path):
            continue
        # File doesn't exist → report
        issues["suggest"].append(
            f"R-23: {filepath}:1 - 目录树显示 `{full_path}` 但文件不存在（{src_name}:{ln}）"
        )
