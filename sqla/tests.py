import unittest
from flask import Flask
from flask_testing import TestCase
from models import Post, User, Tag

# Import your Flask app
from app import app, db, User, Tag, Post

# Define a test case
class AppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_test'
        return app
    
    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_home_page_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/users')

    def test_users_index(self):
        # Create some sample users
        user1 = User(first_name='Jon', last_name='Doe', image_url=None)
        user2 = User(first_name='Jill', last_name='Smith', image_url=None)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        response = self.client.get('/users')
        self.assert200(response)
        self.assertIn(b'Jon Doe', response.data)
        self.assertIn(b'Jill Smith', response.data)
    
    def test_new_user_form(self):
        response = self.client.get('/users/new')
        self.assert200(response)
        self.assertIn(b'New User', response.data)
    
    def test_new_user(self):
        # Simulate form data
        form_data = {
            'first_name': 'Jon',
            'last_name': 'Doe',
            'image_url': 'http://example.com/image.jpg'
        }
        
        response = self.client.post('/users/new', data=form_data, follow_redirects=True)
        self.assertRedirects(response, '/users')
        
        # Check if the user was added to the database
        users = User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].first_name, 'Jon')
        self.assertEqual(users[0].last_name, 'Doe')
        self.assertEqual(users[0].image_url, 'http://example.com/image.jpg')

class AppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_test'
        return app
    
    def setUp(self):
        db.create_all()
        
        # Create a sample post
        post = Post(title='Test Post', content='Lorem ipsum dolor sit amet.')
        db.session.add(post)
        db.session.commit()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_show_posts(self):
        response = self.client.get('/posts/1')
        self.assert200(response)
        self.assertIn(b'Test Post', response.data)
        self.assertIn(b'Lorem ipsum dolor sit amet.', response.data)
    
    def test_edit_post(self):
        response = self.client.get('/posts/1/edit')
        self.assert200(response)
        self.assertIn(b'Edit Post', response.data)
        self.assertIn(b'Test Post', response.data)
        self.assertIn(b'Lorem ipsum dolor sit amet.', response.data)


class AppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app
    
    def setUp(self):
        db.create_all()
        
        # Create some sample tags
        tag1 = Tag(name='Tag 1')
        tag2 = Tag(name='Tag 2')
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.commit()
        
        # Create some sample posts
        post1 = Post(title='Post 1', content='Lorem ipsum dolor sit amet.')
        post2 = Post(title='Post 2', content='Lorem ipsum dolor sit amet.')
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_index_tags(self):
        response = self.client.get('/tags')
        self.assert200(response)
        self.assertIn(b'Tag 1', response.data)
        self.assertIn(b'Tag 2', response.data)
    
    def test_tags_new_form(self):
        response = self.client.get('/tags/new')
        self.assert200(response)
        self.assertIn(b'New Tag', response.data)
        self.assertIn(b'Post 1', response.data)
        self.assertIn(b'Post 2', response.data)

# Run the tests
if __name__ == '__main__':
    unittest.main()
