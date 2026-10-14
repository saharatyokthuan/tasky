import pytest

from tasky.storage import Store, TaskNotFound


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / "tasks.json")


def test_add_assigns_increasing_ids(store):
    a = store.add("first")
    b = store.add("second")
    assert (a.id, b.id) == (1, 2)


def test_all_returns_added_tasks(store):
    store.add("a")
    store.add("b")
    assert [t.title for t in store.all()] == ["a", "b"]


def test_complete_marks_done(store):
    task = store.add("a")
    done = store.complete(task.id)
    assert done.done is True
    assert done.done_at is not None
    assert store.get(task.id).done is True


def test_all_excludes_done(store):
    keep = store.add("keep")
    gone = store.add("gone")
    store.complete(gone.id)
    assert [t.id for t in store.all(include_done=False)] == [keep.id]


def test_remove(store):
    task = store.add("a")
    store.remove(task.id)
    assert store.all() == []


def test_complete_unknown_raises(store):
    with pytest.raises(TaskNotFound):
        store.complete(999)


def test_clear_done(store):
    a = store.add("a")
    store.add("b")
    store.complete(a.id)
    assert store.clear_done() == 1
    assert [t.title for t in store.all()] == ["b"]


def test_persists_across_instances(tmp_path):
    path = tmp_path / "tasks.json"
    Store(path).add("persist")
    assert [t.title for t in Store(path).all()] == ["persist"]


def test_default_path_uses_xdg(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    from tasky.storage import default_path

    assert default_path() == tmp_path / "tasky" / "tasks.json"
