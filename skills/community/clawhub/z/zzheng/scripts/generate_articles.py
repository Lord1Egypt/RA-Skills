#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zzheng - 法律知识公众号文章生成器 v4.0
- 优先抓取实时热门法律新闻
- 结合热点生成原创文章
- 个人篇和企业篇完全独立
"""

import os
import re
import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class HotTopicFetcher:
    """实时热门话题抓取器"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })

    def fetch_all(self) -> List[Dict]:
        """抓取所有来源"""
        all_topics = []
        print("[*] 正在抓取热门法律新闻...")

        # 优先尝试多个来源
        funcs = [
            self.fetch_weibo,
            self.fetch_zhihu,
            self.fetch_baidu_hot,
            self.fetch_tencent_news,
        ]

        for func in funcs:
            try:
                topics = func()
                all_topics.extend(topics)
                if topics:
                    print(f"[*] {func.__name__}: 获取 {len(topics)} 条")
            except Exception as e:
                print(f"[*] {func.__name__} 失败: {e}")

        # 去重
        seen = set()
        unique = []
        for t in all_topics:
            key = re.sub(r'\[.*?\]', '', t['title'])[:10]
            if key not in seen and len(key) > 3:
                seen.add(key)
                unique.append(t)

        print(f"[*] 共获取 {len(unique)} 条热门话题")
        return unique[:20]  # 最多返回20条

    def fetch_weibo(self) -> List[Dict]:
        """微博热搜"""
        topics = []
        try:
            r = self.session.get('https://weibo.com/ajax/side/hotSearch', timeout=8)
            if r.ok:
                data = r.json()
                for item in data.get('data', {}).get('realtime', [])[:30]:
                    text = item.get('word', '')
                    kw = ['法院', '判决', '赔偿', '维权', '侵权', '诈骗', '劳动', '消费', '合同', '法律', '律师', '犯罪', '纠纷', '民法']
                    if any(k in text for k in kw):
                        topics.append({
                            'title': text,
                            'source': '微博热搜',
                            'category': self._cat(text)
                        })
        except Exception as e:
            print(f"[*] 微博热搜: {e}")
        return topics

    def fetch_zhihu(self) -> List[Dict]:
        """知乎热榜"""
        topics = []
        try:
            r = self.session.get('https://www.zhihu.com/api/v4/search_topics/tosuggest?token=&limit=20', timeout=8)
            if r.ok:
                for item in r.json().get('data', [])[:10]:
                    text = item.get('name', '')
                    if len(text) > 5:
                        topics.append({
                            'title': text,
                            'source': '知乎热榜',
                            'category': self._cat(text)
                        })
        except:
            pass
        return topics

    def fetch_baidu_hot(self) -> List[Dict]:
        """百度热搜"""
        topics = []
        try:
            r = self.session.get('https://top.baidu.com/api?from=pc_hotboard', timeout=8, headers={
                'Referer': 'https://top.baidu.com/'
            })
            if r.ok:
                data = r.json()
                for item in data.get('data', {}).get('hotList', [])[:20]:
                    text = item.get('raw_word', '')
                    if len(text) > 4:
                        topics.append({
                            'title': text,
                            'source': '百度热搜',
                            'category': self._cat(text)
                        })
        except:
            pass
        return topics

    def fetch_tencent_news(self) -> List[Dict]:
        """腾讯新闻"""
        topics = []
        try:
            r = self.session.get('https://api.inews.qq.com/event/1.0/getHotRecommendList?page=1&pageSize=20', timeout=8)
            if r.ok:
                data = r.json()
                for item in data.get('data', {}).get('list', [])[:15]:
                    text = item.get('title', '')
                    if len(text) > 8:
                        topics.append({
                            'title': text,
                            'source': '腾讯新闻',
                            'category': self._cat(text)
                        })
        except:
            pass
        return topics

    def _cat(self, text: str) -> str:
        """分类"""
        t = text.lower()
        if any(kw in t for kw in ['劳动', '工资', '加班', '辞职', '辞退', '社保']): return '劳动用工'
        if any(kw in t for kw in ['消费', '退货', '假货', '欺诈', '维权', '投诉']): return '消费维权'
        if any(kw in t for kw in ['婚', '离婚', '财产', '抚养', '继承', '彩礼']): return '婚姻家庭'
        if any(kw in t for kw in ['版权', '商标', '专利', '抄袭', '侵权']): return '知识产权'
        if any(kw in t for kw in ['企业', '公司', '合规', '股权', '融资']): return '企业合规'
        return '综合法律'


class ArticleGenerator:
    """文章生成器"""

    def __init__(self, output_dir: str = r"D:\其它工具\文章"):
        self.out_dir = Path(output_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.today = datetime.now()
        self.today_str = self.today.strftime("%Y-%m-%d")

        self.progress_p = self._load("personal")
        self.progress_e = self._load("enterprise")

    def _load(self, tp: str) -> dict:
        f = self.out_dir / f"v4_{tp}.json"
        if f.exists():
            try: return json.load(open(f, encoding='utf-8'))
            except: pass
        return {}

    def _save(self, d: dict, tp: str):
        with open(self.out_dir / f"v4_{tp}.json", 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)

    def generate(self, hot: List[Dict]) -> tuple:
        """生成文章"""
        # 选择热点
        p_cat, p_kw, p_src = self._select(hot, False)
        e_cat, e_kw, e_src = self._select(hot, True)

        print(f"[*] 个人篇: {p_kw} (来源:{p_src})")
        print(f"[*] 企业篇: {e_kw} (来源:{e_src})")

        p_article = self._make_article("个人", p_cat, p_kw, p_src)
        e_article = self._make_article("企业", e_cat, e_kw, e_src)

        self._save(self.progress_p, "personal")
        self._save(self.progress_e, "enterprise")

        return p_article, e_article, p_kw, e_kw

    def _select(self, hot: List[Dict], is_ent: bool) -> tuple:
        """选择话题"""
        day = int(self.today.strftime("%Y%m%d")[-2:])

        # 优先用热点
        if hot and len(hot) >= 3:
            cats = {}
            for t in hot:
                cats[t['category']] = cats.get(t['category'], 0) + 1
            top_cat = max(cats.items(), key=lambda x: x[1])[0]
            filtered = [t for t in hot if t['category'] == top_cat]
            topic = random.choice(filtered) if filtered else hot[0]
            kw = topic['title'][:10]
            return (top_cat, kw, topic['source'])

        # 备选话题库
        personal_map = {
            '劳动用工': [('试用期被延长合法吗？', '试用期'), ('加班费怎么算？', '加班费'), ('公司拖欠工资怎么办？', '工资维权'), ('被辞退如何争取补偿？', '经济补偿')],
            '消费维权': [('网购遇到假货怎么赔？', '假货赔偿'), ('预付卡充值需谨慎！', '预付卡'), ('七天无理由退货的正确姿势', '退货'), ('商家拒绝退货合法吗？', '退货维权')],
            '婚姻家庭': [('离婚时房产怎么分？', '房产分割'), ('彩礼能不能要回来？', '彩礼返还'), ('抚养权到底归谁？', '抚养权'), ('遭遇家暴怎么办？', '家暴维权')],
            '知识产权': [('转载文章会侵权吗？', '著作权'), ('图片被侵权怎么维权？', '摄影维权'), ('公众号配图的法律风险', '配图'), ('原创被抄袭怎么办？', '抄袭维权')],
            '综合法律': [('高空抛物谁负责？', '高空抛物'), ('遛狗不拴绳伤人怎么赔？', '宠物伤'), ('个人信息被泄露怎么办？', '隐私'), ('网络发言的法律边界', '网络言论')],
        }

        ent_map = {
            '企业合规': [('劳动合同签订10大要点', '合同签订'), ('试用期管理的正确方式', '试用期'), ('加班费合规管理指南', '加班费'), ('解除劳动合同的正确姿势', '解除合同')],
            '广告合规': [('广告法红线词汇汇总', '广告法'), ('产品质量责任的法律后果', '产品责任'), ('职业打假应对指南', '打假'), ('售后服务的法律义务', '售后')],
            '企业知识产权': [('商标注册与保护策略', '商标'), ('商业秘密泄露如何追责', '商业秘密'), ('软件正版化合规指南', '正版化'), ('展会知识产权风险管理', '展会')],
            '企业合同': [('合同审核5个核心要点', '合同审核'), ('采购合同风险防控', '采购'), ('违约金条款如何设定', '违约金'), ('电子合同的法律效力', '电子合同')],
            '企业合规': [('企业合规的必要性', '合规'), ('刑事风险防控', '刑事风险'), ('数据合规要点', '数据'), ('税务合规指南', '税务')],
        }

        topic_dict = ent_map if is_ent else personal_map
        progress = self.progress_e if is_ent else self.progress_p
        cats = list(topic_dict.keys())
        cat = cats[day % len(cats)]
        topics = topic_dict[cat]
        idx = progress.get(cat, 0)
        title, kw = topics[idx % len(topics)]
        progress[cat] = (idx + 1) % len(topics)
        if is_ent: self.progress_e = progress
        else: self.progress_p = progress
        return (cat, kw, '每日热点')

    def _make_article(self, tp: str, cat: str, kw: str, src: str) -> str:
        """生成单篇文章"""
        is_ent = tp == "企业"

        # 案例库
        cases = {
            '劳动用工': {'个人': ('小李被公司以业务调整为由辞退，只愿补半个月工资。申请仲裁后在律师帮助下获得4个月赔偿金。', '根据《劳动合同法》，违法解除应支付双倍赔偿金。'),
                        '企业': ('某科技公司单方解除一批员工仅补一个月工资，员工集体仲裁后公司被判双倍赔偿。', '企业单方解除必须有充分法律依据，建议优先协商解除。')},
            '消费维权': {'个人': ('王女士直播购减肥产品为三无产品，商家拒绝退货。通过消协投诉最终获三倍赔偿。', '经营者欺诈可要求三倍赔偿，增加赔偿不足500的按500算。'),
                        '企业': ('某电商用"全网最低价"绝对化用语，被罚30万。', '《广告法》禁止绝对化用语，违法可罚100-200万。')},
            '婚姻家庭': {'个人': ('张先生婚后共同还贷购房，离婚时妻子主张分割，法院判决还贷部分及增值为共同财产。', '婚后共同还贷及对应增值属夫妻共同财产。'),
                        '企业': ('企业家离婚时家企不分，公司财产被认定家庭财产，股权按共同财产处理。', '企业家应做好家企财产隔离。')},
            '知识产权': {'个人': ('摄影师作品被公众号盗用，阅读量超百万，获赔3万元。', '未经许可使用他人作品应赔偿实际损失或违法所得。'),
                        '企业': ('某公司专利被无效，因权利要求范围过窄无法有效保护核心技术。', '专利布局应从研发阶段开始，请专业代理人撰写。')},
            '综合法律': {'个人': ('刘大爷遛狗不拴绳致人骨折，赔8万元。', '动物致损由饲养人承担侵权责任。'),
                        '企业': ('某公司发不实宣传文章诋毁竞争对手，被判赔50万并道歉。', '企业宣传必须真实，不得损害他人商誉。')}
        }

        tips = {
            '劳动用工': {'个人': ['保留劳动合同和工资流水', '发生纠纷先协商，协商不成找劳动监察', '劳动仲裁免费，别怕维权'],
                         '企业': ['合同条款要完整明确', '解除要有合法依据', '建议聘请常年法律顾问']},
            '消费维权': {'个人': ['购物保留凭证和聊天记录', '发现问题及时拍照留证', '可向消协投诉或起诉'],
                         '企业': ['广告宣传要真实合法', '建立完善的售后制度', '积极处理消费者投诉']},
            '婚姻家庭': {'个人': ['大额财产约定要书面', '注意保留财产凭证', '必要时咨询专业律师'],
                         '企业': ['做好家企财产隔离', '可通过信托规划传承', '重大决策前咨询律师']},
            '知识产权': {'个人': ['原创作品留存原始文件', '发现侵权及时保全证据', '可通过平台投诉或起诉维权'],
                         '企业': ['核心技术申请专利保护', '签订保密协议和竞业限制', '定期进行知识产权排查']},
            '综合法律': {'个人': ['高空不抛物、文明养犬', '网络发言要负责任', '保护个人信息'],
                         '企业': ['建立合规管理体系', '定期开展法律培训', '聘请专业律师团队']}
        }

        c = cases.get(cat, cases['综合法律'])
        t = tips.get(cat, tips['综合法律'])
        case_desc, knowledge = c.get(tp, c['个人'])
        article_tips = t.get(tp, t['个人'])

        # 标题模板
        title_tpl = {
            '个人': [f'「{kw}」引发热议！律师帮你一次性说清楚！', f'热搜上的{kw}问题，你必须知道这些！', f'关于{kw}，法律这样规定！'],
            '企业': [f'企业注意！{kw}的法律风险必须重视！', f'HR和老板必读：{kw}的正确姿势！', f'{kw}频发，企业如何做好风险防控？']
        }

        lines = []
        title = random.choice(title_tpl[tp])
        lines.append(f"**{title}**\n")
        lines.append("─" * 30 + "\n")
        lines.append(f"📢 **今日热点**\n")
        lines.append(f"近期「{kw}」相关话题热度不减（来源：{src}），今天我们就从法律角度来深度分析...\n")
        lines.append("\n📍 **典型案例**\n")
        lines.append(f"{case_desc}\n")
        lines.append(f"🔔 **案例启示**：遇到类似情况，善用法律武器保护自己！\n")
        lines.append("\n📋 **法律知识**\n")
        lines.append(f"{knowledge}\n")
        lines.append("\n💡 **实用建议**\n")
        for i, tip in enumerate(article_tips, 1):
            lines.append(f"  {i}. {tip}\n")
        lines.append("\n✨ **结语**\n")
        if is_ent:
            lines.append(f"关于「{kw}」的企业合规要点就分享到这里。企业合规无小事，建议收藏备用！\n")
        else:
            lines.append(f"关于「{kw}」的法律知识就分享到这里。觉得有用就转发给更多朋友吧！\n")

        return "".join(lines)

    def save(self, p: str, e: str, p_kw: str, e_kw: str) -> tuple:
        """保存文章"""
        p_file = self.out_dir / f"法律知识_{self.today_str}_个人篇.txt"
        e_file = self.out_dir / f"法律知识_{self.today_str}_企业篇.txt"

        with open(p_file, 'w', encoding='utf-8') as f:
            f.write("=" * 40 + "\n")
            f.write(f"【个人法律知识】{p_kw}\n")
            f.write("=" * 40 + "\n\n")
            f.write(p)

        with open(e_file, 'w', encoding='utf-8') as f:
            f.write("=" * 40 + "\n")
            f.write(f"【企业法律知识】{e_kw}\n")
            f.write("=" * 40 + "\n\n")
            f.write(e)

        return str(p_file), str(e_file)


def main():
    print("=" * 40)
    print("[zzheng - 法律公众号文章生成器 v4.0]")
    print("[实时热点 + 原创文章]")
    print("=" * 40)

    # 抓取热点
    hot_topics = []
    if HAS_REQUESTS:
        fetcher = HotTopicFetcher()
        hot_topics = fetcher.fetch_all()
    else:
        print("[*] requests未安装，使用预设话题库")

    # 生成
    gen = ArticleGenerator()
    p_art, e_art, p_kw, e_kw = gen.generate(hot_topics)

    # 保存
    p_file, e_file = gen.save(p_art, e_art, p_kw, e_kw)

    print("\n[OK] 文章生成完成！")
    print(f"[*] 个人篇: {p_file}")
    print(f"[*] 企业篇: {e_file}")

    return {'personal': p_art, 'enterprise': e_art, 'files': (p_file, e_file)}


if __name__ == "__main__":
    main()
