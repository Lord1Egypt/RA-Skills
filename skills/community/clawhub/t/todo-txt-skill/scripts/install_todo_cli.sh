#!/usr/bin/env bash
# Installs the todo.txt CLI (todo.sh) if it isn't already on PATH.
set -euo pipefail

if command -v todo.sh >/dev/null 2>&1; then
  echo "todo.sh is already installed: $(todo.sh -V | head -n1)"
  exit 0
fi

os="$(uname -s)"

case "$os" in
  Darwin)
    if ! command -v brew >/dev/null 2>&1; then
      echo "Homebrew is required to install todo.sh on macOS. Install it from https://brew.sh and re-run this script." >&2
      exit 1
    fi
    brew install todo-txt
    cp -n "$(brew --prefix)/opt/todo-txt/todo.cfg" ~/.todo.cfg
    ;;
  Linux)
    tmp_dir="$(mktemp -d)"
    trap 'rm -rf "$tmp_dir"' EXIT
    git clone --depth 1 https://github.com/todotxt/todo.txt-cli.git "$tmp_dir/todo.txt-cli"
    (cd "$tmp_dir/todo.txt-cli" && make && sudo make install)
    mkdir -p ~/.todo
    cp -n /usr/local/etc/todo/config ~/.todo/config
    ;;
  *)
    echo "Unsupported OS: $os. Install todo.sh manually: https://github.com/todotxt/todo.txt-cli" >&2
    exit 1
    ;;
esac

if command -v todo.sh >/dev/null 2>&1; then
  echo "todo.sh installed successfully: $(todo.sh -V | head -n1)"
else
  echo "Installation finished but todo.sh was not found on PATH." >&2
  exit 1
fi
