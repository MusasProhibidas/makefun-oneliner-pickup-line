"""make.fun entry: The Perfect Pickup Line.

Writes the single pickup line from line.txt to
/output/entry.txt (or $MAKEFUN_OUTPUT / $MAKEFUN_OUTPUT_DIR).
No network access. Deterministic: every run writes the same bytes.
After writing, the output is verified byte-for-byte against the
source (SHA-256) so a partial or corrupted write fails loudly.
"""
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "line.txt"


def _output_path() -> Path:
    if os.environ.get("MAKEFUN_OUTPUT"):
        return Path(os.environ["MAKEFUN_OUTPUT"])
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.txt"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    line = SRC.read_text(encoding="utf-8")
    if len(line.strip()) > 200:
        raise SystemExit("pickup line exceeds 200 characters")
    if len(line.strip().splitlines()) != 1:
        raise SystemExit("pickup line must be a single line")
    out = _output_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(line, encoding="utf-8")
    if _sha256(SRC) != _sha256(out):
        raise SystemExit("entry.txt copy mismatch: output bytes differ from source")


if __name__ == "__main__":
    main()
