"""
Social Media Daily Publisher for OpenClaw
PayLessTax & LevelUpLove - NewsAPI + Templated.io + UploadPost
"""

import json
import os
import random
import time
import argparse
from datetime import datetime
import requests

class NewsAPIScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"

    def fetch_tax_news(self):
        """Fetch SA tax/financial news"""
        params = {
            "q": "South Africa tax OR SARS OR VAT",
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": self.api_key
        }
        try:
            r = requests.get(f"{self.base_url}/everything", params=params, timeout=30)
            data = r.json()
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                return [a for a in articles if "South Africa" in a.get("title", "")][:5]
        except Exception as e:
            print(f"News fetch error: {e}")
        return []

    def fetch_relationship_news(self):
        """Fetch relationship/dating news"""
        params = {
            "q": "dating advice OR relationship tips OR love",
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": self.api_key
        }
        try:
            r = requests.get(f"{self.base_url}/everything", params=params, timeout=30)
            data = r.json()
            if data.get("status") == "ok":
                return data.get("articles", [])[:5]
        except Exception as e:
            print(f"News fetch error: {e}")
        return []

class SocialMediaPublisher:
    def __init__(self, brand, news_api_key, uploadpost_cfg, templated_cfg, oneliner_pool):
        self.brand = brand
        self.news_scraper = NewsAPIScraper(news_api_key)
        self.upload_cfg = uploadpost_cfg
        self.tpl_cfg = templated_cfg
        self.oneliners = oneliner_pool

    def fetch_news(self):
        """Get fresh content"""
        if self.brand == "paylesstax":
            articles = self.news_scraper.fetch_tax_news()
        else:
            articles = self.news_scraper.fetch_relationship_news()
        return articles[0] if articles else None

    def get_oneliner(self):
        """Get random one-liner"""
        return random.choice(self.oneliners) if self.oneliners else "Check out our latest updates!"

    def render_image(self, text):
        """Generate image via Templated.io"""
        tpl_info = self.tpl_cfg.get('templates', {}).get(self.brand, {})
        tpl_id = tpl_info.get('template_id')

        if not tpl_id:
            print("No template configured")
            return None

        headers = {
            "Authorization": f"Bearer {self.tpl_cfg.get('api_key')}",
            "Content-Type": "application/json"
        }
        data = {
            "template": tpl_id,
            "layers": {"text": {"text": text[:150]}},
            "file_type": "png"
        }

        try:
            r = requests.post(
                self.tpl_cfg.get('endpoint', 'https://api.templated.io/v1/render'),
                headers=headers, json=data, timeout=60
            )
            if r.status_code == 200:
                url = r.json().get('render_url')
                if url:
                    img = requests.get(url, timeout=30)
                    if img.status_code == 200:
                        return {"url": url, "data": img.content}
        except Exception as e:
            print(f"Image render error: {e}")
        return None

    def publish_post(self, image_data, caption):
        """Publish via UploadPost API"""
        headers = {"Authorization": f"Bearer {self.upload_cfg.get('api_key')}"}
        files = {"photos": ("post.png", image_data, "image/png")}
        data = {"caption": caption}

        try:
            r = requests.post(
                self.upload_cfg.get('endpoint', 'https://api.upload-post.com/api/upload_photos'),
                headers=headers, files=files, data=data, timeout=60
            )
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def run(self, content_type="news"):
        """Main execution"""
        result = {
            "brand": self.brand,
            "content_type": content_type,
            "timestamp": datetime.now().isoformat(),
            "status": "failed"
        }

        if content_type == "news":
            article = self.fetch_news()
            if not article:
                # Fallback to oneliner
                content_type = "oneliner"
                text = self.get_oneliner()
                result["fallback"] = "No news available"
            else:
                text = article.get("title", "Check out our updates!")
                result["headline"] = text
                result["source"] = article.get("source", {}).get("name", "News")
        else:
            text = self.get_oneliner()
            result["oneliner"] = text

        # Generate image
        image = self.render_image(text)
        if not image:
            result["error"] = "Image generation failed"
            return result

        result["image_url"] = image.get("url")

        # Publish
        caption = f"{text}\n\n#{'PayLessTax' if self.brand == 'paylesstax' else 'LevelUpLove'}"
        post_result = self.publish_post(image.get("data"), caption)
        result["post_result"] = post_result
        result["status"] = "published" if "error" not in post_result else "partial"

        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--brand', choices=['paylesstax', 'leveluplove'], required=True)
    parser.add_argument('--news-api-key', required=True)
    parser.add_argument('--uploadpost-config', required=True, help='Path to uploadpost.json')
    parser.add_argument('--templated-config', required=True, help='Path to templated_io.json')
    parser.add_argument('--oneliners', required=True, help='Path to oneliners JSON')
    parser.add_argument('--content-type', choices=['news', 'oneliner'], default='news')
    parser.add_argument('--output', default='post_result.json')

    args = parser.parse_args()

    # Load configs
    with open(args.uploadpost_config, 'r') as f:
        upload_cfg = json.load(f)
    with open(args.templated_config, 'r') as f:
        templated_cfg = json.load(f)
    with open(args.oneliners, 'r') as f:
        oneliners = json.load(f)

    publisher = SocialMediaPublisher(
        args.brand, args.news_api_key, upload_cfg, templated_cfg, oneliners
    )

    result = publisher.run(args.content_type)

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
