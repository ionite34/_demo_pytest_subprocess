import pytest

from foo import mod


def test_add():
    assert mod.add(1, 2) == 3


@pytest.mark.run_in_subprocess
def test_sub():
    assert mod.sub(1, 1) == 0
