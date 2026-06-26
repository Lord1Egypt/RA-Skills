#!/usr/bin/env python3
"""
迁移脚本 - 从旧版 yaoyao-memory 迁移到模块化架构

特性：
- 事务性迁移：每步可回滚
- 自动备份：所有操作前先备份
- 断点续传：中断后可继续
- 详细日志：每步都记录
"""

import argparse
import json
import os
import shutil
import sys
import traceback
from datetime import datetime
from pathlib import Path

# 路径配置
SKILL_DIR = Path(__file__).parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
MODULES_FILE = SKILL_DIR / "MODULES.json"
MIGRATION_LOG = SKILL_DIR / ".migration.log"
MIGRATION_STATE = SKILL_DIR / ".migration_state.json"
BACKUP_DIR = Path.home() / ".openclaw" / "backup" / "pre-migration"


class MigrationError(Exception):
    """迁移错误"""
    pass


class MigrationLogger:
    """迁移日志"""
    
    def __init__(self):
        self.logs = []
        self.start_time = datetime.now()
    
    def log(self, level, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(entry)
        print(entry)
    
    def info(self, message):
        self.log("INFO", message)
    
    def warn(self, message):
        self.log("WARN", message)
    
    def error(self, message):
        self.log("ERROR", message)
    
    def success(self, message):
        self.log("SUCCESS", message)
    
    def save(self):
        """保存日志"""
        MIGRATION_LOG.write_text("\n".join(self.logs))
        logger.info(f"日志已保存: {MIGRATION_LOG}")


logger = MigrationLogger()


def load_modules():
    """加载模块配置"""
    if not MODULES_FILE.exists():
        raise MigrationError(f"模块配置文件不存在: {MODULES_FILE}")
    return json.loads(MODULES_FILE.read_text())


def load_state():
    """加载迁移状态"""
    if MIGRATION_STATE.exists():
        try:
            return json.loads(MIGRATION_STATE.read_text())
        except:
            pass
    return {"step": 0, "completed": [], "backup_done": False}


def save_state(state):
    """保存迁移状态"""
    MIGRATION_STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def check_old_installation():
    """检查旧版安装"""
    logger.info("检查旧版安装...")
    
    old_paths = [
        Path.home() / ".openclaw" / "workspace" / "skills" / "yaoyao-memory",
        Path.home() / ".openclaw" / "workspace" / "skills" / "yaoyao-memory-v2",
        Path.home() / ".openclaw" / "workspace" / "skills" / "yaoyao-memory-homo",
    ]
    
    old_found = []
    for path in old_paths:
        if path.exists() and path != SKILL_DIR:
            scripts = path / "scripts"
            if scripts.exists():
                script_count = len(list(scripts.glob("*.py")))
                old_found.append({
                    "path": path,
                    "scripts": script_count,
                    "is_large": script_count > 50
                })
    
    if old_found:
        logger.warn(f"发现 {len(old_found)} 个旧版安装：")
        for info in old_found:
            style = "旧版（未拆分）" if info["is_large"] else "新版"
            logger.info(f"  {info['path'].name}: {info['scripts']} 脚本 ({style})")
    else:
        logger.info("未发现旧版安装")
    
    return old_found


def check_data():
    """检查数据"""
    logger.info("检查现有数据...")
    
    data_info = {"memory_files": 0, "db_size_mb": 0}
    
    # 记忆目录
    memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    if memory_dir.exists():
        memory_files = list(memory_dir.glob("*.md"))
        data_info["memory_files"] = len(memory_files)
        logger.info(f"  记忆文件: {len(memory_files)} 个")
    
    # 数据库
    db_path = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
    if db_path.exists():
        size_mb = db_path.stat().st_size / 1024 / 1024
        data_info["db_size_mb"] = round(size_mb, 2)
        logger.info(f"  数据库: {size_mb:.1f} MB")
    
    return data_info


def step1_backup(state):
    """步骤1：备份"""
    if state.get("backup_done"):
        logger.info("步骤1已跳过（已执行）")
        return True
    
    logger.info("步骤1：备份现有数据...")
    
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        # 备份记忆
        memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
        if memory_dir.exists():
            backup_memory = BACKUP_DIR / "memory"
            if backup_memory.exists():
                shutil.rmtree(backup_memory)
            shutil.copytree(memory_dir, backup_memory)
            logger.success(f"  记忆文件已备份: {backup_memory}")
        
        # 备份数据库
        db_path = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
        if db_path.exists():
            backup_db = BACKUP_DIR / "vectors.db"
            shutil.copy2(db_path, backup_db)
            backup_db_size = backup_db.stat().st_size / 1024 / 1024
            logger.success(f"  数据库已备份: {backup_db_size:.1f} MB")
        
        # 备份配置
        config_dir = SKILL_DIR / "config"
        if config_dir.exists():
            backup_config = BACKUP_DIR / "config"
            if backup_config.exists():
                shutil.rmtree(backup_config)
            shutil.copytree(config_dir, backup_config)
            logger.success(f"  配置已备份: {backup_config}")
        
        # 写入备份标记
        backup_info = {
            "backup_time": datetime.now().isoformat(),
            "backup_dir": str(BACKUP_DIR),
            "memory_files": state.get("data_info", {}).get("memory_files", 0),
        }
        (BACKUP_DIR / "backup_info.json").write_text(json.dumps(backup_info, indent=2))
        
        state["backup_done"] = True
        state["backup_time"] = datetime.now().isoformat()
        save_state(state)
        
        logger.success("步骤1完成：备份成功")
        return True
        
    except Exception as e:
        logger.error(f"备份失败: {e}")
        logger.error(traceback.format_exc())
        return False


def step2_detect_modules(state):
    """步骤2：检测已安装的模块"""
    if state.get("modules_detected"):
        logger.info("步骤2已跳过（已执行）")
        return True
    
    logger.info("步骤2：检测已安装模块...")
    
    try:
        modules = load_modules()
        detected = []
        
        for module_id, module in modules["modules"].items():
            scripts = module.get("scripts", [])
            found_count = 0
            for script in scripts:
                script_path = SCRIPTS_DIR / f"{script}.py"
                if script_path.exists():
                    found_count += 1
            
            if found_count > 0:
                detected.append({
                    "id": module_id,
                    "name": module["name"],
                    "found": found_count,
                    "total": len(scripts)
                })
                logger.info(f"  检测到: {module['name']} ({found_count}/{len(scripts)} 脚本)")
        
        state["detected_modules"] = detected
        state["modules_detected"] = True
        save_state(state)
        
        logger.success(f"步骤2完成：检测到 {len(detected)} 个模块")
        return True
        
    except Exception as e:
        logger.error(f"检测失败: {e}")
        return False


def step3_install_core(state):
    """步骤3：安装核心"""
    if state.get("core_installed"):
        logger.info("步骤3已跳过（已执行）")
        return True
    
    logger.info("步骤3：安装核心模块...")
    
    try:
        # 标记核心已安装
        core_marker = SKILL_DIR / ".core_installed"
        core_marker.write_text(datetime.now().isoformat())
        
        state["core_installed"] = True
        state["core_installed_at"] = datetime.now().isoformat()
        save_state(state)
        
        logger.success("步骤3完成：核心模块已标记")
        return True
        
    except Exception as e:
        logger.error(f"核心安装失败: {e}")
        return False


def step4_mark_optional_modules(state):
    """步骤4：标记可选模块"""
    if state.get("modules_marked"):
        logger.info("步骤4已跳过（已执行）")
        return True
    
    logger.info("步骤4：标记可选模块...")
    
    try:
        installed = {
            "modules": [],
            "installed_at": {}
        }
        
        # 核心模块必装
        installed["modules"].append("core")
        installed["installed_at"]["core"] = datetime.now().isoformat()
        
        # 标记检测到的模块
        detected = state.get("detected_modules", [])
        for mod in detected:
            mod_id = mod["id"]
            if mod_id != "core":
                installed["modules"].append(mod_id)
                installed["installed_at"][mod_id] = datetime.now().isoformat()
        
        # 保存安装状态
        INSTALLED_FILE = SKILL_DIR / ".installed_modules.json"
        INSTALLED_FILE.write_text(json.dumps(installed, indent=2, ensure_ascii=False))
        
        logger.success(f"步骤4完成：已标记 {len(installed['modules'])} 个模块")
        for mod_id in installed["modules"]:
            logger.info(f"  - {mod_id}")
        
        state["modules_marked"] = True
        state["marked_modules"] = installed["modules"]
        save_state(state)
        
        return True
        
    except Exception as e:
        logger.error(f"标记失败: {e}")
        return False


def step5_verify_data(state):
    """步骤5：验证数据"""
    if state.get("data_verified"):
        logger.info("步骤5已跳过（已执行）")
        return True
    
    logger.info("步骤5：验证数据完整性...")
    
    try:
        issues = []
        
        # 检查记忆文件
        memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
        if memory_dir.exists():
            memory_files = list(memory_dir.glob("*.md"))
            logger.info(f"  记忆文件: {len(memory_files)} 个")
            
            # 检查关键文件
            critical = ["MEMORY.md", datetime.now().strftime("%Y-%m-%d") + ".md"]
            for f in critical:
                if not (memory_dir / f).exists():
                    issues.append(f"缺少关键文件: {f}")
        
        # 检查数据库
        db_path = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
        if db_path.exists():
            size_mb = db_path.stat().st_size / 1024 / 1024
            logger.info(f"  数据库: {size_mb:.1f} MB")
            
            if size_mb < 0.001:  # 小于 1KB
                issues.append("数据库文件异常小")
        else:
            logger.warn("  数据库: 不存在（首次安装）")
        
        if issues:
            for issue in issues:
                logger.warn(f"  ⚠️  {issue}")
            state["data_issues"] = issues
        else:
            logger.success("  数据验证通过")
        
        state["data_verified"] = True
        save_state(state)
        
        return True
        
    except Exception as e:
        logger.error(f"验证失败: {e}")
        return False


def rollback(state):
    """回滚"""
    logger.warn("开始回滚...")
    
    try:
        # 删除安装标记
        for marker in [".core_installed", ".installed_modules.json", ".migration_state.json"]:
            path = SKILL_DIR / marker
            if path.exists():
                path.unlink()
                logger.info(f"  已删除: {marker}")
        
        logger.success("回滚完成")
        return True
        
    except Exception as e:
        logger.error(f"回滚失败: {e}")
        return False


def migrate(dry_run=False, force=False):
    """执行迁移"""
    state = load_state()
    
    if state.get("completed") and not force:
        logger.info("迁移已完成！")
        logger.info("使用 --force 重新迁移")
        return True
    
    logger.info("=" * 50)
    logger.info("开始迁移")
    logger.info("=" * 50)
    
    if dry_run:
        logger.warn("预览模式：不会实际执行任何操作")
        logger.info("")
    
    # 执行迁移步骤
    steps = [
        ("backup", lambda: step1_backup(state)),
        ("detect", lambda: step2_detect_modules(state)),
        ("core", lambda: step3_install_core(state)),
        ("mark", lambda: step4_mark_optional_modules(state)),
        ("verify", lambda: step5_verify_data(state)),
    ]
    
    if dry_run:
        logger.info("迁移步骤预览：")
        for i, (name, _) in enumerate(steps):
            done = state.get(steps[i][0] + "_done")
            status = "✅ 已完成" if done else "⏳ 待执行"
            logger.info(f"  {i+1}. {name}: {status}")
        return True
    
    # 实际执行
    for i, (name, step_fn) in enumerate(steps):
        done = state.get(name + "_done")
        if done:
            continue
        
        logger.info(f"\n执行步骤 {i+1}/{len(steps)}: {name}")
        
        if not step_fn():
            logger.error(f"步骤 {name} 失败")
            
            # 询问是否回滚
            print("\n选项：")
            print("  r - 回滚所有更改")
            print("  c - 继续尝试（可能丢失数据）")
            print("  q - 退出（保留当前状态）")
            
            choice = input("\n请选择 [r]: ").strip().lower() or "r"
            
            if choice == "r":
                rollback(state)
            elif choice == "c":
                logger.warn("继续执行，风险自负")
            else:
                logger.info("退出，状态已保存，可稍后继续")
                return False
    
    # 标记完成
    state["completed"] = True
    state["completed_at"] = datetime.now().isoformat()
    save_state(state)
    
    logger.success("=" * 50)
    logger.success("迁移完成！")
    logger.success("=" * 50)
    
    logger.info("\n后续操作：")
    logger.info("  python3 install_modules.py --status   # 查看模块状态")
    logger.info("  python3 install_modules.py --list    # 查看所有模块")
    
    logger.save()
    return True


def show_status():
    """显示迁移状态"""
    print("=" * 50)
    print("🦞 yaoyao-memory 迁移状态")
    print("=" * 50)
    print()
    
    # 检测旧版本
    old_installs = check_old_installation()
    data_info = check_data()
    
    if old_installs or data_info.get("memory_files"):
        print("  📦 待迁移数据: ✅ 发现")
        if data_info.get("memory_files"):
            print(f"     记忆文件: {data_info['memory_files']} 个")
        if data_info.get("db_size_mb"):
            print(f"     数据库: {data_info['db_size_mb']} MB")
    else:
        print("  📦 待迁移数据: ❌ 未发现")
    
    print()
    
    # 迁移状态
    state_file = Path(".migration_state.json")
    if state_file.exists():
        state = load_state()
        completed = state.get("completed", False)
        print(f"  🔄 迁移状态: {'✅ 已完成' if completed else '⚠️ 未完成/中断'}")
        
        if state.get("completed_at"):
            print(f"     完成时间: {state['completed_at']}")
        
        if state.get("steps"):
            print("     已完成步骤:")
            for step in state.get("steps", []):
                print(f"       - {step}")
    else:
        print("  🔄 迁移状态: ❌ 未开始")
    
    print()
    
    # 备份检查
    backup_dir = Path.home() / ".openclaw" / "backup"
    if backup_dir.exists():
        backups = list(backup_dir.iterdir())
        print(f"  💾 备份目录: ✅ ({len(backups)} 个备份)")
    else:
        print("  💾 备份目录: ❌ 不存在")
    
    print()
    print("命令:")
    print("  python3 migrate.py --dry      # 预览迁移")
    print("  python3 migrate.py --force    # 执行迁移")
    print("  python3 migrate.py --status   # 本命令")


def main():
    parser = argparse.ArgumentParser(description="yaoyao-memory 迁移工具")
    parser.add_argument("--dry", action="store_true", help="预览迁移（不执行）")
    parser.add_argument("--force", action="store_true", help="强制重新迁移")
    parser.add_argument("--status", action="store_true", help="显示迁移状态")
    
    args = parser.parse_args()
    
    # 状态模式
    if args.status:
        show_status()
        return
    
    print("=" * 50)
    print("🦞 yaoyao-memory 迁移工具 v2")
    print("=" * 50)
    print()
    
    # 检查
    old_installs = check_old_installation()
    data_info = check_data()
    
    if not old_installs and not data_info.get("memory_files"):
        logger.info("未检测到需要迁移的数据")
        logger.info("如需全新安装，运行：")
        logger.info("  python3 install_modules.py --full-install")
        return
    
    print()
    
    if args.dry:
        migrate(dry_run=True)
        return
    
    if args.force:
        logger.warn("强制模式：重新迁移")
        state = load_state()
        state["completed"] = False
        save_state(state)
    
    migrate(dry_run=False)


if __name__ == "__main__":
    main()
