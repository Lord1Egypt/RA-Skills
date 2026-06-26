#!/usr/bin/env python3
"""
xx - Xpert Xchange: A specialized platform for exchanging expertise, knowledge, and skills between experts across different domains
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class XpertXchange:
    def __init__(self):
        self.xperts = {}
        self.xchanges = {}
        self.collaborations = {}
        self.knowledge_resources = {}
        self.load_data()
    
    def load_data(self):
        """Load existing data from storage"""
        try:
            if os.path.exists('xperts.json'):
                with open('xperts.json', 'r') as f:
                    self.xperts = json.load(f)
            if os.path.exists('xchanges.json'):
                with open('xchanges.json', 'r') as f:
                    self.xchanges = json.load(f)
            if os.path.exists('collaborations.json'):
                with open('collaborations.json', 'r') as f:
                    self.collaborations = json.load(f)
            if os.path.exists('knowledge_resources.json'):
                with open('knowledge_resources.json', 'r') as f:
                    self.knowledge_resources = json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save data to storage"""
        try:
            with open('xperts.json', 'w') as f:
                json.dump(self.xperts, f, indent=2)
            with open('xchanges.json', 'w') as f:
                json.dump(self.xchanges, f, indent=2)
            with open('collaborations.json', 'w') as f:
                json.dump(self.collaborations, f, indent=2)
            with open('knowledge_resources.json', 'w') as f:
                json.dump(self.knowledge_resources, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_xpert(self, name, domains, skills, expertise_level="", bio=""):
        """Add a new expert to the platform"""
        xpert_id = f"xpert_{datetime.now().timestamp()}"
        self.xperts[xpert_id] = {
            "id": xpert_id,
            "name": name,
            "domains": domains,  # List of domains
            "skills": skills,      # List of skills
            "expertise_level": expertise_level,
            "bio": bio,
            "created_at": datetime.now().isoformat(),
            "xchanges": 0,
            "collaborations": 0
        }
        self.save_data()
        return xpert_id
    
    def search_xperts(self, domains=None, skills=None, expertise_level=None):
        """Search experts by criteria"""
        results = []
        
        for xpert_id, xpert in self.xperts.items():
            match = True
            
            if domains:
                domain_match = any(domain.lower() in [d.lower() for d in xpert.get("domains", [])] for domain in domains)
                if not domain_match:
                    match = False
            
            if skills:
                skill_match = any(skill.lower() in [s.lower() for s in xpert.get("skills", [])] for skill in skills)
                if not skill_match:
                    match = False
            
            if expertise_level and expertise_level.lower() != xpert.get("expertise_level", "").lower():
                match = False
            
            if match:
                results.append(xpert)
        
        return results
    
    def create_xchange(self, xpert1_id, xpert2_id, skill1, skill2, description):
        """Create a skill exchange between two experts"""
        if xpert1_id not in self.xperts or xpert2_id not in self.xperts:
            return None
        
        xchange_id = f"xchange_{datetime.now().timestamp()}"
        self.xchanges[xchange_id] = {
            "id": xchange_id,
            "xpert1_id": xpert1_id,
            "xpert2_id": xpert2_id,
            "skill1": skill1,  # Skill offered by xpert1
            "skill2": skill2,  # Skill offered by xpert2
            "description": description,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        # Update xpert exchange counts
        self.xperts[xpert1_id]["xchanges"] += 1
        self.xperts[xpert2_id]["xchanges"] += 1
        
        self.save_data()
        return xchange_id
    
    def update_xchange_status(self, xchange_id, status):
        """Update exchange status"""
        if xchange_id not in self.xchanges:
            return False
        
        self.xchanges[xchange_id]["status"] = status
        self.xchanges[xchange_id]["updated_at"] = datetime.now().isoformat()
        
        self.save_data()
        return True
    
    def create_collaboration(self, name, description, xpert_ids):
        """Create a new collaboration project"""
        collaboration_id = f"collab_{datetime.now().timestamp()}"
        self.collaborations[collaboration_id] = {
            "id": collaboration_id,
            "name": name,
            "description": description,
            "xpert_ids": xpert_ids,
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        
        # Update xpert collaboration counts
        for xpert_id in xpert_ids:
            if xpert_id in self.xperts:
                self.xperts[xpert_id]["collaborations"] += 1
        
        self.save_data()
        return collaboration_id
    
    def add_knowledge_resource(self, xpert_id, title, content, resource_type="article"):
        """Add a knowledge resource"""
        if xpert_id not in self.xperts:
            return None
        
        resource_id = f"resource_{datetime.now().timestamp()}"
        self.knowledge_resources[resource_id] = {
            "id": resource_id,
            "xpert_id": xpert_id,
            "title": title,
            "content": content,
            "resource_type": resource_type,
            "created_at": datetime.now().isoformat(),
            "views": 0
        }
        
        self.save_data()
        return resource_id
    
    def search_knowledge_resources(self, keywords=None, resource_type=None):
        """Search knowledge resources"""
        results = []
        
        for resource_id, resource in self.knowledge_resources.items():
            match = True
            
            if keywords:
                content = resource.get("title", "") + " " + resource.get("content", "")
                keyword_match = any(keyword.lower() in content.lower() for keyword in keywords)
                if not keyword_match:
                    match = False
            
            if resource_type and resource_type.lower() != resource.get("resource_type", "").lower():
                match = False
            
            if match:
                results.append(resource)
        
        return results
    
    def get_xpert_profile(self, xpert_id):
        """Get expert profile with exchanges and collaborations"""
        if xpert_id not in self.xperts:
            return None
        
        xpert = self.xperts[xpert_id].copy()
        
        # Get xpert's exchanges
        xpert_xchanges = []
        for xchange_id, xchange in self.xchanges.items():
            if xchange.get("xpert1_id") == xpert_id or xchange.get("xpert2_id") == xpert_id:
                xpert_xchanges.append(xchange)
        xpert["xchanges"] = xpert_xchanges
        
        # Get xpert's collaborations
        xpert_collaborations = []
        for collaboration_id, collaboration in self.collaborations.items():
            if xpert_id in collaboration.get("xpert_ids", []):
                xpert_collaborations.append(collaboration)
        xpert["collaborations"] = xpert_collaborations
        
        # Get xpert's knowledge resources
        xpert_resources = []
        for resource_id, resource in self.knowledge_resources.items():
            if resource.get("xpert_id") == xpert_id:
                xpert_resources.append(resource)
        xpert["resources"] = xpert_resources
        
        return xpert
    
    def match_xperts(self, required_skills):
        """Match experts based on required skills"""
        matches = []
        
        for xpert_id, xpert in self.xperts.items():
            xpert_skills = xpert.get("skills", [])
            # Calculate skill match percentage
            match_count = sum(1 for skill in required_skills if skill.lower() in [s.lower() for s in xpert_skills])
            match_percentage = (match_count / len(required_skills)) * 100 if required_skills else 0
            
            if match_percentage > 0:
                xpert_copy = xpert.copy()
                xpert_copy["match_percentage"] = match_percentage
                matches.append(xpert_copy)
        
        # Sort by match percentage
        matches.sort(reverse=True, key=lambda x: x.get("match_percentage", 0))
        
        return matches

def main():
    """Main function for testing the Xpert Xchange"""
    xchange = XpertXchange()
    
    # Add sample experts
    xpert1_id = xchange.add_xpert(
        "Dr. Jane Smith",
        ["Artificial Intelligence", "Computer Science"],
        ["Machine Learning", "Deep Learning", "NLP"],
        "Senior",
        "PhD in Computer Science with 10+ years of experience in AI research."
    )
    
    xpert2_id = xchange.add_xpert(
        "John Doe",
        ["Business Strategy", "Marketing"],
        ["Startup Consulting", "Market Analysis", "Digital Marketing"],
        "Mid-level",
        "MBA with 7 years of experience helping startups scale."
    )
    
    xpert3_id = xchange.add_xpert(
        "Dr. Maria Garcia",
        ["Healthcare", "Nutrition"],
        ["Preventive Medicine", "Nutrition Science"],
        "Senior",
        "MD with specialization in preventive healthcare and nutrition."
    )
    
    print("Added sample xperts:")
    for xpert_id, xpert in xchange.xperts.items():
        print(f"- {xpert['name']}: {', '.join(xpert['domains'])} - Skills: {', '.join(xpert['skills'])}")
    
    # Search xperts
    print("\nSearching for AI experts:")
    ai_xperts = xchange.search_xperts(domains=["Artificial Intelligence"])
    for xpert in ai_xperts:
        print(f"- {xpert['name']}: {', '.join(xpert['skills'])}")
    
    # Create skill exchange
    print("\nCreating skill exchange between Dr. Jane Smith and John Doe:")
    xchange_id = xchange.create_xchange(
        xpert1_id,
        xpert2_id,
        "Machine Learning",
        "Business Strategy",
        "Exchange AI expertise for business strategy advice"
    )
    print(f"Created exchange: {xchange.xchanges[xchange_id]['description']}")
    
    # Update exchange status
    xchange.update_xchange_status(xchange_id, "completed")
    print(f"Updated exchange status to: {xchange.xchanges[xchange_id]['status']}")
    
    # Create collaboration
    print("\nCreating collaboration project:")
    collaboration_id = xchange.create_collaboration(
        "AI Healthcare Project",
        "Develop AI solutions for healthcare",
        [xpert1_id, xpert3_id]
    )
    print(f"Created collaboration: {xchange.collaborations[collaboration_id]['name']}")
    
    # Add knowledge resource
    print("\nAdding knowledge resource:")
    resource_id = xchange.add_knowledge_resource(
        xpert1_id,
        "Introduction to Machine Learning",
        "Machine learning is a subset of artificial intelligence that focuses on building systems that learn from data...",
        "article"
    )
    print(f"Added resource: {xchange.knowledge_resources[resource_id]['title']}")
    
    # Search knowledge resources
    print("\nSearching for machine learning resources:")
    resources = xchange.search_knowledge_resources(keywords=["machine learning"])
    for resource in resources:
        print(f"- {resource['title']} by {xchange.xperts[resource['xpert_id']]['name']}")
    
    # Match xperts for required skills
    print("\nMatching xperts for AI and Healthcare skills:")
    matches = xchange.match_xperts(["Machine Learning", "Healthcare"])
    for match in matches:
        print(f"- {match['name']}: {match['match_percentage']:.1f}% match")
    
    # Get xpert profile
    print("\nDr. Jane Smith's profile:")
    profile = xchange.get_xpert_profile(xpert1_id)
    print(f"Name: {profile['name']}")
    print(f"Domains: {', '.join(profile['domains'])}")
    print(f"Skills: {', '.join(profile['skills'])}")
    print(f"Exchanges: {len(profile['xchanges'])}")
    print(f"Collaborations: {len(profile['collaborations'])}")
    print(f"Resources: {len(profile['resources'])}")

if __name__ == "__main__":
    main()
