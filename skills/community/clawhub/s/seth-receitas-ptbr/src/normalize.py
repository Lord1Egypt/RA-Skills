#!/usr/bin/env python3
"""
Normalize - Text normalization utilities for recipes
"""

import re
from typing import List, Dict


# Tag mappings for dietary restrictions
DIET_TAGS = {
    # Portuguese -> Tags
    "vegano": ["vegano", "vegana"],
    "vegetariano": ["vegetariano", "vegetariana"],
    "sem glúten": ["sem_gluten", "gluten_free"],
    "sem lactose": ["sem_lactose", "dairy_free"],
    "low carb": ["low_carb", "lowcarb"],
    "alta proteína": ["alta_proteina", "high_protein"],
    "cetogênica": ["keto", "cetogenica"],
    "diet": ["diet", "dietetico"],
    "light": ["light", "baixo_calorias"],
    "sem açúcar": ["sem_acucar", "sugar_free"],
    "frutos do mar": ["seafood", "frutos_do_mar"],
    "peixe": ["fish", "peixe"],
    "frango": ["chicken", "frango"],
    "carne": ["beef", "meat", "carne"],
    "porco": ["pork", "suíno", "porco"],
    "cordeiro": ["lamb", "cordeiro"],
}

# Brazilian measurements normalization
MEASUREMENTS = {
    "colher de sopa": ["colher de sopa", "colheres de sopa", "cs", "colher(es) de sopa"],
    "colher de chá": ["colher de chá", "colheres de chá", "cc", "colher(es) de chá"],
    "colher de café": ["colher de café", "colher(es) de café"],
    "xícara": ["xícara", "xícaras", "xíc", "xicara"],
    "copo": ["copo", "copos"],
    "pitada": ["pitada", "pitadas"],
    "punhado": ["punhado", "punhados"],
    "fatia": ["fatia", "fatias"],
    "unidade": ["unidade", "unidades", "un", "ud"],
    "grama": ["grama", "gramas", "g"],
    "quilograma": ["quilograma", "quilogramas", "kg"],
    "ml": ["ml", "mililitro", "mililitros"],
    "litro": ["litro", "litros", "l"],
    "tablete": ["tablete", "tabletes"],
    "envelope": ["envelope", "envelopes"],
}

# Portuguese ingredient variations
INGREDIENT_VARIATIONS = {
    "cebola": ["cebola", "cebola branca", "cebola roxa"],
    "alho": ["alho", "alho fresco"],
    "tomate": ["tomate", "tomate italiano", "tomate cereja"],
    "cenoura": ["cenoura", "cenouras"],
    "batata": ["batata", "batatas"],
    "farinha de trigo": ["farinha de trigo", "farinha", "farinha branca"],
    "açúcar": ["açúcar", "açúcar refinado", "açúcar cristal"],
    "óleo": ["óleo", "óleo de soja", "óleo vegetal"],
    "manteiga": ["manteiga", "manteiga sem sal"],
    "leite": ["leite", "leite integral"],
    "ovo": ["ovo", "ovos", "gema", "clara"],
    "fermento": ["fermento", "fermento biológico", "fermento químico"],
}


def normalize_text(text: str) -> str:
    """Basic text normalization"""
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep Portuguese accented
    text = re.sub(r'[^\w\sáéíóúàèìòùâêîôûãõç]', '', text)
    
    return text.strip()


def normalize_measurement(measure: str) -> str:
    """Normalize measurement to standard form"""
    if not measure:
        return ""
    
    measure = normalize_text(measure)
    
    for standard, variations in MEASUREMENTS.items():
        for var in variations:
            if var in measure:
                return standard
    
    return measure


def extract_tags(ingredients: List[str], title: str = "", instructions: str = "") -> List[str]:
    """Extract dietary tags from recipe content"""
    tags = set()
    
    all_text = " ".join(ingredients).lower() + " " + title.lower() + " " + instructions.lower()
    
    for tag, keywords in DIET_TAGS.items():
        for keyword in keywords:
            if keyword in all_text:
                # Use canonical tag name
                if tag == "vegano":
                    tags.add("vegano")
                elif tag == "vegetariano":
                    tags.add("vegetariano")
                elif "glúten" in tag or "gluten" in tag:
                    tags.add("sem_glúten")
                elif "lactose" in tag or "dairy" in tag:
                    tags.add("sem_lactose")
                elif "carb" in tag:
                    tags.add("low_carb")
                elif "proteína" in tag or "protein" in tag:
                    tags.add("alta_proteína")
                elif tag == "cetogênica":
                    tags.add("keto")
                break
    
    return list(tags)


def format_ingredient(ingredient: str, measure: str = "") -> str:
    """Format ingredient with measure"""
    ingredient = ingredient.strip()
    measure = measure.strip()
    
    if measure:
        return f"{measure} de {ingredient}"
    return ingredient


def parse_time(time_str: str) -> Dict[str, int]:
    """Parse time string to minutes"""
    if not time_str:
        return {"total_minutes": 0}
    
    time_str = time_str.lower()
    hours = 0
    minutes = 0
    
    # Extract hours
    hour_match = re.search(r'(\d+)\s*(?:hora|horas|h)', time_str)
    if hour_match:
        hours = int(hour_match.group(1))
    
    # Extract minutes
    min_match = re.search(r'(\d+)\s*(?:minuto|minutos|min)', time_str)
    if min_match:
        minutes = int(min_match.group(1))
    
    total = hours * 60 + minutes
    
    return {
        "hours": hours,
        "minutes": minutes,
        "total_minutes": total,
        "formatted": f"{hours}h {minutes}min" if hours > 0 else f"{minutes} min"
    }


def parse_yield(yield_str: str) -> str:
    """Parse yield string to standard form"""
    if not yield_str:
        return ""
    
    # Extract number
    num_match = re.search(r'(\d+)', yield_str)
    if num_match:
        num = num_match.group(1)
        
        # Check for "porções" or "pessoas"
        if "porção" in yield_str.lower() or "pessoa" in yield_str.lower():
            return f"{num} porções"
        elif "unidade" in yield_str.lower():
            return f"{num} unidades"
        elif "fatia" in yield_str.lower():
            return f"{num} fatias"
        elif "pedaço" in yield_str.lower():
            return f"{num} pedaços"
    
    return yield_str


def sanitize_for_output(text: str) -> str:
    """Sanitize text for clean output"""
    if not text:
        return ""
    
    # Remove references
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\[\w+\]', '', text)
    
    # Fix spacing
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()


# Test if run directly
if __name__ == "__main__":
    print("🧪 Testando normalizações:")
    
    # Test tags
    ingredients = ["3 cenouras", "4 ovos", "1 xícara de óleo"]
    title = "Bolo de Cenoura Vegano"
    tags = extract_tags(ingredients, title)
    print(f"  Tags: {tags}")
    
    # Test time
    time_parsed = parse_time("1 hora e 30 minutos")
    print(f"  Tempo: {time_parsed}")
    
    # Test yield
    yield_parsed = parse_yield("Serve 8 pessoas")
    print(f"  Rendimento: {yield_parsed}")
    
    # Test measurement
    measure_norm = normalize_measurement("2 colheres de sopa")
    print(f"  Medida normalizada: {measure_norm}")
