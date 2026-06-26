#!/usr/bin/env python3
import csv
import psycopg2

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="dev_mobile",
    user="openclaw",
    password=""
)
cursor = conn.cursor()

# Read song_types_duration.csv to create lookup
song_types_lookup = {}
with open('/root/.openclaw/media/inbound/song_types_duration---dd287196-9595-4541-a38c-acd13f5d54f9.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        song_type_id = row.get('Id', '').strip()
        if song_type_id:
            song_types_lookup[song_type_id] = {
                'name': row.get('name', ''),
                'duration': row.get('duration', '')
            }

print(f"Loaded {len(song_types_lookup)} song types from duration CSV")

# Read existing FULL_TEMPLATE_STATUS_REPORT.csv
rows = []
template_ids = []
with open('FULL_TEMPLATE_STATUS_REPORT.csv', 'r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames + ['song_type_id', 'duration', 'video_url', 'name', 'title']
    for row in reader:
        template_id = row.get('Template ID', '').strip()
        if template_id:
            template_ids.append(template_id)
        rows.append(row)

print(f"Processing {len(template_ids)} templates")

# Query database for each template
for i, template_id in enumerate(template_ids):
    try:
        cursor.execute("""
            SELECT song_type_id, video_url, name, title 
            FROM song_templates 
            WHERE id = %s
        """, (template_id,))
        result = cursor.fetchone()
        
        if result:
            song_type_id, video_url, name, title = result
            rows[i]['song_type_id'] = song_type_id or ''
            rows[i]['video_url'] = video_url or ''
            rows[i]['name'] = name or ''
            rows[i]['title'] = title or ''
            
            # Look up duration and name from song_types_duration.csv
            if song_type_id and song_type_id in song_types_lookup:
                rows[i]['duration'] = song_types_lookup[song_type_id]['duration']
                # Also update name from song_types if template name is empty
                if not rows[i]['name']:
                    rows[i]['name'] = song_types_lookup[song_type_id]['name']
            else:
                rows[i]['duration'] = ''
        else:
            rows[i]['song_type_id'] = ''
            rows[i]['duration'] = ''
            rows[i]['video_url'] = ''
            rows[i]['name'] = ''
            rows[i]['title'] = ''
            
    except Exception as e:
        print(f"Error processing {template_id}: {e}")
        rows[i]['song_type_id'] = ''
        rows[i]['duration'] = ''
        rows[i]['video_url'] = ''
        rows[i]['name'] = ''
        rows[i]['title'] = ''
    
    if (i + 1) % 50 == 0:
        print(f"Processed {i + 1}/{len(template_ids)} templates")

# Write updated CSV
with open('FULL_TEMPLATE_STATUS_REPORT.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(rows)} records with song_type_id, duration, video_url, name, title")

cursor.close()
conn.close()
