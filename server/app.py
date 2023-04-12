#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Researches(Resource):
    def get(self):
        researches = [r.to_dict() for r in Research.query.all()]
        return make_response(researches, 201)

api.add_resource(Researches, '/researches')

class ResearchId(Resource):
    def get(self, id):
        research = Research.query.filter_by(id=id).first()
        if research ==None:
            return make_response({'error': 'research paper not found'}, 400)

        research_dict = research.to_dict(only = ('id', 'topic', 'year', 'page_count', 'author'))
        return make_response(research_dict, 201)

    def delete(self, id):

        research = Research.query.filter_by(id=id).first()
        if research ==None:
            return make_response({'error': 'research paper not found'}, 400)

        for ra in ResearchAuthors.query.all():
            if ra.research_id == id:
                db.session.delete(ra)
                db.session.commit()
        
        db.session.delete(research)
        db.session.commit()

        return make_response({}, 200)

api.add_resource(ResearchId, '/researches/<int:id>')

class Authors(Resource):
    def get(self):
        authors = [a.to_dict() for a in Author.query.all()]
        return make_response(authors, 201)

api.add_resource(Authors, '/authors')

class ResearchAuthor(Resource):
    def get(self):
        ras= [ra.to_dict() for ra in ResearchAuthors.query.all()]
        return make_response(ras, 201)
    def post(self):
        data = request.get_json()

        try:
            new_ra = ResearchAuthors(author_id = data['author_id'], research_id = data['research_id'])
            db.session.add(new_ra)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response({'errors':['validation errors']}, 400)

        return make_response(new_ra.author.to_dict(), 200)
api.add_resource(ResearchAuthor, '/researchauthor')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
