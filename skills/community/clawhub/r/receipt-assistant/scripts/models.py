"""数据模型定义"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


class TicketType(Enum):
    """票据类型枚举"""
    TRAIN = "火车票"
    DIDI = "打车发票"
    TRIP = "行程单"
    HOTEL = "酒店发票"
    FLIGHT = "飞机票"
    RESTAURANT = "餐饮发票"
    UNKNOWN = "未知"


class ProcessStatus(Enum):
    """处理状态"""
    SUCCESS = "success"
    PENDING = "pending"
    ERROR = "error"


@dataclass
class TicketInfo:
    """票据信息"""
    file_type: TicketType = TicketType.UNKNOWN
    original_name: str = ""
    original_path: str = ""
    new_name: str = ""
    new_path: str = ""

    # 提取的信息
    date: str = ""                    # 开票日期 (YYYYMMDD)
    amount: str = ""                   # 金额（小写）
    invoice_no: str = ""              # 发票号码
    seller: str = ""                  # 销售方名称
    buyer: str = ""                   # 购买方（公司名）
    person: str = ""                  # 乘客/旅客姓名（火车票）

    # 处理状态
    status: ProcessStatus = ProcessStatus.PENDING
    error_msg: str = ""

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "票据类型": self.file_type.value,
            "原始文件名": self.original_name,
            "新文件名": self.new_name,
            "开票日期": self.date,
            "发票号码": self.invoice_no,
            "金额": self.amount,
            "销售方": self.seller,
            "购买方": self.buyer,
            "乘客/旅客": self.person,
            "状态": self.status.value,
            "错误信息": self.error_msg,
        }


@dataclass
class Summary:
    """汇总统计"""
    total_count: int = 0
    success_count: int = 0
    pending_count: int = 0
    error_count: int = 0
    total_amount: float = 0.0
    type_counts: Dict[str, int] = field(default_factory=dict)

    def add_ticket(self, ticket: TicketInfo):
        """添加票据并更新统计"""
        self.total_count += 1

        # 更新状态计数
        if ticket.status == ProcessStatus.SUCCESS:
            self.success_count += 1
        elif ticket.status == ProcessStatus.PENDING:
            self.pending_count += 1
        elif ticket.status == ProcessStatus.ERROR:
            self.error_count += 1

        # 更新金额
        try:
            amount = float(ticket.amount) if ticket.amount else 0
            self.total_amount += amount
        except ValueError:
            pass

        # 更新类型计数
        type_name = ticket.file_type.value
        self.type_counts[type_name] = self.type_counts.get(type_name, 0) + 1
