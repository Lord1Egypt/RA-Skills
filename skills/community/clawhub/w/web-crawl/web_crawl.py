#!/usr/bin/env python3
"""
OpenClaw Web Crawl Tool - Advanced Content Extraction
Enhanced version of web_fetch with multiple extraction modes

Features:
- Multiple extraction modes: text, markdown, links, structured, full
- CSS selector support for targeted extraction
- Intelligent main content detection
- Full HTML to Markdown conversion
- Parallel crawling capability
"""

import re
import json
import concurrent.futures
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    raise ImportError("Required packages: requests, beautifulsoup4. Install: pip3 install requests beautifulsoup4")


class WebCrawler:
    """Advanced web content crawler and extractor"""
    
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
        }
    
    def crawl(
        self,
        url: str,
        mode: str = "markdown",
        max_length: int = 10000,
        selector: str = "",
    ) -> Dict[str, Any]:
        """
        Crawl and extract content from a URL
        
        Args:
            url: Target URL
            mode: Extraction mode (text, markdown, links, structured, full)
            max_length: Maximum content length
            selector: Optional CSS selector for targeted extraction
        
        Returns:
            Dict with success status and extracted content
        """
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            resp.raise_for_status()
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")
            
            # Apply CSS selector if provided
            if selector:
                elements = soup.select(selector)
                if not elements:
                    return {
                        "success": False,
                        "error": f"No elements found for selector: {selector}",
                    }
                # Create new soup with selected elements
                new_soup = BeautifulSoup("<div></div>", "html.parser")
                container = new_soup.div
                for el in elements:
                    container.append(el.copy() if hasattr(el, 'copy') else el)
                soup = new_soup
            
            # Extract based on mode
            if mode == "text":
                result = self._extract_text(soup, max_length)
            elif mode == "markdown":
                result = self._extract_markdown(soup, url, max_length)
            elif mode == "links":
                result = self._extract_links(soup, url, max_length)
            elif mode == "structured":
                result = self._extract_structured(soup, url, max_length)
            elif mode == "full":
                result = self._extract_full(soup, url, max_length)
            else:
                result = self._extract_markdown(soup, url, max_length)
            
            return {
                "success": True,
                "url": url,
                "mode": mode,
                "content": result,
            }
                
        except requests.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}: {url}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Crawl failed: {str(e)}",
            }
    
    def _clean_soup(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Remove useless elements like scripts, styles, ads"""
        for tag in soup.find_all([
            "script", "style", "nav", "footer", "header", 
            "aside", "noscript", "iframe", "svg", "canvas"
        ]):
            tag.decompose()
        return soup
    
    def _extract_text(self, soup: BeautifulSoup, max_length: int) -> str:
        """Extract clean plain text"""
        soup = self._clean_soup(soup)
        text = soup.get_text(separator="\n", strip=True)
        # Clean excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text[:max_length]
    
    def _extract_markdown(self, soup: BeautifulSoup, base_url: str, max_length: int) -> str:
        """Extract content as formatted Markdown"""
        soup = self._clean_soup(soup)
        lines = []
        
        # Extract title
        title = soup.find("title")
        if title:
            title_text = title.get_text(strip=True)
            if title_text:
                lines.append(f"# {title_text}\n")
        
        # Find main content area (smart detection)
        main = (
            soup.find("main")
            or soup.find("article")
            or soup.find(attrs={"role": "main"})
            or soup.find("div", class_=re.compile(r"content|article|post|entry|body", re.I))
            or soup.body
            or soup
        )
        
        if main:
            lines.append(self._tag_to_markdown(main, base_url))
        
        result = "\n".join(lines)
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result[:max_length]
    
    def _tag_to_markdown(self, tag: Tag, base_url: str) -> str:
        """Recursively convert HTML tags to Markdown"""
        parts = []
        
        for child in tag.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:
                    parts.append(text)
                    
            elif isinstance(child, Tag):
                name = child.name
                
                if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                    level = int(name[1])
                    text = child.get_text(strip=True)
                    if text:
                        parts.append(f"\n{'#' * level} {text}\n")
                        
                elif name == "p":
                    text = child.get_text(strip=True)
                    if text:
                        parts.append(f"\n{text}\n")
                        
                elif name == "a":
                    text = child.get_text(strip=True)
                    href = child.get("href", "")
                    if href and text and not href.startswith(("#", "javascript:")):
                        full_url = urljoin(base_url, href)
                        parts.append(f"[{text}]({full_url})")
                    elif text:
                        parts.append(text)
                        
                elif name == "img":
                    alt = child.get("alt", "image")
                    src = child.get("src", "")
                    if src:
                        full_url = urljoin(base_url, src)
                        parts.append(f"![{alt}]({full_url})")
                        
                elif name in ("ul", "ol"):
                    items = child.find_all("li", recursive=False)
                    for i, li in enumerate(items):
                        prefix = f"{i+1}." if name == "ol" else "-"
                        text = li.get_text(strip=True)
                        if text:
                            parts.append(f"\n{prefix} {text}")
                    parts.append("")
                    
                elif name in ("pre", "code"):
                    code = child.get_text()
                    if "\n" in code:
                        parts.append(f"\n```\n{code}\n```\n")
                    else:
                        parts.append(f"`{code.strip()}`")
                        
                elif name == "blockquote":
                    text = child.get_text(strip=True)
                    if text:
                        parts.append(f"\n> {text}\n")
                        
                elif name == "table":
                    parts.append(self._table_to_markdown(child))
                    
                elif name in ("strong", "b"):
                    text = child.get_text(strip=True)
                    if text:
                        parts.append(f"**{text}**")
                        
                elif name in ("em", "i"):
                    text = child.get_text(strip=True)
                    if text:
                        parts.append(f"*{text}*")
                        
                elif name == "br":
                    parts.append("\n")
                    
                elif name == "hr":
                    parts.append("\n---\n")
                    
                else:
                    # Recursively process other tags
                    inner = self._tag_to_markdown(child, base_url)
                    if inner.strip():
                        parts.append(inner)
        
        return " ".join(parts)
    
    def _table_to_markdown(self, table: Tag) -> str:
        """Convert HTML table to Markdown table"""
        rows = table.find_all("tr")
        if not rows:
            return ""
        
        md_rows = []
        for row in rows:
            cells = row.find_all(["th", "td"])
            md_cells = [cell.get_text(strip=True).replace("|", "\\|") for cell in cells]
            if md_cells:
                md_rows.append("| " + " | ".join(md_cells) + " |")
        
        if len(md_rows) > 0:
            # Add separator row
            num_cols = md_rows[0].count("|") - 1
            separator = "| " + " | ".join(["---"] * max(num_cols, 1)) + " |"
            md_rows.insert(1, separator)
        
        return "\n" + "\n".join(md_rows) + "\n"
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str, max_length: int) -> str:
        """Extract all links from the page"""
        links = []
        
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            
            if href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue
                
            full_url = urljoin(base_url, href)
            links.append(f"- [{text or 'link'}]({full_url})")
        
        result = f"Found {len(links)} links:\n\n" + "\n".join(links)
        return result[:max_length]
    
    def _extract_structured(self, soup: BeautifulSoup, base_url: str, max_length: int) -> str:
        """Extract structured data as JSON"""
        data = {
            "url": base_url,
            "title": "",
            "description": "",
            "headings": [],
            "main_text": "",
            "links_count": 0,
            "images_count": 0,
        }
        
        # Title
        title = soup.find("title")
        if title:
            data["title"] = title.get_text(strip=True)
        
        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            data["description"] = meta_desc.get("content", "")
        
        # Headings
        for h in soup.find_all(["h1", "h2", "h3"]):
            text = h.get_text(strip=True)
            if text:
                data["headings"].append({"level": h.name, "text": text})
        
        # Counts
        data["links_count"] = len(soup.find_all("a", href=True))
        data["images_count"] = len(soup.find_all("img"))
        
        # Main text preview
        soup_clean = self._clean_soup(soup)
        data["main_text"] = soup_clean.get_text(separator=" ", strip=True)[:3000]
        
        return json.dumps(data, indent=2, ensure_ascii=False)[:max_length]
    
    def _extract_full(self, soup: BeautifulSoup, base_url: str, max_length: int) -> str:
        """Full extraction: Markdown + Links"""
        md = self._extract_markdown(soup, base_url, max_length // 2)
        links = self._extract_links(soup, base_url, max_length // 4)
        return f"{md}\n\n---\n\n{links}"[:max_length]


def crawl_url(
    url: str,
    mode: str = "markdown",
    max_length: int = 10000,
    selector: str = "",
) -> str:
    """
    Crawl a single URL and return formatted result
    
    Use this for extracting content from web pages.
    """
    crawler = WebCrawler()
    result = crawler.crawl(url, mode, max_length, selector)
    
    if result["success"]:
        return f"✅ Crawled: {result['url']}\n\n{result['content']}"
    else:
        return f"❌ Failed: {result['error']}"


def parallel_crawl(
    urls: List[str],
    mode: str = "markdown",
    max_length: int = 10000,
    max_workers: int = 5,
) -> str:
    """
    Crawl multiple URLs in parallel
    
    Use this for researching multiple sources at once.
    """
    crawler = WebCrawler()
    
    def crawl_one(url: str) -> Dict[str, Any]:
        return crawler.crawl(url, mode, max_length)
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(crawl_one, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"success": False, "error": str(e), "url": url})
    
    # Format results
    output = [f"# Parallel Crawl Results ({len(urls)} URLs)\n"]
    
    for i, result in enumerate(results, 1):
        url = result.get("url", "Unknown")
        output.append(f"\n---\n\n## Source {i}: {url}\n")
        
        if result.get("success"):
            content = result.get("content", "")
            # Truncate if too long
            if len(content) > max_length:
                content = content[:max_length] + "\n\n[Content truncated...]"
            output.append(content)
        else:
            output.append(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    return "\n".join(output)


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python web_crawl.py <url> [mode] [max_length]")
        print("Modes: text, markdown, links, structured, full")
        sys.exit(1)
    
    url = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "markdown"
    max_length = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    
    result = crawl_url(url, mode, max_length)
    print(result)
