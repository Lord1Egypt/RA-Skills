#!/usr/bin/env python3
"""
Yuque CLI - Command line interface for Yuque API
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


class YuqueClient:
    """Yuque API Client"""
    
    BASE_URL = "https://www.yuque.com/api/v2"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("YUQUE_TOKEN")
        if not self.token:
            raise ValueError("Yuque token required. Set YUQUE_TOKEN environment variable.")
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make API request"""
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "X-Auth-Token": self.token,
            "Content-Type": "application/json"
        }
        
        req_data = None
        if data:
            req_data = json.dumps(data).encode("utf-8")
        
        req = urllib.request.Request(
            url,
            data=req_data,
            headers=headers,
            method=method
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"Error: HTTP {e.code} - {error_body}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    def get_user(self) -> Dict:
        """Get current user info"""
        return self._request("GET", "/user")
    
    def list_user_repos(self, login: str) -> Dict:
        """List user's repositories"""
        return self._request("GET", f"/users/{login}/repos")
    
    def list_group_repos(self, login: str) -> Dict:
        """List group's repositories"""
        return self._request("GET", f"/groups/{login}/repos")
    
    def get_repo(self, namespace: str) -> Dict:
        """Get repository details"""
        return self._request("GET", f"/repos/{namespace}")
    
    def list_docs(self, namespace: str) -> Dict:
        """List documents in repository"""
        return self._request("GET", f"/repos/{namespace}/docs")
    
    def get_doc(self, namespace: str, slug: str, raw: bool = False) -> Dict:
        """Get document details"""
        endpoint = f"/repos/{namespace}/docs/{slug}"
        if raw:
            endpoint += "?raw=1"
        return self._request("GET", endpoint)
    
    def create_doc(self, namespace: str, title: str, body: str, 
                   format: str = "markdown") -> Dict:
        """Create new document"""
        data = {
            "title": title,
            "body": body,
            "format": format
        }
        return self._request("POST", f"/repos/{namespace}/docs", data)
    
    def update_doc(self, namespace: str, id: int, title: Optional[str] = None,
                   body: Optional[str] = None) -> Dict:
        """Update document"""
        data = {}
        if title:
            data["title"] = title
        if body:
            data["body"] = body
        return self._request("PUT", f"/repos/{namespace}/docs/{id}", data)
    
    def delete_doc(self, namespace: str, id: int) -> Dict:
        """Delete document"""
        return self._request("DELETE", f"/repos/{namespace}/docs/{id}")
    
    def search_docs(self, namespace: str, query: str) -> list:
        """Search documents by title (client-side filtering)"""
        result = self.list_docs(namespace)
        docs = result.get("data", [])
        query_lower = query.lower()
        return [doc for doc in docs if query_lower in doc.get("title", "").lower()]


def format_doc_list(docs: list) -> str:
    """Format document list for display"""
    if not docs:
        return "No documents found."
    
    lines = []
    for doc in docs:
        lines.append(f"- {doc.get('title', 'Untitled')} (slug: {doc.get('slug')})")
        lines.append(f"  ID: {doc.get('id')} | Updated: {doc.get('updated_at')}")
    return "\n".join(lines)


def format_repo_list(repos: list) -> str:
    """Format repository list for display"""
    if not repos:
        return "No repositories found."
    
    lines = []
    for repo in repos:
        lines.append(f"- {repo.get('name')} (namespace: {repo.get('namespace')})")
        lines.append(f"  Type: {repo.get('type')} | Public: {repo.get('public')}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Yuque CLI")
    parser.add_argument("--token", help="Yuque API token (or set YUQUE_TOKEN env var)")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # User commands
    subparsers.add_parser("user", help="Get current user info")
    
    # Repo commands
    repos_parser = subparsers.add_parser("repos", help="List repositories")
    repos_parser.add_argument("--user", help="User login")
    repos_parser.add_argument("--group", help="Group login")
    
    repo_parser = subparsers.add_parser("repo", help="Get repository details")
    repo_parser.add_argument("namespace", help="Repository namespace (e.g., user/repo)")
    
    # Doc commands
    docs_parser = subparsers.add_parser("docs", help="List documents")
    docs_parser.add_argument("namespace", help="Repository namespace")
    
    doc_parser = subparsers.add_parser("doc", help="Get document details")
    doc_parser.add_argument("namespace", help="Repository namespace")
    doc_parser.add_argument("slug", help="Document slug")
    doc_parser.add_argument("--raw", action="store_true", help="Get raw content")
    
    create_parser = subparsers.add_parser("create", help="Create document")
    create_parser.add_argument("namespace", help="Repository namespace")
    create_parser.add_argument("--title", required=True, help="Document title")
    create_parser.add_argument("--body", required=True, help="Document body (markdown)")
    
    update_parser = subparsers.add_parser("update", help="Update document")
    update_parser.add_argument("namespace", help="Repository namespace")
    update_parser.add_argument("--id", type=int, required=True, help="Document ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--body", help="New body")
    
    search_parser = subparsers.add_parser("search", help="Search documents")
    search_parser.add_argument("namespace", help="Repository namespace")
    search_parser.add_argument("--query", required=True, help="Search query")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    token = args.token or os.environ.get("YUQUE_TOKEN")
    if not token:
        print("Error: Yuque token required. Use --token or set YUQUE_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)
    
    client = YuqueClient(token)
    
    try:
        if args.command == "user":
            result = client.get_user()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "repos":
            if args.user:
                result = client.list_user_repos(args.user)
            elif args.group:
                result = client.list_group_repos(args.group)
            else:
                # Default to current user
                user = client.get_user()
                login = user.get("data", {}).get("login")
                result = client.list_user_repos(login)
            print(format_repo_list(result.get("data", [])))
        
        elif args.command == "repo":
            result = client.get_repo(args.namespace)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "docs":
            result = client.list_docs(args.namespace)
            print(format_doc_list(result.get("data", [])))
        
        elif args.command == "doc":
            result = client.get_doc(args.namespace, args.slug, raw=args.raw)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "create":
            result = client.create_doc(args.namespace, args.title, args.body)
            print(f"Document created successfully!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "update":
            result = client.update_doc(args.namespace, args.id, args.title, args.body)
            print(f"Document updated successfully!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == "search":
            docs = client.search_docs(args.namespace, args.query)
            print(format_doc_list(docs))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
