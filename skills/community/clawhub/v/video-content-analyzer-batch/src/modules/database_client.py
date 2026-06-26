# Supabase database module
import os
from typing import Dict, List, Optional
from supabase import create_client, Client
from dataclasses import asdict

class DatabaseClient:
    def __init__(self, url: str = None, service_key: str = None):
        self.supabase_url = url or os.getenv("SUPABASE_URL")
        self.service_key = service_key or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.supabase_url or not self.service_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables must be set")
        
        self.client: Client = create_client(self.supabase_url, self.service_key)
    
    def save_video_asset(self, user_id: str, filename: str, storage_path: str, duration: float, file_size: int) -> str:
        """Save video asset record to database"""
        data = {
            "user_id": user_id,
            "original_filename": filename,
            "storage_path": storage_path,
            "duration_seconds": duration,
            "file_size_bytes": file_size,
            "status": "processing"
        }
        
        response = self.client.table("video_assets").insert(data).execute()
        return response.data[0]["id"]
    
    def update_video_status(self, video_id: str, status: str) -> None:
        """Update video processing status"""
        self.client.table("video_assets").update({"status": status}).eq("id", video_id).execute()
    
    def save_frame(self, video_id: str, frame_number: int, timestamp: float, storage_path: str, width: int, height: int, ocr_text: str = None, content_tags: List[str] = None) -> str:
        """Save extracted frame record to database"""
        data = {
            "video_id": video_id,
            "frame_number": frame_number,
            "timestamp_seconds": timestamp,
            "storage_path": storage_path,
            "width": width,
            "height": height,
            "ocr_text": ocr_text,
            "content_tags": content_tags or []
        }
        
        response = self.client.table("video_frames").insert(data).execute()
        return response.data[0]["id"]
    
    def save_search_results(self, frame_id: str, query: str, results: List) -> None:
        """Save search results for a frame"""
        records = []
        for result in results:
            records.append({
                "frame_id": frame_id,
                "query": query,
                "search_engine": "google_custom_search",
                "result_url": result.url,
                "title": result.title,
                "snippet": result.snippet,
                "relevance_score": result.relevance_score
            })
        
        if records:
            self.client.table("search_results").insert(records).execute()
    
    def save_wiki_page(self, user_id: str, title: str, content: str, video_id: str, frame_ids: List[str]) -> str:
        """Save generated wiki page record"""
        data = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "source_video_id": video_id,
            "source_frame_ids": frame_ids
        }
        
        response = self.client.table("wiki_pages").insert(data).execute()
        return response.data[0]["id"]

    # ---- Batch job operations ----

    def create_batch_job(self, user_id: str, input_directory: str, feishu_space_id: str,
                         total_videos: int, category_mapping: Dict = None) -> str:
        data = {
            "user_id": user_id,
            "input_directory": input_directory,
            "feishu_space_id": feishu_space_id,
            "total_videos": total_videos,
            "category_mapping": category_mapping or {},
        }
        response = self.client.table("batch_jobs").insert(data).execute()
        return response.data[0]["id"]

    def update_batch_job(self, batch_id: str, **fields) -> None:
        self.client.table("batch_jobs").update(fields).eq("id", batch_id).execute()

    def update_video_wiki_url(self, video_id: str, wiki_url: str) -> None:
        self.client.table("video_assets").update({"wiki_url": wiki_url}).eq("id", video_id).execute()