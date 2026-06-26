# Installation Guide

## Quick Start

Just run `./start-remote-chrome.sh` directly. The script will automatically check dependencies and prompt you if anything is missing.

## Required Dependencies

The script requires these packages:
- **Xvfb** - Virtual X server
- **x11vnc** - VNC server
- **noVNC** - Web-based VNC client (includes websockify)
- **Chromium** or **Google Chrome** - Browser
- **openssl** - Password generation

## Installation Commands

### Debian/Ubuntu

```bash
# Install all dependencies
sudo apt-get update
sudo apt-get install xvfb x11vnc novnc websockify chromium openssl

# Alternative: Use Google Chrome instead of Chromium
sudo apt-get install xvfb x11vnc novnc websockify openssl
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f  # Fix dependencies
```

### CentOS/RHEL

```bash
sudo yum install xorg-x11-server-Xvfb x11vnc novnc websockify chromium openssl
```

### Fedora

```bash
sudo dnf install xorg-x11-server-Xvfb x11vnc novnc websockify chromium openssl
```

## Verification

After installation, verify everything is installed:

```bash
# Check each dependency
which Xvfb
which x11vnc
which websockify
which chromium  # or google-chrome-stable
which openssl

# Or just run the start script - it will check for you
./start-remote-chrome.sh
```

## When Dependencies Are Missing

If you run the script without installing dependencies, you'll see:

```
✗ Error: Missing required dependencies

The following dependencies are not installed:
  ✗ Xvfb (Virtual X Server)
  ✗ x11vnc (VNC Server)

Installation commands:
  sudo apt-get install xvfb
  sudo apt-get install x11vnc

Note: After installing dependencies, re-run this script to start the service
```

Simply copy and run the installation commands, then retry starting the service.
