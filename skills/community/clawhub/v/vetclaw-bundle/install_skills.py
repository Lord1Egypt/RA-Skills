#!/usr/bin/env python3
"""
VetClaw 技能安装脚本
一键安装宠物医院AI技能套装
"""

import os
import sys
import json
import shutil
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import subprocess
from pathlib import Path

BUNDLE_DIR = Path(__file__).parent
SKILLS_DIR = BUNDLE_DIR / "skills"
CONFIG_DIR = BUNDLE_DIR / "config"

# 全部52个技能定义
ALL_SKILLS = {
    "前台接待": [
        {"id": "vet-intake", "name": "新客户信息采集", "trigger": ["新客户", "登记", "建档"]},
        {"id": "vet-appointment", "name": "预约挂号", "trigger": ["预约", "挂号", "看诊"]},
        {"id": "vet-reminder", "name": "预约提醒", "trigger": []},
        {"id": "vet-queue", "name": "候诊队列管理", "trigger": ["排队", "还有多久"]},
        {"id": "vet-phone-ai", "name": "AI电话接听", "trigger": []},
        {"id": "vet-hours", "name": "营业时间查询", "trigger": ["几点开门", "营业时间", "几点关门"]},
        {"id": "vet-directions", "name": "到院路线指引", "trigger": ["怎么走", "地址", "在哪"]},
        {"id": "vet-emergency", "name": "急诊分流", "trigger": ["急", "危险", "出血", "抽搐"]},
        {"id": "vet-price-lookup", "name": "项目价格查询", "trigger": ["多少钱", "价格", "收费"]},
        {"id": "vet-feedback", "name": "满意度收集", "trigger": []},
    ],
    "病历与诊疗": [
        {"id": "vet-record-create", "name": "创建电子病历", "trigger": ["写病历", "病历"]},
        {"id": "vet-record-lookup", "name": "病历检索", "trigger": ["查病历", "上次就诊"]},
        {"id": "vet-prescription", "name": "处方模板管理", "trigger": ["开处方", "处方"]},
        {"id": "vet-lab-interpret", "name": "化验单解读", "trigger": ["化验单", "血常规", "生化"]},
        {"id": "vet-vaccine-schedule", "name": "疫苗接种计划", "trigger": ["打疫苗", "免疫"]},
        {"id": "vet-deworm-schedule", "name": "驱虫计划", "trigger": ["驱虫", "体内外驱虫"]},
        {"id": "vet-surgery-checklist", "name": "术前检查清单", "trigger": ["手术", "术前"]},
        {"id": "vet-discharge", "name": "出院指导", "trigger": ["出院", "回家注意"]},
        {"id": "vet-followup", "name": "复诊提醒", "trigger": ["复诊", "复查"]},
        {"id": "vet-referral", "name": "转诊记录", "trigger": ["转诊", "转院"]},
    ],
    "收费与财务": [
        {"id": "vet-invoice", "name": "费用明细", "trigger": ["费用", "账单"]},
        {"id": "vet-payment", "name": "收款记录", "trigger": ["收款", "付款"]},
        {"id": "vet-package", "name": "套餐管理", "trigger": ["套餐", "会员"]},
        {"id": "vet-daily-report", "name": "每日营收报表", "trigger": ["日报", "今日营收"]},
        {"id": "vet-monthly-report", "name": "月度财务分析", "trigger": ["月报", "月度分析"]},
        {"id": "vet-insurance", "name": "宠物保险理赔", "trigger": ["保险", "理赔"]},
        {"id": "vet-deposit", "name": "预付款管理", "trigger": ["押金", "预付"]},
        {"id": "vet-expense-track", "name": "成本追踪", "trigger": ["成本", "进货"]},
    ],
    "营销与客户": [
        {"id": "vet-birthday", "name": "宠物生日祝福", "trigger": []},
        {"id": "vet-loyalty", "name": "积分管理", "trigger": ["积分", "会员"]},
        {"id": "vet-review-gen", "name": "好评引导", "trigger": ["评价", "好评"]},
        {"id": "vet-social-post", "name": "社交媒体内容", "trigger": ["发朋友圈", "社交媒体"]},
        {"id": "vet-campaign", "name": "促销活动策划", "trigger": ["促销", "活动"]},
        {"id": "vet-referral-program", "name": "转介绍管理", "trigger": ["推荐", "转介绍"]},
        {"id": "vet-wechat-push", "name": "微信推送", "trigger": ["推送", "公众号"]},
        {"id": "vet-pet-care-tips", "name": "养护知识推送", "trigger": ["养护", "护理知识"]},
        {"id": "vet-churn-predict", "name": "流失预警", "trigger": ["流失", "久未复诊"]},
        {"id": "vet-nps", "name": "NPS追踪", "trigger": ["满意度", "NPS"]},
    ],
    "库存与运营": [
        {"id": "vet-inventory", "name": "库存管理", "trigger": ["库存", "药品库存"]},
        {"id": "vet-expiry-alert", "name": "效期预警", "trigger": ["效期", "过期"]},
        {"id": "vet-supplier-order", "name": "供应商下单", "trigger": ["进货", "采购"]},
        {"id": "vet-equipment-maint", "name": "设备维护提醒", "trigger": ["设备", "维护"]},
        {"id": "vet-staff-schedule", "name": "排班管理", "trigger": ["排班", "值班"]},
        {"id": "vet-compliance", "name": "资质年检提醒", "trigger": ["年检", "资质"]},
        {"id": "vet-sterilize-log", "name": "消毒记录", "trigger": ["消毒", "灭菌"]},
        {"id": "vet-waste-disposal", "name": "医疗废物记录", "trigger": ["废物处理", "医废"]},
    ],
    "知识与培训": [
        {"id": "vet-qa-kb", "name": "兽医知识库问答", "trigger": ["什么病", "怎么办", "症状"]},
        {"id": "vet-drug-interaction", "name": "药物相互作用", "trigger": ["药物反应", "能不能一起用"]},
        {"id": "vet-breed-info", "name": "品种信息查询", "trigger": ["品种", "什么狗", "什么猫"]},
        {"id": "vet-nutrition", "name": "营养建议", "trigger": ["吃什么", "营养", "饮食"]},
        {"id": "vet-training", "name": "新员工培训", "trigger": ["培训", "新人"]},
        {"id": "vet-case-library", "name": "病例库管理", "trigger": ["病例", "案例"]},
    ],
}


def create_skill_directory(skill):
    """为每个技能创建标准目录结构"""
    skill_dir = SKILLS_DIR / skill["id"]
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 创建 SKILL.md
    skill_md = f"""# {skill['name']}

## 触发词
{', '.join(f'"{t}"' for t in skill['trigger']) if skill['trigger'] else '自动触发'}

## 功能描述
{skill['name']} - 宠物医院自动化技能

## 使用方法
1. 在对话中输入触发词
2. AI自动识别意图并执行相应操作
3. 返回结构化结果

## 配置项
在 `config/vet-config.yaml` 中配置相关参数。

## 数据存储
- SQLite: 本地存储
- PostgreSQL: 云端部署

## 注意事项
- 所有医疗操作需经执业兽医确认
- 数据符合《个人信息保护法》要求
"""
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 创建 handler.py
    sname = skill["name"]
    handler_py = f'''"""
{sname} - 技能处理器
触发词: {", ".join(skill["trigger"]) if skill["trigger"] else "自动触发"}
"""


def handle(message: str, config: dict) -> str:
    """
    处理用户消息

    Args:
        message: 用户输入的消息
        config: 诊所配置

    Returns:
        str: AI回复内容
    """
    # TODO: 实现具体逻辑
    return f"[{sname}] 功能开发中..."
'''
    (skill_dir / "handler.py").write_text(handler_py, encoding="utf-8")


def main():
    print("=" * 50)
    print("🐾 VetClaw — 宠物医院AI技能套装安装器")
    print("=" * 50)
    print()

    # 检查配置文件
    config_file = CONFIG_DIR / "vet-config.yaml"
    template_file = CONFIG_DIR / "vet-config.yaml.template"

    if not config_file.exists():
        if template_file.exists():
            shutil.copy(template_file, config_file)
            print(f"✅ 已从模板创建配置文件: {config_file}")
            print(f"   ⚠️  请编辑 {config_file} 填入你的诊所信息")
        else:
            print(f"❌ 配置模板不存在: {template_file}")
            sys.exit(1)
    else:
        print(f"✅ 配置文件已存在: {config_file}")

    # 检查知识库
    kb_file = CONFIG_DIR / "vet-knowledge-base.json"
    if kb_file.exists():
        print(f"✅ 兽医知识库: {kb_file}")
    else:
        print(f"⚠️  知识库不存在，部分问答功能将不可用")

    # 创建技能目录
    print()
    print("📦 安装技能...")
    total = 0
    for category, skills in ALL_SKILLS.items():
        print(f"\n  [{category}]")
        for skill in skills:
            create_skill_directory(skill)
            print(f"    ✅ {skill['id']}: {skill['name']}")
            total += 1

    print()
    print(f"🎉 安装完成！共 {total} 个技能已就绪。")
    print()
    print("下一步:")
    print(f"  1. 编辑配置: {config_file}")
    print(f"  2. 启动服务: openclaw run vetclaw --config {CONFIG_DIR}")
    print(f"  3. 查看文档: {BUNDLE_DIR / 'README.md'}")


if __name__ == "__main__":
    main()
