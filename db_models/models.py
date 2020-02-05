from sqlalchemy import Table, MetaData, Column, Integer, Binary, BigInteger, DECIMAL, REAL, String, DateTime, Boolean, \
    ForeignKey, Date, TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, or_, inspect, JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB

from .base_model import BaseTable, EmailType

Base = declarative_base()


class Users(Base, BaseTable):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BaseTable.__init__(self)

    nick = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    birthday = Column(Date, nullable=True)
    bio_gender_id = Column(ForeignKey('bio_genders.id'), index=True, nullable=False)
    bio_gender = relationship("BioGenders", uselist=False, lazy='joined')
    psy_gender_id = Column(ForeignKey('psy_genders.id'), index=True, nullable=True)
    psy_gender = relationship("PsyGenders", uselist=False, lazy='joined')
    email_id = Column(ForeignKey('users_emails.id'), index=True, nullable=True)
    email = relationship("UsersEmails", uselist=False, lazy='joined')
    phone_id = Column(ForeignKey('users_phones.id'), index=True, nullable=True)
    phone = relationship("UsersPhones", uselist=False, lazy='joined')
    social = relationship("UsersSocial", uselist=True, lazy='joined')
    avatar_id = Column(ForeignKey('users_photos.id'), index=True, nullable=True)
    avatar = relationship("UsersPhotos", uselist=False, lazy='joined')
    friends = relationship("Friends", uselist=True, lazy='joined')


class Friends (Base, BaseTable):
    __tablename__ = 'friends'
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    friend_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    friend = relationship("Users", uselist=False, foreign_keys=friend_id,  lazy='joined')
    tags = relationship("TagsFriends", uselist=True, lazy='joined')


class UsersTags(Base, BaseTable):
    __tablename__ = 'users_tags'

    name = Column(String, nullable=False)
    color = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)


class TagsFriends (Base):
    __tablename__ = 'tags_friends'
    id = Column(Integer, unique=True, index=True,
                primary_key=True, nullable=False)
    friend_id = Column(ForeignKey('friends.id'), index=True, nullable=False)
    tag_id = Column(ForeignKey('users_tags.id'), index=True, nullable=False)


class BioGenders(Base):
    __tablename__ = 'bio_genders'
    id = Column(Integer, unique=True, index=True,
                primary_key=True, nullable=False)
    gender = Column(String, nullable=False)


class PsyGenders(Base):
    __tablename__ = 'psy_genders'
    id = Column(Integer, unique=True, index=True,
                primary_key=True, nullable=False)
    gender = Column(String, nullable=False)
    description = Column(String, nullable=True)
    color = Column(String, unique=True, nullable=False)


class UsersEmails(Base, BaseTable):
    __tablename__ = 'users_emails'
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    email = Column(String, nullable=False)


class UsersPhones(Base, BaseTable):
    __tablename__ = 'users_phones'
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    phone = Column(String, nullable=False)


class UsersSocial(Base, BaseTable):
    __tablename__ = 'users_social'
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    link = Column(String, nullable=False)


class UsersPhotos(Base, BaseTable):
    __tablename__ = 'users_photos'
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    photo_path = Column(String, nullable=False)


class Exercises(Base, BaseTable):
    __tablename__ = 'exercises'
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    photos = relationship("ExercisesPhotos", uselist=True, lazy='joined')
    videos = relationship("ExercisesVideos", uselist=True, lazy='joined')
    tags = relationship("ExercisesTags", uselist=True, lazy='joined')


class ExercisesPhotos(Base, BaseTable):
    __tablename__ = 'exercises_photos'
    exercise_id = Column(ForeignKey('exercises.id'), index=True, nullable=False)
    photo_path = Column(String, nullable=False)


class ExercisesVideos(Base, BaseTable):
    __tablename__ = 'exercises_videos'
    exercise_id = Column(ForeignKey('exercises.id'), index=True, nullable=False)
    video_path = Column(String, nullable=False)


class ExercisesTags (Base):
    __tablename__ = 'exercises_tags'
    id = Column(Integer, unique=True, index=True,
                primary_key=True, nullable=False)
    exercise_id = Column(ForeignKey('exercises.id'), index=True, nullable=False)
    tag_id = Column(ForeignKey('sport_tags.id'), index=True, nullable=False)


class SportTags(Base, BaseTable):
    __tablename__ = 'sport_tags'
    name = Column(String, nullable=False)
    color = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)


class Trainings(Base, BaseTable):
    __tablename__ = 'trainings'
    start_date = Column(DateTime, nullable=False)
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    helpers = relationship("Helpers", uselist=True, lazy='joined')
    participants = relationship("Participants", uselist=True, lazy='joined')
    rounds = relationship("Rounds", uselist=True, lazy='joined')


class Helpers(Base):
    __tablename__ = 'helpers'
    id = Column(Integer, unique=True, index=True,
                primary_key=True, nullable=False)
    training_id = Column(ForeignKey('trainings.id'), index=True, nullable=False)
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)


class Participants(Base, BaseTable):
    __tablename__ = 'participants'
    training_id = Column(ForeignKey('trainings.id'), index=True, nullable=False)
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    will = Column(Boolean, default=False)
    do = Column(Boolean, default=False)


class Rounds(Base, BaseTable):
    __tablename__ = 'rounds'
    number = Column(Integer, index=True, nullable=False)
    training_id = Column(ForeignKey('trainings.id'), index=True, nullable=False)
    exercises = relationship("ExercisesList", uselist=True, lazy='joined')
    timer = Column(TIME, nullable=True)


class ExercisesList(Base, BaseTable):
    __tablename__ = 'exercises_list'
    exercise_id = Column(ForeignKey('exercises.id'), index=True, nullable=False)
    round_id = Column(ForeignKey('rounds.id'), index=True, nullable=False)
    params = relationship("ParamsList", uselist=True, lazy='joined')
    users_results = relationship("UsersResults", uselist=True, lazy='joined')


class ParamsList(Base, BaseTable):
    __tablename__ = 'params_list'
    exercises_list_id = Column(ForeignKey('exercises_list.id'), index=True, nullable=False)
    timer = Column(TIME, nullable=True)
    iterations = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    other = Column(String, nullable=True)


class UsersResults(Base, BaseTable):
    __tablename__ = 'users_results'
    exercises_list_id = Column(ForeignKey('exercises_list.id'), index=True, nullable=False)
    user_id = Column(ForeignKey('users.id'), index=True, nullable=False)
    timer = Column(TIME, nullable=True)
    iterations = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    other = Column(String, nullable=True)


class Accounts(BaseTable, Base):
    __tablename__ = 'accounts'
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    user = relationship("Users", uselist=False, lazy='joined')
    password = Column(String, nullable=False)
