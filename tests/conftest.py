import pytest
import server
from .mocks import mock_clubs_data, mock_competitions_data


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    return client


@pytest.fixture
def mock_clubs(mocker):
    return mocker.patch.object(server, 'clubs', mock_clubs_data())


@pytest.fixture
def mock_competitions(mocker):
    return mocker.patch.object(server, 'competitions', mock_competitions_data())
