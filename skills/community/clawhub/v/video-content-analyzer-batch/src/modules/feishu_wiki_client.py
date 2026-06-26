# Feishu Wiki module - adapted from public source
import os
import requests
from typing import Dict, Optional

class FeishuWikiClient:
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        self._access_token = None
        
        if not self.app_id or not self.app_secret:
            raise ValueError("FEISHU_APP_ID and FEISHU_APP_SECRET environment variables must be set")
    
    def _get_access_token(self) -> str:
        """Get valid access token"""
        if self._access_token:
            return self._access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self._access_token = response.json()["tenant_access_token"]
            return self._access_token
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get Feishu access token: {str(e)}") from e
    
    def create_page(self, space_id: str, title: str, content: str, parent_node_token: str = None) -> Dict:
        """Create a new wiki page"""
        url = "https://open.feishu.cn/open-apis/wiki/v2/nodes"
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "space_id": space_id,
            "title": title,
            "content": content,
            "node_type": "wiki"
        }
        
        if parent_node_token:
            payload["parent_node_token"] = parent_node_token
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to create wiki page: {str(e)}") from e
    
    def generate_page_content(self, video_name: str, frames_data: list, category: str = None) -> str:
        """Generate wiki page content from processed video frames"""
        content = f"# Video Analysis: {video_name}\n\n"
        if category:
            content += f"**Category**: {category}\n\n"
        content += "## Summary\n\n"
        content += f"Processed {len(frames_data)} frames from the video. Below are key findings:\n\n"
        
        for i, frame_data in enumerate(frames_data, 1):
            content += f"### Frame {i} (Time: {frame_data['timestamp']:.2f}s)\n\n"
            if frame_data.get('content_tags'):
                content += f"**Content Tags**: {', '.join(frame_data['content_tags'])}\n\n"
            
            if frame_data.get('search_results'):
                content += "**Related References**:\n"
                for j, result in enumerate(frame_data['search_results'][:3], 1):
                    content += f"{j}. [{result['title']}]({result['url']})\n"
                    content += f"   {result['snippet'][:200]}...\n\n"
            
            content += "---\n\n"
        
        return content

    def create_category_page(self, space_id: str, category: str, video_summaries: list) -> Dict:
        """Create a parent wiki page for a category with links to individual video analyses"""
        content = f"# Category: {category}\n\n"
        content += f"{len(video_summaries)} video(s) in this category.\n\n"

        for vs in video_summaries:
            content += f"- [{vs['title']}]({vs.get('wiki_url', '#')}) — {vs.get('frames_processed', 0)} frames\n"

        return self.create_page(space_id=space_id, title=category, content=content)