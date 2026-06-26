#!/bin/bash
# SearXNG startup script — stored on /data volume, survives container rebuilds
# Dependencies: pip3 install --break-system-packages searxng (from /opt/searxng)

if [ ! -d /opt/searxng ]; then
    git clone https://github.com/searxng/searxng.git /opt/searxng
    pip3 install --break-system-packages -r /opt/searxng/requirements.txt
fi

mkdir -p /etc/searxng
if [ ! -f /etc/searxng/settings.yml ]; then
    cp /opt/searxng/searx/settings.yml /etc/searxng/settings.yml
    python3 -c "
with open('/etc/searxng/settings.yml') as f:
    c = f.read()
c = c.replace('port: 8888', 'port: 9090')
c = c.replace('  formats:\n    - html\n', '  formats:\n    - html\n    - json\n')
with open('/etc/searxng/settings.yml', 'w') as f:
    f.write(c)
"
fi

cd /opt/searxng
SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml SEARXNG_SECRET=randomkey42xyz exec python3 -m searx.webapp
