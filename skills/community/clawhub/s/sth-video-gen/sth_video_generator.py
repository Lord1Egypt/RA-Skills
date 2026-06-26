#!/usr/bin/env python3
"""
STH Video Template Generator

Generates videos for Sing The Hook song templates using a two-stage pipeline:
1. seedance1.5pro for original video
2. infinitetalk for final video with audio
"""

import csv
import json
import subprocess
import sys
import time
import os
from typing import Optional, Dict, Any, List, Tuple

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'dev_mobile',
    'user': 'openclaw',
    'password': ''
}

# MCP configuration
MCP_CONFIG = {
    'endpoint': 'https://kansas3.8glabs.com/mcp',
    'api_key': ''
}

# Notification configuration
NOTIFY_CONFIG = {
    'enabled': True,
    'channel': 'telegram',
    'target': ''  # User's Telegram ID
}

def send_notification(message: str):
    """Send a notification message via OpenClaw message tool."""
    if not NOTIFY_CONFIG['enabled']:
        return
    
    try:
        # Write notification to a file that OpenClaw can pick up
        script_dir = os.path.dirname(os.path.abspath(__file__))
        notify_file = os.path.join(script_dir, 'pending_notifications.txt')
        
        with open(notify_file, 'a') as f:
            f.write(f"{message}\n")
        
        print(f"    [Notification queued]")
    except Exception as e:
        print(f"    [Notification failed: {e}]")

def run_psql(query: str) -> Optional[str]:
    """Execute a PostgreSQL query and return the result."""
    cmd = [
        'psql',
        '-h', DB_CONFIG['host'],
        '-p', DB_CONFIG['port'],
        '-U', DB_CONFIG['user'],
        '-d', DB_CONFIG['dbname'],
        '-t',  # Tuples only
        '-A',  # Unaligned
        '-c', query
    ]
    
    env = {'PGPASSWORD': DB_CONFIG['password']}
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"PSQL Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"PSQL Exception: {e}")
        return None

def get_template_data(template_id: str) -> Optional[Dict[str, str]]:
    """Fetch template data from song_templates table."""
    query = f"SELECT image_url, generate_video_prompt, song_type_id FROM song_templates WHERE id = '{template_id}';"
    result = run_psql(query)
    
    if result:
        parts = result.split('|')
        if len(parts) >= 3:
            return {
                'image_url': parts[0],
                'generate_video_prompt': parts[1],
                'song_type_id': parts[2]
            }
    return None

def get_audio_mix_url(song_type_id: str) -> Optional[str]:
    """Fetch audio mix URL from song_types table."""
    query = f"SELECT amix_url FROM song_types WHERE id = '{song_type_id}';"
    result = run_psql(query)
    return result if result else None

def call_mcp_create_video(prompt: str, model: str, 
                          image_url: str = "", video_url: str = "",
                          audio_url: str = "", duration: str = "", 
                          aspect_ratio: str = "") -> Optional[str]:
    """Call MCP create-video tool and return the video URL (handles async jobs)."""
    # MCP uses tools/call method with tool name in arguments
    arguments = {
        "prompt": prompt,
        "model": model
    }
    
    if image_url:
        arguments["imageUrl"] = image_url
    if video_url:
        arguments["videoUrl"] = video_url
    if audio_url:
        arguments["audioUrl"] = audio_url
    if duration:
        arguments["duration"] = duration
    if aspect_ratio:
        arguments["aspectRatio"] = aspect_ratio
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "create-video",
            "arguments": arguments
        }
    }
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        '-H', f'X-API-Key: {MCP_CONFIG["api_key"]}',
        '-H', 'Content-Type: application/json',
        '-H', 'Accept: application/json, text/event-stream',
        '-d', json.dumps(payload),
        MCP_CONFIG['endpoint']
    ]
    
    print(f"    Request: {json.dumps(payload)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        print(f"    Response: {result.stdout}")
        response = json.loads(result.stdout)
        
        if 'result' in response:
            result_data = response['result']
            job_id = None
            
            # Extract job_id from structuredContent or content
            if isinstance(result_data, dict):
                if 'structuredContent' in result_data:
                    sc = result_data['structuredContent']
                    if isinstance(sc, dict) and 'data' in sc:
                        data = sc['data']
                        if isinstance(data, dict) and 'job_id' in data:
                            job_id = data['job_id']
                        elif isinstance(data, dict) and 'url' in data:
                            return data['url']  # Direct URL response
                elif 'content' in result_data:
                    content = result_data['content']
                    if isinstance(content, list) and len(content) > 0:
                        item = content[0]
                        if isinstance(item, dict) and 'text' in item:
                            try:
                                parsed = json.loads(item['text'])
                                if 'data' in parsed and isinstance(parsed['data'], dict):
                                    if 'job_id' in parsed['data']:
                                        job_id = parsed['data']['job_id']
                                    elif 'url' in parsed['data']:
                                        return parsed['data']['url']
                            except:
                                pass
            
            # If we got a job_id, poll for completion
            if job_id:
                print(f"    Job ID: {job_id}, polling for completion...")
                return poll_video_job(job_id, model)
            
        print(f"MCP Error: {response}")
        return None
    except Exception as e:
        print(f"MCP Exception: {e}")
        return None

def poll_video_job(job_id: str, job_type: str, max_attempts: int = 500, poll_interval: int = 5) -> Optional[str]:
    """Poll fetch-asset endpoint until video is ready.
    
    Default: 500 attempts × 5 seconds = ~42 minutes max wait time.
    """
    # Determine the type based on model
    type_map = {
        'seedance1.5pro': 'create-video',
        'infinitetalk': 'create-video',
        'seedance': 'create-video',
        'keling2.1': 'create-video',
        'wanx2.2': 'create-video'
    }
    asset_type = type_map.get(job_type, 'create-video')
    
    for attempt in range(max_attempts):
        time.sleep(poll_interval)
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch-asset",
                "arguments": {
                    "id": job_id,
                    "type": asset_type
                }
            }
        }
        
        cmd = [
            'curl', '-s', '-X', 'POST',
            '-H', f'X-API-Key: {MCP_CONFIG["api_key"]}',
            '-H', 'Content-Type: application/json',
            '-H', 'Accept: application/json, text/event-stream',
            '-d', json.dumps(payload),
            MCP_CONFIG['endpoint']
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            response = json.loads(result.stdout)
            
            if 'result' in response:
                result_data = response['result']
                status = None
                video_url = None
                
                # Parse response
                if isinstance(result_data, dict):
                    if 'structuredContent' in result_data:
                        sc = result_data['structuredContent']
                        if isinstance(sc, dict):
                            status = sc.get('status')
                            if 'data' in sc and isinstance(sc['data'], dict):
                                video_url = sc['data'].get('url') or sc['data'].get('videoUrl')
                    elif 'content' in result_data:
                        content = result_data['content']
                        if isinstance(content, list) and len(content) > 0:
                            item = content[0]
                            if isinstance(item, dict) and 'text' in item:
                                try:
                                    parsed = json.loads(item['text'])
                                    status = parsed.get('status')
                                    if 'data' in parsed and isinstance(parsed['data'], dict):
                                        video_url = parsed['data'].get('url') or parsed['data'].get('videoUrl')
                                except:
                                    pass
                
                print(f"    Attempt {attempt + 1}/{max_attempts}: status={status}")
                
                if status == 'success' and video_url:
                    return video_url
                elif status == 'failed':
                    print(f"    Job failed")
                    return None
                    
        except Exception as e:
            print(f"    Poll error: {e}")
            continue
    
    print(f"    Timeout waiting for job completion")
    return None

def get_audio_duration(audio_url: str, download: bool = False) -> Tuple[float, Optional[str]]:
    """Get audio duration in seconds using ffprobe.
    
    Args:
        audio_url: URL of the audio file
        download: If True, download and save the audio file, return temp path
    
    Returns:
        Tuple of (duration_seconds, temp_file_path or None)
    """
    import tempfile
    import subprocess
    
    temp_path = None
    
    try:
        # Download audio file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name
        
        download_cmd = ['curl', '-s', '-L', '-o', temp_path, audio_url]
        subprocess.run(download_cmd, timeout=60, check=True)
        
        # Probe duration
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            temp_path
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            print(f"    Audio duration: {duration:.2f} seconds")
            if download:
                return duration, temp_path
            else:
                return duration, None
        else:
            print(f"    ffprobe error: {result.stderr}")
            if not download and os.path.exists(temp_path):
                os.unlink(temp_path)
            return 12.0, None
    except Exception as e:
        print(f"    Duration probe error: {e}")
        if not download and temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        return 12.0, None

def trim_video(video_url: str, duration: float, template_id: str) -> Optional[str]:
    """Trim video to specified duration using ffmpeg and upload to GCS. Returns new GCS URL or None."""
    import tempfile
    import subprocess
    import os
    import uuid
    from google.cloud import storage
    
    print(f"    Trimming video to {duration:.2f} seconds...")
    
    # Download video to temp file
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        temp_in = f.name
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        temp_out = f.name
    
    try:
        # Download video
        print(f"    Downloading video for trimming...")
        download_cmd = ['curl', '-s', '-L', '-o', temp_in, video_url]
        subprocess.run(download_cmd, timeout=120, check=True)
        
        # Trim video (trim from start to duration, re-encode for compatibility)
        trim_cmd = [
            'ffmpeg', '-y',
            '-i', temp_in,
            '-t', str(duration),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-shortest',
            temp_out
        ]
        result = subprocess.run(trim_cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"    ffmpeg error: {result.stderr[:200]}")
            return None
        
        print(f"    Video trimmed successfully to {duration:.2f}s")
        
        # Generate unique filename for GCS
        unique_id = str(uuid.uuid4())[:8]
        gcs_filename = f"trimmed/{template_id}_{unique_id}.mp4"
        
        # Upload to GCS using Python client
        print(f"    Uploading to GCS: {gcs_filename}...")
        
        # Get script directory for service account key
        script_dir = os.path.dirname(os.path.abspath(__file__))
        service_account_path = os.getenv("STH_GCS_KEY_PATH", "")
        
        # Initialize GCS client
        client = storage.Client.from_service_account_json(service_account_path)
        bucket = client.get_bucket("claw-data")
        
        # Upload with large chunk size for video files
        blob = bucket.blob(gcs_filename, chunk_size=512 * 1024 * 1024)
        blob.upload_from_filename(temp_out)
        
        # Get public URL
        gcs_url = blob.public_url
        print(f"    ✓ Uploaded to GCS successfully: {gcs_url}")
        
        return gcs_url
        
    except Exception as e:
        print(f"    Trim/upload error: {e}")
        return None
    finally:
        if os.path.exists(temp_in):
            os.unlink(temp_in)
        if os.path.exists(temp_out):
            os.unlink(temp_out)

def update_template_urls(template_id: str, video_url: str) -> bool:
    """Update the song_templates table with video URLs."""
    query = f"""UPDATE song_templates 
                SET video_url = '{video_url}', 
                    video_url_seedream_v4 = '{video_url}'
                WHERE id = '{template_id}';"""
    result = run_psql(query)
    return result is not None

def update_csv_status(csv_file: str, template_id: str, status: str):
    """Update the status column in the CSV file."""
    try:
        # Read all rows
        rows = []
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get('Song Template ID', '').strip() == template_id:
                    row['Status'] = status
                rows.append(row)
        
        # Write back
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✓ CSV status updated to: {status}")
    except Exception as e:
        print(f"  ⚠ Could not update CSV: {e}")

def process_template(template_id: str) -> Tuple[bool, str]:
    """
    Process a single template through the full pipeline.
    Returns (success, final_status)
    """
    print(f"\n{'='*60}", flush=True)
    print(f"🎬 PROCESSING: {template_id}", flush=True)
    print(f"{'='*60}", flush=True)
    
    # Step 1: Get template data
    template_data = get_template_data(template_id)
    if not template_data:
        print(f"  ✗ Failed to fetch template data", flush=True)
        return False, "Failed"
    
    print(f"  ✅ Stage 1.1: Template data fetched", flush=True)
    print(f"      - Image URL: {template_data['image_url'][:50]}...", flush=True)
    print(f"      - Prompt: {template_data['generate_video_prompt'][:50]}...", flush=True)
    
    # Step 2: Get audio mix URL
    audio_url = get_audio_mix_url(template_data['song_type_id'])
    if not audio_url:
        print(f"  ✗ Failed to fetch audio mix URL", flush=True)
        return False, "Failed"
    
    print(f"  ✅ Stage 1.2: Audio mix URL fetched", flush=True)
    
    # Step 3 (NEW Stage 1.3): Download and check audio duration BEFORE video generation
    print(f"  → Stage 1.3: Checking audio duration...", flush=True)
    audio_duration, audio_temp_path = get_audio_duration(audio_url, download=True)
    
    # Decide which model to use based on audio duration
    if audio_duration > 12.0:
        # Use keling3 for longer audio (15s max for keling3)
        video_model = 'keling3'
        video_duration = '15'
        print(f"  ✅ Stage 1.3: Audio is {audio_duration:.2f}s (>12s), using keling3 for 15s video", flush=True)
    else:
        # Use seedance1.5pro for shorter audio (12s video)
        video_model = 'seedance1.5pro'
        video_duration = '12'
        print(f"  ✅ Stage 1.3: Audio is {audio_duration:.2f}s (≤12s), using seedance1.5pro for 12s video", flush=True)
    
    # Step 4 (Stage 2.1): Generate original video
    print(f"  → Stage 2.1: Generating original video ({video_model})...", flush=True)
    original_video_url = call_mcp_create_video(
        prompt=template_data['generate_video_prompt'],
        image_url=template_data['image_url'],
        model=video_model,
        duration=video_duration,
        aspect_ratio='9:16'
    )
    
    if not original_video_url:
        print(f"  ✗ Failed to generate original video", flush=True)
        return False, "Failed"
    
    print(f"  ✅ Stage 2.1: Original video generated", flush=True)
    print(f"      URL: {original_video_url[:60]}...", flush=True)
    
    # Step 5 (Stage 2.2): Generate final video (infinitetalk)
    print(f"  → Stage 2.2: Generating final video (infinitetalk)...", flush=True)
    final_video_url = call_mcp_create_video(
        prompt=template_data['generate_video_prompt'],
        video_url=original_video_url,
        model='infinitetalk',
        audio_url=audio_url
    )
    
    if not final_video_url:
        print(f"  ✗ Failed to generate final video", flush=True)
        return False, "original video generated"
    
    print(f"  ✅ Stage 2.2: Final video generated", flush=True)
    print(f"      URL: {final_video_url[:60]}...", flush=True)
    
    # Step 6 (Stage 3): Trim video to match audio duration (max 15s/12s due to API limit)
    print(f"  → Stage 3: Trimming video to match audio duration...", flush=True)
    
    # Note: Generated video is always video_duration max (API limitation)
    # Trim only if audio is shorter than generated video duration
    req_duration = float(video_duration)
    if audio_duration < req_duration:
        print(f"  ℹ️  Audio is {audio_duration:.2f}s (<{req_duration}s). Trimming video to match...", flush=True)
        trimmed_url = trim_video(final_video_url, audio_duration, template_id)
        if trimmed_url and trimmed_url != final_video_url:
            final_video_url = trimmed_url
            print(f"  ✅ Stage 3: Video trimmed to {audio_duration:.2f}s and uploaded to GCS", flush=True)
            print(f"      URL: {final_video_url[:60]}...", flush=True)
        elif trimmed_url:
            print(f"  ✅ Stage 3: Video trimmed to {audio_duration:.2f}s", flush=True)
        else:
            print(f"  ⚠️  Trimming failed, using original video", flush=True)
    else:
        print(f"  ℹ️  Audio is {audio_duration:.2f}s (≥{req_duration}s). Keeping video as-is.", flush=True)
    
    # Clean up temp audio file if it exists
    if audio_temp_path and os.path.exists(audio_temp_path):
        os.unlink(audio_temp_path)
    
    # Step 7 (Stage 4): Update database with final video URL
    print(f"  → Stage 4: Updating database...", flush=True)
    if update_template_urls(template_id, final_video_url):
        print(f"  ✅ Stage 4: Database updated successfully", flush=True)
        return True, "Success"
    else:
        print(f"  ✗ Failed to update database", flush=True)
        return False, "final video generated"

def main():
    if len(sys.argv) < 2:
        print("Usage: python sth_video_generator.py <csv_file>", flush=True)
        print("CSV should have columns: 'Song Template ID', 'Status'", flush=True)
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Read CSV file
    template_ids = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Support both "Song Template ID" and "Template ID" column names
                template_id = row.get('Song Template ID', row.get('Template ID', '')).strip()
                if template_id:
                    template_ids.append(template_id)
    except Exception as e:
        print(f"Error reading CSV: {e}", flush=True)
        sys.exit(1)
    
    if not template_ids:
        print("No template IDs found in CSV", flush=True)
        sys.exit(1)
    
    print(f"Found {len(template_ids)} templates to process", flush=True)
    
    # Process each template
    results = {
        'success': 0,
        'partial': 0,
        'failed': 0
    }
    
    for template_id in template_ids:
        success, status = process_template(template_id)
        
        if status == "Success":
            results['success'] += 1
            update_csv_status(csv_file, template_id, "TRUE")
        elif status == "original video generated":
            results['partial'] += 1
            update_csv_status(csv_file, template_id, "FALSE")
            print(f"\n  NOTE: Original video exists but DB update skipped")
        else:
            results['failed'] += 1
            update_csv_status(csv_file, template_id, "FALSE")
    
    # Summary
    print(f"\n{'='*60}", flush=True)
    print(f"📊 SUMMARY", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"Total processed: {len(template_ids)}", flush=True)
    print(f"  ✅ Success (DB + CSV updated): {results['success']}", flush=True)
    print(f"  ~ Partial (original video only): {results['partial']}", flush=True)
    print(f"  ✗ Failed: {results['failed']}", flush=True)
    print(f"{'='*60}", flush=True)

if __name__ == '__main__':
    main()
