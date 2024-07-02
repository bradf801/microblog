"""private messages

Revision ID: 8147f8c9c849
Revises: 0bfe9d903b51
Create Date: 2024-07-02 09:48:45.380201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8147f8c9c849'
down_revision = '0bfe9d903b51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_message_recipient_id'), ['recipient_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_sender_id'), ['sender_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_timestamp'), ['timestamp'], unique=False)

    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Float(), nullable=False),
    sa.Column('payload_json', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_notification_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_notification_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_notification_user_id'), ['user_id'], unique=False)

    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('complete', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_task_name'), ['name'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_message_read_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('token', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('token_expiration', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_column('token_expiration')
        batch_op.drop_column('token')
        batch_op.drop_column('last_message_read_time')

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_task_name'))

    op.drop_table('task')
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_notification_user_id'))
        batch_op.drop_index(batch_op.f('ix_notification_timestamp'))
        batch_op.drop_index(batch_op.f('ix_notification_name'))

    op.drop_table('notification')
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_timestamp'))
        batch_op.drop_index(batch_op.f('ix_message_sender_id'))
        batch_op.drop_index(batch_op.f('ix_message_recipient_id'))

    op.drop_table('message')
    # ### end Alembic commands ###
