from app import app, open_file_level
import unittest


class TestCartCheckout(unittest.TestCase):

    def test_level1(testing_client):
        app_checkout = app.test_client()
        response = app_checkout.get('/level1')
        assert response.status_code == 200

        output = open_file_level('./level1/output.json')
        assert output == response.get_json()

    def test_level2(testing_client):
        app_checkout = app.test_client()
        response = app_checkout.get('/level2')
        assert response.status_code == 200

        output = open_file_level('./level2/output.json')
        assert output == response.get_json()

    def test_level3(testing_client):
        app_checkout = app.test_client()
        response = app_checkout.get('/level3')
        assert response.status_code == 200

        output = open_file_level('./level3/output.json')
        assert output == response.get_json()

if __name__ == '__main__':
    unittest.main()