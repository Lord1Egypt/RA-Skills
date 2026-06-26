#!/usr/bin/env python3
"""
编码处理工具模块 - 修复版
解决跨平台兼容性问题，特别是Windows系统的编码问题
"""

import sys
import os
import locale

def get_system_encoding():
    """获取系统编码"""
    try:
        encoding = locale.getpreferredencoding()
        if not encoding:
            encoding = sys.getdefaultencoding()
        return encoding.lower()
    except:
        return 'utf-8'

def is_windows():
    """检查是否在Windows系统上"""
    return sys.platform.startswith('win')

def safe_print(*args, **kwargs):
    """
    安全的打印函数，自动处理编码问题
    支持所有print参数
    """
    # 提取参数
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    file = kwargs.get('file', None)
    flush = kwargs.get('flush', False)
    
    # 构建要打印的文本
    text = sep.join(str(arg) for arg in args) + end
    
    if file:
        # 对于文件输出，使用原始print
        file.write(text)
        if flush:
            file.flush()
        return
    
    # 对于控制台输出，处理编码
    if is_windows():
        # Windows系统：清理文本
        cleaned_text = remove_all_unsupported_chars(text)
        try:
            sys.stdout.write(cleaned_text)
            if flush:
                sys.stdout.flush()
        except:
            # 如果失败，尝试ASCII-only
            try:
                ascii_text = text.encode('ascii', 'ignore').decode('ascii')
                sys.stdout.write(ascii_text)
                if flush:
                    sys.stdout.flush()
            except:
                # 最后的手段
                sys.stdout.write('[...]\n')
    else:
        # 非Windows系统
        try:
            sys.stdout.write(text)
            if flush:
                sys.stdout.flush()
        except UnicodeEncodeError:
            # 如果有编码问题，清理文本
            cleaned_text = remove_all_unsupported_chars(text)
            sys.stdout.write(cleaned_text)
            if flush:
                sys.stdout.flush()

def remove_all_unsupported_chars(text):
    """
    移除所有可能引起编码问题的字符
    返回纯文本
    """
    if not text:
        return text
    
    result = []
    for char in text:
        code_point = ord(char)
        
        # 允许的字符：
        # 1. ASCII (0-127)
        # 2. 基本汉字 (0x4E00-0x9FFF)
        # 3. 常用标点
        # 4. 温度符号
        
        if code_point <= 127:
            # ASCII字符
            result.append(char)
        elif 0x4E00 <= code_point <= 0x9FFF:
            # 基本汉字
            result.append(char)
        elif char in '°℃、。，．：；？！「」『』（）［］｛｝《》':
            # 常用标点
            result.append(char)
        elif char in ' \t\n\r':
            # 空白字符
            result.append(char)
        else:
            # 其他字符，尝试替换
            substitute = get_simple_substitute(char)
            if substitute:
                result.append(substitute)
            # 否则移除
    
    return ''.join(result)

def get_simple_substitute(char):
    """获取简单替代文本"""
    code_point = ord(char)
    
    # 常见符号的文本描述
    if 0x1F300 <= code_point <= 0x1F9FF:
        return '[符号]'
    elif 0x2600 <= code_point <= 0x27BF:
        return '[标记]'
    elif char in '✅✓✔':
        return '[OK]'
    elif char in '❌✗✘':
        return '[错误]'
    elif char in '⚠️⚠':
        return '[警告]'
    elif char in 'ℹ️ℹ':
        return '[信息]'
    elif char in '🔍🔎':
        return '[搜索]'
    elif char == '💡':
        return '[提示]'
    elif char in '📅📆':
        return '[日期]'
    elif char in '📍📌':
        return '[位置]'
    elif char in '🌡️🌡':
        return '[温度]'
    elif char == '💧':
        return '[湿度]'
    elif char in '🌧️🌧':
        return '[降水]'
    elif char in '🌬️🌬':
        return '[风力]'
    elif char in '☀️☀':
        return '[晴]'
    elif char in '🌙🌜🌛':
        return '[夜]'
    elif char in '☁️☁':
        return '[云]'
    elif char == '⛅':
        return '[少云]'
    elif char in '🌤️🌤':
        return '[晴]'
    elif char in '🌥️🌥':
        return '[多云]'
    elif char in '🌦️🌦':
        return '[雨]'
    elif char in '⛈️⛈':
        return '[雷雨]'
    elif char in '🌨️🌨':
        return '[雪]'
    elif char in '❄️❄':
        return '[雪]'
    elif char in '🌂☂️☔':
        return '[伞]'
    elif char == '🌀':
        return '[风]'
    elif char == '🌈':
        return '[彩虹]'
    elif char == '📱':
        return '[手机]'
    elif char == '📝':
        return '[笔记]'
    elif char in '🔧🔨⚙️':
        return '[工具]'
    elif char in '🔗📎':
        return '[链接]'
    elif char in '📊📈📉':
        return '[图表]'
    elif char == '🇨🇳':
        return '[中国]'
    else:
        return ''

def setup_encoding():
    """设置编码环境"""
    encoding = get_system_encoding()
    platform = sys.platform
    
    info = {
        'platform': platform,
        'encoding': encoding,
        'is_windows': is_windows(),
        'python_version': sys.version.split()[0],
    }
    
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    return info

# 测试
if __name__ == "__main__":
    info = setup_encoding()
    safe_print("编码测试")
    safe_print(f"平台: {info['platform']}")
    safe_print(f"编码: {info['encoding']}")
    
    # 测试各种字符
    test_texts = [
        "正常文本",
        "🌤️ 测试表情",
        "✅ 通过 ❌ 失败",
        "📅 日期 📍 位置",
        "🌡️25°C 💧60%",
    ]
    
    for text in test_texts:
        safe_print(f"\n原始: {text}")
        safe_print(f"清理: {remove_all_unsupported_chars(text)}")