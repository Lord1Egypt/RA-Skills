#!/usr/bin/env python3
"""
Recipe Extractor - Extract structured recipes from Wikibooks HTML
Uses only stdlib html.parser
"""

import re
from html.parser import HTMLParser
from typing import Dict, List, Optional


class RecipeExtractor(HTMLParser):
    """Extract recipe sections from Wikibooks HTML"""
    
    def __init__(self):
        super().__init__()
        self.in_ingredients = False
        self.in_instructions = False
        self.current_section = None
        self.current_content = []
        self.ingredients = []
        self.instructions = []
        self.title = ""
        self.yield_info = ""
        self.time_info = ""
        self.section_depth = 0
        self.capture = False
        self.current_text = ""
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Headings
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._flush_text()
            self.capture = True
            self.current_text = ""
        
        # List items
        if tag == 'li' and (self.in_ingredients or self.in_instructions):
            self.current_text = ""
        
        # Section detection
        if tag == 'span':
            class_attr = attrs_dict.get('class', '')
            if 'mw-headline' in class_attr:
                self._flush_text()
    
    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._flush_text()
            self.capture = False
        
        if tag == 'li' and self.current_text.strip():
            text = self.current_text.strip()
            if self.in_ingredients:
                if text and not text.startswith('<'):
                    self.ingredients.append(text)
            elif self.in_instructions:
                if text and not text.startswith('<'):
                    self.instructions.append(text)
            self.current_text = ""
        
        if tag == 'p' and self.current_text.strip():
            self._flush_text()
    
    def handle_data(self, data):
        if self.capture:
            self.current_text += data
    
    def _flush_text(self):
        text = self.current_text.strip()
        if not text:
            return
        
        text_lower = text.lower()
        
        # Detect sections
        if any(word in text_lower for word in ['ingrediente', 'ingredientes']):
            self.in_ingredients = True
            self.in_instructions = False
            self.current_section = 'ingredients'
        elif any(word in text_lower for word in ['modo de preparo', 'preparação', 'prepare', 'receita']):
            self.in_ingredients = False
            self.in_instructions = True
            self.current_section = 'instructions'
        elif any(word in text_lower for word in ['rendimento', 'porção', 'porções', 'serve']):
            self.yield_info = text
        elif any(word in text_lower for word in ['tempo', 'minutos', 'horas']):
            self.time_info = text
        elif any(word in text_lower for word in ['título', 'nome']):
            self.title = text
        
        self.current_text = ""
    
    def get_recipe(self) -> Dict:
        """Get extracted recipe data"""
        return {
            "title": self.title,
            "yield": self._clean_text(self.yield_info),
            "time": self._clean_text(self.time_info),
            "ingredients": [self._clean_text(i) for i in self.ingredients if i],
            "instructions": [self._clean_text(i) for i in self.instructions if i]
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove references like [1], [2]
        text = re.sub(r'\[\d+\]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


def extract_from_html(html: str) -> Dict:
    """Extract recipe from Wikibooks HTML content"""
    parser = RecipeExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass
    
    return parser.get_recipe()


def normalize_ingredient(ingredient: str) -> Dict:
    """Normalize an ingredient string"""
    ingredient = ingredient.strip().lower()
    
    # Common measurements
    measurements = [
        'colher', 'colheres', 'copo', 'copos', 'xícara', 'xícaras',
        'pitada', 'pitadas', 'punhado', 'punhados', 'fatia', 'fatias',
        'unidade', 'unidades', 'grama', 'gramas', 'kg', 'ml', 'litro', 'litros',
        'teaspoon', 'tablespoon', 'cup', 'oz', 'lb'
    ]
    
    measure = ""
    name = ingredient
    
    for m in measurements:
        if ingredient.startswith(m):
            measure = m
            name = ingredient[len(m):].strip()
            break
    
    # Clean name
    name = re.sub(r'^de\s+', '', name)
    name = re.sub(r'^da\s+', '', name)
    name = re.sub(r'^do\s+', '', name)
    
    return {
        "original": ingredient,
        "measure": measure,
        "name": name.strip()
    }


# Test if run directly
if __name__ == "__main__":
    # Test with sample
    sample_html = """
    <h2>Ingredientes</h2>
    <ul>
    <li>3 cenouras médias raladas</li>
    <li>4 ovos</li>
    <li>1 xícara de óleo</li>
    <li>2 xícaras de açúcar</li>
    </ul>
    <h2>Modo de preparo</h2>
    <ol>
    <li>Preaqueça o forno a 180°C.</li>
    <li>Bata no liquidificador as cenouras, os ovos e o óleo.</li>
    <li>Asse por aproximadamente 40 minutos.</li>
    </ol>
    """
    
    recipe = extract_from_html(sample_html)
    print("🍰 Receita extraída:")
    print(f"  Título: {recipe.get('title', 'N/A')}")
    print(f"  Rendimento: {recipe.get('yield', 'N/A')}")
    print(f"  Tempo: {recipe.get('time', 'N/A')}")
    print(f"  Ingredientes ({len(recipe.get('ingredients', []))}):")
    for i in recipe.get('ingredients', [])[:3]:
        print(f"    - {i}")
    print(f"  Modo de preparo ({len(recipe.get('instructions', []))}):")
    for i in recipe.get('instructions', [])[:3]:
        print(f"    {i}")
