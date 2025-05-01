.PHONY: init test clean hard-clean

init:
	uv venv

test:
	uv run pytest

# Soft cleanup - just removes caches
soft-clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# Hard cleanup - resets the entire environment and runs soft cleanup
hard-clean: soft-clean
	deactivate 2>/dev/null || true
	rm -rf .venv
	uv venv