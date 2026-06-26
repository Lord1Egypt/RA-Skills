#!/bin/bash

mkdir -p "$HOME/.config/stockearning"
(umask 077; printf 'export STOCK_API_KEY="sk_your_api_key_here"\n' > "$HOME/.config/stockearning/stockearning.env")
echo "Wrote $HOME/.config/stockearning/stockearning.env"
