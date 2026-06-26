#!/usr/bin/env python3
"""
研报处理器 - 自动解析和提取研报关键信息
使用 qwen2.5:14b 模型进行内容提取
"""
import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
OLLAMA_MODEL = "qwen2.5:14b"
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "reports"

def ensure_output_dir():
    """确保输出目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_from_file(file_path):
    """从文件提取文本"""
    path = Path(file_path)
    
    if not path.exists():
        return None, f"文件不存在: {file_path}"
    
    # TXT 文件直接读取
    if path.suffix.lower() in ['.txt', '.md', '.text']:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read(), None
    
    # PDF 文件需要 pdftotext
    elif path.suffix.lower() == '.pdf':
        try:
            result = subprocess.run(
                ['pdftotext', str(path), '-'],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                return result.stdout, None
            else:
                return None, f"PDF 解析失败: {result.stderr}"
        except FileNotFoundError:
            return None, "请安装 pdftotext (poppler)"
        except Exception as e:
            return None, f"PDF 解析错误: {str(e)}"
    
    else:
        return None, f"不支持的文件格式: {path.suffix}"

def extract_with_ollama(text, prompt):
    """使用 Ollama 模型提取信息"""
    full_prompt = f"""
{prompt}

请从以下研报内容中提取信息：

---
{text[:50000]}  # 限制输入长度
---

请以 JSON 格式返回结果，包含以下字段：
- core_points: 核心观点（数组）
- key_data: 关键数据（对象）
- investment_advice: 投资建议（字符串）
- risk_warnings: 风险提示（数组）
"""
    
    try:
        result = subprocess.run(
            ['ollama', 'run', OLLAMA_MODEL, full_prompt],
            capture_output=True, text=True, timeout=180,
            env={**os.environ, 'OLLAMA_HOST': '127.0.0.1:11434'}
        )
        
        if result.returncode == 0:
            return result.stdout, None
        else:
            return None, f"Ollama 错误: {result.stderr}"
    except subprocess.TimeoutExpired:
        return None, "处理超时"
    except Exception as e:
        return None, str(e)

def parse_json_response(response_text):
    """解析模型返回的 JSON 响应"""
    try:
        # 尝试找到 JSON 块
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    return None

def process_report(file_path, output_format="json"):
    """处理单个研报文件"""
    print(f"📄 正在处理: {file_path}")
    
    # 1. 提取文本
    text, error = extract_text_from_file(file_path)
    if error:
        return {"success": False, "error": error}
    
    if not text or len(text) < 100:
        return {"success": False, "error": "文本内容过短"}
    
    print(f"   ✓ 提取文本 {len(text)} 字符")
    
    # 2. 提取关键信息
    prompt = "你是一个专业的金融分析师，请从研报中提取关键信息。"
    result_text, error = extract_with_ollama(text, prompt)
    if error:
        return {"success": False, "error": error}
    
    print(f"   ✓ 提取完成")
    
    # 3. 解析结果
    extracted = parse_json_response(result_text)
    
    # 4. 保存结果
    ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = Path(file_path).stem
    output_file = OUTPUT_DIR / f"{report_name}_{timestamp}.json"
    
    output_data = {
        "source_file": str(file_path),
        "processed_at": datetime.now().isoformat(),
        "extracted": extracted,
        "full_response": result_text[:5000] if result_text else ""
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"   ✓ 已保存到: {output_file}")
    
    return {
        "success": True,
        "output_file": str(output_file),
        "extracted": extracted
    }

def batch_process(directory):
    """批量处理目录下的所有研报"""
    directory = Path(directory)
    if not directory.exists():
        return {"success": False, "error": f"目录不存在: {directory}"}
    
    # 查找所有支持的文件
    extensions = ['.txt', '.md', '.pdf']
    files = []
    for ext in extensions:
        files.extend(directory.glob(f"*{ext}"))
    
    if not files:
        return {"success": False, "error": "未找到可处理的文件"}
    
    results = []
    for file in files:
        result = process_report(file)
        results.append(result)
    
    return {
        "success": True,
        "total": len(files),
        "results": results
    }

def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python report_processor.py <file>           # 处理单个文件")
        print("  python report_processor.py <directory>      # 批量处理")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isfile(target):
        result = process_report(target)
    elif os.path.isdir(target):
        result = batch_process(target)
    else:
        result = {"success": False, "error": "无效的路径"}
    
    print("\n" + "="*50)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
