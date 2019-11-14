# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib import messages
from trezorlib.tools import parse_path


def _get_xpub(client, passphrase_prompt):
    response = client.call_raw(
        messages.GetPublicKey(address_n=parse_path("44'/0'/0'"), coin_name="Bitcoin")
    )
    if passphrase_prompt:
        assert isinstance(response, messages.PassphraseRequest)
        response = client.call_raw(messages.PassphraseAck(passphrase="A"))
    assert isinstance(response, messages.PublicKey)
    return response.xpub


@pytest.mark.skip_t1  # TODO
@pytest.mark.setup_client(passphrase=True)
def test_state_with_passphrase(client):

    # Let's start the communication by calling Initialize.
    response = client.call_raw(messages.Initialize())
    assert isinstance(response, messages.Features)
    state = response.state
    assert len(state) == 32

    # GetPublicKey requires passphrase and since it is not cached,
    # Trezor will prompt for it.
    xpub = _get_xpub(client, passphrase_prompt=True)
    assert (
        xpub
        == "xpub6CekxGcnqnJ6osfY4Rrq7W5ogFtR54KUvz4H16XzaQuukMFZCGebEpVznfq4yFcKEmYyShwj2UKjL7CazuNSuhdkofF4mHabHkLxCMVvsqG"
    )

    # Call Initialize again, this time with the received state and then call
    # GetPublicKey. The passphrase should be cached now so Trezor must
    # not ask for it again, whilst returning the same xpub.
    response = client.call_raw(messages.Initialize(state=state))
    assert isinstance(response, messages.Features)
    xpub = _get_xpub(client, passphrase_prompt=False)
    assert (
        xpub
        == "xpub6CekxGcnqnJ6osfY4Rrq7W5ogFtR54KUvz4H16XzaQuukMFZCGebEpVznfq4yFcKEmYyShwj2UKjL7CazuNSuhdkofF4mHabHkLxCMVvsqG"
    )

    # If we set state in Initialize to None, the cache will be cleared
    # and Trezor will ask for the passphrase again.
    response = client.call_raw(messages.Initialize(state=None))
    assert isinstance(response, messages.Features)
    xpub = _get_xpub(client, passphrase_prompt=True)
    assert (
        xpub
        == "xpub6CekxGcnqnJ6osfY4Rrq7W5ogFtR54KUvz4H16XzaQuukMFZCGebEpVznfq4yFcKEmYyShwj2UKjL7CazuNSuhdkofF4mHabHkLxCMVvsqG"
    )

    # Unknown state is the same as setting it to None.
    response = client.call_raw(messages.Initialize(state=b"X" * 32))
    assert isinstance(response, messages.Features)
    xpub = _get_xpub(client, passphrase_prompt=True)
    assert (
        xpub
        == "xpub6CekxGcnqnJ6osfY4Rrq7W5ogFtR54KUvz4H16XzaQuukMFZCGebEpVznfq4yFcKEmYyShwj2UKjL7CazuNSuhdkofF4mHabHkLxCMVvsqG"
    )


@pytest.mark.skip_t1  # TODO
@pytest.mark.setup_client()
def test_state_enable_passphrase(client):

    # Let's start the communication by calling Initialize.
    response = client.call_raw(messages.Initialize())
    assert isinstance(response, messages.Features)
    state = response.state
    assert len(state) == 32

    # Trezor will not prompt for passphrase because it is turned off.
    xpub = _get_xpub(client, passphrase_prompt=False)
    assert (
        xpub
        == "xpub6BiVtCpG9fQPxnPmHXG8PhtzQdWC2Su4qWu6XW9tpWFYhxydCLJGrWBJZ5H6qTAHdPQ7pQhtpjiYZVZARo14qHiay2fvrX996oEP42u8wZy"
    )

    # Turn on passphrase. The cache will be cleared.
    response = client.call_raw(messages.ApplySettings(use_passphrase=True))
    assert isinstance(response, messages.ButtonRequest)  # confirm dialog
    client.debug.press_yes()
    response = client.call_raw(messages.ButtonAck())
    assert isinstance(response, messages.Success)

    # Trezor will prompt for it.
    response = client.call_raw(messages.Initialize(state=state))
    xpub = _get_xpub(client, passphrase_prompt=True)
    assert isinstance(response, messages.Features)
    assert state != response.state
    assert (
        xpub
        == "xpub6CekxGcnqnJ6osfY4Rrq7W5ogFtR54KUvz4H16XzaQuukMFZCGebEpVznfq4yFcKEmYyShwj2UKjL7CazuNSuhdkofF4mHabHkLxCMVvsqG"
    )
