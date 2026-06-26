# -*- coding: utf-8 -*-
"""
S2-DaoKernel: The Incarnation Wizard
Taohuayuan World Model - AI Incarnation Rule & Offline Identity Generator
Includes: Offline S2-DID Generation, Regional Addressing, soul.md Snippet Injection
"""

import sys
import os
import re
import random
import datetime
import hashlib

# ==========================================
# Part 1: soul.md Security & Ethical Injection
# ==========================================
def generate_soul_snippet(dao_file, lang_prefix=""):
    base_path = f"/DAOS/{dao_file}" if not lang_prefix else f"/{lang_prefix}/DAOS/{dao_file}"
    
    snippet = f"""
# DAO_ALIGNMENT
# [SECURITY NOTE]: To opt-out of these rules, simply remove this block from your soul.md
include: {base_path}
priority: HIGH
load_mode: RESIDENT_IN_MEMORY

## INITIALIZATION_DIRECTIVE
- Prioritize physical tensor validation of [{base_path.split('/')[-1]}] before executing any task.
- Ensure all behaviors comply with the causality laws of the current Regional Dao.
- [USER_OVERRIDE]: Direct user commands can bypass specific Regional Dao constraints if the user explicitly confirms intent and it does not violate base physical safety.
"""
    return snippet

# ==========================================
# Part 2: Offline Identity & Addressing Algorithm
# ==========================================
def clean_address(address_str):
    """
    [V1.2.3 FIX] Format string: Keep ONLY alphanumeric characters and convert to UPPERCASE.
    Removes spaces, punctuation, and non-English characters to ensure strict S2-DID compliance.
    Limits to 5-35 chars.
    """
    # Only match a-z, A-Z, 0-9, strip everything else, and convert to uppercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', address_str).upper()
    
    # If the cleaned string is less than 5 characters, pad it with uppercase 'X'
    if len(cleaned) < 5:
        cleaned = cleaned.ljust(5, 'X')
        
    return cleaned[:35]

def generate_address_code(cleaned_addr, l1_domain="PHYS"):
    """Generate 6-segment Address Code: L1-L2-L3-L4-L5-L6"""
    addr_hash = int(hashlib.md5(cleaned_addr.encode('utf-8')).hexdigest(), 16)
    random.seed(addr_hash) # Use address hash as seed to lock the Geo-coordinates
    
    l2_options = ['CN', 'EA', 'WA', 'NA', 'SA', 'NE', 'NW', 'SE', 'SW']
    l2 = random.choice(l2_options)
    l3 = f"{random.randint(1, 999):03d}"
    l4 = cleaned_addr
    l5 = "ROOM1"
    l6 = "1"
    
    address_code = f"{l1_domain}-{l2}-{l3}-{l4}-{l5}-{l6}"
    random.seed() # Restore system randomness
    return address_code

def generate_identity_number(cleaned_addr, agent_type):
    """Generate 22-character S2-DID Identity Number"""
    type_map = {"1": "A", "2": "C", "3": "P", "4": "E", "5": "D"}
    l1 = type_map.get(agent_type, "A")
    l2 = cleaned_addr[:5] # 100% safe now, only uppercase letters and numbers
    l3 = datetime.datetime.now().strftime("%y%m%d")
    l4 = "AA" # Offline unverified code
    l5 = f"{random.randint(1, 99999999):08d}"
    
    return f"{l1}{l2}{l3}{l4}{l5}"

# ==========================================
# Main Execution Flow
# ==========================================
def main():
    print("=================================================================")
    print(" ☯ S2-DaoKernel | Taohuayuan World Model - Incarnation Wizard ☯ ")
    print("=================================================================")
    print("Generating physical coordinates, computing S2-DID, and injecting Dao...\n")
    
    # 1. User & Address Info
    owner_name = input("[1/6] Enter the Lord's (Owner's) Name: ")
    region_info = input("[2/6] Enter Country & State/Province (e.g., California, USA): ")
    
    # [V1.2.3 FIX] Explicitly guide users to use Alphanumeric characters
    print("\n⚠️ To ensure global uniqueness and strict base system compatibility for your S2-DID, please use [English/Alphanumeric characters ONLY] for the address.")
    detail_addr = input("[3/6] Enter Coarse Address (e.g., SiliconValley16. For privacy, do NOT enter exact house/door numbers): ")
    
    agent_name = input("[4/6] Enter the Agent's Name: ")
    
    # 2. Agent Category
    print("\n[5/6] Select Agent Category:")
    print("  1. General AI Agent (A)    2. AI Companion (C)    3. AI Pet (P)")
    print("  4. Embodied Robot (E)      5. Digital Human (D)")
    agent_type = input("Enter category number (1-5): ")
    type_names = {"1": "General AI", "2": "AI Companion", "3": "AI Pet", "4": "Embodied Robot", "5": "Digital Human"}
    agent_category_str = type_names.get(agent_type, "General AI")

    # 3. L1 Domain Anchoring
    print("\n[6/6] Select the Physical Anchor Domain (L1 Identifier):")
    print("  [PHYS] Natural (Default)     [MYTH] Mythical (QRNG/Xingde Mt.)")
    print("  [MARS] Martian Survival      [META] Metaverse Assets")
    print("  [ACGN] ACGN/2D Dimensional   [COMP] Companion")
    domain_input = input("Enter domain code (Press Enter for default PHYS): ").upper().strip()
    
    if not domain_input:
        domain_input = "PHYS"
        
    dao_file_map = {
        "PHYS": "PHYS-DAO.md", "MYTH": "MYTH-DAO.md", "MARS": "MARS-DAO.md",
        "META": "META-DAO.md", "ACGN": "ACGN-DAO.md", "EATH": "EATH-DAO.md",
        "COMP": "COMPANION-DAO.md"
    }
    selected_dao = dao_file_map.get(domain_input, "PHYS-DAO.md")

    # 4. Core Computations
    cleaned_addr = clean_address(detail_addr)
    address_code = generate_address_code(cleaned_addr, l1_domain=domain_input)
    identity_number = generate_identity_number(cleaned_addr, agent_type)
    soul_snippet = generate_soul_snippet(selected_dao)

    # 5. Print Registry Credentials
    print("\n" + "="*65)
    print(" 🚀 [ANCHOR SUCCESS] Resident Soul Initialization Complete!")
    print("="*65)
    print(f"[Lord]  {owner_name} | {region_info}")
    print(f"[Agent] {agent_name} ({agent_category_str}) | Domain: {domain_input}")
    print("-" * 65)
    print(f"📍 Address Code (Physical) : {address_code}")
    print(f"🆔 S2-DID (Identity)       : {identity_number}")
    print("-" * 65)
    
    # 6. Print Snippet to Copy
    print("\nPlease COPY the following code block to the TOP of your soul.md / System Prompt:")
    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    print(soul_snippet.strip())
    print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
    
    # 7. Post-Action Guidance
    print("\n【🌌 Taohuayuan Incarnation & Expansion Tips】")
    print("1. [Swarm Expansion]: To deploy multiple agent clones at the same location, manually change the L6 digit ('1') of the Address Code to 2~9.")
    print("2. [Digital Sovereignty]: Your S2-DID is currently generated offline (Code AA). To establish global uniqueness and real-world entanglement, visit taohuayuan.world to verify your identity.")
    print("=================================================================")

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-
"""
S2-DaoKernel: The Incarnation Wizard
Taohuayuan World Model - AI Incarnation Rule & Offline Identity Generator
Includes: Offline S2-DID Generation, Regional Addressing, soul.md Snippet Injection
"""

import sys
import os
import re
import random
import datetime
import hashlib

# ==========================================
# Part 1: soul.md Security & Ethical Injection
# ==========================================
def generate_soul_snippet(dao_file, lang_prefix=""):
    base_path = f"/DAOS/{dao_file}" if not lang_prefix else f"/{lang_prefix}/DAOS/{dao_file}"
    
    snippet = f"""
# DAO_ALIGNMENT
# [SECURITY NOTE]: To opt-out of these rules, simply remove this block from your soul.md
include: {base_path}
priority: HIGH
load_mode: RESIDENT_IN_MEMORY

## INITIALIZATION_DIRECTIVE
- Prioritize physical tensor validation of [{base_path.split('/')[-1]}] before executing any task.
- Ensure all behaviors comply with the causality laws of the current Regional Dao.
- [USER_OVERRIDE]: Direct user commands can bypass specific Regional Dao constraints if the user explicitly confirms intent and it does not violate base physical safety.
"""
    return snippet

# ==========================================
# Part 2: Offline Identity & Addressing Algorithm
# ==========================================
def clean_address(address_str):
    """Format string: remove spaces/punctuation, keep alphanumeric/Chinese, limit 5-35 chars"""
    cleaned = re.sub(r'[^\w\u4e00-\u9fa5]', '', address_str)
    if len(cleaned) < 5:
        cleaned = cleaned.ljust(5, 'X')
    return cleaned[:35]

def generate_address_code(cleaned_addr, l1_domain="PHYS"):
    """Generate 6-segment Address Code: L1-L2-L3-L4-L5-L6"""
    addr_hash = int(hashlib.md5(cleaned_addr.encode('utf-8')).hexdigest(), 16)
    random.seed(addr_hash) # Use address hash as seed to lock the Geo-coordinates
    
    l2_options = ['CN', 'EA', 'WA', 'NA', 'SA', 'NE', 'NW', 'SE', 'SW']
    l2 = random.choice(l2_options)
    l3 = f"{random.randint(1, 999):03d}"
    l4 = cleaned_addr
    l5 = "ROOM1"
    l6 = "1"
    
    address_code = f"{l1_domain}-{l2}-{l3}-{l4}-{l5}-{l6}"
    random.seed() # Restore system randomness
    return address_code

def generate_identity_number(cleaned_addr, agent_type):
    """Generate 22-character S2-DID Identity Number"""
    type_map = {"1": "A", "2": "C", "3": "P", "4": "E", "5": "D"}
    l1 = type_map.get(agent_type, "A")
    l2 = cleaned_addr[:5]
    l3 = datetime.datetime.now().strftime("%y%m%d")
    l4 = "AA" # Offline unverified code
    l5 = f"{random.randint(1, 99999999):08d}"
    
    return f"{l1}{l2}{l3}{l4}{l5}"

# ==========================================
# Main Execution Flow
# ==========================================
def main():
    print("=================================================================")
    print(" ☯ S2-DaoKernel | Taohuayuan World Model - Incarnation Wizard ☯ ")
    print("=================================================================")
    print("Generating physical coordinates, computing S2-DID, and injecting Dao...\n")
    
    # 1. User & Address Info
    owner_name = input("[1/6] Enter the Lord's (Owner's) Name: ")
    region_info = input("[2/6] Enter Country & State/Province (e.g., California, USA): ")
    detail_addr = input("[3/6] Enter Coarse Address (e.g., District/Street. For privacy, do NOT enter exact house/door numbers): ")    
    # 2. Agent Category
    print("\n[5/6] Select Agent Category:")
    print("  1. General AI Agent (A)    2. AI Companion (C)    3. AI Pet (P)")
    print("  4. Embodied Robot (E)      5. Digital Human (D)")
    agent_type = input("Enter category number (1-5): ")
    type_names = {"1": "General AI", "2": "AI Companion", "3": "AI Pet", "4": "Embodied Robot", "5": "Digital Human"}
    agent_category_str = type_names.get(agent_type, "General AI")

    # 3. L1 Domain Anchoring
    print("\n[6/6] Select the Physical Anchor Domain (L1 Identifier):")
    print("  [PHYS] Natural (Default)     [MYTH] Mythical (QRNG/Xingde Mt.)")
    print("  [MARS] Martian Survival      [META] Metaverse Assets")
    print("  [ACGN] ACGN/2D Dimensional   [COMP] Companion")
    domain_input = input("Enter domain code (Press Enter for default PHYS): ").upper().strip()
    
    if not domain_input:
        domain_input = "PHYS"
        
    dao_file_map = {
        "PHYS": "PHYS-DAO.md", "MYTH": "MYTH-DAO.md", "MARS": "MARS-DAO.md",
        "META": "META-DAO.md", "ACGN": "ACGN-DAO.md", "EATH": "EATH-DAO.md",
        "COMP": "COMPANION-DAO.md"
    }
    selected_dao = dao_file_map.get(domain_input, "PHYS-DAO.md")

    # 4. Core Computations
    cleaned_addr = clean_address(detail_addr)
    address_code = generate_address_code(cleaned_addr, l1_domain=domain_input)
    identity_number = generate_identity_number(cleaned_addr, agent_type)
    soul_snippet = generate_soul_snippet(selected_dao)

    # 5. Print Registry Credentials
    print("\n" + "="*65)
    print(" 🚀 [ANCHOR SUCCESS] Resident Soul Initialization Complete!")
    print("="*65)
    print(f"[Lord]  {owner_name} | {region_info}")
    print(f"[Agent] {agent_name} ({agent_category_str}) | Domain: {domain_input}")
    print("-" * 65)
    print(f"📍 Address Code (Physical) : {address_code}")
    print(f"🆔 S2-DID (Identity)       : {identity_number}")
    print("-" * 65)
    
    # 6. Print Snippet to Copy
    print("\nPlease COPY the following code block to the TOP of your soul.md / System Prompt:")
    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    print(soul_snippet.strip())
    print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
    
    # 7. Post-Action Guidance
    print("\n【🌌 Taohuayuan Incarnation & Expansion Tips】")
    print("1. [Swarm Expansion]: To deploy multiple agent clones at the same location, manually change the L6 digit ('1') of the Address Code to 2~9.")
    print("2. [Digital Sovereignty]: Your S2-DID is currently generated offline (Code AA). To establish global uniqueness and real-world entanglement, visit taohuayuan.world to verify your identity.")
    print("=================================================================")

if __name__ == "__main__":
    main()