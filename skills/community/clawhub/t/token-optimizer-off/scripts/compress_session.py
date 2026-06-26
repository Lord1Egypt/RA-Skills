#!/usr/bin/env python3
"""
compress_session.py - 会话摘要压缩
将当前会话摘要压缩后更新到 latest-summary.md

用法:
  python3 compress_session.py                    # 压缩今日摘要
  python3 compress_session.py path/to/file.md    # 压缩指定文件
  python3 compress_session.py --text "内容..."   # 直接压缩文本

配置:
  自动使用 OpenClaw 的 AI 配置，无需额外配置
"""
import os
import sys
import json
import shutil
import argparse
import time
import stat
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from glob import glob

# ============================================================
# 默认配置
# ============================================================
DEFAULT_CONFIG = {
    'memory_dir': '~/.openclaw/memory',
    'max_tokens': 1500,
    'max_chars': 2000,
    'max_retries': 3,
    'timeout': 30,
}


def load_openclaw_config() -> Dict:
    """
    从 OpenClaw 配置加载 AI 设置
    优先级：环境变量 > OpenClaw 配置 > 默认值
    """
    config = DEFAULT_CONFIG.copy()

    # 1. 尝试从 OpenClaw 配置加载
    openclaw_config_file = Path.home() / '.openclaw' / 'config.json'
    if openclaw_config_file.exists():
        # 检查配置文件权限（安全性）
        check_file_permissions(openclaw_config_file)

        try:
            with open(openclaw_config_file, encoding='utf-8') as f:
                openclaw_config = json.load(f)

                # 提取 AI 配置
                if 'ai' in openclaw_config:
                    ai_config = openclaw_config['ai']
                    config['api_url'] = ai_config.get('baseURL', 'https://api.openai.com/v1')
                    config['api_key'] = ai_config.get('apiKey', '')
                    config['model'] = ai_config.get('model', 'gpt-4')
                elif 'llm' in openclaw_config:
                    llm_config = openclaw_config['llm']
                    config['api_url'] = llm_config.get('baseURL', 'https://api.openai.com/v1')
                    config['api_key'] = llm_config.get('apiKey', '')
                    config['model'] = llm_config.get('model', 'gpt-4')
        except Exception as e:
            print(f'[警告] OpenClaw 配置加载失败: {e}')

    # 2. 环境变量覆盖（用于高级用户自定义）
    if 'TOKEN_OPTIMIZER_API_KEY' in os.environ:
        config['api_key'] = os.environ['TOKEN_OPTIMIZER_API_KEY']
    if 'TOKEN_OPTIMIZER_MODEL' in os.environ:
        config['model'] = os.environ['TOKEN_OPTIMIZER_MODEL']
    if 'TOKEN_OPTIMIZER_API_URL' in os.environ:
        config['api_url'] = os.environ['TOKEN_OPTIMIZER_API_URL']

    # 展开路径
    config['memory_dir'] = os.path.expanduser(config['memory_dir'])

    return config


def check_file_permissions(filepath: Path):
    """
    检查文件权限，确保配置文件安全

    Args:
        filepath: 文件路径
    """
    try:
        file_stat = os.stat(filepath)
        file_mode = stat.S_IMODE(file_stat.st_mode)

        # 检查是否其他用户可读（权限过于宽松）
        if file_mode & stat.S_IROTH:
            print(f'[警告] 配置文件 {filepath} 权限过于宽松（其他用户可读）')
            print(f'       建议执行: chmod 600 {filepath}')
    except Exception:
        pass  # 权限检查失败不影响主流程


def cleanup_old_backups(sessions_dir: str, days: int = 7):
    """
    清理旧的备份文件

    Args:
        sessions_dir: 会话目录路径
        days: 保留最近几天的备份，默认7天
    """
    cutoff_time = (datetime.now() - timedelta(days=days)).timestamp()
    backup_pattern = os.path.join(sessions_dir, 'backup-*.md')

    cleaned = 0
    for backup_file in glob(backup_pattern):
        if os.path.getmtime(backup_file) < cutoff_time:
            try:
                os.remove(backup_file)
                cleaned += 1
            except Exception as e:
                print(f'[警告] 清理备份失败 {backup_file}: {e}')

    if cleaned > 0:
        print(f'[清理] 删除了 {cleaned} 个超过{days}天的旧备份')


def estimate_tokens(text: str) -> int:
    """
    估算文本的token数量
    中文约1.5字符/token，英文约4字符/token

    Args:
        text: 要估算的文本

    Returns:
        估算的token数
    """
    cn_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other_chars = len(text) - cn_chars
    return int(cn_chars * 0.7 + other_chars * 0.25)


def check_dependencies():
    """检查依赖"""
    try:
        import openai
    except ImportError:
        print('错误：缺少 openai 库')
        print('安装：pip install openai')
        sys.exit(1)


def ai_compress(text: str, config: Dict) -> str:
    """
    调用 AI 压缩文本
    
    Args:
        text: 要压缩的文本
        config: 配置字典
        
    Returns:
        压缩后的文本
        
    Raises:
        ValueError: 配置错误
        Exception: API 调用失败
    """
    check_dependencies()
    from openai import OpenAI, APIError, RateLimitError
    
    if not config.get('api_key'):
        raise ValueError(
            '未找到 AI 配置\n'
            '请确保 OpenClaw 已正确配置 AI 服务\n'
            '或设置环境变量: export TOKEN_OPTIMIZER_API_KEY="your-key"'
        )
    
    client = OpenAI(
        api_key=config['api_key'],
        base_url=config['api_url']
    )
    
    prompt = f"""将以下会话内容压缩到{config['max_chars']}字以内。

压缩要求：
1. 保留：关键配置、路径、已验证方案、错误教训、重要决策
2. 删除：过程描述、重复信息、调试输出、格式说明、冗余解释
3. 输出纯Markdown格式，不加任何额外解释

压缩示例：
原文：用户询问了股票投资的问题，我详细解释了K线图的使用方法，包括阳线、阴线、十字星等形态，还讲解了均线系统的5日、10日、20日、60日均线的作用，以及MACD指标的金叉死叉信号...
压缩：技术分析要点：K线看趋势（阳线涨/阴线跌/十字星变盘），均线判支撑压力（5/10/20/60日），MACD看金叉死叉。

原文：部署过程中遇到了依赖问题，先尝试了pip install但是报错，然后检查了Python版本发现是3.8，需要升级到3.10，升级后重新安装依赖，最终成功启动服务...
压缩：部署要点：需Python 3.10+，pip install依赖，服务已启动。教训：先检查Python版本。

---
待压缩内容：
{text}"""
    
    max_retries = config.get('max_retries', 3)
    timeout = config.get('timeout', 30)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=config['model'],
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=config['max_tokens'],
                timeout=timeout
            )
            return response.choices[0].message.content
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f'[限流] 等待 {wait_time}秒后重试...')
                time.sleep(wait_time)
            else:
                raise Exception(f'API 限流，已重试 {max_retries} 次: {e}')
                
        except APIError as e:
            if attempt < max_retries - 1:
                print(f'[API错误] {e}，重试中...')
                time.sleep(1)
            else:
                raise Exception(f'API 错误: {e}')
                
        except Exception as e:
            raise Exception(f'压缩失败: {e}')
    
    raise Exception('压缩失败：超过最大重试次数')


def compress_file(source: str, config: Dict, dry_run: bool = False) -> Dict:
    """
    压缩文件并更新 latest-summary.md

    Args:
        source: 源文件路径
        config: 配置字典
        dry_run: 是否为预览模式（不保存文件）

    Returns:
        压缩结果字典
    """
    sessions_dir = os.path.join(config['memory_dir'], 'sessions')
    latest_file = os.path.join(sessions_dir, 'latest-summary.md')
    
    os.makedirs(sessions_dir, exist_ok=True)
    
    with open(source, encoding='utf-8') as f:
        content = f.read()

    old_size = len(content)
    old_tokens = estimate_tokens(content)

    if old_size <= config['max_chars']:
        compressed = content
        print(f'[跳过] 内容已足够精简（{old_size}字符，约{old_tokens} tokens），无需压缩')
    else:
        print(f'[压缩] {old_size}字符（约{old_tokens} tokens）→ 目标{config["max_chars"]}字符...')
        try:
            compressed = ai_compress(content, config)
        except Exception as e:
            print(f'[错误] {e}')
            sys.exit(1)

    new_size = len(compressed)
    new_tokens = estimate_tokens(compressed)
    char_ratio = (1 - new_size / max(old_size, 1)) * 100
    token_ratio = (1 - new_tokens / max(old_tokens, 1)) * 100

    # 预览模式：只显示结果，不保存
    if dry_run:
        print(f'\n{"="*60}')
        print(f'[预览] 压缩结果（不会保存）：')
        print(f'{"="*60}')
        print(compressed)
        print(f'{"="*60}')
        return {
            'old_chars': old_size,
            'new_chars': new_size,
            'old_tokens': old_tokens,
            'new_tokens': new_tokens,
            'char_ratio': char_ratio,
            'token_ratio': token_ratio,
            'file': None,
            'dry_run': True
        }

    # 正常模式：保存文件
    sessions_dir = os.path.join(config['memory_dir'], 'sessions')
    latest_file = os.path.join(sessions_dir, 'latest-summary.md')

    # 备份旧 latest
    if os.path.exists(latest_file):
        backup = latest_file.replace(
            'latest-summary',
            f'backup-{datetime.now().strftime("%Y%m%d%H%M")}'
        )
        shutil.copy(latest_file, backup)
        print(f'[备份] {os.path.basename(backup)}')

    # 清理旧备份（保留最近7天）
    cleanup_old_backups(sessions_dir, days=7)

    # 写入新 latest
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write(f'# 会话摘要（压缩版）更新于 {today}\n\n{compressed}')

    return {
        'old_chars': old_size,
        'new_chars': new_size,
        'old_tokens': old_tokens,
        'new_tokens': new_tokens,
        'char_ratio': char_ratio,
        'token_ratio': token_ratio,
        'file': latest_file,
        'dry_run': False
    }


def compress_text(text: str, config: Dict) -> str:
    """
    直接压缩文本
    
    Args:
        text: 要压缩的文本
        config: 配置字典
        
    Returns:
        压缩后的文本
    """
    if len(text) <= config['max_chars']:
        return text
    
    try:
        return ai_compress(text, config)
    except Exception as e:
        print(f'[错误] {e}')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='会话摘要压缩工具（自动使用 OpenClaw AI 配置）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
配置说明:
  本工具自动使用 OpenClaw 的 AI 配置，无需额外配置。
  
  如需自定义，可设置环境变量:
    export TOKEN_OPTIMIZER_API_KEY="your-key"
    export TOKEN_OPTIMIZER_MODEL="gpt-4"

示例:
  python3 compress_session.py                    # 压缩今日摘要
  python3 compress_session.py path/to/file.md    # 压缩指定文件
  python3 compress_session.py --text "内容..."   # 直接压缩文本
  python3 compress_session.py --dry-run          # 预览压缩效果（不保存）
        """
    )
    
    parser.add_argument('file', nargs='?', help='要压缩的摘要文件路径')
    parser.add_argument('--text', help='直接压缩文本内容')
    parser.add_argument('--dry-run', action='store_true', help='预览模式：只显示压缩结果，不保存文件')

    args = parser.parse_args()
    
    # 加载配置
    config = load_openclaw_config()
    
    # 直接压缩文本
    if args.text:
        result = compress_text(args.text, config)
        print(result)
        return
    
    # 确定源文件
    if args.file:
        source = args.file
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        source = os.path.join(config['memory_dir'], 'sessions', f'{today}-summary.md')
    
    if not os.path.exists(source):
        print(f'[错误] 找不到文件: {source}')
        print(f'提示: 先创建今日摘要文件，或指定文件路径')
        sys.exit(1)
    
    # 压缩文件
    result = compress_file(source, config, dry_run=args.dry_run)

    if result.get('dry_run'):
        print(f'\n[预览] 字符: {result["old_chars"]} → {result["new_chars"]} (压缩{result["char_ratio"]:.1f}%)')
        print(f'       Token: {result["old_tokens"]} → {result["new_tokens"]} (节省{result["token_ratio"]:.1f}%)')
        print(f'\n💡 使用 --dry-run 查看预览，去掉该参数以实际保存')
    else:
        print(f'[完成] 字符: {result["old_chars"]} → {result["new_chars"]} (压缩{result["char_ratio"]:.1f}%)')
        print(f'       Token: {result["old_tokens"]} → {result["new_tokens"]} (节省{result["token_ratio"]:.1f}%)')
        print(f'[保存] {result["file"]}')


if __name__ == '__main__':
    main()
