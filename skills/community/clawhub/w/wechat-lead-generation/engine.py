#!/usr/bin/env python3
"""
wechat-lead-generation 核心引擎

职责:
1. 抓取微信数据（好友/群聊/朋友圈/公众号）
2. AI 分析对话内容，识别客户意向
3. 生成客户画像和线索评分
4. 自动生成回复或输出人工审核报告
"""

import sys
import json
import os
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# 配置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('wechat-lead-generation')

# 工作目录
WORKSPACE = Path('/Users/tom/.openclaw/workspace')
OUTPUT_DIR = WORKSPACE / 'output' / 'wechat-lead-generation'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR = OUTPUT_DIR / 'artifacts'
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

class WeChatLeadEngine:
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.source = params['source']
        self.days_back = params.get('days_back', 7)
        self.keywords = [k.lower() for k in params.get('keywords', [])]
        self.analysis_depth = params.get('analysis_depth', 'basic')
        self.auto_reply = params.get('auto_reply', False)
        self.reply_template = params.get('reply_template', '')

        self.leads = []
        self.profiles = []
        self.raw_data = []

        logger.info(f"启动微信线索抓取: source={self.source}, days_back={self.days_back}")

    async def run(self) -> str:
        """执行完整流程"""
        try:
            # 阶段 1: 抓取微信数据
            await self._fetch_wechat_data()

            # 阶段 2: 分析客户意向
            await self._analyze_leads()

            # 阶段 3: 生成报告
            report_path = await self._generate_report()

            # 阶段 4: 自动回复（可选）
            if self.auto_reply:
                await self._generate_replies()

            # 阶段 5: 存储记忆
            await self._store_memory()

            return report_path
        except Exception as e:
            logger.error(f"执行失败: {e}", exc_info=True)
            raise

    async def _fetch_wechat_data(self):
        """从微信抓取数据"""
        logger.info("📡 开始抓取微信数据...")

        # 这里应该调用 wechat-md-publish 或 bb-browser-openclaw
        # 由于这些技能可能需要实际微信环境，这里使用模拟数据
        data = await self._simulate_fetch()

        # 按关键词过滤
        if self.keywords:
            filtered = []
            for item in data:
                text = item.get('content', '').lower()
                if any(k in text for k in self.keywords):
                    filtered.append(item)
            data = filtered
            logger.info(f"关键词过滤后剩余 {len(data)} 条")

        self.raw_data = data
        logger.info(f"✅ 抓取完成: {len(data)} 条原始数据")

    async def _simulate_fetch(self) -> List[Dict]:
        """模拟抓取数据（实际需调用真实技能）"""
        # 模拟不同来源的数据
        mock_data = []
        now = datetime.now()

        if self.source == 'friends':
            # 好友私聊
            mock_data = [
                {
                    'type': 'friend',
                    'name': '张三',
                    'content': '你们那个 AI 机器人怎么卖？',
                    'timestamp': (now - timedelta(hours=2)).isoformat(),
                    'interest_keywords': ['AI', '机器人', '购买意向']
                },
                {
                    'type': 'friend',
                    'name': '李四',
                    'content': '我看朋友圈发的宇树机器人挺有意思，能详细介绍一下吗？',
                    'timestamp': (now - timedelta(days=1)).isoformat(),
                    'interest_keywords': ['宇树', '机器人', '咨询']
                }
            ]
        elif self.source == 'groups':
            # 群聊
            mock_data = [
                {
                    'type': 'group',
                    'group_name': 'AI 爱好者群',
                    'name': '王五',
                    'content': '有人用过 Step 模型吗？效果怎么样',
                    'timestamp': (now - timedelta(hours=5)).isoformat(),
                    'interest_keywords': ['Step', '模型', 'AI']
                },
                {
                    'type': 'group',
                    'group_name': '机器人研发',
                    'name': '赵六',
                    'content': '我们需要一批人形机器人用于展示，有没有合作渠道？',
                    'timestamp': (now - timedelta(days=2)).isoformat(),
                    'interest_keywords': ['人形机器人', '采购', '合作']
                }
            ]
        elif self.source == 'moments':
            # 朋友圈评论/互动
            mock_data = [
                {
                    'type': 'moment',
                    'name': '孙七',
                    'content': ' coment: 你们新发布的产品看起来很酷，有资料吗？',
                    'timestamp': (now - timedelta(hours=8)).isoformat(),
                    'interest_keywords': ['产品', '资料', '咨询']
                }
            ]
        else:
            # 公众号文章阅读/回复
            mock_data = [
                {
                    'type': 'article',
                    'name': '周八',
                    'article_title': '2026 年 AI 市场趋势预测',
                    'content': '文章底部留言: 非常受启发，希望能进一步交流',
                    'timestamp': (now - timedelta(days=3)).isoformat(),
                    'interest_keywords': ['AI', '交流', '合作意向']
                }
            ]

        return mock_data

    async def _analyze_leads(self):
        """分析客户意向并评分"""
        logger.info("🧠 开始分析客户意向...")

        for item in self.raw_data:
            profile = await self._analyze_item(item)
            self.profiles.append(profile)

            # 计算线索评分
            score = self._calculate_lead_score(profile)
            lead = {
                **profile,
                'lead_score': score,
                'is_lead': score >= 60,
                'recommended_reply': self._generate_reply_suggestion(profile) if self.auto_reply else ''
            }
            self.leads.append(lead)

        logger.info(f"✅ 分析完成: {len(self.leads)} 个潜在客户，{len([l for l in self.leads if l['is_lead']])} 个高评分线索")

    async def _analyze_item(self, item: Dict) -> Dict:
        """分析单条数据"""
        # 简单关键词分析（实际应使用 LLM）
        content = item.get('content', '')
        keywords = item.get('interest_keywords', [])

        # 识别兴趣领域
        interests = []
        interest_categories = {
            'AI': ['ai', '人工智能', 'model', '模型', 'step', 'claude', 'gpt'],
            '机器人': ['机器人', 'robot', '宇树', 'unitree', '人形'],
            '产品': ['产品', '资料', '介绍', 'details', 'price', '价格'],
            '合作': ['合作', '采购', 'business', '合作渠道', '批量'],
            '咨询': ['咨询', '怎么用', '如何使用', 'help']
        }

        text_lower = content.lower()
        for category, words in interest_categories.items():
            if any(w in text_lower for w in words):
                interests.append(category)

        # 购买意向强度
        intent_signals = ['怎么买', '价格', '多少钱', '购买', 'order', 'buy', '采购', '批量']
        intent_score = 3 if any(s in text_lower for s in intent_signals) else 1

        # 互动质量
        engagement_score = min(len(content) / 50, 10)  # 长度加分

        profile = {
            'name': item.get('name', '未知'),
            'type': item.get('type', 'unknown'),
            'source': self.source,
            'raw_content': content,
            'interests': list(set(interests)) if interests else ['未知'],
            'intent_score': intent_score,
            'engagement_score': round(engagement_score, 1),
            'timestamp': item.get('timestamp'),
            'group_name': item.get('group_name', ''),
            'article_title': item.get('article_title', '')
        }

        return profile

    def _calculate_lead_score(self, profile: Dict) -> int:
        """计算线索评分 (0-100)"""
        score = 0

        # 1. 关键词匹配（30分）
        if profile['interests'] and '未知' not in profile['interests']:
            score += 30

        # 2. 意向强度（30分）
        score += profile['intent_score'] * 10  # 1-3 -> 10-30

        # 3. 互动质量（20分）
        score += min(profile['engagement_score'], 20)

        # 4. 最近联系（20分）
        try:
            ts = datetime.fromisoformat(profile['timestamp'].replace('Z', '+00:00'))
            days_ago = (datetime.now() - ts).days
            recency = max(0, 20 - days_ago * 2)  # 越近分数越高
            score += recency
        except:
            score += 10  # 无法解析时间给基础分

        return min(100, int(score))

    def _generate_reply_suggestion(self, profile: Dict) -> str:
        """生成回复建议"""
        name = profile['name']
        interests = '、'.join(profile['interests']) if profile['interests'] else '相关产品'

        if self.reply_template:
            return self.reply_template.format(name=name, interest=interests, product="我们的 AI 解决方案")

        # 默认模板
        templates = [
            f"你好{name}！注意到你对{interests}感兴趣，我们有相关产品和服务，方便留下联系方式吗？",
            f"{name}您好！感谢关注。关于{interests}，我们可以提供专业方案，想了解更详细的信息吗？",
            f"Hi {name}，看到你对{interests}有兴趣，我们正好有成熟案例，是否可以电话详细沟通？"
        ]
        return templates[0]

    async def _generate_report(self) -> Path:
        """生成线索报告"""
        logger.info("📝 生成报告中...")
        now = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"leads-report-{now}.md"
        report_path = OUTPUT_DIR / filename

        # 统计
        high_score_leads = [l for l in self.leads if l['lead_score'] >= 80]
        medium_leads = [l for l in self.leads if 60 <= l['lead_score'] < 80]
        total_leads = len([l for l in self.leads if l['is_lead']])

        # 生成 Markdown
        content = f"""# 微信线索分析报告

**生成时间**: {now}\n
**数据来源**: {self.source}\n
**时间范围**: 最近 {self.days_back} 天\n
**关键词过滤**: {', '.join(self.keywords) if self.keywords else '无'}\n

---

## 📊 概览

| 指标 | 数量 |
|------|------|
| 总抓取数据 | {len(self.raw_data)} |
| 有效线索 | {total_leads} |
| 高评分 (≥80) | {len(high_score_leads)} |
| 中等评分 (60-79) | {len(medium_leads)} |

## 🔥 高评分线索 (≥80)

"""
        if high_score_leads:
            for i, lead in enumerate(high_score_leads, 1):
                content += f"""### {i}. {lead['name']} - {lead['lead_score']}分

**来源**: {lead['type']} {f"({lead['group_name']})" if lead.get('group_name') else ''}\n
**兴趣**: {', '.join(lead['interests'])}\n
**内容**: {lead['raw_content'][:100]}...\n
**建议回复**:\n```\n{lead.get('recommended_reply', '无')}\n```\n\n"""
        else:
            content += "_暂无高评分线索_\n"

        content += """## 📈 中等评分线索 (60-79)

"""
        if medium_leads:
            for i, lead in enumerate(medium_leads, 1):
                content += f"- **{lead['name']}** ({lead['lead_score']}分): {lead['raw_content'][:50]}...\n"
        else:
            content += "_暂无中等评分线索_\n"

        content += f"""

## 📋 原始数据统计

| 类型 | 数量 |
|------|------|
| 好友私聊 | {len([d for d in self.raw_data if d.get('type') == 'friend'])} |
| 群聊 | {len([d for d in self.raw_data if d.get('type') == 'group'])} |
| 朋友圈 | {len([d for d in self.raw_data if d.get('type') == 'moment'])} |
| 公众号 | {len([d for d in self.raw_data if d.get('type') == 'article'])} |

---

*报告由 OpenClaw wechat-lead-generation 技能自动生成*
"""

        report_path.write_text(content, encoding='utf-8')
        logger.info(f"✅ 报告已生成: {report_path}")

        # 保存 artifacts
        await self._save_artifacts()

        return report_path

    async def _generate_replies(self):
        """生成自动回复（如果启用）"""
        if not self.auto_reply:
            return

        # 保存到 artifacts 目录
        reply_path = ARTIFACTS_DIR / 'replies.md'
        content = "# 自动回复草稿\n\n"

        # 对所有有效线索 (lead_score >= 60) 生成回复
        for lead in self.leads:
            if lead['is_lead']:
                content += f"## {lead['name']} ({lead['lead_score']}分)\n\n{lead.get('recommended_reply', '')}\n\n---\n\n"

        reply_path.write_text(content, encoding='utf-8')
        logger.info(f"✅ 回复草稿已生成: {reply_path}")

    async def _store_memory(self):
        """存储客户画像到 agentmemory（可选功能）"""
        logger.info("💾 存储客户记忆中...")
        try:
            # 尝试导入 agentmemory（可能未安装）
            try:
                from agentmemory import create_memory
            except ImportError:
                logger.warning("agentmemory 未安装，跳过记忆存储（可选功能）")
                return

            stored = 0
            for lead in self.leads:
                if lead['is_lead']:
                    # 使用正确的 agentmemory API: create_memory(category, text, metadata={})
                    text = f"微信线索: {lead['name']} - {lead['raw_content'][:100]} (评分: {lead['lead_score']})"
                    metadata = {
                        'source': self.source,
                        'score': lead['lead_score'],
                        'interests': ','.join(lead['interests']),
                        'name': lead['name']
                    }
                    create_memory(
                        category='wechat-lead',
                        text=text,
                        metadata=metadata
                    )
                    stored += 1
            logger.info(f"✅ 存储 {stored} 条线索记忆")
        except Exception as e:
            logger.warning(f"记忆存储失败: {e}")

    async def _save_artifacts(self):
        """保存 artifacts 结构"""
        logger.info("💾 保存 artifacts...")

        # 1. profiles.json - 所有客户画像
        profiles_path = ARTIFACTS_DIR / 'profiles.json'
        with open(profiles_path, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 保存 profiles: {profiles_path}")

        # 2. high_score_leads.json - 高评分线索
        high_score = [l for l in self.leads if l['lead_score'] >= 80]
        high_score_path = ARTIFACTS_DIR / 'high_score_leads.json'
        with open(high_score_path, 'w', encoding='utf-8') as f:
            json.dump(high_score, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 保存 high_score_leads: {high_score_path}")

        # 3. raw_messages.json - 原始抓取数据
        raw_path = ARTIFACTS_DIR / 'raw_messages.json'
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(self.raw_data, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 保存 raw_messages: {raw_path}")

def main():
    """入口: 从 stdin 读取 JSON 参数"""
    try:
        raw = sys.stdin.read()
        params = json.loads(raw)
    except Exception as e:
        logger.error(f"参数解析失败: {e}")
        sys.exit(1)

    engine = WeChatLeadEngine(params)
    try:
        report_path = asyncio.run(engine.run())
        print(f"✅ 线索分析完成\n📄 报告: {report_path}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()