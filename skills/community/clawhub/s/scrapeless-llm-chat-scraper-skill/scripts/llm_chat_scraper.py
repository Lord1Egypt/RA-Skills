#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Chat Scraper Tool for OpenClaw

Scrape AI chat conversations from ChatGPT, Gemini, Perplexity, Copilot, Google AI Mode, and Grok.
"""

import os
import sys
import time
import json
import argparse
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

try:
    import requests
except ImportError:
    print(json.dumps({
        'error': 'Missing dependency',
        'message': 'requests library not found. Please install it: pip install requests'
    }), file=sys.stderr)
    sys.exit(1)


class LLMChatScraper:
    """LLM Chat Scraper for Scrapeless API"""
    
    SUPPORTED_ACTORS = [
        'scraper.chatgpt',
        'scraper.gemini',
        'scraper.perplexity',
        'scraper.copilot',
        'scraper.aimode',
        'scraper.grok'
    ]
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv('X_API_TOKEN')
        if not self.api_token:
            raise ValueError(
                "API token not found. Please set X_API_TOKEN in .env file or environment variable."
            )
        
        self.api_base_url = 'https://api.scrapeless.com'
        self.request_endpoint = '/api/v2/scraper/request'
        self.result_endpoint = '/api/v2/scraper/result'
        
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-token': self.api_token
        }
        
        logger.info(f"LLMChatScraper initialized with API base URL: {self.api_base_url}")
    
    def _validate_actor(self, actor: str) -> bool:
        return actor in self.SUPPORTED_ACTORS
    
    def _build_request_payload(
        self,
        actor: str,
        prompt: str,
        country: str,
        web_search: bool = False,
        mode: Optional[str] = None
    ) -> Dict[str, Any]:
        input_params = {
            'prompt': prompt,
            'country': country
        }
        
        if actor in ['scraper.chatgpt', 'scraper.perplexity']:
            input_params['web_search'] = web_search
        
        if actor == 'scraper.copilot':
            input_params['mode'] = mode or 'search'
        
        if actor == 'scraper.grok':
            input_params['mode'] = mode or 'MODEL_MODE_AUTO'
        
        return {
            'actor': actor,
            'input': input_params,
            'webhook': {'url': ''}
        }
    
    def create_task(
        self,
        actor: str,
        prompt: str,
        country: str,
        web_search: bool = False,
        mode: Optional[str] = None
    ) -> str:
        if not self._validate_actor(actor):
            raise ValueError(f"Unsupported actor: {actor}. Supported: {', '.join(self.SUPPORTED_ACTORS)}")
        
        logger.info(f"Creating task for {actor} with prompt: {prompt[:50]}...")
        
        payload = self._build_request_payload(
            actor=actor,
            prompt=prompt,
            country=country,
            web_search=web_search,
            mode=mode
        )
        
        response = requests.post(
            f"{self.api_base_url}{self.request_endpoint}",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            task_id = result.get('task_id')
            if not task_id:
                raise RuntimeError("No task_id in response")
            logger.info(f"Task created successfully with ID: {task_id}")
            return task_id
        elif response.status_code == 400:
            raise ValueError(f"Invalid request: {response.json()}")
        elif response.status_code == 429:
            raise RuntimeError("Rate limit exceeded")
        else:
            raise RuntimeError(f"Unexpected status code {response.status_code}: {response.text}")
    
    def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        response = requests.get(
            f"{self.api_base_url}{self.result_endpoint}/{task_id}",
            headers=self.headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status')
            
            if status == 'success':
                return result
            elif status in ['pending', 'running']:
                return None
            elif status == 'failed':
                raise RuntimeError(f"Task failed: {result.get('message', 'Unknown error')}")
        elif response.status_code == 202:
            return None
        elif response.status_code == 410:
            raise RuntimeError("Task result has expired")
        elif response.status_code == 404:
            raise RuntimeError(f"Task not found: {task_id}")
        else:
            raise RuntimeError(f"Unexpected status code {response.status_code}")
        
        return None
    
    def poll_for_result(
        self,
        task_id: str,
        interval: int = 10,
        max_retries: int = 30
    ) -> Dict[str, Any]:
        logger.info(f"Polling for task {task_id} with {max_retries} max retries")
        
        for attempt in range(1, max_retries + 1):
            logger.debug(f"Attempt {attempt}/{max_retries} for task {task_id}")
            result = self.get_task_result(task_id)
            
            if result is not None:
                logger.info(f"Task {task_id} completed successfully")
                return {
                    'success': True,
                    'data': result.get('task_result', {}),
                    'status': result.get('status', 'success'),
                    'task_id': task_id
                }
            
            if attempt < max_retries:
                logger.debug(f"Task {task_id} still pending, waiting {interval} seconds")
                time.sleep(interval)
        
        raise TimeoutError(
            f"Task did not complete after {max_retries} attempts. "
            f"You can manually retrieve the result using:\n"
            f"curl --request GET '{self.api_base_url}{self.result_endpoint}/{task_id}' \\\n"
            f"  --header 'Content-Type: application/json' \\\n"
            f"  --header 'x-api-token: REDACTED'"
        )
    
    def execute(
        self,
        actor: str,
        prompt: str,
        country: str = 'US',
        web_search: bool = False,
        mode: Optional[str] = None,
        poll_interval: int = 10,
        max_retries: int = 30
    ) -> Dict[str, Any]:
        try:
            task_id = self.create_task(
                actor=actor,
                prompt=prompt,
                country=country,
                web_search=web_search,
                mode=mode
            )
            
            return self.poll_for_result(
                task_id=task_id,
                interval=poll_interval,
                max_retries=max_retries
            )
            
        except Exception as e:
            return {
                'success': False,
                'error': type(e).__name__,
                'message': str(e)
            }


def main():
    parser = argparse.ArgumentParser(
        description='LLM Chat Scraper Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 llm_chat_scraper.py chatgpt --query "AI trends"
  python3 llm_chat_scraper.py gemini --query "Best restaurants" --country US
  python3 llm_chat_scraper.py perplexity --query "Latest news" --web-search
  python3 llm_chat_scraper.py copilot --query "Explain ML" --mode reasoning
  python3 llm_chat_scraper.py aimode --query "Programming tips"
  python3 llm_chat_scraper.py grok --query "Quantum physics" --mode MODEL_MODE_EXPERT
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # ChatGPT command
    chatgpt_parser = subparsers.add_parser('chatgpt', help='Scrape ChatGPT responses')
    chatgpt_parser.add_argument('--query', required=True, help='Prompt to send to ChatGPT')
    chatgpt_parser.add_argument('--country', default='US', help='Country code (default: US)')
    chatgpt_parser.add_argument('--web-search', action='store_true', help='Enable web search')
    chatgpt_parser.add_argument('--poll-interval', type=int, default=10, help='Polling interval in seconds')
    chatgpt_parser.add_argument('--max-retries', type=int, default=30, help='Maximum retries')
    
    # Gemini command
    gemini_parser = subparsers.add_parser('gemini', help='Scrape Gemini responses')
    gemini_parser.add_argument('--query', required=True, help='Prompt to send to Gemini')
    gemini_parser.add_argument('--country', default='US', help='Country code (default: US)')
    gemini_parser.add_argument('--poll-interval', type=int, default=10, help='Polling interval in seconds')
    gemini_parser.add_argument('--max-retries', type=int, default=30, help='Maximum retries')
    
    # Perplexity command
    perplexity_parser = subparsers.add_parser('perplexity', help='Scrape Perplexity responses')
    perplexity_parser.add_argument('--query', required=True, help='Prompt to send to Perplexity')
    perplexity_parser.add_argument('--country', default='US', help='Country code (default: US)')
    perplexity_parser.add_argument('--web-search', action='store_true', help='Enable web search')
    perplexity_parser.add_argument('--poll-interval', type=int, default=10, help='Polling interval in seconds')
    perplexity_parser.add_argument('--max-retries', type=int, default=30, help='Maximum retries')
    
    # Copilot command
    copilot_parser = subparsers.add_parser('copilot', help='Scrape Copilot responses')
    copilot_parser.add_argument('--query', required=True, help='Prompt to send to Copilot')
    copilot_parser.add_argument('--country', default='US', help='Country code (default: US)')
    copilot_parser.add_argument('--mode', default='search', choices=['search', 'smart', 'chat', 'reasoning', 'study'], help='Mode (default: search)')
    copilot_parser.add_argument('--poll-interval', type=int, default=10, help='Polling interval in seconds')
    copilot_parser.add_argument('--max-retries', type=int, default=30, help='Maximum retries')
    
    # Google AI Mode command
    aimode_parser = subparsers.add_parser('aimode', help='Scrape Google AI Mode responses')
    aimode_parser.add_argument('--query', required=True, help='Prompt to send to Google AI Mode')
    aimode_parser.add_argument('--country', default='US', help='Country code (default: US)')
    aimode_parser.add_argument('--poll-interval', type=int, default=10, help='Polling interval in seconds')
    aimode_parser.add_argument('--max-retries', type=int, default=30, help='Maximum retries')
    
    # Grok command
    grok_parser = subparsers.add_parser('grok', help='Scrape Grok responses')
    grok_parser.add_argument('--query', required=True, help='Prompt to send to Grok')
    grok_parser.add_argument('--country', default='US', help='Country code (default: US)')
    grok_parser.add_argument('--mode', default='MODEL_MODE_AUTO', choices=['MODEL_MODE_FAST', 'MODEL_MODE_EXPERT', 'MODEL_MODE_AUTO'], help='Mode (default: MODEL_MODE_AUTO)')
    grok_parser.add_argument('--poll-interval', type=int, default=10, help='Polling interval in seconds')
    grok_parser.add_argument('--max-retries', type=int, default=30, help='Maximum retries')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        scraper = LLMChatScraper()
        
        if args.command == 'chatgpt':
            result = scraper.execute(
                actor='scraper.chatgpt',
                prompt=args.query,
                country=args.country,
                web_search=args.web_search,
                poll_interval=args.poll_interval,
                max_retries=args.max_retries
            )
        elif args.command == 'gemini':
            result = scraper.execute(
                actor='scraper.gemini',
                prompt=args.query,
                country=args.country,
                poll_interval=args.poll_interval,
                max_retries=args.max_retries
            )
        elif args.command == 'perplexity':
            result = scraper.execute(
                actor='scraper.perplexity',
                prompt=args.query,
                country=args.country,
                web_search=args.web_search,
                poll_interval=args.poll_interval,
                max_retries=args.max_retries
            )
        elif args.command == 'copilot':
            result = scraper.execute(
                actor='scraper.copilot',
                prompt=args.query,
                country=args.country,
                mode=args.mode,
                poll_interval=args.poll_interval,
                max_retries=args.max_retries
            )
        elif args.command == 'aimode':
            result = scraper.execute(
                actor='scraper.aimode',
                prompt=args.query,
                country=args.country,
                poll_interval=args.poll_interval,
                max_retries=args.max_retries
            )
        elif args.command == 'grok':
            result = scraper.execute(
                actor='scraper.grok',
                prompt=args.query,
                country=args.country,
                mode=args.mode,
                poll_interval=args.poll_interval,
                max_retries=args.max_retries
            )
        
        # Output result as JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Exit with error code if failed
        if not result.get('success'):
            sys.exit(1)
            
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': type(e).__name__,
            'message': str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


def scrape_llm_chat(
    prompt: str,
    actor: str = 'scraper.chatgpt',
    country: str = 'US',
    web_search: bool = False,
    mode: Optional[str] = None,
    poll_interval: int = 10,
    max_retries: int = 30,
    api_token: Optional[str] = None
) -> Dict[str, Any]:
    """Scrape LLM chat responses from various AI models
    
    Args:
        prompt: Prompt to send to the AI
        actor: Scraper to use (e.g., 'scraper.gemini')
        country: Country code (default: US)
        web_search: Whether to enable web search (default: False)
        mode: Special mode for certain scrapers (e.g., 'search' for copilot)
        poll_interval: Polling interval in seconds (default: 10)
        max_retries: Maximum retries (default: 30)
        api_token: API token for Scrapeless API
    
    Returns:
        Dict with success status and result data
    """
    scraper = LLMChatScraper(api_token=api_token)
    return scraper.execute(
        actor=actor,
        prompt=prompt,
        country=country,
        web_search=web_search,
        mode=mode,
        poll_interval=poll_interval,
        max_retries=max_retries
    )


if __name__ == '__main__':
    main()
