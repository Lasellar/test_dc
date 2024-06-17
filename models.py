from sqlalchemy import (
    Column,
    Integer, String, Boolean, DateTime,
    ForeignKey, create_engine
)
from sqlalchemy.orm import (
    relationship,
    declarative_base,
    sessionmaker
)

database = declarative_base()


class User(database):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    url = Column(String)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_premium = Column(Boolean)
    language_code = Column(String)
    messages = relationship('Message', backref='user')

    def __repr__(self):
        return (
            f'User('
            f'user_id={self.user_id}, '
            f'url={self.url}, '
            f'username={self.username}, '
            f'first_name={self.first_name}, '
            f'last_name={self.last_name}, '
            f'is_premium={self.is_premium}, '
            f'language_code={self.language_code}'
            f')'
        )


class Message(database):
    __tablename__ = 'messages'

    user_id = Column(Integer, ForeignKey('users.user_id'))
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    text = Column(String)
    sticker = Column(String)
    photo = Column(String)
    video = Column(String)
    voice = Column(String)

    def __repr__(self):
        return (
            f'Message('
            f'user_id={self.user_id}, '
            f'id={self.id}, '
            f'date={self.date}, '
            f'text={self.text}, '
            f'stcker={self.stcker}, '
            f'photo={self.photo}, '
            f'video={self.video}, '
            f'voice={self.voice}'
            f')'
        )


engine = create_engine('sqlite:///db.db')
database.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
