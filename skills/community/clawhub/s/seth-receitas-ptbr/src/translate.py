#!/usr/bin/env python3
"""
Receita.com.br Client - Brazilian recipe API alternative
"""

import json
import urllib.request
import urllib.parse
from typing import List, Dict, Optional


class ReceitaClient:
    """Client for Brazilian recipe sources"""
    
    # Translation dict for common Brazilian ingredients/dishes
    TRANSLATIONS_PT_EN = {
        # Common dishes
        "yakisoba": "stir fry noodles",
        "moqueca": "brazilian fish stew",
        "feijoada": "brazilian black bean stew",
        "vatapá": "brazilian shrimp paste",
        "acarajé": "brazilian fritter",
        "pão de queijo": "brazilian cheese bread",
        "bolo de cenoura": "carrot cake",
        "brigadeiro": "brazilian chocolate truffle",
        "beijinho": "brazilian coconut truffle",
        "coxinha": "brazilian chicken croquette",
        "pastel": "brazilian fried pastry",
        "esfiha": "brazilian meat pie",
        "chu pastry": "churros",
        "tapioca": "brazilian tapioca crepe",
        "açaí": "acai bowl",
        "caipirinha": "brazilian cocktail",
        "arroz de Carreteiro": "brazilian dried beef rice",
        "arroz biro biro": "brazilian pork rice",
        "galinhada": "brazilian chicken rice",
        "guarana": "guarana soda",
        
        # Ingredients
        "frango": "chicken",
        "carne bovina": "beef",
        "carne moída": "ground beef",
        "porco": "pork",
        "coração": "chicken heart",
        "linguiça": "sausage",
        "bacon": "bacon",
        "presunto": "ham",
        "queijo": "cheese",
        "mussarela": "mozzarella",
        "parmesão": "parmesan",
        "requeijão": "cream cheese",
        "creme de leite": "heavy cream",
        "leite de coco": "coconut milk",
        "coco": "coconut",
        "batata": "potato",
        "batata palha": "fried potato sticks",
        "cebola": "onion",
        "alho": "garlic",
        "tomate": "tomato",
        "pimentão": "bell pepper",
        "cenoura": "carrot",
        "brócolis": "broccoli",
        "espinafre": "spinach",
        "repolho": "cabbage",
        "vagem": "green beans",
        "ervilha": "peas",
        "milho": "corn",
        "azeitona": "olive",
        "pepino": "cucumber",
        "alface": "lettuce",
        "maionese": "mayonnaise",
        "ketchup": "ketchup",
        "mostarda": "mustard",
        "shoyu": "soy sauce",
        "molho de soja": "soy sauce",
        "óleo de gergelim": "sesame oil",
        "gengibre": "ginger",
        "limão": "lemon",
        "limão siciliano": "lime",
        "laranja": "orange",
        "abacate": "avocado",
        "banana": "banana",
        "morango": "strawberry",
        "manga": "mango",
        "abacaxi": "pineapple",
        "goiabada": "guava paste",
        "doce de leite": "dulce de leche",
        "açúcar": "sugar",
        "farinha de trigo": "flour",
        "fermento": "yeast",
        "fermento químico": "baking powder",
        "ovo": "egg",
        "manteiga": "butter",
        "óleo": "oil",
        "leite": "milk",
        "café": "coffee",
        "chocolate": "chocolate",
        "cacau": "cocoa",
        "aveia": "oats",
        "mel": "honey",
        "nozes": "walnuts",
        "amendoim": "peanut",
        "castanha": "cashew",
        "amêndoas": "almonds",
        
        # Cooking methods
        "refogar": "saute",
        "fritar": "fry",
        "assar": "bake",
        "grelhar": "grill",
        "cozinhar": "cook",
        "ferver": "boil",
        "misturar": "mix",
        "bater": "beat",
        "emulgelar": "blend",
    }
    
    @staticmethod
    def translate_to_english(text: str) -> str:
        """Translate Portuguese terms to English for API search"""
        text_lower = text.lower()
        
        # Try exact match first
        if text_lower in ReceitaClient.TRANSLATIONS_PT_EN:
            return ReceitaClient.TRANSLATIONS_PT_EN[text_lower]
        
        # Try to find any known term in the text
        for pt_term, en_term in sorted(ReceitaClient.TRANSLATIONS_PT_EN.items(), key=lambda x: len(x[0]), reverse=True):
            if pt_term in text_lower:
                return en_term
        
        # Return original if no translation found
        return text
    
    @staticmethod
    def translate_to_portuguese(text: str) -> str:
        """Translate common English terms back to Portuguese for display"""
        translations_en_pt = {v: k for k, v in ReceitaClient.TRANSLATIONS_PT_EN.items()}
        
        text_lower = text.lower()
        
        # Try exact match
        if text_lower in translations_en_pt:
            return translations_en_pt[text_lower]
        
        # Try partial match
        for en_term, pt_term in sorted(translations_en_pt.items(), key=lambda x: len(x[0]), reverse=True):
            if en_term in text_lower:
                return pt_term
        
        return text


# Test if run directly
if __name__ == "__main__":
    client = ReceitaClient()
    
    print("🔄 Testando traduções PT→EN:")
    tests = ["yakisoba", "frango", "bolo de cenoura", "pão de queijo", "brócolis"]
    for t in tests:
        print(f"  {t} → {client.translate_to_english(t)}")
    
    print("\n🔄 Testando traduções EN→PT:")
    tests2 = ["stir fry", "chicken", "carrot cake", "cheese"]
    for t in tests2:
        print(f"  {t} → {client.translate_to_portuguese(t)}")
