import csv
import subprocess
import os
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'dev_mobile',
    'user': 'openclaw',
    'password': ''
}

def run_psql(query: str):
    cmd = [
        'psql',
        '-h', DB_CONFIG['host'],
        '-p', DB_CONFIG['port'],
        '-U', DB_CONFIG['user'],
        '-d', DB_CONFIG['dbname'],
        '-t', '-A', '-c', query
    ]
    env = {'PGPASSWORD': DB_CONFIG['password']}
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def get_audio_duration(audio_url: str):
    try:
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_url
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip()) if result.returncode == 0 else None
    except:
        return None

def check_csv(input_file, output_file):
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = ['Names', 'Template ID', 'Duration', 'video_url', 'Status']
        rows = list(reader)

    filtered_rows = []
    skipped_count = 0
    under_12s_count = 0
    
    print(f"Checking {len(rows)} templates for duration > 12s and video_url status...")
    for row in rows:
        template_id = row.get('Template ID', '').strip()
        name = row.get('Names', '').strip()
        if not template_id:
            continue
            
        # Get song_type_id
        q1 = f"SELECT song_type_id FROM song_templates WHERE id = '{template_id}';"
        song_type_id = run_psql(q1)
        
        if not song_type_id:
            print(f"Template {template_id}: Failed to find song_type_id. Skipping.")
            skipped_count += 1
            continue
            
        # Get amix_url
        q2 = f"SELECT amix_url FROM song_types WHERE id = '{song_type_id}';"
        amix_url = run_psql(q2)
        
        if not amix_url:
            print(f"Template {template_id}: Failed to find amix_url. Skipping.")
            skipped_count += 1
            continue
        
        # Get video_url
        q3 = f"SELECT video_url FROM song_templates WHERE id = '{template_id}';"
        video_url = run_psql(q3)
        video_status = "GENERATED" if video_url and video_url.strip() else "NOT_GENERATED"
            
        # Check duration
        duration = get_audio_duration(amix_url)
        if duration is not None:
            if duration > 12.0:
                print(f"Template {template_id}: Duration {duration:.2f}s (>12s) ✓ | video_url: {video_status}")
                filtered_rows.append({
                    'Names': name,
                    'Template ID': template_id,
                    'Duration': f"{duration:.2f}",
                    'video_url': video_status,
                    'Status': 'FALSE'
                })
            else:
                under_12s_count += 1
        else:
            print(f"Template {template_id}: Failed to get duration. Skipping.")
            skipped_count += 1

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)
    
    print(f"\nFiltering complete:")
    print(f"Total checked: {len(rows)}")
    print(f"Found (>12s): {len(filtered_rows)}")
    print(f"Skipped (<=12s): {under_12s_count}")
    print(f"Skipped (errors): {skipped_count}")

if __name__ == '__main__':
    check_csv(sys.argv[1], sys.argv[2])
