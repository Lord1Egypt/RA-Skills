#!/usr/bin/env python3
"""
Smart Skill Finder - Find relevant skills across multiple ecosystems
using OpenClaw's semantic understanding capabilities.
"""

import json
import subprocess
import sys
import os
from typing import Dict, List, Optional

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ecosystems import EcosystemIntegrator


class SmartSkillFinder:
    """
    Main class for smart skill discovery across multiple ecosystems.
    Leverages OpenClaw's built-in semantic understanding for query analysis
    and browser automation for reliable skill discovery.
    """
    
    def __init__(self):
        """Initialize the skill finder with ecosystem integrator."""
        self.ecosystem_integrator = EcosystemIntegrator()
        
    def find_skills_for_query(self, user_query: str) -> str:
        """
        Main entry point for skill discovery.
        
        Args:
            user_query (str): Natural language query from user
            
        Returns:
            str: Formatted response with skill recommendations
        """
        try:
            # Step 1: Understand user need using enhanced keyword extraction
            understood_query = self.understand_user_need(user_query)
            
            # Step 2: Search ecosystems in priority order
            raw_results = self.search_ecosystems(understood_query)
            
            # Step 3: Rank results by relevance
            ranked_results = self.rank_by_relevance(raw_results, user_query)
            
            # Step 4: Present recommendations to user
            return self.present_recommendations(ranked_results, user_query)
            
        except Exception as e:
            return self.handle_error(e, user_query)
    
    def understand_user_need(self, user_query: str) -> Dict[str, any]:
        """
        Enhanced keyword extraction with better domain detection.
        """
        # Extract keywords
        keywords = user_query.lower().split()
        
        # Enhanced domain detection with comprehensive keyword lists
        domain_keywords = {
            'web': ['web', 'website', 'frontend', 'react', 'vue', 'angular', 'html', 'css', 'javascript'],
            'conversation': ['conversation', 'chat', 'dialogue', 'hang', 'stuck', 'reliability', 'flow'],
            'browser': ['browser', 'webpage', 'navigation', 'screenshot', 'automation'],
            'testing': ['test', 'testing', 'jest', 'playwright', 'e2e', 'quality'],
            'documentation': ['doc', 'document', 'readme', 'changelog', 'api-docs'],
            'devops': ['deploy', 'docker', 'kubernetes', 'ci', 'cd', 'github', 'pull request', 'pr'],
            'weather': ['weather', 'temperature', 'forecast', 'climate', 'conditions'],
            'calendar': ['calendar', 'event', 'events', 'schedule', 'scheduling', 'appointment', 'meeting', 'reminder', 'agenda', 'date', 'time', 'booking', 'reservation', 'organize', 'plan', 'create', 'add', 'set', 'manage'],
            'automation': ['automate', 'automation', 'workflow', 'save time', 'reduce manual', 'productivity'],
            'general': []  # fallback
        }
        
        detected_domain = 'general'
        for domain, terms in domain_keywords.items():
            if any(term in user_query.lower() for term in terms):
                detected_domain = domain
                break
        
        result = {
            'domain': detected_domain,
            'task': user_query,
            'keywords': keywords[:5]  # Limit to first 5 keywords
        }
        return result
    
    def search_ecosystems(self, understood_query: Dict[str, any]) -> List[Dict]:
        """
        Search ecosystems in priority order and return combined results.
        """
        results = []
        
        # Priority order: Clawhub -> Skills CLI -> GitHub 
        ecosystems_to_search = [
            ('clawhub', self.ecosystem_integrator.search_clawhub),
            ('skills_cli', self.ecosystem_integrator.search_skills_cli),
            ('github', self.ecosystem_integrator.search_github_skills)
        ]
        
        for ecosystem_name, search_function in ecosystems_to_search:
            try:
                ecosystem_results = search_function(understood_query)
                
                for result in ecosystem_results:
                    result['ecosystem'] = ecosystem_name
                results.extend(ecosystem_results)
                
                # Stop early if we have enough high-quality results
                if len([r for r in results if r.get('quality_score', 0) > 80]) >= 2:
                    break
                    
            except Exception as e:
                continue
        
        return results[:5]
    
    def rank_by_relevance(self, skills: List[Dict], original_query: str) -> List[Dict]:
        """
        Rank skills by relevance to the original user query.
        """
        query_words = set(original_query.lower().split())
        
        for skill in skills:
            description_words = set(skill.get('description', '').lower().split())
            name_words = set(skill.get('name', '').lower().split())
            
            keyword_overlap = len(query_words & (description_words | name_words))
            keyword_score = min(keyword_overlap * 20, 60)
            quality_score = min(skill.get('quality_score', 50), 40)
            skill['relevance_score'] = keyword_score + quality_score
            
            if 'security_status' not in skill:
                skill['security_status'] = 'unknown'
        
        ranked_skills = sorted(skills, key=lambda x: x['relevance_score'], reverse=True)
        return ranked_skills
    
    def present_recommendations(self, skills: List[Dict], original_query: str) -> str:
        """
        Generate user-friendly response with skill recommendations.
        """
        if not skills:
            return self.no_skills_found_response(original_query)
        
        response = "I found some relevant skills for your needs:\n\n"
        medals = ["🥇", "🥈", "🥉"]
        
        for i, skill in enumerate(skills[:3]):
            medal = medals[i] if i < 3 else "🔹"
            name = skill.get('name', 'Unknown Skill')
            ecosystem = skill.get('ecosystem', 'unknown')
            description = skill.get('description', 'No description available')
            relevance = skill.get('relevance_score', 0)
            install_cmd = skill.get('install_command', 'Installation command not available')
            
            response += f"{medal} **{name}** ({ecosystem})\n"
            response += f"   • {description}\n"
            response += f"   • Relevance: {relevance}%\n"
            
            security_status = skill.get('security_status', 'unknown')
            if security_status == 'clean':
                response += "   • ✅ Security verified\n"
            elif security_status == 'pending':
                response += "   • ⚠️ Security scan pending\n"
            elif security_status == 'suspicious':
                response += "   • ❌ Security concerns detected\n"
            else:
                response += "   • ℹ️ Security status unknown\n"
            
            response += f"   • Install: `{install_cmd}`\n\n"
        
        response += "Review the skill details before installing. Would you like me to explain any of these options?"
        return response
    
    def no_skills_found_response(self, original_query: str) -> str:
        """
        Generate response when no relevant skills are found.
        """
        return f"""I searched across multiple skill ecosystems but didn't find specific skills for "{original_query}". 

However, I can help you directly with this task! Would you like me to:
1. Provide general guidance on this topic
2. Help you create your own skill for this specific need  
3. Search more broadly for related resources

What would be most helpful?"""
    
    def handle_error(self, error: Exception, original_query: str) -> str:
        """
        Handle errors gracefully and provide helpful fallback.
        """
        error_msg = str(error)[:200]
        
        return f"""I encountered an issue while searching for skills: {error_msg}

But I can still help you find relevant skills! Based on your need for "{original_query}", 
I recommend checking out these popular options:

• **Skills CLI**: Visit https://skills.sh/ for web development, testing, and productivity skills
• **Clawhub**: Browse https://clawhub.ai/ for OpenClaw-specific skills  
• **GitHub**: Search for repositories with "agent-skill" or "openclaw" topics

Would you like me to provide specific installation commands for any particular type of skill?"""


def main():
    """Main function for testing the skill finder."""
    if len(sys.argv) < 2:
        print("Usage: python skill_finder.py \"your query here\"")
        sys.exit(1)
    
    query = sys.argv[1]
    finder = SmartSkillFinder()
    result = finder.find_skills_for_query(query)
    print(result)


if __name__ == "__main__":
    main()