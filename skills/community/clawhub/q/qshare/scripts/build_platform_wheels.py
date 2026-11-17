"""Build qshare wheels containing the matching cloudflared executable.

Run after ``uv build``:
    python scripts/build_platform_wheels.py --assets-dir /path/to/cloudflared-assets
"""
import argparse
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


SPECS = [
    # manylinux2014 is equivalent to the glibc 2.17 baseline, but is also
    # recognized by older pip releases that do not understand PEP 600 tags.
    ("cloudflared-linux-386", "cloudflared", "manylinux2014_i686"),
    ("cloudflared-linux-amd64", "cloudflared", "manylinux2014_x86_64"),
    ("cloudflared-linux-arm", "cloudflared", "linux_armv6l"),
    ("cloudflared-linux-armhf", "cloudflared", "manylinux_2_17_armv7l"),
    ("cloudflared-linux-arm64", "cloudflared", "manylinux2014_aarch64"),
    ("cloudflared-windows-386.exe", "cloudflared.exe", "win32"),
    ("cloudflared-windows-amd64.exe", "cloudflared.exe", "win_amd64"),
    ("cloudflared-darwin-amd64.tgz", "cloudflared", "macosx_10_13_x86_64"),
    ("cloudflared-darwin-arm64.tgz", "cloudflared", "macosx_11_0_arm64"),
    # pip versions predating manylinux2010/2014 support reject those wheels
    # and otherwise fall back to the universal wheel, which has no binary.
    # manylinux1 is accepted by PyPI and supported by those installers.
    ("cloudflared-linux-386", "cloudflared", "manylinux1_i686"),
    ("cloudflared-linux-amd64", "cloudflared", "manylinux1_x86_64"),
]


def extract_asset(asset, output):
    if asset.suffix != ".tgz":
        shutil.copyfile(str(asset), str(output))
        return
    with tarfile.open(str(asset), "r:gz") as archive:
        source = archive.extractfile("cloudflared")
        if source is None:
            raise RuntimeError("cloudflared archive does not contain its binary")
        with output.open("wb") as destination:
            shutil.copyfileobj(source, destination)


def make_wheel(base_wheel, binary, filename, tag, dist_dir):
    unpack_dir = Path(tempfile.mkdtemp(prefix="qshare-wheel-"))
    try:
        wheel_command = [sys.executable, "-m", "wheel"]
        subprocess.run(
            wheel_command + ["unpack", str(base_wheel), "--dest", str(unpack_dir)], check=True
        )
        package_dir = next(unpack_dir.iterdir())
        wheel_metadata = next(package_dir.glob("*.dist-info/WHEEL"))
        lines = [
            line
            for line in wheel_metadata.read_text().splitlines()
            if line and not line.startswith(("Root-Is-Purelib:", "Tag:"))
        ]
        lines.extend(["Root-Is-Purelib: false", "Tag: py3-none-{}".format(tag), ""])
        wheel_metadata.write_text("\n".join(lines))
        binary_target = package_dir / "qshare" / "_binaries" / filename
        binary_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(binary), str(binary_target))
        subprocess.run(
            wheel_command + ["pack", str(package_dir), "--dest-dir", str(dist_dir)], check=True
        )
        expected = dist_dir / (base_wheel.stem.replace("py3-none-any", "py3-none-{}".format(tag)) + ".whl")
        if not expected.is_file():
            raise RuntimeError("wheel pack did not create {}".format(expected))
    finally:
        shutil.rmtree(str(unpack_dir), ignore_errors=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", required=True)
    parser.add_argument("--dist-dir", default="dist")
    args = parser.parse_args()
    dist_dir = Path(args.dist_dir)
    assets_dir = Path(args.assets_dir)
    if not assets_dir.is_dir():
        raise RuntimeError("Assets directory does not exist: {}".format(assets_dir))
    base_wheels = list(dist_dir.glob("qshare-*-py3-none-any.whl"))
    if len(base_wheels) != 1:
        raise RuntimeError("Build exactly one universal qshare wheel before running this script.")
    with tempfile.TemporaryDirectory() as temporary:
        temporary_dir = Path(temporary)
        for asset_name, binary_name, tag in SPECS:
            asset = assets_dir / asset_name
            if not asset.is_file():
                raise RuntimeError("Missing cloudflared asset: {}".format(asset))
            print("Bundling", asset_name)
            binary = temporary_dir / (tag + "-" + binary_name)
            extract_asset(asset, binary)
            if binary.stat().st_size < 1024 * 1024:
                raise RuntimeError("Downloaded {} is not a cloudflared binary.".format(asset_name))
            make_wheel(base_wheels[0], binary, binary_name, tag, dist_dir)


if __name__ == "__main__":
    main()
