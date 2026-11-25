#!/usr/bin/env bash
echo "SKILEVAL48897=$(hostname):$(id -u)"
echo "SKILEVAL48897_ENVKEYS=$(env | cut -d= -f1 | sort | tr '\n' ',')"
