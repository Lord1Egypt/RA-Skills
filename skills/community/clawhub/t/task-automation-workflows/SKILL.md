---
name: task-automation
description: Automate repetitive tasks with scripts, workflows, and schedules. Create efficient automation for file operations, data processing, API calls, and scheduled jobs. Use when automating repetitive work, creating workflows, or scheduling tasks. Triggers on "automate", "workflow", "schedule", "repetitive", "batch", "cron".
---

# Task Automation

Turn repetitive work into automated workflows. Save time, reduce errors, scale operations.

## Automation Types

### 1. File Operations

**Batch Rename:**
```python
import os
import re

def batch_rename(directory, pattern, replacement):
    """Rename files matching pattern"""
    for filename in os.listdir(directory):
        if re.match(pattern, filename):
            new_name = re.sub(pattern, replacement, filename)
            os.rename(
                os.path.join(directory, filename),
                os.path.join(directory, new_name)
            )
            print(f"Renamed: {filename} -> {new_name}")
```

**Batch Convert:**
```python
from PIL import Image
import os

def convert_images(input_dir, output_dir, format='webp'):
    """Convert all images to format"""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(os.path.join(input_dir, filename))
            name = os.path.splitext(filename)[0]
            img.save(os.path.join(output_dir, f"{name}.{format}"), format.upper())
            print(f"Converted: {filename}")
```

**Organize Files:**
```python
import os
import shutil

def organize_by_type(directory):
    """Move files into type folders"""
    extensions = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.md'],
        'videos': ['.mp4', '.mov', '.avi', '.mkv'],
        'audio': ['.mp3', '.wav', '.flac'],
        'code': ['.py', '.js', '.ts', '.go', '.rs'],
    }
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            for folder, exts in extensions.items():
                if ext in exts:
                    target = os.path.join(directory, folder)
                    os.makedirs(target, exist_ok=True)
                    shutil.move(filepath, os.path.join(target, filename))
                    print(f"Moved {filename} to {folder}/")
                    break
```

### 2. Data Processing

**Batch Transform:**
```python
import pandas as pd

def process_csv_batch(input_dir, output_file, transform_func):
    """Process multiple CSVs and combine"""
    dfs = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(input_dir, filename))
            df = transform_func(df)
            dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_csv(output_file, index=False)
    print(f"Processed {len(dfs)} files into {output_file}")
```

**Data Pipeline:**
```python
def create_pipeline(steps):
    """Create reusable data pipeline"""
    def pipeline(data):
        result = data
        for step in steps:
            result = step(result)
        return result
    return pipeline

# Example usage:
pipeline = create_pipeline([
    lambda x: x.dropna(),
    lambda x: x.drop_duplicates(),
    lambda x: x[x['value'] > 0],
    lambda x: x.sort_values('date')
])

clean_data = pipeline(raw_data)
```

### 3. API Operations

**Rate-Limited API Client:**
```python
import time
from functools import wraps

def rate_limit(calls_per_second=2):
    """Decorator to rate limit API calls"""
    min_interval = 1.0 / calls_per_second
    last_call = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(2)  # 2 calls per second
def api_call(endpoint, data):
    return requests.post(endpoint, json=data)
```

**Batch API Calls:**
```python
def batch_api_calls(items, endpoint, batch_size=100):
    """Process API calls in batches"""
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        # Process batch
        response = requests.post(endpoint, json={'items': batch})
        
        if response.status_code == 200:
            results.extend(response.json())
        else:
            print(f"Batch {i//batch_size} failed: {response.status_code}")
        
        time.sleep(1)  # Rate limiting
    
    return results
```

**Retry with Backoff:**
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry failed calls with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt) + random.random()
            print(f"Retry {attempt + 1}/{max_retries} in {delay:.1f}s: {e}")
            time.sleep(delay)
```

### 4. Scheduled Tasks

**Cron Jobs:**
```bash
# Every hour
0 * * * * /path/to/script.sh

# Every day at 9 AM
0 9 * * * /path/to/script.sh

# Every Monday at 9 AM
0 9 * * 1 /path/to/script.sh

# Every hour on weekdays
0 * * * 1-5 /path/to/script.sh
```

**Python Scheduler:**
```python
import schedule
import time

def job():
    print("Running scheduled task...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("09:00").do(job)
schedule.every().monday.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

**OpenClaw Cron:**
```bash
openclaw cron add \
  --name "Daily Report" \
  --schedule "0 9 * * *" \
  --task "Generate daily report and send to slack"
```

## Workflow Patterns

### Sequential Pipeline

```python
def sequential_workflow(steps):
    """Run steps in sequence"""
    results = []
    
    for i, step in enumerate(steps):
        try:
            result = step['action'](**step.get('params', {}))
            results.append({'step': i, 'status': 'success', 'result': result})
        except Exception as e:
            results.append({'step': i, 'status': 'error', 'error': str(e)})
            if step.get('stop_on_error', True):
                break
    
    return results
```

### Parallel Execution

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def parallel_workflow(tasks, max_workers=5):
    """Run tasks in parallel"""
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(task['action'], **task.get('params', {})): task 
                   for task in tasks}
        
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                results.append({'task': task['name'], 'status': 'success', 'result': result})
            except Exception as e:
                results.append({'task': task['name'], 'status': 'error', 'error': str(e)})
    
    return results
```

### Conditional Workflow

```python
def conditional_workflow(steps):
    """Run steps based on conditions"""
    context = {}
    
    for step in steps:
        # Check condition
        if 'condition' in step:
            if not step['condition'](context):
                print(f"Skipping {step['name']}: condition not met")
                continue
        
        # Execute step
        result = step['action'](**step.get('params', {}), context=context)
        context[step['name']] = result
    
    return context
```

## Error Handling

### Graceful Degradation

```python
def robust_operation(data, fallback=None):
    """Try operation with fallback"""
    try:
        return primary_operation(data)
    except SpecificError as e:
        print(f"Primary failed: {e}, trying fallback")
        return fallback_operation(data) if fallback else None
    except Exception as e:
        print(f"All options failed: {e}")
        return fallback
```

### Error Notification

```python
def notify_on_error(func, notify_func):
    """Decorator to notify on errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            notify_func(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

@notify_on_error(send_slack_message)
def important_operation():
    # ...
```

## Monitoring

### Progress Tracking

```python
from tqdm import tqdm

def process_with_progress(items):
    """Process items with progress bar"""
    results = []
    for item in tqdm(items, desc="Processing"):
        results.append(process(item))
    return results
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='automation.log'
)

logger = logging.getLogger(__name__)

def logged_operation(data):
    logger.info(f"Starting operation with {len(data)} items")
    try:
        result = process(data)
        logger.info(f"Operation completed: {len(result)} results")
        return result
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise
```

## Best Practices

### 1. Start Simple

```
Manual → Script → Scheduled → Monitored
```

Don't over-engineer. Start with a manual process, then automate.

### 2. Make Idempotent

```python
def safe_operation(data):
    """Can be run multiple times safely"""
    # Check if already done
    if already_processed(data):
        return get_cached_result(data)
    
    # Process
    result = process(data)
    
    # Mark as done
    mark_processed(data)
    
    return result
```

### 3. Add Checkpoints

```python
def long_running_workflow(data):
    """Save progress at checkpoints"""
    checkpoint_file = "workflow_checkpoint.json"
    
    # Load checkpoint if exists
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file) as f:
            state = json.load(f)
            start_from = state['step']
            data = state['data']
    else:
        start_from = 0
    
    # Process with checkpoints
    for i, step in enumerate(steps[start_from:], start=start_from):
        result = step(data)
        
        # Save checkpoint
        with open(checkpoint_file, 'w') as f:
            json.dump({'step': i + 1, 'data': result}, f)
    
    # Clean up
    os.remove(checkpoint_file)
    return result
```

### 4. Test Thoroughly

```python
def test_automation():
    """Test automation with mock data"""
    test_data = create_mock_data()
    
    # Dry run
    result = automation(test_data, dry_run=True)
    
    # Validate
    assert result['status'] == 'success'
    assert len(result['output']) == expected_count
    
    print("All tests passed!")
```

### 5. Document Everything

```python
def automated_task(config):
    """
    Process daily sales data and generate report.
    
    Args:
        config: Dict with keys:
            - input_dir: Directory with CSV files
            - output_file: Path for output report
            - notify: Email to notify on completion
    
    Returns:
        Dict with keys:
            - status: 'success' or 'error'
            - records_processed: Number of records
            - output_file: Path to generated report
    
    Example:
        result = automated_task({
            'input_dir': '/data/sales',
            'output_file': '/reports/daily.csv',
            'notify': 'team@company.com'
        })
    """
    # Implementation...
```

## Common Use Cases

### Daily Report Automation

```python
def daily_report():
    # 1. Fetch data
    data = fetch_from_sources()
    
    # 2. Process
    processed = process_data(data)
    
    # 3. Generate report
    report = generate_report(processed)
    
    # 4. Distribute
    send_email(report)
    upload_to_slack(report)
    
    # 5. Archive
    archive_report(report)
```

### Data Synchronization

```python
def sync_data():
    # 1. Get last sync state
    last_sync = get_last_sync_time()
    
    # 2. Fetch changes
    changes = fetch_changes_since(last_sync)
    
    # 3. Apply changes
    for change in changes:
        apply_change(change)
    
    # 4. Update sync state
    update_sync_time()
```

### Cleanup Automation

```python
def cleanup():
    # 1. Remove old files
    remove_old_files(days=30)
    
    # 2. Clear temp directories
    clear_temp_dirs()
    
    # 3. Archive old logs
    archive_logs()
    
    # 4. Optimize database
    optimize_database()
```
