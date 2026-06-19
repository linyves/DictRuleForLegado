#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = REPO_ROOT / "dictrule.json"
REQUIRED_KEYS = ("enabled", "name", "showRule", "sortNumber", "urlRule")


def is_rule_object(data: object) -> bool:
    return isinstance(data, dict) and all(key in data for key in REQUIRED_KEYS)


def is_rule_list(data: object) -> bool:
    return isinstance(data, list) and all(is_rule_object(item) for item in data)


def is_legado_rule_file(path: Path) -> bool:
    """Accept both single-rule objects and multiple-rule arrays."""
    if path.name == OUTPUT_FILE.name:
        return False
    if path.suffix != ".json":
        return False

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False

    return is_rule_object(data) or is_rule_list(data)


def main() -> None:
    merged: list[object] = []
    for path in sorted(REPO_ROOT.rglob("*.json")):
        if not is_legado_rule_file(path):
            continue

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if is_rule_object(data):
            merged.append(data)
        elif is_rule_list(data):
            merged.extend(data)

    OUTPUT_FILE.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        f"Generated {OUTPUT_FILE.relative_to(REPO_ROOT)} with {len(merged)} rule(s)."
    )


if __name__ == "__main__":
    main()
