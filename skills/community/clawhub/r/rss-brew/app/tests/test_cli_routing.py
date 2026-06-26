from rss_brew import cli


def test_parser_supports_required_top_level_commands():
    parser = cli.build_parser()

    ns = parser.parse_args(["run"])
    assert ns.command == "run"

    ns = parser.parse_args(["dry-run"])
    assert ns.command == "dry-run"

    ns = parser.parse_args(["inspect", "latest"])
    assert ns.command == "inspect"
    assert ns.inspect_command == "latest"

    ns = parser.parse_args(["delivery", "update", "--status", "sent"])
    assert ns.command == "delivery"
    assert ns.delivery_command == "update"
