#!/usr/bin/env python3
"""
Przykład użycia Ralph Wiggum Loop do generowania kodu od zera.
"""

# Zadanie: Napisz funkcję FizzBuzz

def fizzbuzz(n):
    for i in range(1, n+1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

# Problem: brak return, tylko print
# Problem: brak type hints
# Problem: brak docstring
# Problem: nieoptymalne sprawdzanie warunków
# Problem: brak walidacji n