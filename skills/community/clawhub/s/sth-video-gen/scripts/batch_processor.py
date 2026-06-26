import csv
import subprocess
import os
import json
import time

# Skill directory
SKILL_DIR = "/root/.openclaw/workspace/skills/sth-video-template-generation"
INPUT_CSV = os.path.join(SKILL_DIR, "input.csv")
FINAL_CSV = os.path.join(SKILL_DIR, "Copy_of_CFS_Template_IDS_Final.csv")
GENERATOR_SCRIPT = os.path.join(SKILL_DIR, "sth_video_generator.py")

# DB Config
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'dev_mobile',
    'user': 'openclaw',
    'password': ''
}

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
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip()) if result.returncode == 0 else 0
    except: return 0

def process():
    # Load IDs from input.csv
    with open(INPUT_CSV, 'r') as f:
        rows = list(csv.DictReader(f))

    print(f"Processing {len(rows)} records...")
    
    for i, row in enumerate(rows):
        template_id = row['Song Template ID']
        print(f"[{i+1}/{len(rows)}] Checking {template_id}...")
        
        # 1. Fetch DB info
        query = f"SELECT image_url, song_type_id, video_url FROM song_templates WHERE id = '{template_id}';"
        res = run_psql(query)
        if not res:
            print(f"  Skipping: DB record not found")
            continue
            
        parts = res.split('|')
        image_url, song_type_id, db_video_url = parts[0], parts[1], parts[2]
        
        # 2. Get Audio URL & Duration
        audio_url = run_psql(f"SELECT amix_url FROM song_types WHERE id = '{song_type_id}';")
        if not audio_url:
            print(f"  Skipping: Audio URL not found")
            continue
            
        duration = get_audio_duration(audio_url)
        print(f"  Duration: {duration:.2f}s")
        
        # RULE 1: only process where duration ≤ 12.00s
        if duration > 12.00:
            print(f"  Skipping: Duration > 12s")
            continue
            
        # RULE 2: skip if video_url is NOT empty AND duration ≤ 12.00s
        if db_video_url and db_video_url.strip():
            print(f"  Skipping: Video URL already exists in DB")
            continue
            
        # 3. Execute!
        print(f"  >> EXECUTING generator for {template_id}...")
        # We create a temporary 1-line CSV for the generator to use
        tmp_csv = os.path.join(SKILL_DIR, f"tmp_{template_id}.csv")
        with open(tmp_csv, 'w') as f:
            f.write(f"Song Template ID,Status\n{template_id},Pending\n")
            
        try:
            subprocess.run(['python3', GENERATOR_SCRIPT, tmp_csv], check=True)
            # Read status back
            with open(tmp_csv, 'r') as f:
                tmp_row = list(csv.DictReader(f))[0]
                rows[i]['Status'] = tmp_row['Status']
                print(f"  Result: {tmp_row['Status']}")
        except Exception as e:
            print(f"  Error: {e}")
            rows[i]['Status'] = "FALSE"
        finally:
            if os.path.exists(tmp_csv): os.unlink(tmp_csv)

    # Save final results
    with open(INPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Song Template ID', 'Status'])
        writer.writeheader()
        writer.writerows(rows)
    print("Batch complete.")

if __name__ == "__main__":
    process()
