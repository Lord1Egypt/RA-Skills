#!/usr/bin/env python3
"""
Workspace浏览器3.0 - 阶段1：基础架构和文件浏览
"""

from flask import Flask, jsonify, send_from_directory, send_file, request, render_template
import os
import re
from pathlib import Path
import mimetypes
import requests
import json
import time
import hashlib
import sqlite3
from datetime import datetime, timedelta
import config  # 导入配置文件

app = Flask(__name__)

# CORS支持 - 允许前端跨域访问
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# 处理OPTIONS预检请求
@app.route('/api/explain/<path:req_path>', methods=['OPTIONS'])
@app.route('/api/tree/<path:req_path>', methods=['OPTIONS'])
@app.route('/api/tree/', methods=['OPTIONS'])
@app.route('/api/file/<path:req_path>', methods=['OPTIONS'])
def handle_options(req_path=None):
    return '', 200

# 从配置文件导入配置
WORKSPACE_ROOT = config.WORKSPACE_ROOT
MAX_DIRECT_ITEMS = config.MAX_DIRECT_ITEMS
MAX_TOTAL_ITEMS = config.MAX_TOTAL_ITEMS
MAX_FILE_SIZE = config.MAX_FILE_SIZE
MAX_FILE_SIZE_FOR_EXPLANATION = config.MAX_FILE_SIZE_FOR_EXPLANATION
EXPLANATION_TIMEOUT = config.EXPLANATION_TIMEOUT
EXPLANATION_CACHE_DURATION = config.EXPLANATION_CACHE_DURATION
DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY
DEEPSEEK_API_URL = config.DEEPSEEK_API_URL

# 解释缓存
_explanation_cache = {}

# 请求统计（线程安全）
import threading
_request_stats_lock = threading.Lock()
_request_stats = {
    "total_explain_requests": 0,
    "successful_explanations": 0,
    "failed_explanations": 0,
    "active_requests": 0,
    "last_request_time": None,
    "peak_active_requests": 0
}

def update_request_stats(increment_active=0, increment_success=0, increment_failure=0):
    """更新请求统计（线程安全）"""
    global _request_stats
    with _request_stats_lock:
        _request_stats["total_explain_requests"] += 1
        if increment_active:
            _request_stats["active_requests"] += increment_active
            # 更新峰值
            if _request_stats["active_requests"] > _request_stats["peak_active_requests"]:
                _request_stats["peak_active_requests"] = _request_stats["active_requests"]
        if increment_success:
            _request_stats["successful_explanations"] += increment_success
        if increment_failure:
            _request_stats["failed_explanations"] += increment_failure
        _request_stats["last_request_time"] = datetime.now().isoformat()

def get_request_stats():
    """获取请求统计（线程安全）"""
    with _request_stats_lock:
        return _request_stats.copy()


def get_cached_explanation(file_path, content_hash):
    """获取缓存的解释"""
    if file_path in _explanation_cache:
        cached = _explanation_cache[file_path]
        if cached["content_hash"] == content_hash:
            if time.time() - cached["timestamp"] < EXPLANATION_CACHE_DURATION:
                return cached["explanation"]
    return None


def set_cached_explanation(file_path, content_hash, explanation):
    """设置解释缓存"""
    _explanation_cache[file_path] = {
        "explanation": explanation,
        "content_hash": content_hash,
        "timestamp": time.time()
    }


# 数据库操作函数
def get_db_connection():
    """获取数据库连接"""
    db_path = os.path.join(os.path.dirname(__file__), 'explanations.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 返回字典格式
    return conn


def calculate_file_hash(file_path, content=None):
    """计算文件内容的哈希值"""
    if content is None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 非文本文件，读取二进制计算哈希
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
    
    # 文本文件，使用内容计算哈希
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def get_database_stats():
    """获取数据库统计信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 获取记录总数
        cursor.execute('SELECT COUNT(*) FROM file_explanations')
        total_records = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute('SELECT explanation_type, COUNT(*) FROM file_explanations GROUP BY explanation_type')
        type_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 获取最新更新时间
        cursor.execute('SELECT MAX(updated_at) FROM file_explanations')
        last_updated = cursor.fetchone()[0]
        
        # 获取文件路径示例
        cursor.execute('SELECT file_path, explanation_type, updated_at FROM file_explanations ORDER BY updated_at DESC LIMIT 3')
        recent_records = [
            {
                'file_path': row[0],
                'explanation_type': row[1],
                'updated_at': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        return {
            'total_records': total_records,
            'type_counts': type_counts,
            'last_updated': last_updated,
            'recent_records': recent_records,
            'database_file': 'explanations.db',
            'table_exists': True
        }
    except Exception as e:
        print(f"获取数据库统计失败: {e}")
        return {
            'total_records': 0,
            'type_counts': {},
            'last_updated': None,
            'recent_records': [],
            'database_file': 'explanations.db',
            'table_exists': False,
            'error': str(e)
        }
    finally:
        conn.close()


def save_explanation_to_db(file_path, file_hash, explanation_type, content):
    """保存解释到数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 尝试更新现有记录
        cursor.execute('''
            UPDATE file_explanations 
            SET explanation_type = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE file_path = ? AND file_hash = ?
        ''', (explanation_type, content, file_path, file_hash))
        
        action = "更新" if cursor.rowcount > 0 else "插入"
        
        # 如果没有更新任何行，则插入新记录
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO file_explanations (file_path, file_hash, explanation_type, content)
                VALUES (?, ?, ?, ?)
            ''', (file_path, file_hash, explanation_type, content))
        
        conn.commit()
        print(f"✅ 解释保存成功: {action}记录，文件: {file_path}, 类型: {explanation_type}")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ 保存解释到数据库失败: {e}")
        print(f"   文件: {file_path}, 哈希: {file_hash[:8]}..., 类型: {explanation_type}")
        return False
    finally:
        conn.close()


def get_explanation_from_db(file_path, file_hash):
    """从数据库获取解释"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT explanation_type, content, created_at, updated_at
            FROM file_explanations
            WHERE file_path = ? AND file_hash = ?
        ''', (file_path, file_hash))
        
        row = cursor.fetchone()
        if row:
            print(f"✅ 从数据库加载解释: {file_path}, 类型: {row[0]}, 更新时间: {row[3]}")
            return {
                'explanation_type': row[0],
                'content': row[1],
                'created_at': row[2],
                'updated_at': row[3],
                'source': 'database'
            }
        return None
    except Exception as e:
        print(f"❌ 从数据库获取解释失败: {e}")
        print(f"   文件: {file_path}, 哈希: {file_hash[:8]}...")
        return None
    finally:
        conn.close()


# 安全路径验证
def normalize_and_validate_path(requested_path):
    """
    规范化并验证请求路径是否在WORKSPACE_ROOT内
    返回绝对路径和相对于工作空间的路径
    """
    if not requested_path:
        return WORKSPACE_ROOT, ""
    
    # 移除开头的斜杠
    requested_path = requested_path.lstrip('/')
    
    # 构造绝对路径
    abs_path = os.path.join(WORKSPACE_ROOT, requested_path)
    
    # 规范化路径（解析..等）
    abs_path = os.path.normpath(abs_path)
    
    # 验证是否仍在工作空间内
    if not abs_path.startswith(WORKSPACE_ROOT):
        raise ValueError("路径越界访问")
    
    # 检查路径是否存在
    if not os.path.exists(abs_path):
        raise FileNotFoundError("文件或目录不存在")
    
    return abs_path, requested_path

# API: 健康检查
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "workspace-browser-3.0",
        "version": "stage1",
        "workspace_root": WORKSPACE_ROOT
    })

# API: 测试DeepSeek连接
@app.route('/api/test-deepseek')
def test_deepseek():
    """测试DeepSeek API连接"""
    try:
        # 简单的测试请求
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.AI_MODEL,
            "messages": [
                {"role": "system", "content": "你是一个测试助手。"},
                {"role": "user", "content": "请简单回复'DeepSeek API连接正常'来确认连接正常。"}
            ],
            "max_tokens": 20,
            "temperature": 0.1
        }
        
        start_time = time.time()
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "status": "success",
                "message": "DeepSeek API连接正常",
                "response": result["choices"][0]["message"]["content"],
                "response_time": f"{elapsed:.2f}秒",
                "model": config.AI_MODEL
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"DeepSeek API调用失败: {response.status_code}",
                "response": response.text[:200],
                "response_time": f"{elapsed:.2f}秒"
            }), 500
            
    except requests.exceptions.ConnectionError as e:
        return jsonify({
            "status": "error",
            "message": "网络连接失败",
            "detail": str(e),
            "advice": "请检查网络连接和代理设置"
        }), 503
    except requests.exceptions.Timeout as e:
        return jsonify({
            "status": "error",
            "message": "请求超时",
            "detail": str(e),
            "advice": f"API响应超过30秒，可能需要增加超时时间"
        }), 504
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "未知错误",
            "detail": str(e),
            "error_type": type(e).__name__
        }), 500

# API: 获取目录树
@app.route('/api/tree/')
@app.route('/api/tree/<path:req_path>')
def get_tree(req_path=''):
    try:
        abs_path, rel_path = normalize_and_validate_path(req_path)
        
        if not os.path.isdir(abs_path):
            return jsonify({"error": "不是目录"}), 400
        
        items = []
        total_items_count = 0
        
        # 获取所有项目
        all_items = []
        for item_name in sorted(os.listdir(abs_path)):
            if item_name.startswith('.'):
                continue  # 隐藏文件
            
            item_path = os.path.join(abs_path, item_name)
            item_rel_path = os.path.join(rel_path, item_name) if rel_path else item_name
            
            is_dir = os.path.isdir(item_path)
            
            # 统计子项数量（仅目录）
            item_count = 0
            if is_dir:
                try:
                    dir_items = [f for f in os.listdir(item_path) if not f.startswith('.')]
                    item_count = len(dir_items)
                    total_items_count += item_count
                except:
                    item_count = 0
            
            item_info = {
                "name": item_name,
                "path": item_rel_path,
                "is_dir": is_dir,
                "size": os.path.getsize(item_path) if not is_dir else 0,
                "item_count": item_count,
                "mtime": int(os.path.getmtime(item_path)),
                "ctime": int(os.path.getctime(item_path))
            }
            
            # 检查子文件夹是否超过限制
            if is_dir and item_count > MAX_DIRECT_ITEMS:
                item_info["exceeds_limit"] = True
                item_info["limit_message"] = f"文件夹内项目过多 ({item_count} > {MAX_DIRECT_ITEMS})，为避免性能问题暂不展开显示"
            else:
                item_info["exceeds_limit"] = False
            
            all_items.append(item_info)
        
        # 检查当前目录是否超过显示限制
        total_items = len(all_items)
        truncated = False
        display_items = all_items
        
        if total_items > config.MAX_DISPLAY_ITEMS:
            # 只显示前MAX_DISPLAY_ITEMS个项目
            display_items = all_items[:config.MAX_DISPLAY_ITEMS]
            truncated = True
        
        # 目录在前，文件在后
        display_items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        
        response = {
            "items": display_items,
            "count": len(display_items),
            "total_items_count": total_items_count,
            "total_original_items": total_items,  # 原始项目总数
            "truncated": truncated,  # 是否被截断
            "max_display_items": config.MAX_DISPLAY_ITEMS,  # 最大显示数量
            "path": rel_path,
            "exceeds_total_limit": total_items_count > MAX_TOTAL_ITEMS,
            "limits": {
                "max_direct_items": MAX_DIRECT_ITEMS,
                "max_total_items": MAX_TOTAL_ITEMS,
                "max_display_items": config.MAX_DISPLAY_ITEMS
            }
        }
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 解释生成相关函数
def generate_explanation_for_file(file_path, content, language, filename):
    """
    为文件生成解释
    策略：先尝试DeepSeek API，失败则返回模拟数据
    """
    # 内容哈希用于缓存
    import hashlib
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    
    # 检查缓存
    cached = get_cached_explanation(file_path, content_hash)
    if cached:
        return {
            **cached,
            "source": "cache",
            "cached": True
        }
    
    # 使用配置文件中的提示词模板
    prompt = config.EXPLANATION_PROMPT_TEMPLATE.format(
        language=language,
        content=content
    )
    
    try:
        # 调用DeepSeek API
        print(f"[AI解释] 开始为文件生成解释: {filename} ({len(content)}字节, {language})")
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.AI_MODEL,
            "messages": [
                {"role": "system", "content": config.AI_SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": config.AI_MAX_TOKENS,
            "temperature": config.AI_TEMPERATURE
        }
        
        print(f"[AI解释] 发送请求到DeepSeek API，超时: {EXPLANATION_TIMEOUT}秒")
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=EXPLANATION_TIMEOUT
        )
        
        # 检查HTTP状态码，如果不是200会抛出HTTPError
        response.raise_for_status()
        
        elapsed = time.time() - start_time
        
        # 状态码为200，处理成功响应
        result = response.json()
        explanation_text = result["choices"][0]["message"]["content"]
        
        print(f"[AI解释] ✅ API调用成功! 耗时: {elapsed:.2f}秒，响应长度: {len(explanation_text)}字符")
        
        explanation = {
            "id": f"explain_{int(time.time())}",
            "content": explanation_text,
            "language": language,
            "file_path": file_path,
            "filename": filename,
            "generated_at": datetime.now().isoformat(),
            "source": "deepseek_api",
            "model": config.AI_MODEL,
            "response_time": elapsed
        }
        
        # 缓存结果
        set_cached_explanation(file_path, content_hash, explanation)
        
        return explanation
            
    except requests.exceptions.ConnectionError as e:
        # 网络连接错误
        elapsed = time.time() - start_time
        error_type = "网络连接失败"
        error_detail = "无法连接到DeepSeek API服务器，请检查网络连接。"
        print(f"[AI解释] ❌ 网络连接错误: {e} (耗时: {elapsed:.2f}秒)")
    except requests.exceptions.Timeout as e:
        # 请求超时
        elapsed = time.time() - start_time
        error_type = "请求超时"
        error_detail = f"API请求超时（{EXPLANATION_TIMEOUT}秒），可能是网络慢或服务器响应慢。"
        print(f"[AI解释] ❌ 请求超时: {e} (耗时: {elapsed:.2f}秒，超时设置: {EXPLANATION_TIMEOUT}秒)")
    except requests.exceptions.HTTPError as e:
        # HTTP错误
        elapsed = time.time() - start_time
        error_type = f"HTTP错误 {e.response.status_code}"
        if e.response.status_code == 401:
            error_detail = "API密钥无效或已过期，请检查密钥配置。"
        elif e.response.status_code == 403:
            error_detail = "API权限不足，请检查密钥权限。"
        elif e.response.status_code == 429:
            error_detail = "API请求过于频繁，请稍后重试。"
        else:
            error_detail = f"HTTP错误: {e.response.status_code}"
        print(f"[AI解释] ❌ HTTP错误: {e.response.status_code}, {e.response.text[:200]} (耗时: {elapsed:.2f}秒)")
    except (KeyError, json.JSONDecodeError) as e:
        # API响应格式错误
        elapsed = time.time() - start_time
        error_type = "API响应格式错误"
        error_detail = "DeepSeek API返回了无法解析的响应格式。"
        print(f"[AI解释] ❌ API响应格式错误: {e} (耗时: {elapsed:.2f}秒)")
    except Exception as e:
        # 其他未知错误
        elapsed = time.time() - start_time
        error_type = "未知错误"
        error_detail = f"未知错误: {str(e)[:200]}"
        print(f"[AI解释] ❌ 未知错误: {type(e).__name__}: {e} (耗时: {elapsed:.2f}秒)")
    
    # 降级到模拟数据
    print(f"[AI解释] ⚠️ 生成解释失败，降级到模拟数据: {error_type} (总耗时: {elapsed:.2f}秒)")
    
    # 生成模拟解释数据，包含具体错误原因
    mock_explanation = {
        "id": f"mock_{int(time.time())}",
        "content": f"# {filename} 的代码解释\n\n**文件信息**\n- 语言: {language}\n- 大小: {len(content)} 字节\n- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n**代码概述**\n这是一个{language}代码文件，包含约{len(content.split('\\n'))}行代码。\n\n**⚠️ AI解释服务暂时不可用**\n\n**错误原因**: {error_type}\n**详细说明**: {error_detail}\n\n**后续步骤**\n1. 检查错误原因并修复\n2. 稍后重试获取真实AI解释\n3. 如需帮助，请联系系统管理员",
        "language": language,
        "file_path": file_path,
        "filename": filename,
        "generated_at": datetime.now().isoformat(),
        "source": "mock_fallback",
        "model": "mock",
        "error_type": error_type,
        "error_detail": error_detail,
        "response_time": elapsed
    }
    
    return mock_explanation


# API: 获取文件内容
@app.route('/api/file/<path:req_path>')
def get_file(req_path):
    try:
        abs_path, rel_path = normalize_and_validate_path(req_path)
        
        if os.path.isdir(abs_path):
            return jsonify({"error": "目录无法作为文件读取"}), 400
        
        # 检查文件大小（防止读取过大文件）
        file_size = os.path.getsize(abs_path)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "error": "文件过大",
                "size": file_size,
                "max_size": MAX_FILE_SIZE,
                "download_url": f"/api/download/{rel_path}"
            }), 413
        
        # 读取文件内容
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 非文本文件
            content = None
        
        # 检测文件类型
        mime_type, _ = mimetypes.guess_type(abs_path)
        
        # 检测是否为代码文件
        code_extensions = {'.py', '.js', '.html', '.css', '.json', '.md', '.java', 
                          '.cpp', '.c', '.go', '.rs', '.php', '.ts', '.jsx', '.tsx',
                          '.vue', '.swift', '.kt', '.scala', '.rb', '.pl', '.sh', '.bash'}
        ext = os.path.splitext(abs_path)[1].lower()
        is_code = ext in code_extensions
        
        # 检测语言，使用配置文件中的映射
        language = config.LANGUAGE_MAP.get(ext, 'text')
        
        response = {
            "name": os.path.basename(abs_path),
            "path": rel_path,
            "size": file_size,
            "mtime": int(os.path.getmtime(abs_path)),
            "ctime": int(os.path.getctime(abs_path)),
            "is_code": is_code,
            "language": language,
            "mime_type": mime_type or 'application/octet-stream',
            "download_url": f"/api/download/{rel_path}"
        }
        
        if content is not None:
            response["content"] = content
            response["lines"] = len(content.splitlines())
        else:
            response["content"] = None
            response["lines"] = 0
            response["is_binary"] = True
        
        return jsonify(response)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# API: 下载文件
@app.route('/api/download/<path:req_path>')
def download_file(req_path):
    try:
        abs_path, rel_path = normalize_and_validate_path(req_path)
        
        if os.path.isdir(abs_path):
            return jsonify({"error": "无法下载目录"}), 400
        
        # 使用send_file允许浏览器下载
        return send_file(
            abs_path,
            as_attachment=True,
            download_name=os.path.basename(abs_path),
            mimetype='application/octet-stream'
        )
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@app.route('/api/search')
def search_files():
    """搜索文件"""
    try:
        query = request.args.get('q', '').strip().lower()
        if not query:
            return jsonify({'items': [], 'count': 0})
        
        results = []
        workspace_root = config.WORKSPACE_ROOT
        
        # 使用os.walk一次性遍历所有文件
        for root, dirs, files in os.walk(workspace_root):
            # 搜索文件夹
            for dir_name in dirs:
                if query in dir_name.lower():
                    dir_path = os.path.join(root, dir_name)
                    rel_path = os.path.relpath(dir_path, workspace_root)
                    
                    # 统计文件夹中的项目数量
                    try:
                        dir_items = os.listdir(dir_path)
                        item_count = len(dir_items)
                        exceeds_limit = item_count > config.MAX_DIRECT_ITEMS
                    except:
                        item_count = 0
                        exceeds_limit = False
                    
                    results.append({
                        'path': rel_path,
                        'name': dir_name,
                        'is_dir': True,
                        'size': 0,
                        'item_count': min(item_count, config.MAX_DIRECT_ITEMS) if not exceeds_limit else config.MAX_DIRECT_ITEMS,
                        'exceeds_limit': exceeds_limit,
                        'parent': os.path.dirname(rel_path) if rel_path != '.' else ''
                    })
            
            # 搜索文件
            for file_name in files:
                if query in file_name.lower():
                    file_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(file_path, workspace_root)
                    
                    try:
                        size = os.path.getsize(file_path)
                    except:
                        size = 0
                    
                    results.append({
                        'path': rel_path,
                        'name': file_name,
                        'is_dir': False,
                        'size': size,
                        'parent': os.path.dirname(rel_path)
                    })
        
        # 按路径排序，使结果更有组织性
        results.sort(key=lambda x: x['path'])
        
        # 限制结果数量，避免前端性能问题
        max_results = 200
        if len(results) > max_results:
            results = results[:max_results]
        
        return jsonify({
            'items': results,
            'count': len(results),
            'truncated': len(results) >= max_results
        })
        
    except Exception as e:
        print(f'搜索失败: {e}')
        return jsonify({'error': str(e), 'items': [], 'count': 0}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500

# 主页面
@app.route('/')
@app.route('/')
def index():
    return render_template('index.html')

# API: 生成代码解释
@app.route('/api/explain/<path:req_path>')
def explain_file(req_path):
    """生成代码文件的AI解释"""
    try:
        abs_path, rel_path = normalize_and_validate_path(req_path)
        
        if os.path.isdir(abs_path):
            return jsonify({"error": "目录无法生成解释"}), 400
        
        # 检查文件大小
        file_size = os.path.getsize(abs_path)
        if file_size > MAX_FILE_SIZE_FOR_EXPLANATION:
            return jsonify({
                "error": f"文件太大({file_size}字节)，超过{MAX_FILE_SIZE_FOR_EXPLANATION}字节限制",
                "max_size": MAX_FILE_SIZE_FOR_EXPLANATION
            }), 400
        
        # 读取文件内容
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            return jsonify({"error": "文件不是UTF-8文本格式，无法生成解释"}), 400
        except Exception as e:
            return jsonify({"error": f"读取文件失败: {str(e)}"}), 500
        
        # 获取文件扩展名和语言
        import mimetypes
        from pathlib import Path
        
        filename = Path(abs_path).name
        ext = Path(abs_path).suffix.lower()
        
        # 使用配置文件中的语言映射
        language = config.LANGUAGE_MAP.get(ext, 'text')
        
        # 计算文件哈希
        file_hash = calculate_file_hash(abs_path, content)
        
        # 先检查数据库是否有解释
        db_explanation = get_explanation_from_db(rel_path, file_hash)
        if db_explanation:
            print(f"[解释] 从数据库返回现有解释: {filename}")
            return jsonify({
                "id": f"db_explain_{int(time.time())}",
                "content": db_explanation['content'],
                "language": language,
                "file_path": rel_path,
                "filename": filename,
                "generated_at": db_explanation['created_at'],
                "updated_at": db_explanation['updated_at'],
                "source": "database",
                "explanation_type": db_explanation['explanation_type'],
                "saved_in_db": True
            })
        
        # 生成新的AI解释
        explanation = generate_explanation_for_file(rel_path, content, language, filename)
        
        # 保存到数据库
        if explanation and 'content' in explanation:
            explanation_type = 'ai' if explanation.get('source') in ['deepseek_api', 'cache'] else 'ai_fallback'
            save_success = save_explanation_to_db(rel_path, file_hash, explanation_type, explanation['content'])
            explanation['saved_in_db'] = save_success
            if save_success:
                explanation['source'] = 'database'  # 标记为来自数据库
        
        return jsonify(explanation)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@app.route('/api/save_manual_explanation/<path:req_path>', methods=['POST'])
def save_manual_explanation(req_path):
    """保存手动输入的解释"""
    try:
        abs_path, rel_path = normalize_and_validate_path(req_path)
        
        if os.path.isdir(abs_path):
            return jsonify({"error": "目录无法保存解释"}), 400
        
        # 获取POST数据
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({"error": "缺少解释内容"}), 400
        
        explanation_content = data['content'].strip()
        if not explanation_content:
            return jsonify({"error": "解释内容不能为空"}), 400
        
        # 读取文件内容用于计算哈希
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except UnicodeDecodeError:
            # 非文本文件，尝试二进制读取
            with open(abs_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return jsonify({"error": f"读取文件失败: {str(e)}"}), 500
        else:
            # 文本文件
            file_hash = hashlib.md5(file_content.encode('utf-8')).hexdigest()
        
        # 保存到数据库
        save_success = save_explanation_to_db(rel_path, file_hash, 'manual', explanation_content)
        
        if save_success:
            return jsonify({
                "success": True,
                "message": "手动解释已保存到数据库",
                "file_path": rel_path,
                "explanation_type": "manual",
                "saved_at": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": "保存到数据库失败"}), 500
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@app.route('/api/check_explanation/<path:req_path>', methods=['GET'])
def check_explanation(req_path):
    """检查文件是否有解释（不生成新解释）"""
    try:
        abs_path, rel_path = normalize_and_validate_path(req_path)
        
        if os.path.isdir(abs_path):
            return jsonify({"has_explanation": False, "reason": "目录无法有解释"})
        
        # 计算文件哈希
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
                file_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        except UnicodeDecodeError:
            # 非文本文件，尝试二进制读取
            with open(abs_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return jsonify({"has_explanation": False, "reason": f"读取文件失败: {str(e)}"})
        
        # 检查数据库
        db_explanation = get_explanation_from_db(rel_path, file_hash)
        
        if db_explanation:
            return jsonify({
                "has_explanation": True,
                "explanation_type": db_explanation['explanation_type'],
                "source": "database",
                "content": db_explanation['content'],
                "created_at": db_explanation['created_at'],
                "updated_at": db_explanation['updated_at']
            })
        else:
            return jsonify({"has_explanation": False, "reason": "数据库中无解释"})
        
    except ValueError as e:
        return jsonify({"has_explanation": False, "reason": str(e)}), 403
    except FileNotFoundError as e:
        return jsonify({"has_explanation": False, "reason": str(e)}), 404
    except Exception as e:
        return jsonify({"has_explanation": False, "reason": f"服务器错误: {str(e)}"}), 500


@app.route('/api/status')
def app_status():
    """返回应用状态和开发进展"""
    # 获取数据库统计
    db_stats = get_database_stats()
    
    # 更新系统说明，添加数据库状态
    system_notes = [
        "应用正常运行中，所有功能可用",
        "AI解释服务使用DeepSeek API，已配置60秒超时",
        f"解释结果自动保存到SQLite数据库，当前保存记录数: {db_stats['total_records']}",
        "前端有90秒请求超时控制，避免长时间等待",
        "支持手动输入解释，适合AI服务不可用时",
        "消息通道当前有问题，无法通过Feishu发送回复"
    ]
    
    return jsonify({
        "service": "workspace-browser-3.0",
        "status": "healthy",
        "version": "stage1+enhancements",
        "workspace_root": config.WORKSPACE_ROOT,
        "database_stats": db_stats,
        "development_status": {
            "phase": "阶段2完善中",
            "completed_features": [
                "数据库持久化系统（explanations.db）",
                "界面极简重构",
                "手动输入界面（嵌入式大文本输入框）",
                "复制代码功能优化",
                "美学升级（卡片式设计）",
                "双Tab系统（源代码 + 解释）",
                "代码语法高亮（Prism.js）",
                "AI解释按钮和基础交互",
                "解释结果显示",
                "基本缓存机制（SQLite数据库）"
            ],
            "in_progress": [
                "解释任务队列管理系统",
                "AI解释质量优化",
                "错误处理改进",
                "性能优化"
            ],
            "next_priorities": [
                "实现任务队列避免并发问题",
                "添加进度指示和状态反馈",
                "优化数据库查询性能",
                "全面测试所有功能"
            ]
        },
        "system_notes": system_notes,
        "request_stats": get_request_stats(),
        "timestamp": datetime.now().isoformat(),
        "health_check": "/health",
        "main_page": "/"
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Workspace浏览器3.0 - 阶段1：基础架构和文件浏览")
    print("=" * 60)
    print("功能:")
    print("  1. ✅ 安全路径验证和文件系统API")
    print("  2. ✅ 500px侧边栏文件树")
    print("  3. ✅ 马卡龙色系基础UI")
    print("  4. ✅ 文件内容查看和下载")
    print("  5. ✅ 代码文件识别和基础显示")
    print("=" * 60)
    print("访问地址: http://0.0.0.0:5001")
    print("健康检查: http://0.0.0.0:5001/health")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0', 
        port=5001, 
        debug=False, 
        use_reloader=False,
        threaded=True
    )

# 静态文件路由
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

def init_database():
    """初始化SQLite数据库"""
    try:
        # 确保数据库文件在应用目录中
        import os
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explanations.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建文件解释表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_explanations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                explanation_type TEXT NOT NULL,  -- 'ai' or 'manual'
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_hash ON file_explanations(file_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_path ON file_explanations(file_path)')
        
        conn.commit()
        conn.close()
        
        print('✅ 数据库初始化完成: explanations.db')
        print('   表: file_explanations')
        print('   字段: id, file_path, file_hash, explanation_type, content, created_at, updated_at')
        return True
    except Exception as e:
        print(f'❌ 数据库初始化失败: {e}')
        return False

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    
    # 获取配置
    port = getattr(config, 'PORT', 5001)
    debug = getattr(config, 'DEBUG', False)
    host = getattr(config, 'HOST', '0.0.0.0')
    
    print(f'Workspace浏览器3.0 已启动（分离结构版）')
    print(f'访问地址: http://{host}:{port}')
    print(f'日志文件: app.log')
    print(f'前端文件: templates/index.html, static/css/style.css, static/js/app.js')
    
    app.run(host=host, port=port, debug=debug)
