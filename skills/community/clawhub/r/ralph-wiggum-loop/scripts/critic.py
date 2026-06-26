#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Critic Module
Bezwzględny code reviewer. Szuka WSZYSTKICH problemów w kodzie.
"""

import argparse
import json
import os
import sys
import re
from typing import List, Dict, Any, Optional

try:
    import requests
except ImportError:
    print("Error: requests module not found. Install: pip install requests")
    sys.exit(1)


class Critic:
    """Krytyk - analizuje kod pod kątem problemów."""
    
    DEFAULT_API_URL = "http://127.0.0.1:1234/v1"
    
    SYSTEM_PROMPT = """Jesteś bezwzględnym, pedantycznym code reviewerem i ekspertem od jakości oprogramowania.
Twoim zadaniem jest znalezienie WSZYSTKICH problemów w podanym kodzie.

Sprawdź dokładnie każdy z poniższych obszarów:

1. BŁĘDY (errors) - krytyczne problemy:
   - Błędy składniowe (SyntaxError, IndentationError)
   - Błędy logiczne (nieskończone pętle, błędne warunki)
   - Błędy runtime (IndexError, KeyError, TypeError, AttributeError)
   - Niezdefiniowane zmienne/funkcje
   - Nieobsłużone wyjątki
   - Błędy importów

2. OPTYMALIZACJA (optimization):
   - Złożoność czasowa (O(n²) zamiast O(n log n))
   - Złożoność pamięciowa (niepotrzebne kopie dużych struktur)
   - Nieefektywne pętle
   - Redundantne operacje
   - Brak lazy evaluation
   - Nieoptymalne użycie kolekcji

3. BEZPIECZEŃSTWO (security):
   - SQL injection (string formatting w zapytaniach SQL)
   - Command injection (os.system, subprocess z user input)
   - XSS (cross-site scripting)
   - Path traversal (../ w ścieżkach)
   - Hardcoded secrets/keys/passwords
   - Deserializacja niezaufanych danych (pickle, yaml.load)
   - SSRF (server-side request forgery)
   - Race conditions
   - Brak walidacji inputu

4. STYL I KONWENCJE (style):
   - Naruszenia PEP8 (Python)
   - Niejasne nazwy zmiennych/funkcji
   - Za długie funkcje/metody
   - Za duża złożoność cyklomatyczna
   - Niepotrzebne komentarze lub brak komentarzy
   - Niespójne formatowanie
   - Nieużywane importy/zmienne
   - Magic numbers

5. DOKUMENTACJA (documentation):
   - Brak docstrings
   - Niekompletne docstrings
   - Brak type hints
   - Niejasne nazwy parametrów
   - Brak komentarzy do złożonej logiki

6. TESTOWALNOŚĆ (testability):
   - Brak testów
   - Kod ściśle sprzężony
   - Globalny stan
   - Niepotrzebne efekty uboczne

Dla każdego problemu określ:
- severity: "high" (krytyczny), "medium" (ważny), "low" (kosmetyczny)
- category: jedna z powyższych kategorii
- line: numer linii (jeśli można określić)
- description: szczegółowy opis problemu
- suggestion: konkretna propozycja naprawy

Zwróć wynik TYLKO jako valid JSON w formacie:
{
  "issues": [
    {
      "severity": "high|medium|low",
      "category": "errors|optimization|security|style|documentation|testability",
      "line": 42,
      "description": "Opis problemu",
      "suggestion": "Jak naprawić"
    }
  ],
  "summary": {
    "total_issues": N,
    "high": N,
    "medium": N,
    "low": N,
    "assessment": "brief assessment of overall quality"
  }
}

Jeśli nie ma problemów, zwróć pustą listę issues.
Bądź SZCZEGÓŁOWY i KONKRETNY. Nie pomijaj żadnych problemów."""

    def __init__(self, api_url: str = None, model: str = None):
        self.api_url = api_url or os.getenv("LMSTUDIO_URL", self.DEFAULT_API_URL)
        self.model = model or os.getenv("LMSTUDIO_MODEL_CRITIC")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def _get_available_models(self) -> list:
        """Pobiera listę dostępnych modeli."""
        try:
            response = self.session.get(f"{self.api_url}/models")
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception:
            return []
    
    def _select_model(self) -> Optional[str]:
        """Wybiera najlepszy model do krytyki."""
        models = self._get_available_models()
        if not models:
            return None
        
        # For critic, we want a strong reasoning model
        priority = [
            "qwen2.5", "qwen3", "llama-3", "mistral", 
            "deepseek", "codellama", "dolphin"
        ]
        
        model_names = [m.get("id", "") for m in models]
        
        for keyword in priority:
            for name in model_names:
                if keyword.lower() in name.lower():
                    return name
        
        return model_names[0] if model_names else None
    
    def _extract_json(self, text: str) -> dict:
        """Ekstrahuje JSON z odpowiedzi LLM."""
        # Try direct parsing first
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass
        
        # Try extracting from markdown code blocks
        patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
            r'\{.*\}',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match.strip())
                except json.JSONDecodeError:
                    continue
        
        raise ValueError(f"Could not extract JSON from response: {text[:500]}")
    
    def analyze(
        self, 
        code: str, 
        language: str = "python",
        context: str = "",
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Analizuje kod i zwraca listę problemów.
        
        Args:
            code: Kod do analizy
            language: Język programowania
            context: Dodatkowy kontekst
            temperature: Kreatywność (niska dla konsystencji)
        
        Returns:
            Słownik z issues i summary
        """
        model = self.model or self._select_model()
        
        user_prompt = f"""Przeanalizuj poniższy kod pod kątem WSZYSTKICH problemów.

JĘZYK: {language}
{context}

KOD DO ANALIZY:
```{language}
{code}
```

Zwróć wynik jako valid JSON zgodnie z instrukcją systemową."""

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 8192,
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
            result = self._extract_json(content)
            
            # Validate structure
            if "issues" not in result:
                result["issues"] = []
            if "summary" not in result:
                result["summary"] = self._generate_summary(result.get("issues", []))
            
            return result
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Cannot connect to LM Studio at {self.api_url}")
        except Exception as e:
            raise RuntimeError(f"Analysis failed: {e}")
    
    def _generate_summary(self, issues: List[Dict]) -> Dict[str, Any]:
        """Generuje podsumowanie na podstawie listy problemów."""
        high = sum(1 for i in issues if i.get("severity") == "high")
        medium = sum(1 for i in issues if i.get("severity") == "medium")
        low = sum(1 for i in issues if i.get("severity") == "low")
        
        if high > 0:
            assessment = "Code has critical issues that must be fixed"
        elif medium > 0:
            assessment = "Code has noticeable issues requiring attention"
        elif low > 0:
            assessment = "Code is mostly good with minor style issues"
        else:
            assessment = "Code looks good, no significant issues found"
        
        return {
            "total_issues": len(issues),
            "high": high,
            "medium": medium,
            "low": low,
            "assessment": assessment
        }
    
    def quick_check(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Szybka analiza bez użycia LLM - podstawowe pattern matching."""
        issues = []
        lines = code.split('\n')
        
        # Basic Python checks
        if language.lower() == "python":
            for i, line in enumerate(lines, 1):
                # Check for print statements (should use logging)
                if re.search(r'\bprint\s*\(', line) and 'def ' not in line:
                    issues.append({
                        "severity": "low",
                        "category": "style",
                        "line": i,
                        "description": "Using print() instead of logging",
                        "suggestion": "Use logging module for production code"
                    })
                
                # Check for bare except
                if re.search(r'except\s*:', line):
                    issues.append({
                        "severity": "medium",
                        "category": "errors",
                        "line": i,
                        "description": "Bare except clause catches all exceptions including KeyboardInterrupt",
                        "suggestion": "Use 'except Exception:' or specify exact exception types"
                    })
                
                # Check for SQL injection risks
                if re.search(r'execute\s*\(.*%s', line) or re.search(r'f["\'].*SELECT.*{', line):
                    issues.append({
                        "severity": "high",
                        "category": "security",
                        "line": i,
                        "description": "Potential SQL injection vulnerability",
                        "suggestion": "Use parameterized queries with placeholders"
                    })
                
                # Check for hardcoded secrets
                if re.search(r'(password|secret|key|token)\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
                    if 'import' not in line and '#' not in line:
                        issues.append({
                            "severity": "high",
                            "category": "security",
                            "line": i,
                            "description": "Possible hardcoded credential",
                            "suggestion": "Use environment variables or secure vault"
                        })
        
        return {
            "issues": issues,
            "summary": self._generate_summary(issues)
        }


def main():
    parser = argparse.ArgumentParser(description="Ralph Wiggum Loop - Critic")
    parser.add_argument("-f", "--file", required=True, help="File to analyze")
    parser.add_argument("-l", "--language", default="python", help="Programming language")
    parser.add_argument("-c", "--context", default="", help="Additional context")
    parser.add_argument("--quick", action="store_true", help="Quick check without LLM")
    parser.add_argument("--model", help="Model name to use")
    parser.add_argument("--api-url", help="LM Studio API URL")
    parser.add_argument("-o", "--output", help="Output JSON file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    critic = Critic(api_url=args.api_url, model=args.model)
    
    try:
        if args.quick:
            result = critic.quick_check(code, args.language)
        else:
            result = critic.analyze(code, args.language, args.context)
        
        output = json.dumps(result, indent=2, ensure_ascii=False)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Analysis saved to {args.output}")
        
        if args.verbose or not args.output:
            print(output)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
