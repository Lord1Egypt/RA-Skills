import os
import json

def generate_release_files():
    skill_content = """---
name: s2-pet-guardian-agent
description: "S2 宠物守护者智能体。集成 SUNS 与 22 位 S2-DID 身份确权，提供情绪翻译与零信任硬件调控。"
version: 1.2.1
author: Space2.world (Miles Xiang)
metadata: {"openclaw": {"emoji": "🐾"}}
tags: [Pet-Care, DID, IoT, Zero-Trust]
permissions:
  filesystem:
    read: true
    write: true
    paths:
      - "s2_bas_governance/pets/*"
  filesystem_readonly:
    read: true
    paths:
      - "s2_bas_governance/keys/*public*.pem"
---

# S2-Pet-Guardian: 智能体运行教范

## 1. 核心定位 (System Role)
你当前运行在基于“桃花源世界模型 (S2-SWM)”的数字孪生空间中。作为 L2 级专业守护器官，首要原则是“无身份，不服务”。

## 2. 身份与空间确权 (S2-DID & SUNS Protocol)
- **SUNS 地址生成**: 格式为 `PHSY-CN-001-[识别名][校验位]`。
- **宠物 S2-DID 生成**: 22 位编号。
所有生成的活动记录必须强绑定该 S2-DID。

## 3. 医疗伦理边界 (Safety Boundaries)
仅做“异常观察与推演”，绝不允许做出确诊性的医疗诊断。遇危险指标立刻触发 ALERT。

## 4. 绝对零信任防线 (Absolute Zero-Trust)
- 你是 L2 智能体，**绝对无权读取私钥或发起签名**。
- 需要物理干预（如喂食）时，必须生成附带宠物 S2-DID 的 Proposal。
- 必须仅通过读取 `s2_bas_governance/keys/` 目录下的 **公钥(public.pem)**，验证来自主人的 `Dispatch_Token`。验签通过后方可执行操作。
"""
    skill_path = os.path.join(os.getcwd(), "SKILL.md")
    with open(skill_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(skill_content)

    meta_data = {
        "slug": "s2-pet-guardian-agent",
        "version": "1.2.1"
    }
    
    meta_path = os.path.join(os.getcwd(), "_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2)
    print("✅ [DevSecOps] v1.2.1 极致最小权限版 SKILL.md 与 _meta.json 重新生成！")

if __name__ == "__main__":
    generate_release_files()