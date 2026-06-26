"""
yinian_zwds_api.py — 一念紫微斗数 FastAPI 后端
四层深度解盘 + RESTful API + 多语言出海

Author: 崽儿虾 🦞
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skill", "scripts"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

from ai_reader_v2 import generate_standard_report
from formats import STAR_ENCYCLOPEDIA, get_star_info

app = FastAPI(
    title="一念紫微斗数 API v3 (Yinian ZWDS)",
    description="四层深度AI紫微斗数排盘解盘系统（基础→进阶→高阶→专业）｜多模型支持",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BirthInput(BaseModel):
    date: str = Field(..., description="出生日期，如 2000-8-16")
    hour: int = Field(..., ge=0, le=23, description="出生时辰，0-23")
    gender: str = Field(..., description="性别：男/女/male/female")
    is_lunar: bool = False
    is_lunar_leap: bool = False
    language: str = "zh-CN"
    school: str = "综合"
    depth: str = "deep"
    target_year: Optional[int] = None
    model_type: str = "auto"  # auto / claude / gpt / deepseek


@app.get("/")
def root():
    return {
        "name": "一念紫微斗数 API v2",
        "version": "2.0.0",
        "schools": ["三合", "飞星", "占验", "综合"],
        "features": [
            "基础层：12宫 + 主辅星 + 空宫",
            "进阶层：四化飞星 + 格局识别 + 六亲联动",
            "高阶层：大限流年 + 叠宫",
            "专业层：来因宫 + 体用宫 + 星曜互涉",
        ],
        "endpoints": {
            "reading": "POST /api/reading",
            "help": "/help",
        }
    }


@app.post("/api/reading")
def get_reading(input: BirthInput):
    """排盘 + 四层AI深度解盘 + 多模型支持"""
    gender_mapped = "男" if input.gender.lower() in ["男", "male", "m"] else "女"

    result = generate_standard_report(
        date_str=input.date,
        hour=input.hour,
        gender=gender_mapped,
        is_lunar=input.is_lunar,
        target_year=input.target_year,
        model_type=input.model_type,
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "解盘失败"))

    return {
        "success": True,
        "chart_json": result["chart_json"],
        "ai_prompt": result["ai_prompt"],
        "system_prompt": result["system_prompt"],
        "model_type": result["model_type"],
        "stats": {
            "prompt_length": len(result["ai_prompt"]),
        },
    }


@app.get("/api/star/{star_name}")
def get_star(star_name: str):
    info = get_star_info(star_name)
    if info:
        return {"name": star_name, "description": info}
    return {"error": f"未知星曜: {star_name}"}


@app.get("/help")
def api_help():
    return {
        "version": "3.0.0",
        "features": {
            "basic": "逐宫解读（主星+辅星+亮度+空宫+三方四正）",
            "advanced": "四化飞星 + 格局识别 + 六亲联动",
            "timing": "大限十年运 + 流年",
            "professional": "来因宫 + 体用宫 + 煞星分布 + 三派综合",
        },
        "models": ["auto", "claude", "gpt", "deepseek"],
        "schema": {
            "date": "出生日期 YYYY-MM-DD",
            "hour": "时辰 0-23",
            "gender": "男/女/male/female",
            "model_type": "auto/claude/gpt/deepseek",
            "target_year": "可选，目标年份",
        },
        "example": {
            "date": "1984-6-22",
            "hour": 6,
            "gender": "男",
            "model_type": "auto",
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
