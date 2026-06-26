"""OpenClaw操作实现函数"""

import os
import tempfile
import logging
from typing import Dict, Any, List
from .utils import ensure_directory, create_temp_file
from .tia_core import TiaPortal
from .hardware import HardwareCatalog
from .block_generator import SCLGenerator

logger = logging.getLogger(__name__)

# 全局TIA实例
_tia: TiaPortal = None
_scl_gen = SCLGenerator()

def get_tia(params: Dict[str, Any]) -> TiaPortal:
    """获取或创建TIA Portal实例"""
    global _tia
    if _tia is None:
        tia_version = params.get("tia_version", "V18")
        mode = params.get("tia_mode", "WithUserInterface")
        _tia = TiaPortal(tia_version, mode)
        _tia.start()
    return _tia

def close_tia():
    """关闭TIA Portal实例"""
    global _tia
    if _tia:
        _tia.close()
        _tia = None

# ---------- 操作函数 ----------

def action_create_project(params: Dict[str, Any]) -> Dict[str, Any]:
    """创建新项目"""
    tia = get_tia(params)
    path = params.get("path")
    name = params.get("name")
    author = params.get("author", "")
    comment = params.get("comment", "")
    if not path or not name:
        return {"success": False, "message": "缺少 path 或 name 参数"}
    if not ensure_directory(path):
        return {"success": False, "message": f"无法创建目录: {path}"}
    try:
        proj = tia.create_project(path, name, author, comment)
        return {
            "success": True,
            "message": f"项目创建成功: {name}",
            "project_path": proj.Path.FullName
        }
    except Exception as e:
        logger.exception("创建项目失败")
        return {"success": False, "message": f"创建项目失败: {str(e)}"}

def action_add_plc(params: Dict[str, Any]) -> Dict[str, Any]:
    """添加PLC设备"""
    tia = get_tia(params)
    if not tia.project:
        return {"success": False, "message": "没有打开的项目，请先创建或打开项目"}
    device_name = params.get("device_name", "PLC_1")
    cpu_model = params.get("cpu_model", "CPU 1511-1 PN")
    family = params.get("family", "S7-1500")
    firmware = params.get("firmware", "V4.0")

    # 从硬件目录获取路径
    if family == "S7-1200":
        catalog = HardwareCatalog.CPU_S7_1200.get(cpu_model)
    else:
        catalog = HardwareCatalog.CPU_S7_1500.get(cpu_model)
    if not catalog:
        return {"success": False, "message": f"未知CPU型号: {cpu_model}"}

    try:
        device = tia.add_plc_device(device_name, catalog, firmware)
        return {
            "success": True,
            "message": f"PLC设备添加成功: {device_name}",
            "device_name": device.Name
        }
    except Exception as e:
        logger.exception("添加PLC失败")
        return {"success": False, "message": f"添加PLC失败: {str(e)}"}

def action_create_block(params: Dict[str, Any]) -> Dict[str, Any]:
    """根据描述创建程序块并生成SCL代码"""
    tia = get_tia(params)
    if not tia.project:
        return {"success": False, "message": "没有打开的项目"}
    plc_name = params.get("plc_name")
    block_type = params.get("block_type")  # "OB","FB","FC","DB"
    block_name = params.get("block_name")
    description = params.get("description", "")
    number = params.get("number", 0)
    language = params.get("language", "SCL")

    if not plc_name or not block_type or not block_name:
        return {"success": False, "message": "缺少 plc_name, block_type 或 block_name 参数"}

    try:
        plc_software = tia.get_plc_software(plc_name)
        # 生成SCL代码
        scl_code = _scl_gen.generate(block_type, block_name, description)
        # 创建块
        block = tia.create_block(plc_software, block_type, block_name, number, language, scl_code)
        return {
            "success": True,
            "message": f"{block_type}块创建成功: {block_name}",
            "block_name": block.Name,
            "block_number": block.Number
        }
    except Exception as e:
        logger.exception("创建块失败")
        return {"success": False, "message": f"创建块失败: {str(e)}"}

def action_compile_software(params: Dict[str, Any]) -> Dict[str, Any]:
    """编译PLC软件"""
    tia = get_tia(params)
    if not tia.project:
        return {"success": False, "message": "没有打开的项目"}
    plc_name = params.get("plc_name")
    if not plc_name:
        return {"success": False, "message": "缺少 plc_name 参数"}
    try:
        plc_software = tia.get_plc_software(plc_name)
        success, msgs = tia.compile_plc(plc_software)
        if success:
            return {"success": True, "message": "编译成功", "messages": msgs}
        else:
            return {"success": False, "message": "编译失败", "messages": msgs}
    except Exception as e:
        return {"success": False, "message": f"编译异常: {str(e)}"}

def action_download(params: Dict[str, Any]) -> Dict[str, Any]:
    """下载到PLC"""
    tia = get_tia(params)
    if not tia.project:
        return {"success": False, "message": "没有打开的项目"}
    plc_name = params.get("plc_name")
    interface = params.get("interface", "PN/IE")
    ip_address = params.get("ip_address")
    password = params.get("password")

    if not plc_name:
        return {"success": False, "message": "缺少 plc_name 参数"}

    try:
        plc_software = tia.get_plc_software(plc_name)
        success, result = tia.download_to_plc(plc_software, interface, ip_address, password)
        if success:
            return {"success": True, "message": result}
        else:
            return {"success": False, "message": "下载失败", "details": result}
    except Exception as e:
        logger.exception("下载失败")
        return {"success": False, "message": f"下载异常: {str(e)}"}

def action_save_project(params: Dict[str, Any]) -> Dict[str, Any]:
    """保存项目"""
    tia = get_tia(params)
    if not tia.project:
        return {"success": False, "message": "没有打开的项目"}
    try:
        tia.save_project()
        return {"success": True, "message": "项目保存成功"}
    except Exception as e:
        return {"success": False, "message": f"保存失败: {str(e)}"}

def action_close_project(params: Dict[str, Any]) -> Dict[str, Any]:
    """关闭项目"""
    tia = get_tia(params)
    if not tia.project:
        return {"success": False, "message": "没有打开的项目"}
    try:
        tia.close_project()
        return {"success": True, "message": "项目已关闭"}
    except Exception as e:
        return {"success": False, "message": f"关闭失败: {str(e)}"}

def action_full_automation(params: Dict[str, Any]) -> Dict[str, Any]:
    """完整自动化流程"""
    steps = [
        ("创建项目", action_create_project),
        ("添加PLC", action_add_plc),
        ("创建程序块", action_create_block),
        ("编译软件", action_compile_software),
        ("下载", action_download)
    ]
    results = []
    for step_name, step_func in steps:
        # 为每个步骤传入相同参数（但可根据需要调整）
        res = step_func(params)
        results.append({"step": step_name, "success": res["success"], "message": res.get("message")})
        if not res["success"]:
            break
    return {
        "success": all(r["success"] for r in results),
        "steps": results
    }