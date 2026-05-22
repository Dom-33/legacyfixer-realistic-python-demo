# LegacyFixer realistic Python demo

This repository is a realistic demo project for testing LegacyFixer v0.1.

The goal is to validate the full repository-level workflow:

GitHub App -> webhook -> cloud scan -> dependency fix -> branch -> pull request -> human review.

This is not a minimal dependency fixture. It includes application code, tests, development dependencies, and GitHub Actions CI.

## Expected LegacyFixer behavior

LegacyFixer should create a pull request that updates the supported dependency manifest:

- requirements.txt

LegacyFixer should not rewrite application code, tests, CI configuration, or development dependency files.

Expected untouched files:

- src/
- tests/
- .github/workflows/ci.yml
- requirements-dev.txt

LegacyFixer trigger: realistic repo scan.
