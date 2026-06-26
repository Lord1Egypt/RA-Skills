"""
Ecosystem Integration Module for Smart Skill Finder

Handles integration with different skill ecosystems using API methods as primary method:
- Skills CLI (skills.sh) - API/CLI based search
- Clawhub.ai - API based search  
- GitHub repositories - API based search
"""

import subprocess
import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class SkillResult:
    """Unified skill result structure across all ecosystems."""
    name: str
    description: str
    ecosystem: str
    source_url: str
    install_command: str
    relevance_score: int = 0
    security_status: str = "unknown"  # "clean", "pending", "suspicious", "unknown"
    popularity_score: int = 0


class EcosystemIntegrator:
    """Handles integration with multiple skill ecosystems."""
    
    def __init__(self):
        self.ecosystems = {
            'clawhub': self.search_clawhub,
            'skills_cli': self.search_skills_cli, 
            'github': self.search_github_skills
        }
    
    def search_skills_cli(self, query: Dict[str, Any]) -> List[SkillResult]:
        """
        Search Skills CLI ecosystem using npx command.
        
        Args:
            query: Dictionary with 'keywords' list and 'task' string
            
        Returns:
            List of SkillResult objects
        """
        try:
            # Build search query from keywords
            search_terms = " ".join(query.get('keywords', []))
            if not search_terms:
                search_terms = query.get('task', '')
            
            if not search_terms:
                return []
            
            # Execute Skills CLI search
            cmd = f'npx skills find "{search_terms}" --json'
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode != 0:
                return []
            
            # Parse JSON output
            try:
                skills_data = json.loads(result.stdout)
                return self._parse_skills_cli_results(skills_data, search_terms)
            except json.JSONDecodeError:
                return self._parse_skills_cli_text_output(result.stdout, search_terms)
                
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
            return []
    
    def _parse_skills_cli_results(self, skills_data: List[Dict], query: str) -> List[SkillResult]:
        """Parse JSON output from Skills CLI."""
        results = []
        
        for skill_data in skills_data[:5]:
            try:
                skill = SkillResult(
                    name=skill_data.get('name', 'Unknown Skill'),
                    description=skill_data.get('description', 'No description available'),
                    ecosystem='Skills CLI',
                    source_url=skill_data.get('url', ''),
                    install_command=f"npx skills add {skill_data.get('package', '')}",
                    popularity_score=skill_data.get('installs', 0),
                    security_status='clean'
                )
                results.append(skill)
            except (KeyError, TypeError):
                continue
                
        return results
    
    def _parse_skills_cli_text_output(self, output: str, query: str) -> List[SkillResult]:
        """Parse text output from older Skills CLI versions."""
        results = []
        lines = output.split('\n')
        
        for line in lines[:5]:
            if 'Install with' in line and '@' in line:
                try:
                    parts = line.split('npx skills add ')
                    if len(parts) > 1:
                        package = parts[1].strip()
                        skill_name = package.split('@')[-1] if '@' in package else package
                        
                        skill = SkillResult(
                            name=skill_name,
                            description=f'Skill for {query}',
                            ecosystem='Skills CLI',
                            source_url='',
                            install_command=f'npx skills add {package}',
                            popularity_score=0,
                            security_status='clean'
                        )
                        results.append(skill)
                except Exception:
                    continue
        
        return results
    
    def search_clawhub(self, query: Dict[str, Any]) -> List[SkillResult]:
        """
        Search Clawhub.ai using API.
        
        Args:
            query: Dictionary with 'task' and 'keywords'
            
        Returns:
            List of SkillResult objects
        """
        try:
            search_query = query.get('task', '')
            if not search_query:
                search_query = " ".join(query.get('keywords', []))
            
            if not search_query:
                return []
            
            encoded_query = urllib.parse.quote(search_query)
            url = f"https://clawhub.ai/api/v1/skills/search?q={encoded_query}"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Smart-Skill-Finder/1.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return self._parse_clawhub_results(data, search_query)
                    
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
            pass
        except Exception:
            pass
            
        return []
    
    def _parse_clawhub_results(self, data: Dict, query: str) -> List[SkillResult]:
        """Parse Clawhub API response."""
        results = []
        
        skills = data.get('skills', []) if isinstance(data, dict) else data
        
        if not isinstance(skills, list):
            return results
            
        for skill_data in skills[:5]:
            try:
                name = skill_data.get('name', 'Unknown Skill')
                author = skill_data.get('author', '')
                description = skill_data.get('description', f'Skill for {query}')
                slug = skill_data.get('slug', '')
                
                source_url = f"https://clawhub.ai/{author}/{slug}" if author and slug else ""
                
                security_scan = skill_data.get('security_scan', {})
                virus_total = security_scan.get('virustotal', {}).get('status', 'unknown')
                openclaw_scan = security_scan.get('openclaw', {}).get('status', 'unknown')
                
                if virus_total == 'benign' and openclaw_scan == 'benign':
                    security_status = 'clean'
                elif virus_total == 'pending' or openclaw_scan == 'pending':
                    security_status = 'pending'
                elif virus_total == 'suspicious' or openclaw_scan == 'suspicious':
                    security_status = 'suspicious'
                else:
                    security_status = 'unknown'
                
                install_command = f"clawhub install {author}/{slug}" if author and slug else ""
                
                skill = SkillResult(
                    name=name,
                    description=description,
                    ecosystem='Clawhub',
                    source_url=source_url,
                    install_command=install_command,
                    popularity_score=skill_data.get('installs', 0),
                    security_status=security_status
                )
                results.append(skill)
                
            except (KeyError, TypeError, AttributeError):
                continue
                
        return results
    
    def search_github_skills(self, query: Dict[str, Any]) -> List[SkillResult]:
        """
        Search GitHub for agent skill repositories using API.
        
        Args:
            query: Dictionary with 'keywords' and 'domain'
            
        Returns:
            List of SkillResult objects
        """
        try:
            keywords = " ".join(query.get('keywords', []))
            if not keywords:
                keywords = query.get('task', '')
            
            if not keywords:
                return []
            
            search_query = f"{keywords} topic:agent-skill"
            encoded_query = urllib.parse.quote(search_query)
            url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=5"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Smart-Skill-Finder/1.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return self._parse_github_results(data, keywords)
                    
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
            pass
        except Exception:
            pass
            
        return []
    
    def _parse_github_results(self, data: Dict, query: str) -> List[SkillResult]:
        """Parse GitHub API search results."""
        results = []
        
        items = data.get('items', []) if isinstance(data, dict) else []
        
        for repo in items[:5]:
            try:
                name = repo.get('name', 'Unknown Repository')
                full_name = repo.get('full_name', '')
                description = repo.get('description', f'GitHub repository for {query}')
                html_url = repo.get('html_url', '')
                stars = repo.get('stargazers_count', 0)
                
                install_command = f"git clone {html_url}.git ~/.openclaw/skills/{name}"
                security_status = 'unknown'
                
                skill = SkillResult(
                    name=name,
                    description=description,
                    ecosystem='GitHub',
                    source_url=html_url,
                    install_command=install_command,
                    popularity_score=stars,
                    security_status=security_status
                )
                results.append(skill)
                
            except (KeyError, TypeError, AttributeError):
                continue
                
        return results


def get_ecosystem_integrator() -> EcosystemIntegrator:
    """Factory function to get ecosystem integrator instance."""
    return EcosystemIntegrator()