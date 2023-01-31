
class TestIntegration:
    def test_integration(self, client, mock_clubs, mock_competitions):
        email_login = 'firstclub@test.com'
        club = [c for c in mock_clubs if c['email'] == email_login][0]
        competition = [c for c in mock_competitions if c['name'] == 'First Competition'][0]
        places = '2'

        expected_club_points = 8
        expected_competition_places = 14

        home = client.get('/')
        assert home.status_code == 200

        user_login = client.post('/showSummary', data={'email': email_login})
        assert user_login.status_code == 200
        assert "Welcome," in user_login.data.decode()

        booking = client.get(f"/book/{competition['name']}/{club['name']}")
        assert booking.status_code == 200
        assert f"Booking for {competition['name']} || GUDLFT" in booking.data.decode()

        purchase_places = client.post('/purchasePlaces',
                                      data={'club': club['name'],
                                            'competition': competition['name'],
                                            'places': places
                                            })
        assert purchase_places.status_code == 200
        assert "Great-booking complete!" in purchase_places.data.decode()
        assert f"Points available: {expected_club_points}" in purchase_places.data.decode()
        assert f"Number of Places: {expected_competition_places}" in purchase_places.data.decode()

        user_logout = client.get('/logout', follow_redirects=True)
        assert user_logout.status_code == 200
        assert "Welcome to the GUDLFT Registration Portal!" in user_logout.data.decode()





