import sys
import re
from colorama import Fore, Style, init

init(autoreset=True)

# Список маркеров ИИ (AI slop) для русского языка
SLOP_WORDS = [
    "дело вот в чем",
    "честно говоря",
    "стоит отметить",
    "важно подчеркнуть",
    "нельзя не упомянуть",
    "интересно отметить",
    "правда заключается",
    "я скажу это снова",
    "давайте поговорим",
    "вот в чем проблема",
    "как мы увидим далее",
    "справедливости ради",
    "и точка",
    "просто вдумайтесь",
    "огромное значение",
    "не делайте ошибки",
    "меняет правила игры",
    "в современном мире",
    "в современном быстро меняющемся",
    "двойная ставка",
    "сделать шаг назад",
    "двигаясь вперед",
    "быть на одной волне",
    "синергия",
    "буквально",
    "искренне",
    "поистине",
    "фундаментально",
    "неизбежно",
    "неотъемлемо",
    "кардинально",
    "чрезвычайно",
    "в своей основе",
    "в конце концов",
    "когда дело доходит",
    "реальность такова",
    "спойлер",
    "причины носят структурный",
    "самая глубокая проблема",
    "ставки высоки",
    "серьезные последствия",
    "полотно",
    "мозаика",
    "трансформация",
    "инновация",
    "интеграция",
    "оптимизация",
    "углубиться в",
    "свидетельствовать о",
    "причудливый",
    "виртуозный",
    "симфония",
    "выступает в роли",
    "служит ярким доказательством",
    "является свидетельством",
    "ключевой поворотный момент",
    "оставил неизгладимый след",
    "символизирует",
    "подчеркивает важность",
    "вносит значимый вклад",
    "это не просто",
    "не только",
    "но и",
    "никто изначально не задумывал"
]

def analyze_text(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"{Fore.RED}Ошибка при чтении файла: {e}")
        return

    print(f"{Fore.CYAN}--- Анализ текста на наличие ИИ-штампов ---")
    
    text_lower = text.lower()
    total_words = len(re.findall(r'\b\w+\b', text_lower))
    
    found_issues = []
    
    for word in SLOP_WORDS:
        count = text_lower.count(word.lower())
        if count > 0:
            found_issues.append((word, count))
            
    if not found_issues:
        print(f"{Fore.GREEN}Отлично! В тексте не найдено типичных ИИ-штампов.")
        return
        
    print(f"{Fore.YELLOW}Найдено {len(found_issues)} уникальных штампов.")
    print("Детализация:")
    score_penalty = 0
    for word, count in sorted(found_issues, key=lambda x: x[1], reverse=True):
        print(f" - {Fore.RED}'{word}'{Style.RESET_ALL}: встречается {count} раз(а)")
        score_penalty += count
        
    slop_score = (score_penalty / total_words) * 100 if total_words > 0 else 0
    
    print(f"\n{Fore.CYAN}Индекс 'воды' (Slop Score): {slop_score:.2f}%")
    if slop_score > 2.0:
        print(f"{Fore.RED}Внимание: Текст сильно заштампован. Рекомендуется рерайтинг с использованием humanizer.")
    elif slop_score > 0.5:
        print(f"{Fore.YELLOW}Замечание: Присутствуют признаки ИИ. Текст требует редактуры.")
    else:
        print(f"{Fore.GREEN}Текст выглядит достаточно чистым, но проверьте его структуру вручную.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python slop_detector.py <путь_к_файлу.txt>")
    else:
        analyze_text(sys.argv[1])
