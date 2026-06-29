"""
自动上货脚本 V3 — 直接调用 publisher.py，不走子进程
整合沛神优化：日期过滤 + 已发布标记 + 已上架记录去重

用法：
  python auto_publish.py                                 # 本地模式：自动找到最小 day 文件夹
  python auto_publish.py --day day1                       # 指定上架某个 day 文件夹
  python auto_publish.py --day day1 --all                 # 强制重新上架所有（不检查记录）
  python auto_publish.py --dry-run                        # 预览模式（不实际上架）
  python auto_publish.py --feishu                         # 飞书模式：从飞书多维表格读取商品清单
  python auto_publish.py --feishu --dry-run               # 飞书模式预览

由自动化任务每天触发。
"""

import os
import re
import sys
import glob
import shutil
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# 配置
# ============================================================
BASE_DIR = r"待上架目录"
IMAGE_DIR = r"图片资料目录"
DONE_DIR = os.path.join(BASE_DIR, "done")
RECORD_FILE = os.path.join(BASE_DIR, "已上架记录.txt")

# ============================================================
# 飞书配置
# ============================================================
FEISHU_SPREADSHEET_TOKEN = "CBwesfEuwh8i3JtUPBTc0K63nbd"
FEISHU_SHEET_ID = "f74a94"

# ⚙️ 高级功能开关
# ENABLE_DATE_FILTER = True   → 启用日期过滤（只上架当天日期的商品）
# ENABLE_PUBLISHED_MARK = True → 启用已发布标记（上架后写回总上货.txt）
# ENABLE_RECORD_DEDUP = True   → 启用已上架记录去重
ENABLE_DATE_FILTER = True
ENABLE_PUBLISHED_MARK = True
ENABLE_RECORD_DEDUP = True

# 导入发布函数（不走子进程！）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publisher import publish_product


def get_today_date() -> str:
    """获取今天的日期，格式 M.D（如 6.23）"""
    now = datetime.now()
    return f"{now.month}.{now.day}"


def load_record() -> set:
    """加载已上架记录，返回 set of "日期|标题|店铺" """
    records = set()
    if not os.path.exists(RECORD_FILE):
        return records
    with open(RECORD_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                records.add(line)
    print(f"📋 已上架记录: {len(records)} 条")
    return records


def save_record(record: str):
    """追加一条已上架记录"""
    with open(RECORD_FILE, 'a', encoding='utf-8') as f:
        f.write(record + '\n')
    print(f"  📝 已上架记录已保存: {record}")


def mark_published_in_total(total_txt_path: str, config: dict):
    """
    在总上货.txt中标记该商品为已发布。
    根据发布时间行或数字行追加「已发布」标记。
    """
    if not os.path.exists(total_txt_path):
        return

    with open(total_txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = config['title']
    shop_label = '1号店' if config['shop'] == 1 else '2号店'

    # 尝试多种匹配策略
    lines = content.split('\n')
    modified = False

    # 策略1：匹配 "一、发布时间" 行（新版格式）
    # 找到包含商品标题的块
    in_block = False
    block_start = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^一、', stripped):
            block_start = i
            in_block = True
        elif re.match(r'^一、', stripped) and in_block:
            # 遇到下一个商品块，结束当前块
            in_block = False

        if in_block and title in stripped:
            # 在这个块中找到 "一、发布时间" 行
            for j in range(block_start, i + 1):
                if re.match(r'^一、发布时间', lines[j].strip()):
                    if '已发布' not in lines[j]:
                        lines[j] = lines[j].rstrip() + ' 已发布'
                        modified = True
                    break
            break

    # 策略2：匹配 "数字." 行（旧版格式）
    if not modified:
        for i, line in enumerate(lines):
            stripped = line.strip()
            # 匹配 "1.标题" 格式
            m = re.match(r'^(\d+)\.\s*(.+)', stripped)
            if m and m.group(2).strip() == title:
                if '已发布' not in lines[i]:
                    lines[i] = lines[i].rstrip() + ' 已发布'
                    modified = True
                break

    if modified:
        with open(total_txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"  📌 总上货.txt已标记已发布: {title}")
    else:
        print(f"  ⚠️ 无法在总上货.txt中找到匹配行标记已发布: {title}")


def find_next_day_folder() -> str | None:
    """找到待上架中最小的 dayN 文件夹"""
    if not os.path.exists(BASE_DIR):
        print(f"❌ 目录不存在: {BASE_DIR}")
        return None

    day_dirs = []
    for item in os.listdir(BASE_DIR):
        item_path = os.path.join(BASE_DIR, item)
        if os.path.isdir(item_path) and item.startswith("day"):
            m = re.match(r'^day(\d+)$', item)
            if m:
                day_dirs.append((int(m.group(1)), item_path))

    if not day_dirs:
        print("📭 没有待上架的商品")
        return None

    day_dirs.sort(key=lambda x: x[0])
    return day_dirs[0][1]


def find_config_files(day_dir: str) -> list:
    """在day文件夹中找到所有 .txt 配置文件"""
    txt_files = glob.glob(os.path.join(day_dir, "*.txt"))
    txt_files.sort()
    return txt_files


def parse_day_config(filepath: str) -> dict | None:
    """
    解析三段式配置 txt
    格式：
      第1行：店铺号
      空行
      第2段：宝贝描述（多行）
      空行
      第3段：网盘文本（最后一行是提取码）
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.strip().split('\n')
    if len(lines) < 3:
        print(f"❌ 配置文件格式错误: {filepath}")
        return None

    # 第1行：店铺号
    try:
        shop = int(lines[0].strip())
    except ValueError:
        print(f"❌ 无法解析店铺号: {lines[0]}")
        return None

    if shop not in (1, 2):
        print(f"❌ 无效店铺号: {shop}")
        return None

    # 找到空行位置
    desc_start = 1
    while desc_start < len(lines) and lines[desc_start].strip() == '':
        desc_start += 1
    desc_end = desc_start
    while desc_end < len(lines) and lines[desc_end].strip() != '':
        desc_end += 1
    desc = '\n'.join(lines[desc_start:desc_end]).strip()

    # 第3段网盘
    pan_start = desc_end
    while pan_start < len(lines) and lines[pan_start].strip() == '':
        pan_start += 1
    pan_lines = lines[pan_start:]
    pan_code = pan_lines[-1].strip() if pan_lines else ''
    pan_text = '\n'.join(pan_lines).strip()

    # 从文件名提取标题
    basename = os.path.splitext(os.path.basename(filepath))[0]
    title = basename

    # 图片匹配
    image_file, keyword = match_image(title)

    return {
        'shop': shop,
        'title': title,
        'desc': desc,
        'pan_text': pan_text,
        'pan_code': pan_code,
        'image_file': image_file,
        'image_keyword': keyword,
        'image_dir': IMAGE_DIR,
    }


def match_image(title: str) -> tuple:
    """匹配图片"""
    if not os.path.exists(IMAGE_DIR):
        return ('', title)

    images = {}
    for f in os.listdir(IMAGE_DIR):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            name_no_ext = os.path.splitext(f)[0].lower()
            images[name_no_ext] = f

    title_lower = title.lower()

    for name_no_ext, img_file in images.items():
        if name_no_ext in title_lower or title_lower in name_no_ext:
            print(f"  🖼️ 匹配图片: {img_file}")
            return (img_file, name_no_ext)

    chinese_match = re.search(r'[\u4e00-\u9fff]{2,}', title)
    if chinese_match:
        keyword = chinese_match.group(0)
        for name_no_ext, img_file in images.items():
            if keyword.lower() in name_no_ext or name_no_ext in keyword.lower():
                print(f"  🖼️ 匹配图片: {img_file} (关键词: {keyword})")
                return (img_file, keyword)

    eng_match = re.search(r'[a-zA-Z]{3,}', title)
    if eng_match:
        keyword = eng_match.group(0).lower()
        for name_no_ext, img_file in images.items():
            if keyword in name_no_ext:
                print(f"  🖼️ 匹配图片: {img_file} (关键词: {keyword})")
                return (img_file, keyword)

    print(f"  ⚠️ 未找到匹配图片: {title}")
    return ('', title)


def move_to_done(day_dir: str):
    """将day文件夹移到done/"""
    os.makedirs(DONE_DIR, exist_ok=True)
    dirname = os.path.basename(day_dir)
    dest = os.path.join(DONE_DIR, dirname)
    if os.path.exists(dest):
        dest = os.path.join(DONE_DIR, f"{dirname}_{int(time.time())}")
    shutil.move(day_dir, dest)
    print(f"📁 已移至: {dest}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='自动上货脚本V3')
    parser.add_argument('--day', type=str, help='指定要上架的day文件夹（如day1），不指定则自动找最小的')
    parser.add_argument('--all', action='store_true', help='强制重新上架指定day中所有商品')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际上架')
    parser.add_argument('--feishu', action='store_true', help='从飞书多维表格读取商品清单')
    args = parser.parse_args()

    print("=" * 50)
    print("🤖 自动上货脚本 V3")
    print("=" * 50)

    today = get_today_date()
    print(f"📅 当前日期: {today}")

    if args.feishu:
        # ========== 飞书模式 ==========
        print("📡 飞书模式")
        run_feishu_mode(today, args.dry_run)
    else:
        # ========== 本地文件模式 ==========
        run_local_mode(today, args)


def run_feishu_mode(today: str, dry_run: bool = False):
    """从飞书多维表格读取商品清单，逐个上架"""
    from feishu_reader import FeishuReader

    reader = FeishuReader(spreadsheet_token=FEISHU_SPREADSHEET_TOKEN)

    # 健康检查
    if not reader.health_check():
        print("❌ 飞书 CLI 不可用，请先配置")
        return

    # 读取当天待上架商品
    products = reader.get_today_products(today)
    if not products:
        print("📭 今天没有待上架的商品")
        return

    print(f"📄 共 {len(products)} 个商品待处理:")
    for p in products:
        print(f"  - [{p['row_index']}] {p['title'][:40]} | 店铺{p['shop']}")

    success_count = 0
    total = len(products)

    for idx, product in enumerate(products, 1):
        print(f"\n{'='*50}")
        print(f"📦 [{idx}/{total}] 开始上架: {product['title']}")
        print(f"{'='*50}")

        # 构建 config
        config = {
            'shop': product['shop'],
            'title': product['title'],
            'desc': product['desc'],
            'pan_text': product['pan_text'],
            'pan_code': product['pan_code'],
            'image_file': product['image_file'],
            'image_keyword': product['image_file'].rsplit('.', 1)[0] if product['image_file'] else product['title'],
            'image_dir': IMAGE_DIR,
        }

        print(f"  商品: {config['title']}")
        print(f"  店铺: {'1号店' if config['shop']==1 else '2号店'}")
        print(f"  图片: {config['image_file'] or '无'}")
        print(f"  提取码: {config['pan_code']}")

        # 检查本地图片是否存在
        if config['image_file']:
            img_path = os.path.join(IMAGE_DIR, config['image_file'])
            if os.path.exists(img_path):
                print(f"  🖼️ 本地图片存在: {img_path}")
            else:
                print(f"  ⚠️ 本地图片不存在: {img_path}（将从图库搜索）")

        if dry_run:
            print(f"  🔍 [DRY-RUN] 跳过实际上架")
            success_count += 1
            continue

        # 调用发布函数
        success = publish_product(config)

        if success:
            success_count += 1
            print(f"✅ [{idx}/{total}] {config['title']} 上架成功！")

            # 飞书回写状态
            reader.mark_done(config['title'], config['shop'])
        else:
            print(f"⚠️ [{idx}/{total}] {config['title']} 上架失败，请检查")

        if idx < total:
            print(f"⏳ 等待3秒后继续下一个...")
            time.sleep(3)

    print(f"\n{'='*50}")
    print(f"📊 汇总")
    print(f"{'='*50}")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ❌ 失败: {total - success_count}")


def run_local_mode(today: str, args):
    """本地文件模式（原有的逻辑）"""
    # 加载已上架记录
    records = set()
    if ENABLE_RECORD_DEDUP and not args.all:
        records = load_record()

    # 1. 确定目标 day 文件夹
    if args.day:
        day_dir = os.path.join(BASE_DIR, args.day)
        if not os.path.isdir(day_dir):
            print(f"❌ 文件夹不存在: {day_dir}")
            return
        print(f"📂 指定上架: {day_dir}")
    else:
        day_dir = find_next_day_folder()
        if not day_dir:
            print("📭 没有待上架的商品，任务结束")
            return
        print(f"📂 找到待上架: {day_dir}")

    # 2. 找到所有配置文件
    config_files = find_config_files(day_dir)
    if not config_files:
        print(f"⚠️ {day_dir} 中没有 .txt 配置文件")
        return

    print(f"📄 共 {len(config_files)} 个商品待处理: {[os.path.basename(f) for f in config_files]}")

    # 3. 逐个上架
    success_count = 0
    skip_count = 0
    total = len(config_files)

    for idx, config_file in enumerate(config_files, 1):
        basename = os.path.basename(config_file)

        config = parse_day_config(config_file)
        if not config:
            print(f"❌ 解析失败，跳过: {config_file}")
            continue

        # 日期过滤：只上架当天的商品
        if ENABLE_DATE_FILTER and hasattr(config, 'get') and config.get('publish_date'):
            if config['publish_date'] != today:
                print(f"  ⏭️ [SKIP] {basename} - 发布日期 {config['publish_date']} ≠ 今天 {today}")
                skip_count += 1
                continue

        # 已上架记录去重
        if ENABLE_RECORD_DEDUP and not args.all:
            record_key = f"{today}|{config['title']}|{config['shop']}"
            if record_key in records:
                print(f"  ⏭️ [SKIP] {basename} - 已上架记录存在，跳过")
                skip_count += 1
                continue

        print(f"\n{'='*50}")
        print(f"📦 [{idx}/{total}] 开始上架: {basename}")
        print(f"{'='*50}")

        print(f"  商品: {config['title']}")
        print(f"  店铺: {'1号店' if config['shop']==1 else '2号店'}")
        print(f"  图片: {config['image_file'] or '无'}")
        print(f"  提取码: {config['pan_code']}")

        # dry-run 模式
        if args.dry_run:
            print(f"  🔍 [DRY-RUN] 跳过实际上架")
            success_count += 1
            continue

        # 直接调用发布函数
        success = publish_product(config)

        if success:
            success_count += 1
            print(f"✅ [{idx}/{total}] {config['title']} 上架成功！")

            # 已发布标记（写回总上货.txt）
            if ENABLE_PUBLISHED_MARK:
                mark_published_in_total(r"待上架目录\总上货.txt", config)

            # 已上架记录
            if ENABLE_RECORD_DEDUP:
                record_key = f"{today}|{config['title']}|{config['shop']}"
                save_record(record_key)
        else:
            print(f"⚠️ [{idx}/{total}] {config['title']} 上架失败，请检查")

        # 商品之间间隔3秒
        if idx < total:
            print(f"⏳ 等待3秒后继续下一个...")
            time.sleep(3)

    # 4. 汇总
    print(f"\n{'='*50}")
    print(f"📊 汇总")
    print(f"{'='*50}")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ⏭️ 跳过: {skip_count}")
    print(f"  ❌ 失败: {total - success_count - skip_count}")

    # 5. 如果全部成功，移到 done/
    if success_count + skip_count == total and total > 0:
        move_to_done(day_dir)
        print(f"\n🎉 全部 {total} 个商品处理完成！")
    elif success_count > 0:
        print(f"\n⚠️ 部分商品成功，不移动文件夹，请手动检查")
    else:
        print(f"\n📭 没有商品需要上架")


if __name__ == '__main__':
    main()
