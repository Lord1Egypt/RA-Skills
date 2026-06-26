# Tavily API Reference

## Overview

Tavily is a search engine optimized for AI agents and RAG (Retrieval-Augmented Generation) applications. It provides clean, structured web search results with optional AI-generated answers.

## API Endpoints

### 1. Search API

**Endpoint**: `POST https://api.tavily.com/search`

Search the web for any query.

**Request Body**:
```json
{
  "query": "string (required)",
  "topic": "general | news",
  "search_depth": "basic | comprehensive",
  "chunks_per_source": 3,
  "max_results": 5,
  "time_range": "day | week | month | year | null",
