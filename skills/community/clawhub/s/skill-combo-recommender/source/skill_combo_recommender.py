#!/usr/bin/env python3
"""
Skill Combo Recommender - 技能组合推荐器
根据用户任务推荐最佳技能组合和工作流程
"""

import argparse
import json
from typing import List, Dict, Set, Tuple


# 技能数据库
SKILLS = {
    # 内容创作
    "xiaohongshu-content": {
        "name": "xiaohongshu-content",
        "description": "小红书爆款内容创作",
        "tags": ["content-creation", "xiaohongshu", "social-media"],
        "examples": ["生成小红书爆款笔记", "创作种草文案"]
    },
    "content-researcher": {
        "name": "content-researcher",
        "description": "内容研究员 - 搜索+总结+素材库",
        "tags": ["content-creation", "research", "ai"],
        "examples": ["调研热门话题", "搜集素材"]
    },
    "social-publisher": {
        "name": "social-publisher",
        "description": "多平台内容发布工具",
        "tags": ["content-creation", "publishing", "multi-platform"],
        "examples": ["发布到小红书", "发布到知乎"]
    },
    "ai-content-tailor": {
        "name": "ai-content-tailor",
        "description": "多平台内容裁剪工具",
        "tags": ["content-creation", "formatting", "ai"],
        "examples": ["裁剪为小红书版本", "裁剪为公众号版本"]
    },
    "wechat-formatter": {
        "name": "wechat-formatter",
        "description": "Markdown转公众号格式",
        "tags": ["content-creation", "formatting", "wechat"],
        "examples": ["格式化公众号文章", "转换Markdown"]
    },
    
    # 视频制作
    "video-generate": {
        "name": "video-generate",
        "description": "AI视频生成工具",
        "tags": ["video", "ai", "generation"],
        "examples": ["生成解说视频", "制作短视频"]
    },
    "video-frames": {
        "name": "video-frames",
        "description": "从视频中提取帧",
        "tags": ["video", "processing"],
        "examples": ["提取视频缩略图", "生成预览图"]
    },
    "auto-subtitle": {
        "name": "auto-subtitle",
        "description": "视频自动字幕生成器",
        "tags": ["video", "subtitle", "ai"],
        "examples": ["生成SRT字幕", "添加字幕"]
    },
    "text-to-podcast": {
        "name": "text-to-podcast",
        "description": "文本转播客音频（使用TTS）",
        "tags": ["audio", "tts", "podcast"],
        "examples": ["生成播客音频", "文本转语音"]
    },
    
    # 数据分析
    "stock-analyzer": {
        "name": "stock-analyzer",
        "description": "股票分析工具",
        "tags": ["data-analysis", "finance", "stock"],
        "examples": ["分析股票走势", "预测股价"]
    },
    "data-chart-tool": {
        "name": "data-chart-tool",
        "description": "数据可视化工具",
        "tags": ["data-analysis", "visualization"],
        "examples": ["生成柱状图", "生成折线图"]
    },
    "tushare-finance": {
        "name": "tushare-finance",
        "description": "中国金融市场数据",
        "tags": ["data-analysis", "finance", "api"],
        "examples": ["获取股票数据", "查询财务报表"]
    },
    
    # 文件管理
    "batch-renamer": {
        "name": "batch-renamer",
        "description": "批量文件重命名工具",
        "tags": ["file-management", "batch"],
        "examples": ["批量重命名", "按模式命名"]
    },
    "photo-organizer": {
        "name": "photo-organizer",
        "description": "照片批量整理工具",
        "tags": ["file-management", "photo"],
        "examples": ["整理照片", "按时间分类"]
    },
    "download-organizer": {
        "name": "download-organizer",
        "description": "下载文件自动分类工具",
        "tags": ["file-management", "automation"],
        "examples": ["整理下载文件夹", "自动分类"]
    },
    "video-organizer": {
        "name": "video-organizer",
        "description": "视频文件批量重命名和整理工具",
        "tags": ["file-management", "video"],
        "examples": ["整理视频", "按格式分类"]
    },
    "music-tagger": {
        "name": "music-tagger",
        "description": "音乐文件批量标签工具",
        "tags": ["file-management", "music"],
        "examples": ["编辑音乐标签", "整理音乐"]
    },
    "file-sorter": {
        "name": "file-sorter",
        "description": "通用文件智能分类工具",
        "tags": ["file-management", "sorting"],
        "examples": ["智能分类文件", "整理文件夹"]
    },
    
    # 音频处理
    "audio-note-taker": {
        "name": "audio-note-taker",
        "description": "语音笔记助手",
        "tags": ["audio", "transcription", "ai"],
        "examples": ["录音转文字", "会议纪要"]
    },
    
    # 项目管理
    "skill-composer": {
        "name": "skill-composer",
        "description": "技能工作流编排器",
        "tags": ["workflow", "automation", "composition"],
        "examples": ["编排技能工作流", "自动化流程"]
    },
    "social-media-scheduler": {
        "name": "social-media-scheduler",
        "description": "社交媒体排期发布器",
        "tags": ["workflow", "social-media", "scheduling"],
        "examples": ["排期发布", "定时发布"]
    },
    "email-ai-assistant": {
        "name": "email-ai-assistant",
        "description": "AI邮箱助手",
        "tags": ["workflow", "email", "ai"],
        "examples": ["优先级收件箱", "邮件分类"]
    },
    
    # AI 工具
    "summarize": {
        "name": "summarize",
        "description": "快速总结 URL/文件/YouTube",
        "tags": ["ai", "summarization"],
        "examples": ["总结文章", "总结视频"]
    },
    "openai-image-gen": {
        "name": "openai-image-gen",
        "description": "OpenAI图像批量生成",
        "tags": ["ai", "image", "generation"],
        "examples": ["生成图片", "批量生成"]
    },
    "openai-whisper": {
        "name": "openai-whisper",
        "description": "本地语音转文字",
        "tags": ["ai", "audio", "transcription"],
        "examples": ["转写音频", "语音识别"]
    },
    "xiaohongshu-image-gen": {
        "name": "xiaohongshu-image-gen",
        "description": "小红书图片生成技能",
        "tags": ["ai", "image", "xiaohongshu"],
        "examples": ["生成小红书配图", "家装图片"]
    },
    "xiaohongshu-proxy-manager": {
        "name": "xiaohongshu-proxy-manager",
        "description": "小红书多账号代理池管理",
        "tags": ["proxy", "xiaohongshu", "multi-account"],
        "examples": ["管理代理池", "IP隔离"]
    },
}


# 预设工作流
WORKFLOWS = {
    "xiaohongshu-ops": {
        "name": "小红书运营全流程",
        "description": "完整的小红书账号运营工作流",
        "skills": ["xiaohongshu-content", "xiaohongshu-image-gen", "xiaohongshu-proxy-manager", "social-media-scheduler"],
        "steps": [
            "1. 使用 xiaohongshu-content 生成爆款内容",
            "2. 使用 xiaohongshu-image-gen 生成配图",
            "3. 使用 xiaohongshu-proxy-manager 设置代理IP",
            "4. 使用 social-media-scheduler 排期发布"
        ]
    },
    "content-creation": {
        "name": "内容创作流水线",
        "description": "高效的多平台内容创作工作流",
        "skills": ["content-researcher", "ai-content-tailor", "social-publisher", "wechat-formatter"],
        "steps": [
            "1. 使用 content-researcher 调研热门话题",
            "2. 使用 ai-content-tailor 裁剪为多平台版本",
            "3. 使用 wechat-formatter 格式化公众号版本",
            "4. 使用 social-publisher 发布到各平台"
        ]
    },
    "video-production": {
        "name": "视频内容制作",
        "description": "完整的视频内容制作工作流",
        "skills": ["video-generate", "video-frames", "auto-subtitle", "text-to-podcast"],
        "steps": [
            "1. 使用 video-generate 生成视频",
            "2. 使用 video-frames 提取关键帧",
            "3. 使用 auto-subtitle 生成字幕",
            "4. 使用 text-to-podcast 生成音频配音"
        ]
    },
    "data-analysis": {
        "name": "数据分析和可视化",
        "description": "数据获取到可视化的完整流程",
        "skills": ["tushare-finance", "stock-analyzer", "data-chart-tool"],
        "steps": [
            "1. 使用 tushare-finance 获取数据",
            "2. 使用 stock-analyzer 分析数据",
            "3. 使用 data-chart-tool 生成图表"
        ]
    },
    "file-organization": {
        "name": "文件整理自动化",
        "description": "批量整理各类文件",
        "skills": ["download-organizer", "photo-organizer", "file-sorter"],
        "steps": [
            "1. 使用 download-organizer 整理下载文件夹",
            "2. 使用 photo-organizer 整理照片",
            "3. 使用 file-sorter 智能分类其他文件"
        ]
    },
    "meeting-workflow": {
        "name": "会议记录自动化",
        "description": "从录音到纪要的完整流程",
        "skills": ["openai-whisper", "audio-note-taker", "ai-content-tailor"],
        "steps": [
            "1. 使用 openai-whisper 转写录音",
            "2. 使用 audio-note-taker 生成结构化纪要",
            "3. 使用 ai-content-tailor 裁剪为不同格式"
        ]
    },
}


# 关键词映射
KEYWORD_MAPPING = {
    # 内容创作
    "小红书": ["xiaohongshu-content", "xiaohongshu-image-gen", "xiaohongshu-proxy-manager", "social-media-scheduler"],
    "内容创作": ["content-researcher", "ai-content-tailor", "social-publisher", "wechat-formatter"],
    "写文章": ["content-researcher", "ai-content-tailor", "wechat-formatter"],
    "公众号": ["wechat-formatter", "social-publisher"],
    "知乎": ["ai-content-tailor", "social-publisher"],
    
    # 视频制作
    "视频": ["video-generate", "video-frames", "auto-subtitle", "text-to-podcast"],
    "字幕": ["auto-subtitle"],
    "配音": ["text-to-podcast"],
    "播客": ["text-to-podcast"],
    
    # 数据分析
    "股票": ["tushare-finance", "stock-analyzer", "data-chart-tool"],
    "数据分析": ["data-chart-tool", "stock-analyzer"],
    "图表": ["data-chart-tool"],
    "可视化": ["data-chart-tool"],
    
    # 文件管理
    "重命名": ["batch-renamer"],
    "整理": ["photo-organizer", "download-organizer", "video-organizer", "file-sorter"],
    "照片": ["photo-organizer"],
    "下载": ["download-organizer"],
    "视频文件": ["video-organizer"],
    "音乐": ["music-tagger"],
    "分类": ["file-sorter"],
    
    # 音频处理
    "录音": ["openai-whisper", "audio-note-taker"],
    "会议": ["audio-note-taker", "ai-content-tailor"],
    "转写": ["openai-whisper", "audio-note-taker"],
    
    # 项目管理
    "工作流": ["skill-composer"],
    "排期": ["social-media-scheduler"],
    "邮件": ["email-ai-assistant"],
    "自动化": ["skill-composer", "social-media-scheduler"],
    
    # AI 工具
    "AI": ["summarize", "openai-image-gen", "openai-whisper"],
    "总结": ["summarize"],
    "图片": ["openai-image-gen", "xiaohongshu-image-gen"],
    "生成": ["openai-image-gen", "video-generate", "text-to-podcast"],
}


def calculate_match_score(skill_key: str, task: str, keywords: Set[str]) -> float:
    """计算技能与任务的匹配分数"""
    score = 0.0
    skill = SKILLS[skill_key]
    
    # 1. 技能名称匹配
    if skill_key in task.lower():
        score += 3.0
    
    # 2. 标签匹配
    for tag in skill["tags"]:
        if tag in task.lower():
            score += 2.0
    
    # 3. 关键词匹配
    for keyword in keywords:
        if keyword in task.lower():
            skill_keywords = KEYWORD_MAPPING.get(keyword, [])
            if skill_key in skill_keywords:
                score += 2.5
    
    # 4. 示例匹配
    for example in skill["examples"]:
        if any(word in task.lower() for word in example.split()):
            score += 1.0
    
    return score


def extract_keywords(task: str) -> Set[str]:
    """从任务描述中提取关键词"""
    keywords = set()
    
    for keyword in KEYWORD_MAPPING.keys():
        if keyword in task.lower():
            keywords.add(keyword)
    
    return keywords


def recommend_skills(task: str, top_n: int = 5) -> List[Tuple[str, float]]:
    """根据任务推荐技能"""
    keywords = extract_keywords(task)
    
    # 计算所有技能的匹配分数
    skill_scores = []
    for skill_key in SKILLS.keys():
        score = calculate_match_score(skill_key, task, keywords)
        if score > 0:
            skill_scores.append((skill_key, score))
    
    # 按分数排序
    skill_scores.sort(key=lambda x: x[1], reverse=True)
    
    # 返回 top_n
    return skill_scores[:top_n]


def generate_workflow(task: str) -> Dict:
    """生成工作流"""
    # 推荐相关技能
    recommended = recommend_skills(task, top_n=5)
    skill_names = [s[0] for s in recommended]
    
    # 查找最匹配的预设工作流
    best_workflow = None
    best_match_score = 0
    
    for wf_key, wf in WORKFLOWS.items():
        match_count = len(set(skill_names) & set(wf["skills"]))
        if match_count > best_match_score:
            best_match_score = match_count
            best_workflow = wf
    
    if best_workflow:
        return {
            "type": "preset",
            "workflow": best_workflow,
            "reason": f"找到匹配的预设工作流：{best_workflow['name']}"
        }
    else:
        return {
            "type": "custom",
            "skills": skill_names,
            "reason": "基于关键词分析推荐"
        }


def print_skill_recommendation(skill_key: str, score: float):
    """打印单个技能推荐"""
    skill = SKILLS[skill_key]
    print(f"\n🎯 {skill['name']} (匹配度: {score:.1f})")
    print(f"   描述: {skill['description']}")
    print(f"   标签: {', '.join(skill['tags'])}")
    if skill['examples']:
        print(f"   示例: {', '.join(skill['examples'][:2])}")


def print_workflow(workflow_result: Dict):
    """打印工作流"""
    if workflow_result["type"] == "preset":
        wf = workflow_result["workflow"]
        print(f"\n🚀 推荐工作流: {wf['name']}")
        print(f"   描述: {wf['description']}")
        print(f"   涉及技能: {', '.join(wf['skills'])}")
        print(f"\n   步骤:")
        for step in wf["steps"]:
            print(f"   {step}")
    else:
        skills = workflow_result["skills"]
        print(f"\n🚀 自定义工作流")
        print(f"   推荐技能: {', '.join(skills)}")
        print(f"   {workflow_result['reason']}")


def main():
    parser = argparse.ArgumentParser(description="技能组合推荐器")
    parser.add_argument("--task", "-t", help="任务描述（推荐技能组合）")
    parser.add_argument("--list-skills", "-l", action="store_true", help="列出所有技能")
    parser.add_argument("--list-workflows", "-w", action="store_true", help="列出所有预设工作流")
    parser.add_argument("--workflow", "-f", help="使用特定的工作流")
    parser.add_argument("--top", "-n", type=int, default=5, help="返回的推荐技能数量（默认: 5）")
    parser.add_argument("--output", "-o", choices=["markdown", "json"], help="输出格式")
    
    args = parser.parse_args()
    
    # 列出所有技能
    if args.list_skills:
        print("📚 所有可用技能：\n")
        for key, skill in SKILLS.items():
            print(f"• {skill['name']}: {skill['description']}")
            print(f"  标签: {', '.join(skill['tags'])}\n")
        return
    
    # 列出所有工作流
    if args.list_workflows:
        print("🚀 所有预设工作流：\n")
        for key, wf in WORKFLOWS.items():
            print(f"• {wf['name']}: {wf['description']}")
            print(f"  技能: {', '.join(wf['skills'])}\n")
        return
    
    # 使用特定工作流
    if args.workflow:
        for key, wf in WORKFLOWS.items():
            if wf["name"] == args.workflow or key == args.workflow:
                print_workflow({"type": "preset", "workflow": wf})
                return
        print(f"❌ 未找到工作流: {args.workflow}")
        print("使用 --list-workflows 查看所有可用工作流")
        return
    
    # 推荐技能组合
    if args.task:
        print(f"🎯 任务: {args.task}")
        print("=" * 60)
        
        # 推荐技能
        print("\n📋 推荐技能:")
        recommendations = recommend_skills(args.task, top_n=args.top)
        for skill_key, score in recommendations:
            print_skill_recommendation(skill_key, score)
        
        # 生成工作流
        print("\n" + "=" * 60)
        workflow_result = generate_workflow(args.task)
        print_workflow(workflow_result)
        
        # JSON 输出
        if args.output == "json":
            output_data = {
                "task": args.task,
                "recommendations": [
                    {
                        "skill": skill_key,
                        "score": score,
                        "info": SKILLS[skill_key]
                    }
                    for skill_key, score in recommendations
                ],
                "workflow": workflow_result
            }
            print(f"\n📄 JSON输出:")
            print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
