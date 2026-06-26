# Bad code example - do przetestowania Ralph Wiggum Loop

def calc(x,y):
    if x>0:
        if y>0:
            return x+y
        else:
            return x-y
    else:
        if y>0:
            return x*y
        else:
            return x/y

# Problem: brak obsługi dzielenia przez zero
# Problem: brak type hints
# Problem: brak docstring
# Problem: zagnieżdżone if-y (można uprościć)
# Problem: nieczytelna nazwa funkcji
# Problem: brak walidacji inputu