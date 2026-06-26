from google import genai
from typing import Optional

from utils.logger import get_logger
from config import Settings

# TODO: use LiteLLM to support various models and local deployment in the future

class MarketAnalyzer:
    """AI Market Analyzer"""
    
    def __init__(self, config: Settings):
        self.config = config
        self.logger = get_logger(__name__)
        self.client = None
        
        if config.gemini_api_key:
            self.client = genai.Client(api_key=config.gemini_api_key)
    
    def analyze(self, market_summary: str) -> Optional[str]:
        """
        Analyze market data using AI
        
        Args:
            market_summary: market summary in Markdown format
            
        Returns:
            AI analysis result in Markdown format
        """
        if not self.client:
            self.logger.warning("Gemini API key not set, skipping AI analysis")
            return None
        
        prompt = self._build_prompt(market_summary)
        
        try:
            response = self.client.models.generate_content(
                model=self.config.model_name,
                contents=prompt
            )
            
            self.logger.info("AI analysis completed successfully")
            return response.text
            
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return None
    
    def _build_prompt(self, market_summary: str) -> str:
        """Build prompt for AI analysis"""
        return f"""
        角色设定：你是一位拥有 20 年经验的 A 股资深策略分析师，擅长从成交量能、板块轮动和连板梯队中洞察市场情绪。

        任务描述：请基于下方提供的【当日复盘数据】，进行多维度复盘：

        1. 🚩 市场情绪诊断
        - 结合涨跌比、涨跌停对比、炸板率及全市场成交额，定义当前市场阶段（如：放量普涨、缩量整理、高位分歧、冰点重启等）。
        - 评价当前赚钱效应与亏钱效应的分布情况。

        2. 💰 核心主线与资金流向
        - 分析【成交额前二十】和【行业涨幅榜】，识别出目前资金主要锁定的“热点板块”和“大容错板块”。
        - 判断市场风格：是偏向“题材炒作”还是“权重护盘”？

        3. 🪜 连板梯度与空间博弈
        - 识别【涨停池】中的最高板（空间板）及其带动的属性。
        - 重点解读【炸板池】中的个股信号：是高位减速、还是分歧后的良性分歧？

        4. ⚡ 重点异动个股分析
        - 请从【重点个股 Watchlist】中挑选 3-4 只最具代表性的个股（如大成交涨停、高低位切换的典型），推测其背后的逻辑（资产注入、政策利好、超跌反弹还是技术突破）。

        5. 🧭 次日交易策略建议
        - 给出明日关注的观察点：哪些板块具备“反包”潜力？哪些高位品种需防范“补跌”？
        - 明确操作基调（如：积极参与、逢高止盈、或者多看少动）。
        - 给出重点个股的操作建议（如：建仓、继续持有、部分止盈、或者观望）。

        ---
        **📊 当日复盘数据内容如下**:
        {market_summary}

        要求：专业、客观、语言简练，避免模棱两可。输出格式使用 Markdown 标题和列表，增强可读性。
    """