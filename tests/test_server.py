

def test_login_email_correct(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert "Welcome," in response.data.decode()


def test_login_email_wrong(client):
    response = client.post('/showSummary', data={'email': 'test@test.com'})
    assert response.status_code == 200
    assert "Sorry, that email wasn&#39;t found." in response.data.decode()
