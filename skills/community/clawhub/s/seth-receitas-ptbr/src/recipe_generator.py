#!/usr/bin/env python3
"""
Recipe Generator - Generate original recipes when APIs don't have results
"""

import random
from typing import List, Dict


class RecipeGenerator:
    """Generate original Brazilian recipes"""
    
    # Brazilian cooking techniques
    TECHNIQUES = [
        "Refogue em fogo médio",
        "Cozinhe em fogo baixo",
        "Frite em óleo quente",
        "Asse em forno preaquecido",
        "Grelhe em frigideira quente",
        "Misture bem todos os ingredientes",
        "Deixe descansar por 10 minutos",
        "Coe antes de servir",
    ]
    
    # Common Brazilian measurements
    MEASUREMENTS = [
        "1 xícara",
        "2 colheres de sopa",
        "1 colher de chá",
        "meia xícara",
        "3 colheres de sopa",
        "1 pitada",
        "a gosto",
    ]
    
    @staticmethod
    def generate_recipe(ingredients: List[str], restrictions: str = "", dish_name: str = "") -> Dict:
        """Generate an original recipe based on ingredients"""
        
        # Check for recognized Brazilian dishes first
        dish_name_lower = dish_name.lower() if dish_name else ""
        
        # Known Brazilian/Japanese dishes
        if "yakisoba" in dish_name_lower:
            return RecipeGenerator._generate_yakisoba(ingredients, restrictions)
        elif "feijoada" in dish_name_lower:
            return RecipeGenerator._generate_feijoada(ingredients, restrictions)
        elif "moqueca" in dish_name_lower:
            return RecipeGenerator._generate_moqueca(ingredients, restrictions)
        elif "pf" in dish_name_lower or "prato_feito" in dish_name_lower:
            return RecipeGenerator._generate_prato_feito(ingredients, restrictions)
        
        # Parse restrictions
        is_vegan = "vegan" in restrictions.lower() or "vegano" in restrictions.lower()
        is_vegetarian = "vegetariano" in restrictions.lower() or "vegetarian" in restrictions.lower()
        is_gluten_free = "gluten" in restrictions.lower() or "sem_gluten" in restrictions.lower()
        is_lactose_free = "lactose" in restrictions.lower() or "sem_lactose" in restrictions.lower()
        is_low_carb = "low carb" in restrictions.lower() or "lowcarb" in restrictions.lower()
        
        # Determine dish type based on ingredients
        ingredients_lower = [i.lower() for i in ingredients]
        
        if any(i in ingredients_lower for i in ["macarrão", "massa", "noodle", "espaguete", "lasanha"]):
            dish_type = "massa"
        elif any(i in ingredients_lower for i in ["arroz", "arroz branco"]):
            dish_type = "arroz"
        elif any(i in ingredients_lower for i in ["frango", "galinha"]):
            dish_type = "frango"
        elif any(i in ingredients_lower for i in ["carne", "bife", "contrafilé", "alcatra", "picanha"]):
            dish_type = "carne"
        elif any(i in ingredients_lower for i in ["feijão", "feijoada"]):
            dish_type = "feijão"
        elif any(i in ingredients_lower for i in ["bolo", "biscoito", "doce", "sobremesa"]):
            dish_type = "doce"
        else:
            dish_type = "geral"
        
        # Generate recipe based on type
        recipe = RecipeGenerator._generate_by_type(dish_type, ingredients, is_vegan, is_vegetarian)
        
        # Add tags
        tags = []
        if is_vegan:
            tags.append("vegano")
        elif is_vegetarian:
            tags.append("vegetariano")
        if is_gluten_free:
            tags.append("sem_glúten")
        if is_lactose_free:
            tags.append("sem_lactose")
        if is_low_carb:
            tags.append("low_carb")
        
        recipe["tags"] = tags
        recipe["source"] = "original"
        
        return recipe
    
    @staticmethod
    def _generate_by_type(dish_type: str, ingredients: List[str], is_vegan: bool, is_vegetarian: bool) -> Dict:
        """Generate recipe based on dish type"""
        
        if dish_type == "massa":
            return RecipeGenerator._generate_pasta_recipe(ingredients, is_vegan)
        elif dish_type == "arroz":
            return RecipeGenerator._generate_rice_recipe(ingredients, is_vegan)
        elif dish_type == "frango":
            return RecipeGenerator._generate_chicken_recipe(ingredients, is_vegan)
        elif dish_type == "carne":
            return RecipeGenerator._generate_beef_recipe(ingredients, is_vegan)
        elif dish_type == "feijão":
            return RecipeGenerator._generate_bean_recipe(ingredients, is_vegan)
        elif dish_type == "doce":
            return RecipeGenerator._generate_dessert_recipe(ingredients)
        else:
            return RecipeGenerator._generate_general_recipe(ingredients, is_vegan)
    
    @staticmethod
    def _generate_yakisoba(ingredients: List[str], restrictions: str) -> Dict:
        """Generate a proper yakisoba recipe"""
        
        # Use provided ingredients or default
        if ingredients and len(ingredients) > 0 and len(ingredients[0]) > 3:
            ing_list = ingredients
        else:
            ing_list = [
                "300g de macarrão para yakisoba ou macarrão oriental",
                "300g de frango em tiras (ou carne/bacon)",
                "1 xícara de brócolis em floretes",
                "1 cenoura em rodelas",
                "1 pimentão em tiras",
                "1 cebola em rodelas",
                "3 dentes de alho picados",
                "4 colheres de sopa de molho de soja (shoyu)",
                "1 colher de sopa de óleo de gergelim",
                "1 colher de sopa de amido de milho",
                "Sal e pimenta a gosto",
                "Óleo para fritar"
            ]
        
        return {
            "title": "🍜 Yakisoba",
            "yield": "4 porções",
            "time": "30 minutos",
            "ingredients": ing_list,
            "instructions": [
                "🥢 Cozinhe o macarrão conforme instruções da embalagem (al dente). Escorra e reserve.",
                "🥢 Tempere o frango com sal, pimenta e alho. Deixe marinar 10 minutos.",
                "🥢 Em uma wok ou frigideira grande, aqueça bastante óleo e frite o frango em lotes até dourar. Reserve.",
                "🥢 Na mesma wok, adicione um pouco mais de óleo e refogue a cebola até translúcida.",
                "🥢 Adicione a cenoura e o brócolis, refogue por 2-3 minutos (deve ficar crocante).",
                "🥢 Junte o pimentão e o frango reservado. Misture tudo.",
                "🥢 Adicione o shoyu e o óleo de gergelim. Misture bem.",
                "🥢 Acrescente o amido de milho dissolvido em um pouco de água para engrossar o molho.",
                "🥢 Finalize com o macarrão, misturando rapidamente para não quebrar.",
                "🥢 Sirva quente, optionally com batata palha por cima.",
            ],
        }
    
    @staticmethod
    def _generate_feijoada(ingredients: List[str], restrictions: str) -> Dict:
        """Generate a feijoada recipe"""
        
        return {
            "title": "🍖 Feijoada Completa",
            "yield": "6 porções",
            "time": "2 horas",
            "ingredients": [
                "500g de feijão preto",
                "300g de carne seca",
                "200g de bacon",
                "200g de linguiça calabresa",
                "200g de pork belly (barriga de porco)",
                "2 cebolas picadas",
                "4 dentes de alho picados",
                "2 folhas de louro",
                "Sal e pimenta a gosto",
                "Para servir: arroz branco, couve refogada, laranja, farofa",
            ],
            "instructions": [
                "🥘 Deixe a carne seca de molho por 12 horas (troque a água 3x).",
                "🥘 Cozinhe o feijão na pressão por 30 minutos.",
                "🥘 Em outra panela, frite o bacon até soltar a gordura.",
                "🥘 Adicione a linguiça e frite até dourar.",
                "🥘 Junte a carne seca (já dessalgada) e o pork belly.",
                "🥘 Refogue cebola e alho, adicione ao feijão.",
                "🥘 Misture tudo e cozinhe por mais 1 hora em fogo baixo.",
                "🥘 Tempere com sal, pimenta e louro.",
                "🥘 Sirva com arroz, couve refogada, laranja e farofa.",
            ],
        }
    
    @staticmethod
    def _generate_moqueca(ingredients: List[str], restrictions: str) -> Dict:
        """Generate a moqueca recipe"""
        
        is_fish = "peixe" in restrictions.lower() or "peixe" in str(ingredients).lower()
        
        protein = "peixe" if is_fish else "camarão"
        
        return {
            "title": "🐟 Moqueca Brasileira",
            "yield": "4 porções",
            "time": "45 minutos",
            "ingredients": [
                f"500g de {protein} em Postes",
                "1 vidro de leite de coco",
                "1 xícara de azeite de dendê",
                "2 tomates em rodelas",
                "2 cebolas em rodelas",
                "1 pimentão em rodelas",
                "4 dentes de alho picados",
                "Suco de 2 limões",
                "Coentro e salsinha",
                "Sal e pimenta",
            ],
            "instructions": [
                "🐟 Tempere o {protein} com alho, sal, pimenta e limão. Deixe marinar 20 minutos.",
                "🐟 Em uma panela de barro ou fundo grosso, faça camadas: cebola, tomate, pimentão, {protein}.",
                "🐟 Repita as camadas e finalize com tomate.",
                "🐟 Regue com azeite de dendê e leite de coco.",
                "🐟 Cozinhe em fogo baixo por 25 minutos (sem mexer).",
                "🐟 Finalize com coentro e salsinha picados.",
                "🐟 Sirva com arroz branco e pirão.",
            ],
        }
    
    @staticmethod
    def _generate_prato_feito(ingredients: List[str], restrictions: str) -> Dict:
        """Generate a PF (prato feito) recipe"""
        
        return {
            "title": "🍱 Prato Feito (PF)",
            "yield": "1 porção",
            "time": "25 minutos",
            "ingredients": [
                "1 xícara de arroz branco",
                "1 ovo",
                "100g de carne moída (ou frango/des OSS)",
                "1/2 xícara de feijão tropeiro ou Carijó",
                "1/2 xícara de legumes refogados (batata, cenoura, vagem)",
                "1 colher de sopa de azeite",
                "Sal, alho e cebola a gosto",
            ],
            "instructions": [
                "🍱 Cozinhe o arroz branco Reserve.",
                "🍱 Em uma frigideira, frite o ovo (ou omelete). Reserve.",
                "🍱 Na mesma frigideira, refogue a carne moída com alho, cebola, sal e temperos.",
                "🍱 Aqueça o feijão (ou cozinhe se for feijão seco).",
                "🍱 Em outra panela, refogue os legumes em azeite.",
                "🍱 Monte o prato: arroz no centro, feijão ao lado, carne, ovo e legumes.",
                "🍱 Sirva imediatamente!",
            ],
        }
    
    @staticmethod
    def _generate_pasta_recipe(ingredients: List[str], is_vegan: bool) -> Dict:
        """Generate a pasta recipe"""
        
        # Determine sauce type
        has_tomato = any("tomate" in i.lower() for i in ingredients)
        has_cream = any("creme" in i.lower() or "leite" in i.lower() for i in ingredients)
        
        if has_tomato:
            sauce = "molho de tomate caseiro"
            steps = [
                "Em uma panela, aqueça o azeite e refogue o alho até dourar.",
                "Adicione o tomate picado e cozinhe por 10 minutos.",
                "Tempere com sal, orégano e manjericão.",
                "Cozinhe o macarrão conforme instruções da embalagem.",
                "Misture o macarrão com o molho e sirva quente.",
            ]
        elif has_cream:
            sauce = "molho cremoso"
            steps = [
                "Em uma frigideira, derreta a manteiga.",
                "Adicione o alho e refogue por 1 minuto.",
                "Junte o creme de leite e misture bem.",
                "Tempere com sal, pimenta e noz-moscada.",
                "Cozinhe o macarrão e misture com o molho.",
            ]
        else:
            sauce = "molho simples"
            steps = [
                "Aqueça azeite em uma frigideira grande.",
                "Refogue os vegetais selecionados.",
                "Adicione o alho e tempere.",
                "Cozinhe o macarrão al dente.",
                "Misture tudo e finalize com queijo ralado.",
            ]
        
        # Generate title
        protein = ""
        for i in ingredients:
            i_lower = i.lower()
            if any(p in i_lower for p in ["frango", "carne", "presunto", "bacon", "atum"]):
                protein = i
                break
        
        title = f"Macarrão com {protein}" if protein else "Macarrão Simples"
        
        return {
            "title": title,
            "yield": "4 porções",
            "time": "25 minutos",
            "ingredients": ingredients,
            "instructions": steps,
        }
    
    @staticmethod
    def _generate_rice_recipe(ingredients: List[str], is_vegan: bool) -> Dict:
        """Generate a rice recipe"""
        
        has_beans = any("feijão" in i.lower() for i in ingredients)
        has_meat = any("carne" in i.lower() or "frango" in i.lower() for i in ingredients)
        
        if has_beans:
            title = "Arroz com Feijão"
            steps = [
                "Cozinhe o arroz branco Reserve.",
                "Em outra panela, aqueça azeite.",
                "Refogue cebola e alho.",
                "Adicione o feijão cozido.",
                "Misture o arroz e tempere.",
            ]
        elif has_meat:
            title = "Arroz de Frango (ou Carne)"
            steps = [
                "Tempere a proteína e cozinhe.",
                "Reserve a proteína cozida.",
                "Na mesma panela, refogue cebola e alho.",
                "Adicione o arroz e água.",
                "Quando o arroz estiver quase pronto, adicione a proteína.",
            ]
        else:
            title = "Arroz Branco Simples"
            steps = [
                "Lave o arroz em água corrente.",
                "Aqueça azeite em uma panela.",
                "Refogue cebola e alho.",
                "Adicione o arroz e a água quente.",
                "Cozinhe em fogo baixo até ficar macio.",
            ]
        
        return {
            "title": title,
            "yield": "4 porções",
            "time": "30 minutos",
            "ingredients": ingredients,
            "instructions": steps,
        }
    
    @staticmethod
    def _generate_chicken_recipe(ingredients: List[str], is_vegan: bool) -> Dict:
        """Generate a chicken recipe"""
        
        return {
            "title": "Frango ao Estilo Brasileiro",
            "yield": "4 porções",
            "time": "45 minutos",
            "ingredients": ingredients,
            "instructions": [
                "Corte o frango em pedaços e tempere com sal, pimenta e alho.",
                "Deixe marinar por 15 minutos.",
                "Em uma frigideira grande, aqueça óleo.",
                "Doure o frango de todos os lados.",
                "Adicione cebola e pimentão.",
                "Junte os outros ingredientes e cozinhe por 20 minutos.",
                "Sirva quente com arroz e salada.",
            ],
        }
    
    @staticmethod
    def _generate_beef_recipe(ingredients: List[str], is_vegan: bool) -> Dict:
        """Generate a beef recipe"""
        
        return {
            "title": "Carne na Panela",
            "yield": "4 porções",
            "time": "1 hora",
            "ingredients": ingredients,
            "instructions": [
                "Tempere a carne com sal, pimenta e alho.",
                "Em uma panela de pressão, aqueça óleo.",
                "Selle a carne de todos os lados.",
                "Adicione cebola, alho e tomate.",
                "Acrescente água até cobrir a carne.",
                "Cozinhe por 30 minutos após pegar pressão.",
                "Finalize com batata e cenoura.",
            ],
        }
    
    @staticmethod
    def _generate_bean_recipe(ingredients: List[str], is_vegan: bool) -> Dict:
        """Generate a bean recipe"""
        
        return {
            "title": "Feijão Tropeiro Estilo Mineiro",
            "yield": "6 porções",
            "time": "1 hora",
            "ingredients": ingredients,
            "instructions": [
                "Cozinhe o feijão até ficar macio.",
                "Em uma frigideira, frite o bacon até ficar crocante.",
                "Adicione a linguiça fatiada.",
                "Junte a cebola e o alho refogados.",
                "Misture o feijão cozido.",
                "Finalize com couve fatiada e temperos.",
            ],
        }
    
    @staticmethod
    def _generate_dessert_recipe(ingredients: List[str]) -> Dict:
        """Generate a dessert recipe"""
        
        has_chocolate = any("chocolate" in i.lower() or "cacau" in i.lower() for i in ingredients)
        has_fruit = any(i.lower() in ["banana", "morango", "manga", "abacaxi", "maçã"] for i in ingredients)
        
        if has_chocolate:
            title = "Bolo de Chocolate Brasileiro"
            time_recipe = "50 minutos"
        elif has_fruit:
            title = "Torta de Frutas"
            time_recipe = "40 minutos"
        else:
            title = "Bolo Simples"
            time_recipe = "35 minutos"
        
        return {
            "title": title,
            "yield": "8 porções",
            "time": time_recipe,
            "ingredients": ingredients,
            "instructions": [
                "Preaqueça o forno a 180°C.",
                "Misture os ingredientes secos em uma tigela.",
                "Bata os ovos com o açúcar e manteiga.",
                "Gradualmente adicione os ingredientes secos.",
                "Despeje na forma untada.",
                "Asse até dourar (teste com palito).",
            ],
        }
    
    @staticmethod
    def _generate_general_recipe(ingredients: List[str], is_vegan: bool) -> Dict:
        """Generate a general recipe"""
        
        # Count main ingredients to determine complexity
        main_count = sum(1 for i in ingredients if len(i) > 10)
        
        if main_count <= 3:
            title = "Prato Rápido"
            time_recipe = "20 minutos"
        elif main_count <= 5:
            title = "Prato Principal"
            time_recipe = "40 minutos"
        else:
            title = "Prato Completo"
            time_recipe = "1 hora"
        
        return {
            "title": title,
            "yield": "4 porções",
            "time": time_recipe,
            "ingredients": ingredients,
            "instructions": [
                "Prepare todos os ingredientes.",
                "Aqueça uma panela ou frigideira grande.",
                "Adicione o ingrediente principal.",
                "Refogue os vegetais.",
                "Tempere a gosto.",
                "Cozinhe até ficar no ponto.",
                "Sirva quente.",
            ],
        }


# Test if run directly
if __name__ == "__main__":
    generator = RecipeGenerator()
    
    print("🧪 Testando geração de receitas:\n")
    
    # Test yakisoba
    ingredients = ["macarrão", "frango", "brócolis", "cenoura", "molho de soja", "óleo de gergelim"]
    recipe = generator.generate_recipe(ingredients)
    
    print(f"🍜 {recipe['title']}")
    print(f"⏱️ {recipe['time']} | {recipe['yield']}")
    print(f"\n📝 Ingredientes:")
    for i in recipe['ingredients']:
        print(f"  - {i}")
    print(f"\n👨‍🍳 Modo de preparo:")
    for j, step in enumerate(recipe['instructions'], 1):
        print(f"  {j}. {step}")
    print(f"\n🏷️ Tags: {', '.join(recipe['tags'])}")
    print(f"📦 Fonte: {recipe['source']}")
