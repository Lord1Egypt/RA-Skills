#!/usr/bin/env python3
"""
轻量级标注数据 API 服务
提供数据文件列表、文件内容读取、标注数据保存等功能。

用法:
    python3 annotation-api.py --port 8888 --data-dir /path/to/data
"""

import json
import os
import sys
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 全局配置
DATA_DIR = '/root/annotation-data'


class AnnotationHandler(SimpleHTTPRequestHandler):
    """处理标注数据的 HTTP 请求"""

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == '/':
            # 列出数据文件和标注结果
            data_dir = params.get('dir', [DATA_DIR])[0]
            results_file = params.get('results', [''])[0]
            
            files = self._list_files(data_dir)
            annotations = {}
            
            if results_file and os.path.exists(results_file):
                annotations = self._load_annotations(results_file)
            
            self._send_json({
                'files': files,
                'annotations': annotations,
                'dataDir': data_dir,
                'resultsFile': results_file
            })
        
        elif parsed.path == '/file':
            # 返回文件内容
            file_path = params.get('path', [''])[0]
            if not file_path or not os.path.exists(file_path):
                self._send_json({'error': '文件不存在'}, 404)
                return
            
            # 安全检查：确保文件在 DATA_DIR 下
            real_path = os.path.realpath(file_path)
            real_data = os.path.realpath(DATA_DIR)
            if not real_path.startswith(real_data):
                self._send_json({'error': '无权访问'}, 403)
                return
            
            content_type = self._guess_type(file_path)
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content)
        
        else:
            self._send_json({'error': '未知接口'}, 404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({'error': '无效的 JSON'}, 400)
            return

        if data.get('action') == 'save':
            annotations = data.get('annotations', {})
            results_file = data.get('file', '')
            
            if not results_file:
                # 默认保存到 DATA_DIR 下的 annotations.jsonl
                results_file = os.path.join(DATA_DIR, 'annotations.jsonl')
            
            # 确保目录存在
            os.makedirs(os.path.dirname(results_file), exist_ok=True)
            
            # 保存为 JSONL
            saved = 0
            with open(results_file, 'w', encoding='utf-8') as f:
                for source, ann in annotations.items():
                    if isinstance(ann, dict):
                        ann['source_file'] = source
                        f.write(json.dumps(ann, ensure_ascii=False) + '\n')
                        saved += 1
            
            self._send_json({'success': True, 'saved': saved, 'file': results_file})
        else:
            self._send_json({'error': '未知操作'}, 400)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _list_files(self, data_dir):
        """递归列出数据目录中的文件"""
        files = []
        if not os.path.exists(data_dir):
            return files
        
        image_ext = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}
        video_ext = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
        text_ext = {'.txt', '.md', '.csv', '.json', '.jsonl'}
        
        for root, dirs, filenames in os.walk(data_dir):
            dirs.sort()
            for fname in sorted(filenames):
                fpath = os.path.join(root, fname)
                ext = os.path.splitext(fname)[1].lower()
                
                ftype = 'other'
                if ext in image_ext:
                    ftype = 'image'
                elif ext in video_ext:
                    ftype = 'video'
                elif ext in text_ext:
                    ftype = 'text'
                
                # 跳过 results 目录下的文件
                if '/results/' in fpath.replace('\\', '/'):
                    continue
                
                files.append({
                    'path': fpath,
                    'name': fname,
                    'type': ftype,
                    'size': os.path.getsize(fpath)
                })
        
        return files

    def _load_annotations(self, results_file):
        """从 JSONL 文件加载标注数据"""
        annotations = {}
        if not os.path.exists(results_file):
            return annotations
        
        with open(results_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    source = obj.pop('source_file', '')
                    if source:
                        annotations[source] = obj
                except json.JSONDecodeError:
                    continue
        
        return annotations

    def _guess_type(self, path):
        """根据文件扩展名猜测 MIME 类型"""
        ext = os.path.splitext(path)[1].lower()
        types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
            '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml',
            '.mp4': 'video/mp4', '.avi': 'video/x-msvideo', '.mov': 'video/quicktime',
            '.txt': 'text/plain', '.md': 'text/markdown', '.csv': 'text/csv',
            '.json': 'application/json', '.jsonl': 'application/jsonl',
        }
        return types.get(ext, 'application/octet-stream')

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
    
    def log_message(self, format, *args):
        print(f"[annotation-api] {args[0]}")


def main():
    global DATA_DIR
    parser = argparse.ArgumentParser(description='标注数据 API 服务')
    parser.add_argument('--port', type=int, default=8888, help='监听端口')
    parser.add_argument('--data-dir', type=str, default=DATA_DIR, help='数据根目录')
    args = parser.parse_args()
    
    DATA_DIR = args.data_dir
    
    if not os.path.exists(DATA_DIR):
        print(f"警告: 数据目录不存在: {DATA_DIR}")
        os.makedirs(DATA_DIR, exist_ok=True)
    
    server = HTTPServer(('127.0.0.1', args.port), AnnotationHandler)
    print(f"标注 API 服务已启动: http://127.0.0.1:{args.port}")
    print(f"数据目录: {DATA_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.server_close()


if __name__ == '__main__':
    main()
