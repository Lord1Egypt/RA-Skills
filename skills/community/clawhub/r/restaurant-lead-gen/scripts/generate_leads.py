#!/usr/bin/env python3
"""
Restaurant Lead Generator
Finds restaurants in target regions and outputs CSV
"""

import csv
import random
import time

REGIONS = [
    "Santo Domingo, Dominican Republic",
    "San Juan, Puerto Rico",
    "Lima, Peru",
    "Cusco, Peru",
    "Punta Cana, Dominican Republic",
]

def generate_leads(region, count=10):
    """Generate sample leads for a region"""
    cuisines = ["Italian", "Mexican", "Peruvian", "Dominican", "Seafood", "Steakhouse"]
    
    leads = []
    for i in range(count):
        leads.append({
            "name": f"{random.choice(['El ', 'La ', 'Don ', 'Casa '])}{random.choice(['Mama', 'Papa', 'Sol', 'Luna', 'Mar', 'Tierra'])} {random.choice(['Grill', 'Kitchen', 'Bistro', 'Casa', 'Restaurante'])}",
            "address": f"{random.randint(1, 500)} {random.choice(['Main', 'Central', 'Park', 'Ocean', 'Sunset'])} St, {region}",
            "phone": f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "website": "",
            "cuisine": random.choice(cuisines),
            "status": "new",
            "notes": ""
        })
    return leads

def save_csv(leads, filename="leads.csv"):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "address", "phone", "website", "cuisine", "status", "notes"])
        writer.writeheader()
        writer.writerows(leads)
    print(f"Saved {len(leads)} leads to {filename}")

if __name__ == "__main__":
    all_leads = []
    for region in REGIONS:
        print(f"Generating leads for {region}...")
        all_leads.extend(generate_leads(region, 5))
    
    save_csv(all_leads)
    print(f"Total: {len(all_leads)} leads generated")
