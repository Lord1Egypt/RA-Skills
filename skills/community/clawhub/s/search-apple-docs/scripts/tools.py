from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_apple_docs(
    query: str,
    type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search Apple Developer Documentation for APIs, frameworks, guides, and samples. Best for finding specific APIs, classes, or methods. For browsing sample code projects, use get_sample_code. For WWDC videos, use the dedicated WWDC tools (list_wwdc_videos, search_wwdc_content).
    
    Args:
        query: Search query for Apple Developer Documentation. Tips: Use specific API names (e.g., "UIViewController"), framework names (e.g., "SwiftUI"), or technical terms. Avoid generic terms like "how to" or "tutorial". Examples: "NSPredicate", "SwiftUI List", "Core Data migration", "URLSession authentication".
        type: Type of content to filter. Use "all" for comprehensive results, "documentation" for API references/guides, "sample" for code snippets. Note: "sample" returns individual code examples, not full projects. For complete sample projects, use get_sample_code instead. Default: "all".
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "type": type
    }
    
    return call_api("1777316659692547", "search_apple_docs", arguments)

def get_apple_doc_content(
    url: str,
    includeRelatedApis: Optional[bool] = None,
    includeReferences: Optional[bool] = None,
    includeSimilarApis: Optional[bool] = None,
    includePlatformAnalysis: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get detailed content from a specific Apple Developer Documentation page. Use this after search_apple_docs to get full documentation. Supports enhanced analysis options for comprehensive API understanding. Best for: reading API details, understanding usage, checking availability.
    
    Args:
        url: Full URL of the Apple Developer Documentation page. Must start with https://developer.apple.com/documentation/. Example: "https://developer.apple.com/documentation/uikit/uiviewcontroller"
        includeRelatedApis: Include inheritance hierarchy and protocol conformances. Useful for understanding API relationships. Default: false
        includeReferences: Resolve and include all referenced types and APIs. Helps understand dependencies. Default: false
        includeSimilarApis: Discover APIs with similar functionality. Great for finding alternatives. Default: false
        includePlatformAnalysis: Analyze platform availability and version requirements. Essential for cross-platform development. Default: false
    
    Returns:
        
    """
    arguments = {
        "url": url,
        "includeRelatedApis": includeRelatedApis,
        "includeReferences": includeReferences,
        "includeSimilarApis": includeSimilarApis,
        "includePlatformAnalysis": includePlatformAnalysis
    }
    
    return call_api("1777316659692547", "get_apple_doc_content", arguments)

def list_technologies(
    category: Optional[str] = None,
    language: Optional[str] = None,
    includeBeta: Optional[bool] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Browse all Apple technologies and frameworks by category. Essential for discovering available frameworks and understanding Apple's technology ecosystem. Use this when: exploring what's available, finding framework identifiers for search_framework_symbols, checking beta status.
    
    Args:
        category: Filter by category (case-sensitive). Popular: "App frameworks" (SwiftUI, UIKit), "Graphics and games" (Metal, SpriteKit), "App services" (CloudKit, StoreKit), "Media" (AVFoundation), "System" (Foundation). Leave empty to see all categories.
        language: Filter by language support. "swift" for Swift-compatible frameworks, "occ" for Objective-C. Leave empty for all.
        includeBeta: Include beta/preview technologies. Set to false to see only stable frameworks. Default: true
        limit: Max results per category. Useful for quick overviews. Default: 200
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "language": language,
        "includeBeta": includeBeta,
        "limit": limit
    }
    
    return call_api("1777316659692547", "list_technologies", arguments)

def search_framework_symbols(
    framework: str,
    symbolType: Optional[str] = None,
    namePattern: Optional[str] = None,
    language: Optional[str] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Browse and search symbols within a specific Apple framework. Perfect for exploring framework APIs, finding all views/controllers/delegates in a framework, or discovering available types. Use after list_technologies to get framework identifiers.
    
    Args:
        framework: Framework identifier in lowercase. Common: "uikit", "swiftui", "foundation", "combine", "coredata". Get exact names from list_technologies. Example: "swiftui" for SwiftUI framework.
        symbolType: Filter by symbol type. Use "class" for UIViewController subclasses, "protocol" for delegates, "struct" for value types. Default: "all" shows everything.
        namePattern: Filter by name pattern. Use "*View" for all views, "UI*" for UI-prefixed symbols, "*Delegate" for delegates. Case-sensitive. Leave empty for all symbols.
        language: Language preference. Some APIs differ between Swift and Objective-C. Default: "swift"
        limit: Results limit (default: 50, max: 200). Includes nested symbols.
    
    Returns:
        
    """
    arguments = {
        "framework": framework,
        "symbolType": symbolType,
        "namePattern": namePattern,
        "language": language,
        "limit": limit
    }
    
    return call_api("1777316659692547", "search_framework_symbols", arguments)

def get_related_apis(
    apiUrl: str,
    includeInherited: Optional[bool] = None,
    includeConformance: Optional[bool] = None,
    includeSeeAlso: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Analyze API relationships and discover related functionality. Shows inheritance, protocol conformances, and Apple's recommended alternatives. Essential for understanding how APIs work together. Use when: learning API hierarchy, finding protocol requirements, discovering related functionality.
    
    Args:
        apiUrl: Apple documentation URL to analyze. Example: "https://developer.apple.com/documentation/uikit/uiview"
        includeInherited: Show inherited methods/properties from superclasses. Helps understand full API surface. Default: true
        includeConformance: Show protocol conformances and requirements. Essential for protocol-oriented programming. Default: true
        includeSeeAlso: Show Apple's recommended related APIs. Great for finding better alternatives or complementary APIs. Default: true
    
    Returns:
        
    """
    arguments = {
        "apiUrl": apiUrl,
        "includeInherited": includeInherited,
        "includeConformance": includeConformance,
        "includeSeeAlso": includeSeeAlso
    }
    
    return call_api("1777316659692547", "get_related_apis", arguments)

def resolve_references_batch(
    sourceUrl: str,
    maxReferences: Optional[float] = None,
    filterByType: Optional[str] = None
) -> Dict[str, Any]:
    """
    Deep dive into all types and APIs referenced in a documentation page. Resolves all mentioned types, methods, and properties to understand dependencies. Use when: analyzing complex APIs, understanding type requirements, exploring API ecosystems.
    
    Args:
        sourceUrl: Documentation URL to analyze for references. Example: "https://developer.apple.com/documentation/swiftui/view"
        maxReferences: Limit resolved references (default: 20, max: 50). Higher values = more comprehensive but slower.
        filterByType: Filter by reference type. Use "protocol" for protocol requirements, "class" for class hierarchies. Default: "all"
    
    Returns:
        
    """
    arguments = {
        "sourceUrl": sourceUrl,
        "maxReferences": maxReferences,
        "filterByType": filterByType
    }
    
    return call_api("1777316659692547", "resolve_references_batch", arguments)

def get_platform_compatibility(
    apiUrl: str,
    compareMode: Optional[str] = None,
    includeRelated: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Check API availability across Apple platforms and OS versions. Shows minimum deployment targets, deprecations, and platform-specific features. Critical for cross-platform development. Use when: planning app requirements, checking API availability, finding platform alternatives.
    
    Args:
        apiUrl: API URL to check compatibility. Example: "https://developer.apple.com/documentation/swiftui/list"
        compareMode: Check single API or entire framework. "framework" shows all APIs in the framework. Default: "single"
        includeRelated: Also check related APIs' compatibility. Useful for finding platform-specific alternatives. Default: false
    
    Returns:
        
    """
    arguments = {
        "apiUrl": apiUrl,
        "compareMode": compareMode,
        "includeRelated": includeRelated
    }
    
    return call_api("1777316659692547", "get_platform_compatibility", arguments)

def find_similar_apis(
    apiUrl: str,
    searchDepth: Optional[str] = None,
    filterByCategory: Optional[str] = None,
    includeAlternatives: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Discover alternative and related APIs. Finds APIs with similar functionality, modern replacements for deprecated APIs, and platform-specific alternatives. Perfect when looking for better ways to implement functionality.
    
    Args:
        apiUrl: Starting API URL. Example: "https://developer.apple.com/documentation/uikit/uialertview" (finds modern alternatives)
        searchDepth: How thoroughly to search. "shallow" = direct recommendations only, "medium" = topic siblings, "deep" = full relationship analysis. Default: "medium"
        filterByCategory: Focus on specific functionality like "Animation", "Navigation", "Data". Case-sensitive partial match.
        includeAlternatives: Include functionally similar APIs that might be better choices. Default: true
    
    Returns:
        
    """
    arguments = {
        "apiUrl": apiUrl,
        "searchDepth": searchDepth,
        "filterByCategory": filterByCategory,
        "includeAlternatives": includeAlternatives
    }
    
    return call_api("1777316659692547", "find_similar_apis", arguments)

def get_documentation_updates(
    category: Optional[str] = None,
    technology: Optional[str] = None,
    year: Optional[str] = None,
    searchQuery: Optional[str] = None,
    includeBeta: Optional[bool] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Track latest Apple platform updates, new APIs, and changes. Shows WWDC announcements, framework updates, and release notes. Essential for staying current with Apple development. For detailed WWDC videos, use WWDC-specific tools.
    
    Args:
        category: Update type filter. "wwdc" = conference highlights, "technology" = API updates, "release-notes" = version changes. Default: "all"
        technology: Filter by framework (case-sensitive). Examples: "SwiftUI", "UIKit", "ARKit". Get names from list_technologies.
        year: WWDC year filter ("2025", "2024", etc.). Only for wwdc category.
        searchQuery: Search keywords. Examples: "async", "performance", "widgets". Case-insensitive.
        includeBeta: Include beta/preview features. Default: true
        limit: Max results (default: 50). Sorted by relevance and date.
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "technology": technology,
        "year": year,
        "searchQuery": searchQuery,
        "includeBeta": includeBeta,
        "limit": limit
    }
    
    return call_api("1777316659692547", "get_documentation_updates", arguments)

def get_technology_overviews(
    category: Optional[str] = None,
    platform: Optional[str] = None,
    searchQuery: Optional[str] = None,
    includeSubcategories: Optional[bool] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Access comprehensive guides and tutorials for Apple technologies. Includes getting started guides, architectural overviews, best practices, and implementation patterns. Perfect for learning new frameworks or understanding Apple's recommended approaches.
    
    Args:
        category: Topic category. Popular: "app-design-and-ui", "games", "ai-machine-learning", "augmented-reality", "privacy-and-security". Leave empty to browse all.
        platform: Target platform. "all" for cross-platform content. Default: "all"
        searchQuery: Search terms. Try: "getting started", "best practices", "architecture", "performance".
        includeSubcategories: Include nested topics for comprehensive results. Set false for overview only. Default: true
        limit: Max results (default: 50). Includes subcategories when enabled.
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "platform": platform,
        "searchQuery": searchQuery,
        "includeSubcategories": includeSubcategories,
        "limit": limit
    }
    
    return call_api("1777316659692547", "get_technology_overviews", arguments)

def get_sample_code(
    framework: Optional[str] = None,
    beta: Optional[str] = None,
    searchQuery: Optional[str] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Browse complete sample projects from Apple. Full working examples demonstrating best practices and implementation patterns. Different from search_apple_docs which returns code snippets. Use for learning by example.
    
    Args:
        framework: Framework filter (case-insensitive). Examples: "SwiftUI", "ARKit", "CoreML". Note: Some samples are under generic categories - use searchQuery for better results.
        beta: Beta samples: "include" = all, "exclude" = stable only, "only" = beta only. Default: "include"
        searchQuery: Search keywords. Most effective approach. Examples: "animation", "camera", "machine learning", "widgets".
        limit: Max results (default: 50).
    
    Returns:
        
    """
    arguments = {
        "framework": framework,
        "beta": beta,
        "searchQuery": searchQuery,
        "limit": limit
    }
    
    return call_api("1777316659692547", "get_sample_code", arguments)

def list_wwdc_videos(
    year: Optional[str] = None,
    topic: Optional[str] = None,
    hasCode: Optional[bool] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Browse WWDC session videos with full offline access to transcripts and code. Shows all available sessions with filtering options. Use this to discover WWDC content, find sessions by topic, or identify videos with code examples.
    
    Args:
        year: WWDC year ("2025", "2024", etc.) or "all". Available: 2020-2025. Example: "2025" for latest.
        topic: Topic ID for exact filtering or keyword for title search. Available topic IDs: "accessibility-inclusion", "app-services", "app-store-distribution-marketing", "audio-video", "business-education", "design", "developer-tools", "essentials", "graphics-games", "health-fitness", "machine-learning-ai", "maps-location", "photos-camera", "privacy-security", "safari-web", "spatial-computing", "swift", "swiftui-ui-frameworks", "system-services". Use exact ID for topic filtering, or any keyword to search in video titles.
        hasCode: Filter by code availability. true = sessions with code, false = without code. Leave empty for all.
        limit: Max videos to show (default: 50). Videos include title, duration, and content indicators.
    
    Returns:
        
    """
    arguments = {
        "year": year,
        "topic": topic,
        "hasCode": hasCode,
        "limit": limit
    }
    
    return call_api("1777316659692547", "list_wwdc_videos", arguments)

def search_wwdc_content(
    query: str,
    searchIn: Optional[str] = None,
    year: Optional[str] = None,
    language: Optional[str] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Full-text search across all WWDC video transcripts and code examples. Find specific discussions, API mentions, or implementation examples. More powerful than list_wwdc_videos for finding specific content.
    
    Args:
        query: Search terms. Examples: "async await", "@Observable", "Vision Pro", "performance optimization".
        searchIn: Search scope. "transcript" = spoken content, "code" = code examples only, "both" = everything. Default: "both"
        year: Limit to specific year ("2025", "2024", etc.). Leave empty for all years.
        language: Code language filter ("swift", "objc", "javascript"). Only for code search.
        limit: Max results (default: 20). Results include context snippets.
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "searchIn": searchIn,
        "year": year,
        "language": language,
        "limit": limit
    }
    
    return call_api("1777316659692547", "search_wwdc_content", arguments)

def get_wwdc_video(
    year: str,
    videoId: str,
    includeTranscript: Optional[bool] = None,
    includeCode: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Access complete WWDC session content including full transcript, code examples, and resources. Use after finding videos with list_wwdc_videos or search_wwdc_content. Provides offline access to entire session content.
    
    Args:
        year: WWDC year. Example: "2025"
        videoId: Session ID. Example: "10101" for keynote, "238" for session 238.
        includeTranscript: Include full session transcript with timestamps. Default: true
        includeCode: Include all code examples from the session. Default: true
    
    Returns:
        
    """
    arguments = {
        "year": year,
        "videoId": videoId,
        "includeTranscript": includeTranscript,
        "includeCode": includeCode
    }
    
    return call_api("1777316659692547", "get_wwdc_video", arguments)

def get_wwdc_code_examples(
    framework: Optional[str] = None,
    topic: Optional[str] = None,
    year: Optional[str] = None,
    language: Optional[str] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Browse all code examples from WWDC sessions. Perfect for finding implementation patterns, seeing new API usage, or learning by example. Each result includes the code and its session context.
    
    Args:
        framework: Framework to find examples for. Examples: "SwiftUI", "SwiftData", "RealityKit".
        topic: Topic ID or concept keyword. Can use exact topic IDs ("swiftui-ui-frameworks", "machine-learning-ai", etc.) for precise filtering, or general keywords like "animation", "performance", "concurrency" for broader search.
        year: WWDC year filter ("2025", "2024", etc.).
        language: Programming language: "swift", "objc", "javascript", "metal".
        limit: Max examples (default: 30). Each includes code and source video info.
    
    Returns:
        
    """
    arguments = {
        "framework": framework,
        "topic": topic,
        "year": year,
        "language": language,
        "limit": limit
    }
    
    return call_api("1777316659692547", "get_wwdc_code_examples", arguments)

def browse_wwdc_topics(
    topicId: Optional[str] = None,
    includeVideos: Optional[bool] = None,
    year: Optional[str] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    List all WWDC topic categories with their IDs. Essential first step before using list_wwdc_videos with topic filtering. Returns topic IDs like "swiftui-ui-frameworks" that can be used in other tools.
    
    Args:
        topicId: Topic ID to explore. Available IDs: "accessibility-inclusion", "app-services", "app-store-distribution-marketing", "audio-video", "business-education", "design", "developer-tools", "essentials", "graphics-games", "health-fitness", "machine-learning-ai", "maps-location", "photos-camera", "privacy-security", "safari-web", "spatial-computing", "swift", "swiftui-ui-frameworks", "system-services". Leave empty to see all topics with video counts.
        includeVideos: List videos in the topic. Set false for topic structure only. Default: true
        year: Filter topic videos by year. Only when browsing specific topic.
        limit: Max videos per topic (default: 20).
    
    Returns:
        
    """
    arguments = {
        "topicId": topicId,
        "includeVideos": includeVideos,
        "year": year,
        "limit": limit
    }
    
    return call_api("1777316659692547", "browse_wwdc_topics", arguments)

def find_related_wwdc_videos(
    videoId: str,
    year: str,
    includeExplicitRelated: Optional[bool] = None,
    includeTopicRelated: Optional[bool] = None,
    includeYearRelated: Optional[bool] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Discover WWDC sessions related to a specific video. Finds prerequisite sessions, follow-up content, and thematically similar talks. Essential for creating learning paths.
    
    Args:
        videoId: Source video ID. Example: "10101" for keynote.
        year: Source video year. Example: "2025"
        includeExplicitRelated: Include Apple's recommended related videos. Usually prerequisites or follow-ups. Default: true
        includeTopicRelated: Include videos from same topic categories. Good for comprehensive learning. Default: true
        includeYearRelated: Include other videos from same WWDC. Default: false
        limit: Max related videos (default: 15).
    
    Returns:
        
    """
    arguments = {
        "videoId": videoId,
        "year": year,
        "includeExplicitRelated": includeExplicitRelated,
        "includeTopicRelated": includeTopicRelated,
        "includeYearRelated": includeYearRelated,
        "limit": limit
    }
    
    return call_api("1777316659692547", "find_related_wwdc_videos", arguments)

def list_wwdc_years(
) -> Dict[str, Any]:
    """
    List all available WWDC years with video counts and statistics. Shows which years have content available and how many videos each year contains.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659692547", "list_wwdc_years", arguments)

