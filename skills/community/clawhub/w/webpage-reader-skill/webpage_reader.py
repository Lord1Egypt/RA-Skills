#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Skill: Webpage Downloader

This skill downloads webpage content using Google Chrome headless browser.
"""

import os
import sys
import subprocess
import platform
import logging
import tempfile
import shutil
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('webpage_downloader')

def check_chrome_installed() -> bool:
    """
    Check if Google Chrome is installed on the system.
    
    Returns:
        bool: True if Chrome is installed, False otherwise
    """
    try:
        if platform.system() == 'Windows':
            # Check common Chrome paths on Windows
            chrome_paths = [
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'Application', 'chrome.exe')
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    logger.info(f"Chrome found at: {path}")
                    return True
            return False
        else:
            # For macOS and Linux, use which command
            result = subprocess.run(
                ['which', 'google-chrome'] if platform.system() != 'Darwin' else ['which', 'chrome'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info(f"Chrome found at: {result.stdout.strip()}")
                return True
            return False
    except Exception as e:
        logger.error(f"Error checking Chrome installation: {e}")
        return False

def install_chrome() -> bool:
    """
    Install Google Chrome based on the operating system.
    
    Returns:
        bool: True if installation successful, False otherwise
    """
    try:
        system = platform.system()
        logger.info(f"Installing Chrome on {system}")
        
        if system == 'Windows':
            # Windows installation logic
            logger.info("Please manually download and install Chrome from: https://www.google.com/chrome/")
            return False
        elif system == 'Darwin':  # macOS
            # macOS installation using Homebrew
            try:
                subprocess.run(['brew', 'install', 'google-chrome'], check=True)
                return True
            except subprocess.CalledProcessError:
                logger.error("Homebrew not found. Please install Homebrew first or manually install Chrome.")
                return False
        elif system == 'Linux':
            # Linux installation
            distro = platform.dist()[0].lower() if hasattr(platform, 'dist') else 'unknown'
            
            if 'ubuntu' in distro or 'debian' in distro:
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'google-chrome-stable'], check=True)
                return True
            elif 'fedora' in distro or 'centos' in distro or 'rhel' in distro:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'google-chrome-stable'], check=True)
                return True
            else:
                logger.error("Unsupported Linux distribution. Please manually install Chrome.")
                return False
        else:
            logger.error(f"Unsupported operating system: {system}")
            return False
    except Exception as e:
        logger.error(f"Error installing Chrome: {e}")
        return False

def download_webpage(url: str, output_file: str) -> bool:
    """
    Download webpage content using Chrome headless browser.
    
    Args:
        url: The URL to download
        output_file: The file to save the output
    
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        # Build the Chrome command
        chrome_cmd = [
            'google-chrome' if platform.system() != 'Windows' else 'chrome',
            '--headless=new',
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--virtual-time-budget=8000',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
            '--hide-scrollbars',
            '--blink-settings=imagesEnabled=true',
            '--dump-dom',
            url
        ]
        
        logger.info(f"Running Chrome command: {' '.join(chrome_cmd)}")
        
        # Execute the command and capture output
        result = subprocess.run(
            chrome_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"Chrome command failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            return False
        
        # Write the output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        
        logger.info(f"Webpage downloaded successfully to {output_file}")
        return True
    except subprocess.TimeoutExpired:
        logger.error("Chrome command timed out")
        return False
    except Exception as e:
        logger.error(f"Error downloading webpage: {e}")
        return False

def read_webpage_content(file_path: str) -> Optional[str]:
    """
    Read the content of the downloaded webpage.
    
    Args:
        file_path: Path to the HTML file
    
    Returns:
        Optional[str]: The content of the file, or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Read {len(content)} characters from {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None

def summarize_content(content: str) -> str:
    """
    Generate a simple summary of the webpage content.
    
    Args:
        content: The HTML content
    
    Returns:
        str: Summary of the content
    """
    # Simple summary - count characters and find title if present
    import re
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "No title found"
    
    # Count content length
    content_length = len(content)
    
    # Count paragraphs
    paragraph_count = len(re.findall(r'<p[^>]*>', content, re.IGNORECASE))
    
    summary = f"Webpage Summary:\n"
    summary += f"Title: {title}\n"
    summary += f"Content length: {content_length} characters\n"
    summary += f"Paragraph count: {paragraph_count}\n"
    summary += "\nNote: This is a basic summary. For detailed analysis, please review the full content."
    
    return summary

def main(url: str) -> Dict[str, Any]:
    """
    Main function to download and process webpage.
    
    Args:
        url: The URL to process
    
    Returns:
        Dict[str, Any]: Result containing status and content
    """
    result = {
        'success': False,
        'message': '',
        'content': None,
        'summary': None
    }
    
    try:
        # Check if Chrome is installed
        if not check_chrome_installed():
            logger.info("Chrome not found, attempting to install...")
            if not install_chrome():
                result['message'] = "Chrome installation failed. Please install Chrome manually."
                return result
        
        # Create temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, 'url.html')
            
            # Download webpage
            if not download_webpage(url, output_file):
                result['message'] = "Failed to download webpage"
                return result
            
            # Read content
            content = read_webpage_content(output_file)
            if not content:
                result['message'] = "Failed to read webpage content"
                return result
            
            # Generate summary
            summary = summarize_content(content)
            
            # Set result
            result['success'] = True
            result['message'] = "Webpage downloaded and processed successfully"
            result['content'] = content
            result['summary'] = summary
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        result['message'] = f"An unexpected error occurred: {str(e)}"
    
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python webpage_reader.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = main(url)
    
    if result['success']:
        print("Success!")
        print(result['summary'])
        print("\nFull content saved to url.html (temporary file)")
    else:
        print(f"Error: {result['message']}")
        sys.exit(1)