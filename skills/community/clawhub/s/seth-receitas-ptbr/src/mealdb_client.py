#!/usr/bin/env python3
"""
TheMealDB Client - API client for themealdb.com
"""

import json
import urllib.request
import urllib.parse
from typing import List, Dict, Optional


class MealDBClient:
    BASE_URL = "https://www.themealdb.com/api/json/v1/1"
    
    # Mapeamento de traduções para pt-BR
    TRANSLATIONS = {
        # Categorias
        "Beef": "Carne Bovina",
        "Chicken": "Frango",
        "Dessert": "Sobremesa",
        "Lamb": "Cordeiro",
        "Miscellaneous": "Diversos",
        "Pasta": "Massa",
        "Pork": "Carne Suína",
        "Seafood": "Frutos do Mar",
        "Side": "Acompanhamento",
        "Starter": "Entrada",
        "Vegan": "Vegano",
        "Vegetarian": "Vegetariano",
        "Breakfast": "Café da Manhã",
        "Goat": "Cabra",
        
        # Áreas
        "American": "Americana",
        "British": "Britânica",
        "Canadian": "Canadense",
        "Chinese": "Chinesa",
        "Croatian": "Croata",
        "Dutch": "Holandesa",
        "Egyptian": "Egípcia",
        "Filipino": "Filipina",
        "French": "Francesa",
        "Greek": "Grega",
        "Indian": "Indiana",
        "Irish": "Irlandesa",
        "Italian": "Italiana",
        "Jamaican": "Jamaicana",
        "Japanese": "Japonesa",
        "Kenyan": "Queniana",
        "Malaysian": "Malaia",
        "Mexican": "Mexicana",
        "Moroccan": "Marroquina",
        "Polish": "Polonesa",
        "Portuguese": "Portuguesa",
        "Russian": "Russa",
        "Spanish": "Espanhola",
        "Thai": "Tailandesa",
        "Tunisian": "Tunisiana",
        "Turkish": "Turca",
        "Ukrainian": "Ucraniana",
        "Vietnamese": "Vietnamita",
        "Brazilian": "Brasileira",
        
        # Tags
        "Quick": "Rápido",
        "Easy": "Fácil",
        "Healthy": "Saudável",
        "Under 30 minutes": "Menos de 30 minutos",
        "Vegetarian": "Vegetariano",
        "Vegan": "Vegano",
        "Gluten Free": "Sem Glúten",
        "Dairy Free": "Sem Laticínios",
        "Keto": "Cetogênica",
        "Low Carb": "Low Carb",
        "High Protein": "Alta Proteína",
    }
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def _request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make request to TheMealDB API"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"
        
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"error": str(e)}
    
    def search(self, query: str) -> List[Dict]:
        """Search for meals by name"""
        result = self._request("search.php", {"s": query})
        
        if "error" in result:
            return []
        
        meals = result.get("meals")
        if not meals:
            return []
        
        return [self._translate_meal(m) for m in meals if m]
    
    def search_by_first_letter(self, letter: str) -> List[Dict]:
        """Search by first letter (max 1 result)"""
        if len(letter) != 1:
            letter = letter[0]
            
        result = self._request("search.php", {"f": letter})
        
        if "error" in result:
            return []
        
        meals = result.get("meals")
        if not meals:
            return []
        
        return [self._translate_meal(m) for m in meals if m]
    
    def get_by_id(self, meal_id: str) -> Optional[Dict]:
        """Get meal details by ID"""
        result = self._request("lookup.php", {"i": meal_id})
        
        if "error" in result:
            return None
        
        meals = result.get("meals")
        if not meals:
            return None
        
        return self._translate_meal(meals[0])
    
    def get_random(self) -> Optional[Dict]:
        """Get a random meal"""
        result = self._request("random.php")
        
        if "error" in result:
            return None
        
        meals = result.get("meals")
        if not meals:
            return None
        
        return self._translate_meal(meals[0])
    
    def get_categories(self) -> List[Dict]:
        """Get all meal categories"""
        result = self._request("categories.php")
        
        if "error" in result or "categories" not in result:
            return []
        
        categories = result.get("categories", [])
        return [
            {
                "name": c.get("strCategory", ""),
                "description": c.get("strCategoryDescription", ""),
                "image": c.get("strCategoryThumb", "")
            }
            for c in categories
        ]
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """Filter meals by category"""
        result = self._request("filter.php", {"c": category})
        
        if "error" in result:
            return []
        
        meals = result.get("meals")
        if not meals:
            return []
        
        return [
            {
                "id": m.get("idMeal", ""),
                "name": m.get("strMeal", ""),
                "image": m.get("strMealThumb", "")
            }
            for m in meals
        ]
    
    def filter_by_area(self, area: str) -> List[Dict]:
        """Filter meals by area/cuisine"""
        result = self._request("filter.php", {"a": area})
        
        if "error" in result:
            return []
        
        meals = result.get("meals")
        if not meals:
            return []
        
        return [
            {
                "id": m.get("idMeal", ""),
                "name": m.get("strMeal", ""),
                "image": m.get("strMealThumb", "")
            }
            for m in meals
        ]
    
    def filter_by_ingredient(self, ingredient: str) -> List[Dict]:
        """Filter meals by main ingredient"""
        result = self._request("filter.php", {"i": ingredient})
        
        if "error" in result:
            return []
        
        meals = result.get("meals")
        if not meals:
            return []
        
        return [
            {
                "id": m.get("idMeal", ""),
                "name": m.get("strMeal", ""),
                "image": m.get("strMealThumb", "")
            }
            for m in meals
        ]
    
    def _translate_meal(self, meal: Dict) -> Dict:
        """Translate meal data to pt-BR"""
        translated = meal.copy()
        
        # Translate category
        category = meal.get("strCategory", "")
        translated["strCategory"] = self.TRANSLATIONS.get(category, category)
        
        # Translate area
        area = meal.get("strArea", "")
        translated["strArea"] = self.TRANSLATIONS.get(area, area)
        
        # Translate tags
        tags = meal.get("strTags", "")
        if tags:
            tag_list = [t.strip() for t in tags.split(",")]
            translated_tags = [self.TRANSLATIONS.get(t, t) for t in tag_list]
            translated["strTags"] = ",".join(translated_tags)
        
        return translated
    
    def get_ingredients(self, meal: Dict) -> List[Dict]:
        """Extract ingredients and measures from meal"""
        ingredients = []
        
        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}", "").strip()
            measure = meal.get(f"strMeasure{i}", "").strip()
            
            if ingredient:
                ingredients.append({
                    "ingredient": ingredient,
                    "measure": measure
                })
        
        return ingredients


# Test if run directly
if __name__ == "__main__":
    client = MealDBClient()
    
    print("🔍 Testando busca...")
    results = client.search("chicken")
    for r in results[:3]:
        print(f"  - {r.get('strMeal', 'N/A')[:50]}")
    
    print("\n🎲 Testando random...")
    random_meal = client.get_random()
    if random_meal:
        print(f"  - {random_meal.get('strMeal', 'N/A')}")
    
    print("\n📂 Testando categorias...")
    categories = client.get_categories()
    for c in categories[:5]:
        print(f"  - {c['name']}")
