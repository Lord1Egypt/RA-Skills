import csv
import subprocess
import json
import time
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

def generate_video(template_id: str, video_prompt: str, reference_image_url: str, amix_url: str):
    """Generate video using MCP API with keling3 model for >12s content."""
    
    # Create job parameters
    job_params = {
        "template_id": template_id,
        "video_model": "keling3",
        "duration": "15",
        "video_prompt": video_prompt,
        "reference_image_url": reference_image_url,
        "audio_url": amix_url
    }
    
    # Call MCP generate-video tool via openclaw-mcp-bridge or direct
    # Using the sth_video_generator.py approach
    script_path = os.path.join(os.path.dirname(__file__), 'sth_video_generator.py')
    
    cmd = ['python3', script_path, '--template-id', template_id, '--model', 'keling3', '--duration', '15']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return result.stdout, result.returncode == 0
    except subprocess.TimeoutExpired:
        return "Timeout", False
    except Exception as e:
        return str(e), False

def update_video_url(template_id: str, video_url: str):
    """Update the video_url in the database."""
    query = f"UPDATE song_templates SET video_url = '{video_url}' WHERE id = '{template_id}';"
    result = run_psql(query)
    return result is not None

def process_templates(input_file: str):
    """Process all templates from the CSV file."""
    
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        templates = list(reader)
    
    print(f"Processing {len(templates)} templates...")
    print("=" * 80)
    
    results = []
    
    for i, row in enumerate(templates, 1):
        template_id = row['Template ID'].strip()
        name = row.get('Names', '').strip()
        duration = row.get('Duration', 'N/A')
        
        print(f"\n[{i}/{len(templates)}] Template: {template_id} ({name})")
        print(f"Duration: {duration}s")
        
        # Fetch template data from database
        q1 = f"SELECT song_type_id FROM song_templates WHERE id = '{template_id}';"
        song_type_id = run_psql(q1)
        
        if not song_type_id:
            print(f"  ❌ Failed to find song_type_id")
            results.append({'template_id': template_id, 'status': 'FAILED', 'reason': 'No song_type_id'})
            continue
        
        # Get amix_url
        q2 = f"SELECT amix_url FROM song_types WHERE id = '{song_type_id}';"
        amix_url = run_psql(q2)
        
        if not amix_url:
            print(f"  ❌ Failed to find amix_url")
            results.append({'template_id': template_id, 'status': 'FAILED', 'reason': 'No amix_url'})
            continue
        
        # Get reference_image_url
        q3 = f"SELECT reference_image_url FROM song_templates WHERE id = '{template_id}';"
        reference_image_url = run_psql(q3)
        
        if not reference_image_url:
            print(f"  ❌ Failed to find reference_image_url")
            results.append({'template_id': template_id, 'status': 'FAILED', 'reason': 'No reference_image_url'})
            continue
        
        # Get generate_video_prompt
        q4 = f"SELECT generate_video_prompt FROM song_templates WHERE id = '{template_id}';"
        video_prompt = run_psql(q4)
        
        if not video_prompt:
            print(f"  ❌ Failed to find generate_video_prompt")
            results.append({'template_id': template_id, 'status': 'FAILED', 'reason': 'No video_prompt'})
            continue
        
        print(f"  ✓ Data fetched successfully")
        print(f"  → Generating video with keling3 (15s)...")
        
        # Generate video using the parallel generator script
        gen_script = os.path.join(os.path.dirname(__file__), 'sth_video_generator_parallel.py')
        cmd = ['python3', gen_script, '--single', template_id]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
            output = result.stdout
            
            # Check for success in output
            if 'SUCCESS' in output or 'video_url' in output.lower():
                # Extract video URL from output or database
                time.sleep(2)  # Wait for DB update
                q5 = f"SELECT video_url FROM song_templates WHERE id = '{template_id}';"
                video_url = run_psql(q5)
                
                if video_url:
                    print(f"  ✅ SUCCESS: Video generated")
                    results.append({'template_id': template_id, 'status': 'SUCCESS', 'video_url': video_url})
                else:
                    print(f"  ⚠️ Generated but no URL in DB")
                    results.append({'template_id': template_id, 'status': 'PARTIAL', 'reason': 'No URL after gen'})
            else:
                print(f"  ❌ Generation failed")
                results.append({'template_id': template_id, 'status': 'FAILED', 'reason': 'Generation error'})
                
        except subprocess.TimeoutExpired:
            print(f"  ❌ Timeout during generation")
            results.append({'template_id': template_id, 'status': 'TIMEOUT'})
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append({'template_id': template_id, 'status': 'ERROR', 'reason': str(e)})
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY:")
    success = sum(1 for r in results if r['status'] == 'SUCCESS')
    failed = sum(1 for r in results if r['status'] in ['FAILED', 'ERROR', 'TIMEOUT'])
    partial = sum(1 for r in results if r['status'] == 'PARTIAL')
    print(f"  ✅ Success: {success}")
    print(f"  ⚠️ Partial: {partial}")
    print(f"  ❌ Failed: {failed}")
    
    # Write results
    with open('rerun_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to rerun_results.json")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 rerun_over_12s.py <input_csv>")
        sys.exit(1)
    
    process_templates(sys.argv[1])
