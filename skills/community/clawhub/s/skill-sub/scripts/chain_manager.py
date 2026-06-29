#!/usr/bin/env python3
"""
chain_manager.py - Chain Manager OO Refactor v1.22.0
调用链管理核心脚本：创建、查询、更新、删除、执行调用链。

零外部依赖，仅使用 Python 标准库。
跨平台支持 Windows/Linux/macOS。
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-sub/data/"

SKILL_DIR = Path(__file__).resolve().parent.parent
# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "skill-sub" / "data"


# ============================================================
# 配置类
# ============================================================

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, chain_home):
        self.chain_home = chain_home
        self.config_file = chain_home / "config.json"
        self._config = None
    
    def load(self):
        """加载用户配置"""
        defaults_path = Path(__file__).resolve().parent / "default_config.json"
        defaults = {}
        if defaults_path.exists():
            defaults = json.loads(defaults_path.read_text(encoding="utf-8"))
        
        user_cfg = {}
        if self.config_file.exists():
            user_cfg = json.loads(self.config_file.read_text(encoding="utf-8"))
        
        defaults.update(user_cfg)
        self._config = defaults
        return defaults
    
    def get(self, key, fallback=None):
        """获取配置值"""
        if self._config is None:
            self.load()
        return self._config.get(key, fallback)
    
    def get_default_retry(self):
        """获取默认重试次数"""
        config = self.load()
        try:
            return max(1, int(config.get("default_max_retries", 3)))
        except (TypeError, ValueError):
            return 3

# ============================================================
# 路径管理类
# ============================================================

class PathManager:
    """路径管理器"""
    
    def __init__(self):
        self.chain_home = self._get_chain_home()
        self.chains_dir = self.chain_home / "chains"
        self.index_file = self.chains_dir / "index.json"
        self.blueprints_dir = self.chain_home / "blueprints"  # v1.29.0: 链私有蓝皮书目录
        self.config_file = self.chain_home / "config.json"
        self.skill_dir = Path(__file__).resolve().parent.parent
        self.state_dir = self.chain_home / "state"
        self.logs_dir = self.chain_home / "logs"
    
    def _get_chain_home(self):
        """获取调用链数据目录"""
        env_home = os.environ.get("SKILL_SUB_HOME") or os.environ.get("SKILL_CHAIN_HOME")
        if env_home:
            return Path(env_home)
        # 按照规定：skills/.standardization/<skill-name>/
        default = Path.home() / ".workbuddy" / "skills" / ".standardization" / "skill-sub"
        return default
    
    def get_skills_dir(self):
        """获取已安装技能目录"""
        env_dir = os.environ.get("WORKBUDDY_SKILLS_DIR")
        if env_dir:
            return Path(env_dir)
        return Path.home() / ".workbuddy" / "skills"
    
    def find_skill_path(self, skill_name):
        """查找技能实际目录"""
        skills_dir = self.get_skills_dir()
        if not skills_dir.exists():
            return None
        
        # 精确匹配
        exact = skills_dir / skill_name
        if exact.is_dir():
            return exact
        
        # 模糊匹配
        target = skill_name.lower().replace(" ", "-")
        for entry in skills_dir.iterdir():
            if entry.is_dir():
                if entry.name.lower().replace(" ", "-") == target or target in entry.name.lower():
                    return entry
        
        return None

# ============================================================
# 验证器类
# ============================================================

class ChainValidator:
    """调用链验证器"""
    
    # 里程碑关键词
    MILESTONE_KEYWORDS = [
        "审计", "安全", "部署", "发布", "上线", "打包",
        "测试", "验证", "校验", "审批", "审核",
        "付款", "支付", "下单", "提交", "推送",
        "导入", "导出", "迁移", "备份", "恢复",
        "audit", "deploy", "release", "publish", "push",
        "test", "verify", "validate", "approve", "review",
        "payment", "submit", "import", "export", "migrate",
        "backup", "restore", "build", "compile", "install",
    ]
    
    def __init__(self, path_manager):
        self.path_manager = path_manager
    
    def classify_milestones(self, steps):
        """基于结构特征的通用里程碑判断。
        
        规则优先级（从高到低）：
        1. 用户显式标记 is_milestone=true → 里程碑
        2. 用户显式标记 is_milestone=false → 非里程碑
        3. 总步骤数 <= 2 → 全部里程碑（链太短，每步都关键）
        4. 步骤名包含里程碑关键词 → 里程碑
        5. 被多个后续步骤依赖（瓶颈点，>=2个后续步骤依赖它）→ 里程碑
        6. 是最后一步 → 里程碑（最终交付物）
        7. 其余 → 非里程碑
        
        返回：list[dict] 每项包含 step_index, is_milestone, reason
        """
        n = len(steps)
        if n == 0:
            return []
        
        depended_by = {}
        for i, step in enumerate(steps):
            idx = step.get("index", i + 1)
            depended_by[idx] = set()
        
        for i, step in enumerate(steps):
            idx = step.get("index", i + 1)
            for dep in step.get("depends_on", []):
                if dep in depended_by:
                    depended_by[dep].add(idx)
        
        results = []
        for i, step in enumerate(steps):
            idx = step.get("index", i + 1)
            fm = step.get("failure_mode", {})
            
            if fm.get("is_milestone") is True:
                results.append({"step_index": idx, "is_milestone": True, "reason": "用户显式标记"})
                continue
            
            step_name = step.get("step_name", "")
            step_name_lower = step_name.lower()
            
            if n <= 2:
                results.append({"step_index": idx, "is_milestone": True, "reason": "短链（<=2步），所有步骤均为里程碑"})
                continue
            
            keyword_hit = None
            for kw in self.MILESTONE_KEYWORDS:
                if kw.lower() in step_name_lower:
                    keyword_hit = kw
                    break
            if keyword_hit:
                results.append({"step_index": idx, "is_milestone": True, "reason": f"关键词匹配: '{keyword_hit}'"})
                continue
            
            downstream_count = len(depended_by.get(idx, set()))
            if downstream_count >= 2:
                results.append({"step_index": idx, "is_milestone": True, "reason": f"瓶颈点（{downstream_count}个后续步骤依赖）"})
                continue
            
            if i == n - 1:
                results.append({"step_index": idx, "is_milestone": True, "reason": "最终交付步骤"})
                continue
            
            explicit_false = fm.get("is_milestone") is False
            results.append({
                "step_index": idx,
                "is_milestone": False,
                "reason": "显式取消里程碑" if explicit_false else "默认规则（非关键节点）"
            })
        
        return results
    
    def validate_chain(self, chain_data):
        """验证调用链数据"""
        errors = []
        warnings = []
        
        # 1. 基本结构
        if not chain_data.get("name"):
            errors.append("缺少名称")
        if not chain_data.get("steps"):
            errors.append("没有步骤")
        
        steps = chain_data.get("steps", [])
        
        # 2. 步骤完整性
        indices = set()
        for i, step in enumerate(steps):
            idx = step.get("index", i + 1)
            indices.add(idx)
            
            step_type = step.get("type", "skill")
            
            if not step.get("step_name"):
                warnings.append(f"步骤 {idx}: 缺少步骤名称")

            # adhesion 类型不需要 skill_name 和 action（v1.25.0）
            if step_type == "adhesion":
                adhesion = step.get("adhesion", {})
                if not adhesion.get("reason"):
                    warnings.append(f"步骤 {idx}: 粘连点缺少原因（adhesion.reason）")
                if not adhesion.get("solutions"):
                    warnings.append(f"步骤 {idx}: 粘连点缺少解决方案（adhesion.solutions）")
                continue

            if not step.get("skill_name"):
                warnings.append(f"步骤 {idx}: 缺少技能名称")
            if not step.get("action"):
                warnings.append(f"步骤 {idx}: 缺少动作描述")
        
        # 3. 技能可用性（跳过 adhesion 步骤）
        missing = []
        for step in steps:
            if step.get("type", "skill") == "adhesion":
                continue
            skill_name = step.get("skill_name", "")
            if skill_name in ("(内置)", "(内置打包)", ""):
                continue
            path = self.path_manager.find_skill_path(skill_name)
            if not path:
                missing.append(skill_name)
        
        if missing:
            missing_unique = list(set(missing))
            for ms in missing_unique:
                errors.append(f"技能未安装: {ms}")
        
        return errors, warnings

# ============================================================
# 备份管理类
# ============================================================

class BackupManager:
    """备份管理器（v1.29.0: 备份到链的私有目录）"""
    
    def __init__(self, path_manager):
        self.path_manager = path_manager
        self.backups_dir = path_manager.chains_dir  # 基目录
    
    def _get_backup_dir(self, name):
        """获取链的备份目录"""
        # 优先用链私有目录下的 backups/
        chain_dir = self.path_manager.chains_dir / name
        backup_dir = chain_dir / "backups"
        if chain_dir.exists():
            return backup_dir
        # 回退到全局 backups/
        return self.path_manager.chain_home / "backups"
    
    def ensure_dirs(self, name=""):
        """确保备份目录存在"""
        self._get_backup_dir(name).mkdir(parents=True, exist_ok=True)
    
    def backup_chain(self, name, chain_data, reason="auto"):
        """备份调用链"""
        backup_dir = self._get_backup_dir(name)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"{name}_{reason}_{timestamp}.json"
        
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(chain_data, f, ensure_ascii=False, indent=2)
        
        return backup_file
    
    def list_backups(self, name):
        """列出备份"""
        backup_dir = self._get_backup_dir(name)
        if not backup_dir.exists():
            return []
        
        backups = []
        for f in sorted(backup_dir.iterdir()):
            if f.name.startswith(name) and f.name.endswith(".json"):
                backups.append(f)
        
        return sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def restore_backup(self, name, backup_file):
        """恢复备份"""
        if not backup_file.exists():
            return False, f"备份文件不存在: {backup_file}"
        
        try:
            with open(backup_file, "r", encoding="utf-8") as f:
                chain_data = json.load(f)
            
            chain_dir = self.path_manager.chains_dir / name
            chain_dir.mkdir(parents=True, exist_ok=True)
            chain_file = chain_dir / "chain.json"
            with open(chain_file, "w", encoding="utf-8") as f:
                json.dump(chain_data, f, ensure_ascii=False, indent=2)
            
            return True, f"已从备份恢复: {backup_file.name}"
        except Exception as e:
            return False, f"恢复失败: {e}"

# ============================================================
# 调用链管理类
# ============================================================

class ChainManager:
    """调用链管理器"""
    
    def __init__(self):
        self.path_manager = PathManager()
        self.config_manager = ConfigManager(self.path_manager.chain_home)
        self.validator = ChainValidator(self.path_manager)
        self.backup_manager = BackupManager(self.path_manager)
    
    def _get_chain_dir(self, name):
        """获取链的私有目录（chains/{name}/）"""
        return self.path_manager.chains_dir / name

    def load_index(self):
        """加载调用链索引（备选方式，优先扫目录）"""
        if not self.path_manager.index_file.exists():
            return {}
        try:
            with open(self.path_manager.index_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    
    def save_index(self, index):
        """保存调用链索引"""
        self.path_manager.chains_dir.mkdir(parents=True, exist_ok=True)
        with open(self.path_manager.index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def load_chain(self, name):
        """加载调用链（优先从链目录加载）"""
        chain_dir = self._get_chain_dir(name)
        chain_file = chain_dir / "chain.json"
        if chain_file.exists():
            with open(chain_file, "r", encoding="utf-8") as f:
                return json.load(f)
        # 回退到 index 索引（兼容旧格式）
        index = self.load_index()
        if name in index:
            old_file = Path(index[name])
            if old_file.exists():
                return json.loads(old_file.read_text(encoding="utf-8"))
        return None
    
    def save_chain(self, chain_data):
        """保存调用链到私有目录"""
        name = chain_data["name"]
        chain_dir = self._get_chain_dir(name)
        chain_dir.mkdir(parents=True, exist_ok=True)
        chain_file = chain_dir / "chain.json"
        
        # 备份现有链（如果有旧文件）
        old_chain = self.load_chain(name)
        if old_chain:
            self.backup_manager.backup_chain(name, old_chain, "overwrite")
        
        # 保存新链
        with open(chain_file, "w", encoding="utf-8") as f:
            json.dump(chain_data, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        index = self.load_index()
        index[name] = str(chain_file)
        self.save_index(index)
        
        return True
    
    def delete_chain(self, name, force=False):
        """删除调用链（删除整个私有目录）"""
        chain_dir = self._get_chain_dir(name)
        if not chain_dir.exists():
            return False, f"调用链 '{name}' 不存在"
        
        # 备份
        existing = self.load_chain(name)
        if existing:
            self.backup_manager.backup_chain(name, existing, "delete")
        
        # 删除整个目录
        import shutil
        shutil.rmtree(chain_dir)
        
        # 更新索引
        index = self.load_index()
        if name in index:
            del index[name]
            self.save_index(index)
        
        return True, f"调用链 '{name}' 已删除"
    
    def list_chains(self):
        """列出所有调用链（扫描链目录）"""
        self.path_manager.chains_dir.mkdir(parents=True, exist_ok=True)
        chains = []
        for entry in sorted(self.path_manager.chains_dir.iterdir()):
            if entry.is_dir() and (entry / "chain.json").exists():
                chains.append(entry.name)
        return chains
    
    def create_chain(self, name, description="", purpose="", tags=None, steps=None, user_specified=False, schedule=None):
        """创建调用链（v1.25.0：自动调用 flow_validator + structure_checker 校验）"""
        if tags is None:
            tags = []
        if steps is None:
            steps = []

        # 调用 chain_flow_validator 校验流程
        try:
            from chain_flow_validator import validate as flow_validate
            flow_result = flow_validate(steps)
            if not flow_result["passed"]:
                err_msgs = [i["message"] for i in flow_result["issues"] if i["severity"] == "ERROR"]
                if err_msgs:
                    return False, f"流程校验未通过: {'; '.join(err_msgs[:3])}"
        except ImportError:
            pass  # 校验器不存在时不阻断

        # 调用 chain_structure_checker 校验结构
        try:
            from chain_structure_checker import check as struct_check
            struct_result = struct_check({
                "name": name,
                "steps": steps
            })
            if not struct_result["passed"]:
                err_msgs = [e["message"] for e in struct_result["errors"]]
                if err_msgs:
                    return False, f"结构校验未通过: {'; '.join(err_msgs[:3])}"
        except ImportError:
            pass

        # v1.29.0: 记录步骤私有蓝皮书（存到独立目录，不嵌入链 JSON）
        _save_blueprint_snapshot(self.path_manager, name, steps)

        chain_data = {
            "name": name,
            "description": description,
            "purpose": purpose,
            "tags": tags,
            "user_specified": user_specified,
            "steps": steps,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "exec_count": 0
        }
        if schedule:
            schedule["registered"] = schedule.get("registered", False)
            chain_data["schedule"] = schedule
        
        success = self.save_chain(chain_data)
        if success:
            return True, f"调用链 '{name}' 创建成功"
        else:
            return False, f"调用链 '{name}' 创建失败"
    

# ============================================================
# ChainEditor - 调用链编辑器
# ============================================================

class ChainEditor:
    """调用链编辑器（负责创建/更新/删除操作）"""
    
    def __init__(self, chain_manager):
        self.cm = chain_manager
        self.backup_manager = self.cm.backup_manager
        self.validator = self.cm.validator
    
    def create(self, name, description="", purpose="", tags=None, steps=None):
        """创建调用链"""
        if tags is None:
            tags = []
        if steps is None:
            steps = []
        
        chain_data = {
            "name": name,
            "description": description,
            "purpose": purpose,
            "tags": tags,
            "steps": steps,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "exec_count": 0
        }
        
        # 验证
        errors, warnings = self.validator.validate_chain(chain_data)
        if errors:
            return False, f"验证失败: {'; '.join(errors)}"
        
        for w in warnings:
            print(f"[警告] {w}")
        
        # 保存
        success = self.cm.save_chain(chain_data)
        if success:
            return True, f"调用链 '{name}' 创建成功"
        else:
            return False, f"调用链 '{name}' 创建失败"
    
    def update(self, name, **kwargs):
        """更新调用链"""
        chain_data = self.cm.load_chain(name)
        if not chain_data:
            return False, f"调用链 '{name}' 不存在"
        
        # 备份
        self.backup_manager.backup_chain(name, chain_data, "update")
        
        # 更新字段
        for key, value in kwargs.items():
            if key in chain_data:
                chain_data[key] = value
        
        chain_data["updated_at"] = datetime.now().isoformat()
        
        # 验证（保留原有 validate_chain + 新增 structure_checker 作为最后一道关）
        errors, warnings = self.validator.validate_chain(chain_data)
        if errors:
            return False, f"验证失败: {'; '.join(errors)}"
        try:
            from chain_structure_checker import check as struct_check
            struct_result = struct_check(chain_data)
            if not struct_result["passed"]:
                err_msgs = [e["message"] for e in struct_result["errors"]]
                return False, f"结构校验未通过: {'; '.join(errors[:3])}"
        except ImportError:
            pass
        
        # 保存
        self.cm.save_chain(chain_data)
        return True, f"调用链 '{name}' 已更新"
    
    def delete(self, name, force=False):
        """删除调用链"""
        return self.cm.delete_chain(name, force=force)
    
    def add_step(self, name, step):
        """添加步骤"""
        chain_data = self.cm.load_chain(name)
        if not chain_data:
            return False, f"调用链 '{name}' 不存在"
        
        # 备份
        self.backup_manager.backup_chain(name, chain_data, "add_step")
        
        # 添加步骤
        steps = chain_data.get("steps", [])
        step["index"] = len(steps) + 1
        steps.append(step)
        chain_data["steps"] = steps
        chain_data["updated_at"] = datetime.now().isoformat()
        
        # 保存
        self.cm.save_chain(chain_data)
        return True, f"步骤已添加到 '{name}'"
    
    def remove_step(self, name, index):
        """删除步骤"""
        chain_data = self.cm.load_chain(name)
        if not chain_data:
            return False, f"调用链 '{name}' 不存在"
        
        # 备份
        self.backup_manager.backup_chain(name, chain_data, "remove_step")
        
        # 删除步骤
        steps = chain_data.get("steps", [])
        idx = index - 1  # 转换为 0-based
        if idx < 0 or idx >= len(steps):
            return False, f"步骤索引无效: {index}"
        
        steps.pop(idx)
        
        # 重新编号
        for i, s in enumerate(steps):
            s["index"] = i + 1
        
        chain_data["steps"] = steps
        chain_data["updated_at"] = datetime.now().isoformat()
        
        # 保存
        self.cm.save_chain(chain_data)
        return True, f"步骤 {index} 已从 '{name}' 删除"
    

# ============================================================
# CLI 命令处理类
# ============================================================

class CLIHandler:
    """CLI 命令处理器"""
    
    def __init__(self):
        self.chain_manager = ChainManager()
    
    def cmd_init(self, args):
        """初始化"""
        self.chain_manager.path_manager.chains_dir.mkdir(parents=True, exist_ok=True)
        print("✅ 初始化完成")
        return 0
    
    def cmd_create(self, args):
        """创建调用链"""
        name = args.name
        description = args.description or ""
        purpose = args.purpose or ""
        tags = args.tags or []
        
        steps = []
        if args.steps:
            try:
                steps = json.loads(args.steps)
            except json.JSONDecodeError as e:
                print(f"❌ 步骤 JSON 解析失败: {e}")
                return 1

        user_specified = getattr(args, "user_specified", False) or getattr(args, "user", False)

        # ═══════════════════════════════════════════════════
        # [强制钩子] 技能能力扫描 — 创建链前必须扫描每个引用的技能
        # ═══════════════════════════════════════════════════
        skill_names_in_chain = set()
        for s in steps:
            if s.get("type") == "skill":
                skill_names_in_chain.add(s.get("skill_name", ""))
            elif s.get("type") == "branch":
                for ss in s.get("branch", {}).get("if_steps", []):
                    if ss.get("type") == "skill":
                        skill_names_in_chain.add(ss.get("skill_name", ""))
                for ss in s.get("branch", {}).get("else_steps", []):
                    if ss.get("type") == "skill":
                        skill_names_in_chain.add(ss.get("skill_name", ""))

        if skill_names_in_chain:
            print(f"\n{'='*55}")
            print(f"  [能力扫描] 分析链路中引用的技能")
            print(f"{'='*55}")
            from skill_extractor import extract_all as extract_skill_info
            skills_dir = self.chain_manager.skills_dir if hasattr(self.chain_manager, 'skills_dir') else Path.home() / ".workbuddy" / "skills"
            for sname in sorted(skill_names_in_chain):
                sk_path = Path(skills_dir) / sname
                if not sk_path.exists():
                    print(f"  ⚠️  技能目录不存在: {sname}")
                    continue
                info = extract_skill_info(sname, skill_path=sk_path, use_cache=False)
                if info.get("error"):
                    print(f"  ⚠️  {sname}: {info['error']}")
                    continue
                triggers = info.get("trigger_keywords", [])
                desc = info.get("description", "")[:80]
                ver = info.get("version", "?")
                cmds = info.get("core_commands", [])
                steps_info = info.get("key_steps", [])
                print(f"\n  ── {sname} v{ver} ──")
                print(f"     描述: {desc}")
                if triggers:
                    print(f"     触发: {', '.join(str(t)[:30] for t in triggers[:3])}")
                if cmds:
                    print(f"     核心指令: {', '.join(c[:40] if isinstance(c,str) else str(c)[:40] for c in cmds[:3])}")
                if steps_info:
                    print(f"     关键步骤: {len(steps_info)} 个")
                print()
            print(f"{'='*55}\n")

        # ═══════════════════════════════════════════════════
        # [强制钩子] 缺口分析与步骤规划 — 扫描后强制检查缝合点
        # ═══════════════════════════════════════════════════
        if len(steps) > 1:
            print(f"{'='*55}")
            print(f"  [缺口分析] 扫描技能衔接点 — {len(steps)} 步骤")
            print(f"{'='*55}")

            # v1.29.0: 尝试用 step_link_validator 做自动化衔接分析
            link_validation_available = False
            try:
                from step_link_validator import validate_link
                from skill_extractor import find_skill_dir, extract_step_semantics
                link_validation_available = True
            except ImportError:
                pass

            for i in range(len(steps) - 1):
                curr = steps[i]
                nxt = steps[i + 1]
                if curr.get("type") == "skill" and nxt.get("type") == "skill":
                    cname = curr.get("skill_name", "?")
                    cact = curr.get("action", "")[:40]
                    nname = nxt.get("skill_name", "?")
                    nact = nxt.get("action", "")[:40]
                    print(f"  ⛓️ {cname} ({cact})")
                    print(f"     → 缝合点 →")
                    print(f"     {nname} ({nact})")

                    # v1.29.0: 自动化衔接校验
                    if link_validation_available:
                        try:
                            curr_steps = extract_step_semantics(find_skill_dir(cname)) if find_skill_dir(cname) else []
                            nxt_steps = extract_step_semantics(find_skill_dir(nname)) if find_skill_dir(nname) else []

                            # 找最佳的 interface 匹配
                            curr_iface = {"produces": [], "consumes": []}
                            nxt_iface = {"produces": [], "consumes": []}

                            # 用 curr 的 action 匹配其步骤
                            cact_lower = cact.lower()
                            for s in curr_steps:
                                if cact_lower in s.get("description", "").lower() or cact_lower in s.get("step_name", "").lower():
                                    curr_iface = s.get("interface", {"produces": [], "consumes": []})
                                    break

                            nact_lower = nact.lower()
                            for s in nxt_steps:
                                if nact_lower in s.get("description", "").lower() or nact_lower in s.get("step_name", "").lower():
                                    nxt_iface = s.get("interface", {"consumes": [], "produces": []})
                                    break

                            # 执行校验
                            link_result = validate_link(curr_iface, nxt_iface, cname, nname)
                            if link_result["adhesion_suggestion"]:
                                print(f"     ⛔ 缺口检测: {link_result['gap_type']}")
                                print(f"     匹配分数: {link_result['score']}")
                                print(f"     建议插入粘连点")
                            elif link_result["passed"]:
                                print(f"     ✅ 衔接通过 (分数: {link_result['score']})")
                            else:
                                print(f"     ⚠️ 衔接存疑 (分数: {link_result['score']})")
                        except Exception as e:
                            if hasattr(args, 'verbose') and args.verbose:
                                print(f"     ⚠️  衔接校验异常: {e}")

            print()
            if not link_validation_available:
                print(f"  ── LLM 执行规则 ──")
                print(f"  逐步骤检查缝合点：")
                print(f"  • 无缺口 → 直接串联（不需要粘连点）")
                print(f"  • 有缺口 → 插入 adhesion 步骤（类型可选：manual/auto/hybrid）")
                print(f"  • 禁止连续粘连点（两个 adhesion 步骤必须合并）")
                print(f"  • 粘连点占比不得超过 30%")
            print(f"{'=' * 55}\n")

        # 定时/自动化关键字检测 —— 强制提醒，不靠 AI 自觉（v1.25.0）
        _TIMING_KEYWORDS = ["每天", "每周", "每月", "每年", "定时", "定期", "自动化", "自动执行",
                            "cron", "每小时", "每分", "每", "定期执行", "周期"]
        search_text = f"{description} {purpose}".lower()
        has_timing_intent = any(kw in search_text for kw in _TIMING_KEYWORDS)

        schedule = None
        if getattr(args, "schedule", ""):
            try:
                schedule = json.loads(args.schedule)
            except json.JSONDecodeError as e:
                print(f"❌ 调度配置 JSON 解析失败: {e}")
                return 1
        elif has_timing_intent:
            print("⚠️  检测到定时/自动化意图，但未提供 --schedule 参数。")
            print("   请补充调度配置，例如：")
            print("   --schedule '{\"type\":\"cron\",\"expression\":\"0 6 * * *\",\"description\":\"每天早上6点\"}'")
            print("   或取消链创建，移除描述中的时间相关词后重试。")
            return 1

        success, message = self.chain_manager.create_chain(name, description, purpose, tags, steps, user_specified=user_specified, schedule=schedule)
        if success:
            print(f"✅ {message}")

            # ═══════════════════════════════════════════════
            # [强制钩子] 创建后自动校验
            # ═══════════════════════════════════════════════
            print(f"\n  [自动校验] 验证链结构和流程...")
            try:
                from chain_structure_checker import check as structure_check
                result = structure_check(steps)
                if result.get("passed", False):
                    print(f"  ✅ 结构校验通过 ({len(result.get('issues', []))} 个问题)")
                else:
                    issues = result.get("issues", [])
                    for iss in issues:
                        print(f"  ❌ {iss.get('message', '?')}")
            except ImportError:
                pass

            try:
                from chain_flow_validator import validate_flow
                vresult = validate_flow(steps)
                if vresult.get("passed", False):
                    print(f"  ✅ 流程校验通过")
                else:
                    for err in vresult.get("errors", []):
                        print(f"  ❌ [流程] {err.get('message', '?')}")
            except ImportError:
                pass

            if schedule:
                print("")
                print("=" * 60)
                print("  [强制] 调度尚未注册到平台！")
                print(f"  链 '{name}' 配置了定时/自动化任务，但尚未注册。")
                desc = schedule.get("description", "")
                expr = schedule.get("expression", "")
                stype = schedule.get("type", "")
                print(f"  调度: {desc} ({stype}: {expr})")
                print("")
                print("  AI 必须立即完成注册，否则调度不会生效：")
                print(f"    选项1: 调用平台调度注册接口")
                print(f"    选项2: chain_manager.py register-schedule --name \"{name}\"")
                print()
                print("  ⛔ 调度未注册 — exit(1) 截断")
                print("  🚫 LLM 必须完成注册后再继续")
                print("=" * 60)
                import sys as _sys
                _sys.exit(1)
            return 0
        else:
            print(f"❌ {message}")
            return 1
    
    def cmd_list(self, args):
        """列出所有调用链"""
        chains = self.chain_manager.list_chains()
        if not chains:
            print("没有调用链")
            return 0
        
        print(f"调用链列表 ({len(chains)} 个):")
        for name in chains:
            print(f"  - {name}")
        
        return 0
    
    def cmd_show(self, args):
        """显示调用链"""
        name = args.name
        chain = self.chain_manager.load_chain(name)
        if not chain:
            print(f"❌ 调用链 '{name}' 不存在")
        if not chain:
            print(f"❌ 调用链 '{name}' 不存在")
            return 1
        
        print(f"调用链: {chain['name']}")
        print(f"描述: {chain.get('description', '')}")
        print(f"目的: {chain.get('purpose', '')}")
        print(f"步骤数: {len(chain.get('steps', []))}")

        sched = chain.get("schedule")
        if sched:
            print(f"调度: {sched.get('description', '')} ({sched.get('type', '')}: {sched.get('expression', '')})")

        return 0

    def cmd_schedule(self, args):
        """设置/查看/删除调用链调度配置（v1.25.0）"""
        name = args.name
        chain = self.chain_manager.load_chain(name)
        if not chain:
            print(f"❌ 调用链 '{name}' 不存在")
            return 1

        if args.remove:
            if "schedule" in chain:
                del chain["schedule"]
                chain["updated_at"] = datetime.now().isoformat()
                self.chain_manager.save_chain(chain)
                print(f"✅ 调度配置已删除: {name}")
            else:
                print("ℹ️ 无调度配置")
            return 0

        if args.cron or args.interval or args.once:
            if args.cron:
                sched = {"type": "cron", "expression": args.cron}
            elif args.interval:
                sched = {"type": "interval", "expression": str(args.interval)}
            elif args.once:
                sched = {"type": "once", "expression": args.once}

            if args.desc:
                sched["description"] = args.desc
            elif not sched.get("description"):
                sched["description"] = f"{sched['type']}: {sched['expression']}"

            sched["registered"] = False  # 新建调度默认未注册
            chain["schedule"] = sched
            chain["updated_at"] = datetime.now().isoformat()
            self.chain_manager.save_chain(chain)
            print(f"✅ 调度配置已设置: {sched['description']}")
            return 0

        # 无参数则查看
        sched = chain.get("schedule")
        if sched:
            print(f"调度: {sched.get('description', '')}")
            print(f"  类型: {sched.get('type', '')}")
            print(f"  表达式: {sched.get('expression', '')}")
        else:
            print("ℹ️ 无调度配置")
        return 0

    def cmd_register_schedule(self, args):
        """标记调用链的调度已在平台注册（v1.26.0）"""
        name = args.name
        chain = self.chain_manager.load_chain(name)
        if not chain:
            print(f"❌ 调用链 '{name}' 不存在")
            return 1

        sched = chain.get("schedule")
        if not sched:
            print(f"❌ 调用链 '{name}' 没有调度配置")
            return 1

        sched["registered"] = True
        chain["schedule"] = sched
        chain["updated_at"] = datetime.now().isoformat()
        self.chain_manager.save_chain(chain)

        print(f"✅ 调度已注册: {name}")
        print(f"   {sched.get('description', '')} ({sched['type']}: {sched['expression']})")
        print(f"   平台已确认，将按计划执行")
        return 0

    def cmd_check_gaps(self, args):
        """检查所有调用链的粘连点，尝试用新 skill 填补（v1.25.0）"""
        chains = self.chain_manager.list_chains()
        if not chains:
            print("没有调用链")
            return 0
        
        skills_dir = self.chain_manager.path_manager.skill_dir
        installed_skills = {}
        if skills_dir.exists():
            for d in sorted(skills_dir.iterdir()):
                if (d / "SKILL.md").exists():
                    installed_skills[d.name] = d
        
        total_gaps = 0
        filled = 0
        
        for name in chains:
            chain_data = self.chain_manager.load_chain(name)
            if not chain_data:
                continue

            # 用户指定 skill 的链跳过自愈
            if chain_data.get("user_specified", False):
                continue

            steps = chain_data.get("steps", [])
            changed = False
            chain_filled = 0
            for step in steps:
                if step.get("type", "skill") != "adhesion":
                    continue
                total_gaps += 1
                adhesion = step.get("adhesion", {})
                reason = adhesion.get("reason", "")
                
                best_match = None
                for sk_name, sk_path in installed_skills.items():
                    try:
                        skill_md = (sk_path / "SKILL.md").read_text(encoding="utf-8")
                        if reason.lower() in skill_md.lower():
                            best_match = sk_name
                            break
                    except Exception:
                        continue
                
                if best_match:
                    import json as _json
                    step["type"] = "skill"
                    step["skill_name"] = best_match
                    step["action"] = adhesion.get("solutions", [{}])[0].get("description", reason)
                    step["notes"] = f"原为粘连点，由 check-gaps 升级。原方案: {_json.dumps(adhesion.get('solutions', []), ensure_ascii=False)}"
                    del step["adhesion"]
                    chain_filled += 1
                    filled += 1
                    changed = True
            
            if changed:
                chain_data["updated_at"] = datetime.now().isoformat()
                self.chain_manager.save_chain(chain_data)
                print(f"  ✅ {name}: {chain_filled} 个粘连点已升级为 skill 步骤")
        
        print(f"检查完成: {total_gaps} 个粘连点，{filled} 个可升级")
        return 0
    
    def cmd_delete(self, args):
        """删除调用链"""
        name = args.name
        force = getattr(args, "force", False)
        
        success, message = self.chain_manager.delete_chain(name, force=force)
        if success:
            print(f"✅ {message}")
            return 0
        else:
            print(f"❌ {message}")
            return 1
    
    # ═══════════════════════════════════════════════════
    # v1.29.0: 链健康检查 - 蓝皮书比对（私有蓝皮书 + md5）
    # ═══════════════════════════════════════════════════
    def cmd_check_health(self, args):
        """检查调用链健康状态：比对当前 SKILL.md vs 链私有蓝皮书"""
        name = args.name
        chain = self.chain_manager.load_chain(name)
        if not chain:
            print(f"❌ 调用链 '{name}' 不存在")
            return 1

        # 读取私有蓝皮书
        pm = self.chain_manager.path_manager
        bp_file = pm.chains_dir / name / "blueprints.json"
        if not bp_file.exists():
            print(f"⚠️  调用链 '{name}' 没有私有蓝皮书（需 v1.29.0 重新创建）")
            return 0

        with open(bp_file, "r", encoding="utf-8") as f:
            blueprint_data = json.load(f)

        from skill_extractor import find_skill_dir, extract_step_semantics, read_skill_md
        import hashlib

        print(f"🏥 链健康检查: {name}")
        print(f"{'='*55}")
        print(f"  步骤数: {len(chain.get('steps', []))}")
        print(f"  蓝皮书步骤: {len(blueprint_data)} 个")
        print()

        # 按 skill 分组，避免重复读 md5
        skill_groups = {}
        for step_id, bp in blueprint_data.items():
            skill_name = step_id.split(".")[0]
            skill_groups.setdefault(skill_name, []).append((step_id, bp))

        results = {"healthy": 0, "changed": 0, "missing": 0}

        print(f"{'':-<90}")
        print(f"{'步骤ID':<40} {'状态':<12} {'说明'}")
        print(f"{'':-<90}")

        for skill_name, entries in skill_groups.items():
            skill_path = find_skill_dir(skill_name)
            if not skill_path:
                for step_id, _ in entries:
                    print(f"{step_id:<40} {'❌ 技能缺失':<12} 技能目录不存在")
                    results["missing"] += 1
                continue

            # md5 快速校验
            skill_md5 = hashlib.md5((read_skill_md(skill_path) or "").encode("utf-8")).hexdigest()
            old_md5 = blueprint_data.get("_skill_md5s", {}).get(skill_name, "")

            if skill_md5 == old_md5:
                # md5 一致 → 蓝皮书仍最新，直接比对
                for step_id, bp in entries:
                    iface_ok = _compare_interfaces(bp)
                    if iface_ok:
                        print(f"{step_id:<40} {'✅ 健康':<12} interface 未变化")
                        results["healthy"] += 1
                    else:
                        print(f"{step_id:<40} {'⚠️ 无interface':<12} 蓝皮书无 interface 数据")
                        results["changed"] += 1
                continue

            # md5 不一致 → SKILL.md 变了，现场重提
            current_steps = extract_step_semantics(skill_path)
            current_map = {}
            for cs in current_steps:
                current_map[cs.get("step_id", "")] = cs
                current_map[cs.get("step_name", "")] = cs  # 名称备查

            for step_id, bp in entries:
                # 在当前蓝皮书中找匹配
                cur = current_map.get(step_id)
                if not cur:
                    # 模糊匹配
                    step_rel = step_id[len(skill_name) + 1:]
                    for cid, c in current_map.items():
                        if isinstance(cid, str) and step_rel in cid:
                            cur = c
                            break

                if cur is None:
                    print(f"{step_id:<40} {'❌ 步骤消失':<12} 当前 SKILL.md 无此步骤")
                    results["missing"] += 1
                    continue

                # 比对 full blueprint
                old_bp = bp
                new_bp = {
                    "description": cur.get("description", ""),
                    "usage_hint": cur.get("usage_hint", ""),
                    "call_address": cur.get("call_address", {}),
                    "interface": cur.get("interface", {}),
                }

                changes = _diff_blueprint(old_bp, new_bp)
                if changes:
                    print(f"{step_id:<40} {'⚠️ 已变化':<12} {', '.join(changes)}")
                    results["changed"] += 1
                else:
                    print(f"{step_id:<40} {'✅ 健康':<12} interface 未变化")
                    results["healthy"] += 1

        print(f"\n{'='*55}")
        total = results["healthy"] + results["changed"] + results["missing"]
        print(f"  健康: {results['healthy']}/{total}")
        if results["changed"]:
            print(f"  ⚠️  已变化: {results['changed']}/{total} → 建议重新创建链或更新蓝皮书")
        if results["missing"]:
            print(f"  ❌ 已丢失: {results['missing']}/{total} → 链可能损坏")
        print()

        return 0


# ============================================================
# v1.29.0: 蓝皮书私有化（存独立文件，不嵌入链 JSON）
# ============================================================

def _save_blueprint_snapshot(path_manager, chain_name, steps):
    """保存链的私有蓝皮书到 chains/{chain_name}/blueprints.json

    每个步骤保存完整 blueprint（description, call_address, usage_hint, interface），
    并记录对应 skill 的 md5 以便后续快速校验。
    """
    from skill_extractor import find_skill_dir, extract_step_semantics, read_skill_md
    import hashlib

    blueprint_data = {}
    skill_md5s = {}

    for step in steps:
        if step.get("type", "skill") != "skill":
            continue
        skill_name = step.get("skill_name", "")
        step_name = step.get("step_name", "")
        if not skill_name or not step_name:
            continue

        step_id = f"{skill_name}.{step_name.replace(' ', '-')[:30]}"

        # 尝试从当前 SKILL.md 提取完整 blueprint
        try:
            skill_dir = find_skill_dir(skill_name)
            if skill_dir:
                # 记录 skill md5
                md5_val = hashlib.md5((read_skill_md(skill_dir) or "").encode("utf-8")).hexdigest()
                skill_md5s[skill_name] = md5_val

                steps_info = extract_step_semantics(skill_dir)
                for si in steps_info:
                    if si.get("step_id") == step_id or si.get("step_name", "") == step_name:
                        blueprint_data[step_id] = {
                            "step_id": step_id,
                            "step_name": si.get("step_name", step_name),
                            "skill_name": skill_name,
                            "description": si.get("description", ""),
                            "usage_hint": si.get("usage_hint", ""),
                            "call_address": si.get("call_address", {}),
                            "interface": si.get("interface", {}),
                        }
                        break
                else:
                    # 没精确匹配，存基础信息
                    blueprint_data[step_id] = {
                        "step_id": step_id,
                        "step_name": step_name,
                        "skill_name": skill_name,
                        "description": step.get("action", ""),
                        "usage_hint": "",
                        "call_address": {"instructions": [], "cli": ""},
                        "interface": {"consumes": [], "produces": []},
                    }
            else:
                blueprint_data[step_id] = {
                    "step_id": step_id,
                    "step_name": step_name,
                    "skill_name": skill_name,
                    "description": step.get("action", ""),
                    "usage_hint": "",
                    "call_address": {"instructions": [], "cli": ""},
                    "interface": {"consumes": [], "produces": []},
                }
        except Exception:
            blueprint_data[step_id] = {
                "step_id": step_id,
                "step_name": step_name,
                "skill_name": skill_name,
                "description": step.get("action", ""),
                "usage_hint": "",
                "call_address": {"instructions": [], "cli": ""},
                "interface": {"consumes": [], "produces": []},
            }

    # 存 skill md5s 供后续快速校验
    blueprint_data["_skill_md5s"] = skill_md5s

    # 写入文件到链私有目录
    bp_dir = path_manager.chains_dir / chain_name
    bp_dir.mkdir(parents=True, exist_ok=True)
    bp_file = bp_dir / "blueprints.json"
    with open(bp_file, "w", encoding="utf-8") as f:
        json.dump(blueprint_data, f, ensure_ascii=False, indent=2)


def _diff_blueprint(old_bp, new_bp):
    """比对单个步骤的蓝皮书变化"""
    changes = []

    old_iface = old_bp.get("interface", {})
    new_iface = new_bp.get("interface", {})

    old_produces = old_iface.get("produces", [])
    new_produces = new_iface.get("produces", [])
    old_consumes = old_iface.get("consumes", [])
    new_consumes = new_iface.get("consumes", [])

    if old_produces != new_produces:
        changes.append("输出变化")
    if old_consumes != new_consumes:
        changes.append("输入变化")

    old_ca = old_bp.get("call_address", {})
    new_ca = new_bp.get("call_address", {})
    if old_ca.get("instructions") != new_ca.get("instructions"):
        changes.append("指令变化")
    if old_ca.get("cli") != new_ca.get("cli"):
        changes.append("CLI变化")

    return changes


def _compare_interfaces(bp):
    """检查蓝皮书中是否有有效的 interface 数据"""
    iface = bp.get("interface", {})
    return bool(iface.get("consumes") or iface.get("produces"))


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    # 修复 Windows 控制台编码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python <3.7 不支持
    
    parser = argparse.ArgumentParser(
        description="Chain Manager v1.2.0 - 调用链管理 (OO Refactor)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python chain_manager.py init
  python chain_manager.py create --name "发布流水线" --description "技能发布流程"
  python chain_manager.py list
  python chain_manager.py show --name "发布流水线"
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # init
    subparsers.add_parser("init", help="初始化")
    
    # create
    p_create = subparsers.add_parser("create", help="创建调用链")
    p_create.add_argument("--name", required=True, help="调用链名称")
    p_create.add_argument("--description", default="", help="描述")
    p_create.add_argument("--purpose", default="", help="目的")
    p_create.add_argument("--tags", default="", help="标签 (JSON 数组)")
    p_create.add_argument("--steps", default="", help="步骤 (JSON 数组)")
    p_create.add_argument("--user-specified", action="store_true", help="标记为用户显式指定的 skill，自愈时跳过")
    p_create.add_argument("--schedule", default="", help="调度配置 (JSON 对象，如 '{\"type\":\"cron\",\"expression\":\"0 6 * * *\"}')")
    
    # list
    subparsers.add_parser("list", help="列出所有调用链")
    
    # show
    p_show = subparsers.add_parser("show", help="显示调用链")
    p_show.add_argument("--name", required=True, help="调用链名称")
    
    # delete
    p_delete = subparsers.add_parser("delete", help="删除调用链")
    p_delete.add_argument("--name", required=True, help="调用链名称")
    p_delete.add_argument("--force", action="store_true", help="强制删除（不确认）")
    
    # check-gaps (v1.25.0)
    subparsers.add_parser("check-gaps", help="检查所有调用链的粘连点，尝试用新 skill 填补")
    
    # schedule (v1.25.0)
    p_sched = subparsers.add_parser("schedule", help="设置/查看/删除调用链调度配置")
    p_sched.add_argument("--name", required=True, help="调用链名称")
    p_sched.add_argument("--cron", default="", help="cron 表达式（如 '0 6 * * *' 每天早上6点）")
    p_sched.add_argument("--interval", type=int, default=0, help="间隔秒数（如 86400 每天）")
    p_sched.add_argument("--once", default="", help="单次执行（ISO 时间，如 '2026-06-03T06:00:00'）")
    p_sched.add_argument("--desc", default="", help="调度描述（自然语言）")
    p_sched.add_argument("--remove", action="store_true", help="删除调度配置")
    
    # register-schedule (v1.26.0)
    p_reg = subparsers.add_parser("register-schedule", help="标记调度已注册到平台")
    p_reg.add_argument("--name", required=True, help="调用链名称")
    
    # check-health (v1.29.0)
    p_health = subparsers.add_parser("check-health", help="检查调用链健康状态（蓝皮书比对）")
    p_health.add_argument("--name", required=True, help="调用链名称")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    cli_handler = CLIHandler()
    
    commands = {
        "init": cli_handler.cmd_init,
        "create": cli_handler.cmd_create,
        "list": cli_handler.cmd_list,
        "show": cli_handler.cmd_show,
        "delete": cli_handler.cmd_delete,
        "check-gaps": cli_handler.cmd_check_gaps,
        "check-health": cli_handler.cmd_check_health,
        "schedule": cli_handler.cmd_schedule,
        "register-schedule": cli_handler.cmd_register_schedule,
    }
    
    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
