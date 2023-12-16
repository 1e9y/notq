from sqlalchemy import Boolean, ForeignKey, MetaData, Table, Column, Integer, Float, String, DateTime, UniqueConstraint, func, Index

db_metadata = MetaData()

user_table = Table('notquser', db_metadata, 
                   Column('id', Integer, primary_key=True),
                   Column('username', String, unique=True, nullable=False),
                   Column('password', String, nullable=False),
                   Column('created', DateTime(), server_default=func.now()),
                   Column('about', String),
                   Column('is_golden', Boolean, nullable=False, default=False),
                   Column('is_moderator', Boolean, nullable=False, default=False),
                   Column('banned_until', DateTime()),
                   Column('about_post_id', Integer, ForeignKey('post.id'))
                   )
Index("idx_user_name", user_table.c.username)

post_table = Table('post', db_metadata,
                   Column('id', Integer, primary_key=True),
                   Column('author_id', Integer, ForeignKey('notquser.id'), nullable=False),
                   Column('created', DateTime(), server_default=func.now()),
                   Column('edited', DateTime()),
                   Column('title', String, nullable=False),
                   Column('body', String, nullable=False),
                   Column('rendered', String, nullable=False),
                   Column('cut_rendered', String),
                   Column('anon', Boolean),
                   Column('show_in_feed', Boolean, nullable=False, default=True),
                   Column('edited_by_moderator', Boolean),
                   )
Index("idx_post_created", post_table.c.created)
Index("idx_post_author", post_table.c.author_id)

vote_table = Table('vote', db_metadata,
                   Column('user_id', Integer, ForeignKey('notquser.id'), nullable=False),
                   Column('post_id', Integer, ForeignKey('post.id'), nullable=False),
                   Column('vote', Integer, nullable=False),
                   Column('weighted_vote', Integer, nullable=False),
                   Column('karma_vote', Float, nullable=False),
                   UniqueConstraint("user_id", "post_id")
                   )

comment_table = Table('comment', db_metadata,
                   Column('id', Integer, primary_key=True),
                   Column('author_id', Integer, ForeignKey('notquser.id'), nullable=False),
                   Column('created', DateTime(), server_default=func.now()),
                   Column('edited', DateTime()),
                   Column('body', String, nullable=False),
                   Column('rendered', String, nullable=False),
                   Column('post_id', Integer, ForeignKey('post.id'), nullable=False),
                   Column('parent_id', Integer),
                   Column('anon', Boolean),
                   Column('edited_by_moderator', Boolean),
                   Column('linked_post_id', Integer, ForeignKey('post.id')),
                )
Index("idx_comment_post", comment_table.c.post_id)
Index("idx_comment_author", post_table.c.author_id)

commentvote_table = Table('commentvote', db_metadata,
                        Column('user_id', Integer, ForeignKey('notquser.id'), nullable=False),
                        Column('post_id', Integer, ForeignKey('post.id'), nullable=False),
                        Column('comment_id', Integer, ForeignKey('comment.id'), nullable=False),
                        Column('vote', Integer, nullable=False),
                        Column('weighted_vote', Integer, nullable=False),
                        Column('karma_vote', Float, nullable=False),
                        UniqueConstraint("user_id", "post_id", "comment_id")
                    )
Index("idx_commentvote_post", commentvote_table.c.post_id)

tag_table = Table('tag', db_metadata,
                Column('id', Integer, primary_key=True),
                Column('tagname', String, unique=True, nullable=False)
            )
Index('idx_tag_name', tag_table.c.tagname)

posttag_table = Table('posttag', db_metadata,
                    Column('tag_id', Integer, ForeignKey('tag.id'), nullable=False),
                    Column('post_id', Integer, ForeignKey('post.id'), nullable=False),
                    UniqueConstraint("tag_id", "post_id")
                )
Index('idx_posttag_tag', posttag_table.c.tag_id)