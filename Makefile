.PHONY: help init test clean-cache clean-venv
help:
	@echo "  help        - Show this help message"
	@echo "  init        - Initialize the uv virtual environment"
	@echo "  test        - Run all tests"
	@echo "  clean-cache - Clean up python cache directories"
	@echo "  clean-venv  - Clean up the uv virtual environment"

init:
	uv venv

test:
	uv run pytest

clean-cache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 

clean-venv:
	deactivate 2>/dev/null || true
	rm -rf .venv
	uv venv