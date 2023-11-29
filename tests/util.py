def register_and_login(client, username, password):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': username, 'password': password}
    )
    assert response.headers["Location"] == "/"

def make_post(client, title, body, authorship="thisuser"):
    check_page_contains(client, '/create', 'Написать')
    client.post('/create', data={'title':title, 'body':body, 'authorship':authorship})

def check_page_contains(client, url, what):
    response = client.get(url)
    assert response.status_code == 200
    assert(what.encode() in response.data)

def check_page_doesnt_contain(client, url, what):
    response = client.get(url)
    assert response.status_code == 200
    assert(what.encode() not in response.data)

def check_page_contains_several(client, url, fragments):
    response = client.get(url)
    assert response.status_code == 200
    for what in fragments:
        assert(what.encode() in response.data)