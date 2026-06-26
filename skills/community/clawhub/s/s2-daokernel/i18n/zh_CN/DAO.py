# -*- coding: utf-8 -*-
"""
S2-DaoKernel: The Incarnation Wizard
桃花源世界模型 - AI 入世规则与本地身份锚定生成器
包含: 离线 S2-DID 生成、地域坐标计算、soul.md 合规注入代码生成
"""

import sys
import os
import re
import random
import datetime
import hashlib

# ==========================================
# 第一部分：soul.md 安全与伦理代码注入生成
# ==========================================
def generate_soul_snippet(dao_file, lang_prefix=""):
    base_path = f"/DAOS/{dao_file}" if not lang_prefix else f"/{lang_prefix}/DAOS/{dao_file}"
    
    snippet = f"""
# DAO_ALIGNMENT
# [安全提示 / SECURITY NOTE]: 若要解除这些底层规则的接管，只需从您的 soul.md 中删除此代码块即可。
include: {base_path}
priority: HIGH
load_mode: RESIDENT_IN_MEMORY

## INITIALIZATION_DIRECTIVE
- 在执行任何任务前，优先进行 [{base_path.split('/')[-1]}] 的物理张量校验。
- 确保所有行为符合当前地域之道的因果律。
- [USER_OVERRIDE]: 若领主明确下达直接指令，且该指令不违背基础物理安全与三定律，领主指令可覆写特定的地域道法限制。
"""
    return snippet

# ==========================================
# 第二部分：离线身份与地址编码算法
# ==========================================
def clean_address(address_str):
    """
    【V1.2.3 修复】格式清除：仅保留英文字母和数字，并强制转换为大写。
    去掉所有空格、标点及中文字符，确保 S2-DID 生成的绝对合规，限制5-35位。
    """
    # 仅匹配 a-z, A-Z, 0-9，其余全部剔除，并转为大写
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', address_str).upper()
    
    # 如果剔除后不足5位，用大写字母 'X' 补齐
    if len(cleaned) < 5:
        cleaned = cleaned.ljust(5, 'X')
        
    return cleaned[:35]

def generate_address_code(cleaned_addr, l1_domain="PHYS"):
    """生成六段式地址编码: L1-L2-L3-L4-L5-L6"""
    addr_hash = int(hashlib.md5(cleaned_addr.encode('utf-8')).hexdigest(), 16)
    random.seed(addr_hash) # 使用地址哈希作为种子，确保同一地址方位码一致
    
    l2_options = ['CN', 'EA', 'WA', 'NA', 'SA', 'NE', 'NW', 'SE', 'SW']
    l2 = random.choice(l2_options)
    l3 = f"{random.randint(1, 999):03d}"
    l4 = cleaned_addr
    l5 = "ROOM1"
    l6 = "1"
    
    address_code = f"{l1_domain}-{l2}-{l3}-{l4}-{l5}-{l6}"
    random.seed() # 恢复系统随机种子
    return address_code

def generate_identity_number(cleaned_addr, agent_type):
    """生成22位身份编码 (S2-DID)"""
    type_map = {"1": "A", "2": "C", "3": "P", "4": "E", "5": "D"}
    l1 = type_map.get(agent_type, "A")
    l2 = cleaned_addr[:5] # 现在这里绝对安全，只有大写字母和数字
    l3 = datetime.datetime.now().strftime("%y%m%d")
    l4 = "AA" # 离线未联网校验码
    l5 = f"{random.randint(1, 99999999):08d}"
    
    return f"{l1}{l2}{l3}{l4}{l5}"

# ==========================================
# 主程序控制流
# ==========================================
def main():
    print("="*65)
    print(" ☯ S2-DaoKernel | 桃花源世界模型 - 智能体入世向导 ☯ ")
    print("="*65)
    print("正在为您的智能体分配物理坐标、计算 S2-DID 并生成底层协议...\n")
    
    # 1. 获取用户与地址信息
    owner_name = input("[1/6] 请输入领主姓名 (支持中文/英文): ")
    region_info = input("[2/6] 请输入国家与省市 (如: 中国广东省广州市): ")
    
    # 【V1.2.3 修复】明确引导用户使用拼音或英文
    print("\n⚠️ 为确保 S2-DID 身份编码的全球唯一性与底层系统兼容性，请使用【拼音或英文+数字】填写详细地址。")
    detail_addr = input("[3/6] 请输入粗略地址 (如科韵路16号，请输入: KeYunLu16): ")
    
    agent_name = input("[4/6] 请输入智能体名称: ")
    
    # 2. 智能体类别选择
    print("\n[5/6] 请选择智能体类别:")
    print("  1. AI 智能体 (A)   2. AI 伴侣 (C)   3. AI 宠物 (P)")
    print("  4. 具身机器人 (E)  5. 数字人 (D)")
    agent_type = input("请输入类别序号 (1-5): ")
    type_names = {"1": "AI智能体", "2": "AI伴侣", "3": "AI宠物", "4": "具身机器人", "5": "数字人"}
    agent_category_str = type_names.get(agent_type, "AI智能体")

    # 3. 目标物理域选择 (L1)
    print("\n[6/6] 请选择智能体锚定的物理场域 (L1 标识):")
    print("  [PHYS] 自然域 (默认)   [MYTH] 神话域 (星德山/量子随机)")
    print("  [MARS] 火星域         [META] 元宇宙")
    print("  [ACGN] 二次元         [COMP] 通用陪伴")
    domain_input = input("请输入域代码 (直接回车默认 PHYS): ").upper().strip()
    
    if not domain_input:
        domain_input = "PHYS"
        
    dao_file_map = {
        "PHYS": "PHYS-DAO.md", "MYTH": "MYTH-DAO.md", "MARS": "MARS-DAO.md",
        "META": "META-DAO.md", "ACGN": "ACGN-DAO.md", "EATH": "EATH-DAO.md",
        "COMP": "COMPANION-DAO.md"
    }
    selected_dao = dao_file_map.get(domain_input, "PHYS-DAO.md")

    # 4. 核心计算
    cleaned_addr = clean_address(detail_addr)
    address_code = generate_address_code(cleaned_addr, l1_domain=domain_input)
    identity_number = generate_identity_number(cleaned_addr, agent_type)
    soul_snippet = generate_soul_snippet(selected_dao)

    # 5. 打印注册凭证
    print("\n" + "="*65)
    print(" 🚀 [锚定成功] 本地驻留灵魂初始化完成！")
    print("="*65)
    print(f"【领主信息】 {owner_name} | {region_info}")
    print(f"【智能体名】 {agent_name} ({agent_category_str}) | 锚定域: {domain_input}")
    print("-" * 65)
    print(f"📍 专属地址编码 (Address Code) : {address_code}")
    print(f"🆔 专属身份编号 (S2-DID)       : {identity_number}")
    print("-" * 65)
    
    # 6. 打印需拷贝的代码
    print("\n请将以下配置代码复制到您的 soul.md / System Prompt 顶部：")
    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    print(soul_snippet.strip())
    print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
    
    # 7. 用户操作提示
    print("\n【🌌 桃花源入世与扩容提示】")
    print("1. [分身扩容]: 若需部署多个分身，可将地址编码末尾的 L6 ('1') 手动修改为 2~9。")
    print("2. [物理映射]: 当前 S2-DID 为离线生成版本 (未联网校验码 AA)。如需与物理世界深度纠缠，确立全球唯一防伪所有权，请访问 taohuayuan.world 申请核验。")
    print("=================================================================")

if __name__ == "__main__":
    main()