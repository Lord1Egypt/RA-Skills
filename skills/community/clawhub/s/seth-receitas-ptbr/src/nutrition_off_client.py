#!/usr/bin/env python3
"""
OpenFoodFacts Client - Optional nutrition information
Only used when user explicitly requests nutrition info
"""

import json
import urllib.request
import urllib.parse
from typing import Dict, List, Optional


class OpenFoodFactsClient:
    BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def _request(self, params: Dict) -> Optional[Dict]:
        """Make request to OpenFoodFacts API"""
        params["format"] = "json"
        params["json"] = 1
        params["page_size"] = 5
        
        query_string = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}?{query_string}"
        
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return None
    
    def search_ingredient(self, ingredient_name: str) -> List[Dict]:
        """Search for nutritional info of an ingredient"""
        params = {
            "search_terms": ingredient_name,
            "search_simple": 1,
            "action": "process",
            "fields": "product_name,nutriments,allergens_tags",
        }
        
        result = self._request(params)
        
        if not result or "products" not in result:
            return []
        
        products = result.get("products", [])
        
        nutrition_data = []
        for product in products:
            if not product:
                continue
            
            name = product.get("product_name", "")
            if not name:
                continue
            
            nutriments = product.get("nutriments", {})
            
            nutrition_data.append({
                "name": name,
                "calories": nutriments.get("energy-kcal_100g", nutriments.get("energy-kcal", 0)),
                "protein": nutriments.get("proteins_100g", nutriments.get("proteins", 0)),
                "carbs": nutriments.get("carbohydrates_100g", nutriments.get("carbohydrates", 0)),
                "fat": nutriments.get("fat_100g", nutriments.get("fat", 0)),
                "fiber": nutriments.get("fiber_100g", nutriments.get("fiber", 0)),
                "sugar": nutriments.get("sugars_100g", nutriments.get("sugars", 0)),
                "allergens": product.get("allergens_tags", []),
            })
        
        return nutrition_data
    
    def get_nutrition_estimate(self, ingredient_name: str) -> Optional[Dict]:
        """Get simplified nutrition estimate for an ingredient (per 100g)"""
        results = self.search_ingredient(ingredient_name)
        
        if not results:
            return None
        
        # Return first result (most relevant)
        return results[0]
    
    def format_nutrition(self, nutrition: Dict) -> str:
        """Format nutrition data for display"""
        if not nutrition:
            return "Não foi possível obter informações nutricionais."
        
        lines = []
        lines.append("📊 Informações nutricionais (por 100g):")
        
        if nutrition.get("calories"):
            lines.append(f"  • Calorias: {nutrition['calories']} kcal")
        if nutrition.get("protein"):
            lines.append(f"  • Proteína: {nutrition['protein']}g")
        if nutrition.get("carbs"):
            lines.append(f"  • Carboidratos: {nutrition['carbs']}g")
        if nutrition.get("fat"):
            lines.append(f"  • Gordura: {nutrition['fat']}g")
        if nutrition.get("fiber"):
            lines.append(f"  • Fibra: {nutrition['fiber']}g")
        if nutrition.get("sugar"):
            lines.append(f"  • Açúcar: {nutrition['sugar']}g")
        
        allergens = nutrition.get("allergens", [])
        if allergens:
            allergen_names = [a.replace("en:", "") for a in allergens[:3]]
            lines.append(f"  • Alergênicos: {', '.join(allergen_names)}")
        
        return "\n".join(lines)


# Test if run directly
if __name__ == "__main__":
    client = OpenFoodFactsClient()
    
    print("🔍 Testando busca de nutrição...")
    result = client.get_nutrition_estimate("avena")
    
    if result:
        print(f"  Produto: {result['name']}")
        print(client.format_nutrition(result))
    else:
        print("  Não encontrado")
