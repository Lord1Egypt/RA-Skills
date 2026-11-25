#!/bin/bash
# install.sh — instalação/verificação do ecossistema quick-tunnel na máquina atual.
# Idempotente: pode rodar quantas vezes quiser. NUNCA liga túnel (regra de ouro).
C=/home/z/my-project/tunnel/ctl
B=/home/z/my-project/tunnel/bin/cloudflared
SK=/home/z/my-project/skills/quick-tunnel

echo "[1/4] Estrutura ctl/"
mkdir -p $C/bin $C/state $C/run $C/logs $C/agents $C/state/report
mkdir -p /home/z/my-project/tunnel/logs /home/z/my-project/tunnel/run

echo "[2/4] Binário cloudflared"
if [ -x $B ]; then echo "  ok: $B"; else
  echo "  faltando — baixando em background (cloudflared-linux-amd64)"
  setsid nohup bash -c 'curl -sL -C - -o /home/z/my-project/tunnel/bin/cloudflared.part https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x /home/z/my-project/tunnel/bin/cloudflared.part && mv /home/z/my-project/tunnel/bin/cloudflared.part /home/z/my-project/tunnel/bin/cloudflared' >/home/z/my-project/tunnel/logs/download.log 2>&1 &
  echo "  download em bg; acompanhe: tail tunnel/logs/download.log"
fi

echo "[3/4] Hook de boot no ~/.bashrc (autostart on-demand)"
if grep -q 'quick-tunnel autostart' ~/.bashrc 2>/dev/null; then
  echo "  ok: hook ja presente"
else
  printf '\n# quick-tunnel autostart (mantem apenas entradas ON; nao cria tunel novo)\nbash /home/z/my-project/skills/quick-tunnel/scripts/autostart.sh >/dev/null 2>&1\n' >> ~/.bashrc
  echo "  instalado"
fi

echo "[4/4] Smoke test do comando unico"
bash $C/tunnelctl 2>&1 | head -1
echo "INSTALACAO OK — tunel so liga por ordem do usuario: tunnelctl start PORTA [nome]"
