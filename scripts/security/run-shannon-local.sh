#!/usr/bin/env bash
set -euo pipefail

: "${DK1_STAGING_URL:?Set DK1_STAGING_URL to a local/staging URL, never production}"
: "${SHANNON_TEST_USERNAME:?Set SHANNON_TEST_USERNAME to a non-production test user}"
: "${SHANNON_TEST_PASSWORD:?Set SHANNON_TEST_PASSWORD to the non-production test password}"
: "${ANTHROPIC_API_KEY:?Set ANTHROPIC_API_KEY for Shannon}"

host="${DK1_STAGING_URL#*://}"
host="${host%%/*}"
host="${host%%:*}"
case "$host" in
  prod|production|prod.*|production.*|*.prod|*.production|*.prod.*|*.production.*)
    echo "Refusing to run Shannon against a production-like host: $DK1_STAGING_URL" >&2
    exit 2
    ;;
esac

OUTPUT_DIR="${SHANNON_OUTPUT_DIR:-security/reports}"
RUNTIME_CONFIG="${TMPDIR:-/tmp}/shannon-dk1.runtime.yaml"

"${PYTHON:-python3}" scripts/security/render_shannon_config.py           --template security/shannon-dk1.template.yaml           --output "$RUNTIME_CONFIG"

npx -y @keygraph/shannon start           -u "$DK1_STAGING_URL"           -r "$(pwd)"           -c "$RUNTIME_CONFIG"           -o "$OUTPUT_DIR"           -w "${SHANNON_WORKSPACE:-dk1-local}"
