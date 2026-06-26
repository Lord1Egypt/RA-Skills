from typing import Iterable, Iterator, Tuple, TypeVar

T = TypeVar("T")


def bounded_candidates(items: Iterable[T], max_count: int) -> Iterator[Tuple[int, T]]:
    for idx, item in enumerate(items, start=1):
        if idx > max_count:
            break
        yield idx, item
