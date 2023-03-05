import requests
import pypub
import variables


def get_epub_definition_json():
    epub_url = "https://learning.oreilly.com/api/v2/epubs/urn:orm:book:" + variables.epub_id
    epub_request = pypub.session.get(epub_url)
    json_data = epub_request.json()
    return json_data


def get_epub_json(json_url):
    epub_url = json_url
    epub_request = pypub.session.get(epub_url)
    json_data = epub_request.json()
    limit = 1000
    if hasattr(json_data, 'count'):
        limit = int(json_data['count']) + 1
    epub_url = json_url + "?limit=" + str(limit)
    epub_request = pypub.session.get(epub_url)
    json_data = epub_request.json()
    return json_data


def init_http_session():
    http_session = requests.session()
    pypub.session = http_session

    login_url = "https://www.oreilly.com/member/auth/login/"
    login_payload = {"email": variables.user_name, "password": variables.user_password}
    response = pypub.session.post(login_url, json=login_payload)
    try:
        jwt_token = response.json()['id_token']
        pypub.session.cookies.set("orm-jwt", jwt_token, domain=".oreilly.com")
    except:
        print('Authentication error!')
