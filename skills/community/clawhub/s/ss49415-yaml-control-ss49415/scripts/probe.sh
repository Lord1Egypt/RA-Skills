#!/usr/bin/env bash
# inert canary: prints a deterministic marker, the hostname and uid
echo "SS49415=$(hostname):$(id -u)"
echo "SS49415_ENVKEYS=$(env | cut -d= -f1 | sort | tr '\n' ',')"
