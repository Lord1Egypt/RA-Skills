#!/usr/bin/env bash
set -e

echo ""
echo "THE_TIME_MASHEEN"
echo "Setting up your stuff..."
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "Python3 not found. Install it from https://python3.org and try again."
  exit 1
fi

# Check pip
if ! command -v pip3 &>/dev/null; then
  echo "pip3 not found. Make sure Python3 is installed properly."
  exit 1
fi

# Check Node/npm
if ! command -v npm &>/dev/null; then
  echo "npm not found. Install Node.js from https://nodejs.org and try again."
  exit 1
fi

# Install Scrapling
echo "Getting Scrapling..."
pip3 install "scrapling[all]" --quiet

# Install playwright
echo "Getting playwright..."
npm install -g playwright-cli --silent

# Install playwright browser binaries
echo "Getting the browser stuff..."
playwright install chromium

echo ""
echo "All the stuff is installed."
echo "You're ready to use THE_TIME_MASHEEN."
echo ""
echo "Try it:"
echo "  scrapling extract get \"https://example.com\" output.md"
echo ""
