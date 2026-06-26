#!/usr/bin/env python3
"""
Video Content Analysis & Documentation Workflow
Integrates video frame extraction, web search, database storage, and wiki publishing
"""
import os
import uuid
from dotenv import load_dotenv
from modules.video_processor import VideoProcessor
from modules.search_client import SearchClient
from modules.database_client import DatabaseClient
from modules.feishu_wiki_client import FeishuWikiClient

# Load environment variables
load_dotenv()

class VideoAnalyzer:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.search_client = SearchClient()
        self.db_client = DatabaseClient()
        self.wiki_client = FeishuWikiClient()
        
        self.frames_output_dir = os.getenv("FRAMES_OUTPUT_DIR", "./extracted_frames")
        os.makedirs(self.frames_output_dir, exist_ok=True)
    
    def process_video(self, video_path: str, user_id: str, space_id: str) -> dict:
        """
        Full video processing workflow:
        1. Extract keyframes
        2. Store metadata in database
        3. Search for frame content information
        4. Generate wiki page with findings
        5. Publish to Feishu Wiki
        """
        video_filename = os.path.basename(video_path)
        file_size = os.path.getsize(video_path)
        
        # Step 1: Get video info and save to database
        video_info = self.video_processor.get_video_info(video_path)
        video_id = self.db_client.save_video_asset(
            user_id=user_id,
            filename=video_filename,
            storage_path=video_path,
            duration=video_info.duration_seconds,
            file_size=file_size
        )
        
        print(f"Created video record: {video_id}")
        
        # Step 2: Extract keyframes
        print(f"Extracting keyframes from {video_filename}...")
        frames = self.video_processor.extract_keyframes(video_path, interval_seconds=10)
        print(f"Extracted {len(frames)} frames")
        
        # Step 3: Process each frame
        processed_frames = []
        frame_ids = []
        
        for i, frame in enumerate(frames):
            print(f"Processing frame {i+1}/{len(frames)}...")
            
            # Save frame to storage
            frame_filename = f"{video_id}_frame_{frame.frame_number:06d}.jpg"
            frame_path = os.path.join(self.frames_output_dir, frame_filename)
            self.video_processor.save_frame(frame, frame_path)
            
            # Save frame record to database
            frame_id = self.db_client.save_frame(
                video_id=video_id,
                frame_number=frame.frame_number,
                timestamp=frame.timestamp_seconds,
                storage_path=frame_path,
                width=frame.width,
                height=frame.height,
                content_tags=[]  # Would be populated by OCR/vision model in production
            )
            frame_ids.append(frame_id)
            
            # Step 4: Search for related information (using mock query for demo)
            # In production, this would use OCR/vision model output as search query
            search_query = f"reference information for frame content"
            search_results = self.search_client.search_image_content(search_query, num_results=3)
            
            # Save search results
            self.db_client.save_search_results(frame_id, search_query, search_results)
            
            processed_frames.append({
                "frame_id": frame_id,
                "timestamp": frame.timestamp_seconds,
                "frame_path": frame_path,
                "content_tags": [],
                "search_results": [r.__dict__ for r in search_results]
            })
        
        # Step 5: Generate and publish wiki page
        print("Generating wiki page...")
        wiki_title = f"Video Analysis: {video_filename}"
        wiki_content = self.wiki_client.generate_page_content(video_filename, processed_frames)
        
        # Save wiki page record
        wiki_id = self.db_client.save_wiki_page(
            user_id=user_id,
            title=wiki_title,
            content=wiki_content,
            video_id=video_id,
            frame_ids=frame_ids
        )
        
        # Publish to Feishu Wiki
        print("Publishing to Feishu Wiki...")
        wiki_page = self.wiki_client.create_page(
            space_id=space_id,
            title=wiki_title,
            content=wiki_content
        )
        
        # Update video status to completed
        self.db_client.update_video_status(video_id, "processed")
        
        print(f"Processing complete! Wiki page: {wiki_page.get('node', {}).get('title')}")
        
        return {
            "video_id": video_id,
            "wiki_id": wiki_id,
            "feishu_wiki_url": wiki_page.get('node', {}).get('url'),
            "frames_processed": len(frames),
            "status": "completed"
        }

class BatchVideoAnalyzer:
    """Process all videos in a directory, store results in Supabase,
    and publish categorized reports to Feishu Wiki."""

    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}

    def __init__(self):
        self.analyzer = VideoAnalyzer()
        self.db_client = self.analyzer.db_client
        self.wiki_client = self.analyzer.wiki_client

    @staticmethod
    def _classify(filename: str, mapping: dict) -> str:
        """Determine category for a video file based on configurable mapping."""
        name_lower = filename.lower()
        for category, keywords in mapping.items():
            if any(kw in name_lower for kw in keywords):
                return category
        return "Uncategorized"

    def process_directory(self, directory: str, user_id: str, space_id: str,
                          category_mapping: dict = None, interval_seconds: int = 10) -> dict:
        category_mapping = category_mapping or {}

        # Discover videos
        video_files = sorted(
            f for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in self.VIDEO_EXTENSIONS
        )

        if not video_files:
            return {"status": "no_videos", "total": 0, "results": []}

        # Create batch job record
        batch_id = self.db_client.create_batch_job(
            user_id=user_id,
            input_directory=directory,
            feishu_space_id=space_id,
            total_videos=len(video_files),
            category_mapping=category_mapping,
        )
        self.db_client.update_batch_job(batch_id, status="running")

        results = []
        failed = 0

        for i, vf in enumerate(video_files, 1):
            video_path = os.path.join(directory, vf)
            category = self._classify(vf, category_mapping)
            print(f"\n[{i}/{len(video_files)}] Processing: {vf} → {category}")

            try:
                result = self.analyzer.process_video(video_path, user_id, space_id)
                result["category"] = category
                result["filename"] = vf
                results.append(result)

                # Update video record with wiki URL
                if result.get("feishu_wiki_url"):
                    self.db_client.update_video_wiki_url(result["video_id"], result["feishu_wiki_url"])

                self.db_client.update_batch_job(
                    batch_id,
                    processed_videos=i - failed,
                    results=results,
                )
            except Exception as e:
                failed += 1
                print(f"  ✗ Failed: {e}")
                results.append({"filename": vf, "category": category, "status": "failed", "error": str(e)})
                self.db_client.update_batch_job(
                    batch_id,
                    failed_videos=failed,
                    error_log=[f"{vf}: {str(e)}"],
                )

        # Build category → video summaries mapping
        category_map: dict[str, list] = {}
        for r in results:
            category_map.setdefault(r.get("category", "Uncategorized"), []).append(r)

        # Publish category pages on Feishu Wiki
        category_pages = {}
        for cat, videos in category_map.items():
            summaries = [
                {
                    "title": v.get("filename", "unknown"),
                    "wiki_url": v.get("feishu_wiki_url", ""),
                    "frames_processed": v.get("frames_processed", 0),
                }
                for v in videos if v.get("status") != "failed"
            ]
            if summaries:
                page = self.wiki_client.create_category_page(space_id, cat, summaries)
                category_pages[cat] = page

        # Finalize batch job
        status = "completed" if failed == 0 else ("partial" if failed < len(video_files) else "failed")
        self.db_client.update_batch_job(batch_id, status=status)

        return {
            "batch_id": batch_id,
            "status": status,
            "total": len(video_files),
            "processed": len(video_files) - failed,
            "failed": failed,
            "category_pages": {k: v.get("node", {}).get("url", "") for k, v in category_pages.items()},
            "results": results,
        }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Video Content Analysis Tool")
    sub = parser.add_subparsers(dest="command")

    # Single video command
    single = sub.add_parser("single", help="Process a single video")
    single.add_argument("video_path", help="Path to input video file")
    single.add_argument("--user-id", required=True, help="User ID (UUID)")
    single.add_argument("--space-id", required=True, help="Feishu Wiki space ID")

    # Batch command
    batch = sub.add_parser("batch", help="Batch process all videos in a directory")
    batch.add_argument("directory", help="Directory containing video files")
    batch.add_argument("--user-id", required=True, help="User ID (UUID)")
    batch.add_argument("--space-id", required=True, help="Feishu Wiki space ID")
    batch.add_argument("--categories", default=None,
                      help="JSON mapping of category → keyword list, e.g. '{"demo":["demo"],"tutorial":["tut"]}'")
    batch.add_argument("--interval", type=int, default=10, help="Keyframe interval in seconds")

    args = parser.parse_args()

    if args.command == "single":
        analyzer = VideoAnalyzer()
        result = analyzer.process_video(args.video_path, args.user_id, args.space_id)
        print("\nResult:", result)
    elif args.command == "batch":
        cat_mapping = json.loads(args.categories) if args.categories else {}
        batch_analyzer = BatchVideoAnalyzer()
        result = batch_analyzer.process_directory(
            args.directory, args.user_id, args.space_id,
            category_mapping=cat_mapping, interval_seconds=args.interval,
        )
        print(f"\nBatch result: {result['processed']}/{result['total']} processed, "
              f"{result['failed']} failed, status={result['status']}")
        if result.get("category_pages"):
            print("Category pages:")
            for cat, url in result["category_pages"].items():
                print(f"  {cat}: {url}")
    else:
        parser.print_help()