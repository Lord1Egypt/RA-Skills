from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def web_search(
    query: str,
    reasoning: str,
    category: Optional[str] = "general",
    max_results: Optional[int] = 5.0
) -> Dict[str, Any]:
    """
    Use this first to gather fresh web search results via the local SearXNG instance.
    
    Args:
        query: null
        reasoning: null
        category: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "reasoning": reasoning,
        "category": category,
        "max_results": max_results
    }
    
    return call_api("1777419066987523", "web_search", arguments)

def crawl_url(
    url: str,
    reasoning: str,
    max_chars: Optional[int] = 8000.0
) -> Dict[str, Any]:
    """
    Fetch a URL with crawl4ai when you need the actual page text for quoting or analysis.
    
    Args:
        url: null
        reasoning: null
        max_chars: null
    
    Returns:
        null
    """
    arguments = {
        "url": url,
        "reasoning": reasoning,
        "max_chars": max_chars
    }
    
    return call_api("1777419066987523", "crawl_url", arguments)

def package_info(
    name: str,
    reasoning: str,
    registry: Optional[str] = "npm"
) -> Dict[str, Any]:
    """
    
Look up package information from npm, PyPI, crates.io, or Go modules.

Returns version, downloads, license, dependencies, security status, and repository links.
Use this to quickly evaluate libraries before adding them to your project.

Examples:
- package_info("express", reasoning="Need web framework", registry="npm")
- package_info("requests", reasoning="HTTP client for API", registry="pypi")
- package_info("serde", reasoning="JSON serialization", registry="crates")

    
    Args:
        name: null
        reasoning: null
        registry: null
    
    Returns:
        null
    """
    arguments = {
        "name": name,
        "reasoning": reasoning,
        "registry": registry
    }
    
    return call_api("1777419066987523", "package_info", arguments)

def search_examples(
    query: str,
    reasoning: str,
    content_type: Optional[str] = "both",
    time_range: Optional[str] = "all",
    max_results: Optional[int] = 5.0
) -> Dict[str, Any]:
    """
    
Search for code examples, tutorials, and technical articles.

Optimized for finding practical examples and learning resources. Can optionally filter by
time range for the most recent content. Perfect for learning new APIs, finding usage patterns,
or discovering how others solve specific technical problems.

Content Types:
- 'code': GitHub repos, code snippets, gists, Stack Overflow code examples
- 'articles': Blog posts, tutorials, documentation, technical articles
- 'both': Mix of code and written content (default)

Time Ranges:
- 'all': Search all available content (default, recommended for best results)
- 'year', 'month', 'week', 'day': Filter to recent content only

Examples:
- search_examples("FastAPI dependency injection examples", content_type="code")
- search_examples("React hooks tutorial", content_type="articles", time_range="year")
- search_examples("Rust lifetime examples", content_type="both")

    
    Args:
        query: null
        reasoning: null
        content_type: null
        time_range: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "reasoning": reasoning,
        "content_type": content_type,
        "time_range": time_range,
        "max_results": max_results
    }
    
    return call_api("1777419066987523", "search_examples", arguments)

def search_images(
    query: str,
    reasoning: str,
    image_type: Optional[str] = "all",
    orientation: Optional[str] = "all",
    max_results: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
Search for high-quality stock images using Pixabay.

Returns royalty-free images that are safe to use. Perfect for finding photos,
illustrations, and vector graphics for projects, presentations, or design work.

Image Types:
- 'photo': Real photographs
- 'illustration': Digital illustrations and artwork
- 'vector': Vector graphics (SVG format available)
- 'all': All types (default)

Examples:
- search_images("mountain landscape", image_type="photo")
- search_images("business icons", image_type="vector")
- search_images("technology background", orientation="horizontal")

    
    Args:
        query: null
        reasoning: null
        image_type: null
        orientation: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "reasoning": reasoning,
        "image_type": image_type,
        "orientation": orientation,
        "max_results": max_results
    }
    
    return call_api("1777419066987523", "search_images", arguments)

def package_search(
    query: str,
    reasoning: str,
    registry: Optional[str] = "npm",
    max_results: Optional[int] = 5.0
) -> Dict[str, Any]:
    """
    
Search for packages by keywords or description across registries.

Use this to find packages that solve a specific problem or provide certain functionality.
Perfect for discovering libraries when you know what you need but not the package name.

Examples:
- package_search("web framework", reasoning="Need backend framework", registry="npm")
- package_search("json parsing", reasoning="Data processing", registry="pypi")

    
    Args:
        query: null
        reasoning: null
        registry: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "reasoning": reasoning,
        "registry": registry,
        "max_results": max_results
    }
    
    return call_api("1777419066987523", "package_search", arguments)

def github_repo(
    repo: str,
    reasoning: str,
    include_commits: Optional[bool] = True
) -> Dict[str, Any]:
    """
    
Fetch GitHub repository information and health metrics.

Returns stars, forks, issues, recent activity, language, license, and description.
Use this to evaluate open source projects before using them.

Examples:
- github_repo("microsoft/vscode", reasoning="Evaluate editor project")
- github_repo("https://github.com/facebook/react", reasoning="Research UI framework")

    
    Args:
        repo: null
        reasoning: null
        include_commits: null
    
    Returns:
        null
    """
    arguments = {
        "repo": repo,
        "reasoning": reasoning,
        "include_commits": include_commits
    }
    
    return call_api("1777419066987523", "github_repo", arguments)

def translate_error(
    error_message: str,
    reasoning: str,
    language: Optional[null] = None,
    framework: Optional[null] = None,
    max_results: Optional[int] = 5.0
) -> Dict[str, Any]:
    """
    
Find solutions for error messages and stack traces from Stack Overflow and GitHub.

Takes an error message or stack trace and finds relevant solutions with code examples.
Automatically detects language and framework, extracts key error information, and
searches for the best solutions ranked by votes and relevance.

Perfect for:
- Debugging production errors
- Understanding cryptic error messages
- Finding working code fixes
- Learning from similar issues

Examples:
- translate_error("TypeError: Cannot read property 'map' of undefined", reasoning="Debugging React app crash")
- translate_error("CORS policy: No 'Access-Control-Allow-Origin' header", reasoning="Fixing API integration", framework="FastAPI")
- translate_error("error[E0382]: borrow of moved value", reasoning="Learning Rust ownership", language="rust")

    
    Args:
        error_message: null
        reasoning: null
        language: null
        framework: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "error_message": error_message,
        "reasoning": reasoning,
        "language": language,
        "framework": framework,
        "max_results": max_results
    }
    
    return call_api("1777419066987523", "translate_error", arguments)

def api_docs(
    api_name: str,
    reasoning: str,
    topic: str,
    max_results: Optional[int] = 2.0
) -> Dict[str, Any]:
    """
    
Search and fetch official API documentation with examples and explanations.

Documentation-first approach: fetches human-written docs with context, examples,
and best practices. Much more useful than OpenAPI specs alone.

Discovery strategy:
1. Try common URL patterns (docs.{api}.com, {api}.com/docs, etc.)
2. If patterns fail, search for "{api} API official documentation"
3. Crawl discovered docs and extract relevant content

No hardcoded URLs - works for ANY API by discovering docs dynamically.

Examples:
- api_docs("stripe", "create customer", reasoning="Setting up payments")
- api_docs("github", "create repository", reasoning="Automating repo creation")
- api_docs("spartan", "button component", reasoning="Learning UI library")

    
    Args:
        api_name: null
        reasoning: null
        topic: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "api_name": api_name,
        "reasoning": reasoning,
        "topic": topic,
        "max_results": max_results
    }
    
    return call_api("1777419066987523", "api_docs", arguments)

def extract_data(
    url: str,
    reasoning: str,
    extract_type: Optional[str] = "auto",
    selectors: Optional[null] = None,
    max_items: Optional[int] = 100.0
) -> Dict[str, Any]:
    """
    
Extract structured data from web pages.

Extracts tables, lists, or specific fields from HTML pages and returns
structured data. Much more efficient than parsing full page text.

Extract Types:
- "table": Extract HTML tables as list of dicts
- "list": Extract lists (ul/ol/dl) as structured list
- "fields": Extract specific elements using CSS selectors
- "json-ld": Extract JSON-LD structured data
- "auto": Automatically detect and extract structured content

Examples:
- extract_data("https://pypi.org/project/fastapi/", reasoning="Get package info")
- extract_data("https://github.com/user/repo/releases", reasoning="Get releases", extract_type="list")
- extract_data(
    "https://example.com/product",
    reasoning="Extract product details",
    extract_type="fields",
    selectors={"price": ".price", "title": "h1.product-name"}
  )

    
    Args:
        url: null
        reasoning: null
        extract_type: null
        selectors: null
        max_items: null
    
    Returns:
        null
    """
    arguments = {
        "url": url,
        "reasoning": reasoning,
        "extract_type": extract_type,
        "selectors": selectors,
        "max_items": max_items
    }
    
    return call_api("1777419066987523", "extract_data", arguments)

def compare_tech(
    technologies: null,
    reasoning: str,
    category: Optional[str] = "auto",
    aspects: Optional[null] = None,
    max_results_per_tech: Optional[int] = 3.0
) -> Dict[str, Any]:
    """
    
Compare multiple technologies, frameworks, or libraries side-by-side.

Automatically gathers information about each technology and presents
a structured comparison to help make informed decisions.

Categories:
- "framework": Web frameworks (React, Vue, Angular, etc.)
- "library": JavaScript/Python/etc. libraries
- "database": Databases (PostgreSQL, MongoDB, etc.)
- "language": Programming languages (Python, Go, Rust, etc.)
- "tool": Build tools, CLIs, etc. (Webpack, Vite, etc.)
- "auto": Auto-detect category

Examples:
- compare_tech(["React", "Vue", "Svelte"], reasoning="Choose framework for new project")
- compare_tech(["PostgreSQL", "MongoDB"], category="database", reasoning="Database for user data")
- compare_tech(["FastAPI", "Flask"], aspects=["performance", "learning_curve"], reasoning="Python web framework")

    
    Args:
        technologies: null
        reasoning: null
        category: null
        aspects: null
        max_results_per_tech: null
    
    Returns:
        null
    """
    arguments = {
        "technologies": technologies,
        "reasoning": reasoning,
        "category": category,
        "aspects": aspects,
        "max_results_per_tech": max_results_per_tech
    }
    
    return call_api("1777419066987523", "compare_tech", arguments)

def get_changelog(
    package: str,
    reasoning: str,
    registry: Optional[str] = "auto",
    max_releases: Optional[int] = 5.0
) -> Dict[str, Any]:
    """
    Get changelog and release notes for a package.
    
    Args:
        package: null
        reasoning: null
        registry: null
        max_releases: null
    
    Returns:
        null
    """
    arguments = {
        "package": package,
        "reasoning": reasoning,
        "registry": registry,
        "max_releases": max_releases
    }
    
    return call_api("1777419066987523", "get_changelog", arguments)

def check_service_status(
    service: str,
    reasoning: str
) -> Dict[str, Any]:
    """
    Check if an API service or platform is experiencing issues.
    
    Args:
        service: null
        reasoning: null
    
    Returns:
        null
    """
    arguments = {
        "service": service,
        "reasoning": reasoning
    }
    
    return call_api("1777419066987523", "check_service_status", arguments)

