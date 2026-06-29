#!/usr/bin/env python3
"""
亚马逊/Shopify/TikTok Shop Listing 生成器
基于 TokenApi 计费网关，支持多平台格式与多语言输出。

Usage:
    python listing_generator.py --product "无线蓝牙耳机" --keywords "降噪,长续航" --platform amazon --lang zh
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

_SCRIPT_DIR = Path(__file__).resolve().parent
_SHARED_DIR = _SCRIPT_DIR.parent.parent / "_shared"
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))
from bootstrap import ensure_harness_packages_path

ensure_harness_packages_path(__file__)
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from format_listing import format_listing
from tokenapi_harness import Harness, get_catalog
from tokenapi_harness.listing_delivery import (
    listing_payload_from_data,
    resolve_listing_validation,
)
from tokenapi_sdk import TokenApiError

SKILL_NAME = "tokenapi-ecommerce-listing"
SKILL_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_FILES = {
    "amazon": "amazon-prompt-v1.txt",
    "shopify": "shopify-prompt-v1.txt",
    "tiktok": "tiktok-prompt-v1.txt",
}
REFERENCE_FILES = {
    "amazon": "platform-rules-amazon.md",
    "shopify": "shopify-best-practices.md",
    "tiktok": "tiktok-shop-tips.md",
}

LISTING_SCENE = "listing"

@dataclass
class ListingResult:
    """Listing 生成结果"""
    title: str
    bullet_points: List[str]
    description: str
    keywords: List[str]
    platform: str
    language: str
    model_used: str
    tokens_used: int
    meta_title: str = ""
    meta_description: str = ""
    hashtags: List[str] = field(default_factory=list)
    hook: str = ""
    validation: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def _listing_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "bullet_points": self.bullet_points,
            "description": self.description,
            "keywords": self.keywords,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "hashtags": self.hashtags,
            "hook": self.hook,
        }

    def to_amazon_format(self) -> str:
        return format_listing(self._listing_dict(), "amazon", self.language)

    def to_shopify_format(self) -> str:
        return format_listing(self._listing_dict(), "shopify", self.language)

    def to_tiktok_format(self) -> str:
        return format_listing(self._listing_dict(), "tiktok", self.language)


class ListingGenerator:
    """
    Listing 生成器核心类

    平台 / 语种 / 品类白名单来自 harness/catalog.yaml（见 get_catalog()）。
    """

    def __init__(
        self,
        platform: str = "amazon",
        lang: str = "zh",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self._catalog = get_catalog()
        platforms = self._catalog.scene_platform_ids(LISTING_SCENE)
        locales = self._catalog.locale_ids()
        if platform not in platforms:
            raise ValueError(f"Unsupported platform: {platform}. Use: {list(platforms)}")
        if lang not in locales:
            raise ValueError(f"Unsupported language: {lang}. Use: {list(locales)}")

        self.platform = platform
        self.lang = lang

        self.harness = Harness(
            skill_name=SKILL_NAME,
            api_key=api_key or os.getenv("TOKENAPI_KEY"),
            base_url=base_url or os.getenv("TOKENAPI_BASE_URL"),
        )
        self.last_run_id: Optional[str] = None

    @staticmethod
    def load_prompt_template(platform: str) -> str:
        """离线测试：从 harness/ 加载模板。"""
        from tokenapi_harness.assets import load_text
        from tokenapi_harness.paths import discover_harness_root

        filename = TEMPLATE_FILES.get(platform)
        if not filename:
            raise ValueError(f"No template for platform: {platform}")
        root = discover_harness_root()
        return load_text(root / "scenes" / "listing" / "templates" / filename)

    @staticmethod
    def load_reference_excerpt(platform: str, max_chars: int = 2000) -> str:
        """离线测试：从 harness/platforms 加载规范。"""
        from tokenapi_harness.catalog import HarnessCatalog
        from tokenapi_harness.composer import load_platform_knowledge
        from tokenapi_harness.paths import discover_harness_root

        root = discover_harness_root()
        cat = HarnessCatalog.load(root)
        return load_platform_knowledge(cat, platform, max_chars=max_chars)

    def _parse_listing_response(
        self,
        data: Dict[str, Any],
        keywords: List[str],
        run_model: str,
        tokens_used: int,
        validation: Optional[Dict[str, Any]] = None,
    ) -> ListingResult:
        payload = listing_payload_from_data(data, keywords_fallback=keywords)
        return ListingResult(
            title=payload["title"],
            bullet_points=payload["bullet_points"],
            description=payload["description"],
            keywords=payload["keywords"],
            platform=self.platform,
            language=self.lang,
            model_used=run_model,
            tokens_used=tokens_used,
            meta_title=payload["meta_title"],
            meta_description=payload["meta_description"],
            hashtags=payload["hashtags"],
            hook=payload["hook"],
            validation=validation,
        )

    def generate(
        self,
        product: str,
        keywords: List[str],
        features: Optional[List[str]] = None,
        target_audience: Optional[str] = None,
        competitor_info: Optional[str] = None,
        brand_tone: Optional[str] = None,
        category: Optional[str] = None,
        external_id: Optional[str] = None,
        asin: Optional[str] = None,
        listing_id: Optional[str] = None,
        sku: Optional[str] = None,
        user_id: Optional[str] = None,
        temperature: float = 0.7,
        strict_validation: bool = False,
    ) -> ListingResult:
        payload: Dict[str, Any] = {
            "platform": self.platform,
            "lang": self.lang,
            "product": product,
            "keywords": keywords,
            "features": features,
            "target_audience": target_audience,
            "competitor_info": competitor_info,
            "brand_tone": brand_tone,
            "temperature": temperature,
        }
        if category:
            payload["category"] = category.strip().lower()
        if external_id:
            payload["external_id"] = external_id
        if asin:
            payload["asin"] = asin
        if listing_id:
            payload["listing_id"] = listing_id
        if sku:
            payload["sku"] = sku
        if user_id:
            payload["user_id"] = str(user_id).strip()

        if user_id:
            payload["user_id"] = str(user_id).strip()
        if strict_validation:
            payload["strict_validation"] = True

        run = None
        try:
            run = self.harness.run("listing", payload)
            self.last_run_id = run.run_id
            content = run.content
            data, validation_dict = resolve_listing_validation(
                self.platform,
                content,
                harness_validation=run.validation,
            )

            if strict_validation and not validation_dict.get("ok", True):
                raise TokenApiError(
                    "Listing validation failed: "
                    + "; ".join(validation_dict.get("errors") or [])
                )

            return self._parse_listing_response(
                data, keywords, run.model_used, run.total_tokens, validation_dict
            )

        except json.JSONDecodeError as e:
            raise TokenApiError(
                f"Failed to parse LLM response as JSON: {e}\nRaw: {run.content[:500] if run else 'N/A'}"
            )
        except TokenApiError:
            raise
        except Exception as e:
            raise TokenApiError(f"Listing generation failed: {e}")

    def batch_generate(
        self,
        products: List[Dict[str, Any]],
        **kwargs,
    ) -> List[Optional[ListingResult]]:
        import time

        results: List[Optional[ListingResult]] = []
        for i, prod in enumerate(products):
            print(f"[{i+1}/{len(products)}] Generating for: {prod.get('product', 'Unknown')}")
            try:
                result = self.generate(**prod, **kwargs)
                results.append(result)
                if i < len(products) - 1:
                    time.sleep(1)
            except Exception as e:
                print(f"Failed for {prod.get('product', 'Unknown')}: {e}")
                results.append(None)
        return results


def main():
    reg = get_catalog()
    parser = argparse.ArgumentParser(description="TokenApi E-commerce Listing Generator")
    parser.add_argument("--product", required=True, help="Product name")
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords")
    parser.add_argument(
        "--platform",
        default="amazon",
        choices=list(reg.scene_platform_ids(LISTING_SCENE)),
    )
    parser.add_argument("--lang", default="zh", choices=list(reg.locale_ids()))
    parser.add_argument("--features", help="Comma-separated product features")
    parser.add_argument("--audience", help="Target audience description")
    parser.add_argument(
        "--competitor",
        "--competitor-asin",
        dest="competitor",
        help="Competitor ASIN or public selling points for differentiation",
    )
    parser.add_argument("--tone", default="专业可信", help="Brand tone")
    parser.add_argument(
        "--category",
        choices=list(reg.category_ids()) or None,
        help="Product category (see harness/categories/_index.yaml)",
    )
    parser.add_argument("--external-id", help="Business external id for effect loop")
    parser.add_argument("--asin", help="Amazon ASIN (stored as external_id)")
    parser.add_argument("--listing-id", help="Internal listing id")
    parser.add_argument("--sku", help="SKU for effect loop tracking")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "amazon", "shopify", "tiktok"],
        help="Output format",
    )
    parser.add_argument("--strict-validation", action="store_true", help="Fail on validation errors")
    parser.add_argument("--api-key", default=os.getenv("TOKENAPI_KEY"))
    parser.add_argument("--base-url", default=os.getenv("TOKENAPI_BASE_URL"))
    args = parser.parse_args()

    if not args.api_key:
        print("Error: TOKENAPI_KEY not set. Use --api-key or env var.")
        sys.exit(1)

    generator = ListingGenerator(
        platform=args.platform,
        lang=args.lang,
        api_key=args.api_key,
        base_url=args.base_url,
    )

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    features = [f.strip() for f in args.features.split(",")] if args.features else None

    print(f"Generating {args.platform.upper()} listing for: {args.product}")
    print(f"Keywords: {keywords}")

    formatters = {
        "json": lambda r: r.to_json(),
        "amazon": lambda r: r.to_amazon_format(),
        "shopify": lambda r: r.to_shopify_format(),
        "tiktok": lambda r: r.to_tiktok_format(),
    }

    try:
        result = generator.generate(
            product=args.product,
            keywords=keywords,
            features=features,
            target_audience=args.audience,
            competitor_info=args.competitor,
            brand_tone=args.tone,
            category=args.category,
            external_id=args.external_id,
            asin=args.asin,
            listing_id=args.listing_id,
            sku=args.sku,
            strict_validation=args.strict_validation,
        )

        if result.validation and result.validation.get("warnings"):
            print("Validation warnings:", "; ".join(result.validation["warnings"]), file=sys.stderr)

        output = formatters[args.format](result)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"\nSaved to: {args.output}")
        else:
            print("\n" + "=" * 50)
            print(output)

        print(f"\nTokens used: {result.tokens_used}")
        print(f"Model: {result.model_used}")
        if generator.last_run_id:
            print(f"Harness run_id: {generator.last_run_id}  (效果闭环: scripts/harness-effect-loop.py record --run-id ...)")

    except TokenApiError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
