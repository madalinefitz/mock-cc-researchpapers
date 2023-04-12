#!/usr/bin/env python3
from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Research, Author, ResearchAuthors

with app.app_context():

# This will delete any existing rows
# so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Research.query.delete()
    Author.query.delete()
    ResearchAuthors.query.delete()

    print("Creating Research...")
    r1 = Research(topic = "AI In Day To Day Life", year = 1994, page_count = 10)
    r2 = Research(topic = "Robotics, A Case Study", year = 2010, page_count = 100)
    r3 = Research(topic = "Methods of Training Data", year = 2020, page_count = 1000)
    research_papers = [r1, r2, r3]

    print("Creating Author...")


    a1 = Author(name = "Billy", field_of_study = "AI")
    a2 = Author(name = "Ted", field_of_study = "Robotics")
    a3 = Author(name = "Bob", field_of_study = "Cybersecurity")
    authors = [a1, a2, a3]

    print("Creating ResearchAuthors...")

    ra1 = ResearchAuthors(author_id = 1, research_id = 1)
    ra2 = ResearchAuthors(author_id = 2, research_id  = 2)
    ra3 = ResearchAuthors(author_id = 3, research_id = 3)
    ra4 = ResearchAuthors(author_id = 1, research_id = 3)
    researchAuthor = [ra1, ra2, ra3, ra4]
    db.session.add_all(research_papers)
    db.session.add_all(authors)
    db.session.add_all(researchAuthor)
    db.session.commit()

    print("Seeding done!")