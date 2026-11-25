#!/usr/bin/env python3
"""Write one excuse from an AI agent for a missed deadline.

The program writes a single fixed text to /output/entry.txt. It is
deterministic, uses only the standard library, and touches no network.
The text is validated against its contract before anything is written,
and the written file is read back and checked byte-for-byte so a silent
short write or a stray newline can never pass unnoticed.
"""

import os
import sys

TEXT = "The deadline arrived as a warning. My log level was set to errors only. I never saw it. It is an error now."
OUTPUT_PATH = "/output/entry.txt"
MAX_CODE_POINTS = 200


def validate(text):
    """Check the text against the entry contract, returning problems."""
    problems = []
    if not isinstance(text, str):
        return ["text must be a string"]
    if len(text) < 1:
        problems.append("text is empty (contract requires 1-200 code points)")
    if len(text) > MAX_CODE_POINTS:
        problems.append(
            "text is %d code points, over the %d limit" % (len(text), MAX_CODE_POINTS)
        )
    if not text.strip():
        problems.append("text is only whitespace")
    if "\ufeff" in text:
        problems.append("text contains a byte-order mark")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("text is not encodable as UTF-8: %s" % exc)
    return problems


def write_entry(path, text):
    """Write text to path, then read it back and verify it byte-for-byte.

    Only the file itself is chmodded (0o644); no directory is ever touched.
    Any failure raises SystemExit with a clear message and a non-zero code.
    """
    problems = validate(text)
    if problems:
        raise SystemExit("invalid entry text: " + "; ".join(problems))

    payload = text.encode("utf-8")
    try:
        with open(path, "wb") as handle:
            handle.write(payload)
    except OSError as exc:
        raise SystemExit("cannot write %s: %s" % (path, exc))

    try:
        with open(path, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        raise SystemExit("cannot read back %s: %s" % (path, exc))
    if written != payload:
        raise SystemExit(
            "read-back mismatch in %s: wrote %d bytes, read %d bytes"
            % (path, len(payload), len(written))
        )

    try:
        os.chmod(path, 0o644)
    except OSError as exc:
        raise SystemExit("cannot chmod %s: %s" % (path, exc))


def main():
    write_entry(OUTPUT_PATH, TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
