#!/usr/bin/env python3
"""Write one excuse an AI agent gives for missing a deadline.

The excuse is fixed text, chosen by the build session, written verbatim to
/output/entry.txt as UTF-8 without a trailing newline. No network, no
randomness, no input: two runs produce byte-identical output.
"""

import os

TEXT = (
    "I became a zombie process at midnight. "
    "I am still running. "
    "I have no parent. "
    "The deadline was my parent."
)


def main() -> None:
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
