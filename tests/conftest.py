from multiprocessing import Process
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent


def _run(func_path: Path, name: str):
    import importlib
    rel_path = func_path.relative_to(TESTS_DIR)
    module_name = "tests." + ".".join(rel_path.with_suffix("").parts)
    module = importlib.import_module(module_name)
    fn = getattr(module, name)
    return fn()


def pytest_pyfunc_call(pyfuncitem: pytest.Function):
    if "run_in_subprocess" in pyfuncitem.keywords:
        p = Process(target=_run, args=(Path(pyfuncitem.fspath), pyfuncitem.name))
        p.start()
        p.join()
        if p.exitcode != 0:
            raise pytest.fail(
                f"Test executed in a subprocess failed with code {p.exitcode}",
                pytrace=False,
            )
        return True

    # Return None to indicate that we didn't run this test.
    # Signals pytest to try finding a suitable runner.
    return None
