#!/bin/bash
# tunnel.sh (v2, FINO) — wrapper de compatibilidade da skill quick-tunnel.
# SEM lógica própria: tudo delega ao comando único ctl/tunnelctl (reforma F1).
# Uso: bash skills/quick-tunnel/scripts/tunnel.sh start|status|stop|delete|say|autostart|watchdog|ensure ...
exec bash /home/z/my-project/tunnel/ctl/tunnelctl "$@"
