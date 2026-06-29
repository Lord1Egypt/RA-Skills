"""
商品配置文件解析器

将简化格式的三段式文本块，解析为 full_flow.py 所需的7个配置变量。

=== 输入格式 ===
第1行：店铺号（1 或 2）
空行
第2段：宝贝描述（多行，从第二行开始写，不要重复标题，不含网盘链接）
空行
第3段：网盘分享文本（多行，最后一行是提取码）

=== 使用方式 ===
方式1：直接运行本脚本 + 商品配置文本文件路径
    python product_parser.py "D:/Desktop_Archive/闲鱼资源/商品配置/落叶楼.txt"

方式2：在本脚本底部直接修改 PRODUCT_CONFIG 变量，然后运行
    python product_parser.py

方式3：作为模块导入，调用 parse_config(text) 函数
"""

import os
import sys


def parse_config(text: str) -> dict:
    """
    解析三段式商品配置文本，返回字典：
    {
        'SHOP': int,
        'TITLE': str,        # 自动从文件名推断，调用者需传入
        'DESC': str,
        'IMAGE_FILE': str,   # 自动从文件名推断
        'IMAGE_KEYWORD': str,
        'PAN_TEXT': str,
        'PAN_CODE': str,
    }
    """
    # 按空行分割成段落
    lines = text.strip().split('\n')

    # 第1行：店铺号
    SHOP = int(lines[0].strip())

    # 去除行尾回车符
    clean_lines = [l.rstrip('\r') for l in lines]

    # 找到所有非空行的索引（跳过第1行）
    content_indices = []
    for i, line in enumerate(clean_lines):
        if i == 0:
            continue
        if line.strip() != '':
            content_indices.append(i)

    # 第2段：第1行后第一个非空行开始，到空行前结束
    # 先找到第1行后第一个非空行
    desc_start = 1
    while desc_start < len(clean_lines) and clean_lines[desc_start].strip() == '':
        desc_start += 1
    # 从desc_start开始找下一个空行作为结束
    desc_end = desc_start
    while desc_end < len(clean_lines) and clean_lines[desc_end].strip() != '':
        desc_end += 1
    DESC = '\n'.join(clean_lines[desc_start:desc_end]).strip()

    # 第3段：从desc_end之后第一个非空行到末尾
    pan_start = desc_end
    while pan_start < len(clean_lines) and clean_lines[pan_start].strip() == '':
        pan_start += 1
    pan_lines = clean_lines[pan_start:]
    # 最后一行是提取码
    PAN_CODE = pan_lines[-1].strip()
    PAN_TEXT = '\n'.join(pan_lines).strip()

    return {
        'SHOP': SHOP,
        'DESC': DESC,
        'PAN_TEXT': PAN_TEXT,
        'PAN_CODE': PAN_CODE,
    }


def generate_full_flow_config(parsed: dict, filename_without_ext: str) -> str:
    """
    将解析结果和文件名组合成 full_flow.py 的商品配置区代码片段
    """
    title = filename_without_ext
    image_file = f"{filename_without_ext}.jpg"
    keyword = filename_without_ext

    shop = parsed['SHOP']
    desc = parsed['DESC']
    pan_text = parsed['PAN_TEXT']
    pan_code = parsed['PAN_CODE']

    # 格式化 DESC 为多行字符串
    desc_lines = desc.split('\n')
    if len(desc_lines) == 1:
        desc_str = f'"{desc}"'
    else:
        desc_lines_fmt = []
        for i, line in enumerate(desc_lines):
            if i == 0:
                desc_lines_fmt.append(f'("{line}\\n')
            elif i == len(desc_lines) - 1:
                desc_lines_fmt.append(f'        "{line}")')
            else:
                desc_lines_fmt.append(f'        "{line}\\n')
        desc_str = '\n'.join(desc_lines_fmt)

    # 格式化 PAN_TEXT 为多行字符串
    pan_lines = pan_text.split('\n')
    if len(pan_lines) == 1:
        pan_str = f'"{pan_text}"'
    else:
        pan_lines_fmt = []
        for i, line in enumerate(pan_lines):
            if i == 0:
                pan_lines_fmt.append(f'("{line}\\n')
            elif i == len(pan_lines) - 1:
                pan_lines_fmt.append(f'            "{line}")')
            else:
                pan_lines_fmt.append(f'            "{line}\\n')
        pan_str = '\n'.join(pan_lines_fmt)

    return f"""# ⭐ 商品配置 — {title}
SHOP = {shop}

TITLE = "{title}"

DESC = {desc_str}

IMAGE_FILE = "{image_file}"
IMAGE_KEYWORD = "{keyword}"

PAN_TEXT = {pan_str}
PAN_CODE = "{pan_code}"
"""


def main():
    # 默认演示配置（你可以改成自己的）
    DEMO_CONFIG = """2

拥有海量小说资源，所有内容全免费，一键即可开启阅读。平台提供多种类型的图文资源，支持离线缓存和听书功能。
自动发货 24h内发货
百度网盘发货
虚拟商品拍下不退不换

通过网盘分享的文件：落叶楼阅读_1.0.2(102)-纯净版.apk等2个文件
链接: https://pan.baidu.com/s/106bJAysM4341QtGwR6a9Ew 提取码: thav
thav"""

    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"❌ 文件不存在: {filepath}")
            sys.exit(1)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        basename = os.path.splitext(os.path.basename(filepath))[0]
    else:
        text = DEMO_CONFIG
        basename = "落叶楼阅读纯净版"

    print("=" * 50)
    print("📄 原始配置文本：")
    print("-" * 50)
    print(text)
    print("-" * 50)

    parsed = parse_config(text)

    print("\n🔍 解析结果：")
    print(f"  SHOP       = {parsed['SHOP']} ({'1号店-一号店铺名' if parsed['SHOP']==1 else '2号店-二号店铺名'})")
    print(f"  TITLE      = {basename}")
    print(f"  IMAGE_FILE = {basename}.jpg")
    print(f"  IMAGE_KEY  = {basename}")
    print(f"  DESC       = {repr(parsed['DESC'][:60])}...")
    print(f"  PAN_TEXT   = {repr(parsed['PAN_TEXT'][:60])}...")
    print(f"  PAN_CODE   = {parsed['PAN_CODE']}")

    print("\n" + "=" * 50)
    print("📝 生成 full_flow.py 配置代码：")
    print("=" * 50)
    config_code = generate_full_flow_config(parsed, basename)
    print(config_code)


if __name__ == '__main__':
    main()
