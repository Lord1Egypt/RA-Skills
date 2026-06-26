#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ezviz Restaurant Inspection Skill
萤石餐厅巡检技能 - 自动智能体管理 + 设备抓图 + AI分析

Usage:
    python3 restaurant_inspection.py [app_key] [app_secret] [device_serial] [channel_no]

Environment Variables (alternative to command line args):
    EZVIZ_APP_KEY, EZVIZ_APP_SECRET, EZVIZ_DEVICE_SERIAL, EZVIZ_CHANNEL_NO
"""

import os
import sys
import time
import json
import requests
from datetime import datetime, timedelta

# Default values
DEFAULT_CHANNEL_NO = "1"
DEFAULT_ANALYSIS_TEXT = "请分析这张照片"
TEMPLATE_ID = "f4c255b2929e463d86e9"  # 餐厅行业通用模板ID

# Production environment domains (online)
TOKEN_CAPTURE_URL = "https://open.ys7.com/api/lapp/token/get"
CAPTURE_URL = "https://open.ys7.com/api/lapp/device/capture"
AGENT_LIST_URL = "https://open.ys7.com/api/service/open/intelligent/agent/app/list"
AGENT_COPY_URL = "https://open.ys7.com/api/service/open/intelligent/agent/template/copy"
ANALYSIS_URL = "https://aidialoggw.ys7.com/api/service/open/intelligent/agent/engine/agent/anaylsis"
ENV_NAME = "Production Environment (Online)"

def get_env_or_arg(env_var, arg_value, default=None):
    """Get value from environment variable or command line argument"""
    return os.getenv(env_var) or arg_value or default

def get_access_token(app_key, app_secret):
    """Get access token from Ezviz API"""
    print("=" * 70)
    print("[Step 1] Getting access token...")
    
    payload = {
        'appKey': app_key,
        'appSecret': app_secret
    }
    
    try:
        response = requests.post(TOKEN_CAPTURE_URL, data=payload, timeout=10)
        result = response.json()
        
        if result.get('code') == '200':
            token = result['data']['accessToken']
            expire_time = datetime.now() + timedelta(days=7)
            print(f"[SUCCESS] Token obtained, expires: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
            return token
        else:
            print(f"[ERROR] Failed to get token: {result.get('msg', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when getting token: {str(e)}")
        return None

def get_agent_list(access_token):
    """Get user's intelligent agent list - prioritize '餐厅行业通用智能体'"""
    print("=" * 70)
    print("[Step 2] Checking existing intelligent agents...")
    
    params = {
        '_r': '0.6149525825375246',
        'appType': '1',
        'pageStart': '0',
        'pageSize': '100'  # Increased to get more agents
    }
    
    headers = {
        'accessToken': access_token
    }
    
    try:
        response = requests.get(AGENT_LIST_URL, params=params, headers=headers, timeout=30)
        result = response.json()
        
        agents = []
        # Handle both response formats
        if 'data' in result:
            if isinstance(result['data'], dict) and 'appList' in result['data']:
                agents = result['data']['appList']
            elif isinstance(result['data'], list):
                agents = result['data']
        
        if agents:
            print(f"[INFO] Found {len(agents)} agents total")
            
            # Priority 1: Look for exact match "餐厅行业通用智能体"
            for agent in agents:
                agent_name = agent.get('appName', '')
                if '餐厅行业通用智能体' in agent_name:
                    agent_id = agent.get('appId')
                    app_status = agent.get('appStatus', 0)
                    status_text = 'Published' if app_status == 1 else 'Draft'
                    print(f"[INFO] Found '餐厅行业通用智能体': {agent_id} ({agent_name}) [{status_text}]")
                    print(f"[SUCCESS] Using existing agent: {agent_id}")
                    return agent_id
            
            # Priority 2: Look for other restaurant-related agents
            for agent in agents:
                agent_name = agent.get('appName', '')
                if '餐厅' in agent_name or '餐饮' in agent_name:
                    agent_id = agent.get('appId')
                    app_status = agent.get('appStatus', 0)
                    status_text = 'Published' if app_status == 1 else 'Draft'
                    print(f"[INFO] Found restaurant-related agent: {agent_id} ({agent_name}) [{status_text}]")
                    print(f"[SUCCESS] Using existing agent: {agent_id}")
                    return agent_id
            
            print("[INFO] No existing restaurant agent found")
            return None
        else:
            print(f"[ERROR] Unexpected response format: {result}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when getting agent list: {str(e)}")
        return None

def copy_agent_template(access_token, template_id):
    """Copy agent template to create new agent"""
    print("[INFO] Creating new restaurant agent from template...")
    
    headers = {
        'accessToken': access_token
    }
    
    data = {
        'templateId': template_id
    }
    
    try:
        response = requests.post(AGENT_COPY_URL, headers=headers, data=data, timeout=60)
        result = response.json()
        
        if 'data' in result:
            new_agent_data = result['data']
            # Handle both string appId and full agent object
            if isinstance(new_agent_data, str):
                new_agent_id = new_agent_data
            elif isinstance(new_agent_data, dict):
                new_agent_id = new_agent_data.get('appId')
                print(f"[INFO] Agent name: {new_agent_data.get('appName', 'Unknown')}")
            else:
                print(f"[ERROR] Unexpected agent data format: {new_agent_data}")
                return None
            print(f"[SUCCESS] New agent created: {new_agent_id}")
            # Wait for agent to be ready
            print("[INFO] Waiting for agent to initialize (5 seconds)...")
            time.sleep(5)
            return new_agent_id
        else:
            print(f"[ERROR] Failed to create agent: {result.get('msg', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when copying agent template: {str(e)}")
        return None

def manage_intelligent_agent(access_token):
    """Manage intelligent agent - check existing or create new"""
    print("=" * 70)
    print("[Step 2] Managing intelligent agent...")
    
    # Check if existing restaurant agent exists
    existing_agent_id = get_agent_list(access_token)
    if existing_agent_id:
        return existing_agent_id
    
    # Create new agent from template
    new_agent_id = copy_agent_template(access_token, TEMPLATE_ID)
    if new_agent_id:
        print(f"[SUCCESS] Using new agent: {new_agent_id}")
        return new_agent_id
    
    print("[ERROR] Failed to manage intelligent agent")
    return None

def capture_image(access_token, device_serial, channel_no):
    """Capture image from device"""
    print(f"\n[Device] {device_serial} (Channel: {channel_no})")
    
    payload = {
        'accessToken': access_token,
        'deviceSerial': device_serial,
        'channelNo': channel_no
    }
    
    try:
        response = requests.post(CAPTURE_URL, data=payload, timeout=30)
        result = response.json()
        
        if result.get('code') == '200':
            pic_url = result['data']['picUrl']
            print(f"[SUCCESS] Image captured: {pic_url[:50]}...")
            return pic_url
        else:
            msg = result.get('msg', 'Unknown error')
            code = result.get('code', 'Unknown')
            print(f"[ERROR] Failed to capture image: Code {code}, Message: {msg}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when capturing image: {str(e)}")
        return None

def analyze_image(access_token, agent_id, pic_url, analysis_text):
    """Analyze image using intelligent agent"""
    headers = {
        'Content-Type': 'application/json',
        'accessToken': access_token
    }
    
    payload = {
        'appId': agent_id,
        'text': analysis_text,
        'mediaType': 'image',
        'dataType': 'url',
        'data': pic_url
    }
    
    try:
        response = requests.post(ANALYSIS_URL, headers=headers, json=payload, timeout=60)
        result = response.json()
        
        if result.get('meta', {}).get('code') == 200:
            analysis_result = result.get('data', {})
            print("[SUCCESS] Analysis completed!")
            return analysis_result
        else:
            msg = result.get('meta', {}).get('message', 'Unknown error')
            code = result.get('meta', {}).get('code', 'Unknown')
            print(f"[ERROR] Failed to analyze image: Code {code}, Message: {msg}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Exception when analyzing image: {str(e)}")
        return None

def parse_device_list(device_serial_str):
    """Parse device serial string with optional channel numbers"""
    devices = []
    for item in device_serial_str.split(','):
        item = item.strip()
        if ':' in item:
            serial, channel = item.split(':', 1)
            devices.append((serial, channel))
        else:
            devices.append((item, DEFAULT_CHANNEL_NO))
    return devices

def main():
    # Parse command line arguments
    app_key = None
    app_secret = None
    device_serial = None
    channel_no = DEFAULT_CHANNEL_NO
    
    if len(sys.argv) >= 4:
        app_key = sys.argv[1]
        app_secret = sys.argv[2]
        device_serial = sys.argv[3]
        if len(sys.argv) >= 5:
            channel_no = sys.argv[4]
    
    # Get from environment variables if not provided
    if not app_key:
        app_key = get_env_or_arg('EZVIZ_APP_KEY', None)
    if not app_secret:
        app_secret = get_env_or_arg('EZVIZ_APP_SECRET', None)
    if not device_serial:
        device_serial = get_env_or_arg('EZVIZ_DEVICE_SERIAL', None)
    if channel_no == DEFAULT_CHANNEL_NO:
        channel_no = get_env_or_arg('EZVIZ_CHANNEL_NO', DEFAULT_CHANNEL_NO)
    
    # Validate required parameters
    if not all([app_key, app_secret, device_serial]):
        print("Error: Missing required parameters!")
        print("Please provide app_key, app_secret, and device_serial")
        print("\nUsage:")
        print("  python3 restaurant_inspection.py app_key app_secret device_serial [channel_no]")
        print("")
        print("  # Environment variables")
        print("  export EZVIZ_APP_KEY=your_key")
        print("  export EZVIZ_APP_SECRET=your_secret")
        print("  export EZVIZ_DEVICE_SERIAL=dev1,dev2")
        print("  python3 restaurant_inspection.py")
        sys.exit(1)
    
    # Parse devices
    devices = parse_device_list(device_serial)
    
    # Print header
    print("=" * 70)
    print("Ezviz Restaurant Inspection Skill (萤石餐厅巡检)")
    print("=" * 70)
    print(f"[Time] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] Environment: {ENV_NAME}")
    print(f"[INFO] Target devices: {len(devices)}")
    for i, (serial, chan) in enumerate(devices, 1):
        print(f" - {serial} (Channel: {chan})")
    
    # Get access token
    access_token = get_access_token(app_key, app_secret)
    if not access_token:
        print("Failed to get access token. Exiting.")
        sys.exit(1)
    
    # Manage intelligent agent
    agent_id = manage_intelligent_agent(access_token)
    if not agent_id:
        print("Failed to manage intelligent agent. Exiting.")
        sys.exit(1)
    
    # Capture and analyze images
    print("\n" + "=" * 70)
    print("[Step 3] Capturing and analyzing images...")
    print("=" * 70)
    
    success_count = 0
    analysis_results = []
    
    for i, (device_serial, channel_no) in enumerate(devices):
        if i > 0:
            time.sleep(4)  # Rate limiting for capture API
        
        # Capture image
        pic_url = capture_image(access_token, device_serial, channel_no)
        if not pic_url:
            continue
        
        # Analyze image
        analysis_result = analyze_image(access_token, agent_id, pic_url, DEFAULT_ANALYSIS_TEXT)
        if analysis_result is not None:
            success_count += 1
            analysis_results.append({
                'device': device_serial,
                'channel': channel_no,
                'result': analysis_result
            })
            print(f"\n[Analysis Result]")
            print(json.dumps(analysis_result, ensure_ascii=False, indent=2))
    
    # Print summary
    print("\n" + "=" * 70)
    print("INSPECTION SUMMARY")
    print("=" * 70)
    print(f" Total devices: {len(devices)}")
    print(f" Success: {success_count}")
    print(f" Failed: {len(devices) - success_count}")
    print(f" Agent ID: {agent_id}")

if __name__ == "__main__":
    main()