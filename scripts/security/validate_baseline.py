#!/usr/bin/env python3
"""DK1 Security Baseline: validate committed baseline files."""

from __future__ import annotations

import re
from pathlib import Path

REQUIRED_PATHS = (
    ".github/workflows/codeql.yml",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/security-audit.yml",
    ".github/workflows/shannon-staging.yml",
    ".github/dependabot.yml",
    ".github/dependency-review-config.yml",
    "security/shannon-dk1.template.yaml",
    "scripts/security/render_shannon_config.py",
    "scripts/security/run-shannon-local.sh",
    "SECURITY.md",
)
FORBIDDEN_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{8,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"BEGIN (RSA|OPENSSH) PRIVATE KEY"),
    re.compile(r"(?i)(ANTHROPIC_API_KEY|SHANNON_TEST_PASSWORD)\s*=\s*[\"']?(?!(\$\{|replace-with|example|placeholder))([^\"'\s]+)"),
)
SKIP_DIRS = {".git", ".venv", "node_modules", "shannon-reports", "reports"}


def main() -> None:
    missing = [path for path in REQUIRED_PATHS if not Path(path).exists()]
    if missing:
        raise SystemExit("Missing security baseline files: " + ", ".join(missing))
    hits: list[str] = []
    for path in Path(".").rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.match("*.runtime.yaml"):
            hits.append(str(path))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                hits.append(f"{path}: pattern {pattern.pattern!r}")
    if hits:
        raise SystemExit("Potential secret/runtime artifact found: " + "; ".join(hits))
    print("DK1 security baseline files are present and no obvious secrets were found.")


if __name__ == "__main__":
    main()
