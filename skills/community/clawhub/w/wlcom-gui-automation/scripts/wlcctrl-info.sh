#!/usr/bin/env bash
set -u

have() { command -v "$1" >/dev/null 2>&1; }

echo '== wlcctrl =='
if ! have wlcctrl; then
  echo 'wlcctrl: not found' >&2
  exit 1
fi
command -v wlcctrl
wlcctrl --version 2>&1 || true

echo
echo '== outputs =='
wlcctrl --outputs 2>&1 || true

mapfile -t outputs < <(wlcctrl --outputs 2>&1 | sed -n 's/^output "\([^"]*\)"/\1/p')
for o in "${outputs[@]}"; do
  echo
  echo "== display geometry: $o =="
  wlcctrl --getdisplaygeometry "$o" 2>&1 || true
done

echo
echo '== scale candidates =='
gsettings get org.ukui.SettingsDaemon.plugins.xsettings scaling-factor 2>/dev/null || true
xdpyinfo 2>/dev/null | grep -Ei 'dimensions|resolution' || true

echo
echo '== active window =='
wlcctrl --getactivewindow 2>&1 || true

echo
echo '== mouse location =='
wlcctrl --getmouselocation 2>&1 || true
