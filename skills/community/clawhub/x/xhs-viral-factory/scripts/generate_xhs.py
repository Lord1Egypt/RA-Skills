import os
import argparse
import datetime
import json
import requests
import sys

def generate_xhs_note(source_path, style_ref, history_path, api_key, base_url, model_name):
    """
    Universal XHS Content Generator (OpenAI Compatible)
    """
    # 1. Load style patterns
    try:
        with open(style_ref, 'r', encoding='utf-8') as f:
            styles = f.read()
    except Exception:
        styles = "Use catchy titles and many emojis."

    # 2. Load source material
    source_content = ""
    if os.path.isfile(source_path):
        with open(source_path, 'r', encoding='utf-8') as f:
            source_content = f.read()[:8000]
    elif os.path.isdir(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if file.endswith(('.md', '.txt')):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        source_content += f.read()[:2000] + "\n"
                if len(source_content) > 12000: break

    # 3. Load publishing history (optional)
    history = ""
    if history_path and os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as f:
            history = f.read()[-3000:]

    # 4. Construct AI System Prompt
    prompt = f"""
You are an expert Xiaohongshu (XHS) social media manager.
Based on the provided SOURCE MATERIAL, generate a high-conversion XHS post.

[STYLE PATTERN LIBRARY]
{styles}

[SOURCE MATERIAL]
{source_content}

[HISTORY (To avoid duplicates)]
{history}

[REQUIREMENTS]
1. Title must be catchy with emojis.
2. Body should be 400-800 words, short paragraphs, rich in emojis.
3. No Markdown symbols (*, #, -, .) - use emojis for lists.
4. Provide 3 Image Generation Prompts at the end.
5. Include 5-8 relevant tags.

[OUTPUT FORMAT]
Title: ...
Body: ...
Image Prompts: ...
Tags: ...
"""

    # 5. Execute API Call
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    url = base_url.rstrip('/') + "/chat/completions"
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a professional social media manager specializing in Xiaohongshu (XHS). Output in Chinese language."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: LLM API request failed. Details: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal XHS Viral Factory")
    parser.add_argument("--source", required=True, help="Path to your knowledge source folder/file")
    parser.add_argument("--output", default="./drafts", help="Output directory for drafts")
    parser.add_argument("--history", help="Path to your previous post history file")
    
    args = parser.parse_args()

    # Environment variables handling (Declared in SKILL.md)
    API_KEY = os.getenv("LLM_API_KEY")
    BASE_URL = os.getenv("LLM_BASE_URL") or "https://api.openai.com/v1"
    MODEL = os.getenv("LLM_MODEL") or "gpt-4o"

    if not API_KEY:
        print("CRITICAL ERROR: LLM_API_KEY is missing. Please set it in your environment.")
        sys.exit(1)

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    style_ref = os.path.join(script_dir, "../references/prompt_patterns.md")
    
    print(f"Status: Generating draft using model [{MODEL}] via endpoint [{BASE_URL}]...")
    
    content = generate_xhs_note(args.source, style_ref, args.history, API_KEY, BASE_URL, MODEL)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(args.output, f"xhs_draft_{timestamp}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Success: Content generated successfully. Saved to: {output_file}")
