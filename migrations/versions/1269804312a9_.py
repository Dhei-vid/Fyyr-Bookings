"""empty message

Revision ID: 1269804312a9
Revises: ffdbd056017b
Create Date: 2022-08-08 09:00:58.979087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1269804312a9'
down_revision = 'ffdbd056017b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', sa.Column('looking_for_talent', sa.Boolean(), nullable=True))
    op.alter_column('Venue', sa.Column('looking_for_talent', sa.Boolean(), nullable=True))
    # op.alter_column('Artist', 'looking_for_talent', sa.Boolean(), nullable=True)
    # op.alter_column('Venue', sa.Column('looking_for_talent', sa.Boolean(), nullable=True))
    # op.drop_column('Venue', 'lookingForTalent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('lookingForTalent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'looking_for_talent')
    op.add_column('Artist', sa.Column('lookingForTalent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'looking_for_talent')
    # ### end Alembic commands ###
