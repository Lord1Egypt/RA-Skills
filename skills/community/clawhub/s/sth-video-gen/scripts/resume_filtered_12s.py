import csv
import subprocess
import os
import json
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration from the original parallel script
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'dev_mobile',
    'user': 'openclaw',
    'password': ''
}

SKILL_DIR = "/root/.openclaw/workspace/skills/sth-video-template-generation"
GENERATOR_SCRIPT = os.path.join(SKILL_DIR, "sth_video_generator_parallel.py")
SOURCE_CSV = "/root/.openclaw/media/inbound/Copy_of_CFS_Template_IDS_-_Sheet1-original---adbe8d51-b0b7-46df-9382-2b0a640fef49.csv"
FILTERED_CSV = os.path.join(SKILL_DIR, "filtered_batch_12s.csv")

def run_psql(query):
    cmd = [
        'psql', '-h', DB_CONFIG['host'], '-p', DB_CONFIG['port'],
        '-U', DB_CONFIG['user'], '-d', DB_CONFIG['dbname'],
        '-t', '-A', '-c', query
    ]
    env = {'PGPASSWORD': DB_CONFIG['password']}
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else None
    except: return None

def get_audio_duration(audio_url):
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name
        subprocess.run(['curl', '-s', '-L', '-o', temp_path, audio_url], timeout=60, check=True)
        probe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', temp_path]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        duration = float(result.stdout.strip())
        if os.path.exists(temp_path): os.unlink(temp_path)
        return duration
    except:
        if temp_path and os.path.exists(temp_path): os.unlink(temp_path)
        return 999.0

def check_template(row):
    tid = row.get('Song Template ID', row.get('Template ID', '')).strip()
    if not tid: return None
    
    # Get song_type_id
    query = f"SELECT song_type_id FROM song_templates WHERE id = '{tid}';"
    song_type_id = run_psql(query)
    if not song_type_id: return None
    
    # Get audio URL
    audio_url = run_psql(f"SELECT amix_url FROM song_types WHERE id = '{song_type_id}';")
    if not audio_url: return None
    
    duration = get_audio_duration(audio_url)
    if duration <= 12.0:
        return row
    return None

def main():
    print("Filtering templates by audio duration (<= 12s)...")
    templates_to_process = []
    
    with open(SOURCE_CSV, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Use parallel checking to speed up filtering
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_template, row) for row in rows]
        for future in as_completed(futures):
            res = future.result()
            if res:
                templates_to_process.append(res)

    print(f"Found {len(templates_to_process)} templates with duration <= 12s.")
    
    with open(FILTERED_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(templates_to_process)
    
    print(f"Filtered CSV saved to {FILTERED_CSV}")
    print("Launching parallel generator...")
    
    # Launch the actual generator
    subprocess.run(['python3', GENERATOR_SCRIPT, FILTERED_CSV])

if __name__ == "__main__":
    main()
