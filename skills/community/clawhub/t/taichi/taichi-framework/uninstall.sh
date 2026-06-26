#!/bin/bash
set -e
cd "$(dirname "$0")"

read -p "Remove taichi-framework directory? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

cd ..
rm -rf "$(dirname "$0")"
echo "Uninstalled taichi-framework."
