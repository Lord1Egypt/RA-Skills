#!/usr/bin/env python3
"""
监管动态爬虫 - 支持 NFRA, CSRC, PBOC
================================================
本脚本支持对国家金融监督管理总局 (NFRA)、证监会 (CSRC)、人民银行 (PBOC) 
官网的监管动态进行抓取。

使用方法:
  python3 crawler.py --regulator nfra --days 30
  python3 crawler.py --regulator csrc --days 7
  python3 crawler.py --regulator pboc --days 14
  python3 crawler.py --regulator all --days 7

依赖: pip install requests beautifulsoup4
"""

import requests
import json
import time
import argparse
import sys
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# ─── 通用配置与设置 ─────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

def is_recent(date_str: str, days: int) -> bool:
    """判断日期是否在最近 N 天内"""
    if not date_str or date_str == "未知":
        return False
    try:
        # 兼容多种日期格式
        date_str = date_str.strip()
        if "/" in date_str:
            pub_date = datetime.strptime(date_str[:10], "%Y/%m/%d")
        else:
            pub_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return pub_date >= datetime.now() - timedelta(days=days)
    except Exception:
        return True

def clean_html_content(html_content: str) -> str:
    """清洗带有 HTML 标签的正文内容"""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    for s in soup(["script", "style"]):
        s.decompose()
    
    raw_text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    
    cleaned_lines = []
    if lines:
        current_paragraph = lines[0]
        for next_line in lines[1:]:
            if current_paragraph.endswith(("。", "！", "？", "?", "！", "”", "；", "：", ":", "；")):
                cleaned_lines.append(current_paragraph)
                current_paragraph = next_line
            else:
                if re.match(r"^(\([一二三四五六七八九十]+\)|[0-9]+\.|[一二三四五六七八九十]+、)", next_line):
                    cleaned_lines.append(current_paragraph)
                    current_paragraph = next_line
                else:
                    current_paragraph += next_line
        cleaned_lines.append(current_paragraph)
    
    return "\n\n".join(cleaned_lines)

# ─── NFRA 爬虫 ────────────────────────────────────────────────────────────────

class NFRACrawler:
    BASE_URL = "https://www.nfra.gov.cn"
    API_TEMPLATE = "https://www.nfra.gov.cn/cn/static/data/DocInfo/SelectDocByItemIdAndChild/data_itemId={itemId},pageIndex={pageIndex},pageSize={pageSize}.json"
    DETAIL_API = "https://www.nfra.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId={docId}.json"
    
    CHANNELS = [
        {"name": "政策规章规范性文件", "itemId": "928", "category": "⚖️ 监管政策/规章"},
        {"name": "行政处罚（总局机关）", "itemId": "4113", "category": "🔨 行政处罚案例"},
        {"name": "征求意见", "itemId": "951", "category": "📋 征求意见"},
    ]

    def fetch_list(self, item_id: str, page: int = 1) -> List[Dict]:
        url = self.API_TEMPLATE.format(itemId=item_id, pageIndex=page, pageSize=18)
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            data = r.json()
            if data.get("rptCode") != 200: return []
            
            results = []
            for row in data.get("data", {}).get("rows", []):
                doc_id = row.get("docId")
                results.append({
                    "title": (row.get("docTitle") or row.get("docSubtitle") or "无标题").strip(),
                    "url": f"{self.BASE_URL}/cn/view/pages/ItemDetail.html?docId={doc_id}&itemId={item_id}&generaltype=1",
                    "date": (row.get("publishDate") or row.get("builddate") or "")[:10],
                    "docId": doc_id,
                    "attachments": self._get_attachments(row),
                    "summary": row.get("docSummary") or ""
                })
            return results
        except Exception as e:
            print(f"  ❌ NFRA 抓取列表失败: {e}")
            return []

    def _get_attachments(self, row):
        atts = []
        if row.get("pdfFileUrl"): atts.append({"name": "PDF文件", "url": urljoin(self.BASE_URL, row["pdfFileUrl"])})
        if row.get("docFileUrl"): atts.append({"name": "DOC文件", "url": urljoin(self.BASE_URL, row["docFileUrl"])})
        return atts

    def fetch_detail(self, doc_id: str) -> str:
        url = self.DETAIL_API.format(docId=doc_id)
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            data = r.json()
            if data.get("rptCode") != 200: return "接口异常"
            return clean_html_content(data.get("data", {}).get("docClob", ""))
        except Exception as e:
            return f"详情获取失败: {e}"

# ─── CSRC 爬虫 ────────────────────────────────────────────────────────────────

class CSRCCrawler:
    BASE_URL = "https://www.csrc.gov.cn"
    CHANNELS = [
        {
            "name": "监管规定",
            "url": "https://www.csrc.gov.cn/searchList/cd11df89f5894c1eac37ae37cc11e369?_isAgg=true&_isJson=true&_pageSize=10&_template=index&page={page}",
            "category": "⚖️ 监管政策/规章"
        },
        {
            "name": "行政处罚",
            "url": "https://www.csrc.gov.cn/searchList/17d5ff2fe43e488dba825807ae40d63f?_isAgg=true&_isJson=true&_pageSize=10&_template=index&page={page}",
            "category": "🔨 行政处罚案例"
        }
    ]

    def fetch_list(self, channel_url: str, page: int = 1) -> List[Dict]:
        url = channel_url.format(page=page)
        try:
            headers = HEADERS.copy()
            headers["Referer"] = "https://www.csrc.gov.cn/"
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            data = r.json()
            
            results = []
            for item in data.get("data", {}).get("results", []):
                doc_no = ""
                meta_list = item.get("domainMetaList", [])
                if meta_list and "resultList" in meta_list[0]:
                    for m in meta_list[0]["resultList"]:
                        if m.get("name") == "文号":
                            doc_no = f" [{m.get('value')}]"
                            break

                results.append({
                    "title": f"{item.get('title')}{doc_no}".strip(),
                    "url": urljoin(self.BASE_URL, item.get("url")),
                    "date": item.get("publishedTimeStr", "")[:10]
                })
            return results
        except Exception as e:
            print(f"  ❌ CSRC 抓取列表失败: {e}")
            return []

    def fetch_detail(self, url: str) -> Dict:
        """
        抓取证监会详情页，获取完整正文和正确的附件链接
        """
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            
            # 正文提取
            # 证监会正文通常在 class="content" 或特定的 div 中
            content_div = soup.find(class_="content") or soup.find(id="main")
            if content_div:
                content = clean_html_content(str(content_div))
            else:
                content = clean_html_content(r.text)
                
            # 附件提取 - 证监会附件通常是相对路径，需要相对于当前 URL 拼接
            attachments = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                # 过滤掉常见的导航链接，关注包含 files 的路径或者特定后缀
                if "files/" in href.lower() or any(href.lower().endswith(ext) for ext in [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip"]):
                    name = a.get_text(strip=True) or "附件"
                    abs_url = urljoin(url, href)
                    attachments.append({"name": name, "url": abs_url})
            
            return {"content": content, "attachments": attachments}
        except Exception as e:
            return {"content": f"获取详情失败: {e}", "attachments": []}

# ─── PBOC 爬虫 ────────────────────────────────────────────────────────────────

class PBOCCrawler:
    BASE_URL = "https://www.pbc.gov.cn"
    BJ_BASE_URL = "https://beijing.pbc.gov.cn"
    
    CHANNELS = [
        {"name": "人行条法司行政法规", "url": "https://www.pbc.gov.cn/tiaofasi/144941/144953/index.html", "category": "⚖️ 监管政策/规章"},
        {"name": "人行条法司部门规章", "url": "https://www.pbc.gov.cn/tiaofasi/144941/144957/index.html", "category": "⚖️ 监管政策/规章"},
        {"name": "人行条法司规范性文件", "url": "https://www.pbc.gov.cn/tiaofasi/144941/3581332/index.html", "category": "⚖️ 监管政策/规章"},
        {"name": "人行北京分行行政处罚", "url": "https://beijing.pbc.gov.cn/beijing/132030/132052/132059/index.html", "category": "🔨 行政处罚案例", "is_bj": True},
    ]

    def fetch_list(self, channel: Dict) -> List[Dict]:
        try:
            r = requests.get(channel["url"], headers=HEADERS, timeout=30)
            r.raise_for_status()
            # PBOC 编码有时不固定，尝试检测
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")
            
            results = []
            base = self.BJ_BASE_URL if channel.get("is_bj") else self.BASE_URL
            blacklist = ["无障碍", "网站地图", "联系我们", "法律声明", "关于我们", "政府信息公开"]
            
            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                if len(title) < 5: continue # 过滤掉导航等短链接
                if any(word in title for word in blacklist): continue
                
                date_str = ""
                # 寻找日期：
                if channel.get("is_bj"):
                    # 北京分行：在 tr 的后续 td 中
                    parent_tr = a.find_parent("tr")
                    if parent_tr:
                        all_tds = parent_tr.find_all("td")
                        for td in all_tds:
                            txt = td.get_text(strip=True)
                            if re.search(r"\d{4}-\d{1,2}-\d{1,2}", txt):
                                date_str = txt
                                break
                else:
                    # 总行条法司：通常在 a 的同级 span.hui12 中
                    parent_td = a.find_parent("td")
                    if parent_td:
                        span = parent_td.find("span", class_="hui12")
                        if span:
                            date_str = span.get_text(strip=True)
                        else:
                            # 托底方案：在文本中搜索 YYYY-MM-DD
                            date_match = re.search(r"\d{4}-\d{1,2}-\d{1,2}", parent_td.get_text())
                            if date_match:
                                date_str = date_match.group()
                
                href = a["href"]
                if not href.startswith("http"):
                    href = urljoin(base, href)
                
                # 过滤并去重
                if "/index.html" in href and len(href.split("/")) > 6:
                    # 过滤掉明显的导航或目录链接（准则：必须有日期，或者标题足够长且不是纯导航词）
                    if date_str and date_str != "未知":
                        results.append({
                            "title": title,
                            "url": href,
                            "date": date_str,
                            "is_bj": channel.get("is_bj", False)
                        })
            
            # 去重
            seen = set()
            unique_results = []
            for item in results:
                if item["url"] not in seen:
                    unique_results.append(item)
                    seen.add(item["url"])
            return unique_results
        except Exception as e:
            print(f"  ❌ PBOC 抓取列表失败: {e}")
            return []

    def fetch_detail(self, url: str, is_bj: bool = False) -> Dict:
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")
            
            # 附件处理
            attachments = []
            for a in soup.find_all("a", href=True):
                if any(ext in a["href"].lower() for ext in [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip"]):
                    atts_name = a.get_text(strip=True) or "附件"
                    atts_url = urljoin(url, a["href"])
                    attachments.append({"name": atts_name, "url": atts_url})

            if is_bj:
                # 北京分行提取表格内容
                # 优先查找 class="hei14jj" 的容器，这是北京分行存放主表格的标准位置
                container = soup.find(class_="hei14jj")
                table = None
                if container:
                    table = container.find("table")
                
                # 如果没找到，尝试托底寻找包含“序号”的表格
                if not table:
                    for t in soup.find_all("table"):
                        if "序号" in t.get_text():
                            table = t
                            break

                if table:
                    # 将表格转换为文本格式
                    rows = []
                    for tr in table.find_all("tr"):
                        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                        if any(cells): # 过滤空行
                            rows.append(" | ".join(cells))
                    content = "\n".join(rows)
                else:
                    content = clean_html_content(r.text)
            else:
                # 条法司常规正文
                # 通常在 id="zoom" 或 class="content" 中
                zoom = soup.find(id="zoom") or soup.find(class_="content")
                if zoom:
                    content = clean_html_content(str(zoom))
                else:
                    content = clean_html_content(r.text)
            
            return {"content": content, "attachments": attachments}
        except Exception as e:
            return {"content": f"获取详情失败: {e}", "attachments": []}

# ─── 统一输出格式 ─────────────────────────────────────────────────────────────

def format_output(regulator_name: str, channel: Dict, articles: List[Dict]) -> str:
    lines = []
    lines.append(f"\n{'═'*60}")
    lines.append(f"【{regulator_name}】{channel['category']}")
    lines.append(f"栏目：{channel['name']}（获取到 {len(articles)} 条）")
    lines.append(f"{'═'*60}\n")

    if not articles:
        lines.append("  (暂无符合条件的新动态)")
    else:
        for art in articles:
            lines.append(f"📌 标题：{art['title']}")
            lines.append(f"📅 日期：{art['date']}")
            lines.append(f"🔗 链接：{art['url']}")
            
            if art.get("full_content"):
                lines.append("📖 正文内容：")
                lines.append(art["full_content"])
            
            if art.get("attachments"):
                lines.append("📎 附件：")
                for att in art["attachments"]:
                    lines.append(f"   - {att.get('name', '附件')}: {att['url']}")
            lines.append("─" * 60)

    return "\n".join(lines)

# ─── 主函数 ───────────────────────────────────────────────────────────────────

def run_nfra(days: int):
    crawler = NFRACrawler()
    all_res = []
    total = 0
    for ch in crawler.CHANNELS:
        print(f"🔍 正在处理 NFRA：{ch['name']}...")
        raw = crawler.fetch_list(ch["itemId"])
        articles = [a for a in raw if is_recent(a["date"], days)]
        for a in articles:
            a["full_content"] = crawler.fetch_detail(a["docId"])
            time.sleep(0.5)
        all_res.append(format_output("国家金融监督管理总局 NFRA", ch, articles))
        total += len(articles)
    return "\n".join(all_res), total

def run_csrc(days: int):
    crawler = CSRCCrawler()
    all_res = []
    total = 0
    for ch in crawler.CHANNELS:
        print(f"🔍 正在处理证监会 CSRC：{ch['name']}...")
        raw = crawler.fetch_list(ch["url"])
        articles = [a for a in raw if is_recent(a["date"], days)]
        for a in articles:
            print(f"    🔎 抓取详情: {a['title'][:30]}...")
            detail = crawler.fetch_detail(a["url"])
            a["full_content"] = detail["content"]
            a["attachments"] = detail["attachments"]
            time.sleep(0.5)
        all_res.append(format_output("证监会 CSRC", ch, articles))
        total += len(articles)
    return "\n".join(all_res), total

def run_pboc(days: int):
    crawler = PBOCCrawler()
    all_res = []
    total = 0
    for ch in crawler.CHANNELS:
        print(f"🔍 正在处理央行 PBOC：{ch['name']}...")
        raw = crawler.fetch_list(ch)
        articles = [a for a in raw if is_recent(a["date"], days)]
        for a in articles:
            detail = crawler.fetch_detail(a["url"], a.get("is_bj", False))
            a["full_content"] = detail["content"]
            a["attachments"] = detail["attachments"]
            time.sleep(0.5)
        all_res.append(format_output("人民银行 PBOC", ch, articles))
        total += len(articles)
    return "\n".join(all_res), total

def main():
    parser = argparse.ArgumentParser(description="多机构监管动态爬虫")
    parser.add_argument("--regulator", type=str, default="all", choices=["nfra", "csrc", "pboc", "all"], help="指定监管机构")
    parser.add_argument("--days", type=int, default=30, help="抓取最近 N 天内容（默认30天）")
    parser.add_argument("--output", type=str, default=None, help="输出到文件")
    args = parser.parse_args()

    print(f"🚀 开始抓取监管动态 (机构: {args.regulator}, 周期: {args.days} 天)...")
    
    final_output = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    final_output.append(f"📊 金融监管动态简报")
    final_output.append(f"监控时间：{now_str} | 监控周期：{args.days}天")
    final_output.append("") # 统计占位

    total_articles = 0
    
    if args.regulator in ["nfra", "all"]:
        out, count = run_nfra(args.days)
        final_output.append(out)
        total_articles += count
    
    if args.regulator in ["csrc", "all"]:
        out, count = run_csrc(args.days)
        final_output.append(out)
        total_articles += count
        
    if args.regulator in ["pboc", "all"]:
        out, count = run_pboc(args.days)
        final_output.append(out)
        total_articles += count

    final_output[2] = f"统计：本次共发现 {total_articles} 条新动态"
    result_text = "\n".join(final_output)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_text)
        print(f"\n✨ 结果已保存至: {args.output}")
    else:
        print("\n" + result_text)

if __name__ == "__main__":
    main()
