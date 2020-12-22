check:
	poetry run mypy git_speed tests
	poetry run pytype git_speed tests
	poetry run pytest

test:
	poetry run pytest
