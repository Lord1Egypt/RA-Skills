#!/usr/bin/env python3
"""
路径分发协议（Path-Dispatch Protocol）打包/解包工具

用法：
    python archive.py pack <source_dir> <output_file>
    python archive.py unpack <input_file> <output_dir>
"""

import os, sys, json, base64, re, secrets

def parse_archive(text: str):
    text = text.lstrip()
    if not text.startswith('{'):
        raise ValueError("文本必须以 JSON 元数据区开头")
    depth = 0; in_string = False; escape = False; json_end = -1
    for i, ch in enumerate(text):
        if in_string:
            if escape: escape = False
            elif ch == '\\': escape = True
            elif ch == '"': in_string = False
        else:
            if ch == '"': in_string = True
            elif ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0: json_end = i; break
    if json_end == -1: raise ValueError("未找到闭合的 JSON 对象")
    manifest = json.loads(text[:json_end + 1])
    if "files" not in manifest: manifest["files"] = {}
    content_text = text[json_end + 1:].strip()
    sep = manifest.get("separator", "")
    if sep:
        sep_esc = re.escape(sep)
        file_prefix = f"---file_{sep}:"; symlink_prefix = f"---symlink_{sep}:"
    else:
        sep_esc = ""; file_prefix = "---file:"; symlink_prefix = "---symlink:"
    file_pattern = re.compile(
        rf'^{re.escape(file_prefix)}\s+(.+?)\s+\((text|base64)\)\s*$(.*?)(?=^{re.escape(file_prefix)}\s|^{re.escape(symlink_prefix)}\s|\Z)',
        re.MULTILINE | re.DOTALL)
    symlink_pattern = re.compile(rf'^{re.escape(symlink_prefix)}\s+(.+?)\s*->\s*(.+?)\s*$', re.MULTILINE)
    file_contents = {}
    for m in symlink_pattern.finditer(content_text):
        lp = m.group(1).strip(); tgt = m.group(2).strip()
        if lp not in manifest["files"]: manifest["files"][lp] = {"type": "symlink", "target": tgt}
    for m in file_pattern.finditer(content_text):
        path = m.group(1).strip(); ftype = m.group(2).strip(); content = m.group(3).strip()
        file_contents[path] = content.encode("utf-8") if ftype == "text" else base64.b64decode(re.sub(r'\s+', '', content))
    for path, info in manifest["files"].items():
        if info.get("type") in ("text", "base64") and path not in file_contents:
            raise ValueError(f"文件 '{path}' 在元数据中声明但内容区未找到")
    return manifest, file_contents

def rebuild_directory(manifest, file_contents, base_dir="output"):
    for path, info in manifest["files"].items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        ftype = info.get("type", "text")
        if ftype == "dir": os.makedirs(full_path, exist_ok=True)
        elif ftype == "symlink":
            target = info.get("target")
            if os.path.lexists(full_path): os.remove(full_path)
            try: os.symlink(target, full_path)
            except OSError as e:
                print(f"[警告] 无法创建软链接 {path} -> {target}: {e}")
                open(full_path, 'w').write(f"# symbolic link: {target}\n")
        else:
            with open(full_path, "wb") as f: f.write(file_contents.get(path, b""))
    print(f"目录结构已重建于: {os.path.abspath(base_dir)}")

def pack_directory(source_dir, output_path):
    source_dir = os.path.abspath(source_dir)
    separator = secrets.token_hex(4)
    manifest_files = {}; file_contents = {}
    for root, dirs, files in os.walk(source_dir, followlinks=False):
        for d in dirs:
            full_dir = os.path.join(root, d)
            rel_path = os.path.relpath(full_dir, source_dir).replace(os.sep, '/')
            if os.path.islink(full_dir):
                target = os.readlink(full_dir)
                if not os.path.exists(full_dir): continue
                manifest_files[rel_path] = {"type": "symlink", "target": target}
            else: manifest_files[rel_path] = {"type": "dir"}
        for f in files:
            full_file = os.path.join(root, f)
            rel_path = os.path.relpath(full_file, source_dir).replace(os.sep, '/')
            if os.path.islink(full_file):
                target = os.readlink(full_file)
                if not os.path.exists(full_file): continue
                manifest_files[rel_path] = {"type": "symlink", "target": target}
            else:
                try:
                    raw = open(full_file, 'rb').read()
                    manifest_files[rel_path] = {"type": "text"}
                    file_contents[rel_path] = raw.decode('utf-8')
                except UnicodeDecodeError:
                    manifest_files[rel_path] = {"type": "base64"}
                    file_contents[rel_path] = base64.b64encode(raw).decode('ascii')
                except Exception as e: print(f"[错误] {full_file}: {e}")
    manifest = {"separator": separator, "files": manifest_files}
    fp = f"---file_{separator}:"; sp = f"---symlink_{separator}:"
    parts = []
    for path, info in manifest_files.items():
        if info["type"] == "dir": continue
        elif info["type"] == "symlink": parts.append(f"{sp} {path} -> {info['target']}\n")
        elif info["type"] == "text": parts.append(f"{fp} {path} (text)\n{file_contents[path]}\n")
        elif info["type"] == "base64": parts.append(f"{fp} {path} (base64)\n{file_contents[path]}\n")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n" + "".join(parts))
    print(f"打包完成: {os.path.abspath(output_path)}")

def main():
    if len(sys.argv) < 4: print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "pack":
        if not os.path.isdir(sys.argv[2]): print(f"错误：源目录不存在"); sys.exit(1)
        pack_directory(sys.argv[2], sys.argv[3])
    elif cmd == "unpack":
        if not os.path.isfile(sys.argv[2]): print(f"错误：输入文件不存在"); sys.exit(1)
        manifest, contents = parse_archive(open(sys.argv[2], 'r', encoding='utf-8').read())
        rebuild_directory(manifest, contents, sys.argv[3])
    else: print(f"未知命令: {cmd}"); sys.exit(1)

if __name__ == "__main__": main()