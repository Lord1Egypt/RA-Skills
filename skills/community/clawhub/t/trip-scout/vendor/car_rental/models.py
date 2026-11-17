"""
租车网点查询统一数据模型

两平台（神州租车/一嗨租车）输出统一的 StoreInfo 格式。
"""


from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class StoreInfo:
    """租车网点信息（统一格式）"""

    name: str               # 网点名称
    address: str            # 详细地址
    phone: str              # 电话
    work_time: str          # 营业时间
    source: str             # "zuche" | "ehi"
    lat: str | None = None  # 纬度（高德坐标系）
    lon: str | None = None  # 经度（高德坐标系）
    district: str | None = None        # 所属区域
    is_self_service: bool = False      # 是否自助取还
    is_airport: bool = False           # 是否机场网点
    is_train_station: bool = False     # 是否高铁/火车站网点

    def to_dict(self) -> dict:
        return asdict(self)
