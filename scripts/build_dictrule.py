#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = REPO_ROOT / "dictrule.json"


def is_legado_rule_file(path: Path) -> bool:
    if path.name == OUTPUT_FILE.name:
        return False
    if path.suffix != ".json":
        return False

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False

    if isinstance(data, dict):
        return any(key in data for key in ("urlRule", "showRule", "enabled", "name"))
    if isinstance(data, list):
        return all(isinstance(item, dict) and all(key in item for key in ("urlRule", "showRule", "enabled", "name")) for item in data)
    return False


def main() -> None:
    merged: dict[str, object] = {}
    for path in sorted(REPO_ROOT.rglob("*.json")):
        if not is_legado_rule_file(path):
            continue
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        with path.open("r", encoding="utf-8") as f:
            merged[rel_path] = json.load(f)

    OUTPUT_FILE.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Generated {OUTPUT_FILE.relative_to(REPO_ROOT)} with {len(merged)} entries.")


if __name__ == "__main__":
    main()
