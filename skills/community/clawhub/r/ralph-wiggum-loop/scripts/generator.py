#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Generator Module
Tworzy początkowy output (kod, tekst, analiza) używając lokalnego LLM przez LM Studio.
"""

import argparse
import json
import os
import sys
import textwrap
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: requests module not found. Install: pip install requests")
    sys.exit(1)


class Generator:
    """Generator - tworzy początkowy output używając LLM."""
    
    DEFAULT_API_URL = "http://127.0.0.1:1234/v1"
    DEFAULT_MODEL = None  # Auto-select first available
    
    SYSTEM_PROMPT = """Jesteś ekspertem programistą i inżynierem oprogramowania. 
Twoim zadaniem jest tworzenie wysokiej jakości kodu, tekstu lub analizy.

Zasady:
- Pisz czysty, czytelny kod
- Używaj najlepszych praktyk i wzorców projektowych
- Dodawaj komentarze tam gdzie to potrzebne
- Rozwiązuj problemy efektywnie i elegancko
- Jeśli kontekst zawiera konkretne wymagania - spełnij je dokładnie

Odpowiadaj tylko treścią wyjściową (kodem/tekstem/analizą), bez dodatkowych wyjaśnień.
"""

    def __init__(self, api_url: str = None, model: str = None):
        self.api_url = api_url or os.getenv("LMSTUDIO_URL", self.DEFAULT_API_URL)
        self.model = model or os.getenv("LMSTUDIO_MODEL", self.DEFAULT_MODEL)
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def _get_available_models(self) -> list:
        """Pobiera listę dostępnych modeli z LM Studio."""
        try:
            response = self.session.get(f"{self.api_url}/models")
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            print(f"Warning: Could not fetch models: {e}", file=sys.stderr)
            return []
    
    def _select_model(self) -> Optional[str]:
        """Wybiera najlepszy dostępny model."""
        models = self._get_available_models()
        if not models:
            return None
        
        # Priority order for model selection
        priority_keywords = [
            "uncensored", "liberated", "dolphin", "wizard",
            "qwen2.5-coder", "qwen3-coder", "codellama",
            "deepseek-coder", "llama-3", "mistral"
        ]
        
        model_names = [m.get("id", "") for m in models]
        
        # Try priority keywords
        for keyword in priority_keywords:
            for name in model_names:
                if keyword.lower() in name.lower():
                    return name
        
        # Default to first available
        return model_names[0]
    
    def generate(
        self, 
        task: str, 
        context: str = "",
        input_content: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """
        Generuje output na podstawie zadania.
        
        Args:
            task: Opis zadania do wykonania
            context: Dodatkowy kontekst/wymagania
            input_content: Istniejąca treść do przerobienia (opcjonalnie)
            temperature: Kreatywność (0.0 - 1.0)
            max_tokens: Max długość odpowiedzi
        
        Returns:
            Wygenerowany output (kod/tekst)
        """
        model = self.model or self._select_model()
        
        # Build user prompt
        if input_content:
            user_prompt = f"""ZADANIE: {task}

KONTEKST/WYMAGANIA:
{context}

ISTNIEJĄCA TREŚĆ DO PRZERÓBKI:
```
{input_content}
```

Przerób/wypełnij zgodnie z zadaniem. Odpowiedz TYLKO gotową treścią."""
        else:
            user_prompt = f"""ZADANIE: {task}

KONTEKST/WYMAGANIA:
{context}

Stwórz rozwiązanie. Odpowiedz TYLKO gotową treścią, bez dodatkowych komentarzy."""

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        if model:
            payload["model"] = model
        
        try:
            response = self.session.post(
                f"{self.api_url}/chat/completions",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            data = response.json()
            
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content.strip()
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to LM Studio at {self.api_url}. "
                "Make sure LM Studio is running with API enabled."
            )
        except Exception as e:
            raise RuntimeError(f"Generation failed: {e}")
    
    def generate_json(
        self,
        task: str,
        context: str = "",
        input_content: str = "",
        temperature: float = 0.3
    ) -> dict:
        """Generuje output w formacie JSON."""
        json_prompt = task + "\n\nIMPORTANT: Return ONLY valid JSON, no markdown, no comments."
        content = self.generate(json_prompt, context, input_content, temperature)
        
        # Try to extract JSON from markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        try:
            return json.loads(content.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON generated: {e}\nContent: {content[:500]}")


def main():
    parser = argparse.ArgumentParser(description="Ralph Wiggum Loop - Generator")
    parser.add_argument("-t", "--task", required=True, help="Task description")
    parser.add_argument("-c", "--context", default="", help="Additional context")
    parser.add_argument("-f", "--file", help="Input file to process")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--model", help="Model name to use")
    parser.add_argument("--api-url", help="LM Studio API URL")
    parser.add_argument("--temp", type=float, default=0.7, help="Temperature")
    
    args = parser.parse_args()
    
    input_content = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    
    gen = Generator(api_url=args.api_url, model=args.model)
    
    try:
        if args.json:
            result = gen.generate_json(
                args.task, args.context, input_content, args.temp
            )
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            result = gen.generate(
                args.task, args.context, input_content, args.temp
            )
            output = result
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output saved to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
