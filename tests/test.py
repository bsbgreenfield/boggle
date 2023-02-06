from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def test_root_view(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)
            play_resp = client.get('/play')
            html = play_resp.get_data(as_text=True)
            self.assertEqual(play_resp.status_code, 200)
            self.assertIn('<label for="guess">Type a word!</label>', html)
            self.assertIsInstance(session['game_board'], list)

            post_resp = client.post('/play', json={'guess': 'kjds'})
            self.assertEqual(post_resp.status_code, 200)
            self.assertEqual(b'{\n  "guess": "kjds",\n  "status": "not-word"\n}\n',post_resp.data)


            


