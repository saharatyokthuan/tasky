import pytest

from tasky.cli import main


@pytest.fixture
def store_file(tmp_path):
    return str(tmp_path / "tasks.json")


def test_add_then_list(store_file, capsys):
    assert main(["--file", store_file, "add", "buy milk"]) == 0
    capsys.readouterr()

    assert main(["--file", store_file, "list", "--all"]) == 0
    out = capsys.readouterr().out
    assert "buy milk" in out
    assert "[ ]" in out


def test_list_empty(store_file, capsys):
    assert main(["--file", store_file, "list"]) == 0
    assert "no tasks" in capsys.readouterr().out


def test_done_removes_from_default_list(store_file, capsys):
    main(["--file", store_file, "add", "task"])
    capsys.readouterr()

    main(["--file", store_file, "done", "1"])
    capsys.readouterr()

    main(["--file", store_file, "list"])
    assert "no tasks" in capsys.readouterr().out

    main(["--file", store_file, "list", "--all"])
    assert "[x]" in capsys.readouterr().out


def test_missing_task_returns_error(store_file, capsys):
    assert main(["--file", store_file, "done", "42"]) == 1
    assert "not found" in capsys.readouterr().err


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "tasky" in capsys.readouterr().out
