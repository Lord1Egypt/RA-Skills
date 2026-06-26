"""AI content summarizer module."""

import json
from typing import List, Optional

from .config import Settings
from .llm_client import BaseLLMClient, create_llm_client
from .models import WeeklyReportData, SummarizedReport, DateRange, WorkCategories, CategoryItem
from .date_utils import get_week_range

# System prompt for summarization
SYSTEM_PROMPT = """你是一个专业的工作周报总结助手。你的任务是将员工提交的周报内容进行提炼和总结，生成一份结构清晰、内容精炼的周报汇总。

工作分类说明：
- 人才转型：AI培训、技能学习、人才培养相关工作
- 自主开发：自主开发的应用、工具、系统相关工作
- 科创支撑：专利申报、创新项目支撑、科创制度相关工作
- AI架构及网运安全自智规划：AI架构规划、监控智能化、态势感知相关工作
- 系统需求规划建设：系统需求分析、平台建设、系统规划相关工作
- 综合工作：日常运维、综合事务、其他工作

输出要求：
1. 语言简洁专业，使用"①...②...③..."格式列出具体工作
2. 突出重点工作和成果
3. 按人员分组，每人一条记录
4. 每条记录末尾标注"--人员姓名"

请严格按照指定的JSON格式输出，不要添加任何额外的文字说明。"""

# User prompt template
USER_PROMPT_TEMPLATE = """请根据以下员工周报原始数据，生成一份科创团队周报总结。

## 团队信息
- 团队名称：{team_name}
- 周报时间：{week_range}
- 提交数量：{item_count}条

## 原始周报数据
{raw_data}

## 输出要求
请严格按照以下JSON格式输出总结结果，每个分类下按人员列出工作内容：

```json
{{
    "this_week": {{
        "人才转型": [
            {{"content": "①工作内容1；②工作内容2；③工作内容3。--张三", "person": "张三"}},
            {{"content": "①工作内容1；②工作内容2。--李四", "person": "李四"}}
        ],
        "自主开发": [
            {{"content": "①工作内容1；②工作内容2。--王五", "person": "王五"}}
        ],
        "科创支撑": [],
        "AI架构及网运安全自智规划": [],
        "系统需求规划建设": [],
        "综合工作": []
    }},
    "next_week": {{
        "人才转型": [],
        "自主开发": [],
        "科创支撑": [],
        "AI架构及网运安全自智规划": [],
        "系统需求规划建设": [],
        "综合工作": []
    }},
    "overview": "本周工作概述（2-3句话概括本周主要工作内容）",
    "issues": "遇到的问题（如果没有重大问题，写'本周工作进展顺利，无重大问题'）"
}}
```

注意：
1. 根据实际工作内容归类到对应的分类中
2. 如果某个分类没有相关工作，保持空数组[]
3. 工作内容要精炼，使用"①...②...③..."格式
4. 每条内容末尾必须标注"--人员姓名"
5. this_week是本周已完成的工作，next_week是下周计划的工作
6. 保持原始周报中人员姓名的准确性"""


class ReportSummarizer:
    """Summarizes weekly report data using LLM."""

    def __init__(
        self,
        settings: Settings,
        llm_client: Optional[BaseLLMClient] = None,
    ):
        self.settings = settings
        self.llm_client = llm_client or create_llm_client(settings=settings)

    def _format_raw_data(self, data: WeeklyReportData) -> str:
        """Format raw report data for the LLM prompt."""
        if data.is_empty():
            return "暂无周报数据"

        team_members = self.settings.defaults.team_members

        formatted_items = []
        filtered_count = 0
        for i, item in enumerate(data.items, 1):
            item_dict = item.model_dump(by_alias=True)

            # Get owner name from ownerid field
            owner_name = ""
            ownerid_raw = item_dict.get("ownerid", "")
            if ownerid_raw:
                try:
                    ownerid_data = json.loads(ownerid_raw)
                    if isinstance(ownerid_data, list) and len(ownerid_data) > 0:
                        owner_name = ownerid_data[0].get("fullname", "")
                except (json.JSONDecodeError, TypeError):
                    pass

            # Filter out non-team members
            if owner_name and owner_name not in team_members:
                filtered_count += 1
                continue

            item_str = f"### 周报 {i}\n"

            for key, value in item_dict.items():
                if value and key not in ("rowid", "row_id", "ctime", "ownerid"):
                    display_key = key.replace("_", " ").title()
                    item_str += f"- {display_key}: {value}\n"

            formatted_items.append(item_str)

        if filtered_count > 0:
            print(f"[Summarizer] Filtered out {filtered_count} items from non-team members")

        if not formatted_items:
            return "暂无周报数据"

        return "\n\n".join(formatted_items)

    def _parse_llm_response(self, response: str) -> dict:
        """Parse the LLM response to extract structured data."""
        response = response.strip()

        # Remove markdown code blocks if present
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()

        try:
            parsed = json.loads(response)
            return parsed
        except json.JSONDecodeError:
            print("[Summarizer] Warning: Could not parse LLM response as JSON")
            return {
                "this_week": {},
                "next_week": {},
                "overview": response,
                "completed_tasks": [],
                "issues": "无法解析详细信息",
                "next_week_plan": "",
            }

    def _build_work_categories(self, data: dict, key: str) -> WorkCategories:
        """Build WorkCategories from parsed data."""
        categories = WorkCategories()
        category_data = data.get(key, {})

        category_names = ["人才转型", "自主开发", "科创支撑", "AI架构及网运安全自智规划", "系统需求规划建设", "综合工作"]

        for cat_name in category_names:
            items_data = category_data.get(cat_name, [])
            items = []
            for item_data in items_data:
                if isinstance(item_data, dict):
                    items.append(CategoryItem(
                        content=item_data.get("content", ""),
                        person=item_data.get("person", "")
                    ))
                elif isinstance(item_data, str):
                    content = item_data
                    person = ""
                    if "--" in content:
                        parts = content.rsplit("--", 1)
                        content = parts[0].strip()
                        person = parts[1].strip() if len(parts) > 1 else ""
                    items.append(CategoryItem(content=content, person=person))

            setattr(categories, cat_name, items)

        return categories

    async def summarize(
        self,
        data: WeeklyReportData,
        team_name: Optional[str] = None,
        week_range: Optional[DateRange] = None,
        verbose: bool = True,
    ) -> SummarizedReport:
        """Summarize the weekly report data."""
        if data.is_empty():
            if verbose:
                print("[Summarizer] No data to summarize")
            if week_range is None:
                start, end = get_week_range()
                week_range = DateRange(start_date=start, end_date=end)

            return SummarizedReport(
                week_range=week_range,
                team_name=team_name or self.settings.defaults.team,
                overview="本周暂无周报数据",
                completed_tasks=[],
                issues="",
                next_week_plan="",
                raw_items_count=0,
            )

        if verbose:
            print("[Summarizer] Summarizing report data with AI...")

        team_name = team_name or self.settings.defaults.team
        if week_range is None:
            start, end = get_week_range()
            week_range = DateRange(start_date=start, end_date=end)

        raw_data = self._format_raw_data(data)

        prompt = USER_PROMPT_TEMPLATE.format(
            team_name=team_name,
            week_range=str(week_range),
            item_count=len(data.items),
            raw_data=raw_data,
        )

        response = await self.llm_client.complete(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            temperature=self.settings.llm.temperature,
            max_tokens=self.settings.llm.max_tokens,
        )

        parsed = self._parse_llm_response(response)

        this_week = self._build_work_categories(parsed, "this_week")
        next_week = self._build_work_categories(parsed, "next_week")

        summary = SummarizedReport(
            week_range=week_range,
            team_name=team_name,
            this_week=this_week,
            next_week=next_week,
            overview=parsed.get("overview", ""),
            completed_tasks=parsed.get("completed_tasks", []),
            issues=parsed.get("issues", ""),
            next_week_plan=parsed.get("next_week_plan", ""),
            raw_items_count=len(data.items),
        )

        if verbose:
            print("[Summarizer] Report summarized successfully")

        return summary


async def summarize_reports(
    data: WeeklyReportData,
    settings: Settings,
    team_name: Optional[str] = None,
    week_range: Optional[DateRange] = None,
    verbose: bool = True,
) -> SummarizedReport:
    """Convenience function to summarize reports."""
    summarizer = ReportSummarizer(settings)
    return await summarizer.summarize(data, team_name, week_range, verbose)
