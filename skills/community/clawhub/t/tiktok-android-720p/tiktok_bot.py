#!/usr/bin/env python3
"""
TikTok Android Bot - Main Script

Two modes of operation:

1. SEARCH MODE - Search specific topics and comment on related videos
   python3 tiktok_bot.py search --topics fitness,gaming --videos 5

2. EXPLORE MODE - Scroll through For You feed and comment on random videos
   python3 tiktok_bot.py explore --videos 10

Usage Examples:
  # Search for fitness videos and comment on 5 of them
  python3 tiktok_bot.py search --topics fitness --videos 5
  
  # Search multiple topics, 3 videos each
  python3 tiktok_bot.py search --topics "fitness,cooking,travel" --videos 3
  
  # Explore For You feed, comment on 10 random videos
  python3 tiktok_bot.py explore --videos 10
  
  # Use specific device (optional)
  python3 tiktok_bot.py search --topics gaming --device 001431538002547
"""

import sys
import os
import subprocess
import time
import random
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.bot.android.tiktok_android_bot import TikTokAndroidBot
from src.bot.android.tiktok_navigation import TikTokNavigation

# Check if config exists
if not os.path.exists("config.py"):
    print("\n" + "="*60)
    print("⚠️  Configuration not found!")
    print("="*60)
    print("\nThis is your first time running the bot.")
    print("Let's set it up!\n")
    
    response = input("Run interactive setup now? [Y/n]: ").strip().lower()
    if response in ['', 'y', 'yes']:
        print("\nStarting setup wizard...\n")
        os.system("python3 setup.py")
        if not os.path.exists("config.py"):
            print("\n❌ Setup was not completed. Exiting.")
            sys.exit(1)
        print("\n✅ Setup complete! Starting bot...\n")
    else:
        print("\n❌ Cannot run without configuration.")
        print("   Run: python3 setup.py")
        sys.exit(1)

# Import config
try:
    from config import TOPICS, COMMENT_STYLE
    
    # Import based on comment style
    if COMMENT_STYLE == "static":
        from config import COMMENTS_BY_TOPIC, GENERIC_COMMENTS
    else:  # AI mode
        from config import AI_PROVIDER, AI_MODEL, AI_COMMENT_PROMPT, GENERIC_COMMENTS
        from src.ai_comments import generate_ai_comment
        
except ImportError as e:
    print(f"❌ Error loading config: {e}")
    print("   Run: python3 setup.py")
    sys.exit(1)


def get_device_id(specified_device=None):
    """Get device ID from argument, environment, or auto-detect."""
    if specified_device:
        return specified_device
    
    device_id = os.environ.get("ANDROID_DEVICE_ID")
    if device_id:
        return device_id
    
    # Auto-detect first connected device
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices = [line.split()[0] for line in result.stdout.split("\n")[1:] 
               if line.strip() and "device" in line]
    
    if not devices:
        print("❌ No Android device found!")
        print("   1. Connect device via USB")
        print("   2. Enable USB debugging")
        print("   3. Authorize computer on device")
        sys.exit(1)
    
    return devices[0]


def get_comment_static(topic, used_comments):
    """Get a static comment from templates."""
    if topic not in COMMENTS_BY_TOPIC:
        # Fall back to generic comments
        available = [c for c in GENERIC_COMMENTS if c not in used_comments]
    else:
        available = [c for c in COMMENTS_BY_TOPIC[topic] if c not in used_comments]
    
    if not available:
        # All used, reset
        used_comments.clear()
        available = COMMENTS_BY_TOPIC.get(topic, GENERIC_COMMENTS)
    
    comment = random.choice(available)
    used_comments.add(comment)
    return comment


def get_comment_ai(screenshot_path, topic):
    """Generate comment using AI vision."""
    try:
        comment = generate_ai_comment(
            screenshot_path=screenshot_path,
            topic=topic,
            provider=AI_PROVIDER,
            model=AI_MODEL,
            prompt_template=AI_COMMENT_PROMPT
        )
        
        if comment:
            return comment
        else:
            # Fall back to generic
            return random.choice(GENERIC_COMMENTS)
    except Exception as e:
        print(f"    ⚠️  AI failed, using fallback: {e}")
        return random.choice(GENERIC_COMMENTS)


def get_comment(topic, screenshot_path=None, used_comments=None):
    """Get comment based on configured style."""
    if COMMENT_STYLE == "ai":
        if not screenshot_path:
            print("    ⚠️  No screenshot for AI, using fallback")
            return random.choice(GENERIC_COMMENTS)
        return get_comment_ai(screenshot_path, topic)
    else:  # static
        if used_comments is None:
            used_comments = set()
        return get_comment_static(topic, used_comments)


def search_mode(bot, nav, topics, videos_per_topic, device_id):
    """Search specific topics and comment on videos."""
    print("\n" + "="*60)
    print("🔍 SEARCH MODE")
    print("="*60)
    print(f"Topics: {', '.join(topics)}")
    print(f"Videos per topic: {videos_per_topic}")
    print(f"Device: {device_id}")
    print("="*60)
    
    all_results = []
    
    for topic_idx, topic in enumerate(topics, 1):
        print(f"\n📍 TOPIC {topic_idx}/{len(topics)}: {topic.upper()}")
        print("-" * 60)
        
        used_comments = set()
        commented_videos = set()
        scroll_count = 0
        
        # Navigate and search
        bot.launch_tiktok()
        bot.wait_for_feed()
        nav.go_to_home()
        time.sleep(1)
        nav.tap_search_icon()
        nav.search_query(topic)
        
        # Engage with videos
        for video_num in range(1, videos_per_topic + 1):
            print(f"\n  📹 Video {video_num}/{videos_per_topic}")
            
            try:
                position = ((video_num - 1) % 4) + 1
                
                # Scroll if needed
                if video_num > 4 and (video_num - 1) % 4 == 0:
                    scroll_count += 1
                    print(f"    📜 Scrolling for more videos...")
                    bot.scroll_down()
                    time.sleep(2)
                
                video_id = f"s{scroll_count}_p{position}"
                
                if video_id in commented_videos:
                    print(f"    ⏭️  Already commented, skipping")
                    continue
                
                # Open video
                nav.tap_video_from_grid(position)
                time.sleep(2)
                
                # Generate comment (static only, no screenshot)
                comment = get_comment(topic, used_comments=used_comments)
                
                print(f"    💬 {comment}")
                
                success = bot.post_comment(comment)
                commented_videos.add(video_id)
                
                if success:
                    print(f"    ✅ Posted!")
                    all_results.append({
                        "topic": topic,
                        "video_num": video_num,
                        "comment": comment,
                        "success": True
                    })
                else:
                    print(f"    ❌ Failed")
                
                # Go back
                if video_num < videos_per_topic:
                    bot.go_back()
                    time.sleep(2)
                    
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        # Pause between topics
        if topic_idx < len(topics):
            print(f"\n⏸️  Pausing 10s before next topic...")
            time.sleep(10)
    
    return all_results


def explore_mode(bot, nav, num_videos, device_id):
    """Explore For You feed and comment on random videos."""
    print("\n" + "="*60)
    print("🌟 EXPLORE MODE (For You Feed)")
    print("="*60)
    print(f"Videos to engage: {num_videos}")
    print(f"Device: {device_id}")
    print("="*60)
    
    results = []
    used_comments = set()
    
    # Launch TikTok and go to For You feed
    bot.launch_tiktok()
    bot.wait_for_feed()
    nav.go_to_home()
    time.sleep(2)
    
    for video_num in range(1, num_videos + 1):
        print(f"\n📹 Video {video_num}/{num_videos}")
        
        try:
            # Take screenshot
            screenshot_path = f"data/explore_v{video_num}.png"
            bot.take_screenshot(screenshot_path)
            
            # Generate comment (AI or generic)
            if COMMENT_STYLE == "ai":
                print(f"  🤖 Analyzing video with AI...")
                comment = get_comment("general", screenshot_path=screenshot_path)
            else:
                comment = get_comment(None, used_comments=used_comments)
            
            print(f"  💬 {comment}")
            
            # Post comment
            success = bot.post_comment(comment)
            
            if success:
                print(f"  ✅ Posted!")
                results.append({
                    "video_num": video_num,
                    "comment": comment,
                    "success": True
                })
            else:
                print(f"  ❌ Failed")
            
            # Scroll to next video
            if video_num < num_videos:
                print(f"  ⏭️  Scrolling to next video...")
                bot.scroll_down()
                time.sleep(3)
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return results


def interact_mode(bot, nav, num_videos, do_like, do_favorite, do_comment, topics, device_id, like_rate, favorite_rate):
    """Interact with videos: like, favorite, and optionally comment.

    Args:
        bot: TikTokAndroidBot instance
        nav: TikTokNavigation instance
        num_videos: Number of videos to interact with
        do_like: Whether to like videos
        do_favorite: Whether to favorite videos
        do_comment: Whether to comment on videos
        topics: Topics for comment (if comment enabled)
        device_id: Device ID
        like_rate: Probability of liking (1-100)
        favorite_rate: Probability of favoriting (1-100)

    Returns:
        List of interaction results
    """
    print("\n" + "="*60)
    print("👍 INTERACT MODE")
    print("="*60)
    print(f"Videos to interact: {num_videos}")
    print(f"Like: {'Yes' if do_like else 'No'} (rate: {like_rate}%)")
    print(f"Favorite: {'Yes' if do_favorite else 'No'} (rate: {favorite_rate}%)")
    print(f"Comment: {'Yes' if do_comment else 'No'}")
    print(f"Device: {device_id}")
    print("="*60)

    results = []
    used_comments = set()
    liked_videos = set()
    favorited_videos = set()
    scroll_count = 0

    # Launch TikTok and go to For You feed
    bot.launch_tiktok()
    bot.wait_for_feed()
    nav.go_to_home()
    time.sleep(2)

    for video_num in range(1, num_videos + 1):
        print(f"\n📹 Video {video_num}/{num_videos}")

        video_id = f"v{video_num}"

        try:
            # Like video (with probability and duplicate check)
            if do_like:
                if video_id in liked_videos:
                    print(f"  ⏭️  Already liked, skipping")
                elif random.randint(1, 100) <= like_rate:
                    success = bot.like_video()
                    liked_videos.add(video_id)
                    if success:
                        print(f"  ❤️ Liked!")
                        results.append({"video_num": video_num, "action": "like", "success": True})
                    else:
                        print(f"  ❌ Like failed")
                        results.append({"video_num": video_num, "action": "like", "success": False})
                else:
                    print(f"  ⏭️  Skipped like (probability)")

            # Favorite video (with probability and duplicate check)
            if do_favorite:
                if video_id in favorited_videos:
                    print(f"  ⏭️  Already favorited, skipping")
                elif random.randint(1, 100) <= favorite_rate:
                    success = bot.favorite_video()
                    favorited_videos.add(video_id)
                    if success:
                        print(f"  ⭐ Favorited!")
                        results.append({"video_num": video_num, "action": "favorite", "success": True})
                    else:
                        print(f"  ❌ Favorite failed")
                        results.append({"video_num": video_num, "action": "favorite", "success": False})
                else:
                    print(f"  ⏭️  Skipped favorite (probability)")
            
            # Comment on video (if enabled)
            if do_comment:
                # Interact mode uses generic comments for For You feed
                # (topics are only relevant for search_mode)
                comment = get_comment("general", used_comments=used_comments)
                print(f"  💬 {comment}")
                
                success = bot.post_comment(comment)
                if success:
                    print(f"  ✅ Posted!")
                    results.append({"video_num": video_num, "action": "comment", "success": True, "comment": comment})
                else:
                    print(f"  ❌ Comment failed")
                    results.append({"video_num": video_num, "action": "comment", "success": False})
            
            # Scroll to next video
            if video_num < num_videos:
                print(f"  ⏭️  Scrolling to next video...")
                bot.scroll_down()
                time.sleep(3)
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return results


def publish_mode(bot, video_url, description, device_id):
    """Publish a video to TikTok from URL.

    Args:
        bot: TikTokAndroidBot instance
        video_url: URL or local path to video
        description: Video description
        device_id: Device ID

    Returns:
        List of publish results
    """
    print("\n" + "="*60)
    print("📹 PUBLISH MODE")
    print("="*60)
    print(f"Video URL: {video_url}")
    print(f"Description: {description[:50]}..." if len(description) > 50 else f"Description: {description}")
    print(f"Device: {device_id}")
    print("="*60)

    results = []

    try:
        # Step 0: Clean up all videos in DCIM/Camera folder
        print(f"\n🧹 Cleaning up all videos in DCIM/Camera...")
        # Delete all video files except .thumbnails folder
        subprocess.run(
            ["adb", "-s", device_id, "shell", "rm -f /sdcard/DCIM/Camera/*.mp4"],
            capture_output=True,
            timeout=10
        )
        subprocess.run(
            ["adb", "-s", device_id, "shell", "rm -f /sdcard/DCIM/Camera/*.3gp"],
            capture_output=True,
            timeout=10
        )
        print(f"✅ All videos cleaned")

        # Step 1: Download video if URL, or push if local file
        if video_url.startswith("http://") or video_url.startswith("https://"):
            # Download video from URL
            print(f"\n📥 Downloading video from URL...")
            # Use unique timestamp filename for identification
            timestamp = int(time.time())
            device_video_path = f"/sdcard/DCIM/Camera/video_{timestamp}.mp4"

            # Use curl to download directly to device
            curl_result = subprocess.run(
                ["adb", "-s", device_id, "shell", f"curl -L -o {device_video_path} '{video_url}'"],
                capture_output=True,
                timeout=300  # 5 minutes for download
            )

            if curl_result.returncode != 0:
                print(f"❌ Failed to download video: {curl_result.stderr.decode()}")
                return [{"success": False, "error": "download_failed"}]

            print(f"✅ Video downloaded to {device_video_path}")
        else:
            # Video is local, push to device DCIM/Camera folder with unique name
            print(f"\n📤 Pushing video to device DCIM/Camera...")
            timestamp = int(time.time())
            device_video_path = f"/sdcard/DCIM/Camera/video_{timestamp}.mp4"

            push_result = subprocess.run(
                ["adb", "-s", device_id, "push", video_url, device_video_path],
                capture_output=True,
                timeout=120
            )

            if push_result.returncode != 0:
                print(f"❌ Failed to push video: {push_result.stderr.stderr.decode()}")
                return [{"success": False, "error": "push_failed"}]

            print(f"✅ Video pushed to {device_video_path}")

        # Step 2: Scan media files so TikTok can recognize the new video
        print(f"\n📷 Scanning media files...")
        subprocess.run(
            ["adb", "-s", device_id, "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{device_video_path}"],
            capture_output=True,
            timeout=30
        )
        time.sleep(3)  # Wait for scan to complete
        print(f"✅ Media scan completed")

        # Step 3: Publish video
        print(f"\n🚀 Publishing video...")
        bot.launch_tiktok()
        bot.wait_for_feed()
        success = bot.publish_video(device_video_path, description)

        if success:
            print(f"  ✅ Video published!")
            results.append({"success": True, "video": video_url})
        else:
            print(f"  ❌ Publish failed")
            results.append({"success": False, "video": video_url})

        # Step 4: Clean up published video
        print(f"\n🧹 Cleaning up published video...")
        subprocess.run(
            ["adb", "-s", device_id, "shell", f"rm -f {device_video_path}"],
            capture_output=True,
            timeout=10
        )
        print(f"✅ Published video cleaned")

    except Exception as e:
        print(f"  ❌ Error: {e}")
        results.append({"success": False, "error": str(e)})

    return results


def print_summary(results, mode):
    """Print session summary."""
    print("\n" + "="*60)
    print("📊 SESSION SUMMARY")
    print("="*60)
    
    success_count = len([r for r in results if r.get("success")])
    total = len(results)
    
    print(f"\nMode: {mode.upper()}")
    print(f"✅ Success: {success_count}/{total} videos")
    
    if mode == "search" and results:
        # Group by topic
        by_topic = {}
        for r in results:
            topic = r.get("topic", "unknown")
            if topic not in by_topic:
                by_topic[topic] = []
            by_topic[topic].append(r)
        
        print(f"\nBy topic:")
        for topic, items in by_topic.items():
            success = len([i for i in items if i.get("success")])
            print(f"  {topic}: {success}/{len(items)}")
    
    # Show sample comments for search/interact modes
    if mode in ["search", "interact"] and results:
        comments = [r for r in results if r.get("comment")]
        if comments:
            print("\nSample comments:")
            for r in comments[:5]:
                comment_text = r.get("comment", "")
                if comment_text:
                    print(f"  • {comment_text[:60]}...")
    
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="TikTok Android Bot - Automated commenting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Search mode (specific topics):
    %(prog)s search --topics fitness --videos 5
    %(prog)s search --topics "fitness,gaming,cooking" --videos 3
  
  Explore mode (For You feed):
    %(prog)s explore --videos 10
    %(prog)s explore --videos 5 --device 001431538002547
    
  Interact mode (like, favorite, comment):
    %(prog)s interact --videos 10 --like --favorite
    %(prog)s interact --videos 5 --like --favorite --comment --topics fitness
    
  Publish mode (publish video):
    %(prog)s publish --video /path/to/video.mp4 --description "My video #tiktok"
        """
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")
    
    # Search mode
    search_parser = subparsers.add_parser("search", help="Search topics and comment")
    search_parser.add_argument("--topics", required=True, 
                              help="Comma-separated topics to search (e.g., fitness,gaming)")
    search_parser.add_argument("--videos", type=int, default=5,
                              help="Videos per topic (default: 5)")
    search_parser.add_argument("--device", help="Device ID (optional, auto-detects if not specified)")
    
    # Explore mode
    explore_parser = subparsers.add_parser("explore", help="Explore For You feed")
    explore_parser.add_argument("--videos", type=int, default=10,
                               help="Number of videos to comment on (default: 10)")
    explore_parser.add_argument("--device", help="Device ID (optional, auto-detects if not specified)")
    
    # Interact mode (like, favorite, comment)
    interact_parser = subparsers.add_parser("interact", help="Interact with videos (like, favorite, comment)")
    interact_parser.add_argument("--videos", type=int, default=10,
                               help="Number of videos to interact with (default: 10)")
    interact_parser.add_argument("--like", action="store_true", default=True,
                               help="Like videos (default: True)")
    interact_parser.add_argument("--favorite", action="store_true", default=False,
                               help="Favorite videos (default: False)")
    interact_parser.add_argument("--comment", action="store_true", default=False,
                               help="Comment on videos (default: False)")
    interact_parser.add_argument("--topics",
                               help="Topics to search (for comment mode, e.g., fitness,gaming)")
    interact_parser.add_argument("--like-rate", type=int, default=100,
                               help="Like probability %% (default: 100, range: 1-100)")
    interact_parser.add_argument("--favorite-rate", type=int, default=100,
                               help="Favorite probability %% (default: 100, range: 1-100)")
    interact_parser.add_argument("--device", help="Device ID (optional, auto-detects if not specified)")
    
    # Publish mode
    publish_parser = subparsers.add_parser("publish", help="Publish video to TikTok")
    publish_parser.add_argument("--video", type=str, required=True,
                               help="Video URL or local path to video file")
    publish_parser.add_argument("--description", type=str, default="",
                               help="Video description/caption")
    publish_parser.add_argument("--device", help="Device ID (optional, auto-detects if not specified)")
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # Get device
    device_id = get_device_id(args.device)
    print(f"\n📱 Using device: {device_id}")
    
    # Initialize bot
    bot = TikTokAndroidBot(device_id=device_id)
    nav = TikTokNavigation(bot)
    
    # Run mode
    if args.mode == "search":
        topics = [t.strip() for t in args.topics.split(",")]
        results = search_mode(bot, nav, topics, args.videos, device_id)
    elif args.mode == "explore":
        results = explore_mode(bot, nav, args.videos, device_id)
    elif args.mode == "interact":
        results = interact_mode(bot, nav, args.videos, args.like, args.favorite, args.comment, args.topics, device_id, args.like_rate, args.favorite_rate)
    elif args.mode == "publish":
        results = publish_mode(bot, args.video, args.description, device_id)
    else:
        print(f"❌ Unknown mode: {args.mode}")
        sys.exit(1)
    
    # Print summary
    print_summary(results, args.mode)


if __name__ == "__main__":
    main()
