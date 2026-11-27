#!/usr/bin/env python3
"""Register the UNIHIKER K10 board in an esp32sim source tree.

Three source edits are needed on top of dropping in `unihiker_k10.rs`:

1. `esp32s3/src/board/mod.rs`  - declare the module, re-export it, add the match arm.
2. `esp-soc/src/board.rs`      - a default `BoardModel::gpio_input()` no-op.
3. `esp32s3/src/soc.rs`        - call it from `gpio_set_input()` so a scripted
                                 `press btnA` reaches boards whose buttons sit
                                 behind an I/O expander instead of a pad.

Every edit is idempotent: re-running the script on a patched tree changes nothing.

Usage: python3 k10-sim-patch.py <esp32sim-source-dir>
"""
import os
import re
import shutil
import sys

MOD_ARM = '        "unihiker-k10" | "k10" | "unihiker" => Some(Box::new(UnihikerK10::new())),\n'


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def patch_mod_rs(root):
    path = os.path.join(root, "esp32s3", "src", "board", "mod.rs")
    text = read(path)
    if "unihiker_k10" in text:
        return "mod.rs: already registered"
    lines = text.splitlines(keepends=True)

    last_mod = max(i for i, l in enumerate(lines) if l.startswith("pub mod "))
    lines.insert(last_mod + 1, "pub mod unihiker_k10;\n")

    glob_uses = [i for i, l in enumerate(lines) if re.match(r"pub use \w+::\*;", l)]
    if not glob_uses:
        return "mod.rs: no `pub use <mod>::*;` line found - register the board by hand"
    lines.insert(glob_uses[-1] + 1, "pub use unihiker_k10::*;\n")

    body = "".join(lines)
    if "fn make_board" not in body:
        return "mod.rs: no make_board() found - register the board by hand"
    start = body.index("fn make_board")
    fallback = body.find("_ => None", start)
    if fallback < 0:
        return "mod.rs: no catch-all arm in make_board() - register the board by hand"
    line_start = body.rfind("\n", 0, fallback) + 1
    body = body[:line_start] + MOD_ARM + body[line_start:]
    write(path, body)
    return "mod.rs: module + arm added"


def patch_board_rs(root):
    path = os.path.join(root, "esp-soc", "src", "board.rs")
    text = read(path)
    if "fn gpio_input" in text:
        return "board.rs: gpio_input already present"
    anchor = "    fn spi_tx(&mut self, _host: u8, _data: &[u8]) {}\n"
    if anchor not in text:
        return "board.rs: spi_tx default not found - add `fn gpio_input(&mut self, _pin: u8, _level: bool) {}` by hand"
    addition = (
        "    /// A host- or script-driven input level on a pad (the `press` and `gpio` script\n"
        "    /// actions). Boards whose buttons are not read from a pad - those behind an I/O\n"
        "    /// expander - map it to whatever the firmware actually reads.\n"
        "    fn gpio_input(&mut self, _pin: u8, _level: bool) {}\n"
    )
    write(path, text.replace(anchor, anchor + addition, 1))
    return "board.rs: gpio_input default added"


def patch_soc_rs(root):
    path = os.path.join(root, "esp32s3", "src", "soc.rs")
    text = read(path)
    if "board.gpio_input" in text:
        return "soc.rs: gpio_input already wired"
    anchor = "self.irq_dirty |= self.periph.gpio.set_input(pin, level);\n"
    if anchor not in text:
        return "soc.rs: gpio_set_input() body not found - wire board.gpio_input(pin, level) by hand"
    addition = (
        "        // Buttons that hang off an I/O expander rather than a pad still see the press.\n"
        "        self.board.gpio_input(pin, level);\n"
    )
    write(path, text.replace(anchor, anchor + addition, 1))
    return "soc.rs: gpio_set_input() forwards to the board"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = os.path.abspath(sys.argv[1])
    board_dir = os.path.join(root, "esp32s3", "src", "board")
    if not os.path.isdir(board_dir):
        print("not an esp32sim source tree: %s" % root)
        return 2

    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, os.pardir, "references", "esp32sim", "unihiker_k10.rs")
    shutil.copyfile(src, os.path.join(board_dir, "unihiker_k10.rs"))
    print("board/unihiker_k10.rs: copied")

    for step in (patch_mod_rs, patch_board_rs, patch_soc_rs):
        print(step(root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
