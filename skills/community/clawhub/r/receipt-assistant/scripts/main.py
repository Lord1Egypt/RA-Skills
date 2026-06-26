#!/usr/bin/env python3
"""
报销助手 - OpenClaw Skill 辅助脚本

视觉识别由 OpenClaw 的 image 工具完成，本脚本仅提供：
- 目录扫描
- 文件名生成
- Excel 报表生成
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scanner import FileScanner
from namer import FileNamer
from reporter import ReportGenerator
from models import TicketType, ProcessStatus
from config import get_config, save_config, is_configured


def scan_directory(directory: str) -> dict:
    """
    扫描目录，返回文件列表和类型统计
    
    Returns:
        {
            "files": [{"path": "...", "name": "...", "pretype": "..."}],
            "summary": {"火车票": 2, "打车发票": 3, ...}
        }
    """
    scanner = FileScanner(directory)
    files = scanner.scan()
    
    return {
        "files": [
            {"path": f.path, "name": f.name, "pretype": f.pretype.value}
            for f in files
        ],
        "summary": scanner.get_summary()
    }


def generate_filename(
    ticket_type: str,
    date: str,
    amount: str,
    invoice_no: str = "",
    seller: str = "",
    person: str = "",
    original_name: str = ""
) -> str:
    """
    根据票据信息生成标准化文件名
    
    Args:
        ticket_type: 票据类型（火车票/打车发票/行程单/酒店发票/飞机票）
        date: 日期（YYYYMMDD）
        amount: 金额
        invoice_no: 发票号码
        seller: 销售方
        person: 乘客姓名（火车票用）
        original_name: 原始文件名（用于获取扩展名）
    """
    type_map = {
        "火车票": TicketType.TRAIN,
        "打车发票": TicketType.DIDI,
        "行程单": TicketType.TRIP,
        "酒店发票": TicketType.HOTEL,
        "飞机票": TicketType.FLIGHT,
    }
    
    from models import TicketInfo
    ticket = TicketInfo(
        file_type=type_map.get(ticket_type, TicketType.UNKNOWN),
        date=date,
        amount=amount,
        invoice_no=invoice_no,
        seller=seller,
        person=person,
        original_name=original_name,
    )
    
    namer = FileNamer(".")
    return namer.generate_name(ticket)


def generate_excel_report(tickets: list, output_dir: str, filename: str = "报销汇总.xlsx") -> str:
    """
    生成 Excel 汇总报表
    
    Args:
        tickets: 票据列表，每个元素:
            {
                "type": "火车票",
                "original_name": "xxx.pdf",
                "new_name": "张三-20240327-533-中国铁路.pdf",
                "date": "20240327",
                "invoice_no": "",
                "amount": "533",
                "seller": "",
                "person": "张三",
                "status": "success"
            }
    """
    from models import TicketInfo
    
    type_map = {
        "火车票": TicketType.TRAIN,
        "打车发票": TicketType.DIDI,
        "行程单": TicketType.TRIP,
        "酒店发票": TicketType.HOTEL,
        "飞机票": TicketType.FLIGHT,
    }
    
    status_map = {
        "success": ProcessStatus.SUCCESS,
        "pending": ProcessStatus.PENDING,
        "error": ProcessStatus.ERROR,
    }
    
    ticket_list = []
    for t in tickets:
        ticket = TicketInfo(
            file_type=type_map.get(t.get("type", ""), TicketType.UNKNOWN),
            original_name=t.get("original_name", ""),
            new_name=t.get("new_name", ""),
            date=t.get("date", ""),
            invoice_no=t.get("invoice_no", ""),
            amount=t.get("amount", ""),
            seller=t.get("seller", ""),
            person=t.get("person", ""),
            status=status_map.get(t.get("status", ""), ProcessStatus.PENDING),
        )
        ticket_list.append(ticket)
    
    reporter = ReportGenerator(output_dir)
    return reporter.generate_excel(ticket_list, filename)


def check_config() -> dict:
    """检查配置状态"""
    config = get_config()
    return {
        "configured": is_configured(),
        "company_name": config.get("company_name", ""),
        "person_name": config.get("person_name", ""),
        "output_dir": config.get("output_dir", ""),
    }


def update_config(company_name: str = None, person_name: str = None, output_dir: str = None) -> dict:
    """更新配置"""
    config = get_config()
    if company_name is not None:
        config["company_name"] = company_name
    if person_name is not None:
        config["person_name"] = person_name
    if output_dir is not None:
        config["output_dir"] = output_dir
    save_config(config)
    return config


# CLI 入口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python main.py scan <目录>")
        print("  python main.py config")
        print("  python main.py name <类型> <日期> <金额> [发票号] [销售方] [姓名] [原文件名]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "scan":
        if len(sys.argv) < 3:
            print("请提供目录路径")
            sys.exit(1)
        result = scan_directory(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "config":
        result = check_config()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "name":
        if len(sys.argv) < 5:
            print("用法: python main.py name <类型> <日期> <金额> [发票号] [销售方] [姓名] [原文件名]")
            sys.exit(1)
        result = generate_filename(
            sys.argv[2], sys.argv[3], sys.argv[4],
            sys.argv[5] if len(sys.argv) > 5 else "",
            sys.argv[6] if len(sys.argv) > 6 else "",
            sys.argv[7] if len(sys.argv) > 7 else "",
            sys.argv[8] if len(sys.argv) > 8 else "",
        )
        print(result)
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
