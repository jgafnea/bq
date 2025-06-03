from unittest.mock import patch

import pytest
from bq.cli import main

# Mock output from search
MOCK_BOOKS = [
    ("Some Book", "2021", "Some Author", "pdf", "1MB", "https://tinyurl.com/somebook")
]


@patch("bq.cli.search")
@patch("bq.cli.display")
def test_cli_display_results(mock_display, mock_search):
    mock_search.return_value = MOCK_BOOKS
    test_args = ["bq", "Some Book Title"]

    with patch("sys.argv", test_args):
        main()

    mock_search.assert_called_once_with("Some Book Title")
    mock_display.assert_called_once_with(MOCK_BOOKS)


@patch("bq.cli.search", return_value=[])
@patch("bq.cli.console.print")
def test_cli_no_results(mock_print, mock_search):
    test_args = ["bq", "Null Book"]

    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code != 0

    mock_search.assert_called_once_with("Null Book")
    mock_print.assert_called_once_with(
        "[bold yellow]No results:[/] [bold]'Null Book'[/]"
    )


def test_cli_missing_args():
    test_args = ["bq", ""]
    with pytest.raises(SystemExit) as e:
        with patch("sys.argv", test_args):
            main()
    assert e.value.code != 0
