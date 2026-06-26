import os
import argparse
import base64
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
from urllib.parse import urljoin, urlparse

def get_image_data(url):
    """Download image, handle some basic retries or headers."""
    try:
        # WeChat requires generic headers or sometimes no referer
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
        }
        if url.startswith('//'):
            url = 'https:' + url
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        content_type = response.headers.get('content-type', 'image/jpeg')
        # Some URLs don't have extension, infer from content-type
        ext = 'jpg'
        if 'png' in content_type: ext = 'png'
        elif 'gif' in content_type: ext = 'gif'
        elif 'webp' in content_type: ext = 'webp'
        elif 'svg' in content_type: ext = 'svg'
        
        return {
            'content': response.content,
            'content_type': content_type,
            'ext': ext,
            'url': url
        }
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return None

def base64_encode_image(img_data):
    if not img_data:
        return ""
    b64_data = base64.b64encode(img_data['content']).decode('utf-8')
    return f"data:{img_data['content_type']};base64,{b64_data}"

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def save_html_to_pdf(html_path, pdf_path):
    print(f"\nGenerating PDF... (this may take a few seconds)")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            abs_path = os.path.abspath(html_path)
            file_url = f"file://{abs_path}"
            
            page.goto(file_url, wait_until="networkidle")
            # Give extra time for fonts/styles to render
            page.wait_for_timeout(1000)
            
            page.pdf(
                path=pdf_path, 
                format="A4", 
                print_background=True,
                margin={"top": "40px", "bottom": "40px", "left": "20px", "right": "20px"}
            )
            browser.close()
            print(f"=> Saved PDF to: {pdf_path}")
    except ImportError:
        print("\nSkipping PDF generation. 'playwright' is not installed.")
        print("To enable PDF, run: pip install playwright && playwright install chromium")
    except Exception as e:
        print(f"\nError generating PDF: {e}")

def process_article(url, output_dir="."):
    print(f"Fetching: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    # Try to find WeChat title first, then generic
    title_element = soup.find('h1', class_='rich_media_title') or \
                    soup.find('h2', class_='rich_media_title') or \
                    soup.find('title')
                    
    title_text = title_element.text.strip() if title_element else "Untitled_Article"
    title_text = re.sub(r'\s+', ' ', title_text)
    safe_title = sanitize_filename(title_text)
    if not safe_title:
        safe_title = "WeChat_Article"
        
    print(f"Title: {title_text}")

    # Find the main content. WeChat uses div#js_content
    content_element = soup.find('div', id='js_content')
    if not content_element:
        print("Warning: Could not find 'js_content', falling back to body. (Maybe not a WeChat article)")
        content_element = soup.find('body')
        
    if not content_element:
        print("Error: Could not find any content to parse.")
        return

    # Create clones for HTML and Markdown processing
    import copy
    html_soup = copy.copy(soup)
    html_content = html_soup.find('div', id='js_content') or html_soup.find('body')
    
    md_soup = copy.copy(soup)
    md_content = md_soup.find('div', id='js_content') or md_soup.find('body')

    # Create assets directory for markdown
    assets_dir_name = f"{safe_title}_assets"
    assets_dir_path = os.path.join(output_dir, assets_dir_name)
    os.makedirs(assets_dir_path, exist_ok=True)

    img_tags_html = html_content.find_all('img')
    img_tags_md = md_content.find_all('img')

    total_imgs = len(img_tags_html)
    print(f"Found {total_imgs} images. Downloading...")

    # Both HTML and MD images need to be processed.
    # To save bandwidth, we download once, then apply to both.
    for i in range(total_imgs):
        html_img = img_tags_html[i]
        md_img = img_tags_md[i] if i < len(img_tags_md) else None

        # WeChat lazy loads images using data-src
        src = html_img.get('data-src') or html_img.get('src')
        if not src:
            continue
            
        print(f"[{i+1}/{total_imgs}] Downloading...")
        img_data = get_image_data(src)
        
        if img_data:
            # 1. For HTML: Use Base64 inline
            b64_url = base64_encode_image(img_data)
            html_img['src'] = b64_url
            if html_img.has_attr('data-src'):
                del html_img['data-src']
            
            # 2. For Markdown: Save to local folder and link
            img_filename = f"img_{i:03d}.{img_data['ext']}"
            img_filepath = os.path.join(assets_dir_path, img_filename)
            with open(img_filepath, 'wb') as f:
                f.write(img_data['content'])
            
            if md_img:
                md_img['src'] = os.path.join(assets_dir_name, img_filename)
                if md_img.has_attr('data-src'):
                    del md_img['data-src']
        else:
            # Fallback for HTML
            html_img['src'] = src
            if md_img:
                md_img['src'] = src

    # Also check for background-images (can be inline style)
    # This is a bit complex to do perfectly for both without splitting, but let's do HTML at least.
    sections_html = html_content.find_all(style=re.compile(r'background-image:\s*url'))
    for section in sections_html:
        style = section.get('style')
        match = re.search(r'url\([\'"]?(.*?)[\'"]?\)', style)
        if match:
            bg_url = match.group(1)
            # Basic protocol fix
            if bg_url.startswith('//'): bg_url = 'https:' + bg_url
            if not bg_url.startswith('http'): continue
            
            img_data = get_image_data(bg_url)
            if img_data:
                b64_bg = base64_encode_image(img_data)
                section['style'] = style.replace(bg_url, b64_bg)

    # --- Save HTML ---
    # Add a simple wrapper around HTML so it looks decent
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title_text}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fafafa;
            }}
            #content-wrapper {{
                background-color: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
            img {{
                max-width: 100%;
                height: auto !important;
                display: block;
                margin: 10px auto;
            }}
            /* Force visibility for elements hidden by WeChat JS */
            #js_content {{
                visibility: visible !important;
                opacity: 1 !important;
                height: auto !important;
            }}
            .rich_media_content {{
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div id="content-wrapper">
            <h1>{title_text}</h1>
            {str(html_content)}
        </div>
    </body>
    </html>
    """
    
    html_output_path = os.path.join(output_dir, f"{safe_title}.html")
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"\n=> Saved single-file HTML to: {html_output_path}")

    # --- Save PDF ---
    pdf_output_path = os.path.join(output_dir, f"{safe_title}.pdf")
    save_html_to_pdf(html_output_path, pdf_output_path)

    # --- Save Markdown ---
    try:
        md_text = md(str(md_content), heading_style="ATX", default_title=True)
        md_output_path = os.path.join(output_dir, f"{safe_title}.md")
        with open(md_output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title_text}\n\n{md_text}")
        print(f"=> Saved Markdown to: {md_output_path}")
        print(f"=> Markdown images saved in: {assets_dir_path}/")
    except Exception as e:
        print(f"Error generating Markdown: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert article to offline HTML and Markdown.")
    parser.add_argument("url", help="Target URL (e.g. WeChat article URL)")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    args = parser.parse_args()
    
    process_article(args.url, args.output)
