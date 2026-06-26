# -*- coding: utf-8 -*-
"""
Report-gama — 俄罗斯医疗器械注册证数据库模块
抓取 Roszdravnadzor（联邦卫生监督局）和 GRLS（国家药品/器械注册系统）的注册证数据
"""

import random
import time
import logging
import re
import json
import os
from datetime import datetime, timedelta
from urllib.parse import quote_plus, urljoin, urlencode
import threading

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"[ERROR] 缺少必需依赖: {e}")
    print("请运行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)

from config import (
    CATEGORY_KEYWORDS, USER_AGENTS, REQUEST_TIMEOUT, REQUEST_RETRIES,
    PROXY, HTTPS_PROXY, LOG_LEVEL, LOG_FORMAT, OUTPUT_DIR, DATA_DIR
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class RegistrationDB:
    """俄罗斯医疗器械注册证数据库"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._country_to_code(country)
        self.session = self._create_session()
        self.results = []
        
        # 创建输出目录
        self.registration_dir = os.path.join(OUTPUT_DIR, "registrations")
        os.makedirs(self.registration_dir, exist_ok=True)
        
        # 医疗器械分类映射
        self.medical_device_categories = {
            "血糖检测设备": ["A10B", "A10B-血糖仪", "глюкометр", "измеритель глюкозы"],
            "血压计": ["A02B", "A02B-血压计", "тонометр", "измеритель артериального давления"],
            "体温计": ["A02A", "A02A-体温计", "термометр"],
            "心电图机": ["B07A", "B07A-心电图机", "электрокардиограф"],
            "雾化器": ["R01A", "R01A-雾化器", "небулайзер"],
            "一次性手套": ["Z29A", "Z29A-手套", "перчатки медицинские"],
        }
        
        # 注册类型映射
        self.registration_types = {
            "medical_device": "Медицинские изделия",
            "pharmaceutical": "Лекарственные средства",
            "diagnostic": "Диагностические средства",
        }

    def _country_to_code(self, country):
        """国家代码映射"""
        codes = {
            "俄罗斯": "RU", "哈萨克斯坦": "KZ", "乌兹别克斯坦": "UZ",
            "白俄罗斯": "BY", "中国": "CN", "美国": "US",
        }
        return codes.get(country, "RU")

    def _create_session(self):
        """创建HTTP会话"""
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": f"{self.lang},en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
        if PROXY:
            session.proxies = {"http": PROXY, "https": HTTPS_PROXY or PROXY}
        return session

    def _make_request(self, url, source_name="generic", max_retries=REQUEST_RETRIES):
        """带重试的HTTP请求"""
        for attempt in range(max_retries + 1):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    # 遵守礼貌爬虫规则，添加延迟
                    time.sleep(random.uniform(3, 5))
                    return response.text
                elif response.status_code == 429:
                    wait_time = (attempt + 1) * 10
                    logger.warning(f"[{source_name}] 请求过于频繁，等待 {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.warning(f"[{source_name}] HTTP {response.status_code}: {url}")
            except requests.RequestException as e:
                logger.warning(f"[{source_name}] 请求失败 (尝试 {attempt+1}/{max_retries+1}): {e}")
                time.sleep(3)
        return None

    def _search_roszdravnadzor(self, product_name):
        """
        在 Roszdravnadzor 网站搜索注册证
        URL: https://roszdravnadzor.gov.ru
        """
        results = []
        try:
            search_url = f"https://roszdravnadzor.gov.ru/search?q={quote_plus(product_name)}&sort=relevance"
            logger.info(f"搜索 Roszdravnadzor: {search_url}")
            
            html = self._make_request(search_url, "roszdravnadzor")
            if not html:
                logger.warning("Roszdravnadzor 搜索失败")
                return results
                
            soup = BeautifulSoup(html, "lxml")
            
            # 解析搜索结果（假设页面结构）
            search_items = soup.select(".search-result-item, .document-item, .result-item")
            
            for item in search_items[:20]:  # 限制结果数量
                try:
                    title_elem = item.select_one(".title, h3, .document-title")
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link_elem = item.select_one("a[href]")
                    url = urljoin("https://roszdravnadzor.gov.ru", link_elem["href"]) if link_elem else ""
                    
                    # 提取注册证编号（模式：RU-XXXX-XXXX-XXXX 或 № РЗН-XXXXXX）
                    reg_number = ""
                    reg_patterns = [
                        r'№\s*(РЗН[\-\s]*[\d\-]+)',
                        r'RU[\-\s]*[\d\-]+',
                        r'Рег\.?\s*№?\s*[\d\-]+',
                        r'регистрационное\s*удостоверение\s*№?\s*[\d\-]+',
                    ]
                    
                    for pattern in reg_patterns:
                        match = re.search(pattern, title, re.IGNORECASE)
                        if match:
                            reg_number = match.group(0).strip()
                            break
                    
                    # 如果没有找到编号，尝试从链接中提取
                    if not reg_number and "number=" in url:
                        match = re.search(r'number=([\d\-]+)', url)
                        if match:
                            reg_number = match.group(1)
                    
                    # 提取日期信息
                    date_text = ""
                    date_elem = item.select_one(".date, .published, time")
                    if date_elem:
                        date_text = date_elem.get_text(strip=True)
                    
                    # 创建结果项
                    if reg_number or "регистра" in title.lower():
                        result = {
                            "reg_number": reg_number,
                            "product_name": title,
                            "holder": self._extract_company(title),
                            "source_url": url,
                            "source": "roszdravnadzor",
                            "date_info": date_text,
                            "confidence": "medium" if reg_number else "low",
                        }
                        results.append(result)
                        
                except Exception as e:
                    logger.debug(f"解析单个结果失败: {e}")
                    continue
            
            logger.info(f"从 Roszdravnadzor 找到 {len(results)} 条结果")
            
        except Exception as e:
            logger.error(f"Roszdravnadzor 搜索异常: {e}")
        
        return results

    def _search_grls(self, product_name):
        """
        在 GRLS (grls.rosminzdrav.ru) 搜索注册证
        URL: https://grls.rosminzdrav.ru
        """
        results = []
        try:
            # GRLS 搜索接口（根据公开信息推测）
            search_url = f"https://grls.rosminzdrav.ru/grls.aspx?s={quote_plus(product_name)}&Eng=&search=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8"
            logger.info(f"搜索 GRLS: {search_url}")
            
            html = self._make_request(search_url, "grls")
            if not html:
                logger.warning("GRLS 搜索失败")
                return results
            
            soup = BeautifulSoup(html, "lxml")
            
            # 尝试解析表格结果
            tables = soup.select("table.grid, table.results, table.data")
            
            for table in tables:
                rows = table.select("tr")
                for row in rows[1:]:  # 跳过表头
                    try:
                        cells = row.select("td")
                        if len(cells) < 3:
                            continue
                        
                        # 假设表格结构：编号 | 名称 | 持有人 | 日期
                        reg_number = cells[0].get_text(strip=True) if len(cells) > 0 else ""
                        product_name_text = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                        holder_text = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                        date_text = cells[3].get_text(strip=True) if len(cells) > 3 else ""
                        
                        # 查找链接
                        link_elem = row.select_one("a")
                        url = urljoin("https://grls.rosminzdrav.ru", link_elem["href"]) if link_elem else ""
                        
                        if reg_number and product_name_text:
                            result = {
                                "reg_number": reg_number,
                                "product_name": product_name_text,
                                "holder": holder_text,
                                "source_url": url,
                                "source": "grls",
                                "date_info": date_text,
                                "confidence": "high",
                            }
                            results.append(result)
                            
                    except Exception as e:
                        logger.debug(f"解析表格行失败: {e}")
                        continue
            
            # 如果没有表格，尝试其他选择器
            if not results:
                items = soup.select(".search-result, .item, .record")
                for item in items[:20]:
                    try:
                        title = item.get_text(strip=True)
                        if "регистра" in title.lower() or product_name.lower() in title.lower():
                            link_elem = item.select_one("a")
                            url = urljoin("https://grls.rosminzdrav.ru", link_elem["href"]) if link_elem else ""
                            
                            # 提取编号
                            reg_number = ""
                            patterns = [r'№\s*[\d\-]+', r'РУ\s*[\d\-]+', r'RU[\d\-]+']
                            for pattern in patterns:
                                match = re.search(pattern, title)
                                if match:
                                    reg_number = match.group(0)
                                    break
                            
                            result = {
                                "reg_number": reg_number,
                                "product_name": title[:200],  # 截断长文本
                                "holder": self._extract_company(title),
                                "source_url": url,
                                "source": "grls",
                                "date_info": "",
                                "confidence": "medium" if reg_number else "low",
                            }
                            results.append(result)
                            
                    except Exception as e:
                        continue
            
            logger.info(f"从 GRLS 找到 {len(results)} 条结果")
            
        except Exception as e:
            logger.error(f"GRLS 搜索异常: {e}")
        
        return results

    def _search_google_backup(self, product_name):
        """
        Google 搜索作为备用数据源
        搜索 site:roszdravnadzor.gov.ru 和 site:grls.rosminzdrav.ru
        """
        results = []
        try:
            # 构建Google搜索查询
            queries = [
                f'site:roszdravnadzor.gov.ru "{product_name}" регистрационное удостоверение',
                f'site:grls.rosminzdrav.ru "{product_name}" РУ',
                f'"регистрационное удостоверение" "{product_name}" Россия',
            ]
            
            for query in queries:
                google_url = f"https://www.google.com/search?q={quote_plus(query)}&hl=ru&gl=RU"
                logger.info(f"Google 搜索: {query}")
                
                html = self._make_request(google_url, "google")
                if not html:
                    continue
                
                soup = BeautifulSoup(html, "lxml")
                
                # 解析Google搜索结果
                for item in soup.select("div.g")[:10]:
                    try:
                        title_elem = item.select_one("h3")
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        link_elem = item.select_one("a[href]")
                        if not link_elem:
                            continue
                        
                        url = link_elem["href"]
                        # 跳过非目标网站的链接
                        if "roszdravnadzor" not in url and "grls" not in url:
                            continue
                        
                        snippet_elem = item.select_one(".VwiC3b, .MUxGbd")
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        # 提取注册证编号
                        reg_number = ""
                        patterns = [
                            r'№\s*(РЗН[\-\s]*[\d\-]+)',
                            r'РУ\s*[\d\-]+',
                            r'RU[\-\s]*[\d\-]+',
                            r'Рег\.?\s*№?\s*[\d\-]+',
                        ]
                        
                        combined_text = title + " " + snippet
                        for pattern in patterns:
                            match = re.search(pattern, combined_text, re.IGNORECASE)
                            if match:
                                reg_number = match.group(0).strip()
                                break
                        
                        if reg_number or "регистра" in combined_text.lower():
                            result = {
                                "reg_number": reg_number,
                                "product_name": title,
                                "holder": self._extract_company(combined_text),
                                "source_url": url,
                                "source": "google",
                                "date_info": "",
                                "confidence": "low",
                            }
                            results.append(result)
                            
                    except Exception as e:
                        logger.debug(f"解析Google结果失败: {e}")
                        continue
                
                time.sleep(2)  # 礼貌延迟
            
            logger.info(f"从Google找到 {len(results)} 条结果")
            
        except Exception as e:
            logger.error(f"Google搜索异常: {e}")
        
        return results

    def _extract_company(self, text):
        """从文本中提取公司名称"""
        # 常见的俄罗斯医疗器械公司关键词
        company_keywords = [
            "ООО", "ЗАО", "АО", "ПАО", "ФГУП", "ГУП", "ИП",
            "LLC", "JSC", "Inc.", "Ltd.", "GmbH", "AG",
            "Medtronic", "Abbott", "Roche", "Johnson & Johnson", "Siemens",
            "Philips", "GE Healthcare", "Bayer", "Novartis", "Sanofi",
            "Биотех", "Медтехника", "Фармацевт", "Медицинские технологии",
            "Омрон", "Анд", "Микролайф", "Литл Доктор", "Элта", "Сателлит",
        ]
        
        text_lower = text.lower()
        
        # 查找公司标识
        for keyword in company_keywords:
            if keyword.lower() in text_lower:
                # 提取公司名称部分
                pattern = rf'([А-ЯЁA-Z][а-яёa-z\-]+\s+{re.escape(keyword)}|{re.escape(keyword)}\s+[«"][^«"]+[»"])'
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(0).strip()
        
        # 如果没有找到，尝试提取看起来像公司名的部分
        words = text.split()
        for i, word in enumerate(words):
            if word in ["ООО", "ЗАО", "АО", "LLC", "Inc."] and i > 0:
                return f"{words[i-1]} {word}"
        
        return "未知"

    def _categorize_product(self, product_name):
        """根据产品名称分类"""
        product_lower = product_name.lower()
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            ru_keywords = keywords.get("ru", [])
            en_keywords = keywords.get("en", [])
            zh_keywords = keywords.get("zh", [])
            
            all_keywords = ru_keywords + en_keywords + zh_keywords
            
            for keyword in all_keywords:
                if keyword.lower() in product_lower:
                    return category
        
        return "其他医疗器械"

    def _parse_registration_detail(self, reg_number, source_url):
        """获取注册证详情（模拟实现）"""
        detail = {
            "reg_number": reg_number,
            "full_name": "",
            "holder": "",
            "holder_address": "",
            "manufacturer": "",
            "manufacturer_country": "",
            "product_type": "",
            "classification": "",
            "reg_date": "",
            "expiry_date": "",
            "changes": [],
            "status": "active",
            "source_url": source_url,
        }
        
        # 尝试从URL获取更多信息
        if source_url and "roszdravnadzor" in source_url:
            try:
                html = self._make_request(source_url, "detail")
                if html:
                    soup = BeautifulSoup(html, "lxml")
                    
                    # 尝试提取详情信息（根据实际页面结构调整）
                    details_table = soup.select_one("table.details, table.info, .document-content")
                    if details_table:
                        # 解析表格或内容
                        rows = details_table.select("tr")
                        for row in rows:
                            cells = row.select("td")
                            if len(cells) >= 2:
                                key = cells[0].get_text(strip=True).lower()
                                value = cells[1].get_text(strip=True)
                                
                                if "наименование" in key or "название" in key:
                                    detail["full_name"] = value
                                elif "держатель" in key or "владелец" in key:
                                    detail["holder"] = value
                                elif "производитель" in key or "manufacturer" in key:
                                    detail["manufacturer"] = value
                                elif "дата регистрации" in key:
                                    detail["reg_date"] = value
                                elif "срок действия" in key or "действительно до" in key:
                                    detail["expiry_date"] = value
                                elif "статус" in key:
                                    detail["status"] = value
            except Exception as e:
                logger.debug(f"解析详情页面失败: {e}")
        
        return detail

    def search_registrations(self, product_name, registration_type="medical_device"):
        """
        搜索医疗器械注册证
        
        Args:
            product_name (str): 产品名称
            registration_type (str): 注册类型，可选值: "medical_device", "pharmaceutical", "diagnostic"
        
        Returns:
            list: 注册证列表，每个元素为字典包含:
                - reg_number: 注册证编号
                - holder: 注册证持有人
                - product_name: 产品名称
                - product_type: 产品类型
                - reg_date: 注册日期
                - expiry_date: 有效期至
                - holder_country: 持有人国家
                - source_url: 数据源URL
                - confidence: 数据置信度
        """
        logger.info(f"搜索注册证: {product_name} (类型: {registration_type})")
        
        all_results = []
        
        # 策略1: Roszdravnadzor 官方数据库
        ros_results = self._search_roszdravnadzor(product_name)
        all_results.extend(ros_results)
        
        # 策略2: GRLS 国家注册系统
        grls_results = self._search_grls(product_name)
        all_results.extend(grls_results)
        
        # 策略3: Google 搜索作为备用
        if len(all_results) < 5:
            google_results = self._search_google_backup(product_name)
            all_results.extend(google_results)
        
        # 去重（基于注册证编号）
        unique_results = []
        seen_numbers = set()
        
        for result in all_results:
            reg_num = result.get("reg_number", "")
            if reg_num and reg_num in seen_numbers:
                continue
            if reg_num:
                seen_numbers.add(reg_num)
            
            # 标准化结果格式
            standardized = {
                "reg_number": reg_num,
                "holder": result.get("holder", ""),
                "product_name": result.get("product_name", product_name),
                "product_type": self._categorize_product(result.get("product_name", "")),
                "reg_date": result.get("date_info", ""),
                "expiry_date": "",
                "holder_country": "俄罗斯",  # 默认为俄罗斯
                "source_url": result.get("source_url", ""),
                "confidence": result.get("confidence", "low"),
                "source": result.get("source", "unknown"),
            }
            unique_results.append(standardized)
        
        # 尝试获取部分结果的详细日期信息
        for result in unique_results[:10]:  # 限制数量
            if result["reg_number"] and not result["reg_date"]:
                detail = self._parse_registration_detail(result["reg_number"], result["source_url"])
                result["reg_date"] = detail.get("reg_date", result["reg_date"])
                result["expiry_date"] = detail.get("expiry_date", result["expiry_date"])
                if detail.get("holder") and not result["holder"]:
                    result["holder"] = detail.get("holder", result["holder"])
        
        # 保存结果
        self._save_results(unique_results, product_name)
        
        logger.info(f"搜索完成，共找到 {len(unique_results)} 个注册证")
        return unique_results

    def get_registration_detail(self, reg_number):
        """获取注册证详情"""
        logger.info(f"获取注册证详情: {reg_number}")
        
        # 首先检查已有结果
        for result in self.results:
            if result.get("reg_number") == reg_number:
                detail = self._parse_registration_detail(reg_number, result.get("source_url"))
                return detail
        
        # 如果没有找到，搜索该注册证
        search_results = self.search_registrations(reg_number)
        for result in search_results:
            if result.get("reg_number") == reg_number:
                detail = self._parse_registration_detail(reg_number, result.get("source_url"))
                return detail
        
        # 如果还是没有，返回基础信息
        return {
            "reg_number": reg_number,
            "full_name": "",
            "holder": "",
            "product_type": "",
            "reg_date": "",
            "expiry_date": "",
            "status": "unknown",
            "source_url": "",
            "error": "未找到该注册证"
        }

    def get_competitor_registrations(self, company_name):
        """获取某公司所有注册证"""
        logger.info(f"获取公司注册证: {company_name}")
        
        # 搜索公司名称
        results = self.search_registrations(company_name)
        
        # 筛选出该公司持有的注册证
        company_results = []
        for result in results:
            holder = result.get("holder", "").lower()
            company_lower = company_name.lower()
            
            if (company_lower in holder or 
                any(word in holder for word in company_lower.split()) or
                self._extract_company(holder).lower() in company_lower):
                company_results.append(result)
        
        # 如果没有找到，尝试其他搜索词
        if not company_results:
            search_terms = [
                f'"{company_name}" регистрационное удостоверение',
                f'держатель "{company_name}"',
            ]
            for term in search_terms:
                term_results = self.search_registrations(term)
                company_results.extend(term_results)
                time.sleep(2)
        
        # 去重
        unique_results = []
        seen = set()
        for result in company_results:
            key = result.get("reg_number", "") + result.get("product_name", "")
            if key and key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        # 保存结果
        self._save_results(unique_results, f"company_{company_name}")
        
        logger.info(f"找到 {len(unique_results)} 个公司注册证")
        return unique_results

    def analyze_competitor_portfolio(self, company_name):
        """分析竞品注册证组合"""
        registrations = self.get_competitor_registrations(company_name)
        
        analysis = {
            "company_name": company_name,
            "total_registrations": len(registrations),
            "by_category": {},
            "by_year": {},
            "recent_registrations": [],
            "expiring_soon": [],
            "portfolio_strength": "low",
        }
        
        # 按品类统计
        for reg in registrations:
            category = reg.get("product_type", "未知")
            analysis["by_category"][category] = analysis["by_category"].get(category, 0) + 1
            
            # 按年份统计
            reg_date = reg.get("reg_date", "")
            if reg_date:
                year_match = re.search(r'\d{4}', reg_date)
                if year_match:
                    year = year_match.group(0)
                    analysis["by_year"][year] = analysis["by_year"].get(year, 0) + 1
            
            # 最近注册（假设最近3年）
            if "2023" in reg_date or "2024" in reg_date or "2025" in reg_date:
                analysis["recent_registrations"].append(reg)
            
            # 即将过期（假设今年）
            expiry = reg.get("expiry_date", "")
            if "2025" in expiry:
                analysis["expiring_soon"].append(reg)
        
        # 评估组合强度
        total = analysis["total_registrations"]
        recent = len(analysis["recent_registrations"])
        
        if total >= 10 and recent >= 3:
            analysis["portfolio_strength"] = "strong"
        elif total >= 5 and recent >= 1:
            analysis["portfolio_strength"] = "medium"
        elif total > 0:
            analysis["portfolio_strength"] = "weak"
        else:
            analysis["portfolio_strength"] = "none"
        
        # 保存分析结果
        self._save_analysis(analysis, company_name)
        
        return analysis

    def get_active_registrations_by_category(self, category):
        """按品类获取有效注册证列表"""
        logger.info(f"按品类获取注册证: {category}")
        
        # 获取该品类的关键词
        category_keywords = CATEGORY_KEYWORDS.get(category, {})
        search_keywords = category_keywords.get("ru", [])[:3]  # 取前3个俄语关键词
        
        all_results = []
        for keyword in search_keywords:
            results = self.search_registrations(keyword)
            all_results.extend(results)
            time.sleep(2)  # 礼貌延迟
        
        # 筛选和去重
        unique_results = []
        seen = set()
        for result in all_results:
            result_category = self._categorize_product(result.get("product_name", ""))
            if result_category == category or category in result.get("product_type", ""):
                key = result.get("reg_number", "") + result.get("product_name", "")
                if key and key not in seen:
                    seen.add(key)
                    unique_results.append(result)
        
        # 标记为"有效"（假设所有找到的都是有效的）
        for result in unique_results:
            result["status"] = "active"
        
        logger.info(f"找到 {len(unique_results)} 个 {category} 品类注册证")
        return unique_results

    def check_registration_expiry(self, company_name, months_ahead=6):
        """检查即将过期的注册证"""
        logger.info(f"检查即将过期的注册证: {company_name} (未来{months_ahead}个月)")
        
        registrations = self.get_competitor_registrations(company_name)
        expiring = []
        
        current_date = datetime.now()
        future_date = current_date + timedelta(days=30 * months_ahead)
        
        date_patterns = [
            r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY
            r'\d{4}\-\d{2}\-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',    # MM/DD/YYYY
        ]
        
        for reg in registrations:
            expiry_str = reg.get("expiry_date", "")
            if not expiry_str:
                continue
            
            for pattern in date_patterns:
                match = re.search(pattern, expiry_str)
                if match:
                    date_str = match.group(0)
                    try:
                        # 尝试解析日期
                        if "." in date_str:
                            expiry_date = datetime.strptime(date_str, "%d.%m.%Y")
                        elif "-" in date_str:
                            expiry_date = datetime.strptime(date_str, "%Y-%m-%d")
                        elif "/" in date_str:
                            expiry_date = datetime.strptime(date_str, "%m/%d/%Y")
                        else:
                            continue
                        
                        # 检查是否在未来N个月内
                        if current_date <= expiry_date <= future_date:
                            days_left = (expiry_date - current_date).days
                            reg["days_until_expiry"] = days_left
                            reg["expiry_date_parsed"] = expiry_date.strftime("%Y-%m-%d")
                            expiring.append(reg)
                        
                    except ValueError:
                        continue
                    break
        
        # 按过期时间排序
        expiring.sort(key=lambda x: x.get("days_until_expiry", 9999))
        
        # 保存结果
        if expiring:
            expiry_file = os.path.join(self.registration_dir, f"expiring_{company_name}.json")
            with open(expiry_file, "w", encoding="utf-8") as f:
                json.dump(expiring, f, ensure_ascii=False, indent=2)
        
        logger.info(f"找到 {len(expiring)} 个即将过期的注册证")
        return expiring

    def _save_results(self, results, query_name):
        """保存搜索结果"""
        if not results:
            return
        
        # 创建文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"registrations_{query_name}_{timestamp}.json"
        filepath = os.path.join(self.registration_dir, filename)
        
        # 保存为JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 同时保存为CSV（简化版）
        csv_file = filepath.replace(".json", ".csv")
        try:
            with open(csv_file, "w", encoding="utf-8") as f:
                # 写入表头
                headers = ["reg_number", "holder", "product_name", "product_type", 
                          "reg_date", "expiry_date", "holder_country", "source_url", "confidence"]
                f.write(",".join(headers) + "\n")
                
                # 写入数据
                for result in results:
                    row = []
                    for header in headers:
                        value = str(result.get(header, "")).replace(",", ";")
                        row.append(f'"{value}"')
                    f.write(",".join(row) + "\n")
        except Exception as e:
            logger.debug(f"保存CSV失败: {e}")
        
        logger.info(f"结果已保存到: {filepath}")

    def _save_analysis(self, analysis, company_name):
        """保存分析结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{company_name}_{timestamp}.json"
        filepath = os.path.join(self.registration_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        logger.info(f"分析结果已保存到: {filepath}")


# ============================================================
# 使用示例
# ============================================================
if __name__ == "__main__":
    # 示例用法
    db = RegistrationDB(country="俄罗斯", lang="ru")
    
    # 1. 搜索注册证
    print("=== 搜索血糖仪注册证 ===")
    results = db.search_registrations("глюкометр")
    for i, result in enumerate(results[:5], 1):
        print(f"{i}. {result.get('reg_number')} - {result.get('product_name')[:50]}...")
    
    # 2. 获取公司注册证
    print("\n=== 获取公司注册证 ===")
    company_regs = db.get_competitor_registrations("Омрон")
    print(f"找到 {len(company_regs)} 个 Omron 注册证")
    
    # 3. 分析竞品组合
    print("\n=== 分析竞品组合 ===")
    analysis = db.analyze_competitor_portfolio("Омрон")
    print(f"组合强度: {analysis['portfolio_strength']}")
    print(f"品类分布: {analysis['by_category']}")
    
    # 4. 检查过期注册证
    print("\n=== 检查过期注册证 ===")
    expiring = db.check_registration_expiry("Омрон")
    print(f"即将过期: {len(expiring)} 个")
    
    print("\n=== 完成 ===")