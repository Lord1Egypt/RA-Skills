from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def toronto_start_here(
) -> Dict[str, Any]:
    """
    🚀 START HERE! Essential first call for any Toronto data query. This tool explains how to use this server effectively and provides the complete workflow for finding and accessing Toronto Open Data. Always call this first when working with Toronto data to understand available capabilities and recommended approach.
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072193539", "toronto_start_here", arguments)

def toronto_popular_datasets(
) -> Dict[str, Any]:
    """
    ⭐ POPULAR TORONTO DATASETS: Quick access to the most commonly used Toronto Open Datasets. Shows dataset IDs and what they contain. Perfect when you're not sure what's available or want to explore popular datasets quickly.
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072193539", "toronto_popular_datasets", arguments)

def toronto_smart_data_helper(
    dataset_id: str,
    user_question: str,
    limit: Optional[null] = 10.0
) -> Dict[str, Any]:
    """
    🧠 SMART DATA HELPER - The easiest way to get Toronto data! Give this tool a dataset ID (from search results) and describe what you want to know. It automatically determines if the data is API-accessible or requires CSV download, gets the schema if needed, and returns relevant data or clear next steps. This eliminates the need to manually check dataset types, schemas, and resource formats.
    
    Args:
        dataset_id: null
        user_question: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "dataset_id": dataset_id,
        "user_question": user_question,
        "limit": limit
    }
    
    return call_api("1777419072193539", "toronto_smart_data_helper", arguments)

def toronto_list_datasets(
) -> Dict[str, Any]:
    """
    📋 LIST ALL DATASETS: Shows all 500+ available Toronto Open Datasets with titles and descriptions. Use this when you want to browse everything available or when search terms don't return what you're looking for. Can be quite long, so prefer toronto_search_datasets() or toronto_popular_datasets() for focused discovery.
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419072193539", "toronto_list_datasets", arguments)

def toronto_search_datasets(
    query: str,
    limit: Optional[null] = 10.0
) -> Dict[str, Any]:
    """
    🔍 FIND TORONTO DATA: Search 500+ Toronto Open Datasets by keywords (e.g., 'traffic', 'parks', 'budget', 'health'). Returns dataset IDs and descriptions. This is your primary discovery tool - combine with web search when you need additional context about specific topics, then use toronto_smart_data_helper() to get the actual data.
    
    Args:
        query: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777419072193539", "toronto_search_datasets", arguments)

def toronto_get_dataset_schema(
    dataset_id: str
) -> Dict[str, Any]:
    """
    📋 GET DATA STRUCTURE: Shows the schema (column names, field IDs, and types) for a Toronto dataset if it has an active datastore. Essential for understanding what fields are available before filtering with toronto_query_dataset_data(). For CSV files, suggests checking the header row manually.
    
    Args:
        dataset_id: null
    
    Returns:
        null
    """
    arguments = {
        "dataset_id": dataset_id
    }
    
    return call_api("1777419072193539", "toronto_get_dataset_schema", arguments)

def toronto_query_dataset_data(
    dataset_id: str,
    filters: Optional[null] = None,
    fields: Optional[null] = None,
    limit: Optional[null] = 10.0,
    sort: Optional[null] = None
) -> Dict[str, Any]:
    """
    🔧 ADVANCED QUERYING: Query Toronto datasets with precise filtering, sorting, and field selection. 

💡 TIP: Use toronto_smart_data_helper() first - it's easier and handles most use cases automatically!

This tool is for when you need advanced filtering:
📋 REQUIRED: Get field names first with toronto_get_dataset_schema(dataset_id)
🔍 FILTERS: Use exact field names like {"establishment_status": "Pass", "inspection_date": "2024-01-01"}
📊 SORT: Use field names like "inspection_date desc" or "score asc"
📝 FIELDS: Specify which columns to return like ["name", "address", "score"]

⚠️ For CSV files, this returns download links instead of query results.
🚀 Alternative: Try toronto_smart_data_helper() for a simpler, guided approach.
    
    Args:
        dataset_id: null
        filters: null
        fields: null
        limit: null
        sort: null
    
    Returns:
        null
    """
    arguments = {
        "dataset_id": dataset_id,
        "filters": filters,
        "fields": fields,
        "limit": limit,
        "sort": sort
    }
    
    return call_api("1777419072193539", "toronto_query_dataset_data", arguments)

def toronto_get_dataset_stats(
    dataset_id: str
) -> Dict[str, Any]:
    """
    📈 DATASET STATISTICS: Get basic statistics for a Toronto dataset including record counts, field information, and resource overview. Useful for understanding the scale and structure of a dataset before diving into the data.
    
    Args:
        dataset_id: null
    
    Returns:
        null
    """
    arguments = {
        "dataset_id": dataset_id
    }
    
    return call_api("1777419072193539", "toronto_get_dataset_stats", arguments)

def toronto_fetch_csv_data(
    csv_url: str,
    max_lines: Optional[null] = 50.0
) -> Dict[str, Any]:
    """
    📄 FETCH CSV DATA: Downloads and returns sample content from a CSV file URL. Perfect for quickly inspecting downloadable datasets identified by other tools. Shows headers and sample rows to understand the data structure.
    
    Args:
        csv_url: null
        max_lines: null
    
    Returns:
        null
    """
    arguments = {
        "csv_url": csv_url,
        "max_lines": max_lines
    }
    
    return call_api("1777419072193539", "toronto_fetch_csv_data", arguments)

