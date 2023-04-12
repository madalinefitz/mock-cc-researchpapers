from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Research(db.Model, SerializerMixin):
    __tablename__ = 'researches'

    serialize_rules = ( '-researchauthors', '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('year')
    def year_validation(self, key, year):
        length = len(str(year))
        if length == 4:
            return year
        else:
            raise ValueError('Validation Error: must be valid year')

    researchauthors = db.relationship('ResearchAuthors', back_populates = 'research')
    author = association_proxy('researchauthors', 'author')

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ( '-researchauthors', '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('field_of_study')
    def fos_validation(self, key, field_of_study):
        options = ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']

        for o in options:
            if field_of_study == o :
                return field_of_study
        else:
            raise ValueError('Validation Error: must be valid field of study')

    researchauthors = db.relationship('ResearchAuthors', back_populates = 'author')
    research = association_proxy('researchauthors', 'research')


class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    serialize_rules = ( '-research', '-author' )

    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author = db.relationship('Author', back_populates = 'researchauthors')
    research = db.relationship('Research', back_populates = 'researchauthors')