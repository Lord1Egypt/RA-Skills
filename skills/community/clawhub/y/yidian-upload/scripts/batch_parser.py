"""
批量商品解析器 + 按天拆分工具 v3.3
（整合沛神优化：日期过滤、店铺识别、已发布标记）

支持两种格式：
  格式A（旧）：数字. 开头，首行标识店铺
  格式B（新）：一、发布时间 / 二、商品文案 / 三、店铺 / 四、网盘发货文案

用法：
  python batch_parser.py                     # 解析并预览拆分结果
  python batch_parser.py --apply             # 解析并实际拆分到 day1/day2/... 目录
  python batch_parser.py --apply --by-date   # 按日期拆分（每个日期的商品放一起）

总上货.txt 格式B示例：
  一、发布时间：6.23
  二、商品文案：
  商品标题
  商品描述内容...
  温馨提示：自动发货...
  三、店铺：2号店（二号店铺名）
  四、网盘发货文案：
  通过网盘分享的文件：xxx
  链接: https://pan.baidu.com/s/xxx 提取码: xxxx

输出：
  待上架目录\
    ├── day1\ 商品名.txt
    ├── day2\ 商品名.txt
    ├── ...
    └── done\        ← 已上架的会移到这里
"""

import os
import re
import sys
import shutil

# ============================================================
# 配置
# ============================================================
TOTAL_TXT = r"待上架目录\总上货.txt"
OUTPUT_DIR = r"待上架目录"
IMAGE_DIR = r"图片资料目录"

# ============================================================
# 店铺映射表
# ============================================================
SHOP_MAP = {
    "一号店铺名": 1,
    "1号店": 1,
    "天空的流星": 1,
    "二号店铺名": 2,
    "2号店": 2,
    "林酱": 2,
    "xy020109151403": 2,
}

# ============================================================
# 解析逻辑
# ============================================================

def detect_format(content: str) -> str:
    """检测总上货.txt的格式：'old'（数字.） 或 'new'（一、发布时间）"""
    # 只看前50行
    lines = content.split('\n')[:50]
    for line in lines:
        stripped = line.strip()
        if re.match(r'^[一二三四五]、', stripped):
            return 'new'
    return 'old'


def parse_total_txt(filepath: str) -> list:
    """
    解析总上货.txt，返回商品列表：
    [
        {
            'shop': 1 or 2,
            'title': str,
            'desc': str,
            'pan_text': str,
            'pan_code': str,
            'image_file': str,
            'image_keyword': str,
            'index': int,
            'publish_date': str or None,  # 格式 "M.D" 如 "6.23"
        },
        ...
    ]
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fmt = detect_format(content)
    print(f"📋 检测到格式: {'新版（一/二/三/四）' if fmt == 'new' else '旧版（数字.）'}")

    if fmt == 'new':
        return _parse_new_format(content)
    else:
        return _parse_old_format(content)


def _resolve_shop(shop_text: str, default_shop: int = 2) -> int:
    """根据店铺文本解析店铺号"""
    if not shop_text:
        return default_shop
    for keyword, shop_id in SHOP_MAP.items():
        if keyword in shop_text:
            return shop_id
    return default_shop


def _parse_new_format(content: str) -> list:
    """
    解析新版格式（一、发布时间 / 二、商品文案 / 三、店铺 / 四、网盘发货文案）
    支持「已发布」标记跳过
    """
    lines = content.split('\n')

    # ---- 第1步：按「一、」分割商品块 ----
    block_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^一、', stripped):
            block_starts.append(i)

    if not block_starts:
        print("❌ 未找到商品分隔符（一、），请检查格式")
        return []

    print(f"📦 共发现 {len(block_starts)} 个商品块")

    # ---- 第2步：解析每个商品块 ----
    products = []
    for idx, start in enumerate(block_starts):
        # 确定结束行
        if idx + 1 < len(block_starts):
            end = block_starts[idx + 1]
        else:
            end = len(lines)

        block_text = '\n'.join(lines[start:end]).strip()

        # ---- 检查是否已发布 ----
        if '已发布' in block_text:
            # 提取标题用于显示
            title_match = re.search(r'二、商品文案[：:]\s*\n\s*(.+)', block_text)
            title_hint = title_match.group(1).strip() if title_match else "未知"
            print(f"  ⏭️ [SKIP] 商品{idx+1}({title_hint}) 已标记为已发布，跳过")
            continue

        # ---- 提取发布时间 ----
        publish_date = None
        date_match = re.search(r'一、发布时间[：:]\s*(\d+\.\d+)', block_text)
        if date_match:
            publish_date = date_match.group(1).strip()

        # ---- 提取标题 ----
        title = ""
        # 二、商品文案：后的第一行非空行作为标题
        desc_match = re.search(r'二、商品文案[：:]\s*\n([\s\S]*?)(?=\n三、|$)', block_text)
        if desc_match:
            desc_text = desc_match.group(1).strip()
            desc_lines = [l.strip() for l in desc_text.split('\n') if l.strip()]
            if desc_lines:
                title = desc_lines[0]  # 第一行是标题
                # 剩余是描述
                desc = '\n'.join(desc_lines[1:]).strip()
            else:
                title = f"商品{idx+1}"
                desc = ""
        else:
            title = f"商品{idx+1}"
            desc = ""

        # ---- 提取店铺 ----
        shop_text = ""
        shop_match = re.search(r'三、店铺[：:]\s*(.+)', block_text)
        if shop_match:
            shop_text = shop_match.group(1).strip()

        shop = _resolve_shop(shop_text)

        # ---- 提取网盘信息 ----
        pan_text = ""
        pan_code = ""
        pan_match = re.search(r'四、网盘发货文案[：:]\s*\n([\s\S]*)', block_text)
        if pan_match:
            pan_text = pan_match.group(1).strip()
            # 提取码
            code_match = re.search(r'提取码[：:]\s*(\S+)', pan_text)
            if code_match:
                pan_code = code_match.group(1).strip()
            # 也检查 pwd= 格式
            if not pan_code:
                pwd_match = re.search(r'pwd[=：]\s*(\S+)', pan_text)
                if pwd_match:
                    pan_code = pwd_match.group(1).strip()
        else:
            print(f"  ⚠️ 商品{idx+1}({title}) 未找到网盘发货文案段")
            # 不完全跳过，尝试在块末尾找网盘链接
            link_match = re.search(r'(https?://[^\s]+)', block_text)
            if link_match:
                pan_text = block_text
                code_match = re.search(r'提取码[：:]\s*(\S+)', block_text)
                if code_match:
                    pan_code = code_match.group(1).strip()

        # ---- 图片匹配 ----
        image_file, keyword = _match_image(title, shop)

        result = {
            'shop': shop,
            'title': title,
            'desc': desc,
            'pan_text': pan_text,
            'pan_code': pan_code,
            'image_file': image_file,
            'image_keyword': keyword,
            'index': idx + 1,
            'publish_date': publish_date,
        }
        products.append(result)

    return products


def _parse_old_format(content: str) -> list:
    """
    解析旧版格式（数字. 开头，首行标识店铺）
    """
    lines = content.split('\n')

    # ---- 第1步：识别默认店铺 ----
    default_shop = 2
    first_line = lines[0].strip() if lines else ''
    if '2号店' in first_line or '林酱' in first_line:
        default_shop = 2
    elif '1号店' in first_line or '天空的流星' in first_line:
        default_shop = 1
    else:
        print(f"⚠️ 无法从首行识别店铺: {first_line}")
        print("   默认使用 2号店（二号店铺名）")
        default_shop = 2

    print(f"🏪 默认店铺: {'1号店-一号店铺名' if default_shop == 1 else '2号店-二号店铺名'}")

    # ---- 第2步：按"数字."分割商品块 ----
    block_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = re.match(r'^(\d{1,2})\.\s*(.*)', stripped)
        if not m:
            continue
        num = int(m.group(1))
        if num < 1 or num > 50:
            continue
        is_separator = False
        if i == 0:
            is_separator = True
        elif i > 0:
            prev_line = lines[i - 1].strip()
            if prev_line == '' or '以下为' in prev_line:
                is_separator = True
        if is_separator:
            block_starts.append(i)

    if not block_starts:
        print("❌ 未找到商品分隔符（数字.），请检查格式")
        return []

    print(f"📦 共发现 {len(block_starts)} 个商品")

    # ---- 第3步：提取每个商品块 ----
    products = []
    for idx, start in enumerate(block_starts):
        if idx + 1 < len(block_starts):
            end = block_starts[idx + 1]
        else:
            end = len(lines)

        block_lines = lines[start:end]
        product = _parse_old_product_block(block_lines, default_shop, idx + 1)
        if product:
            products.append(product)

    return products


def _parse_old_product_block(block_lines: list, shop: int, index: int) -> dict:
    """解析旧版单个商品块"""
    non_empty = [l.rstrip('\r') for l in block_lines if l.strip() != '']

    if not non_empty:
        return None

    # ---- 标题 ----
    title_line = non_empty[0].strip()
    if re.match(r'^\d+\.?\s*$', title_line):
        if len(non_empty) > 1:
            title_line = non_empty[1].strip()
            desc_start = 2
        else:
            title = f"商品{index}"
            desc_start = 1
    else:
        title_line = re.sub(r'^\d+\.\s*', '', title_line).strip()
        desc_start = 1

    title = title_line
    if not title:
        title = f"商品{index}"

    # ---- 找到"通过网盘分享的文件"行 ----
    pan_start = None
    for i, line in enumerate(non_empty):
        if '通过网盘分享的文件' in line:
            pan_start = i
            break

    if pan_start is None:
        print(f"⚠️ 商品{index}({title}) 未找到网盘链接段，跳过")
        return None

    desc_lines = non_empty[desc_start:pan_start]
    desc = '\n'.join(desc_lines).strip()

    pan_lines = non_empty[pan_start:]
    pan_text = '\n'.join(pan_lines).strip()

    pan_code = ''
    for line in pan_lines:
        m = re.search(r'提取码:\s*(\S+)', line)
        if m:
            pan_code = m.group(1).strip()
            break
    if not pan_code and pan_lines:
        pan_code = pan_lines[-1].strip()

    image_file, keyword = _match_image(title, shop)

    result = {
        'shop': shop,
        'title': title,
        'desc': desc,
        'pan_text': pan_text,
        'pan_code': pan_code,
        'image_file': image_file,
        'image_keyword': keyword,
        'index': index,
        'publish_date': None,
    }

    return result


def _match_image(title: str, shop: int = None) -> tuple:
    """
    用标题关键词匹配图片资料目录中的图片。
    如果 shop 指定且启用多店铺图片目录，则按店铺分目录查找。
    返回 (image_file, keyword)
    """
    if not os.path.exists(IMAGE_DIR):
        return ('', title)

    # 获取所有图片文件
    images = {}
    for f in os.listdir(IMAGE_DIR):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            name_no_ext = os.path.splitext(f)[0].lower()
            images[name_no_ext] = f

    title_lower = title.lower()

    # 策略1：标题直接包含图片名
    for name_no_ext, img_file in images.items():
        if name_no_ext in title_lower or title_lower in name_no_ext:
            print(f"  🖼️ 匹配图片: {img_file} (关键词: {name_no_ext})")
            return (img_file, name_no_ext)

    # 策略2：中文词匹配
    chinese_match = re.search(r'[\u4e00-\u9fff]{2,}', title)
    if chinese_match:
        keyword = chinese_match.group(0)
        for name_no_ext, img_file in images.items():
            if keyword.lower() in name_no_ext or name_no_ext in keyword.lower():
                print(f"  🖼️ 匹配图片: {img_file} (关键词: {keyword})")
                return (img_file, keyword)

    # 策略3：英文词匹配
    eng_match = re.search(r'[a-zA-Z]{3,}', title)
    if eng_match:
        keyword = eng_match.group(0).lower()
        for name_no_ext, img_file in images.items():
            if keyword in name_no_ext:
                print(f"  🖼️ 匹配图片: {img_file} (关键词: {keyword})")
                return (img_file, keyword)

    print(f"  ⚠️ 未找到匹配图片，标题: {title}")
    return ('', title)


def format_product_txt(product: dict) -> str:
    """将商品信息格式化为三段式txt内容"""
    shop = product['shop']
    desc = product['desc']
    pan_text = product['pan_text']
    pan_code = product['pan_code']

    return f"""{shop}

{desc}

{pan_text}
{pan_code}"""


def print_product_summary(product: dict):
    """打印商品摘要"""
    shop_label = '1号店' if product['shop'] == 1 else '2号店'
    date_info = f" 📅 {product.get('publish_date', '未指定')}" if product.get('publish_date') else ""

    print(f"\n{'='*50}")
    print(f"📦 商品{product['index']}: {product['title']}{date_info}")
    print(f"{'='*50}")
    print(f"🏪 店铺: {shop_label}")
    print(f"📝 描述预览: {product['desc'][:80]}...")
    print(f"🖼️ 图片: {product['image_file'] or '未匹配'}")
    print(f"🔑 关键词: {product['image_keyword']}")
    print(f"🔗 网盘: {product['pan_text'][:80]}...")
    print(f"🔐 提取码: {product['pan_code']}")


def save_to_day_folders(products: list, base_dir: str, apply: bool = False, by_date: bool = False):
    """
    按天拆分到 day1/day2/... 目录

    by_date=True 时：按日期分组，同一日期的放一起
    by_date=False 时：每个商品单独一个day文件夹（默认行为）
    """
    if not apply:
        print("\n\n📋 预览模式（加 --apply 才会实际写入文件）")
        print(f"   将拆分到: {base_dir}\\day1\\, day2\\, ...")
        for p in products:
            date_info = f" [{p.get('publish_date', '?')}]" if p.get('publish_date') else ""
            print(f"   day{p['index']} → {p['title']}{date_info}")
        return

    if by_date and any(p.get('publish_date') for p in products):
        # 按日期分组
        from collections import defaultdict
        date_groups = defaultdict(list)
        for p in products:
            date_key = p.get('publish_date', 'unknown')
            date_groups[date_key].append(p)

        day_num = 1
        for date_key in sorted(date_groups.keys()):
            day_dir = os.path.join(base_dir, f"day{day_num}")
            os.makedirs(day_dir, exist_ok=True)
            for p in date_groups[date_key]:
                txt_content = format_product_txt(p)
                txt_path = os.path.join(day_dir, f"{p['title']}.txt")
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(txt_content)
                print(f"  ✅ day{day_num}/{p['title']}.txt")
            day_num += 1
    else:
        # 每个商品单独一个day文件夹（向后兼容）
        for p in products:
            day_dir = os.path.join(base_dir, f"day{p['index']}")
            os.makedirs(day_dir, exist_ok=True)

            txt_content = format_product_txt(p)
            txt_path = os.path.join(day_dir, f"{p['title']}.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(txt_content)

            print(f"  ✅ day{p['index']}/{p['title']}.txt")

    print(f"\n✅ 全部拆分完成！共 {len(products)} 个商品")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='批量商品解析器 v3.3')
    parser.add_argument('--apply', action='store_true', help='实际拆分到day目录（不加则仅预览）')
    parser.add_argument('--by-date', action='store_true', help='按发布日期分组（新版格式专用）')
    args = parser.parse_args()

    print("=" * 50)
    print("📄 批量商品解析器 v3.3")
    print("=" * 50)

    if not os.path.exists(TOTAL_TXT):
        print(f"❌ 总上货.txt 不存在: {TOTAL_TXT}")
        sys.exit(1)

    products = parse_total_txt(TOTAL_TXT)

    if not products:
        print("\n❌ 未解析到任何商品")
        sys.exit(1)

    # 打印统计
    total = len(products)
    shop1_count = sum(1 for p in products if p['shop'] == 1)
    shop2_count = total - shop1_count
    print(f"\n📊 统计: 共{total}个商品 (1号店: {shop1_count}, 2号店: {shop2_count})")

    # 打印每个商品的摘要
    for p in products:
        print_product_summary(p)

    # 保存到day文件夹
    save_to_day_folders(products, OUTPUT_DIR, apply=args.apply, by_date=args.by_date)


if __name__ == '__main__':
    main()
