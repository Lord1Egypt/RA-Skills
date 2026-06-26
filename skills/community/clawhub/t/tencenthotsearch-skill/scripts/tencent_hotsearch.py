#!/usr/bin/env python3
"""
TencentCloud HotSearch - Online search tool using Tencent Cloud API
Supports web-wide search and site-specific search (e.g., qq.com, news.qq.com)
API Version: 2025-05-08
API Endpoint: wsa.tencentcloudapi.com
"""

import json
import os
import sys
import hashlib
import hmac
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import urllib.request
import urllib.parse


class TencentCloudHotSearch:
    """Main class for searching news and articles using Tencent Cloud API."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize TencentCloudHotSearch with configuration."""
        self.config = self._load_config(config_path)
        self.results = []
    
    def _mask_secret(self, secret: str) -> str:
        """
        Mask secret key for safe logging/error messages.
        
        Args:
            secret: Secret string to mask
            
        Returns:
            Masked secret string
        """
        if not secret or len(secret) < 8:
            return "***"
        return secret[:4] + "..." + secret[-4:]
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                "Please create a config.json file with your Tencent Cloud API credentials.\n"
                "See CONFIG.md for detailed setup instructions."
            )
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate required fields
            if 'secret_id' not in config or 'secret_key' not in config:
                raise ValueError(
                    "Missing required credentials in config.json.\n"
                    "Please add 'secret_id' and 'secret_key' fields."
                )
            
            return config
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON format in config.json: {e}\n"
                "Please ensure the file contains valid JSON."
            )
    
    def _sign_request(self, params: Dict, secret_id: str, secret_key: str) -> Dict:
        """Sign the request using Tencent Cloud signature method."""
        from datetime import datetime, timezone
        
        # Get current timestamp
        timestamp = int(time.time())
        date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
        
        # Build canonical request
        service = "wsa"
        host = f"{service}.tencentcloudapi.com"
        action = "SearchPro"
        version = "2025-05-08"
        region = ""
        
        # Build request payload
        payload = json.dumps(params)
        payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
        # Build canonical headers
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        canonical_headers = f"content-type:application/json\nhost:{host}\n"
        signed_headers = "content-type;host"
        
        canonical_request = (http_request_method + "\n" +
                            canonical_uri + "\n" +
                            canonical_querystring + "\n" +
                            canonical_headers + "\n" +
                            signed_headers + "\n" +
                            payload_hash)
        
        # Build string to sign
        algorithm = "TC3-HMAC-SHA256"
        credential_scope = date + "/" + service + "/" + "tc3_request"
        string_to_sign = (algorithm + "\n" +
                         str(timestamp) + "\n" +
                         credential_scope + "\n" +
                         hashlib.sha256(canonical_request.encode('utf-8')).hexdigest())
        
        # Calculate signature
        secret_date = hmac.new(("TC3" + secret_key).encode('utf-8'), date.encode('utf-8'), hashlib.sha256).digest()
        secret_service = hmac.new(secret_date, service.encode('utf-8'), hashlib.sha256).digest()
        secret_signing = hmac.new(secret_service, "tc3_request".encode('utf-8'), hashlib.sha256).digest()
        signature = hmac.new(secret_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # Build authorization header
        authorization = (algorithm + " " +
                        "Credential=" + secret_id + "/" + credential_scope + ", " +
                        "SignedHeaders=" + signed_headers + ", " +
                        "Signature=" + signature)
        
        return {
            "host": host,
            "timestamp": timestamp,
            "authorization": authorization,
            "payload": payload
        }
    
    def search(self, keywords: List[str], site: Optional[str] = None, 
               mode: int = 0, limit: int = 10,
               from_time: Optional[int] = None, to_time: Optional[int] = None,
               industry: Optional[str] = None) -> List[Dict]:
        """
        Search for articles/news based on keywords using Tencent Cloud API.
        
        Args:
            keywords: List of 1-5 search keywords
            site: Optional site filter (e.g., 'qq.com', 'news.qq.com')
            mode: Result type (0-natural search, 1-multimodal VR, 2-mixed)
            limit: Number of results to return (default: 10, max: 50)
            from_time: Start time filter (Unix timestamp in seconds)
            to_time: End time filter (Unix timestamp in seconds)
            industry: Industry filter (gov/news/acad/finance)
            
        Returns:
            List of search results with title, summary, source, date, url, score, etc.
        """
        if not keywords or len(keywords) < 1 or len(keywords) > 5:
            raise ValueError("Keywords must be a list of 1-5 items")
        
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50")
        
        if mode not in [0, 1, 2]:
            raise ValueError("Mode must be 0 (natural), 1 (multimodal VR), or 2 (mixed)")
        
        # Set default time range: from yesterday to current time
        if mode != 1:  # Time parameters are only valid for mode != 1
            if from_time is None:
                # Calculate yesterday's timestamp (24 hours ago)
                from_time = int(time.time()) - 24 * 3600
            if to_time is None:
                # Current time
                to_time = int(time.time())
        
        query = ' '.join(keywords)
        results = self._search_tencent_cloud(query, site, mode, limit, from_time, to_time, industry)
        
        self.results = results
        return results
    
    def _search_tencent_cloud(self, query: str, site: Optional[str], mode: int,
                              limit: int, from_time: Optional[int], 
                              to_time: Optional[int], industry: Optional[str]) -> List[Dict]:
        """Search using Tencent Cloud Online Search API (SearchPro)."""
        
        secret_id = self.config.get('secret_id')
        secret_key = self.config.get('secret_key')
        
        if not secret_id or not secret_key:
            raise ValueError("Tencent Cloud API credentials not found in config.json")
        
        try:
            # Build request parameters
            params = {
                "Query": query,
                "Mode": mode
            }
            
            # Add optional parameters
            if site and mode != 1:  # Site parameter is invalid when mode=1
                params["Site"] = site
            
            # Use valid limit value
            if limit in [10, 20, 30, 40, 50]:
                params["Cnt"] = limit
            else:
                params["Cnt"] = 10  # Default to 10 if invalid limit
            
            if from_time and mode != 1:
                params["FromTime"] = from_time
            
            if to_time and mode != 1:
                params["ToTime"] = to_time
            
            if industry and industry in ['gov', 'news', 'acad', 'finance']:
                params["Industry"] = industry
            
            # Sign the request
            signed_request = self._sign_request(params, secret_id, secret_key)
            
            # Build HTTP request
            url = f"https://{signed_request['host']}"
            headers = {
                "Content-Type": "application/json",
                "Host": signed_request['host'],
                "X-TC-Action": "SearchPro",
                "X-TC-Version": "2025-05-08",
                "X-TC-Timestamp": str(signed_request['timestamp']),
                "Authorization": signed_request['authorization']
            }
            
            req = urllib.request.Request(
                url,
                data=signed_request['payload'].encode('utf-8'),
                headers=headers,
                method="POST"
            )
            
            # Send request
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))
            
            results = []
            
            # Parse response
            if 'Response' in response_data:
                response_body = response_data['Response']
                pages = response_body.get('Pages', [])
                
                for page_str in pages:
                    try:
                        page = json.loads(page_str)
                        results.append({
                            "title": page.get('title', ''),
                            "summary": page.get('passage', ''),
                            "dynamic_summary": page.get('content', ''),  # Premium version field
                            "source": page.get('site', ''),
                            "publishTime": page.get('date', ''),
                            "url": page.get('url', ''),
                            "score": page.get('score', 0),
                            "images": page.get('images', []),
                            "favicon": page.get('favicon', '')
                        })
                    except json.JSONDecodeError:
                        continue
            
            return results
            
        except urllib.error.HTTPError as e:
            # Handle HTTP errors without exposing sensitive information
            error_msg = f"API request failed with status {e.code}"
            if e.code == 401:
                error_msg = "API authentication failed. Please check your credentials."
            elif e.code == 403:
                error_msg = "Access denied. Please verify your API permissions."
            elif e.code == 429:
                error_msg = "Rate limit exceeded. Please try again later."
            elif e.code >= 500:
                error_msg = "Tencent Cloud API error. Please try again later."
            print(f"Error: {error_msg}")
            return []
        except urllib.error.URLError as e:
            # Handle network errors
            print(f"Network error: Unable to connect to Tencent Cloud API. Please check your internet connection.")
            return []
        except Exception as e:
            # Generic error handling - avoid exposing sensitive information
            error_type = type(e).__name__
            print(f"Error occurred during search ({error_type}). Please check your configuration and try again.")
            return []
    
    def _validate_output_path(self, output_path: str) -> Path:
        """
        Validate and sanitize output path to prevent directory traversal attacks.
        
        Args:
            output_path: Path to validate
            
        Returns:
            Validated Path object
            
        Raises:
            ValueError: If path is invalid or attempts directory traversal
        """
        output_file = Path(output_path).resolve()
        
        # Get the configured output directory
        config_output_dir = Path(self.config.get('output_dir', './output')).resolve()
        
        # Ensure the output file is within the configured output directory
        try:
            output_file.relative_to(config_output_dir)
        except ValueError:
            # If output_file is not relative to config_output_dir, check if it's an absolute path
            # For absolute paths, just ensure it doesn't contain suspicious patterns
            if '..' in str(output_path):
                raise ValueError(
                    f"Invalid output path: Directory traversal detected. "
                    f"Path must be within the configured output directory ({config_output_dir})"
                )
        
        # Check for suspicious patterns
        if '..' in str(output_path):
            raise ValueError(
                f"Invalid output path: Directory traversal not allowed. "
                f"Use paths within {config_output_dir}"
            )
        
        # Ensure parent directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        return output_file
    
    def save_results(self, output_path: str, format: str = "md"):
        """
        Save search results to a file.
        
        Args:
            output_path: Path to save the results
            format: Output format - 'json', 'csv', 'txt', or 'md' (default: md)
        """
        if not self.results:
            print("No results to save. Please run a search first.")
            return
        
        # Validate and sanitize output path
        output_file = self._validate_output_path(output_path)
        
        if format == "json":
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "results": self.results,
                    "total": len(self.results),
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            print(f"Results saved to: {output_file}")
            
        elif format == "csv":
            try:
                import pandas as pd
            except ImportError:
                raise ImportError(
                    "Please install pandas for CSV export: pip install pandas"
                )
            
            df = pd.DataFrame(self.results)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"Results saved to: {output_file}")
            
        elif format == "txt":
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Search Results\n")
                f.write(f"Total results: {len(self.results)}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write("=" * 80 + "\n\n")
                
                for i, result in enumerate(self.results, 1):
                    f.write(f"[{i}] {result['title']}\n")
                    f.write(f"Summary: {result['summary']}\n")
                    if result.get('dynamic_summary'):
                        f.write(f"Dynamic Summary: {result['dynamic_summary']}\n")
                    f.write(f"Source: {result['source']}\n")
                    f.write(f"Time: {result['publishTime']}\n")
                    f.write(f"Link: {result['url']}\n")
                    if result.get('score'):
                        f.write(f"Relevance: {result['score']:.4f}\n")
                    f.write("-" * 80 + "\n\n")
            print(f"Results saved to: {output_file}")
            
        elif format == "md":
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Search Results\n\n")
                f.write(f"**Total results:** {len(self.results)}\n")
                f.write(f"**Timestamp:** {datetime.now().isoformat()}\n\n")
                f.write("---\n\n")
                
                for i, result in enumerate(self.results, 1):
                    f.write(f"## {i}. {result['title']}\n\n")
                    f.write(f"**Summary:** {result['summary']}\n\n")
                    if result.get('dynamic_summary'):
                        f.write(f"**Dynamic Summary:** {result['dynamic_summary']}\n\n")
                    f.write(f"**Source:** {result['source']}\n\n")
                    f.write(f"**Time:** {result['publishTime']}\n\n")
                    f.write(f"**Link:** [{result['url']}]({result['url']})\n\n")
                    if result.get('score'):
                        f.write(f"**Relevance:** {result['score']:.4f}\n\n")
                    if result.get('images') and len(result['images']) > 0:
                        f.write(f"**Images:** {', '.join(result['images'])}\n\n")
                    f.write("---\n\n")
            print(f"Results saved to: {output_file}")
            
        else:
            raise ValueError("Format must be 'json', 'csv', 'txt', or 'md'")
    
    def print_results(self):
        """Print search results to console."""
        if not self.results:
            print("No results to display.")
            return
        
        print(f"\nFound {len(self.results)} results:\n")
        for i, result in enumerate(self.results, 1):
            print(f"[{i}] {result['title']}")
            print(f"    Summary: {result['summary'][:100]}...")
            if result.get('dynamic_summary'):
                print(f"    Dynamic Summary: {result['dynamic_summary'][:100]}...")
            print(f"    Source: {result['source']}")
            print(f"    Time: {result['publishTime']}")
            print(f"    Link: {result['url']}")
            if result.get('score'):
                print(f"    Relevance: {result['score']:.4f}")
            print()


def main():
    """Command-line interface for TencentCloudHotSearch."""
    parser = argparse.ArgumentParser(
        description="TencentCloud HotSearch - Online search tool using Tencent Cloud API"
    )
    parser.add_argument(
        "keywords",
        nargs="+",
        help="Search keywords (1-5 keywords)"
    )
    parser.add_argument(
        "-s", "--site",
        help="Specify search site (e.g., qq.com, news.qq.com). If not specified, searches the entire web."
    )
    parser.add_argument(
        "-m", "--mode",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Search mode: 0-natural search (default), 1-multimodal VR, 2-mixed"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=10,
        help="Number of results (default: 10, max: 50, options: 10/20/30/40/50)"
    )
    parser.add_argument(
        "--from-time",
        type=int,
        help="Start time filter (Unix timestamp in seconds)"
    )
    parser.add_argument(
        "--to-time",
        type=int,
        help="End time filter (Unix timestamp in seconds)"
    )
    parser.add_argument(
        "--industry",
        choices=["gov", "news", "acad", "finance"],
        help="Industry filter: gov/news/acad/finance (premium only)"
    )
    parser.add_argument(
        "-c", "--config",
        default="config.json",
        help="Path to config file (default: config.json)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (e.g., results.json, results.md, results.txt)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "csv", "txt", "md"],
        default="md",
        help="Output format (default: md)"
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print results to console"
    )
    
    args = parser.parse_args()
    
    try:
        searcher = TencentCloudHotSearch(args.config)
        results = searcher.search(
            keywords=args.keywords,
            site=args.site,
            mode=args.mode,
            limit=args.limit,
            from_time=args.from_time,
            to_time=args.to_time,
            industry=args.industry
        )
        
        if args.print:
            searcher.print_results()
        
        if args.output:
            searcher.save_results(args.output, args.format)
        else:
            # If output path is not specified, use the default path from config file
            config = searcher.config
            default_output_dir = config.get('output_dir', './output')
            default_filename = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
            default_output_path = os.path.join(default_output_dir, default_filename)
            searcher.save_results(default_output_path, args.format)
        
        site_info = f" in {args.site}" if args.site else ""
        mode_info = f" (mode: {args.mode})"
        print(f"\n✅ Successfully retrieved {len(results)} results from Tencent Cloud{site_info}{mode_info}")
        
    except FileNotFoundError as e:
        # Handle missing config file
        print(f"❌ Configuration file not found. Please create config.json with your Tencent Cloud API credentials.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        # Handle validation errors (including path traversal attempts)
        error_msg = str(e)
        # Don't expose sensitive information in error messages
        if 'secret' in error_msg.lower() or 'key' in error_msg.lower():
            print(f"❌ Configuration error: Invalid or missing API credentials.", file=sys.stderr)
        else:
            print(f"❌ {error_msg}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Generic error handling - avoid exposing sensitive information
        error_type = type(e).__name__
        print(f"❌ An error occurred ({error_type}). Please check your configuration and try again.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
