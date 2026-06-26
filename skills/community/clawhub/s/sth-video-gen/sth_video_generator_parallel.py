#!/usr/bin/env python3
"""
STH Video Template Generator (Parallel Version) - Phase-Separated

Generates videos for Sing The Hook song templates using a two-phase pipeline:

PHASE 1 (Generate): 5 parallel workers
  - Stage 3: Generate original video (keling3/seedance1.5pro)
  - Stage 4: Generate final video with lip-sync (infinitetalk)
  - Save raw video URL to local JSON file (raw_video_urls.json)

PHASE 2 (Trim): 1 sequential worker
  - Stage 5: Download and trim video with ffmpeg
  - Stage 6: Upload to GCS and update video_url column in database

Usage:
  python sth_video_generator_parallel.py templates.csv --mode full        # Default: both phases
  python sth_video_generator_parallel.py templates.csv --mode generate     # Phase 1 only
  python sth_video_generator_parallel.py templates.csv --mode trim         # Phase 2 only
"""

import csv
import json
import subprocess
import sys
import time
import os
import uuid
import tempfile
import logging
import traceback
import argparse
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, Any, List, Tuple
from google.cloud import storage

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create log filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"video_generation_{timestamp}.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, f"errors_{timestamp}.log")

# Local state file for raw video URLs (Phase 1 output → Phase 2 input)
RAW_VIDEO_STATE_FILE = os.path.join(SCRIPT_DIR, "raw_video_urls.json")

# Configure logging - detailed format with thread info
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(threadName)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Separate error logger for quick access to failures
error_logger = logging.getLogger('errors')
error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S'))
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

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

# Parallel Configuration
MAX_WORKERS_GENERATE = 5  # Phase 1: API calls (network-bound)
MAX_WORKERS_TRIM = 3      # Phase 2: ffmpeg (CPU-bound, optimized for 8c8g server)

# Path to the stop signal file
STOP_SIGNAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stop_signal.txt")

# Thread-safe lock for raw video state file
state_lock = threading.Lock()

def check_stop_signal():
    """Returns True if the stop signal file exists."""
    return os.path.exists(STOP_SIGNAL_FILE)

def load_raw_video_state() -> Dict[str, str]:
    """Load raw video URL state from local JSON file."""
    if os.path.exists(RAW_VIDEO_STATE_FILE):
        try:
            with open(RAW_VIDEO_STATE_FILE, 'r') as f:
                data = json.load(f)
                logger.debug(f"Loaded {len(data)} raw video URLs from state file")
                return data
        except Exception as e:
            logger.warning(f"Could not load state file: {e}")
            return {}
    return {}

def save_raw_video_url(template_id: str, video_url: str):
    """Save raw video URL to local JSON file (thread-safe)."""
    with state_lock:
        data = load_raw_video_state()
        data[template_id] = video_url
        try:
            with open(RAW_VIDEO_STATE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved raw video URL for {template_id[:8]}... to state file")
        except Exception as e:
            logger.error(f"Failed to save state file: {e}")
            error_logger.error(f"State file save failed - template={template_id[:8]}... | error={str(e)}")

def get_raw_video_url_from_state(template_id: str) -> Optional[str]:
    """Get raw video URL from local state file."""
    data = load_raw_video_state()
    return data.get(template_id)

def run_psql(query: str, log_query: bool = False) -> Optional[str]:
    """Execute a PostgreSQL query and return the result."""
    cmd = [
        'psql',
        '-h', DB_CONFIG['host'],
        '-p', DB_CONFIG['port'],
        '-U', DB_CONFIG['user'],
        '-d', DB_CONFIG['dbname'],
        '-t',
        '-A',
        '-c', query
    ]
    
    env = {'PGPASSWORD': DB_CONFIG['password']}
    try:
        if log_query:
            logger.debug(f"   [DB Query] {query[:200]}...")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            output = result.stdout.strip()
            logger.debug(f"   [DB Result] {output[:100] if output else '(empty)'}")
            return output
        else:
            logger.warning(f"   [DB Error] Return code: {result.returncode} | stderr: {result.stderr[:200]}")
            return None
    except subprocess.TimeoutExpired:
        logger.error(f"   [DB Timeout] Query timed out after 30s")
        return None
    except Exception as e:
        logger.error(f"   [DB Exception] {type(e).__name__}: {str(e)}")
        error_logger.error(f"DB Exception - Query: {query[:200]} | Error: {type(e).__name__}: {str(e)}")
        return None

def get_template_data(template_id: str) -> Optional[Dict[str, str]]:
    """Fetch template data from song_templates table."""
    query = f"SELECT image_url, generate_video_prompt, song_type_id FROM song_templates WHERE id = '{template_id}';"
    result = run_psql(query, log_query=True)
    
    if result:
        parts = result.split('|')
        if len(parts) >= 3:
            data = {
                'image_url': parts[0],
                'generate_video_prompt': parts[1],
                'song_type_id': parts[2]
            }
            logger.debug(f"   [Template Data] image_url: {parts[0][:50]}... | song_type_id: {parts[2]}")
            return data
        else:
            logger.error(f"   [Parse Error] Unexpected result format: {result[:100]}")
            error_logger.error(f"Template data parse failed - ID: {template_id} | Result: {result[:200]}")
    else:
        logger.error(f"   [DB Empty] No data returned for template {template_id[:8]}...")
        error_logger.error(f"Template data fetch failed - ID: {template_id}")
    return None

def get_audio_mix_url(song_type_id: str) -> Optional[str]:
    """Fetch audio mix URL from song_types table."""
    query = f"SELECT amix_url FROM song_types WHERE id = '{song_type_id}';"
    result = run_psql(query, log_query=True)
    if result:
        logger.debug(f"   [Audio URL] {result[:80]}...")
        return result
    else:
        logger.error(f"   [Audio Missing] No amix_url for song_type {song_type_id}")
        error_logger.error(f"Audio mix URL missing - song_type_id: {song_type_id}")
    return None

def get_audio_duration(audio_url: str, download: bool = False) -> Tuple[float, Optional[str]]:
    """Get audio duration in seconds using ffprobe."""
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name
        
        logger.debug(f"   [Audio Download] {audio_url[:60]}...")
        download_start = time.time()
        download_cmd = ['curl', '-s', '-L', '-o', temp_path, audio_url]
        result = subprocess.run(download_cmd, timeout=60, check=True, capture_output=True)
        download_time = time.time() - download_start
        logger.debug(f"   [Audio Downloaded] {os.path.getsize(temp_path)} bytes | {download_time:.1f}s")
        
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            temp_path
        ]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        if probe_result.returncode == 0:
            duration = float(probe_result.stdout.strip())
            logger.debug(f"   [Audio Duration] {duration:.2f}s")
            if download:
                return duration, temp_path
            else:
                if os.path.exists(temp_path): os.unlink(temp_path)
                return duration, None
        else:
            logger.error(f"   [ffprobe Error] {probe_result.stderr[:200]}")
            error_logger.error(f"ffprobe failed - audio_url={audio_url[:80]}... | stderr={probe_result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        logger.error(f"   [Audio Timeout] Download or probe timed out")
        error_logger.error(f"Audio timeout - audio_url={audio_url[:80]}...")
    except Exception as e:
        logger.error(f"   [Audio Exception] {type(e).__name__}: {str(e)}")
        error_logger.error(f"Audio exception - audio_url={audio_url[:80]}... | error={type(e).__name__}: {str(e)}")
    finally:
        if temp_path and os.path.exists(temp_path): os.unlink(temp_path)
    
    return 12.0, None

def call_mcp_create_video(template_id: str, prompt: str, model: str, 
                          image_url: str = "", video_url: str = "",
                          audio_url: str = "", duration: str = "", 
                          aspect_ratio: str = "") -> Optional[str]:
    """Call MCP create-video tool and return the video URL."""
    arguments = {
        "prompt": prompt,
        "model": model
    }
    
    if image_url: arguments["imageUrl"] = image_url
    if video_url: arguments["videoUrl"] = video_url
    if audio_url: arguments["audioUrl"] = audio_url
    if duration: arguments["duration"] = duration
    if aspect_ratio: arguments["aspectRatio"] = aspect_ratio
    
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
    
    logger.debug(f"   [MCP Request] model={model} | duration={duration} | prompt_len={len(prompt)}")
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        elapsed = time.time() - start_time
        logger.debug(f"   [MCP Response] {elapsed:.1f}s | status={result.returncode}")
        
        if result.returncode != 0:
            logger.error(f"   [MCP Curl Error] returncode={result.returncode} | stderr={result.stderr[:200]}")
            error_logger.error(f"MCP curl failed - template={template_id[:8]}... | stderr={result.stderr[:300]}")
            return None
        
        response = json.loads(result.stdout)
        
        if 'result' in response:
            result_data = response['result']
            job_id = None
            
            if isinstance(result_data, dict):
                if 'structuredContent' in result_data:
                    sc = result_data['structuredContent']
                    if isinstance(sc, dict) and 'data' in sc:
                        data = sc['data']
                        if isinstance(data, dict) and 'job_id' in data:
                            job_id = data['job_id']
                            logger.debug(f"   [Job ID] {job_id}")
                        elif isinstance(data, dict) and 'url' in data:
                            url = data['url']
                            logger.debug(f"   [Direct URL] {url[:60]}...")
                            return url
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
                                        logger.debug(f"   [Job ID] {job_id}")
                                    elif 'url' in parsed['data']:
                                        return parsed['data']['url']
                            except json.JSONDecodeError as je:
                                logger.error(f"   [JSON Parse Error] {str(je)}")
                                error_logger.error(f"JSON parse failed - template={template_id[:8]}... | raw={item['text'][:200]}")
            
            if job_id:
                return poll_video_job(template_id, job_id, model)
            else:
                logger.error(f"   [No Job ID] Response: {json.dumps(result_data)[:300]}")
                error_logger.error(f"No job_id in response - template={template_id[:8]}... | response={json.dumps(result_data)[:400]}")
        else:
            logger.error(f"   [No Result] Response: {json.dumps(response)[:300]}")
            error_logger.error(f"No result in MCP response - template={template_id[:8]}... | response={json.dumps(response)[:400]}")
        return None
    except subprocess.TimeoutExpired:
        logger.error(f"   [MCP Timeout] Request timed out after 120s")
        error_logger.error(f"MCP timeout - template={template_id[:8]}... | model={model}")
        return None
    except json.JSONDecodeError as je:
        logger.error(f"   [JSON Error] {str(je)} | raw={result.stdout[:200]}")
        error_logger.error(f"JSON decode failed - template={template_id[:8]}... | error={str(je)} | raw={result.stdout[:300]}")
        return None
    except Exception as e:
        logger.error(f"   [MCP Exception] {type(e).__name__}: {str(e)}")
        error_logger.error(f"MCP exception - template={template_id[:8]}... | error={type(e).__name__}: {str(e)} | traceback={traceback.format_exc()[:500]}")
        return None

def poll_video_job(template_id: str, job_id: str, job_type: str, max_attempts: int = 500, poll_interval: int = 5) -> Optional[str]:
    """Poll fetch-asset endpoint until video is ready."""
    asset_type = 'create-video'
    logger.debug(f"   [Poll Start] job_id={job_id} | max_attempts={max_attempts} | interval={poll_interval}s")
    
    poll_start = time.time()
    for attempt in range(max_attempts):
        time.sleep(poll_interval)
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "fetch-asset",
                "arguments": { "id": job_id, "type": asset_type }
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
            
            if result.returncode != 0:
                logger.warning(f"   [Poll {attempt+1}] curl error: {result.stderr[:100]}")
                continue
            
            response = json.loads(result.stdout)
            
            if 'result' in response:
                result_data = response['result']
                status = None
                video_url = None
                
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
                                except json.JSONDecodeError:
                                    pass
                
                if attempt % 20 == 0 or attempt < 5:  # Log every 20 attempts or first 5
                    logger.debug(f"   [Poll {attempt+1}] status={status} | elapsed={(time.time()-poll_start)/60:.1f}min")
                
                if status == 'success' and video_url:
                    logger.info(f"   [Poll Success] {attempt+1} polls | {(time.time()-poll_start)/60:.1f}min | URL: {video_url[:60]}...")
                    return video_url
                elif status == 'failed':
                    logger.error(f"   [Poll Failed] Job failed after {attempt+1} polls | {(time.time()-poll_start)/60:.1f}min")
                    error_logger.error(f"Video generation failed - template={template_id[:8]}... | job_id={job_id} | attempts={attempt+1}")
                    return None
        except subprocess.TimeoutExpired:
            logger.warning(f"   [Poll Timeout] Attempt {attempt+1}")
            continue
        except json.JSONDecodeError as je:
            logger.warning(f"   [Poll JSON Error] {str(je)}")
            continue
        except Exception as e:
            logger.warning(f"   [Poll Exception] {type(e).__name__}: {str(e)}")
            continue
    
    total_time = time.time() - poll_start
    logger.error(f"   [Poll Timeout] Max attempts ({max_attempts}) reached after {total_time/60:.1f}min")
    error_logger.error(f"Poll timeout - template={template_id[:8]}... | job_id={job_id} | total_time={total_time/60:.1f}min")
    return None

def update_final_video_url(template_id: str, video_url: str) -> bool:
    """Update the song_templates table with final video URL (video_url and video_url_seedream_v4 columns)."""
    query = f"UPDATE song_templates SET video_url = '{video_url}', video_url_seedream_v4 = '{video_url}' WHERE id = '{template_id}';"
    logger.debug(f"   [DB Update Final] {query[:150]}...")
    result = run_psql(query, log_query=True)
    if result is not None:
        logger.info(f"   [DB Updated] video_url saved")
        return True
    else:
        logger.error(f"   [DB Update Final Failed] No result returned")
        error_logger.error(f"DB update final failed - template={template_id[:8]}... | video_url={video_url[:80]}...")
        return False

def trim_video(video_url: str, duration: float, template_id: str) -> Optional[str]:
    """Trim video and upload to GCS."""
    temp_in = None
    temp_out = None
    try:
        fd_in, temp_in = tempfile.mkstemp(suffix='.mp4')
        os.close(fd_in)
        fd_out, temp_out = tempfile.mkstemp(suffix='.mp4')
        os.close(fd_out)

        logger.debug(f"   [Video Download] {video_url[:60]}...")
        download_start = time.time()
        download_cmd = ['curl', '-s', '-L', '-o', temp_in, video_url]
        subprocess.run(download_cmd, timeout=120, check=True)
        download_time = time.time() - download_start
        logger.debug(f"   [Video Downloaded] {os.path.getsize(temp_in)} bytes | {download_time:.1f}s")
        
        logger.debug(f"   [Video Trim] duration={duration:.1f}s")
        trim_start = time.time()
        trim_cmd = [
            'ffmpeg', '-y', '-i', temp_in, '-t', str(duration),
            '-c:v', 'libx264', '-c:a', 'aac', '-shortest', temp_out
        ]
        trim_result = subprocess.run(trim_cmd, capture_output=True, text=True, timeout=300)
        trim_time = time.time() - trim_start
        if trim_result.returncode != 0:
            logger.error(f"   [ffmpeg Error] {trim_result.stderr[:200]}")
            error_logger.error(f"ffmpeg trim failed - template={template_id[:8]}... | stderr={trim_result.stderr[:300]}")
            return None
        logger.debug(f"   [Video Trimmed] {os.path.getsize(temp_out)} bytes | {trim_time:.1f}s")
        
        unique_id = str(uuid.uuid4())[:8]
        gcs_filename = f"trimmed/{template_id}_{unique_id}.mp4"
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        service_account_path = os.getenv("STH_GCS_KEY_PATH", "")
        
        logger.debug(f"   [GCS Upload] bucket=claw-data | file={gcs_filename}")
        upload_start = time.time()
        client = storage.Client.from_service_account_json(service_account_path)
        bucket = client.get_bucket("claw-data")
        blob = bucket.blob(gcs_filename, chunk_size=512 * 1024 * 1024)
        blob.upload_from_filename(temp_out)
        upload_time = time.time() - upload_start
        public_url = blob.public_url
        logger.info(f"   [GCS Uploaded] {public_url[:60]}... | {upload_time:.1f}s")
        
        return public_url
    except subprocess.TimeoutExpired as te:
        logger.error(f"   [Trim Timeout] {str(te)}")
        error_logger.error(f"Trim timeout - template={template_id[:8]}... | error={str(te)}")
        return None
    except Exception as e:
        logger.error(f"   [Trim Exception] {type(e).__name__}: {str(e)}")
        error_logger.error(f"Trim exception - template={template_id[:8]}... | error={type(e).__name__}: {str(e)} | traceback={traceback.format_exc()[:400]}")
        return None
    finally:
        if temp_in and os.path.exists(temp_in): os.unlink(temp_in)
        if temp_out and os.path.exists(temp_out): os.unlink(temp_out)

# ============================================================================
# PHASE 1: Generate Videos (API calls only, 5 workers)
# ============================================================================

def generate_video_phase(template_id: str) -> Tuple[str, bool, str]:
    """Phase 1: Generate raw video (Stages 3-4) and save to local JSON file."""
    thread_name = f"gen-{template_id[:8]}"
    logger.info(f"🎬 GENERATE: {template_id} [{thread_name}]")
    stage_start = time.time()
    
    try:
        # Stage -1: Check if final video URL already exists (skip Phase 1 entirely)
        existing_final = get_raw_video_url_from_state(template_id)
        if existing_final:
            # Check if it's infinitetalk URL (Stage 4 complete) or keling3 URL (Stage 3 only)
            if '/infinitetalk/' in existing_final:
                logger.info(f"   ── [SKIP Phase 1] Stage 4 (infinitetalk) already complete: {existing_final[:60]}...")
                logger.info(f"   ── [INFO] Template ready for Phase 2 (trim + DB update)")
                total_time = time.time() - stage_start
                return template_id, True, "Success_Phase1AlreadyDone"
            elif '/keling' in existing_final or '/seedance' in existing_final:
                # Stage 3 done, need Stage 4
                logger.info(f"   ── [RECOVER] Stage 3 complete, running Stage 4 (infinitetalk)...")
                stage_start_recovery = time.time()
                template_data = get_template_data(template_id)
                if not template_data:
                    error_logger.error(f"FAILED recovery - template={template_id} | error=No template data")
                    return template_id, False, "Failed_Recovery_NoData"
                audio_url = get_audio_mix_url(template_data['song_type_id'])
                if not audio_url:
                    error_logger.error(f"FAILED recovery - template={template_id} | error=No audio URL")
                    return template_id, False, "Failed_Recovery_NoAudio"
                final_video_url = call_mcp_create_video(
                    template_id=template_id,
                    prompt=template_data['generate_video_prompt'],
                    video_url=existing_final,
                    model='infinitetalk',
                    audio_url=audio_url
                )
                if not final_video_url:
                    error_logger.error(f"FAILED recovery at infinitetalk - template={template_id}")
                    return template_id, False, "Failed_Recovery_Infinitetalk"
                logger.info(f"   ── Stage 4 Complete (recovery): {(time.time()-stage_start_recovery)/60:.1f}min | URL: {final_video_url[:60]}...")
                logger.info(f"   ── Stage 5: Saving final video URL to local state file...")
                save_raw_video_url(template_id, final_video_url)
                total_time = time.time() - stage_start
                logger.info(f"✅ GENERATE COMPLETE (recovery): {template_id} | Total: {total_time/60:.1f}min")
                return template_id, True, "Success_Recovery_Stage4"
        
        # Stage 0: Fetch template data
        logger.info(f"   ── Stage 0: Fetching template data...")
        template_data = get_template_data(template_id)
        if not template_data:
            error_logger.error(f"FAILED at Stage 0 - template={template_id} | error=No template data")
            return template_id, False, "Failed_Stage0"
        
        # Stage 1: Fetch audio
        logger.info(f"   ── Stage 1: Fetching audio mix...")
        audio_url = get_audio_mix_url(template_data['song_type_id'])
        if not audio_url:
            error_logger.error(f"FAILED at Stage 1 - template={template_id} | error=No audio URL")
            return template_id, False, "Failed_Stage1"
        
        # Stage 2: Get audio duration
        logger.info(f"   ── Stage 2: Analyzing audio duration...")
        audio_duration, audio_temp_path = get_audio_duration(audio_url, download=True)
        video_model = 'keling3' if audio_duration > 12.0 else 'seedance1.5pro'
        video_duration = '15' if audio_duration > 12.0 else '12'
        logger.info(f"   ── Stage 2 Complete: duration={audio_duration:.1f}s | model={video_model} | output={video_duration}s")
        
        # Stage 3: Generate original video
        logger.info(f"   ── Stage 3: Generating original video ({video_model})...")
        stage3_start = time.time()
        original_video_url = call_mcp_create_video(
            template_id=template_id,
            prompt=template_data['generate_video_prompt'],
            image_url=template_data['image_url'],
            model=video_model,
            duration=video_duration,
            aspect_ratio='9:16'
        )
        stage3_time = time.time() - stage3_start
        if not original_video_url:
            error_logger.error(f"FAILED at Stage 3 - template={template_id} | model={video_model} | time={stage3_time/60:.1f}min")
            if audio_temp_path and os.path.exists(audio_temp_path): os.unlink(audio_temp_path)
            return template_id, False, "Failed_Stage3"
        logger.info(f"   ── Stage 3 Complete: {stage3_time/60:.1f}min | URL: {original_video_url[:60]}...")
        
        # SAVE Stage 3 URL to state file so we don't regenerate it if Stage 4 fails
        save_raw_video_url(template_id, original_video_url)
        
        # Stage 4: Generate final video with infinitetalk
        logger.info(f"   ── Stage 4: Generating final video (infinitetalk)...")
        stage4_start = time.time()
        final_video_url = call_mcp_create_video(
            template_id=template_id,
            prompt=template_data['generate_video_prompt'],
            video_url=original_video_url,
            model='infinitetalk',
            audio_url=audio_url
        )
        stage4_time = time.time() - stage4_start
        if not final_video_url:
            error_logger.error(f"FAILED at Stage 4 - template={template_id} | time={stage4_time/60:.1f}min")
            if audio_temp_path and os.path.exists(audio_temp_path): os.unlink(audio_temp_path)
            return template_id, False, "Failed_Stage4"
        logger.info(f"   ── Stage 4 Complete: {stage4_time/60:.1f}min | URL: {final_video_url[:60]}...")
        
        # Cleanup temp audio
        if audio_temp_path and os.path.exists(audio_temp_path): os.unlink(audio_temp_path)
        
        # Stage 5: Save to local state file (NOT database)
        logger.info(f"   ── Stage 5: Saving raw video URL to local state file...")
        stage5_start = time.time()
        save_raw_video_url(template_id, final_video_url)
        stage5_time = time.time() - stage5_start
        total_time = time.time() - stage_start
        
        logger.info(f"✅ GENERATE COMPLETE: {template_id} | Total: {total_time/60:.1f}min")
        return template_id, True, "Success"
            
    except Exception as e:
        total_time = time.time() - stage_start
        logger.error(f"❌ EXCEPTION: {template_id} | {type(e).__name__}: {str(e)} | Total: {total_time/60:.1f}min")
        error_logger.error(f"EXCEPTION - template={template_id} | error={type(e).__name__}: {str(e)} | traceback={traceback.format_exc()[:500]}")
        return template_id, False, f"Exception_{type(e).__name__}"

# ============================================================================
# PHASE 2: Trim Videos (ffmpeg + GCS, 1 worker sequential)
# ============================================================================

def trim_video_phase(template_id: str) -> Tuple[str, bool, str]:
    """Phase 2: Download, trim, and upload video (Stages 3-4)."""
    thread_name = f"trim-{template_id[:8]}"
    logger.info(f"✂️  TRIM: {template_id} [{thread_name}]")
    stage_start = time.time()
    
    try:
        # Stage 0: Fetch raw video URL from local state file
        logger.info(f"   ── Stage 0: Fetching raw video URL from state file...")
        raw_video_url = get_raw_video_url_from_state(template_id)
        if not raw_video_url:
            error_logger.error(f"FAILED at Stage 0 - template={template_id} | error=No video_url_raw in state file")
            return template_id, False, "Failed_Stage0_NoRawVideo"
        logger.info(f"   ── Stage 0 Complete: {raw_video_url[:60]}...")
        
        # Stage 1: Get audio duration (to determine trim length)
        logger.info(f"   ── Stage 1: Fetching audio duration...")
        template_data = get_template_data(template_id)
        if not template_data:
            error_logger.error(f"FAILED at Stage 1 - template={template_id} | error=No template data")
            return template_id, False, "Failed_Stage1"
        
        audio_url = get_audio_mix_url(template_data['song_type_id'])
        if not audio_url:
            error_logger.error(f"FAILED at Stage 1 - template={template_id} | error=No audio URL")
            return template_id, False, "Failed_Stage1_Audio"
        
        audio_duration, _ = get_audio_duration(audio_url, download=False)
        video_duration = '15' if audio_duration > 12.0 else '12'
        logger.info(f"   ── Stage 1 Complete: audio_duration={audio_duration:.1f}s | trim_to={audio_duration:.1f}s")
        
        # Stage 2: Trim video (only if audio_duration < video_duration)
        if audio_duration < float(video_duration):
            logger.info(f"   ── Stage 2: Trimming video to {audio_duration:.1f}s...")
            stage2_start = time.time()
            trimmed_url = trim_video(raw_video_url, audio_duration, template_id)
            stage2_time = time.time() - stage2_start
            if not trimmed_url:
                error_logger.error(f"FAILED at Stage 2 - template={template_id} | trim failed")
                return template_id, False, "Failed_Stage2_Trim"
            logger.info(f"   ── Stage 2 Complete: {stage2_time:.1f}s | URL: {trimmed_url[:60]}...")
            final_video_url = trimmed_url
        else:
            logger.info(f"   ── Stage 2: No trimming needed (audio={audio_duration:.1f}s >= max={video_duration}s)")
            final_video_url = raw_video_url
        
        # Stage 3: Update database (video_url, video_url_seedream_v4)
        logger.info(f"   ── Stage 3: Updating database (video_url)...")
        stage3_start = time.time()
        success = update_final_video_url(template_id, final_video_url)
        stage3_time = time.time() - stage3_start
        total_time = time.time() - stage_start
        
        if success:
            logger.info(f"✅ TRIM COMPLETE: {template_id} | Total: {total_time/60:.1f}min")
            return template_id, True, "Success"
        else:
            error_logger.error(f"FAILED at Stage 3 - template={template_id} | DB update failed")
            return template_id, False, "Failed_Stage3"
            
    except Exception as e:
        total_time = time.time() - stage_start
        logger.error(f"❌ EXCEPTION: {template_id} | {type(e).__name__}: {str(e)} | Total: {total_time/60:.1f}min")
        error_logger.error(f"EXCEPTION - template={template_id} | error={type(e).__name__}: {str(e)} | traceback={traceback.format_exc()[:500]}")
        return template_id, False, f"Exception_{type(e).__name__}"

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_phase(phase_name: str, process_func, template_ids: List[str], max_workers: int, csv_file: str) -> Dict[str, str]:
    """Run a phase with specified workers."""
    results_map = {}
    start_time = time.time()
    
    logger.info("=" * 80)
    logger.info(f"🚀 {phase_name} START")
    logger.info(f"   Templates: {len(template_ids)}")
    logger.info(f"   Workers: {max_workers}")
    logger.info(f"   Time: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    # Remove any existing stop signal
    if os.path.exists(STOP_SIGNAL_FILE):
        os.unlink(STOP_SIGNAL_FILE)
        logger.info("   [Cleanup] Removed existing stop signal file")

    executor = ThreadPoolExecutor(max_workers=max_workers)
    try:
        futures = {}
        to_submit = list(template_ids)
        
        def submit_next():
            if to_submit and not check_stop_signal():
                tid = to_submit.pop(0)
                future = executor.submit(process_func, tid)
                futures[future] = tid
                logger.debug(f"   [Submitted] {tid[:8]}... | pending={len(to_submit)} | running={len(futures)}")
                return True
            return False

        # Initial fill
        for _ in range(max_workers):
            if not submit_next(): break

        completed = 0
        loop_iterations = 0
        try:
            while futures:
                loop_iterations += 1
                done_futures = [f for f in futures if f.done()]
                if not done_futures:
                    time.sleep(1)
                    # Log progress every 60 seconds to confirm we're still alive
                    if loop_iterations % 60 == 0:
                        logger.info(f"   [Heartbeat] {completed}/{len(template_ids)} complete | {len(futures)} running | {len(to_submit)} pending")
                    continue
                    
                for future in done_futures:
                    tid = futures.pop(future)
                    completed += 1
                    try:
                        tid, success, status = future.result()
                        results_map[tid] = "TRUE" if success else "FALSE"
                        elapsed = time.time() - start_time
                        eta_min = (elapsed / completed * (len(template_ids) - completed) / 60) if completed > 0 else 0
                        success_count = sum(1 for v in results_map.values() if v == "TRUE")
                        logger.info(f"📊 PROGRESS: {completed}/{len(template_ids)} | {elapsed/60:.1f}min elapsed | ETA: {eta_min:.0f}min | Success: {success_count}")
                    except Exception as e:
                        logger.error(f"Error processing {tid}: {type(e).__name__}: {str(e)}")
                        error_logger.error(f"Future exception - template={tid[:8]}... | error={type(e).__name__}: {str(e)}")
                        results_map[tid] = "FALSE"
                    
                    if not check_stop_signal():
                        submit_next()
                    elif to_submit:
                        logger.warning(f"⏹️  STOP SIGNAL: {len(to_submit)} pending jobs cancelled.")
                        error_logger.warning(f"Stop signal received - {len(to_submit)} templates cancelled")
                        for pending_tid in to_submit:
                            results_map[pending_tid] = "FALSE"
                        to_submit = []
            
            logger.info(f"   [Loop Exit] All {completed} templates processed successfully")
        except Exception as e:
            logger.error(f"❌ Main loop exception: {type(e).__name__}: {str(e)}")
            error_logger.error(f"Main loop crashed - completed={completed}/{len(template_ids)} | error={type(e).__name__}: {str(e)} | traceback={traceback.format_exc()[:500]}")
            # Continue to finally block to shutdown executor properly
            raise
        finally:
            # Ensure all submitted futures complete before shutting down
            if futures:
                logger.warning(f"   [Shutdown] Waiting for {len(futures)} running jobs to complete...")
                # Don't submit more, just wait for existing
                for future in list(futures.keys()):
                    try:
                        tid = futures[future]
                        tid_result, success, status = future.result(timeout=300)  # 5 min timeout per job
                        results_map[tid_result] = "TRUE" if success else "FALSE"
                        logger.info(f"   [Recovered] {tid[:8]}... | success={success}")
                    except Exception as e:
                        logger.error(f"   [Recovery Failed] {tid[:8]}... | {type(e).__name__}")
                        results_map[tid] = "FALSE"
                logger.info(f"   [Shutdown] All running jobs completed or timed out")
    finally:
        executor.shutdown(wait=True)
        logger.info("   [Executor] Shutdown complete")

    total_elapsed = time.time() - start_time
    success_count = sum(1 for v in results_map.values() if v == "TRUE")
    fail_count = len(results_map) - success_count
    
    logger.info("=" * 80)
    logger.info(f"✅ {phase_name} COMPLETE")
    logger.info(f"   Total Processed: {len(results_map)}")
    logger.info(f"   Success: {success_count} ({success_count/len(results_map)*100:.1f}%)")
    logger.info(f"   Failed: {fail_count} ({fail_count/len(results_map)*100:.1f}%)")
    logger.info(f"   Total Time: {total_elapsed/60:.1f}min ({total_elapsed:.0f}s)")
    logger.info(f"   Avg per Template: {total_elapsed/len(results_map):.1f}s")
    logger.info(f"   End Time: {datetime.now().isoformat()}")
    logger.info("=" * 80)

    # Update CSV status
    try:
        rows = []
        fieldnames = []
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                tid = row.get('Song Template ID', row.get('Template ID', '')).strip()
                if tid in results_map:
                    row['Status'] = results_map[tid]
                rows.append(row)
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info("✅ CSV status updated.")
    except Exception as e:
        logger.error(f"⚠ Could not update CSV: {type(e).__name__}: {str(e)}")
        error_logger.error(f"CSV update failed - file={csv_file} | error={type(e).__name__}: {str(e)}")
    
    return results_map

def main():
    parser = argparse.ArgumentParser(description='STH Video Template Generator - Phase-Separated')
    parser.add_argument('csv_file', help='Path to CSV file with template IDs')
    parser.add_argument('--mode', choices=['full', 'generate', 'trim'], default='full',
                        help='Execution mode: full (both phases), generate (Phase 1 only), trim (Phase 2 only)')
    args = parser.parse_args()
    
    csv_file = args.csv_file
    mode = args.mode
    
    # Read template IDs
    template_ids = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tid = row.get('Song Template ID', row.get('Template ID', '')).strip()
                status = row.get('Status', '').strip()
                if tid and status != "TRUE":
                    template_ids.append(tid)
    except Exception as e:
        logger.error(f"Error reading CSV: {type(e).__name__}: {str(e)}")
        error_logger.error(f"CSV read failed - file={csv_file} | error={type(e).__name__}: {str(e)}")
        sys.exit(1)
    
    if not template_ids:
        logger.error("No template IDs found in CSV")
        sys.exit(1)
    
    # Check which templates already have Stage 4 complete (skip Phase 1)
    phase1_ids = []
    phase2_only_ids = []
    try:
        with open(RAW_VIDEO_STATE_FILE, 'r') as f:
            raw_data = json.load(f)
        for tid in template_ids:
            if tid in raw_data and '/infinitetalk/' in raw_data[tid]:
                phase2_only_ids.append(tid)
                logger.info(f"   [Skip Phase 1] {tid[:8]}... (Stage 4 already complete)")
            else:
                phase1_ids.append(tid)
    except:
        phase1_ids = template_ids  # If no state file, run Phase 1 for all
    
    logger.info("=" * 80)
    logger.info(f"🎬 STH VIDEO GENERATOR - PHASE SEPARATED")
    logger.info(f"   Mode: {mode.upper()}")
    logger.info(f"   Total Templates: {len(template_ids)}")
    logger.info(f"   Need Phase 1 (generate): {len(phase1_ids)}")
    logger.info(f"   Need Phase 2 only (trim): {len(phase2_only_ids)}")
    logger.info(f"   CSV: {csv_file}")
    logger.info(f"   Log: {LOG_FILE}")
    logger.info(f"   Error Log: {ERROR_LOG_FILE}")
    logger.info(f"   State File: {RAW_VIDEO_STATE_FILE}")
    logger.info("=" * 80)
    
    all_results = {}
    
    if mode in ['full', 'generate']:
        # Phase 1: Generate videos (5 workers) - only for templates that need it
        if phase1_ids:
            generate_results = run_phase(
                phase_name="PHASE 1 (GENERATE)",
                process_func=generate_video_phase,
                template_ids=phase1_ids,
                max_workers=MAX_WORKERS_GENERATE,
                csv_file=csv_file
            )
            all_results.update(generate_results)
        else:
            logger.info("\n⏭️  Skipping Phase 1 - all templates already have Stage 4 complete")
        
        if mode == 'generate':
            logger.info("\n🏁 GENERATE MODE COMPLETE - Skipping trim phase")
            logger.info(f"📄 Raw video URLs saved to: {RAW_VIDEO_STATE_FILE}")
            sys.exit(0)
    
    if mode in ['full', 'trim']:
        # For trim phase, combine templates that completed Phase 1 + those that skipped it
        if mode == 'trim':
            # Re-read to get templates that need trimming
            template_ids = []
            try:
                with open(csv_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        tid = row.get('Song Template ID', row.get('Template ID', '')).strip()
                        status = row.get('Status', '').strip()
                        if tid and status != "TRUE":
                            template_ids.append(tid)
            except Exception as e:
                logger.error(f"Error reading CSV for trim phase: {type(e).__name__}: {str(e)}")
                sys.exit(1)
        else:
            # Full mode: combine Phase 1 completions + Phase 2-only templates
            template_ids = phase1_ids + phase2_only_ids
        
        if not template_ids:
            logger.info("\n🏁 No templates remaining for trim phase")
            sys.exit(0)
        
        # Phase 2: Trim videos (1 worker, sequential)
        trim_results = run_phase(
            phase_name="PHASE 2 (TRIM)",
            process_func=trim_video_phase,
            template_ids=template_ids,
            max_workers=MAX_WORKERS_TRIM,
            csv_file=csv_file
        )
        all_results.update(trim_results)
    
    # Final summary
    logger.info("=" * 80)
    logger.info(f"🏁 ALL PHASES COMPLETE")
    logger.info(f"   Total Templates: {len(all_results)}")
    logger.info(f"   Success: {sum(1 for v in all_results.values() if v == 'TRUE')}")
    logger.info(f"   Failed: {sum(1 for v in all_results.values() if v == 'FALSE')}")
    logger.info(f"   State File: {RAW_VIDEO_STATE_FILE}")
    logger.info(f"   Log: {LOG_FILE}")
    logger.info(f"   Error Log: {ERROR_LOG_FILE}")
    logger.info("=" * 80)

if __name__ == '__main__':
    main()
