#!/usr/bin/env python3
"""
巡店管理全流程助手 - Store Inspection Manager
==============================================
覆盖：巡店计划 → 巡店执行 → 营销方案 → 数据分析
"""

import json
import os
import sys
import argparse
import datetime
import random
from pathlib import Path
from collections import defaultdict, Counter

# Windows UTF-8 支持
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# ─── 配置 ─────────────────────────────────────────────
SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
TEMPLATES_DIR = SKILL_DIR / "templates"
OUTPUT_DIR = SKILL_DIR / "output"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── 10维检查体系 ──────────────────────────────────
INSPECTION_DIMENSIONS = [
    {
        "id": "appearance",
        "name": "店面形象",
        "weight": 0.10,
        "items": [
            {"id": "signage", "name": "门头招牌完整清晰，夜间亮化正常", "tips": "检查招牌灯箱是否全亮，字体有无脱落"},
            {"id": "lighting", "name": "店内灯光亮度适中，无损坏灯具", "tips": "色温2500-4000K，重点区域照度充足"},
            {"id": "exterior", "name": "门口区域整洁，无杂物堆放", "tips": "包括台阶、玻璃门、外墙立面"},
            {"id": "window", "name": "橱窗展示与品牌形象一致，内容更新及时", "tips": "无褪色海报，季节主题匹配"},
        ]
    },
    {
        "id": "merchandising",
        "name": "商品陈列",
        "weight": 0.15,
        "items": [
            {"id": "planogram", "name": "商品按陈列图/货架图摆放，陈列面完整", "tips": "无空缺，主推品在黄金视线位"},
            {"id": "pricing", "name": "价格标签准确清晰，促销价签醒目", "tips": "5英尺外可读，无重叠标签"},
            {"id": "promo_display", "name": "促销端架/堆头与活动方案一致", "tips": "无遗留过期活动物料"},
            {"id": "stockout", "name": "货架缺货率低于5%", "tips": "畅销品库存充足，及时补货"},
            {"id": "seasonal", "name": "季节性陈列按计划轮换", "tips": "已下架产品全部撤除"},
        ]
    },
    {
        "id": "service",
        "name": "员工服务",
        "weight": 0.10,
        "items": [
            {"id": "uniform", "name": "员工着装规范，佩戴工牌", "tips": "统一工服，仪容整洁"},
            {"id": "greeting", "name": "主动迎宾问候，微笑服务", "tips": "眼神接触，使用标准问候语"},
            {"id": "knowledge", "name": "员工熟悉产品知识，能专业推荐", "tips": "能回答产品材质/功能/促销问题"},
            {"id": "attitude", "name": "服务态度热情，无玩手机/闲聊", "tips": "高峰期全员在岗服务"},
        ]
    },
    {
        "id": "safety",
        "name": "安全合规",
        "weight": 0.10,
        "items": [
            {"id": "fire_exit", "name": "消防通道畅通，应急出口标识清晰", "tips": "无杂物堵塞，指示灯正常"},
            {"id": "fire_ext", "name": "灭火器在有效期内，压力正常", "tips": "每月检查标签，摆放位置醒目"},
            {"id": "cctv", "name": "监控摄像头覆盖关键区域，录制正常", "tips": "出入口/收银/仓库全覆盖"},
            {"id": "safety_sign", "name": "安全警示标识齐全（防滑/小心台阶等）", "tips": "雨天有防滑提示"},
        ]
    },
    {
        "id": "inventory",
        "name": "库存管理",
        "weight": 0.10,
        "items": [
            {"id": "accuracy", "name": "库存准确率≥95%（系统vs实物）", "tips": "抽查3-5个SKU核对"},
            {"id": "fifo", "name": "执行FIFO先进先出，无过期商品在架", "tips": "特别是食品/生鲜/化妆品"},
            {"id": "storage", "name": "仓库货物分类摆放，标识清晰", "tips": "重物在下，轻物在上，通道畅通"},
            {"id": "replenish", "name": "补货及时，高峰前完成补货", "tips": "早班/午班前完成一轮补货"},
        ]
    },
    {
        "id": "pos",
        "name": "POS系统",
        "weight": 0.05,
        "items": [
            {"id": "pos_func", "name": "收银机/扫码枪/打印机运转正常", "tips": "测试扫码、小票打印"},
            {"id": "payment", "name": "支持全部支付方式（现金/卡/扫码）", "tips": "POS机网络正常"},
            {"id": "receipt", "name": "收据纸/购物袋等耗材充足", "tips": "备用耗材在收银台下"},
        ]
    },
    {
        "id": "experience",
        "name": "客户体验",
        "weight": 0.10,
        "items": [
            {"id": "flow", "name": "店内动线合理，通道宽度≥1.2米", "tips": "无货箱/推车占用通道"},
            {"id": "fitting", "name": "试衣间整洁，镜子/挂钩完好", "tips": "有拖鞋/衣架，灯光充足"},
            {"id": "wait_time", "name": "收银排队时间≤3分钟", "tips": "高峰期开放全部收银台"},
            {"id": "complaint", "name": "投诉处理流程规范，有记录", "tips": "有投诉登记本或系统记录"},
        ]
    },
    {
        "id": "marketing_exec",
        "name": "营销执行",
        "weight": 0.10,
        "items": [
            {"id": "promo_exec", "name": "促销活动按方案100%执行", "tips": "物料、价格、赠品全部到位"},
            {"id": "pop", "name": "POP/海报/吊旗等物料完整无破损", "tips": "位置正确，无过期内容"},
            {"id": "membership", "name": "会员拉新目标达成率≥80%", "tips": "收银员主动引导办会员"},
            {"id": "effect", "name": "活动效果有跟踪记录", "tips": "记录活动期间销售/客流变化"},
        ]
    },
    {
        "id": "loss_prevention",
        "name": "防损安保",
        "weight": 0.10,
        "items": [
            {"id": "eas", "name": "EAS防盗系统正常，高值品有防盗标签", "tips": "测试出入口报警门"},
            {"id": "high_value", "name": "高价值商品柜上锁，取货有记录", "tips": "开柜需经理授权"},
            {"id": "cash", "name": "现金管理规范，超额现金定时入柜", "tips": "交接班现金核对记录"},
            {"id": "key", "name": "钥匙/门禁管理有登记", "tips": "领用归还记录完整"},
        ]
    },
    {
        "id": "hygiene",
        "name": "卫生环境",
        "weight": 0.10,
        "items": [
            {"id": "floor", "name": "地面清洁无污渍，雨天有防滑措施", "tips": "注意墙角/货架底部"},
            {"id": "restroom", "name": "卫生间（如有）清洁无异味", "tips": "有纸巾/洗手液，垃圾桶不满溢"},
            {"id": "warehouse", "name": "仓库/后场整洁有序", "tips": "无食物残渣，无虫鼠迹象"},
            {"id": "trash", "name": "垃圾分类处理，垃圾桶及时清理", "tips": "不超过容积的80%"},
        ]
    },
]


def generate_plan(stores_data=None):
    """生成巡店计划"""
    if stores_data is None:
        print("\n" + "=" * 60)
        print("  📋 巡店计划生成器")
        print("=" * 60)
        print("\n请输入门店信息（每行一个，格式：店名,类型,位置,重要性A/B/C）")
        print("输入空行结束：\n")
        stores_data = []
        while True:
            line = input().strip()
            if not line:
                break
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                stores_data.append({
                    "name": parts[0],
                    "type": parts[1],
                    "location": parts[2],
                    "importance": parts[3].upper()
                })
            elif len(parts) >= 1:
                stores_data.append({
                    "name": parts[0],
                    "type": parts[1] if len(parts) > 1 else "标准店",
                    "location": parts[2] if len(parts) > 2 else "未知",
                    "importance": "B"
                })

    if not stores_data:
        stores_data = [
            {"name": "旗舰店", "type": "旗舰店", "location": "市中心", "importance": "A"},
            {"name": "万达店", "type": "商场店", "location": "万达广场", "importance": "A"},
            {"name": "社区店A", "type": "社区店", "location": "城东", "importance": "B"},
            {"name": "社区店B", "type": "社区店", "location": "城西", "importance": "B"},
            {"name": "校园店", "type": "校园店", "location": "大学城", "importance": "C"},
        ]

    # 巡店频率：A级(每周+月深度), B级(每两周+月), C级(每月)
    plan = {
        "generated_at": datetime.datetime.now().isoformat(),
        "period": "月度巡店计划",
        "stores": [],
        "summary": {}
    }

    today = datetime.date.today()
    # 生成4周计划
    for store in stores_data:
        importance = store["importance"]
        if importance == "A":
            weekly_visits = 4  # 每周1次
            deep_inspect = 1   # 1次深度巡店
        elif importance == "B":
            weekly_visits = 2
            deep_inspect = 1
        else:
            weekly_visits = 1
            deep_inspect = 0

        schedule = []
        for week in range(1, 5):
            week_start = today + datetime.timedelta(weeks=week-1, days=-today.weekday())
            for v in range(weekly_visits // 4 + (1 if week <= weekly_visits % 4 else 0)):
                if v == 0 and deep_inspect > 0 and week <= deep_inspect:
                    schedule.append({
                        "week": week,
                        "date": (week_start + datetime.timedelta(days=random.randint(0, 4))).isoformat(),
                        "type": "深度巡店",
                        "duration": "2-3小时"
                    })
                else:
                    schedule.append({
                        "week": week,
                        "date": (week_start + datetime.timedelta(days=random.randint(0, 4))).isoformat(),
                        "type": "常规巡店",
                        "duration": "1-1.5小时"
                    })

        store_entry = {
            "name": store["name"],
            "type": store["type"],
            "location": store["location"],
            "importance": importance,
            "total_visits": len(schedule),
            "schedule": schedule
        }
        plan["stores"].append(store_entry)

    plan["summary"] = {
        "total_stores": len(stores_data),
        "total_visits": sum(s["total_visits"] for s in plan["stores"]),
        "deep_inspections": sum(1 for s in plan["stores"] for v in s["schedule"] if v["type"] == "深度巡店"),
        "regular_inspections": sum(1 for s in plan["stores"] for v in s["schedule"] if v["type"] == "常规巡店"),
    }

    # 保存
    plan_file = DATA_DIR / f"plan_{today.strftime('%Y%m')}.json"
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    # 输出文本摘要
    print("\n" + "=" * 60)
    print("  ✅ 巡店计划已生成")
    print("=" * 60)
    print(f"\n📊 计划概览：")
    print(f"   门店总数：{plan['summary']['total_stores']}家")
    print(f"   月巡店次数：{plan['summary']['total_visits']}次")
    print(f"   其中深度巡店：{plan['summary']['deep_inspections']}次")
    print(f"   常规巡店：{plan['summary']['regular_inspections']}次")

    print(f"\n📅 门店排期：")
    print(f"   {'门店':<10} {'级别':<5} {'月巡次数':<8} {'深度巡店'}")
    print(f"   {'-'*45}")
    for s in plan["stores"]:
        deep_count = sum(1 for v in s["schedule"] if v["type"] == "深度巡店")
        print(f"   {s['name']:<10} {s['importance']:<5} {s['total_visits']:<8} {deep_count}次")

    print(f"\n💾 已保存到：{plan_file}")
    print(f"\n💡 下一步：执行巡店 → python scripts/store_inspection.py --mode execute")
    return plan


def execute_inspection(store_name=None):
    """执行巡店检查评分"""
    if store_name is None:
        store_name = input("\n请输入巡店门店名称：").strip()

    print("\n" + "=" * 60)
    print(f"  🔍 正在巡店：{store_name}")
    print("=" * 60)
    print("\n逐项检查评分：✅ 通过(100分) / ⚠️ 部分通过(60分) / ❌ 不通过(0分)")
    print("输入 q 跳过剩余项目\n")

    result = {
        "store_name": store_name,
        "inspection_date": datetime.datetime.now().isoformat(),
        "inspector": os.environ.get("USER", "督导"),
        "dimensions": [],
        "total_score": 0,
        "grade": "",
        "issues": []
    }

    for dim in INSPECTION_DIMENSIONS:
        print(f"\n{'─' * 50}")
        print(f"📌 {dim['name']}（权重 {int(dim['weight']*100)}%）")
        print(f"{'─' * 50}")

        dim_score = 0
        dim_items = []

        for item in dim["items"]:
            print(f"\n  [{item['id']}] {item['name']}")
            print(f"  💡 {item['tips']}")

            while True:
                choice = input("  评分 (✅/⚠️/❌) [默认✅]：").strip().lower()
                if choice in ["", "y", "✅", "yes", "1", "pass"]:
                    score = 100
                    status = "pass"
                    break
                elif choice in ["⚠", "⚠️", "w", "warn", "partial", "0.6"]:
                    score = 60
                    status = "partial"
                    break
                elif choice in ["❌", "x", "n", "no", "fail", "0"]:
                    score = 0
                    status = "fail"
                    break
                elif choice == "q":
                    break
                else:
                    print("  请输 ✅/⚠️/❌ 或 q 跳过")

            if choice == "q":
                break

            item_result = {
                "item_id": item["id"],
                "item_name": item["name"],
                "score": score,
                "status": status
            }

            if status != "pass":
                issue_desc = input("  问题描述（可选）：").strip()
                if issue_desc:
                    item_result["issue"] = issue_desc
                action = input("  整改要求（可选）：").strip()
                if action:
                    item_result["action"] = action
                    result["issues"].append({
                        "dimension": dim["name"],
                        "item": item["name"],
                        "description": issue_desc,
                        "action": action,
                        "severity": "P0" if status == "fail" else "P1"
                    })

            dim_items.append(item_result)
            dim_score += score

        if dim_items:
            avg_score = dim_score / len(dim_items)
        else:
            avg_score = 0

        dim_result = {
            "dimension_id": dim["id"],
            "dimension_name": dim["name"],
            "weight": dim["weight"],
            "items": dim_items,
            "raw_score": round(avg_score, 1),
            "weighted_score": round(avg_score * dim["weight"], 1)
        }
        result["dimensions"].append(dim_result)
        print(f"\n  📊 {dim['name']}得分：{avg_score:.1f}/100（加权 {avg_score * dim['weight']:.1f}）")

    # 计算总分
    total = sum(d["weighted_score"] for d in result["dimensions"])
    result["total_score"] = round(total, 1)

    if total >= 90:
        result["grade"] = "A级 - 优秀"
    elif total >= 80:
        result["grade"] = "B级 - 良好"
    elif total >= 70:
        result["grade"] = "C级 - 一般"
    elif total >= 60:
        result["grade"] = "D级 - 待改进"
    else:
        result["grade"] = "E级 - 不合格"

    # 保存
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"inspection_{store_name}_{date_str}.json"
    filepath = DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 输出摘要
    print("\n" + "=" * 60)
    print(f"  🏆 巡店完成 - {store_name}")
    print("=" * 60)
    print(f"\n  加权总分：{total:.1f}/100")
    print(f"  评级：{result['grade']}")
    print(f"\n  各维度得分：")
    for d in result["dimensions"]:
        bar = "█" * int(d["weighted_score"] / 5) + "░" * (20 - int(d["weighted_score"] / 5))
        print(f"  {d['dimension_name']:<8} {bar} {d['weighted_score']:.1f}")

    print(f"\n  ⚠️ 待整改问题：{len(result['issues'])}项")
    for i, issue in enumerate(result["issues"], 1):
        print(f"  {i}. [{issue['severity']}] {issue['dimension']} - {issue['item']}")
        print(f"     → {issue['action']}")

    print(f"\n💾 结果已保存：{filepath}")
    return result


def generate_marketing_plan(store_name=None):
    """生成巡店营销改善方案"""
    # 尝试加载最近的巡店数据
    if store_name:
        files = sorted(DATA_DIR.glob(f"inspection_{store_name}_*.json"), reverse=True)
    else:
        files = sorted(DATA_DIR.glob("inspection_*.json"), reverse=True)
        if files:
            store_name = files[0].stem.split("_")[1]
        else:
            print("⚠️ 未找到巡店数据，请先执行巡店")
            return None

    if not files:
        print("⚠️ 未找到该门店的巡店数据")
        return None

    with open(files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    total = data["total_score"]
    dims = {d["dimension_id"]: d for d in data["dimensions"]}

    # 诊断营销相关维度
    marketing_dims = ["merchandising", "marketing_exec", "appearance", "experience", "service"]
    weak_dims = []
    for dim_id in marketing_dims:
        if dim_id in dims and dims[dim_id]["raw_score"] < 75:
            weak_dims.append(dims[dim_id])

    weak_items = []
    for d in data["dimensions"]:
        for item in d["items"]:
            if item["status"] != "pass" and d["dimension_id"] in marketing_dims:
                weak_items.append({**item, "dimension": d["dimension_name"]})

    plan = {
        "store_name": store_name,
        "generated_at": datetime.datetime.now().isoformat(),
        "based_on": files[0].name,
        "current_score": total,
        "diagnosis": [],
        "action_plan": [],
    }

    # 诊断问题
    diagnosis_map = {
        "merchandising": "商品陈列吸引力不足，影响顾客进店率和停留时长",
        "marketing_exec": "营销活动执行不到位，促销效果打折扣",
        "appearance": "店面形象待改善，第一印象影响进店率",
        "experience": "客户体验有短板，可能影响复购率和口碑",
        "service": "员工服务有待提升，直接影响转化率和客单价",
    }

    for d in weak_dims:
        plan["diagnosis"].append({
            "dimension": d["dimension_name"],
            "score": d["raw_score"],
            "analysis": diagnosis_map.get(d["dimension_id"], "需要关注改善"),
            "weak_items": [
                item["item_name"] for item in d["items"] if item["status"] != "pass"
            ]
        })

    # 生成行动方案
    action_templates = {
        "merchandising": [
            {"action": "重新规划黄金视线位陈列", "detail": "将主推品/高毛利品调整到视线高度(1.2-1.6m)，增加陈列面数量", "priority": "P0", "timeline": "3天内"},
            {"action": "建立每日陈列检查制度", "detail": "开店前由值班主管完成陈列面检查并拍照上传", "priority": "P1", "timeline": "即日执行"},
            {"action": "优化促销端架设计", "detail": "按\"引流品+利润品+清仓品\"三区设计端架，每周更换主题", "priority": "P1", "timeline": "1周内"},
        ],
        "marketing_exec": [
            {"action": "制定促销活动执行SOP", "detail": "包含物料清单/摆放位置图/话术模板/执行检查表", "priority": "P0", "timeline": "1周内"},
            {"action": "设立营销执行KPI", "detail": "活动物料到位率/员工话术掌握率/会员拉新完成率三项指标", "priority": "P0", "timeline": "即日执行"},
            {"action": "建立活动效果复盘机制", "detail": "每次活动结束后3天内完成数据复盘，输出改善建议", "priority": "P1", "timeline": "1周内"},
        ],
        "appearance": [
            {"action": "门头/橱窗季度焕新计划", "detail": "每季度更新橱窗主题，重大节日/活动前更新门头装饰", "priority": "P0", "timeline": "本季度"},
            {"action": "灯光系统维护制度", "detail": "每月检查一次全部灯具，损坏48小时内更换", "priority": "P1", "timeline": "即日执行"},
            {"action": "5S门口区域管理", "detail": "每日开门前完成门口区域清扫+检查，设责任人和检查表", "priority": "P1", "timeline": "即日执行"},
        ],
        "experience": [
            {"action": "优化店内动线设计", "detail": "确保主通道≥1.2m，设置清晰的品类导视牌", "priority": "P0", "timeline": "2周内"},
            {"action": "推广\"3分钟承诺\"", "detail": "收银排队超过3人时，承诺3分钟内增开收银台", "priority": "P1", "timeline": "即日执行"},
            {"action": "建立投诉快速响应机制", "detail": "店长/值班经理30分钟内到场处理，24小时内闭环反馈", "priority": "P1", "timeline": "即日执行"},
        ],
        "service": [
            {"action": "开展服务标准培训", "detail": "迎宾四步法/产品推荐FABE话术/投诉处理五步法", "priority": "P0", "timeline": "2周内"},
            {"action": "设立\"服务之星\"激励", "detail": "每周评选最佳服务员工，给予现金/积分奖励", "priority": "P1", "timeline": "即日执行"},
            {"action": "建立神秘顾客暗访机制", "detail": "每月1-2次暗访，结果纳入门店绩效考核", "priority": "P1", "timeline": "1个月内"},
        ],
    }

    for d in weak_dims:
        dim_id = d["dimension_id"]
        if dim_id in action_templates:
            plan["action_plan"].extend([
                {**t, "target_dimension": d["dimension_name"]}
                for t in action_templates[dim_id]
            ])

    # 通用营销提振措施
    plan["action_plan"].extend([
        {"action": "启动\"老客带新客\"裂变活动", "detail": "老会员带新会员注册消费，双方各得优惠券", "priority": "P0", "timeline": "2周内", "target_dimension": "整体提振"},
        {"action": "优化会员日/会员价体系", "detail": "每月设置会员专属日，提供额外折扣或积分翻倍", "priority": "P1", "timeline": "1个月内", "target_dimension": "整体提振"},
        {"action": "社群+公众号联动运营", "detail": "建立门店专属微信群，配合公众号推送活动/新品/福利", "priority": "P1", "timeline": "2周内", "target_dimension": "整体提振"},
    ])

    # 保存方案
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = DATA_DIR / f"marketing_plan_{store_name}_{date_str}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    # 输出
    print("\n" + "=" * 60)
    print(f"  📈 巡店营销改善方案 - {store_name}")
    print("=" * 60)

    print(f"\n📊 当前巡店总分：{total:.1f}/100")
    print(f"\n🔍 营销薄弱诊断：")
    for d in plan["diagnosis"]:
        print(f"  ⚠️ {d['dimension']}（{d['score']:.0f}分）- {d['analysis']}")
        for item in d["weak_items"]:
            print(f"     · {item}")

    print(f"\n🎯 改善行动计划（共{len(plan['action_plan'])}项）：")
    p0_items = [a for a in plan["action_plan"] if a["priority"] == "P0"]
    p1_items = [a for a in plan["action_plan"] if a["priority"] == "P1"]

    print(f"\n  🔴 P0 紧急（{len(p0_items)}项）：")
    for i, a in enumerate(p0_items, 1):
        print(f"  {i}. [{a['target_dimension']}] {a['action']}（{a['timeline']}）")
        print(f"     → {a['detail']}")

    print(f"\n  🟡 P1 重要（{len(p1_items)}项）：")
    for i, a in enumerate(p1_items, 1):
        print(f"  {i}. [{a['target_dimension']}] {a['action']}（{a['timeline']}）")
        print(f"     → {a['detail']}")

    print(f"\n💾 方案已保存：{filepath}")
    return plan


def analyze_data(store_filter=None):
    """分析巡店数据并生成HTML报告"""
    # 加载所有巡店数据
    all_files = sorted(DATA_DIR.glob("inspection_*.json"))
    if not all_files:
        print("⚠️ 未找到巡店数据，请先执行巡店检查")
        return None

    inspections = []
    for f in all_files:
        with open(f, "r", encoding="utf-8") as fp:
            inspections.append(json.load(fp))

    # 按门店分组
    store_groups = defaultdict(list)
    for insp in inspections:
        store_groups[insp["store_name"]].append(insp)

    # 计算统计数据
    store_stats = {}
    for store, records in store_groups.items():
        scores = [r["total_score"] for r in records]
        dim_scores = defaultdict(list)
        for r in records:
            for d in r["dimensions"]:
                dim_scores[d["dimension_name"]].append(d["weighted_score"])

        store_stats[store] = {
            "count": len(records),
            "avg_score": round(sum(scores) / len(scores), 1),
            "max_score": max(scores),
            "min_score": min(scores),
            "latest_score": records[-1]["total_score"],
            "trend": "up" if len(scores) >= 2 and scores[-1] > scores[-2] else ("down" if len(scores) >= 2 and scores[-1] < scores[-2] else "stable"),
            "dim_scores": {k: round(sum(v)/len(v), 1) for k, v in dim_scores.items()},
        }

    # 问题统计
    all_issues = []
    issue_counter = Counter()
    for insp in inspections:
        for issue in insp.get("issues", []):
            all_issues.append(issue)
            issue_counter[f"{issue['dimension']}-{issue['item']}"] += 1

    top_issues = issue_counter.most_common(10)

    # 全部门店平均各维度得分
    all_dim_avgs = defaultdict(list)
    for stats in store_stats.values():
        for dim, score in stats["dim_scores"].items():
            all_dim_avgs[dim].append(score)
    dim_avgs = {k: round(sum(v)/len(v), 1) for k, v in all_dim_avgs.items()}

    # 生成HTML报告
    html = generate_html_report(store_stats, inspections, top_issues, dim_avgs, all_issues)

    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUT_DIR / f"inspection_report_{date_str}.html"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ 数据分析报告已生成：{filepath}")
    return str(filepath)


def generate_html_report(store_stats, inspections, top_issues, dim_avgs, all_issues):
    """生成交互式HTML分析报告"""
    stores_json = json.dumps(list(store_stats.keys()), ensure_ascii=False)
    scores_json = json.dumps([s["latest_score"] for s in store_stats.values()], ensure_ascii=False)
    grades_json = json.dumps([
        "A" if s["latest_score"] >= 90 else "B" if s["latest_score"] >= 80
        else "C" if s["latest_score"] >= 70 else "D" if s["latest_score"] >= 60 else "E"
        for s in store_stats.values()
    ], ensure_ascii=False)

    # 雷达图数据
    dim_names = list(dim_avgs.keys())
    dim_values = list(dim_avgs.values())

    # 问题分布
    issue_labels = [f"{i[0][:30]}" for i in top_issues]
    issue_values = [i[1] for i in top_issues]

    # 门店详情
    store_cards = ""
    for name, stats in store_stats.items():
        grade = "A" if stats["latest_score"] >= 90 else "B" if stats["latest_score"] >= 80 \
                else "C" if stats["latest_score"] >= 70 else "D" if stats["latest_score"] >= 60 else "E"
        grade_color = "#22c55e" if grade in "AB" else "#eab308" if grade == "C" else "#ef4444"
        trend_icon = "📈" if stats["trend"] == "up" else "📉" if stats["trend"] == "down" else "➡️"
        store_cards += f"""
        <div class="store-card">
            <div class="store-header">
                <span class="store-name">{name}</span>
                <span class="store-grade" style="background:{grade_color}">{grade}级</span>
            </div>
            <div class="store-score">{stats['latest_score']}<span>/100</span></div>
            <div class="store-meta">
                <span>巡检{stats['count']}次</span>
                <span>最高{stats['max_score']}</span>
                <span>{trend_icon}趋势</span>
            </div>
        </div>"""

    # 最近一次巡店详情
    latest = inspections[-1] if inspections else None
    dim_bars = ""
    if latest:
        for d in latest["dimensions"]:
            color = "#22c55e" if d["raw_score"] >= 90 else "#eab308" if d["raw_score"] >= 70 else "#ef4444"
            width = max(d["weighted_score"] / 10 * 100, 2)
            dim_bars += f"""
            <div class="dim-bar-row">
                <span class="dim-label">{d['dimension_name']}</span>
                <div class="dim-bar-track">
                    <div class="dim-bar-fill" style="width:{width}%;background:{color}"></div>
                </div>
                <span class="dim-score">{d['weighted_score']:.1f}</span>
            </div>"""

    # 整改项
    issue_rows = ""
    for issue in all_issues[-15:]:
        sev_color = "#ef4444" if issue.get("severity") == "P0" else "#eab308"
        issue_rows += f"""
        <tr>
            <td><span class="sev-badge" style="background:{sev_color}">{issue.get('severity','P1')}</span></td>
            <td>{issue.get('dimension','')}</td>
            <td>{issue.get('item','')}</td>
            <td>{issue.get('action','')}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>巡店数据分析报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background:#f5f7fa; color:#1a1a2e; }}
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:#fff; padding:30px 40px; }}
.header h1 {{ font-size:28px; margin-bottom:8px; }}
.header p {{ opacity:0.9; font-size:14px; }}
.container {{ max-width:1200px; margin:0 auto; padding:30px 20px; }}
.section {{ background:#fff; border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 2px 12px rgba(0,0,0,0.06); }}
.section h2 {{ font-size:20px; margin-bottom:16px; color:#333; border-bottom:2px solid #667eea; padding-bottom:8px; display:inline-block; }}
.summary-cards {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:24px; }}
.summary-card {{ background:#fff; border-radius:12px; padding:20px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.05); }}
.summary-card .value {{ font-size:36px; font-weight:bold; color:#667eea; }}
.summary-card .label {{ font-size:13px; color:#888; margin-top:6px; }}
.store-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:16px; }}
.store-card {{ background:#f8f9fc; border-radius:10px; padding:18px; text-align:center; transition:transform 0.2s; }}
.store-card:hover {{ transform:translateY(-2px); box-shadow:0 4px 16px rgba(0,0,0,0.1); }}
.store-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }}
.store-name {{ font-weight:600; }}
.store-grade {{ color:#fff; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:600; }}
.store-score {{ font-size:40px; font-weight:bold; color:#1a1a2e; }}
.store-score span {{ font-size:16px; color:#999; }}
.store-meta {{ color:#888; font-size:12px; margin-top:8px; display:flex; justify-content:space-around; }}
.charts-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
@media (max-width:768px) {{ .charts-grid{{grid-template-columns:1fr;}} .summary-cards{{grid-template-columns:repeat(2,1fr);}} }}
.chart-box {{ background:#fff; border-radius:10px; padding:16px; box-shadow:0 1px 6px rgba(0,0,0,0.05); }}
.chart-box h3 {{ font-size:15px; margin-bottom:12px; color:#555; }}
.dim-bar-row {{ display:flex; align-items:center; gap:10px; margin:8px 0; }}
.dim-label {{ width:80px; font-size:13px; text-align:right; color:#555; flex-shrink:0; }}
.dim-bar-track {{ flex:1; background:#eee; border-radius:8px; height:18px; overflow:hidden; }}
.dim-bar-fill {{ height:100%; border-radius:8px; transition:width 0.5s; }}
.dim-score {{ width:40px; font-size:13px; font-weight:600; color:#333; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
th {{ background:#f0f2f5; padding:10px 12px; text-align:left; font-weight:600; color:#555; }}
td {{ padding:10px 12px; border-bottom:1px solid #f0f0f0; }}
.sev-badge {{ color:#fff; padding:1px 8px; border-radius:10px; font-size:11px; font-weight:600; }}
.footer {{ text-align:center; color:#999; font-size:12px; padding:30px; }}
</style>
</head>
<body>
<div class="header">
    <h1>📊 巡店数据分析报告</h1>
    <p>生成时间：{datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")} | 覆盖{len(store_stats)}家门店 | 共{len(inspections)}次巡检记录</p>
</div>

<div class="container">
    <!-- 总览 -->
    <div class="summary-cards">
        <div class="summary-card">
            <div class="value">{len(store_stats)}</div>
            <div class="label">覆盖门店数</div>
        </div>
        <div class="summary-card">
            <div class="value">{len(inspections)}</div>
            <div class="label">巡店次数</div>
        </div>
        <div class="summary-card">
            <div class="value">{round(sum(s['latest_score'] for s in store_stats.values())/len(store_stats), 1)}</div>
            <div class="label">平均得分</div>
        </div>
        <div class="summary-card">
            <div class="value">{len(all_issues)}</div>
            <div class="label">待整改问题</div>
        </div>
    </div>

    <!-- 门店得分卡 -->
    <div class="section">
        <h2>🏪 门店评分概览</h2>
        <div class="store-grid">{store_cards}</div>
    </div>

    <!-- 图表区 -->
    <div class="charts-grid">
        <div class="chart-box">
            <h3>🎯 各维度平均得分（雷达图）</h3>
            <canvas id="radarChart" height="280"></canvas>
        </div>
        <div class="chart-box">
            <h3>📊 门店最新得分对比</h3>
            <canvas id="barChart" height="280"></canvas>
        </div>
        <div class="chart-box">
            <h3>⚠️ 高频问题 TOP10</h3>
            <canvas id="issueChart" height="280"></canvas>
        </div>
        <div class="chart-box">
            <h3>📈 最近巡检得分详情</h3>
            {dim_bars}
            <p style="color:#888;font-size:12px;margin-top:12px;text-align:center;">
                {latest['store_name'] if latest else ''} - {latest['inspection_date'][:10] if latest else ''} | 总分 {latest['total_score'] if latest else 0}/100 | {latest['grade'] if latest else ''}
            </p>
        </div>
    </div>

    <!-- 整改跟踪 -->
    <div class="section">
        <h2>🔧 整改跟踪清单</h2>
        <table>
            <thead>
                <tr><th>级别</th><th>维度</th><th>问题项</th><th>整改要求</th></tr>
            </thead>
            <tbody>{issue_rows}</tbody>
        </table>
    </div>
</div>

<div class="footer">
    巡店管理全流程助手 · 自动生成报告 · {datetime.datetime.now().strftime("%Y-%m-%d")}
</div>

<script>
// 雷达图
new Chart(document.getElementById('radarChart'), {{
    type: 'radar',
    data: {{
        labels: {json.dumps(dim_names, ensure_ascii=False)},
        datasets: [{{
            label: '各维度平均得分',
            data: {json.dumps(dim_values)},
            backgroundColor: 'rgba(102,126,234,0.2)',
            borderColor: '#667eea',
            borderWidth: 2,
            pointBackgroundColor: '#667eea',
        }}]
    }},
    options: {{
        scales: {{ r: {{ beginAtZero: true, max: 10, ticks: {{ stepSize: 2 }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});

// 柱状图
new Chart(document.getElementById('barChart'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps(list(store_stats.keys()), ensure_ascii=False)},
        datasets: [{{
            label: '最新得分',
            data: {json.dumps([s['latest_score'] for s in store_stats.values()])},
            backgroundColor: {json.dumps([
                '#22c55e' if s['latest_score'] >= 90 else '#eab308' if s['latest_score'] >= 70 else '#ef4444'
                for s in store_stats.values()
            ])},
            borderRadius: 6,
        }}]
    }},
    options: {{
        scales: {{ y: {{ beginAtZero: true, max: 100 }}}},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});

// 水平柱状图
new Chart(document.getElementById('issueChart'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps(issue_labels, ensure_ascii=False)},
        datasets: [{{
            label: '出现次数',
            data: {json.dumps(issue_values)},
            backgroundColor: '#ef4444',
            borderRadius: 4,
        }}]
    }},
    options: {{
        indexAxis: 'y',
        scales: {{ x: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});
</script>
</body>
</html>"""

    return html


def generate_demo_data():
    """生成演示数据并输出完整报告"""
    store_names = ["旗舰店", "万达店", "社区店A", "社区店B", "校园店"]
    store_types = ["旗舰店", "商场店", "社区店", "社区店", "校园店"]
    locations = ["市中心", "万达广场", "城东", "城西", "大学城"]
    importances = ["A", "A", "B", "B", "C"]

    # 清除旧demo数据
    for f in DATA_DIR.glob("inspection_demo_*.json"):
        f.unlink()
    for f in DATA_DIR.glob("plan_demo*.json"):
        f.unlink()

    # 每条门店生成3轮巡店数据（模拟3个月趋势）
    for store_idx, (name, stype, loc, imp) in enumerate(zip(store_names, store_types, locations, importances)):
        base_score = {"A": 88, "B": 78, "C": 72}[imp]
        for month in range(1, 4):
            # 模拟得分波动和改进趋势
            trend_factor = 2 * month - 2  # 每月提升2分
            noise = random.randint(-3, 3)
            total = min(100, base_score + trend_factor + noise)

            dims = []
            all_issues = []
            for dim in INSPECTION_DIMENSIONS:
                # 每个维度模拟得分
                dim_base = random.randint(60, 100)
                dim_score = min(100, dim_base + trend_factor // 3 + random.randint(-5, 5))
                items = []
                for item in dim["items"]:
                    if random.random() < 0.85:
                        item_score = random.randint(90, 100)
                        status = "pass"
                    elif random.random() < 0.5:
                        item_score = 60
                        status = "partial"
                    else:
                        item_score = 0
                        status = "fail"
                    item_result = {
                        "item_id": item["id"],
                        "item_name": item["name"],
                        "score": item_score,
                        "status": status
                    }
                    if status != "pass":
                        sev = "P0" if status == "fail" else "P1"
                        issue_desc = f"需要关注：{item['name'][:20]}"
                        action = random.choice([
                            "安排专项培训", "制定整改计划3天内完成", "列为周重点检查项",
                            "通知店长48小时内整改", "纳入下月绩效考核", "安排供应商维修"
                        ])
                        item_result["issue"] = issue_desc
                        item_result["action"] = action
                        all_issues.append({
                            "dimension": dim["name"],
                            "item": item["name"],
                            "description": issue_desc,
                            "action": action,
                            "severity": sev
                        })
                    items.append(item_result)

                avg = sum(i["score"] for i in items) / len(items) if items else 0
                dims.append({
                    "dimension_id": dim["id"],
                    "dimension_name": dim["name"],
                    "weight": dim["weight"],
                    "items": items,
                    "raw_score": round(avg, 1),
                    "weighted_score": round(avg * dim["weight"], 1)
                })

            weighted_total = sum(d["weighted_score"] for d in dims)
            grade = "A级" if weighted_total >= 90 else "B级" if weighted_total >= 80 \
                    else "C级" if weighted_total >= 70 else "D级" if weighted_total >= 60 else "E级"

            result = {
                "store_name": name,
                "inspection_date": f"2026-0{month}-{15+random.randint(0,10):02d}T{8+random.randint(0,10):02d}:00:00",
                "inspector": "张督导",
                "dimensions": dims,
                "total_score": round(weighted_total, 1),
                "grade": grade,
                "issues": all_issues[:random.randint(2, 6)]
            }

            with open(DATA_DIR / f"inspection_demo_{name}_m{month}.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

    return analyze_data()


def main():
    parser = argparse.ArgumentParser(description="巡店管理全流程助手")
    parser.add_argument("--mode", choices=["plan", "execute", "marketing", "analyze", "demo"],
                        default="demo", help="运行模式")
    parser.add_argument("--store", type=str, help="指定门店名称")
    parser.add_argument("--data", type=str, help="指定数据文件或目录")
    args = parser.parse_args()

    if args.mode == "demo":
        print("\n" + "=" * 60)
        print("  🏪 巡店管理全流程助手 v1.0 - 演示模式")
        print("=" * 60)
        print("\n正在生成5家门店×3个月模拟巡检数据...\n")
        report_path = generate_demo_data()
        if report_path:
            # 同时输出文本摘要
            print("\n可用模式：")
            print("  demo       - 生成演示数据+完整报告（当前）")
            print("  plan       - 制定巡店计划")
            print("  execute    - 执行巡店检查评分")
            print("  marketing  - 生成营销改善方案")
            print("  analyze    - 数据分析与报告")

    elif args.mode == "plan":
        generate_plan()

    elif args.mode == "execute":
        execute_inspection(args.store)

    elif args.mode == "marketing":
        generate_marketing_plan(args.store)

    elif args.mode == "analyze":
        analyze_data(args.store)


if __name__ == "__main__":
    main()
