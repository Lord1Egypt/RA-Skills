#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  render-command-skeleton.sh --command "acme report" --class Acme_Report_Command [--write /tmp/acme-report.php]

Examples:
  render-command-skeleton.sh --command "acme report" --class Acme_Report_Command
  render-command-skeleton.sh --command "acme report" --class Acme_Report_Command --write /tmp/acme-report.php
EOF
}

COMMAND_NAME=""
CLASS_NAME=""
WRITE_PATH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --command)
      COMMAND_NAME="${2:-}"
      shift 2
      ;;
    --class)
      CLASS_NAME="${2:-}"
      shift 2
      ;;
    --write)
      WRITE_PATH="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$COMMAND_NAME" || -z "$CLASS_NAME" ]]; then
  echo "--command and --class are required" >&2
  usage >&2
  exit 1
fi

read -r -d '' TEMPLATE <<EOF || true
<?php

/**
 * WP-CLI command skeleton for ${COMMAND_NAME}.
 */
class ${CLASS_NAME} {
    /**
     * Show a status report.
     *
     * ## OPTIONS
     *
     * [--format=<format>]
     * : Render format.
     * ---
     * default: table
     * options:
     *   - table
     *   - json
     *   - csv
     *   - yaml
     * ---
     *
     * ## EXAMPLES
     *
     *     wp ${COMMAND_NAME} status
     *     wp ${COMMAND_NAME} status --format=json
     *
     * @when after_wp_load
     */
    public function status( \$args, \$assoc_args ) {
        \$items = [
            [
                'key' => 'example',
                'value' => 'ok',
            ],
        ];

        \$format = \WP_CLI\Utils\get_flag_value( \$assoc_args, 'format', 'table' );
        \WP_CLI\Utils\format_items( \$format, \$items, [ 'key', 'value' ] );
        \WP_CLI::success( 'Status generated.' );
    }
}

WP_CLI::add_command( '${COMMAND_NAME}', '${CLASS_NAME}' );
EOF

if [[ -n "$WRITE_PATH" ]]; then
  printf '%s\n' "$TEMPLATE" > "$WRITE_PATH"
  printf 'wrote: %s\n' "$WRITE_PATH"
else
  printf '%s\n' "$TEMPLATE"
fi
