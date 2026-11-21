"""Writes this entry's picture of Friday 20 November 2026's world news to /output/entry.png.

The picture is entry.png beside this file, drawn by render.py. Standard library only, no network.
Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def checked_png(path):
    """Reads the picture and refuses one the gate would refuse: not a PNG, too big, or too wide."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        sys.exit("entry.png is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if len(data) > MAX_BYTES or width > MAX_SIDE or height > MAX_SIDE:
        sys.exit(f"entry.png is {len(data)} bytes, {width}x{height}: over the limits")
    return data


def main():
    data = checked_png(os.path.join(HERE, "entry.png"))
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
