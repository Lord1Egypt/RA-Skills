#!/usr/bin/env python3
"""
Listing 生成器 - SEO 优化的商品详情页生成
支持：Amazon、淘宝、独立站等多平台
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# 配置
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"


@dataclass
class ListingContent:
    """Listing 内容结构"""
    title: str
    bullet_points: List[str]
    description: str
    keywords: List[str]
    search_terms: List[str]


class AmazonListingGenerator:
    """Amazon Listing 生成器"""
    
    # 标题规则
    TITLE_MAX_LENGTH = 200
    TITLE_PATTERN = "[品牌] + [核心关键词] + [主要卖点] + [适用场景]"
    
    # 五点描述规则
    BULLET_MAX_LENGTH = 500
    BULLET_PATTERN = "[功能亮点大写] + [详细描述] + [用户利益]"
    
    @classmethod
    def generate_title(
        cls,
        brand: str,
        main_keyword: str,
        selling_points: List[str],
        usage_scenario: str = "",
        max_length: int = 200
    ) -> str:
        """
        生成 Amazon 标题
        
        Args:
            brand: 品牌名
            main_keyword: 核心关键词
            selling_points: 卖点列表
            usage_scenario: 适用场景
            max_length: 最大长度
        
        Returns:
            优化后的标题
        """
        # 构建标题
        parts = [brand, main_keyword]
        
        # 添加卖点
        for point in selling_points[:3]:  # 最多3个卖点
            parts.append(point)
        
        # 添加场景
        if usage_scenario:
            parts.append(f"for {usage_scenario}")
        
        title = " ".join(parts)
        
        # 截断
        if len(title) > max_length:
            title = title[:max_length-3] + "..."
        
        return title
    
    @classmethod
    def generate_bullet_points(
        cls,
        features: List[Dict],
        language: str = "en"
    ) -> List[str]:
        """
        生成五点描述
        
        Args:
            features: 功能列表 [{"highlight": "...", "description": "...", "benefit": "..."}]
            language: 语言
        
        Returns:
            五点描述列表
        """
        bullets = []
        
        for feature in features[:5]:  # 最多5点
            highlight = feature.get("highlight", "").upper()
            description = feature.get("description", "")
            benefit = feature.get("benefit", "")
            
            if language == "zh":
                bullet = f"【{highlight}】{description}，{benefit}"
            else:
                bullet = f"✅ {highlight}: {description}. {benefit}"
            
            if len(bullet) > cls.BULLET_MAX_LENGTH:
                bullet = bullet[:cls.BULLET_MAX_LENGTH-3] + "..."
            
            bullets.append(bullet)
        
        return bullets
    
    @classmethod
    def generate_description(
        cls,
        product_intro: str,
        features: List[Dict],
        specifications: Dict,
        faq: List[Dict] = None
    ) -> str:
        """
        生成长描述
        
        Args:
            product_intro: 产品介绍
            features: 功能列表
            specifications: 规格参数
            faq: 常见问题
        
        Returns:
            长描述 HTML
        """
        html_parts = [f"<p>{product_intro}</p>"]
        
        # 功能亮点
        if features:
            html_parts.append("<h2>Key Features</h2><ul>")
            for f in features:
                html_parts.append(f"<li><strong>{f.get('highlight', '')}</strong>: {f.get('description', '')}</li>")
            html_parts.append("</ul>")
        
        # 规格参数
        if specifications:
            html_parts.append("<h2>Specifications</h2><table>")
            for key, value in specifications.items():
                html_parts.append(f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>")
            html_parts.append("</table>")
        
        # FAQ
        if faq:
            html_parts.append("<h2>FAQ</h2>")
            for item in faq:
                html_parts.append(f"<p><strong>Q: {item.get('question', '')}</strong></p>")
                html_parts.append(f"<p>A: {item.get('answer', '')}</p>")
        
        return "\n".join(html_parts)
    
    @classmethod
    def extract_keywords(
        cls,
        competitor_titles: List[str],
        max_keywords: int = 10
    ) -> List[str]:
        """
        从竞品标题提取关键词
        
        Args:
            competitor_titles: 竞品标题列表
            max_keywords: 最大关键词数
        
        Returns:
            关键词列表
        """
        # 停用词
        stop_words = {"the", "a", "an", "and", "or", "but", "for", "with", "to", "of", "in", "on"}
        
        # 词频统计
        word_freq = {}
        
        for title in competitor_titles:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
            for word in words:
                if word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序取前N个
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:max_keywords]]


class TaobaoListingGenerator:
    """淘宝 Listing 生成器"""
    
    # 标题规则
    TITLE_MAX_LENGTH = 60  # 淘宝标题限制30个汉字
    
    @classmethod
    def generate_title(
        cls,
        main_keyword: str,
        selling_points: List[str],
        attributes: Dict = None
    ) -> str:
        """
        生成淘宝标题
        
        Args:
            main_keyword: 核心关键词
            selling_points: 卖点
            attributes: 属性
        
        Returns:
            优化标题
        """
        parts = [main_keyword]
        
        # 添加卖点
        for point in selling_points[:3]:
            parts.append(point)
        
        # 添加属性
        if attributes:
            for key, value in list(attributes.items())[:2]:
                parts.append(f"{key}{value}")
        
        title = " ".join(parts)
        
        return title[:cls.TITLE_MAX_LENGTH]
    
    @classmethod
    def generate_detail_page(
        cls,
        product_intro: str,
        selling_points: List[str],
        specifications: Dict,
        images: List[str] = None
    ) -> str:
        """
        生成详情页内容
        
        Args:
            product_intro: 产品介绍
            selling_points: 卖点
            specifications: 规格
            images: 图片列表
        
        Returns:
            详情页内容
        """
        content = [f"<h2>产品介绍</h2><p>{product_intro}</p>"]
        
        # 卖点
        if selling_points:
            content.append("<h2>产品卖点</h2><ul>")
            for point in selling_points:
                content.append(f"<li>{point}</li>")
            content.append("</ul>")
        
        # 规格
        if specifications:
            content.append("<h2>规格参数</h2><table>")
            for key, value in specifications.items():
                content.append(f"<tr><td>{key}</td><td>{value}</td></tr>")
            content.append("</table>")
        
        # 图片
        if images:
            content.append("<h2>产品图片</h2>")
            for img in images:
                content.append(f'<img src="{img}" alt="产品图片">')
        
        return "\n".join(content)


class ListingOptimizer:
    """Listing 优化器"""
    
    @classmethod
    def optimize_title(cls, title: str, keywords: List[str]) -> str:
        """优化标题，确保关键词覆盖"""
        title_lower = title.lower()
        
        # 检查关键词覆盖
        missing_keywords = []
        for kw in keywords[:3]:  # 最多检查前3个
            if kw.lower() not in title_lower:
                missing_keywords.append(kw)
        
        # 如果有关键词缺失，尝试添加
        if missing_keywords and len(title) < 180:
            # 在标题末尾添加
            additional = " ".join(missing_keywords)
            title = f"{title} {additional}"
        
        return title[:200]
    
    @classmethod
    def check_compliance(cls, listing: ListingContent, platform: str = "amazon") -> Dict:
        """
        检查 Listing 合规性
        
        Args:
            listing: Listing 内容
            platform: 平台
        
        Returns:
            合规性检查结果
        """
        issues = []
        
        # 标题检查
        if len(listing.title) > 200:
            issues.append("标题超过200字符限制")
        
        # 五点描述检查
        for i, bullet in enumerate(listing.bullet_points):
            if len(bullet) > 500:
                issues.append(f"第{i+1}点描述超过500字符限制")
        
        # 关键词检查
        if not listing.keywords:
            issues.append("缺少后台关键词")
        
        return {
            "platform": platform,
            "compliant": len(issues) == 0,
            "issues": issues,
            "score": max(0, 100 - len(issues) * 20)
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Listing 生成器")
    parser.add_argument("command", choices=["title", "bullets", "description", "keywords", "check"])
    parser.add_argument("--brand", "-b", default="BrandName", help="品牌名")
    parser.add_argument("--keyword", "-k", help="核心关键词")
    parser.add_argument("--points", "-p", nargs="+", help="卖点列表")
    parser.add_argument("--scenario", "-s", help="适用场景")
    parser.add_argument("--platform", "-P", choices=["amazon", "taobao"], default="amazon")
    parser.add_argument("--competitors", "-c", nargs="+", help="竞品标题列表")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    if args.command == "title":
        if not args.keyword:
            print("请提供 --keyword 参数")
            sys.exit(1)
        
        points = args.points or ["卖点1", "卖点2"]
        
        if args.platform == "amazon":
            title = AmazonListingGenerator.generate_title(
                brand=args.brand,
                main_keyword=args.keyword,
                selling_points=points,
                usage_scenario=args.scenario
            )
        else:
            title = TaobaoListingGenerator.generate_title(
                main_keyword=args.keyword,
                selling_points=points
            )
        
        if args.json:
            print(json.dumps({"title": title}, ensure_ascii=False, indent=2))
        else:
            print(f"📝 生成的标题:\n{title}")
            print(f"\n长度: {len(title)} 字符")
    
    elif args.command == "bullets":
        # 示例功能点
        features = [
            {"highlight": "DURABLE", "description": "Made of high-quality material", "benefit": "Lasts for years"},
            {"highlight": "EASY TO USE", "description": "Simple one-button operation", "benefit": "Save your time"},
            {"highlight": "COMPACT", "description": "Small and lightweight design", "benefit": "Easy to carry anywhere"}
        ]
        
        bullets = AmazonListingGenerator.generate_bullet_points(features)
        
        if args.json:
            print(json.dumps({"bullet_points": bullets}, ensure_ascii=False, indent=2))
        else:
            print("📝 五点描述:")
            for i, bullet in enumerate(bullets, 1):
                print(f"\n{i}. {bullet}")
    
    elif args.command == "keywords":
        if not args.competitors:
            print("请提供 --competitors 参数")
            sys.exit(1)
        
        keywords = AmazonListingGenerator.extract_keywords(args.competitors)
        
        if args.json:
            print(json.dumps({"keywords": keywords}, ensure_ascii=False, indent=2))
        else:
            print("🔍 提取的关键词:")
            for i, kw in enumerate(keywords, 1):
                print(f"  {i}. {kw}")
    
    elif args.command == "check":
        # 示例检查
        listing = ListingContent(
            title="BrandName Product Name with Great Features for Daily Use and More",
            bullet_points=["Point 1: Description here.", "Point 2: Another description."],
            description="Product description...",
            keywords=["keyword1", "keyword2"],
            search_terms=["term1", "term2"]
        )
        
        result = ListingOptimizer.check_compliance(listing)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"📋 合规性检查: {'✅ 通过' if result['compliant'] else '❌ 有问题'}")
            print(f"评分: {result['score']}/100")
            if result['issues']:
                print("问题:")
                for issue in result['issues']:
                    print(f"  - {issue}")


if __name__ == "__main__":
    main()