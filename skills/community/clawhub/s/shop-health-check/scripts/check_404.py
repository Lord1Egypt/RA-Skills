#!/usr/bin/env python3
"""
check_404.py - 分类页爬取 + 商品页抽检 + 内容错误检测
动态爬取分类页，从中随机抽取商品页检测 404 和错误内容
"""
import sys
import random
import configparser
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: 缺少依赖库。请运行: pip3 install requests beautifulsoup4")
    sys.exit(1)


# 在商品列表容器中常见的标签/属性模式（适配不同建站系统）
PRODUCT_LINK_SELECTORS = [
    "a[href*='/products/']",
    "a.product-item__link",
    "a.product-card__link",
    "a[class*='product']",
    "a[href*='/p/']",
    "a[href*='/item/']",
]

# 检测错误内容的关键词
ERROR_KEYWORDS = [
    "this product is no longer available",
    "此商品已下架",
    "商品已下架",
    "page not found",
    "404",
    "not found",
    "the page you're looking for",
    "product not found",
    "sold out",
    "out of stock",
]


def extract_product_links(html, base_url):
    """从 HTML 中提取商品链接"""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for selector in PRODUCT_LINK_SELECTORS:
        for a in soup.select(selector):
            href = a.get("href", "")
            if href:
                # 补全相对路径
                full_url = urljoin(base_url, href)
                # 只保留同域名的商品页
                if base_url.split("//")[1].split("/")[0] in full_url:
                    links.add(full_url)
    return list(links)


def check_product_page(url, timeout=3):
    """检查单个商品页的状态和内容"""
    result = {
        "url": url,
        "status": None,
        "content_check": None,
        "error": None,
        "ok": True,
        "is_404": False,
        "has_error_text": False
    }
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        result["status"] = response.status_code

        if response.status_code == 404:
            result["is_404"] = True
            result["ok"] = False
            return result

        if response.status_code != 200:
            result["ok"] = False
            return result

        # 检查错误内容
        text = response.text.lower()
        for keyword in ERROR_KEYWORDS:
            if keyword.lower() in text:
                result["has_error_text"] = True
                result["content_check"] = f"检测到错误内容: {keyword}"
                result["ok"] = False
                break

    except requests.exceptions.Timeout:
        result["error"] = "超时"
        result["ok"] = False
    except Exception as e:
        result["error"] = str(e)[:80]
        result["ok"] = False
    return result


def crawl_category_for_products(base_url, category_path, sample_size=5, timeout=3):
    """爬取分类页，抽取商品页链接"""
    category_url = base_url.rstrip("/") + "/" + category_path.lstrip("/")
    try:
        resp = requests.get(category_url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        if resp.status_code != 200:
            return []
        links = extract_product_links(resp.text, base_url)
        if len(links) > sample_size:
            return random.sample(links, sample_size)
        return links
    except Exception:
        return []


def check_shop_products(config, shop_name, sample_size=None):
    """检查指定店铺的分类页商品可用性"""
    base_url = config.get(shop_name, "base_url")
    default_sample = int(config.get(shop_name, "check_sample_size", fallback=5))
    sample_size = sample_size or default_sample

    category_paths_str = config.get(shop_name, "category_paths", fallback="")
    if not category_paths_str:
        return []

    category_paths = [p.strip() for p in category_paths_str.split(",") if p.strip()]

    all_results = []
    for cat_path in category_paths:
        product_urls = crawl_category_for_products(base_url, cat_path, sample_size)
        for product_url in product_urls:
            r = check_product_page(product_url)
            r["category"] = cat_path
            all_results.append(r)

    return all_results


def load_config(config_path):
    """加载配置文件"""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def main():
    config_path = __file__.replace("scripts/check_404.py", "config/shops.conf")
    config = load_config(config_path)

    all_results = {}
    for shop in config.sections():
        if shop == "DEFAULT":
            continue
        shop_name = config.get(shop, "name", fallback=shop)
        results = check_shop_products(config, shop)
        all_results[shop] = {"name": shop_name, "results": results}

    # 输出
    for shop, data in all_results.items():
        print(f"\n📦 {data['name']}")
        results = data["results"]
        if not results:
            print("   ⚠️  未检测到商品页（分类页可能为空或无法访问）")
            continue

        ok_count = sum(1 for r in results if r["ok"])
        print(f"   🔍 抽检 {len(results)} 个商品页，{ok_count} 个正常")

        for r in results:
            if r["ok"]:
                print(f"   ✅ {r['url']}")
            elif r["is_404"]:
                print(f"   ❌ 404: {r['url']}")
            elif r["has_error_text"]:
                print(f"   ❌ 内容错误: {r['url']} — {r['content_check']}")
            else:
                print(f"   ❌ 错误: {r['url']} — {r.get('error', 'unknown')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())