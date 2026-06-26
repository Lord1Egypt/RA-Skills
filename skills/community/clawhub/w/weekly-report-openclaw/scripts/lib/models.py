"""Report data models."""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class WeeklyReportItem(BaseModel):
    """A single weekly report item from the API."""

    row_id: str = Field(alias="rowid", description="Row ID")
    create_time: Optional[str] = Field(default=None, alias="ctime", description="Creation time")
    owner_id: Optional[str] = Field(default=None, alias="ownerid", description="Owner ID")
    owner_name: Optional[str] = Field(default=None, description="Owner name")

    class Config:
        populate_by_name = True
        extra = "allow"


class WeeklyReportData(BaseModel):
    """Collection of weekly report data."""

    items: List[WeeklyReportItem] = Field(default_factory=list, description="Report items")
    total_count: int = Field(default=0, description="Total number of items")

    def is_empty(self) -> bool:
        """Check if there are any items."""
        return len(self.items) == 0


class DateRange(BaseModel):
    """A date range for the report."""

    start_date: date = Field(description="Start date (Monday)")
    end_date: date = Field(description="End date (Sunday)")

    def __str__(self) -> str:
        return f"{self.start_date.strftime('%Y.%m.%d')}-{self.end_date.strftime('%Y.%m.%d')}"

    def to_chinese_format(self) -> str:
        """Return date range in Chinese format for document title."""
        return f"{self.start_date.year}年{self.start_date.month}月{self.start_date.day}日-{self.end_date.month}月{self.end_date.day}日"


class CategoryItem(BaseModel):
    """A single item in a category."""

    content: str = Field(description="工作内容")
    person: str = Field(default="", description="人员姓名")


class WorkCategories(BaseModel):
    """Work categories for weekly report."""

    人才转型: List[CategoryItem] = Field(default_factory=list)
    自主开发: List[CategoryItem] = Field(default_factory=list)
    科创支撑: List[CategoryItem] = Field(default_factory=list)
    AI架构及网运安全自智规划: List[CategoryItem] = Field(default_factory=list)
    系统需求规划建设: List[CategoryItem] = Field(default_factory=list)
    综合工作: List[CategoryItem] = Field(default_factory=list)


class SummarizedReport(BaseModel):
    """AI-summarized report content."""

    week_range: DateRange = Field(description="Date range of the report")
    team_name: str = Field(description="Team name")

    this_week: WorkCategories = Field(default_factory=WorkCategories, description="本周工作")
    next_week: WorkCategories = Field(default_factory=WorkCategories, description="下周计划")

    overview: str = Field(default="", description="本周工作概述")
    issues: str = Field(default="", description="遇到的问题")

    completed_tasks: List[str] = Field(default_factory=list, description="主要完成事项")
    next_week_plan: str = Field(default="", description="下周计划")

    raw_items_count: int = Field(default=0, description="Number of raw items processed")

    def to_template_context(self) -> dict:
        """Convert to template context for docx generation."""
        context = {
            "week_range": str(self.week_range),
            "week_range_cn": self.week_range.to_chinese_format(),
            "team_name": self.team_name,
            "overview": self.overview,
            "issues": self.issues,
            "report_date": self.week_range.end_date.strftime("%Y年%m月%d日"),
            "completed_tasks": self.completed_tasks,
            "next_week_plan": self.next_week_plan,
        }

        category_names = ["人才转型", "自主开发", "科创支撑", "AI架构及网运安全自智规划", "系统需求规划建设", "综合工作"]

        for category_name in category_names:
            items = getattr(self.this_week, category_name, [])
            context[f"this_week_{category_name}"] = items
            context[f"this_week_{category_name}_numbered"] = [
                {"num": i + 1, "content": item.content, "person": item.person}
                for i, item in enumerate(items)
            ]

        for category_name in category_names:
            items = getattr(self.next_week, category_name, [])
            context[f"next_week_{category_name}"] = items
            context[f"next_week_{category_name}_numbered"] = [
                {"num": i + 1, "content": item.content, "person": item.person}
                for i, item in enumerate(items)
            ]

        return context
