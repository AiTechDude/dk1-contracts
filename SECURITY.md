<!-- DK1 Security Baseline: security-policy -->
# Security Policy

## Supported Versions

`AiTechDude/dk1-contracts` is an internal DK1 repository. Security fixes target the current `main` branch
unless a release branch is explicitly maintained.

## Reporting A Vulnerability

Report suspected vulnerabilities directly through the DK1 internal security channel. Do not open public
issues for exploitable findings, credentials, customer data exposure, or attack details.

## Handling Rules

- Do not commit secrets, runtime pentest configs, scanner databases, or generated reports.
- Do not run active testing against production URLs.
- Use seeded non-production data and non-production credentials for staging/local tests.
- Keep GitHub Actions, dependency review, CodeQL, and security audit workflows enabled on protected branches.
