from trezor.crypto import random

if False:
    from typing import Optional

_cached_seed = None  # type: Optional[bytes]
_cached_seed_without_passphrase = None  # type: Optional[bytes]
_cached_state = None  # type: Optional[str]


def get_state() -> Optional[bytes]:
    global _cached_state
    if not _cached_state:
        _cached_state = random.bytes(32)
    return _cached_state


def set_seed(seed: Optional[bytes]) -> None:
    global _cached_seed
    _cached_seed = seed


def get_seed() -> Optional[bytes]:
    return _cached_seed


def set_seed_without_passphrase(seed: Optional[bytes]) -> None:
    global _cached_seed_without_passphrase
    _cached_seed_without_passphrase = seed


def get_seed_without_passphrase() -> Optional[bytes]:
    return _cached_seed_without_passphrase


def clear() -> None:
    global _cached_state
    _cached_state = None

    set_seed(None)
    set_seed_without_passphrase(None)
