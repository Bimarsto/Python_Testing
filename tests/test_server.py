from server import loadClubs, loadCompetitions


class TestLoadingData:
    def test_loading_clubs(self):
        loaded_data = loadClubs()
        expected_data = [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13",
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4",
            },
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12",
            },
        ]
        assert loaded_data == expected_data

    def test_loading_competitions(self):
        loaded_data = loadCompetitions()
        expected_data = [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
        assert loaded_data == expected_data


class TestLogin:
    def test_login_email_correct(self, client, mock_clubs):
        response = client.post('/showSummary', data={'email': 'firstclub@test.com'})
        assert response.status_code == 200
        assert "Welcome," in response.data.decode()

    def test_login_email_wrong(self, client):
        response = client.post('/showSummary', data={'email': 'test@test.com'})
        assert response.status_code == 200
        assert "Sorry, that email wasn&#39;t found." in response.data.decode()


class TestBookingCompetition:
    def test_correct_competition_booking(self, client, mock_clubs, mock_competitions):
        club = [c for c in mock_clubs if c['name'] == 'First Club'][0]
        competition = [c for c in mock_competitions if c['name'] == 'First Competition'][0]
        places = '2'

        expected_club_points = 8
        expected_competition_places = 14

        response = client.post('/purchasePlaces', data={'club': club['name'],
                                                        'competition': competition['name'],
                                                        'places': places
                                                        })
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode()
        assert f"Points available: {expected_club_points}" in response.data.decode()
        assert f"Number of Places: {expected_competition_places}" in response.data.decode()

    def test_not_enough_club_points(self, client, mock_clubs, mock_competitions):
        club = [c for c in mock_clubs if c['name'] == 'Third Club'][0]
        competition = [c for c in mock_competitions if c['name'] == 'First Competition'][0]
        places = '3'

        expected_club_points = 2
        expected_competition_places = 16

        response = client.post('/purchasePlaces', data={'club': club['name'],
                                                        'competition': competition['name'],
                                                        'places': places
                                                        })
        assert response.status_code == 200
        assert "Not enough club points." in response.data.decode()
        assert f"Points available: {expected_club_points}" in response.data.decode()
        assert f"Number of Places: {expected_competition_places}" in response.data.decode()

    def test_many_places_required(self, client, mock_clubs, mock_competitions):
        club = [c for c in mock_clubs if c['name'] == 'First Club'][0]
        competition = [c for c in mock_competitions if c['name'] == 'Third Competition'][0]
        places = '3'

        expected_club_points = 10
        expected_competition_places = 2

        response = client.post('/purchasePlaces', data={'club': club['name'],
                                                        'competition': competition['name'],
                                                        'places': places
                                                        })
        assert response.status_code == 200
        assert "Too many places required." in response.data.decode()
        assert f"Points available: {expected_club_points}" in response.data.decode()
        assert f"Number of Places: {expected_competition_places}" in response.data.decode()

    def test_booking_more_than_twelve_places(self, client, mock_clubs, mock_competitions):
        club = [c for c in mock_clubs if c['name'] == 'Second Club'][0]
        competition = [c for c in mock_competitions if c['name'] == 'First Competition'][0]
        places = '13'

        response = client.post('/purchasePlaces', data={'club': club['name'],
                                                        'competition': competition['name'],
                                                        'places': places
                                                        })
        assert response.status_code == 200
        assert "You can&#39;t book more than 12 places per competition." in response.data.decode()

    def test_booking_past_competition(self, client, mock_clubs, mock_competitions):
        club = [c for c in mock_clubs if c['name'] == 'First Club'][0]
        competition = [c for c in mock_competitions if c['name'] == 'Second Competition'][0]
        places = '2'

        response = client.post('/purchasePlaces', data={'club': club['name'],
                                                        'competition': competition['name'],
                                                        'places': places
                                                        })
        assert response.status_code == 200
        assert "This competition is already passed." in response.data.decode()


class TestPointsView:
    def test_clubs_points_display(self, client, mock_clubs, mock_competitions):
        response = client.get('/clubs')
        assert response.status_code == 200
        assert "Clubs | GUDLFT Registration" in response.data.decode()
        assert "Third Club" in response.data.decode()

