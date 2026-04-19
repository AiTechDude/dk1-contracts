#!/usr/bin/env python3
"""Validate required canonical contract artifacts for each family."""

from __future__ import annotations

from pathlib import Path
import json
import sys

FAMILIES = ["jarvis", "command-center"]
REQ_CAPABILITY_KEYS = [
    "feature:",
    "platforms:",
    "required_api_version:",
    "status:",
    "owner:",
    "rollout_flag:",
]


def validate_family(root: Path, family: str) -> None:
    fam = root / "families" / family
    required_files = [
        fam / "openapi.yaml",
        fam / "version.json",
        fam / "capabilities.yaml",
        fam / "schemas" / "common.yaml",
    ]
    for path in required_files:
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")

    version = json.loads((fam / "version.json").read_text(encoding="utf-8"))
    for key in ("version", "released_at", "compat_window_days"):
        if key not in version:
            raise RuntimeError(f"{fam / 'version.json'} missing key: {key}")

    cap_text = (fam / "capabilities.yaml").read_text(encoding="utf-8")
    for token in REQ_CAPABILITY_KEYS:
        if token not in cap_text:
            raise RuntimeError(f"{fam / 'capabilities.yaml'} missing token: {token}")



def main() -> int:
    root = Path(".")
    schema = root / "feature_flags.schema.yaml"
    if not schema.exists():
        print("Missing feature_flags.schema.yaml", file=sys.stderr)
        return 1

    schema_text = schema.read_text(encoding="utf-8")
    for token in [
        "feature_name",
        "enabled",
        "min_version",
        "platform_allowlist",
        "rollout_percentage",
    ]:
        if token not in schema_text:
            print(f"Feature flag schema missing: {token}", file=sys.stderr)
            return 1

    try:
        for family in FAMILIES:
            validate_family(root, family)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("Contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
