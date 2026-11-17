# Shell Productivity Tips

## 1. Use `Ctrl+R` for reverse history search
Press `Ctrl+R`, type a fragment, and keep pressing to cycle matches.

## 2. `!!` repeats the last command
Prefix with `sudo` when you forgot permissions:
```bash
sudo !!
```

## 3. `cd -` goes back to the previous directory
Faster than typing the path again.

## 4. Brace expansion saves typing
```bash
cp config.{yml,yml.bak}
mkdir -p project/{src,test,docs}
```

## 5. `tee` when you need root + pipe
```bash
echo "hello" | sudo tee /etc/motd
```

## 6. Use `fzf` for fuzzy everything
Install `fzf`, then `Ctrl+T` to fuzzy-find files and `Alt+C` to fuzzy-cd.

## 7. `history | awk` for stats
```bash
history | awk '{print $2}' | sort | uniq -c | sort -rn | head
```
Shows your most-used commands.
