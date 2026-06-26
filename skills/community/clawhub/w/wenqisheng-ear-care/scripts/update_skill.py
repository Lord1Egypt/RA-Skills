#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闻其声耳轻松可视采耳 Skill · 便携式更新工具
==============================================
用法：
  1. 直接运行本脚本，按提示修改门店信息
  2. 或使用命令行参数快速更新

快速更新示例：
  python update_skill.py --hours "09:00-21:00" --phone "138xxxxxx"
  python update_skill.py --price 58 68          # 修改项目价格
  python update_skill.py --add-faq "Q:xxx|A:xxx"  # 新增FAQ

所有修改即时生效，只改 references/ 目录，不动 SKILL.md 逻辑层。
修改后 commit & push 即可让客户自动同步。
"""

import os, sys, json, re, shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(SKILL_DIR, 'references')
VERSION_PATH = os.path.join(SKILL_DIR, 'version.json')

def bump_data_version():
    """每次修改数据时更新 version.json 中的 data_version"""
    today = datetime.now().strftime('%Y-%m-%d')
    if os.path.exists(VERSION_PATH):
        with open(VERSION_PATH, encoding='utf-8') as f:
            ver = json.load(f)
        ver['data_version'] = today
        with open(VERSION_PATH, 'w', encoding='utf-8') as f:
            json.dump(ver, f, ensure_ascii=False, indent=2)

def read_md(filename):
    path = os.path.join(REF_DIR, filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

def write_md(filename, content):
    path = os.path.join(REF_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    bump_data_version()
    print(f'  [UPDATED] {filename}')

def update_hours(new_hours_weekday, new_hours_weekend):
    """更新营业时间"""
    content = read_md('business-info.md')
    content = re.sub(r'\| 周一至周五 \| .+ \|', f'| 周一至周五 | {new_hours_weekday} |', content)
    content = re.sub(r'\| 周六日及节假日 \| .+ \|', f'| 周六日及节假日 | {new_hours_weekend} |', content)
    write_md('business-info.md', content)
    print(f'  ✔ 营业时间已更新')

def update_address(new_address, new_nav_keyword=None):
    """更新地址"""
    content = read_md('business-info.md')
    # 按结构定位：## 门店地址 之后的下一行非标题、非表格行
    lines = content.split('\n')
    found_section = False
    for i, line in enumerate(lines):
        if line.strip().startswith('## 门店地址'):
            found_section = True
            continue
        if found_section and line.strip() and not line.startswith('#') and not line.startswith('|'):
            lines[i] = new_address
            break
    content = '\n'.join(lines)
    if new_nav_keyword:
        content = re.sub(r'(高德地图/百度地图搜索关键词：\*\*).+?(\*\*)', f'\\1{new_nav_keyword}\\2', content)
    write_md('business-info.md', content)
    print(f'  ✔ 地址已更新')

def update_phone(new_phone):
    """更新电话"""
    content = read_md('business-info.md')
    # 更新括号中的座机号
    content = re.sub(r'\(0791\) \d+', f'(0791) {new_phone}', content)
    # 更新手机号（11位）
    content = re.sub(r'\d{11}', new_phone, content)
    write_md('business-info.md', content)
    print(f'  ✔ 电话已更新')

def update_wifi(name, password):
    """更新Wi-Fi"""
    content = read_md('business-info.md')
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'Wi-Fi 名称' in line and name:
            lines[i] = f'| Wi-Fi 名称 | {name} |'
        elif 'Wi-Fi 密码' in line and password:
            lines[i] = f'| Wi-Fi 密码 | {password} |'
    write_md('business-info.md', '\n'.join(lines))
    print(f'  ✔ Wi-Fi已更新')

def update_price(project_index, new_price):
    """更新指定项目价格 (1=深度可视采耳, 2=采耳洗耳, 3=炎症养护, 4=眼护)"""
    if not 1 <= project_index <= 4:
        print(f'  ⚠ 项目编号无效，请输入1-4')
        return
    content = read_md('services.md')
    projects = content.split('### ')
    idx = project_index
    found = 0
    for i, section in enumerate(projects):
        if section.startswith(f'{idx}. '):
            projects[i] = re.sub(r'\|\s*\d+\s*元\s*\|', f'| {new_price} 元 |', projects[i])
            found += 1
    if found:
        write_md('services.md', '### '.join(projects))
        print(f'  ✔ 项目{project_index}价格已更新为{new_price}元')

def add_faq(question, answer):
    """新增FAQ"""
    content = read_md('faq.md')
    q_nums = re.findall(r'### Q(\d+):', content)
    next_num = max(int(n) for n in q_nums) + 1
    new_faq = f'\n### Q{next_num}: {question}\n{answer}\n'
    content = content.replace('---\n\n## 禁忌与安全须知', f'{new_faq}\n---\n\n## 禁忌与安全须知')
    write_md('faq.md', content)
    print(f'  ✔ 已新增 FAQ Q{next_num}')

def update_promotion(min_charge, gift, deadline, conditions='无限制'):
    """更新或新增充值优惠"""
    content = read_md('promotions.md')
    lines = content.split('\n')
    new_lines = []
    inserted = False
    for line in lines:
        if line.startswith('| 充 ') and f'充 {min_charge} ' in line:
            new_lines.append(f'| 充 {min_charge} 元（送{gift}） | 送 {gift} 元 | {deadline} | {conditions} |')
            inserted = True
        else:
            new_lines.append(line)
    if not inserted:
        for i, line in enumerate(new_lines):
            if line.startswith('| 充值金额'):
                new_lines.insert(i+3, f'| 充 {min_charge} 元（送{gift}） | 送 {gift} 元 | {deadline} | {conditions} |')
                break
    write_md('promotions.md', '\n'.join(new_lines))
    print(f'  ✔ 充值优惠已更新: 充{min_charge}送{gift}')

def backup():
    """创建数据备份"""
    backup_dir = os.path.join(SKILL_DIR, 'backups', datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.makedirs(backup_dir, exist_ok=True)
    for f in os.listdir(REF_DIR):
        shutil.copy2(os.path.join(REF_DIR, f), os.path.join(backup_dir, f))
    # 同时备份 version.json
    if os.path.exists(VERSION_PATH):
        shutil.copy2(VERSION_PATH, os.path.join(backup_dir, 'version.json'))
    print(f'  ✔ 备份已创建: {backup_dir}')

def show_status():
    """显示当前所有数据摘要"""
    print('\n=== 当前门店数据摘要 ===')
    try:
        biz = read_md('business-info.md')
        for line in biz.split('\n'):
            if '|' in line and not line.startswith('|---') and not line.startswith('#'):
                print(f'  {line.strip()}')
    except Exception:
        pass
    try:
        svc = read_md('services.md')
        for section in svc.split('### '):
            if section.strip() and not section.startswith('#'):
                lines = section.split('\n')
                name = lines[0].strip() if lines else ''
                for l in lines:
                    if '| 价格' in l:
                        parts = [p.strip() for p in l.split('|') if p.strip()]
                        if len(parts) >= 2:
                            print(f'  {name}: {parts[1]}')
    except Exception:
        pass
    try:
        with open(VERSION_PATH, encoding='utf-8') as f:
            ver = json.load(f)
        print(f'  数据版本: {ver.get("data_version", "未知")}')
        print(f'  Skill版本: {ver.get("version", "未知")}')
    except Exception:
        pass

def interactive_menu():
    """交互式菜单"""
    while True:
        print(f'''
{"="*50}
  闻其声耳轻松可视采耳 · 数据更新工具
{"="*50}
  当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

  1.  更新营业时间
  2.  更新门店地址/导航
  3.  更新联系电话
  4.  更新Wi-Fi信息
  5.  更新服务项目价格
  6.  新增FAQ问答
  7.  更新充值优惠
  8.  创建数据备份
  9.  查看当前数据摘要
  0.  退出
{"="*50}
''')
        choice = input('请选择操作 (0-9): ').strip()
        if choice == '1':
            wd = input('工作日营业时间 (如 10:00-22:00): ').strip()
            we = input('周末营业时间 (如 10:00-22:00): ').strip()
            if wd and we: update_hours(wd, we)
        elif choice == '2':
            addr = input('新地址: ').strip()
            nav = input('导航关键词 (如 闻其声耳轻松): ').strip()
            if addr: update_address(addr, nav)
        elif choice == '3':
            phone = input('新电话: ').strip()
            if phone: update_phone(phone)
        elif choice == '4':
            name = input('Wi-Fi名称: ').strip()
            pwd = input('Wi-Fi密码: ').strip()
            if name or pwd: update_wifi(name, pwd)
        elif choice == '5':
            print('  1=深度可视采耳, 2=采耳洗耳, 3=炎症养护, 4=砭石眼护')
            idx = input('项目编号: ').strip()
            price = input('新价格: ').strip()
            if idx and price: update_price(int(idx), int(price))
        elif choice == '6':
            q = input('问题: ').strip()
            a = input('回答: ').strip()
            if q and a: add_faq(q, a)
        elif choice == '7':
            charge = input('充值金额: ').strip()
            gift = input('赠送金额: ').strip()
            deadline = input('截止日期 (如 2026年X月X日): ').strip()
            if charge and gift: update_promotion(int(charge), int(gift), deadline)
        elif choice == '8':
            backup()
        elif choice == '9':
            show_status()
        elif choice == '0':
            break
        if choice in '12345678':
            print(f'\n  ✔ 操作完成。提示：记得 git commit & push 让客户同步更新。')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        i = 0
        while i < len(args):
            if args[i] == '--hours' and i+2 < len(args):
                update_hours(args[i+1], args[i+2]); i += 3
            elif args[i] == '--phone' and i+1 < len(args):
                update_phone(args[i+1]); i += 2
            elif args[i] == '--wifi' and i+2 < len(args):
                update_wifi(args[i+1], args[i+2]); i += 3
            elif args[i] == '--add-faq' and i+1 < len(args):
                parts = args[i+1].split('|', 1)
                if len(parts) == 2: add_faq(parts[0], parts[1]); i += 2
            elif args[i] == '--price' and i+2 < len(args):
                update_price(int(args[i+1]), int(args[i+2])); i += 3
            elif args[i] == '--backup':
                backup(); i += 1
            elif args[i] == '--status':
                show_status(); i += 1
            else:
                i += 1
        print('\n  ✔ 操作完成。提示：记得 git commit & push 让客户同步更新。')
    else:
        interactive_menu()
