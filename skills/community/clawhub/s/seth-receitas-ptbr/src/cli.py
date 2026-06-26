#!/usr/bin/env python3
"""
CLI - Command Line Interface for seth_receitas_ptbr
Main entry point for the skill
"""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wikibooks_client import WikibooksClient
from mealdb_client import MealDBClient
from recipe_extract import extract_from_html, normalize_ingredient
from normalize import extract_tags, parse_time, parse_yield, sanitize_for_output
from nutrition_off_client import OpenFoodFactsClient
from cache import Cache
from translate import ReceitaClient
from recipe_generator import RecipeGenerator


# Initialize clients
wikibooks = WikibooksClient()
mealdb = MealDBClient()
nutrition = OpenFoodFactsClient()
cache = Cache()
translator = ReceitaClient()
generator = RecipeGenerator()


def format_recipe_meal(recipe: dict) -> str:
    """Format TheMealDB recipe for output"""
    lines = []
    
    # Title
    title = recipe.get("strMeal", "Receita sem título")
    lines.append(f"🍽️ {title}")
    lines.append("")
    
    # Category and Area
    category = recipe.get("strCategory", "")
    area = recipe.get("strArea", "")
    if category or area:
        info = []
        if category:
            info.append(category)
        if area:
            info.append(area)
        lines.append(f"📋 {' | '.join(info)}")
        lines.append("")
    
    # Image
    image = recipe.get("strMealThumb", "")
    if image:
        lines.append(f"🖼️ Imagem: {image}")
        lines.append("")
    
    # Ingredients
    ingredients = mealdb.get_ingredients(recipe)
    if ingredients:
        lines.append("📝 Ingredientes:")
        for i, ing in enumerate(ingredients, 1):
            measure = ing.get("measure", "").strip()
            name = ing.get("ingredient", "").strip()
            if measure and name:
                lines.append(f"  {i}. {measure} de {name}")
            elif name:
                lines.append(f"  {i}. {name}")
        lines.append("")
    
    # Instructions
    instructions = recipe.get("strInstructions", "")
    if instructions:
        lines.append("👨‍🍳 Modo de preparo:")
        # Split by capital letters or numbered steps
        steps = instructions.split("\r\n")
        for i, step in enumerate(steps, 1):
            step = sanitize_for_output(step)
            if step and len(step) > 5:
                lines.append(f"  {i}. {step}")
        lines.append("")
    
    # Tags
    tags_str = recipe.get("strTags", "")
    if tags_str:
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        if tags:
            tag_icons = []
            for tag in tags:
                tag_lower = tag.lower()
                if "vegan" in tag_lower:
                    tag_icons.append("🌱")
                elif "veget" in tag_lower:
                    tag_icons.append("🥬")
                elif "gluten" in tag_lower:
                    tag_icons.append("🚫")
                elif "carb" in tag_lower:
                    tag_icons.append("🍞")
                else:
                    tag_icons.append("🏷️")
            lines.append(f"{' '.join(tag_icons)} Tags: {', '.join(tags)}")
            lines.append("")
    
    # Source
    source_url = recipe.get("strSource", "")
    youtube = recipe.get("strYoutube", "")
    
    lines.append("📦 Fonte: TheMealDB")
    if source_url:
        lines.append(f"🔗 URL: {source_url}")
    if youtube:
        lines.append(f"▶️ YouTube: {youtube}")
    lines.append(f"🆔 ID: {recipe.get('idMeal', 'N/A')}")
    
    return "\n".join(lines)


def format_recipe_wikibooks(title: str, html: str, url: str) -> str:
    """Format Wikibooks recipe for output"""
    recipe = extract_from_html(html)
    
    lines = []
    
    # Title
    lines.append(f"🍽️ {title.replace('_', ' ')}")
    lines.append("")
    
    # Yield
    if recipe.get("yield"):
        lines.append(f"👥 Rendimento: {recipe.get('yield')}")
        lines.append("")
    
    # Time
    if recipe.get("time"):
        lines.append(f"⏱️ Tempo: {recipe.get('time')}")
        lines.append("")
    
    # Ingredients
    if recipe.get("ingredients"):
        lines.append("📝 Ingredientes:")
        for i, ing in enumerate(recipe.get("ingredients", []), 1):
            lines.append(f"  {i}. {ing}")
        lines.append("")
    
    # Instructions
    if recipe.get("instructions"):
        lines.append("👨‍🍳 Modo de preparo:")
        for i, inst in enumerate(recipe.get("instructions", []), 1):
            inst_clean = sanitize_for_output(inst)
            if inst_clean:
                lines.append(f"  {i}. {inst_clean}")
        lines.append("")
    
    # Source
    lines.append(f"📦 Fonte: Wikilivros (licença livre)")
    lines.append(f"🔗 URL: {url}")
    
    return "\n".join(lines)


def cmd_buscar(args):
    """Search for recipes"""
    query = args.q
    fonte = args.fonte or "auto"
    max_results = args.max or 5
    
    # Translate from Portuguese to English for API search
    search_query = translator.translate_to_english(query)
    
    if search_query != query.lower():
        print(f"🔄 Traduzindo: '{query}' → '{search_query}'")
    
    results = []
    
    # Search Wikibooks
    if fonte in ["auto", "wikibooks"]:
        cache_key = f"search_wikibooks_{search_query}"
        cached = cache.get(cache_key, "wikibooks")
        
        if cached:
            results.extend(cached)
        else:
            wb_results = wikibooks.search(search_query, max_results * 2)
            results.extend(wb_results)
            cache.set(cache_key, wb_results, "wikibooks")
    
    # Search TheMealDB
    if fonte in ["auto", "mealdb"]:
        cache_key = f"search_mealdb_{search_query}"
        cached = cache.get(cache_key, "mealdb")
        
        if cached:
            db_results = cached
        else:
            db_results = mealdb.search(search_query)
            cache.set(cache_key, db_results, "mealdb")
        
        for meal in db_results[:max_results]:
            results.append({
                "title": meal.get("strMeal", ""),
                "description": meal.get("strCategory", ""),
                "url": f"https://www.themealdb.com/meal/{meal.get('idMeal', '')}",
                "source": "mealdb",
                "id": meal.get("idMeal", "")
            })
    
    # Limit results
    results = results[:max_results]
    
    if not results:
        # Try generating an original recipe
        print("😕 Nenhuma receita encontrada nas fontes.")
        print("\n💡 Vou gerar uma receita original para você!\n")
        
        # Use original query as ingredients
        potential_ingredients = query.split()
        
        # But also try to generate a specific dish if we recognize the term
        recognized_dish = translator.translate_to_english(query.lower())
        
        recipe = generator.generate_recipe(potential_ingredients, dish_name=query)
        
        # Format and display the generated recipe
        print(f"🍽️ {recipe['title']}")
        print(f"⏱️ Tempo: {recipe.get('time', 'N/A')} | 👥 {recipe.get('yield', 'N/A')}")
        print("")
        
        if recipe.get("ingredients"):
            print("📝 Ingredientes:")
            for ing in recipe["ingredients"]:
                print(f"  • {ing}")
            print("")
        
        if recipe.get("instructions"):
            print("👨‍🍳 Modo de preparo:")
            for j, step in enumerate(recipe["instructions"], 1):
                print(f"  {j}. {step}")
            print("")
        
        if recipe.get("tags"):
            print(f"🏷️ Tags: {', '.join(recipe['tags'])}")
        
        print("\n📦 Fonte: Receita original gerada por Seth")
        
        return
    
    # Display results
    print(f"\n🔍 Resultados para '{query}':\n")
    
    for i, r in enumerate(results, 1):
        source_icon = "🍽️" if r.get("source") == "mealdb" else "📚"
        source_name = "TheMealDB" if r.get("source") == "mealdb" else "Wikilivros"
        
        print(f"{i}. {r.get('title', 'Sem título')}")
        if r.get("description"):
            print(f"   {r.get('description')}")
        print(f"   {source_icon} Fonte: {source_name}")
        
        if r.get("id"):
            print(f"   🆔 ID: {r.get('id')}")
        
        print("")


def cmd_obter(args):
    """Get specific recipe details"""
    fonte = args.fonte
    
    if fonte == "mealdb":
        meal_id = args.id
        if not meal_id:
            print("❌ Para mealdb, forneça o ID com --id")
            return
        
        cache_key = f"meal_{meal_id}"
        cached = cache.get(cache_key, "mealdb")
        
        if cached:
            meal = cached
        else:
            meal = mealdb.get_by_id(meal_id)
            if meal:
                cache.set(cache_key, meal, "mealdb")
        
        if not meal:
            print(f"❌ Receita não encontrada: {meal_id}")
            return
        
        print(format_recipe_meal(meal))
    
    elif fonte == "wikibooks":
        title = args.titulo
        if not title:
            print("❌ Para wikibooks, forneça o título com --titulo")
            return
        
        cache_key = f"wikibooks_{title}"
        cached = cache.get(cache_key, "wikibooks")
        
        if cached:
            html_content = cached
        else:
            html_content = wikibooks.get_page_content(title)
            if html_content:
                cache.set(cache_key, html_content, "wikibooks")
        
        if not html_content:
            print(f"❌ Receita não encontrada: {title}")
            return
        
        url = f"https://pt.wikibooks.org/wiki/{title}"
        print(format_recipe_wikibooks(title, html_content, url))
    
    else:
        print(f"❌ Fonte desconhecida: {fonte}")


def cmd_sugerir(args):
    """Suggest recipe based on ingredients"""
    ingredients = args.ingredientes
    restrictions = args.restricoes or ""
    tempo_max = args.tempo_max
    dificuldade = args.dificuldade
    
    print(f"\n🍳 Sugerindo receitas com: {ingredients}")
    if restrictions:
        print(f"   Restrições: {restrictions}")
    if tempo_max:
        print(f"   Tempo máximo: {tempo_max} minutos")
    print("")
    
    # Parse ingredients
    ing_list = [i.strip() for i in ingredients.split(",")]
    
    # Translate ingredients to English for search
    translated_ings = [translator.translate_to_english(i) for i in ing_list]
    
    # Search in TheMealDB first
    main_ingredient = translated_ings[0] if translated_ings else ""
    
    if main_ingredient:
        # Try to find recipes with main ingredient
        cache_key = f"filter_ingredient_{main_ingredient}"
        cached = cache.get(cache_key, "mealdb")
        
        if cached:
            meals = cached
        else:
            meals = mealdb.filter_by_ingredient(main_ingredient)
            cache.set(cache_key, meals, "mealdb")
        
        if meals:
            # Get first 3 random meals
            import random
            selected = random.sample(meals, min(3, len(meals)))
            
            print(f"📋 Encontrei {len(meals)} receitas com '{translated_ings[0]}':\n")
            
            for meal in selected:
                meal_detail = mealdb.get_by_id(meal.get("id"))
                if meal_detail:
                    print(format_recipe_meal(meal_detail))
                    print("\n" + "="*50 + "\n")
            return
    
    # If no results, generate original recipe
    print("😕 Não encontrei receitas com esses ingredientes nas fontes disponíveis.")
    print("💡 Vou gerar uma receita original para você!\n")
    
    recipe = generator.generate_recipe(ing_list, restrictions)
    
    # Format and display
    print(f"🍽️ {recipe['title']}")
    print(f"⏱️ Tempo: {recipe.get('time', 'N/A')} | 👥 {recipe.get('yield', 'N/A')}")
    print("")
    
    if recipe.get("ingredients"):
        print("📝 Ingredientes:")
        for ing in recipe["ingredients"]:
            print(f"  • {ing}")
        print("")
    
    if recipe.get("instructions"):
        print("👨‍🍳 Modo de preparo:")
        for j, step in enumerate(recipe["instructions"], 1):
            print(f"  {j}. {step}")
        print("")
    
    if recipe.get("tags"):
        print(f"🏷️ Tags: {', '.join(recipe['tags'])}")
    
    print("\n📦 Fonte: Receita original gerada por Seth")


def cmd_random(args):
    """Get random recipe"""
    print("\n🎲 Buscando receita aleatória...\n")
    
    # Try TheMealDB first (has better random)
    meal = mealdb.get_random()
    
    if meal:
        print(format_recipe_meal(meal))
    else:
        # Fallback to Wikibooks
        print("😕 TheMealDB não respondeu. Tentando Wikibooks...")
        recipes = wikibooks.search("", 20)
        
        if recipes:
            import random
            selected = random.choice(recipes)
            html = wikibooks.get_page_content(selected.get("title", ""))
            
            if html:
                print(format_recipe_wikibooks(
                    selected.get("title", ""),
                    html,
                    selected.get("url", "")
                ))
            else:
                print("❌ Não foi possível obter detalhes.")
        else:
            print("❌ Nenhuma receita disponível.")


def cmd_nutricao(args):
    """Get nutrition info for an ingredient"""
    ingredient = args.ingrediente
    
    if not ingredient:
        print("❌ Forneça um ingrediente com --ingrediente")
        return
    
    print(f"\n🔍 Buscando informações nutricionais de: {ingredient}\n")
    
    result = nutrition.get_nutrition_estimate(ingredient)
    
    if result:
        print(nutrition.format_nutrition(result))
    else:
        print(f"😕 Não foi possível encontrar informações para '{ingredient}'")
        print("   O OpenFoodFacts pode não ter dados para este ingrediente.")


def main():
    parser = argparse.ArgumentParser(
        description="seth_receitas_ptbr - Buscador de receitas em português do Brasil"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Buscar
    parser_buscar = subparsers.add_parser("buscar", help="Buscar receitas")
    parser_buscar.add_argument("--q", required=True, help="Termo de busca")
    parser_buscar.add_argument("--fonte", choices=["auto", "wikibooks", "mealdb"], 
                               help="Fonte (padrão: auto)")
    parser_buscar.add_argument("--max", type=int, default=5, help="Máximo de resultados")
    
    # Obter
    parser_obter = subparsers.add_parser("obter", help="Obter receita específica")
    parser_obter.add_argument("--fonte", required=True, choices=["wikibooks", "mealdb"],
                              help="Fonte da receita")
    parser_obter.add_argument("--id", help="ID da receita (para mealdb)")
    parser_obter.add_argument("--titulo", help="Título da página (para wikibooks)")
    
    # Sugerir
    parser_sugerir = subparsers.add_parser("sugerir", help="Sugerir receita por ingredientes")
    parser_sugerir.add_argument("--ingredientes", required=True, 
                                help="Ingredientes separados por vírgula")
    parser_sugerir.add_argument("--restricoes", help="Restrições (vegano, vegetariana, etc)")
    parser_sugerir.add_argument("--tempo-max", type=int, help="Tempo máximo em minutos")
    parser_sugerir.add_argument("--dificuldade", choices=["facil", "media", "dificil"],
                                help="Dificuldade desejada")
    
    # Random
    parser_random = subparsers.add_parser("random", help="Receita aleatória")
    
    # Nutrição
    parser_nutricao = subparsers.add_parser("nutricao", help="Informações nutricionais")
    parser_nutricao.add_argument("--ingrediente", required=True, help="Nome do ingrediente")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("\n" + "="*50)
        print("💡 Promise: Eu busco receitas nas fontes suportadas")
        print("   (Wikilivros + TheMealDB). Se não encontrar algo")
        print("   bom, posso gerar uma receita original!")
        return
    
    # Execute command
    if args.command == "buscar":
        cmd_buscar(args)
    elif args.command == "obter":
        cmd_obter(args)
    elif args.command == "sugerir":
        cmd_sugerir(args)
    elif args.command == "random":
        cmd_random(args)
    elif args.command == "nutricao":
        cmd_nutricao(args)


if __name__ == "__main__":
    main()
