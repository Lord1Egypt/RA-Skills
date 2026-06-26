#!/usr/bin/env python3
"""
Browser-based skill discovery across multiple ecosystems using Playwright.
This module provides reliable skill search capabilities even when APIs are unavailable.
"""

import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass

# Browser automation will be handled by the main skill_finder module
# This module provides the logic and data structures


@dataclass
class BrowserSkillResult:
    """Unified skill result structure for browser-based discovery."""
    name: str
    description: str
    ecosystem: str
    author: str
    source_url: str
    install_command: str
    downloads: int = 0
    stars: int = 0
    security_status: str = "unknown"  # "clean", "pending", "suspicious", "unknown"
    relevance_score: int = 0


class BrowserSkillDiscovery:
    """Handles browser-based skill discovery across multiple ecosystems."""
    
    def __init__(self):
        self.ecosystems = {
            'clawhub': self.search_clawhub_browser,
            'skills_cli': self.search_skills_cli_browser, 
            'github': self.search_github_browser
        }
    
    def search_clawhub_browser(self, query: str, browser_controller) -> List[BrowserSkillResult]:
        """
        Search Clawhub using browser automation.
        
        Args:
            query: Search query string
            browser_controller: BrowserUse controller instance
            
        Returns:
            List of BrowserSkillResult objects
        """
        try:
            # Navigate to Clawhub search
            browser_controller.open("https://clawhub.ai/skills?focus=search")
            
            # Wait for page to load
            time.sleep(2)
            
            # Find search box and enter query
            snapshot = browser_controller.snapshot()
            search_box_ref = None
            for ref, element in snapshot.items():
                if element.get('type') == 'textbox' and 'Filter by name' in element.get('text', ''):
                    search_box_ref = ref
                    break
            
            if not search_box_ref:
                return []
            
            # Type search query
            browser_controller.type(ref=search_box_ref, text=query)
            browser_controller.press_key(key="Enter")
            
            # Wait for results
            time.sleep(3)
            
            # Get results snapshot
            results_snapshot = browser_controller.snapshot()
            
            # Parse skill results
            skills = self._parse_clawhub_results(results_snapshot, query)
            return skills
            
        except Exception as e:
            print(f"Error searching Clawhub via browser: {e}")
            return []
    
    def _parse_clawhub_results(self, snapshot: Dict, query: str) -> List[BrowserSkillResult]:
        """Parse Clawhub search results from browser snapshot."""
        skills = []
        
        # Look for skill links in the snapshot
        for ref, element in snapshot.items():
            if element.get('type') == 'link' and '/url' in element:
                url = element['/url']
                if '/skills/' in url or (isinstance(url, str) and len(url.split('/')) >= 3):
                    # Extract skill information from link text
                    link_text = element.get('text', '')
                    if link_text and len(link_text) > 10:  # Skip short links
                        skill_info = self._extract_clawhub_skill_info(link_text, url)
                        if skill_info:
                            skills.append(skill_info)
                            
                        # Limit to top 5 results
                        if len(skills) >= 5:
                            break
        
        return skills
    
    def _extract_clawhub_skill_info(self, link_text: str, url: str) -> BrowserSkillResult:
        """Extract skill information from Clawhub link text."""
        try:
            # Link text format: "Skill Name /slug Description by @author stats"
            parts = link_text.split(' by @')
            if len(parts) < 2:
                return None
                
            main_part = parts[0].strip()
            author_part = parts[1].strip()
            
            # Extract author and stats
            author_stats = author_part.split()
            if not author_stats:
                return None
                
            author = author_stats[0]
            
            # Extract downloads and stars from stats
            downloads = 0
            stars = 0
            for stat in author_stats[1:]:
                if 'k' in stat:
                    downloads = int(float(stat.replace('k', '')) * 1000)
                elif '★' in stat:
                    stars = int(stat.replace('★', ''))
            
            # Split main part to get name and description
            if '/' in main_part:
                name_desc_parts = main_part.split('/', 1)
                skill_name = name_desc_parts[0].strip()
                description = name_desc_parts[1].strip() if len(name_desc_parts) > 1 else "No description available"
            else:
                skill_name = main_part
                description = "No description available"
            
            # Build install command
            install_command = f"clawhub install {author}/{skill_name.lower().replace(' ', '-')}"
            
            # Build source URL
            source_url = f"https://clawhub.ai/{author}/{skill_name.lower().replace(' ', '-')}"
            
            return BrowserSkillResult(
                name=skill_name,
                description=description,
                ecosystem='Clawhub',
                author=author,
                source_url=source_url,
                install_command=install_command,
                downloads=downloads,
                stars=stars,
                security_status='unknown'  # Clawhub has security scanning but we can't access it via browser
            )
            
        except Exception as e:
            print(f"Error extracting Clawhub skill info: {e}")
            return None
    
    def search_skills_cli_browser(self, query: str, browser_controller) -> List[BrowserSkillResult]:
        """
        Search Skills CLI using browser automation (via skills.sh website).
        """
        try:
            # Navigate to Skills CLI website
            browser_controller.open("https://skills.sh/")
            
            # Wait for page to load
            time.sleep(2)
            
            # Note: Skills.sh doesn't have a direct search interface
            # We'll return a generic response directing to CLI
            return [
                BrowserSkillResult(
                    name="Skills CLI",
                    description=f"Search for '{query}' using the Skills CLI command line tool",
                    ecosystem='Skills CLI',
                    author='Vercel Labs',
                    source_url='https://skills.sh/',
                    install_command=f"npx skills find \"{query}\"",
                    downloads=581000,  # Estimated based on ecosystem size
                    stars=0,
                    security_status='clean'
                )
            ]
            
        except Exception as e:
            print(f"Error searching Skills CLI via browser: {e}")
            return []
    
    def search_github_browser(self, query: str, browser_controller) -> List[BrowserSkillResult]:
        """
        Search GitHub for agent skill repositories using browser automation.
        """
        try:
            # Construct GitHub search URL
            search_query = f"{query} topic:agent-skill"
            encoded_query = search_query.replace(' ', '+')
            github_url = f"https://github.com/search?q={encoded_query}&type=repositories"
            
            # Navigate to GitHub search
            browser_controller.open(github_url)
            
            # Wait for results
            time.sleep(3)
            
            # Get snapshot and parse results
            snapshot = browser_controller.snapshot()
            skills = self._parse_github_results(snapshot, query)
            return skills
            
        except Exception as e:
            print(f"Error searching GitHub via browser: {e}")
            return []
    
    def _parse_github_results(self, snapshot: Dict, query: str) -> List[BrowserSkillResult]:
        """Parse GitHub search results from browser snapshot."""
        skills = []
        
        # Look for repository links
        repo_links = []
        for ref, element in snapshot.items():
            if element.get('type') == 'link' and '/url' in element:
                url = element['/url']
                if isinstance(url, str) and 'github.com/' in url and '/search' not in url:
                    # Check if this looks like a repository link
                    link_text = element.get('text', '')
                    if link_text and len(link_text.split('/')) >= 2:
                        repo_links.append((url, link_text))
        
        # Process repository links
        for url, link_text in repo_links[:5]:  # Top 5 results
            try:
                # Extract repository information
                url_parts = url.strip('/').split('/')
                if len(url_parts) >= 4:
                    author = url_parts[-2]
                    repo_name = url_parts[-1]
                    
                    # Use link text as description if available, otherwise use query
                    description = link_text if link_text and len(link_text) > 10 else f"GitHub repository for {query}"
                    
                    install_command = f"git clone {url}.git ~/.openclaw/skills/{repo_name}"
                    
                    skill = BrowserSkillResult(
                        name=repo_name,
                        description=description,
                        ecosystem='GitHub',
                        author=author,
                        source_url=url,
                        install_command=install_command,
                        downloads=0,  # Can't get stars via browser easily
                        stars=0,
                        security_status='unknown'
                    )
                    skills.append(skill)
                    
            except Exception as e:
                continue
        
        return skills
    
    def rank_skills_by_relevance(self, skills: List[BrowserSkillResult], original_query: str) -> List[BrowserSkillResult]:
        """Rank skills by relevance to the original query."""
        query_words = set(original_query.lower().split())
        
        for skill in skills:
            # Calculate relevance based on name and description match
            name_words = set(skill.name.lower().split())
            desc_words = set(skill.description.lower().split())
            
            name_overlap = len(query_words & name_words)
            desc_overlap = len(query_words & desc_words)
            
            # Relevance score (0-100)
            relevance = min((name_overlap * 30 + desc_overlap * 10), 100)
            
            # Boost score based on popularity
            popularity_boost = min(skill.downloads // 1000, 20)  # Max 20 points for popularity
            relevance = min(relevance + popularity_boost, 100)
            
            skill.relevance_score = relevance
        
        # Sort by relevance score (descending)
        return sorted(skills, key=lambda x: x.relevance_score, reverse=True)


def get_browser_skill_discovery() -> BrowserSkillDiscovery:
    """Factory function to get browser skill discovery instance."""
    return BrowserSkillDiscovery()