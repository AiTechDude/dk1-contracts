#!/usr/bin/env python3
"""DK1 Security Baseline: render Shannon YAML from environment variables."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

PLACEHOLDER_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")
REQUIRED_ENV_VARS = {"DK1_STAGING_URL", "SHANNON_TEST_USERNAME", "SHANNON_TEST_PASSWORD"}


def render_template(template_text: str) -> str:
    missing: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        value = os.environ.get(name)
        if not value:
            missing.add(name)
            return match.group(0)
        return value

    rendered = PLACEHOLDER_PATTERN.sub(replace, template_text)
    all_missing = sorted(missing | {name for name in REQUIRED_ENV_VARS if not os.environ.get(name)})
    if all_missing:
        raise SystemExit("Missing required environment variables for Shannon config: " + ", ".join(all_missing))
    unresolved = sorted(set(PLACEHOLDER_PATTERN.findall(rendered)))
    if unresolved:
        raise SystemExit("Unresolved placeholders remain in rendered Shannon config: " + ", ".join(unresolved))
    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(description="Render DK1 Shannon config")
    parser.add_argument("--template", default="security/shannon-dk1.template.yaml")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    template = Path(args.template)
    output = Path(args.output)
    if not template.exists():
        raise SystemExit(f"Template not found: {template}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_template(template.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"Rendered Shannon config to {output}")


if __name__ == "__main__":
    main()
