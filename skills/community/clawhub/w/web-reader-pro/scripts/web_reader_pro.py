#!/usr/bin/env python3
"""
Web Reader Pro - Advanced Web Content Extraction for OpenClaw

A multi-tier web content extraction system with:
- Three-tier fallback strategy (Jina → Scrapling → WebFetch)
- Jina quota monitoring and alerting
- Smart cache layer
- Quality scoring and auto-escalation
- Domain-level routing learning
- Exponential backoff retry
"""

import os
import re
import time
import json
import hashlib
import logging
import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from urllib.parse import urlparse

import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

# Optional imports with fallbacks
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    import markdownify
    MARKDOWNIFY_AVAILABLE = True
except ImportError:
    MARKDOWNIFY_AVAILABLE = False

try:
    import diskcache
    DISKCACHE_AVAILABLE = True
except ImportError:
    DISKCACHE_AVAILABLE = False

try:
    from selectolax.parser import HTMLParser
    SELECTOLAX_AVAILABLE = True
except ImportError:
    SELECTOLAX_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("web-reader-pro")


class ExtractionTier(str, Enum):
    """Extraction tier enumeration"""
    JINA = "jina"
    SCRAPLING = "scrapling"
    WEBFETCH = "webfetch"
    
    @classmethod
    def get_order(cls) -> list:
        return [cls.JINA, cls.SCRAPLING, cls.WEBFETCH]
    
    @classmethod
    def get_next(cls, tier: 'ExtractionTier') -> Optional['ExtractionTier']:
        order = cls.get_order()
        try:
            idx = order.index(tier)
            return order[idx + 1] if idx < len(order) - 1 else None
        except ValueError:
            return None


@dataclass
class ExtractionResult:
    """Result container for extracted content"""
    title: str
    content: str
    url: str
    tier_used: str
    quality_score: int
    cached: bool
    domain_learned_tier: Optional[str] = None
    extracted_at: str = None
    
    def __post_init__(self):
        if self.extracted_at is None:
            self.extracted_at = datetime.datetime.utcnow().isoformat() + "Z"
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class JinaQuotaStatus:
    """Jina API quota status"""
    call_count: int
    limit: int
    percentage: float
    warning_issued: bool
    exhausted: bool
    
    def to_dict(self) -> Dict:
        return asdict(self)


class JinaQuotaMonitor:
    """
    Jina API quota monitoring system.
    Tracks API call count and warns when approaching limits.
    """
    
    DEFAULT_QUOTA_LIMIT = 100000
    WARNING_THRESHOLD = 0.80  # Warn at 80% usage
    CRITICAL_THRESHOLD = 0.95  # Critical at 95% usage
    
    def __init__(self, quota_limit: int = None, storage_path: str = None):
        self.limit = quota_limit or int(os.environ.get(
            'WEB_READER_JINA_QUOTA', self.DEFAULT_QUOTA_LIMIT
        ))
        self.storage_path = self._get_storage_path(storage_path)
        self._ensure_storage()
        
    def _get_storage_path(self, storage_path: str = None) -> Path:
        if storage_path:
            return Path(storage_path)
        cache_dir = Path(os.environ.get(
            'WEB_READER_CACHE_DIR',
            Path.home() / '.openclaw' / 'cache' / 'web-reader-pro'
        ))
        return cache_dir / 'jina_quota.json'
    
    def _ensure_storage(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._save_state({'count': 0, 'last_reset': time.time()})
    
    def _load_state(self) -> Dict:
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {'count': 0, 'last_reset': time.time()}
    
    def _save_state(self, state: Dict):
        with open(self.storage_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def increment(self) -> JinaQuotaStatus:
        """
        Increment call count and return current status.
        """
        state = self._load_state()
        state['count'] += 1
        self._save_state(state)
        
        return self.get_status()
    
    def get_status(self) -> JinaQuotaStatus:
        """
        Get current quota status.
        """
        state = self._load_state()
        count = state['count']
        percentage = (count / self.limit) * 100 if self.limit > 0 else 0
        
        warning_issued = percentage >= (self.WARNING_THRESHOLD * 100)
        exhausted = percentage >= 100
        
        if percentage >= self.CRITICAL_THRESHOLD * 100 and not exhausted:
            logger.warning(
                f"⚠️ Jina API quota critical: {percentage:.1f}% used "
                f"({count}/{self.limit}). Consider using lower tiers."
            )
        
        return JinaQuotaStatus(
            call_count=count,
            limit=self.limit,
            percentage=percentage,
            warning_issued=warning_issued,
            exhausted=exhausted
        )
    
    def should_fallback(self) -> bool:
        """
        Check if we should fallback to lower tiers.
        """
        status = self.get_status()
        return status.exhausted or status.percentage >= self.CRITICAL_THRESHOLD * 100
    
    def reset(self):
        """Reset the counter (for testing or manual reset)."""
        self._save_state({'count': 0, 'last_reset': time.time()})
        logger.info("Jina quota counter reset")


class CacheManager:
    """
    Smart cache layer for web content.
    Caches extracted content with TTL-based expiration.
    """
    
    def __init__(self, cache_dir: str = None, ttl: int = 3600):
        self.ttl = ttl
        self.cache_dir = Path(cache_dir or os.environ.get(
            'WEB_READER_CACHE_DIR',
            Path.home() / '.openclaw' / 'cache' / 'web-reader-pro'
        ))
        
        if DISKCACHE_AVAILABLE:
            self.cache = diskcache.Cache(str(self.cache_dir))
            self._backend = 'diskcache'
        else:
            self._backend = 'simple'
            self._simple_cache: Dict[str, Tuple[Any, float]] = {}
        
        logger.info(f"Cache initialized: backend={self._backend}, ttl={ttl}s")
    
    def _make_key(self, url: str) -> str:
        """Generate cache key from URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:32]
    
    def get(self, url: str) -> Optional[Dict]:
        """Get cached result for URL."""
        key = self._make_key(url)
        
        if self._backend == 'diskcache':
            try:
                result = self.cache.get(key)
                if result:
                    cached_time = result.get('_cached_at', 0)
                    if time.time() - cached_time < self.ttl:
                        result['cached'] = True
                        logger.debug(f"Cache hit for {url}")
                        return result
                    else:
                        del self.cache[key]
            except Exception as e:
                logger.warning(f"Cache get error: {e}")
        else:
            if key in self._simple_cache:
                result, cached_time = self._simple_cache[key]
                if time.time() - cached_time < self.ttl:
                    result['cached'] = True
                    logger.debug(f"Cache hit for {url}")
                    return result
                else:
                    del self._simple_cache[key]
        
        return None
    
    def set(self, url: str, result: Dict):
        """Cache result for URL."""
        key = self._make_key(url)
        result['_cached_at'] = time.time()
        
        if self._backend == 'diskcache':
            try:
                self.cache.set(key, result)
            except Exception as e:
                logger.warning(f"Cache set error: {e}")
        else:
            self._simple_cache[key] = (result, time.time())
        
        logger.debug(f"Cached result for {url}")
    
    def invalidate(self, url: str = None):
        """Invalidate cache for URL or all URLs."""
        if url:
            key = self._make_key(url)
            if self._backend == 'diskcache':
                try:
                    del self.cache[key]
                except KeyError:
                    pass
            else:
                self._simple_cache.pop(key, None)
            logger.debug(f"Cache invalidated for {url}")
        else:
            if self._backend == 'diskcache':
                self.cache.clear()
            else:
                self._simple_cache.clear()
            logger.info("All cache invalidated")


class QualityScorer:
    """
    Extraction quality scoring system.
    Scores based on word count, title detection, and content density.
    """
    
    MIN_WORD_COUNT = 100
    MIN_TITLE_LENGTH = 5
    MAX_TITLE_LENGTH = 300
    
    def __init__(self, min_word_count: int = None):
        self.min_word_count = min_word_count or self.MIN_WORD_COUNT
    
    def score(self, title: str, content: str, url: str = None) -> Tuple[int, Dict]:
        """
        Calculate quality score for extracted content.
        
        Returns:
            Tuple of (score 0-100, details_dict)
        """
        details = {}
        total_score = 0
        
        # Word count score (0-40 points)
        word_count = self._count_words(content)
        word_score = min(40, (word_count / self.min_word_count) * 40)
        total_score += word_score
        details['word_count'] = word_count
        details['word_score'] = word_score
        
        # Title score (0-30 points)
        title_score = self._score_title(title)
        total_score += title_score
        details['title_length'] = len(title) if title else 0
        details['title_score'] = title_score
        
        # Content density score (0-20 points)
        density_score = self._score_content_density(content)
        total_score += density_score
        details['density_score'] = density_score
        
        # URL relevance score (0-10 points)
        url_score = self._score_url_relevance(title, url) if url else 10
        total_score += url_score
        details['url_score'] = url_score
        
        final_score = min(100, int(total_score))
        details['total_score'] = final_score
        details['meets_threshold'] = (
            word_count >= self.min_word_count and 
            title_score > 0 and 
            final_score >= 50
        )
        
        return final_score, details
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        if not text:
            return 0
        # Count Chinese characters as words, split English by whitespace
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        return chinese_chars + english_words
    
    def _score_title(self, title: str) -> int:
        """
        Score title quality.
        """
        if not title:
            return 0
        
        title = title.strip()
        length = len(title)
        
        if length < self.MIN_TITLE_LENGTH:
            return 5
        elif length > self.MAX_TITLE_LENGTH:
            return 15
        else:
            # Check for meaningful content
            if re.search(r'[\u4e00-\u9fff}]', title) or re.search(r'[a-zA-Z]{3,}', title):
                return 30
            return 20
    
    def _score_content_density(self, content: str) -> int:
        """
        Score content density (removing boilerplate).
        """
        if not content:
            return 0
        
        # Simple heuristic: check ratio of meaningful chars
        total_len = len(content)
        meaningful_chars = len(re.findall(
            r'[\u4e00-\u9fff}a-zA-Z0-9.,!?;:\'\"-]',
            content
        ))
        
        if total_len == 0:
            return 0
        
        ratio = meaningful_chars / total_len
        return int(ratio * 20)
    
    def _score_url_relevance(self, title: str, url: str) -> int:
        """
        Score URL-relevance (basic check for placeholder titles).
        """
        if not title:
            return 0
        
        # Penalize generic/default titles
        generic_patterns = [
            r'^Untitled',
            r'^404',
            r'^Page Not Found',
            r'^Login',
            r'^Sign In',
        ]
        
        for pattern in generic_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                return 2
        
        return 10


class DomainRouter:
    """
    Domain-level routing learning system.
    Learns and persists optimal extraction tier per domain.
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = self._get_db_path(db_path)
        self._ensure_db()
        self.routes = self._load_routes()
    
    def _get_db_path(self, db_path: str = None) -> Path:
        if db_path:
            return Path(db_path)
        data_dir = Path(os.environ.get(
            'WEB_READER_LEARNING_DB',
            Path.home() / '.openclaw' / 'data' / 'web-reader-pro'
        ))
        return data_dir / 'routes.json'
    
    def _ensure_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._save_routes({})
    
    def _load_routes(self) -> Dict:
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_routes(self, routes: Dict):
        with open(self.db_path, 'w') as f:
            json.dump(routes, f, indent=2)
    
    def get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc.lower()
        except Exception:
            return 'unknown'
    
    def get_learned_tier(self, url: str) -> Optional[ExtractionTier]:
        """
        Get learned optimal tier for domain.
        """
        domain = self.get_domain(url)
        
        if domain in self.routes:
            tier_str = self.routes[domain].get('preferred_tier')
            if tier_str:
                try:
                    return ExtractionTier(tier_str)
                except ValueError:
                    pass
        return None
    
    def record_success(self, url: str, tier: ExtractionTier, quality_score: int):
        """
        Record successful extraction for a domain.
        """
        domain = self.get_domain(url)
        
        if domain not in self.routes:
            self.routes[domain] = {
                'preferred_tier': tier.value,
                'success_count': {},
                'total_quality': {},
            }
        
        # Update success count
        tier_key = tier.value
        if tier_key not in self.routes[domain]['success_count']:
            self.routes[domain]['success_count'][tier_key] = 0
            self.routes[domain]['total_quality'][tier_key] = 0
        
        self.routes[domain]['success_count'][tier_key] += 1
        self.routes[domain]['total_quality'][tier_key] += quality_score
        self.routes[domain]['last_updated'] = datetime.datetime.utcnow().isoformat()
        
        # Recalculate preferred tier
        self._update_preferred_tier(domain)
        
        self._save_routes(self.routes)
        logger.debug(f"Recorded success for {domain}: tier={tier.value}, score={quality_score}")
    
    def _update_preferred_tier(self, domain: str):
        """
        Update preferred tier based on historical success rates.
        """
        if domain not in self.routes:
            return
        
        success_count = self.routes[domain].get('success_count', {})
        total_quality = self.routes[domain].get('total_quality', {})
        
        if not success_count:
            return
        
        # Calculate weighted score (quality * success_count)
        best_tier = None
        best_score = -1
        
        for tier_key, count in success_count.items():
            quality = total_quality.get(tier_key, 0)
            weighted = (quality / count) * count  # avg_quality * count
            if weighted > best_score:
                best_score = weighted
                best_tier = tier_key
        
        if best_tier:
            self.routes[domain]['preferred_tier'] = best_tier
    
    def get_all_routes(self) -> Dict:
        """Get all domain routes."""
        return self.routes.copy()
    
    def clear_routes(self, domain: str = None):
        """Clear routes for domain or all domains."""
        if domain:
            self.routes.pop(domain, None)
        else:
            self.routes = {}
        self._save_routes(self.routes)


class TierExtractor:
    """
    Individual tier extractor with retry logic.
    Each tier implements its own extraction method with exponential backoff.
    """
    
    def __init__(self, tier: ExtractionTier, max_retries: int = 3, scrapling_path: str = None):
        self.tier = tier
        self.max_retries = max_retries
        self.scrapling_path = scrapling_path or self._find_scrapling()
    
    def _find_scrapling(self) -> str:
        """Find scrapling binary path."""
        common_paths = [
            '/usr/local/bin/scrapling',
            '/usr/bin/scrapling',
            'scrapling',
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # Check PATH
        import shutil
        path = shutil.which('scrapling')
        if path:
            return path
        
        return 'scrapling'  # Default to PATH lookup
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((requests.RequestException, TimeoutError)),
        reraise=True,
    )
    def extract_with_retry(self, url: str) -> Tuple[str, str]:
        """
        Extract content with retry logic.
        
        Returns:
            Tuple of (title, content)
        """
        if self.tier == ExtractionTier.JINA:
            return self._extract_jina(url)
        elif self.tier == ExtractionTier.SCRAPLING:
            return self._extract_scrapling(url)
        else:
            return self._extract_webfetch(url)
    
    def extract(self, url: str) -> Tuple[str, str]:
        """
        Extract content without retry (for direct calls).
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.extract_with_retry(url)
            except Exception as e:
                logger.warning(
                    f"Tier {self.tier.value} attempt {attempt}/{self.max_retries} "
                    f"failed for {url}: {str(e)}"
                )
                if attempt == self.max_retries:
                    raise
        
        raise RuntimeError(f"All {self.max_retries} attempts failed for {url}")
    
    def _extract_jina(self, url: str) -> Tuple[str, str]:
        """
        Extract using Jina Reader API.
        """
        api_key = os.environ.get('JINA_API_KEY')
        if not api_key:
            raise ValueError("JINA_API_KEY not set")
        
        # Use Jina's reader API
        jina_url = f"https://r.jina.ai/{url}"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'X-Return-Format': 'markdown',
        }
        
        response = requests.get(jina_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        content = response.text
        
        # Parse Jina's format: title is first line starting with # 
        title = ""
        if content.startswith('#'):
            lines = content.split('\n', 1)
            title = lines[0].lstrip('#').strip()
            content = lines[1] if len(lines) > 1 else ""
        
        return title, content.strip()
    
    def _extract_scrapling(self, url: str) -> Tuple[str, str]:
        """
        Extract using Scrapling (requires Node.js).
        """
        import subprocess
        
        scrapling_cmd = [
            self.scrapling_path,
            '--url', url,
            '--format', 'markdown',
        ]
        
        try:
            result = subprocess.run(
                scrapling_cmd,
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )
            
            output = result.stdout
            
            # Parse title from output
            title = ""
            if output.startswith('#'):
                lines = output.split('\n', 1)
                title = lines[0].lstrip('#').strip()
                output = lines[1] if len(lines) > 1 else ""
            
            return title, output.strip()
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Scrapling timed out for {url}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Scrapling error: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                f"Scrapling not found at {self.scrapling_path}. "
                "Run ./scripts/install_scrapling.sh to install."
            )
    
    def _extract_webfetch(self, url: str) -> Tuple[str, str]:
        """
        Extract using basic HTTP request + HTML parsing.
        Fallback method when other tiers fail.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; WebReaderPro/1.0)',
            'Accept': 'text/html,application/xhtml+xml',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        html = response.text
        
        # Parse HTML
        if SELECTOLAX_AVAILABLE:
            return self._parse_with_selectolax(html)
        elif BS4_AVAILABLE:
            return self._parse_with_bs4(html)
        else:
            return self._parse_basic(html)
    
    def _parse_with_selectolax(self, html: str) -> Tuple[str, str]:
        """Parse using selectolax (faster)."""
        parser = HTMLParser(html)
        
        title = ""
        title_node = parser.css_first('title')
        if title_node:
            title = title_node.text()
        
        # Extract main content
        content = ""
        for tag in ['article', 'main', 'div[role="main"]', '.content', '#content']:
            node = parser.css_first(tag)
            if node:
                content = node.text()
                break
        
        if not content:
            body = parser.css_first('body')
            content = body.text() if body else ""
        
        return title.strip(), content.strip()
    
    def _parse_with_bs4(self, html: str) -> Tuple[str, str]:
        """Parse using BeautifulSoup4."""
        soup = BeautifulSoup(html, 'lxml')
        
        title = ""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text()
        
        # Remove script and style elements
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        
        # Find main content
        content = ""
        for tag in ['article', 'main', 'div[role="main"]', '.content', '#content']:
            element = soup.select_one(tag)
            if element:
                content = element.get_text(separator=' ', strip=True)
                break
        
        if not content:
            body = soup.find('body')
            content = body.get_text(separator=' ', strip=True) if body else ""
        
        return title.strip(), content.strip()
    
    def _parse_basic(self, html: str) -> Tuple[str, str]:
        """Basic regex-based parsing when no parser available."""
        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else ""
        
        # Remove scripts and styles
        html_clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
        html_clean = re.sub(r'<style[^>]*>.*?</style>', '', html_clean, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove tags
        content = re.sub(r'<[^>]+>', ' ', html_clean)
        content = re.sub(r'\s+', ' ', content)
        
        return title, content.strip()


class WebReaderPro:
    """
    Main web content extraction class.
    Orchestrates all components for intelligent content extraction.
    """
    
    def __init__(
        self,
        jina_api_key: str = None,
        cache_ttl: int = 3600,
        quality_threshold: int = 200,
        max_retries: int = 3,
        enable_learning: bool = True,
        scrapling_path: str = None,
        quota_limit: int = None,
        cache_dir: str = None,
        learning_db_path: str = None,
    ):
        """
        Initialize WebReaderPro.
        
        Args:
            jina_api_key: Jina API key (or set via JINA_API_KEY env)
            cache_ttl: Cache TTL in seconds (default: 3600)
            quality_threshold: Minimum word count threshold (default: 200)
            max_retries: Max retries per tier (default: 3)
            enable_learning: Enable domain learning (default: True)
            scrapling_path: Path to scrapling binary
            quota_limit: Jina API quota limit
            cache_dir: Cache directory path
            learning_db_path: Domain learning database path
        """
        # Store configuration
        self.quality_threshold = quality_threshold
        self.max_retries = max_retries
        self.enable_learning = enable_learning
        
        # Initialize components
        self.jina_monitor = JinaQuotaMonitor(quota_limit=quota_limit)
        self.cache = CacheManager(ttl=cache_ttl, cache_dir=cache_dir)
        self.quality_scorer = QualityScorer(min_word_count=quality_threshold)
        self.domain_router = DomainRouter(db_path=learning_db_path)
        
        # Set Jina API key if provided
        if jina_api_key:
            os.environ['JINA_API_KEY'] = jina_api_key
        
        logger.info(
            f"WebReaderPro initialized: cache_ttl={cache_ttl}, "
            f"quality_threshold={quality_threshold}, max_retries={max_retries}, "
            f"enable_learning={enable_learning}"
        )
    
    def fetch(self, url: str, force_refresh: bool = False) -> Dict:
        """
        Fetch and extract content from URL.
        
        Args:
            url: Target URL
            force_refresh: Bypass cache if True
            
        Returns:
            Dict with title, content, metadata
        """
        logger.info(f"Fetching URL: {url}")
        
        # Check cache first
        if not force_refresh:
            cached = self.cache.get(url)
            if cached:
                logger.info(f"Returning cached result for {url}")
                return cached
        
        # Get learned tier for domain
        learned_tier = self.domain_router.get_learned_tier(url) if self.enable_learning else None
        
        # Determine extraction order
        if learned_tier:
            tiers_to_try = [learned_tier] + [t for t in ExtractionTier.get_order() if t != learned_tier]
        else:
            tiers_to_try = ExtractionTier.get_order()
        
        # Try each tier
        last_error = None
        for tier in tiers_to_try:
            # Check if we should skip Jina due to quota
            if tier == ExtractionTier.JINA and self.jina_monitor.should_fallback():
                logger.info(f"Skipping Jina tier due to quota limits")
                continue
            
            try:
                extractor = TierExtractor(tier, max_retries=self.max_retries)
                title, content = extractor.extract(url)
                
                # Score quality
                quality_score, score_details = self.quality_scorer.score(title, content, url)
                
                logger.info(
                    f"Tier {tier.value} succeeded for {url}: "
                    f"score={quality_score}, words={score_details['word_count']}"
                )
                
                # Check if quality meets threshold
                if not score_details['meets_threshold'] and tier != ExtractionTier.WEBFETCH:
                    logger.info(
                        f"Quality below threshold ({quality_score}), "
                        f"trying next tier..."
                    )
                    continue
                
                # Increment Jina quota if using Jina
                if tier == ExtractionTier.JINA:
                    quota_status = self.jina_monitor.increment()
                    if quota_status.warning_issued:
                        logger.warning(
                            f"Jina quota warning: {quota_status.percentage:.1f}% used "
                            f"({quota_status.call_count}/{quota_status.limit})"
                        )
                
                # Record success for learning
                if self.enable_learning:
                    self.domain_router.record_success(url, tier, quality_score)
                
                # Build result
                result = {
                    'title': title or 'Untitled',
                    'content': content,
                    'url': url,
                    'tier_used': tier.value,
                    'quality_score': quality_score,
                    'cached': False,
                    'domain_learned_tier': self.domain_router.get_learned_tier(url).value if self.enable_learning else None,
                }
                
                # Cache result
                self.cache.set(url, result)
                
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"Tier {tier.value} failed for {url}: {str(e)}")
                continue
        
        # All tiers failed
        error_msg = f"All tiers failed for {url}. Last error: {str(last_error)}"
        logger.error(error_msg)
        
        return {
            'title': '',
            'content': '',
            'url': url,
            'tier_used': 'none',
            'quality_score': 0,
            'cached': False,
            'error': error_msg,
        }
    
    def fetch_with_tier(self, url: str, preferred_tier: str) -> Dict:
        """
        Fetch using a specific tier (bypassing automatic selection).
        
        Args:
            url: Target URL
            preferred_tier: "jina", "scrapling", or "webfetch"
            
        Returns:
            Dict with title, content, metadata
        """
        try:
            tier = ExtractionTier(preferred_tier.lower())
        except ValueError:
            return {
                'title': '',
                'content': '',
                'url': url,
                'error': f"Invalid tier: {preferred_tier}. Use: jina, scrapling, or webfetch",
            }
        
        extractor = TierExtractor(tier, max_retries=self.max_retries)
        
        try:
            title, content = extractor.extract(url)
            quality_score, _ = self.quality_scorer.score(title, content, url)
            
            # Increment Jina quota if using Jina
            if tier == ExtractionTier.JINA:
                self.jina_monitor.increment()
            
            return {
                'title': title or 'Untitled',
                'content': content,
                'url': url,
                'tier_used': tier.value,
                'quality_score': quality_score,
                'cached': False,
            }
        except Exception as e:
            return {
                'title': '',
                'content': '',
                'url': url,
                'tier_used': tier.value,
                'error': str(e),
            }
    
    def get_jina_status(self) -> Dict:
        """
        Get current Jina API quota status.
        
        Returns:
            Dict with count, limit, percentage, warnings
        """
        return self.jina_monitor.get_status().to_dict()
    
    def clear_cache(self, url: str = None):
        """
        Clear cache for URL or all URLs.
        
        Args:
            url: Specific URL to clear, or None for all
        """
        self.cache.invalidate(url)
    
    def get_domain_routes(self) -> Dict:
        """
        Get learned domain-to-tier mappings.
        
        Returns:
            Dict of domain -> preferred tier
        """
        return self.domain_router.get_all_routes()
    
    def reset_jina_quota(self):
        """Reset Jina quota counter."""
        self.jina_monitor.reset()
    
    def clear_learning_data(self, domain: str = None):
        """
        Clear learning data for domain or all domains.
        
        Args:
            domain: Specific domain to clear, or None for all
        """
        self.domain_router.clear_routes(domain)


def main():
    """CLI entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Web Reader Pro - Web Content Extraction')
    parser.add_argument('url', help='URL to fetch')
    parser.add_argument('--tier', choices=['jina', 'scrapling', 'webfetch'], 
                        help='Force specific tier')
    parser.add_argument('--no-cache', action='store_true', help='Bypass cache')
    parser.add_argument('--status', action='store_true', help='Show Jina quota status')
    parser.add_argument('--routes', action='store_true', help='Show domain routes')
    
    args = parser.parse_args()
    
    if args.status:
        reader = WebReaderPro()
        status = reader.get_jina_status()
        print(f"Jina Quota Status:")
        print(f"  Calls: {status['call_count']}/{status['limit']}")
        print(f"  Usage: {status['percentage']:.1f}%")
        print(f"  Warning issued: {status['warning_issued']}")
        print(f"  Exhausted: {status['exhausted']}")
        return
    
    if args.routes:
        reader = WebReaderPro()
        routes = reader.get_domain_routes()
        print(f"Domain Routes ({len(routes)} domains):")
        for domain, data in routes.items():
            print(f"  {domain}: {data.get('preferred_tier', 'unknown')}")
        return
    
    reader = WebReaderPro()
    
    if args.tier:
        result = reader.fetch_with_tier(args.url, args.tier)
    else:
        result = reader.fetch(args.url, force_refresh=args.no_cache)
    
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Tier Used: {result.get('tier_used', 'N/A')}")
    print(f"Quality Score: {result.get('quality_score', 'N/A')}")
    print(f"Cached: {result.get('cached', False)}")
    print(f"\nContent ({len(result.get('content', ''))} chars):")
    print("-" * 50)
    print(result.get('content', '')[:2000])
    if len(result.get('content', '')) > 2000:
        print("... (truncated)")


if __name__ == '__main__':
    main()
