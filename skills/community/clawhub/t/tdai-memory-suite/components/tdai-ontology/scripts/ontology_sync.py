#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ontology 自动灌入脚本 — 从记忆文件提取实体并更新知识图谱
由 Cron 定时任务调用，或 Agent 手动触发。

用法：
    python scripts/ontology_sync.py          # 全量同步（近7天）
    python scripts/ontology_sync.py --days 3  # 只同步近3天
    python scripts/ontology_sync.py --dry-run # 预览不执行
    python scripts/ontology_sync.py --status  # 查看当前图谱状态
"""

import sys
import io
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import OrderedDict

# ==================== 配置 ====================
WORKSPACE = Path(__file__).resolve().parent.parent
GRAPH_PATH = WORKSPACE / "memory" / "ontology" / "graph.jsonl"
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = WORKSPACE / "memory"  # 报告也在 memory 目录下

# 实体 ID 生成
_id_counter = {}

def gen_id(prefix):
    """生成确定性 ID（同名同 ID）"""
    if prefix not in _id_counter:
        _id_counter[prefix] = 1
    else:
        _id_counter[prefix] += 1
    return f"{prefix}_{_id_counter[prefix]:03d}"

# ==================== 加载现有图谱 ====================

def load_existing_graph():
    """加载已有的 entity ID 映射，避免重复创建"""
    entities = {}
    relations = []
    if not GRAPH_PATH.exists():
        return entities, relations
    with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            op = record.get("op")
            if op == "create":
                e = record["entity"]
                entities[e["id"]] = e
            elif op == "update":
                eid = record["id"]
                if eid in entities:
                    entities[eid]["properties"].update(record.get("properties", {}))
            elif op == "delete":
                entities.pop(record["id"], None)
            elif op == "relate":
                relations.append(record)
    return entities, relations

def find_entity_by_type_name(entities, type_name, name):
    """按类型+名称查找已有实体"""
    for eid, e in entities.items():
        if e["type"] == type_name and e["properties"].get("name") == name:
            return eid
    return None

def find_entity_by_type_prop(entities, type_name, prop_key, prop_val):
    """按类型+属性查找已有实体"""
    for eid, e in entities.items():
        if e["type"] == type_name and e["properties"].get(prop_key) == prop_val:
            return eid
    return None

# ==================== 实体写入 ====================

pending_ops = []

def op_create(type_name, entity_id, properties):
    ts = datetime.utcnow().isoformat()
    entity = {
        "id": entity_id,
        "type": type_name,
        "properties": properties,
        "created": ts,
        "updated": ts
    }
    pending_ops.append({"op": "create", "entity": entity, "timestamp": ts})

def op_update(entity_id, properties):
    ts = datetime.utcnow().isoformat()
    pending_ops.append({"op": "update", "id": entity_id, "properties": properties, "timestamp": ts})

def op_relate(from_id, rel, to_id):
    ts = datetime.utcnow().isoformat()
    pending_ops.append({"op": "relate", "from": from_id, "rel": rel, "to": to_id, "properties": {}, "timestamp": ts})

def flush_ops():
    """写入所有待处理操作"""
    if not pending_ops:
        print("  ⏭️  无新操作，跳过写入")
        return
    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_PATH, 'a', encoding='utf-8') as f:
        for op in pending_ops:
            f.write(json.dumps(op, ensure_ascii=False) + "\n")
    print(f"  ✅ 已写入 {len(pending_ops)} 条操作到图谱")

# ==================== 记忆解析 ====================

def parse_daily_notes(days=7):
    """从 memory/YYYY-MM-DD.md 提取实体（严格过滤，只取真正的项目/事件）"""
    results = {
        "projects": [],
        "people": [],
        "orgs": [],
        "skills": [],
        "techs": [],
        "events": [],
        "decisions": [],
    }
    cutoff = datetime.now() - timedelta(days=days)
    
    if not MEMORY_DIR.exists():
        return results
    
    # 跳过的文件类型
    skip_prefixes = ("report_", "daily_news_", "tech_trend_", "quality_blueprint", "memory_tdai_check")
    
    for fname in sorted(MEMORY_DIR.glob("*.md")):
        if fname.name in skip_prefixes or fname.name.endswith("行业深度分析报告.md"):
            continue
        if any(fname.name.startswith(p) for p in skip_prefixes):
            continue
        # 只匹配 YYYY-MM-DD.md
        m = re.match(r'(\d{4}-\d{2}-\d{2})\.md$', fname.name)
        if not m:
            continue
        date_str = m.group(1)
        try:
            fdate = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if fdate < cutoff:
            continue
        
        try:
            content = fname.read_text(encoding='utf-8-sig', errors='ignore')
        except:
            continue
        
        # 严格提取项目名：只取 ## 级别标题中明确是项目的
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('##'):
                name = re.sub(r'^#+\s*', '', line).strip()
                # 跳过各种非项目标题
                skip_patterns = [
                    r'^Tags[:\s]', r'^Confidence', r'^(persona|episodic|instruction)\s*[-:]',
                    r'目录', r'概览', r'核心', r'总结', r'建议', r'风险', r'差距',
                    r'路线图', r'附录', r'对比', r'结论', r'状态', r'修复方案',
                    r'备份位置', r'长期方案', r'更新文件', r'修复动作',
                    r'费用执行', r'任务来源', r'根因', r'教训', r'重要教训',
                    r'违规教训', r'重要行为规则', r'规则', r'心跳检查',
                    r'定时任务', r'Git代码', r'后台任务', r'异常记录',
                    r'定时任务管理', r'网站结构', r'机电系统', r'费用执行',
                    r'集合竞价', r'安装过程', r'最终成功路径', r'失败路径',
                    r'正确端点', r'评审意见结构', r'评审权重', r'安装的技能',
                    r'四大', r'技术要点', r'空间记忆', r'邮件中文', r'升级尝试',
                    r'发布.*技能', r'技术报告', r'技能更新',
                ]
                if any(re.search(p, name, re.IGNORECASE) for p in skip_patterns):
                    continue
                if len(name) > 4 and len(name) < 60:
                    results["projects"].append({"name": name, "source": f"{date_str}: {fname.name}"})
    
    return results

def parse_reports():
    """从分析报告提取实体和项目"""
    results = {
        "projects": [],
        "techs": [],
        "companies": [],
        "relations": []
    }
    
    # 分析6大维度报告
    report_files = [
        "report_自动化检测.md",
        "report_视觉检测.md",
        "report_新技术探索.md",
        "report_抽空灌注.md",
        "report_自研自制.md",
        "report_品质数字化.md",
    ]
    
    for fname in report_files:
        fpath = MEMORY_DIR / fname
        if not fpath.exists():
            continue
        try:
            content = fpath.read_text(encoding='utf-8-sig', errors='ignore')
        except:
            continue
        
        # 提取企业名称（去重：同名只取一次）
        company_pattern = r'(美的|海尔|海信|格力|谛声科技|科大讯飞|深眸科技|海康机器人|凌云光|科陆电子|万福莱|SHINGCHEM|Platinum Overseas|巨化集团|科瑞自动化|FLIR|博众精工|赛腾股份|天准科技|卡莱特|夏普|美菱|奥马|卡奥斯|COSMOPlat)'
        seen_companies = set()
        for m in re.finditer(company_pattern, content):
            company = m.group(1)
            if company not in seen_companies:
                seen_companies.add(company)
                results["companies"].append({"name": company, "source": fname})
        
        # 提取技术名词
        tech_pattern = r'(深度学习|声纹检测|红外测温|氦质谱检漏|差压法检漏|AI视觉|3D视觉|M-BUS|Modbus TCP|OPC UA|MQTT|PXIe|CNAS|R600a|R290|VOC-VOP|Agent|知识图谱|RAG|工业听诊器|自动检漏|冷媒灌注|视觉检测|表面缺陷检测)'
        for m in re.finditer(tech_pattern, content):
            tech = m.group(1)
            if not any(t["name"] == tech for t in results["techs"]):
                results["techs"].append({"name": tech, "source": fname})
        
        # 提取项目（蓝图相关）
        project_patterns = [
            r'质量技术研究蓝图',
            r'商检(\d\.\d)体系',
            r'抽空灌注(\d\.\d)',
            r'Mbus商检系统',
            r'品质Agent',
            r'自动化检测线体',
            r'视觉检测系统',
            r'声纹检测系统',
            r'红外检测系统',
            r'制冰机检测设备',
        ]
        seen_projects = set()
        for pat in project_patterns:
            for m in re.finditer(pat, content):
                proj = m.group(0)
                if proj not in seen_projects:
                    seen_projects.add(proj)
                    results["projects"].append({"name": proj, "source": fname})
    
    return results

# ==================== 主同步流程 ====================

def sync(dry_run=False, days=7):
    print(f"{'[DRY RUN] ' if dry_run else ''}🔄 开始 Ontology 同步（近 {days} 天）")
    print(f"   图谱路径: {GRAPH_PATH}")
    print(f"   记忆目录: {MEMORY_DIR}")
    
    # 加载已有图谱
    entities, relations = load_existing_graph()
    print(f"   当前图谱: {len(entities)} 实体, {len(relations)} 关系")
    
    # 解析记忆文件
    daily = parse_daily_notes(days=days)
    reports = parse_reports()
    
    new_entities = 0
    new_relations = 0
    
    # ---- 1. 人 ----
    # Paudy（确保存在）
    paudy_id = find_entity_by_type_prop(entities, "Person", "name", "尹德斌")
    if not paudy_id:
        paudy_id = find_entity_by_type_prop(entities, "Person", "name", "Paudy")
    if not paudy_id:
        paudy_id = gen_id("person")
        op_create("Person", paudy_id, {"name": "尹德斌", "alias": "Paudy", "title": "智能制造研究院·智能装备所所长", "company": "美的集团"})
        new_entities += 1
    else:
        # 更新属性
        existing = entities[paudy_id]
        if "alias" not in existing["properties"]:
            op_update(paudy_id, {"alias": "Paudy"})
    
    # ---- 2. 组织 ----
    orgs = ["美的集团", "智能制造研究院", "智能装备所"]
    org_ids = {}
    for org_name in orgs:
        oid = find_entity_by_type_name(entities, "Organization", org_name)
        if not oid:
            oid = gen_id("org")
            props = {"name": org_name}
            if org_name == "智能制造研究院":
                props["type"] = "部门"
            elif org_name == "智能装备所":
                props["type"] = "子部门"
            op_create("Organization", oid, props)
            new_entities += 1
        org_ids[org_name] = oid
    
    # 关系
    def has_relation(rels, from_id, rel_type, to_id):
        return any(r.get("from") == from_id and r.get("rel") == rel_type and r.get("to") == to_id for r in rels)
    
    if not has_relation(relations, org_ids.get("智能装备所"), "sub_unit_of", org_ids.get("智能制造研究院")):
        op_relate(org_ids["智能装备所"], "sub_unit_of", org_ids["智能制造研究院"])
        new_relations += 1
    if not has_relation(relations, paudy_id, "works_at", org_ids.get("美的集团")):
        op_relate(paudy_id, "works_at", org_ids["美的集团"])
        new_relations += 1
    
    # ---- 3. 项目 ----
    # 从报告提取的项目
    all_projects = []
    for p in daily["projects"]:
        all_projects.append(p)
    for p in reports["projects"]:
        all_projects.append(p)
    
    # 去重
    seen_proj = set()
    for p in all_projects:
        name = p["name"]
        if name in seen_proj or len(name) < 4:
            continue
        # 也跳过已有实体
        if find_entity_by_type_name(entities, "Project", name):
            seen_proj.add(name)
            continue
        seen_proj.add(name)
        
        pid = gen_id("proj")
        props = {"name": name, "status": "active", "source": p["source"]}
        # 尝试识别领域
        if any(k in name for k in ["检测", "视觉", "声纹", "红外"]):
            props["domain"] = "工业检测"
        elif "抽空" in name or "灌注" in name:
            props["domain"] = "制冷工艺"
        elif "商检" in name or "Mbus" in name:
            props["domain"] = "质量检测"
        elif "Agent" in name or "数字化" in name or "品质" in name:
            props["domain"] = "数字化"
        op_create("Project", pid, props)
        new_entities += 1
        
        # 关联到 Paudy
        if not has_relation(relations, pid, "has_owner", paudy_id):
            op_relate(pid, "has_owner", paudy_id)
            new_relations += 1
    
    # ---- 4. 技术（去重） ----
    seen_tech = set()
    for t in reports["techs"]:
        name = t["name"]
        if name in seen_tech:
            continue
        if find_entity_by_type_name(entities, "Technology", name):
            seen_tech.add(name)
            continue
        seen_tech.add(name)
        tid = gen_id("tech")
        op_create("Technology", tid, {"name": name, "source": t["source"]})
        new_entities += 1
    
    # ---- 5. 公司/供应商（去重） ----
    seen_org = set()
    for c in reports["companies"]:
        name = c["name"]
        if name in seen_org:
            continue
        if find_entity_by_type_name(entities, "Organization", name):
            seen_org.add(name)
            continue
        seen_org.add(name)
        cid = gen_id("org")
        op_create("Organization", cid, {"name": name, "type": "供应商/合作伙伴", "source": c["source"]})
        new_entities += 1
    
    # ---- 6. Skill（从 workspace/skills/ 扫描）----
    skills_dir = WORKSPACE / "skills"
    if skills_dir.exists():
        seen_skills = set()
        for eid, e in entities.items():
            if e["type"] == "Skill":
                seen_skills.add(e["properties"].get("name", ""))
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            sk_name = skill_dir.name
            if sk_name in seen_skills:
                continue
            seen_skills.add(sk_name)
            sid = gen_id("skil")
            sk_meta = {"name": sk_name, "source": f"skills/{sk_name}/"}
            sk_meta_file = skill_dir / "_meta.json"
            if sk_meta_file.exists():
                try:
                    meta = json.loads(sk_meta_file.read_text(encoding='utf-8'))
                    sk_meta["version"] = meta.get("version", "unknown")
                except:
                    pass
            op_create("Skill", sid, sk_meta)
            new_entities += 1
    
    # 写入
    if not dry_run:
        flush_ops()
    else:
        print(f"  📋 待写入: {len(pending_ops)} 条操作")
        for op in pending_ops:
            print(f"     {op['op']}: {json.dumps(op, ensure_ascii=False)[:120]}")
    
    # 最终状态
    if not dry_run:
        final_entities, final_rels = load_existing_graph()
        print(f"   最终图谱: {len(final_entities)} 实体, {len(final_rels)} 关系")
    
    return {
        "new_entities": new_entities,
        "new_relations": new_relations,
        "total_entities": len(entities) + new_entities,
        "total_relations": len(relations) + new_relations,
    }

# ==================== 入口 ====================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ontology 自动灌入脚本")
    parser.add_argument("--dry-run", action="store_true", help="预览不执行")
    parser.add_argument("--days", type=int, default=7, help="同步近 N 天的日记")
    parser.add_argument("--status", action="store_true", help="查看图谱状态")
    args = parser.parse_args()
    
    if args.status:
        entities, relations = load_existing_graph()
        print(f"📊 Ontology 图谱状态:")
        print(f"   实体: {len(entities)}")
        print(f"   关系: {len(relations)}")
        types = {}
        for e in entities.values():
            t = e["type"]
            types[t] = types.get(t, 0) + 1
        print(f"   类型分布:")
        for t, c in sorted(types.items()):
            print(f"     {t}: {c}")
        # 检查 graph.jsonl 最后修改时间
        if GRAPH_PATH.exists():
            mtime = datetime.fromtimestamp(GRAPH_PATH.stat().st_mtime)
            print(f"   最后修改: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"   图谱文件不存在")
    else:
        result = sync(dry_run=args.dry_run, days=args.days)
        print(f"\n✅ 同步完成: +{result['new_entities']} 实体, +{result['new_relations']} 关系")
