#!/usr/bin/env python3
"""
Vocational Education Policy Scraper
职业教育政策信息抓取工具

Automatically scrapes policy documents and project announcements from:
- Ministry of Education (教育部)
- Ministry of Human Resources and Social Security (人社部)
- Provincial Education Departments (各省教育厅)

Usage:
    python scrape_voc_ed_policy.py --keywords "双高计划" --days 30
    python scrape_voc_ed_policy.py --category policy --output results.json
"""

import sys
import os
import json
import time
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, urlparse
import argparse

# Add current directory to path for imports
SKILL_PATH = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_PATH))

# Import i18n helper
try:
    from i18n_helper import I18NHelper, get_i18n
    i18n = I18n_helper = get_i18n(SKILL_PATH)
except ImportError:
    # Fallback if i18n helper not available
    class SimpleI18N:
        def get(self, key, default=None):
            return default or key
        def get_language(self):
            return os.environ.get('HERMES_LANG', os.environ.get('LANG', 'zh'))[:2]
    i18n = SimpleI18N()

# Website configurations
EDU_WEBSITES = {
    "教育部": {
        "base_url": "https://www.moe.gov.cn",
        "policy_url": "https://www.moe.gov.cn/jyb_xxgk/",
        "vocational_url": "https://www.moe.gov.cn/s78/A07/",
        "selectors": {
            "title": "a[title]",
            "date": ".date, .time, span[class*='date'], span[class*='time']",
            "link": "a[href]"
        },
        "keywords": ["职业教育", "双高计划", "1+X证书", "产教融合", "教学成果奖"]
    },
    "人社部": {
        "base_url": "http://www.mohrss.gov.cn",
        "policy_url": "http://www.mohrss.gov.cn/SYrlzyhshbzb/dongtaixinwen/",
        "selectors": {
            "title": "a[title]",
            "date": ".date, .time, span[class*='date'], span[class*='time']",
            "link": "a[href]"
        },
        "keywords": ["职业培训", "技能人才", "职业技能", "工匠精神"]
    },
    "北京市教委": {
        "base_url": "http://jw.beijing.gov.cn",
        "policy_url": "http://jw.beijing.gov.cn/zwgk/zcwj/",
        "selectors": {
            "title": "a[title]",
            "date": ".date, .time, span[class*='date'], span[class*='time']",
            "link": "a[href]"
        },
        "keywords": ["职业教育", "高职", "中职"]
    }
    # Additional provinces can be added here
}

# Category mappings
CATEGORIES = {
    "policy": ["政策", "通知", "规定", "办法", "意见", "Policy", "Notice"],
    "project": ["课题", "申报", "项目", "Project", "Application"],
    "achievement": ["教学成果", "奖", "Award", "Achievement"],
    "integration": ["产教融合", "校企合作", "Integration", "Cooperation"],
    "certificate": ["1+X", "证书", "Certificate"],
    "double_high": ["双高", "高水平", "High Level"]
}


class VocationalEdScraper:
    """Main scraper class for vocational education policy documents"""

    def __init__(self, keywords: Optional[List[str]] = None,
                 days: int = 30,
                 category: Optional[str] = None):
        """
        Initialize the scraper

        Args:
            keywords: List of keywords to filter results
            days: Number of days to look back (default: 30)
            category: Filter by category (policy, project, achievement, etc.)
        """
        self.keywords = keywords or []
        self.days = days
        self.category = category
        self.results: List[Dict] = []
        self.errors: List[str] = []

    def determine_category(self, title: str) -> Optional[str]:
        """
        Determine the category of a document based on keywords

        Args:
            title: Document title

        Returns:
            Category name or None
        """
        if not self.category:
            for cat, cat_keywords in CATEGORIES.items():
                for kw in cat_keywords:
                    if kw in title:
                        return cat
        return self.category

    def filter_by_keywords(self, title: str) -> bool:
        """
        Check if title matches any of the specified keywords

        Args:
            title: Document title

        Returns:
            True if matches, False otherwise
        """
        if not self.keywords:
            return True

        title_lower = title.lower()
        for keyword in self.keywords:
            if keyword.lower() in title_lower:
                return True
        return False

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string to datetime object

        Args:
            date_str: Date string in various formats

        Returns:
            Datetime object or None
        """
        if not date_str:
            return None

        # Common date patterns for Chinese government websites
        patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
            r'(\d{4})\.(\d{1,2})\.(\d{1,2})'
        ]

        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    year, month, day = map(int, match.groups())
                    return datetime(year, month, day)
                except ValueError:
                    continue

        return None

    def is_within_date_range(self, date: datetime) -> bool:
        """
        Check if date is within the specified range

        Args:
            date: Datetime object

        Returns:
            True if within range, False otherwise
        """
        cutoff_date = datetime.now() - timedelta(days=self.days)
        return date >= cutoff_date

    def scrape_website(self, site_name: str, site_config: Dict) -> int:
        """
        Scrape a single website

        Args:
            site_name: Name of the website
            site_config: Configuration dictionary for the website

        Returns:
            Number of documents found
        """
        print(f"\n{i18n.get('messages.fetching', default='Fetching data...')}: {site_name}")

        try:
            import requests
            from bs4 import BeautifulSoup

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Try vocational_url first, then policy_url
            urls_to_try = []
            if 'vocational_url' in site_config and site_config['vocational_url']:
                urls_to_try.append(site_config['vocational_url'])
            if 'policy_url' in site_config and site_config['policy_url']:
                urls_to_try.append(site_config['policy_url'])

            docs_found = 0

            for url in urls_to_try:
                try:
                    print(f"  访问: {url}")
                    response = requests.get(url, headers=headers, timeout=10)
                    response.encoding = response.apparent_encoding
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find all links with titles
                    links = soup.find_all('a', href=True)

                    for link in links:
                        title = link.get('title', '') or link.get_text(strip='')

                        if not title or len(title) < 5:
                            continue

                        # Skip javascript: links and anchors
                        href = link.get('href', '')
                        if not href or href.startswith('javascript:') or href.startswith('#'):
                            continue

                        # Skip navigation links (contains "司" and ends with ')')
                        if re.search(r'司$|委员会$|办公室$', title):
                            continue

                        # Skip IC/licenses info
                        if 'ICP' in title or '网安备' in title:
                            continue

                        # Check if title contains vocational keywords
                        has_vocational_keyword = any(kw in title for kw in site_config.get('keywords', []))

                        # Filter by user-specified keywords
                        if not self.filter_by_keywords(title):
                            continue

                        # Get date from link text or nearby element
                        date_str = ''
                        link_text = link.get_text(strip=True)

                        # Try to extract date from link text
                        date_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', link_text)
                        if date_match:
                            date_str = date_match.group(0)
                        else:
                            # Try Chinese date format
                            date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', link_text)
                            if date_match:
                                year, month, day = date_match.groups()
                                date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                        # Parse date
                        doc_date = self.parse_date(date_str) if date_str else None

                        # Check if within date range
                        if doc_date and not self.is_within_date_range(doc_date):
                            continue

                        # Get full URL
                        href = link.get('href', '')
                        if href:
                            full_url = urljoin(url, href)
                        else:
                            continue

                        # Determine category
                        category = self.determine_category(title)

                        # Add to results
                        result = {
                            "title": title,
                            "url": full_url,
                            "date": date_str or datetime.now().strftime("%Y-%m-%d"),
                            "source": site_name,
                            "category": category,
                            "keywords": [kw for kw in site_config.get('keywords', []) if kw in title]
                        }

                        # Only add if not duplicate
                        if not any(r['title'] == title and r['url'] == full_url for r in self.results):
                            self.results.append(result)
                            docs_found += 1
                            print(f"    ✓ {title}")

                except Exception as e:
                    error_msg = f"{url}: {str(e)}"
                    self.errors.append(error_msg)
                    print(f"    ⚠️  错误: {str(e)[:100]}")
                    continue

            return docs_found

        except ImportError:
            error_msg = "缺少依赖库: requests 或 beautifulsoup4。请安装: pip install requests beautifulsoup4"
            self.errors.append(error_msg)
            print(f"❌ {error_msg}")
            return 0

    def scrape_all(self) -> Dict:
        """
        Scrape all configured websites

        Returns:
            Dictionary containing results summary
        """
        total_docs = 0
        sites_scraped = 0

        print(i18n.get('title', default='Vocational Education Policy Scraper'))
        print("=" * 50)

        for site_name, site_config in EDU_WEBSITES.items():
            try:
                docs = self.scrape_website(site_name, site_config)
                total_docs += docs
                sites_scraped += 1
                time.sleep(1)  # Be respectful to servers
            except Exception as e:
                error_msg = f"{site_name}: {str(e)}"
                self.errors.append(error_msg)
                print(f"❌ {i18n.get('messages.error', default='Error')}: {error_msg}")

        summary = {
            "websites_scraped": sites_scraped,
            "total_documents": total_docs,
            "results": self.results,
            "errors": self.errors,
            "timestamp": datetime.now().isoformat(),
            "filters": {
                "keywords": self.keywords,
                "days": self.days,
                "category": self.category
            }
        }

        return summary

    def save_results(self, results: Dict, output_file: str = None) -> str:
        """
        Save results to a file

        Args:
            results: Results dictionary
            output_file: Output file path

        Returns:
            Path to saved file
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"voc_ed_policy_{timestamp}.json"

        output_path = Path(output_file)
        output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')

        print(f"\n{i18n.get('messages.saving', default='Saving results...')}")
        print(f"✅ {i18n.get('output.title', default='Results saved to')}: {output_path.absolute()}")

        return str(output_path.absolute())

    def print_summary(self, results: Dict):
        """
        Print a formatted summary of results

        Args:
            results: Results dictionary
        """
        print("\n" + "=" * 50)
        print(i18n.get('output.summary', default='Summary'))
        print("=" * 50)
        print(f"{i18n.get('output.websites_scraped', default='Websites Scraped')}: {results['websites_scraped']}")
        print(f"{i18n.get('output.files_found', default='Files Found')}: {results['total_documents']}")

        if results['errors']:
            print(f"\n{i18n.get('output.errors', default='Errors')}:")
            for error in results['errors']:
                print(f"  • {error}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description=i18n.get('description', default='Vocational Education Policy Scraper'),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_voc_ed_policy.py --keywords "双高计划" "产教融合" --days 30
  python scrape_voc_ed_policy.py --category policy --output policy_results.json
  python scrape_voc_ed_policy.py --keywords "1+X证书" --days 7
        """
    )

    parser.add_argument(
        '--keywords',
        nargs='+',
        help='Keywords to filter results (e.g., "双高计划" "产教融合")'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to look back (default: 30)'
    )
    parser.add_argument(
        '--category',
        choices=['policy', 'project', 'achievement', 'integration', 'certificate', 'double_high'],
        help='Filter by category'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: auto-generated timestamped JSON)'
    )
    parser.add_argument(
        '--lang',
        choices=['zh', 'en'],
        help='Language (zh/en)'
    )

    args = parser.parse_args()

    # Override language if specified
    if args.lang:
        i18n.lang = args.lang

    # Create scraper
    scraper = VocationalEdScraper(
        keywords=args.keywords,
        days=args.days,
        category=args.category
    )

    # Scrape all websites
    results = scraper.scrape_all()

    # Save results
    scraper.save_results(results, args.output)

    # Print summary
    scraper.print_summary(results)


if __name__ == "__main__":
    main()