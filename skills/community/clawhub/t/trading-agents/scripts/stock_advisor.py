#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope 股票诊断智能体系统
基于 AgentScope 框架实现的多智能体协作股票分析系统

核心功能:
1. 分析师团队 - 使用 ReActAgent 自主调用工具获取数据
2. 研究员团队 - 使用 AgentBase 实现看多看空辩论
3. 交易员 - 综合分析报告制定交易策略
4. 风险管理团队 - 评估交易策略的风险
5. 基金经理 - 做出最终投资决策
"""

import os
import sys
import json
import logging
import glob
import re
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置日志级别，过滤 AgentScope 的 WARNING 日志（如 thinking 块警告）
logging.getLogger("agentscope").setLevel(logging.ERROR)
# 过滤 OpenAI formatter 的 thinking 块警告
logging.getLogger("_openai_formatter").setLevel(logging.ERROR)

import agentscope

from dotenv import load_dotenv
load_dotenv()

from .config import config
from .tools.tushare_tools import TushareTools

# 分析师团队（ReActAgent）
from .agents.analysts import (
    MarketAnalystAgent,
    FundamentalsAnalystAgent,
    NewsAnalystAgent,
)
# 研究员团队（AgentBase）
from .agents.researchers import (
    BullishResearcherAgent,
    BearishResearcherAgent,
    ResearchFacilitatorAgent,
)
# 交易员和风控（原实现）
from .agents.trader import Trader
from .agents.risk_managers import (
    AggressiveRisk, NeutralRisk, ConservativeRisk, RiskFacilitator
)
from .agents.manager import Manager


@dataclass
class GlobalState:
    """全局状态管理"""
    ts_code: str = ""
    stock_name: str = ""
    report_dir: str = ""
    analyst_reports: Dict[str, str] = field(default_factory=dict)
    trader_report: str = ""
    research_debate: str = ""
    risk_discussion: str = ""
    final_decision: str = ""


class StockAdvisorSystem:
    """
    股票诊断智能体系统
    
    使用 AgentScope 框架实现:
    - 分析师使用 ReActAgent，可自主调用工具
    - 研究员使用 AgentBase，支持标准消息传递
    - 全流程使用 AgentScope 框架特性
    """
    
    def __init__(self):
        """初始化系统"""
        print("=" * 60)
        print("AgentScope 股票诊断智能体系统")
        print("=" * 60)
        
        # 初始化 AgentScope
        agentscope.init(project="股票诊断系统")
        
        # 初始化全局状态
        self.state = GlobalState()
        
        # 初始化数据工具（用于获取基本信息）
        self.tushare = TushareTools(config.tushare_token)
        
        # 保存配置引用
        self.config = config
        
        # 初始化智能体
        self._init_agents()
        
        print("系统初始化完成")
    
    def _init_agents(self):
        """初始化所有智能体"""
        print("\n初始化智能体...")
        
        # 分析师团队（ReActAgent）
        self.market_analyst = MarketAnalystAgent()
        self.fundamentals_analyst = FundamentalsAnalystAgent()
        self.news_analyst = NewsAnalystAgent()
        print("  分析师团队就绪 (ReActAgent)")
        
        # 研究员团队（AgentBase）
        self.bullish_researcher = BullishResearcherAgent()
        self.bearish_researcher = BearishResearcherAgent()
        self.research_facilitator = ResearchFacilitatorAgent()
        print("  研究员团队就绪 (AgentBase)")
        
        # 交易员
        self.trader = Trader()
        print("  交易员就绪")
        
        # 风险管理团队
        self.aggressive_risk = AggressiveRisk()
        self.neutral_risk = NeutralRisk()
        self.conservative_risk = ConservativeRisk()
        self.risk_facilitator = RiskFacilitator()
        print("  风险管理团队就绪")
        
        # 基金经理
        self.manager = Manager()
        print("  基金经理就绪")
    
    def diagnose(self, ts_code: str, base_report_dir: str = "report") -> Dict:
        """
        诊断股票
        
        Args:
            ts_code: 股票代码
            base_report_dir: 报告目录
            
        Returns:
            诊断结果字典
        """
        print(f"\n{'=' * 60}")
        print(f"开始诊断股票: {ts_code}")
        print(f"{'=' * 60}")
        
        start_time = datetime.now()
        
        # 创建报告目录
        timestamp = start_time.strftime('%Y%m%d_%H%M%S')
        ts_code_safe = ts_code.replace('.', '_')
        report_subdir = f"{ts_code_safe}_{timestamp}"
        report_dir = os.path.join(base_report_dir, report_subdir)
        
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        print(f"\n报告目录: {report_dir}")
        
        # 初始化状态
        self.state = GlobalState(ts_code=ts_code, report_dir=report_dir)
        
        # 获取股票基本信息
        basic_info = self.tushare.get_stock_basic(ts_code)
        self.state.stock_name = basic_info.get('name', ts_code)
        print(f"\n股票名称: {self.state.stock_name}")
        
        # 阶段1: 数据采集（ReActAgent）
        print(f"\n{'─' * 40}")
        print("阶段1: 数据采集（分析师团队）")
        print(f"{'─' * 40}")
        self._run_analysts()
        
        # 阶段2: 研究员辩论（AgentBase）
        print(f"\n{'─' * 40}")
        print("阶段2: 研究员辩论")
        print(f"{'─' * 40}")
        self._run_research_debate()
        
        # 阶段3: 交易员决策
        print(f"\n{'─' * 40}")
        print("阶段3: 交易员决策")
        print(f"{'─' * 40}")
        self._run_trader()
        
        # 阶段4: 风险管理讨论
        print(f"\n{'─' * 40}")
        print("阶段4: 风险管理讨论")
        print(f"{'─' * 40}")
        self._run_risk_discussion()
        
        # 阶段5: 基金经理最终决策
        print(f"\n{'─' * 40}")
        print("阶段5: 基金经理最终决策")
        print(f"{'─' * 40}")
        self._run_final_decision()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{'=' * 60}")
        print(f"诊断完成! 耗时: {duration:.1f}秒")
        print(f"{'=' * 60}")
        
        # 返回结果
        return {
            "ts_code": self.state.ts_code,
            "stock_name": self.state.stock_name,
            "report_dir": self.state.report_dir,
            "analyst_reports": self.state.analyst_reports,
            "research_debate": self.state.research_debate,
            "trader_report": self.state.trader_report,
            "risk_discussion": self.state.risk_discussion,
            "final_decision": self.state.final_decision,
            "diagnosis_time": datetime.now().isoformat(),
            "duration_seconds": duration,
        }
    
    def _run_analysts(self):
        """运行分析师团队"""
        print("\n[MarketAnalyst] 正在分析技术面...")
        market_report = self.market_analyst.analyze(self.state.ts_code)
        self.state.analyst_reports["MarketAnalyst"] = market_report
        self._save_analyst_report("MarketAnalyst", "技术面分析", market_report)
        print("  技术面分析完成")
        
        print("\n[FundamentalsAnalyst] 正在分析基本面...")
        fund_report = self.fundamentals_analyst.analyze(self.state.ts_code)
        self.state.analyst_reports["FundamentalsAnalyst"] = fund_report
        self._save_analyst_report("FundamentalsAnalyst", "基本面分析", fund_report)
        print("  基本面分析完成")
        
        print("\n[NewsAnalyst] 正在分析舆情面...")
        news_report = self.news_analyst.analyze(self.state.ts_code, self.state.stock_name)
        self.state.analyst_reports["NewsAnalyst"] = news_report
        self._save_analyst_report("NewsAnalyst", "舆情面分析", news_report)
        print("  舆情面分析完成")
    
    def _run_research_debate(self):
        """运行研究员辩论"""
        print("\n[ResearchFacilitator] 主持研究员辩论...")
        self.state.research_debate = self.research_facilitator.facilitate_debate_sync(
            self.bullish_researcher,
            self.bearish_researcher,
            self.state.analyst_reports,
            rounds=config.debate_rounds
        )
        self._save_report("研究员辩论报告", self.state.research_debate)
        print("  研究员辩论完成")
    
    def _run_trader(self):
        """运行交易员决策"""
        print("\n[Trader] 正在制定交易决策...")
        self.state.trader_report = self.trader.make_decision(
            self.state.analyst_reports,
            self.state.research_debate
        )
        self._save_report("交易员决策报告", self.state.trader_report)
        print("  交易决策完成")
    
    def _run_risk_discussion(self):
        """运行风险管理讨论"""
        print("\n[RiskFacilitator] 主持风险管理讨论...")
        self.state.risk_discussion = self.risk_facilitator.facilitate_discussion(
            self.aggressive_risk,
            self.neutral_risk,
            self.conservative_risk,
            self.state.trader_report,
            rounds=config.risk_discussion_rounds
        )
        self._save_report("风险管理讨论报告", self.state.risk_discussion)
        print("  风险管理讨论完成")
    
    def _run_final_decision(self):
        """运行基金经理最终决策"""
        print("\n[Manager] 正在做出最终决策...")
        self.state.final_decision = self.manager.make_final_decision(
            self.state.ts_code,
            self.state.stock_name,
            self.state.analyst_reports,
            self.state.research_debate,
            self.state.trader_report,
            self.state.risk_discussion
        )
        self._save_report("最终决策报告", self.state.final_decision)
        print("  最终决策完成")
    
    def _save_analyst_report(self, analyst_name: str, report_title: str, report_content: str):
        """保存分析师报告"""
        filename = f"{analyst_name}_{report_title}.md"
        filepath = os.path.join(self.state.report_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"    已保存: {filename}")
    
    def _save_report(self, report_name: str, report_content: str):
        """保存报告"""
        filename = f"{report_name.replace(' ', '_')}.md"
        filepath = os.path.join(self.state.report_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"    已保存: {filename}")
    
    def save_report(self, result: Dict):
        """保存完整诊断报告（JSON格式）"""
        report_dir = result.get('report_dir', 'report')
        
        json_filename = "complete_diagnosis_report.json"
        json_path = os.path.join(report_dir, json_filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n完整JSON报告已保存: {json_path}")
        
        # 合并所有MD文件为PDF
        self._merge_md_to_pdf(report_dir)
        
        return json_path
    
    def _get_md_files_in_order(self, report_dir: str) -> List[str]:
        """
        按照生成顺序获取MD文件列表
        
        生成顺序:
        1. MarketAnalyst_技术面分析.md
        2. FundamentalsAnalyst_基本面分析.md
        3. NewsAnalyst_舆情面分析.md
        4. 研究员辩论报告.md
        5. 交易员决策报告.md
        6. 风险管理讨论报告.md
        7. 最终决策报告.md
        """
        # 定义文件顺序映射
        order_mapping = {
            'MarketAnalyst_技术面分析.md': 1,
            'FundamentalsAnalyst_基本面分析.md': 2,
            'NewsAnalyst_舆情面分析.md': 3,
            '研究员辩论报告.md': 4,
            '交易员决策报告.md': 5,
            '风险管理讨论报告.md': 6,
            '最终决策报告.md': 7,
        }
        
        # 获取所有MD文件
        md_files = glob.glob(os.path.join(report_dir, '*.md'))
        
        # 按预定义顺序排序
        def get_sort_key(filepath):
            filename = os.path.basename(filepath)
            return order_mapping.get(filename, 999)
        
        sorted_files = sorted(md_files, key=get_sort_key)
        return sorted_files
    
    def _merge_md_to_pdf(self, report_dir: str) -> str:
        """
        将所有MD文件按生成顺序合并为PDF
        
        Args:
            report_dir: 报告目录路径
            
        Returns:
            PDF文件路径
        """
        # 获取按顺序排列的MD文件
        md_files = self._get_md_files_in_order(report_dir)
        
        if not md_files:
            print("\n警告: 未找到MD文件，跳过PDF生成")
            return ""
        
        print(f"\n开始合并 {len(md_files)} 个MD文件为PDF...")
        
        # 读取所有MD文件内容
        md_contents = []
        for i, md_file in enumerate(md_files, 1):
            filename = os.path.basename(md_file)
            print(f"  [{i}/{len(md_files)}] 读取: {filename}")
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                md_contents.append({
                    'filename': filename,
                    'content': content
                })
        
        # 使用替代方法生成PDF
        return self._merge_md_to_pdf_alternative(report_dir, md_contents)
    

    def _merge_md_to_pdf_alternative(self, report_dir: str, md_contents: List[Dict]) -> str:
        """
        使用 fpdf2 直接生成 PDF
        直接解析 Markdown 内容渲染，不经过 HTML 中间层
        """
        return self._generate_pdf_with_fpdf2(report_dir, md_contents)
    
    def _generate_pdf_with_fpdf2(self, report_dir: str, md_contents: List[Dict]) -> str:
        """
        使用 fpdf2 生成 PDF
        直接解析 Markdown 内容渲染为 PDF
        """
        try:
            from fpdf import FPDF  # pyright: ignore[reportMissingModuleSource]
        except ImportError:
            print("正在安装 fpdf2...")
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'fpdf2'])
            from fpdf import FPDF  # pyright: ignore[reportMissingModuleSource]
        
        # 获取中文字体路径
        font_path = self._get_chinese_font_path()
        
        class PDF(FPDF):
            def __init__(self, font_path=None, ts_code="", stock_name=""):
                super().__init__()
                self.font_path = font_path
                self.ts_code = ts_code
                self.stock_name = stock_name
                self.has_font = font_path is not None
                
            def header(self):
                if self.page_no() > 1:
                    if self.has_font:
                        self.set_font('CustomFont', '', 9)
                    else:
                        self.set_font('Arial', '', 9)
                    self.set_text_color(128, 128, 128)
                    self.cell(0, 8, f'股票诊断报告 - {self.stock_name} ({self.ts_code})', align='C')
                    self.ln(8)
                    self.set_text_color(0, 0, 0)
            
            def footer(self):
                self.set_y(-15)
                if self.has_font:
                    self.set_font('CustomFont', '', 8)
                else:
                    self.set_font('Arial', '', 8)
                self.set_text_color(128, 128, 128)
                self.cell(0, 10, f'第 {self.page_no()} 页', align='C')
                self.set_text_color(0, 0, 0)
        
        pdf = PDF(font_path=font_path, ts_code=self.state.ts_code, stock_name=self.state.stock_name)
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.set_margins(20, 20, 20)
        
        if font_path:
            try:
                pdf.add_font('CustomFont', '', font_path)
                pdf.add_font('CustomFont', 'B', font_path)
                pdf.has_font = True
                print(f"  成功加载字体: {font_path}")
            except Exception as e:
                print(f"警告: 无法加载中文字体: {e}")
                pdf.has_font = False
        else:
            print("警告: 未找到中文字体，PDF可能无法正确显示中文")
            pdf.has_font = False
        
        # 添加封面
        self._add_cover_page(pdf)
        
        # 添加各章节内容
        for idx, md_item in enumerate(md_contents, 1):
            filename = md_item['filename']
            content = md_item['content']
            section_title = filename.replace('.md', '')
            
            print(f"  生成PDF章节: {section_title}")
            
            pdf.add_page()
            
            self._set_font(pdf, 'B', 16)
            pdf.set_text_color(30, 30, 30)
            pdf.cell(0, 12, f'{idx}. {section_title}')
            pdf.ln(12)
            
            pdf.set_draw_color(200, 200, 200)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(8)
            
            self._render_markdown_to_pdf(pdf, content)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        diagnosis_result = self._extract_diagnosis_result()
        pdf_filename = f"{self.state.stock_name}_{self.state.ts_code}_{timestamp}_{diagnosis_result}.pdf"
        pdf_path = os.path.join(report_dir, pdf_filename)
        pdf.output(pdf_path)
        print(f"\nPDF报告已保存: {pdf_path}")
        return pdf_path
    
    def _add_cover_page(self, pdf):
        """添加封面页"""
        pdf.add_page()
        
        self._set_font(pdf, 'B', 28)
        pdf.set_text_color(30, 30, 30)
        pdf.ln(50)
        pdf.cell(0, 15, '股票诊断报告', align='C')
        pdf.ln(25)
        
        self._set_font(pdf, '', 22)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 12, self.state.stock_name, align='C')
        pdf.ln(12)
        
        self._set_font(pdf, '', 16)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, self.state.ts_code, align='C')
        pdf.ln(40)
        
        self._set_font(pdf, '', 12)
        pdf.cell(0, 8, f'生成时间: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}', align='C')
        pdf.ln(80)
        
        pdf.set_text_color(150, 150, 150)
        self._set_font(pdf, '', 10)
        pdf.cell(0, 8, '本报告由AI智能体自动生成，仅供参考', align='C')
        
        pdf.set_text_color(0, 0, 0)
    
    def _set_font(self, pdf, style: str = '', size: int = 11):
        """设置字体"""
        if pdf.has_font:
            pdf.set_font('CustomFont', style, size)
        else:
            pdf.set_font('Arial', style, size)
    
    def _render_markdown_to_pdf(self, pdf, content: str):
        """
        将 Markdown 内容直接渲染到 PDF
        支持标题、段落、列表、表格、代码块、引用等
        """
        import re
        
        lines = content.split('\n')
        i = 0
        in_code_block = False
        in_table = False
        table_data = []
        
        while i < len(lines):
            line = lines[i]
            
            # 代码块处理
            if line.strip().startswith('```'):
                if in_code_block:
                    in_code_block = False
                    pdf.ln(3)
                else:
                    in_code_block = True
                    pdf.ln(2)
                i += 1
                continue
            
            if in_code_block:
                self._set_font(pdf, '', 9)
                pdf.set_fill_color(245, 245, 245)
                code_line = line if line else ' '
                available_width = pdf.w - pdf.l_margin - pdf.r_margin - 4
                pdf.set_x(pdf.l_margin + 2)
                pdf.multi_cell(available_width, 5, code_line, fill=True)
                i += 1
                continue
            
            # 表格处理
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    table_data = []
                
                cells = [cell.strip() for cell in line.strip().split('|')[1:-1]]
                if cells and not all(c.replace('-', '').replace(':', '') == '' for c in cells):
                    table_data.append(cells)
                i += 1
                continue
            elif in_table:
                self._render_table(pdf, table_data)
                in_table = False
                table_data = []
            
            # 引用块处理
            if line.strip().startswith('>'):
                quote_text = line.strip()[1:].strip()
                self._render_quote(pdf, quote_text)
                i += 1
                continue
            
            # 空行处理
            if not line.strip():
                pdf.ln(2)
                i += 1
                continue
            
            # 分隔线处理
            if line.strip() in ['---', '***', '___']:
                pdf.ln(3)
                pdf.set_draw_color(200, 200, 200)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(3)
                i += 1
                continue
            
            # 标题处理
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2)
                self._render_heading(pdf, level, text)
                i += 1
                continue
            
            # 无序列表处理
            list_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
            if list_match:
                indent = len(list_match.group(1)) // 2
                text = list_match.group(2)
                self._render_list_item(pdf, indent, text)
                i += 1
                continue
            
            # 有序列表处理
            ordered_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
            if ordered_match:
                indent = len(ordered_match.group(1)) // 2
                text = ordered_match.group(2)
                self._render_list_item(pdf, indent, text, ordered=True)
                i += 1
                continue
            
            # 普通段落处理
            self._render_paragraph(pdf, line)
            i += 1
        
        if in_table and table_data:
            self._render_table(pdf, table_data)
    
    def _render_heading(self, pdf, level: int, text: str):
        """渲染标题"""
        sizes = {1: 18, 2: 15, 3: 13, 4: 12, 5: 11, 6: 11}
        size = sizes.get(level, 11)
        
        pdf.ln(4)
        self._set_font(pdf, 'B', size)
        pdf.set_text_color(30, 30, 30)
        
        text = self._clean_markdown(text)
        
        pdf.multi_cell(0, 8, text)
        pdf.ln(2)
        self._set_font(pdf, '', 11)
        pdf.set_text_color(0, 0, 0)
    
    def _render_paragraph(self, pdf, text: str):
        """渲染段落"""
        self._set_font(pdf, '', 11)
        text = self._clean_markdown(text)
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(available_width, 6, text)
        pdf.ln(2)
    
    def _render_list_item(self, pdf, indent: int, text: str, ordered: bool = False):
        """渲染列表项"""
        self._set_font(pdf, '', 11)
        text = self._clean_markdown(text)
        indent_width = 8 * (indent + 1)
        pdf.set_x(pdf.l_margin + indent_width)
        marker = '• ' if not ordered else '◦ '
        available_width = pdf.w - pdf.l_margin - pdf.r_margin - indent_width
        pdf.multi_cell(available_width, 6, marker + text)
        pdf.ln(1)
    
    def _render_quote(self, pdf, text: str):
        """渲染引用块"""
        self._set_font(pdf, '', 10)
        pdf.set_text_color(80, 80, 80)
        
        text = self._clean_markdown(text)
        
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(x, y, 3, 6, 'F')
        
        pdf.set_x(x + 6)
        available_width = pdf.w - pdf.l_margin - pdf.r_margin - 6
        pdf.multi_cell(available_width, 6, text, fill=True)
        pdf.ln(2)
        
        self._set_font(pdf, '', 11)
        pdf.set_text_color(0, 0, 0)
    
    def _render_table(self, pdf, table_data):
        """渲染表格"""
        if not table_data:
            return
        
        pdf.ln(2)
        self._set_font(pdf, '', 10)
        
        num_cols = max(len(row) for row in table_data)
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        col_width = available_width / num_cols
        
        if table_data:
            self._set_font(pdf, 'B', 10)
            pdf.set_fill_color(240, 240, 240)
            for cell in table_data[0]:
                cell = self._clean_markdown(cell)
                pdf.cell(col_width, 7, cell[:25], border=1, fill=True)
            pdf.ln()
        
        self._set_font(pdf, '', 10)
        pdf.set_fill_color(255, 255, 255)
        for row in table_data[1:]:
            for j, cell in enumerate(row):
                if j < num_cols:
                    cell = self._clean_markdown(cell)
                    pdf.cell(col_width, 7, cell[:25], border=1)
            pdf.ln()
        
        pdf.ln(2)

    def _extract_diagnosis_result(self) -> str:
        """从最终决策中提取诊断结果"""
        if not self.state.final_decision:
            return "未确定"
        
        decision = self.state.final_decision.upper()
        
        # 定义关键词映射
        if any(word in decision for word in ['买入', '买进', 'BUY', '强烈买入']):
            return "买入"
        elif any(word in decision for word in ['卖出', '抛售', 'SELL', '强烈卖出']):
            return "卖出"
        elif any(word in decision for word in ['持有', '观望', 'HOLD', '中性']):
            return "持有"
        else:
            return "综合诊断"
    
    def _clean_markdown(self, text: str) -> str:
        """清理Markdown标记"""
        import re
        # 移除粗体标记
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        # 移除斜体标记
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        # 移除代码标记
        text = re.sub(r'`(.+?)`', r'\1', text)
        # 移除链接标记，保留文本
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        return text
    
    def _get_chinese_font_path(self) -> Optional[str]:
        """获取中文字体路径"""
        # 常见中文字体路径（macOS）
        possible_fonts = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/STHeiti Medium.ttc',
            '/System/Library/Fonts/Hiragino Sans GB.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
        ]
        
        # Linux
        possible_fonts.extend([
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        ])
        
        # Windows
        possible_fonts.extend([
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/simsun.ttc',
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/msyhbd.ttc',
            'C:/Windows/Fonts/arialuni.ttf',
        ])
        
        for font_path in possible_fonts:
            if os.path.exists(font_path):
                print(f"  使用字体: {font_path}")
                return font_path
        
        return None


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AgentScope 股票诊断智能体系统'
    )
    parser.add_argument(
        '--stock', '-s', 
        type=str, 
        default='600519.SH',
        help='股票代码（默认: 600519.SH）'
    )
    parser.add_argument(
        '--output', '-o', 
        type=str, 
        default='report',
        help='输出目录（默认: report）'
    )
    
    args = parser.parse_args()
    
    # 创建系统实例
    advisor = StockAdvisorSystem()
    
    # 执行诊断
    result = advisor.diagnose(args.stock, args.output)
    
    # 保存完整报告
    advisor.save_report(result)
    
    # 输出最终决策
    print("\n" + "=" * 60)
    print("最终诊股意见")
    print("=" * 60)
    print(result['final_decision'])
    
    print("\n" + "=" * 60)
    print(f"所有报告已保存到: {result['report_dir']}")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    main()
