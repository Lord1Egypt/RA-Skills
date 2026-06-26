#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TechRecruiter Pro - 技术人员招聘专家
专门针对算法工程师和研发工程师的智能化招聘助手

注意：数据持久化路径可通过环境变量配置
默认：当前 skill 目录下的 data/ 文件夹
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import webbrowser

# 配置（支持环境变量覆盖）
# 优先使用环境变量 OPENCLAW_WORKSPACE，否则使用当前脚本所在目录
WORKSPACE = Path(os.getenv("OPENCLAW_WORKSPACE", Path(__file__).parent.parent))
RECRUITER_DIR = Path(__file__).parent
DATA_DIR = RECRUITER_DIR / "data"
TEMPLATES_DIR = RECRUITER_DIR / "templates"

# 确保目录存在（只在目录可写时创建）
try:
    DATA_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)
except (PermissionError, OSError) as e:
    # 如果无法创建目录，使用临时目录
    import tempfile
    DATA_DIR = Path(tempfile.gettempdir()) / "tech-recruiter-pro" / "data"
    TEMPLATES_DIR = Path(tempfile.gettempdir()) / "tech-recruiter-pro" / "templates"
    DATA_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)


class CandidateProfile:
    """候选人画像"""
    
    def __init__(self, name: str):
        self.name = name
        self.current_company: str = ""
        self.current_position: str = ""
        self.research_areas: List[str] = []
        
        # 联系方式
        self.email: str = ""
        self.github: str = ""
        self.google_scholar: str = ""
        self.aminer: str = ""
        self.linkedin: str = ""
        self.twitter: str = ""
        
        # 学术指标
        self.paper_count: int = 0
        self.total_citations: int = 0
        self.h_index: int = 0
        
        # 技术评估
        self.github_repos: List[Dict] = []
        self.top_papers: List[Dict] = []
        self.skills: List[str] = []
        
        # 招聘流程
        self.match_score: int = 0  # 0-100
        self.status: str = "发现"  # 发现/初筛/联系/面试/Offer/入职
        self.priority: str = "中"  # 高/中/低
        self.last_contact: str = ""
        self.next_followup: str = ""
        self.notes: List[str] = []
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "姓名": self.name,
            "当前公司": self.current_company,
            "职位": self.current_position,
            "研究方向": ", ".join(self.research_areas),
            "邮箱": self.email,
            "GitHub": self.github,
            "Google Scholar": self.google_scholar,
            "AMiner": self.aminer,
            "LinkedIn": self.linkedin,
            "论文数": self.paper_count,
            "总引用": self.total_citations,
            "H-index": self.h_index,
            "匹配度": self.match_score,
            "状态": self.status,
            "优先级": self.priority,
            "最后联系": self.last_contact,
            "下次跟进": self.next_followup,
            "备注": "\n".join(self.notes)
        }


class TechRecruiterPro:
    """技术人员招聘专家"""
    
    def __init__(self):
        self.candidates: List[CandidateProfile] = []
        self.templates: Dict[str, str] = {}
        self.load_templates()
    
    def load_templates(self):
        """加载邮件模板"""
        template_file = TEMPLATES_DIR / "email_templates.json"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
        else:
            self.create_default_templates()
    
    def create_default_templates(self):
        """创建默认模板"""
        self.templates = {
            "initial_outreach": self._get_initial_outreach_template(),
            "follow_up_1": self._get_followup_template(1),
            "follow_up_2": self._get_followup_template(2),
            "interview_invite": self._get_interview_invite_template()
        }
        
        # 保存模板
        with open(TEMPLATES_DIR / "email_templates.json", 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, ensure_ascii=False, indent=2)
    
    def _get_initial_outreach_template(self) -> str:
        """初次联系模板"""
        return """主题：[{company}] {position} 机会 - 看到您的{research_area}工作很感兴趣

{name}您好，

我是{company}的{recruiter_name}。

【我为什么联系您】
我最近拜读了您的论文《{paper_title}》({paper_year})，特别是您提出的{method_highlight}让我印象深刻。
您在 GitHub 项目 {github_project} 中的实现也非常精彩，特别是 {project_highlight} 的设计。

【关于我们】
{company} 正在 {research_direction} 方向投入大量资源，目前团队规模 {team_size}，包括 {team_highlights}。

【职位机会】
我们正在招募 {position}，主要负责：
- {job_responsibility_1}
- {job_responsibility_2}
- {job_responsibility_3}

这个岗位需要 {key_skill_1}、{key_skill_2} 等技能，与您的背景非常匹配。

【技术亮点】
- 使用 {tech_stack_1} 进行大规模训练
- {tech_highlight_2}
- {tech_highlight_3}

【下一步】
如果您对这个机会感兴趣，我们可以安排一个 30 分钟的电话沟通，了解更多细节。
您看以下哪个时间方便？
- {time_option_1}
- {time_option_2}
- {time_option_3}

期待您的回复！

祝好，
{recruiter_name}
{title}
{company}
{contact_info}

---
如果您不希望收到此类邮件，请回复"取消"，我会将您从列表中移除。
"""
    
    def _get_followup_template(self, round: int) -> str:
        """跟进模板"""
        if round == 1:
            return """主题：Re: [{company}] {position} 机会

{name}您好，

希望您一切顺利！

上周我给您发了一封关于 {position} 机会的邮件，不知道您是否有时间查看？

我理解您作为研究人员/工程师工作繁忙，如果您对这个机会感兴趣，我们可以找一个您方便的时间简单聊聊。

如果目前不是合适的时机，也请告知，我可以在 {followup_month} 再联系您。

祝好，
{recruiter_name}
"""
        else:
            return """主题：Re: [{company}] {position} 机会 - 最后跟进

{name}您好，

这是我最后一次跟进关于 {position} 的机会。

我理解您可能目前不考虑新的机会，或者对这个职位不感兴趣。

如果您未来改变主意，或者有其他问题，随时可以联系我。

祝您在{current_company}工作顺利！

祝好，
{recruiter_name}
"""
    
    def _get_interview_invite_template(self) -> str:
        """面试邀请模板"""
        return """主题：[{company}] {position} 面试邀请

{name}您好，

很高兴您对我们 {position} 的机会感兴趣！

经过初步沟通，我们想邀请您参加正式的面试流程。

【面试流程】
1. 技术面试 ({duration_1}): {interview_content_1}
2. 系统设计 ({duration_2}): {interview_content_2}
3. 团队匹配 ({duration_3}): {interview_content_3}

【时间安排】
您可以选择以下时间：
- {time_slot_1}
- {time_slot_2}
- {time_slot_3}

或者，您也可以在这个链接选择您方便的时间：{calendar_link}

【面试准备】
- 技术面试：复习{tech_area}相关知识
- 系统设计：准备一个您熟悉的项目
- 团队匹配：准备一些问题了解团队

如有任何问题，请随时联系我。

期待与您的交流！

祝好，
{recruiter_name}
"""
    
    def search_candidates(self, 
                         keywords: List[str],
                         target_companies: List[str] = None,
                         min_citations: int = None,
                         min_h_index: int = None) -> List[CandidateProfile]:
        """
        搜索候选人
        
        Args:
            keywords: 搜索关键词，如 ["RLHF", "PPO", "LLM"]
            target_companies: 目标公司列表
            min_citations: 最小引用数
            min_h_index: 最小 H-index
        
        Returns:
            候选人列表
        """
        print(f"🔍 开始搜索候选人...")
        print(f"   关键词：{', '.join(keywords)}")
        if target_companies:
            print(f"   目标公司：{', '.join(target_companies)}")
        if min_citations:
            print(f"   最小引用：{min_citations}")
        if min_h_index:
            print(f"   最小 H-index: {min_h_index}")
        
        # TODO: 实现搜索逻辑
        # 1. 搜索 AMiner
        # 2. 搜索 Google Scholar
        # 3. 搜索 GitHub
        # 4. 搜索 arXiv
        
        print("✅ 搜索完成")
        return self.candidates
    
    def analyze_profile(self, 
                       github_url: str = None,
                       scholar_url: str = None,
                       aminer_url: str = None) -> CandidateProfile:
        """
        分析候选人画像
        
        Args:
            github_url: GitHub 主页链接
            scholar_url: Google Scholar 链接
            aminer_url: AMiner 主页链接
        
        Returns:
            候选人画像
        """
        profile = CandidateProfile(name="待提取")
        
        # TODO: 实现分析逻辑
        # 1. 抓取 GitHub 信息
        # 2. 抓取 Google Scholar 信息
        # 3. 抓取 AMiner 信息
        # 4. 计算匹配度
        
        return profile
    
    def generate_email(self,
                      candidate: CandidateProfile,
                      job_description: Dict,
                      template_type: str = "initial_outreach") -> str:
        """
        生成个性化邮件
        
        Args:
            candidate: 候选人画像
            job_description: 职位描述
            template_type: 模板类型
        
        Returns:
            生成的邮件内容
        """
        template = self.templates.get(template_type, self.templates["initial_outreach"])
        
        # 提取个性化信息
        paper_title = candidate.top_papers[0]["title"] if candidate.top_papers else "相关工作"
        paper_year = candidate.top_papers[0]["year"] if candidate.top_papers else "近期"
        method_highlight = candidate.research_areas[0] if candidate.research_areas else "研究"
        github_project = candidate.github_repos[0]["name"] if candidate.github_repos else "开源项目"
        project_highlight = "技术实现"
        
        # 填充模板
        email = template.format(
            company=job_description.get("company", "我们公司"),
            position=job_description.get("position", "工程师"),
            research_area=candidate.research_areas[0] if candidate.research_areas else "技术",
            name=candidate.name,
            recruiter_name="招聘负责人",
            paper_title=paper_title,
            paper_year=paper_year,
            method_highlight=method_highlight,
            github_project=github_project,
            project_highlight=project_highlight,
            research_direction=job_description.get("research_direction", "前沿技术"),
            team_size="XX 人",
            team_highlights="多位顶尖学者",
            job_responsibility_1=job_description.get("responsibility_1", "负责核心算法研发"),
            job_responsibility_2=job_description.get("responsibility_2", "推动技术创新"),
            job_responsibility_3=job_description.get("responsibility_3", "指导初级工程师"),
            key_skill_1=job_description.get("skill_1", "深度学习"),
            key_skill_2=job_description.get("skill_2", "大规模训练"),
            tech_stack_1=job_description.get("tech_stack_1", "PyTorch/JAX"),
            tech_highlight_2=job_description.get("tech_highlight_2", "千卡集群"),
            tech_highlight_3=job_description.get("tech_highlight_3", "前沿研究"),
            time_option_1="本周三下午 2-4 点",
            time_option_2="本周四上午 10-12 点",
            time_option_3="本周五下午 3-5 点",
            followup_month="下个月",
            current_company=candidate.current_company,
            title="招聘经理",
            contact_info="email@company.com"
        )
        
        return email
    
    def save_candidate(self, candidate: CandidateProfile):
        """保存候选人到 Bitable"""
        # TODO: 使用 feishu_bitable 保存
        print(f"💾 保存候选人：{candidate.name}")
        print(f"   状态：{candidate.status}")
        print(f"   匹配度：{candidate.match_score}")
    
    def export_report(self, output_path: str = None):
        """导出招聘报告"""
        if not output_path:
            output_path = DATA_DIR / f"recruiting_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        report = f"""# 招聘报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 候选人统计

- 总候选人：{len(self.candidates)}
- 高优先级：{sum(1 for c in self.candidates if c.priority == '高')}
- 中优先级：{sum(1 for c in self.candidates if c.priority == '中')}
- 低优先级：{sum(1 for c in self.candidates if c.priority == '低')}

## Pipeline 状态

| 状态 | 人数 |
|-----|------|
"""
        
        status_count = {}
        for c in self.candidates:
            status_count[c.status] = status_count.get(c.status, 0) + 1
        
        for status, count in status_count.items():
            report += f"| {status} | {count} |\n"
        
        report += f"""
## 高优先级候选人

"""
        
        high_priority = [c for c in self.candidates if c.priority == '高']
        for c in high_priority[:10]:
            report += f"""### {c.name}
- **公司**: {c.current_company}
- **职位**: {c.current_position}
- **研究方向**: {', '.join(c.research_areas)}
- **匹配度**: {c.match_score}
- **论文**: {c.paper_count} 篇
- **引用**: {c.total_citations}
- **H-index**: {c.h_index}
- **GitHub**: {c.github}
- **Scholar**: {c.google_scholar}

"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📊 报告已导出：{output_path}")


# 主函数
def main():
    """主函数"""
    recruiter = TechRecruiterPro()
    
    # 示例：搜索候选人
    candidates = recruiter.search_candidates(
        keywords=["RLHF", "PPO", "LLM", "Alignment"],
        target_companies=["DeepMind", "OpenAI", "Meta", "Moonshot"],
        min_citations=100,
        min_h_index=10
    )
    
    # 示例：生成邮件
    if candidates:
        candidate = candidates[0]
        job_desc = {
            "company": "某某 AI",
            "position": "高级算法工程师",
            "research_direction": "大模型对齐与强化学习",
            "responsibility_1": "负责 RLHF 算法研发",
            "responsibility_2": "优化大规模训练系统",
            "responsibility_3": "指导初级研究员",
            "skill_1": "深度强化学习",
            "skill_2": "PyTorch/JAX",
            "tech_stack_1": "分布式训练框架",
            "tech_highlight_2": "千卡 GPU 集群",
            "tech_highlight_3": "前沿论文发表"
        }
        
        email = recruiter.generate_email(candidate, job_desc)
        print("\n📧 生成的邮件:\n")
        print(email)


if __name__ == "__main__":
    main()
