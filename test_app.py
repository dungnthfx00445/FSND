
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from database.models import setup_db, db_drop_and_create_all
from config import DB_USER, DB_PASSWORD
from app import create_app

casting_assistant_auth_header= {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild0cVhvOUlaaElqM1FMbjlGTE9KLSJ9.eyJpc3MiOiJodHRwczovL2Rldi03MDZsaGNuOGpoNTVkeHp5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMDY5NzEyNjE0NDg4MjM2MzU3MiIsImF1ZCI6Imh0dHBzOi8vMTI3LjAuMC4xOjgwODAvbG9naW4iLCJpYXQiOjE3MTU5MTU3MzIsImV4cCI6MTcxNTkyMjkzMiwic2NvcGUiOiIiLCJhenAiOiJWWlhjSWFoelJwVlB6YWpEVjRIanYyZWhrSExUbGtlOCIsInBlcm1pc3Npb25zIjpbXX0.tpZGF5_O6gYx0GfWsaRtnkaPDO6NvcLTOUs8ZFU3RHzPM35Bl1vprEBbwl-4_HsACyuBs7j0k1u5dg0booxAWnxez_oWkWL8h9lEDiQXrKmt4mPu-BuGvDsoYrUK07PPv7g_C69yqVya-9AGxnjA_8hhel7RlQx0YALa_OE77f0rltLvxdSoUK9Ud_oRjL5NrmuYyS6iP1lGhcmjd3pn2zhW6fCWx2E9EiqqcBDWExc0JGmwLSeMp3tVZdpMsP3C_Cco_eWoV7ybAAPNuISA3xmxhy2eb9zO2OuK2CRBN1LWdrddTMtwj2n18GxI-7MHw9XT645n3rfMs1LM8FPFeA'
}

casting_director_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild0cVhvOUlaaElqM1FMbjlGTE9KLSJ9.eyJpc3MiOiJodHRwczovL2Rldi03MDZsaGNuOGpoNTVkeHp5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNTIzODA3ODEyOTMwMzk1OTA2MSIsImF1ZCI6Imh0dHBzOi8vMTI3LjAuMC4xOjgwODAvbG9naW4iLCJpYXQiOjE3MTU5MTU2ODMsImV4cCI6MTcxNTkyMjg4Mywic2NvcGUiOiIiLCJhenAiOiJWWlhjSWFoelJwVlB6YWpEVjRIanYyZWhrSExUbGtlOCIsInBlcm1pc3Npb25zIjpbXX0.MHlSpMgQYImDlwzejL_8OKAnhSQriO60Ds90IQVhnYv8OVCp4U2BQtdT4qAlYb35W-UR0P06VgpR781ush6jif4V1ltF8Xelc4Y0H1f8mXb3IoWSeLfq09tufMApOa2TouWiHHR8hoRej_MNch24l9G3bAsrj4jKtIzQP9VyHeKt_oLIuPmGELLk0W3VXEVwPLTnLk9aWRoLigMlLEeUjkt3v8gZaS4Ydy7HnMJzHPs67rcJpnvgZsO5dTRc_C2ZnxGnFw0lUQ0QDkvmF85zminM4Aeht2mLNXHCBufsxpf7gUJpOZlWuHuO4RAJDwtMBw0s988B6u3KUXfw0bGTAA'
}

executive_producer_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild0cVhvOUlaaElqM1FMbjlGTE9KLSJ9.eyJpc3MiOiJodHRwczovL2Rldi03MDZsaGNuOGpoNTVkeHp5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjQxNDMxNTc0MDEyNTAyMjg2OSIsImF1ZCI6Imh0dHBzOi8vMTI3LjAuMC4xOjgwODAvbG9naW4iLCJpYXQiOjE3MTU5MTU2NDAsImV4cCI6MTcxNTkyMjg0MCwic2NvcGUiOiIiLCJhenAiOiJWWlhjSWFoelJwVlB6YWpEVjRIanYyZWhrSExUbGtlOCIsInBlcm1pc3Npb25zIjpbXX0.pbk2b8Bk9H5S9SkJBnABPb-RaefFGlzh9dopGblH4BsDv1MWs1bhaMVZWsEOv6IOBZoJK3QH2oMUnPl_5-wFpKbBO-2qDq-OGjcma5Ik5bzHej3S0e2NZ53mhthXAW1ACJdiluDFVjmHfrRDh8oYkwWRA76JRQP6r-4Rfr9_d9Yc-3fM1ZgxCiQk3W89A9mB7GCqhCNQZQOu-wsvAQBQnhhYxXk31dWMwUo6GsrU-gpkYdAxFxl6dDZL4u0bhqiz1qt2yCbHKBqLwWjUe__Ldlba6GOBmj21FEnVEfe4bZaNcYB5j4z-fEKTsPLv1KTvkqxMY1i9yk9_0OHvxoMrEA'
}

fake_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNPUU5pMmNQbHFkSk1BajFjczhaNCJ9.eyJpc3MiOKhoiVN10MW8xZ3h2NDczYjRkYzhvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzMxNDg5MTg4MDQwNjU0ODA3OSIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9sb2dpbiIsImlhdCI6MTY5NjgzODc2NCwiZXhwIjoxNjk2ODQ1OTY0LCJhenAiOiJLelFiNGZXYkowYkRPd28zTU9kRzB1Y3owVHZ0dTJTWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.Nkm0-htqUxFozmhGpHYGDvfLIslrPFLb06h3WUx_v2H1dmwbyQVfDpileF0VtTWTYG4_Ygmwq3axFkFCkS1zG-Dq7O9ajLfz41ZDhnb9wb_hQx0IVCZVl8JfaPSylVRnGPMWzkOw5zRNM7_MUt5oHcKQxQa21w73Pew7HQbZzQrYPhvjHv4RIUo4MxE6IWMlzKLMBjiV74qYY0PTa7SfN4CaCFnBWe1-DovlB_CMl36DChGXlUj30rQwtwtG_kesZUOL3mS_e28D9unNeylWbKNr5MvVAOVs9_CnWiXvhpKKx4gKhr_OZUOvW8uYv-KPzRAMMzTRBPeCek-C1gf3wg'
}


class CoffeeShopTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test=True)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.database_name = "capstone_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            DB_USER,
            DB_PASSWORD,
            'localhost:5432',
            self.database_name
        )
        setup_db(app=self.app, database_path=self.database_path)
        with self.app.app_context():
            db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_root(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_actor_casting_assistant(self):
        response = self.client.get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_casting_director(self):
        response = self.client.get('/actors', headers=casting_director_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_actor_executive_producer(self):
        response = self.client.get('/actors', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_fake(self):
        response = self.client.get('/actors', headers=fake_auth_header)
        self.assertEqual(response.status_code, 401)

    def test_get_actor_detail(self):
        response = self.client.get('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_fail(self):
        response = self.client.get('/actors', headers={})
        self.assertEqual(response.status_code, 401)

    def test_get_actor_detail_casting_assistant(self):
        response = self.client.get(
            '/actors-detail',
            headers=casting_assistant_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_detail_casting_director(self):
        response = self.client.get(
            '/actors-detail',
            headers=casting_director_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_detail_executive_producer(self):
        response = self.client.get(
            '/actors-detail',
            headers=executive_producer_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_detail_fake(self):
        response = self.client.get('/actors-detail', headers=fake_auth_header)
        self.assertEqual(response.status_code, 401)

    def test_get_actors_detail_fail(self):
        response = self.client.get('/actors-detail', headers={})
        self.assertEqual(response.status_code, 401)
    
    def test_post_actor_casting_assistant(self):
        response = self.client.post(
            '/actors',
            headers=casting_assistant_auth_header,
            json={
                'name': 'Test',
                'age': 23,
                'gender': "Female"
            })
        self.assertEqual(response.status_code, 403)

    def test_post_actor_casting_director(self):
        response = self.client.post(
            '/actors',
            headers=casting_director_auth_header,
            json={
                'name': 'Test',
                'age': 23,
                'gender': "Female"
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_actor_executive_producer(self):
        response = self.client.post(
            '/actors',
            headers=executive_producer_auth_header,
            json={
                'name': 'Test 1',
                'age': 23,
                'gender': "Female"
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_actors_fake(self):
        response = self.client.post('/actors', headers=fake_auth_header, json={
                'name': 'Test 1',
                'age': 23,
                'gender': "Female"
        })
        self.assertEqual(response.status_code, 401)

    def test_post_actor_fail(self):
        response = self.client.post('/actors', headers={}, json={
                'name': 'Test 1',
                'age': 23,
                'gender': "Female"
        })
        self.assertEqual(response.status_code, 401)
    
    def test_patch_actors_casting_assistant(self):
        response = self.client.patch(
            '/actors/1',
            headers=casting_assistant_auth_header,
            json={
                'name': 'Test 1',
                'age': 23,
                'gender': "Female"
            })
        self.assertEqual(response.status_code, 403)

    def test_patch_actor_casting_director(self):
        response = self.client.patch(
            '/actors/1',
            headers=casting_assistant_auth_header,
            json={
                'name': 'Test 1',
                'age': 23,
                'gender': "Female"
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_executive_producer(self):
        response = self.client.patch(
            '/actors/1',
            headers=executive_producer_auth_header,
            json={
                'name': 'Test 1',
                'age': 23,
                'gender': "Female"
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_fail(self):
        response = self.client.patch('/actors/1', headers={},
        json={
                'name': 'Test 1',
                'age': 23,
                'gender': "Female"
            })
        self.assertEqual(response.status_code, 401)
    
    def test_delete_actors_casting_assistant(self):
        response = self.client.delete('/actors/1', headers=casting_assistant_auth_header)
        self.assertEqual(response.status_code, 403)

    def test_delete_actors_casting_director(self):
        response = self.client.delete('/actors/1', headers=casting_director_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_executive_producer(self):
        response = self.client.delete('/actors/1', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_fail(self):
        response = self.client.delete('/actors/1', headers={})
        self.assertEqual(response.status_code, 401)

    def test_get_movies_casting_assistant(self):
        response = self.client.get('/movies', headers=casting_assistant_auth_header)
        self.assertEqual(response.status_code, 200)

    def test_get_movies_casting_director(self):
        response = self.client.get('/movies', headers=casting_director_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_executive_producer(self):
        response = self.client.get('/movies', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_fail(self):
        response = self.client.get('/movies', headers={})
        self.assertEqual(response.status_code, 401)

    def test_post_movies_casting_assistant(self):
        response = self.client.post(
            '/movies',
            headers=casting_assistant_auth_header,
            json={
                'title': 'Test',
                'release_date': '2015-11-02 11:18:42'})
        self.assertEqual(response.status_code, 403)

    def test_post_movies_casting_director(self):
        response = self.client.post(
            '/movies',
            headers=casting_director_auth_header,
            json={
                'title': 'Test',
                'release_date': '2015-11-02 11:18:42'})
        self.assertEqual(response.status_code, 403)

    def test_post_movie_executive_producer(self):
        response = self.client.post(
            '/movies',
            headers=executive_producer_auth_header,
            json={
                'title': 'Test',
                'release_date': '2015-11-02 11:18:42'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movies_fail(self):
        response = self.client.post('/movies', headers={}, json={
                'title': 'Test',
                'release_date': '2015-11-02 11:18:42'})
        self.assertEqual(response.status_code, 401)

    def test_patch_movie_casting_assistant(self):
        response = self.client.patch(
            '/movies/1',
            headers=casting_assistant_auth_header,
            json={
                'title': 'Test',
                'release_date': '2015-11-02 11:18:42'})
        self.assertEqual(response.status_code, 403)

    def test_patch_movie_casting_director(self):
        response = self.client.patch(
            '/movies/1',
            headers=casting_director_auth_header,
            json={
                'title': 'Test',
                'release_date': '2015-11-02 11:18:42'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_executive_producer(self):
        response = self.client.patch(
            '/movies/1',
            headers=executive_producer_auth_header,
            json={
                'title': 'Test',
                'release_date': '2015-11-02 11:18:42'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_fail(self):
        response = self.client.patch('/movies/1', headers={}, json={
            'title': 'Test',
            'release_date': '2015-11-02 11:18:42'})
        self.assertEqual(response.status_code, 401)

    def test_delete_movie_casting_assistant(self):
        response = self.client.delete(
            '/movies/1', headers=casting_assistant_auth_header)
        self.assertEqual(response.status_code, 403)

    
    def test_delete_movie_casting_director(self):
        response = self.client.delete(
            '/movies/1', headers=casting_director_auth_header)
        self.assertEqual(response.status_code, 403)

    def test_delete_movie_xecutive_producer(self):
        response = self.client.delete(
            '/movies/1', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_fail(self):
        response = self.client.delete('/movies/1', headers={})
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()