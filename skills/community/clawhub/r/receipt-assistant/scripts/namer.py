"""文件命名器 - 根据命名规则生成新文件名"""
import os
import shutil
from pathlib import Path
from typing import Optional

try:
    from .config import COMPANY_NAME, NAMING_RULES
    from .models import TicketInfo, TicketType, ProcessStatus
except ImportError:
    from config import COMPANY_NAME, NAMING_RULES
    from models import TicketInfo, TicketType, ProcessStatus


class FileNamer:
    """文件命名器"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_name(self, ticket: TicketInfo) -> str:
        """根据票据信息和类型生成新文件名"""
        ticket_type = ticket.file_type

        if ticket_type == TicketType.TRAIN:
            return self._generate_train_name(ticket)
        elif ticket_type == TicketType.DIDI:
            return self._generate_didi_name(ticket)
        elif ticket_type == TicketType.TRIP:
            return self._generate_trip_name(ticket)
        elif ticket_type == TicketType.HOTEL:
            return self._generate_hotel_name(ticket)
        elif ticket_type == TicketType.FLIGHT:
            return self._generate_flight_name(ticket)
        else:
            return ticket.original_name

    def _generate_train_name(self, ticket: TicketInfo) -> str:
        """火车票命名: {person}-{date}-{amount}-中国铁路"""
        person = ticket.person or "未知"
        date = ticket.date or "未知"
        amount = ticket.amount or "未知"
        ext = Path(ticket.original_name).suffix
        return f"{person}-{date}-{amount}-中国铁路{ext}"

    def _generate_didi_name(self, ticket: TicketInfo) -> str:
        """打车发票命名: {company}-{date}-{invoice_no}-{amount}-{seller}-发票"""
        company = COMPANY_NAME
        date = ticket.date or "未知"
        invoice_no = ticket.invoice_no or "未知"
        amount = ticket.amount or "未知"
        seller = ticket.seller or "未知"
        ext = Path(ticket.original_name).suffix
        return f"{company}-{date}-{invoice_no}-{amount}-{seller}-发票{ext}"

    def _generate_trip_name(self, ticket: TicketInfo) -> str:
        """行程单命名: {company}-{date}-{invoice_no}-{amount}-{seller}-行程单"""
        company = COMPANY_NAME
        date = ticket.date or "未知"
        invoice_no = ticket.invoice_no or "未知"
        amount = ticket.amount or "未知"
        seller = ticket.seller or "未知"
        ext = Path(ticket.original_name).suffix
        return f"{company}-{date}-{invoice_no}-{amount}-{seller}-行程单{ext}"

    def _generate_hotel_name(self, ticket: TicketInfo) -> str:
        """酒店发票命名: {company}-{date}-{invoice_no}-{amount}-{seller}"""
        company = COMPANY_NAME
        date = ticket.date or "未知"
        invoice_no = ticket.invoice_no or "未知"
        amount = ticket.amount or "未知"
        seller = ticket.seller or "未知"
        ext = Path(ticket.original_name).suffix
        return f"{company}-{date}-{invoice_no}-{amount}-{seller}{ext}"

    def _generate_flight_name(self, ticket: TicketInfo) -> str:
        """机票命名: {company}-{date}-{invoice_no}-{amount}-{seller}-机票"""
        company = COMPANY_NAME
        date = ticket.date or "未知"
        invoice_no = ticket.invoice_no or "未知"
        amount = ticket.amount or "未知"
        seller = ticket.seller or "未知"
        ext = Path(ticket.original_name).suffix
        return f"{company}-{date}-{invoice_no}-{amount}-{seller}-机票{ext}"

    def rename_file(self, ticket: TicketInfo, create_subdir: bool = True) -> TicketInfo:
        """重命名并移动文件"""
        if ticket.status != ProcessStatus.SUCCESS:
            return ticket

        # 生成新文件名
        new_name = self.generate_name(ticket)
        ticket.new_name = new_name

        # 确定输出子目录
        if create_subdir:
            type_dir = self.output_dir / ticket.file_type.value
            type_dir.mkdir(parents=True, exist_ok=True)
            output_path = type_dir / new_name
        else:
            output_path = self.output_dir / new_name

        # 处理文件名冲突
        if output_path.exists():
            base_name = Path(new_name).stem
            ext = Path(new_name).suffix
            counter = 1
            while output_path.exists():
                new_name = f"{base_name}_{counter}{ext}"
                output_path = (type_dir if create_subdir else self.output_dir) / new_name
                counter += 1
            ticket.new_name = new_name

        # 复制文件（原文件保留）
        try:
            shutil.copy2(ticket.original_path, output_path)
            ticket.new_path = str(output_path)
        except Exception as e:
            ticket.status = ProcessStatus.ERROR
            ticket.error_msg = f"文件复制失败: {str(e)}"

        return ticket
