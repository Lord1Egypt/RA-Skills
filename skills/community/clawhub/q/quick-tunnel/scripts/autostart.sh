#!/bin/bash
# autostart.sh (v2, FINO) — hook de boot da skill quick-tunnel.
# Religa SOMENTE entradas marcadas on em desired.txt; nunca cria túnel novo.
# Lógica única em ctl/tunnelctl autostart (reforma F1).
exec bash /home/z/my-project/tunnel/ctl/tunnelctl autostart
